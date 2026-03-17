---
name: codex-orchestrator
description: Orchestrate OpenAI Codex CLI with specialized subagents for code review, debugging, architecture analysis, security audits, refactoring, and documentation. This skill should be used when delegating focused development tasks to Codex subagents (gpt-5.3-codex, gpt-5.3-codex-spark, gpt-5.2) via AGENTS.md persona injection.
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

# Full-auto mode (no approval prompts)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh reviewer "Fix all lint errors" --full-auto

# Create execution plan for complex feature
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh planner "Create an ExecPlan for adding WebSocket support"

# Build new feature from spec
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "Implement user authentication with JWT"

# Continue from previous builder session
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "continue"

# Ask a question about the codebase (read-only, no file changes)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh researcher "Explain the authentication flow in this project"

# Research with Exa web search (falls back to built-in if Exa unavailable)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh researcher "What are the latest React Server Component patterns?" --web-search
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

### Creation Tasks
- **architect** for design decisions
- **builder** for new feature implementation
- **docs** for documentation
- **refactor** for implementation improvements
- **planner** for multi-hour implementation plans

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
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "Implement milestone 1 from the auth ExecPlan" --full-auto
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

## Script Options

### codex-exec.sh Options

| Option | Description |
|--------|-------------|
| `--model <model>` | Override model (default: per-profile, see below) |
| `--reasoning <level>` | Override reasoning effort: `minimal`, `low`, `medium`, `high`, `xhigh` |
| `--sandbox <mode>` | read-only, workspace-write, danger-full-access |
| `--full-auto` | Skip approval prompts |
| `--web-search` | Enable Exa web search (built-in fallback if Exa unavailable) |

### Model & Reasoning Defaults

Each profile has a default model and reasoning effort. User flags override these.

| Profile Type | Profiles | Model | Reasoning |
|-------------|----------|-------|-----------|
| **Coding** | builder, reviewer, debugger, refactor, syseng, security, docs | `gpt-5.3-codex` | `xhigh` |
| **Planning** | planner, architect, researcher | `gpt-5.2` | `xhigh` |

**Reasoning effort levels**: `minimal` < `low` < `medium` < `high` < `xhigh`

```bash
# Uses profile defaults (builder → gpt-5.3-codex + xhigh)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "Implement auth module"

# Uses profile defaults (planner → gpt-5.2 + xhigh)
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh planner "Create ExecPlan for caching"

# Override model only
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh reviewer "Style check" --model gpt-5.3-codex-spark

# Override reasoning only
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh builder "Quick lint fix" --reasoning medium

# Override both
~/.claude/skills/codex-orchestrator/scripts/codex-exec.sh planner "Design distributed cache" --model gpt-5.3-codex --reasoning high
```

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
Older model names (`codex-mini`, `o3`, `o4-mini`) have been deprecated. Current models: `gpt-5.3-codex`, `gpt-5.3-codex-spark`, `gpt-5.2`.
Set an API key instead of using `codex login`:
```bash
export OPENAI_API_KEY=sk-...
```

### "Profile not found"
Available profiles: reviewer, debugger, architect, security, refactor, docs, planner, syseng, builder, researcher

Check profile exists:
```bash
ls ~/.claude/skills/codex-orchestrator/agents/
```

### Poor Results
- Narrow the task scope
- Provide more context in the prompt
- Try a different profile
- Use `--model gpt-5.3-codex` for complex tasks
