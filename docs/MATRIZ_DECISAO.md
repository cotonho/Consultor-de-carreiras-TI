# Fase 1 — Matriz de Decisão (Engenharia de Conhecimento)

Este documento define os fatos de entrada, a lógica de pontuação e como as respostas do usuário ativam as regras das 10 trilhas. É a base para a codificação em `src/engine.py`.

## 1. Fatos de Entrada (Entrevista)

| Atributo (Fact) | Pergunta | Opções |
|---|---|---|
| `afinidade_matematica` | Qual seu nível de afinidade com matemática/estatística? | `baixa` \| `media` \| `alta` |
| `preferencia_diaria` | O que você mais gosta de fazer no dia a dia? | `algoritmos` \| `layouts` \| `servidores` \| `dados_brutos` \| `seguranca` \| `qualidade` \| `negocio` \| `pipelines` \| `mobile` |
| `linguagem` | Qual sua linguagem/ferramenta de maior afinidade? | `python` \| `javascript` \| `linux_redes` \| `nenhuma` |
| `entrega_valor` | Que tipo de valor você prefere entregar? | `usuario_final` \| `infraestrutura` \| `seguranca` \| `dados_insights` \| `negocio` |
| `aspecto_tecnico` | Qual aspecto do trabalho técnico mais te atrai? | `automacao` \| `arquitetura` \| `descoberta` \| `resolucao` \| `criacao` |

> A 5ª dimensão (`aspecto_tecnico`) foi adicionada para desambiguar pares próximos — principalmente **DevOps × Cloud** (ambos "servidores + infraestrutura", diferenciados por `automacao` vs `arquitetura`).

> Fato de saída: `trilha` (uma das 10 opções) + lista de regras disparadas (justificativa).

## 2. Catálogo de Trilhas e Assinaturas

Cada trilha possui uma **assinatura ideal** (preferências que a representam). O sistema pontua cada trilha conforme as regras disparadas e recomenda a de maior pontuação.

| # | Trilha | Preferências que a fortalecem | Afinidade matemática | Linguagem típica | Entrega típica |
|---|---|---|---|---|---|
| 1 | Back-end | `algoritmos`, `servidores` | media/alta | python | usuario_final, infraestrutura |
| 2 | Front-end & UI/UX | `layouts` | baixa/media | javascript | usuario_final |
| 3 | Ciência de Dados / ML | `dados_brutos` | **alta** | python | dados_insights |
| 4 | Engenharia de Dados | `pipelines`, `dados_brutos` | media/alta | python | infraestrutura, dados_insights |
| 5 | Cibersegurança | `seguranca` | media | linux_redes | seguranca |
| 6 | DevOps & SRE | `servidores`, `qualidade` | media | linux_redes | infraestrutura |
| 7 | Cloud | `servidores` | media | linux_redes | infraestrutura |
| 8 | Mobile | `mobile`, `layouts` | baixa/media | javascript/python | usuario_final |
| 9 | QA | `qualidade` | baixa/media | qualquer | usuario_final (confiabilidade) |
| 10 | Product Management | `negocio` | baixa/media | nenhuma | negocio |

## 3. Regras de Diferenciação (cruzadas — evitam ambiguidade)

| Conflito típico | Como o sistema diferencia |
|---|---|
| Cientista de Dados × Eng. de Dados | `dados_brutos` + afinidade **alta** + `dados_insights` → CDS; `pipelines` + `infraestrutura` → EGD |
| Back-end × DevOps | `algoritmos` + `usuario_final` → Back-end; `servidores` + `infraestrutura` + `linux_redes` → DevOps |
| DevOps × Cloud | DevOps valoriza `qualidade`/CI-CD; Cloud valoriza `infraestrutura` pura/escalabilidade. Regras específicas com saliência |
| Front-end × Mobile | `layouts` + `javascript` → Front-end; `mobile` explícito → Mobile |
| QA × Back-end | QA = `qualidade` como preferência principal; Back-end = `algoritmos` como principal |
| PM × qualquer | `negocio` como preferência + `negocio` como entrega → PM (ponte negócio/design/dev) |

## 4. Estratégia de Inferência

1. **Forward chaining** com Experta: cada regras `@Rule` com ` saliência` (peso) avalia os fatos e incrementa o placar da trilha correspondente via `TrilhaScore`.
2. **Desempate por saliência**: regras mais específicas (ex.: "dados_brutos + alta afinidade + python") têm saliência maior que regras genéricas.
3. **Regra final** (`@Rule` com saliência baixa, disparada após consolidação): seleciona a trilha de maior pontuação e grava a justificativa (regras que pontuaram).

## 5. Regras Implementadas (~30, em `src/engine.py`)

| Trilha | Regras | Exemplos (sal → pontos) |
|---|---|---|
| Back-end | 4 | `algoritmos`+python (10→5); `algoritmos`+`arquitetura` (9→4); `servidores`+python+`usuario_final` (8→4) |
| Front-end | 3 | `layouts`+javascript (10→5); `layouts`+`criacao` (9→4); `layouts`+`usuario_final` (8→3) |
| Ciência de Dados | 4 | `dados_brutos`+`alta`+python (12→6); `dados_brutos`+`descoberta`+`alta` (11→5) |
| Engenharia de Dados | 5 | `pipelines`+python (11→5); `dados_brutos`+`infraestrutura` (9→4) |
| Cibersegurança | 3 | `seguranca` (10→4); `seguranca`+linux_redes (9→3) |
| DevOps & SRE | 4 | `servidores`+`automacao` (10→5); `servidores`+linux_redes+`automacao` (9→4) |
| Cloud | 3 | `servidores`+`arquitetura` (10→5); `servidores`+linux_redes+`arquitetura` (9→4) |
| Mobile | 3 | `mobile`+javascript (10→5); `mobile` (8→3) |
| QA | 3 | `qualidade`+`resolucao` (10→5); `qualidade`+`usuario_final` (9→4) |
| Product Management | 3 | `negocio`+`negocio` (10→6); `negocio`+`criacao` (9→4) |
| **Total** | **35** | ≥ 20 requisitado |

**Consolidação:** maior pontuação vence; desempate por nº de regras disparadas e ordem do catálogo (`ORDEM_DESEMPATE`).
