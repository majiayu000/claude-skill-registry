---
name: agent-ops-housekeeping
description: "Comprehensive project hygiene: archive issues, validate schema, clean clutter, align docs, check git, update ignores."
category: state
invokes: [agent-ops-state, agent-ops-docs, agent-ops-tasks]
invoked_by: []
state_files:
  read: [issues/index.md, issues/*.md, focus.md, memory.md]
  write: [issues/index.md, issues/*.md, focus.md]
reference: [REFERENCE.md]
---

# Housekeeping

Keep the project clean, organized, and maintainable.

**Reference**: See [REFERENCE.md](REFERENCE.md) for detailed procedures, CLI commands, gitignore checklist.

---

## Core Tasks (Always Run)

1. **Archive completed issues** → history.md
2. **Regenerate index.md** → compact issue summary
3. **Validate issue schema** → fix malformed issues
4. **Clean clutter** → remove temp files, fix ignores

---

## Issue Archival ⚡ (Auto-Run)

**Runs automatically by default.** Use `--dry-run` to preview.

**Procedure:**
1. Scan ALL issue files including splits (`*.md`, `*-*.md`)
2. Find issues with status: `done`, `cancelled`, `dropped`, `wont-fix`
3. Append to `history.md` under `## Archived [YYYY-MM-DD]`
4. Remove from source file
5. If history.md > 500 lines, rotate to `archives/history-YYYYMMDD.md`
6. Check if split files can be compacted

---

## Hygiene Checks

### 1. Issue File Management
- **Split** files > 100K into numbered files
- **Compact** split files when combined < 80K
- Keep OLDEST in numbered files, NEWEST in main

### 2. Backlog Triage
Prompt to prioritize items with `status: needs_triage` or > 2 weeks old.

### 3. Schema Validation
Validate against `.github/reference/issue-schema.json`:
- Required: `id`, `type`, `priority`, `title`, `status`
- ID format: `{TYPE}-{NNNN}@{HHHHHH}`
- Auto-fix: missing status, wrong priority file

### 4. Clutter Detection
Find generated/stale markdown outside `.agent/docs/`.

### 5. README Alignment
Check if README reflects actual project state.

### 6. Git Health
- Uncommitted changes count
- Untracked files
- Stale branches (30+ days)
- Large uncommitted files

### 7. Gitignore Audit
Check for missing ignores: node_modules, .venv, dist, build, .env

### 8. State File Health
- Required files exist
- Valid YAML frontmatter
- No orphaned references

---

## Invocation

```bash
/agent-housekeeping           # Full sweep (archives automatically)
/agent-housekeeping --dry-run # Preview only
/agent-housekeeping --fix     # Auto-fix safe issues
/agent-housekeeping issues    # Just archival
/agent-housekeeping git       # Just git health
```

---

## When to Run

- After completing milestone/feature
- Before starting new major work
- Weekly maintenance
- When context feels cluttered
- Before handoff
