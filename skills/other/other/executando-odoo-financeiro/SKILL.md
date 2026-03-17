---
name: executando-odoo-financeiro
description: |
  EXECUTA operacoes financeiras no Odoo: criar pagamentos, reconciliar extratos, baixar titulos.

  USAR QUANDO:
  - Criar pagamento no Odoo: "crie pagamento para NF 12345", "baixe titulo no Odoo"
  - Reconciliar extrato bancario: "reconcilie extrato 31615", "vincule pagamento ao extrato"
  - Pagamento COM juros: "crie pagamento com juros", "baixe com write-off"
  - Corrigir extrato nao reconciliado: "extrato is_reconciled=False"
  - Baixar titulo a receber: "marque como pago no Odoo"

  NAO USAR QUANDO:
  - Apenas consultar/rastrear documentos sem modificar
  - Explorar campos de modelo Odoo desconhecido
  - Criar lancamentos fiscais (CTe, despesas extras)
---

## QUANDO NAO USAR ESTA SKILL
- Apenas CONSULTAR/rastrear documentos sem modificar (esta skill EXECUTA operacoes)
- Explorar modelo Odoo desconhecido (esta skill trabalha com modelos financeiros conhecidos)
- Validar match NF x PO (este e processo de recebimento, nao financeiro)
- Exportar balancete/razao geral (existe skill especializada para relatorios contabeis)

# Executando Odoo Financeiro

Skill para **EXECUTAR** operacoes financeiras no Odoo (diferente de rastreando-odoo que apenas consulta).

## Operacoes Suportadas

| Operacao | Metodo | Resultado |
|----------|--------|-----------|
| Criar pagamento simples | `_criar_pagamento()` | Payment draft → precisa postar |
| Criar pagamento com juros | `_criar_pagamento_com_writeoff_juros()` | Payment posted + reconciliado |
| Reconciliar titulo | `reconcile()` em `account.move.line` | Full/Partial reconcile |
| Reconciliar extrato | `reconcile()` linha transitoria <-> payment | is_reconciled=True |

## Fluxo Completo de Recebimento

```
┌─────────────────────────────────────────────────────────────────────┐
│ 1. IDENTIFICAR DADOS                                                │
│    → Titulo: account.move.line (asset_receivable, not reconciled)  │
│    → Extrato: account.bank.statement.line (is_reconciled=False)    │
│    → Partner: res.partner (via extrato ou titulo)                  │
│    → Calcular: valor_juros = valor_extrato - saldo_titulo          │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 2. CRIAR PAGAMENTO                                                  │
│    → SEM juros: _criar_pagamento() → postar → reconcile manual     │
│    → COM juros: _criar_pagamento_com_writeoff_juros()              │
│      ↳ Wizard account.payment.register ja faz TUDO automatico     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 3. RECONCILIAR EXTRATO                                              │
│    → Buscar linha PENDENTES (conta 26868) do payment               │
│    → Buscar linha TRANSITORIA (conta 22199) do extrato             │
│    → Executar reconcile() entre as duas linhas                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Referencias

| Arquivo | Conteudo |
|---------|----------|
| [fluxo-recebimento.md](references/fluxo-recebimento.md) | Codigo validado para criar pagamentos e reconciliar |
| [erros-comuns.md](references/erros-comuns.md) | Armadilhas e como evita-las |
| [contas-por-empresa.md](references/contas-por-empresa.md) | IDs de contas por company |

## Dados Criticos

### Contas por Empresa (Juros de Recebimento)

```python
CONTA_JUROS_RECEBIMENTOS_POR_COMPANY = {
    1: 22778,  # NACOM GOYA - FB
    3: 24061,  # NACOM GOYA - SC
    4: 25345,  # NACOM GOYA - CD
    5: 26629,  # LA FAMIGLIA - LF
}
```

### Contas Importantes

| ID | Codigo | Nome | Uso |
|----|--------|------|-----|
| 26868 | 1110100004 | PENDENTES | Contrapartida do payment |
| 22199 | 1110100003 | TRANSITORIA | Contrapartida do extrato |
| 24801 | 1120100001 | CLIENTES NACIONAIS | Titulo a receber |
| 25345 | 3702010003 | JUROS DE RECEBIMENTOS | Receita de juros (CD) |

### Journals Bancarios

| ID | Codigo | Nome | Banco CNAB |
|----|--------|------|------------|
| 883 | GRAFENO | Banco Grafeno | 274 (BMP Money Plus) |

> **FLUXO TESTADO (22/01/2026)**: Retorno CNAB do Banco Grafeno (codigo 274).
> Outros bancos devem ser mapeados em `CNAB_BANCO_PARA_JOURNAL` conforme configurados.

### Mapeamento CNAB → Journal

```python
# app/financeiro/services/baixa_titulos_service.py
CNAB_BANCO_PARA_JOURNAL = {
    '274': {  # BMP Money Plus / Banco Grafeno
        'journal_id': 883,
        'journal_code': 'GRAFENO',
        'journal_name': 'Banco Grafeno',
    },
    # Adicionar outros bancos conforme configurados:
    # '001': {'journal_id': ???, 'journal_code': 'BB', 'journal_name': 'Banco do Brasil'},
    # '341': {'journal_id': ???, 'journal_code': 'ITAU', 'journal_name': 'Itaú'},
}
```

**Para adicionar novo banco:**
1. Descobrir o `journal_id` no Odoo: `account.journal` com `type='bank'`
2. Adicionar entrada em `CNAB_BANCO_PARA_JOURNAL`
3. Testar importacao de arquivo CNAB do novo banco

## Uso Rapido

### Criar Pagamento COM Juros (Recomendado)

```python
from app.odoo.utils.connection import get_odoo_connection

odoo = get_odoo_connection()

# IDs necessarios
titulo_line_id = 2514959  # account.move.line do titulo (asset_receivable)
partner_id = 204534
valor_total = 1342.52  # Valor do extrato (principal + juros)
journal_id = 883       # GRAFENO
company_id = 4         # NACOM CD
conta_juros = 25345    # Conta de juros da empresa
data = '2026-01-19'
ref = 'NF-e: 140743 Serie: 1'

# Wizard com Write-Off (JA faz tudo!)
wizard_context = {
    'active_model': 'account.move.line',
    'active_ids': [titulo_line_id],
}

wizard_data = {
    'payment_type': 'inbound',
    'partner_type': 'customer',
    'partner_id': partner_id,
    'amount': valor_total,
    'journal_id': journal_id,
    'payment_date': data,
    'communication': ref,
    'payment_difference_handling': 'reconcile',
    'writeoff_account_id': conta_juros,
    'writeoff_label': 'Juros de recebimento em atraso',
}

wizard_id = odoo.execute_kw(
    'account.payment.register',
    'create',
    [wizard_data],
    {'context': wizard_context}
)

# Executar wizard
try:
    odoo.execute_kw(
        'account.payment.register',
        'action_create_payments',
        [[wizard_id]],
        {'context': wizard_context}
    )
except Exception as e:
    if "cannot marshal None" not in str(e):
        raise
    # Erro "cannot marshal None" e NORMAL - operacao foi executada!
```

### Reconciliar Extrato com Payment

```python
# Buscar linha PENDENTES do payment
payment_move_id = 474858  # Move do payment criado
linhas = odoo.search_read(
    'account.move.line',
    [
        ['move_id', '=', payment_move_id],
        ['account_id', '=', 26868],  # PENDENTES
    ],
    ['id', 'debit', 'reconciled'],
    limit=5
)

payment_line_id = None
for l in linhas:
    if l['debit'] > 0 and not l['reconciled']:
        payment_line_id = l['id']
        break

# Linha do extrato (transitoria)
extrato_line_id = 2968184  # account.move.line do extrato (conta TRANSITORIA)

# Reconciliar
try:
    odoo.execute_kw(
        'account.move.line',
        'reconcile',
        [[payment_line_id, extrato_line_id]],
        {}
    )
except Exception as e:
    if "cannot marshal None" not in str(e):
        raise
    # Erro "cannot marshal None" = SUCESSO!
```

### Corrigir Campos do Extrato (OBRIGATORIO para Boletos)

Apos reconciliar extrato com payment, **SEMPRE** corrigir os 3 campos:

```python
from app.financeiro.services.baixa_pagamentos_service import (
    BaixaPagamentosService, CONTA_TRANSITORIA, CONTA_PAGAMENTOS_PENDENTES
)

baixa_service = BaixaPagamentosService()

# 1. ANTES de reconciliar: trocar conta
baixa_service.trocar_conta_move_line_extrato(
    move_id=extrato_move_id,
    conta_origem=CONTA_TRANSITORIA,            # 22199
    conta_destino=CONTA_PAGAMENTOS_PENDENTES,  # 26868
)

# 2. Reconciliar (codigo existente)

# 3. DEPOIS: atualizar partner e rotulo
baixa_service.atualizar_statement_line_partner(statement_line_id, partner_id)
rotulo = BaixaPagamentosService.formatar_rotulo_pagamento(valor, nome, data)
baixa_service.atualizar_rotulo_extrato(extrato_move_id, statement_line_id, rotulo)
```

> **REGRA:** Qualquer operacao que reconcilie payment ↔ extrato DEVE incluir estes 3 passos.
> Ver [erros-comuns.md](references/erros-comuns.md) Erro 11 e `.claude/references/odoo/GOTCHAS.md` secao "Extrato Bancario: 3 Campos".

### Correcao Retroativa (Registros Ja Conciliados)

Quando registros JA estao reconciliados (`is_reconciled=True`) mas com campos incorretos (lancamentos anteriores a 03/02/2026), usar o fluxo **CORRETIVO** de 7 passos:

**Diferenca dos fluxos:**
- **PREVENTIVO** (acima): Corrige ANTES de reconciliar — simples, sem desconciliacao
- **CORRETIVO**: Corrige DEPOIS de ja reconciliado — exige desconciliar → draft → editar → post → re-reconciliar

**Gotchas criticos:**
- Odoo RECRIA move lines ao editar em draft (IDs mudam!)
- `account_id` DEVE ser ultimo campo alterado antes de `action_post`
- TRANSITORIA pode estar no debito (pagamentos) OU credito (recebimentos)

**Script**: `scripts/correcao_campos_extrato_odoo.py` — modos `--verificar-*` e `--corrigir-*`

> Ver [erros-comuns.md](references/erros-comuns.md) Erro 12 e `.claude/references/odoo/GOTCHAS.md` secao "Correcao Retroativa" para fluxo completo.

## Skills Relacionadas

| Skill | Quando usar |
|-------|-------------|
| [rastreando-odoo](../rastreando-odoo/SKILL.md) | Consultar/rastrear documentos (leitura) |
| [descobrindo-odoo-estrutura](../descobrindo-odoo-estrutura/SKILL.md) | Descobrir campos de modelos |
| [integracao-odoo](../integracao-odoo/SKILL.md) | Criar CTe, despesas extras |
