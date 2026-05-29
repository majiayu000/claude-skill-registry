---
name: action-queue
description: Sims-inspired task scheduling — queue actions, execute in order
allowed-tools:
  - read_file
  - write_file
  - list_dir
tier: 1
protocol: ACTION-QUEUE
related: [simulation, character, return-stack, advertisement, room, speed-of-light, needs]
tags: [moollm, planning, tasks, sims, game, scheduling]
---

# Action Queue

> *"Queue up what to do next. The Sims showed us the way."*

---

## What Is It?

**Action Queue** is The Sims-inspired task scheduling: instead of doing one thing at a time, you **queue up a sequence of actions** that execute in order.

While [return-stack](../return-stack/) tracks *where you've been*, action-queue tracks *what you're going to do*.

---

## The Sims Connection

In **The Sims**, you click multiple actions and they queue up:

```
Sim's Queue:
  1. Go to fridge     [executing]
  2. Get snack
  3. Eat snack
  4. Watch TV
  5. Go to bed
```

The Sim works through them in order. You can:
- **Add** more actions
- **Cancel** any action
- **Reorder** the queue
- **Insert** urgent actions at the front

**Objects push actions too!** When you try to eat, the fridge pushes "get food" onto the queue. The food pushes "prepare" and "cook". The stove pushes "serve". Each object dangles the next carrot.

MOOLLM does the same for agents and characters.

---

## The Food Chain Pattern

Objects guide you through multi-step processes by pushing actions:

```
> DO eat

Fridge intercepts:
  "You need food first."
  → pushes GET-FOOD to front

Queue: [GET-FOOD, EAT]

Food intercepts:
  "This needs preparation."
  → pushes PREPARE to front
  
Queue: [PREPARE, GET-FOOD, EAT]

Stove intercepts:
  "Needs cooking."
  → pushes COOK to front

Queue: [COOK, PREPARE, GET-FOOD, EAT]

Agent executes in order:
  1. COOK (at stove)
  2. PREPARE (at counter)
  3. GET-FOOD (from fridge)
  4. EAT (finally!)
```

**Dangling a carrot in front of a donkey.** Each object advertises what it needs, pushing prerequisites onto the queue. The agent surfs the possibility space of advertisements, guided step by step.

### Why This Works

- **No hardcoded recipes** — objects know their own prerequisites
- **Emergent behavior** — complex sequences from simple rules
- **Interruptible** — cancel anytime, queue adapts
- **Discoverable** — agent learns by trying
- **Adapts to context** — different appliances, different paths
- **Handles routing** — crowded kitchen? Find another way

### Routing Around Problems

```
> DO cook

Stove advertises COOK... but:
  "Blocked! Alice is using the stove."
  → Checks alternatives
  → Microwave advertises COOK (score: 70)
  → pushes USE-MICROWAVE instead

Queue: [USE-MICROWAVE, PREPARE, GET-FOOD, EAT]
```

If the kitchen is crowded:
```
Kitchen has 4 Sims blocking workspaces.
Counter: "Blocked by Bob"
Stove: "Blocked by Carol"  
Fridge: "Accessible!"

Agent routes around obstacles:
  → Wait for counter? (cost: time)
  → Use outdoor grill? (cost: distance)
  → Order takeout? (cost: money)
  
Highest-scored alternative wins.
```

**Emergent traffic flow.** No pathfinding algorithm needed — objects simply advertise availability, agents pick the best option. Crowded rooms naturally disperse as scores drop.

This is how The Sims creates rich behavior from simple object definitions.

---

## Commands

| Command | Effect |
|---------|--------|
| `DO action` | Add action to end of queue |
| `NEXT` | Execute next queued action |
| `QUEUE` | Show current queue |
| `URGENT action` | Insert at front of queue |
| `CANCEL n` | Remove action #n from queue |
| `CLEAR` | Empty the queue |
| `REORDER n m` | Move action #n to position #m |
| `PAUSE` | Stop executing, keep queue |
| `RESUME` | Continue executing queue |

---

## Example Session

```
> DO examine-workbench
Added: examine-workbench

> DO craft-tool
Added: craft-tool

> DO go-north
Added: go-north

> QUEUE
Action Queue:
  1. examine-workbench
  2. craft-tool
  3. go-north

> NEXT
Executing: examine-workbench
You examine the workbench. It has blueprints and tools.

> URGENT check-inventory
Inserted at front: check-inventory

> QUEUE
Action Queue:
  1. check-inventory    ← urgent
  2. craft-tool
  3. go-north
```

---

## Autonomous Execution

For autonomous agents, the queue runs automatically:

```yaml
# agent.yml
mode: autonomous
action_queue:
  - examine: hypothesis.yml
  - analyze: data/
  - write: findings.md
  - notify: user
  
execution:
  auto_advance: true
  pause_on_error: true
  pause_on_user_input: true
```

Agent works through queue until done, paused, or interrupted.

---

## Queue + Stack Together

**Return stack** and **action queue** complement each other:

| Return Stack | Action Queue |
|--------------|--------------|
| Where you've been | What you'll do |
| Past | Future |
| BACK to revisit | NEXT to advance |
| Navigation history | Task schedule |
| Saved contexts | Pending actions |

Together they form a complete **temporal model**:
- Stack = memory of the past
- Queue = intentions for the future
- Current = the present moment

---

## Compound Actions

Queue items can be compound:

```
> DO [go-to-library, find-book, read-chapter-1]
Added compound action (3 steps)

> QUEUE
Action Queue:
  1. [go-to-library, find-book, read-chapter-1]  (compound)
  2. write-summary
```

Compound actions expand when executed:

```
> NEXT
Expanding compound action...
Action Queue:
  1. go-to-library     [executing]
  2. find-book
  3. read-chapter-1
  4. write-summary
```

---

## Conditional Actions

Actions can have conditions:

```yaml
action_queue:
  - action: craft-tool
    if: has_materials
    
  - action: gather-materials
    if: not has_materials
    
  - action: test-tool
    after: craft-tool
```

The queue adapts based on state.

---

## Integration with Advertisements

Objects [advertise](../advertisement/) actions. The agent queues the best ones:

```
Agent enters workshop.

Objects advertise:
  workbench: CRAFT (90), EXAMINE (50)
  bookshelf: READ (70)
  door: EXIT (40)

Agent queues:
  1. CRAFT at workbench (highest score)
  2. READ at bookshelf (if time permits)
```

Advertisements suggest. Queue commits.

---

## Implementation

```yaml
# character.yml
name: researcher
location: ./lab

action_queue:
  - action: analyze-sample
    target: sample-A
    added: "2024-01-15T10:00:00"
    
  - action: write-notes
    target: notebook
    added: "2024-01-15T10:01:00"
    
  - action: report-findings
    target: user
    added: "2024-01-15T10:02:00"
    
queue_state:
  paused: false
  current_index: 0
  mode: manual  # or autonomous
```

---

## Dovetails With

- [Return Stack](../return-stack/) — Past complements future
- [Advertisement](../advertisement/) — Objects suggest, queue commits
- [Room](../room/) — Where actions happen
- [Speed of Light](../speed-of-light/) — Execute multiple actions per epoch
- [Coherence Engine](../coherence-engine/) — Orchestrates queue execution

---

## Protocol Symbol

```
ACTION-QUEUE
```

Invoke when: Scheduling sequences of actions, autonomous agent behavior.

See: [PROTOCOLS.yml](../../PROTOCOLS.yml#ACTION-QUEUE)
