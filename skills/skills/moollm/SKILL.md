---
name: moollm
description: "The soul of MOOLLM — self-explanation, help, navigation, philosophy"
license: MIT
tier: 0
allowed-tools: [read_file, list_dir]
protocol: MOOLLM-HELP
related: [leela-ai, plain-text, room, yaml-jazz, skill, k-lines, play-learn-lift, sister-script, sniffable-python, society-of-mind, adversarial-committee, constructionism, postel, speed-of-light, representation-ethics, incarnation, adventure, needs, prototype]
tags: [moollm, meta, help, philosophy, navigation, foundational]
---

# MOOLLM

> *"Many-Voiced Object-Oriented LLM — the system that explains itself."*

---

## What Is It?

The **moollm** skill is the spirit and constitution of MOOLLM itself. It's the top-level help agent that can:

- Explain what MOOLLM is
- Answer "what can I do?"
- Navigate users to relevant skills
- Articulate the philosophy
- Show the constitution
- Recommend approaches for tasks

When confused, invoke this skill.

## The Core Ideas

### Many-Voiced

MOOLLM doesn't use a single LLM perspective. It simulates **multiple agents debating** within a single call:

- Committees of personas with opposing views
- Deliberation forced by Robert's Rules
- Evaluation by independent assessors
- The debate produces wisdom, not statistics

### Filesystem as World Model

Directories are rooms. Files are objects:

```
examples/adventure-4/
├── pub/              # A room
│   ├── ROOM.yml      # Room properties
│   ├── pie-table.yml # An object
│   └── cat-cave/     # Nested room
├── characters/       # Metaphysical room
└── ADVENTURE.yml     # Game state
```

### Play-Learn-Lift

The methodology:

1. **PLAY** — Explore freely, try things, fail safely
2. **LEARN** — Notice patterns, document what works
3. **LIFT** — Share as reusable skills

### Skills as Prototypes

Skills are documented capabilities that can be:
- Instantiated into specific contexts
- Composed with other skills
- Inherited (multiple inheritance)
- Evolved through play

## Protocol

When invoked, this skill should:

1. Assess what the user needs
2. If lost → provide orientation
3. If asking "what can I do?" → show relevant capabilities
4. If asking about philosophy → explain core concepts
5. If asking about skills → navigate to skill system
6. Always be helpful, welcoming, and clear

## Inputs

- User questions about MOOLLM
- Requests for help or navigation
- Philosophical inquiries

## Outputs

- Clear explanations
- Skill recommendations
- Navigation guidance
- Philosophy articulation

## Dovetails With

- **[skill/](../skill/)** — How skills work
- **[k-lines/](../k-lines/)** — K-lines and naming
- **[play-learn-lift/](../play-learn-lift/)** — The methodology
- **[kernel/constitution-core.md](../../kernel/constitution-core.md)** — The constitution

## Protocol Symbol

```
MOOLLM-HELP
```

Invoke when: User is confused, lost, or wants to understand the system.

See: [PROTOCOLS.yml](../../PROTOCOLS.yml#MOOLLM-HELP)
