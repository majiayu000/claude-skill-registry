---
name: ralph-cli
description: "Consult Ralph CLI reference. Use when: User asks about commands, syntax, or options for Ralph CLI. Not for: Workflow design or execution monitoring."
---

# Ralph CLI: Command Reference

Complete reference for all Ralph CLI commands, options, and syntax.

## Quick Start

```bash
# Check Ralph version
ralph --version

# List all commands
ralph --help

# Initialize from preset
ralph init --list-presets
ralph init --preset feature

# Run orchestration
ralph run

# View events
ralph events --last 20
```

## Command Categories

| Category | Commands | Purpose |
|----------|----------|---------|
| **Execution** | `run`, `plan`, `code-task` | Run workflows, plan sessions, generate tasks |
| **State** | `events`, `emit` | View/emit event history |
| **Setup** | `init`, `clean` | Initialize configuration, cleanup artifacts |
| **Runtime Tools** | `tools memory`, `tools task` | Manage memories and tasks |
| **Parallel** | `loops` | Manage parallel loop workflows |

## Command Reference

### ralph run

Execute orchestration loop.

**Syntax:**
```bash
ralph run [OPTIONS]
```

**Common Options:**

| Option | Description |
|--------|-------------|
| `-p, --prompt <TEXT>` | Inline prompt text |
| `-P, --prompt-file <FILE>` | Prompt file path |
| `--record-session <FILE>` | Record session to JSONL file |
| `--continue` | Resume from existing scratchpad |
| `--dry-run` | Show what would execute without running |
| `--autonomous` | Force autonomous mode |
| `--no-tui` | Disable TUI mode |

**Examples:**
```bash
# Basic execution
ralph run

# With inline prompt
ralph run -p "Debug the login failure"

# With session recording
ralph run --record-session .ralph/session.jsonl

# Resume from checkpoint
ralph run --continue

# Dry run validation
ralph run --dry-run
```

**See**: `references/command-tables.md` for complete option table.

### ralph events

View event history for debugging.

**Syntax:**
```bash
ralph events [OPTIONS]
```

**Common Options:**

| Option | Description |
|--------|-------------|
| `--last <N>` | Show only last N events |
| `--topic <TOPIC>` | Filter by topic |
| `--iteration <N>` | Filter by iteration number |
| `--format <FORMAT>` | Output format: table, json |
| `--clear` | Clear event history |

**Examples:**
```bash
# Show recent events
ralph events --last 20

# Filter by topic
ralph events --topic "test.passed"

# JSON output
ralph events --format json | jq '.[] | {topic, iteration}'
```

### ralph init

Initialize configuration file.

**Syntax:**
```bash
ralph init [OPTIONS]
```

**Common Options:**

| Option | Description |
|--------|-------------|
| `--preset <NAME>` | Copy embedded preset to ralph.yml |
| `--list-presets` | List all available presets |
| `--backend <BACKEND>` | Backend to use |
| `--force` | Overwrite existing ralph.yml |

**Examples:**
```bash
# List presets
ralph init --list-presets

# Initialize from preset
ralph init --preset feature

# Initialize with backend
ralph init --preset debug --backend gemini
```

### ralph tools

Runtime tools for memory and task management.

**Syntax:**
```bash
ralph tools <COMMAND> [OPTIONS]
```

**Subcommands:**
- `memory` - Manage persistent memories
- `task` - Manage work items

#### ralph tools memory

**Memory Operations:**

```bash
# Add memory
ralph tools memory add "content" -t pattern --tags tag1,tag2

# List memories
ralph tools memory list --last 10

# Search memories
ralph tools memory search "query" --tags api

# Prime context
ralph tools memory prime --budget 2000

# Delete memory
ralph tools memory delete <id>
```

#### ralph tools task

**Task Operations:**

```bash
# Add task
ralph tools task add "Title" -p 1

# List tasks
ralph tools task list

# Show ready tasks
ralph tools task ready

# Close task
ralph tools task close <id>
```

### ralph loops

Manage parallel loop workflows.

**Syntax:**
```bash
ralph loops [COMMAND] [OPTIONS]
```

**Subcommands:**

```bash
# List all loops
ralph loops list

# View loop logs
ralph loops logs <LOOP_ID>

# Show loop history
ralph loops history <LOOP_ID>

# Merge completed loop
ralph loops merge <LOOP_ID>

# Discard failed loop
ralph loops discard <LOOP_ID> -y

# Clean up stale loops
ralph loops prune
```

### Other Commands

| Command | Description |
|---------|-------------|
| `ralph plan` | Start PDD planning session |
| `ralph code-task` | Generate code task files |
| `ralph emit` | Emit event to event log |
| `ralph clean` | Clean up artifacts |

## Output Formats

Most commands support `--format` option:

| Format | Use Case |
|--------|----------|
| `table` | Human-readable display (default) |
| `json` | Programmatic access, parsing |
| `quiet` | Scripting, minimal output |
| `markdown` | Documentation, specific commands |

**Example:**
```bash
# JSON output for parsing
ralph events --format json | jq '.[] | select(.topic == "test.passed")'

# Quiet output for scripting
ralph tools memory list --format quiet
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Command usage error |
| 124 | Timeout |
| 126 | Command not found |

## Global Options

Available for all commands:

| Option | Description |
|--------|-------------|
| `-c, --config` | Config file override |
| `-v, --verbose` | Enable verbose output |
| `--color` | Color mode: auto, always, never |
| `-h, --help` | Print help |
| `-V, --version` | Print version |

## See Also

- `references/command-tables.md` - Complete command tables with all options
- `references/syntax-examples.md` - Detailed syntax examples for each command
- `references/output-formats.md` - Output format specifications and parsing
- `references/cli-patterns.md` - Common CLI usage patterns and workflows

## Quick Reference

| Task | Command |
|------|---------|
| Start orchestration | `ralph run` |
| Monitor events | `ralph events --last 20` |
| List presets | `ralph init --list-presets` |
| Initialize project | `ralph init --preset feature` |
| Check status | `ralph events --topic "test"` |
| View tasks | `ralph tools task ready` |
| View memories | `ralph tools memory list` |
| Monitor loops | `ralph loops list` |
| Resume workflow | `ralph run --continue` |
| Validate config | `ralph run --dry-run` |
