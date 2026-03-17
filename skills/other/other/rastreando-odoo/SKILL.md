---
name: rastreando-odoo
description: |
  Rastreia fluxos documentais completos no Odoo, executa auditorias financeiras e gerencia conciliacoes bancarias.

  USAR QUANDO:
  - Rastrear NF de compra/venda: "rastreie NF 12345", "fluxo da nota 54321"
  - Rastrear pedido de compra: "rastreie PO00789", "fluxo do pedido de compra"
  - Rastrear pedido de venda: "rastreie VCD123", "fluxo do VFB456"
  - Rastrear por parceiro: "documentos do Atacadao", "fluxo do fornecedor Vale Sul"
  - Rastrear por CNPJ: "rastreie 18467441000123"
  - Rastrear por chave NF-e: "rastreie 3525..."
  - Ver titulos e conciliacoes: "pagamentos da NF 12345", "titulos do PO00789"
  - Verificar devolucoes: "devolucao da NF 54321", "nota de credito"
  - Auditoria de faturas de compra: "auditoria faturas novembro", "faturas fornecedores"
  - Auditoria de extrato bancario: "extrato bancario 2024", "conciliacao bancaria"
  - Mapeamento de vinculos: "extratos sem vinculo", "titulos soltos", "faturas sem pagamento"
  - Vincular extrato com fatura via Excel: "processar planilha de vinculacao", "conciliar via Excel"

  NAO USAR QUANDO:
  - Descobrir campos de modelo desconhecido (esta skill rastreia fluxos, nao explora estrutura)
  - Criar lancamentos fiscais (esta skill apenas consulta, nao cria documentos)
  - Apenas listar registros sem rastrear fluxo
---


## QUANDO NAO USAR ESTA SKILL
- Match NF x PO especifico (Fase 2 do recebimento, nao rastreamento geral)
- Split/consolidar PO (Fase 3, operacao de escrita em POs)
- Recebimento fisico com lotes/quality checks (Fase 4, operacao no armazem)
- Criar pagamentos ou reconciliar extratos (operacao financeira de escrita)
- Explorar modelo Odoo desconhecido (esta skill usa modelos ja mapeados)
- Criar nova integracao/service (esta skill consulta, nao desenvolve)

# Rastreando Odoo

Rastreia fluxo completo de documentos e executa auditorias financeiras.

## Fluxos Suportados

| Fluxo | Caminho |
|-------|---------|
| **Compra** | DFE → Requisicao → PO → Fatura → Titulos → Conciliacao |
| **Venda** | SO (VCD/VFB/VSC) → Picking → Fatura → Titulos → Conciliacao |
| **Devolucao** | DFE (finnfe=4) → Nota Credito → NF Original → Pedido Original |

## Workflow

1. **Normalizar entrada** → Transforma texto humano em ID Odoo
2. **Detectar tipo** → Identifica se e compra, venda ou devolucao
3. **Rastrear fluxo** → Navega pelos relacionamentos
4. **Retornar JSON** → Estrutura completa com todos os documentos

## Scripts

### [normalizar.py](scripts/normalizar.py)

Transforma mencoes humanas em identificadores Odoo.

```bash
source .venv/bin/activate

# Por nome de parceiro
python .claude/skills/rastreando-odoo/scripts/normalizar.py "Atacadao" --json

# Por CNPJ
python .claude/skills/rastreando-odoo/scripts/normalizar.py "18467441" --json

# Por numero de NF
python .claude/skills/rastreando-odoo/scripts/normalizar.py "NF 12345" --json

# Por PO (formatos: PO00123, C2513147)
python .claude/skills/rastreando-odoo/scripts/normalizar.py "PO00789" --json

# Por SO (prefixos: VCD, VFB, VSC)
python .claude/skills/rastreando-odoo/scripts/normalizar.py "VCD123" --json

# Apenas detectar tipo (sem buscar)
python .claude/skills/rastreando-odoo/scripts/normalizar.py "VCD123" --detectar
```

### [rastrear.py](scripts/rastrear.py)

Rastreia fluxo completo a partir de qualquer entrada.

```bash
source .venv/bin/activate

# Por chave NF-e
python .claude/skills/rastreando-odoo/scripts/rastrear.py "35251218467441..." --json

# Por numero de NF
python .claude/skills/rastreando-odoo/scripts/rastrear.py "NF 12345" --json

# Por PO ou SO
python .claude/skills/rastreando-odoo/scripts/rastrear.py "PO00789" --json
python .claude/skills/rastreando-odoo/scripts/rastrear.py "VCD123" --json

# Por parceiro
python .claude/skills/rastreando-odoo/scripts/rastrear.py "Atacadao" --json

# Forcar tipo de fluxo
python .claude/skills/rastreando-odoo/scripts/rastrear.py "12345" --fluxo compra --json
```

### [auditoria_faturas_compra.py](scripts/auditoria_faturas_compra.py)

Extrai auditoria completa de faturas de compra com titulos, pagamentos e conciliacoes.

```bash
source .venv/bin/activate

# Auditoria de mes especifico
python .claude/skills/rastreando-odoo/scripts/auditoria_faturas_compra.py --mes 11 --ano 2025

# Todo o periodo disponivel
python .claude/skills/rastreando-odoo/scripts/auditoria_faturas_compra.py --all

# Exportar para JSON
python .claude/skills/rastreando-odoo/scripts/auditoria_faturas_compra.py --mes 11 --ano 2025 --json

# Exportar formato tabular (para Excel via skill exportando-arquivos)
python .claude/skills/rastreando-odoo/scripts/auditoria_faturas_compra.py --mes 11 --ano 2025 --excel
```

**Dados extraidos**: fatura, fornecedor, CNPJ, parcelas, vencimentos, pagamentos, conciliacao bancaria, notas de credito/estornos.

### [auditoria_extrato_bancario.py](scripts/auditoria_extrato_bancario.py)

Extrai auditoria de extrato bancario com status de conciliacao.

```bash
source .venv/bin/activate

# Extrato de periodo
python .claude/skills/rastreando-odoo/scripts/auditoria_extrato_bancario.py --inicio 2024-07-01 --fim 2025-12-31

# Exportar para JSON
python .claude/skills/rastreando-odoo/scripts/auditoria_extrato_bancario.py --inicio 2024-07-01 --fim 2025-12-31 --json

# Exportar formato tabular (para Excel)
python .claude/skills/rastreando-odoo/scripts/auditoria_extrato_bancario.py --inicio 2024-07-01 --fim 2025-12-31 --excel
```

**Dados extraidos**: data, referencia, valor, parceiro, conta bancaria, status conciliacao.

### [mapeamento_vinculos_completo.py](scripts/mapeamento_vinculos_completo.py)

Extrai 5 visoes cruzadas para identificar registros "soltos" (sem vinculo):

```bash
source .venv/bin/activate

# Mapeamento de pagamentos (extratos < 0)
python .claude/skills/rastreando-odoo/scripts/mapeamento_vinculos_completo.py --inicio 2024-07-01 --fim 2025-12-31 --pagamentos

# Exportar JSON completo
python .claude/skills/rastreando-odoo/scripts/mapeamento_vinculos_completo.py --inicio 2024-07-01 --fim 2025-12-31 --json

# Exportar formato tabular (para Excel)
python .claude/skills/rastreando-odoo/scripts/mapeamento_vinculos_completo.py --inicio 2024-07-01 --fim 2025-12-31 --excel
```

**Visoes extraidas**:
- EXTRATOS: titulo_ids, fatura_ids, nc_ids, payment_ids, CNPJ, conta_bancaria
- TITULOS: extrato_ids, fatura_id, nc_ids, payment_ids, parcela, CNPJ
- FATURAS: titulo_ids, extrato_ids, nc_ids, chave_nfe, CNPJ
- NOTAS_CREDITO: fatura_origem_id, titulo_ids, extrato_ids, CNPJ
- PAGAMENTOS: extrato_ids, titulo_ids, CNPJ

### [vincular_extrato_fatura_excel.py](scripts/vincular_extrato_fatura_excel.py)

Processa planilha Excel para vincular extratos com faturas automaticamente.

```bash
source .venv/bin/activate

# Simular (dry-run)
python .claude/skills/rastreando-odoo/scripts/vincular_extrato_fatura_excel.py -a planilha.xlsx --dry-run

# Executar modo otimizado (3-4x mais rapido)
python .claude/skills/rastreando-odoo/scripts/vincular_extrato_fatura_excel.py -a planilha.xlsx --otimizado

# Executar em lotes de 500
python .claude/skills/rastreando-odoo/scripts/vincular_extrato_fatura_excel.py -a planilha.xlsx --otimizado -o 0 -b 500
```

**Colunas esperadas na planilha**:
- A (0): ID do extrato
- H (7): FATURA (name)
- I (8): CNPJ
- K (10): FATURA.1 (ID)
- L (11): PARCELA
- M (12): VALOR
- T (19): Movimento

**Processo**: Cria account.payment, posta, reconcilia com titulo e extrato.

## Estrutura JSON de Saida

### Fluxo de Compra

```json
{
  "entrada": "NF 12345",
  "sucesso": true,
  "fluxo": {
    "tipo": "compra",
    "dfe": { "id": 1234, "nfe_infnfe_ide_nnf": "12345" },
    "pedido_compra": { "id": 789, "name": "PO00789", "amount_total": 10000.00 },
    "fatura": { "id": 456, "name": "BILL/2025/0001", "payment_state": "paid" },
    "titulos": [{ "date_maturity": "2025-01-15", "debit": 10000.00, "reconciled": true }]
  }
}
```

### Fluxo de Venda

```json
{
  "fluxo": {
    "tipo": "venda",
    "pedido_venda": { "id": 500, "name": "VCD123", "state": "sale" },
    "pickings": [{ "name": "WH/OUT/00600", "state": "done" }],
    "faturas": [...],
    "titulos": [...]
  }
}
```

## References

| Arquivo | Conteudo |
|---------|----------|
| [relacionamentos.md](references/relacionamentos.md) | Mapeamento de campos, relacionamentos entre tabelas, estrategias de navegacao |
| [troubleshooting.md](references/troubleshooting.md) | Solucoes para problemas comuns de busca e rastreamento |

## Prefixos de Pedido de Venda

| Prefixo | Filial |
|---------|--------|
| VCD | Centro de Distribuicao |
| VFB | Filial FB |
| VSC | Filial SC |

## Skills Relacionadas

| Skill | Quando usar |
|-------|-------------|
| [descobrindo-odoo-estrutura](../descobrindo-odoo-estrutura/SKILL.md) | Descobrir campos de modelos nao mapeados |
| [integracao-odoo](../integracao-odoo/SKILL.md) | Criar novos lancamentos fiscais (CTe, despesas) |
| [exportando-arquivos](../exportando-arquivos/SKILL.md) | Exportar resultados de auditoria para Excel |
