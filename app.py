"""Interface web do Consultor Inteligente de Carreiras em TI.

Execução:  streamlit run app.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

from src.engine import ConsultorCarreiras
from src.trilhas import OPCOES_ASPECTO, OPCOES_ENTREGA, ROTULOS, TRILHAS

st.set_page_config(
    page_title="Consultor Inteligente de Carreiras em TI",
    layout="centered",
)

st.title("Consultor Inteligente de Carreiras em TI")
st.markdown(
    "Sistema Especialista baseado em Regras que diagnostica e recomenda "
    "**uma das 10 trilhas de carreira em TI**, justificando a decisão com "
    "base nas regras disparadas (motor de inferência Experta)."
)
st.divider()

with st.form("entrevista"):
    st.subheader("Entrevista — responda com sinceridade")

    col1, col2 = st.columns(2)
    with col1:
        afinidade = st.radio(
            "Qual seu nível de afinidade com matemática/estatística?",
            options=list(ROTULOS["afinidade"].keys()),
            format_func=lambda k: ROTULOS["afinidade"][k],
            horizontal=False,
        )
        preferencia = st.selectbox(
            "O que você mais gosta de fazer no dia a dia?",
            options=list(ROTULOS["preferencia"].keys()),
            format_func=lambda k: ROTULOS["preferencia"][k],
        )
        linguagem = st.selectbox(
            "Linguagem/ferramenta de maior afinidade atual?",
            options=list(ROTULOS["linguagem"].keys()),
            format_func=lambda k: ROTULOS["linguagem"][k],
        )
    with col2:
        entrega = st.radio(
            "Que tipo de valor você prefere entregar?",
            options=list(ROTULOS["entrega"].keys()),
            format_func=lambda k: ROTULOS["entrega"][k],
        )
        aspecto = st.selectbox(
            "Qual aspecto do trabalho técnico mais te atrai?",
            options=list(ROTULOS["aspecto"].keys()),
            format_func=lambda k: ROTULOS["aspecto"][k],
        )

    enviado = st.form_submit_button("🔍 Diagnosticar trilha", use_container_width=True)

if enviado:
    motor = ConsultorCarreiras()
    resultado = motor.diagnosticar(
        afinidade=afinidade,
        preferencia=preferencia,
        linguagem=linguagem,
        entrega=entrega,
        aspecto=aspecto,
    )

    st.divider()

    if resultado["trilha"] is None:
        st.warning(resultado["mensagem"])
    else:
        st.success(f"### Trilha recomendada: {resultado['nome']}")
        st.caption(resultado["descricao"])
        st.metric("Pontuação acumulada", resultado["pontuacao"])

        st.subheader("Justificativa — regras disparadas")
        for m in resultado["motivos"]:
            st.markdown(f"- **+{m['pontos']}** — {m['motivo']}")

        with st.expander("Ver placar completo (todas as trilhas pontuadas)"):
            for trilha_id, pontos in resultado["placar"].items():
                st.write(f"{TRILHAS[trilha_id]['nome']}: **{pontos}** pontos")
else:
    st.info("Preencha o formulário acima e clique em **Diagnosticar trilha**.")
