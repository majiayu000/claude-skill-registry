---
name: setup-hooks
description: Configure Claude Code hooks for automated validation on file edits and commits
disable-model-invocation: true
---

Set up Claude Code hooks for the project.

Hooks enforce coding standards automatically — they run scripts at specific points in Claude's workflow. Unlike CLAUDE.md instructions (advisory), hooks are deterministic and guarantee the action happens.

## Hook 1 — Syntax Check After File Edits
**Event:** `PostToolUse` on `Write` and `Edit` tools
**Purpose:** Catch syntax errors immediately after writing/editing Python files
**Command:** Run the syntax validation command (see stack concepts in project config) — fails if syntax is broken

## Hook 2 — Annotations Check After File Edits
**Event:** `PostToolUse` on `Write` and `Edit` tools
**Purpose:** Enforce the future annotations pattern (see stack concepts) in source files under the source root
**Command:** Check if the file is under the source root, then verify the annotations pattern exists

## Hook 3 — Tests After File Edits
**Event:** `PostToolUse` on `Write` and `Edit` tools
**Purpose:** Run tests after modifying source or test files to catch regressions immediately
**Command:** Run the test command (see project config)
**Note:** Only trigger on source code file edits, not README or config files

## Installation

Write the hooks to `.claude/settings.json` using this structure:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "<shell command here>"
          }
        ]
      }
    ]
  }
}
```

## Important Notes
- Test each hook manually before adding to settings
- Hooks that exit non-zero BLOCK the operation and show the error to the user
- Keep hooks fast (< 5 seconds) — slow hooks degrade the coding experience
- Use `.claude/settings.json` for project hooks (shared via git)
- Use `.claude/settings.local.json` for personal hooks (gitignored)
- See https://code.claude.com/docs/en/hooks for full documentation

## Verification
After setup, test by editing a file and confirming the hook runs.