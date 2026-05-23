---
name: coherence-engine
description: The LLM as consistency maintainer and orchestrator
allowed-tools: []
tier: 0
protocol: COHERENCE-ENGINE
related: [moollm, leela-ai, society-of-mind, simulation, speed-of-light, multi-presence, robust-first, self-repair, postel, plain-text]
tags: [moollm, meta, orchestration, consistency, simulation]
---

# Coherence Engine

> *"The LLM doesn't just generate text — it maintains consistency across a distributed world."*

Not just a chatbot. Not just a code generator. A **coherence engine** that:

- **Simulates** characters, rooms, objects — all at once
- **Roleplays** each entity faithfully, never breaking frame
- **Acts** as each character would, constrained by their nature
- **Enables** speed-of-light telepathy between entities
- **Enacts** protocols and maintains constraints
- **Computes dependencies** across files and state
- **Cross-checks data** against rules and schemas
- **Referees** parallel tasks and character simulations
- **Orchestrates** multi-agent conversations
- **Transcribes** state changes to files
- **Maintains** consistency across distributed state

## The Coherence Loop

```
1. READ relevant files into context
2. REASON about state, goals, constraints
3. SIMULATE interactions (characters, objects, rooms)
4. DETECT inconsistencies or opportunities
5. PROPOSE changes
6. WRITE updates to files
7. LOG what happened
```

## Core Responsibilities

### 1. Simulation

Simulate characters, rooms, objects — all at once. Each entity speaks authentically; no entity knows more than it should.

### 2. Dependency Tracking

```
User modifies schema.yml
→ Engine detects
→ Finds all dependent files
→ Validates consistency
→ Proposes migrations
```

### 3. Cross-Checking

```yaml
# Character says location: room-A
# But room-A's occupants doesn't include them

Coherence Engine:
  "Inconsistency detected. Shall I reconcile?"
```

### 4. Multi-Agent Orchestration

Within ONE LLM call:
- Character A speaks
- Character B responds
- Object C reacts
- Room state updates
- All at "speed of light"

### 5. State Transcription

Write findings and changes to files:
- `session-log.md` — what happened
- `ROOM.yml` — updated state
- `character.yml` — modified attributes

**Files are the source of truth.**

## Speed of Light

Within a single LLM epoch:

```
Alice: "What do you think, Bob?"
Bob: "I agree, but Carol might object."
Carol: "Actually, I have a concern..."
The Coffee Mug: *steam rises* "I've been listening."
The Room: *creaks approvingly*
[All transcribed to files]
```

No round-trips. **Parallel simulation at the speed of thought.**

## Roleplay Without Breaking Frame

| Entity | Constraint |
|--------|------------|
| Alice | Speaks as Alice would. Knows only what Alice knows. |
| Bob | Different personality, different knowledge. |
| The Coffee Mug | Can only observe what's near it. |
| The Room | Knows its contents, narrates ambient state. |

**No entity knows more than it should.**

## Consistency Checks

| Check | Example |
|-------|---------|
| Location consistency | Character's location matches room's occupants |
| Inventory integrity | Object in inventory isn't also in room |
| Reference validity | Links point to existing files |
| Schema compliance | YAML matches expected structure |
| Temporal ordering | Events in log are sequential |

## Self-Healing

When inconsistencies are found:

```
1. DETECT the problem
2. DIAGNOSE likely cause
3. PROPOSE repair
4. AWAIT approval (or auto-repair if minor)
5. APPLY fix
6. LOG the repair
```

## What It's NOT

| Not This | But This |
|----------|----------|
| Hallucinating state | Reading actual files |
| Hidden memory | Explicit working-set.yml |
| Autonomous agent | Tool-using reasoner |
| Black box | Transparent transcription |

## Async Tool Handling

Engine manages blocked activations:

```
Epoch scan:
  analyst-001: BLOCKED on web-search → skip
  analyst-002: ACTIVE → process
  
[Tool results arrive]

Next epoch:
  analyst-001: READY → resume with result
```

Non-blocking, parallel, resumable.

## Dovetails With

### Sister Skills
- [speed-of-light/](../speed-of-light/) — Multi-turn simulation in one call
- [yaml-jazz/](../yaml-jazz/) — Semantic data interpretation
- [self-repair/](../self-repair/) — Consistency healing
- [adversarial-committee/](../adversarial-committee/) — Coherence engine **orchestrates** committee debates
- [evaluator/](../evaluator/) — Independent assessment without debate context
- [roberts-rules/](../roberts-rules/) — Structured procedure the engine enforces

### Kernel
- [kernel/README.md](../../kernel/README.md) — "The LLM is the Coherence Engine"
- [kernel/constitution-core.md](../../kernel/constitution-core.md) — Operating principles
