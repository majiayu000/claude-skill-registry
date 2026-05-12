<!-- SOURCE-OF-TRUTH: shared/references/numbering_conventions.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Numbering Conventions

Unified rules for Epic, Story, and Task numbering across the workflow.

## Epic Numbering

### Initiative-Internal Index vs Linear Number

| Concept | Description | Example |
|---------|-------------|---------|
| **Initiative Index** | Internal ordering (0-N) | Epic 0, Epic 1, Epic 2 |
| **Linear Number** | Global sequential number | Epic 11, Epic 12, Epic 13 |

### Epic 0 Reserved

**Rule:** Epic 0 is reserved for Infrastructure within an initiative.

```
Initiative "E-Commerce Platform":
  Epic 0: Infrastructure & Operations (Index 0 → Linear "Epic 11")
  Epic 1: User Management (Index 1 → Linear "Epic 12")
  Epic 2: Product Catalog (Index 2 → Linear "Epic 13")
```

### When to Use Epic 0

| Condition | Use Epic 0? |
|-----------|-------------|
| New project (no infrastructure docs) | ✅ Yes |
| Multi-stack (Frontend + Backend) | ✅ Yes |
| Needs CI/CD, monitoring, security | ✅ Yes |
| Existing project with infra | ❌ No |
| Simple feature addition | ❌ No |

### Epic 0 Content Template

When creating Infrastructure Epic, use this template:

| Field | Value |
|-------|-------|
| **Goal** | Establish foundational infrastructure, deployment pipeline, operational capabilities |
| **Scope** | Logging, error handling, monitoring, CI/CD, security baseline, performance |

**Multi-stack projects:** Each Story doubles (Frontend Story + Backend Story for same functionality)

## Story Numbering

### Format: US{NNN}

Stories numbered **sequentially across ALL Epics** (not per-Epic).

```
Epic 11 (Infrastructure):
  US001: Setup CI/CD pipeline
  US002: Configure logging
  US003: Setup monitoring

Epic 12 (User Management):
  US004: User registration      ← Continues from US003
  US005: User login
  US006: Password reset
```

### No Story 0

**Rule:** Stories start from US001. No reserved Story 0.

**Rationale:** Epic 0 groups infrastructure Stories (US001-US010), not a single "Story 0".

## Task Numbering

### Format: T{NNN}

Tasks numbered **per Story** (reset for each Story).

```
Story US004:
  T001: Create Users table
  T002: Implement UserService
  T003: Create API endpoints

Story US005:
  T001: Create Sessions table    ← Resets to T001
  T002: Implement AuthService
```

## Reading Next Numbers

**Source:** `docs/tasks/kanban_board.md`

```markdown
## Linear Configuration

| Setting | Value |
|---------|-------|
| Team ID | abc123 |
| Next Epic Number | 14 |

## Epic Story Counters

| Epic | Last Story | Next Story | Last Task | Next Task |
|------|------------|------------|-----------|-----------|
| Epic 11 | US003 | US004 | T002 | T003 |
| Epic 12 | US006 | US007 | T003 | T004 |
```

## Update Rules

| After Creating | Update |
|----------------|--------|
| Epic | Increment Next Epic Number |
| Story | Update Epic's Next Story in counters |
| Task | Update Story's Next Task in counters |

## Usage in SKILL.md

```markdown
## Numbering

See `references/numbering_conventions.md` for:
- Epic 0 reservation rules
- Story sequential numbering
- Task per-Story numbering
- Kanban counter updates
```

---
**Version:** 1.0.0
**Last Updated:** 2026-02-05
