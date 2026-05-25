---
name: meta:cli-feature-creator
description: CLI Feature Creator wizard for adding new aaa CLI commands. Use when user asks to "add aaa command", "create CLI feature", "add CLI command", or needs to extend the aaa CLI with new functionality.
allowed-tools: Read, Write, Bash(mkdir:*)
---

# AAA CLI Feature Wizard

Wizard-style guide for adding new CLI features to the `aaa` command.

@context/workflows/aaa-cli-feature.md

## When to Use

- Adding a new `aaa <command>` subcommand
- Adding a new `aaa ralph plan <feature>` subcommand
- Adding new flags to existing commands
- Extending the CLI with new functionality

## Workflow

### 1. Gather Requirements

Ask about:
- Feature name
- Feature type (plan-subcommand, top-level, flag)
- Required arguments and optional flags
- Whether it needs auto mode

### 2. Create Files

Follow the workflow to create:
1. Prompt file (source of truth)
2. CLI command implementation
3. Shell completions (bash/zsh/fish)
4. E2E tests
5. Skill file (if auto-triggered)

### 3. Verify

Run verification checklist from workflow.

## References

- **Full workflow:** @context/workflows/aaa-cli-feature.md
- **CLI architecture:** @tools/CLAUDE.md
- **CLI stack:** @context/stacks/cli/cli-bun.md
