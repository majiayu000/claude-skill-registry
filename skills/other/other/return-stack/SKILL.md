---
name: return-stack
description: "Where you've been is where you can go back to."
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [room, adventure, character, memory-palace, action-queue, card, session-log, prototype, debugging]
tags: [moollm, navigation, history, breadcrumbs, continuations, deoptimization, introspection]
---

# Return Stack

> *"Where you've been is where you can go back to."*

---

## What Is It?

**Return Stack** treats navigation history as a first-class **continuation** — a stack of saved positions you can manipulate like browser history or a call stack.

---

## The Metaphor

| Programming | Browser | MOOLLM |
|-------------|---------|--------|
| Call stack | History | Return stack |
| Return address | Back button | Previous room |
| Stack frame | Tab | Room context |
| Push | Navigate | ENTER |
| Pop | Back | BACK |

---

## Commands

| Command | Effect |
|---------|--------|
| `ENTER room` | Push current room, enter new one |
| `BACK` | Pop stack, return to previous room |
| `FORWARD` | Redo after BACK (if available) |
| `HISTORY` | Show the stack |
| `BOOKMARK` | Save current position |
| `GOTO bookmark` | Jump to saved position |
| `STACK` | Show all open "tabs" (parallel stacks) |
| `FORK` | Create new tab from current position |

---

## Example Session

```
> ENTER workshop
[Stack: lobby]

> ENTER storage
[Stack: lobby → workshop]

> ENTER archive
[Stack: lobby → workshop → storage]

> BACK
Returning to storage...
[Stack: lobby → workshop]

> BACK
Returning to workshop...
[Stack: lobby]

> HISTORY
  1. lobby (start)
  2. workshop
  3. storage
  4. archive ← furthest
  
Current: workshop (position 2)
```

---

## Bookmarks

Save positions for later:

```
> BOOKMARK "interesting-spot"
Bookmarked: workshop as "interesting-spot"

> ENTER research
> ENTER data-room
> ENTER sub-analysis
[Deep in the hierarchy]

> GOTO interesting-spot
Returning to workshop...
[Stack cleared, at bookmark]
```

---

## Forking (Tabs)

Create parallel exploration paths:

```
> FORK
Created new tab from workshop.
Tab 1: lobby → workshop
Tab 2: workshop (active) ←

> ENTER experiment-A
[Tab 2: workshop → experiment-A]

> STACK
Tab 1: lobby → workshop
Tab 2: workshop → experiment-A ←

> TAB 1
Switching to Tab 1...
[Now at workshop via tab 1]
```

---

## As Continuation

The return stack IS a continuation:

```yaml
# Stored in character's pocket
return_stack:
  - path: "./lobby"
    context: {examining: "welcome-sign"}
  - path: "./workshop" 
    context: {crafting: "blueprint-v2"}
  - path: "./storage"
    context: {searching: "rare-materials"}
    
# Current position
current: "./archive"
context: {reading: "old-records"}
```

When you BACK, you don't just return to the room — you **restore the context** you had there.

---

## Portable Journey

The stack travels with you:

```
> INVENT
Inventory:
  - notebook
  - pen
  - return_stack: [lobby → workshop → storage]
```

You can:
- **Save** your journey to a file
- **Share** it with others
- **Replay** someone else's exploration
- **Branch** from any point in their journey

---

## HyperCard Heritage

HyperCard had:
- Stacks of cards
- "Go back" button
- Breadcrumb trail
- Bookmarks

MOOLLM extends this:
- Rooms as cards
- BACK command
- Return stack as data
- Bookmarks as saved positions
- FORK for parallel exploration

---

## Implementation

```yaml
# character.yml
name: explorer
location: ./archive

navigation:
  return_stack:
    - room: ./lobby
      entered: "2024-01-15T10:00:00"
    - room: ./workshop
      entered: "2024-01-15T10:05:00"
      context:
        active_task: "crafting"
    - room: ./storage
      entered: "2024-01-15T10:15:00"
      
  bookmarks:
    interesting-spot:
      room: ./workshop
      context: {task: "blueprint-review"}
    start:
      room: ./lobby
      
  forward_stack: []  # After BACK, stores where you came from
```

---

## Dynamic Deoptimization

The Self programming language (source of our prototype inheritance) pioneered **dynamic deoptimization**: aggressively inlining code for performance, then reconstructing the "logical" call stack on demand when debugging.

The LLM does this naturally for narrative:

| Self | MOOLLM |
|------|--------|
| Inlined bytecode | Flattened conversation |
| Deoptimized frames | Reconstructed causality |
| Breakpoint trigger | "How did we get here?" |
| Stack trace | Causal chain from evidence |

**The stack isn't explicitly maintained, but it's recoverable.**

### How It Works

When you ask for history, the LLM examines:

```yaml
evidence_sources:
  - session_log: "Append-only narrative trail"
  - room_state: "Accumulated changes"
  - character_location: "Current position"
  - file_timestamps: "Order of modifications"
  - chat_context: "Recent decisions"
```

And synthesizes a virtual stack trace:

```
Deduced navigation:
1. lobby (start)
2. workshop (examining blueprints)
3. storage (found locked chest)
4. workshop (returned for key) ← BACK
5. storage (unlocked chest)
6. archive (following map) ← current
```

**This is introspection without instrumentation** — the same insight that made Self's debugger magical.

---

## Dovetails With

- [Action Queue](../action-queue/) — **The complement**: stack = past, queue = future
- [Room](../room/) — What you're navigating between
- [Coherence Engine](../coherence-engine/) — Tracks navigation state
- [Adventure](../adventure/) — Narrative exploration
- [Session Log](../session-log/) — Records the journey
- [Prototype](../prototype/) — Self language heritage
- [Debugging](../debugging/) — Stack traces on demand

---

## Protocol Symbols

```
RETURN-STACK      — Navigation history as data
BACK / FORWARD    — Stack manipulation
BOOKMARK / GOTO   — Saved positions
FORK              — Parallel exploration
HYPERCARD-HIERARCHY — The room/card model
```

See: [PROTOCOLS.yml](../../PROTOCOLS.yml#RETURN-STACK)
