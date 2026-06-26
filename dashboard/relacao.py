# -*- coding: utf-8 -*-
"""
Dados (a "fonte da verdade" do dashboard):
  - CURSOS: os 46 itens da planilha (nome + categoria).
  - FORMACAO_CURSOS: quais cursos cada formação contém.
  - ALIASES: nome no export WooCommerce -> nome do curso/formação na planilha
             (ou AM_BLACK). Cobre variações históricas de nome.

Para incluir um produto novo ou um nome diferente que apareça no export,
adicione uma linha em ALIASES. A aba "Itens ignorados" do app mostra o que
ainda não foi mapeado.
"""

# Marcador especial: assinatura que dá acesso a TUDO (propaga a todos os itens)
AM_BLACK = "__AM_BLACK__"

# Janelas de validade da matrícula, em meses, a partir da data de referência.
JANELAS = {"curso": 24, "formacao": 48, "amblack": 12}

# ---------------------------------------------------------------------------
# Os 46 itens da planilha: (nome, categoria)
# ---------------------------------------------------------------------------
CURSOS = [
    ("SQL para Negócios e Tomada de Decisão", "Básicos fundamentais"),
    ("Como Pensar com Dados", "Básicos fundamentais"),
    ("Programação em R para Análise de Dados", "Básicos de R"),
    ("Teoria Macroeconômica usando R", "Básicos de R"),
    ("Estatística para Análise de Dados usando R", "Básicos de R"),
    ("Econometria Aplicada usando R", "Básicos de R"),
    ("Modelagem e Previsão usando R", "Básicos de R"),
    ("Análise de Conjuntura usando R", "Básicos de R"),
    ("Produção de Relatórios Automáticos usando R", "Especialização em R"),
    ("Produção de Dashboards Automáticos usando R", "Especialização em R"),
    ("Análise de Séries Temporais usando R", "Especialização em R"),
    ("Macroeconometria usando R", "Especialização em R"),
    ("Modelos Preditivos de Machine Learning usando R", "Especialização em R"),
    ("Mercado Financeiro e Gestão de Portfólios usando R", "Especialização em R"),
    ("Análise de Demonstrativos Financeiros usando R", "Especialização em R"),
    ("Avaliação de Políticas Públicas usando R", "Especialização em R"),
    ("Programação em Python para Análise de Dados", "Básicos de Python"),
    ("Teoria Macroeconômica usando Python", "Básicos de Python"),
    ("Análise de Conjuntura usando Python", "Básicos de Python"),
    ("Estatística para Análise de Dados usando Python", "Básicos de Python"),
    ("Econometria Aplicada usando Python", "Básicos de Python"),
    ("Modelagem e Previsão usando Python", "Básicos de Python"),
    ("Produção de Relatórios Automáticos usando Python", "Especialização em Python"),
    ("Produção de Dashboards Automáticos usando Python", "Especialização em Python"),
    ("Macroeconometria usando Python", "Especialização em Python"),
    ("Mercado Financeiro e Gestão de Portfólios usando Python", "Especialização em Python"),
    ("Python para Investimentos", "Especialização em Python"),
    ("Modelos Financeiros usando Python", "Especialização em Python"),
    ("Análise de Demonstrativos Financeiros usando Python", "Especialização em Python"),
    ("Avaliação de Políticas Públicas usando Python", "Especialização em Python"),
    ("Análise de Séries Temporais usando Python", "Especialização em Python"),
    ("Fundamentos de Engenharia de Dados", "Especialização em Python"),
    ("Previsão Macroeconômica usando Python e IA", "Especialização em Inteligência Artificial"),
    ("IA para Análise de Dados usando Python", "Especialização em Inteligência Artificial"),
    ("Inteligência Artificial para Todos", "Especialização em Inteligência Artificial"),
    ("Inteligência Artificial para Contadores e Administradores", "Especialização em Inteligência Artificial"),
    ("Inteligência Artificial para Economistas", "Especialização em Inteligência Artificial"),
    ("Imersão Claude Code", "Workshops e Cursos Ao Vivo"),
    ("Imersão Agentes Autônomos para Análise Macro", "Workshops e Cursos Ao Vivo"),
    ("Formação Como Pensar com Dados", "Formações"),
    ("Formação Analista de Pesquisa Quantitativa", "Formações"),
    ("Formação em Análise Macroeconômica", "Formações"),
    ("Formação Python e Automação para o Mercado Financeiro", "Formações"),
    ("Formação Analista de Dados em Python", "Formações"),
    ("Do Zero à Análise de Dados Econômicos e Financeiros usando a Linguagem R", "Formações"),
    ("Do Zero à Análise de Dados Econômicos e Financeiros usando Python e Inteligência Artificial", "Formações"),
]

CATEGORIA = {nome: cat for nome, cat in CURSOS}
NOMES = [nome for nome, _ in CURSOS]

# ---------------------------------------------------------------------------
# Relação formação -> cursos que ela contém (nomes iguais aos de CURSOS).
# Só entram cursos que existem na planilha; itens como workshops, práticas,
# Clube AM, "SQL para Economia e Finanças" etc. ficam de fora (não contáveis).
# ---------------------------------------------------------------------------
FORMACAO_CURSOS = {
    "Formação Como Pensar com Dados": [
        "Como Pensar com Dados",
        "SQL para Negócios e Tomada de Decisão",
        "Programação em Python para Análise de Dados",
        "Fundamentos de Engenharia de Dados",
        "Inteligência Artificial para Todos",
    ],
    "Formação Analista de Pesquisa Quantitativa": [
        "Programação em Python para Análise de Dados",
        "Programação em R para Análise de Dados",
        "Estatística para Análise de Dados usando Python",
        "Estatística para Análise de Dados usando R",
        "Econometria Aplicada usando Python",
        "Econometria Aplicada usando R",
        "Modelagem e Previsão usando Python",
        "Modelagem e Previsão usando R",
        "Análise de Séries Temporais usando Python",
        "Análise de Séries Temporais usando R",
        "Inteligência Artificial para Todos",
        "IA para Análise de Dados usando Python",
        "Inteligência Artificial para Economistas",
    ],
    "Formação em Análise Macroeconômica": [
        "Como Pensar com Dados",
        "SQL para Negócios e Tomada de Decisão",
        "Programação em R para Análise de Dados",
        "Programação em Python para Análise de Dados",
        "Teoria Macroeconômica usando R",
        "Teoria Macroeconômica usando Python",
        "Análise de Conjuntura usando R",
        "Análise de Conjuntura usando Python",
        "Estatística para Análise de Dados usando R",
        "Estatística para Análise de Dados usando Python",
        "Econometria Aplicada usando Python",
        "Econometria Aplicada usando R",
        "Modelagem e Previsão usando R",
        "Modelagem e Previsão usando Python",
        "Análise de Séries Temporais usando R",
        "Análise de Séries Temporais usando Python",
        "Macroeconometria usando R",
        "Macroeconometria usando Python",
        "Modelos Preditivos de Machine Learning usando R",
        "Previsão Macroeconômica usando Python e IA",
        "Inteligência Artificial para Economistas",
    ],
    "Formação Python e Automação para o Mercado Financeiro": [
        "Como Pensar com Dados",
        "SQL para Negócios e Tomada de Decisão",
        "Programação em Python para Análise de Dados",
        "Modelagem e Previsão usando Python",
        "Modelos Financeiros usando Python",
    ],
    "Formação Analista de Dados em Python": [
        "Programação em Python para Análise de Dados",
        "Inteligência Artificial para Todos",
        "Estatística para Análise de Dados usando Python",
        "Modelagem e Previsão usando Python",
        "Produção de Dashboards Automáticos usando Python",
        "Produção de Relatórios Automáticos usando Python",
    ],
    "Do Zero à Análise de Dados Econômicos e Financeiros usando a Linguagem R": [
        "Como Pensar com Dados",
        "SQL para Negócios e Tomada de Decisão",
        "Programação em R para Análise de Dados",
        "Teoria Macroeconômica usando R",
        "Análise de Conjuntura usando R",
        "Estatística para Análise de Dados usando R",
        "Econometria Aplicada usando R",
        "Modelagem e Previsão usando R",
        "Produção de Dashboards Automáticos usando R",
        "Produção de Relatórios Automáticos usando R",
        "Análise de Séries Temporais usando R",
        "Macroeconometria usando R",
        "Modelos Preditivos de Machine Learning usando R",
        "Mercado Financeiro e Gestão de Portfólios usando R",
        "Análise de Demonstrativos Financeiros usando R",
        "Avaliação de Políticas Públicas usando R",
    ],
    "Do Zero à Análise de Dados Econômicos e Financeiros usando Python e Inteligência Artificial": [
        "Como Pensar com Dados",
        "SQL para Negócios e Tomada de Decisão",
        "Programação em Python para Análise de Dados",
        "Teoria Macroeconômica usando Python",
        "Análise de Conjuntura usando Python",
        "Estatística para Análise de Dados usando Python",
        "Econometria Aplicada usando Python",
        "Modelagem e Previsão usando Python",
        "Produção de Dashboards Automáticos usando Python",
        "Produção de Relatórios Automáticos usando Python",
        "Python para Investimentos",
        "Mercado Financeiro e Gestão de Portfólios usando Python",
        "Análise de Demonstrativos Financeiros usando Python",
        "Modelos Financeiros usando Python",
        "Macroeconometria usando Python",
        "Avaliação de Políticas Públicas usando Python",
        "IA para Análise de Dados usando Python",
        "Previsão Macroeconômica usando Python e IA",
    ],
}

FORMACOES = set(FORMACAO_CURSOS.keys())

# ---------------------------------------------------------------------------
# ALIASES: nome no export (exato) -> nome do curso/formação na planilha (ou AM_BLACK)
# ---------------------------------------------------------------------------
ALIASES = {
    # AM Black (propaga para tudo)
    "AM Black": AM_BLACK,
    "AM Black - Assinatura Anual": AM_BLACK,

    # Básicos fundamentais
    "Como Pensar com Dados": "Como Pensar com Dados",
    "SQL para Negócios e Tomada de Decisão": "SQL para Negócios e Tomada de Decisão",

    # Programação
    "Programação em R para Análise de Dados": "Programação em R para Análise de Dados",
    "R para Análise de Dados": "Programação em R para Análise de Dados",
    "Programação em Python para Análise de Dados": "Programação em Python para Análise de Dados",
    "Python para Análise de Dados": "Programação em Python para Análise de Dados",

    # Teoria Macroeconômica
    "Teoria Macroeconômica usando R": "Teoria Macroeconômica usando R",
    "Teoria Macroeconômica com a Linguagem R": "Teoria Macroeconômica usando R",
    "Teoria Macroeconômica usando Python": "Teoria Macroeconômica usando Python",
    "Teoria Macroeconômica com Python": "Teoria Macroeconômica usando Python",

    # Análise de Conjuntura
    "Análise de Conjuntura usando R": "Análise de Conjuntura usando R",
    "Análise de Conjuntura usando Python": "Análise de Conjuntura usando Python",

    # Estatística
    "Estatística para Análise de Dados usando R": "Estatística para Análise de Dados usando R",
    "Estatística para Análise de Dados usando Python": "Estatística para Análise de Dados usando Python",

    # Econometria Aplicada
    "Econometria Aplicada usando R": "Econometria Aplicada usando R",
    "Econometria Aplicada usando Python": "Econometria Aplicada usando Python",

    # Modelagem e Previsão
    "Modelagem e Previsão usando R": "Modelagem e Previsão usando R",
    "Modelagem e Previsão (R)": "Modelagem e Previsão usando R",
    "Modelagem e Previsão usando Python": "Modelagem e Previsão usando Python",

    # Séries Temporais
    "Análise de Séries Temporais usando R": "Análise de Séries Temporais usando R",
    "Análise de Séries Temporais (R)": "Análise de Séries Temporais usando R",
    "Análise de Séries Temporais usando Python": "Análise de Séries Temporais usando Python",

    # Macroeconometria
    "Macroeconometria usando R": "Macroeconometria usando R",
    "Macroeconometria usando Python": "Macroeconometria usando Python",

    # Modelos Preditivos de ML usando R
    "Modelos Preditivos de Machine Learning usando R": "Modelos Preditivos de Machine Learning usando R",
    "Modelos Preditivos de Machine Learning": "Modelos Preditivos de Machine Learning usando R",
    "Modelos Preditivos aplicados à Macroeconomia": "Modelos Preditivos de Machine Learning usando R",
    "Modelos Machine Learning (R)": "Modelos Preditivos de Machine Learning usando R",
    "Machine Learning usando R": "Modelos Preditivos de Machine Learning usando R",

    # Mercado Financeiro e Gestão de Portfólios
    "Mercado Financeiro e Gestão de Portfólios usando R": "Mercado Financeiro e Gestão de Portfólios usando R",
    "Mercado Financeiro e Gestão de Portfólio usando R": "Mercado Financeiro e Gestão de Portfólios usando R",
    "Mercado Financeiro e Gestão de Portfólio (R)": "Mercado Financeiro e Gestão de Portfólios usando R",
    "R para o Mercado Financeiro": "Mercado Financeiro e Gestão de Portfólios usando R",
    "Mercado Financeiro e Gestão de Portfólios usando Python": "Mercado Financeiro e Gestão de Portfólios usando Python",
    "Mercado Financeiro e Gestão de Portfólios com Python": "Mercado Financeiro e Gestão de Portfólios usando Python",

    # Análise de Demonstrativos Financeiros
    "Análise de Demonstrativos Financeiros usando R": "Análise de Demonstrativos Financeiros usando R",
    "Análise de Demonstrativos Financeiros com a Linguagem R": "Análise de Demonstrativos Financeiros usando R",
    "Análise de Demonstrativos Financeiros usando Python": "Análise de Demonstrativos Financeiros usando Python",
    "Análise de Demonstrativos Financeiros com Python": "Análise de Demonstrativos Financeiros usando Python",

    # Avaliação de Políticas Públicas
    "Avaliação de Políticas Públicas usando R": "Avaliação de Políticas Públicas usando R",
    "Avaliação de Políticas Públicas usando Python": "Avaliação de Políticas Públicas usando Python",

    # Python para Investimentos / Macro p/ Investimentos
    "Python para Investimentos": "Python para Investimentos",
    "Macroeconomia para Investimentos com Python": "Python para Investimentos",
    "Macroeconomia para Investimentos usando Python": "Python para Investimentos",

    # Modelos Financeiros usando Python
    "Modelos Financeiros usando Python": "Modelos Financeiros usando Python",

    # Fundamentos de Engenharia de Dados
    "Fundamentos de Engenharia de Dados": "Fundamentos de Engenharia de Dados",

    # IA
    "Inteligência Artificial para Todos": "Inteligência Artificial para Todos",
    "Inteligência Artificial para Análise de Dados usando Python": "IA para Análise de Dados usando Python",
    "Inteligência Artificial para Contadores e Administradores": "Inteligência Artificial para Contadores e Administradores",
    "Inteligência Artificial para Economistas": "Inteligência Artificial para Economistas",
    "Previsão Macroeconômica usando Python e Inteligência Artificial": "Previsão Macroeconômica usando Python e IA",

    # Produção de Dashboards / Relatórios
    "Produção de Dashboards Automáticos usando R": "Produção de Dashboards Automáticos usando R",
    "Produção de Dashboards Automáticos usando Python": "Produção de Dashboards Automáticos usando Python",
    "Produção de Relatórios Automáticos usando R": "Produção de Relatórios Automáticos usando R",
    "Produção de Relatórios Automáticos usando Python": "Produção de Relatórios Automáticos usando Python",

    # Imersões (Workshops e Cursos Ao Vivo) — produtos da planilha
    "Imersão Claude Code": "Imersão Claude Code",
    "Imersão Claude Code para Economistas": "Imersão Claude Code",
    "Imersão Claude Code para Economistas, Administradores e Contadores": "Imersão Claude Code",
    "Imersão Agentes Autônomos para Análise Macro": "Imersão Agentes Autônomos para Análise Macro",
    # OBS: "Imersão Como Criar um Agente de IA Econometrista", "Imersão Econometria
    # vs. IA na Previsão Macro" e "Imersão IA com Python" NÃO são produtos da
    # planilha -> ficam ignorados de propósito.

    # Formações (nomes históricos -> formação atual da planilha)
    "Formação Como Pensar com Dados": "Formação Como Pensar com Dados",
    "Formação em Análise Macroeconômica": "Formação em Análise Macroeconômica",
    "Formação em Análise Macroeconômica  usando Python e IA": "Formação em Análise Macroeconômica",
    "Formação Analista Macroeconômico": "Formação em Análise Macroeconômica",
    "Formação Python e Automação para o Mercado Financeiro": "Formação Python e Automação para o Mercado Financeiro",
    "Formação Analista de Dados em Python e IA": "Formação Analista de Dados em Python",
    "Analista de Pesquisa Quantitativa": "Formação Analista de Pesquisa Quantitativa",
    "Formação em Pesquisa Macroeconômica": "Formação em Análise Macroeconômica",
    "Formação em Pesquisa Macroeconômica usando Inteligência Artificial e Python": "Formação em Análise Macroeconômica",
    # "Do Zero..." longo (Econômicos e Financeiros) -> formações Do Zero (R / Python e IA)
    "Do Zero à Análise de Dados Econômicos e Financeiros usando a Linguagem R": "Do Zero à Análise de Dados Econômicos e Financeiros usando a Linguagem R",
    "Do Zero à Análise de Dados Econômicos e Financeiros com a Linguagem R": "Do Zero à Análise de Dados Econômicos e Financeiros usando a Linguagem R",
    "Do Zero à Análise de Dados Econômicos e Financeiros usando R": "Do Zero à Análise de Dados Econômicos e Financeiros usando a Linguagem R",
    "Do Zero à Análise de Dados Econômicos e Financeiros usando Python e IA": "Do Zero à Análise de Dados Econômicos e Financeiros usando Python e Inteligência Artificial",
    "Do Zero à Análise de Dados Econômicos e Financeiros usando Python": "Do Zero à Análise de Dados Econômicos e Financeiros usando Python e Inteligência Artificial",
    "Do Zero à Análise de Dados Econômicos e Financeiros com Python": "Do Zero à Análise de Dados Econômicos e Financeiros usando Python e Inteligência Artificial",
    # "Do Zero à Análise de Dados ..." CURTO (sem "Econômicos e Financeiros"):
    #   versão Python -> Formação Analista de Dados em Python
    #   versão R      -> Do Zero ... usando a Linguagem R
    "Do Zero à Análise de Dados com Python": "Formação Analista de Dados em Python",
    "Do Zero à Análise de Dados usando Python": "Formação Analista de Dados em Python",
    "Do Zero à Análise de Dados com a Linguagem R": "Do Zero à Análise de Dados Econômicos e Financeiros usando a Linguagem R",
    "Do Zero à Análise de Dados com a Linguagem R ": "Do Zero à Análise de Dados Econômicos e Financeiros usando a Linguagem R",
}
