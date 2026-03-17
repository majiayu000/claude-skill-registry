---
name: obsidian-daily-driver
description: |
  Manages daily notes workflow in Obsidian. Appends tasks, session logs, and
  learnings to today's daily note. Creates the daily note if it doesn't exist.
  Bridges Claude Code sessions to your daily note so nothing gets lost. Activates
  on "add to daily", "log this", "daily note", or end of session when daily
  notes are enabled.
allowed-tools: |
  bash: ls, find, date, obsidian-cli, obsidian, cat
  file: read, write
---

# Obsidian Daily Driver

<purpose>
Your daily note is the hub. Tasks you worked on, things you learned, links to
what you created — it all flows through the daily note. But Claude Code sessions
are stateless. You do an hour of work, close the terminal, and none of it shows
up in today's note. This skill bridges that gap — every session can log to your
daily note, so when you open Obsidian tomorrow, you see what happened.
</purpose>

## When To Activate

<triggers>
- User says "add to daily", "log this", "daily note", "today's note"
- User says "what did I do today" (read daily note)
- End of a work session when daily notes exist in the vault
- After completing significant work that should be logged
- User says "task" or "todo" in the context of daily notes
- Session produces artifacts worth tracking (new files, discoveries, decisions)
</triggers>

Do NOT trigger for:
- Vaults without daily notes
- When user explicitly doesn't want daily logging
- Trivial interactions (single questions, typo fixes)

## Instructions

### Step 1: Find Today's Daily Note

<find_daily>
Daily notes follow a date-based naming convention:

```bash
TODAY=$(date +%Y-%m-%d)

# Check common locations
DAILY="$VAULT_PATH/Daily/$TODAY.md"
[ -f "$DAILY" ] || DAILY="$VAULT_PATH/Journal/$TODAY.md"
[ -f "$DAILY" ] || DAILY="$VAULT_PATH/daily/$TODAY.md"

# Or use CLI
obsidian daily:read 2>/dev/null
obsidian-cli daily 2>/dev/null

# Check CLAUDE.md for daily note path convention
grep -i "daily" "$VAULT_PATH/CLAUDE.md" 2>/dev/null
```

If today's note doesn't exist, create it from the daily template:
```bash
# Find the daily template
TEMPLATE=$(find "$VAULT_PATH/Templates" -iname "*daily*" | head -1)
```

Create with proper frontmatter:
```markdown
---
type: daily
date: YYYY-MM-DD
tags:
  - daily
---

# YYYY-MM-DD

## Tasks

- [ ]

## Log


## Links

```
</find_daily>

### Step 2: Read Existing Content

<read_daily>
Before appending, read what's already there:

```bash
cat "$DAILY"
```

Understand the structure so you append to the RIGHT section:
- Tasks go under `## Tasks`
- Logs go under `## Log`
- Links go under `## Links`

Don't duplicate entries that already exist.
</read_daily>

### Step 3: Append Content

<append>
Based on what you're logging, append to the correct section.

**Adding a task:**
```bash
# Using CLI
obsidian daily:append content="- [ ] Task description"

# Direct file: find ## Tasks section and append after it
```

Append under `## Tasks`:
```markdown
- [ ] Task description
```

**Logging work done:**

Append under `## Log`:
```markdown
- Worked on [[project-name]]: brief description of what was done
- Fixed: [[bug-or-issue]] — what was wrong and how it was fixed
- Created: [[new-note]] — why it was created
```

**Adding links to created artifacts:**

Append under `## Links`:
```markdown
- [[note-created-today]] — context for why
- [[meeting-note]] — key takeaways
```

**Session summary (end of session):**

Append under `## Log`:
```markdown
### Claude Session — HH:MM

**Worked on:** brief description
**Created:**
- [[note-1]]
- [[note-2]]
**Decisions:**
- Decision made and why
**Next:**
- [ ] Follow-up task
```
</append>

### Step 4: Handle CLI vs Direct Write

<write_method>
**Official CLI (preferred — respects plugins/templates):**
```bash
obsidian daily:append content="- [ ] New task"
obsidian daily:append content="- Completed: task description"
```

**Yakitrak CLI:**
```bash
obsidian-cli create "$TODAY" --append --content "- [ ] New task"
```

**Direct file append:**
```bash
# Careful: append to the right SECTION, not just end of file
# Read the file, find the section, insert content, write back
```

When using direct file write, you MUST:
1. Read the file first
2. Find the target section (## Tasks, ## Log, etc.)
3. Insert content after the section heading (or after existing items)
4. Write the whole file back

Do NOT just append to the end of the file — it breaks the structure.
</write_method>

### Step 5: Cross-Link

<crosslink>
If today's work relates to project notes, meeting notes, or other daily notes:

- Link from daily to the related note: `[[related-note]]`
- Also add a backlink FROM the related note TO today's daily note
  (only if the related note doesn't already link back)

```markdown
# In today's daily note:
- Continued work on [[project-x-api-design]]

# In project-x-api-design.md, add:
## Activity
- [[2026-02-12]] — added rate limiting approach
```

This creates bidirectional links that show up in Obsidian's backlinks panel
and graph view.
</crosslink>

## Log Entry Formats

<formats>
Keep entries concise. The daily note is a log, not a journal.

**Task added:**
```markdown
- [ ] Brief task description
```

**Task completed:**
```markdown
- [x] Completed task description
```

**Work log:**
```markdown
- Worked on [[note]]: one sentence of what was done
```

**Decision made:**
```markdown
- Decided: decision summary (see [[decision-note]] for detail)
```

**Discovery:**
```markdown
- Found: discovery summary — [[related-note]]
```

**Session summary:**
```markdown
### Claude Session — HH:MM
**Worked on:** [topic]
**Outcome:** [result]
**Next:** [what's left]
```
</formats>

## Output Format

When appending:
```markdown
Added to daily note (YYYY-MM-DD):
- [what was added and to which section]
```

When creating daily note:
```markdown
Created daily note: [[YYYY-MM-DD]]
Path: Daily/YYYY-MM-DD.md
Added: [initial content]
```

When reading:
```markdown
Today's note (YYYY-MM-DD):
- Tasks: X open, Y completed
- Log: [summary of entries]
```

## NEVER

- Overwrite the daily note (append only)
- Append to the end of the file without finding the right section
- Duplicate entries that already exist
- Create verbose log entries (keep them to one line)
- Skip reading the existing note before appending
- Log trivial interactions (single questions, typo fixes)

## ALWAYS

- Read the daily note before appending to it
- Append to the correct section (Tasks/Log/Links)
- Use wikilinks when referencing other notes
- Create the daily note from template if it doesn't exist
- Include timestamps on session summaries
- Check for the daily note path in CLAUDE.md first

## Example

**End of session where user built a new API endpoint:**

```
Session ending. Logging to today's daily note...

Reading Daily/2026-02-12.md...

Appended to ## Log:
- Worked on [[project-api]]: built rate limiting endpoint, added tests
- Created: [[api-rate-limiting]] — design doc for rate limit approach

Appended to ## Tasks:
- [ ] Deploy rate limiting to staging
- [x] Write rate limiting tests

Appended to ## Links:
- [[api-rate-limiting]]

Daily note updated.
```

**User says "add a task to my daily":**

```
Reading Daily/2026-02-12.md...

What task should I add?

[User: Review the PR from Sarah]

Appended to ## Tasks:
- [ ] Review the PR from Sarah

Daily note updated.
```

<failed-attempts>
What DOESN'T work:
- Appending to end of file — breaks note structure, content ends up after footer
- Using echo >> for append — doesn't respect sections, can corrupt YAML
- Creating daily note without checking template — inconsistent format
- Not reading existing content — duplicates tasks or logs
</failed-attempts>
