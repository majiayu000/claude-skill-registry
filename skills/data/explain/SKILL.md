---
name: explain
description: Explain all bluera-base plugin functionality in human-readable format
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
---

# bluera-base Explained

User guide for the bluera-base plugin.

## Subcommands

- `/bluera-base:explain` or `/bluera-base:explain all` - Show everything
- `/bluera-base:explain overview` - What is bluera-base?
- `/bluera-base:explain features` - Configurable features
- `/bluera-base:explain commands` - Available commands
- `/bluera-base:explain behaviors` - Automatic behaviors
- `/bluera-base:explain config` - Configuration system
- `/bluera-base:explain philosophy` - Design principles

---

## Algorithm

**Present the documentation below to the user.** This is a documentation command - output the content directly, don't just acknowledge it.

### Show All (default)

Present all sections in order.

### Overview

Present only the Overview section.

### Features

Present only the Features section.

### Commands

Present only the Commands section.

### Behaviors

Present only the Automatic Behaviors section.

### Config

Present only the Configuration section.

### Philosophy

Present only the Philosophy section.

---

## Overview

### What is Bluera Base?

Bluera Base is a **conventions plugin** for Claude Code. It provides shared development workflows, quality gates, and patterns that you can use across all your projects. Instead of copying hooks and skills between repositories, install Bluera Base once and every project gets the same standards.

### What It Does

**Enforces quality patterns:**

- Blocks anti-patterns like `any` types, fallback code, and commented-out code
- Requires atomic commits with conventional format
- Prevents manual versioning (use the release workflow instead)

**Provides development workflows:**

- Atomic commit creation with README/CLAUDE.md awareness
- Multi-agent code review
- Iterative development loops (milhouse)
- Automated release cutting with CI monitoring

**Automates repetitive tasks:**

- Desktop notifications when Claude needs input
- Auto-commit on session end
- Duplicate code detection
- Lint and typecheck validation after edits

### Supported Languages

Bluera Base works with 13 languages:

JavaScript/TypeScript, Python, Rust, Go, Java, Kotlin, Ruby, PHP, C#/.NET, Swift, Elixir, C/C++, Scala

---

## Quick Start

### Install

```bash
# Add the Bluera marketplace (one-time)
/plugin marketplace add blueraai/bluera-marketplace

# Install the plugin
/plugin install bluera-base@bluera
```

### Configure

```bash
# Interactive setup - walks through each feature
/bluera-base:config init

# Or enable features individually
/bluera-base:config enable notifications
/bluera-base:config enable strict-typing
```

### Explore

```bash
# See all commands
/bluera-base:help

# See this documentation
/bluera-base:explain
```

---

## Features

Features are opt-in capabilities you can enable or disable. Each feature has a clear purpose and observable behavior.

### Desktop Notifications

**What it does:** Sends a desktop notification when Claude Code needs your input (permission prompts, questions, idle timeouts). Notifications include the **project name** so you know which project needs attention.

**Why you'd want it:** When you're multitasking in other windows, you won't miss Claude asking for permission or waiting on your response.

**How to use:**

```bash
/bluera-base:config enable notifications   # Enable
/bluera-base:config disable notifications  # Disable
```

**What you'll see:** Notifications like `"bluera-base - Permission Required"` with the project name in the title.

**Platform support:**

| Platform | Tool | Icon Support |
|----------|------|--------------|
| macOS | osascript (default) | No |
| macOS | terminal-notifier | Yes |
| Linux | notify-send | Yes |
| Windows | PowerShell toast | No |

**For icons on macOS**, install terminal-notifier:

```bash
brew install terminal-notifier
```

**To avoid duplicate notifications** (if you see two per event):

- **iTerm 2**: Preferences → Profiles → Terminal → Uncheck "Send Growl/Notification Center alerts"
- **VS Code / other terminals**: Usually don't send native notifications, so you'll only see ours

**Default:** Enabled

---

### Auto-Learn

**What it does:** Tracks commands you run frequently and suggests adding them to CLAUDE.md so Claude remembers them in future sessions.

**Why you'd want it:** If you always run `bun test` after edits, or `git status` before commits, Claude can learn this and do it automatically.

**How to use:**

```bash
/bluera-base:config enable auto-learn      # Enable tracking
/bluera-base:config set .autoLearn.mode suggest  # Suggest updates (default)
/bluera-base:config set .autoLearn.mode auto     # Auto-apply updates
```

**What you'll see:** At session end, suggestions for CLAUDE.md updates based on patterns observed. In auto mode, updates are applied directly.

**Default:** Disabled

---

### Auto-Commit

**What it does:** Prompts you to commit uncommitted changes when your Claude session ends, using the atomic commit workflow.

**Why you'd want it:** Never lose work because you forgot to commit before ending a session. You can then commit changes with proper conventional commit messages.

**How to use:**

```bash
/bluera-base:config enable auto-commit     # Prompt on session end
/bluera-base:config enable auto-push       # Add push instruction to prompt
```

**What you'll see:** When you end a session with uncommitted changes, you're prompted to run `/bluera-base:commit` (and optionally push).

**Default:** Disabled

---

### DRY Check

**What it does:** Detects duplicate/copy-paste code in your codebase using jscpd.

**Why you'd want it:** Catch copy-paste code before it becomes a maintenance burden. See exactly which files have duplicated logic.

**How to use:**

```bash
/bluera-base:config enable dry-check       # Enable the feature
/bluera-base:dry scan                      # Manual scan
/bluera-base:config enable dry-auto        # Auto-scan on session end
```

**What you'll see:** A report showing duplicate code blocks, their locations, and suggestions for refactoring.

**Default:** Disabled

---

### Strict Typing

**What it does:** Blocks unsafe type patterns when you edit files:

- **TypeScript:** `any` type, `as` casts (except `as const`), `@ts-ignore` without explanation
- **Python:** `Any` type, `# type: ignore` without error code, `cast()`

**Why you'd want it:** Catch type safety issues at edit time, not at runtime. Forces explicit typing decisions.

**How to use:**

```bash
/bluera-base:config enable strict-typing
```

**What you'll see:** When you edit a file with forbidden patterns, Claude is notified and asked to fix them.

**Escape hatch:** Add `// ok:` (TypeScript) or `# ok:` (Python) comment on specific lines when truly unavoidable.

**Default:** Disabled

---

### Milhouse Loop

**What it does:** Runs iterative development loops where Claude continues working through a prompt file, iteration after iteration, until a completion condition is met.

**Why you'd want it:** For tasks that require multiple passes (refactoring, test-driven development, migrations), milhouse keeps working without you re-prompting each time.

**How to use:**

```bash
/bluera-base:milhouse-loop prompt.md --promise "all tests pass" --gate "bun test"
/bluera-base:cancel-milhouse  # Stop an active loop
```

**What you'll see:** Claude works through iterations, running gate commands between each. Stops when the promise is fulfilled or max iterations reached.

**Configuration:**

```bash
/bluera-base:config set .milhouse.defaultMaxIterations 10  # Limit iterations
/bluera-base:config set .milhouse.defaultStuckLimit 3      # Ask if stuck after 3 no-progress iterations
```

**Default:** Unlimited iterations, stuck limit 3

---

## Commands

Commands are organized by category. All commands are prefixed with `/bluera-base:` (e.g., `/bluera-base:commit`).

### Getting Started

| Command | Purpose |
|---------|---------|
| `/init` | Initialize a new project with bluera-base conventions |
| `/config` | Manage plugin settings (show, init, enable, disable, set, reset) |
| `/help` | Show available commands and features |
| `/explain` | This documentation |

### Development

| Command | Purpose |
|---------|---------|
| `/commit` | Create atomic commits with README/CLAUDE.md awareness |
| `/milhouse-loop` | Start an iterative development loop |
| `/cancel-milhouse` | Stop an active milhouse loop |
| `/todo` | Manage project TODO tasks |
| `/learn` | Manage learnings from session analysis |
| `/checklist` | Manage project checklist |

### Quality

| Command | Purpose |
|---------|---------|
| `/code-review` | Multi-agent codebase review with confidence scoring |
| `/dry` | Detect duplicate code and suggest DRY refactors |
| `/clean` | Diagnose slow Claude Code startup and guide cleanup |
| `/large-file-refactor` | Break apart files exceeding token limits |

### Documentation

| Command | Purpose |
|---------|---------|
| `/claude-md` | Audit and maintain CLAUDE.md files |
| `/readme` | Maintain README.md with GitHub advanced formatting |

### Project Setup

| Command | Purpose |
|---------|---------|
| `/harden-repo` | Set up linters, formatters, git hooks (13 languages) |
| `/install-rules` | Install rule templates to `.claude/rules/` |

### Release

| Command | Purpose |
|---------|---------|
| `/release` | Cut a release with conventional commits and CI monitoring |

### Git

| Command | Purpose |
|---------|---------|
| `/worktree` | Manage Git worktrees for parallel development |
| `/statusline` | Configure terminal status line display |

### Meta

| Command | Purpose |
|---------|---------|
| `/analyze-config` | Scan `.claude/**` for overlap with bluera-base |
| `/audit-plugin` | Audit a plugin against best practices |
| `/test-plugin` | Run plugin validation test suite |

---

## Automatic Behaviors

These behaviors happen automatically without you invoking a command. They run in the background based on your actions.

### Anti-Pattern Detection

**When:** Every time you edit a file (Write or Edit tool)

**What happens:** The plugin scans your changes for forbidden patterns:

- `any` type, `as` casts (when strict-typing enabled)
- Fallback code, graceful degradation patterns
- Backward compatibility shims
- Commented-out code

**What you'll see:** If a pattern is detected, Claude is notified and typically fixes it before continuing.

---

### Release Protection

**When:** You try to run `npm version`, `git tag`, or similar versioning commands

**What happens:** The command is blocked with a message to use `/bluera-base:release` instead.

**Why:** Manual versioning bypasses the release workflow, which handles CHANGELOG generation, CI monitoring, and proper tag creation.

---

### Auto-Validation

**When:** You edit JavaScript, TypeScript, Python, Rust, or Go files

**What happens:** Lint and typecheck commands run automatically to catch issues early.

**What you'll see:** If lint/typecheck fails, Claude is notified and can fix the issues.

---

### Context Preservation

**When:** Claude's context is about to be compacted (long conversations)

**What happens:** Important state is preserved so milhouse loops and other features continue working after compaction.

**What you'll see:** Nothing - this happens transparently. Your milhouse loops and feature states survive compactions.

---

## Configuration

### Config Files

Configuration is stored in `.bluera/bluera-base/` in your project:

| File | Purpose | Git Status |
|------|---------|------------|
| `config.json` | Team settings (shared conventions) | Committed |
| `config.local.json` | Personal overrides | Gitignored |

Settings merge in order: defaults → `config.json` → `config.local.json`

### Feature Toggles

| Feature | What It Does | Default |
|---------|--------------|---------|
| `notifications` | Desktop notifications when Claude needs input | ON |
| `auto-learn` | Track command patterns, suggest CLAUDE.md updates | OFF |
| `auto-commit` | Commit uncommitted changes on session stop | OFF |
| `auto-push` | Push to remote after auto-commit | OFF |
| `dry-check` | Enable duplicate code detection | OFF |
| `dry-auto` | Auto-scan for duplicates on session stop | OFF |
| `strict-typing` | Block any/as casts, type: ignore | OFF |

### Config Commands

```bash
# Show current configuration
/bluera-base:config show

# Interactive setup
/bluera-base:config init

# Enable/disable features
/bluera-base:config enable strict-typing
/bluera-base:config disable notifications

# Set specific values
/bluera-base:config set .milhouse.defaultMaxIterations 10
/bluera-base:config set .autoLearn.mode auto

# Reset to defaults
/bluera-base:config reset          # Remove personal overrides
/bluera-base:config reset --all    # Remove all config
```

---

## Philosophy

Bluera Base is opinionated. Here's why.

### Fail Fast

**Principle:** Errors should be visible immediately, not hidden.

When something goes wrong, you should know about it right away. Silent failures lead to bugs discovered much later when they're harder to fix. Bluera Base blocks problematic patterns at edit time rather than letting them slip through.

### No Fallbacks

**Principle:** Code works as designed or fails visibly.

Fallback code, graceful degradation, and "just in case" defaults often hide bugs. If your code expects a value to exist, it should fail if it doesn't - not silently use a default that may or may not be correct. This makes bugs obvious instead of subtle.

### Atomic Commits

**Principle:** Each commit is one logical change.

A commit should do one thing. "Fix login bug" is good. "Fix login bug and update README and refactor utils" is three commits. Atomic commits make git history useful for understanding what changed and why, and make reverts safe.

### Clean Code

**Principle:** If it's in the codebase, it runs.

No commented-out code "for reference." No deprecated functions kept "just in case." No unused exports. Dead code is noise that makes the codebase harder to understand. If you need old code, that's what git history is for.

### Strict Typing

**Principle:** Types are documentation that the compiler checks.

`any` and `as` casts defeat the purpose of TypeScript. They tell the compiler "trust me" when you should be telling it what to expect. Strict typing catches bugs at write time instead of runtime, and makes refactoring safe.
