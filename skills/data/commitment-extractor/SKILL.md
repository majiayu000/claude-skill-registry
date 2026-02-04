---
name: commitment-extractor
description: Extract and track commitments from meeting notes - who promised what to whom, with deadlines and status tracking.
---

# Commitment Extractor

Scan meeting notes to extract, structure, and track commitments. Identifies promises, action items, and follow-ups with their owners, recipients, deadlines, and status.

## Arguments

- `$SCOPE` - Optional. Filter scope:
  - `all` - All meetings (default)
  - `recent` - Last 7 days only
  - `YYYY-MM-DD` - Specific date
  - `person:Name` - Commitments involving a specific person
  - `overdue` - Only show overdue/aging commitments

## Process

### Step 1: Scan Meeting Notes

**Locate meeting notes:**
```bash
# Find all meeting notes
find 00-Inbox/Meetings/ -name "*.md" -type f | grep -v README
```

**Apply scope filter:**
- `all`: Process all files
- `recent`: Filter to files modified in last 7 days
- `YYYY-MM-DD`: Filter to files with date in filename
- `person:Name`: Will filter in extraction phase
- `overdue`: Process all, filter in status phase

### Step 2: Extract Commitment Language

For each meeting note, scan for commitment patterns:

**First-person commitments ("I/We will do X"):**
- `I'll...`, `I will...`, `I'm going to...`
- `Let me...`, `I can...`, `I should...`
- `We'll...`, `We will...`, `We need to...`, `We should...`
- `I'll get back to you on...`, `I'll follow up...`

**Second-person requests ("You will do X"):**
- `Can you...`, `Could you...`, `Would you...`
- `You'll need to...`, `You should...`
- `Please...` (when directed at someone)

**Third-person assignments ("They will do X"):**
- `@[[Person]]...`, `@Person:...`
- `[Name] will...`, `[Name] to...`
- `Action for [Name]:...`

**Explicit action items:**
- `- [ ] ...` (unchecked tasks)
- `Action Items:` section contents
- `Follow-up:`, `Next steps:` section contents
- Lines containing `^mt-` or `^task-` block IDs

### Step 3: Structure Each Commitment

For each commitment found, extract:

```yaml
commitment:
  text: "[Exact commitment language]"
  owner: "[Who made/owns the commitment]"
  recipient: "[Who it was made to, if applicable]"
  deadline: "[Date if mentioned, or 'None specified']"
  source_meeting: "[Meeting title and date]"
  source_file: "[Full path to meeting note]"
  block_id: "[^mt-xxx or ^task-xxx if present]"
  extracted_date: "[Today's date]"
  status: "[new|aging|overdue|completed]"
```

**Owner detection rules:**
1. First-person language in meeting with known attendees = meeting owner/author
2. `@[[Person]]` or `@Person:` = that person
3. Text after "Action for [Name]:" = that person
4. If ambiguous, mark as "Unknown - needs clarification"

**Deadline detection:**
- Look for: `by [date]`, `before [date]`, `end of [week/month]`, `tomorrow`, `next [day]`, `this week`
- Convert relative dates to absolute (based on meeting date)
- If no deadline found: `None specified`

### Step 4: Calculate Status

**Status rules:**
- `new` - Extracted today or commitment < 7 days old
- `aging` - Commitment > 7 days old, no completion evidence
- `overdue` - Past explicit deadline
- `completed` - Task has `[x]` or referenced in completion notes

**Aging calculation:**
```
days_old = today - meeting_date
if deadline and today > deadline:
    status = "overdue"
elif days_old > 7 and not completed:
    status = "aging"
elif extracted_today:
    status = "new"
```

### Step 5: Cross-Reference Completion

Check if commitments have been completed:

1. **Task file check:** Search `03-Tasks/Tasks.md` for matching block IDs or similar task text
2. **Meeting follow-up check:** Look for "completed", "done", "finished" mentions in subsequent meeting notes
3. **Person page check:** Check referenced person pages for task completion

Mark as `completed` if evidence found.

### Step 6: Filter by Scope

If `person:Name` scope was specified:
- Include commitments where owner = Name
- Include commitments where recipient = Name
- Include commitments that mention Name in text

If `overdue` scope was specified:
- Only include commitments with status = `overdue` or `aging`

### Step 7: Generate Output

**Default output - grouped by person:**

```markdown
# Commitment Tracker

*Generated: [YYYY-MM-DD HH:MM]*
*Scope: [scope applied]*
*Meetings scanned: [count]*

---

## Summary

| Status | Count |
|--------|-------|
| Overdue | X |
| Aging (>7 days) | X |
| New | X |
| Completed | X |
| **Total Open** | **X** |

---

## By Owner

### [[Person Name]]

**Overdue:**
| Commitment | To | Deadline | Source Meeting |
|------------|-----|----------|----------------|
| [commitment text] | [recipient] | [date] | [[Meeting link]] |

**Aging:**
| Commitment | To | Days Old | Source Meeting |
|------------|-----|----------|----------------|
| [commitment text] | [recipient] | [N] | [[Meeting link]] |

**Recent:**
| Commitment | To | Deadline | Source Meeting |
|------------|-----|----------|----------------|
| [commitment text] | [recipient] | [date/none] | [[Meeting link]] |

---

### [[Another Person]]
...

---

## Commitments Made TO You

| From | Commitment | Deadline | Status | Source |
|------|------------|----------|--------|--------|
| [[Person]] | [text] | [date] | [status] | [[Meeting]] |

---

## Needs Attention

### Overdue (Past Deadline)

1. **[Commitment text]**
   - Owner: [[Person]]
   - Deadline: [date] (X days overdue)
   - Source: [[Meeting - Date]]
   - Suggested action: Follow up or mark complete

### Aging (No Response >7 days)

1. **[Commitment text]**
   - Owner: [[Person]]
   - Days since commitment: X
   - Source: [[Meeting - Date]]
   - Suggested action: Check status or create task

---

## Recently Completed

| Commitment | Owner | Completed | Source |
|------------|-------|-----------|--------|
| [text] | [[Person]] | [date] | [[Meeting]] |
```

**Alternative output - grouped by status (use flag `--by-status`):**

Group all overdue first, then aging, then new.

### Step 8: Optional Actions

After presenting results, offer:

1. **Create tasks:** "Would you like me to create tasks in `03-Tasks/Tasks.md` for any open commitments?"
2. **Update person pages:** "Should I add these commitments to the relevant person pages?"
3. **Mark complete:** "Any of these already done? Tell me which to mark complete."
4. **Set deadlines:** "Want to add deadlines to commitments that don't have them?"

### Step 9: Save Report (Optional)

If user requests, save report to:
`06-Resources/Intel/Commitment_Reports/YYYY-MM-DD_Commitments.md`

---

## Pattern Library

### High-Confidence Commitment Patterns

These patterns strongly indicate a commitment:

```
# First-person future tense
/I('ll| will| am going to| can| should| need to) (get|send|create|update|follow|schedule|reach|contact|review|prepare|build|write)/i

# Action item markers
/^- \[ \] .+/m
/Action (item|for|:)/i
/^### (For Me|My Actions|Dave|I need to)/im

# Explicit promises
/(I('ll| will) get back to you|I('ll| will) follow up|Let me (check|find|get|send))/i

# Request patterns
/(@\[\[.+?\]\]|@\w+):\s*.+/
/(Can|Could|Would) you (please )?(send|create|review|check|update|schedule)/i
```

### Context Clues

Look for these section headers that often contain commitments:
- `## Action Items`
- `## Follow-up`
- `## Next Steps`
- `## Tasks`
- `### For Me` / `### For Others`
- `## Decisions Made` (may contain implied commitments)

### Exclusion Patterns

Skip these (not commitments):
- Questions: `Should I...?`, `Can we...?`, `What if I...?`
- Past tense: `I did...`, `We completed...`, `I sent...`
- Hypotheticals: `I would...`, `I could...` (without context)
- Already completed: `- [x] ...`

---

## Usage Examples

```bash
# Extract all commitments from all meetings
/commitment-extractor

# Only commitments from last 7 days
/commitment-extractor recent

# Commitments involving a specific person
/commitment-extractor person:Paul

# Only show overdue/aging items
/commitment-extractor overdue

# Commitments from a specific date
/commitment-extractor 2026-01-26
```

---

## Integration Points

### Person Pages

After extraction, optionally update person pages with:
```markdown
## Open Commitments

### Commitments TO [[Person]]
- [commitment] - from [[Meeting]] (due: [date])

### Commitments FROM [[Person]]
- [commitment] - from [[Meeting]] (due: [date])
```

### Task System

Commitments can be promoted to tasks:
- Add to `03-Tasks/Tasks.md` with source link
- Generate proper `^task-YYYYMMDD-XXX` block ID
- Link back to original meeting note

### Weekly Review

The `/week-review` command can call this to surface:
- Commitments made this week
- Aging commitments that need attention
- Overdue items requiring action

---

## Notes

- This command is read-only by default (extraction only)
- Modifications (create tasks, update pages) require explicit confirmation
- Commitment detection uses heuristics - may have false positives/negatives
- When in doubt about owner, ask for clarification before creating tasks
- Block IDs enable bidirectional linking between meetings and task system
