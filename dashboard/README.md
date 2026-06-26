# Dashboard de Inscritos — Análise Macro

App **Shiny for Python** que lê o **export de pedidos do WooCommerce** e calcula o **total de inscritos** por curso e formação, aplicando as regras de negócio da AM. Você sobe o CSV no app e os números aparecem na hora.

## Como rodar

```bash
# 1) instalar dependências (uma vez)
pip install -r dashboard/requirements.txt

# 2) rodar o app
shiny run dashboard/app.py --reload
```

Abra **http://127.0.0.1:8000** no navegador, clique em **Procurar** e envie o CSV de pedidos (ex.: `orders-AAAA-MM-DD.csv`). Os números aparecem com KPIs e filtros (tipo, categoria).

## Regras de cálculo

1. **Só pedidos com status "Concluído"** entram.
2. **Matching:** cada *Nome do item* do export é mapeado para um curso/formação da planilha via `ALIASES` (cobre variações históricas de nome). **Nome sem correspondência é ignorado** (livros, combos, kits, workshops avulsos, Clube AM, etc.). A aba **"Itens ignorados"** mostra o que não casou.
3. **Janelas de validade** (a partir da data de referência, padrão = hoje):
   - Curso: últimos **24 meses** · Formação: **48 meses** · AM Black: **12 meses**.
   - Pedido fora da janela do seu tipo não conta (já expirou).
4. **Propagação:**
   - **Formação** → +1 em cada **curso que ela contém**.
   - **AM Black** (assinatura que dá acesso a tudo) → +1 em **todos** os cursos e formações.
5. Métrica = **inscrições/matrículas**, não pessoas únicas (1 aluno na formação + 1 no curso = 2).

## Publicar no Posit (Connect / Cloud) via GitHub

O app já está configurado para deploy. **Versão do Python fixada em 3.11.9** (não use 3.14 — é nova demais para o Connect). Os dados continuam vindo de **upload do usuário** no app publicado; nenhum dado de cliente vai para o repositório (`orders-*.csv` está no `.gitignore`).

**Arquivos de configuração já incluídos:**
- `requirements.txt` — dependências com versões fixadas.
- `.python-version` — fixa o Python em `3.11.9`.
- `manifest.json` — manifesto do Posit Connect (deploy Git-backed).
- `.posit/publish/dashboard.toml` — configuração do **Posit Publisher** (extensão VSCode / CLI).

**Opção A — Posit Publisher (recomendado):**
1. Instale a extensão *Posit Publisher* no VSCode (ou a CLI `publisher`).
2. Aponte para a pasta `dashboard/` (entrypoint `app.py`).
3. Conecte na sua conta do Posit Connect e clique em *Deploy*. A config em `.posit/publish/dashboard.toml` já define tipo, entrypoint e Python 3.11.

**Opção B — Git-backed deploy no Posit Connect:**
1. No Connect: *Publish → Import from Git*, informe o repositório e o **subdiretório `dashboard/`**.
2. O Connect lê o `manifest.json` e instala o `requirements.txt` na Python 3.11.

> Se editar `app.py`/`logica.py`/`relacao.py`/`requirements.txt`, regenere o `manifest.json` (os checksums mudam):
> ```bash
> pip install rsconnect-python
> rsconnect write-manifest shiny dashboard/ --overwrite --entrypoint app
> ```

## Arquivos

| Arquivo | Papel |
|---|---|
| `app.py` | Interface (UI + server) do Shiny for Python. Entrypoint: objeto `app`. |
| `logica.py` | Cálculo: status, janelas, matching, propagação. Recebe um DataFrame e devolve os totais. |
| `relacao.py` | **Fonte da verdade**: os 46 itens da planilha, a relação formação→cursos e os `ALIASES` (nome export → curso). |
| `requirements.txt` | Dependências (versões fixadas). |
| `.python-version` | Python 3.11.9. |
| `manifest.json` | Manifesto do Posit Connect (Git-backed). |
| `.posit/publish/dashboard.toml` | Config do Posit Publisher. |

## Manutenção

Quando surgir um **produto novo** ou um **nome diferente** no export que deva contar:
1. Abra `relacao.py` e adicione a linha em `ALIASES` (`"Nome no export": "Nome do curso na planilha"`).
2. Pronto — o app passa a contar. Use a aba **"Itens ignorados"** para descobrir o que ainda falta mapear.

Nenhuma etapa manual fora isso: o app é autossuficiente e roda só com Python.
