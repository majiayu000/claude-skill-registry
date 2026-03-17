
<!-- name: vscode-bridge
description: >-
  Drive VS Code programmatically via a local JSON-RPC WebSocket bridge.
  Use when you need to read/edit files through VS Code, list and fix diagnostics,
  run tasks and tests, perform refactors (rename, code actions, organize imports),
  navigate code (definitions, references, symbols, hover), format documents,
  manage debug sessions, execute notebook cells, or control the VS Code UI.
  Ideal for agentic coding workflows where you want the editor's full language
  intelligence instead of raw text manipulation.
license: Apache-2.0
compatibility: >-
  Requires VS Code (or compatible editor) with the AI-Native Bridge extension
  installed and running. Works on macOS, Linux, and Windows. Node.js 18+ for
  the CLI controller; Python 3.10+ for the async SDK.
metadata:
  author: Harkirat155
  version: "1.0"
  repo: https://github.com/Harkirat155/ai-native -->

# VS Code Bridge Skill

Expose VS Code's full capabilities — diagnostics, code actions, refactoring,
formatting, tasks, debugging, notebooks, and UI helpers — to any AI agent via
a local JSON-RPC WebSocket API.

## When to use this skill

Use this skill when:

- You are working inside a VS Code workspace and need **editor-native
  intelligence** (language server diagnostics, code actions, symbol navigation)
  rather than raw file I/O.
- You want to **fix lint errors** automatically using the same code actions a
  human would use in the editor.
- You need to **rename symbols** safely across an entire project.
- You want to **run tasks and tests** defined in the workspace.
- You need **transactional edits** with preview-before-commit and rollback.

## Prerequisites & installation

### Quick check

```bash
vscode-bridge doctor
```

If the command is not found or fails, install the bridge:

### Bootstrap install (macOS / Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/Harkirat155/ai-native/main/scripts/bootstrap.sh | bash -s -- --workspace "$PWD"
```

### Bootstrap install (Windows / PowerShell)

```powershell
iex "& { $(iwr -useb https://raw.githubusercontent.com/Harkirat155/ai-native/main/scripts/bootstrap.ps1) } -Workspace '$pwd'"
```

Alternatively, run the helper script bundled with this skill:

```bash
bash vscode-bridge/scripts/bootstrap.sh
```

After installation, reload the VS Code window so the extension activates.

## Connecting to the bridge

The bridge runs a WebSocket server on `ws://127.0.0.1:<port>` (default port:
`57110`). Authentication uses a pairing token.

**Token resolution order:**

1. `--token` CLI flag
2. `$BRIDGE_TOKEN` (or `$TOKEN`) environment variable
3. `--token-file` CLI flag
4. `.vscode/bridge.token` file in the workspace root (default)

## Core workflow

Always start with these two steps:

### 1. Health check

```bash
vscode-bridge doctor
```

This verifies: VS Code is running, the extension is loaded, WebSocket is
reachable, and the token is valid.

### 2. Discover capabilities

```bash
vscode-bridge --method bridge.capabilities
```

Returns the full list of available methods and events.

## Key methods

### Diagnostics (lint errors, warnings)

```bash
# List all diagnostics in the workspace
vscode-bridge --method diagnostics.list

# Preview available fixes for a diagnostic
vscode-bridge --method diagnostics.fix.preview \
  --params '{"uri":"file:///path/to/file.ts","diagnosticRange":{"start":{"line":5,"character":0},"end":{"line":5,"character":10}}}'

# Apply a fix
vscode-bridge --method diagnostics.fix.commit \
  --params '{"uri":"file:///path/to/file.ts","diagnosticRange":{"start":{"line":5,"character":0},"end":{"line":5,"character":10}},"actionIndex":0}'
```

### Document operations

```bash
# Read a file through VS Code (gets language ID, version)
vscode-bridge --method doc.read --params '{"uri":"file:///path/to/file.ts"}'

# Format a document
vscode-bridge --method doc.format --params '{"uri":"file:///path/to/file.ts"}'

# Apply text edits (direct)
vscode-bridge --method doc.applyEdits \
  --params '{"uri":"file:///path/to/file.ts","edits":[{"range":{"start":{"line":0,"character":0},"end":{"line":0,"character":0}},"newText":"// hello\n"}]}'
```

### Refactoring

```bash
# Rename a symbol across the project
vscode-bridge --method refactor.rename \
  --params '{"uri":"file:///path/to/file.ts","position":{"line":10,"character":5},"newName":"newSymbolName"}'

# List available code actions at a range
vscode-bridge --method refactor.codeActions \
  --params '{"uri":"file:///path/to/file.ts","range":{"start":{"line":5,"character":0},"end":{"line":5,"character":20}}}'

# Apply a specific code action
vscode-bridge --method refactor.codeActions.apply \
  --params '{"uri":"file:///path/to/file.ts","range":{"start":{"line":5,"character":0},"end":{"line":5,"character":20}},"index":0}'

# Organize imports
vscode-bridge --method refactor.organizeImports --params '{"uri":"file:///path/to/file.ts"}'

# Fix all auto-fixable issues
vscode-bridge --method refactor.fixAll --params '{"uri":"file:///path/to/file.ts"}'
```

### Code navigation

```bash
# Go to definition
vscode-bridge --method code.definitions \
  --params '{"uri":"file:///path/to/file.ts","position":{"line":10,"character":5}}'

# Find all references
vscode-bridge --method code.references \
  --params '{"uri":"file:///path/to/file.ts","position":{"line":10,"character":5}}'

# Document symbols (outline)
vscode-bridge --method code.symbols.document --params '{"uri":"file:///path/to/file.ts"}'

# Workspace-wide symbol search
vscode-bridge --method code.symbols.workspace --params '{"query":"MyClass"}'

# Hover info
vscode-bridge --method code.hover \
  --params '{"uri":"file:///path/to/file.ts","position":{"line":10,"character":5}}'
```

### Tasks and tests

```bash
# List available tasks
vscode-bridge --method tasks.list

# Run a task by label
vscode-bridge --method tasks.run --params '{"label":"build"}'

# Run and capture output
vscode-bridge --method tasks.run.capture --params '{"label":"test"}'

# Terminate a running task
vscode-bridge --method tasks.terminate --params '{"label":"build"}'
```

### Transactional edits (preview → commit / rollback)

For multi-file changes, use transactions to preview diffs before applying:

```bash
# Begin a transaction
vscode-bridge --method tx.begin
# Returns: { "txId": "...", "createdAt": ... }

# Stage edits (preview mode)
vscode-bridge --method doc.applyEdits.preview \
  --params '{"txId":"<txId>","uri":"file:///path/to/file.ts","edits":[...]}'

# Preview all staged changes
vscode-bridge --method tx.preview --params '{"txId":"<txId>"}'

# Commit if satisfied
vscode-bridge --method tx.commit --params '{"txId":"<txId>"}'

# Or rollback
vscode-bridge --method tx.rollback --params '{"txId":"<txId>"}'
```

### Snapshots (checkpoint & restore)

```bash
# Create a git-stash snapshot before risky changes
vscode-bridge --method tx.snapshot.create

# Restore if something goes wrong
vscode-bridge --method tx.snapshot.restore \
  --params '{"snapshotId":"<id>","dangerouslyDiscardLocalChanges":true}'
```

### UI control

```bash
# Open a file in the editor
vscode-bridge --method ui.openFile --params '{"uri":"file:///path/to/file.ts"}'

# Show a quick-pick menu
vscode-bridge --method ui.quickPick --params '{"items":["Option A","Option B"]}'
```

### MCP compatibility

The bridge can also run as an MCP (Model Context Protocol) server over stdio:

```bash
vscode-bridge mcp
```

This exposes all bridge methods as MCP tools, enabling integration with any
MCP-compatible agent.

## Recommended agent workflow

1. **`vscode-bridge doctor`** — verify environment
2. **`bridge.capabilities`** — discover available methods
3. **`diagnostics.list`** → observe problems
4. **`refactor.codeActions`** / **`refactor.rename`** → fix using semantic tools
5. **`doc.format`** → clean up formatting
6. **`diagnostics.list`** → verify improvements

Prefer semantic operations (`refactor.*`, `diagnostics.fix.*`) over raw text
edits (`doc.applyEdits`) whenever possible — they are safer and produce
minimal, correct diffs.

## Edge cases & troubleshooting

- **Bridge not reachable**: Ensure VS Code is running and the extension is
  active. Run `vscode-bridge doctor` for diagnostics.
- **Token mismatch**: Delete `.vscode/bridge.token` and reload the VS Code
  window to regenerate.
- **Port conflict**: The default port is `57110`. If another process uses it,
  check the extension output for the actual port.
- **Stale diagnostics**: After applying fixes, wait ~1-2 seconds for the
  language server to recompute diagnostics before re-listing.

## Additional resources

- See [the protocol quick-reference](references/PROTOCOL-QUICK-REF.md) for
  a complete method listing with parameter shapes.
- Run `bash vscode-bridge/scripts/doctor.sh` for a quick health check.
- Run `bash vscode-bridge/scripts/call.sh <method> [params-json]` to call any
  bridge method.
