"""Validacao do motor ponderado com personas de teste (Fase 4/5).

Execucao:  py -3.11 -m tests.personas
"""

from src.motor import MotorPonderado

PERSONAS = [
    {
        "nome": "Ana - perfil analitico (Ciencia de Dados)",
        "esperado": "ciencia_dados",
        "respostas": {
            "experiencia": "estudante",
            "conhecimentos": ["logica", "git", "python", "estatistica", "pandas"],
            "logica_algoritmos": 4,
            "matematica_estatistica": 5,
            "design_visual": 1,
            "infraestrutura": 2,
            "dados_analise": 5,
            "seguranca": 2,
            "automacao_qualidade": 3,
            "gestao_lideranca": 2,
            "mobile_apps": 1,
            "comunicacao_pessoas": 3,
            "preferencia_diaria": "dados_brutos",
            "linguagem": "python",
            "entrega_valor": "dados_insights",
            "aspecto_tecnico": "descoberta",
        },
    },
    {
        "nome": "Bruno - perfil infra/automacao (DevOps)",
        "esperado": "devops",
        "respostas": {
            "experiencia": "estudante",
            "conhecimentos": ["logica", "git", "linux"],
            "logica_algoritmos": 3,
            "matematica_estatistica": 2,
            "design_visual": 1,
            "infraestrutura": 5,
            "dados_analise": 3,
            "seguranca": 3,
            "automacao_qualidade": 5,
            "gestao_lideranca": 2,
            "mobile_apps": 1,
            "comunicacao_pessoas": 2,
            "preferencia_diaria": "servidores",
            "linguagem": "linux_redes",
            "entrega_valor": "infraestrutura",
            "aspecto_tecnico": "automacao",
        },
    },
    {
        "nome": "Carla - perfil visual (Front-end)",
        "esperado": "front",
        "respostas": {
            "experiencia": "estudante",
            "conhecimentos": ["logica", "git", "javascript"],
            "logica_algoritmos": 2,
            "matematica_estatistica": 1,
            "design_visual": 5,
            "infraestrutura": 1,
            "dados_analise": 1,
            "seguranca": 1,
            "automacao_qualidade": 1,
            "gestao_lideranca": 3,
            "mobile_apps": 3,
            "comunicacao_pessoas": 4,
            "preferencia_diaria": "layouts",
            "linguagem": "javascript",
            "entrega_valor": "usuario_final",
            "aspecto_tecnico": "criacao",
        },
    },
    {
        "nome": "Diego - perfil negocios (Product Management)",
        "esperado": "product",
        "respostas": {
            "experiencia": "nenhum",
            "conhecimentos": ["comunicacao"],
            "logica_algoritmos": 1,
            "matematica_estatistica": 1,
            "design_visual": 2,
            "infraestrutura": 1,
            "dados_analise": 2,
            "seguranca": 1,
            "automacao_qualidade": 2,
            "gestao_lideranca": 5,
            "mobile_apps": 1,
            "comunicacao_pessoas": 5,
            "preferencia_diaria": "negocio",
            "linguagem": "nenhuma",
            "entrega_valor": "negocio",
            "aspecto_tecnico": "criacao",
        },
    },
    {
        "nome": "Eva - arquiteta de nuvem (Cloud)",
        "esperado": "cloud",
        "respostas": {
            "experiencia": "estudante",
            "conhecimentos": ["linux", "docker", "redes"],
            "logica_algoritmos": 3,
            "matematica_estatistica": 2,
            "design_visual": 1,
            "infraestrutura": 5,
            "dados_analise": 3,
            "seguranca": 3,
            "automacao_qualidade": 4,
            "gestao_lideranca": 3,
            "mobile_apps": 1,
            "comunicacao_pessoas": 3,
            "preferencia_diaria": "servidores",
            "linguagem": "linux_redes",
            "entrega_valor": "infraestrutura",
            "aspecto_tecnico": "arquitetura",
        },
    },
    {
        "nome": "Fabio - engenheiro de dados",
        "esperado": "engenharia_dados",
        "respostas": {
            "experiencia": "estudante",
            "conhecimentos": ["git", "python", "sql", "pandas"],
            "logica_algoritmos": 3,
            "matematica_estatistica": 3,
            "design_visual": 1,
            "infraestrutura": 4,
            "dados_analise": 5,
            "seguranca": 2,
            "automacao_qualidade": 4,
            "gestao_lideranca": 2,
            "mobile_apps": 1,
            "comunicacao_pessoas": 2,
            "preferencia_diaria": "pipelines",
            "linguagem": "python",
            "entrega_valor": "infraestrutura",
            "aspecto_tecnico": "automacao",
        },
    },
    {
        "nome": "Gabriela - seguranca ofensiva",
        "esperado": "ciberseguranca",
        "respostas": {
            "experiencia": "estudante",
            "conhecimentos": ["linux", "redes", "git"],
            "logica_algoritmos": 3,
            "matematica_estatistica": 2,
            "design_visual": 1,
            "infraestrutura": 4,
            "dados_analise": 2,
            "seguranca": 5,
            "automacao_qualidade": 3,
            "gestao_lideranca": 2,
            "mobile_apps": 1,
            "comunicacao_pessoas": 2,
            "preferencia_diaria": "seguranca",
            "linguagem": "linux_redes",
            "entrega_valor": "seguranca",
            "aspecto_tecnico": "resolucao",
        },
    },
    {
        "nome": "Henrique - desenvolvedor back-end",
        "esperado": "back",
        "respostas": {
            "experiencia": "estagiario",
            "conhecimentos": ["logica", "git", "python", "sql"],
            "logica_algoritmos": 5,
            "matematica_estatistica": 3,
            "design_visual": 1,
            "infraestrutura": 3,
            "dados_analise": 2,
            "seguranca": 2,
            "automacao_qualidade": 3,
            "gestao_lideranca": 2,
            "mobile_apps": 2,
            "comunicacao_pessoas": 2,
            "preferencia_diaria": "algoritmos",
            "linguagem": "python",
            "entrega_valor": "usuario_final",
            "aspecto_tecnico": "arquitetura",
        },
    },
    {
        "nome": "Isabela - desenvolvedora mobile",
        "esperado": "mobile",
        "respostas": {
            "experiencia": "estudante",
            "conhecimentos": ["logica", "git", "javascript"],
            "logica_algoritmos": 3,
            "matematica_estatistica": 2,
            "design_visual": 4,
            "infraestrutura": 1,
            "dados_analise": 2,
            "seguranca": 2,
            "automacao_qualidade": 2,
            "gestao_lideranca": 3,
            "mobile_apps": 5,
            "comunicacao_pessoas": 4,
            "preferencia_diaria": "mobile",
            "linguagem": "javascript",
            "entrega_valor": "usuario_final",
            "aspecto_tecnico": "criacao",
        },
    },
    {
        "nome": "Joao - engenheiro de QA",
        "esperado": "qa",
        "respostas": {
            "experiencia": "nenhum",
            "conhecimentos": ["git"],
            "logica_algoritmos": 2,
            "matematica_estatistica": 1,
            "design_visual": 2,
            "infraestrutura": 2,
            "dados_analise": 2,
            "seguranca": 2,
            "automacao_qualidade": 4,
            "gestao_lideranca": 2,
            "mobile_apps": 2,
            "comunicacao_pessoas": 2,
            "preferencia_diaria": "qualidade",
            "linguagem": "nenhuma",
            "entrega_valor": "usuario_final",
            "aspecto_tecnico": "resolucao",
        },
    },
]


def rodar() -> int:
    motor = MotorPonderado()
    acertos = 0

    for persona in PERSONAS:
        r = motor.diagnosticar(persona["respostas"])
        rec = r["recomendacao"]
        ok = rec is not None and rec["trilha"] == persona["esperado"]
        acertos += ok
        status = "OK " if ok else "FALHOU"
        print(f"[{status}] {persona['nome']}")
        if rec:
            top3 = " | ".join(
                f"{i+1}º {t['nome']} {t['compatibilidade']}%" for i, t in enumerate(r["top3"])
            )
            print(f"         top3: {top3}")
        if not ok:
            print(f"         esperado={persona['esperado']} | obtido={rec and rec['trilha']}")
        print()

    total = len(PERSONAS)
    print(f"Resultado: {acertos}/{total} personas corretas")
    return 0 if acertos == total else 1


if __name__ == "__main__":
    raise SystemExit(rodar())
