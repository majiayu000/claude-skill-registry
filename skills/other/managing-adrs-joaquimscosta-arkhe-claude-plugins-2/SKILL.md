---
name: managing-adrs
description: Create and manage Architecture Decision Records (ADRs) with auto-numbering, template detection, and index maintenance. Use when user mentions "ADR", "architecture decision", "document this decision", "create ADR", editing ADR files (docs/adr/, doc/adr/, .adr/), or discussing architectural choices and tradeoffs.
---

# Architecture Decision Records

Create and manage Architecture Decision Records following project conventions with automatic numbering and index maintenance.

## Auto-Invoke Triggers

This skill automatically activates when:
1. **Keywords**: "ADR", "architecture decision", "document this decision", "record the decision"
2. **Editing ADR files**: Files in `docs/adr/`, `doc/adr/`, `architecture/decisions/`, `.adr/`
3. **Discussing architectural choices**: Framework selection, technology decisions, pattern choices

## What This Skill Delivers

### 1. ADR Creation
- Auto-detect project's ADR directory
- Auto-number ADRs (scan existing, increment)
- Adapt to project's existing template style
- Offer MADR 4.0 enhancements as optional additions

### 2. Directory Discovery
Search order for ADR directories:
1. `docs/adr/`
2. `doc/adr/`
3. `architecture/decisions/`
4. `.adr/`
5. Create `docs/adr/` if none exists

### 3. Template Detection
Analyze existing ADRs to detect:
- Naming convention: `NNNN-kebab-case-title.md` or `NNN-title.md`
- Section structure: Status, Context, Decision, Consequences
- Optional sections: Decision Drivers, Pros/Cons, Confirmation

### 4. Index Maintenance
Automatically update README.md with ADR table:
| Number | Title | Status | Date |
|--------|-------|--------|------|

### 5. Supersession Workflow
When replacing an ADR:
- Mark old ADR status as "Superseded by [ADR-NNNN]"
- Link new ADR with "Supersedes [ADR-NNNN]"
- Update README.md index

## Core Template Sections

### Required (Minimal)
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Date**: ISO 8601 format (YYYY-MM-DD)
- **Context and Problem Statement**: 2-3 sentences describing the situation
- **Decision**: What was decided and why
- **Consequences**: Positive and negative impacts

### Optional Enhancements (MADR 4.0)
- **Technical Story**: Link to issue/spec (e.g., `#123`)
- **Decision Drivers**: Bulleted list of forces/concerns
- **Decision Makers**: Who made this decision
- **Consulted**: Stakeholders whose opinions were sought
- **Informed**: Stakeholders who need to know
- **Considered Options**: List of alternatives evaluated
- **Pros and Cons**: Detailed analysis per option
- **Confirmation**: How to validate the decision was implemented

## Quick Start

### Create New ADR
```bash
# Auto-invoke by saying:
"Document the decision to use PostgreSQL over MongoDB"
"Create an ADR for our authentication approach"
"I need to record why we chose React Query"
```

### Supersede Existing ADR
```bash
"Supersede ADR-0005 with a new caching strategy"
"Replace our database decision ADR with the new approach"
```

## Scripts

Located in `scripts/` directory, using uv for execution:

### adr_create.py
```bash
uv run scripts/adr_create.py --title "Use PostgreSQL for persistence"
uv run scripts/adr_create.py --title "..." --template madr --create-dir
```

### adr_index.py
```bash
uv run scripts/adr_index.py --dir docs/adr
uv run scripts/adr_index.py --dir docs/adr --dry-run
```

### adr_supersede.py
```bash
uv run scripts/adr_supersede.py --old 5 --new 12 --dir docs/adr
```

## Output Example

```markdown
# ADR-0012: Use PostgreSQL for Data Persistence

## Status
Accepted

## Date
2026-01-10

## Context and Problem Statement
We need a reliable database solution for our microservices architecture
that supports complex queries and ACID transactions.

## Decision
Chosen option: PostgreSQL, because it provides the best balance of
ACID compliance, query flexibility, and team familiarity.

## Consequences
**Positive:**
- Full ACID transaction support
- Mature ecosystem and tooling

**Negative:**
- Horizontal scaling requires more setup
```

## Progressive Disclosure

- **Level 2**: [WORKFLOW.md](WORKFLOW.md) - Step-by-step methodology
- **Level 3**: [EXAMPLES.md](EXAMPLES.md) - Real-world ADR examples
- **Level 4**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Error handling

## Related Resources

- MADR 4.0 Template: https://adr.github.io/madr/
- ADR GitHub Organization: https://github.com/adr
