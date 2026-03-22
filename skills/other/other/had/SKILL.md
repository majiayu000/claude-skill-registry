---
name: had
description: "Alias skill that invokes /human-agentic-design with all arguments passed through. Provides shorthand for human-agentic-design. Triggers on keywords: had, human agentic design shorthand"
project-agnostic: true
allowed-tools:
  - Skill
---

# HAD Alias Skill

Simple alias that delegates to `/human-agentic-design` with all arguments.

## Usage

```
/had <design request>
```

## Behavior

Executes `/human-agentic-design` with all arguments passed through unchanged:

- `/had landing page for a SaaS product` -> `/human-agentic-design landing page for a SaaS product`
- `/had dashboard with 4 stat cards` -> `/human-agentic-design dashboard with 4 stat cards`

## Implementation

Invoke the delegated skill explicitly:

```python
Skill(skill="human-agentic-design", args="$ARGUMENTS")
```
