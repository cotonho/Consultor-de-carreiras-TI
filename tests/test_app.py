"""Teste de fumaca da interface Streamlit (fluxo completo do wizard).

Executa o app de verdade com streamlit.testing, percorrendo as 3 etapas
ate o resultado. Protege contra erros de API do Streamlit (ex.: uso
incorreto de DeltaGenerator) que nao aparecem na validacao do motor.

Execucao:  py -3.11 -m tests.test_app
"""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def rodar() -> int:
    at = AppTest.from_file(APP, default_timeout=30)
    at.run()
    assert not at.exception, f"Passo 1 falhou: {[e.value for e in at.exception]}"
    assert at.session_state["etapa"] == 0

    at.button[0].click().run()  # Passo 1 -> 2
    assert not at.exception, f"Passo 2 falhou: {[e.value for e in at.exception]}"
    assert at.session_state["etapa"] == 1

    at.button[1].click().run()  # Passo 2 -> 3
    assert not at.exception, f"Passo 3 falhou: {[e.value for e in at.exception]}"
    assert at.session_state["etapa"] == 2

    at.button[1].click().run()  # Diagnosticar
    assert not at.exception, f"Resultado falhou: {[e.value for e in at.exception]}"
    assert at.session_state["etapa"] == 3

    resultado = at.session_state["resultado"]
    assert resultado["recomendacao"] is not None
    assert len(resultado["top3"]) == 3

    print("[OK ] fluxo completo: Perfil -> Afinidades -> Objetivos -> Resultado")
    print(f"      recomendacao: {resultado['recomendacao']['nome']} "
          f"({resultado['recomendacao']['compatibilidade']}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(rodar())
