"""Modulo de recomendacao: analise de skill gaps e roadmap personalizado.

Cruza a trilha vencedora com o conhecimento atual do usuario para listar o
que falta para o nivel Junior e gerar um plano de estudo ordenado por
prioridade (o que preenche gap vem primeiro).
"""

from __future__ import annotations

from .knowledge import BaseConhecimento


def analisar_gaps(
    kb: BaseConhecimento, trilha_id: str, conhecimentos: list[str] | set[str] | None
) -> dict:
    """Compara o conhecimento atual com o requerido para Júnior na trilha."""
    conhecidos = set(conhecimentos or [])
    requeridos = kb.trilhas[trilha_id].nivel_junior_requerido
    dominados = [k for k in requeridos if k in conhecidos]
    faltantes = [k for k in requeridos if k not in conhecidos]
    pronto_pct = round(100 * len(dominados) / len(requeridos)) if requeridos else 100
    return {
        "trilha": trilha_id,
        "requeridos": requeridos,
        "dominados": dominados,
        "faltantes": faltantes,
        "pronto_percentual": pronto_pct,
        "pronto_para_junior": not faltantes,
        "rotulos": {k: kb.conhecimentos.get(k, {}).get("nome", k) for k in requeridos},
    }


def gerar_roadmap(kb: BaseConhecimento, trilha_id: str, gaps: dict) -> dict:
    """Plano de acao: itens que preenchem gaps primeiro, depois complementares."""
    rm = kb.trilhas[trilha_id].roadmap
    faltantes = set(gaps.get("faltantes", []))
    prioritarios = [i for i in rm["estudar_primeiro"] if i.preenche in faltantes]
    complementares = [i for i in rm["estudar_primeiro"] if i.preenche not in faltantes]
    return {
        "trilha": trilha_id,
        "estudar_primeiro": prioritarios,
        "complementar": complementares,
        "certificacoes": rm["certificacoes"],
        "projetos_portfolio": rm["projetos_portfolio"],
    }


def plano_de_acao(kb: BaseConhecimento, trilha_id: str, conhecimentos: list[str] | None) -> dict:
    """Gera gaps + roadmap de uma vez para a trilha indicada."""
    gaps = analisar_gaps(kb, trilha_id, conhecimentos)
    roadmap = gerar_roadmap(kb, trilha_id, gaps)
    return {"gaps": gaps, "roadmap": roadmap}
