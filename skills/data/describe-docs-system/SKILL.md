---
name: describe-docs-system
description: Documentation system location and maintenance requirements. Load when consulting or updating project documentation.
user-invocable: false
---

## Documentation System

Project documentation lives in `.ushabti/docs/`.

```
.ushabti/docs/
├── index.md      # Index of all project documentation
└── *.md          # Documentation on project systems
```

### Agent Responsibilities

**Scribe**: MUST consult `.ushabti/docs/` when planning Phases. Understanding documented systems is prerequisite to coherent planning.

**Builder**: MUST consult `.ushabti/docs/` during implementation. When code changes affect documented systems, update the relevant docs. Include docs files in the `touched` list in progress.yaml when updated.

**Overseer**: MUST verify that docs are reconciled with code changes before declaring a Phase complete. Stale docs are defects.

### Review Gate

A Phase cannot be marked complete until docs are reconciled with the code work performed during that Phase. This is a hard requirement enforced by Overseer.
