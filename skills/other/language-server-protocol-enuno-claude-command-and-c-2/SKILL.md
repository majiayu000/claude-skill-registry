---
name: language-server-protocol
version: "1.2.0"
description: Language Server Protocol (LSP) - Microsoft's open standard for IDE-language server communication. Use for building language servers, implementing LSP clients, understanding protocol architecture, and integrating code intelligence features.
specification_version: "3.17"
---

# Language Server Protocol Skill

The Language Server Protocol (LSP) is an open standard that defines the protocol used between an editor or IDE and a language server that provides language features like auto-complete, go to definition, find all references, and more. Think of LSP as **"USB-C for code intelligence"** - a standardized interface that allows any language server to work with any compatible editor.

**Core Value Proposition**: Build once, integrate everywhere. A single language server implementation works across VS Code, Neovim, Emacs, Sublime Text, and dozens of other editors without modification.

## When to Use This Skill

This skill should be triggered when:
- Building language servers for programming languages or DSLs
- Implementing LSP client support in editors or IDEs
- Understanding LSP protocol architecture and message flow
- Adding code intelligence features (completion, diagnostics, navigation)
- Debugging LSP communication issues
- Integrating existing language servers into tools
- Extending language server capabilities

## Protocol Overview

### The Problem LSP Solves

Before LSP:
- Each editor implemented language features independently
- Every language needed N integrations for N editors
- M languages × N editors = M×N implementations

After LSP:
- One protocol specification
- M + N implementations needed
- Any server works with any client

### The USB-C Analogy

Just as USB-C provides a universal connector:
- **LSP Client** = Device (editor like VS Code, Neovim)
- **LSP Server** = Peripheral (language analyzer like rust-analyzer, pyright)
- **LSP Protocol** = USB-C specification (JSON-RPC over stdio/TCP)

---

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    LSP ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    EDITOR / IDE (Client)                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                    LSP CLIENT                           │  │
│  │  • Sends document events (open, change, save)          │  │
│  │  • Requests language features (completion, definition) │  │
│  │  • Displays diagnostics and suggestions                │  │
│  └───────────┬────────────────────────────────────────────┘  │
└──────────────┼───────────────────────────────────────────────┘
               │ JSON-RPC (stdio / TCP / WebSocket)
               ▼
┌──────────────────────────────────────────────────────────────┐
│                    LANGUAGE SERVER                            │
│                                                              │
│  • Parses and analyzes source code                          │
│  • Maintains project model and symbol tables                │
│  • Responds to feature requests                             │
│  • Publishes diagnostics (errors, warnings)                 │
└──────────────────────────────────────────────────────────────┘
```

### Communication Protocol

LSP uses **JSON-RPC 2.0** with a specific message format:

```
Content-Length: 123\r\n
Content-Type: application/vscode-jsonrpc; charset=utf-8\r\n
\r\n
{"jsonrpc":"2.0","id":1,"method":"textDocument/definition","params":{...}}
```

**Message Types:**

| Type | Has ID | Expects Response | Example |
|------|--------|------------------|---------|
| Request | Yes | Yes | `textDocument/completion` |
| Response | Yes (matches request) | N/A | Result or error |
| Notification | No | No | `textDocument/didOpen` |

### Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    LSP LIFECYCLE                             │
└─────────────────────────────────────────────────────────────┘

1. INITIALIZATION
   Client ──initialize──────────► Server
     └─ capabilities, rootUri, clientInfo

   Client ◄──result────────────── Server
     └─ capabilities, serverInfo

   Client ──initialized─────────► Server (notification)

2. DOCUMENT SYNCHRONIZATION
   Client ──didOpen─────────────► Server (file opened)
   Client ──didChange───────────► Server (content changed)
   Client ◄──publishDiagnostics── Server (errors/warnings)
   Client ──didSave─────────────► Server (file saved)
   Client ──didClose────────────► Server (file closed)

3. FEATURE REQUESTS
   Client ──completion──────────► Server
   Client ◄──completionItems───── Server

   Client ──definition──────────► Server
   Client ◄──location───────────── Server

4. SHUTDOWN
   Client ──shutdown────────────► Server
   Client ◄──result (null)─────── Server
   Client ──exit────────────────► Server (notification)
```

---

## Language Features

### Navigation Features

| Method | Purpose | Returns |
|--------|---------|---------|
| `textDocument/definition` | Go to symbol definition | Location(s) |
| `textDocument/declaration` | Go to symbol declaration | Location(s) |
| `textDocument/typeDefinition` | Go to type definition | Location(s) |
| `textDocument/implementation` | Go to implementations | Location(s) |
| `textDocument/references` | Find all references | Location[] |

**Example Request (Go to Definition):**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "textDocument/definition",
  "params": {
    "textDocument": {
      "uri": "file:///project/src/main.ts"
    },
    "position": {
      "line": 10,
      "character": 15
    }
  }
}
```

**Example Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "uri": "file:///project/src/utils.ts",
    "range": {
      "start": { "line": 5, "character": 0 },
      "end": { "line": 5, "character": 20 }
    }
  }
}
```

### Completion

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "textDocument/completion",
  "params": {
    "textDocument": { "uri": "file:///project/src/main.ts" },
    "position": { "line": 12, "character": 8 },
    "context": {
      "triggerKind": 1,
      "triggerCharacter": "."
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "isIncomplete": false,
    "items": [
      {
        "label": "toString",
        "kind": 2,
        "detail": "(): string",
        "documentation": "Returns a string representation",
        "insertText": "toString()"
      },
      {
        "label": "valueOf",
        "kind": 2,
        "detail": "(): number",
        "insertText": "valueOf()"
      }
    ]
  }
}
```

**Completion Item Kinds:**
| Kind | Value | Kind | Value |
|------|-------|------|-------|
| Text | 1 | Method | 2 |
| Function | 3 | Constructor | 4 |
| Field | 5 | Variable | 6 |
| Class | 7 | Interface | 8 |
| Module | 9 | Property | 10 |
| Snippet | 15 | Keyword | 14 |

### Diagnostics

Servers push diagnostics via notification:

```json
{
  "jsonrpc": "2.0",
  "method": "textDocument/publishDiagnostics",
  "params": {
    "uri": "file:///project/src/main.ts",
    "version": 3,
    "diagnostics": [
      {
        "range": {
          "start": { "line": 10, "character": 0 },
          "end": { "line": 10, "character": 10 }
        },
        "severity": 1,
        "code": "TS2322",
        "source": "typescript",
        "message": "Type 'string' is not assignable to type 'number'",
        "relatedInformation": [
          {
            "location": {
              "uri": "file:///project/src/types.ts",
              "range": { "start": { "line": 5, "character": 2 }, "end": { "line": 5, "character": 8 } }
            },
            "message": "The expected type comes from property 'count'"
          }
        ]
      }
    ]
  }
}
```

**Diagnostic Severities:**
| Value | Severity |
|-------|----------|
| 1 | Error |
| 2 | Warning |
| 3 | Information |
| 4 | Hint |

### Hover Information

```json
// Request
{
  "method": "textDocument/hover",
  "params": {
    "textDocument": { "uri": "file:///project/src/main.ts" },
    "position": { "line": 8, "character": 10 }
  }
}

// Response
{
  "result": {
    "contents": {
      "kind": "markdown",
      "value": "```typescript\nfunction calculateSum(a: number, b: number): number\n```\n\nCalculates the sum of two numbers."
    },
    "range": {
      "start": { "line": 8, "character": 4 },
      "end": { "line": 8, "character": 16 }
    }
  }
}
```

### Code Actions

Request quick fixes and refactorings:

```json
// Request
{
  "method": "textDocument/codeAction",
  "params": {
    "textDocument": { "uri": "file:///project/src/main.ts" },
    "range": {
      "start": { "line": 10, "character": 0 },
      "end": { "line": 10, "character": 20 }
    },
    "context": {
      "diagnostics": [...],
      "only": ["quickfix"]
    }
  }
}

// Response
{
  "result": [
    {
      "title": "Convert to template literal",
      "kind": "refactor.rewrite",
      "edit": {
        "changes": {
          "file:///project/src/main.ts": [
            {
              "range": { "start": { "line": 10, "character": 0 }, "end": { "line": 10, "character": 25 } },
              "newText": "`Hello, ${name}!`"
            }
          ]
        }
      }
    }
  ]
}
```

### Document Symbols

```json
// Request
{
  "method": "textDocument/documentSymbol",
  "params": {
    "textDocument": { "uri": "file:///project/src/main.ts" }
  }
}

// Response (hierarchical)
{
  "result": [
    {
      "name": "Calculator",
      "kind": 5,
      "range": { "start": { "line": 0, "character": 0 }, "end": { "line": 20, "character": 1 } },
      "selectionRange": { "start": { "line": 0, "character": 6 }, "end": { "line": 0, "character": 16 } },
      "children": [
        {
          "name": "add",
          "kind": 6,
          "range": { "start": { "line": 2, "character": 2 }, "end": { "line": 4, "character": 3 } },
          "selectionRange": { "start": { "line": 2, "character": 2 }, "end": { "line": 2, "character": 5 } }
        }
      ]
    }
  ]
}
```

**Symbol Kinds:**
| Kind | Value | Kind | Value |
|------|-------|------|-------|
| File | 1 | Module | 2 |
| Namespace | 3 | Package | 4 |
| Class | 5 | Method | 6 |
| Property | 7 | Field | 8 |
| Constructor | 9 | Enum | 10 |
| Interface | 11 | Function | 12 |
| Variable | 13 | Constant | 14 |

---

## Capabilities Negotiation

### Client Capabilities (sent in `initialize`)

```json
{
  "capabilities": {
    "textDocument": {
      "synchronization": {
        "dynamicRegistration": true,
        "willSave": true,
        "willSaveWaitUntil": true,
        "didSave": true
      },
      "completion": {
        "completionItem": {
          "snippetSupport": true,
          "commitCharactersSupport": true,
          "documentationFormat": ["markdown", "plaintext"],
          "resolveSupport": {
            "properties": ["documentation", "detail"]
          }
        },
        "contextSupport": true
      },
      "hover": {
        "contentFormat": ["markdown", "plaintext"]
      },
      "definition": {
        "linkSupport": true
      },
      "codeAction": {
        "codeActionLiteralSupport": {
          "codeActionKind": {
            "valueSet": ["quickfix", "refactor", "source"]
          }
        }
      }
    },
    "workspace": {
      "workspaceFolders": true,
      "configuration": true,
      "didChangeConfiguration": {
        "dynamicRegistration": true
      }
    }
  }
}
```

### Server Capabilities (returned in `initialize` response)

```json
{
  "capabilities": {
    "textDocumentSync": {
      "openClose": true,
      "change": 2,
      "save": { "includeText": false }
    },
    "completionProvider": {
      "triggerCharacters": [".", ":", "<"],
      "resolveProvider": true
    },
    "hoverProvider": true,
    "definitionProvider": true,
    "referencesProvider": true,
    "documentSymbolProvider": true,
    "workspaceSymbolProvider": true,
    "codeActionProvider": {
      "codeActionKinds": ["quickfix", "refactor.extract", "source.organizeImports"]
    },
    "documentFormattingProvider": true,
    "renameProvider": {
      "prepareProvider": true
    },
    "diagnosticProvider": {
      "interFileDependencies": true,
      "workspaceDiagnostics": true
    }
  }
}
```

### Text Document Sync Kinds

| Value | Mode | Description |
|-------|------|-------------|
| 0 | None | No synchronization |
| 1 | Full | Full document on every change |
| 2 | Incremental | Only send changes (preferred) |

---

## Building a Language Server

### TypeScript (vscode-languageserver)

```typescript
import {
  createConnection,
  TextDocuments,
  ProposedFeatures,
  InitializeParams,
  TextDocumentSyncKind,
  InitializeResult,
  CompletionItem,
  CompletionItemKind,
  TextDocumentPositionParams,
  Diagnostic,
  DiagnosticSeverity
} from 'vscode-languageserver/node';

import { TextDocument } from 'vscode-languageserver-textdocument';

// Create connection using all proposed features
const connection = createConnection(ProposedFeatures.all);

// Create document manager
const documents: TextDocuments<TextDocument> = new TextDocuments(TextDocument);

connection.onInitialize((params: InitializeParams): InitializeResult => {
  return {
    capabilities: {
      textDocumentSync: TextDocumentSyncKind.Incremental,
      completionProvider: {
        resolveProvider: true,
        triggerCharacters: ['.']
      },
      hoverProvider: true,
      definitionProvider: true,
      referencesProvider: true
    }
  };
});

// Validate documents on change
documents.onDidChangeContent(change => {
  validateTextDocument(change.document);
});

async function validateTextDocument(document: TextDocument): Promise<void> {
  const diagnostics: Diagnostic[] = [];
  const text = document.getText();

  // Example: Find TODO comments
  const todoPattern = /\bTODO\b/g;
  let match;
  while ((match = todoPattern.exec(text))) {
    diagnostics.push({
      severity: DiagnosticSeverity.Information,
      range: {
        start: document.positionAt(match.index),
        end: document.positionAt(match.index + match[0].length)
      },
      message: 'TODO comment found',
      source: 'my-language-server'
    });
  }

  connection.sendDiagnostics({ uri: document.uri, diagnostics });
}

// Provide completions
connection.onCompletion((params: TextDocumentPositionParams): CompletionItem[] => {
  return [
    {
      label: 'console',
      kind: CompletionItemKind.Module,
      detail: 'Console object',
      documentation: 'The console object provides access to debugging console'
    },
    {
      label: 'console.log',
      kind: CompletionItemKind.Function,
      detail: '(message: any): void',
      insertText: 'console.log($1)',
      insertTextFormat: 2 // Snippet
    }
  ];
});

// Provide hover information
connection.onHover((params) => {
  const document = documents.get(params.textDocument.uri);
  if (!document) return null;

  // Get word at position and return hover info
  return {
    contents: {
      kind: 'markdown',
      value: '**Symbol Info**\n\nDocumentation here'
    }
  };
});

// Listen for document events
documents.listen(connection);

// Start the connection
connection.listen();
```

### Python (pygls)

```python
from pygls.server import LanguageServer
from lsprotocol import types as lsp

server = LanguageServer("my-language-server", "v1.0")

@server.feature(lsp.INITIALIZE)
def initialize(params: lsp.InitializeParams) -> lsp.InitializeResult:
    return lsp.InitializeResult(
        capabilities=lsp.ServerCapabilities(
            text_document_sync=lsp.TextDocumentSyncOptions(
                open_close=True,
                change=lsp.TextDocumentSyncKind.Incremental,
            ),
            completion_provider=lsp.CompletionOptions(
                trigger_characters=["."],
                resolve_provider=True,
            ),
            hover_provider=True,
            definition_provider=True,
        )
    )

@server.feature(lsp.TEXT_DOCUMENT_DID_OPEN)
def did_open(params: lsp.DidOpenTextDocumentParams):
    """Handle document open."""
    validate_document(params.text_document.uri)

@server.feature(lsp.TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: lsp.DidChangeTextDocumentParams):
    """Handle document changes."""
    validate_document(params.text_document.uri)

def validate_document(uri: str):
    """Validate document and publish diagnostics."""
    document = server.workspace.get_text_document(uri)
    diagnostics = []

    # Example: Find syntax issues
    for i, line in enumerate(document.lines):
        if "TODO" in line:
            diagnostics.append(lsp.Diagnostic(
                range=lsp.Range(
                    start=lsp.Position(line=i, character=line.index("TODO")),
                    end=lsp.Position(line=i, character=line.index("TODO") + 4),
                ),
                message="TODO comment found",
                severity=lsp.DiagnosticSeverity.Information,
                source="my-language-server",
            ))

    server.publish_diagnostics(uri, diagnostics)

@server.feature(lsp.TEXT_DOCUMENT_COMPLETION)
def completions(params: lsp.CompletionParams) -> lsp.CompletionList:
    """Provide completion items."""
    return lsp.CompletionList(
        is_incomplete=False,
        items=[
            lsp.CompletionItem(
                label="print",
                kind=lsp.CompletionItemKind.Function,
                detail="print(*args, **kwargs)",
                documentation="Print to stdout",
            ),
            lsp.CompletionItem(
                label="len",
                kind=lsp.CompletionItemKind.Function,
                detail="len(obj) -> int",
                documentation="Return the length of an object",
            ),
        ],
    )

@server.feature(lsp.TEXT_DOCUMENT_HOVER)
def hover(params: lsp.HoverParams) -> lsp.Hover | None:
    """Provide hover information."""
    document = server.workspace.get_text_document(params.text_document.uri)
    # Get word at position and return info
    return lsp.Hover(
        contents=lsp.MarkupContent(
            kind=lsp.MarkupKind.Markdown,
            value="**Symbol Info**\n\nDocumentation here",
        )
    )

if __name__ == "__main__":
    server.start_io()
```

---

## Building an LSP Client

### Node.js Client Example

```typescript
import * as cp from 'child_process';
import * as rpc from 'vscode-jsonrpc/node';

// Spawn the language server
const serverProcess = cp.spawn('node', ['path/to/server.js']);

// Create JSON-RPC connection
const connection = rpc.createMessageConnection(
  new rpc.StreamMessageReader(serverProcess.stdout),
  new rpc.StreamMessageWriter(serverProcess.stdin)
);

// Listen for notifications from server
connection.onNotification('textDocument/publishDiagnostics', (params) => {
  console.log('Diagnostics:', params.diagnostics);
});

// Start connection
connection.listen();

// Send initialize request
const initResult = await connection.sendRequest('initialize', {
  processId: process.pid,
  rootUri: 'file:///path/to/workspace',
  capabilities: {
    textDocument: {
      completion: { completionItem: { snippetSupport: true } },
      hover: { contentFormat: ['markdown'] }
    }
  }
});

console.log('Server capabilities:', initResult.capabilities);

// Send initialized notification
connection.sendNotification('initialized', {});

// Open a document
connection.sendNotification('textDocument/didOpen', {
  textDocument: {
    uri: 'file:///path/to/file.ts',
    languageId: 'typescript',
    version: 1,
    text: 'const x = 1;\nconsole.log(x);'
  }
});

// Request completion
const completions = await connection.sendRequest('textDocument/completion', {
  textDocument: { uri: 'file:///path/to/file.ts' },
  position: { line: 1, character: 8 }
});

console.log('Completions:', completions);

// Shutdown
await connection.sendRequest('shutdown');
connection.sendNotification('exit');
```

---

## SDK Reference

### Official and Popular SDKs

| Language | SDK | Repository |
|----------|-----|------------|
| **TypeScript** | vscode-languageserver | [microsoft/vscode-languageserver-node](https://github.com/microsoft/vscode-languageserver-node) |
| **Python** | pygls | [openlawlibrary/pygls](https://github.com/openlawlibrary/pygls) |
| **Java** | LSP4J | [eclipse/lsp4j](https://github.com/eclipse/lsp4j) |
| **Rust** | tower-lsp | [tower-rs/tower-lsp](https://github.com/tower-rs/tower-lsp) |
| **C#** | OmniSharp | [OmniSharp/csharp-language-server-protocol](https://github.com/OmniSharp/csharp-language-server-protocol) |
| **Go** | go-lsp | [sourcegraph/go-lsp](https://github.com/sourcegraph/go-lsp) |
| **Haskell** | lsp | [haskell/lsp](https://github.com/haskell/lsp) |

### Popular Language Servers

| Language | Server | Notes |
|----------|--------|-------|
| TypeScript/JavaScript | typescript-language-server | Uses tsserver |
| Python | pyright, pylsp | Static typing / general |
| Rust | rust-analyzer | Official Rust analyzer |
| Go | gopls | Official Go team |
| C/C++ | clangd | LLVM-based |
| Java | Eclipse JDT LS | Used by VS Code Java |
| C# | OmniSharp | .NET ecosystem |

---

## Debugging LSP

### Enable Tracing

Most clients support logging LSP messages:

**VS Code** (`settings.json`):
```json
{
  "myExtension.trace.server": "verbose"
}
```

**Neovim** (Lua):
```lua
vim.lsp.set_log_level("debug")
-- Logs at: ~/.local/state/nvim/lsp.log
```

### Manual Testing with JSON-RPC

```bash
# Start server and send messages manually
echo 'Content-Length: 108\r\n\r\n{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"processId":null,"rootUri":null,"capabilities":{}}}' | node server.js
```

### Common Issues

**Server doesn't start:**
- Check executable path and permissions
- Verify runtime (Node.js, Python) is installed
- Check stderr for error messages

**No completions:**
- Verify `completionProvider` capability is advertised
- Check trigger characters match
- Ensure document is open (`didOpen` sent)

**Diagnostics not showing:**
- Check `textDocumentSync` capability
- Verify `publishDiagnostics` notifications are being sent
- Check diagnostic severity levels

---

## Best Practices

### For Server Developers

1. **Use incremental sync** - Full sync is expensive for large files
2. **Debounce validation** - Don't validate on every keystroke
3. **Support cancellation** - Long operations should check `$/cancelRequest`
4. **Provide resolve** - Return minimal completion items, resolve on demand
5. **Include code actions** - Quick fixes improve user experience
6. **Report progress** - Use `$/progress` for long operations

### For Client Developers

1. **Cache capabilities** - Don't re-check server capabilities repeatedly
2. **Batch requests** - Combine related requests when possible
3. **Handle partial results** - Some servers support streaming results
4. **Implement timeout** - Don't wait forever for responses
5. **Support dynamic registration** - Allow servers to register/unregister capabilities

### Performance Tips

```typescript
// Debounce document changes
let validationTimeout: NodeJS.Timeout;
documents.onDidChangeContent(change => {
  clearTimeout(validationTimeout);
  validationTimeout = setTimeout(() => {
    validateDocument(change.document);
  }, 500);
});

// Support cancellation
connection.onDefinition(async (params, token) => {
  // Check cancellation periodically
  if (token.isCancellationRequested) {
    return null;
  }

  const result = await findDefinition(params);

  if (token.isCancellationRequested) {
    return null;
  }

  return result;
});
```

---

## LSP 3.17 Features

### Inlay Hints

Display inline parameter names, type annotations:

```json
{
  "method": "textDocument/inlayHint",
  "params": {
    "textDocument": { "uri": "file:///project/src/main.ts" },
    "range": { "start": { "line": 0, "character": 0 }, "end": { "line": 50, "character": 0 } }
  }
}

// Response
{
  "result": [
    {
      "position": { "line": 10, "character": 15 },
      "label": ": number",
      "kind": 1,
      "paddingLeft": true
    }
  ]
}
```

### Type Hierarchy

Navigate type relationships:

```json
// Prepare
{ "method": "textDocument/prepareTypeHierarchy", "params": { "textDocument": {...}, "position": {...} } }

// Get supertypes
{ "method": "typeHierarchy/supertypes", "params": { "item": {...} } }

// Get subtypes
{ "method": "typeHierarchy/subtypes", "params": { "item": {...} } }
```

### Diagnostic Pull Model

Client-initiated diagnostics (alternative to push):

```json
// Request diagnostics for a document
{ "method": "textDocument/diagnostic", "params": { "textDocument": { "uri": "..." } } }

// Request workspace-wide diagnostics
{ "method": "workspace/diagnostic", "params": { "previousResultIds": [...] } }
```

---

## Development Tools

### LSP DevTools

LSP DevTools is a collection of CLI utilities for inspecting and visualizing language server interactions. Essential for debugging protocol issues.

**Installation:**
```bash
pipx install lsp-devtools
```

**Architecture:** The LSP Agent acts as a proxy between client and server, forwarding messages while copying them to a monitoring application.

```
┌────────────────┐      ┌─────────────┐      ┌─────────────────┐
│ Language Client│◄────►│  LSP Agent  │◄────►│ Language Server │
└────────────────┘      └──────┬──────┘      └─────────────────┘
                               │
                               ▼ TCP (localhost:8765)
                        ┌──────────────┐
                        │ lsp-devtools │
                        │   record /   │
                        │   inspect    │
                        └──────────────┘
```

#### Agent Command

Wrap your language server to enable inspection:

```bash
# Basic usage - wrap server command
lsp-devtools agent -- <server-cmd>

# Custom host/port
lsp-devtools agent --host 127.0.0.1 --port 1234 -- python -m my_server

# Example: wrap esbonio server
lsp-devtools agent -- esbonio
```

**Neovim Configuration:**
```lua
-- In nvim-lspconfig setup
require('lspconfig').esbonio.setup {
  cmd = { "lsp-devtools", "agent", "--", "esbonio" }
}
```

**VS Code Configuration:**
```json
{
  "myLanguage.server.path": "lsp-devtools",
  "myLanguage.server.args": ["agent", "--", "my-server"]
}
```

#### Record Command

Capture LSP sessions to various destinations:

```bash
# Record to console (pretty-printed JSON)
lsp-devtools record

# Record to file (JSON-RPC, one message per line)
lsp-devtools record --to-file session.jsonl

# Record to SQLite database (for analysis)
lsp-devtools record --to-sqlite session.db

# Save console output as HTML/SVG
lsp-devtools record --save-output session.html
```

**Filtering Options:**
```bash
# Filter by source
lsp-devtools record --message-source client
lsp-devtools record --message-source server

# Filter by message type
lsp-devtools record --include-message-type request
lsp-devtools record --include-message-type notification

# Filter by method
lsp-devtools record --include-method textDocument/completion
lsp-devtools record --exclude-method textDocument/didChange

# Custom format
lsp-devtools record -f "{message.method}: {message.params.position.line}"
```

#### Inspect Command

Interactive TUI for real-time LSP message inspection:

```bash
# Launch inspector
lsp-devtools inspect

# Custom port
lsp-devtools inspect --port 1234
```

**Features:**
- Browse all messages between client and server
- Hierarchical capability display (30+ capability types)
- Real-time message flow visualization
- Detailed message content inspection

### pytest-lsp

End-to-end testing framework for language servers, built on pygls.

**Installation:**
```bash
pip install pytest-lsp
```

**Key Features:**
- Run language servers in subprocesses
- Communicate via stdio (mimics real clients)
- Language-agnostic (test servers in any language)
- Async test support

#### Basic Test Setup

```python
import pytest
import pytest_lsp
from pytest_lsp import ClientServerConfig, LanguageClient
from lsprotocol.types import (
    InitializeParams,
    CompletionParams,
    TextDocumentIdentifier,
    Position,
)

@pytest_lsp.fixture(
    config=ClientServerConfig(
        server_command=["python", "-m", "my_server"],
    ),
)
async def client(lsp_client: LanguageClient):
    # Setup: Initialize the LSP session
    await lsp_client.initialize_session(
        InitializeParams(
            capabilities={},
            root_uri="file:///workspace",
        )
    )

    yield

    # Teardown: Shutdown gracefully
    await lsp_client.shutdown_session()

@pytest.mark.asyncio
async def test_completions(client: LanguageClient):
    """Test that completion returns expected items."""
    result = await client.text_document_completion_async(
        CompletionParams(
            text_document=TextDocumentIdentifier(uri="file:///test.py"),
            position=Position(line=0, character=0),
        )
    )

    labels = [item.label for item in result.items]
    assert "hello" in labels
    assert "world" in labels
```

#### Parameterized Client Testing

Test against multiple client configurations:

```python
@pytest.fixture(params=["neovim", "vscode", "emacs"])
def client_name(request):
    return request.param

@pytest_lsp.fixture(
    config=ClientServerConfig(
        server_command=["python", "-m", "my_server"],
    ),
)
async def client(lsp_client: LanguageClient, client_name: str):
    # Get capabilities for specific client
    capabilities = client_capabilities(client_name)

    await lsp_client.initialize_session(
        InitializeParams(
            capabilities=capabilities,
            client_info={"name": client_name},
        )
    )
    yield
    await lsp_client.shutdown_session()
```

#### Testing Diagnostics

```python
@pytest.mark.asyncio
async def test_diagnostics(client: LanguageClient):
    """Test diagnostic publishing."""
    # Open a document with errors
    client.text_document_did_open(
        TextDocumentItem(
            uri="file:///test.py",
            language_id="python",
            version=1,
            text="def foo(\n  invalid syntax",
        )
    )

    # Wait for diagnostics
    await client.wait_for_notification("textDocument/publishDiagnostics")

    # Check diagnostics were received
    diagnostics = client.diagnostics["file:///test.py"]
    assert len(diagnostics) > 0
    assert diagnostics[0].severity == DiagnosticSeverity.Error
```

#### Common Pitfall

Servers must explicitly start I/O handling:

```python
# In your server's __main__.py
if __name__ == "__main__":
    server = MyLanguageServer()
    server.start_io()  # Don't forget this!
```

### Monaco Editor Integration

When building browser-based LSP clients with Monaco Editor, use `monaco-languageserver-types` for bidirectional type conversion.

**Installation:**
```bash
npm install monaco-languageserver-types
```

**Key Concept:** Monaco Editor and LSP use different type representations. This library provides `from*` and `to*` functions for seamless conversion:

- **`from*`** - Convert Monaco types → LSP types
- **`to*`** - Convert LSP types → Monaco types

#### Type Conversion Examples

**Position & Range:**
```typescript
import { fromRange, toRange, fromPosition, toPosition } from 'monaco-languageserver-types';

// Monaco uses 1-based lines, LSP uses 0-based
const monacoRange = {
  startLineNumber: 1,
  startColumn: 2,
  endLineNumber: 3,
  endColumn: 4
};

// Convert to LSP format
const lspRange = fromRange(monacoRange);
// { start: { line: 0, character: 1 }, end: { line: 2, character: 3 } }

// Convert back to Monaco format
const backToMonaco = toRange(lspRange);
// { startLineNumber: 1, startColumn: 2, endLineNumber: 3, endColumn: 4 }
```

**Diagnostics:**
```typescript
import { fromMarkerData, toMarkerData, fromMarkerSeverity } from 'monaco-languageserver-types';

// Convert Monaco marker to LSP diagnostic
const monacoMarker = {
  severity: monaco.MarkerSeverity.Error,
  message: "Unexpected token",
  startLineNumber: 5,
  startColumn: 10,
  endLineNumber: 5,
  endColumn: 15
};

const lspDiagnostic = fromMarkerData(monacoMarker);
// Ready to send to language server

// Convert LSP diagnostic to Monaco marker
const marker = toMarkerData(lspDiagnostic);
monaco.editor.setModelMarkers(model, 'lsp', [marker]);
```

**Completion Items:**
```typescript
import { fromCompletionItem, toCompletionItem, toCompletionList } from 'monaco-languageserver-types';

// Handle LSP completion response for Monaco
connection.onCompletion(async (params) => {
  const lspCompletions = await languageServer.getCompletions(params);
  return lspCompletions;
});

// In Monaco provider
const monacoProvider: monaco.languages.CompletionItemProvider = {
  provideCompletionItems: async (model, position) => {
    const lspPosition = fromPosition(position);
    const lspResult = await client.sendRequest('textDocument/completion', {
      textDocument: { uri: model.uri.toString() },
      position: lspPosition
    });

    return toCompletionList(lspResult);
  }
};
```

**Hover:**
```typescript
import { fromPosition, toHover } from 'monaco-languageserver-types';

const hoverProvider: monaco.languages.HoverProvider = {
  provideHover: async (model, position) => {
    const lspHover = await client.sendRequest('textDocument/hover', {
      textDocument: { uri: model.uri.toString() },
      position: fromPosition(position)
    });

    return lspHover ? toHover(lspHover) : null;
  }
};
```

#### Available Conversions

| Category | Functions |
|----------|-----------|
| **Structural** | `fromPosition`, `toPosition`, `fromRange`, `toRange`, `fromLocation`, `toLocation` |
| **Diagnostics** | `fromMarkerData`, `toMarkerData`, `fromMarkerSeverity`, `toMarkerSeverity` |
| **Completion** | `fromCompletionItem`, `toCompletionItem`, `toCompletionList`, `fromCompletionItemKind` |
| **Code Actions** | `fromCodeAction`, `toCodeAction`, `fromCodeActionContext` |
| **Navigation** | `fromDefinition`, `toDefinition`, `fromDocumentHighlight`, `toDocumentHighlight` |
| **Symbols** | `fromDocumentSymbol`, `toDocumentSymbol`, `fromSymbolKind`, `toSymbolKind` |
| **Formatting** | `fromTextEdit`, `toTextEdit`, `fromFormattingOptions` |
| **Semantic** | `fromSemanticTokens`, `toSemanticTokens`, `fromInlayHint`, `toInlayHint` |
| **Workspace** | `fromWorkspaceEdit`, `toWorkspaceEdit` |

#### Full Monaco LSP Client Example

```typescript
import * as monaco from 'monaco-editor';
import {
  fromPosition, fromRange, toCompletionList, toHover,
  toMarkerData, toDocumentHighlight, toCodeAction
} from 'monaco-languageserver-types';
import { createLanguageClient } from './lsp-client';

// Create LSP client connection
const client = createLanguageClient('ws://localhost:3000/lsp');

// Register Monaco providers that bridge to LSP
monaco.languages.registerCompletionItemProvider('typescript', {
  triggerCharacters: ['.', '"', "'", '/'],
  provideCompletionItems: async (model, position) => {
    const result = await client.textDocumentCompletion({
      textDocument: { uri: model.uri.toString() },
      position: fromPosition(position)
    });
    return toCompletionList(result);
  }
});

monaco.languages.registerHoverProvider('typescript', {
  provideHover: async (model, position) => {
    const result = await client.textDocumentHover({
      textDocument: { uri: model.uri.toString() },
      position: fromPosition(position)
    });
    return result ? toHover(result) : null;
  }
});

// Handle diagnostics from server
client.onNotification('textDocument/publishDiagnostics', (params) => {
  const model = monaco.editor.getModel(monaco.Uri.parse(params.uri));
  if (model) {
    const markers = params.diagnostics.map(toMarkerData);
    monaco.editor.setModelMarkers(model, 'lsp', markers);
  }
});
```

---

## Resources

### Official Documentation
- [LSP Website](https://microsoft.github.io/language-server-protocol/)
- [Specification 3.17](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/)
- [GitHub Repository](https://github.com/Microsoft/language-server-protocol)

### Implementations
- [Server Implementations](https://microsoft.github.io/language-server-protocol/implementors/servers/)
- [Client Implementations](https://microsoft.github.io/language-server-protocol/implementors/tools/)
- [SDKs](https://microsoft.github.io/language-server-protocol/implementors/sdks/)

### Development Tools
- [LSP DevTools](https://lsp-devtools.readthedocs.io/) - CLI utilities for inspecting LSP interactions
- [pytest-lsp](https://lsp-devtools.readthedocs.io/en/latest/pytest-lsp/) - End-to-end testing framework
- [monaco-languageserver-types](https://github.com/remcohaszing/monaco-languageserver-types) - Type conversion for Monaco Editor

### Tutorials
- [VS Code LSP Tutorial](https://code.visualstudio.com/api/language-extensions/language-server-extension-guide)
- [pygls Documentation](https://pygls.readthedocs.io/)
- [LSP4J Documentation](https://github.com/eclipse/lsp4j/wiki)

---

## Version History

- **1.2.0** (2026-01-11): Added Monaco Editor integration
  - monaco-languageserver-types library documentation
  - Bidirectional type conversion (from*/to* functions)
  - Position, Range, Diagnostic conversions
  - Completion, Hover, Code Action examples
  - Full Monaco LSP client example
  - Available conversions reference table

- **1.1.0** (2026-01-11): Added Development Tools section
  - LSP DevTools integration (agent, record, inspect commands)
  - pytest-lsp testing framework with examples
  - Architecture diagrams for debugging workflow
  - Parameterized client testing patterns
  - Diagnostic testing examples

- **1.0.0** (2026-01-10): Initial skill release
  - Complete protocol overview (architecture, lifecycle, capabilities)
  - All language features documented (completion, diagnostics, navigation, etc.)
  - Server development guides (TypeScript, Python)
  - Client development guide
  - SDK reference table
  - LSP 3.17 features (inlay hints, type hierarchy, diagnostic pull)
  - Debugging and best practices
