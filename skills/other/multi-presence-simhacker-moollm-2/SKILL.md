---
name: multi-presence
description: Same card active in multiple rooms simultaneously
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
  - list_dir
origin: "Actor model, parallel processing, distributed systems"
commands:
  - PLAY card IN room
  - INSTANCES card
  - BROADCAST message TO card
  - MERGE instance-1 instance-2
statuses:
  - active
  - blocked
  - ready
  - paused
  - completed
related: [card, society-of-mind, character, room, prototype, coherence-engine, speed-of-light, data-flow]
tags: [moollm, actor, parallel, instances, distributed]
---

# Multi-Presence

> *"The same card, active in many rooms at once."*

---

## What Is It?

**Multi-Presence** allows a single card (character, tool, skill) to be **instantiated in multiple rooms simultaneously**, each instance with its own state.

Like running the same program in multiple terminals. Same code, different contexts, parallel execution.

---

## Why It Matters

### Parallel Exploration

Send your researcher character to explore three branches at once:

```
research-room-A/
  → Researcher instance (exploring hypothesis A)
  
research-room-B/
  → Researcher instance (exploring hypothesis B)
  
research-room-C/
  → Researcher instance (exploring hypothesis C)
```

All three run in parallel. Compare results. Merge insights.

### Cross-Pollination

The Debugger character in Room A notices something. The Debugger in Room B has context that helps. They can communicate:

```
[Room A: Debugger]
"I found a pattern but don't understand it."

[Room B: Debugger] 
"That matches what I'm seeing here. Together it suggests..."
```

Same card, different vantages, shared insight.

### Distributed Work

A large task splits across rooms:

```
Task: "Analyze all 50 documents"

document-batch-1/
  → Analyst instance (docs 1-10)
  
document-batch-2/
  → Analyst instance (docs 11-20)
  
[... etc ...]

aggregator/
  → Results flow in from all instances
```

---

## How It Works

### Playing a Card Multiple Times

```
> PLAY analyst-card IN room-A
Analyst instance created in room-A

> PLAY analyst-card IN room-B  
Analyst instance created in room-B

> PLAY analyst-card IN room-C
Analyst instance created in room-C
```

Now `analyst-card` has three **activations**, each with independent state.

### Instance State

Each activation has its own:
- **Local variables** — what it's working on
- **Progress** — how far along
- **Findings** — what it's discovered
- **Tags** — how to reference it

```yaml
# room-A/activations/analyst-001.yml
card: analyst-card
instance_id: analyst-001
tags: [moollm, @hypothesis-A, @active]
state:
  current_document: "doc-007.pdf"
  findings:
    - "Pattern X detected"
  progress: 70%
```

### Speed of Light Communication

Within one LLM call, all instances can communicate:

```
[LLM epoch]
  Analyst-A: "Found Pattern X in docs 1-10"
  Analyst-B: "Found Pattern Y in docs 11-20"
  Analyst-C: "Pattern X + Y together suggest Z!"
  Aggregator: "Capturing insight Z as primary finding"
[End epoch — all written to files]
```

No round-trips. Instant collaboration.

---

## Actor Model

Multi-presence follows the **Actor Model**:

| Actor Model | Multi-Presence |
|-------------|----------------|
| Actor | Card activation |
| Mailbox | Room's inbox |
| Message | Thrown object |
| Spawn | PLAY card |
| State | Instance YAML |

Each activation is an independent actor with:
- Own state
- Own mailbox (room inbox)
- Ability to spawn more actors
- No shared mutable state (files are the state)

---

## Consensus Building

Multiple instances can vote or reach consensus:

```yaml
# Three reviewers examine a document
room-review/activations/
  reviewer-001.yml  # Vote: APPROVE
  reviewer-002.yml  # Vote: APPROVE  
  reviewer-003.yml  # Vote: NEEDS_WORK

# Consensus protocol
consensus:
  method: majority
  votes: [APPROVE, APPROVE, NEEDS_WORK]
  result: APPROVE (2/3)
```

---

## Example: Research Swarm

```yaml
# research-project/
swarm:
  card: researcher-card
  instances: 5
  distribution:
    - room: literature-review/
      focus: "Prior work"
    - room: data-analysis/
      focus: "Dataset exploration"
    - room: methodology/
      focus: "Approach options"
    - room: experiments/
      focus: "Running tests"
    - room: writing/
      focus: "Draft sections"
      
coordination:
  sync_interval: "After each major finding"
  aggregation: "Weekly synthesis in main room"
```

Five researchers, one project, parallel progress.

---

## Lifecycle

```
1. PLAY card IN room     → Activation created
2. Activation runs       → State updated
3. Activation finishes   → Can DELETE or TRANSFORM
4. TRANSFORM into result → Becomes output card
```

Activations can:
- **Complete** and delete themselves
- **Transform** into result cards
- **Spawn** child activations
- **Merge** with other instances
- **Block** on async tool calls

---

## Async Tool Calls

Activations can **block** waiting for external tools:

```yaml
# room-A/activations/analyst-001.yml
card: analyst-card
status: blocked
blocked_on:
  tool: web-search
  query: "latest research on topic X"
  submitted: "2024-01-15T10:30:00"
  expected_duration: "~5 seconds"
```

The **Coherence Engine** leaves blocked activations alone:

```
Epoch scan:
  analyst-001: BLOCKED on web-search → skip
  analyst-002: ACTIVE → process
  analyst-003: ACTIVE → process
  
[web-search returns]

Next epoch:
  analyst-001: READY (result arrived) → resume
  analyst-002: ACTIVE → process
  analyst-003: BLOCKED on file-read → skip
```

### Blocking States

| Status | Meaning |
|--------|---------|
| `active` | Running, process this epoch |
| `blocked` | Waiting for tool result, skip |
| `ready` | Tool returned, resume processing |
| `paused` | User paused, skip until resumed |
| `completed` | Done, can be cleaned up |

### Tool Results

When a tool returns, the result is written to the activation:

```yaml
# After web-search returns
card: analyst-card
status: ready
blocked_on: null
tool_results:
  - tool: web-search
    query: "latest research on topic X"
    completed: "2024-01-15T10:30:05"
    result:
      articles:
        - title: "New Findings on X"
          url: "https://..."
```

The activation resumes with the result in context.

### Parallel Tool Calls

Multiple activations can have outstanding tool calls simultaneously:

```
analyst-001: blocked on web-search
analyst-002: blocked on file-read  
analyst-003: blocked on api-call
analyst-004: active (no tool call)

[All tools return in parallel]

Next epoch: all four ready to process!
```

This is async/await for LLM agents — non-blocking, parallel, resumable.

---

## Dovetails With

- [Trading Card](../card/) — What gets multi-instantiated
- [Room](../room/) — Where activations live
- [Data Flow](../data-flow/) — THROW between instances
- [Coherence Engine](../coherence-engine/) — Orchestrates all instances
- [Speed of Light](../coherence-engine/) — Instant communication

---

## Protocol Symbols

```
MULTI-PRESENCE   — Same card in multiple rooms
ACTOR            — Independent activation with state
CARD-IN-PLAY     — An instantiated card
ACTIVATION       — Runtime instance of a card
```

See: [PROTOCOLS.yml](../../PROTOCOLS.yml#MULTI-PRESENCE)
