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

## Constitutional File Map (kernel/)

- `kernel/README.md` — index and navigation for kernel docs
- `kernel/constitution-core.md` — core constitution and invariants
- `kernel/constitution-template.md` — template for new constitutions
- `kernel/ARCHITECTURE.md` — system architecture overview
- `kernel/context-assembly-protocol.md` — context assembly rules
- `kernel/memory-management-protocol.md` — memory, limits, persistence
- `kernel/event-logging-protocol.md` — logging and provenance
- `kernel/tool-calling-protocol.md` — tool usage contract
- `kernel/self-healing-protocol.md` — recovery and repair behaviors
- `kernel/DIRECTORY-AS-OBJECT.md` — directory as object model
- `kernel/SELFISH-COM-IMPLEMENTATION.md` — SELF lineage in practice
- `kernel/INTEREST-GATES.yml` — attention gating rules
- `kernel/NAMING.yml` — top-level naming policy
- `kernel/naming/NAMING.yml` — detailed naming rules
- `kernel/naming/NAMING-K-LINES.yml` — K-line naming standards
- `kernel/naming/NAMING-CONSTELLATIONS.yml` — constellation naming
- `kernel/naming/NAMING-COMPILATION.yml` — compiled name patterns
- `kernel/naming/NAMING-PATH-VARIABLES.yml` — path variable rules
- `kernel/naming/NAMING-RELATIONSHIPS.yml` — relationship naming
- `kernel/naming/URLS.yml` — URL conventions
- `kernel/drivers/README.md` — driver index
- `kernel/drivers/cursor.yml` — Cursor-specific driver
- `kernel/drivers/generic.yml` — baseline driver
- `kernel/drivers/custom.yml` — site-specific overrides
- `kernel/drivers/claude-code.yml` — Claude Code driver
- `kernel/drivers/antigravity.yml` — experimental driver

## Local Runtime Files (.moollm/)

These are gitignored runtime files for session state, scratch, and logs.

- `.moollm/working-set.yml` — current focus and active files
- `.moollm/hot.yml` — priority hints
- `.moollm/cold.yml` — cold-start state
- `.moollm/startup.yml` — startup context
- `.moollm/output.md` — append-only output log
- `.moollm/session-log.md` — append-only session log
- `.moollm/bootstrap-probe.yml` — bootstrap probes and checks

## Cursor Boot Optimization (cursor-mirror)

Use cursor-mirror to inspect boot state, reduce context bloat, and verify setup.

Commands (need composer ID):
- `tree` — list sessions/composers
- `status` — quick health check
- `tail --limit 50` — recent messages
- `timeline <composer>` — full event sequence
- `thinking <composer>` — reasoning blocks
- `tools <composer>` — tool call history
- `grep <pattern>` — search transcripts

Use this to:
- confirm which bootstrap ran
- locate missing context
- triage performance issues
- audit tool-call provenance

## Plan: MOOLLM Linter, Mirror, Compiler

### Phase 0 — Meta Inhale (Planning Only)

1. Inventory the repository structure and file types.
2. Define categories: essential, primary, secondary, hidden.
3. Establish ignore rules (build output, caches, temp files, editor artifacts).
4. Identify canonical docs to preserve: top-level `README.md`, `designs/`, `docs/`.
5. Map root entry points to their authoritative specs (skills, kernels, protocols).
6. Reverse-engineer the root `README.md` into a structured spec:
   - Purpose
   - Audience
   - Sections
   - Source references
   - Link strategy
7. Define a report format for validation output:
   - Structural warnings
   - Missing declarations
   - Naming consistency
   - Cross-link integrity
8. Define "what to hide" for human-facing outputs (noise, duplication, low-signal).
9. Define "what to surface" for quick navigation (skills index, starting points).
10. Define sister-script scope: lint, mirror, compile.
11. Write a sister-script design brief (no code yet).

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
