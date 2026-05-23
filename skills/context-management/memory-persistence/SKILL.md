---
name: memory-persistence
description: "Provide session lifecycle hooks for cross-platform context persistence. Use when maintaining state across sessions or creating handoff documents. Not for in-memory variables or temporary state."
---

# Memory Persistence

Session lifecycle hooks that maintain context and knowledge across Claude Code sessions.

## What This Does

Captures session metadata and context:

- **Session Start**: Initialize session directory, record metadata
- **Session End**: Generate summary, prepare for next session
- **Session Logging**: Track session activity for pattern extraction

## Architecture

```
Session Start → Initialize → Capture Metadata
     │
     │ (work session)
     │
     ▼
Session End → Generate Summary → Extract Patterns
     │
     ▼
~/.claude/sessions/<session-id>/
├── start.jsonl    # Session start metadata
├── end.jsonl      # Session end metadata
├── session.log    # Activity log
└── summary.md     # Human-readable summary
```

## Session Structure

Each session creates a directory in `~/.claude/sessions/`:

```
~/.claude/sessions/
├── 20250127-143022-12345/
│   ├── start.jsonl    # {"timestamp":"...","event":"session_start",...}
│   ├── end.jsonl      # {"timestamp":"...","event":"session_end",...}
│   ├── session.log    # Activity log
│   └── summary.md     # Session summary
├── 20250127-154530-12346/
│   ├── ...
```

## Hooks Configuration

Configure in `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/scripts/session-start.sh",
            "description": "Initialize session logging"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/scripts/session-end.sh",
            "description": "Finalize session summary"
          }
        ]
      }
    ]
  }
}
```

## Session Metadata

**Session Start Records:**

- Timestamp
- Session ID (YYYYMMDD-HHMMSS-PID)
- Working directory
- Git branch
- Environment variables

**Session End Records:**

- Timestamp
- Session duration (calculated)
- Working directory
- Final state

## Integration with Handoff

Memory persistence integrates with the `/handoff` command:

**Session End → Handoff Generation:**

1. Session ends (hook triggers)
2. Summary generated automatically
3. Handoff document created with session context
4. Next session loads handoff for continuity

**Handoff Document Structure:**

```yaml
goal: [What was being worked on]
now: [Current state]
context:
  session_id: [Previous session ID]
  session_summary: [Link to session summary]
  files_modified: [List of files changed]
next_steps: [What to do next]
```

## Cross-Platform Compatibility

Hooks use POSIX-compliant bash for cross-platform support:

- macOS: Works natively
- Linux: Works natively
- Windows: Works via Git Bash or WSL

## Session Management

**View Sessions:**

```bash
# List all sessions
ls ~/.claude/sessions/

# View recent sessions
ls -lt ~/.claude/sessions/ | head -10

# Count total sessions
ls ~/.claude/sessions/ | wc -l
```

**Clean Old Sessions:**

```bash
# Remove sessions older than 30 days
find ~/.claude/sessions/ -type d -mtime +30 -exec rm -rf {} \;
```

**Archive Important Sessions:**

```bash
# Archive specific session
cp -r ~/.claude/sessions/20250127-143022-12345 ~/archive/sessions/
```

## Best Practices

1. **Review session summaries** - Check summary.md before starting new session
2. **Extract patterns** - Use `/learn` to capture valuable patterns from sessions
3. **Archive key sessions** - Save important sessions for future reference
4. **Clean periodically** - Remove old sessions to manage disk space
5. **Integrate with handoff** - Use handoff for session continuity

## Privacy Considerations

- **Local storage only** - Sessions stored on your machine
- **No cloud sync** - Session data never uploaded
- **No conversation content** - Only metadata and summaries
- **User control** - You decide when to archive or delete

## Integration with Seed System

### Handoff Command

Session hooks integrate with `/handoff`:

- Session end → Generate handoff document automatically
- Next session → Load previous handoff for continuity
- Seamless transition between sessions

## Related Skills

- **handoff** - Session continuity and context transfer
- **filesystem-context** - Persistent storage patterns

## Key Principle

Session lifecycle hooks maintain context continuity across sessions, enable pattern extraction, and integrate with handoff for seamless workflow transitions.

---

<critical_constraint>
MANDATORY: Capture session metadata at start and end
MANDATORY: Create handoff documents for session continuity
MANDATORY: Never lose TaskList ID across sessions
No exceptions. Session persistence enables multi-session workflows.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---
