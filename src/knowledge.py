"""Carregamento dinamico da Base de Conhecimento (arquivo JSON externo)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

CAMINHO_PADRAO = Path(__file__).resolve().parent.parent / "knowledge" / "regras_carreiras.json"


@dataclass
class Pergunta:
    id: str
    etapa: str
    tipo: str  # likert | selecao | multi
    titulo: str
    descricao: str = ""
    min: int | None = None
    max: int | None = None
    rotulos: dict = field(default_factory=dict)
    pesos: dict = field(default_factory=dict)  # likert: trilha -> peso por ponto
    opcoes: dict = field(default_factory=dict)  # selecao: opcao_id -> rotulo
    pesos_por_opcao: dict = field(default_factory=dict)  # selecao: opcao_id -> {trilha: peso}


@dataclass
class Regra:
    id: str
    descricao: str
    condicoes: dict
    efeito: dict  # trilha -> pontos (positivos = bonus, negativos = penalidade)


@dataclass
class RoadmapItem:
    item: str
    preenche: str  # id do conhecimento


@dataclass
class Trilha:
    id: str
    nome: str
    descricao: str
    nivel_junior_requerido: list[str]
    roadmap: dict  # estudar_primeiro: list[RoadmapItem], certificacoes: list[str], projetos_portfolio: list[str]


class BaseConhecimento:
    """Base de conhecimento carregada do JSON (desacoplada do motor)."""

    def __init__(self, dados: dict):
        self.versao = dados.get("versao", "?")
        self.descricao = dados.get("descricao", "")
        self.conhecimentos: dict[str, dict] = dados.get("conhecimentos", {})
        self.perguntas: list[Pergunta] = [Pergunta(**p) for p in dados.get("perguntas", [])]
        self.regras: list[Regra] = [Regra(**r) for r in dados.get("regras", [])]
        self.penalidades: list[Regra] = [Regra(**r) for r in dados.get("penalidades", [])]

        self.trilhas: dict[str, Trilha] = {}
        for tid, t in dados.get("trilhas", {}).items():
            rm = t.get("roadmap", {})
            self.trilhas[tid] = Trilha(
                id=tid,
                nome=t["nome"],
                descricao=t["descricao"],
                nivel_junior_requerido=t.get("nivel_junior_requerido", []),
                roadmap={
                    "estudar_primeiro": [RoadmapItem(**i) for i in rm.get("estudar_primeiro", [])],
                    "certificacoes": rm.get("certificacoes", []),
                    "projetos_portfolio": rm.get("projetos_portfolio", []),
                },
            )

        self.ordem_trilhas: list[str] = list(self.trilhas.keys())

    @classmethod
    def carregar(cls, caminho: str | Path = CAMINHO_PADRAO) -> "BaseConhecimento":
        caminho = Path(caminho)
        if not caminho.exists():
            raise FileNotFoundError(f"Base de conhecimento nao encontrada: {caminho}")
        with open(caminho, encoding="utf-8-sig") as f:
            return cls(json.load(f))

    def perguntas_da_etapa(self, etapa: str) -> list[Pergunta]:
        return [p for p in self.perguntas if p.etapa == etapa]

    def categorias_conhecimentos(self) -> dict[str, list[tuple[str, str]]]:
        """Agrupa conhecimentos por categoria: {categoria: [(id, nome), ...]}."""
        cats: dict[str, list[tuple[str, str]]] = {}
        for cid, c in sorted(self.conhecimentos.items()):
            cats.setdefault(c["categoria"], []).append((cid, c["nome"]))
        return cats
