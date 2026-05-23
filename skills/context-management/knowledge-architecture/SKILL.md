---
name: knowledge-architecture
description: Design knowledge systems using ontological principles—organizing by what things ARE rather than arbitrary hierarchies. Use when structuring personal knowledge bases, designing documentation systems, creating cross-domain linking patterns, building the {OS.me} ecosystem, or architecting information that reveals rather than obscures essential nature. Triggers on knowledge management, documentation architecture, information ontology, or systematic organization of complex domains.
license: MIT
---

# Knowledge Architecture

Organize knowledge by being, not bureaucracy.

## Ontological Foundations

### The Problem with Arbitrary Categories

Most knowledge systems fail because they organize by:
- **Convention**: "This is how it's always been done"
- **Convenience**: "This was easiest at the time"
- **Accident**: "It just ended up here"

Result: Knowledge fragments. Connections hide. Understanding atrophies.

### Ontological Alternative

Organize by asking: **What is this thing, essentially?**

Not "where should this file go?" but "what is the nature of this entity, and what does it relate to by that nature?"

## Categories of Being

### Substances (Primary Entities)

Things that exist in themselves, not as properties of other things.

| Category | Examples | Identifying Question |
|----------|----------|---------------------|
| Persons | You, collaborators, mentors | Who acts? |
| Projects | in-midst-my-life, AI Council | What is being built? |
| Tools | Claude, Figma, modular synth | What enables action? |
| Works | Essays, code, art pieces | What has been created? |
| Concepts | Ideas, theories, frameworks | What is understood? |

### Properties (Dependent Entities)

Exist only as aspects of substances.

| Category | Examples | Identifying Question |
|----------|----------|---------------------|
| States | In-progress, complete, abandoned | What phase? |
| Qualities | Elegant, experimental, stable | What character? |
| Relations | Depends-on, extends, contradicts | How connected? |
| Measures | Size, duration, complexity | What quantity? |

### Events (Temporal Entities)

Things that happen, with beginning and end.

| Category | Examples | Identifying Question |
|----------|----------|---------------------|
| Actions | Decisions, commits, publications | What was done? |
| Processes | Learning, building, evolving | What unfolds? |
| Occasions | Meetings, deadlines, milestones | What marks time? |

## Structural Principles

### Essential vs. Accidental Properties

**Essential**: What makes the thing *that* thing. Remove it, and it's something else.
**Accidental**: Could be otherwise without changing identity.

Example: A "portfolio website"
- Essential: Displays work, represents identity
- Accidental: Uses React, hosted on Vercel, blue color scheme

**Organizing principle**: Group by essential properties. Tag/filter by accidental.

### Genus and Differentia

Classical definition structure: "A is a B that C"

```
Project
├── Software Project (produces code)
│   ├── Library (produces reusable code)
│   ├── Application (produces usable program)
│   └── Infrastructure (produces enabling system)
├── Creative Project (produces art/writing)
│   ├── Visual Work (produces images)
│   ├── Written Work (produces text)
│   └── Interactive Work (produces experience)
└── Research Project (produces knowledge)
    ├── Academic (produces citable work)
    └── Applied (produces practical insight)
```

### Relations as First-Class Citizens

Don't bury relations in properties. Make them navigable.

| Relation Type | Meaning | Inverse |
|---------------|---------|---------|
| depends-on | Cannot exist without | enables |
| extends | Builds upon foundation | is-extended-by |
| contradicts | In tension with | is-contradicted-by |
| implements | Realizes abstraction | is-implemented-by |
| exemplifies | Is instance of pattern | is-exemplified-by |
| supersedes | Replaces previous | is-superseded-by |

## Architecture Patterns

### The Atomic Note

Each note captures ONE thing:
- One concept
- One decision
- One reference
- One connection

Connections emerge from linking atoms, not from cramming compounds into single containers.

### The Index Pattern

Create navigational hubs, not hierarchical folders.

```
# Project Index

## By Nature
- [[Software Projects]]
- [[Creative Projects]]
- [[Research Projects]]

## By State
- [[Active Work]]
- [[Completed Work]]
- [[Archived Work]]

## By Relation
- [[Dependencies Map]]
- [[Influence Graph]]
```

### The Context Layer

Same entity, different contexts:

```
/entities/project-alpha.md          # The thing itself
/contexts/technical/project-alpha.md  # Technical view
/contexts/business/project-alpha.md   # Business view
/contexts/personal/project-alpha.md   # Personal meaning
```

### The Temporal Layer

Knowledge changes. Track it:

```
/current/concept-x.md      # Current understanding
/history/concept-x/        # Evolution
  ├── 2024-01-understanding.md
  ├── 2024-06-revision.md
  └── changelog.md
```

## Naming Conventions

### Entity Naming

```
[type]-[identifier]

project-in-midst-my-life
concept-modular-synthesis
person-mentor-name
tool-claude-desktop
```

### Relation Naming

```
[source]--[relation]--[target]

project-alpha--depends-on--library-beta
concept-x--contradicts--concept-y
```

### State Naming

```
[entity].[state-type]

project-alpha.status = active
project-alpha.phase = development
project-alpha.health = stable
```

## Cross-Domain Integration

### The Translation Pattern

Same concept, different domain vocabularies:

```yaml
concept: feedback-loop
domains:
  synthesis: "output patches to input, creating evolving timbre"
  systems: "output affects input, creating dynamic behavior"
  learning: "results inform practice, creating improvement"
  biology: "effect influences cause, creating homeostasis"
```

### The Isomorphism Pattern

Find structural similarities across domains:

```
Modular Synthesis     ←→     Software Architecture
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Oscillator            ←→     Data Source
Filter                ←→     Transformer
Patch Cable           ←→     API Connection
Mixer                 ←→     Aggregator
CV                    ←→     Configuration
Audio Signal          ←→     Data Payload
```

### The Emergence Pattern

Document what emerges from combination:

```
Component A + Component B = Emergent Property C

# Example
Note-taking + Linking + Time = Evolving understanding
(None of the parts alone produces this)
```

## Implementation

### File System Mapping

```
knowledge/
├── entities/           # Primary substances
│   ├── projects/
│   ├── concepts/
│   ├── works/
│   └── tools/
├── relations/          # Connection maps
│   ├── dependencies.md
│   ├── influences.md
│   └── contradictions.md
├── contexts/           # Perspective layers
│   ├── technical/
│   ├── personal/
│   └── temporal/
├── indices/            # Navigation hubs
│   ├── by-nature.md
│   ├── by-state.md
│   └── by-domain.md
└── meta/               # About the system itself
    ├── ontology.md
    ├── conventions.md
    └── changelog.md
```

### Metadata Schema

```yaml
---
type: [entity-type]
nature: [essential description]
state: [current state]
created: [date]
modified: [date]
relations:
  depends-on: [list]
  extends: [list]
  relates-to: [list]
contexts: [list of applicable contexts]
tags: [accidental properties for filtering]
---
```

## References

- `references/ontological-terms.md` - Philosophical vocabulary
- `references/implementation-patterns.md` - Concrete file/linking patterns
