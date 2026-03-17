---
name: prototype
description: "Objects clone from prototypes, not instances from classes"
license: MIT
tier: 0
allowed-tools: []
related: [skill, room, container, character, card, simulation, constructionism, return-stack, debugging]
tags: [moollm, inheritance, self, javascript, clone, deoptimization]
protocol: PROTOTYPE
credits:
  - "David Ungar — Self language creator"
  - "Randall Smith — Self language co-creator"
  - "Brendan Eich — JavaScript (Self-influenced)"
---

# PROTOTYPE

> **"Objects all the way down."**

The philosophy of prototype-based inheritance: no classes, just concrete examples that you clone and modify.

---

## The Problem with Classes

Classical inheritance says:
1. Define an abstract blueprint (class)
2. Instantiate it to create objects
3. Objects are "instances of" classes

But this creates problems:
- **Abstraction gap**: Classes describe things that don't exist
- **Rigidity**: Class hierarchies are hard to change
- **Ceremony**: Lots of boilerplate to create simple things

---

## The Prototype Solution

Prototype-based inheritance says:
1. Create a concrete example (prototype)
2. Clone it to make new objects
3. Modify the clone as needed
4. Clones delegate to prototypes for missing slots

**Everything is concrete. Everything exists.**

---

## How Self Works

### Slots

Objects are collections of **slots**:

```
cat: (|
  name <- "Terpie".
  color <- "orange".
  meow = (| | "Meow!" |).
  parent* = catPrototype.
|)
```

- `name`, `color` — data slots
- `meow` — method slot
- `parent*` — parent slot (for delegation)

### Delegation

When you send a message to an object:
1. Look in the object's own slots
2. If not found, look in parent's slots
3. Continue up the chain
4. First match wins

### Cloning

To create a new cat:
```
newCat := cat clone.
newCat name: "Stroopwafel".
newCat color: "tabby".
```

The new cat:
- Has its own `name` and `color` slots
- Delegates `meow` to the prototype
- Can add new slots anytime

---

## MOOLLM Implementation

MOOLLM implements prototype inheritance via the **Delegation Object Protocol (DOP)**:

### PROTOTYPES.yml

```yaml
# In an instance directory
prototypes:
  - path: "skills/room"
  - path: "skills/adventure"
  
resolution:
  strategy: "first-match-wins"
```

### File Resolution

1. Check local directory
2. Check each prototype in order
3. First match wins
4. State never inherits (always local)

### Example: A Room Instance

```
examples/adventure-4/pub/
├── ROOM.yml           # Local override (shadows prototype)
├── PROTOTYPES.yml     # Points to skills/room
├── state/             # Local-only state
│   └── visitors.yml
└── (missing files delegate to skills/room/)
```

---

## Why Prototypes for LLMs?

LLMs don't compute inheritance algorithms. They navigate files.

Prototype-based inheritance is **LLM-friendly** because:
- **Explicit**: You can see the prototype chain
- **Navigable**: Just follow file paths
- **Concrete**: No abstract classes to imagine
- **Forgettable**: Each lookup is independent

---

## The Wisdom of Self

> *"The best message is no message."*

Self taught us that simplicity wins:
- One mechanism (slots) instead of many
- Objects are just dictionaries
- Methods are just slots that happen to be code
- Inheritance is just delegation

MOOLLM applies this: directories are objects, files are slots, resolution is delegation.

---

## Historical Context

| Year | Event |
|------|-------|
| 1986 | Ungar & Smith begin Self at Xerox PARC |
| 1987 | Self paper published |
| 1991 | Self 2.0 with compilation |
| 1995 | JavaScript created (heavily Self-influenced) |
| 2024 | MOOLLM applies Self to LLM filesystems |

---

## See Also

- **[../skill/delegation-object-protocol.md](../skill/delegation-object-protocol.md)** — The DOP specification
- **[../skill/skill-instantiation-protocol.md](../skill/skill-instantiation-protocol.md)** — How skills become instances
- **[../constructionism/](../constructionism/)** — Learning by building
- **[../character/](../character/)** — Characters as prototype instances

---

## Further Reading

- Ungar, D. & Smith, R. (1987). *Self: The Power of Simplicity*
- Ungar, D. (1995). *Organizing Programs Without Classes*
- [selflanguage.org](http://selflanguage.org/)

---

*"Self is a network, not a node."*
