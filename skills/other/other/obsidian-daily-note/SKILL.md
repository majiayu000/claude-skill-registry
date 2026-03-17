---
name: obsidian-daily-note
description: Manage daily notes in Obsidian vault with consistent structure
---

When working with daily notes, load this skill to:
- Add session summaries to Tasks (Work) section
- Maintain consistent checkbox formatting

## Location
Skills directory: ~/.config/opencode/skill/obsidian-daily-note/SKILL.md
Daily notes: daily/YYYY-MM-DD.md in vault
Vault root: /Users/alexismanuel/workspace/obsidian_notes/notes/

## Daily Note Structure
- Previous episode
- Tasks (Work)
- Learnings
- Next episode
- Links back
- Ideas for Notes

## Finding Daily Notes

Current daily notes are in: `daily/YYYY-MM-DD.md`
Archived daily notes (previous days) are in: `archives/daily/YYYY-MM-DD.md`

When looking for previous day's note, always check `archives/daily/` first.
Use `ls` to list available archived notes if not sure which exists.

## Adding Session Entries
Add to "Tasks (Work)" section:
```markdown
- [x] [Task description]
  - Key changes/details
  - Files affected
  - Outcomes/results
```

Use `- [x]` for completed, `- [ ]` for pending

Always preserve existing content in daily notes.

## Ticket Reference Pattern
Tickets are stored in a structured format: `work/tickets/[Ticket Name]/Ticket.md`
- Vault location: `/Users/alexismanuel/workspace/obsidian_notes/notes/`
- Ticket path pattern: `work/tickets/[Ticket Name]/Ticket.md`
- Example: `work/tickets/RD-4391 Ajouter la récupération du contenu d'un website/Ticket.md`

## Pre-Check Before Adding References
Before adding any ticket reference, always verify the ticket exists:

1. Run grep to search for ticket name:
```bash
grep -r "RD-[0-9]\+" /Users/alexismanuel/workspace/obsidian_notes/notes/work/tickets/ 2>/dev/null | head -20
```

2. List ticket directories to confirm structure:
```bash
ls -la /Users/alexismanuel/workspace/obsidian_notes/notes/work/tickets/
```

3. If ticket is found, note the exact ticket directory name for wiki-link

## Wiki-Link Formatting Rules
When referencing tickets in daily notes, use the full wiki-link path with `/Ticket` suffix:

- Correct: `[[RD-4391 Ajouter la récupération du contenu d'un website/Ticket]]`
- Incorrect: `[[RD-4391 Ajouter la récupération du contenu d'un website]]`

The `/Ticket` suffix is REQUIRED because:
- It references the actual file `Ticket.md` inside the ticket directory
- Without it, Obsidian creates a new note instead of linking to existing ticket
- The ticket directory contains `Ticket.md` as the main content file

## Verification Steps
After adding ticket references:

1. Verify the wiki-link target exists:
```bash
ls /Users/alexismanuel/workspace/obsidian_notes/notes/work/tickets/*/Ticket.md 2>/dev/null
```

2. Check that linked ticket contains expected content:
```bash
grep -l "Ticket Name" /Users/alexismanuel/workspace/obsidian_notes/notes/work/tickets/*/Ticket.md 2>/dev/null
```

3. Test the wiki-link in Obsidian by Ctrl+clicking the link

## When Delegating to Other Agents
When delegating work to other agents (Claude Code, OpenCode sessions, etc.):

1. ALWAYS provide the exact ticket reference format:
   - Include full ticket path: `work/tickets/[Ticket Name]/Ticket.md`
   - Specify the wiki-link format: `[[Ticket Name/Ticket]]`

2. Include context about existing tickets:
   - "Before creating new notes, verify ticket exists at `work/tickets/[Ticket Name]/Ticket.md`"
   - "Use wiki-link format `[[Name/Ticket]]` NOT `[[Name]]`"

3. Reference this skill for guidance:
   - "Use obsidian-daily-note skill for proper ticket referencing"
   - "Run pre-check before adding any ticket references"

## Content Transfer from Archived Notes (Bootstrap)

When starting a new day, transfer content from previous day's archived note.

### Bootstrap Rules (CRITICAL)

| Section | Source | Action |
|---------|--------|--------|
| Previous episode | Yesterday's Tasks/Work | Summarize completed work |
| Todo | Yesterday's Next episode | Copy as `- [ ]` checkboxes |
| Work | — | **Leave empty** (just `- [ ]` placeholder) |

**Key distinction:**
- **Todo** = planned intentions for the day (what you intend to do)
- **Work** = actual completed tasks (logged as you work)

During bootstrap, Work section must remain empty because no actual work has been done yet.

### Transfer Steps

1. **Previous episode**: Add summary of yesterday's completed work (not full copy)
   - Summarize key accomplishments and outcomes
   - Include ticket references with proper wiki-link format
   - Keep to bullet points, concise

2. **Todo**: Add yesterday's "Next episode" items as checkboxes
   - Use `- [ ]` format for pending tasks
   - Include context/ticket references if applicable

3. **Work**: Leave empty with just `- [ ]` placeholder
   - Do NOT copy Todo items here
   - Work entries are added during the day as tasks are completed

### Example (Correct Bootstrap)

```markdown
# Previous episode
- Implemented feature X for RD-1234 ([[RD-1234 Feature Name/Ticket|RD-1234]])
- Fixed bug in data pipeline

# Todo
- [ ] Merge MR #7890 (review completed)
- [ ] Test feature Y locally

## Work
- [ ]
```

### Anti-Pattern (WRONG)

Do NOT duplicate Todo items into Work during bootstrap:

```markdown
# Todo
- [ ] Merge MR #7890
- [ ] Test feature Y

## Work
- [ ] Merge MR #7890    ← WRONG: Work should be empty at bootstrap
- [ ] Test feature Y    ← WRONG: These go in Todo only
```
