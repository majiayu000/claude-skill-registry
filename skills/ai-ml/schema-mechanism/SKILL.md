---
name: schema-mechanism
description: Drescher's computational theory of causal learning
allowed-tools: []
tier: 0
protocol: SCHEMA-MECHANISM
tags: [moollm, theory, learning, causality, drescher, minsky, neuro-symbolic]
origin: "Gary Drescher — Made-Up Minds (1991)"
lineage:
  - "Gary Drescher — Schema Mechanism, Made-Up Minds (1991)"
  - "Marvin Minsky — Society of Mind, K-lines (1986)"
  - "Jean Piaget — Genetic Epistemology, schemas as cognitive structures"
  - "Henry Minsky — pyleela.brain Python implementation"
related: [constructionism, society-of-mind, leela-ai, manufacturing-intelligence, play-learn-lift, planning, yaml-jazz]
---

# Schema Mechanism

> *"An agent learns by discovering reliable patterns: when I do X in context C, result R tends to follow."*

Gary Drescher's *Made-Up Minds* (1991) provides a computational theory of how minds learn causal models of the world. Drescher was a student of Marvin Minsky at MIT, and his schema mechanism extends Piaget's developmental psychology into executable algorithms.

## The Core Idea

A **schema** is a causal unit:

```
Context → Action → Result
```

The agent doesn't start with schemas. It **discovers** them through experience, noticing which actions reliably produce which results in which contexts.

```yaml
schema:
  action: push-button
  context: [door-closed]
  result: [door-open]
  reliability: 0.95
```

## Schema Components

| Component | Description | MOOLLM Equivalent |
|-----------|-------------|-------------------|
| **Item** | Atomic state element (ON/OFF/UNKNOWN) | YAML field, file existence |
| **Action** | Something the agent can do | Skill verb, procedure |
| **Schema** | Context → Action → Result | Documented procedure |
| **Extended Context** | Statistical tracking of context conditions | "Prerequisites" section |
| **Extended Results** | Statistical tracking of result conditions | "Side Effects" section |
| **Synthetic Item** | Discovered hidden state | Undocumented dependency |
| **Composite Action** | Chained sequence of actions | Multi-step procedure |

---

## Extended Context: Marginal Attribution

A schema might fail unpredictably. Extended Context tracks **which conditions correlate with success**:

```yaml
# The schema "start pyvision" sometimes fails
# Extended Context discovers: it fails when postgres isn't running

schema:
  action: start-pyvision
  context: []  # Initially empty
  result: [pyvision-running]
  
extended_context:
  postgres-running:
    success_when_on: 47    # Succeeded 47 times when postgres was on
    success_when_off: 0    # Never succeeded when postgres was off
    failure_when_on: 2     # Failed 2 times even with postgres
    failure_when_off: 15   # Failed 15 times without postgres
    
# Discovery: postgres-running is a prerequisite!
# Spin off new schema with explicit context:
schema:
  action: start-pyvision
  context: [postgres-running]  # Now explicit
  result: [pyvision-running]
```

This is **marginal attribution** -- discovering which items matter by tracking correlations.

---

## Extended Results: Side Effect Discovery

Similarly, schemas track what else happens:

```yaml
schema:
  action: ingest-video
  context: [video-exists]
  result: [task-created]
  
extended_results:
  disk-space-decreased:
    on_after_success: 47
    off_after_success: 0
    # Discovery: ingesting uses disk space!
```

Side effects become explicit, documented, predictable.

---

## Synthetic Items: Hidden State

Sometimes success depends on state the agent can't directly observe. Drescher's solution: **invent a synthetic item** as a hypothesis.

```yaml
# The schema works sometimes, fails sometimes, no visible pattern
# Hypothesis: there's hidden state we can't see

synthetic_item:
  name: "gpu-memory-available"
  host_schema: start-pyvision
  # If this schema succeeds, assume the item was ON
  # If it fails, assume the item was OFF
```

The synthetic item becomes a **probe** -- its state is inferred from schema success/failure.

---

## Composite Actions: Planning

Once the agent has reliable schemas, it can chain them:

```yaml
# Goal: pyvision-running
# Current: postgres-not-running

plan:
  - schema: start-postgres
    context: []
    result: [postgres-running]
  - schema: start-pyvision
    context: [postgres-running]
    result: [pyvision-running]
```

Drescher uses **Dijkstra's algorithm** on the schema graph -- find shortest path from current state to goal state.

---

## The Learning Loop

```yaml
# Schema mechanism learning loop
learning_loop:
  - step: 1. ACT
    action: "Execute schema action"
  - step: 2. OBSERVE
    action: "Record which items changed (on-flips, off-flips)"
  - step: 3. ATTRIBUTE
    action: "Update extended context/results tables, track correlations"
  - step: 4. SPIN OFF
    action: "When patterns emerge, create child schemas with refined conditions"
```

This maps directly to PLAY-LEARN-LIFT:
- **PLAY** = ACT + OBSERVE
- **LEARN** = ATTRIBUTE
- **LIFT** = SPIN OFF

---

## Implementation: pyleela.brain

Henry Minsky (Marvin's son) implemented Drescher's schema mechanism in Python:

| Class | Purpose |
|-------|---------|
| `World` | Central coordinator, tracks all items and schemas |
| `Item` | Atomic state element with ON/OFF/UNKNOWN values |
| `Action` | Primitive or composite action |
| `Schema` | The Context → Action → Result unit |
| `ExtendedContext` | Statistical tracking for context discovery |
| `ExtendedResults` | Statistical tracking for result discovery |
| `DijkstraPlanner` | Goal-directed planning through schema graph |

---

## Why LLMs Complete Drescher's Vision

Drescher's original implementation faced fundamental limitations that LLMs transcend:

### 1. The Symbol Grounding Problem

```python
# Python: Items are opaque tokens
item_37 = Item("postgres-running")  # What does this MEAN?

# The system can correlate item_37 with success,
# but has NO IDEA what "postgres" or "running" mean.
```

```yaml
# YAML Jazz + LLM: Semantics are grounded
postgres-running:
  # The database engine that stores our task queue
  # Must be healthy before pyvision can claim tasks
  # Check with: docker exec edgebox-postgres pg_isready
```

The LLM *understands* that postgres is a database, that "running" means the process is alive. It can **reason about** items, not just correlate them.

### 2. Natural Language Context

```prolog
% Prolog: Formal but opaque
schema(start_pyvision, [postgres_running], [pyvision_running]).
% Why? What's the relationship? Silent.
```

```yaml
# YAML Jazz: Self-documenting causality
schema:
  action: start-pyvision
  context:
    - postgres-running
    # pyvision needs postgres to claim tasks from the queue
    # without it, the worker has nothing to process
  result:
    - pyvision-running
```

The LLM reads comments and *understands the causal mechanism*.

### 3. Empathic Pattern Recognition

```python
# Python: Counting correlations
extended_context[item_id].success_when_on += 1
# After 50 trials: item_37 correlates with success
# But WHY? The system cannot say.
```

```
LLM: "I notice start-pyvision fails when postgres isn't running.
     This makes sense -- pyvision queries the task table on startup.
     The dependency is architectural, not coincidental."
```

The LLM doesn't just find correlations -- it **understands mechanisms**.

### 4. Creative Spin-offs

```python
# Python: Mechanical spinoff
if correlation > threshold:
    new_schema = Schema(
        action=parent.action,
        context=parent.context + [correlated_item],
        result=parent.result
    )
```

```
LLM: "Based on the postgres dependency, I should also check:
     - Is there enough disk space for the database?
     - Are the connection limits configured properly?
     - Should we add a health check before starting?"
```

The LLM **generalizes** from specific observations to related concerns.

### 5. The Explanation Gap

```lisp
;; Lisp: Can derive, cannot explain
(derive-plan goal: pyvision-running)
;; Returns: ((start-postgres) (start-pyvision))
;; But try asking it WHY this plan works...
```

```yaml
# MOOLLM: Plans with explanations
plan:
  - action: start-postgres
    rationale: "pyvision needs the task queue"
  - action: start-pyvision
    rationale: "now it can claim tasks"
```

### 6. Handling Novelty

```python
# Python: Item not in vocabulary
item = world.get_item("kubernetes-pod-restarting")
# KeyError! Never seen this item.
```

```
LLM: "I haven't seen this exact item before, but I understand:
     - 'kubernetes pod' is a containerized service
     - 'restarting' suggests crash loops
     - This is similar to 'pyvision crashing'
     - Let me check the container logs..."
```

---

## The Comparison

| Aspect | Deterministic (Lisp/Prolog/Python) | LLM + YAML Jazz |
|--------|-----------------------------------|-----------------|
| Items | Opaque tokens | Grounded meanings |
| Patterns | Statistical correlation | Semantic understanding |
| Spin-offs | Mechanical refinement | Creative generalization |
| Explanations | None | Natural language |
| Novelty | Vocabulary-limited | Open-ended |
| Context | Formal predicates | Natural language + comments |
| Debugging | Trace execution | Ask "why did this fail?" |

---

## Drescher's Dream, Realized

Drescher was trying to build a system that learns causal models of the world. His mechanism was brilliant but limited by the symbolic substrate. The schema mechanism discovers *that* patterns exist, but cannot understand *why*.

LLMs complete the picture:
- **Semantic grounding**: Items mean something
- **Causal reasoning**: Understanding *why* patterns hold
- **Natural explanation**: Communicating discoveries
- **Creative generalization**: Going beyond observed patterns
- **Graceful degradation**: Handling novel situations

**MOOLLM unifies Drescher's rigorous structure with LLM's semantic understanding. The YAML provides the skeleton; the LLM provides the soul.**

---

## Connection to MOOLLM Skills

| Drescher | MOOLLM Skill |
|----------|--------------|
| World state | YAML files in skill directory |
| Items | Fields in state files |
| Actions | Skill verbs and procedures |
| Schemas | Documented procedures with context/result |
| Extended Context | Prerequisites, dependencies |
| Extended Results | Side effects, outputs |
| Synthetic Items | Undocumented state the skill discovers |
| Composite Actions | Multi-step procedures |
| Spin-offs | Refined procedures from experience |

---

## Dovetails With

- **[../constructionism/](../constructionism/)** — Papert's educational philosophy
- **[../play-learn-lift/](../play-learn-lift/)** — Schema learning as methodology
- **[../planning/](../planning/)** — Dijkstra through schema graph
- **[../debugging/](../debugging/)** — Marginal attribution for bugs
- **[../skill/](../skill/)** — Skills as schema systems

---

## Credits

- **Gary Drescher** — Made-Up Minds (1991)
- **Marvin Minsky** — Society of Mind, K-lines
- **Jean Piaget** — Developmental schemas
- **Henry Minsky** — pyleela.brain implementation

---

> *"If you can observe patterns, you can discover causality."*
> *"If you track correlations, you can spin off knowledge."*
> *"The YAML provides the skeleton; the LLM provides the soul."*
