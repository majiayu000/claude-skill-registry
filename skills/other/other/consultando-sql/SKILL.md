---
name: consultando-sql
description: "Executa consultas analiticas SQL no banco de dados via linguagem natural. Use para perguntas ad-hoc sobre rankings, agregacoes, distribuicoes, tendencias, cruzamentos de tabelas. Converte perguntas em SQL, valida com Evaluator-Optimizer, e executa read-only. Cobre 104 tabelas ativas via catalogo dinamico."
---

# Consultando SQL - Consultas Analiticas via Linguagem Natural

Skill para **consultas analiticas** ao banco de dados PostgreSQL via linguagem natural.

> **ESCOPO:** Esta skill converte perguntas em SQL e executa read-only.
> Para operacoes logisticas (separacao, estoque, disponibilidade), use `gerindo-expedicao`.
> Para exportar resultados como Excel/CSV, use `exportando-arquivos`.

## Quando Usar

```
USE consultando-sql:
├── Rankings e Top N
│   "Top 10 clientes por valor de carteira"
│   "Vendedores com mais pedidos este mes"
│
├── Agregacoes e Estatisticas
│   "Valor medio de pedido por vendedor"
│   "Quantidade total de pedidos por estado"
│
├── Distribuicoes
│   "Distribuicao de pedidos por incoterm"
│   "Pedidos por faixa de valor"
│
├── Tendencias e Periodos
│   "Faturamento dos ultimos 30 dias"
│   "Evolucao de pedidos por mes"
│
├── Cruzamentos entre Tabelas
│   "Produtos sem estoque mas com pedidos pendentes"
│   "Clientes com separacoes pendentes e valor alto"
│
├── Consultas Financeiras
│   "Top 10 clientes por valor de contas a receber vencidas"
│   "Total de titulos a pagar nos proximos 30 dias"
│
├── Analise de Fretes
│   "Valor total de fretes por transportadora nos ultimos 60 dias"
│   "Custo medio de frete por UF de destino"
│
└── Qualquer pergunta analitica/estatistica ad-hoc
```

## Quando NAO Usar

```
NAO USE consultando-sql (use gerindo-expedicao):
├── Consulta especifica de 1 pedido/cliente
│   "Tem pedido do Atacadao?" -> gerindo-expedicao
│
├── Operacoes com side-effects
│   "Crie separacao" -> gerindo-expedicao
│
├── Projecao de estoque/disponibilidade
│   "Quando VCD123 fica disponivel?" -> gerindo-expedicao
│
└── Consultas que exigem logica complexa de negocio
    "Qual a prioridade P1-P7?" -> subagente analista-carteira
```

## Regras Criticas

1. **Feature Flag**: Requer `AGENT_TEXT_TO_SQL=true`. Se desabilitado, retorna aviso.
2. **Seguranca Multi-Camada**:
   - Generator: Apenas SELECT (instruido via prompt)
   - Evaluator: Valida corretude semantica e sintatica com schema detalhado
   - Safety: Regex validator bloqueia DELETE/DROP/INSERT/UPDATE/tabelas proibidas/funcoes perigosas
   - Executor: `SET TRANSACTION READ ONLY` + timeout 5s
3. **Limites**: Max 500 linhas retornadas. Timeout 5 segundos.
4. **Guardrail Anti-Alucinacao**: Evaluator recebe schema DETALHADO (campos, tipos, FKs) apenas das tabelas usadas e corrige campos inexistentes.
5. **Tabelas Bloqueadas**: usuarios, permissions, agent_sessions, agent_memories, agent_memory_versions, alembic_version, portal_sessoes, tagplus_oauth_token, e 9 outras (17 total)

## Script Principal

### text_to_sql.py

```bash
source .venv/bin/activate && \
AGENT_TEXT_TO_SQL=true python .claude/skills/consultando-sql/scripts/text_to_sql.py --pergunta "PERGUNTA"
```

## Parametros

| Parametro | Obrigatorio | Descricao | Exemplo |
|-----------|-------------|-----------|---------|
| `--pergunta` / `-p` | Sim | Pergunta em linguagem natural (portugues) | `--pergunta "Top 10 clientes por valor"` |
| `--debug` | Nao | Mostrar detalhes de cada etapa do pipeline | `--debug` |

## Exemplos de Uso

### Ranking de clientes (tabela core)
```bash
source .venv/bin/activate && \
AGENT_TEXT_TO_SQL=true python .claude/skills/consultando-sql/scripts/text_to_sql.py \
  --pergunta "Top 10 clientes por valor total na carteira"
```

### Contas a receber vencidas (tabela expandida)
```bash
AGENT_TEXT_TO_SQL=true python .../text_to_sql.py \
  --pergunta "Top 10 clientes por valor de contas a receber vencidas"
```

### Fretes por transportadora (tabela expandida)
```bash
AGENT_TEXT_TO_SQL=true python .../text_to_sql.py \
  --pergunta "Valor total de fretes por transportadora nos ultimos 60 dias"
```

### Cross-domain (carteira + faturamento)
```bash
AGENT_TEXT_TO_SQL=true python .../text_to_sql.py \
  --pergunta "Clientes com pedidos pendentes mas sem faturamento nos ultimos 30 dias"
```

### Distribuicao por estado
```bash
AGENT_TEXT_TO_SQL=true python .../text_to_sql.py \
  --pergunta "Quantos pedidos pendentes por estado?"
```

### Debug detalhado
```bash
AGENT_TEXT_TO_SQL=true python .../text_to_sql.py \
  --pergunta "Top 5 vendedores por valor total" --debug
```

## Retorno JSON

### Sucesso
```json
{
  "sucesso": true,
  "pergunta": "Top 10 clientes por valor total na carteira",
  "sql": "SELECT cnpj_cpf, raz_social, ROUND(SUM(qtd_saldo_produto_pedido * preco_produto_pedido)::numeric, 2) AS valor_total FROM carteira_principal WHERE ativo = True AND qtd_saldo_produto_pedido > 0 GROUP BY cnpj_cpf, raz_social ORDER BY valor_total DESC LIMIT 10",
  "sql_original": "SELECT ...",
  "dados": [
    {"cnpj_cpf": "75.315.333/0183-18", "raz_social": "ATACADAO S.A.", "valor_total": 5228553.10}
  ],
  "colunas": ["cnpj_cpf", "raz_social", "valor_total"],
  "total_linhas": 10,
  "aviso": "SQL corrigida pelo evaluator (tentativa 1): ...",
  "tabelas_usadas": ["carteira_principal"],
  "etapas": {
    "generator_ms": 1800,
    "evaluator_ms": 2200,
    "safety": {"safe": true, "concerns": []},
    "executor_ms": 2000
  },
  "tempo_total_ms": 6000
}
```

### Erro (seguranca)
```json
{
  "sucesso": false,
  "pergunta": "DELETE FROM carteira_principal",
  "sql": null,
  "aviso": "Query bloqueada por seguranca: Keywords proibidas: DELETE"
}
```

### Feature flag desabilitada
```json
{
  "sucesso": false,
  "pergunta": "Top 10 clientes",
  "aviso": "Text-to-SQL desabilitado. Ative com AGENT_TEXT_TO_SQL=true"
}
```

## Arquitetura B: Catalogo Completo + Retrieval em 2 Fases

```
Pergunta do usuario
    |
    v
[GENERATOR] Haiku recebe CATALOGO LEVE (104 tabelas, ~2.7K tokens)
    |         Gera SQL com nomes de tabela corretos, campos aproximados
    v
[RETRIEVAL] Extrai tabelas do SQL (regex FROM/JOIN)
    |         Carrega schemas DETALHADOS apenas das tabelas usadas (2-4 tipicamente)
    v
[EVALUATOR] Haiku recebe SCHEMA DETALHADO (campos, tipos, FKs, regras)
    |         Valida campos, corrige nomes, adiciona filtros
    |-- Aprovado? -> Safety
    |-- Corrigido? -> Usa SQL corrigida -> Safety
    |-- Reprovado? -> Re-gera com feedback (max 2 tentativas)
    |
    v
[SAFETY] Regex validator (keywords, funcoes, tabelas bloqueadas)
    |-- Seguro? -> Executor
    |-- Bloqueado? -> Retorna erro
    |
    v
[EXECUTOR] SET TRANSACTION READ ONLY + timeout 5s + LIMIT 500
    |
    v
JSON com dados + SQL usada + tabelas_usadas + metricas de tempo
```

### Vantagem da Arquitetura B

- **Generator** ve TODAS as 104 tabelas ativas (nome + descricao) → encontra qualquer tabela relevante
- **Evaluator** recebe schema DETALHADO apenas das 2-4 tabelas usadas → validacao precisa
- **2 chamadas LLM** (mesmo que antes) → sem overhead de latencia
- **Cross-domain nativo**: sem barreira de dominios, JOIN entre financeiro + logistica funciona

## Cobertura de Tabelas

| Metrica | Valor |
|---------|-------|
| Total de tabelas no banco | ~196 |
| Tabelas bloqueadas (auth, agent, etc.) | 17 |
| Tabelas mortas (0 registros em prod) | 57 |
| Tabelas irrelevantes (curadoria manual) | 18 |
| Tabelas no catalogo | **104** |
| Tabelas core (schema manual curado) | 9 |
| Tabelas auto-geradas | 95 |
| Cobertura (tabelas analiticas relevantes) | **100%** |

### Tabelas Core (schema manual com regras de negocio)

| Tabela | Descricao |
|--------|-----------|
| `carteira_principal` | Pedidos com saldo pendente. Fonte da verdade para demanda. |
| `separacao` | Itens separados para expedicao. Projeta saidas de estoque. |
| `movimentacao_estoque` | Movimentos de estoque: entradas, saidas, ajustes, producao. |
| `programacao_producao` | Producao programada por data e linha. |
| `cadastro_palletizacao` | Cadastro de produtos com peso, pallet, conversoes. |
| `faturamento_produto` | NFs emitidas por produto. Registros de faturamento. |
| `embarques` | Embarques que agrupam separacoes para transporte. |
| `embarque_itens` | Itens individuais dentro de um embarque. |
| `saldo_standby` | Pedidos em espera: saldo, comercial ou PCP. |

### Dominios Expandidos

- **Financeiro**: contas_a_receber, contas_a_pagar, extrato_item, baixa_pagamento_item, baixa_titulo_item, cnab_retorno_item, comprovante_*
- **Fretes**: fretes, faturas_frete, despesas_extras, conhecimento_transporte, tabelas_frete, aprovacoes_frete
- **Devolucoes**: nf_devolucao, nf_devolucao_linha, ocorrencia_devolucao, frete_devolucao
- **Recebimento**: validacao_fiscal_dfe, match_nf_po_*, divergencia_nf_po, picking_recebimento_*
- **Rastreamento**: entregas_monitoradas, entregas_rastreadas, agendamentos_entrega, eventos_entrega
- **Cadastros**: transportadoras, cidades, cadastro_rota, grupo_empresarial, depara_produto_cliente

## Geracao de Schemas

Os schemas sao auto-gerados a partir dos modelos SQLAlchemy:

```bash
source .venv/bin/activate && \
python .claude/skills/consultando-sql/scripts/generate_schemas.py
```

### Opcoes
```bash
# Apenas estatisticas (nao gera arquivos)
python .../generate_schemas.py --stats
```

### Arquivos Gerados

| Arquivo | Descricao |
|---------|-----------|
| `schemas/catalog.json` | Catalogo leve: nome + descricao + 3 campos-chave por tabela (~25KB) |
| `schemas/tables/{tabela}.json` | Schema detalhado por tabela: campos, tipos, FKs, indices (104 arquivos) |
| `schemas/relationships.json` | Mapa de ForeignKeys entre tabelas (171 relacionamentos) |
| `schemas/schema.json` | Schema manual curado das 9 tabelas core (mantido como referencia) |

### Quando Regenerar

Regenere schemas quando:
- Novas tabelas forem adicionadas ao sistema
- Campos forem alterados em modelos existentes
- Novas descricoes forem adicionadas ao `TABLE_DESCRIPTIONS` em `generate_schemas.py`

## Tratamento de Erros

| Erro | Causa | Comportamento |
|------|-------|---------------|
| Feature flag desabilitada | `AGENT_TEXT_TO_SQL=false` | Retorna aviso, pipeline nao executa |
| ANTHROPIC_API_KEY ausente | Env var nao configurada | Retorna aviso |
| Schema nao encontrado | catalog.json ou schema.json faltando | RuntimeError |
| SQL bloqueada (safety) | DELETE, DROP, tabela proibida | `sucesso=false`, aviso com motivo |
| Timeout (>5s) | Query muito pesada | RuntimeError com sugestao de simplificar |
| Campo/tabela inexistente | Haiku alucionou campo nao corrigido pelo Evaluator | Erro PostgreSQL capturado |

## Notas

- Custo estimado: ~$0.010/query (2 chamadas Haiku)
- Tempo medio: 6-10 segundos (cold start + LLM + DB)
- Catalogo dinamico: 104 tabelas ativas, ~2.700 tokens no prompt do Generator
- Tabelas mortas (0 registros) excluidas via DEAD_TABLES
- Tabelas irrelevantes (curadoria manual) excluidas via IRRELEVANT_TABLES
- Evaluator focado: recebe schema detalhado apenas das 2-4 tabelas usadas
- Retry loop: Evaluator re-gera SQL com feedback se reprovada (max 2 tentativas)
- Todos os valores monetarios em BRL (R$)
- Datas retornadas em ISO 8601 (YYYY-MM-DD)

## Relacionado

| Skill | Uso |
|-------|-----|
| `gerindo-expedicao` | Consultas operacionais (pedido especifico, separacao, estoque) |
| `exportando-arquivos` | Exportar resultado como Excel/CSV para download |
| `lendo-arquivos` | Processar planilhas enviadas pelo usuario |

> **NOTA**: Esta skill e para consultas ANALITICAS ao banco de dados.
> Para operacoes logisticas do dia-a-dia, use `gerindo-expedicao`.
> Para exportar os resultados, combine com `exportando-arquivos`.
