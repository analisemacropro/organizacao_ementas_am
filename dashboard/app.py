# -*- coding: utf-8 -*-
"""
Dashboard de Inscritos — Análise Macro (Shiny for Python)

Você envia o export de pedidos (CSV do WooCommerce) e o app entrega o total de
inscritos por curso e formação, aplicando as regras de negócio da AM.

Rodar:
    shiny run dashboard/app.py --reload
    # ou, de dentro da pasta dashboard/:
    shiny run app.py --reload
Depois abra http://127.0.0.1:8000 no navegador.
"""
import io
from datetime import date, datetime
import pandas as pd
from shiny import App, reactive, render, ui

import logica
from relacao import CATEGORIA, JANELAS

CATEGORIAS = ["Todas"] + sorted(set(CATEGORIA.values()))

LOGO_AM = ("https://analisemacro.com.br/wp-content/uploads/2025/11/"
           "logo-analise-macro-branco-fundo-transparente.png")

# Paleta da identidade visual da Análise Macro (tema escuro / grafite)
COR = {
    "navy":      "#10141c",   # fundo principal (grafite escuro, neutro)
    "navy2":     "#1a2230",   # cartões / sidebar (cinza-azulado suave)
    "navy3":     "#2a3647",   # bordas / hover
    "ciano":     "#34d1bf",   # destaque (números/links)
    "ciano2":    "#5ad0e6",
    "amarelo":   "#f4b740",   # destaque secundário
    "texto":     "#e8eef5",
    "texto_mut": "#9fb3c8",
}

CSS = f"""
:root {{
  --navy:{COR['navy']}; --navy2:{COR['navy2']}; --navy3:{COR['navy3']};
  --ciano:{COR['ciano']}; --amarelo:{COR['amarelo']};
  --txt:{COR['texto']}; --txtmut:{COR['texto_mut']};
}}
body, .bslib-page-sidebar {{
  background: radial-gradient(1200px 600px at 80% -10%, #1c2533 0%, var(--navy) 55%);
  background-color: var(--navy); color:var(--txt);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }}

/* Cabeçalho com logo */
.am-header {{ display:flex; align-items:center; gap:18px; padding:18px 22px;
  background:linear-gradient(90deg,var(--navy2),var(--navy)); border-bottom:2px solid var(--navy3);
  border-radius:12px; margin-bottom:6px; }}
.am-header img {{ height:46px; }}
.am-header .t {{ font-size:22px; font-weight:700; color:#fff; line-height:1.1; }}
.am-header .s {{ font-size:13px; color:var(--txtmut); }}

/* Sidebar */
.sidebar, aside, .bslib-sidebar-layout > .sidebar {{ background:var(--navy2) !important;
  border-right:1px solid var(--navy3) !important; }}
.sidebar .form-label, .sidebar label, .sidebar .control-label {{ color:var(--txt) !important;
  font-weight:600; }}
.sidebar .form-text, .help-block, .shiny-input-container .help-text {{ color:var(--txtmut) !important; }}

/* Inputs */
.form-control, .selectize-input, .form-select, input, select {{
  background:var(--navy) !important; color:var(--txt) !important;
  border:1px solid var(--navy3) !important; }}
.selectize-dropdown {{ background:var(--navy2) !important; color:var(--txt) !important;
  border:1px solid var(--navy3) !important; }}
/* hover/seleção do dropdown do select: fundo escuro, não branco */
.selectize-dropdown .option {{ color:var(--txt) !important; background:transparent !important; }}
.selectize-dropdown .option:hover,
.selectize-dropdown .option.active,
.selectize-dropdown .active {{ background:var(--navy3) !important; color:#fff !important; }}
.form-select option:hover, .form-select option:checked {{ background:var(--navy3) !important; }}

/* Switch (Aplicar janelas) — toggle estilizado para o tema escuro */
.bslib-input-switch.form-switch input.form-check-input[role="switch"],
.form-switch input[type="checkbox"][role="switch"] {{
  width:2.6em !important; height:1.35em !important; margin-top:.15em !important;
  background-color:var(--navy3) !important;
  border:1px solid var(--navy3) !important; box-shadow:none !important;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='%239fb3c8'/%3e%3c/svg%3e") !important;
  cursor:pointer; appearance:none !important; -webkit-appearance:none !important; }}
.bslib-input-switch.form-switch input.form-check-input[role="switch"]:checked,
.form-switch input[type="checkbox"][role="switch"]:checked {{
  background-color:var(--ciano) !important; border-color:var(--ciano) !important;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='%2310141c'/%3e%3c/svg%3e") !important; }}
.form-switch input[role="switch"]:focus {{ box-shadow:0 0 0 .2rem rgba(52,209,191,.25) !important; }}

/* Radio / checkbox: marcador ciano e hover suave */
.form-check-input {{ background-color:var(--navy) !important; border:1px solid var(--navy3) !important; }}
.form-check-input:checked {{ background-color:var(--ciano) !important; border-color:var(--ciano) !important; }}
.form-check:hover, .form-check-label:hover {{ color:#fff !important; }}
.shiny-input-radiogroup .form-check:hover {{ background:rgba(255,255,255,.04); border-radius:6px; }}

/* Faixa do período */
.am-periodo {{ background:var(--navy2); border:1px solid var(--navy3); border-left:4px solid var(--ciano);
  border-radius:10px; padding:12px 16px; margin:10px 0 4px; color:var(--txt); font-size:14px; }}
.am-periodo b {{ color:var(--ciano); }}

/* Value boxes (KPIs) */
.bslib-value-box, .value-box {{ background:var(--navy2) !important; border:1px solid var(--navy3) !important;
  border-radius:14px !important; box-shadow:0 4px 14px rgba(0,0,0,.25); }}
.bslib-value-box .value-box-title, .value-box .value-box-title {{ color:var(--txtmut) !important;
  font-size:13px !important; font-weight:600; }}
.bslib-value-box .value-box-value, .value-box .value-box-value {{ color:var(--ciano) !important;
  font-size:34px !important; font-weight:800 !important; }}
.bslib-value-box .value-box-showcase, .bslib-value-box p {{ color:var(--txtmut) !important; }}

/* Cards / abas */
.card, .nav-tabs, .tab-content, .bslib-card {{ background:var(--navy2) !important;
  border:1px solid var(--navy3) !important; color:var(--txt) !important; border-radius:12px; }}
.nav-tabs .nav-link {{ color:var(--txtmut) !important; }}
.nav-tabs .nav-link.active {{ color:#fff !important; background:var(--navy3) !important;
  border-color:var(--navy3) !important; }}

/* Tabela de dados */
.shiny-data-grid, .shiny-data-grid table {{ color:var(--txt) !important; }}
.shiny-data-grid thead th {{ background:var(--navy3) !important; color:#fff !important; }}
.shiny-data-grid tbody tr td {{ background:var(--navy2) !important; color:var(--txt) !important;
  border-color:var(--navy3) !important; }}
.shiny-data-grid tbody tr:nth-child(even) td {{ background:#1f2937 !important; }}
/* HOVER da linha: fundo escuro de destaque + texto branco (não branco-no-branco) */
.shiny-data-grid tbody tr:hover td,
.shiny-data-grid tbody tr:hover {{ background:var(--navy3) !important; color:#fff !important; }}
/* célula selecionada */
.shiny-data-grid tbody td.selected, .shiny-data-grid tbody tr.selected td {{
  background:#26405e !important; color:#fff !important; }}
/* campos de filtro no topo das colunas */
.shiny-data-grid thead input {{ background:var(--navy) !important; color:var(--txt) !important;
  border:1px solid var(--navy3) !important; }}

/* Texto auxiliar / legendas */
.am-legenda {{ color:var(--txtmut); font-size:13px; line-height:1.5; margin:6px 0 12px; }}
.am-legenda b {{ color:var(--txt); }}
.am-chip {{ display:inline-block; background:var(--navy3); color:var(--ciano);
  border-radius:20px; padding:2px 10px; font-size:12px; margin-right:6px; }}
h5, .am-titulo {{ color:#fff; font-weight:700; }}
a {{ color:var(--ciano); }}

/* Barra de progresso do upload no tema (em vez do azul Bootstrap) */
.progress {{ background:var(--navy) !important; border:1px solid var(--navy3) !important; }}
.progress-bar {{ background:var(--ciano) !important; color:var(--navy) !important; font-weight:600; }}
.shiny-file-input-progress .progress-bar {{ background:var(--ciano) !important; color:var(--navy) !important; }}

/* botão "Procurar" do upload */
.btn-file, .input-group-text, .btn-default {{ background:var(--navy3) !important; color:var(--txt) !important;
  border:1px solid var(--navy3) !important; }}

/* botões de exportar */
.am-export {{ display:flex; align-items:center; gap:10px; margin:10px 0 14px; flex-wrap:wrap; }}
.am-btn, a.am-btn {{ background:var(--ciano) !important; color:var(--navy) !important;
  border:none !important; border-radius:8px !important; font-weight:700 !important;
  padding:8px 16px !important; cursor:pointer; text-decoration:none !important; }}
.am-btn:hover, a.am-btn:hover {{ filter:brightness(1.12); }}
"""

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h5("Configurações", class_="am-titulo"),
        ui.input_file(
            "arquivo", "1. Planilha de pedidos (CSV do WooCommerce)",
            accept=[".csv"], multiple=False, button_label="Procurar...",
            placeholder="Nenhum arquivo",
        ),
        ui.help_text("Exporte os pedidos da loja (WooCommerce) e envie aqui. "
                     "O app lê apenas; nada é alterado no arquivo."),
        ui.hr(),
        ui.input_date("hoje", "2. Data de referência (hoje):", value=date.today()),
        ui.help_text("Base para as janelas de validade. Pedidos anteriores ao "
                     "limite de cada tipo já expiraram e não contam."),
        ui.input_switch(
            "janela",
            "Aplicar janelas de validade",
            value=True,
        ),
        ui.help_text(
            f"Curso: últimos {JANELAS['curso']} meses · "
            f"Formação: {JANELAS['formacao']} meses · "
            f"AM Black: {JANELAS['amblack']} meses."
        ),
        ui.hr(),
        ui.h5("Filtros da tabela", class_="am-titulo"),
        ui.input_radio_buttons(
            "tipo", "3. Mostrar:",
            {"tudo": "Tudo", "Curso": "Só cursos", "Formação": "Só formações"},
        ),
        ui.input_select("categoria", "4. Categoria:", choices=CATEGORIAS),
        width=360,
    ),

    # Cabeçalho com a logo da AM
    ui.HTML(
        f"""<div class="am-header">
              <img src="{LOGO_AM}" alt="Análise Macro">
              <div>
                <div class="t">Dashboard de Inscritos</div>
                <div class="s">Total de alunos por curso e formação · a partir do export de pedidos</div>
              </div>
            </div>"""
    ),

    # Como funciona (explicação geral)
    ui.HTML(
        """<div class="am-legenda">
        <span class="am-chip">Como funciona</span>
        Envie o CSV de pedidos no painel à esquerda. O app conta apenas pedidos
        <b>concluídos</b>, identifica cada produto (mesmo com nomes antigos) e calcula
        o número de inscritos aplicando duas regras de propagação:
        toda <b>formação</b> soma +1 a cada curso que ela contém, e o
        <b>AM Black</b> (assinatura que dá acesso a tudo) soma +1 a todos os cursos e formações.
        A métrica é de <b>matrículas</b>, não de pessoas únicas.
        </div>"""
    ),

    # Período do documento
    ui.output_ui("periodo"),

    # KPIs
    ui.layout_columns(
        ui.value_box("Inscritos (soma de todos os itens)", ui.output_text("kpi_total")),
        ui.value_box("Cursos catalogados", ui.output_text("kpi_cursos")),
        ui.value_box("Formações catalogadas", ui.output_text("kpi_form")),
        ui.value_box("AM Black (somado a tudo)", ui.output_text("kpi_amblack")),
        col_widths=(3, 3, 3, 3),
    ),
    ui.HTML(
        """<div class="am-legenda">
        <b>Inscritos (soma)</b>: total de matrículas somando todas as linhas exibidas na tabela (com os filtros aplicados).
        <b>AM Black</b>: nº de assinaturas válidas — esse valor é somado em cada curso e formação.
        </div>"""
    ),

    # Abas
    ui.navset_card_tab(
        ui.nav_panel(
            "Inscritos por item",
            ui.HTML(
                """<div class="am-legenda" style="margin-top:10px">
                Cada linha é um curso ou formação do catálogo.
                <b>Inscritos diretos</b> = matrículas feitas no próprio item (vendas avulsas).
                <b>Inscritos (total)</b> = diretos + o que entra por formações que contêm o curso + AM Black.
                Para formações, "total" = diretos + AM Black (formação não recebe de outra formação).
                Clique no cabeçalho para ordenar; use os campos de filtro de cada coluna para buscar.
                </div>"""
            ),
            ui.div(
                ui.download_button("baixar_csv", "⬇ Exportar CSV", class_="am-btn"),
                ui.download_button("baixar_xlsx", "⬇ Exportar Excel", class_="am-btn"),
                ui.HTML('<span class="am-legenda" style="margin-left:8px">'
                        'Exporta a tabela como está na tela (com os filtros aplicados).</span>'),
                class_="am-export",
            ),
            ui.output_data_frame("tabela"),
        ),
        ui.nav_panel(
            "Itens ignorados (auditoria)",
            ui.HTML(
                """<div class="am-legenda" style="margin-top:10px">
                Nomes que apareceram no export mas <b>não contam</b>: livros, combos/kits,
                workshops avulsos, Clube AM, mentorias e produtos descontinuados.
                Se algum aqui <b>deveria</b> ser um curso/formação atual, é só mapeá-lo
                (adicionar um alias em <code>relacao.py</code>).
                </div>"""
            ),
            ui.output_data_frame("tab_ignorados"),
        ),
    ),
    ui.HTML(
        f"""<div class="am-legenda" style="text-align:center; margin-top:14px; opacity:.7">
        Análise Macro · Dashboard interno de inscritos · tema {COR['navy']}
        </div>"""
    ),

    ui.head_content(ui.tags.style(CSS)),
    title="Dashboard de Inscritos — Análise Macro",
    fillable=False,
)


# ---------------------------------------------------------------------------
# SERVER
# ---------------------------------------------------------------------------
def server(input, output, session):

    @reactive.calc
    def dados() -> pd.DataFrame:
        f = input.arquivo()
        if not f:
            return pd.DataFrame()
        path = f[0]["datapath"]
        try:
            return pd.read_csv(path, dtype=str, keep_default_na=False,
                               encoding="utf-8-sig")
        except UnicodeDecodeError:
            return pd.read_csv(path, dtype=str, keep_default_na=False,
                               encoding="latin-1")

    @reactive.calc
    def resultado():
        df = dados()
        if df.empty:
            return None
        hoje = datetime.combine(input.hoje(), datetime.min.time())
        try:
            return logica.calcular(df, hoje=hoje, aplicar_janela=input.janela())
        except ValueError as e:
            ui.notification_show(str(e), type="error", duration=8)
            return None

    @reactive.calc
    def tabela_filtrada() -> pd.DataFrame:
        r = resultado()
        if r is None:
            return pd.DataFrame(
                columns=["Nome", "Categoria", "Tipo",
                         "Inscritos_diretos", "Inscritos_total"]
            )
        t = r["tabela"]
        if input.tipo() in ("Curso", "Formação"):
            t = t[t["Tipo"] == input.tipo()]
        if input.categoria() != "Todas":
            t = t[t["Categoria"] == input.categoria()]
        return t.reset_index(drop=True)

    # ---- Período do documento ----
    @render.ui
    def periodo():
        r = resultado()
        if r is None:
            return ui.HTML(
                """<div class="am-periodo">📄 Nenhum arquivo carregado ainda —
                envie o CSV de pedidos no painel à esquerda para começar.</div>"""
            )
        dmin, dmax = r.get("data_min"), r.get("data_max")
        if dmin and dmax:
            periodo_txt = (f"<b>{dmin.strftime('%d/%m/%Y')}</b> a "
                           f"<b>{dmax.strftime('%d/%m/%Y')}</b>")
        else:
            periodo_txt = "datas não disponíveis no arquivo"
        return ui.HTML(
            f"""<div class="am-periodo">
            📄 <b>Período do documento:</b> pedidos de {periodo_txt}
            &nbsp;·&nbsp; {r['concluidos']:,} pedidos concluídos analisados.
            </div>""".replace(",", ".")
        )

    # ---- KPIs ----
    @render.text
    def kpi_total():
        t = tabela_filtrada()
        return f"{int(t['Inscritos_total'].sum()):,}".replace(",", ".") if len(t) else "—"

    @render.text
    def kpi_cursos():
        r = resultado()
        return str(int((r["tabela"]["Tipo"] == "Curso").sum())) if r else "—"

    @render.text
    def kpi_form():
        r = resultado()
        return str(int((r["tabela"]["Tipo"] == "Formação").sum())) if r else "—"

    @render.text
    def kpi_amblack():
        r = resultado()
        return str(r["am_black"]) if r else "—"

    # ---- Tabelas ----
    @render.data_frame
    def tabela():
        t = tabela_filtrada().rename(columns={
            "Inscritos_diretos": "Inscritos diretos",
            "Inscritos_total": "Inscritos (total)",
        })
        return render.DataGrid(t, width="100%", height="560px", filters=True)

    @render.data_frame
    def tab_ignorados():
        r = resultado()
        ig = r["ignorados"] if r else pd.DataFrame(
            columns=["Nome do item", "Pedidos"])
        return render.DataGrid(ig, width="100%", height="560px", filters=True)

    # ---- Exportar ----
    def _tabela_export() -> pd.DataFrame:
        return tabela_filtrada().rename(columns={
            "Inscritos_diretos": "Inscritos diretos",
            "Inscritos_total": "Inscritos (total)",
        })

    def _nome_arquivo(ext: str) -> str:
        ref = input.hoje().strftime("%Y-%m-%d")
        return f"inscritos_analise_macro_{ref}.{ext}"

    @render.download(filename=lambda: _nome_arquivo("csv"))
    def baixar_csv():
        # utf-8-sig (com BOM) para abrir certo no Excel com acentos
        yield _tabela_export().to_csv(index=False).encode("utf-8-sig")

    @render.download(filename=lambda: _nome_arquivo("xlsx"))
    def baixar_xlsx():
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            _tabela_export().to_excel(writer, index=False, sheet_name="Inscritos")
        buf.seek(0)
        yield buf.read()


app = App(app_ui, server)
