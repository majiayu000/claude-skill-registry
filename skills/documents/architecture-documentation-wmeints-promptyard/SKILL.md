---
name: documenting-architecture
description: Use this skill when modifying or creating architecture documentation.
---

## Documenting architecture

Use this skill to make changes to the architecture documentation in the project
following the guidelines described below.

## Guidelines for specific sections

- Introduction and goals: ./references/01-introduction-and-goals.md
- Constraints: ./references/02-constraints.md
- Context and scope: ./references/03-context-and-scope.md
- Solution strategy: ./references/04-solution-strategy.md
- Building block view: ./references/05-building-block-view.md
- Runtime view: ./references/06-runtime-view.md
- Deployment view: ./references/07-deployment-view.md
- Concepts: ./references/08-concepts.md

## Recording decisions

IMPORTANT: Make sure to use the `record-adr` skill to record decision records!

## Diagrams

- Use mermaid to record diagrams
- Prefer to use C4 diagrams where possible, otherwise use block diagrams
- Prefer to use sequence diagrams for recording runtime scenarios or program flows