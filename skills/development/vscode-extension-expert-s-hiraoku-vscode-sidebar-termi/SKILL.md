---
name: vscode-extension-expert
description: This skill provides expert-level guidance for VS Code extension development. Use when implementing new extension features, debugging extension code, designing WebView UIs, implementing Language Server Protocol features, or optimizing extension performance. Covers activation events, contribution points, VS Code API patterns, security best practices, testing strategies, and publishing workflows.
---

# VS Code Extension Expert

## Overview

This skill enables expert-level VS Code extension development by providing comprehensive knowledge of the VS Code Extension API, architectural patterns, security requirements, and best practices. It should be used when creating new extensions, adding features to existing extensions, implementing WebViews, designing language support, or optimizing performance.

## When to Use This Skill

- Implementing new VS Code extension features
- Designing extension architecture and structure
- Creating WebView-based UIs with proper security
- Implementing Language Server Protocol (LSP) features
- Debugging extension activation or runtime issues
- Optimizing extension performance and startup time
- Preparing extensions for Marketplace publication

## Core Concepts

### Extension Anatomy

Every VS Code extension requires:

```
extension-name/
├── .vscode/              # Debug configurations
│   ├── launch.json
│   └── tasks.json
├── src/
│   └── extension.ts      # Main entry point
├── package.json          # Extension manifest (critical)
├── tsconfig.json         # TypeScript config
└── .vscodeignore         # Exclude from package
```

### Package.json Essential Fields

```json
{
  "name": "extension-name",
  "publisher": "publisher-id",
  "version": "0.0.1",
  "engines": { "vscode": "^1.80.0" },
  "main": "./out/extension.js",
  "activationEvents": [],
  "contributes": {
    "commands": [],
    "configuration": {},
    "views": {}
  },
  "extensionKind": ["workspace"]
}
```

### Extension Entry Point Pattern

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  // Register commands, providers, listeners
  const disposable = vscode.commands.registerCommand('ext.command', () => {
    // Command implementation
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {
  // Cleanup resources
}
```

## Activation Events

Choose the most specific activation event to minimize startup impact:

| Event | Use Case | Example |
|-------|----------|---------|
| `onLanguage:<lang>` | Language-specific features | `onLanguage:python` |
| `onCommand:<command>` | Command-driven extensions | `onCommand:ext.showPanel` |
| `onView:<viewId>` | Sidebar view expansion | `onView:myTreeView` |
| `workspaceContains:<glob>` | Project-specific features | `workspaceContains:**/.eslintrc*` |
| `onFileSystem:<scheme>` | Custom file systems | `onFileSystem:sftp` |
| `onStartupFinished` | Background tasks | (prefer over `*`) |

**Critical**: Avoid using `*` as it activates on every VS Code startup.

## Contribution Points

### Commands

```json
{
  "contributes": {
    "commands": [{
      "command": "ext.doSomething",
      "title": "Do Something",
      "category": "My Extension",
      "icon": "$(symbol-method)"
    }]
  }
}
```

### Configuration

```json
{
  "contributes": {
    "configuration": {
      "title": "My Extension",
      "properties": {
        "myExtension.enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable the extension"
        }
      }
    }
  }
}
```

### Views (Tree Views)

```json
{
  "contributes": {
    "views": {
      "explorer": [{
        "id": "myTreeView",
        "name": "My View"
      }]
    },
    "viewsContainers": {
      "activitybar": [{
        "id": "myContainer",
        "title": "My Extension",
        "icon": "resources/icon.svg"
      }]
    }
  }
}
```

## VS Code API Namespaces

### window API

```typescript
// Show messages
vscode.window.showInformationMessage('Hello!');
vscode.window.showErrorMessage('Error occurred');

// Quick picks
const item = await vscode.window.showQuickPick(['Option 1', 'Option 2']);

// Input boxes
const input = await vscode.window.showInputBox({ prompt: 'Enter value' });

// Active editor
const editor = vscode.window.activeTextEditor;
```

### workspace API

```typescript
// Read configuration
const config = vscode.workspace.getConfiguration('myExtension');
const value = config.get<boolean>('enabled');

// Watch files
const watcher = vscode.workspace.createFileSystemWatcher('**/*.ts');
watcher.onDidChange(uri => { /* handle change */ });

// Open documents
const doc = await vscode.workspace.openTextDocument(uri);
```

### commands API

```typescript
// Register
const disposable = vscode.commands.registerCommand('ext.cmd', (arg) => {
  // Implementation
});

// Execute
await vscode.commands.executeCommand('ext.cmd', argument);
```

## WebView Development

### Security Requirements (Critical)

1. **Content Security Policy (CSP)** - Always implement strict CSP:

```typescript
function getWebviewContent(webview: vscode.Webview): string {
  const nonce = getNonce();

  return `<!DOCTYPE html>
  <html>
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy" content="
      default-src 'none';
      style-src ${webview.cspSource} 'unsafe-inline';
      script-src 'nonce-${nonce}';
      img-src ${webview.cspSource} https:;
    ">
  </head>
  <body>
    <script nonce="${nonce}">
      const vscode = acquireVsCodeApi();
      // Use vscode.postMessage() for communication
    </script>
  </body>
  </html>`;
}
```

2. **Input Sanitization** - Always sanitize user input
3. **HTTPS Only** - External resources must use HTTPS
4. **Minimal Permissions** - Limit `localResourceRoots`

### Message Passing Pattern

```typescript
// Extension → WebView
panel.webview.postMessage({ type: 'update', data: payload });

// WebView → Extension
panel.webview.onDidReceiveMessage(message => {
  switch (message.type) {
    case 'action':
      handleAction(message.data);
      break;
  }
});

// In WebView JavaScript
window.addEventListener('message', event => {
  const message = event.data;
  // Handle message
});

vscode.postMessage({ type: 'action', data: result });
```

### State Persistence

```typescript
// Simple state (survives webview hide/show)
const state = webview.getState() || { count: 0 };
webview.setState({ count: state.count + 1 });

// Full persistence (survives VS Code restart)
class MySerializer implements vscode.WebviewPanelSerializer {
  async deserializeWebviewPanel(panel: vscode.WebviewPanel, state: any) {
    panel.webview.html = getHtmlForWebview(panel.webview, state);
  }
}

vscode.window.registerWebviewPanelSerializer('myWebview', new MySerializer());
```

## Language Server Protocol (LSP)

### Architecture

```
┌─────────────────────┐     ┌─────────────────────┐
│  Language Client    │────│  Language Server    │
│  (VS Code Extension)│ LSP │  (Separate Process) │
│  vscode-languageclient    │  vscode-languageserver
└─────────────────────┘     └─────────────────────┘
```

### Client Implementation

```typescript
import { LanguageClient, LanguageClientOptions, ServerOptions } from 'vscode-languageclient/node';

const serverOptions: ServerOptions = {
  run: { module: serverPath, transport: TransportKind.ipc },
  debug: { module: serverPath, transport: TransportKind.ipc }
};

const clientOptions: LanguageClientOptions = {
  documentSelector: [{ scheme: 'file', language: 'mylang' }],
  synchronize: {
    fileEvents: vscode.workspace.createFileSystemWatcher('**/*.mylang')
  }
};

const client = new LanguageClient('mylang', 'My Language', serverOptions, clientOptions);
client.start();
```

### Server Implementation

```typescript
import { createConnection, TextDocuments, ProposedFeatures } from 'vscode-languageserver/node';
import { TextDocument } from 'vscode-languageserver-textdocument';

const connection = createConnection(ProposedFeatures.all);
const documents = new TextDocuments(TextDocument);

connection.onInitialize((params) => {
  return {
    capabilities: {
      textDocumentSync: TextDocumentSyncKind.Incremental,
      completionProvider: { resolveProvider: true },
      hoverProvider: true
    }
  };
});

connection.onCompletion((params) => {
  return [
    { label: 'suggestion1', kind: CompletionItemKind.Text }
  ];
});

documents.listen(connection);
connection.listen();
```

## Tree View Implementation

```typescript
class MyTreeDataProvider implements vscode.TreeDataProvider<MyItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<MyItem | undefined>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  refresh(): void {
    this._onDidChangeTreeData.fire(undefined);
  }

  getTreeItem(element: MyItem): vscode.TreeItem {
    return {
      label: element.name,
      collapsibleState: element.children ?
        vscode.TreeItemCollapsibleState.Collapsed :
        vscode.TreeItemCollapsibleState.None,
      command: {
        command: 'ext.selectItem',
        title: 'Select',
        arguments: [element]
      }
    };
  }

  getChildren(element?: MyItem): Thenable<MyItem[]> {
    if (!element) {
      return Promise.resolve(this.getRootItems());
    }
    return Promise.resolve(element.children || []);
  }
}

// Register
const provider = new MyTreeDataProvider();
vscode.window.registerTreeDataProvider('myTreeView', provider);
```

## Performance Best Practices

### Lazy Loading

```typescript
// Delay expensive imports
let heavyModule: typeof import('./heavyModule') | undefined;

async function getHeavyModule() {
  if (!heavyModule) {
    heavyModule = await import('./heavyModule');
  }
  return heavyModule;
}
```

### Bundling (Required for VS Code Web)

Use esbuild for fast bundling:

```javascript
// esbuild.config.js
const esbuild = require('esbuild');

esbuild.build({
  entryPoints: ['./src/extension.ts'],
  bundle: true,
  outfile: './out/extension.js',
  external: ['vscode'],
  format: 'cjs',
  platform: 'node',
  minify: process.env.NODE_ENV === 'production',
  sourcemap: true
});
```

### Resource Cleanup

```typescript
export function activate(context: vscode.ExtensionContext) {
  // Always add to subscriptions for automatic cleanup
  context.subscriptions.push(
    vscode.commands.registerCommand(...),
    vscode.window.registerTreeDataProvider(...),
    watcher,
    client
  );
}

export function deactivate() {
  // Explicit cleanup for async resources
  return client?.stop();
}
```

## Testing Strategy

### Integration Tests with @vscode/test-cli

```typescript
// .vscode-test.js
const { defineConfig } = require('@vscode/test-cli');

module.exports = defineConfig({
  files: 'out/test/**/*.test.js',
  version: 'stable',
  workspaceFolder: './test-fixtures',
  mocha: {
    timeout: 20000
  }
});
```

### Test Structure

```typescript
import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Test Suite', () => {
  vscode.window.showInformationMessage('Start tests.');

  test('Command registration', async () => {
    const commands = await vscode.commands.getCommands();
    assert.ok(commands.includes('ext.myCommand'));
  });

  test('Configuration access', () => {
    const config = vscode.workspace.getConfiguration('myExtension');
    assert.strictEqual(config.get('enabled'), true);
  });
});
```

## Common Pitfalls and Solutions

### Extension Not Activating

**Cause**: Activation events don't match user actions
**Solution**: Verify `activationEvents` in package.json match actual triggers

### WebView Security Errors

**Cause**: Missing or incorrect CSP
**Solution**: Always include strict Content-Security-Policy meta tag

### Memory Leaks

**Cause**: Untracked event listeners or disposables
**Solution**: Add all disposables to `context.subscriptions`

### Slow Startup

**Cause**: Synchronous heavy operations in `activate()`
**Solution**: Use lazy loading and defer non-critical initialization

### Commands Not in Palette

**Cause**: Missing `contributes.commands` declaration
**Solution**: Ensure command is declared in package.json AND registered with `registerCommand`

## Security Checklist

- [ ] Implement strict Content Security Policy for WebViews
- [ ] Sanitize all user input before rendering
- [ ] Use HTTPS for external resources
- [ ] Validate all messages from WebViews
- [ ] Limit `localResourceRoots` to necessary paths
- [ ] Use regex with word boundaries for URL validation (not `includes()`)
- [ ] Don't store secrets in settings (use `SecretStorage`)

## Publishing Checklist

- [ ] Unique name and publisher combination
- [ ] PNG icon (128x128 minimum)
- [ ] Complete README.md with features and screenshots
- [ ] CHANGELOG.md with version history
- [ ] LICENSE file
- [ ] Semantic versioning
- [ ] .vscodeignore excluding dev files
- [ ] Test on Windows, macOS, and Linux
- [ ] Bundle for web compatibility if needed

## Resources

For detailed reference documentation, see:
- `references/api-reference.md` - Complete VS Code API documentation
- `references/webview-security.md` - WebView security guidelines
- `references/lsp-guide.md` - Language Server Protocol implementation guide

For working examples, reference the official samples:
- https://github.com/microsoft/vscode-extension-samples
