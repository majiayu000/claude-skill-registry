---
description: Visao 360 de produto - agrega dados de cadastro, estoque, custo, faturamento, carteira e producao em uma consulta unificada.
triggers:
  - resumo completo de produto
  - visao 360 produto
  - tudo sobre produto X
  - producao vs realizado
  - programado vs produzido
---

# Skill: visao-produto

## Proposito
Consulta cross-domain de produto. Agrega 7+ tabelas (CadastroPalletizacao, MovimentacaoEstoque, CarteiraPrincipal, Separacao, FaturamentoProduto, CustoConsiderado, ProgramacaoProducao) em uma visao unificada.

## Mapeamento Rapido

| Se a pergunta menciona... | Use este script | Com estes parametros |
|---------------------------|-----------------|----------------------|
| **Resumo completo de produto** ("tudo sobre palmito") | `consultando_produto_completo.py` | `--produto palmito` |
| **Producao vs realizado** ("cumpriram a programacao?") | `consultando_producao_vs_real.py` | `--produto palmito --de 2026-01-01 --ate 2026-01-31` |
| **Producao geral** (sem produto especifico) | `consultando_producao_vs_real.py` | `--de 2026-01-01 --ate 2026-01-31` |

## Regras de Decisao

1. **VISAO 360**: "resumo completo", "tudo sobre", "dados do produto"
   -> `consultando_produto_completo.py --produto X`

2. **PRODUCAO VS REAL**: "producao", "programado", "realizado", "cumpriu", "OP"
   -> `consultando_producao_vs_real.py --produto X --de Y --ate Z`

3. SE o usuario menciona APENAS estoque, sem querer visao completa:
   -> Use `gerindo-expedicao` (consultando_produtos_estoque.py --produto X --completo)

4. SE o usuario menciona APENAS faturamento/vendas:
   -> Use `consultando-sql` (query direta em faturamento_produto)

---

## Scripts

### 1. consultando_produto_completo.py

**Proposito:** Visao 360 de um produto — cadastro, estoque, custo, demanda, faturamento, producao.

```bash
source .venv/bin/activate && \
python .claude/skills/visao-produto/scripts/consultando_produto_completo.py [parametros]
```

| Parametro | Descricao | Exemplo |
|-----------|-----------|---------|
| `--produto` | Nome ou codigo do produto | `--produto palmito`, `--produto "az verde"` |

**Retorna JSON com secoes:**
- `cadastro`: dados de CadastroPalletizacao (peso, palletizacao, categoria, dimensoes)
- `estoque`: saldo atual de MovimentacaoEstoque (entradas - saidas)
- `custo`: custo considerado atual de CustoConsiderado
- `demanda_carteira`: total pendente em CarteiraPrincipal (qtd_saldo_produto_pedido > 0)
- `demanda_separacao`: total em separacao (Separacao com sincronizado_nf=False AND qtd_saldo > 0)
- `faturamento_recente`: ultimos 30 dias de FaturamentoProduto
- `producao_programada`: proximos 14 dias de ProgramacaoProducao

---

### 2. consultando_producao_vs_real.py

**Proposito:** Comparar producao PROGRAMADA (ProgramacaoProducao) vs REALIZADA (MovimentacaoEstoque tipo_movimentacao=PRODUCAO).

```bash
source .venv/bin/activate && \
python .claude/skills/visao-produto/scripts/consultando_producao_vs_real.py [parametros]
```

| Parametro | Descricao | Exemplo |
|-----------|-----------|---------|
| `--produto` | Nome ou codigo do produto (opcional — se omitido, retorna todos) | `--produto palmito` |
| `--de` | Data inicio (YYYY-MM-DD) | `--de 2026-01-01` |
| `--ate` | Data fim (YYYY-MM-DD) | `--ate 2026-01-31` |
| `--limite` | Max resultados (default: 50) | `--limite 20` |

**Retorna JSON com:**
- `comparativo`: lista de produtos com qtd_programada, qtd_realizada, diferenca, percentual_cumprimento
- `resumo`: totais gerais e mensagem

---

## Tabelas do Dominio

| Tabela | Chave de produto | Uso |
|--------|-----------------|-----|
| `cadastro_palletizacao` | `cod_produto` | Master data (peso, pallet, dimensoes) |
| `movimentacao_estoque` | `cod_produto` | Saldo e movimentos |
| `custo_considerado` | `cod_produto` | Custo final (WHERE custo_atual = true) |
| `carteira_principal` | `cod_produto` | Demanda pendente (qtd_saldo_produto_pedido > 0) |
| `separacao` | `cod_produto` | Em separacao (sincronizado_nf=False AND qtd_saldo > 0) |
| `faturamento_produto` | `cod_produto` | Vendas faturadas |
| `programacao_producao` | `cod_produto` | Agenda de producao |

**NOTA**: TODAS as tabelas usam `cod_produto`. Filtros de pendencia: CarteiraPrincipal usa `qtd_saldo_produto_pedido > 0`, Separacao usa `sincronizado_nf = False AND qtd_saldo > 0`.
