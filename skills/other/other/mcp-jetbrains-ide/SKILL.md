---
name: mcp-jetbrains-ide
description: Control JetBrains IDE (IntelliJ, WebStorm, PyCharm) via MCP. Use when manipulating IDE files, running configurations, searching code, or performing refactoring. Triggers on "open in IDE", "run configuration", "refactor code", "IDE search", "JetBrains".
---

# JetBrains IDE Integration

MCP service at `http://localhost:64342/sse` (sse) with 22 tools.

## Requirements

- `mh` CLI must be installed. If not available, install with:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/vaayne/mcphub/main/scripts/install.sh | sh
  ```
- JetBrains IDE must be running with MCP plugin enabled

## Usage

List tools: `mh -u http://localhost:64342/sse -t sse list`
Get tool details: `mh -u http://localhost:64342/sse -t sse inspect <tool-name>`
Invoke tool: `mh -u http://localhost:64342/sse -t sse invoke <tool-name> '{"param": "value"}'`

## Notes

- Run `inspect` before invoking unfamiliar tools to get full parameter schema
- Timeout: 30s default, use `--timeout <seconds>` to adjust
- SSE port may vary - check IDE MCP plugin settings if connection fails
- All file paths are relative to project root unless absolute

## Tools

### File Operations

| Tool                  | Description                                                          |
| --------------------- | -------------------------------------------------------------------- |
| `createNewFile`       | Create a new file at specified path, auto-creates parent directories |
| `getFileTextByPath`   | Read file contents by project-relative path                          |
| `replaceTextInFile`   | Replace text in file with flexible find/replace options              |
| `reformatFile`        | Apply code formatting rules to a file                                |
| `openFileInEditor`    | Open a file in the IDE editor                                        |
| `getAllOpenFilePaths` | Get paths of all currently open files                                |

### Search

| Tool                     | Description                                       |
| ------------------------ | ------------------------------------------------- |
| `findFilesByNameKeyword` | Find files by name keyword (case-insensitive)     |
| `findFilesByGlob`        | Find files matching glob pattern (e.g. `**/*.ts`) |
| `searchInFilesByText`    | Search for text substring across project files    |
| `searchInFilesByRegex`   | Search with regex pattern across project files    |

### Code Intelligence

| Tool                | Description                                     |
| ------------------- | ----------------------------------------------- |
| `getSymbolInfo`     | Get documentation/info about symbol at position |
| `getFileProblems`   | Analyze file for errors and warnings            |
| `renameRefactoring` | Rename symbol across entire project             |

### Project

| Tool                     | Description                         |
| ------------------------ | ----------------------------------- |
| `listDirectoryTree`      | Tree view of directory structure    |
| `getProjectModules`      | List all project modules with types |
| `getProjectDependencies` | List all project dependencies       |
| `getRepositories`        | List VCS roots in project           |

### Execution

| Tool                      | Description                           |
| ------------------------- | ------------------------------------- |
| `getRunConfigurations`    | List available run configurations     |
| `executeRunConfiguration` | Run a specific run configuration      |
| `executeTerminalCommand`  | Execute shell command in IDE terminal |

### Other

| Tool               | Description               |
| ------------------ | ------------------------- |
| `permissionPrompt` | Permission prompt utility |

## Examples

```bash
# List project structure
mh -u http://localhost:64342/sse -t sse invoke listDirectoryTree '{"path": "."}'

# Search for text in files
mh -u http://localhost:64342/sse -t sse invoke searchInFilesByText '{"query": "TODO"}'

# Read a file
mh -u http://localhost:64342/sse -t sse invoke getFileTextByPath '{"path": "src/index.ts"}'

# Rename a symbol
mh -u http://localhost:64342/sse -t sse invoke renameRefactoring '{"path": "src/utils.ts", "line": 10, "column": 5, "newName": "newFunctionName"}'

# Run a configuration
mh -u http://localhost:64342/sse -t sse invoke executeRunConfiguration '{"name": "Run Tests"}'
```
