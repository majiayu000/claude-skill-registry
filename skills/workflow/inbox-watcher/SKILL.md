---
name: inbox-watcher
context: fork
description: Check for unprocessed files and suggest appropriate skills to handle them
model: haiku
---

# /inbox-watcher

Monitor for unprocessed files in the vault and suggest the appropriate skill to handle each.

## Usage

```
/inbox-watcher              # Check and classify all unprocessed files
/inbox-watcher --process    # Check and auto-process with suggested skills
```

## Instructions

### 1. Check for Unprocessed Inbox Items

```bash
npm run inbox:check 2>/dev/null
```

If no inbox script output, fall back to scanning common drop locations:

```bash
# Check for files that may need processing
ls -t voicenotes/*.md 2>/dev/null | head -10
ls -t Attachments/*.pdf Attachments/*.pptx 2>/dev/null | head -10
```

### 2. Check for Untyped Notes

Find markdown files that lack a `type` field in frontmatter (potential unprocessed content):

```bash
node .claude/scripts/graph-query.js --where="type=" --json 2>/dev/null
```

If graph-query.js does not support querying for empty/null type, use a Grep fallback:
```bash
# Find notes without a type field in frontmatter
find . -name "*.md" -not -path "./.claude/*" -not -path "./.obsidian/*" -not -path "./node_modules/*" -not -path "./Templates/*" -not -path "./Archive/*" | while read f; do
  if \! head -20 "$f" | grep -q "^type:"; then echo "$f"; fi
done
```

### 3. Classify and Recommend

For each unprocessed file, suggest the appropriate skill:

| File Pattern | Suggested Skill | Rationale |
|-------------|----------------|-----------|
| `voicenotes/*.md` | `/meeting` or `/daily` | Voice transcriptions → meeting notes or daily entries |
| `Attachments/*.pdf` | `/pdf-to-page` | PDFs → structured page notes |
| `Attachments/*.pptx` | `/pptx-to-page` | PowerPoints → page notes with slide images |
| `*.csv` in root | `/csv-to-page` or `/csv-to-sql` | Data files → markdown tables or SQLite |
| Untyped `.md` at root | `/incubator` or manual triage | Loose notes need classification |
| `Email - *.md` without type | `/email` | Email drafts needing frontmatter |

### 4. Present Report

```markdown
## Inbox Report — YYYY-MM-DD

### Unprocessed Files (N found)

| # | File | Type | Suggested Action |
|---|------|------|-----------------|
| 1 | voicenotes/2026-02-13... | Voice note | `/meeting` — transcribe to meeting note |
| 2 | Attachments/report.pdf | PDF | `/pdf-to-page` — extract to page |

### Quick Actions
- Process all: `/inbox-watcher --process`
- Process one: Run the suggested skill command
```

### 5. Auto-Process (--process flag)

If `--process` flag is set, run `npm run inbox:process` and then invoke the suggested skill for each file sequentially, confirming with the user before each.

## Guidelines

- Read-only by default — only process files when `--process` is explicitly requested
- Always confirm before processing — show what will happen first
- Skip files in `Archive/`, `Templates/`, and `.claude/`
- Voice notes are the most common inbox item — prioritise these
