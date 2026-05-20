---
name: razao-geral-odoo
description: "Exporta Razao Geral (General Ledger) do Odoo em Excel. Busca account.move.line com paginacao, calcula saldo inicial para contas patrimoniais via read_group, gera Excel com coluna de conta contabil e saldo acumulado. Use quando: exportar razao geral, relatorio contabil, balancete, consulta account.move.line em massa."
---

## QUANDO NAO USAR ESTA SKILL
- Operacoes financeiras como pagamentos ou reconciliacao de extratos (esta skill apenas exporta relatorios)
- Rastrear fluxo documental de NF/PO/SO (esta skill gera relatorio contabil, nao rastreia documentos)
- Explorar modelo Odoo desconhecido (esta skill trabalha exclusivamente com account.move.line)

# Razão Geral do Odoo (General Ledger)

Skill para **exportação do relatório Razão Geral** a partir do Odoo via XML-RPC.

> **QUANDO USAR:**
> - Exportar Razão Geral de um período
> - Consultar movimentos contábeis (account.move.line) em massa
> - Calcular saldos acumulados de contas
> - Relatórios contábeis que envolvem account.move.line

## Tela Web

**URL**: `/relatorios-fiscais/razao-geral`
**Menu**: Financeiro → Central Financeira → Relatórios Contábeis → Razão Geral
**Blueprint**: `relatorios_fiscais`

## Script Standalone

```bash
source .venv/bin/activate && python scripts/exportar_razao_geral.py
```

**Configuração** (editar no script):
- `DATA_INICIO`: Data inicial (YYYY-MM-DD)
- `DATA_FIM`: Data final (YYYY-MM-DD)
- `COMPANY_IDS`: Lista de company_ids

## Service (Importável)

**Arquivo**: `app/relatorios_fiscais/services/razao_geral_service.py`

### Funções Disponíveis

| Função | Descrição | Retorno |
|--------|-----------|---------|
| `calcular_saldos_iniciais(conn, acc_ids, data_ini, company_ids)` | Saldos via read_group | `dict` |
| `buscar_movimentos_razao(conn, data_ini, data_fim, company_ids, conta_filter)` | Busca com ID-cursor + transformação inline | `tuple(dados_agrupados, contas_info, saldos, total)` |
| `gerar_excel_razao(dados_agrupados, contas_info, saldos, ...)` | Gera Excel via xlsxwriter | `BytesIO` |

### Exemplo de Uso

```python
from app.odoo.utils.connection import get_odoo_connection
from app.relatorios_fiscais.services.razao_geral_service import (
    buscar_movimentos_razao, gerar_excel_razao
)

connection = get_odoo_connection()
connection.authenticate()

dados_agrupados, contas_info, saldos, total = buscar_movimentos_razao(
    connection,
    data_ini='2024-08-01',
    data_fim='2024-08-31',
    company_ids=[4, 1, 3],
    conta_filter='1010'  # Opcional: filtrar por código de conta
)

excel = gerar_excel_razao(
    dados_agrupados, contas_info, saldos,
    data_ini='2024-08-01', data_fim='2024-08-31', company_ids=[4, 1, 3]
)

# excel é BytesIO pronto para send_file() ou salvar em disco
```

---

## Modelos Odoo Envolvidos

### account.move.line (Modelo Base)

Cada linha representa um débito ou crédito individual.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `date` | date | Data do lançamento |
| `move_name` | char | Número do lançamento (INV/2024/0001) |
| `account_id` | many2one → account.account | Conta contábil |
| `partner_id` | many2one → res.partner | Cliente/Fornecedor |
| `ref` | char | Referência |
| `name` | char | Rótulo/Label da linha |
| `debit` | monetary | Valor a débito |
| `credit` | monetary | Valor a crédito |
| `balance` | monetary | Saldo (debit - credit) |
| `journal_id` | many2one → account.journal | Diário contábil |
| `matching_number` | char | Número de conciliação |
| `parent_state` | selection | Status: draft, posted, cancel |
| `account_type` | selection | Tipo interno da conta |
| `company_id` | many2one → res.company | Empresa |

### account.account (Plano de Contas)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `code` | char | Código da conta (ex: 1010100010) |
| `name` | char | Nome da conta |
| `account_type` | selection | Tipo: asset_*, liability_*, equity_*, income_*, expense_* |

### account.journal (Diários)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `code` | char | Código curto (GRA1, SIC, BRAD) |
| `name` | char | Nome do diário |
| `type` | selection | bank, cash, sale, purchase, general |

---

## Mapeamento de Empresas

| ID | Nome | Sigla | CNPJ |
|----|------|-------|------|
| 1 | NACOM GOYA - FB | FB | 61.724.241/0001-78 |
| 3 | NACOM GOYA - SC | SC | 61.724.241/0002-59 |
| 4 | NACOM GOYA - CD | CD | 61.724.241/0003-30 |
| 5 | LA FAMIGLIA - LF | LF | 18.467.441/0001-63 |

---

## Contas Patrimoniais vs Resultado

### Patrimoniais (RECEBEM saldo inicial)

| Tipo | Descrição |
|------|-----------|
| `asset_receivable` | Ativo - A Receber |
| `asset_cash` | Ativo - Caixa/Banco |
| `asset_current` | Ativo Circulante |
| `asset_non_current` | Ativo Não Circulante |
| `asset_prepayments` | Ativo - Adiantamentos |
| `asset_fixed` | Ativo Fixo |
| `liability_payable` | Passivo - A Pagar |
| `liability_credit_card` | Passivo - Cartão de Crédito |
| `liability_current` | Passivo Circulante |
| `liability_non_current` | Passivo Não Circulante |
| `equity` | Patrimônio Líquido |
| `equity_unaffected` | Lucros/Prejuízos Acumulados |

### Resultado (SEM saldo inicial)

| Tipo | Descrição |
|------|-----------|
| `income` | Receita |
| `income_other` | Outras Receitas |
| `expense` | Despesa |
| `expense_depreciation` | Depreciação |
| `expense_direct_cost` | Custo Direto |

---

## Padrões Técnicos Utilizados

### Paginação com ID-cursor

Usa cursor baseado em ID para performance constante O(1) por batch (sem degradação por offset):

```python
last_id = 0
while True:
    domain_cursor = domain + [['id', '>', last_id]]
    lote = connection.execute_kw(
        'account.move.line', 'search_read', [domain_cursor],
        {'fields': campos, 'limit': 3000, 'order': 'id asc'},
        timeout_override=120
    )
    if not lote:
        break
    last_id = lote[-1]['id']
    # transformar inline...
```

> **Nota**: Os dados são ordenados por `(date, move_name)` dentro de cada conta no momento da geração do Excel.

### Saldo Inicial via read_group

Uma ÚNICA query para calcular saldos de todas as contas patrimoniais:

```python
result = connection.execute_kw(
    'account.move.line', 'read_group',
    [domain],
    {
        'fields': ['account_id', 'debit:sum', 'credit:sum', 'balance:sum'],
        'groupby': ['account_id'],
        'lazy': False
    },
    timeout_override=180
)
```

### Tratamento de campos Many2one

Campos many2one retornam `[id, display_name]` ou `False`:

```python
# Extrair display_name
partner_name = reg['partner_id'][1] if isinstance(reg.get('partner_id'), (list, tuple)) else ''
```

### Tratamento de False do Odoo

Campos vazios retornam `False` (não None):

```python
valor = reg.get('ref') or '' if reg.get('ref') is not False else ''
```

---

## Formato do Excel Gerado

### Colunas
`Conta Contábil | Data | Lançamento | Diário | Parceiro | Referência | Label | Débito | Crédito | Saldo Acumulado | Conciliação`

### Estrutura
- Linha de título + subtítulo
- Cabeçalho das colunas (fundo azul)
- Para cada conta (ordenada por código):
  - Se patrimonial: linha "Saldo Inicial" (itálico cinza)
  - Linhas de movimentos com saldo acumulado progressivo
- Formato numérico: `#,##0.00`
- Datas: DD/MM/YYYY

---

## Volume de Dados Observado

| Período | Empresas | Linhas | Contas | Débito = Crédito |
|---------|----------|--------|--------|------------------|
| Agosto/2024 | 3 (FB, SC, CD) | 133.526 | 249 | R$ 324.569.925,49 |

**Tempo de execução estimado**: ~100s (ID-cursor ~90s + Excel xlsxwriter ~8s)
**Pico de memória**: ~40MB (transformação inline sem duplicação)

---

## Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| Timeout na busca | Muitos registros | Aumentar `timeout_override` ou reduzir período |
| Timeout no read_group | Histórico grande | Já usa `timeout_override=180` |
| Valores False | Campos vazios no Odoo | Tratar com `or ''` / `or 0` |
| Saldo não bate | Lançamentos draft incluídos | Verificar filtro `parent_state='posted'` |
| Conta não aparece | Sem movimentos no período | Normal - só lista contas com movimento |
