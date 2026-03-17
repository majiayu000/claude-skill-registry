---
name: granola-sync
description: |
  Syncs Granola meeting notes to Obsidian vault. Reads from Granola's local
  cache to extract meeting metadata and notes, then creates properly formatted
  markdown files with frontmatter. Also handles manual transcript formatting
  when cache doesn't have content.
allowed-tools: |
  bash: read granola cache
  file: read, write
---

# Granola Sync

<purpose>
Granola captures meeting transcripts and notes, but they live in the app.
This skill bridges Granola → Obsidian, creating searchable, linked meeting
notes that persist in your knowledge base. Works with both auto-sync from
local cache and manual paste when transcripts aren't cached locally.
</purpose>

## When To Activate

<triggers>
**Auto-sync from cache:**
- User says "sync granola" or "granola-sync"
- User asks to import meeting notes
- Beginning of session when reviewing recent meetings

**Manual formatting:**
- User pastes a meeting transcript
- User shares Granola export content
- User says "format this meeting" with pasted content
</triggers>

## Important Limitation

<limitation>
Granola stores most content **server-side only**. The local cache contains:
- Meeting metadata (title, date, attendees) for all meetings
- `notes_markdown` for only **some** meetings (user-edited notes)
- Transcripts are NOT stored locally

When local cache has no notes, ask user to copy from Granola app.
</limitation>

## Instructions

### Granola Cache Location

```
~/Library/Application Support/Granola/cache-v3.json
```

### Cache Structure

```json
{
  "cache": "{\"state\":{\"documents\":{...}}}"  // nested JSON string
}
```

Each document contains:
- `id` - unique meeting ID
- `title` - meeting title
- `notes_markdown` - notes content (often empty)
- `notes_plain` - plain text version
- `google_calendar_event.start.dateTime` - meeting time
- `google_calendar_event.attendees` - list with `email` fields

### Reading the Cache

<read_cache>
```bash
cat ~/Library/Application\ Support/Granola/cache-v3.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
cache=json.loads(d['cache'])
docs=cache['state']['documents']

# List meetings with notes
for doc in docs.values():
    md = doc.get('notes_markdown', '')
    if md and len(md) > 50:
        title = doc.get('title', 'Untitled')
        cal = doc.get('google_calendar_event') or {}
        start = cal.get('start') or {}
        dt = start.get('dateTime', '')[:10]
        print(f'{dt} | {title[:40]} | {len(md)} chars')
"
```
</read_cache>

### Output File Format

<file_format>
**Filename:** `YYYY-MM-DD-kebab-case-title.md`
**Location:** Project meetings folder (e.g., `Projects/project-name/meetings/`)

```markdown
---
type: meeting
project: <project-name>
status: active
date: YYYY-MM-DD
attendees:
  - name1
  - name2
source: granola
granola-id: <meeting-id>
tags:
  - meeting
---

# Meeting Title

**Date**: YYYY-MM-DD
**Attendees**: Name1, Name2

---

## Notes

<notes_markdown content>
```
</file_format>

### Manual Transcript Formatting

<manual_format>
When user pastes a transcript without cache data:

1. **Ask for metadata** if not obvious:
   - Meeting date
   - Attendees
   - Topic/title

2. **Structure the content:**

```markdown
---
type: meeting
project: <project>
status: active
date: YYYY-MM-DD
attendees:
  - name1
  - name2
source: granola-manual
tags:
  - meeting
---

# Topic Name

**Date**: YYYY-MM-DD
**Attendees**: Name1, Name2

---

## Summary

<2-3 sentence summary>

## Key Decisions

- Decision 1
- Decision 2

## Discussion Notes

<cleaned transcript, organized by topic>

## Action Items

- [ ] Action 1 (owner)
- [ ] Action 2 (owner)
```
</manual_format>

## Output Format

When syncing from cache:
```markdown
📥 **Granola Sync**

Found X meetings with notes:
- YYYY-MM-DD: Meeting Title (XXX chars)

Syncing to `Projects/project/meetings/`...

✓ Created: 2025-01-28-meeting-title.md
```

When no notes in cache:
```markdown
📥 **Granola Sync**

Found X meetings but none have local notes cached.
Paste transcript content and I'll format it.
```

## NEVER

- Sync meetings without notes content
- Overwrite existing meeting files without asking
- Include sensitive attendee details beyond names
- Create duplicate files for same meeting

## ALWAYS

- Use kebab-case lowercase filenames
- Add frontmatter with proper metadata
- Check for existing files before creating
- Ask which project folder to use if unclear
- Include granola-id to prevent duplicates
