---
name: vscode-extension
# prettier-ignore
description: Use when developing VSCode extensions - covers language support, LSP integration, and packaging
---

# VSCode Extension Development

## Quick Start

```json
// package.json
{
  "name": "vscode-lea",
  "displayName": "Lea Language",
  "engines": { "vscode": "^1.85.0" },
  "categories": ["Programming Languages"],
  "contributes": {
    "languages": [{
      "id": "lea",
      "extensions": [".lea"],
      "configuration": "./language-configuration.json"
    }],
    "grammars": [{
      "language": "lea",
      "scopeName": "source.lea",
      "path": "./syntaxes/lea.tmLanguage.json"
    }]
  }
}
```

## Core Components

### Language Configuration

```json
// language-configuration.json
{
  "comments": { "lineComment": "--" },
  "brackets": [
    ["{", "}"],
    ["[", "]"],
    ["(", ")"]
  ],
  "autoClosingPairs": [
    { "open": "{", "close": "}" },
    { "open": "[", "close": "]" },
    { "open": "(", "close": ")" },
    { "open": "\"", "close": "\"" }
  ],
  "surroundingPairs": [
    ["{", "}"],
    ["[", "]"],
    ["(", ")"],
    ["\"", "\""]
  ]
}
```

### LSP Client Integration

```typescript
import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions,
} from "vscode-languageclient/node";

export function activate(context: vscode.ExtensionContext) {
  const serverModule = context.asAbsolutePath("server/index.js");

  const serverOptions: ServerOptions = {
    run: { module: serverModule, transport: TransportKind.ipc },
    debug: { module: serverModule, transport: TransportKind.ipc }
  };

  const clientOptions: LanguageClientOptions = {
    documentSelector: [{ scheme: "file", language: "lea" }],
  };

  const client = new LanguageClient("lea", "Lea", serverOptions, clientOptions);
  client.start();
}
```

### Snippets

```json
// snippets/lea.json
{
  "Function": {
    "prefix": "fn",
    "body": ["let ${1:name} = (${2:params}) -> ${0:body}"],
    "description": "Define a function"
  },
  "Pipeline": {
    "prefix": "pipe",
    "body": ["${1:value}", "  /> ${2:transform}", "  /> ${0:result}"],
    "description": "Create a pipeline"
  }
}
```

## Packaging & Publishing

```bash
# Install vsce
npm install -g @vscode/vsce

# Package extension
vsce package

# Publish to marketplace
vsce publish
```

## Reference Files

- [references/activation.md](references/activation.md) - Activation events
- [references/commands.md](references/commands.md) - Command registration
