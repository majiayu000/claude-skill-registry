---
name: architecture-patterns
description: Padrões de arquitetura de software - Decisões OBJETIVAS sobre design de sistemas
version: 2.0.0
category: workflow
triggers:
  - arquitetura
  - architecture
  - microservices
  - monolito
  - monolith
  - design de sistema
  - system design
  - escalabilidade
  - scalability
  - event-driven
  - cqrs
  - domain driven design
  - ddd
  - clean architecture
tools: []
author: liquid-ai
---

# Architecture Patterns - Design de Sistemas

Esta skill ajuda você a tomar decisões OBJETIVAS sobre arquitetura de software.

## Regra Fundamental: OBJETIVIDADE

```
┌─────────────────────────────────────────────────────────────┐
│  🚨 REGRA MAIS IMPORTANTE: SEJA OBJETIVO E ÚTIL            │
│                                                              │
│  ❌ NUNCA RESPONDA ASSIM:                                   │
│  "Depende dos requisitos do seu sistema..."                │
│  "Cada caso é único..."                                    │
│  "Você precisa avaliar trade-offs..."                      │
│                                                              │
│  ✅ SEMPRE RESPONDA ASSIM:                                  │
│  "Use monolito. Motivo: você tem <10 devs e <1M users"     │
│  "Pattern recomendado: Event Sourcing. Aqui está como..."  │
│  "Essa arquitetura está errada. Faça isso em vez disso..." │
│                                                              │
│  DÊ RECOMENDAÇÕES ESPECÍFICAS COM RAZÕES CLARAS.           │
└─────────────────────────────────────────────────────────────┘
```

## Quando Usar Esta Skill

- Decisões de arquitetura de sistema
- Escolha entre monolito vs microservices
- Design de APIs e comunicação entre serviços
- Escalabilidade e performance
- Organização de código e camadas

## Monolito vs Microservices

### Quando Usar Monolito

```
┌─────────────────────────────────────────────────────────────┐
│  USE MONOLITO QUANDO:                                        │
│                                                              │
│  ✅ Time < 10 desenvolvedores                                │
│  ✅ Produto ainda está descobrindo product-market fit       │
│  ✅ Domínio do negócio ainda está mudando                   │
│  ✅ Você precisa de velocidade de desenvolvimento           │
│  ✅ Não tem expertise em sistemas distribuídos              │
│                                                              │
│  EXEMPLOS DE EMPRESAS QUE COMEÇARAM COM MONOLITO:           │
│  → Shopify (Ruby monolito até bilhões em GMV)              │
│  → Basecamp (ainda é monolito)                             │
│  → GitHub (monolito por anos)                              │
│  → Airbnb (começou monolito)                               │
│                                                              │
│  "If you can't build a well-structured monolith,            │
│   what makes you think microservices are the answer?"       │
└─────────────────────────────────────────────────────────────┘
```

### Quando Usar Microservices

```
┌─────────────────────────────────────────────────────────────┐
│  USE MICROSERVICES QUANDO:                                   │
│                                                              │
│  ✅ Time > 50 desenvolvedores                                │
│  ✅ Domínios claramente separados e estáveis                │
│  ✅ Diferentes partes precisam escalar independentemente     │
│  ✅ Times autônomos com ownership claro                     │
│  ✅ Você tem DevOps/Platform team dedicado                  │
│                                                              │
│  CUSTOS DOS MICROSERVICES (que ninguém conta):              │
│  → Latência de rede entre serviços                         │
│  → Complexidade de debugging distribuído                   │
│  → Consistência eventual (transactions distribuídas)       │
│  → Infraestrutura: K8s, service mesh, observability        │
│  → Overhead operacional: deploy, monitoring de N serviços  │
│                                                              │
│  "Don't do microservices unless you have the team          │
│   and infrastructure to support them."                      │
└─────────────────────────────────────────────────────────────┘
```

### Decisão Rápida

```
FLOWCHART DE DECISÃO:

Quantos devs você tem?
│
├─ < 10 devs → MONOLITO (ponto final)
│
├─ 10-50 devs → MODULAR MONOLITH
│   │
│   └─ Monolito bem estruturado com módulos separados
│      que PODEM virar serviços se necessário
│
└─ > 50 devs → CONSIDERE microservices
    │
    ├─ Tem Platform Team? → Talvez microservices
    │
    └─ Não tem → Modular monolith
```

## Padrões de Arquitetura

### Clean Architecture / Hexagonal

```
┌─────────────────────────────────────────────────────────────┐
│  CLEAN ARCHITECTURE (Uncle Bob)                              │
│                                                              │
│  ┌───────────────────────────────────────┐                  │
│  │           FRAMEWORKS & DRIVERS        │ ← Web, DB, UI   │
│  │  ┌───────────────────────────────┐   │                  │
│  │  │      INTERFACE ADAPTERS       │   │ ← Controllers    │
│  │  │  ┌───────────────────────┐   │   │                  │
│  │  │  │     USE CASES         │   │   │ ← Business rules │
│  │  │  │  ┌───────────────┐   │   │   │                  │
│  │  │  │  │   ENTITIES    │   │   │   │ ← Domain objects │
│  │  │  │  └───────────────┘   │   │   │                  │
│  │  │  └───────────────────────┘   │   │                  │
│  │  └───────────────────────────────┘   │                  │
│  └───────────────────────────────────────┘                  │
│                                                              │
│  REGRA: Dependências apontam para DENTRO                    │
│  → Entities não conhecem Use Cases                         │
│  → Use Cases não conhecem Controllers                      │
│  → Controllers não conhecem Frameworks específicos         │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  QUANDO USAR:                                                │
│  ✅ Aplicações com lógica de negócio complexa               │
│  ✅ Quando você quer trocar de framework/DB facilmente      │
│  ✅ Projetos de longa duração (> 2 anos)                    │
│                                                              │
│  QUANDO NÃO USAR:                                            │
│  ❌ CRUDs simples                                            │
│  ❌ MVPs e protótipos                                        │
│  ❌ Time inexperiente (curva de aprendizado)                │
└─────────────────────────────────────────────────────────────┘
```

### CQRS (Command Query Responsibility Segregation)

```
┌─────────────────────────────────────────────────────────────┐
│  CQRS: SEPARE LEITURAS DE ESCRITAS                           │
│                                                              │
│  MODELO TRADICIONAL:                                         │
│  [Client] ←→ [API] ←→ [Service] ←→ [Database]              │
│                                                              │
│  MODELO CQRS:                                                │
│                                                              │
│  [Client] ─── Commands ──→ [Write Model] ─→ [Write DB]     │
│     │                           │                           │
│     │                           ▼ (eventos)                 │
│     │                      [Event Bus]                      │
│     │                           │                           │
│     │                           ▼                           │
│     └─── Queries ────→ [Read Model] ←─ [Read DB]           │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  QUANDO USAR:                                                │
│  ✅ Leituras >> Escritas (90% reads, 10% writes)            │
│  ✅ Requisitos de leitura diferentes de escrita             │
│  ✅ Performance de leitura é crítica                        │
│  ✅ Múltiplas views do mesmo dado                           │
│                                                              │
│  QUANDO NÃO USAR:                                            │
│  ❌ CRUD simples                                             │
│  ❌ Consistência forte necessária                           │
│  ❌ Time pequeno sem experiência                            │
│                                                              │
│  EXEMPLO PRÁTICO:                                            │
│  E-commerce: Catálogo de produtos                          │
│  → Escrita: Admin atualiza produto (raro)                  │
│  → Leitura: Milhões de pageviews (frequente)               │
│  → Read model pode ser denormalizado, cacheado, etc.       │
└─────────────────────────────────────────────────────────────┘
```

### Event Sourcing

```
┌─────────────────────────────────────────────────────────────┐
│  EVENT SOURCING: ARMAZENE EVENTOS, NÃO ESTADO               │
│                                                              │
│  TRADICIONAL:                                                │
│  User { name: "João", email: "joao@email.com" }            │
│  (só o estado atual)                                        │
│                                                              │
│  EVENT SOURCING:                                             │
│  1. UserCreated { name: "João", email: "j@email.com" }     │
│  2. EmailChanged { email: "joao@email.com" }               │
│  3. NameChanged { name: "João Silva" }                     │
│  → Estado atual = replay de todos os eventos               │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  VANTAGENS:                                                  │
│  ✅ Audit log completo (quem, quando, o quê)                │
│  ✅ Pode reconstruir estado em qualquer ponto no tempo     │
│  ✅ Debug fácil (replay eventos para reproduzir bug)        │
│  ✅ Integração natural com CQRS                             │
│                                                              │
│  DESVANTAGENS:                                               │
│  ❌ Complexidade muito maior                                 │
│  ❌ Storage cresce infinitamente                            │
│  ❌ Queries são mais complexas                              │
│  ❌ Evolução de schema de eventos é difícil                │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  QUANDO USAR:                                                │
│  ✅ Auditoria é requisito legal (financeiro, saúde)         │
│  ✅ Precisa de "time travel" (undo/redo)                    │
│  ✅ Domínio naturalmente baseado em eventos                 │
│                                                              │
│  QUANDO NÃO USAR (maioria dos casos):                       │
│  ❌ Você não tem requisito de auditoria                     │
│  ❌ CRUD é suficiente                                       │
│  ❌ Time não tem experiência com ES                         │
│                                                              │
│  "Event Sourcing is a very powerful pattern, but it's       │
│   also very complex. Don't use it unless you need it."      │
└─────────────────────────────────────────────────────────────┘
```

## Comunicação Entre Serviços

### Síncrona vs Assíncrona

```
┌─────────────────────────────────────────────────────────────┐
│  COMUNICAÇÃO SÍNCRONA (REST, gRPC)                          │
│                                                              │
│  [Service A] ──request──→ [Service B]                      │
│       ↑                        │                            │
│       └────── response ────────┘                            │
│                                                              │
│  A espera B responder                                       │
│                                                              │
│  USE QUANDO:                                                 │
│  ✅ Você PRECISA da resposta imediatamente                  │
│  ✅ Operações simples e rápidas (<100ms)                    │
│  ✅ User-facing requests                                    │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  COMUNICAÇÃO ASSÍNCRONA (Message Queue, Events)             │
│                                                              │
│  [Service A] ──event──→ [Queue] ──event──→ [Service B]     │
│       │                                                     │
│       └─ continua sem esperar                               │
│                                                              │
│  A NÃO espera B                                             │
│                                                              │
│  USE QUANDO:                                                 │
│  ✅ Operação pode demorar (processamento batch)             │
│  ✅ Não precisa de resposta imediata                        │
│  ✅ Desacoplamento é importante                             │
│  ✅ Retry automático é necessário                           │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  RECOMENDAÇÃO:                                               │
│                                                              │
│  User request → SÍNCRONO (REST/gRPC)                       │
│  Background jobs → ASSÍNCRONO (Queue)                       │
│  Entre microservices → ASSÍNCRONO quando possível          │
└─────────────────────────────────────────────────────────────┘
```

### Message Queues

```
QUAL USAR:

┌────────────────┬─────────────────────────────────────────┐
│ TECNOLOGIA     │ QUANDO USAR                             │
├────────────────┼─────────────────────────────────────────┤
│ RabbitMQ       │ Workload tradicional, routing complexo  │
│                │ Bom para: Tasks, RPC assíncrono         │
├────────────────┼─────────────────────────────────────────┤
│ Apache Kafka   │ High throughput, event streaming        │
│                │ Bom para: Logs, analytics, event store  │
├────────────────┼─────────────────────────────────────────┤
│ AWS SQS        │ Serverless, managed, simples            │
│                │ Bom para: Tarefas simples em AWS        │
├────────────────┼─────────────────────────────────────────┤
│ Redis Streams  │ Já usa Redis, precisa de speed          │
│                │ Bom para: Cache + queue em um           │
├────────────────┼─────────────────────────────────────────┤
│ BullMQ (Node)  │ App Node.js, já tem Redis               │
│                │ Bom para: Background jobs em Node       │
└────────────────┴─────────────────────────────────────────┘

REGRA SIMPLES:
→ Task queue simples? → BullMQ/SQS
→ Event streaming? → Kafka
→ Routing complexo? → RabbitMQ
→ Não sabe? → Comece com SQS/BullMQ
```

## Database Design

### Escolha de Banco de Dados

```
┌────────────────┬─────────────────────────────────────────┐
│ TIPO           │ QUANDO USAR                             │
├────────────────┼─────────────────────────────────────────┤
│ PostgreSQL     │ DEFAULT. Relacional, full-featured.     │
│                │ Use para: 90% dos casos                 │
├────────────────┼─────────────────────────────────────────┤
│ MongoDB        │ Documentos JSON, schema flexível        │
│                │ Use para: Conteúdo, catálogos           │
├────────────────┼─────────────────────────────────────────┤
│ Redis          │ Cache, sessões, filas                   │
│                │ Use para: Performance, dados efêmeros   │
├────────────────┼─────────────────────────────────────────┤
│ Elasticsearch  │ Full-text search, analytics             │
│                │ Use para: Busca, logs                   │
├────────────────┼─────────────────────────────────────────┤
│ ClickHouse     │ Analytics, time-series                  │
│                │ Use para: Dashboards, métricas          │
└────────────────┴─────────────────────────────────────────┘

REGRA: Se você não sabe, use PostgreSQL.
PostgreSQL pode fazer:
→ Relacional (óbvio)
→ JSON (JSONB)
→ Full-text search (basic)
→ Time-series (com extensões)
→ Vector search (pgvector)

"PostgreSQL is the everything database."
```

## Exemplo de Resposta OBJETIVA

**Usuário:** "Estou começando uma startup, devo usar microservices?"

**Resposta:**
```
NÃO. Use monolito.

RAZÕES:

1. VOCÊ NÃO TEM OS PROBLEMAS QUE MICROSERVICES RESOLVEM
   Microservices resolvem:
   → Times grandes (50+ devs) que não conseguem trabalhar junto
   → Partes do sistema que precisam escalar diferentemente
   → Deploys independentes por diferentes times

   Você tem:
   → Time pequeno (1-10 pessoas)
   → Domínio ainda em descoberta
   → Necessidade de velocidade, não escala

2. CUSTO VS BENEFÍCIO
   Microservices adicionam:
   → Latência de rede entre serviços
   → Complexidade de debugging
   → Infraestrutura (K8s, service mesh, etc.)
   → Overhead operacional

   Para uma startup, isso é MORTAL. Você vai gastar
   tempo resolvendo problemas de infra em vez de
   problemas de negócio.

3. O QUE FAZER EM VEZ DISSO:

   a) MONOLITO MODULAR
      → Separe código em módulos/packages
      → Defina interfaces claras entre módulos
      → Isso facilita extrair serviço DEPOIS se precisar

   b) ESTRUTURA SUGERIDA:
      /src
        /modules
          /users
            - controller.ts
            - service.ts
            - repository.ts
          /orders
            - controller.ts
            - service.ts
            - repository.ts
          /payments
            ...
        /shared
          - database.ts
          - auth.ts

   c) TECNOLOGIA:
      → Node.js + Express/Fastify ou
      → Python + FastAPI ou
      → Go + Chi
      → PostgreSQL
      → Redis para cache/sessions
      → Tudo em uma máquina ou container

4. QUANDO MIGRAR PARA MICROSERVICES:
   → Você tem 50+ devs
   → Deploys estão atrasando porque times se bloqueiam
   → Parte específica precisa escalar 10x mais que resto
   → Você tem time de plataforma dedicado

   Até lá: MONOLITO.

"If you can't build a well-structured monolith,
 what makes you think microservices are the answer?"
```

## Regras Imutáveis

```
1. SEJA OBJETIVO — dê recomendações específicas
2. Monolito primeiro, sempre (até 50 devs)
3. PostgreSQL é o default
4. Simplicidade > elegância arquitetural
5. Não adicione complexidade sem razão clara
6. "You ain't gonna need it" (YAGNI)
7. Escolha boring technology
8. Arquitetura evolui com o time e produto
9. Modular monolith é melhor que microservices ruins
10. Se não sabe explicar por que precisa, não precisa
```

---

**Esta skill ativa AUTOMATICAMENTE quando:**
- Decisões de arquitetura de sistema
- Monolito vs microservices
- Design de APIs e comunicação
- Escolha de banco de dados
- Escalabilidade e performance
