---
name: memory-clean
description: Audit memory directory for structural issues (orphans, dangling refs, duplicates, missing sections, oversized entries) and staleness against session-history transcripts; report-first, fix-on-confirmation. Use when the user says "audit memory", "memory hygiene", or "find stale/duplicate memories".
---

Audit memory for structural rot and staleness, report with evidence, fix only on user confirmation.

## Scope

Audits and fixes existing memory files. Does not create new memories from session signals (that is `memory-update`). Does not redact PII or credentials (that is `memory-sanitize`, which `memory-clean` will recommend when it detects suspected credentials at critical severity).

## Path resolution

Scripts live under this skill's own `scripts/` directory. Resolve the skill root from `$HOME` (the conventional install path is `$HOME/.claude/claude/skills/memory-clean/`):

```sh
SKILL_SCRIPTS="${MEMORY_CLEAN_SKILL_SCRIPTS:-$HOME/.claude/claude/skills/memory-clean/scripts}"
MEMORY_DIR=$("$SKILL_SCRIPTS/resolve-paths.sh" memory_dir)
SESSION_HISTORY_GLOB=$("$SKILL_SCRIPTS/resolve-paths.sh" session_history_glob)
```

Set `MEMORY_CLEAN_SKILL_SCRIPTS` to override when the skill is installed outside `$HOME/.claude`. Abort on non-zero exit from the resolver. Overrides via `MEMORY_DIR` / `SESSION_HISTORY_GLOB` env vars.

## Workflow

### 1. Resolve paths (above)

### 2. Snapshot before any fix

```sh
cp -r "$MEMORY_DIR" /tmp/memory-snapshot-$(date +%s)
```

Never mutate originals without a snapshot.

### 3. Run structural audit

```sh
./scripts/audit-memory.sh "$MEMORY_DIR" "$SESSION_HISTORY_GLOB" > /tmp/memory-audit-$(date +%s).json
```

The script emits JSON with these arrays:

| Field | What it detects |
|---|---|
| `orphans` | Files in dir with no MEMORY.md entry |
| `dangling` | MEMORY.md entries pointing to missing files |
| `near_duplicates` | File pairs with >70% content overlap |
| `structural` | Missing frontmatter, missing **Why:**/**How to apply:**, index line > 150 chars, MEMORY.md > 200 lines, type-mismatch, fix-recipe content |
| `staleness` | Memories whose stated rule conflicts with recent session evidence |

Read `references/AUDIT-CHECKLIST.md` for full detection rules per category.

### 4. Render report grouped by severity

```
CRITICAL (N)
  [cred-scan] feedback_no-html-comments.md — suspected credential on line 7
  → Recommend: run memory-sanitize first

WARN (N)
  [near-dup] feedback_consistent-config.md ↔ feedback_no-html-comments.md (82% overlap)
  [stale] feedback_bump-minor-versions.md — rule contradicted in 4 recent sessions
    Evidence: turns uuid-aaa, uuid-bbb, uuid-ccc, uuid-ddd

INFO (N)
  [orphan] user_role_data_scientist.md — not in MEMORY.md index
  [index-long] project_auth-rewrite.md — index entry is 163 chars (limit 150)
```

For staleness items, always show the specific turn IDs and a snippet of the contradicting evidence.

### 5. Wait for confirmation per group

Present each fix group with a diff preview. Wait for explicit user confirmation before applying. Never auto-fix.

### 6. Apply confirmed fixes

- Orphan: append entry to MEMORY.md.
- Dangling: remove line from MEMORY.md.
- Near-duplicate: present merged draft; write merged file + remove the superseded one; update MEMORY.md.
- Structural: targeted in-place edit via `Edit` tool.
- Stale: present options — update the rule, archive the file, or delete it.

### 7. Re-run audit; confirm zero critical issues

```sh
./scripts/audit-memory.sh "$MEMORY_DIR" "$SESSION_HISTORY_GLOB"
```

Report residual warn/info items; leave them for the user to act on separately if desired.

## Anti-patterns (never do)

- Auto-fix without user confirmation.
- Mutate originals without the `/tmp/` snapshot.
- Delete a file without showing the user its content first.
- Attempt credential redaction (surface critical flag, recommend `memory-sanitize`).
