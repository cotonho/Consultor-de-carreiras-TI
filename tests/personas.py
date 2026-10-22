"""Validação do motor de inferência com personas de teste (Fase 4).

Execução:  py -3.11 -m tests.personas
"""

from src.engine import ConsultorCarreiras

PERSONAS = [
    {
        "nome": "Ana — perfil analítico (Ciência de Dados)",
        "esperado": "ciencia_dados",
        "respostas": {
            "afinidade": "alta",
            "preferencia": "dados_brutos",
            "linguagem": "python",
            "entrega": "dados_insights",
            "aspecto": "descoberta",
        },
    },
    {
        "nome": "Bruno — perfil infra/segurança (DevOps)",
        "esperado": "devops",
        "respostas": {
            "afinidade": "media",
            "preferencia": "servidores",
            "linguagem": "linux_redes",
            "entrega": "infraestrutura",
            "aspecto": "automacao",
        },
    },
    {
        "nome": "Carla — perfil visual (Front-end)",
        "esperado": "front",
        "respostas": {
            "afinidade": "baixa",
            "preferencia": "layouts",
            "linguagem": "javascript",
            "entrega": "usuario_final",
            "aspecto": "criacao",
        },
    },
    {
        "nome": "Diego — perfil negócios (Product Management)",
        "esperado": "product",
        "respostas": {
            "afinidade": "baixa",
            "preferencia": "negocio",
            "linguagem": "nenhuma",
            "entrega": "negocio",
            "aspecto": "criacao",
        },
    },
    {
        "nome": "Eva — arquiteta de nuvem (Cloud)",
        "esperado": "cloud",
        "respostas": {
            "afinidade": "media",
            "preferencia": "servidores",
            "linguagem": "linux_redes",
            "entrega": "infraestrutura",
            "aspecto": "arquitetura",
        },
    },
    {
        "nome": "Fábio — engenheiro de dados",
        "esperado": "engenharia_dados",
        "respostas": {
            "afinidade": "media",
            "preferencia": "dados_brutos",
            "linguagem": "python",
            "entrega": "infraestrutura",
            "aspecto": "automacao",
        },
    },
    {
        "nome": "Gabriela — segurança ofensiva",
        "esperado": "ciberseguranca",
        "respostas": {
            "afinidade": "media",
            "preferencia": "seguranca",
            "linguagem": "linux_redes",
            "entrega": "seguranca",
            "aspecto": "resolucao",
        },
    },
    {
        "nome": "Henrique — desenvolvedor back-end",
        "esperado": "back",
        "respostas": {
            "afinidade": "media",
            "preferencia": "algoritmos",
            "linguagem": "python",
            "entrega": "usuario_final",
            "aspecto": "arquitetura",
        },
    },
    {
        "nome": "Isabela — desenvolvedora mobile",
        "esperado": "mobile",
        "respostas": {
            "afinidade": "media",
            "preferencia": "mobile",
            "linguagem": "javascript",
            "entrega": "usuario_final",
            "aspecto": "criacao",
        },
    },
    {
        "nome": "João — engenheiro de QA",
        "esperado": "qa",
        "respostas": {
            "afinidade": "baixa",
            "preferencia": "qualidade",
            "linguagem": "nenhuma",
            "entrega": "usuario_final",
            "aspecto": "resolucao",
        },
    },
]


def rodar() -> int:
    motor = ConsultorCarreiras()
    acertos = 0

    for persona in PERSONAS:
        r = motor.diagnosticar(**persona["respostas"])
        ok = r["trilha"] == persona["esperado"]
        acertos += ok
        status = "OK " if ok else "FALHOU"
        print(f"[{status}] {persona['nome']}")
        print(f"         esperado={persona['esperado']} | obtido={r['trilha']} | pontos={r['pontuacao']}")
        if not ok:
            print(f"         placar completo: {r['placar']}")
            for m in motor.motivos:
                print(f"           - {m['trilha']}: +{m['pontos']} ({m['motivo']})")
        print()

    total = len(PERSONAS)
    print(f"Resultado: {acertos}/{total} personas corretas")
    return 0 if acertos == total else 1


if __name__ == "__main__":
    raise SystemExit(rodar())
