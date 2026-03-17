---
name: plan-manager
description: Manage plans and context documents with automatic indexing
---

# Plan Manager Skill

Manage workflow plans and context documents with automatic file tracking and indexing.

## Commands

### Create Plan

Creates a new plan document with timestamp-based naming.

**Usage**: `create-plan <title> --workflow <name>`

**Example**:
```
create-plan "Add contact form" --workflow tdd
```

**Creates**: `.claude/plans/active/YYYY-MM-DD--add-contact-form.md`

### Update Step

Updates the status of a specific step in an active plan.

**Usage**: `update-step <plan-slug> <step-number> <status>`

**Status options**: `pending`, `in_progress`, `completed`, `blocked`

**Example**:
```
update-step add-contact-form 1 in_progress
```

### Create Context

Creates a new context document for a codebase area.

**Usage**: `create-context <title> --areas <area1,area2>`

**Example**:
```
create-context "Authentication" --areas auth,security,api
```

**Creates**: `.claude/context/auth--context.md`

### Update Indexes

Regenerates all index files from current markdown files.

**Usage**: `update-indexes`

**Updates**:
- `.claude/indexes/_plans.md`
- `.claude/indexes/_context.md`
- `.claude/indexes/_workflows.md`

### Archive Plan

Moves a completed plan to the archive directory.

**Usage**: `archive-plan <plan-slug>`

**Example**:
```
archive-plan add-contact-form
```

**Moves**: `.claude/plans/active/` → `.claude/plans/archive/`

### List Active

Lists all active plans with their current status.

**Usage**: `list-active` or `list-plans`

## File Naming Conventions

### Plans
- Format: `YYYY-MM-DD--[slug].md`
- Location: `.claude/plans/active/` (or `/archive/` when completed)
- Slug derivation: lowercase, hyphen-separated words

### Context
- Format: `[area]--context.md`
- Location: `.claude/context/`
- Example: `auth--context.md`, `routing--context.md`

### Indexes
- Format: `_<type>.md`
- Location: `.claude/indexes/`
- Auto-generated, never manually edited

## Workflow Integration

When using any workflow (TDD, UI-iteration, Bug-fix), the plan manager automatically:

1. **Plan Phase**: Creates a plan document if the task is complex
2. **Execution**: Updates step statuses as you progress
3. **Completion**: Marks the plan as completed and archives it
4. **Context**: Creates or updates context documents for areas explored

## Token Efficiency Guidelines

Context documents should reference source files rather than duplicate content:

**DO**:
```markdown
## Source Files
- [src/lib/auth.ts](src/lib/auth.ts) - JWT utilities
- [src/middleware.ts](src/middleware.ts) - Route protection
```

**DON'T**:
```markdown
## Source Files
src/lib/auth.ts contains:
```typescript
export function jwtSign(payload) { ... }
```
```

## Frontmatter Schema

### Plan Document
```yaml
---
created: 2025-01-10
started: null        # null if still in planning phase
updated: 2025-01-10  # null if never updated
completed: null      # null until done
status: planning|in_progress|blocked|completed|archived
workflow: tdd|ui-iteration|bug-fix
related_context:
  - auth--context.md
priority: p1|p2|p3   # P1=Critical, P2=Important, P3=Nice-to-Have
quality_gates_passed: false  # Set to true when all quality gates pass
scrutiny:            # Added after plan scrutiny (Step 3.5)
  p1_findings: 0
  p2_findings: 0
  p3_findings: 0
  confidence_score: 95
---
```

**Severity Classification (P1/P2/P3):**

See the `quality-severity` skill for detailed classification guidelines:

- **P1 (Critical)**: Blocks implementation - must be addressed before proceeding
  - Security vulnerabilities
  - Data corruption risks
  - Breaking changes
  - Missing critical context

- **P2 (Important)**: Should address - significant issues that impact quality
  - Performance concerns
  - Architectural issues
  - Code clarity problems
  - Missing edge cases

- **P3 (Nice-to-Have)**: Consider addressing - improvements and optimizations
  - Code cleanup
  - Minor optimizations
  - Documentation improvements
  - Style consistency

### Context Document
```yaml
---
created: 2025-01-10
updated: null              # null if never updated
areas:
  - auth
  - security
related_plans:
  - 2025-01-10--add-contact-form.md
---
```

## Implementation Notes

- The `update-indexes` command is a shell script: `.claude/bin/update-indexes.sh`
- Indexes are sorted by last modified time (newest first)
- Status is extracted from frontmatter `status:` field
- Description comes from frontmatter `description:` field or first heading
