# Consultor Avançado de Carreiras em TI

> **Atividade da matéria de Inteligência Artificial (IA)** — Sistema Especialista Baseado em Regras com **tratamento de incerteza e pontuação ponderada** que analisa o perfil multifacetado do usuário, calcula uma **matriz de compatibilidade percentual para 10 trilhas**, identifica **skill gaps** e gera um **roadmap personalizado** (estudo, certificações e portfólio).

## Diferenciais (versão 2)

- **Entrada gradual (Likert 1–5):** afinidades respondidas com grau, não sim/não.
- **Ranking multi-trilha em %:** Top 3 com percentual de aderência (ex.: 1º DevOps 83%, 2º Cloud 65%).
- **Penalidades lógicas:** perfis conflitantes (ex.: forte design × pouca lógica) reduzem trilhas incompatíveis.
- **Skill Gap Analysis:** compara o conhecimento atual com o exigido para Júnior na trilha indicada.
- **Roadmap personalizado:** o que estudar primeiro (priorizando lacunas), certificações e projetos de portfólio.
- **Base de conhecimento desacoplada:** pesos, regras, gaps e roadmap vivem em `knowledge/regras_carreiras.json`, não no código.
- **Nunca retorna vazio:** mesmo com respostas vazias/neutras, há sempre uma recomendação.

## As 10 Trilhas

Back-end · Front-end & UI/UX · Ciência de Dados e ML · Engenharia de Dados · Cibersegurança · DevOps & SRE · Cloud Architecture · Mobile · QA · Product Management

## Instalação

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

Requer Python ≥ 3.10.

## Execução

### Interface web (Streamlit)

```bash
streamlit run app.py
```

Wizard em 3 etapas: **Passo 1** perfil pessoal → **Passo 2** afinidades (1–5) → **Passo 3** objetivos → **Resultado** (Top 3 em barras + radar, skill gaps e plano de ação).

### Testes

```bash
# validação com 10 personas (deve imprimir 10/10)
python -m tests.personas

# casos-limite e robustez (deve imprimir 11/11)
python -m tests.edge_cases

# teste de fumaça do wizard completo (Perfil -> Afinidades -> Objetivos -> Resultado)
python -m tests.test_app
```

## Relatório

O relatório técnico da atividade está em **`docs/relatorio-consultor.tex`** (LaTeX),
com a versão compilada em **`docs/relatorio-consultor.pdf`**.

Para recompilar:

```bash
cd docs
pdflatex relatorio-consultor.tex
pdflatex relatorio-consultor.tex   # segunda passada: sumário e referências cruzadas
```

Ou, sem instalar nada, importe o `.tex` no [Overleaf](https://www.overleaf.com/).
O documento usa apenas pacotes de uma instalação LaTeX completa
(`babel`, `tikz`, `booktabs`, `longtable`, `listings`).

## Como funciona

1. **Entrevista gradual:** 10 afinidades em Likert (1–5) + seleções de objetivo.
2. **Motor ponderado** (`src/motor.py`): cada resposta multiplica o peso da trilha correspondente; **16 regras SE-ENTÃO** somam bônus e **7 penalidades** reduzem perfis conflitantes.
3. **Normalização:** placar / pontuação máxima possível × 100 → compatibilidade 0–100% por trilha; ordenação gera o Top 3.
4. **Plano de ação** (`src/recomendacoes.py`): cruza a trilha vencedora com os conhecimentos marcados → gaps + roadmap priorizado.

## Estrutura do projeto

```
.
├── app.py                         # Interface Streamlit (wizard)
├── requirements.txt
├── knowledge/
│   └── regras_carreiras.json      # Base de conhecimento (pesos, regras, gaps, roadmap)
├── src/
│   ├── knowledge.py               # Loader dinâmico do JSON
│   ├── motor.py                   # Motor de inferência ponderado
│   └── recomendacoes.py           # Skill gaps + roadmap
├── tests/
│   ├── personas.py                # 10 personas de validação
│   ├── edge_cases.py              # 11 casos-limite/robustez
│   └── test_app.py                # Teste de fumaça da interface
└── docs/
    ├── relatorio-consultor.tex    # Relatório da atividade (LaTeX)
    ├── PLANO.md                   # Planejamento
    └── MATRIZ_DECISAO.md          # Matriz de decisão (versão 1)
```
