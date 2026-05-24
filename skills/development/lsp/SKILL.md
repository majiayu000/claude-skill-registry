---
name: lsp
# prettier-ignore
description: Use when implementing Language Server Protocol features - diagnostics, completions, hover, go-to-definition, and editor integration
---

# Language Server Protocol (LSP)

## Quick Start

```typescript
import { createConnection, TextDocuments, ProposedFeatures } from 'vscode-languageserver/node';
import { TextDocument } from 'vscode-languageserver-textdocument';

const connection = createConnection(ProposedFeatures.all);
const documents = new TextDocuments(TextDocument);

connection.onInitialize((params) => ({
  capabilities: {
    textDocumentSync: TextDocumentSyncKind.Incremental,
    completionProvider: { resolveProvider: true },
    hoverProvider: true,
    definitionProvider: true,
    diagnosticProvider: { interFileDependencies: false, workspaceDiagnostics: false }
  }
}));

documents.onDidChangeContent((change) => {
  validateDocument(change.document);
});

documents.listen(connection);
connection.listen();
```

## Core Concepts

- **Connection**: JSON-RPC communication channel between client and server
- **TextDocuments**: Manages open document state with incremental sync
- **Capabilities**: Server declares features in `onInitialize` response
- **Diagnostics**: Errors/warnings pushed via `connection.sendDiagnostics()`

## Common Providers

| Provider | Purpose | Key Method |
|----------|---------|------------|
| `completionProvider` | Autocomplete suggestions | `onCompletion` |
| `hoverProvider` | Tooltip on hover | `onHover` |
| `definitionProvider` | Go-to-definition | `onDefinition` |
| `referencesProvider` | Find all references | `onReferences` |
| `documentSymbolProvider` | Outline/symbols | `onDocumentSymbol` |
| `codeActionProvider` | Quick fixes | `onCodeAction` |

## Key Patterns

- Use `TextDocument.positionAt(offset)` and `offsetAt(position)` for conversions
- Return `null` from handlers when no result available
- Diagnostics use `DiagnosticSeverity.Error | Warning | Information | Hint`
- Use `Location` for definitions, `LocationLink` for richer go-to-definition
