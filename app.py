"""Interface web do Consultor Avancado de Carreiras em TI (wizard em etapas).

Execucao:  streamlit run app.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.knowledge import BaseConhecimento
from src.motor import MotorPonderado
from src.recomendacoes import plano_de_acao

st.set_page_config(
    page_title="Consultor Avancado de Carreiras em TI",
    page_icon="🧭",
    layout="wide",
)

ETAPAS = ["Passo 1 — Perfil pessoal", "Passo 2 — Afinidades técnicas", "Passo 3 — Objetivos de carreira", "Resultado"]


@st.cache_resource
def carregar_sistema():
    kb = BaseConhecimento.carregar()
    return kb, MotorPonderado(kb)


KB, MOTOR = carregar_sistema()


def init_state():
    st.session_state.setdefault("etapa", 0)
    st.session_state.setdefault("respostas", {})


def radar_compatibilidade(ranking_full: dict) -> go.Figure:
    trilhas = list(ranking_full.keys())
    nomes = [KB.trilhas[t].nome for t in trilhas]
    valores = [ranking_full[t] for t in trilhas]
    fig = go.Figure(
        data=go.Scatterpolar(
            r=valores + [valores[0]],
            theta=nomes + [nomes[0]],
            fill="toself",
            name="Compatibilidade",
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=420,
        margin=dict(t=30, b=30),
    )
    return fig


def barras_top3(top3: list) -> go.Figure:
    fig = go.Figure(
        go.Bar(
            x=[t["compatibilidade"] for t in top3],
            y=[t["nome"] for t in top3],
            orientation="h",
            text=[f"{t['compatibilidade']}%" for t in top3],
            textposition="auto",
            marker_color=["#2e7d32", "#ef6c00", "#6a1b9a"],
        )
    )
    fig.update_layout(
        xaxis_title="Compatibilidade (%)",
        yaxis=dict(autorange="reversed"),
        height=300,
        margin=dict(t=20, b=40),
    )
    return fig


def render_etapa_perfil():
    st.header("Passo 1 — Perfil pessoal")
    st.caption(KB.perguntas_da_etapa("perfil")[0].descricao)

    experiencia = st.radio(
        "Qual seu nível de experiência atual com programação?",
        options=list(KB.perguntas[0].opcoes.keys()),
        format_func=lambda k: KB.perguntas[0].opcoes[k],
        horizontal=True,
    )

    st.subheader("Quais conhecimentos você já possui?")
    st.caption(KB.perguntas[1].descricao)
    conhecimentos = []
    for categoria, itens in KB.categorias_conhecimentos().items():
        with st.expander(categoria, expanded=False):
            marcar = st.multiselect(
                categoria,
                options=[i[0] for i in itens],
                format_func=lambda k: dict(itens)[k],
                key=f"conc_{categoria}",
                label_visibility="collapsed",
            )
            conhecimentos.extend(marcar)

    if st.button("Avançar →", type="primary", use_container_width=True):
        st.session_state.respostas["experiencia"] = experiencia
        st.session_state.respostas["conhecimentos"] = conhecimentos
        st.session_state.etapa = 1
        st.rerun()


def render_etapa_afinidades():
    st.header("Passo 2 — Afinidades técnicas")
    st.caption("Responda de 1 (nada) a 5 (extremamente) cada dimensão.")
    respostas = {}
    perguntas = KB.perguntas_da_etapa("afinidades")
    cols = st.columns(2)
    for i, p in enumerate(perguntas):
        with cols[i % 2].st.container():
            respostas[p.id] = st.slider(
                f"{p.titulo}",
                min_value=p.min,
                max_value=p.max,
                value=st.session_state.respostas.get(p.id, 3),
                help=p.descricao,
                key=f"lik_{p.id}",
            )
    c1, c2 = st.columns(2)
    if c1.button("← Voltar"):
        st.session_state.etapa = 0
        st.rerun()
    if c2.button("Avançar →", type="primary"):
        st.session_state.respostas.update(respostas)
        st.session_state.etapa = 2
        st.rerun()


def render_etapa_objetivos():
    st.header("Passo 3 — Objetivos de carreira")
    respostas = {}
    for p in KB.perguntas_da_etapa("objetivos"):
        respostas[p.id] = st.selectbox(
            p.titulo,
            options=list(p.opcoes.keys()),
            format_func=lambda k, p=p: p.opcoes[k],
            index=list(p.opcoes.keys()).index(st.session_state.respostas.get(p.id, list(p.opcoes.keys())[0])),
            help=p.descricao,
            key=f"sel_{p.id}",
        )
    c1, c2 = st.columns(2)
    if c1.button("← Voltar"):
        st.session_state.etapa = 1
        st.rerun()
    if c2.button("🔍 Diagnosticar", type="primary"):
        st.session_state.respostas.update(respostas)
        st.session_state.resultado = MOTOR.diagnosticar(st.session_state.respostas)
        st.session_state.etapa = 3
        st.rerun()


def render_resultado():
    st.header("Resultado do diagnóstico")
    resultado = st.session_state.resultado
    rec = resultado["recomendacao"]

    if rec is None:
        st.warning("Não foi possível diagnosticar. Refaça a entrevista.")
        if st.button("Recomeçar"):
            st.session_state.etapa = 0
            st.rerun()
        return

    st.success(f"### 🎯 Trilha recomendada: {rec['nome']} — {rec['compatibilidade']}% de compatibilidade")
    st.caption(rec["descricao"])

    tab_ranking, tab_gaps, tab_plano = st.tabs(
        ["🏆 Ranking de compatibilidade", "🔍 Skill Gaps (nível Júnior)", "🗺️ Plano de ação"]
    )

    with tab_ranking:
        c1, c2 = st.columns([3, 2])
        with c1:
            st.plotly_chart(barras_top3(resultado["top3"]), use_container_width=True)
        with c2:
            st.plotly_chart(radar_compatibilidade(resultado["compatibilidade"]), use_container_width=True)

        st.subheader("Top 3 em detalhes")
        for i, t in enumerate(resultado["top3"], 1):
            with st.expander(f"{i}º {t['nome']} — {t['compatibilidade']}%", expanded=(i == 1)):
                st.write(t["descricao"])
                for m in t["motivos"][:5]:
                    sinal = "+" if m["pontos"] > 0 else ""
                    st.markdown(f"- {sinal}{m['pontos']} — {m['descricao']}")

        st.subheader("Placar completo (todas as 10 trilhas)")
        df = pd.DataFrame(
            [
                {"Trilha": KB.trilhas[t].nome, "Compatibilidade (%)": v, "Pontos": resultado["placar"][t]}
                for t, v in sorted(resultado["compatibilidade"].items(), key=lambda kv: -kv[1])
            ]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

        with st.expander("📝 Explicação do motor"):
            for linha in resultado["explicacao"]:
                st.write("• " + linha)

    with tab_gaps:
        gaps = plano_de_acao(KB, rec["trilha"], st.session_state.respostas.get("conhecimentos", []))["gaps"]
        st.subheader(f"Nível Júnior em {rec['nome']}")
        st.progress(gaps["pronto_percentual"] / 100)
        st.write(f"Você já domina **{gaps['pronto_percentual']}%** dos conhecimentos requeridos.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**✅ Você já tem:**")
            for k in gaps["dominados"]:
                st.markdown(f"- {gaps['rotulos'][k]}")
            if not gaps["dominados"]:
                st.caption("Nenhum ainda — tudo a construir.")
        with c2:
            st.markdown("**❌ Lacunas (faltantes):**")
            for k in gaps["faltantes"]:
                st.markdown(f"- {gaps['rotulos'][k]}")
            if gaps["pronto_para_junior"]:
                st.success("Nenhuma lacuna — você já cobre o básico Júnior!")

    with tab_plano:
        plano = plano_de_acao(KB, rec["trilha"], st.session_state.respostas.get("conhecimentos", []))["roadmap"]
        st.subheader("1. O que estudar primeiro (preenche suas lacunas)")
        for i in plano["estudar_primeiro"]:
            st.markdown(f"- **{i.item}**")
        if plano["complementar"]:
            with st.expander("Complementares (já são seu ponto forte)"):
                for i in plano["complementar"]:
                    st.markdown(f"- {i.item}")
        st.subheader("2. Certificações sugeridas")
        for c in plano["certificacoes"]:
            st.markdown(f"- {c}")
        st.subheader("3. Projetos para o portfólio (GitHub)")
        for p in plano["projetos_portfolio"]:
            st.markdown(f"- {p}")

    if st.button("🔄 Refazer diagnóstico", use_container_width=True):
        st.session_state.etapa = 0
        st.session_state.respostas = {}
        st.rerun()


def main():
    init_state()
    st.title("🧭 Consultor Avancado de Carreiras em TI")
    st.caption(
        "Sistema Especialista com tratamento de incerteza: respostas graduais (1-5), "
        "ranking multi-trilha em %, análise de skill gaps e roadmap personalizado."
    )

    if st.session_state.etapa < 3:
        st.progress((st.session_state.etapa + 1) / len(ETAPAS))
        st.caption(ETAPAS[st.session_state.etapa])

    renderers = [render_etapa_perfil, render_etapa_afinidades, render_etapa_objetivos, render_resultado]
    renderers[st.session_state.etapa]()


if __name__ == "__main__":
    main()
