---
name: Smart Intent Detection
description: "Automatic workflow suggestion and utility agent routing based on prompt analysis. Trigger keywords: auto-detect, intent, suggest, trigger, routing, workflow detection, utility agents, prompt analysis, smart routing"
version: 1.0.0
---

# Smart Intent Detection

The ReAcTree plugin includes smart detection that analyzes your prompts and suggests appropriate workflows or utility agents automatically.

## How It Works

When you type a prompt, the system:

1. **Checks configuration** - Respects your enabled/disabled settings
2. **Filters noise** - Skips simple questions and explicit commands
3. **Detects utility intent** - Routes to specialized agents for file/code/git/log tasks
4. **Detects workflow intent** - Suggests feature/debug/refactor workflows
5. **Outputs suggestion** - Shows helpful message with recommended action

## Utility Agent Routing

### file-finder
**Triggers:** "find files", "where is file", "list directory", "show folder"

Fast file discovery using Glob and Grep:
- Find files by pattern (`**/*.rb`, `app/models/*.rb`)
- Find files by name or content
- List directory structure

### code-line-finder
**Triggers:** "where is defined", "find method", "find usages", "who calls"

Precise code location using LSP:
- Find method/class definitions with line numbers
- Find all usages and references
- Go to definition

### git-diff-analyzer
**Triggers:** "what changed", "show diff", "git blame", "commit history"

Git change analysis:
- Analyze staged/unstaged changes
- Compare branches
- Blame and history

### log-analyzer
**Triggers:** "show log", "development.log", "errors in log", "slow queries"

Rails log parsing:
- Parse development.log/production.log
- Find errors and stack traces
- Identify slow SQL queries

## Workflow Detection

### Feature Development
**Triggers:** implement, build, create, add, develop, user story

Suggests:
- `/reactree-dev` - Full parallel workflow
- `/reactree-feature` - Feature-driven with user stories

Strong indicators: User story format ("As a user, I want...")

### Debugging
**Triggers:** fix, debug, error, bug, not working, troubleshoot

Suggests:
- `/reactree-debug` - Systematic debugging workflow

Strong indicators: Error types (NoMethodError), stack traces, line numbers

### Refactoring
**Triggers:** refactor, cleanup, optimize, restructure, improve

Suggests:
- `/reactree-dev` - With refactor focus and test preservation

Strong indicators: "code smell", "technical debt", "decouple"

### TDD Mode
**Triggers:** test-first, TDD, with tests, ensure coverage

Adds TDD emphasis to feature suggestions.

## Configuration

Edit `.claude/reactree-rails-dev.local.md`:

```yaml
---
smart_detection_enabled: true  # Enable/disable
detection_mode: suggest        # suggest | inject | disabled
annoyance_threshold: medium    # low | medium | high
use_claude_analysis: true      # Use Claude CLI for intelligent intent analysis
---
```

## Detection Modes

### suggest (Default)
Shows a suggestion message. Non-intrusive - you can ignore and proceed.

### inject
Automatically activates the workflow with context injection.

### disabled
Turns off smart detection entirely. Use commands manually.

## Annoyance Thresholds

### low
Only triggers for very explicit keywords:
- "implement", "build", "create"
- "fix", "debug"
- "refactor"

### medium (Default)
Skips:
- Simple questions (what, how, why, etc.)
- Short prompts (<5 words)
- Informational requests

### high
Triggers for most Rails-related prompts with relevant keywords.

## When Detection Skips

- Commands already using `/reactree-*`, `/rails-*`
- Simple questions without action verbs
- Very short prompts (<5 words)
- Non-Rails context (no Rails keywords, not in Rails project)
- Informational/documentation requests

## Tips

1. **Be explicit** - "Implement user authentication" triggers better than "auth stuff"
2. **Include context** - Mention models, controllers, services for higher confidence
3. **Use keywords** - "fix", "build", "refactor" are strong signals
4. **User stories work** - "As a user, I want to..." strongly triggers feature mode
5. **Utility agents** - Ask for files/code/diffs/logs to trigger specialized agents
