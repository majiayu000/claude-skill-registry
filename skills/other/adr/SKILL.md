---
name: adr
description: >-
  Create, review, and manage Architecture Decision Records (ADRs) with
  auto-numbering, template detection, quality review, and index maintenance.
  Use when user mentions "ADR", "architecture decision", "document this
  decision", "create ADR", "review ADR", editing ADR files (docs/adr/,
  doc/adr/, .adr/), or discussing architectural choices and tradeoffs.
argument-hint: "<action> [args]  (create <title> | review <path> | status <number> <status> | list | supersede <old> <new> | index)"
---

# ADR Manager

Create and manage Architecture Decision Records following project conventions with automatic numbering and index maintenance.

## Argument Parsing

When invoked explicitly with `/adr <action>`, parse the first word:

| First word | Remaining args | Operation |
|------------|---------------|-----------|
| `create` | `<title>` | Create a new ADR with the given title |
| `review` | `<path>` | Lightweight quality review of an ADR |
| `status` | `<number> <status>` | Transition ADR status with validation and side effects |
| `list` | (none) | List all ADRs (same as running `adr_index.py --dry-run`) |
| `supersede` | `<old-number> <new-number>` | Supersede an old ADR with a new one |
| `index` | (none) | Regenerate the README.md index |
| (empty) | | Auto-detect from conversation context |

If the first word doesn't match an action, treat the entire `$ARGUMENTS` as a title and default to `create`.

When auto-invoked (no explicit `/adr` command), detect the operation from conversation context as before.

## Auto-Invoke Triggers

This skill automatically activates when:
1. **Keywords**: "ADR", "architecture decision", "document this decision", "record the decision"
2. **Editing ADR files**: Files in `docs/adr/`, `doc/adr/`, `architecture/decisions/`, `.adr/`
3. **Discussing architectural choices**: Framework selection, technology decisions, pattern choices

## What This Skill Delivers

### 1. ADR Creation (Enhanced)
- Gather context from conversation, codebase, and existing ADRs
- Confirm decision topic with user before drafting
- Auto-detect project's ADR directory and template style
- Auto-number ADRs (scan existing, increment)
- Draft populated ADR with real content (not blank template)
- Always append Author's Notes section (2-5 items)
- Offer MADR 4.0 enhancements as optional additions
- Suggest `/adr review <path>` after creation

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

### 6. ADR Review
Lightweight quality check using the `adr-critic` agent:
1. Read ADR at given path (if empty, ask — suggest globbing ADR dirs)
2. Spawn adr-critic agent (`subagent_type: "doc:adr-critic"`)
   - Pass: full ADR content
   - Instruct: "Read Author's Notes first as prioritized review targets"
3. Agent evaluates 4 dimensions, returns score + verdict + 3-5 findings
4. Present review to user
5. Verdicts: **Approve** | **Needs improvement** | **Needs rethink**
6. Suggest next steps based on verdict

### 7. Author's Notes (Confession)
Every ADR gets an `## Author's Notes` section after Consequences:
- **Shortcuts**: What was simplified or hand-waved?
- **Assumptions**: What was believed but not verified?
- **Uncertainties**: Which parts had least information?

Target: 2-5 items. Be specific, reference ADR sections.

**Lifecycle**: Added on create (always) | Read by adr-critic as review targets | Stripped when Status → Accepted (via `/adr status`) | Preserved on Superseded | Refreshed on major rewrites.

### 8. Status Transitions
Dedicated command for changing ADR status with validation and side effects:
1. Find ADR by number, read current status
2. Validate transition — warn on unusual paths (allow but confirm):
   - Accepted → Proposed: "Going backwards — re-opening a decided matter"
   - → Accepted without prior `/adr review`: "Consider reviewing first"
   - → Superseded directly: "Use `/adr supersede` to link replacement"
3. Apply status change, handle side effects:
   - **→ Accepted**: Strip `## Author's Notes` section entirely
4. Update README.md index via `adr_index.py`

**Valid statuses**: Proposed | Accepted | Deprecated | Superseded

## Core Template Sections

### Required (Minimal)
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Date**: ISO 8601 format (YYYY-MM-DD)
- **Context and Problem Statement**: 2-3 sentences describing the situation
- **Decision**: What was decided and why
- **Consequences**: Positive and negative impacts
- **Author's Notes**: Shortcuts, assumptions, uncertainties (stripped on Accepted)

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
# Explicit subcommands:
/adr create Use PostgreSQL over MongoDB
/adr create Authentication approach for mobile apps

# Auto-invoke by saying:
"Document the decision to use PostgreSQL over MongoDB"
"Create an ADR for our authentication approach"
"I need to record why we chose React Query"
```

### Review an ADR
```bash
# Explicit subcommand:
/adr review docs/adr/0005-use-postgresql-for-persistence.md

# Auto-invoke:
"Review ADR-0005 for decision quality"
"Check if our caching ADR has solid reasoning"
```

### Supersede Existing ADR
```bash
# Explicit subcommand:
/adr supersede 5 12

# Auto-invoke:
"Supersede ADR-0005 with a new caching strategy"
"Replace our database decision ADR with the new approach"
```

### Change Status
```bash
# Transition with validation and side effects:
/adr status 14 accepted
/adr status 7 deprecated

# Auto-strips Author's Notes when accepting
# Warns on unusual transitions (e.g., skipping review)
```

### List and Index
```bash
/adr list
/adr index
```

## Scripts

Located in `${CLAUDE_SKILL_DIR}/scripts/` directory, using uv for execution:

### adr_create.py
```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/adr_create.py --title "Use PostgreSQL for persistence"
uv run ${CLAUDE_SKILL_DIR}/scripts/adr_create.py --title "..." --template madr --create-dir
```

### adr_index.py
```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/adr_index.py --dir docs/adr
uv run ${CLAUDE_SKILL_DIR}/scripts/adr_index.py --dir docs/adr --dry-run
```

### adr_supersede.py
```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/adr_supersede.py --old 5 --new 12 --dir docs/adr
```

## Output Examples

### Proposed ADR (with Author's Notes)
```markdown
# ADR-0012: Use PostgreSQL for Data Persistence

## Status
Proposed

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

## Author's Notes
- **Shortcut**: Did not benchmark PostgreSQL vs CockroachDB under our expected write load; relied on team experience instead
- **Assumption**: Assumed read replicas will handle 5x current read traffic based on similar projects, not our actual query patterns
- **Uncertainty**: License compatibility of pgvector extension with our Apache 2.0 project not verified
```

### Accepted ADR (Author's Notes stripped)
```markdown
# ADR-0012: Use PostgreSQL for Data Persistence

## Status
Accepted

## Date
2026-01-10

(same content, but ## Author's Notes section removed entirely)
```

## Progressive Disclosure

- **Level 2**: [WORKFLOW.md](WORKFLOW.md) - Step-by-step methodology
- **Level 3**: [EXAMPLES.md](EXAMPLES.md) - Real-world ADR examples
- **Level 4**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Error handling

## Related Resources

- MADR 4.0 Template: https://adr.github.io/madr/
- ADR GitHub Organization: https://github.com/adr
