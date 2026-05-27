---
name: descobrindo-odoo-estrutura
description: "Descobre campos e estrutura de qualquer modelo do Odoo. Lista campos de tabela, busca campo por nome, inspeciona registro, faz consulta generica. Use quando: nao conhecer um modelo Odoo, precisar descobrir nome de campo, explorar estrutura de tabela, consulta em modelo nao mapeado."
---

## QUANDO NAO USAR ESTA SKILL (ULTIMO RECURSO)
Esta skill e ULTIMO RECURSO. Nao use se a tarefa se encaixa em um dominio ja coberto:
- Validacao/match de NF contra PO (dominio de recebimento Fase 2)
- Split ou consolidacao de pedidos de compra (dominio de recebimento Fase 3)
- Preenchimento de lotes ou quality checks (dominio de recebimento Fase 4)
- Operacoes financeiras: pagamentos, extratos, reconciliacoes
- Rastrear fluxo documental completo de NF/PO/SO
- Exportar razao geral ou relatorios contabeis
- Criar nova integracao (service, route, migration)

# Descobrindo Odoo Estrutura

Skill para **descoberta de campos e estrutura** de modelos do Odoo.

> **QUANDO USAR:** Quando o Agent nao conhecer um modelo/campo especifico do Odoo
> e precisar descobrir a estrutura para enriquecer a resposta ao usuario.

## Casos de Uso

1. **Usuario pergunta sobre dado que nao esta mapeado**
   - Agent usa esta skill para descobrir campos
   - Retorna informacao enriquecida ao usuario

2. **Implementar nova consulta**
   - Descobrir estrutura do modelo
   - Mapear campos relevantes
   - Documentar em rastreando-odoo (references/relacionamentos.md)

3. **Debug de integracoes**
   - Inspecionar registro especifico
   - Verificar valores de campos

## Script Disponivel

### descobrindo.py

```bash
source .venv/bin/activate && \
python .claude/skills/descobrindo-odoo-estrutura/scripts/descobrindo.py [opcoes]
```

### Operacoes Disponiveis

| Operacao | Flag | Descricao | Exemplo |
|----------|------|-----------|---------|
| Listar campos | `--listar-campos` | Lista todos os campos do modelo | `--modelo res.partner --listar-campos` |
| Buscar campo | `--buscar-campo` | Busca campo por nome/descricao | `--modelo res.partner --buscar-campo cnpj` |
| Inspecionar | `--inspecionar` | Mostra todos os campos de um registro | `--modelo res.partner --inspecionar 123` |
| Consulta generica | `--filtro` | Consulta com filtro JSON | `--modelo res.partner --filtro '[["name","ilike","teste"]]'` |

### Parametros

| Parametro | Obrigatorio | Descricao |
|-----------|-------------|-----------|
| `--modelo` | Sim | Nome do modelo Odoo (ex: `res.partner`, `account.move`) |
| `--listar-campos` | Nao | Lista todos os campos do modelo |
| `--buscar-campo` | Nao | Termo para buscar nos nomes/descricoes dos campos |
| `--inspecionar` | Nao | ID do registro para inspecionar |
| `--filtro` | Nao | Filtro em formato JSON |
| `--campos` | Nao | Campos a retornar (JSON), usado com --filtro |
| `--limit` | Nao | Limite de resultados (padrao: 10) |
| `--json` | Nao | Saida em formato JSON |

## Exemplos de Uso

### Descobrir campos de um modelo
```bash
python .../descobrindo.py --modelo l10n_br_ciel_it_account.dfe --listar-campos
```

### Buscar campo especifico
```bash
python .../descobrindo.py --modelo res.partner --buscar-campo cnpj
```

### Inspecionar registro
```bash
python .../descobrindo.py --modelo res.partner --inspecionar 123
```

### Consulta generica com filtro
```bash
python .../descobrindo.py \
  --modelo res.partner \
  --filtro '[["vat","ilike","93209765"]]' \
  --campos '["id","name","vat"]' \
  --limit 5
```

---

## Cenarios Praticos de Descoberta

### Cenario 1: Usuario pergunta sobre campo desconhecido

**Situacao**: "Qual o campo que guarda o codigo de barras do produto?"

```bash
# Passo 1: Buscar campos relacionados a "barcode" no modelo product.product
source .venv/bin/activate && \
python .claude/skills/descobrindo-odoo-estrutura/scripts/descobrindo.py \
  --modelo product.product \
  --buscar-campo barcode

# Resultado esperado: Lista campos como barcode, barcode_ids, etc.
```

**Acao apos descoberta**: Documentar em `.claude/references/odoo/MODELOS_CAMPOS.md` se for campo Odoo, ou `.claude/references/modelos/REGRAS_MODELOS.md` se for regra/gotcha de campo local. Para campos, a fonte de verdade sao os schemas auto-gerados em `.claude/skills/consultando-sql/schemas/tables/{tabela}.json`.

---

### Cenario 2: Debug de campo com valor inesperado

**Situacao**: "Qual o valor do campo X no registro Y?"

> **NOTA**: Para RASTREAR documentos (NF, PO, SO), use a skill `rastreando-odoo` em vez desta.

```bash
# Inspecionar TODOS os campos de um registro especifico
source .venv/bin/activate && \
python .claude/skills/descobrindo-odoo-estrutura/scripts/descobrindo.py \
  --modelo res.partner \
  --inspecionar 12345
```

**Resultado**: Ver todos os valores de campos do registro para debug.

---

### Cenario 3: Preparar nova integracao

**Situacao**: "Preciso criar integracao com modelo stock.picking (movimentacao de estoque)"

```bash
# Passo 1: Listar TODOS os campos do modelo
source .venv/bin/activate && \
python .claude/skills/descobrindo-odoo-estrutura/scripts/descobrindo.py \
  --modelo stock.picking \
  --listar-campos \
  --json > /tmp/stock_picking_campos.json

# Passo 2: Buscar campos especificos de interesse
python .claude/skills/descobrindo-odoo-estrutura/scripts/descobrindo.py \
  --modelo stock.picking \
  --buscar-campo partner

python .claude/skills/descobrindo-odoo-estrutura/scripts/descobrindo.py \
  --modelo stock.picking \
  --buscar-campo origin

# Passo 3: Pegar um registro de exemplo para entender estrutura
python .claude/skills/descobrindo-odoo-estrutura/scripts/descobrindo.py \
  --modelo stock.picking \
  --filtro '[["state","=","done"]]' \
  --limit 1 \
  --inspecionar
```

**Proximo passo**: Usar skill `integracao-odoo` para criar o Service com os campos descobertos.

## Modelos Conhecidos (Referencia)

| Modelo | Descricao | Skill Relacionada |
|--------|-----------|-------------------|
| `l10n_br_ciel_it_account.dfe` | Documentos Fiscais | rastreando-odoo |
| `l10n_br_ciel_it_account.dfe.line` | Linhas dos DFE | rastreando-odoo |
| `res.partner` | Parceiros (clientes, fornecedores) | rastreando-odoo |
| `account.move` | Faturas/Lancamentos | rastreando-odoo |
| `account.move.line` | Linhas de fatura | rastreando-odoo |
| `purchase.order` | Pedidos de compra | rastreando-odoo |
| `sale.order` | Pedidos de venda | rastreando-odoo |
| `product.product` | Produtos | - |

## Fluxo de Trabalho

```
Usuario pergunta sobre dado desconhecido
        │
        ▼
Agent verifica: modelo/campo conhecido?
        │
        ├── SIM → Usa rastreando-odoo para consultar fluxos
        │
        └── NAO → Usa esta skill para descobrir
                    │
                    ▼
              descobrindo.py --modelo X --listar-campos
                    │
                    ▼
              Retorna informacao ao usuario
```

## Relacionado

| Skill | Uso |
|-------|-----|
| rastreando-odoo | Consultas e rastreamento de fluxos documentais (NF, PO, SO, titulos) |
| integracao-odoo | Desenvolvimento de novas integracoes |
| gerindo-expedicao | Consultas de carteira, separacoes e estoque |
