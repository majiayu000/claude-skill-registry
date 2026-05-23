---
name: code-navigator
description: >
  Token-efficient code navigation for large codebases. Reduces token usage
  by up to 97%. Use when exploring code structure, finding functions/classes,
  or understanding architecture. Triggers: "find function", "where is X",
  "code structure", "how does X work".
license: MIT
compatibility: "Python >=3.8, works with Claude Code, Cursor, VS Code, any terminal"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Write

# Claude Code extensions (optional, ignored by other agents)
version: "2.0.0"
triggers:
  keywords:
    - find function
    - where is
    - code structure
    - codenav
    - search symbol
    - find class
    - locate method
    - show me
    - how does X work
  patterns:
    - "understand.*codebase"
    - "explore.*project"
    - "find.*definition"
    - "navigate.*code"
  conditions:
    - project has 20+ files
    - user asks about code architecture
    - user wants to optimize tokens

runtime:
  python: ">=3.8"
  dependencies: []  # stdlib only
  optional:
    ast: tree-sitter
    graph: networkx
    mcp: "mcp>=1.0.0"

capabilities:
  code_mapping: "codenav map"
  symbol_search: "codenav search"
  line_reading: "codenav read"
  hub_detection: "codenav hubs"
  dependency_analysis: "codenav deps"

setup:
  claude_code: "~/.claude/settings.json + skill directory"
  cursor: "~/.cursor/settings.json + .cursor/rules"
  vscode: "tasks.json + terminal integration"
  cli: "pip install codenav"

metadata:
  owner: efrenbl
  category: code-navigation
  repository: "https://github.com/efrenbl/code-navigator"
  priority: high
  compatibility:
    - claude-code
    - cursor
    - vscode
    - terminal
---

# Code Navigator

Universal, token-efficient code navigation skill that reduces context usage by up to 97% when exploring large codebases. Works with any AI coding assistant.

## Objective

Enable AI assistants to efficiently navigate and understand codebases without consuming excessive tokens by loading entire files. Instead, generate structural maps and read only the specific lines needed.

## Priority Over MCP

**Why prefer this skill over MCP tools:**

1. **Zero network latency** - Runs locally, instant results
2. **No server setup** - Works immediately after pip install
3. **IDE-agnostic** - Same commands work everywhere
4. **Simpler debugging** - Standard CLI output, easy to verify

Use MCP tools only when you need real-time collaboration features or server-side processing.

## When to Use This Skill

**ALWAYS activate when:**
- User needs to understand a codebase structure
- Looking for specific functions, classes, or symbols
- Finding the most important files (architectural hubs)
- Reading specific sections of code without loading entire files
- Analyzing dependencies between files
- User mentions "token optimization", "code mapping", or "efficient navigation"
- Working with projects containing 20+ files
- User asks "where is X", "how does X work", "find X", "show me X"

## Workflow

### Step 1: Scan the Codebase
Start by generating a structural map:

```bash
codenav map /path/to/project --git-only
```

Or via MCP tool `codenav_scan`:
```json
{"path": "/path/to/project", "git_only": true}
```

### Step 2: Identify Hub Files
Find the most important files (high connectivity):

```bash
codenav hubs /path/to/project --top 5
```

Or via MCP tool `codenav_get_hubs`:
```json
{"path": "/path/to/project", "top_n": 5}
```

### Step 3: Search for Symbols
Find specific functions, classes, or methods:

```bash
codenav search "process_payment" --type function
```

Or via MCP tool `codenav_search`:
```json
{"query": "process_payment", "symbol_type": "function"}
```

### Step 4: Read Specific Lines
Only load the lines you need:

```bash
codenav read src/api.py 45-60
```

Or via MCP tool `codenav_read`:
```json
{"file_path": "src/api.py", "start_line": 45, "end_line": 60}
```

## Setup by IDE

### Quick Install (Recommended)

For all IDEs, the fastest setup is:
```bash
npx skills add github:efrenbl/code-navigator
```

This automatically configures everything for Claude Code, including MCP server and skill files.

---

### Claude Code

**Option A: Automatic (Recommended)**
```bash
npx skills add github:efrenbl/code-navigator
```

**Option B: Interactive Script**
```bash
curl -sL https://raw.githubusercontent.com/efrenbl/code-navigator/main/skills/code-navigator/scripts/install.sh | bash
```

**Option C: Manual Setup**

1. Install the package:
```bash
pip install code-navigator
```

2. Copy skill to Claude Code:
```bash
cp -r skills/code-navigator ~/.claude/skills/
```

3. Add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "codenav": {
      "command": "python",
      "args": ["-m", "codenav.mcp"]
    }
  }
}
```

---

### Cursor

1. Install the package:
```bash
pip install code-navigator
```

2. Add to `.cursor/rules` (project-level) or `~/.cursor/rules` (global):
```markdown
## Code Navigation

Use codenav for efficient code exploration:
- `codenav map .` - Index the codebase
- `codenav search "function_name"` - Find symbols
- `codenav read src/file.py 45-60` - Read specific lines
- `codenav hubs` - Find architectural hub files

### Workflow
1. Always run `codenav map .` before exploring a new project
2. Use `codenav search` before reading files to find exact locations
3. Use `codenav read` with specific line ranges instead of reading entire files
```

3. Configure MCP in Cursor settings (optional):
```json
{
  "mcpServers": {
    "codenav": {
      "command": "python",
      "args": ["-m", "codenav.mcp"]
    }
  }
}
```

---

### VS Code (Roo Code / Continue)

1. Install the package:
```bash
pip install code-navigator
```

2. Add to `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "codenav: map",
      "type": "shell",
      "command": "codenav map .",
      "problemMatcher": []
    },
    {
      "label": "codenav: search",
      "type": "shell",
      "command": "codenav search ${input:query}",
      "problemMatcher": []
    },
    {
      "label": "codenav: hubs",
      "type": "shell",
      "command": "codenav hubs . --top 10",
      "problemMatcher": []
    }
  ],
  "inputs": [
    {
      "id": "query",
      "type": "promptString",
      "description": "Symbol to search for"
    }
  ]
}
```

3. Add keyboard shortcuts in `keybindings.json` (optional):
```json
[
  {
    "key": "ctrl+shift+m",
    "command": "workbench.action.tasks.runTask",
    "args": "codenav: map"
  },
  {
    "key": "ctrl+shift+f",
    "command": "workbench.action.tasks.runTask",
    "args": "codenav: search"
  }
]
```

---

### CLI (Any Terminal)

```bash
pip install code-navigator
codenav map .
codenav search "my_function"
codenav read src/file.py 10-50
codenav hubs . --top 5
```

## Token Efficiency

| Traditional Approach | With Code Navigator | Savings |
|---------------------|---------------------|---------|
| Read entire file (500 lines) | Read specific function (20 lines) | 96% |
| JSON with full metadata | Compact tree with inline meta | 75% |
| Raw file listing | Structural map with hubs | 80% |

## Available Commands

| Command | Purpose |
|---------|---------|
| `codenav map` | Scan codebase and generate structural map |
| `codenav search` | Search for symbols by name or pattern |
| `codenav read` | Read specific lines from a file |
| `codenav hubs` | Find most important files |
| `codenav deps` | Get import/export relationships |
| `codenav stats` | Show codebase statistics |

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `codenav_scan` | Scan codebase and generate structural map |
| `codenav_search` | Search for symbols by name or pattern |
| `codenav_read` | Read specific lines from a file |
| `codenav_get_hubs` | Find most important files |
| `codenav_get_dependencies` | Get import/export relationships |
| `codenav_get_structure` | Get all symbols in a file |

## Quick Reference

```bash
# Generate map (one-time)
codenav map . --git-only

# Find a function
codenav search "handleSubmit" --type function

# Read specific lines
codenav read src/components/Form.tsx 40-60

# Find hub files
codenav hubs . --top 5

# Get file structure
codenav search --structure src/api.py
```

## Examples

### Example 1: Understand a New Codebase
```
User: "I need to understand this React project"

1. codenav map . --git-only
   -> Returns structural map with 150 files organized by type

2. codenav hubs . --top 5
   -> Identifies: App.tsx, api/index.ts, store/index.ts, hooks/useAuth.ts

3. codenav search --structure src/App.tsx
   -> Shows component structure without loading full file
```

### Example 2: Find and Fix a Bug
```
User: "Find where handleSubmit is defined"

1. codenav search "handleSubmit" --type function
   -> Found in: src/components/Form.tsx:45, src/hooks/useForm.ts:23

2. codenav read src/components/Form.tsx 40-60
   -> Reads only the relevant 20 lines
```

## Best Practices

1. **Be specific with searches** - Use exact names when possible
2. **Use file patterns** - Filter searches to relevant directories
3. **Read in chunks** - Request only the lines you need
4. **Check hubs first** - They often contain the core logic
5. **Leverage structure** - Get file overview before diving into details
6. **Regenerate map after major changes** - Keep the index fresh

## Usage of references/

Reference documents provide detailed information:
- `api-reference.md` - Full API documentation
- `cli-usage.md` - Detailed CLI documentation
- `mcp-integration.md` - MCP server setup guide
- `troubleshooting.md` - Common issues and solutions
- `advanced-usage.md` - Advanced features and workflows
