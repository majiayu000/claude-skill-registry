---
name: todo
description: TODO tracking system for spec TODOs. Use when creating, updating, or querying spec TODOs in docs/spec/todos/.
---

# TODO Tracking System

Spec TODOs live in `docs/spec/todos/` as individual markdown files with YAML frontmatter.

## Finding TODOs

- **Index:** `docs/spec/todos/index.md` — Single table sorted by ID with status, priority, and dates
- **Individual files:** `docs/spec/todos/TODO-NNNN.md` (zero-padded to 4 digits)
- **Quick lookup:** `glob docs/spec/todos/TODO-*.md`

## Creating a New TODO

1. **Derive next ID:** Find the highest existing ID and add 1 (do NOT fill gaps — IDs are never reused)
2. **Create file** using this template:

```yaml
---
id: <next_id>
title: <short title>
status: todo              # todo | in-progress | done
priority: high            # high | medium | low
created: <YYYY-MM-DD>
depends_on: []            # list of TODO IDs that must complete first
blocks: []                # list of TODO IDs this blocks
---
```

```markdown
# TODO-NNNN: <Title>

## Summary
<1-3 sentences describing the goal>

## Details
<Full description: steps, design questions, files to create/update>
```

3. **Update `index.md`:** Add row to the table (sorted by ID)

## Updating Status

### Starting work (`todo` → `in-progress`)
- Update frontmatter: `status: in-progress`
- Update index.md if needed

### Completing (`in-progress` → `done`)
1. Update frontmatter:
   ```yaml
   status: done
   completed: <YYYY-MM-DD>
   files_created: [...]    # files created during resolution
   files_updated: [...]    # files modified during resolution
   ```
2. Replace `## Details` with `## Resolution` containing the resolution notes
3. Update index.md: change status, add completed date

### Subsumption (absorbed by another TODO)
When a TODO is fully covered by another TODO's implementation:
1. On the **subsumed** TODO:
   ```yaml
   status: done
   completed: <date of subsuming TODO's completion>
   subsumed_by: <subsuming TODO ID>
   ```
2. Rename `## Details` to `## Original Scope`, add:
   ```markdown
   ## Resolution
   Subsumed by [TODO-NNNN](TODO-NNNN.md). <brief explanation>.
   ```
3. On the **subsuming** TODO, add:
   ```yaml
   subsumed:
     - <absorbed TODO ID>
   ```

## Dependency Conventions

- `depends_on: [8]` means "cannot start until #8 is done"
- `blocks: [9]` means "#9 cannot start until this is done"
- Keep both sides consistent (if A blocks B, then B depends_on A)

## File Impact Conventions

Only populated on completion:
- `files_created`: New files created as part of the resolution
- `files_updated`: Existing files modified as part of the resolution
- Use spec-relative paths (e.g., `commands/check.md`, `workflows/inference.md`)

## Relative Links

TODO files live at `docs/spec/todos/`. Adjust relative links accordingly:
- To spec files: `../terminology.md`, `../storage.md`, `../commands/check.md`, `../workflows/inference.md`
- To other TODOs: `TODO-NNNN.md` (same directory)