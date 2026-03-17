---
name: shared-adr
description: Create and manage Architecture Decision Records (ADRs) to document significant technical decisions.
argument-hint: "[--new <title>] [--list] [--supersede <id>]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Document significant technical decisions with context, rationale, and consequences. ADRs create a searchable history of why things were built the way they were.

## Arguments
- `--new <title>` — Create new ADR
- `--list` — List all ADRs
- `--supersede <id>` — Create ADR that supersedes an existing one
- (no args) — Interactive mode

## What gets created

```
docs/adr/
├── 0001-record-architecture-decisions.md
├── 0002-use-mongodb-for-persistence.md
├── 0003-adopt-swiftui-mvvm-pattern.md
└── template.md
```

## ADR structure

```markdown
# [ID]. [Title]

Date: YYYY-MM-DD
Status: [proposed | accepted | deprecated | superseded by ADR-XXXX]

## Context
What is the issue we're facing? What forces are at play?

## Decision
What have we decided to do?

## Consequences
What are the positive and negative results of this decision?
```

## When to write an ADR
- Choosing a framework, library, or tool
- Defining architectural patterns (MVVM, monorepo, etc.)
- Changing data models or API contracts
- Selecting third-party services
- Making security or compliance decisions
- Any decision you might need to explain later

## Naming convention
- Format: `NNNN-title-in-kebab-case.md`
- Numbers: Sequential, zero-padded (0001, 0002...)
- Title: Short, descriptive, lowercase with hyphens

## Statuses
| Status | Meaning |
|--------|---------|
| **proposed** | Under discussion |
| **accepted** | Approved and in effect |
| **deprecated** | No longer recommended |
| **superseded** | Replaced by another ADR |

## Workflow
1. Identify decision that needs documentation
2. Create ADR using template
3. Write context (forces, constraints)
4. Document decision clearly
5. List consequences (good and bad)
6. Review with team (if applicable)
7. Update status to accepted

## Output
- ADR file created
- ID assigned
- Status set to proposed

## Reference
For templates and examples, see `reference/shared-adr-reference.md`
