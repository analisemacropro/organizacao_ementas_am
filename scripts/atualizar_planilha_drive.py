# -*- coding: utf-8 -*-
"""
Atualiza a MESMA planilha do Google Sheets (link fixo) com o conteúdo atual de
`Organizacao_Cursos_AM.csv`. Não cria arquivo novo: sobrescreve as células da
planilha existente, então o link nunca muda.

Planilha de destino (Google Sheets nativo, na pasta "Organização Produtos AM - Site"):
  https://docs.google.com/spreadsheets/d/1SQtDqY2kJLKF4V5EDwiVbtFBPT3lzfH1iShAJ6ecUe4/edit

Autenticação: OAuth de usuário (abre o navegador na 1ª vez, guarda token.json).

Uso:
    python scripts/atualizar_planilha_drive.py

Pré-requisitos (uma vez):
    pip install gspread google-auth-oauthlib
    Colocar o arquivo de credenciais OAuth do Google Cloud em scripts/credentials.json
    (ver scripts/README.md).
"""
from __future__ import annotations
import sys
from pathlib import Path

import pandas as pd
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------
SPREADSHEET_ID = "1SQtDqY2kJLKF4V5EDwiVbtFBPT3lzfH1iShAJ6ecUe4"
SHEET_NAME = "Cursos e Workshops"  # nome da aba (worksheet) de destino

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "Organizacao_Cursos_AM.csv"

AQUI = Path(__file__).resolve().parent
CRED = AQUI / "credentials.json"   # baixado do Google Cloud (OAuth client)
TOKEN = AQUI / "token.json"        # gerado na 1ª autorização; reaproveitado depois

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def _autenticar() -> Credentials:
    """OAuth de usuário: usa token.json se existir/for válido; senão, abre o navegador."""
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CRED.exists():
                sys.exit(
                    f"ERRO: falta o arquivo de credenciais OAuth em {CRED}\n"
                    "Baixe-o no Google Cloud Console (ver scripts/README.md)."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CRED), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN.write_text(creds.to_json(), encoding="utf-8")
    return creds


def main() -> None:
    if not CSV.exists():
        sys.exit(f"ERRO: não encontrei {CSV}")

    # lê o CSV de controle (utf-8-sig) e normaliza vazios
    df = pd.read_csv(CSV, encoding="utf-8-sig", dtype=str, keep_default_na=False)
    print(f"Lido {CSV.name}: {len(df)} linhas, {len(df.columns)} colunas.")

    creds = _autenticar()
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SPREADSHEET_ID)

    # pega (ou cria) a aba de destino
    try:
        ws = sh.worksheet(SHEET_NAME)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=SHEET_NAME, rows=len(df) + 10, cols=len(df.columns) + 2)

    # sobrescreve tudo: limpa e regrava (cabeçalho + dados) numa única chamada
    valores = [df.columns.tolist()] + df.values.tolist()
    ws.clear()
    ws.update(range_name="A1", values=valores)

    # garante que abas antigas/vazias não confundam: se houver uma "Sheet1"/"Página1" vazia
    # diferente da nossa, deixamos como está (não apagamos nada sem pedir).

    print(
        "OK — planilha atualizada (mesmo link):\n"
        f"  https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit"
    )


if __name__ == "__main__":
    main()
