---
name: gerindo-expedicao
description: |
  Consulta pedidos em carteira, estoque, disponibilidade e cria separacoes.

  USAR QUANDO (ANTES de faturar):
  - Pedidos: "tem pedido do Atacadao?", "pedido VCD123 esta em separacao?"
  - Estoque: "quanto tem de palmito?", "chegou cogumelo?"
  - Disponibilidade: "quando VCD123 fica disponivel?", "o que vai dar falta?"
  - Lead time: "se embarcar amanha, quando chega?"
  - Criar separacao: "crie separacao do VCD123 pra amanha"

  NAO USAR QUANDO (APOS faturar):
  - Status de entrega → usar **monitorando-entregas**
  - "que dia embarcou?", "foi entregue?" → usar **monitorando-entregas**
  - Rastrear NF no Odoo → usar **rastreando-odoo**
allowed-tools: Read, Bash, Glob, Grep
---

# Gerindo Expedicao

Skill para consultas e operacoes logisticas da Nacom Goya.

---

## Quando Usar Esta Skill

USE para:
- Consultas de pedidos: "tem pedido do Atacadao?", "pedido VCD123 esta em separacao?"
- Consultas de estoque: "quanto tem de palmito?", "chegou cogumelo?"
- Analise de disponibilidade: "quando VCD123 fica disponivel?", "o que vai dar falta?"
- Calculo de prazo: "se embarcar amanha, quando chega?"
- Criacao de separacao: "crie separacao do VCD123 pra amanha"

NAO USE para:
- Analise COMPLETA da carteira com decisoes (use o Agent `analista-carteira`)
- Comunicacao com PCP ou Comercial (use o Agent)
- Decisoes de priorizacao P1-P7 (use o Agent)

---

## REGRAS CRITICAS (NUNCA VIOLAR)

### 1. GUARDRAIL ANTI-ALUCINACAO
**PROIBIDO** criar, calcular ou inferir dados que NAO foram retornados pelo script.
Se precisar de dado que nao veio no script: EXECUTE o script com flag adequado ou PERGUNTE ao usuario.

### 2. REGRA DE FALLBACK (NUNCA TRAVAR)
Se um script falhar: SEMPRE responda ao usuario com erro e alternativa.
**NUNCA:** Ficar em silencio, travar, ou tentar criar scripts customizados.

### 3. SIMULAR ANTES DE EXECUTAR (ACOES)
Para QUALQUER acao que modifica dados (criar separacao):
1. Executar SEM --executar (simular)
2. Mostrar resultado ao usuario
3. AGUARDAR confirmacao explicita
4. So entao executar COM --executar

---

## DECISION TREE - Qual Script Usar?

### Mapeamento Rapido

| Se a pergunta menciona... | Use este script | Com estes parametros |
|---------------------------|-----------------|----------------------|
| **PRODUTO + CLIENTE/GRUPO** ("quanto de X pro Y?") | `consultando_situacao_pedidos.py` | `--grupo Y --produto X` |
| **Pedidos de um grupo** ("tem pedido do atacadao?") | `consultando_situacao_pedidos.py` | `--grupo atacadao` |
| **Pedidos de um cliente** ("tem pedido do Carrefour?") | `consultando_situacao_pedidos.py` | `--cliente Carrefour` |
| **Pedidos atrasados** | `consultando_situacao_pedidos.py` | `--atrasados` |
| **Estoque de produto** ("quanto tem de X?") | `consultando_produtos_estoque.py` | `--produto X --completo` |
| **Entradas recentes** ("chegou X?") | `consultando_produtos_estoque.py` | `--produto X --entradas` |
| **Ruptura/falta** ("vai faltar X?") | `consultando_produtos_estoque.py` | `--ruptura --dias 7` |
| **Scan ruptura proativo** ("o que vai faltar?") | `consultando_produtos_estoque.py` | `--scan-ruptura-global --dias 7` |
| **Co-passageiros embarque** | `consultando_situacao_pedidos.py` | `--co-passageiros-embarque 1234` |
| **Quando pedido fica disponivel** | `analisando_disponibilidade_estoque.py` | `--pedido VCD123` |
| **Disponibilidade de grupo** | `analisando_disponibilidade_estoque.py` | `--grupo atacadao --completude` |
| **Prazo de entrega** ("quando chega?") | `calculando_leadtime_entrega.py` | `--pedido X --data-embarque Y` |
| **Criar separacao** | `criando_separacao_pedidos.py` | `--pedido X --expedicao Y` (SEM --executar!) |
| **Programacao de producao** | `consultando_programacao_producao.py` | `--listar --dias 7` |
| **Analise completa da carteira** | `analisando_carteira_completa.py` | `--resumo` ou sem parametros |
| **Priorizar por P1-P7** | `analisando_carteira_completa.py` | `--prioridade N` |

### Regras de Decisao (em ordem de prioridade)

1. **PRODUTO + CLIENTE/GRUPO juntos:** → `consultando_situacao_pedidos.py --grupo X --produto Y`
2. **PEDIDOS de cliente/grupo (sem produto):** → `consultando_situacao_pedidos.py --grupo X`
3. **ESTOQUE de produto (sem cliente):** → `consultando_produtos_estoque.py --produto X --completo`
4. **DISPONIBILIDADE de pedido:** → `analisando_disponibilidade_estoque.py --pedido X`
5. **PRAZO de entrega:** → `calculando_leadtime_entrega.py`
6. **ACAO de criar separacao:** → `criando_separacao_pedidos.py` (SEMPRE simular antes!)

### Como Decidir (Raciocinio Obrigatorio)

**PASSO 1**: O que o usuario quer? (PEDIDOS / ESTOQUE / DISPONIBILIDADE / PRAZO / ACAO)
**PASSO 2**: Tem cliente/grupo? (SIM + produto → situacao_pedidos | SIM sem produto → situacao_pedidos | NAO → produtos_estoque)
**PASSO 3**: A escolha faz sentido? (ESTOQUE mas "pro atacadao" → ERRADO, use PEDIDOS)
**PASSO 4**: Em duvida → pergunte ao usuario!

---

## Termos Ambiguos - PERGUNTE antes de agir!

#### "programacao de entrega" (CRITICO - 4 interpretacoes)
A) Data que cliente solicitou (`data_entrega_pedido`) | B) Data de expedicao (`expedicao`) | C) Data de chegada (`agendamento`) | D) Protocolo de agendamento (`protocolo`)

#### "quantidade pendente"
Acao padrao: Mostrar AMBOS: "Na carteira: X un | Em separacao: Y un | Total: Z un"

#### Multiplas lojas do mesmo grupo
Se resultado tiver mais de 1 loja: PERGUNTAR qual loja.

---

## Scripts — Referencia Detalhada

**Para parametros completos, retornos e modos de operacao**: LER `SCRIPTS.md`

Resumo dos 8 scripts:

| # | Script | Proposito |
|---|--------|-----------|
| 1 | `analisando_disponibilidade_estoque.py` | Disponibilidade para pedidos/grupos |
| 2 | `consultando_situacao_pedidos.py` | Pedidos por filtros diversos |
| 3 | `consultando_produtos_estoque.py` | Estoque, movimentacoes, projecoes |
| 4 | `calculando_leadtime_entrega.py` | Data entrega ou data embarque reversa |
| 5 | `criando_separacao_pedidos.py` | Criar separacoes (simular antes!) |
| 6 | `consultando_programacao_producao.py` | Programacao de producao |
| 7 | `resolver_entidades.py` | Utilitario interno de resolucao |
| 8 | `analisando_carteira_completa.py` | Analise P1-P7 completa com decisoes |

---

## Fluxo de Criacao de Separacao

| Campo | Obrigatorio | Como Obter |
|-------|-------------|------------|
| Pedido | SIM | Usuario informa |
| Data expedicao | SIM | Usuario informa |
| Tipo (completa/parcial) | SIM | Perguntar se nao especificado |
| Agendamento | CONDICIONAL | Verificar ContatoAgendamento pelo CNPJ |
| Protocolo | CONDICIONAL | Se exige agendamento |

Sequencia: SIMULAR → Verificar alertas → Mostrar → Confirmar → EXECUTAR

---

## Leitura de References (Sob Demanda)

| Gatilho na Pergunta | Reference a Ler |
|---------------------|-----------------|
| Produto mencionado | `references/products.md` |
| Cliente/Grupo | `references/business.md` |
| Termo desconhecido | `references/glossary.md` |
| Variacao de escrita | `references/synonyms.md` |
| Comunicar PCP/Comercial | `references/communication.md` |
| Duvida de script | `references/examples.md` |
| Priorizacao, clientes top, SLAs | `references/context.md` |

**Grupos Empresariais:** `--grupo atacadao`, `--grupo assai`, `--grupo tenda`
