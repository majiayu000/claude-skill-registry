---

name: coderabbit
description: "CodeRabbit AI code review. Covers CLI, configuration, triage workflow. Keywords: @coderabbitai, code review."
version: "—"
release_date: "2026-01-21"

# CodeRabbit

AI-powered code review for pull requests and local changes.

## Quick Navigation

| Task                          | Reference                                                                                         |
| ----------------------------- | ------------------------------------------------------------------------------------------------- |
| Install & run CLI             | [cli-usage.md](references/cli-usage.md)                                                           |
| Configure .coderabbit.yaml    | [configuration.md](references/configuration.md)                                                   |
| Supported tools (40+ linters) | [tools.md](references/tools.md)                                                                   |
| Git platform setup            | [platforms.md](references/platforms.md)                                                           |
| PR commands (@coderabbitai)   | [pr-commands.md](references/pr-commands.md)                                                       |
| Claude/Cursor/Codex workflow  | [agent-integration.md](references/agent-integration.md)                                           |
| Triage findings               | [triage.md](references/triage.md)                                                                 |
| Fix single issue              | [fix.md](references/fix.md)                                                                       |
| Reporting & metrics           | [end-to-end-workflow.md#reporting--metrics](references/end-to-end-workflow.md#reporting--metrics) |
| End-to-end workflow           | [end-to-end-workflow.md](references/end-to-end-workflow.md)                                       |
| Windows/WSL setup             | [windows-wsl.md](references/windows-wsl.md)                                                       |

## Quick Start

### Install

```bash
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
source ~/.zshrc
coderabbit auth login
```

### Run Review

```bash
# AI agent workflow (most common)
coderabbit --prompt-only --type uncommitted

# Interactive mode
coderabbit

# Plain text output
coderabbit --plain
```

### Local Capture Script

If you need to persist raw prompt-only output to a file, use the bundled script:

```bash
python3 scripts/run_coderabbit.py --output coderabbit-report.txt
```

Options:

- `--output` to choose a different file name
- `--timeout` to adjust the timeout in seconds (default: 1800)

### PR Commands

```text
@coderabbitai review          # Incremental review
@coderabbitai full review     # Complete review
@coderabbitai pause           # Stop auto-reviews
@coderabbitai resume          # Resume auto-reviews
@coderabbitai resolve         # Mark comments resolved
```

## Severity Matrix

| Severity     | Action          | Examples                                          |
| ------------ | --------------- | ------------------------------------------------- |
| **CRITICAL** | Fix immediately | Security, data loss, tenant isolation             |
| **HIGH**     | Should fix      | Reliability, performance, architecture violations |
| **MEDIUM**   | Judgment call   | Maintainability, type safety (quick wins)         |
| **LOW**      | Skip            | Style/formatting, subjective nits                 |

## AI Agent Workflow Pattern

```text
Implement [feature] and then run the capture script to generate .code-review/coderabbit-report.txt,
run it in a background terminal and wait for the process to complete before reading the report.
Fix any critical issues. Ignore nits.
```

Key points:

- Use `--prompt-only` for AI-optimized output
- Reviews take 7-30+ minutes depending on changeset size
- Run command in **background terminal** (`background=true`)
- **Wait for terminal to become idle** (not busy) using `get_terminal_output`
- **Poll every 60 seconds**, not more frequently — CodeRabbit takes time
- Do NOT just check for file existence — file is created early but populated gradually
- Once terminal shows completion, read `.code-review/coderabbit-report.txt`
- If process times out (30 min default) or errors, report failure to user
- Limit to 2-3 review iterations maximum

## Minimal Configuration

```yaml
# .coderabbit.yaml
language: en-US
reviews:
  profile: chill
  high_level_summary: true
  tools:
    gitleaks:
      enabled: true
    ruff:
      enabled: true
```

## Critical Prohibitions

- Do not introduce fallbacks, mocks, or stubs in production code
- Do not broaden scope beyond what CodeRabbit flagged
- Do not "fix" style nits handled by formatters/linters
- Do not ignore CRITICAL findings; escalate if unclear
- Stop and resolve CLI errors (auth/network) before fixing code

## Links

- Official docs: https://docs.coderabbit.ai/
- Schema: https://coderabbit.ai/integrations/schema.v2.json

## Templates

- [coderabbit.minimal.yaml](assets/coderabbit.minimal.yaml) — Minimal configuration
- [coderabbit.full.yaml](assets/coderabbit.full.yaml) — Full example with all options
- [agent-prompts.md](assets/agent-prompts.md) — Ready-to-use AI agent prompts
