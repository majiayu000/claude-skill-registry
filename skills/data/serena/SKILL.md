---
name: serena
description: |
  Semantic code understanding with IDE-like symbol operations. Use when: (1) Large codebase analysis (>50 files), (2) Symbol-level operations (find, rename, refactor), (3) Cross-file reference tracking, (4) Project memory and session persistence, (5) Multi-language semantic navigation. Triggers: "find symbol", "rename function", "find references", "symbol overview", "project memory". IMPORTANT: Prioritize Serena's symbolic tools over file-based grep/read for code exploration.
---

# Serena - Semantic Code Understanding

IDE-like semantic code operations via CLI. Provides symbol-level code navigation, editing, and project memory.

## Execution Methods

```bash
# Prerequisites: pip install serena-agent typer
# Environment: SERENA_PROJECT (default: current directory)

# Symbol operations
python -m skills.serena.tools symbol find MyClass --body
python -m skills.serena.tools symbol overview src/main.py
python -m skills.serena.tools symbol refs MyClass/method
python -m skills.serena.tools symbol rename OldName NewName --path src/file.py

# Memory operations
python -m skills.serena.tools memory list
python -m skills.serena.tools memory read project_overview
python -m skills.serena.tools memory write api_notes --content "..."

# File operations
python -m skills.serena.tools file list --recursive
python -m skills.serena.tools file find "**/*.py"
python -m skills.serena.tools file search "TODO:.*" --path src

# Extended tools
python -m skills.serena.tools cmd run "git status"
python -m skills.serena.tools config read config.json
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

## Workflow

### Phase 1: Exploration
```bash
symbol overview src/main.py           # Understand file structure
symbol find MyClass --depth 1         # Explore class members
symbol find MyClass/method --body     # Get implementation details
```

### Phase 2: Analysis
```bash
symbol refs MyClass/method            # Impact analysis
memory list                           # Check project knowledge
memory read architecture              # Retrieve context
```

### Phase 3: Modification
```bash
symbol find target --body             # Verify target
symbol replace target --path f --body "..."  # Edit
symbol rename old new --path f        # Refactor
```

## Error Handling

```json
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
