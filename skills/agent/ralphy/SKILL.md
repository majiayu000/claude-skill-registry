---
name: ralphy
description: Autonomous AI coding orchestration using the Ralph Wiggum technique and Ralphy CLI. This skill should be used when running AI agents in continuous loops until tasks complete, orchestrating multi-task development with PRD/YAML files, configuring parallel agent execution, or implementing the Ralph Wiggum autonomous development methodology. Triggers on mentions of ralphy, ralph, autonomous loops, PRD-driven development, or multi-agent orchestration.
---

# Ralphy & Ralph Wiggum Technique

Ralphy is an autonomous AI coding orchestrator that runs agents on tasks until done. Built on Geoffrey Huntley's Ralph Wiggum technique - a continuous loop methodology where AI agents iterate until completion.

## Quick Reference

```bash
# Single task
ralphy "add dark mode"

# From PRD/YAML
ralphy --prd PRD.md
ralphy --yaml tasks.yaml

# Parallel execution
ralphy --parallel --max-parallel 5

# With branches and PRs
ralphy --branch-per-task --create-pr
```

## Core Concepts

### The Ralph Wiggum Technique

The foundational principle: run an AI agent in a loop until the job is done.

```bash
# Minimal form
while :; do cat PROMPT.md | claude ; done
```

**Key insight**: Failures inform improvements. When Ralph fails, tune the prompts like a guitar - add specific guidance based on observed failure patterns.

### Three-Phase Architecture

1. **Requirements Definition**: Discuss project, identify Jobs to Be Done (JTBD), break into topics
2. **Planning Loop**: Gap analysis between specs and code, generate IMPLEMENTATION_PLAN.md
3. **Building Loop**: Implement tasks, validate with tests, commit on success

## Ralphy CLI Usage

### Task Sources

**Markdown PRD** (checkbox format):
```markdown
## Tasks
- [ ] create auth system
- [ ] add dashboard
- [x] completed task (skipped)
```

**YAML format**:
```yaml
tasks:
  - title: create auth
    completed: false
    parallel_group: 1
  - title: add dashboard
    completed: false
    parallel_group: 2
```

**GitHub Issues**:
```bash
ralphy --github owner/repo --github-label "ready"
```

### Parallel Execution

Run multiple agents simultaneously with isolation:

```bash
ralphy --parallel              # 3 agents default
ralphy --parallel --max-parallel 5
ralphy --parallel --sandbox    # Lightweight sandboxes for large repos
```

Each agent gets:
- Isolated worktree or sandbox
- Unique branch: `ralphy/agent-N-task-slug`
- Independent execution context

**Parallel Groups** in YAML control execution order:
```yaml
tasks:
  - title: Create User model
    parallel_group: 1
  - title: Create Post model
    parallel_group: 1    # Runs with above
  - title: Add relationships
    parallel_group: 2    # Waits for group 1
```

### Branch Workflow

```bash
ralphy --branch-per-task           # One branch per task
ralphy --branch-per-task --create-pr   # Plus pull requests
ralphy --branch-per-task --draft-pr    # Draft PRs
ralphy --base-branch main          # Branch from specific base
```

### Engine Selection

```bash
ralphy "task"                      # Claude Code (default)
ralphy --opencode "task"           # OpenCode
ralphy --cursor "task"             # Cursor
ralphy --codex "task"              # Codex
ralphy --qwen "task"               # Qwen-Code
ralphy --copilot "task"            # GitHub Copilot
```

**Model override**:
```bash
ralphy --model sonnet "task"
ralphy --sonnet "task"             # Shortcut
```

**Pass args to engine**:
```bash
ralphy --claude "task" -- --no-permissions-prompt
```

## Project Configuration

Initialize with auto-detection:
```bash
ralphy --init
```

Creates `.ralphy/config.yaml`:
```yaml
project:
  name: "my-app"
  language: "TypeScript"
  framework: "Next.js"

commands:
  test: "npm test"
  lint: "npm run lint"
  build: "npm run build"

rules:
  - "use server actions not API routes"
  - "follow error pattern in src/utils/errors.ts"

boundaries:
  never_touch:
    - "src/legacy/**"
    - "*.lock"

capabilities:
  browser: "auto"

notifications:
  discord_webhook: "https://discord.com/..."
  slack_webhook: "https://hooks.slack.com/..."
```

Add rules dynamically:
```bash
ralphy --add-rule "always use TypeScript strict mode"
```

## CLI Flags Reference

| Flag | Purpose |
|------|---------|
| `--prd PATH` | Task file/folder (default: PRD.md) |
| `--yaml FILE` | YAML task file |
| `--github REPO` | Use GitHub issues |
| `--parallel` | Run parallel agents |
| `--max-parallel N` | Max agents (default: 3) |
| `--sandbox` | Lightweight sandboxes vs worktrees |
| `--branch-per-task` | One branch per task |
| `--create-pr` | Create pull requests |
| `--draft-pr` | Create draft PRs |
| `--no-merge` | Skip auto-merge in parallel |
| `--no-tests` | Skip tests |
| `--no-lint` | Skip linting |
| `--fast` | Skip tests and lint |
| `--no-commit` | Don't auto-commit |
| `--max-iterations N` | Stop after N tasks |
| `--max-retries N` | Retries per task (default: 3) |
| `--dry-run` | Preview only |
| `--browser` | Enable browser automation |
| `-v, --verbose` | Debug output |

## The Ralph Loop Pattern

For advanced usage implementing the full Ralph Wiggum technique:

See [references/ralph_loop_pattern.md](references/ralph_loop_pattern.md) for:
- Complete file structure
- PROMPT_plan.md and PROMPT_build.md templates
- Context management strategies
- Backpressure mechanisms
- Plan regeneration triggers

## Security Considerations

**Critical**: Running with `--dangerously-skip-permissions` requires sandboxing.

- Always set `--max-iterations` (e.g., 20-50) to prevent runaway costs
- Run in sandboxed environments (Docker, Fly Sprites, E2B)
- Use minimum viable API key access
- Escape hatches: Ctrl+C stops loop, `git reset --hard` reverts

## Best Practices

1. **Start with clear specs**: Well-defined PRD items lead to better outcomes
2. **Use parallel groups**: Organize dependent tasks to run efficiently
3. **Set boundaries**: Protect critical files in config
4. **Add project rules**: Guide consistent patterns
5. **Monitor iterations**: Watch for loops that aren't progressing
6. **Iterate on prompts**: When Ralph fails, tune the guidance

## Troubleshooting

**Agent stuck in loop**: Check if task is too vague. Add specific acceptance criteria.

**Merge conflicts in parallel**: Use `--no-merge` and resolve manually, or let AI resolve.

**Rate limits**: Ralphy detects and defers tasks on quota errors.

**Tests failing**: Ensure `commands.test` in config matches your test runner.
