---
name: memory-sanitize
description: Produce share-safe copies of memory files under /tmp with PII redacted (paths, emails, session IDs, dates) and credentials scanned (tokens, keys); never mutates originals. Use when the user says "sanitize memory for sharing", "redact memory PII", or "scan memory for credentials".
---

Redact PII and scan for credentials in memory files — write copies to `/tmp`, never touch originals.

## Scope

Memory-dir-only. Does not read session histories. Structural audit (orphans, duplicates) belongs in `memory-clean`; run that first if the directory is messy. This skill is a best-effort redactor, not a formal DLP tool — the user is the final reviewer.

## Path resolution

```sh
SKILL_SCRIPTS="${MEMORY_SANITIZE_SKILL_SCRIPTS:-$HOME/.claude/claude/skills/memory-sanitize/scripts}"
MEMORY_DIR=$("$SKILL_SCRIPTS/resolve-paths.sh" memory_dir)
```

`SESSION_HISTORY_GLOB` is not used by this skill. Abort on non-zero exit. Override `MEMORY_SANITIZE_SKILL_SCRIPTS` if installed outside `$HOME/.claude`.

## Workflow

### 1. Resolve memory dir (above)

### 2. Run sanitizer

```sh
DST="/tmp/memory-sanitized-$(date +%s)"
"$SKILL_SCRIPTS/sanitize-memory.sh" "$MEMORY_DIR" "$DST"
```

The script writes redacted copies under `$DST/` and emits a JSON report to stdout:

```json
{
  "files": [
    { "source": "feedback_foo.md", "redactions": 3, "credentials": 0 },
    { "source": "MEMORY.md",       "redactions": 1, "credentials": 1 }
  ],
  "total_redactions": 4,
  "total_credentials": 1
}
```

Read `references/REDACTION-RULES.md` for the full pattern table and severity tiers.

### 3. Show diff and credential hits

```sh
difft "$MEMORY_DIR" "$DST"
```

For each file with credential hits, show the specific line(s) with the hit pattern highlighted. **If any credential remains in the source originals (zero redaction applied despite a credential pattern match), abort with a critical warning** and recommend the user manually remediate the original before sharing.

### 4. Present to user

Render:

```
Sanitized N files → $DST
  N redactions applied (paths, emails, session IDs, dates)
  N credential hits (see above)

Original files are unchanged. Review the diff before sharing.
```

Wait for user acknowledgement before exiting.

## Boundary fences

- Read-only on originals. Writes only to `/tmp/memory-sanitized-<ts>/`.
- Does not update `MEMORY.md` in the originals — sanitized copies are not a replacement.
- Does not read session histories.
- Security limitation: pattern-based scanning misses novel or obfuscated formats — the user is the final reviewer before sharing.
