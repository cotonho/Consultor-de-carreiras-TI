"""Testes de robustez e casos-limite (Fase 5).

Cobre perfis ambigos, empates parciais, respostas minimas/maximas e vazias,
e garante que o motor SEMPRE retorna uma recomendacao.

Execucao:  py -3.11 -m tests.edge_cases
"""

from src.knowledge import BaseConhecimento
from src.motor import MotorPonderado
from src.recomendacoes import analisar_gaps, gerar_roadmap

KB = BaseConhecimento.carregar()
MOTOR = MotorPonderado(KB)

BASE = {
    "experiencia": "estudante",
    "conhecimentos": [],
    "logica_algoritmos": 3,
    "matematica_estatistica": 3,
    "design_visual": 3,
    "infraestrutura": 3,
    "dados_analise": 3,
    "seguranca": 3,
    "automacao_qualidade": 3,
    "gestao_lideranca": 3,
    "mobile_apps": 3,
    "comunicacao_pessoas": 3,
    "preferencia_diaria": "algoritmos",
    "linguagem": "python",
    "entrega_valor": "usuario_final",
    "aspecto_tecnico": "arquitetura",
}

TESTES = []


def teste(nome):
    def decorador(fn):
        TESTES.append((nome, fn))
        return fn
    return decorador


@teste("perfil totalmente neutro (tudo 3) ainda recomenda algo")
def _():
    r = MOTOR.diagnosticar(dict(BASE))
    assert r["recomendacao"] is not None, "recomendacao nula em perfil neutro"
    assert len(r["top3"]) == 3
    assert all(0 <= t["compatibilidade"] <= 100 for t in r["top3"])


@teste("respostas minimas (tudo 1) nao quebra e recomenda")
def _():
    respostas = dict(BASE)
    for k in ["logica_algoritmos","matematica_estatistica","design_visual","infraestrutura",
              "dados_analise","seguranca","automacao_qualidade","gestao_lideranca",
              "mobile_apps","comunicacao_pessoas"]:
        respostas[k] = 1
    r = MOTOR.diagnosticar(respostas)
    assert r["recomendacao"] is not None


@teste("respostas maximas (tudo 5) nao quebra e recomenda")
def _():
    respostas = dict(BASE)
    for k in ["logica_algoritmos","matematica_estatistica","design_visual","infraestrutura",
              "dados_analise","seguranca","automacao_qualidade","gestao_lideranca",
              "mobile_apps","comunicacao_pessoas"]:
        respostas[k] = 5
    r = MOTOR.diagnosticar(respostas)
    assert r["recomendacao"] is not None


@teste("dicionario vazio nao quebra (motor usa defaults)")
def _():
    r = MOTOR.diagnosticar({})
    assert r["recomendacao"] is not None, "recomendacao nula com respostas vazias"


@teste("respostas parciais (só afinidades) ainda recomenda")
def _():
    parcial = {k: BASE[k] for k in BASE if k in
               ["logica_algoritmos","matematica_estatistica","design_visual","infraestrutura",
                "dados_analise","seguranca","automacao_qualidade","gestao_lideranca",
                "mobile_apps","comunicacao_pessoas"]}
    r = MOTOR.diagnosticar(parcial)
    assert r["recomendacao"] is not None


@teste("perfil ambiguo (dados + web) retorna top3 coerente com ambos")
def _():
    # alguem que gosta igualmente de dados e de criar interfaces
    respostas = dict(BASE)
    respostas.update({
        "logica_algoritmos": 4, "matematica_estatistica": 4, "design_visual": 4,
        "dados_analise": 4, "preferencia_diaria": "dados_brutos",
        "linguagem": "python", "entrega_valor": "dados_insights",
        "aspecto_tecnico": "descoberta",
    })
    r = MOTOR.diagnosticar(respostas)
    top3_ids = [t["trilha"] for t in r["top3"]]
    assert "ciencia_dados" in top3_ids or "front" in top3_ids, "ambiguidade nao refletida no top3"
    # diferencas parciais: 1º e 2º relativamente proximos
    dif = abs(r["top3"][0]["compatibilidade"] - r["top3"][1]["compatibilidade"])
    assert dif <= 30, f"gap grande demais entre 1º e 2º em perfil ambiguo ({dif}%)"


@teste("empate exato: desempate deterministico (mesma resposta = mesmo vencedor)")
def _():
    respostas = dict(BASE)
    r1 = MOTOR.diagnosticar(respostas)
    r2 = MOTOR.diagnosticar(dict(respostas))
    assert r1["recomendacao"]["trilha"] == r2["recomendacao"]["trilha"]


@teste("percentuais sempre entre 0 e 100")
def _():
    r = MOTOR.diagnosticar(dict(BASE))
    for t, v in r["compatibilidade"].items():
        assert 0 <= v <= 100, f"{t} = {v}% fora da faixa"


@teste("gaps: sem conhecimentos = todas as lacunas, roadmap prioriza lacunas")
def _():
    r = MOTOR.diagnosticar(dict(BASE))
    trilha = r["recomendacao"]["trilha"]
    gaps = analisar_gaps(KB, trilha, [])
    assert gaps["pronto_percentual"] == 0
    assert len(gaps["faltantes"]) == len(gaps["requeridos"])
    roadmap = gerar_roadmap(KB, trilha, gaps)
    assert roadmap["estudar_primeiro"], "roadmap vazio sem conhecimentos"


@teste("gaps: todos os conhecimentos = 100% e nenhum prioritario")
def _():
    r = MOTOR.diagnosticar(dict(BASE))
    trilha = r["recomendacao"]["trilha"]
    requeridos = KB.trilhas[trilha].nivel_junior_requerido
    gaps = analisar_gaps(KB, trilha, requeridos)
    assert gaps["pronto_percentual"] == 100
    assert gaps["pronto_para_junior"]
    roadmap = gerar_roadmap(KB, trilha, gaps)
    assert not roadmap["estudar_primeiro"]


@teste("conhecimento desconhecido no input e ignorado com seguranca")
def _():
    r = MOTOR.diagnosticar({**BASE, "conhecimentos": ["logica", "coisa_inexistente"]})
    assert r["recomendacao"] is not None


def rodar() -> int:
    falhas = 0
    for nome, fn in TESTES:
        try:
            fn()
            print(f"[OK ] {nome}")
        except AssertionError as e:
            falhas += 1
            print(f"[FALHOU] {nome}: {e}")
    total = len(TESTES)
    print(f"\nResultado: {total - falhas}/{total} testes de robustez")
    return 0 if falhas == 0 else 1


if __name__ == "__main__":
    raise SystemExit(rodar())
