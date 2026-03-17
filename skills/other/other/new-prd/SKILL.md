---
name: new-prd
description: Create a new PRD from the template with all 11 sections
---

# New PRD Skill

Create a new Product Requirements Document from the x4-mono PRD template.

## Arguments

The user describes what they want to build. If unclear, ask for:

- Feature name / title
- Problem it solves
- High-level scope (what's in, what's out)

## Workflow

1. **Determine PRD number**: Read `wiki/status.md` to find the next available PRD number
2. **Create slug**: Derive a kebab-case slug from the title (e.g., `user-notifications`)
3. **Copy template**: Copy `wiki/_templates/prd-template.md` to `wiki/inbox/prd-NNN-{slug}.md`
4. **Fill metadata**: Set PRD ID, Title, Author, Status (Draft), Version (0.1), Date
5. **Guide through sections**: Help the user fill all 11 required sections
6. **Update status.md**: Add a row to the PRD Inventory table

## File Locations

- **Template**: `wiki/_templates/prd-template.md`
- **New PRD**: `wiki/inbox/prd-NNN-{slug}.md`
- **Status**: `wiki/status.md`

## Required Sections

| #   | Section                     | Key Content                                   |
| --- | --------------------------- | --------------------------------------------- |
| 1   | Problem Statement           | Pain point, why it matters                    |
| 2   | Success Criteria            | Measurable targets (table)                    |
| 3   | Scope                       | In scope, out of scope, assumptions           |
| 4   | System Context              | Dependency diagram, consumed by               |
| 5   | Technical Design            | Data model, architecture, API, file structure |
| 6   | Implementation Plan         | Task table + Claude Code annotations          |
| 7   | Testing Strategy            | Test pyramid, key scenarios                   |
| 8   | Non-Functional Requirements | Performance, security targets                 |
| 9   | Rollout & Migration         | Steps, rollback plan                          |
| 10  | Open Questions              | Unresolved items with impact                  |
| 11  | Revision History            | Version log                                   |

## Task Annotation Format (Section 6)

Every task marked as Claude Code Candidate must include:

```markdown
**Task N (Name)**:

- **Context needed**: [files to read before starting]
- **Constraints**: [what NOT to do, boundaries to respect]
- **Done state**: [specific completion criteria]
- **Verification command**: [shell command to verify]
```

## Status.md Update

Add to the PRD Inventory table:

```markdown
| PRD-NNN | [Title](inbox/prd-NNN-slug.md) | Draft | PRD-XXX (if any) | `wiki/inbox/` |
```

If the PRD has dependencies, update the Dependency Graph section too.

## Conventions

- PRD IDs are sequential: PRD-001, PRD-002, etc.
- Status starts as `Draft` in `wiki/inbox/`
- All task estimates use t-shirt sizes: XS, S, M, L, XL
- Dependencies reference other PRD IDs
- Success criteria must be measurable (numbers, yes/no, specific outcomes)
