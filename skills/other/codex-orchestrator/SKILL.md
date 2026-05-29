---
name: codex-orchestrator
description: "Spawn specialized OpenAI Codex CLI subagents for code review, debugging, architecture analysis, security audits, refactoring, documentation, comparative evidence adjudication, and autonomous /goal runs via AGENTS.md persona injection (gpt-5.5, gpt-5.5-pro, gpt-5-mini). Triggers on 'delegate to Codex', 'Codex subagent', 'code review agent', 'security audit', 'refactor with Codex', 'goal run', 'autonomous goal', 'have Codex weigh this'."
---

# Codex Orchestrator

Spawn specialized Codex CLI subagents for focused development tasks. Each profile injects a custom AGENTS.md persona that shapes the agent's behavior, focus areas, and output format.

## Architecture

```
Claude Code (orchestrator)
    ↓ invokes skill
codex-orchestrator scripts
    ↓ spawns via Bash
Codex CLI with AGENTS.md
    ↓ executes
Specialized subagent task
```

## Prerequisites

Verify Codex CLI is installed and configured:

```bash
~/.claude/skills/codex-orchestrator/scripts/codex-status.sh
```

Required:
- Codex CLI: `npm install -g @openai/codex`
- API Key: `export OPENAI_API_KEY=sk-...`

## Auto-Update

The skill automatically checks for Codex CLI updates on each invocation and updates if needed. This prevents issues caused by outdated CLI versions.

To manually check/update:

```bash
# Check version only
~/.claude/skills/codex-orchestrator/scripts/codex-version-check.sh

# Check and auto-update if needed
~/.claude/skills/codex-orchestrator/scripts/codex-version-check.sh --auto-update
```

## Available Profiles

| Profile | Purpose | Use When |
|---------|---------|----------|
| `reviewer` | Code quality, bugs, performance | Pre-commit review, PR assessment |
| `debugger` | Root cause analysis, fixes | Investigating bugs, tracing issues |
| `architect` | System design, component boundaries | Planning changes, evaluating architecture |
| `security` | OWASP, vulnerabilities, secrets | Security audits, compliance checks |
| `refactor` | Code cleanup, modernization | Reducing tech debt, improving structure |
| `docs` | API docs, READMEs, comments | Documentation tasks |
| `planner` | ExecPlan design documents | Multi-hour tasks, complex features, significant refactors |
| `syseng` | Infrastructure, DevOps, CI/CD, monitoring | Deployment, containers, observability, production ops |
| `builder` | Greenfield implementation, new features | Creating new code from specs, incremental feature development |
| `researcher` | Read-only Q&A, codebase analysis | Questions, analysis, comparisons (no file changes) |
| `adjudicator` | Read-only comparative evidence weighing | Ambiguous hypotheses, rival interpretations, corpus comparisons, sign-value adjudication |
| `chat` | Open-ended conversation | General questions, brainstorming, discussion (read-only, ephemeral) |
| `goal` | Goal specification for /goal runs | Drafting structured objectives for autonomous multi-hour Codex sessions |

## Quick Execution

Execute a one-shot task with a specific profile:

```bash
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh <profile> "<prompt>"
```

Examples:

```bash
# Code review
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh reviewer "Review src/auth.ts for security issues"

# Debug investigation
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh debugger "Debug the login timeout on slow networks"

# Architecture design
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh architect "Design a caching layer for the API"

# Security audit
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh security "Audit the payment module for vulnerabilities"

# Write profiles auto-approve by default (uses -a never + --sandbox workspace-write)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh reviewer "Fix all lint errors"

# Create execution plan for complex feature
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh planner "Create an ExecPlan for adding WebSocket support"

# Build new feature from spec
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "Implement user authentication with JWT"

# Continue from previous builder session
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "continue"

# Open-ended conversation (read-only, ephemeral, gpt-5.4 via subscription)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh chat "What are the tradeoffs of event sourcing vs CRUD?"

# Conversation via API billing (gpt-5.5, bypasses Codex subscription)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh chat "Explain quantum error correction" --api --model gpt-5.5

# Multi-turn API chat with session file
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh chat "What is the tallest mountain?" --api --session /tmp/chat.json
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh chat "And the deepest ocean?" --api --session /tmp/chat.json

# Streaming API response
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh chat "Tell me about CQRS" --api --model gpt-5.5 --stream

# Ask a question about the codebase (read-only, no file changes)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh researcher "Explain the authentication flow in this project"

# Weigh rival hypotheses or ambiguous evidence (read-only, high reasoning)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh adjudicator "With Linear B and Linear A inscriptions side-by-side, weigh candidate values for the missing sound and rank the hypotheses."

# Research with Exa web search (injects Exa guide into AGENTS.md)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh researcher "What are the latest React Server Component patterns?" --web-search

# Research with native Codex web search (model-level tool, works in all sandboxes)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh researcher "What are the latest React patterns?" --search

# Review a screenshot (vision input)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh reviewer "Review this mockup for UX issues" --image screenshot.png

# Resume previous builder session
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "continue" --resume

# JSONL output for structured capture
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh researcher "What is 2+2?" --json | head -5
```

## Session Management

For more control, use the Python session manager:

```bash
# List available profiles
python3 ~/.claude/skills/codex-orchestrator/scripts/codex-session.py list

# Start non-interactive session
python3 ~/.claude/skills/codex-orchestrator/scripts/codex-session.py start debugger "Trace the null pointer in UserService"

# Start interactive session
python3 ~/.claude/skills/codex-orchestrator/scripts/codex-session.py interactive architect

# Show profile details
python3 ~/.claude/skills/codex-orchestrator/scripts/codex-session.py info security
```

## Profile Selection Guide

### Review Tasks
- **reviewer** for general code quality and bugs
- **security** for vulnerability-focused review
- **refactor** for cleanup opportunities

### Investigation Tasks
- **debugger** for bug investigation
- **architect** for understanding system behavior
- **researcher** for questions and analysis (read-only, no changes)
- **adjudicator** for weighing rival hypotheses, ambiguous evidence, and corpus-level comparisons (read-only, high reasoning)
- **chat** for open-ended conversation and brainstorming (read-only, ephemeral)

### Creation Tasks
- **architect** for design decisions
- **builder** for new feature implementation
- **docs** for documentation
- **refactor** for implementation improvements
- **planner** for multi-hour implementation plans
- **goal** for autonomous /goal objective specifications

## Chaining Patterns

### Review → Debug → Fix
```bash
# 1. Identify issues
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh reviewer "Review src/api/ for bugs"

# 2. Investigate specific bug
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh debugger "Debug the race condition found in cache.ts"
```

### Planner → Architect → Builder
```bash
# 1. Create comprehensive ExecPlan
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh planner "Create ExecPlan for new authentication system"

# 2. Validate architecture
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh architect "Review the auth system ExecPlan for design issues"

# 3. Build (plan guides implementation)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "Implement milestone 1 from the auth ExecPlan"
```

### Architect → Builder → Reviewer
```bash
# 1. Design approach
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh architect "Design a caching layer for the API"

# 2. Build the feature
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "Implement the caching layer from architect's design"

# 3. Review the implementation
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh reviewer "Review the new caching implementation"
```

### Architect → Review → Refactor
```bash
# 1. Design approach
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh architect "Design repository layer extraction"

# 2. Validate design
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh reviewer "Review the proposed repository pattern"

# 3. Implement
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh refactor "Extract repository pattern from services"
```

### Syseng → Architect → Planner
```bash
# 1. Assess infrastructure needs
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh syseng "Evaluate current deployment for scaling to 10x traffic"

# 2. Design architecture changes
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh architect "Design infrastructure to support 10x scale"

# 3. Create implementation plan
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh planner "Create ExecPlan for infrastructure scaling"
```

### Security → Syseng
```bash
# 1. Security audit
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh security "Audit the Kubernetes cluster configuration"

# 2. Infrastructure hardening
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh syseng "Implement security recommendations from audit"
```

### Researcher → Architect → Builder
```bash
# 1. Understand the problem space
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh researcher "How does the current caching work? What are its limitations?"

# 2. Design the solution
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh architect "Design a new caching layer addressing the limitations"

# 3. Implement
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "Implement the caching layer from architect's design"
```

## Backgrounding & Parallel Execution

Codex CLI v0.124.0+ requires a controlling TTY. When run with shell `&` or Claude Code's `run_in_background: true`, the TTY is detached and Codex silently produces empty output (openai/codex#19945). Longer prompts increase failure likelihood (empirically observed) — the researcher profile is especially vulnerable.

`codex-exec.sh` and `codex-goal.sh` automatically detect non-TTY contexts and wrap `codex exec` with `script(1)` to re-attach a pseudo-TTY. No user action is required.

For direct `codex exec` calls (not through `codex-exec.sh`), wrap manually:

```bash
# macOS
script -q /dev/null codex exec --skip-git-repo-check "prompt" </dev/null

# Linux
script -qfc 'codex exec --skip-git-repo-check "prompt" </dev/null' /dev/null
```

AGENTS.md backups are PID-scoped — multiple `codex-exec.sh` instances can safely run in the same directory.

**`--no-cleanup` flag** (codex-exec.sh only): When set, the output temp file is preserved after exit and its path is printed to stderr (`OUTPUT_FILE=<path>`). Use when the caller needs to retrieve the output file asynchronously.

## Goal Runs

The `/goal` command sets a persistent objective that Codex works toward autonomously for hours. Goals are TUI-only (not available in `codex exec` mode), so goal runs use a two-phase workflow.

### Two-Phase Workflow

**Phase 1 — Draft:** Generate a structured goal specification file using `codex exec` with the `goal` profile.

**Phase 2 — Run:** Launch the interactive Codex TUI with `/goal` set from the spec file.

### Usage

```bash
# Draft a goal specification
~/.claude/skills/codex-orchestrator/scripts/codex-goal.sh draft "Add authentication with JWT to the API"

# Draft with custom output path
~/.claude/skills/codex-orchestrator/scripts/codex-goal.sh draft "Migrate to PostgreSQL" --output goals/pg-migration.md

# List existing goals
~/.claude/skills/codex-orchestrator/scripts/codex-goal.sh list

# Launch Codex TUI with a goal
~/.claude/skills/codex-orchestrator/scripts/codex-goal.sh run goals/goal-20260518-143000.md

# Run with custom model
~/.claude/skills/codex-orchestrator/scripts/codex-goal.sh run goals/goal-01.md --model gpt-5.5-pro
```

### Goal File Format

Goal specifications follow a structured format with YAML frontmatter:

```markdown
---
objective: "One-line summary"
status: draft
created: 2026-05-18
project: /path/to/project
---

# Goal: <objective>

## Objective / Stopping Condition / Context / Constraints / Validation / Checkpoints / Progress Log
```

Goals under 3,500 characters are inlined directly into the `/goal` command. Longer goals are referenced by file path.

### Chaining: Planner → Goal → Run → Reviewer

```bash
# 1. Plan the feature
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh planner "Create ExecPlan for caching layer"

# 2. Draft a goal from the plan
~/.claude/skills/codex-orchestrator/scripts/codex-goal.sh draft "Implement caching layer per ExecPlan"

# 3. Launch autonomous goal run
~/.claude/skills/codex-orchestrator/scripts/codex-goal.sh run goals/goal-20260518-143000.md

# 4. Review what Codex built
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh reviewer "Review the caching implementation"
```

### Caveats

- `/goal` is TUI-only — the `run` subcommand launches an interactive Codex session (stdin is not redirected)
- Requires `features.goals = true` in `~/.codex/config.toml` (or `--enable goals` flag, which the script passes automatically)
- One goal per thread — must `/goal clear` before setting a different goal
- 4,000 character limit on `/goal` content (the draft phase targets under 3,500 to leave overhead)

See `references/goal-command.md` for the full `/goal` command reference.

## Script Options

### codex-exec.sh Options

| Option | Description |
|--------|-------------|
| `--model <model>` | Override model (default: per-profile, see below) |
| `--reasoning <level>` | Override reasoning effort: `minimal`, `low`, `medium`, `high`, `xhigh` |
| `--sandbox <mode>` | read-only, workspace-write, danger-full-access |
| `--no-approve` | Force read-only sandbox (no file writes) |
| `--web-search` | Enable Exa web search (injects guide into AGENTS.md) |
| `--search` | Enable native Codex web search (model-level tool, works in all sandboxes) |
| `--json` | Output JSONL event stream (pipe to jq, logs, etc.) |
| `--image <file>` | Attach image to prompt (vision input) |
| `--resume` | Resume previous exec session (builder "continue" workflow) |
| `--with-mcp` | (no-op, kept for compatibility; manage MCPs in ~/.codex/config.toml) |
| `--api` | Use OpenAI API directly (API billing, not Codex subscription) |
| `--session <file>` | Session file for multi-turn API chat (requires `--api`) |
| `--system <prompt>` | System prompt for API chat (requires `--api`) |
| `--stream` | Stream API response tokens (requires `--api`) |

### Model & Reasoning Defaults

Each profile has a default model and reasoning effort. User flags override these.

| Profile Type | Profiles | Model | Reasoning |
|-------------|----------|-------|-----------|
| **Coding** | builder, reviewer, debugger, refactor, syseng, security, docs | `gpt-5.5` | `high` |
| **Planning** | planner, architect, goal | `gpt-5.5` | `high` |
| **Research** | researcher | `gpt-5.5` | `medium` |
| **Adjudication** | adjudicator | `gpt-5.5` | `high` |
| **Chat** | chat | `gpt-5.4` | `medium` |

**Reasoning effort levels**: `none` < `minimal` < `low` < `medium` < `high` < `xhigh`

```bash
# Uses profile defaults (builder → gpt-5.5 + high)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "Implement auth module"

# Uses profile defaults (planner → gpt-5.5 + high)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh planner "Create ExecPlan for caching"

# Override model for quick tasks
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh reviewer "Style check" --model gpt-5-mini

# Override reasoning only
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "Quick lint fix" --reasoning medium

# Override both
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh planner "Design distributed cache" --model gpt-5.5 --reasoning high
```

## API Mode (Direct OpenAI API)

The `--api` flag bypasses Codex CLI entirely and calls the OpenAI API directly via `gpt-api-chat.py`. Billing goes to your `OPENAI_API_KEY`, not the Codex subscription.

**When to use API mode:**
- Access models not in your Codex subscription (e.g. `gpt-5.5`)
- Multi-turn conversations with session persistence
- Streaming responses
- Custom system prompts

```bash
# One-shot API query
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh chat "Explain X" --api --model gpt-5.5

# Multi-turn with session file (context carries across calls)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh chat "What is X?" --api --session /tmp/session.json
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh chat "Tell me more" --api --session /tmp/session.json

# Streaming output
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh chat "Describe Y" --api --model gpt-5.5 --stream

# Custom system prompt
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh chat "Analyze this" --api --system "You are a security analyst"

# Any profile works with --api (sends raw prompt to OpenAI API, no Codex CLI)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh researcher "What are the latest React patterns?" --api --model gpt-5.5
```

**Supported models:** `gpt-5.5`, `gpt-5.5-pro`, `gpt-5.4`, `gpt-5-mini`, `gpt-5-nano`

**Three-way mode (Claude + GPT):** Within a Claude Code session, invoke `gpt-api-chat.py` via Bash, read GPT's response, synthesize perspectives, and steer the conversation. Use `--session` to maintain GPT's context across turns.

**Requires:** `OPENAI_API_KEY` in environment (loaded from `~/.config/env/secrets.env`)

## Testing

Run the test suite to verify installation:

```bash
~/.claude/skills/codex-orchestrator/scripts/test-codex.sh         # Full tests
~/.claude/skills/codex-orchestrator/scripts/test-codex.sh --quick # Skip API test
```

## Reference Documentation

For detailed information:

- `references/codex-cli.md` - Complete CLI command reference
- `references/agents-md-format.md` - AGENTS.md syntax and best practices
- `references/subagent-patterns.md` - Delegation patterns and examples
- `references/goal-command.md` - /goal command reference and best practices

## Troubleshooting

### "Codex CLI not found"
```bash
npm install -g @openai/codex
```

### "Authentication error"
```bash
export OPENAI_API_KEY=sk-...
# or
codex login
```

### "Model not supported with ChatGPT account"
Older model names (`codex-mini`, `o3`, `o4-mini`) have been deprecated. Current models: `gpt-5.5`, `gpt-5.5-pro`, `gpt-5-mini`, `gpt-5-nano`. Previous generation (`gpt-5.4`, `gpt-5.4-pro`, `gpt-5.3-codex`, `gpt-5.2`) still works but is superseded.
Set an API key instead of using `codex login`:
```bash
export OPENAI_API_KEY=sk-...
```

### "Profile not found"
Available profiles: reviewer, debugger, architect, security, refactor, docs, planner, syseng, builder, researcher, adjudicator, chat, goal

Check profile exists:
```bash
ls ~/.claude/skills/codex-orchestrator/agents/
```

### "Codex produced no output"
The researcher/adjudicator/chat profiles capture output to a temp file. If Codex exits without writing to it, the script warns and exits 1. Common causes:
- **TTY detachment (most common)**: Codex CLI v0.124.0+ silently crashes when backgrounded without a TTY. `codex-exec.sh` auto-wraps with `script(1)` — verify your Codex version (`codex --version`). Longer prompts increase failure rate.
- Codex session too short to produce a response
- Model returned empty response (retry)
- AGENTS.md was missing (check for stale `.AGENTS.md.codex-backup.*` files in working directory)

### Poor Results
- Narrow the task scope
- Provide more context in the prompt
- Try a different profile
- Use `--model gpt-5.5-pro` for complex tasks
