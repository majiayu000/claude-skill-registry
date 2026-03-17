---
name: resume-handoff
description: |
  Resume from a previous session handoff. Use when:
  - User says "resume", "continue where we left off", "pick up where"
  - Starting a new session after a break
  - User mentions "last session", "previous work"
---

# Resume Session Handoff

Load state from a previous session and continue work.

## Usage

```bash
bash ~/.claude/scripts/handoff.sh resume
```

Or use:
```
/resume-handoff
```

## What Gets Loaded

- **Previous task**: What you were working on
- **Progress**: What was completed
- **Decisions**: Key choices made
- **Files modified**: What was changed
- **Next steps**: What remains
- **Context**: Important information

## Available Handoffs

List handoffs for current project:
```bash
ls ~/.claude/handoffs/ | grep "$(basename $(pwd))"
```

## Resume Options

### Most Recent
```
/resume-handoff
```
Loads the most recent handoff for current project.

### Specific Handoff
```
/resume-handoff project-name-2024-01-15-1430
```
Loads a specific handoff file.

### List All
```
/resume-handoff list
```
Shows available handoffs.

## Workflow

1. **Load handoff** - Read previous state
2. **Review context** - Understand where we left off
3. **Verify files** - Check current state vs handoff
4. **Continue work** - Pick up next steps

## Output

Displays:
- Summary of previous session
- Progress made
- Next steps to take
- Any relevant learnings

## Automatic Session Start

When starting a new session, the setup automatically:
- Recalls project learnings
- Shows recent handoff if available
- Displays context from previous work
