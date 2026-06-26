# Organização de Cursos e Formações — Análise Macro

Repositório de organização do catálogo de produtos educacionais da [Análise Macro](https://analisemacro.com.br/): cursos, formações, workshops e imersões. Reúne três entregas que nasceram do mesmo esforço de **colocar todo o portfólio em ordem** — do levantamento das informações à publicação das ementas e à medição de inscritos.

## A proposta

O ponto de partida foi simples: o catálogo da Análise Macro cresceu ao longo dos anos e as informações de cada curso (carga horária, número de aulas, conteúdo programático, preço, links) estavam espalhadas. O objetivo deste trabalho foi **consolidar tudo de forma estruturada e reaproveitável**, em três frentes:

1. **Planilha de relação** — um inventário único de todos os cursos e formações, com categoria, carga horária total, horas de vídeo, número de aulas, links e preços. É a fonte de verdade do catálogo, usada para gerar as ementas e alimentar o dashboard. *(Documento de controle interno — não versionado neste repositório e não compartilhado publicamente.)*

2. **Ementas padronizadas** — para cada curso/formação, uma página de ementa no padrão visual da Análise Macro (feita em [Quarto](https://quarto.org/)), com resumo, pré-requisitos, objetivos, programa detalhado e informações de inscrição. São publicadas como site estático (ver abaixo).

3. **Dashboard de inscritos** — um aplicativo que transforma o export de pedidos da loja no número de alunos inscritos por curso e formação, aplicando as regras de negócio da casa. Fica em [`dashboard/`](dashboard/).

## Estrutura do repositório

```
.
├── 01-basicos-fundamentais/      ┐
├── 02-basicos-de-r/              │
├── 03-especializacao-em-r/       │  ementas (.qmd + .html) organizadas
├── 04-basicos-de-python/         │  pelas 8 categorias do catálogo
├── 05-especializacao-em-python/  │
├── 06-especializacao-em-inteligencia-artificial/
├── 07-workshops-e-cursos-ao-vivo/
├── 08-formacoes/                 ┘
└── dashboard/                    → app de inscritos (Shiny for Python)
```

Cada curso fica em sua própria pasta, com a ementa em Quarto (`.qmd`) e a versão renderizada (`.html`). São **46 ementas** no total, distribuídas em 8 categorias.

## As ementas

Cada ementa segue o mesmo padrão: cabeçalho com a identidade da Análise Macro, **Resumo** (o que é, para quem é, ficha técnica), **Pré-requisitos e Objetivos**, **Programa Detalhado** (módulos e aulas) e **Inscrição** (links da página do curso e da matrícula). Elas são publicadas como site estático via GitHub Pages.

### Catálogo

#### Básicos fundamentais
- [como-pensar-com-dados](https://analisemacropro.github.io/organizacao_ementas_am/01-basicos-fundamentais/como-pensar-com-dados/como-pensar-com-dados.html)
- [sql-para-negocios-e-tomada-de-decisao](https://analisemacropro.github.io/organizacao_ementas_am/01-basicos-fundamentais/sql-para-negocios-e-tomada-de-decisao/sql-para-negocios-e-tomada-de-decisao.html)

#### Básicos de R
- [programacao-em-r-para-analise-de-dados](https://analisemacropro.github.io/organizacao_ementas_am/02-basicos-de-r/programacao-em-r-para-analise-de-dados/programacao-em-r-para-analise-de-dados.html)
- [teoria-macroeconomica-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/02-basicos-de-r/teoria-macroeconomica-usando-r/teoria-macroeconomica-usando-r.html)
- [estatistica-para-analise-de-dados-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/02-basicos-de-r/estatistica-para-analise-de-dados-usando-r/estatistica-para-analise-de-dados-usando-r.html)
- [econometria-aplicada-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/02-basicos-de-r/econometria-aplicada-usando-r/econometria-aplicada-usando-r.html)
- [modelagem-e-previsao-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/02-basicos-de-r/modelagem-e-previsao-usando-r/modelagem-e-previsao-usando-r.html)
- [analise-de-conjuntura-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/02-basicos-de-r/analise-de-conjuntura-usando-r/analise-de-conjuntura-usando-r.html)

#### Especialização em R
- [producao-de-relatorios-automaticos-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/03-especializacao-em-r/producao-de-relatorios-automaticos-usando-r/producao-de-relatorios-automaticos-usando-r.html)
- [producao-de-dashboards-automaticos-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/03-especializacao-em-r/producao-de-dashboards-automaticos-usando-r/producao-de-dashboards-automaticos-usando-r.html)
- [analise-de-series-temporais-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/03-especializacao-em-r/analise-de-series-temporais-usando-r/analise-de-series-temporais-usando-r.html)
- [macroeconometria-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/03-especializacao-em-r/macroeconometria-usando-r/macroeconometria-usando-r.html)
- [modelos-preditivos-de-machine-learning-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/03-especializacao-em-r/modelos-preditivos-de-machine-learning-usando-r/modelos-preditivos-de-machine-learning-usando-r.html)
- [mercado-financeiro-e-gestao-de-portfolios-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/03-especializacao-em-r/mercado-financeiro-e-gestao-de-portfolios-usando-r/mercado-financeiro-e-gestao-de-portfolios-usando-r.html)
- [analise-de-demonstrativos-financeiros-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/03-especializacao-em-r/analise-de-demonstrativos-financeiros-usando-r/analise-de-demonstrativos-financeiros-usando-r.html)
- [avaliacao-de-politicas-publicas-usando-r](https://analisemacropro.github.io/organizacao_ementas_am/03-especializacao-em-r/avaliacao-de-politicas-publicas-usando-r/avaliacao-de-politicas-publicas-usando-r.html)

#### Básicos de Python
- [programacao-em-python-para-analise-de-dados](https://analisemacropro.github.io/organizacao_ementas_am/04-basicos-de-python/programacao-em-python-para-analise-de-dados/programacao-em-python-para-analise-de-dados.html)
- [teoria-macroeconomica-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/04-basicos-de-python/teoria-macroeconomica-usando-python/teoria-macroeconomica-usando-python.html)
- [analise-de-conjuntura-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/04-basicos-de-python/analise-de-conjuntura-usando-python/analise-de-conjuntura-usando-python.html)
- [estatistica-para-analise-de-dados-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/04-basicos-de-python/estatistica-para-analise-de-dados-usando-python/estatistica-para-analise-de-dados-usando-python.html)
- [econometria-aplicada-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/04-basicos-de-python/econometria-aplicada-usando-python/econometria-aplicada-usando-python.html)
- [modelagem-e-previsao-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/04-basicos-de-python/modelagem-e-previsao-usando-python/modelagem-e-previsao-usando-python.html)

#### Especialização em Python
- [producao-de-relatorios-automaticos-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/05-especializacao-em-python/producao-de-relatorios-automaticos-usando-python/producao-de-relatorios-automaticos-usando-python.html)
- [producao-de-dashboards-automaticos-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/05-especializacao-em-python/producao-de-dashboards-automaticos-usando-python/producao-de-dashboards-automaticos-usando-python.html)
- [macroeconometria-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/05-especializacao-em-python/macroeconometria-usando-python/macroeconometria-usando-python.html)
- [mercado-financeiro-e-gestao-de-portfolios-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/05-especializacao-em-python/mercado-financeiro-e-gestao-de-portfolios-usando-python/mercado-financeiro-e-gestao-de-portfolios-usando-python.html)
- [python-para-investimentos](https://analisemacropro.github.io/organizacao_ementas_am/05-especializacao-em-python/python-para-investimentos/python-para-investimentos.html)
- [modelos-financeiros-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/05-especializacao-em-python/modelos-financeiros-usando-python/modelos-financeiros-usando-python.html)
- [analise-de-demonstrativos-financeiros-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/05-especializacao-em-python/analise-de-demonstrativos-financeiros-usando-python/analise-de-demonstrativos-financeiros-usando-python.html)
- [avaliacao-de-politicas-publicas-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/05-especializacao-em-python/avaliacao-de-politicas-publicas-usando-python/avaliacao-de-politicas-publicas-usando-python.html)
- [analise-de-series-temporais-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/05-especializacao-em-python/analise-de-series-temporais-usando-python/analise-de-series-temporais-usando-python.html)
- [fundamentos-de-engenharia-de-dados](https://analisemacropro.github.io/organizacao_ementas_am/05-especializacao-em-python/fundamentos-de-engenharia-de-dados/fundamentos-de-engenharia-de-dados.html)

#### Especialização em Inteligência Artificial
- [previsao-macroeconomica-usando-python-e-ia](https://analisemacropro.github.io/organizacao_ementas_am/06-especializacao-em-inteligencia-artificial/previsao-macroeconomica-usando-python-e-ia/previsao-macroeconomica-usando-python-e-ia.html)
- [ia-para-analise-de-dados-usando-python](https://analisemacropro.github.io/organizacao_ementas_am/06-especializacao-em-inteligencia-artificial/ia-para-analise-de-dados-usando-python/ia-para-analise-de-dados-usando-python.html)
- [inteligencia-artificial-para-todos](https://analisemacropro.github.io/organizacao_ementas_am/06-especializacao-em-inteligencia-artificial/inteligencia-artificial-para-todos/inteligencia-artificial-para-todos.html)
- [inteligencia-artificial-para-contadores-e-administradores](https://analisemacropro.github.io/organizacao_ementas_am/06-especializacao-em-inteligencia-artificial/inteligencia-artificial-para-contadores-e-administradores/inteligencia-artificial-para-contadores-e-administradores.html)
- [inteligencia-artificial-para-economistas](https://analisemacropro.github.io/organizacao_ementas_am/06-especializacao-em-inteligencia-artificial/inteligencia-artificial-para-economistas/inteligencia-artificial-para-economistas.html)

#### Workshops e Cursos Ao Vivo
- [imersao-claude-code](https://analisemacropro.github.io/organizacao_ementas_am/07-workshops-e-cursos-ao-vivo/imersao-claude-code/imersao-claude-code.html)
- [imersao-agentes-autonomos-para-analise-macro](https://analisemacropro.github.io/organizacao_ementas_am/07-workshops-e-cursos-ao-vivo/imersao-agentes-autonomos-para-analise-macro/imersao-agentes-autonomos-para-analise-macro.html)

#### Formações
- [formacao-como-pensar-com-dados](https://analisemacropro.github.io/organizacao_ementas_am/08-formacoes/formacao-como-pensar-com-dados/formacao-como-pensar-com-dados.html)
- [formacao-analista-de-pesquisa-quantitativa](https://analisemacropro.github.io/organizacao_ementas_am/08-formacoes/formacao-analista-de-pesquisa-quantitativa/formacao-analista-de-pesquisa-quantitativa.html)
- [formacao-em-analise-macroeconomica](https://analisemacropro.github.io/organizacao_ementas_am/08-formacoes/formacao-em-analise-macroeconomica/formacao-em-analise-macroeconomica.html)
- [formacao-python-e-automacao-para-o-mercado-financeiro](https://analisemacropro.github.io/organizacao_ementas_am/08-formacoes/formacao-python-e-automacao-para-o-mercado-financeiro/formacao-python-e-automacao-para-o-mercado-financeiro.html)
- [formacao-analista-de-dados-em-python](https://analisemacropro.github.io/organizacao_ementas_am/08-formacoes/formacao-analista-de-dados-em-python/formacao-analista-de-dados-em-python.html)
- [do-zero-a-analise-de-dados-economicos-e-financeiros-usando-a-linguagem-r](https://analisemacropro.github.io/organizacao_ementas_am/08-formacoes/do-zero-a-analise-de-dados-economicos-e-financeiros-usando-a-linguagem-r/do-zero-a-analise-de-dados-economicos-e-financeiros-usando-a-linguagem-r.html)
- [do-zero-a-analise-de-dados-economicos-e-financeiros-usando-python-e-ia](https://analisemacropro.github.io/organizacao_ementas_am/08-formacoes/do-zero-a-analise-de-dados-economicos-e-financeiros-usando-python-e-ia/do-zero-a-analise-de-dados-economicos-e-financeiros-usando-python-e-inteligencia-artificial.html)

## O dashboard de inscritos

Em [`dashboard/`](dashboard/) há um aplicativo que responde a uma pergunta prática: **quantos alunos inscritos cada curso e formação tem hoje?**

A loja (WooCommerce) registra os pedidos, mas o número bruto não responde isso diretamente — porque um mesmo produto teve vários nomes ao longo do tempo, porque comprar uma formação dá acesso a vários cursos, e porque a assinatura AM Black dá acesso a tudo. O dashboard resolve isso aplicando as regras de negócio da casa.

**O que ele faz:**
- Considera apenas pedidos **concluídos**.
- Reconhece cada produto mesmo quando o nome mudou ao longo dos anos (e ignora o que não é curso: livros, combos, mentorias, etc.).
- Respeita as **janelas de validade** das matrículas (cursos e formações têm prazos de acesso diferentes; matrículas expiradas não contam).
- **Propaga** corretamente: quem compra uma formação conta como inscrito em cada curso que ela contém; quem assina o AM Black conta em tudo.

**Como usar:** abra o aplicativo, envie o arquivo de pedidos exportado da loja e os números aparecem na hora — total de inscritos por curso e formação, com filtros por tipo e categoria e botões para exportar em CSV ou Excel. Nenhum dado de cliente fica armazenado: o app apenas lê o arquivo enviado e calcula.

Os detalhes técnicos (como rodar localmente, regras exatas e manutenção da lista de produtos) estão no [README do dashboard](dashboard/README.md).

---

*Análise Macro — organização interna do catálogo de cursos e formações.*
