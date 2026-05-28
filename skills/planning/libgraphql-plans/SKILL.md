---
name: libgraphql-plans
description: Track, organize, and maintain plans.md files and code TODOs for the libgraphql project. Use when the user asks to update plans, sync TODOs, mark tasks complete, add new tasks, identify high-impact work, or asks what's left to do in the libgraphql codebase. Triggers include phrases like "update plans", "sync TODOs", "what's left to do", "mark X as done", "track a new task", "highest-impact work", or references to plans.md files.
---

# libgraphql-plans

Manage project planning for the `libgraphql` workspace via `plans.md` files and code TODO comments.

## Overview

The libgraphql project tracks work in two ways:
1. **`plans.md` files** — Structured planning documents at crate roots and workspace root
2. **Code TODOs** — Inline comments marking work to be done

This skill keeps these synchronized and helps prioritize work.

## File Hierarchy

```
libgraphql/
├── plans.md                           # Workspace-level plans (items outside crates)
└── crates/
    ├── libgraphql-parser/plans.md     # Parser crate plans
    ├── libgraphql-core/plans.md       # Core crate plans
    └── libgraphql-macros/plans.md     # Macros crate plans
```

**Rule:** TODOs go to the nearest `plans.md` — if in a crate, use that crate's file; otherwise use the root.

## Workflows

### 1. Sync TODOs from Codebase

When asked to sync or update plans:

1. Run `.claude/skills/libgraphql-plans/scripts/scan_todos.py <repo-path>` to find all TODOs
2. For each `plans.md` file, compare found TODOs against the "Appendix: Code TODOs" table
3. **New TODOs:** Present them to the user for review before adding to the appropriate section
4. **Missing TODOs:** If a TODO in the appendix no longer exists in code, it may have been completed or removed — investigate and update accordingly
5. Regenerate the "Appendix: Code TODOs" table
6. Update "Last Updated" date

### 2. Mark Work Complete

When asked to mark something done:

1. Locate the plan item by section number (e.g., "2.1") or description
2. **Wholly complete:**
   - Move to "Past Completed Work" section with title, terse description, and date
   - Check all "Definition of Done" boxes
3. **Partially complete:**
   - Leave in place
   - Update "Current Progress" to reflect what's done
   - Update description to reflect remaining work
4. **NEVER re-number plan identifiers** — IDs like 2.1, 4.3 must remain stable
5. Update "Last Updated" date

### 3. Add New Task

When asked to track a new task:

1. Determine the appropriate `plans.md` file based on which crate it affects
2. Determine the appropriate section (or create a new section if needed)
3. Draft the new plan item following the format in `references/plans_format.md`
4. **Present to user for review before adding**
5. Assign the next available ID within that section (never reuse IDs)
6. Update "Last Updated" date

### 4. Identify High-Impact Work

When asked what to work on next:

1. First, sync TODOs and update all `plans.md` files
2. Analyze by priority markers (HIGH/MEDIUM/LOW) in the Priority Summary
3. Consider dependencies (blocked items vs ready items)
4. Consider scope (quick wins vs large efforts)
5. Present top 3-5 recommendations with rationale

## TODO Comment Patterns

Scan for these patterns in `.rs` files:

**Explicit markers:**
- `// TODO:` or `// TODO` — Standard TODO
- `// FIXME:` or `// FIXME` — Bug or broken code
- `// NOTE:` — May indicate future consideration. Exclude these if they only explain something but do not indicate a need to come back and change or otherwise take action on something.
- `// HACK:` — Temporary solution needing cleanup

**Semantic patterns** (use judgment):
- Comments mentioning "fix this", "clean up", "reconsider", "revisit"
- Comments about "temporary", "workaround", "should be changed"
- Comments with future tense about changes ("will need to", "should eventually")

Not every comment needs to become a plan item — only clear action items.

## plans.md Format

See `references/plans_format.md` for the full template.

General style:
- All markdown table cells in a column should have consistent width for
  human-readability

Key sections:
- **Current State Summary** — Test counts, implementation status
- **Numbered Sections** — Grouped by category (Testing, Performance, etc.)
- **Priority Summary** — HIGH/MEDIUM/LOW categorization
- **Past Completed Work** — Archive of finished items
- **Appendix: Code TODOs** — Auto-generated table of inline TODOs

Each plan item includes:
- **Purpose** — Why this matters
- **Current Progress** — What's done
- **Priority** — HIGH/MEDIUM/LOW
- **Tasks** — Numbered subtasks
- **Definition of Done** — Checkboxes for completion criteria

## Important Rules

1. **Stable IDs:** Never renumber plan items. If Section 2.1 is completed, the next item in Section 2 is 2.7 (or whatever follows), not 2.1.

2. **Always regenerate Code TODOs appendix** when updating any `plans.md`.

3. **Ask before adding:** New items from TODO scans should be presented for user review.

4. **Update timestamps:** Always update "Last Updated" date when modifying a `plans.md`.

5. **Terse completions:** When moving to "Past Completed Work", use only a title and one-line description.
