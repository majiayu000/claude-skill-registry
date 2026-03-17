---
name: create-handoff
description: |
  Save session state for later resumption. Use when:
  - User says "done for today", "ending session", "save state"
  - Context is getting full (80%+)
  - User is taking a break
  - Before context compaction
  - User mentions "handoff", "pause work", "wrapping up"
---

# Create Session Handoff

Save current session state for seamless resumption.

## Usage

```bash
bash ~/.claude/scripts/handoff.sh create
```

Or use the native command:
```
/create-handoff
```

## What Gets Saved

The handoff file includes:
- **Current task**: What you're working on
- **Progress**: What's been completed
- **Decisions made**: Key choices and rationale
- **Files modified**: List of changed files
- **Next steps**: What remains to be done
- **Context**: Important information to remember
- **Learnings**: Patterns discovered in session

## Handoff Location

```
~/.claude/handoffs/
├── project-name-2024-01-15-1430.md
├── project-name-2024-01-14-0900.md
└── ...
```

## When to Create Handoff

1. **End of work session** - Before closing Claude Code
2. **Context at 80%+** - Before auto-compaction
3. **Taking a break** - Preserve state for later
4. **Switching tasks** - Save before context switch
5. **Before compacting** - Auto-triggered by PreCompact hook

## Auto-Handoff

The setup automatically creates handoffs:
- Before context compaction (PreCompact hook)
- At session end (SessionEnd hook)

## Output

Confirms:
- Handoff file created
- Location of file
- Key information saved

## Resume Later

To resume from a handoff:
```
/resume-handoff
```

This loads the most recent handoff for the current project.
