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
pede mais login — até ele expirar (ver abaixo).

## Se pedir login de novo ("Token expirado ou revogado")

Enquanto a tela de consentimento OAuth estiver em modo **"Teste"**, o Google invalida o
*refresh token* a cada **7 dias**. Quando isso acontece, o script avisa e reabre o
navegador sozinho: basta autorizar de novo e ele segue.

Para parar de repetir esse login, publique o app no Google Cloud Console:
**APIs e Serviços → Tela de permissão OAuth → Publicar app** ("Em produção"). Como o app
é de uso interno e usa escopo do Sheets, a publicação não exige verificação do Google.

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
