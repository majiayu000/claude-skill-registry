---
name: archive-weekly
description: Archive Week.md content to Periodic/Weekly/. Handles the metabolic transition from Captive (volatile) to Periodic (permanent record).
disable-model-invocation: true
allowed-tools: Read, Write, Bash
---

# Archive Weekly Sub-Skill

Archives a week's content from Captive to Periodic/Weekly/, transforming it into the archive format.

## Input Arguments

Arguments are passed as key-value pairs:
- `vault`: Path to the vault
- `week`: Target week in YYYY-Www format
- `content`: Synthesis content from the interactive review (theme, accomplishments, patterns)
- `daily_links`: Formatted wikilinks to daily archives

## Instructions

### 1. Validate Paths

Verify required directories exist:

```bash
ls -d "$VAULT/00_Brain/Periodic/Weekly/" 2>/dev/null
```

If missing, create it:
```bash
mkdir -p "$VAULT/00_Brain/Periodic/Weekly/"
```

### 2. Check for Existing Archive

Check if `$VAULT/00_Brain/Periodic/Weekly/{week}.md` already exists:

```bash
ls "$VAULT/00_Brain/Periodic/Weekly/{week}.md" 2>/dev/null
```

**If exists:**
- Read existing content
- Compare with new content
- If different: Return error prompting user decision (overwrite/merge/cancel)
- If same: Return success with note "Already archived"

### 3. Read Week.md

Read the current Week.md content from `$VAULT/00_Brain/Captive/Week.md`

### 4. Read Archive Template

Read the archive template from `$VAULT/00_Brain/Systemic/Templates/Periodic/weekly.md`

### 5. Transform Content

Using the template structure, build the archive:

**Frontmatter:**
```yaml
---
week: {from Week.md}
dates: {from Week.md}
month: {from Week.md}
quarter: {from Week.md}
year: {from Week.md}
archived: {today's date YYYY-MM-DD}
---
```

**Navigation:**
Update links to point to Periodic archives (not Captive):
```markdown
[[00_Brain/✱ Home|✱ Home]] | [[00_Brain/Periodic/Monthly/{month}|Month]] | [[00_Brain/Periodic/Quarterly/{quarter}|Quarter]]
```

**Header:**
```markdown
# Week {week}

*Archived from Captive/Week.md on {archived date}*
```

**Week Overview Section:**
Preserve from Week.md:
- Key Outcomes
- Focus Theme

**Daily Summary Section:**
Insert the `daily_links` formatted content:
```markdown
## Daily Summary

### Days This Week
{daily_links}
```

**Wins This Week Section:**
Preserve from Week.md:
- Personal wins
- Organisational wins
- Strategic wins

**Reflections Section:**
Preserve from Week.md:
- What Went Well
- What Could Be Better
- Key Learning
- Patterns Observed

**Synthesis Section:**
Add new content from interactive review:
```markdown
## Synthesis

*Added during weekly review ritual*

### Week Theme
{content.theme}

### Key Accomplishments
{content.accomplishments}

### Patterns Observed
{content.patterns}

### Next Week Setup
{content.next_week}
```

### 6. Write Archive

Write the transformed content to `$VAULT/00_Brain/Periodic/Weekly/{week}.md`

### 7. Verify Write

Read back the file to confirm write succeeded:
- Check file exists
- Check content length matches expected

### 8. Update Week.md

Replace Week.md with a minimal placeholder indicating it was archived:

```markdown
---
archived: {week}
---

[[00_Brain/✱ Home|✱ Home]] | [[00_Brain/Captive/Today|Today]] | [[00_Brain/Captive/Month|Month]]

---

# Archived

This week has been archived to [[00_Brain/Periodic/Weekly/{week}]].

Run `/weekly-planning` to start a new week.
```

## Output

Return structured JSON:

**Success:**
```json
{
  "success": true,
  "archive_path": "/Users/.../00_Brain/Periodic/Weekly/2026-W07.md",
  "bytes_written": 8192,
  "week_cleared": true,
  "daily_archives_linked": 5
}
```

**Already exists (same content):**
```json
{
  "success": true,
  "archive_path": "/Users/.../00_Brain/Periodic/Weekly/2026-W07.md",
  "already_existed": true,
  "message": "Archive already exists with matching content."
}
```

**Already exists (different content):**
```json
{
  "success": false,
  "error": "archive_conflict",
  "archive_path": "/Users/.../00_Brain/Periodic/Weekly/2026-W07.md",
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

For backwards compatibility, also output human-readable summary:
```
Week Archived Successfully

Archive: 00_Brain/Periodic/Weekly/2026-W07.md (8192 bytes)
Daily Links: 5 days linked
Week.md: Cleared with archived placeholder

Link: [[00_Brain/Periodic/Weekly/2026-W07]]
```

## Error Cases

| Condition | Error Message |
|-----------|---------------|
| Vault not found | "Vault directory does not exist: {vault}" |
| Cannot create directory | "Failed to create Periodic/Weekly directory" |
| Week.md not found | "Week.md not found—nothing to archive" |
| Archive conflict | "Archive already exists with different content" |
| Write failed | "Failed to write archive: {system_error}" |
| Verification failed | "Write verification failed: content mismatch" |

## Safety

- Always check for existing archive before writing
- Never overwrite without explicit user confirmation
- Archive is write-only to Periodic/Weekly/ (never to other directories)
- Week.md placeholder preserves a link to the archive
- Original Week.md content is fully captured in the archive before clearing
