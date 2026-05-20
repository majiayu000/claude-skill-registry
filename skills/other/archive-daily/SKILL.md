---
name: archive-daily
description: Archive Today.md content to Periodic/Daily/. Handles the metabolic transition from Captive (volatile) to Periodic (permanent record).
disable-model-invocation: true
allowed-tools: Read, Write, Bash
---

# Archive Daily Sub-Skill

Archives a day's content from Captive to Periodic/Daily/, transforming it into the archive format.

## Input Arguments

Arguments are passed as key-value pairs:
- `vault`: Path to the vault
- `date`: Target date in YYYY-MM-DD format
- `content`: Full markdown content to archive (already transformed by the review skill)

## Instructions

### 1. Validate Paths

Verify required directories exist:

```bash
ls -d "$VAULT/00_Brain/Periodic/Daily/"
```

If missing, create it:
```bash
mkdir -p "$VAULT/00_Brain/Periodic/Daily/"
```

### 2. Check for Existing Archive

Check if `$VAULT/00_Brain/Periodic/Daily/{date}.md` already exists:

```bash
ls "$VAULT/00_Brain/Periodic/Daily/{date}.md" 2>/dev/null
```

**If exists:**
- Read existing content
- Compare with new content
- If different: Return error prompting user decision (overwrite/merge/cancel)
- If same: Return success with note "Already archived"

### 3. Write Archive

Write the content to `$VAULT/00_Brain/Periodic/Daily/{date}.md`

### 4. Verify Write

Read back the file to confirm write succeeded.

### 5. Update Today.md (Optional)

If the archive was successful and Today.md was the source:
- Replace Today.md with a minimal placeholder indicating it was archived

**Placeholder content:**
```markdown
---
archived: {date}
---

# Archived

This day has been archived to [[00_Brain/Periodic/Daily/{date}]].

Run `/daily-planning` to start a new day.
```

## Output

Return structured JSON:

**Success:**
```json
{
  "success": true,
  "archive_path": "/Users/.../00_Brain/Periodic/Daily/2026-02-14.md",
  "bytes_written": 4096,
  "today_cleared": true
}
```

**Already exists (same content):**
```json
{
  "success": true,
  "archive_path": "/Users/.../00_Brain/Periodic/Daily/2026-02-14.md",
  "already_existed": true,
  "message": "Archive already exists with matching content."
}
```

**Already exists (different content):**
```json
{
  "success": false,
  "error": "archive_conflict",
  "archive_path": "/Users/.../00_Brain/Periodic/Daily/2026-02-14.md",
  "message": "Archive already exists with different content.",
  "suggestion": "Review existing archive or confirm overwrite."
}
```

**Error:**
```json
{
  "success": false,
  "error": "write_failed",
  "message": "Failed to write archive: {system_error}"
}
```

## Error Cases

| Condition | Error Message |
|-----------|---------------|
| Vault not found | "Vault directory does not exist: {vault}" |
| Cannot create directory | "Failed to create Periodic/Daily directory" |
| Archive conflict | "Archive already exists with different content" |
| Write failed | "Failed to write archive: {system_error}" |
| Verification failed | "Write verification failed: content mismatch" |

## Safety

- Always check for existing archive before writing
- Never overwrite without explicit user confirmation
- Archive is write-only to Periodic/Daily/ (never to other directories)
- Today.md placeholder preserves a link to the archive
