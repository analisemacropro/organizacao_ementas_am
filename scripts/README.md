# Atualizar a planilha no Google Sheets (link fixo)

O script `atualizar_planilha_drive.py` pega o `Organizacao_Cursos_AM.csv` (na raiz do
projeto) e sobrescreve a **mesma** planilha do Google Sheets — o link nunca muda:

<https://docs.google.com/spreadsheets/d/1SQtDqY2kJLKF4V5EDwiVbtFBPT3lzfH1iShAJ6ecUe4/edit>

## Como usar (depois de configurado)

```bash
pip install gspread google-auth-oauthlib      # só na 1ª vez
python scripts/atualizar_planilha_drive.py
```

Na 1ª execução abre o navegador para você autorizar com a conta
`analisemacro.cloud@gmail.com`. Depois disso, o `token.json` é reaproveitado e não
pede mais login.

## Configuração inicial (uma vez) — credencial OAuth

1. Acesse <https://console.cloud.google.com/> logado como `analisemacro.cloud@gmail.com`.
2. Crie (ou selecione) um projeto qualquer.
3. Menu **APIs e Serviços → Biblioteca** → procure **Google Sheets API** → **Ativar**.
4. **APIs e Serviços → Tela de permissão OAuth**: configure como **Externo** (ou Interno,
   se for Workspace), preencha o nome do app e o e-mail de suporte. Em "Usuários de teste",
   adicione `analisemacro.cloud@gmail.com`.
5. **APIs e Serviços → Credenciais → Criar credenciais → ID do cliente OAuth**:
   - Tipo de aplicativo: **App para computador (Desktop app)**.
   - Baixe o JSON e salve como **`scripts/credentials.json`**.
6. Rode `python scripts/atualizar_planilha_drive.py` e autorize no navegador.

## Segurança

`credentials.json` e `token.json` são **chaves** — já estão no `.gitignore` e **não** vão
para o GitHub. Não compartilhe esses arquivos.
