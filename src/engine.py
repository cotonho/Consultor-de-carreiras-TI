"""Motor de inferência do Consultor Inteligente de Carreiras em TI."""

from experta import KnowledgeEngine, Rule

from .facts import (
    AfinidadeMatematica,
    AspectoTecnico,
    EntregaValor,
    Linguagem,
    PreferenciaDiaria,
)
from .trilhas import ORDEM_DESEMPATE, TRILHAS


class ConsultorCarreiras(KnowledgeEngine):
    """Entrevista → trilha recomendada + justificativa (regras disparadas)."""

    def __init__(self) -> None:
        super().__init__()
        self.placar: dict[str, int] = {}
        self.motivos: list[dict] = []

    # ------------------------------------------------------------------
    # Infraestrutura do motor
    # ------------------------------------------------------------------

    def _pontuar(self, trilha: str, pontos: int, descricao: str) -> None:
        self.placar[trilha] = self.placar.get(trilha, 0) + pontos
        self.motivos.append({"trilha": trilha, "pontos": pontos, "motivo": descricao})

    def diagnosticar(
        self,
        afinidade: str,
        preferencia: str,
        linguagem: str,
        entrega: str,
        aspecto: str,
    ) -> dict:
        """Executa a inferência e retorna o resultado estruturado."""
        self.reset()
        self.placar = {}
        self.motivos = []

        self.declare(AfinidadeMatematica(nivel=afinidade))
        self.declare(PreferenciaDiaria(tipo=preferencia))
        self.declare(Linguagem(nome=linguagem))
        self.declare(EntregaValor(tipo=entrega))
        self.declare(AspectoTecnico(aspecto=aspecto))
        self.run()

        return self._consolidar()

    def _consolidar(self) -> dict:
        if not self.placar:
            return {
                "trilha": None,
                "nome": None,
                "descricao": None,
                "pontuacao": 0,
                "placar": {},
                "motivos": [],
                "mensagem": (
                    "Não foi possível diagnosticar uma trilha com as respostas "
                    "fornecidas. Tente refazer a entrevista."
                ),
            }

        def chave_ordenacao(item: tuple[str, int]) -> tuple:
            trilha, pontos = item
            n_regras = sum(1 for m in self.motivos if m["trilha"] == trilha)
            prioridade = -ORDEM_DESEMPATE.index(trilha)
            return (pontos, n_regras, prioridade)

        vencedor = max(self.placar.items(), key=chave_ordenacao)[0]
        info = TRILHAS[vencedor]
        motivos_vencedor = [m for m in self.motivos if m["trilha"] == vencedor]
        motivos_vencedor.sort(key=lambda m: m["pontos"], reverse=True)

        return {
            "trilha": vencedor,
            "nome": info["nome"],
            "descricao": info["descricao"],
            "pontuacao": self.placar[vencedor],
            "placar": dict(sorted(self.placar.items(), key=lambda kv: -kv[1])),
            "motivos": motivos_vencedor,
            "mensagem": None,
        }

    # ==================================================================
    # BACK-END
    # ==================================================================

    @Rule(PreferenciaDiaria(tipo="algoritmos"), Linguagem(nome="python"), salience=10)
    def regra_back_algoritmos_python(self):
        self._pontuar(
            "back",
            5,
            "Preferência por algoritmos lógicos + afinidade com Python = "
            "perfil clássico de desenvolvimento back-end (APIs, regras de negócio).",
        )

    @Rule(
        PreferenciaDiaria(tipo="algoritmos"),
        AspectoTecnico(aspecto="arquitetura"),
        salience=9,
    )
    def regra_back_algoritmos_arquitetura(self):
        self._pontuar(
            "back",
            4,
            "Gosto de lógica combinado com projeção de arquiteturas "
            "bem estruturadas aponta para back-end.",
        )

    @Rule(
        PreferenciaDiaria(tipo="algoritmos"),
        AfinidadeMatematica(nivel="media"),
        salience=8,
    )
    def regra_back_algoritmos_media(self):
        self._pontuar(
            "back",
            3,
            "Algoritmos com afinidade matemática média indicam resolução de "
            "problemas de servidor/negócio sem foco em ciência de dados.",
        )

    @Rule(
        PreferenciaDiaria(tipo="servidores"),
        Linguagem(nome="python"),
        EntregaValor(tipo="usuario_final"),
        salience=8,
    )
    def regra_back_servidores_python_usuario(self):
        self._pontuar(
            "back",
            4,
            "Servidores + Python + entrega para o usuário final = "
            "desenvolvimento de APIs e serviços de produto (back-end).",
        )

    # ==================================================================
    # FRONT-END & UI/UX
    # ==================================================================

    @Rule(
        PreferenciaDiaria(tipo="layouts"),
        Linguagem(nome="javascript"),
        salience=10,
    )
    def regra_front_layouts_javascript(self):
        self._pontuar(
            "front",
            5,
            "Layouts visuais + JavaScript = combinação clássica de "
            "desenvolvimento front-end e frameworks reativos.",
        )

    @Rule(
        PreferenciaDiaria(tipo="layouts"),
        AspectoTecnico(aspecto="criacao"),
        salience=9,
    )
    def regra_front_layouts_criacao(self):
        self._pontuar(
            "front",
            4,
            "Criar interfaces visuais voltadas a experiências para pessoas "
            "é o núcleo do front-end e da UI/UX.",
        )

    @Rule(
        PreferenciaDiaria(tipo="layouts"),
        EntregaValor(tipo="usuario_final"),
        salience=8,
    )
    def regra_front_layouts_usuario(self):
        self._pontuar(
            "front",
            3,
            "Foco em layouts entregando valor direto ao usuário final "
            "aponta para interfaces web.",
        )

    # ==================================================================
    # CIÊNCIA DE DADOS & MACHINE LEARNING
    # ==================================================================

    @Rule(
        PreferenciaDiaria(tipo="dados_brutos"),
        AfinidadeMatematica(nivel="alta"),
        Linguagem(nome="python"),
        salience=12,
    )
    def regra_ds_dados_alta_python(self):
        self._pontuar(
            "ciencia_dados",
            6,
            "Dados brutos + afinidade matemática ALTA + Python = "
            "assinatura clássica de Ciência de Dados / Machine Learning.",
        )

    @Rule(
        PreferenciaDiaria(tipo="dados_brutos"),
        AspectoTecnico(aspecto="descoberta"),
        AfinidadeMatematica(nivel="alta"),
        salience=11,
    )
    def regra_ds_dados_descoberta_alta(self):
        self._pontuar(
            "ciencia_dados",
            5,
            "Busca por padrões/insights em dados com forte base matemática "
            "é o coração da modelagem preditiva e da IA.",
        )

    @Rule(
        PreferenciaDiaria(tipo="dados_brutos"),
        AspectoTecnico(aspecto="descoberta"),
        Linguagem(nome="python"),
        salience=9,
    )
    def regra_ds_dados_descoberta_python(self):
        self._pontuar(
            "ciencia_dados",
            4,
            "Analisar dados para descobrir padrões com Python aponta para "
            "análise estatística e modelagem.",
        )

    @Rule(
        PreferenciaDiaria(tipo="dados_brutos"),
        EntregaValor(tipo="dados_insights"),
        salience=8,
    )
    def regra_ds_dados_insights(self):
        self._pontuar(
            "ciencia_dados",
            3,
            "Entregar insights a partir de dados brutos é a proposta de "
            "valor da Ciência de Dados.",
        )

    # ==================================================================
    # ENGENHARIA DE DADOS
    # ==================================================================

    @Rule(PreferenciaDiaria(tipo="pipelines"), Linguagem(nome="python"), salience=11)
    def regra_de_pipelines_python(self):
        self._pontuar(
            "engenharia_dados",
            5,
            "Construir pipelines de dados com Python = ETL/ELT e "
            "infraestrutura de dados (Engenharia de Dados).",
        )

    @Rule(
        PreferenciaDiaria(tipo="pipelines"),
        AspectoTecnico(aspecto="automacao"),
        salience=10,
    )
    def regra_de_pipelines_automacao(self):
        self._pontuar(
            "engenharia_dados",
            4,
            "Automatizar fluxos de dados é o dia a dia de quem constrói "
            "pipelines e Data Lakes.",
        )

    @Rule(
        PreferenciaDiaria(tipo="pipelines"),
        AspectoTecnico(aspecto="arquitetura"),
        salience=9,
    )
    def regra_de_pipelines_arquitetura(self):
        self._pontuar(
            "engenharia_dados",
            4,
            "Projetar a arquitetura de movimentação de dados "
            "(lake/lakehouse) é papel do Engenheiro de Dados.",
        )

    @Rule(
        PreferenciaDiaria(tipo="dados_brutos"),
        EntregaValor(tipo="infraestrutura"),
        salience=9,
    )
    def regra_de_dados_infra(self):
        self._pontuar(
            "engenharia_dados",
            4,
            "Dados brutos + entrega de infraestrutura = construir a "
            "plataforma/pipeline que sustenta os dados (não a modelagem).",
        )

    @Rule(
        PreferenciaDiaria(tipo="dados_brutos"),
        AspectoTecnico(aspecto="automacao"),
        salience=8,
    )
    def regra_de_dados_automacao(self):
        self._pontuar(
            "engenharia_dados",
            3,
            "Automatizar processamento de dados aponta para engenharia "
            "de pipelines, não para modelagem preditiva.",
        )

    # ==================================================================
    # CIBERSEGURANÇA
    # ==================================================================

    @Rule(PreferenciaDiaria(tipo="seguranca"), salience=10)
    def regra_sec_seguranca(self):
        self._pontuar(
            "ciberseguranca",
            4,
            "Preferência diária por garantir segurança de sistemas "
            "aponta direto para Cibersegurança / Pentesting.",
        )

    @Rule(
        PreferenciaDiaria(tipo="seguranca"),
        Linguagem(nome="linux_redes"),
        salience=9,
    )
    def regra_sec_linux_redes(self):
        self._pontuar(
            "ciberseguranca",
            3,
            "Segurança + Linux/Redes = defesa cibernética, análise de "
            "vulnerabilidades e redes seguras.",
        )

    @Rule(
        PreferenciaDiaria(tipo="seguranca"),
        AspectoTecnico(aspecto="resolucao"),
        salience=9,
    )
    def regra_sec_resolucao(self):
        self._pontuar(
            "ciberseguranca",
            3,
            "Investigar e resolver problemas complexos de segurança "
            "(forense, pentest) combina com este perfil.",
        )

    # ==================================================================
    # DEVOPS & SRE
    # ==================================================================

    @Rule(
        PreferenciaDiaria(tipo="servidores"),
        AspectoTecnico(aspecto="automacao"),
        salience=10,
    )
    def regra_devops_servidores_automacao(self):
        self._pontuar(
            "devops",
            5,
            "Servidores + automação de processos = CI/CD, infra como código "
            "e estabilidade (DevOps & SRE).",
        )

    @Rule(
        PreferenciaDiaria(tipo="servidores"),
        Linguagem(nome="linux_redes"),
        AspectoTecnico(aspecto="automacao"),
        salience=9,
    )
    def regra_devops_linux_automacao(self):
        self._pontuar(
            "devops",
            4,
            "Linux/Redes + automação operacional é o coração do DevOps/SRE.",
        )

    @Rule(
        PreferenciaDiaria(tipo="servidores"),
        EntregaValor(tipo="infraestrutura"),
        AspectoTecnico(aspecto="automacao"),
        salience=8,
    )
    def regra_devops_infra_automacao(self):
        self._pontuar(
            "devops",
            4,
            "Entregar infraestrutura automatizada e confiável é a missão "
            "de DevOps & SRE.",
        )

    @Rule(
        PreferenciaDiaria(tipo="servidores"),
        Linguagem(nome="linux_redes"),
        salience=6,
    )
    def regra_devops_linux_generica(self):
        self._pontuar(
            "devops",
            2,
            "Atuação em servidores com Linux/Redes gera afinidade com "
            "operações e confiabilidade (DevOps & SRE).",
        )

    # ==================================================================
    # COMPUTAÇÃO EM NUVEM
    # ==================================================================

    @Rule(
        PreferenciaDiaria(tipo="servidores"),
        AspectoTecnico(aspecto="arquitetura"),
        salience=10,
    )
    def regra_cloud_servidores_arquitetura(self):
        self._pontuar(
            "cloud",
            5,
            "Servidores + projeção de arquiteturas escaláveis = "
            "Cloud Architecture (AWS/Azure/GCP).",
        )

    @Rule(
        PreferenciaDiaria(tipo="servidores"),
        Linguagem(nome="linux_redes"),
        AspectoTecnico(aspecto="arquitetura"),
        salience=9,
    )
    def regra_cloud_linux_arquitetura(self):
        self._pontuar(
            "cloud",
            4,
            "Base em Linux/Redes + foco em arquitetura escalável "
            "aponta para desenho de soluções em nuvem.",
        )

    @Rule(
        PreferenciaDiaria(tipo="servidores"),
        EntregaValor(tipo="infraestrutura"),
        AspectoTecnico(aspecto="arquitetura"),
        salience=8,
    )
    def regra_cloud_infra_arquitetura(self):
        self._pontuar(
            "cloud",
            4,
            "Entregar infraestrutura escalável projetada de forma "
            "deliberada é o papel do arquiteto de nuvem.",
        )

    # ==================================================================
    # DESENVOLVIMENTO MOBILE
    # ==================================================================

    @Rule(
        PreferenciaDiaria(tipo="mobile"),
        Linguagem(nome="javascript"),
        salience=10,
    )
    def regra_mobile_javascript(self):
        self._pontuar(
            "mobile",
            5,
            "Mobile + JavaScript = frameworks multiplataforma "
            "(React Native, Ionic, Flutter com web stack).",
        )

    @Rule(PreferenciaDiaria(tipo="mobile"), salience=8)
    def regra_mobile_generica(self):
        self._pontuar(
            "mobile",
            3,
            "Preferência explícita por aplicativos móveis aponta para "
            "o ecossistema Android/iOS.",
        )

    @Rule(
        PreferenciaDiaria(tipo="mobile"),
        AspectoTecnico(aspecto="criacao"),
        salience=7,
    )
    def regra_mobile_criacao(self):
        self._pontuar(
            "mobile",
            2,
            "Criar experiências focadas no usuário no bolso "
            "complementa o perfil mobile.",
        )

    # ==================================================================
    # ENGENHARIA DE QUALIDADE E TESTES (QA)
    # ==================================================================

    @Rule(
        PreferenciaDiaria(tipo="qualidade"),
        AspectoTecnico(aspecto="resolucao"),
        salience=10,
    )
    def regra_qa_qualidade_resolucao(self):
        self._pontuar(
            "qa",
            5,
            "Garantir qualidade investigando e resolvendo falhas = "
            "testes, confiabilidade e processos de qualidade (QA).",
        )

    @Rule(
        PreferenciaDiaria(tipo="qualidade"),
        EntregaValor(tipo="usuario_final"),
        salience=9,
    )
    def regra_qa_qualidade_usuario(self):
        self._pontuar(
            "qa",
            4,
            "Entregar confiabilidade ao usuário final é o objetivo "
            "direto da Engenharia de Qualidade e Testes.",
        )

    @Rule(PreferenciaDiaria(tipo="qualidade"), salience=7)
    def regra_qa_qualidade_generica(self):
        self._pontuar(
            "qa",
            2,
            "Foco diário em qualidade de software já diferencia o "
            "perfil QA.",
        )

    # ==================================================================
    # GESTÃO DE PRODUTOS (PRODUCT MANAGEMENT)
    # ==================================================================

    @Rule(
        PreferenciaDiaria(tipo="negocio"),
        EntregaValor(tipo="negocio"),
        salience=10,
    )
    def regra_pm_negocio_negocio(self):
        self._pontuar(
            "product",
            6,
            "Preferência por negócio + entrega de valor de negócio = "
            "ponte entre negócio, design e desenvolvimento (Product Manager).",
        )

    @Rule(
        PreferenciaDiaria(tipo="negocio"),
        AspectoTecnico(aspecto="criacao"),
        salience=9,
    )
    def regra_pm_negocio_criacao(self):
        self._pontuar(
            "product",
            4,
            "Liderar criação de produtos para pessoas, priorizando "
            "valor, é o coração do Product Management.",
        )

    @Rule(PreferenciaDiaria(tipo="negocio"), salience=7)
    def regra_pm_negocio_generica(self):
        self._pontuar(
            "product",
            3,
            "Atuação diária orientada a produto/negócio diferencia "
            "o perfil de gestão de produtos.",
        )
