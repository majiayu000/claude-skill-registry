---
name: academics
description: Track assignments, due dates, grades, and study notes from Canvas LMS (iCal feed) and GoodNotes exports.
user-invocable: true
argument-hint: "<due|events|courses|notes|study> [args]"
context: fork
agent: researcher
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - mcp__vault__vault_search
  - mcp__vault__vault_read
---

# Academic Tracker — Canvas iCal + GoodNotes

Canvas iCal feed (assignments, quizzes, events across all courses):
!command curl -s "$CANVAS_ICAL_URL" 2>/dev/null | grep -c "BEGIN:VEVENT" | xargs -I{} echo "{} upcoming events in Canvas feed"

Recent GoodNotes exports:
!command ls -lt ~/Documents/GoodNotes-Export/*.pdf 2>/dev/null | head -5 || echo "No PDFs found"

## Canvas Commands

Canvas data comes from the iCal feed at `$CANVAS_ICAL_URL`. Parse the `.ics` format to extract events.

### `due` — Upcoming assignments and events
Fetch the iCal feed and show events due in the next 7 days:
```bash
curl -s "$CANVAS_ICAL_URL" | python3 -c "
import sys, re
from datetime import datetime, timedelta, timezone

data = sys.stdin.read()
now = datetime.now(timezone.utc)
window = now + timedelta(days=7)
events = data.split('BEGIN:VEVENT')
for ev in events[1:]:
    summary = re.search(r'SUMMARY:(.*)', ev)
    dtstart = re.search(r'DTSTART[^:]*:(.*)', ev)
    desc = re.search(r'DESCRIPTION:(.*)', ev)
    if summary and dtstart:
        name = summary.group(1).strip()
        try:
            dt = datetime.strptime(dtstart.group(1).strip()[:15], '%Y%m%dT%H%M%S').replace(tzinfo=timezone.utc)
            if now <= dt <= window:
                print(f'  {dt.strftime(\"%a %b %d %I:%M %p\")} — {name}')
        except ValueError:
            pass
"
```
Sort by date. If nothing is due, say so. Note: not all teachers post assignments to Canvas, so this may not capture everything.

### `events` — All upcoming events
Same as `due` but with a 30-day window. Includes lectures, office hours, and any calendar items professors have added.

### `courses` — List courses in the feed
Parse the iCal feed for unique course names:
```bash
curl -s "$CANVAS_ICAL_URL" | grep -oP '(?<=\[)[^\]]+' | sort -u
```
Course names appear in brackets in event summaries (e.g., `[CS 4310] Homework 3`).

## GoodNotes Commands

GoodNotes folders:
- **Auto-backup**: `~/Library/CloudStorage/GoogleDrive-$GOOGLE_DRIVE_ACCOUNT/My Drive/GoodNotes/`
- **Manual exports**: `~/Documents/GoodNotes-Export/`

### `notes list` — List exported PDFs
```bash
ls -ltR ~/Library/CloudStorage/GoogleDrive-$GOOGLE_DRIVE_ACCOUNT/My\ Drive/GoodNotes\ 6/*.pdf ~/Documents/GoodNotes-Export/*.pdf 2>/dev/null | head -20
```

### `notes read <filename>` — Read a PDF
Use the Read tool to read the PDF file. Claude can read PDFs natively.
```
Read ~/Documents/GoodNotes-Export/<filename>
```

### `notes search <query>` — Search across notes
Search PDF filenames for the query term:
```bash
ls ~/Documents/GoodNotes-Export/ | grep -i "<query>"
```

### `study <topic>` — Generate study material from ingested notes

The vault contains structured course notes at `vault/shared/course-notes/`. Each subdirectory is a course:

| Directory | Course |
|-----------|--------|
| `numerical-methods/` | Numerical Methods |
| `philosophy/` | Intro to Philosophy |
| `systems-programming/` | Systems Programming (CS 2600) |
| `comp-society/` | Computers and Society |

**Steps:**
1. Identify which course the topic belongs to (or search all if ambiguous)
2. Use Grep to search vault course notes for the topic:
   ```bash
   grep -ril "<topic>" vault/shared/course-notes/
   ```
3. Read the most relevant note files (up to 5) — these are already structured markdown with concepts, definitions, and examples extracted from lecture notes
4. Check Canvas feed for related upcoming events/deadlines (exams, homework due)
5. Check `vault/shared/course-notes/systems-programming/exam-schedule.md` if the topic is CS 2600
6. Generate a study summary with:
   - **Key concepts** from the matched notes
   - **Definitions** and formulas
   - **Practice questions** (generate 3-5 based on the material)
   - **Upcoming deadlines** related to this topic
   - **Cross-references** to related notes the student should review

If no vault notes match, fall back to searching raw GoodNotes PDFs at `~/Library/CloudStorage/GoogleDrive-$GOOGLE_DRIVE_ACCOUNT/My Drive/GoodNotes 6/`.

### `study <course>` — Full course review

If the argument matches a course name (e.g., `study numerical-methods`), read ALL notes for that course and generate a comprehensive review covering all topics covered so far.

## Notes

- Canvas data comes from the iCal feed — no API token needed, no expiration
- Not all assignments may appear (depends on whether teachers add them to Canvas)
- Other events (lectures, office hours, campus events) will show up too
- The assignment-reminder heartbeat checks for events due in the next 3 days every 12h
- The goodnotes-watch heartbeat detects new PDF exports every hour
- The notes-ingest heartbeat processes new GoodNotes PDFs every 4h into vault course notes
- The cs2600-watch heartbeat crawls the CS 2600 website weekly for updates
