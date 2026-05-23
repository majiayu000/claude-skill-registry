---
name: lsp-implementation
# prettier-ignore
description: Use when implementing Language Server Protocol features - covers completions, hover, diagnostics, and navigation
---

# Language Server Protocol Implementation

## Quick Start

```typescript
import {
  createConnection,
  TextDocuments,
  ProposedFeatures,
} from "vscode-languageserver/node";
import { TextDocument } from "vscode-languageserver-textdocument";

const connection = createConnection(ProposedFeatures.all);
const documents = new TextDocuments(TextDocument);

connection.onInitialize(() => ({
  capabilities: {
    textDocumentSync: TextDocumentSyncKind.Incremental,
    completionProvider: { triggerCharacters: [".", "/"] },
    hoverProvider: true,
    definitionProvider: true,
  }
}));

documents.listen(connection);
connection.listen();
```

## Core Features

### Completions

```typescript
connection.onCompletion((params): CompletionItem[] => {
  const document = documents.get(params.textDocument.uri);
  const position = params.position;

  // Get context at cursor
  const line = document?.getText({
    start: { line: position.line, character: 0 },
    end: position
  });

  // Return builtins
  return [
    { label: "map", kind: CompletionItemKind.Function, detail: "(fn) -> List" },
    { label: "filter", kind: CompletionItemKind.Function, detail: "(fn) -> List" },
    { label: "reduce", kind: CompletionItemKind.Function, detail: "(init, fn) -> Value" },
  ];
});
```

### Hover Information

```typescript
connection.onHover((params): Hover | null => {
  const document = documents.get(params.textDocument.uri);
  const word = getWordAtPosition(document, params.position);

  const builtin = BUILTINS[word];
  if (builtin) {
    return {
      contents: {
        kind: "markdown",
        value: `**${word}**\n\n${builtin.description}\n\n\`\`\`lea\n${builtin.signature}\n\`\`\``
      }
    };
  }
  return null;
});
```

### Diagnostics

```typescript
documents.onDidChangeContent((change) => {
  const document = change.document;
  const diagnostics: Diagnostic[] = [];

  try {
    parse(document.getText());
  } catch (error) {
    if (error instanceof ParseError) {
      diagnostics.push({
        severity: DiagnosticSeverity.Error,
        range: error.range,
        message: error.message,
        source: "lea"
      });
    }
  }

  connection.sendDiagnostics({ uri: document.uri, diagnostics });
});
```

### Go to Definition

```typescript
connection.onDefinition((params): Definition | null => {
  const document = documents.get(params.textDocument.uri);
  const word = getWordAtPosition(document, params.position);

  // Find definition in AST
  const definition = findDefinition(document.getText(), word);
  if (definition) {
    return {
      uri: params.textDocument.uri,
      range: definition.range
    };
  }
  return null;
});
```

## Protocol Messages

- `textDocument/completion` - Code completions
- `textDocument/hover` - Hover information
- `textDocument/definition` - Go to definition
- `textDocument/references` - Find all references
- `textDocument/documentSymbol` - Document outline
- `textDocument/formatting` - Code formatting

## Reference Files

- [references/capabilities.md](references/capabilities.md) - Server capabilities
- [references/diagnostics.md](references/diagnostics.md) - Error reporting
