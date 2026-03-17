---
name: exportando-arquivos
description: "Gera arquivos Excel, CSV ou JSON para download pelo usuario. Use quando o usuario pedir para exportar dados, criar planilha, gerar relatorio ou baixar informacoes. SEMPRE use esta skill em vez de Write para criar arquivos que o usuario precisa baixar."
---

# Exportando Arquivos - Gerar Downloads para Usuario

Skill para **criacao de arquivos** que o usuario pode baixar.

> **ESCOPO:** Esta skill CRIA arquivos Excel, CSV e JSON para download.
> Para LER arquivos enviados pelo usuario, use `lendo-arquivos`.
> **IMPORTANTE:** SEMPRE use esta skill em vez da tool `Write` para arquivos de download!

## Script Principal

### exportar.py

```bash
source .venv/bin/activate && \
echo '{"dados": [...]}' | python .claude/skills/exportando-arquivos/scripts/exportar.py [opcoes]
```

## Formatos de Saida

```
FORMATOS SUPORTADOS
│
├── Excel (.xlsx)
│   Engine: xlsxwriter
│   Recursos: Formatacao, cabecalho colorido, largura auto
│
├── CSV (.csv)
│   Separador: ponto-e-virgula (;)
│   Encoding: UTF-8 com BOM
│
├── JSON (.json)
│   Formatacao: indentado, UTF-8
│   Uso: Integracao com outros sistemas
│
└── Imagem (.png, .jpg, .jpeg, .gif)
    Copia imagem existente para pasta de downloads
    Pode ser exibida inline ou baixada
```

## Parametros

### Parametros Principais

| Parametro | Obrigatorio | Descricao | Exemplo |
|-----------|-------------|-----------|---------|
| `--formato` | Sim | Formato do arquivo | `--formato excel` ou `--formato imagem` |
| `--nome` | Sim | Nome do arquivo (sem extensao) | `--nome pedidos_atacadao` |
| `--titulo` | Nao | Titulo da planilha (Excel) | `--titulo "Pedidos Atacadao"` |
| `--colunas` | Nao | Colunas a incluir (JSON array) | `--colunas '["Pedido","Cliente"]'` |
| `--imagem` | Sim* | Caminho da imagem (apenas formato imagem) | `--imagem /tmp/screenshot.png` |

### Entrada de Dados

Dados sao recebidos via **stdin** no formato JSON:

```json
{
  "dados": [
    {"Pedido": "VCD123", "Cliente": "ATACADAO 123", "Valor": 50000},
    {"Pedido": "VCD456", "Cliente": "ATACADAO 456", "Valor": 75000}
  ]
}
```

## Exemplos de Uso

### Gerar Excel simples
```bash
source .venv/bin/activate && \
echo '{"dados": [{"col1": "val1"}]}' | python .claude/skills/exportando-arquivos/scripts/exportar.py \
  --formato excel \
  --nome relatorio
```

### Gerar Excel com titulo
```bash
echo '{"dados": [...]}' | python .../exportar.py \
  --formato excel \
  --nome pedidos_atacadao \
  --titulo "10 Maiores Pedidos"
```

### Gerar CSV
```bash
echo '{"dados": [...]}' | python .../exportar.py \
  --formato csv \
  --nome exportacao
```

### Gerar JSON
```bash
echo '{"dados": [...]}' | python .../exportar.py \
  --formato json \
  --nome dados
```

### Selecionar colunas
```bash
echo '{"dados": [...]}' | python .../exportar.py \
  --formato excel \
  --nome resumo \
  --colunas '["Pedido", "Valor"]'
```

### Exportar imagem
```bash
python .claude/skills/exportando-arquivos/scripts/exportar.py \
  --formato imagem \
  --imagem /tmp/screenshot.png \
  --nome grafico_vendas
```

> **Nota**: Para imagens, nao precisa de stdin (echo). O arquivo e copiado diretamente.

## Retorno JSON

```json
{
  "sucesso": true,
  "arquivo": {
    "nome": "abc123_pedidos.xlsx",
    "nome_original": "pedidos.xlsx",
    "url": "/agente/api/files/default/abc123_pedidos.xlsx",
    "url_completa": "https://sistema-fretes.onrender.com/agente/api/files/default/abc123_pedidos.xlsx",
    "tamanho": 15234,
    "tamanho_formatado": "14.9 KB",
    "registros": 10,
    "formato": "excel"
  },
  "mensagem": "Arquivo EXCEL criado com 10 registros!",
  "instrucao_agente": "Informe ao usuario... 📥 **[Clique aqui para baixar](URL_COMPLETA)**"
}
```

## Fluxo de Uso Completo

Quando o usuario pedir "exporte os 10 maiores pedidos para Excel":

1. **Buscar dados** usando skill apropriada (ex: `gerindo-expedicao`)
2. **Formatar como JSON**: `{"dados": [...]}`
3. **Executar script**:
   ```bash
   echo '{"dados": [...]}' | python .../exportar.py --formato excel --nome pedidos
   ```
4. **Ler URL** do campo `arquivo.url_completa` no retorno (SEMPRE usar URL completa!)
5. **Responder ao usuario** com link para download:
   ```
   📥 **[Clique aqui para baixar](https://sistema-fretes.onrender.com/agente/api/files/default/abc_pedidos.xlsx)**
   Arquivo: pedidos.xlsx | 10 registros
   ```

> **IMPORTANTE**: No Render, SEMPRE use `url_completa` para garantir que o link funcione!

## Formatacao Automatica (Excel)

| Tipo de Coluna | Formatacao Aplicada |
|----------------|---------------------|
| Valor, Preco, Custo, Total | R$ #,##0.00 |
| Cabecalho | Negrito, fundo azul, texto branco |
| Largura | Auto-ajuste ate 50 caracteres |

## Tratamento de Erros

| Erro | Causa | Solucao |
|------|-------|---------|
| Nenhum dado via stdin | echo vazio | Verificar pipe do echo |
| JSON invalido | Formato incorreto | Validar estrutura JSON |
| Campo "dados" vazio | Lista vazia | Verificar dados de entrada |
| Dependencia faltando | Biblioteca ausente | pip install pandas xlsxwriter |

## Notas

- Arquivos salvos em `/tmp/agente_files/default/`
- URL retornada eh acessivel via HTTP
- Nome do arquivo inclui prefixo UUID para evitar colisoes
- Tamanho maximo recomendado: 10MB
- Arquivos removidos automaticamente apos 24h (limpeza do /tmp)

## Relacionado

| Skill | Uso |
|-------|-----|
| lendo-arquivos | LER arquivos enviados pelo usuario |
| gerindo-expedicao | Consultas de carteira para exportar |
| rastreando-odoo | Consultas Odoo (NF, PO, SO, titulos) para exportar |

> **NOTA**: Esta skill eh para CRIAR arquivos para download.
> Para ler arquivos do usuario, use `lendo-arquivos`.
> NUNCA use a tool `Write` para criar arquivos que o usuario precisa baixar!
