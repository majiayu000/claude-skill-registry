---
name: conciliando-odoo-po
description: |
  EXECUTA operacoes de conciliacao de Pedidos de Compra (PO) com DFe no Odoo: split, consolidacao, criacao de PO Conciliador, ajuste de saldos.

  USAR QUANDO:
  - Executar consolidacao de POs: "consolide os POs da NF 12345", "execute split do pedido"
  - Criar PO Conciliador: "crie PO conciliador", "duplique pedido de compra"
  - Ajustar saldo de PO: "reduza quantidade do PO", "ajuste saldo"
  - Reverter consolidacao: "reverta consolidacao", "desfaca split"
  - Depurar erro em consolidacao: "erro ao consolidar", "PO nao criado"
  - Entender fluxo split/consolidacao: "como funciona o split?", "o que e PO Conciliador?"

  NAO USAR QUANDO:
  - Apenas consultar/rastrear documentos sem modificar POs
  - Explorar campos de modelo Odoo desconhecido
  - Operacoes financeiras (pagamentos, extratos, reconciliacao)
  - Validar match NF x PO (este e processo anterior, Fase 2)
---

## QUANDO NAO USAR ESTA SKILL
- Validar match NF x PO (este e Fase 2, anterior a consolidacao)
- Processar recebimento fisico com lotes/quality check (este e Fase 4, posterior)
- Operacoes financeiras como pagamentos ou reconciliacao de extratos
- Apenas consultar/rastrear documentos sem modificar POs

# Conciliando Odoo PO

Skill para **EXECUTAR** operacoes de Split e Consolidacao de Pedidos de Compra no Odoo.

## Contexto

Quando uma NF-e (DFe) chega com quantidades diferentes dos POs existentes, o sistema precisa:
1. Criar um **PO Conciliador** que casa 100% com a NF
2. Ajustar os POs originais para ficarem com o **saldo restante**
3. Vincular o DFe ao PO Conciliador

## Operacoes Suportadas

| Operacao | Metodo | Resultado |
|----------|--------|-----------|
| Simular consolidacao | `simular_consolidacao()` | Preview sem executar no Odoo |
| Executar consolidacao | `consolidar_pos()` | PO Conciliador criado + POs ajustados |
| Reverter consolidacao | `reverter_consolidacao()` | Desfaz acoes (best-effort) |
| Criar PO Conciliador | `_criar_po_conciliador()` | Duplica PO via copy() |
| Criar linha conciliador | `_criar_linha_po_conciliador()` | Duplica linha via copy() |
| Ajustar quantidade | `_ajustar_quantidade_linha()` | Reduz qtd no PO original |
| Vincular DFe ao PO | `_vincular_dfe_ao_po()` | Escreve dfe_id no PO |
| Cancelar PO vazio | `_cancelar_po()` | Cancela PO sem saldo |

## Arquivo Principal

`app/recebimento/services/odoo_po_service.py` (1281 linhas)

## Classe Principal

```python
from app.recebimento.services.odoo_po_service import OdooPoService

service = OdooPoService()
```

## Fluxo Completo de Consolidacao

```
ENTRADA:
  - validacao_id (ValidacaoNfPoDfe com status='aprovado')
  - pos_para_consolidar: [{'po_id': 123, 'po_name': 'PO00123'}, ...]

PASSO 1: Buscar fornecedor_id pelo CNPJ
  → odoo.search('res.partner', [('l10n_br_cnpj', '=', cnpj_formatado)])

PASSO 2: Criar PO Conciliador VAZIO
  → copy(PO de referencia) com overrides: partner_id, date_order, origin, state=draft, order_line=False
  → Fallback: se copy() copiar linhas, remove-las via unlink

PASSO 3: Para CADA item da NF com match:
  → Para cada MatchAlocacao (suporte multi-PO):
    a) copy(linha de referencia) → nova linha no PO Conciliador com qtd_nf e preco_nf
    b) write(linha original) → reduzir product_qty no PO original

PASSO 4: Confirmar PO Conciliador
  → execute_kw('purchase.order', 'button_confirm', [po_id])

PASSO 5: Vincular DFe ao PO Conciliador
  → write('purchase.order', po_id, {'dfe_id': dfe_id})
```

## Modelos Locais Envolvidos

| Modelo | Tabela | Uso |
|--------|--------|-----|
| `ValidacaoNfPoDfe` | `validacao_nf_po_dfe` | Validacao principal (status, resultado) |
| `MatchNfPoItem` | `match_nf_po_item` | Cada item da NF com match de PO |
| `MatchAlocacao` | `match_alocacao` | Alocacao multi-PO (1 item NF → N POs) |

## Modelos Odoo Envolvidos

| Modelo | Campos Principais | Operacoes |
|--------|-------------------|-----------|
| `purchase.order` | name, partner_id, date_order, origin, state, order_line, dfe_id | copy, write, button_confirm, button_cancel |
| `purchase.order.line` | order_id, product_id, product_qty, price_unit, qty_received | copy, write, unlink |
| `res.partner` | l10n_br_cnpj | search |

## Metodo de Conexao Odoo

```python
from app.odoo.utils.connection import get_odoo_connection

odoo = get_odoo_connection()
odoo.authenticate()

# UNICO metodo generico disponivel:
resultado = odoo.execute_kw(modelo, metodo, args, kwargs)

# Helpers especificos (wrapper de execute_kw):
odoo.search(modelo, domain, limit=None)
odoo.read(modelo, ids, fields)
odoo.write(modelo, id_ou_ids, values)
odoo.create(modelo, values)
```

## IMPORTANTE: NAO existe `odoo.execute()`

A classe `OdooConnection` (app/odoo/utils/connection.py) possui APENAS:
- `execute_kw(model, method, args, kwargs)` - generico
- `search()`, `read()`, `write()`, `create()` - helpers

**NUNCA usar `odoo.execute()`** — nao existe e causara AttributeError.

## Cenarios de Uso

### SPLIT (1 NF parcial de 1 PO)
```
PO Original: 500 un produto X
NF chegou: 400 un produto X

Resultado:
  PO Original: 100 un (saldo)
  PO Conciliador (NOVO): 400 un → vinculado a NF
```

### CONSOLIDACAO (1 NF com itens de N POs)
```
PO-A: 500 un produto X
PO-B: 500 un produto Y
NF chegou: 400 X + 400 Y

Resultado:
  PO-A: 100 un X (saldo)
  PO-B: 100 un Y (saldo)
  PO Conciliador (NOVO): 400 X + 400 Y → vinculado a NF
```

### MULTI-PO SPLIT (1 item NF → N POs)
```
PO-A: 200 un produto X
PO-B: 300 un produto X
NF chegou: 450 un produto X

Resultado (via MatchAlocacao):
  PO-A: 0 un (consumido total, pode ser cancelado)
  PO-B: 50 un (saldo)
  PO Conciliador: 200 X (do PO-A) + 250 X (do PO-B) = 450 X
```

## Pre-requisitos para Consolidacao

1. Validacao com `status='aprovado'`
2. MatchNfPoItem com `status_match='match'` para cada item
3. MatchAlocacao com `odoo_po_line_id` preenchido para multi-PO
4. Conexao Odoo funcional

## Referencia Cruzada com Outras Skills

| Skill | Quando usar em vez desta |
|-------|--------------------------|
| `validacao-nf-po` | ANTES da consolidacao (match, de-para, divergencias) |
| `rastreando-odoo` | CONSULTAR documentos (nao executar) |
| `descobrindo-odoo-estrutura` | Explorar campos nao documentados |
| `executando-odoo-financeiro` | Operacoes financeiras (pagamentos, extratos) |
