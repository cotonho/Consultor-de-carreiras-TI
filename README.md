# 🧭 Consultor Inteligente de Carreiras em TI

> **Atividade da matéria de Inteligência Artificial (IA)** — Sistema Especialista baseado em Regras (SE-ENTÃO) que entrevista o usuário e recomenda uma das **10 trilhas de carreira em TI**, justificando a decisão com base nas regras disparadas.

- **Motor de inferência:** [Experta](https://github.com/nilp0inter/experta) (forward chaining)
- **Interface web:** [Streamlit](https://streamlit.io/)
- **Linguagem:** Python ≥ 3.10

## As 10 Trilhas

1. Desenvolvimento Back-end
2. Desenvolvimento Front-end & UI/UX
3. Ciência de Dados e Machine Learning
4. Engenharia de Dados
5. Cibersegurança (Security / Pentesting)
6. DevOps & SRE
7. Computação em Nuvem (Cloud Architecture)
8. Desenvolvimento Mobile
9. Engenharia de Qualidade e Testes (QA)
10. Gestão de Produtos (Product Management)

## Instalação

> **Importante:** use Python 3.10–3.12 (o Experta ainda não suporta 3.13+). O `requirements.txt` força `frozendict>=2.0` porque a versão antiga pinada pelo Experta quebra no Python 3.10+.

```bash
# criar e ativar ambiente virtual (recomendado)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# instalar dependências
pip install -r requirements.txt
```

## Execução

### Interface web (Streamlit)

```bash
streamlit run app.py
```

Abra o endereço exibido no terminal (normalmente `http://localhost:8501`), responda à entrevista e clique em **Diagnosticar trilha**.

### Validação com personas (sem interface)

```bash
python -m tests.personas
```

Deve imprimir `Resultado: 10/10 personas corretas`.

## Estrutura do projeto

```
.
├── app.py                 # Interface Streamlit
├── requirements.txt
├── src/
│   ├── facts.py           # Classes de Fatos (Fact)
│   ├── engine.py          # Motor de inferência (regras @Rule)
│   └── trilhas.py         # Catálogo das 10 trilhas + opções da entrevista
├── tests/
│   └── personas.py        # 10 personas de validação
└── docs/
    ├── PLANO.md           # Planejamento geral do projeto
    └── MATRIZ_DECISAO.md  # Fase 1 — matriz de decisão e regras
```

## Como funciona

1. **Entrevista (5 dimensões):** afinidade matemática/estatística, preferência de atuação diária, linguagem/ferramenta, tipo de entrega de valor e aspecto técnico mais atrativo.
2. **Motor de inferência:** ~30 regras `@Rule` com saliência pontuam cada trilha conforme os fatos declarados (forward chaining).
3. **Consolidação:** a trilha de maior pontuação vence (desempate por nº de regras e ordem do catálogo). A interface exibe a trilha, a pontuação e as regras que motivaram a decisão.
