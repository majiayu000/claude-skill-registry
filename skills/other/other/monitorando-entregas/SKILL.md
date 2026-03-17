---
name: monitorando-entregas
description: |
  Consulta status de entregas, datas de embarque/faturamento, canhotos e devolucoes.

  USAR QUANDO (NFs JA FATURADAS):
  - Status: "NF 12345 foi entregue?", "status da entrega do Atacadao"
  - Datas de embarque: "que dia saiu?", "que dia embarcou?", "quando expediu?"
  - Datas de faturamento: "quando faturou?", "data da NF"
  - Datas de entrega: "quando chegou?", "foi entregue quando?"
  - Canhoto: "tem canhoto da NF?", "canhotos pendentes"
  - Devolucoes: "houve devolucao?", "NFs devolvidas"
  - Pendencias: "entregas pendentes", "NFs no CD", "entregas com problema"

  NAO USAR QUANDO (ANTES de faturar):
  - Pedidos em carteira/separacao → usar **gerindo-expedicao**
  - Estoque, disponibilidade → usar **gerindo-expedicao**
  - Criar separacao → usar **gerindo-expedicao**
  - Rastrear NF no Odoo → usar **rastreando-odoo**
allowed-tools: Read, Bash, Glob, Grep
---

# Monitorando Entregas

Skill para consultar status de entregas, canhotos, devoluções e agendamentos.

---

## Índice

1. [Quando NÃO Usar Esta Skill](#quando-não-usar-esta-skill)
2. [DECISION TREE - Qual Script Usar?](#decision-tree---qual-script-usar)
3. [Regras de Negócio (Anti-Alucinação)](#regras-de-negócio-anti-alucinação)
4. [Scripts Disponíveis](#scripts-disponíveis)
5. [Referência Cruzada](#referência-cruzada)
6. [References](#references)

---

## Quando NÃO Usar Esta Skill

| Situação | Usar em vez desta |
|----------|-------------------|
| Pedido ainda não faturado | **gerindo-expedicao** |
| Rastrear NF/PO/pagamento no Odoo | **rastreando-odoo** |
| Criar separação de pedido | **gerindo-expedicao** |
| Análise completa da carteira (P1-P7) | **analista-carteira** (subagente) |
| Consultas SQL analíticas complexas | **consultando-sql** |

---

## DECISION TREE - Qual Script Usar?

### Mapeamento Rápido

| Se a pergunta menciona... | Use este script | Com estes parâmetros |
|---------------------------|-----------------|----------------------|
| **Status de NF específica** | `consultando_status_entrega.py` | `--nf 12345` |
| **Status por cliente/CNPJ** | `consultando_status_entrega.py` | `--cliente "Atacadao"` ou `--cnpj 123...` |
| **Data de embarque** ("que dia saiu?", "quando embarcou?", "quando expediu?") | `consultando_status_entrega.py` | `--nf 12345` (retorna `data_embarque`) |
| **Data de faturamento** ("quando faturou?", "data da NF") | `consultando_status_entrega.py` | `--nf 12345` (retorna `data_faturamento`) |
| **Data de entrega** ("quando chegou?", "foi entregue quando?") | `consultando_status_entrega.py` | `--nf 12345` (retorna `data_hora_entrega_realizada`) |
| **Entregas pendentes** | `consultando_status_entrega.py` | `--pendentes` |
| **Entregas no CD** | `consultando_status_entrega.py` | `--no-cd` |
| **Entregas reagendadas** | `consultando_status_entrega.py` | `--reagendadas` |
| **Entregas entregues** (período) | `consultando_status_entrega.py` | `--entregues --de 2025-01-01 --ate 2025-01-31` |
| **Canhoto de NF** | `consultando_canhotos.py` | `--nf 12345` |
| **Canhotos pendentes** | `consultando_canhotos.py` | `--pendentes` |
| **Devoluções abertas** | `consultando_devolucoes.py` | `--abertas` |
| **Devolução de NF específica** | `consultando_devolucoes.py` | `--nf 12345` |
| **Devoluções de cliente** | `consultando_devolucoes_detalhadas.py` | `--cliente "Sendas"` |
| **Produtos mais devolvidos** | `consultando_devolucoes_detalhadas.py` | `--ranking` |
| **Custo de devoluções** | `consultando_devolucoes_detalhadas.py` | `--custo` |
| **Agendamento de entrega** | `consultando_agendamentos.py` | `--nf 12345` |
| **Agendamentos do dia** | `consultando_agendamentos.py` | `--data 2025-02-05` |

### Regras de Decisão (em ordem de prioridade)

1. **Se pergunta sobre STATUS de entrega:**
   → Use `consultando_status_entrega.py`
   → Exemplo: "NF 12345 foi entregue?" → `--nf 12345`

2. **Se pergunta sobre CANHOTO:**
   → Use `consultando_canhotos.py`
   → Exemplo: "tem canhoto da NF?" → `--nf 12345`

3. **Se pergunta sobre DEVOLUÇÃO:**
   → Use `consultando_devolucoes.py`
   → Exemplo: "houve devolução?" → `--nf 12345`

4. **Se pergunta sobre AGENDAMENTO:**
   → Use `consultando_agendamentos.py`
   → Exemplo: "quando está agendada?" → `--nf 12345`

5. **Se pergunta sobre PROBLEMAS genéricos:**
   → Use `consultando_status_entrega.py --problemas`
   → Inclui: nf_cd=True OU reagendar=True

---

## Regras de Negócio (Anti-Alucinação)

### status_finalizacao - Valores Válidos

| Valor | Significado |
|-------|-------------|
| `NULL` | **Em andamento/pendente** - NF ainda não finalizada |
| `Entregue` | NF entregue com sucesso ao cliente |
| `Cancelada` | Entrega cancelada (NF não será entregue) |
| `Devolvida` | Cliente devolveu a mercadoria |
| `Troca de NF` | NF substituída por outra (ver campo `nova_nf`) |
| `Sinistro` | Perda/extravio da mercadoria |
| `nao_finalizado` | NF saiu do monitoramento sem conclusão |

### Fórmulas CORRETAS (O que o agente DEVE usar)

| Consulta | Fórmula SQL CORRETA |
|----------|---------------------|
| Entregas pendentes | `status_finalizacao IS NULL` |
| Entregas finalizadas | `status_finalizacao IS NOT NULL` |
| Entregas entregues | `status_finalizacao = 'Entregue'` |
| Entregas devolvidas | `status_finalizacao = 'Devolvida' OR teve_devolucao = True` |
| Entregas com problema | `nf_cd = True OR reagendar = True` |

### O Agente PODE Afirmar:

- Status atual da entrega (baseado em `status_finalizacao`)
- Se tem canhoto (baseado em `canhoto_arquivo IS NOT NULL`)
- Data de entrega (baseado em `data_hora_entrega_realizada`)
- Se está no CD (baseado em `nf_cd = True`)
- Se precisa reagendar (baseado em `reagendar = True`)

### O Agente NÃO PODE Inventar:

- Lead time se não calculado pelo script
- Motivo de devolução sem consultar `ocorrencia_devolucao`
- Status de agendamento sem consultar `agendamentos_entrega`
- Previsão de entrega sem dados no sistema

### Campos Importantes

| Campo | Descrição |
|-------|-----------|
| `entregue` | **Boolean** - True APENAS quando `status_finalizacao='Entregue'`. NÃO usar isoladamente para filtrar pendentes |
| `nf_cd` | **Boolean** - True = NF está fisicamente no CD. Pode ser NF que nunca saiu OU que saiu e voltou |
| `reagendar` | **Boolean** - True = cliente solicitou reagendamento |
| `teve_devolucao` | **Boolean** - True = houve devolução (mesmo que parcial) |
| `nova_nf` | Número da NF substituta (quando `status_finalizacao='Troca de NF'`) |

---

## Scripts Disponíveis

### 1. consultando_status_entrega.py

Consulta status de entregas com vários filtros.

```bash
source .venv/bin/activate && python .claude/skills/monitorando-entregas/scripts/consultando_status_entrega.py [opções]
```

**Parâmetros:**

| Param | Obrig | Descrição |
|-------|-------|-----------|
| `--nf` | Não | Número da NF (busca exata ou parcial) |
| `--cliente` | Não | Nome do cliente (busca parcial) |
| `--cnpj` | Não | CNPJ do cliente |
| `--transportadora` | Não | Transportadora |
| `--pendentes` | Não | Apenas entregas pendentes (status_finalizacao IS NULL) |
| `--entregues` | Não | Apenas entregas entregues |
| `--no-cd` | Não | Apenas NFs no CD (nf_cd=True) |
| `--reagendadas` | Não | Apenas reagendadas (reagendar=True) |
| `--problemas` | Não | Com problema (nf_cd=True OR reagendar=True) |
| `--de` | Não | Data inicial (YYYY-MM-DD) |
| `--ate` | Não | Data final (YYYY-MM-DD) |
| `--limite` | Não | Máximo de registros (default: 50) |
| `--formato` | Não | json ou tabela (default: json) |

**Retorno esperado:**
```json
{
  "sucesso": true,
  "total": 15,
  "entregas": [
    {
      "id": 1234,
      "numero_nf": "144533",
      "cliente": "ATACADAO SA",
      "status_finalizacao": null,
      "entregue": false,
      "nf_cd": false,
      "reagendar": false,
      "data_faturamento": "2025-01-15",
      "data_embarque": "2025-01-16",
      "data_entrega_prevista": "2025-01-20",
      "transportadora": "BRASPRESS",
      "municipio": "SAO PAULO",
      "uf": "SP"
    }
  ]
}
```

### 2. consultando_canhotos.py

Consulta canhotos de entregas.

```bash
source .venv/bin/activate && python .claude/skills/monitorando-entregas/scripts/consultando_canhotos.py [opções]
```

**Parâmetros:**

| Param | Obrig | Descrição |
|-------|-------|-----------|
| `--nf` | Não | Número da NF |
| `--pendentes` | Não | Apenas entregas sem canhoto |
| `--com-canhoto` | Não | Apenas entregas com canhoto |
| `--de` | Não | Data inicial |
| `--ate` | Não | Data final |
| `--limite` | Não | Máximo de registros |

### 3. consultando_devolucoes.py

Consulta devoluções e ocorrências.

```bash
source .venv/bin/activate && python .claude/skills/monitorando-entregas/scripts/consultando_devolucoes.py [opções]
```

**Parâmetros:**

| Param | Obrig | Descrição |
|-------|-------|-----------|
| `--nf` | Não | Número da NF original |
| `--nfd` | Não | Número da NF de devolução |
| `--abertas` | Não | Apenas ocorrências abertas |
| `--cliente` | Não | Nome do cliente |
| `--de` | Não | Data inicial |
| `--ate` | Não | Data final |
| `--limite` | Não | Máximo de registros |

### 4. consultando_agendamentos.py

Consulta agendamentos de entrega.

```bash
source .venv/bin/activate && python .claude/skills/monitorando-entregas/scripts/consultando_agendamentos.py [opções]
```

**Parâmetros:**

| Param | Obrig | Descrição |
|-------|-------|-----------|
| `--nf` | Não | Número da NF |
| `--data` | Não | Data do agendamento (YYYY-MM-DD) |
| `--pendentes` | Não | Apenas agendamentos aguardando confirmação |
| `--confirmados` | Não | Apenas agendamentos confirmados |
| `--limite` | Não | Máximo de registros |

### 5. consultando_devolucoes_detalhadas.py

Consulta devoluções detalhadas com entity resolution e análises agregadas.

```bash
source .venv/bin/activate && python .claude/skills/monitorando-entregas/scripts/consultando_devolucoes_detalhadas.py [opções]
```

**Parâmetros (modos mutuamente exclusivos):**

| Param | Obrig | Descrição |
|-------|-------|-----------|
| `--cliente` | Sim* | Histórico de devoluções por cliente (LIKE no nome_emitente) |
| `--produto` | Sim* | Produtos devolvidos (LIKE na descricao_produto_cliente ou descricao_produto_interno) |
| `--ranking` | Sim* | Top N produtos mais devolvidos (GROUP BY codigo_produto_interno) |
| `--custo` | Sim* | Custo total de devoluções (via despesas_extras.tipo_despesa='DEVOLUCAO') |
| `--de` | Não | Data início (YYYY-MM-DD) |
| `--ate` | Não | Data fim (YYYY-MM-DD) |
| `--limite` | Não | Máximo de registros (default: 50) |
| `--incluir-custo` | Não | Incluir custo (apenas com --cliente) |
| `--ordenar-por` | Não | 'ocorrencias' ou 'quantidade' (apenas com --ranking, default: ocorrencias) |

*Um dos 4 modos deve ser especificado.

**Retorno esperado (modo --cliente):**
```json
{
  "sucesso": true,
  "modo": "cliente",
  "resumo": {
    "mensagem": "Historico de devolucoes de 12 NFDs do cliente 'Sendas'",
    "total_nfds": 12,
    "exibindo": 10,
    "valor_total_devolucoes": 45678.90,
    "custo_total": 3456.78,
    "cliente": "Sendas",
    "periodo": {"de": "2025-01-01", "ate": "2025-12-31"}
  },
  "nfds": [
    {
      "id": 123,
      "numero_nfd": "12345",
      "nome_emitente": "Sendas Distribuidora SA",
      "cnpj_emitente": "12.345.678/0001-99",
      "data_registro": "2025-01-15",
      "valor_total": 4567.89,
      "status": "REGISTRADA",
      "motivo": "AVARIA",
      "total_linhas": 3
    }
  ]
}
```

**Retorno esperado (modo --ranking):**
```json
{
  "sucesso": true,
  "modo": "ranking",
  "resumo": {
    "mensagem": "Top 10 produtos mais devolvidos (ordenado por ocorrencias)",
    "criterio": "ocorrencias",
    "total_produtos": 10
  },
  "ranking": [
    {
      "produto_referencia": "PALMITO-400G",
      "descricao_produto_interno": "Palmito Inteiro 400g",
      "total_ocorrencias": 45,
      "qtd_total": 234.0,
      "total_nfds": 38,
      "total_clientes": 12
    }
  ]
}
```

---

## Exemplos de Uso

### Cenário 1: Status de NF específica

```
Pergunta: "NF 144533 foi entregue?"
Raciocínio: Pergunta sobre STATUS de NF → consultando_status_entrega.py
Comando: --nf 144533
Resultado: "A NF 144533 está pendente (em andamento). Data de embarque: 16/01/2025."
```

### Cenário 2: Entregas pendentes do Atacadão

```
Pergunta: "tem entrega pendente do Atacadão?"
Raciocínio: STATUS + CLIENTE → consultando_status_entrega.py
Comando: --cliente atacadao --pendentes
Resultado: "Encontrei 5 entregas pendentes do Atacadão: [lista com NFs]"
```

### Cenário 3: Canhotos pendentes

```
Pergunta: "quais entregas não têm canhoto?"
Raciocínio: CANHOTO + pendentes → consultando_canhotos.py
Comando: --pendentes --limite 20
Resultado: "20 entregas sem canhoto registrado: [lista]"
```

### Cenário 4: Devoluções abertas

```
Pergunta: "tem devolução aberta?"
Raciocínio: DEVOLUÇÃO + abertas → consultando_devolucoes.py
Comando: --abertas
Resultado: "3 ocorrências de devolução abertas: [detalhes]"
```

### Cenário 5: Data de embarque

```
Pergunta: "que dia saiu a NF 144533?"
Raciocínio: Pergunta sobre DATA DE EMBARQUE → consultando_status_entrega.py
Comando: --nf 144533
Resultado: "A NF 144533 saiu (embarcou) em 16/01/2025."
```

### Cenário 6: Data de faturamento

```
Pergunta: "quando faturou a NF do Atacadão loja 183?"
Raciocínio: DATA DE FATURAMENTO + CLIENTE → resolver grupo primeiro, depois consultando_status_entrega.py
Comando: --cliente "Atacadao 183"
Resultado: "Encontrei 3 NFs do Atacadão 183. Faturamento: NF 144533 em 15/01/2025, NF 144534 em 16/01/2025..."
```

### Cenário 7: Data de entrega realizada

```
Pergunta: "quando chegou a NF 144533?"
Raciocínio: DATA DE ENTREGA REALIZADA → consultando_status_entrega.py
Comando: --nf 144533
Resultado: "A NF 144533 foi entregue em 20/01/2025 às 14:32."
```

---

## Referência Cruzada

| Skill | Quando usar em vez desta |
|-------|--------------------------|
| **gerindo-expedicao** | Pedidos antes de faturar, estoque, separação |
| **rastreando-odoo** | Rastrear NF/PO/pagamento no Odoo |
| **consultando-sql** | Consultas analíticas complexas (agregações, rankings) |
| **analista-carteira** | Análise completa da carteira com decisões P1-P7 |

---

## References (sob demanda)

| Gatilho na Pergunta | Reference a Ler | Motivo |
|---------------------|-----------------|--------|
| "status de devolução" | `references/devolucoes.md` | Fluxo completo de devolução |
| "categorias de ocorrência" | `references/devolucoes.md` | Valores válidos de categoria/subcategoria |
| "como funciona agendamento" | `references/agendamentos.md` | Fluxo de agendamento e confirmação |
| "tabelas relacionadas" | `references/tables.md` | Relacionamentos entre tabelas |

---

## Tabelas do Domínio

| Tabela | Descrição | FK principal |
|--------|-----------|--------------|
| `entregas_monitoradas` | Status principal de cada NF | - |
| `agendamentos_entrega` | Histórico de agendamentos | `entrega_id → entregas_monitoradas.id` |
| `nf_devolucao` | NFs de devolução recebidas | `entrega_monitorada_id → entregas_monitoradas.id` |
| `nf_devolucao_linha` | Linhas/produtos da NFD | `nf_devolucao_id → nf_devolucao.id` |
| `ocorrencia_devolucao` | Ocorrências/tratativa | `nf_devolucao_id → nf_devolucao.id` |
