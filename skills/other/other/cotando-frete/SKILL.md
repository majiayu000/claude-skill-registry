---
name: cotando-frete
description: |
  Consulta precos de frete por cidade, calcula cotacoes detalhadas e explica logica de calculo.

  USAR QUANDO:
  - Precos/tabelas: "qual preco para Manaus?", "tabelas que atendem Campinas"
  - Cotacao: "quanto sai 5000kg R$50mil para AM?", "frete para SP 3 toneladas"
  - Explicacao: "como funciona o calculo de frete?", "o que e GRIS?"
  - Pedidos: "frete do pedido VCD123", "recalcular frete da separacao"
  - Comparacao: "qual transportadora mais barata para RJ?"
  - Lead time: "prazo de entrega para Manaus?" (lead_time vem nos vinculos)

  - Frete real: "quanto gastei de frete com Atacadao?", "divergencia CTe", "fretes pendentes Odoo"
  - Despesas frete: "custo real do pedido com despesas extras"

  NAO USAR QUANDO:
  - Criar embarque/separacao → usar **gerindo-expedicao**
  - Status de entrega pos-faturamento → usar **monitorando-entregas**
  - Consultas analiticas SQL → usar **consultando-sql**
  - Rastrear NF/PO no Odoo → usar **rastreando-odoo**
allowed-tools: Read, Bash, Glob, Grep
---

# Cotando Frete

Skill para consultar precos de frete, calcular cotacoes detalhadas e explicar a logica de calculo.

---

## Quando NAO Usar Esta Skill

| Situacao | Skill Correta | Por que? |
|----------|---------------|----------|
| Criar embarque/separacao | **gerindo-expedicao** | Esta skill apenas CONSULTA precos — nao cria documentos logisticos |
| Status de entrega pos-faturamento | **monitorando-entregas** | Frete cotado ≠ status de entrega. Apos NF emitida, usar entregas |
| Consultas analiticas SQL complexas | **consultando-sql** | Rankings, agregacoes, tendencias — nao envolvem calculo de frete |
| Rastrear NF/PO/pagamento no Odoo | **rastreando-odoo** | Fluxo documental Odoo e diferente de cotacao de frete |
| Analise completa da carteira (P1-P7) | **analista-carteira** | Priorizacao de embarque exige analise de toda a carteira, nao apenas frete |

---

## DECISION TREE - Qual Script Usar?

### Mapeamento Rapido

| Se a pergunta menciona... | Use este script | Com estes parametros |
|---------------------------|-----------------|----------------------|
| **Tabelas/precos para cidade** | `buscar_tabelas_cidade.py` | `--cidade "Manaus" --uf AM` |
| **Tabelas por tipo de carga** | `buscar_tabelas_cidade.py` | `--cidade "SP" --uf SP --tipo-carga FRACIONADA` |
| **Cotacao com peso/valor** | `calcular_cotacao.py` | `--peso 5000 --valor 50000 --cidade "Manaus" --uf AM` |
| **Cotacao detalhada (breakdown)** | `calcular_cotacao.py` | `+ --detalhado` |
| **Menor prazo** | `calcular_cotacao.py` | `+ --ordenar menor_prazo` |
| **Carga direta especifica** | `calcular_cotacao.py` | `+ --tipo-carga DIRETA` |
| **Frete de pedido existente** | `consultar_pedido_frete.py` | `--pedido VCD2565291` |
| **Frete de separacao** | `consultar_pedido_frete.py` | `--separacao SEP-2025-001` |
| **Frete de NF** | `consultar_pedido_frete.py` | `--nf 144533` |
| **Recalcular frete** | `consultar_pedido_frete.py` | `--pedido VCD123 --recalcular` |
| **Quanto GASTEI de frete** | `consultando_frete_real.py` | `--cliente "Atacadao" --de 2026-01-01` |
| **Frete REAL de pedido** | `consultando_frete_real.py` | `--pedido VCD123` |
| **Divergencia CTe vs cotacao** | `consultando_frete_real.py` | `--divergencias` |
| **Fretes pendentes Odoo** | `consultando_frete_real.py` | `--pendentes-odoo` |
| **Frete por transportadora** | `consultando_frete_real.py` | `--transportadora "Braspress"` |
| **Custo real com despesas** | `consultando_frete_real.py` | `--pedido VCD123 --com-despesas` |

### Regras de Decisao

1. **TABELAS/PRECOS de cidade (sem peso/valor):** → `buscar_tabelas_cidade.py`
2. **COTACAO com peso e valor:** → `calcular_cotacao.py`
3. **Frete de PEDIDO/SEPARACAO/NF existente:** → `consultar_pedido_frete.py`
4. **Frete REAL GASTO (historico, divergencias, pendentes Odoo):** → `consultando_frete_real.py`
5. **EXPLICACAO do calculo:** → Ler `references/calculo_frete.md`
6. **TERMOS (GRIS, ADV, etc.):** → Ler `references/glossario_frete.md`

### Fluxo de Ambiguidade de Cidade

Se o script retornar `ambiguidade: true`:
1. Script retorna `opcoes_uf: ["MG", "SP"]`
2. Agente DEVE perguntar ao usuario qual estado
3. Re-executar script com `--uf` informada

---

## Regras de Negocio (Anti-Alucinacao)

### O Agente PODE Afirmar:
- Precos e valores retornados pelos scripts (baseados em tabelas REAIS)
- Lead time em dias uteis (campo `lead_time` dos vinculos)
- Comparacoes entre transportadoras (baseadas nos resultados)

### O Agente NAO PODE Inventar:
- Precos de frete sem executar o script
- Lead times sem dados no sistema
- Tabelas de frete que nao existem
- Descontos ou negociacoes especiais

### Formulas CORRETAS

| Calculo | Formula |
|---------|---------|
| Frete base | `(peso x valor_kg) + (valor_mercadoria x percentual_valor%)` — e SOMA, nao MAX |
| GRIS | `max(valor x percentual_gris%, gris_minimo)` |
| ADV | `max(valor x percentual_adv%, adv_minimo)` |
| RCA | `valor x percentual_rca%` (sem minimo) |
| Pedagio (fracao) | `ceil(peso/100) x pedagio_por_100kg` |
| ICMS (nao incluso) | `frete_liquido / (1 - icms)` |

### Frete Minimo - CONFUSAO COMUM
- `frete_minimo_peso` = PESO minimo em kg (NAO e valor em R$)
- `frete_minimo_valor` = VALOR minimo em R$ (piso do frete)

---

## Scripts — Referencia Detalhada

**Para parametros completos, retornos JSON e exemplos**: LER `SCRIPTS.md`

| # | Script | Proposito |
|---|--------|-----------|
| 1 | `buscar_tabelas_cidade.py` | Tabelas de frete por cidade |
| 2 | `calcular_cotacao.py` | Cotacao detalhada peso/valor/destino |
| 3 | `consultar_pedido_frete.py` | Frete de pedido/separacao/NF |
| 4 | `consultando_frete_real.py` | Frete real: historico, divergencias, pendentes |

---

## Referencia Cruzada

| Skill | Quando usar em vez desta |
|-------|--------------------------|
| **gerindo-expedicao** | Criar embarque/separacao (antes de faturar) |
| **monitorando-entregas** | Status de entrega (apos faturar) |
| **consultando-sql** | Consultas analiticas complexas |
| **rastreando-odoo** | Rastrear NF/PO/pagamento no Odoo |
| **resolvendo-entidades** | Resolver cliente/cidade para IDs |

---

## References (sob demanda)

| Gatilho na Pergunta | Reference a Ler |
|---------------------|-----------------|
| "como funciona o calculo?" | `references/calculo_frete.md` |
| "o que e GRIS?", termos de frete | `references/glossario_frete.md` |
| "frete minimo peso vs valor" | `references/calculo_frete.md` Passo 2 e 6 |
| "ICMS no frete" | `references/calculo_frete.md` Passo 8 e 9 |
| "direta vs fracionada" | `references/glossario_frete.md` + `references/calculo_frete.md` |

---

## Tabelas do Dominio

| Tabela | Usada por |
|--------|-----------|
| `cidades` | Resolucao de cidade |
| `cidades_atendidas` | buscar_tabelas_cidade.py |
| `tabelas_frete` | buscar_tabelas_cidade.py, calcular_cotacao.py |
| `transportadoras` | Calculo de frete |
| `veiculos` | Carga DIRETA |
| `carteira_principal` | consultar_pedido_frete.py |
| `separacao` | consultar_pedido_frete.py |
| `faturamento_produto` | consultar_pedido_frete.py |
| `fretes` | consultando_frete_real.py |
| `embarques` | consultando_frete_real.py |
| `embarque_itens` | consultando_frete_real.py |
| `despesas_extras` | consultando_frete_real.py |
