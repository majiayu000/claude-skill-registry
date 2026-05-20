---
name: lendo-arquivos
description: "Le arquivos Excel (.xlsx, .xls) e CSV enviados pelo usuario. Use quando o usuario anexar um arquivo e pedir para analisar, importar ou processar os dados. Retorna o conteudo como JSON para analise."
---

# Lendo Arquivos - Processar Uploads do Usuario

Skill para **leitura de arquivos** enviados pelo usuario via upload.

> **ESCOPO:** Esta skill processa Excel (.xlsx, .xls) e CSV.
> Para CRIAR/EXPORTAR arquivos para download, use `exportando-arquivos`.
> Para consultas Odoo (NF, PO, SO, titulos), use `rastreando-odoo`.

## Script Principal

### ler.py

```bash
source .venv/bin/activate && \
python .claude/skills/lendo-arquivos/scripts/ler.py [opcoes]
```

## Tipos de Arquivo

```
FORMATOS SUPORTADOS
│
├── Excel (.xlsx)
│   Engine: openpyxl
│   Usar: Planilhas modernas (2007+)
│
├── Excel (.xls)
│   Engine: xlrd
│   Usar: Planilhas legado (97-2003)
│
└── CSV (.csv)
    Separadores: ; , \t |
    Usar: Arquivos texto estruturados
```

## Parametros

### Parametros Principais

| Parametro | Obrigatorio | Descricao | Exemplo |
|-----------|-------------|-----------|---------|
| `--url` | Sim | URL do arquivo (do upload) | `--url /agente/api/files/default/abc.xlsx` |
| `--limite` | Nao | Limite de linhas (default: 1000) | `--limite 100` |
| `--aba` | Nao | Nome ou indice da aba (Excel) | `--aba 0` ou `--aba "Dados"` |
| `--cabecalho` | Nao | Linha do cabecalho (default: 0) | `--cabecalho 1` |

## Exemplos de Uso

### Ler arquivo Excel
```bash
source .venv/bin/activate && \
python .claude/skills/lendo-arquivos/scripts/ler.py \
  --url "/agente/api/files/default/abc123_planilha.xlsx"
```

### Ler com limite de linhas
```bash
python .../ler.py --url "/agente/api/files/default/dados.xlsx" --limite 50
```

### Ler aba especifica
```bash
python .../ler.py --url "/agente/api/files/default/multi.xlsx" --aba "Vendas"
```

### Ler CSV
```bash
python .../ler.py --url "/agente/api/files/default/dados.csv"
```

## Retorno JSON

```json
{
  "sucesso": true,
  "arquivo": {
    "nome": "planilha.xlsx",
    "tipo": "excel",
    "tamanho": 15234,
    "tamanho_formatado": "14.9 KB",
    "abas": ["Dados", "Resumo"],
    "aba_lida": "Dados"
  },
  "dados": {
    "colunas": ["Pedido", "Cliente", "Valor"],
    "total_linhas": 150,
    "linhas_retornadas": 100,
    "registros": [
      {"Pedido": "VCD123", "Cliente": "ATACADAO", "Valor": 50000},
      {"Pedido": "VCD456", "Cliente": "ASSAI", "Valor": 75000}
    ]
  },
  "resumo": "Arquivo EXCEL com 150 linhas e 3 colunas (limitado). Colunas: Pedido, Cliente, Valor"
}
```

## Fluxo de Uso

Quando o usuario anexar um arquivo e pedir "analise essa planilha":

1. **Identificar URL** do arquivo nos metadados do anexo
2. **Executar script**:
   ```bash
   source .../venv/bin/activate && python .../ler.py --url "URL_DO_ARQUIVO"
   ```
3. **Analisar JSON** retornado
4. **Responder ao usuario** com insights dos dados

## Tratamento de Erros

| Erro | Causa | Solucao |
|------|-------|---------|
| Arquivo nao encontrado | URL invalida | Verificar URL do anexo |
| Formato nao suportado | Extensao invalida | Apenas xlsx, xls, csv |
| Arquivo corrompido | Arquivo danificado | Pedir ao usuario reenviar |
| Dependencia faltando | Biblioteca nao instalada | pip install pandas openpyxl xlrd |

## Conversoes Automaticas

| Tipo Original | Conversao |
|---------------|-----------|
| Datas | ISO 8601 (YYYY-MM-DD) |
| Numeros | float/int preservado |
| NaN/vazio | null |
| Texto | string |

## Notas

- Limite padrao: 1000 linhas (para evitar respostas muito grandes)
- Para arquivos grandes, use `--limite` para obter amostra
- Separador CSV eh detectado automaticamente (`;`, `,`, `\t`, `|`)
- Encoding: UTF-8 com BOM suportado

## Relacionado

| Skill | Uso |
|-------|-----|
| exportando-arquivos | CRIAR/EXPORTAR arquivos para download |
| rastreando-odoo | Consultas e rastreamento de fluxos Odoo |
| gerindo-expedicao | Consultas de carteira, separacoes e estoque |

> **NOTA**: Esta skill eh para LEITURA de arquivos do usuario.
> Para criar arquivos para download, use `exportando-arquivos`.
