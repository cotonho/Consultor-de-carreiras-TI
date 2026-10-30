"""Motor de inferencia com pontuacao ponderada e tratamento de incerteza.

Le a Base de Conhecimento (JSON), processa respostas graduais (Likert 1-5 e
selecoes), aplica regras bonus e penalidades logicas, e calcula uma matriz de
compatibilidade percentual com ranking multi-trilha (Top 3).

A cada resposta, o valor (1..5 ou opcao escolhida) multiplica o peso da
pergunta/trilha correspondente; regras SE-ENTAO avaliam combinacoes de
respostas e somam bonus ou penalidades. O placar final e normalizado pela
pontuacao maxima possivel de cada trilha (0-100%).
"""

from __future__ import annotations

from .knowledge import BaseConhecimento, Regra


class MotorPonderado:
    def __init__(self, kb: BaseConhecimento | None = None):
        self.kb = kb or BaseConhecimento.carregar()
        self._maximo_possivel = self._calcular_maximos()

    # ------------------------------------------------------------------
    # Regras e normalizacao
    # ------------------------------------------------------------------

    def _condicao_atendida(self, cond: dict, respostas: dict) -> bool:
        """Avalia uma condicao: igualdade, faixa {min}/{max} ou lista de opcoes."""
        for atributo, esperado in cond.items():
            valor = respostas.get(atributo)
            if isinstance(esperado, dict):
                if valor is None:
                    return False
                if "min" in esperado and valor < esperado["min"]:
                    return False
                if "max" in esperado and valor > esperado["max"]:
                    return False
            elif isinstance(esperado, list):
                if valor not in esperado:
                    return False
            else:
                if valor != esperado:
                    return False
        return True

    def _calcular_maximos(self) -> dict[str, float]:
        """Pontuacao maxima (100%) de cada trilha (resposta perfeita no perfil)."""
        maximos: dict[str, float] = {t: 0.0 for t in self.kb.trilhas}
        for p in self.kb.perguntas:
            if p.tipo == "likert":
                for trilha, peso in p.pesos.items():
                    maximos[trilha] += (p.max or 5) * peso
            elif p.tipo == "selecao":
                # selecao contribui uma unica vez: vale a melhor opcao possivel
                for trilha in maximos:
                    melhor = max(
                        (pesos.get(trilha, 0) for pesos in p.pesos_por_opcao.values()),
                        default=0,
                    )
                    maximos[trilha] += melhor
        for r in self.kb.regras:
            for trilha, valor in r.efeito.items():
                if valor > 0:
                    maximos[trilha] += valor
        # garante pelo menos 1 para evitar divisao por zero
        return {t: max(v, 1.0) for t, v in maximos.items()}

    # ------------------------------------------------------------------
    # Diagnostico
    # ------------------------------------------------------------------

    def diagnosticar(self, respostas: dict) -> dict:
        """Calcula o ranking de compatibilidade. Sempre retorna uma recomendacao."""
        placar: dict[str, float] = {t: 0.0 for t in self.kb.trilhas}
        contribuicoes: dict[str, list[dict]] = {t: [] for t in self.kb.trilhas}
        justificativas: list[dict] = []

        # 1) Pontuacao ponderada por resposta (Likert e selecoes)
        for p in self.kb.perguntas:
            valor = respostas.get(p.id)
            if p.tipo == "likert":
                if valor is None:
                    continue
                for trilha, peso in p.pesos.items():
                    pts = valor * peso
                    if pts:
                        placar[trilha] += pts
                        contribuicoes[trilha].append(
                            {
                                "origem": "afinidade",
                                "descricao": f"{p.titulo} = {valor}/5 (peso {peso}) -> +{pts}",
                                "pontos": pts,
                            }
                        )
            elif p.tipo == "selecao":
                if valor is None or valor not in p.pesos_por_opcao:
                    continue
                for trilha, peso in p.pesos_por_opcao[valor].items():
                    if peso:
                        placar[trilha] += peso
                        contribuicoes[trilha].append(
                            {
                                "origem": "objetivo",
                                "descricao": f"{p.titulo}: {p.opcoes.get(valor, valor)} -> +{peso}",
                                "pontos": peso,
                            }
                        )

        # 2) Regras bonus e penalidades (logica SE-ENTAO com fator de peso)
        regras_disparadas = self._aplicar_regras(respostas, placar, justificativas)

        # 3) Normalizacao 0-100% e ranking
        compatibilidade: dict[str, int] = {}
        for trilha, pts in placar.items():
            pct = 100.0 * pts / self._maximo_possivel[trilha]
            compatibilidade[trilha] = max(0, min(100, round(pct)))

        ordenadas = sorted(
            self.kb.trilhas.items(),
            key=lambda kv: (
                -compatibilidade[kv[0]],
                -sum(1 for r in regras_disparadas if r["trilha"] == kv[0]),
                self.kb.ordem_trilhas.index(kv[0]),
            ),
        )

        top3 = []
        for trilha, info in ordenadas[:3]:
            motivos = sorted(
                contribuicoes[trilha] + [
                    {"origem": "regra", "descricao": r["descricao"], "pontos": r["efeito"]}
                    for r in regras_disparadas
                    if r["trilha"] == trilha and r["efeito"] > 0
                ] + [
                    {"origem": "penalidade", "descricao": r["descricao"], "pontos": r["efeito"]}
                    for r in regras_disparadas
                    if r["trilha"] == trilha and r["efeito"] < 0
                ],
                key=lambda m: abs(m["pontos"]),
                reverse=True,
            )
            top3.append(
                {
                    "trilha": trilha,
                    "nome": info.nome,
                    "descricao": info.descricao,
                    "compatibilidade": compatibilidade[trilha],
                    "pontuacao": round(placar[trilha], 1),
                    "motivos": motivos,
                }
            )

        # Garantia: mesmo com empate total ou placar zero, ha uma recomendacao
        recomendado = top3[0] if top3 else None

        return {
            "recomendacao": recomendado,
            "top3": top3,
            "compatibilidade": compatibilidade,
            "placar": {t: round(v, 1) for t, v in placar.items()},
            "regras_disparadas": regras_disparadas,
            "explicacao": self._explicacao(recomendado, regras_disparadas),
        }

    def _aplicar_regras(self, respostas: dict, placar: dict, justificativas: list) -> list:
        disparadas = []
        for regra in self.kb.regras + self.kb.penalidades:
            if self._condicao_atendida(regra.condicoes, respostas):
                tipo = "bonus" if regra.id.startswith("R") else "penalidade"
                for trilha, valor in regra.efeito.items():
                    if trilha not in placar:
                        continue
                    placar[trilha] += valor
                    disparadas.append(
                        {
                            "id": regra.id,
                            "tipo": tipo,
                            "trilha": trilha,
                            "descricao": regra.descricao,
                            "efeito": valor,
                        }
                    )
        return disparadas

    def _explicacao(self, recomendado: dict | None, regras: list) -> list[str]:
        """Justificativa em frases para o usuario final."""
        if recomendado is None:
            return ["Nao foi possivel gerar diagnostico com as respostas fornecidas."]
        linhas = [
            f"Compatibilidade calculada com {recomendado['compatibilidade']}% "
            f"para {recomendado['nome']}."
        ]
        principais = [r for r in regras if r["trilha"] == recomendado["trilha"]]
        bonus = sorted([r for r in principais if r["efeito"] > 0], key=lambda r: -r["efeito"])
        pen = [r for r in principais if r["efeito"] < 0]
        for r in bonus[:3]:
            linhas.append(f"Regra {r['id']} (+{r['efeito']}): {r['descricao']}.")
        for r in pen:
            linhas.append(f"Atencao, {r['id']} ({r['efeito']}): {r['descricao']}.")
        return linhas
