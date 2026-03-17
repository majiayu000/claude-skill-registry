---
name: recebimento-fisico-odoo
description: |
  Consulta e opera o modulo de Recebimento Fisico (Fase 4): preenchimento de lotes, quantidades e quality checks com processamento assincrono no Odoo via Redis Queue.

  USAR QUANDO:
  - Debugar recebimento fisico: "erro ao validar picking", "lote nao criou", "quality check falhou"
  - Modificar logica do worker: "alterar passos do processamento", "adicionar etapa"
  - Consultar status de recebimento: "picking nao foi para done", "status pendente"
  - Extender funcionalidade: "adicionar campo", "novo tipo de check", "nova validacao"
  - Entender fluxo: "como funciona o recebimento?", "quais passos o worker executa?"
  - Problema com lotes: "lote duplicado", "quantidade errada", "move.line nao criou"

  NAO USAR QUANDO:
  - Rastrear documentos fiscais (NF, PO, SO) sem operar recebimento fisico
  - Descobrir campos de modelo Odoo desconhecido (esta skill usa modelos de picking conhecidos)
  - Criar pagamentos ou reconciliar extratos (operacao financeira, nao de armazem)
  - Depurar match NF x PO (Fase 2, anterior ao recebimento fisico)
  - Conciliar POs por split/consolidacao (Fase 3, anterior ao recebimento fisico)
---

## QUANDO NAO USAR ESTA SKILL
- Match NF x PO (Fase 2, anterior ao recebimento fisico)
- Split/consolidar PO (Fase 3, anterior ao recebimento fisico)
- Operacoes financeiras como pagamentos ou reconciliacao de extratos
- Rastrear fluxo documental completo de NF/PO/SO (esta skill opera o armazem, nao rastreia)

# Recebimento Fisico - Odoo (Fase 4)

Skill para operar o modulo de **Recebimento Fisico**: preencher lotes, quantidades e quality checks,
com processamento assincrono no Odoo via Redis Queue (RQ).

## Contexto

Quando um picking de compra (incoming) chega ao armazem, o operador precisa:
1. Informar os **lotes** e **quantidades** de cada produto recebido
2. Executar **quality checks** (aprovacao pass/fail ou medicao)
3. **Validar o picking** no Odoo (button_validate → state=done)

O sistema sincroniza pickings do Odoo para cache local (APScheduler 30min),
salva LOCALMENTE (imediato) e processa no Odoo via **worker RQ** (assincrono).

## Arquitetura

```
APScheduler (30 min)              TELA 1 (pickings)              WORKER RQ
    Sync Odoo → Local         ─┐     Lista (cache local)         Processar pendentes
    4 tabelas normalizadas     │     Ao clicar → refresh Odoo    Enviar para Odoo
    Incremental (write_date)   │     Preencher lotes + QC        button_validate
                               └┐    SALVAR (banco local)    ────┘
                                │
TELA 2 (status)                 │
    Consultar Odoo              │
    Mostrar status              │
    Retry erros                 │
```

## Arquivos Principais

- **Sync (cache)**: `app/recebimento/services/picking_recebimento_sync_service.py`
- Service local: `app/recebimento/services/recebimento_fisico_service.py`
- Service Odoo: `app/recebimento/services/recebimento_fisico_odoo_service.py`
- Worker RQ: `app/recebimento/workers/recebimento_fisico_jobs.py`
- Scheduler: `app/scheduler/sincronizacao_incremental_definitiva.py` (variavel: `picking_recebimento_sync_service`)

## Classe Principal

```python
from app.recebimento.services.recebimento_fisico_service import RecebimentoFisicoService
from app.recebimento.services.recebimento_fisico_odoo_service import RecebimentoFisicoOdooService

service = RecebimentoFisicoService()
odoo_service = RecebimentoFisicoOdooService()
```

## Fluxo do Worker (8 Passos)

```
ENTRADA:
  - recebimento_id (RecebimentoFisico com status='pendente')

PASSO 1: Conectar Odoo e verificar picking (state=assigned)
  → get_odoo_connection() + authenticate()
  → Ler picking_data → se state != assigned, erro

PASSO 2: Resolver lotes com expiration_date (stock.lot manual)
  → Para cada lote com data_validade + use_expiration_date=True:
    a) Verificar se stock.lot ja existe (name + product_id + company_id)
    b) Se NAO: create('stock.lot', {name, product_id, company_id, expiration_date})
    c) Se SIM: write('stock.lot', lot_id, {expiration_date})
    d) Usar lot_id no passo 3 (em vez de lot_name)

PASSO 3: Preencher lotes (stock.move.line)
  → Para cada lote do recebimento:
    a) 1o lote: write(move_line_id, {lot_id/lot_name, quantity})
    b) Lotes extras: create('stock.move.line', {picking_id, move_id, product_id, lot_id/lot_name, quantity, locations})

PASSO 4: Quality checks passfail
  → execute_kw('quality.check', 'do_pass', [[check_id]])
  → execute_kw('quality.check', 'do_fail', [[check_id]])

PASSO 5: Quality checks measure
  → write('quality.check', check_id, {'measure': valor})
  → execute_kw('quality.check', 'do_measure', [[check_id]])

PASSO 6: Validar picking
  → execute_kw('stock.picking', 'button_validate', [[picking_id]])
  → Tratar "cannot marshal None" como sucesso

PASSO 7: Verificar resultado
  → Ler picking: state='done' = sucesso

PASSO 8: Atualizar status local
  → recebimento.status = 'processado' / 'erro'
  → Marcar lotes e checks como processado=True
```

## Operacoes Suportadas

| Operacao | Metodo | Resultado |
|----------|--------|-----------|
| Sync pickings (scheduler) | `sincronizar_pickings_incremental()` | Importa pickings do Odoo → cache local |
| Sync por periodo | `sincronizar_por_periodo(data_de, data_ate)` | Importa pickings por datas absolutas (YYYY-MM-DD) |
| Refresh 1 picking | `refresh_picking(odoo_id)` | Busca fresco do Odoo e atualiza cache |
| Buscar pickings disponiveis | `buscar_pickings_disponiveis()` | **Le do cache local** (dedup por PO/write_date) |
| Buscar detalhes picking | `buscar_detalhes_picking()` | **Refresh Odoo + le cache** |
| Salvar recebimento | `salvar_recebimento()` | Grava local + enqueue RQ |
| Validar lotes | `validar_lotes()` | Soma lotes == qtd esperada |
| Processar no Odoo | `processar_recebimento()` | 8 passos completos |
| Retry | `retry_recebimento()` | Re-enqueue job |
| Consultar Odoo | `consultar_status_odoo()` | Estado real do picking |

## Tabelas de Cache (Sync APScheduler - 4 tabelas normalizadas)

| Tabela | Modelo | Descricao |
|--------|--------|-----------|
| `picking_recebimento` | PickingRecebimento | 1 linha por picking (state, partner, PO, dates) |
| `picking_recebimento_produto` | PickingRecebimentoProduto | 1 linha por stock.move (product, qty, tracking) |
| `picking_recebimento_move_line` | PickingRecebimentoMoveLine | 1 linha por stock.move.line (lot, qty) |
| `picking_recebimento_quality_check` | PickingRecebimentoQualityCheck | 1 linha por quality.check |

**Sync**: APScheduler a cada 30 min, janela 90 min (env: `JANELA_PICKINGS`)
**Filtro**: `picking_type_code='incoming'` AND `purchase_id != False`
**Dedup**: Por `write_date` (mais recente por PO)

## Tabelas de Trabalho (Recebimento local)

| Tabela | Modelo | Campos-chave |
|--------|--------|--------------|
| `recebimento_fisico` | RecebimentoFisico | odoo_picking_id, status, tentativas, job_id, erro_mensagem |
| `recebimento_lote` | RecebimentoLote | lote_nome, quantidade, data_validade, processado, odoo_lot_id |
| `recebimento_quality_check` | RecebimentoQualityCheck | test_type, resultado, valor_medido, processado |

## Modelos Odoo Envolvidos

| Modelo | Campos Principais | Operacoes |
|--------|-------------------|-----------|
| `stock.picking` | state, picking_type_code, partner_id, origin, purchase_id, move_line_ids | search_read, button_validate |
| `stock.move` | product_id, product_uom_qty, move_line_ids | search_read |
| `stock.move.line` | lot_name, quantity, qty_done, product_id, move_id, picking_id, location_id | search_read, write, create |
| `stock.lot` | name, product_id, company_id, expiration_date | search, create, write (manual quando use_expiration_date=True) |
| `quality.check` | quality_state, test_type, measure, tolerance_min/max, norm_unit | search_read, write, do_pass, do_fail, do_measure |
| `quality.point` | test_type, product_category_ids, picking_type_ids, measure_on | search_read (templates) |
| `product.product` | tracking, use_expiration_date | search_read |

## Campos stock.move.line (ATENCAO - Versao Odoo)

**IMPORTANTE**: O campo `reserved_uom_qty` NAO existe nesta versao do Odoo.

| Campo Odoo | Descricao | Uso |
|------------|-----------|-----|
| `quantity` | Quantidade reservada/atribuida | Qtd que o Odoo reservou |
| `qty_done` | Quantidade realizada | Qtd efetivamente recebida |
| `lot_name` | Nome do lote (cria auto) | Usado quando NAO precisa de expiration_date |
| `lot_id` | ID do stock.lot existente | Usado quando precisa de expiration_date |
| `location_id` | Origem (obrigatorio no create) | Vem do picking |
| `location_dest_id` | Destino (obrigatorio no create) | Vem do picking |

**Coluna local `reserved_uom_qty`**: Armazena valor de `qty_done` do Odoo (nome historico mantido por compatibilidade).

## Metodo de Conexao Odoo

```python
from app.odoo.utils.connection import get_odoo_connection

odoo = get_odoo_connection()
odoo.authenticate()

# UNICO metodo generico:
resultado = odoo.execute_kw(modelo, metodo, args, kwargs)

# Helpers (wrappers de execute_kw):
odoo.search(modelo, domain, limit=None)
odoo.read(modelo, ids, fields)
odoo.write(modelo, id_ou_ids, values)
odoo.create(modelo, values)
```

**NUNCA usar `odoo.execute()`** — nao existe, causa AttributeError.

## Redis (Worker RQ)

| Chave | Formato | TTL |
|-------|---------|-----|
| `recebimento_progresso:{recebimento_id}` | JSON: `{etapa, total, mensagem}` | 1 hora |
| `recebimento_lock:{picking_id}` | String: `"locked"` (nx=True) | 30 min |

Queue: `'recebimento'` (dedicada, timeout 10min por job)

## APIs Disponiveis

| Rota | Metodo | Query Params / Body |
|------|--------|---------------------|
| `/recebimento/fisico/pickings` | GET | company_id, filtro_nf, filtro_fornecedor |
| `/recebimento/fisico/picking/<id>/detalhes` | GET | - |
| `/recebimento/fisico/salvar` | POST | JSON: picking_id, company_id, lotes[], quality_checks[] |
| `/recebimento/fisico/status/listar` | GET | company_id, status, limit |
| `/recebimento/fisico/status/<id>/retry` | POST | - |
| `/recebimento/fisico/status/<id>/consultar-odoo` | GET | - |

## Tracking de Produtos

- **73.6%** dos produtos tem `tracking='lot'` (1191 de 1618)
- Produtos com tracking='lot' EXIGEM lote no recebimento
- Produtos com tracking='none' usam 'SEM_LOTE' como placeholder (nao cria lote no Odoo)

## Cenarios de Uso

### Recebimento simples (1 lote por produto)
```
Picking IN/00123: 500 un produto X (tracking=lot)
Operador preenche: Lote "L2026-001", Qtd 500

Worker:
  1. write(move_line_id, {lot_name: 'L2026-001', quantity: 500})
  2. button_validate → state=done
  3. Odoo cria stock.lot automaticamente
```

### Recebimento multi-lote (N lotes por produto)
```
Picking IN/00124: 1000 un produto Y (tracking=lot)
Operador preenche:
  - Lote "L2026-A", Qtd 600
  - Lote "L2026-B", Qtd 400

Worker:
  1. write(move_line_existente, {lot_name: 'L2026-A', quantity: 600})
  2. create('stock.move.line', {..., lot_name: 'L2026-B', quantity: 400})
  3. button_validate → state=done
```

### Recebimento com data de validade (expiration_date)
```
Picking IN/00125: 500 un produto W (tracking=lot, use_expiration_date=True)
Operador preenche: Lote "L2026-VAL", Qtd 500, Validade 15/06/2026

Worker (_resolver_lote):
  1. Buscar stock.lot existente: search([name='L2026-VAL', product_id=W])
  2. NAO existe → create('stock.lot', {name, product_id, company_id, expiration_date: '2026-06-15 00:00:00'})
  3. write(move_line, {lot_id: novo_lot_id, quantity: 500})  ← usa lot_id, NAO lot_name
  4. button_validate → state=done (lote JA existe com validade)
```

### Recebimento com quality check (measure)
```
Picking IN/00126: 200 kg produto Z + check de umidade
  - Quality check: measure, tolerance 10-15%

Operador: Valor medido = 12.5% → PASS

Worker:
  1. Preencher lotes
  2. write('quality.check', check_id, {'measure': 12.5})
  3. execute_kw('quality.check', 'do_measure', [[check_id]])
  4. button_validate
```

## Validacao Cross-Phase (Pipeline Obrigatorio)

A Fase 4 (Recebimento Fisico) e a etapa FINAL de um pipeline sequencial obrigatorio:

```
Fase 1 (Fiscal) → Fase 2 (Match NF×PO) → Fase 3 (Consolidacao PO) → Fase 4 (Recebimento)
```

### Service: CrossPhaseValidationService

**Arquivo**: `app/recebimento/services/cross_phase_validation_service.py`

```python
from app.recebimento.services.cross_phase_validation_service import CrossPhaseValidationService

service = CrossPhaseValidationService()

# Validar 1 picking
phase_status = service.validar_fases_picking(purchase_order_id, origin)
# → PhaseStatus: pode_receber, tipo_liberacao, bloqueio_motivo, contato_resolucao, diagnostico

# Validar batch (lista de pickings, 2 queries max)
results = service.validar_fases_batch(pickings)
# → Dict: {odoo_picking_id: PhaseStatus}
```

### Tipos de Liberacao

| tipo_liberacao | Significado | Quando |
|----------------|-------------|--------|
| `'full'` | Consolidacao executada (Fase 3 manual) | `ValidacaoNfPoDfe.status='consolidado'` |
| `'finalizado_odoo'` | Odoo ja vinculou PO correto | `ValidacaoNfPoDfe.status='finalizado_odoo'` |
| `'legacy'` | Picking anterior ao sistema | Sem DFE ou sem PO |

### Bloqueios Possiveis

| Bloqueio | Causa | Contato |
|----------|-------|---------|
| Fase 1 bloqueada | Divergencia fiscal | Fiscal |
| Fase 1 nao executada | Scheduler nao rodou | Sistema |
| Fase 1 primeira compra | Cadastro pendente | Fiscal |
| Fase 2 bloqueada | Match NF×PO incompleto | Compras |
| Fase 3 aguardando | Match 100% OK mas consolidacao nao executada | Compras |
| Fase 3 pendente | Fases anteriores nao concluiram | Compras |

### REGRA CRITICA: status='aprovado' NAO e pass-through

`ValidacaoNfPoDfe.status='aprovado'` significa "pronto para consolidar" — a Fase 3 AINDA NAO foi executada.
A consolidacao SEMPRE cria um PO Conciliador novo. Pular causa: NF desvinculada, estoque duplicado.

### Pontos de Integracao

| Metodo | Tipo | Efeito |
|--------|------|--------|
| `buscar_pickings_disponiveis()` | Badge na lista | Campo `fase_validacao` em cada picking |
| `buscar_detalhes_picking()` | Diagnostico completo | Campos `validacao_fases` + `validacao_id_sugerido` |
| `salvar_recebimento()` | **HARD BLOCK** | Raise ValueError se `pode_receber=False` |

### Lookup Chain

```
PickingRecebimento.odoo_purchase_order_id
    → ValidacaoNfPoDfe.odoo_po_vinculado_id (ou po_consolidado_id)
        → ValidacaoFiscalDfe.odoo_dfe_id
```

### Indice de Performance

```sql
CREATE INDEX idx_validacao_nf_po_po_consolidado
ON validacao_nf_po_dfe (po_consolidado_id)
WHERE po_consolidado_id IS NOT NULL;
```

Script de migration: `scripts/add_index_po_consolidado.py`

## Pre-requisitos para Processar

1. **Validacao cross-phase aprovada** (Fases 1→2→3 concluidas)
2. Picking com `state='assigned'`
3. `picking_type_code='incoming'`
4. Soma dos lotes == `product_uom_qty` do move
5. TODOS os quality checks com resultado definido
6. Conexao Odoo funcional

## Referencia Cruzada com Outras Skills

| Skill | Quando usar em vez desta |
|-------|--------------------------|
| `validacao-nf-po` | ANTES do recebimento fisico (match NF x PO, fase 2) |
| `conciliando-odoo-po` | Se precisar split/consolidar POs antes de receber |
| `rastreando-odoo` | CONSULTAR documentos (nao executar) |
| `descobrindo-odoo-estrutura` | Explorar campos nao documentados |
| `executando-odoo-financeiro` | Operacoes financeiras pos-recebimento |
