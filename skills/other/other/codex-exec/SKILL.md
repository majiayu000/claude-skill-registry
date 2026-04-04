---
name: codex-exec
description: "Run autonomous task execution using the codex CLI. Use when the user asks to \"codex exec\", \"run codex exec\", \"execute a task with codex\", or \"delegate to codex\"."
---

# Codex Exec

Autonomous task execution via the codex CLI. Runs non-interactively. Progress streams to stderr; final result on stdout.

```bash
codex exec "task description"
```

For large context, pipe it via stdin. The prompt stays as the argument, context is passed as `<stdin>` automatically:

```bash
cat context.txt | codex exec "question about the context"
```

## Permission Levels

| Level | Flag | When to Use |
|-------|------|-------------|
| Read-only (default) | *(none)* | Analysis, code reading, generating reports |
| Workspace write | `--sandbox workspace-write` | Editing files within the project |
| Full access | `--sandbox danger-full-access` | Installing packages, running tests, system operations |
| Full auto | `--full-auto` | Combined with a sandbox level for unattended execution |

For fix or implementation tasks, default to `--sandbox workspace-write --full-auto` so Codex can edit files without confirmation prompts. Use read-only for analysis or research tasks.

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

## Prompt Shaping

Codex uses XML tags in its own context scaffolding, so the model parses them natively. Structure prompts with XML tags for clearer responses:

- `<task>`: The concrete job and relevant context.
- `<structured_output_contract>`: Required output shape, ordering, and format.
- `<compact_output_contract>`: Same purpose but for concise prose responses.
- `<grounding_rules>`: When claims must be evidence-based.
- `<dig_deeper_nudge>`: Push past surface-level findings to check for second-order failures.
- `<verification_loop>`: When correctness matters — ask Codex to verify before finalizing.

Keep prompts compact. Prefer tighter output contracts over raising reasoning effort. One clear task per exec call.

## Parallel Execution

Codex supports parallel sub-agents via `spawn_agent` / `wait_agent`. The model will not fan out unless the prompt explicitly requests it. See [references/parallel-execution.md](references/parallel-execution.md) for patterns and limitations.

## Interpreting Results

- Exec output is a starting point, not a guaranteed solution
- Cross-reference suggestions with project documentation and conventions
- Test incrementally rather than applying all changes at once
- For file-editing tasks, always review the diff before committing
- Use a generous timeout (60 minutes / 3600000ms)
