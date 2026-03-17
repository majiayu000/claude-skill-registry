---
name: pickup
description: Load session context from handoff files
invocable: true
---

# Session Pickup Skill

Loads session context from handoff files to continue where you left off.

## Instructions

When this skill is invoked, load the most recent (or specified) session handoff to recover context:

1. **Show current date/time**:
   - Run `date` command to show when the pickup session is starting
   - This helps track when you resumed work

2. **Determine which handoff file to load**:
   - If `$ARGUMENTS` is empty: Find the most recent handoff file
   - If `$ARGUMENTS` contains a date (YYYY-MM-DD): Load that specific handoff file
   - Handoff files are located in: `contexts/_LifeOS/handoff/session-handoff-*.md`

3. **Find the handoff file**:
   - Use Glob or Bash to list files in `contexts/_LifeOS/handoff/`
   - Sort by modification time (most recent first)
   - If specific date requested, look for `session-handoff-YYYY-MM-DD.md`

4. **Read and present the handoff**:
   - Read the entire handoff file
   - Present a summary to the user showing:
     - Which handoff file was loaded (date)
     - Brief overview of what session(s) it contains
     - Key highlights: main accomplishments, open questions, next steps

5. **Context loading**:
   - The full handoff content is now in your context
   - You should reference specific sections when relevant
   - Treat the handoff as authoritative context for continuing work

6. **After loading**:
   - Confirm what was loaded
   - Highlight the "Next Steps" section if it exists
   - Ask the user if they want to continue with any of the listed next steps

## Usage Examples

**Load most recent handoff:**
```
/pickup
```

**Load specific date:**
```
/pickup 2026-01-11
```

**Alternative date formats (be flexible):**
```
/pickup jan 11
/pickup yesterday
/pickup last friday
```

## Response Format

After loading a handoff file, respond with:

```markdown
## Session Context Loaded

📁 **File**: `session-handoff-YYYY-MM-DD.md`
📅 **Date**: January 11, 2026

### What Happened

[Brief 2-3 sentence summary of the session(s)]

### Key Points

- [Important decision or change 1]
- [Important decision or change 2]
- [Important decision or change 3]

### Next Steps

[Show the checklist from the handoff, or indicate if there are no pending items]

---

Ready to continue! Would you like to tackle any of the next steps, or start something new?
```

## Implementation Notes

- If no handoff files exist, inform the user and suggest using `/handoff` to create one
- If the requested date doesn't exist, show available dates
- Be smart about date parsing - accept various formats
- The handoff file content remains in your context throughout the session
- This pairs with `/handoff` to create a complete session continuity system

## Error Handling

- **No handoff files found**: "I couldn't find any handoff files. Use `/handoff` at the end of your session to create one!"
- **Date not found**: "I couldn't find a handoff for [date]. Available handoffs: [list dates]"
- **Multiple sessions in one file**: Present all sessions with timestamps
