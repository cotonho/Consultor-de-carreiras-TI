"""Catálogo das 10 trilhas de carreira em TI."""

TRILHAS: dict[str, dict[str, str]] = {
    "back": {
        "nome": "Desenvolvimento Back-end",
        "descricao": (
            "Foco em lógica de servidores, construção de APIs, "
            "regras de negócio e bancos de dados."
        ),
    },
    "front": {
        "nome": "Desenvolvimento Front-end & UI/UX",
        "descricao": (
            "Foco em interfaces web responsivas, experiência do usuário "
            "e frameworks reativos."
        ),
    },
    "ciencia_dados": {
        "nome": "Ciência de Dados e Machine Learning",
        "descricao": (
            "Foco em estatística, modelagem preditiva, análise de grandes "
            "massas de dados e inteligência artificial."
        ),
    },
    "engenharia_dados": {
        "nome": "Engenharia de Dados",
        "descricao": (
            "Foco em arquitetura de dados, construção de pipelines (ETL/ELT) "
            "e infraestrutura para Data Lakes."
        ),
    },
    "ciberseguranca": {
        "nome": "Cibersegurança (Security / Pentesting)",
        "descricao": (
            "Foco em defesa cibernética, análise de vulnerabilidades, "
            "criptografia e redes seguras."
        ),
    },
    "devops": {
        "nome": "DevOps & SRE",
        "descricao": (
            "Foco em automação de processos, integração e entrega contínua "
            "(CI/CD) e contêineres."
        ),
    },
    "cloud": {
        "nome": "Computação em Nuvem (Cloud Architecture)",
        "descricao": (
            "Foco em planejamento, migração e gestão de infraestruturas "
            "escaláveis (AWS/Azure/GCP)."
        ),
    },
    "mobile": {
        "nome": "Desenvolvimento Mobile",
        "descricao": (
            "Foco no ecossistema de dispositivos móveis (nativo ou "
            "multiplataforma com Flutter/React Native)."
        ),
    },
    "qa": {
        "nome": "Engenharia de Qualidade e Testes (QA)",
        "descricao": (
            "Foco em testes automatizados, confiabilidade de software "
            "e processos de qualidade."
        ),
    },
    "product": {
        "nome": "Gestão de Produtos (Product Management)",
        "descricao": (
            "Foco na ponte entre negócio, design e desenvolvimento, "
            "metodologias ágeis e priorização de produto."
        ),
    },
}

ORDEM_DESEMPATE: list[str] = list(TRILHAS.keys())

OPCOES_AFINIDADE = ("baixa", "media", "alta")
OPCOES_PREFERENCIA = (
    "algoritmos",
    "layouts",
    "servidores",
    "dados_brutos",
    "seguranca",
    "qualidade",
    "negocio",
    "pipelines",
    "mobile",
)
OPCOES_LINGUAGEM = ("python", "javascript", "linux_redes", "nenhuma")
OPCOES_ENTREGA = (
    "usuario_final",
    "infraestrutura",
    "seguranca",
    "dados_insights",
    "negocio",
)
OPCOES_ASPECTO = (
    "automacao",
    "arquitetura",
    "descoberta",
    "resolucao",
    "criacao",
)

ROTULOS = {
    "afinidade": {
        "baixa": "Baixa",
        "media": "Média",
        "alta": "Alta",
    },
    "preferencia": {
        "algoritmos": "Escrever algoritmos e lógica de programação",
        "layouts": "Criar layouts e interfaces visuais",
        "servidores": "Lidar com servidores e infraestrutura",
        "dados_brutos": "Analizar dados brutos e extrair padrões",
        "seguranca": "Garantir a segurança de sistemas",
        "qualidade": "Garantir qualidade e testar software",
        "negocio": "Liderar pessoas, produto e decisões de negócio",
        "pipelines": "Construir pipelines e fluxos de dados",
        "mobile": "Desenvolver aplicativos para celular",
    },
    "linguagem": {
        "python": "Python",
        "javascript": "JavaScript / TypeScript",
        "linux_redes": "Linux / Redes",
        "nenhuma": "Nenhuma / Iniciante",
    },
    "entrega": {
        "usuario_final": "O produto final para o usuário",
        "infraestrutura": "A infraestrutura que sustenta o sistema",
        "seguranca": "A segurança contra invasões",
        "dados_insights": "Dados e insights para decisões",
        "negocio": "Decisões e valor de negócio",
    },
    "aspecto": {
        "automacao": "Automatizar processos e operações",
        "arquitetura": "Projetar arquiteturas escaláveis",
        "descoberta": "Descobrir padrões e insights",
        "resolucao": "Investigar e resolver problemas complexos",
        "criacao": "Criar experiências para pessoas",
    },
}
