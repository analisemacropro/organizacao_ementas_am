# -*- coding: utf-8 -*-
"""
Relação Formação -> Cursos da Análise Macro + método de cálculo de inscritos.

Regra de negócio (ver memória dashboard-inscritos-regras):
- Métrica = inscrições/matrículas (não pessoas únicas).
- Formação PROPAGA aos cursos: 1 inscrito numa formação conta +1 na formação
  E +1 em cada curso que ela contém.
- Inscritos de um curso = inscritos avulsos + soma dos inscritos das formações que o incluem.
- AM Black (assinatura) NÃO entra na contagem.
- Janelas de acesso: formações 48 meses; cursos 24 meses; AM Black anual.

Este arquivo define a RELAÇÃO (estrutura) e um cálculo de referência em Python.
O dashboard final será em Shiny (R) e usará a mesma relação.

Os nomes de curso usados aqui são EXATAMENTE os da coluna "Nome" da planilha
(Organizacao_Cursos_AM.csv). Itens dos blocos das formações que NÃO são cursos
da planilha (workshops, imersões, práticas, mentorias, Clube AM, cursos ainda
inexistentes como "SQL para Economia e Finanças" ou "Fundamentos de Análise de
Dados") ficam listados em ITENS_NAO_CURSO para rastreabilidade, mas não entram
na propagação.
"""

import csv, os, sys, unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(ROOT, "Organizacao_Cursos_AM.csv")

# ---------------------------------------------------------------------------
# 1) RELAÇÃO FORMAÇÃO -> CURSOS DA PLANILHA
#    Chave = nome da formação (igual à planilha).
#    Valor = lista de nomes de curso (iguais à coluna "Nome" da planilha) que a
#    formação contém. Nomes já normalizados para casar com a planilha.
# ---------------------------------------------------------------------------
FORMACAO_CURSOS = {
    "Formação Como Pensar com Dados": [
        "Como Pensar com Dados",
        "SQL para Negócios e Tomada de Decisão",
        "Programação em Python para Análise de Dados",
        "Fundamentos de Engenharia de Dados",
        "Inteligência Artificial para Todos",
        # Bloco 6 (Power BI / Streamlit) não é curso da planilha -> ITENS_NAO_CURSO
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
        # "Dados em Painel usando R" e "Econometria Financeira usando R" foram
        # removidos da planilha -> ficam em ITENS_NAO_CURSO
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

# Itens citados nos blocos das formações que NÃO são cursos da planilha
# (registrados para rastreabilidade; não entram na propagação).
ITENS_NAO_CURSO = [
    "SQL para Economia e Finanças",
    "Fundamentos de Análise de Dados",
    "Clube AM / Acesso ao Clube AM",
    "Construção de Portfólio de Data Science / Macroeconômico",
    "Dados em Painel usando R (removido da planilha)",
    "Econometria Financeira usando R (removido da planilha)",
    "Workshops, imersões, mentorias e práticas (itens 'Workshop:', 'Imersão:', "
    "'Prática:', 'Mentoria', 'Boas-Vindas')",
    "Power BI / Streamlit (Bloco 6 da Formação Como Pensar com Dados)",
]


# ---------------------------------------------------------------------------
# 2) Utilidades
# ---------------------------------------------------------------------------
def carregar_planilha(caminho=CSV):
    """Lê a planilha e retorna (header, rows[list[dict]])."""
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return reader.fieldnames, rows


def validar_relacao(rows):
    """Confere que todo curso citado na relação existe na planilha."""
    nomes_planilha = {r["Nome"] for r in rows}
    problemas = []
    for formacao, cursos in FORMACAO_CURSOS.items():
        if formacao not in nomes_planilha:
            problemas.append(f"FORMAÇÃO ausente na planilha: {formacao}")
        for c in cursos:
            if c not in nomes_planilha:
                problemas.append(f"  curso não encontrado na planilha: '{c}' (em {formacao})")
    return problemas


# ---------------------------------------------------------------------------
# 3) CÁLCULO DE INSCRITOS (com propagação formação -> cursos)
# ---------------------------------------------------------------------------
def calcular_inscritos(rows, col_inscritos="Número de Alunos"):
    """
    Recebe as linhas da planilha (cada uma com inscritos DIRETOS/avulsos no
    campo col_inscritos) e devolve um dict nome -> total de inscritos.

    - Curso: total = inscritos avulsos do curso + soma dos inscritos de cada
      formação que o contém (propagação).
    - Formação: total = seus próprios inscritos diretos (não recebe propagação).
    - Demais itens (ex.: AM Black, se existir como linha): ficam de fora.
    """
    def parse(v):
        v = (v or "").strip().replace(".", "").replace(",", ".")
        try:
            return int(float(v)) if v else 0
        except ValueError:
            return 0

    diretos = {r["Nome"]: parse(r.get(col_inscritos, "")) for r in rows}

    total = dict(diretos)  # começa com os diretos
    # propaga cada formação para os cursos que ela contém
    for formacao, cursos in FORMACAO_CURSOS.items():
        insc_formacao = diretos.get(formacao, 0)
        if insc_formacao:
            for c in cursos:
                if c in total:
                    total[c] += insc_formacao
    return total


# ---------------------------------------------------------------------------
# 4) Execução: valida a relação e imprime um resumo
# ---------------------------------------------------------------------------
def main():
    header, rows = carregar_planilha()
    print(f"Planilha: {len(rows)} linhas de produto.")
    print(f"Formações mapeadas: {len(FORMACAO_CURSOS)}")
    print()

    problemas = validar_relacao(rows)
    if problemas:
        print("⚠️  PROBLEMAS na relação (corrigir os nomes):")
        for p in problemas:
            print("  -", p)
    else:
        print("✅ Relação validada: todos os cursos citados existem na planilha.")
    print()

    # Quantos cursos cada formação contém e quais cursos pertencem a alguma formação
    print("Cursos por formação:")
    for f, cs in FORMACAO_CURSOS.items():
        print(f"  {len(cs):2d}  {f}")
    print()

    cursos_em_formacao = set()
    for cs in FORMACAO_CURSOS.values():
        cursos_em_formacao.update(cs)
    todos_cursos = [r["Nome"] for r in rows
                    if r["Categoria"] not in ("Formações",)
                    and not r["Nome"].startswith("Imersão")]
    avulsos = [c for c in todos_cursos if c not in cursos_em_formacao]
    print(f"Cursos que pertencem a >=1 formação: {len(cursos_em_formacao & set(todos_cursos))}")
    print(f"Cursos que NÃO entram em nenhuma formação (só avulso): {len(avulsos)}")
    for c in avulsos:
        print("   -", c)


if __name__ == "__main__":
    main()
