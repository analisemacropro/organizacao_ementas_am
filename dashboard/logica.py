# -*- coding: utf-8 -*-
"""
Lógica de cálculo de inscritos (independente da interface).

Recebe o DataFrame do export de pedidos (WooCommerce) e devolve o total de
inscritos por curso/formação, aplicando:
  - filtro de status "Concluído";
  - matching nome do item -> curso/formação (ALIASES); sem match = ignora;
  - janela de validade por tipo (curso 24m, formação 48m, AM Black 12m);
  - propagação: formação -> seus cursos; AM Black -> tudo.
"""
from __future__ import annotations
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from relacao import (
    NOMES, CATEGORIA, FORMACOES, FORMACAO_CURSOS, ALIASES, AM_BLACK, JANELAS,
)

# Nomes das colunas no export do WooCommerce
COL_STATUS = "Status do pedido"
COL_NOME = "Nome do item"
COL_DATA = "Data do pedido"
COL_QTD = "Quantidade (- reembolso)"

_FORMATOS_DATA = ("%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d")


def _parse_data(s) -> datetime | None:
    s = str(s).strip()
    for fmt in _FORMATOS_DATA:
        try:
            return datetime.strptime(s, fmt)
        except (ValueError, TypeError):
            continue
    return None


def _parse_qtd(v) -> int:
    s = str(v).strip().replace(",", ".")
    try:
        return int(float(s)) if s and s.lower() != "nan" else 1
    except ValueError:
        return 1


def _tipo(alvo: str) -> str:
    if alvo == AM_BLACK:
        return "amblack"
    if alvo in FORMACOES:
        return "formacao"
    return "curso"


def calcular(df: pd.DataFrame, hoje: datetime | None = None,
             aplicar_janela: bool = True):
    """
    Parâmetros
    ----------
    df : DataFrame do CSV de pedidos.
    hoje : data de referência para as janelas (default = agora).
    aplicar_janela : se False, ignora as janelas (conta tudo) — útil p/ auditoria.

    Retorna
    -------
    dict com:
      'tabela'   : DataFrame [Nome, Categoria, Tipo, Inscritos_diretos, Inscritos_total]
      'am_black' : inscrições de AM Black na janela (propagadas a tudo)
      'ignorados': DataFrame [Nome do item, Pedidos] (não casaram)
      'concluidos': nº de linhas com status Concluído
    """
    if hoje is None:
        hoje = datetime.now()

    faltando = [c for c in (COL_STATUS, COL_NOME) if c not in df.columns]
    if faltando:
        raise ValueError(
            "O CSV não parece ser o export de pedidos. Faltam colunas: "
            + ", ".join(faltando)
        )

    df = df[df[COL_STATUS].astype(str).str.strip() == "Concluído"].copy()
    n_concluidos = len(df)

    direto = {n: 0 for n in NOMES}
    am_black = 0
    ignorados: dict[str, int] = {}

    tem_data = COL_DATA in df.columns
    tem_qtd = COL_QTD in df.columns

    # período do documento: menor e maior data entre os pedidos concluídos
    data_min = data_max = None
    if tem_data:
        datas = [d for d in (_parse_data(v) for v in df[COL_DATA]) if d is not None]
        if datas:
            data_min, data_max = min(datas), max(datas)

    for _, row in df.iterrows():
        nome = str(row[COL_NOME]).strip()
        alvo = ALIASES.get(nome)
        if alvo is None:
            ignorados[nome] = ignorados.get(nome, 0) + 1
            continue
        q = _parse_qtd(row[COL_QTD]) if tem_qtd else 1
        tp = _tipo(alvo)
        if aplicar_janela and tem_data:
            d = _parse_data(row[COL_DATA])
            if d is None or d < hoje - relativedelta(months=JANELAS[tp]):
                continue
        if alvo == AM_BLACK:
            am_black += q
        else:
            direto[alvo] += q

    total = dict(direto)
    # 1) formação propaga aos cursos que contém
    for formacao, lista in FORMACAO_CURSOS.items():
        insc = direto.get(formacao, 0)
        if insc:
            for c in lista:
                if c in total:
                    total[c] += insc
    # 2) AM Black propaga a tudo
    if am_black:
        for n in total:
            total[n] += am_black

    tabela = pd.DataFrame({
        "Nome": NOMES,
        "Categoria": [CATEGORIA[n] for n in NOMES],
        "Tipo": ["Formação" if n in FORMACOES else "Curso" for n in NOMES],
        "Inscritos_diretos": [direto[n] for n in NOMES],
        "Inscritos_total": [total[n] for n in NOMES],
    }).sort_values("Inscritos_total", ascending=False, ignore_index=True)

    ign_df = (
        pd.DataFrame(sorted(ignorados.items(), key=lambda x: -x[1]),
                     columns=["Nome do item", "Pedidos"])
        if ignorados else pd.DataFrame(columns=["Nome do item", "Pedidos"])
    )

    return {
        "tabela": tabela,
        "am_black": am_black,
        "ignorados": ign_df,
        "concluidos": n_concluidos,
        "data_min": data_min,
        "data_max": data_max,
    }
