---
name: continuous-learning
description: "This skill should be used when the user asks to 'extract patterns from this session', 'save what we learned', 'create a skill from this workflow', 'learn from this conversation', 'capture reusable knowledge', or wants to turn session patterns into reusable skills."
user-invocable: false
---

# Continuous Learning Skill

Extract reusable patterns from sessions and save them as learned skills for future use.

## How It Works

This skill analyzes the session transcript to identify extractable patterns:

1. **Session Evaluation**: Checks if session has enough messages (default: 10+)
2. **Pattern Detection**: Identifies error resolutions, workarounds, debugging techniques
3. **Skill Extraction**: Saves useful patterns to `~/.claude/skills/`

## When to Use

- At end of long sessions with multiple problem-solving cycles
- After resolving complex errors that might recur
- When you develop project-specific conventions

## Invocation

Use `/learn` command or invoke directly:
```
/continuous-learning
```

## Configuration

Edit `config.json` to customize:

```json
{
  “min_session_length”: 10,
  “extraction_threshold”: “medium”,
  “auto_approve”: false,
  "learned_skills_path": "~/.claude/skills/learned/",
  “patterns_to_detect”: [
    “error_resolution”,
    “user_corrections”,
    “workarounds”,
    “debugging_techniques”,
    “project_specific”
  ]
}
```

## Pattern Types

| Pattern | Description |
|---------|-------------|
| `error_resolution` | How specific errors were resolved |
| `user_corrections` | Patterns from user corrections |
| `workarounds` | Solutions to framework/library quirks |
| `debugging_techniques` | Effective debugging approaches |
| `project_specific` | Project-specific conventions |

## Learned Skills Format

Extracted skills are saved following the standard skill directory structure:

```
~/.claude/skills/learned/
├── fix-marimo-import-error/
│   └── SKILL.md
├── debug-pixi-environment/
│   └── SKILL.md
└── wrds-connection-pattern/
    └── SKILL.md
```

Each learned skill follows standard SKILL.md format with:
- Frontmatter (name and description)
- Problem context
- Solution pattern
- Example usage

## Integration

The skill reads from `CLAUDE_TRANSCRIPT_PATH` (JSON conversation transcript)
which is automatically set by Claude Code during sessions.

## Related

- `/learn` command - Manual pattern extraction mid-session
- `/checkpoint` command - Save session state
- Session-end hook - Auto-evaluates sessions for patterns
