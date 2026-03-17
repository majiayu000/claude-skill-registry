---
name: serena
description: |
  Semantic code understanding with IDE-like symbol operations. Use when: (1) Large codebase analysis (>50 files), (2) Symbol-level operations (find, rename, refactor), (3) Cross-file reference tracking, (4) Project memory and session persistence, (5) Multi-language semantic navigation. Triggers: "find symbol", "rename function", "find references", "symbol overview", "project memory". IMPORTANT: Prioritize Serena's symbolic tools over file-based grep/read for code exploration.
---

# Serena - Semantic Code Understanding

IDE-like semantic code operations via CLI. Provides symbol-level code navigation, editing, and project memory.

## Prerequisites

```bash
pip install serena-agent typer pyyaml
```

## Quick Start

**First-time setup**: Launch the Web Dashboard to initialize and register the project:

```bash
python -m tools dashboard serve --open-browser
```

This will:
- Initialize Serena configuration
- Register the current project in `~/.serena/serena_config.yml`
- Open the Web Dashboard for monitoring and configuration

**Configuration**: Edit `.env` file in `skills/serena/` directory:
```bash
SERENA_CONTEXT=claude-code
SERENA_MODES=interactive,editing,onboarding
SERENA_PROJECT=.
```

## Usage

### Basic Command Structure

```bash
python -m tools [GLOBAL OPTIONS] <command> [COMMAND OPTIONS]
```

**Global Options** (must be specified before the command):
- `-p, --project PATH` - Project directory (default: current directory, env: SERENA_PROJECT)
- `-c, --context TEXT` - Execution context (auto-detected if not specified, env: SERENA_CONTEXT)
- `-m, --mode TEXT` - Operation modes (can be specified multiple times, env: SERENA_MODES)

### Working with Different Projects

**Important**: When working with projects in different locations (especially cross-drive on Windows), use `--project`:

```bash
# Correct: Use --project for different project locations
python -m tools --project "/path/to/project" symbol find MyClass
python -m tools --project "E:\MyProject" file search "pattern"

# Incorrect: Don't use --path with absolute paths from different drives
python -m tools file search "pattern" --path "E:\MyProject"  # Will fail!
```

The `--path` option in subcommands expects **relative paths** within the project. Always use `--project` to set the project root first.

### Common Operations

```bash
# Dashboard
python -m tools dashboard serve --open-browser
python -m tools dashboard info

# Symbol operations
python -m tools symbol find MyClass --body
python -m tools symbol overview src/main.py
python -m tools symbol refs MyClass/method
python -m tools symbol rename OldName NewName --path src/file.py

# Memory operations
python -m tools memory list
python -m tools memory read project_overview
python -m tools memory write api_notes --content "..."

# File operations
python -m tools file list --recursive
python -m tools file find "**/*.py"
python -m tools file search "TODO:.*" --path src

# Extended tools
python -m tools cmd run "git status"
python -m tools config read config.json
```

## Tool Routing Policy

### Prefer Serena Over Built-in Tools

| Task | Avoid | Use Serena CLI |
|------|-------|----------------|
| Find function | `grep "def func"` | `symbol find func --body` |
| List file structure | `cat file.py` | `symbol overview file.py` |
| Find usages | `grep "func("` | `symbol refs func` |
| Edit function | `Edit` tool | `symbol replace func --path file.py` |
| Rename | Manual find/replace | `symbol rename old new --path file.py` |

### When to Use Built-in Tools
- Simple text search (non-code patterns)
- Configuration files (JSON, YAML)
- Documentation files (Markdown)

## Command Reference

### Dashboard Commands
| Command | Description |
|---------|-------------|
| `dashboard serve [--open-browser] [--browser-cmd <path>]` | Start Web Dashboard server |
| `dashboard info` | Show current configuration |
| `dashboard tools` | List active and available tools |
| `dashboard modes` | List active and available modes |
| `dashboard contexts` | List active and available contexts |

### Symbol Commands
| Command | Description |
|---------|-------------|
| `symbol find <name> [--body] [--depth N] [--path file]` | Find symbols by name |
| `symbol overview <path>` | List all symbols in file |
| `symbol refs <name> [--path file]` | Find symbol references |
| `symbol replace <name> --path <file> --body <code>` | Replace symbol body |
| `symbol insert-after <name> --path <file> --content <code>` | Insert after symbol |
| `symbol insert-before <name> --path <file> --content <code>` | Insert before symbol |
| `symbol rename <name> <new> --path <file>` | Rename symbol |

### Memory Commands
| Command | Description |
|---------|-------------|
| `memory list` | List all memories |
| `memory read <name>` | Read memory content |
| `memory write <name> --content <text>` | Create/update memory |
| `memory edit <name> --content <text>` | Edit memory |
| `memory delete <name>` | Delete memory |

### File Commands
| Command | Description |
|---------|-------------|
| `file list [--path dir] [--recursive]` | List directory |
| `file find <pattern>` | Find files by glob pattern |
| `file search <pattern> [--path dir]` | Search for regex pattern |

### Extended Commands
| Command | Description |
|---------|-------------|
| `cmd run <command> [--cwd dir] [--timeout N]` | Execute shell command |
| `cmd script <path> [--args "..."]` | Execute script file |
| `config read <path> [--format json\|yaml]` | Read config file |
| `config update <path> <key> <value>` | Update config value |

### Workflow Commands
| Command | Description |
|---------|-------------|
| `workflow onboarding` | Run project onboarding |
| `workflow check` | Check onboarding status |
| `workflow tools [--scope all]` | List available tools |

## Workflow Examples

### Phase 1: Exploration
```bash
python -m tools symbol overview src/main.py           # Understand file structure
python -m tools symbol find MyClass --depth 1         # Explore class members
python -m tools symbol find MyClass/method --body     # Get implementation details
```

### Phase 2: Analysis
```bash
python -m tools symbol refs MyClass/method            # Impact analysis
python -m tools memory list                           # Check project knowledge
python -m tools memory read architecture              # Retrieve context
```

### Phase 3: Modification
```bash
python -m tools symbol find target --body             # Verify target
python -m tools symbol replace target --path f --body "..."  # Edit
python -m tools symbol rename old new --path f        # Refactor
```

## Error Handling

All CLI output is JSON:

```json
// Success
{"result": <data>}

// Error
{"error": {"code": "ERROR_CODE", "message": "description"}}
```

| Error Code | Recovery |
|------------|----------|
| `INVALID_ARGS` | Check `--help` |
| `TOOL_NOT_FOUND` | Use `workflow tools` |
| `INIT_FAILED` | Check serena-agent installation |
| `RUNTIME_ERROR` | Check error message |

## Anti-Patterns

| Prohibited | Correct |
|------------|---------|
| Read entire file to find function | `symbol find func --body` |
| Grep for function calls | `symbol refs func` |
| Manual search-replace rename | `symbol rename old new --path f` |
| Skip impact analysis | `symbol refs` before editing |
