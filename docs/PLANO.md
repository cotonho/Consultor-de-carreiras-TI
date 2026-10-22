# Plano do Projeto — Consultor Inteligente de Carreiras em TI

Sistema Especialista baseado em Regras (SE-ENTÃO) que diagnostica e recomenda uma das 10 trilhas de carreira em TI, justificando a decisão com base nas regras disparadas.

## Stack Tecnológica

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Linguagem | Python ≥ 3.10 | Requisito do enunciado |
| Motor de inferência | Experta | Forward chaining com `@Rule` e saliência |
| Interface | Streamlit | Interface web amigável sem frontend separado |
| Versionamento | Git / GitHub | Controle de versão + README |

## Estrutura do Repositório

```
AECO2/
├── README.md                  # Instruções de instalação e execução
├── requirements.txt           # streamlit, experta
├── app.py                     # Interface Streamlit (Fase 3)
├── src/
│   ├── __init__.py
│   ├── facts.py               # Classes de Fatos (Fase 2)
│   ├── engine.py              # Motor de inferência / regras (Fase 2)
│   └── trilhas.py             # Catálogo das 10 trilhas + descrições
├── tests/
│   ├── __init__.py
│   └── personas.py            # 4+ personas de validação (Fase 4)
└── docs/
    ├── PLANO.md               # Este arquivo
    └── MATRIZ_DECISAO.md      # Fase 1 — matriz de decisão
```

## Fases de Desenvolvimento

### Fase 1 — Engenharia de Conhecimento e Matriz de Decisão
- Definir os atributos de entrada (dimensões da entrevista).
- Montar a matriz decisão: quais combinações de respostas ativam cada trilha.
- Arquivo: `docs/MATRIZ_DECISAO.md`.

### Fase 2 — Base de Conhecimento (Python/Experta)
- Criar classes `Fact` (fatos de entrada + fato-resultado `trilha`).
- Codificar 20–25 regras `@Rule` cruzadas com saliência para evitar ambiguidades.
- Implementar o "diagnóstico por pontuação" (contagem de regras disparadas por trilha) e desempate transparente.
- Arquivos: `src/facts.py`, `src/engine.py`, `src/trilhas.py`.

### Fase 3 — Interface Web (Streamlit)
- Componentes de entrada: selects/radios para as dimensões da entrevista.
- Botão "Diagnosticar" → executa o motor → exibe trilha + justificativa (regras disparadas).
- Arquivo: `app.py`.

### Fase 4 — Validação com Personas
- 4+ personas: analítico (dados), infra/segurança, visual/frontend, negócios/produto.
- Script de teste que roda o motor isoladamente (sem Streamlit) e imprime o resultado.
- Arquivo: `tests/personas.py`.

### Fase 5 — Documentação e GitHub
- `README.md` com instalação (`pip install -r requirements.txt`) e execução (`streamlit run app.py`).
- Commits incrementais por fase, branch `main` + tag final.

## As 10 Trilhas (escopo congelado)

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

## Dimensões da Entrevista (dados de entrada)

| Dimensão | Opções |
|---|---|
| Afinidade matemática/estatística | Baixa, Média, Alta |
| Preferência de atuação diária | Algoritmos lógicos, Layouts visuais, Servidores/infra, Dados brutos, Segurança, Processos/qualidade, Pessoas/negócio |
| Linguagem/ferramenta de maior afinidade | Python, JavaScript, Linux/Redes, Nenhuma/Iniciante |
| Tipo de entrega de valor preferida | Produto final para o usuário, Infraestrutura que sustenta o sistema, Segurança contra invasões, Decisões de negócio |

> Observação: as dimensões podem ser refinadas na Fase 1 (ex.: separar "mobile" de "front-end", adicionar "metodologias ágeis") — a matriz de decisão definirá os fatos exatos.

## Critérios de Sucesso

- [x] 20–25 regras implementadas e documentadas. *(35 regras em `src/engine.py`)*
- [x] Sistema diferencia perfis próximos (CDS×EGD, DevOps×Cloud, FE×Mobile) — validado com 10 personas.
- [x] Justificativa exibida lista as regras/motivos que levaram à recomendação.
- [x] 4+ personas validadas com resultado esperado. *(10/10 corretas em `tests/personas.py`)*
- [x] README completo e app rodando via `streamlit run app.py`.
