---
name: gemini-cli-extension-porting
description: Use when porting beads or superpowers workflows into Gemini CLI extensions or designing Gemini CLI command prompts that emulate multi-step agent workflows - covers extension layout, GEMINI.md context, command TOML patterns, and enforceable guardrails (tests/CI/pre-commit)
---

# Gemini CLI Extension Porting (Beads + Superpowers)

## Overview

Turn skills-based workflows into Gemini CLI extensions by mapping each workflow stage to a command, centralizing shared context in `GEMINI.md`, and backing prompt-only rules with repository guardrails.

## When to Use

- When converting Superpowers or beads workflows into Gemini CLI extension commands
- When designing `/namespace:command` flows with explicit artifacts and verification
- When you need TDD and quality gates enforced beyond prompt instructions
- When wiring MCP tools or shell commands into Gemini CLI workflows

## Core Principles

1. **Command-first, no hooks**: Invoke commands explicitly and document startup steps in `GEMINI.md`.
2. **Soft + hard enforcement**: Define the workflow in prompts and enforce it with CI/pre-commit.
3. **Small, composable commands**: Keep each command focused on one stage or artifact.
4. **Single source of truth**: Persist specs, plans, and checkpoints in files instead of chat history.

## Extension Skeleton (Pattern)

```
my-extension/
  gemini-extension.json
  GEMINI.md
  commands/
    superpowers/
      brainstorm.toml
      write-plan.toml
      execute-plan.toml
    beads/
      ready.toml
      show.toml
      update.toml
```

## Pattern: Map Skills to Commands

1. Inventory the entrypoints, artifacts, and success criteria in beads and Superpowers.
2. Define command names and expected outputs for each stage.
3. Write each command prompt to:
   - Load required context files
   - Run required tools or shell commands
   - Update artifacts (specs, plans, checkpoints)
   - Halt on failed tool calls or missing inputs
4. Keep naming consistent with existing skill namespaces (e.g., `superpowers`, `beads`).

## Pattern: Persistent Context in `GEMINI.md`

- Document the workflow rules and startup checklist (e.g., “Run `/beads:ready` at session start”).
- List required files, artifact paths, and expected status markers.
- Describe guardrails and when to stop for user confirmation.

## Pattern: Enforce TDD and Quality Gates

- In prompts, require Red/Green/Refactor and explicit test runs per task.
- In the repo, add hard gates (pre-commit + CI) for lint, type-check, tests, and coverage.
- Require plan updates and commit checkpoints after each task/phase.

## Pattern: Tool Wiring

- Configure MCP servers in `.gemini/settings.json` (workspace or user scope).
- Document required tools and environment variables in `GEMINI.md`.

## Common Workflow: Port Beads + Superpowers

```
1. Read the source skills and list core commands/artifacts.
2. Scaffold the extension and draft `GEMINI.md`.
3. Implement command TOMLs for brainstorm, plan, execute, and beads sync.
4. Add CI/pre-commit guardrails and verify they fail when tests fail.
5. Install the extension locally and confirm commands appear in `/help`.
```

## Integration with Other Skills

### With `model-mediated-development`
Use the model-mediated lens to keep decisions in prompts and logic in code.

### With `orchestrating-tmux-claudes` or `orchestrating-tmux-codex`
Use tmux orchestration when you need parallel execution or review of plan tasks.

### With `workspace-cleanup`
Reduce context noise before writing `GEMINI.md` or reading large repos.

## Checklist

- [ ] Inventory source skills and artifacts
- [ ] Define command namespaces and file layout
- [ ] Write `GEMINI.md` shared context
- [ ] Implement command TOMLs with clear stop conditions
- [ ] Add CI/pre-commit gates and test scripts
- [ ] Install and verify extension commands

## References

- https://geminicli.com/docs/extensions/
- https://geminicli.com/docs/cli/commands/
- https://github.com/google-gemini/gemini-cli
- https://github.com/obra/superpowers
- /Users/braydon/projects/experiments/tmux-beads-loops/skills/beads/SKILL.md
