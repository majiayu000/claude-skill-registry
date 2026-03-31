---
name: codex-exec
description: "Run autonomous task execution using the codex CLI. Use when the user asks to \"codex exec\", \"run codex exec\", \"execute a task with codex\", or \"delegate to codex\"."
---

# Codex Exec

Autonomous task execution via the codex CLI. Runs non-interactively. Progress streams to stderr; final result on stdout.

```bash
codex exec "task description"
```

## Permission Levels

| Level | Flag | When to Use |
|-------|------|-------------|
| Read-only (default) | *(none)* | Analysis, code reading, generating reports |
| Workspace write | `--sandbox workspace-write` | Editing files within the project |
| Full access | `--sandbox danger-full-access` | Installing packages, running tests, system operations |
| Full auto | `--full-auto` | Combined with a sandbox level for unattended execution |

## Options

| Option | Description |
|--------|-------------|
| `--full-auto` | Allow file edits without confirmation prompts |
| `--sandbox <level>` | Permission level: `danger-full-access`, `workspace-write` |
| `--json` | JSON Lines output (progress + final message) |
| `-o <path>` | Write final message to a file |
| `--output-schema <path>` | Enforce JSON Schema on the output |
| `--ephemeral` | No persisted session files |
| `--skip-git-repo-check` | Bypass git repository requirement |
| `-m, --model <MODEL>` | Specify the model to use |

## Interpreting Results

- Exec output is a starting point, not a guaranteed solution
- Cross-reference suggestions with project documentation and conventions
- Test incrementally rather than applying all changes at once
- For file-editing tasks, always review the diff before committing
- Use a generous timeout (60 minutes / 3600000ms)
