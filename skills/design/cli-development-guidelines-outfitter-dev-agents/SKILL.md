---
name: cli-development-guidelines
description: 'Design and review command-line interfaces (CLI tools) with human-first
  UX and UNIX composability: arguments/flags, help text, stdout/stderr, exit codes,
  interactivity, configuration, errors, telemetry'
---

---
name: cli-development-guidelines
description: Design and review command-line interfaces (CLI tools) with human-first UX and UNIX composability: arguments/flags, help text, stdout/stderr, exit codes, interactivity, configuration, errors, telemetry, and distribution.
license: CC-BY-SA-4.0 (docs, adapted from clig.dev); MIT (scripts)
compatibility: Scripts use Python 3.10+ (scripts/cli_audit.py).
metadata:
  version: "0.1.0"
  upstream: "clig.dev + POSIX/GNU/Heroku/12-factor + Agent Skills spec"
---
# CLI Development Guidelines

## When to activate this skill

- You are *designing*, *implementing*, or *reviewing* a command-line tool.
- The user mentions (explicitly or implicitly): `--help`, flags, subcommands, exit codes, stdout/stderr, piping, JSON output, color, prompts, config files, env vars, “works in CI”, install/uninstall, telemetry.

## What this skill produces

- A *CLI contract* (what users can rely on): commands, flags, IO behavior, exit codes, config/env, examples, and safety behavior.
- Draft *help output* and docs structure (example-first).
- A *compliance audit* (when runnable) using `scripts/cli_audit.py`.

## Non-negotiable CLI citizenship

- Exit codes:
  - `0` on success.
  - Non-zero on failure (and ideally meaningful, documented codes).
- Streams:
  - `stdout` is for primary output and machine-readable output.
  - `stderr` is for errors, warnings, progress, and “what I’m doing” messaging.
- Discoverability:
  - `--help` (and usually `-h`) shows help and exits.
  - `--version` prints version and exits.
- Interactivity:
  - Prompts only when `stdin` is a TTY.
  - Provide `--no-input` to force non-interactive behavior.
- Scripting friendliness:
  - No ANSI color / spinners when output isn’t a TTY.
  - Support `NO_COLOR` and `--no-color`.
  - Consider `--json` and `--plain` for stable output.

## Workflow

### Sketch the CLI contract first

- Start from the user’s jobs-to-be-done (what they’re trying to accomplish).
- Decide:
  - Command shape: single command vs subcommands (`noun verb` is common).
  - Inputs: args vs flags vs stdin vs prompts vs config/env.
  - Outputs: human default, plus machine modes (`--json`, `--plain`, `--quiet`).
  - Safety: confirmations, `--dry-run`, `--force`, secret handling.

Use:
- [CLI reference](references/REFERENCE.md)
- [CLI spec template](templates/cli-command-spec-template.json)

### Implement with safe defaults

- Use a CLI parsing library (don’t hand-roll).
- Make “boundary-crossing” actions explicit:
  - Network calls
  - Writing files not explicitly provided
  - Mutating remote state
- Avoid footguns:
  - Don’t accept secrets via flags or environment variables.
  - Don’t print stack traces by default.
  - Don’t assume TTY (detect it).

### Validate and iterate

- Run an automated sanity check (when possible):
  - `python scripts/cli_audit.py -- <your-cli> [subcommand]`
- Fix in this order:
  - Broken stdout/stderr separation
  - Incorrect exit codes
  - Help that’s missing or undiscoverable
  - Unsafe defaults (destructive ops, secrets, hidden network writes)
  - Unscriptable output (no stable modes)

Use:
- [Checklist](references/CHECKLIST.md)
- `scripts/cli_audit.py`

## Reference library

- Core reference: [references/REFERENCE.md](references/REFERENCE.md)
- Quick audit checklist: [references/CHECKLIST.md](references/CHECKLIST.md)
- Evaluation prompts: [references/EVAL_PROMPTS.md](references/EVAL_PROMPTS.md)

## Templates and scripts

- CLI spec template: `templates/cli-command-spec-template.json`
- Help text template: `templates/help-text-template.md`
- Error message template: `templates/error-message-template.md`
- Audit a CLI: `scripts/cli_audit.py`
