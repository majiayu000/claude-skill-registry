---
name: vscode-webview-expert
description: This skill provides expert-level guidance for implementing VS Code WebView features. Use when creating WebView panels, implementing secure CSP policies, handling Extension-WebView communication, managing WebView state persistence, optimizing WebView performance, or debugging WebView rendering issues. Covers security best practices, message protocols, and VS Code-specific WebView patterns.
---

# VS Code WebView Expert

## Overview

This skill enables expert-level implementation of VS Code WebView features. It provides comprehensive knowledge of WebView security requirements, communication patterns, state management, and performance optimization techniques specific to VS Code extensions.

## When to Use This Skill

- Creating new WebView panels or views
- Implementing Content Security Policy (CSP)
- Designing Extension ↔ WebView communication protocols
- Managing WebView state and persistence
- Handling WebView lifecycle events
- Optimizing WebView rendering performance
- Debugging WebView-related issues
- Implementing custom editors with WebViews

## WebView Fundamentals

### Creating WebView Panels

```typescript
import * as vscode from 'vscode';

class WebViewManager {
  private panel: vscode.WebviewPanel | undefined;

  show(context: vscode.ExtensionContext): void {
    if (this.panel) {
      this.panel.reveal();
      return;
    }

    this.panel = vscode.window.createWebviewPanel(
      'myWebview',           // viewType - unique identifier
      'My WebView',          // title
      vscode.ViewColumn.One, // column to show in
      {
        enableScripts: true,
        retainContextWhenHidden: true,  // Keep state when hidden
        localResourceRoots: [
          vscode.Uri.joinPath(context.extensionUri, 'media'),
          vscode.Uri.joinPath(context.extensionUri, 'dist')
        ]
      }
    );

    this.panel.webview.html = this.getHtmlContent(
      this.panel.webview,
      context.extensionUri
    );

    // Handle disposal
    this.panel.onDidDispose(() => {
      this.panel = undefined;
    });
  }
}
```

### WebView in Sidebar (TreeView alternative)

```typescript
class SidebarWebViewProvider implements vscode.WebviewViewProvider {
  private view?: vscode.WebviewView;

  constructor(private readonly extensionUri: vscode.Uri) {}

  resolveWebviewView(
    webviewView: vscode.WebviewView,
    context: vscode.WebviewViewResolveContext,
    token: vscode.CancellationToken
  ): void {
    this.view = webviewView;

    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this.extensionUri]
    };

    webviewView.webview.html = this.getHtmlContent(webviewView.webview);

    // Handle visibility changes
    webviewView.onDidChangeVisibility(() => {
      if (webviewView.visible) {
        this.refresh();
      }
    });
  }
}

// Register in package.json
/*
"contributes": {
  "views": {
    "explorer": [{
      "type": "webview",
      "id": "myWebviewView",
      "name": "My View"
    }]
  }
}
*/
```

## Security: Content Security Policy

### CSP Implementation (Critical)

```typescript
function getHtmlContent(
  webview: vscode.Webview,
  extensionUri: vscode.Uri
): string {
  // Generate unique nonce for scripts
  const nonce = getNonce();

  // Get resource URIs
  const styleUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, 'media', 'style.css')
  );
  const scriptUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, 'dist', 'webview.js')
  );

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Content-Security-Policy" content="
    default-src 'none';
    style-src ${webview.cspSource} 'unsafe-inline';
    script-src 'nonce-${nonce}';
    img-src ${webview.cspSource} https: data:;
    font-src ${webview.cspSource};
    connect-src https:;
  ">
  <link href="${styleUri}" rel="stylesheet">
  <title>My WebView</title>
</head>
<body>
  <div id="app"></div>
  <script nonce="${nonce}" src="${scriptUri}"></script>
</body>
</html>`;
}

function getNonce(): string {
  let text = '';
  const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  for (let i = 0; i < 32; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}
```

### CSP Directives Reference

| Directive | Purpose | Recommended Value |
|-----------|---------|-------------------|
| `default-src` | Fallback for other directives | `'none'` |
| `script-src` | JavaScript sources | `'nonce-${nonce}'` |
| `style-src` | Stylesheet sources | `${webview.cspSource} 'unsafe-inline'` |
| `img-src` | Image sources | `${webview.cspSource} https: data:` |
| `font-src` | Font sources | `${webview.cspSource}` |
| `connect-src` | XHR/Fetch destinations | `https:` or specific origins |
| `frame-src` | iframe sources | `'none'` (unless needed) |

### Common CSP Issues and Solutions

```typescript
// Issue: Inline styles not working
// Solution: Add 'unsafe-inline' to style-src (acceptable for styles)
style-src ${webview.cspSource} 'unsafe-inline';

// Issue: External images not loading
// Solution: Add https: to img-src
img-src ${webview.cspSource} https: data:;

// Issue: Web fonts not loading
// Solution: Ensure font-src includes cspSource
font-src ${webview.cspSource} https://fonts.gstatic.com;

// Issue: Fetch/XHR blocked
// Solution: Add connect-src with allowed origins
connect-src https://api.example.com;
```

## Extension ↔ WebView Communication

### Message Protocol Design

```typescript
// Shared message types (use in both Extension and WebView)
interface Message {
  type: string;
  payload?: unknown;
  id?: string;  // For request-response pattern
}

// Extension → WebView messages
type ExtensionMessage =
  | { type: 'init'; payload: { config: Config; state: State } }
  | { type: 'update'; payload: { data: Data } }
  | { type: 'theme-changed'; payload: { theme: 'light' | 'dark' } }
  | { type: 'response'; id: string; payload: unknown; error?: string };

// WebView → Extension messages
type WebViewMessage =
  | { type: 'ready' }
  | { type: 'action'; payload: { action: string; data: unknown } }
  | { type: 'request'; id: string; payload: { method: string; args: unknown[] } }
  | { type: 'error'; payload: { message: string; stack?: string } };
```

### Extension Side: Message Handling

```typescript
class WebViewMessageHandler {
  private pendingRequests = new Map<string, {
    resolve: (value: unknown) => void;
    reject: (error: Error) => void;
    timeout: NodeJS.Timeout;
  }>();

  constructor(private panel: vscode.WebviewPanel) {
    this.setupMessageHandler();
  }

  private setupMessageHandler(): void {
    this.panel.webview.onDidReceiveMessage(
      async (message: WebViewMessage) => {
        try {
          await this.handleMessage(message);
        } catch (error) {
          console.error('Message handling error:', error);
          this.sendError(error as Error);
        }
      }
    );
  }

  private async handleMessage(message: WebViewMessage): Promise<void> {
    switch (message.type) {
      case 'ready':
        await this.onWebViewReady();
        break;

      case 'action':
        await this.handleAction(message.payload);
        break;

      case 'request':
        await this.handleRequest(message.id!, message.payload);
        break;

      case 'error':
        console.error('WebView error:', message.payload);
        break;
    }
  }

  private async onWebViewReady(): Promise<void> {
    // Send initial state when WebView is ready
    this.send({
      type: 'init',
      payload: {
        config: await this.getConfig(),
        state: await this.getState()
      }
    });
  }

  private async handleRequest(id: string, payload: any): Promise<void> {
    try {
      const result = await this.executeMethod(payload.method, payload.args);
      this.send({ type: 'response', id, payload: result });
    } catch (error) {
      this.send({
        type: 'response',
        id,
        payload: null,
        error: (error as Error).message
      });
    }
  }

  send(message: ExtensionMessage): void {
    this.panel.webview.postMessage(message);
  }

  private sendError(error: Error): void {
    this.send({
      type: 'response',
      id: 'error',
      payload: null,
      error: error.message
    });
  }
}
```

### WebView Side: Message Handling

```typescript
// In WebView JavaScript
declare const acquireVsCodeApi: () => {
  postMessage(message: unknown): void;
  getState(): unknown;
  setState(state: unknown): void;
};

class VSCodeBridge {
  private vscode = acquireVsCodeApi();
  private pendingRequests = new Map<string, {
    resolve: (value: unknown) => void;
    reject: (error: Error) => void;
  }>();
  private ready = false;
  private messageQueue: unknown[] = [];

  constructor() {
    this.setupMessageListener();
    this.notifyReady();
  }

  private setupMessageListener(): void {
    window.addEventListener('message', (event) => {
      const message = event.data as ExtensionMessage;
      this.handleMessage(message);
    });
  }

  private handleMessage(message: ExtensionMessage): void {
    switch (message.type) {
      case 'init':
        this.ready = true;
        this.flushMessageQueue();
        this.onInit(message.payload);
        break;

      case 'update':
        this.onUpdate(message.payload);
        break;

      case 'theme-changed':
        this.onThemeChanged(message.payload.theme);
        break;

      case 'response':
        this.handleResponse(message);
        break;
    }
  }

  private handleResponse(message: ExtensionMessage & { type: 'response' }): void {
    const pending = this.pendingRequests.get(message.id!);
    if (pending) {
      this.pendingRequests.delete(message.id!);
      if (message.error) {
        pending.reject(new Error(message.error));
      } else {
        pending.resolve(message.payload);
      }
    }
  }

  // Request-response pattern
  async request<T>(method: string, ...args: unknown[]): Promise<T> {
    const id = crypto.randomUUID();

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.pendingRequests.delete(id);
        reject(new Error(`Request timeout: ${method}`));
      }, 10000);

      this.pendingRequests.set(id, {
        resolve: (value) => {
          clearTimeout(timeout);
          resolve(value as T);
        },
        reject: (error) => {
          clearTimeout(timeout);
          reject(error);
        }
      });

      this.send({ type: 'request', id, payload: { method, args } });
    });
  }

  send(message: WebViewMessage): void {
    if (!this.ready && message.type !== 'ready') {
      this.messageQueue.push(message);
      return;
    }
    this.vscode.postMessage(message);
  }

  private flushMessageQueue(): void {
    while (this.messageQueue.length > 0) {
      this.vscode.postMessage(this.messageQueue.shift());
    }
  }

  private notifyReady(): void {
    this.vscode.postMessage({ type: 'ready' });
  }

  // State persistence
  getState<T>(): T | undefined {
    return this.vscode.getState() as T | undefined;
  }

  setState<T>(state: T): void {
    this.vscode.setState(state);
  }

  // Override these in subclass
  protected onInit(payload: { config: any; state: any }): void {}
  protected onUpdate(payload: { data: any }): void {}
  protected onThemeChanged(theme: 'light' | 'dark'): void {}
}
```

## State Management

### WebView State Persistence

```typescript
// Simple state (survives hide/show, lost on reload)
class SimpleStateManager {
  private vscode = acquireVsCodeApi();

  save<T>(state: T): void {
    this.vscode.setState(state);
  }

  load<T>(): T | undefined {
    return this.vscode.getState() as T | undefined;
  }
}

// Full persistence (survives VS Code restart)
class PersistentStateManager {
  constructor(
    private context: vscode.ExtensionContext,
    private key: string
  ) {}

  async save<T>(state: T): Promise<void> {
    await this.context.globalState.update(this.key, state);
  }

  load<T>(): T | undefined {
    return this.context.globalState.get<T>(this.key);
  }
}

// WebView Serializer for panel restoration
class WebViewSerializer implements vscode.WebviewPanelSerializer {
  constructor(private manager: WebViewManager) {}

  async deserializeWebviewPanel(
    panel: vscode.WebviewPanel,
    state: unknown
  ): Promise<void> {
    // Restore panel with saved state
    this.manager.restorePanel(panel, state);
  }
}

// Register serializer
vscode.window.registerWebviewPanelSerializer('myWebview', new WebViewSerializer(manager));
```

### State Synchronization Pattern

```typescript
class StateSynchronizer<T> {
  private state: T;
  private webview: vscode.Webview;
  private context: vscode.ExtensionContext;
  private saveDebouncer: NodeJS.Timeout | undefined;

  constructor(
    webview: vscode.Webview,
    context: vscode.ExtensionContext,
    initialState: T
  ) {
    this.webview = webview;
    this.context = context;
    this.state = this.loadState() ?? initialState;
  }

  private loadState(): T | undefined {
    return this.context.workspaceState.get<T>('webviewState');
  }

  private async persistState(): Promise<void> {
    await this.context.workspaceState.update('webviewState', this.state);
  }

  update(partial: Partial<T>): void {
    this.state = { ...this.state, ...partial };

    // Notify WebView
    this.webview.postMessage({
      type: 'state-update',
      payload: this.state
    });

    // Debounced persistence
    if (this.saveDebouncer) {
      clearTimeout(this.saveDebouncer);
    }
    this.saveDebouncer = setTimeout(() => {
      this.persistState();
    }, 1000);
  }

  getState(): T {
    return this.state;
  }
}
```

## Performance Optimization

### Lazy Loading Resources

```typescript
function getHtmlContent(webview: vscode.Webview, extensionUri: vscode.Uri): string {
  const nonce = getNonce();

  return `<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="Content-Security-Policy" content="...">
  <!-- Critical CSS inline for fast first paint -->
  <style>
    body { font-family: var(--vscode-font-family); }
    .loading { display: flex; justify-content: center; }
  </style>
</head>
<body>
  <div id="app">
    <div class="loading">Loading...</div>
  </div>

  <!-- Defer non-critical resources -->
  <link rel="preload" href="${styleUri}" as="style" onload="this.rel='stylesheet'">

  <!-- Load scripts with defer -->
  <script nonce="${nonce}" src="${scriptUri}" defer></script>
</body>
</html>`;
}
```

### Message Batching

```typescript
class MessageBatcher {
  private queue: Message[] = [];
  private flushTimeout: NodeJS.Timeout | undefined;
  private readonly flushInterval = 16; // ~60fps

  constructor(private webview: vscode.Webview) {}

  send(message: Message): void {
    this.queue.push(message);
    this.scheduleFlush();
  }

  private scheduleFlush(): void {
    if (!this.flushTimeout) {
      this.flushTimeout = setTimeout(() => {
        this.flush();
      }, this.flushInterval);
    }
  }

  private flush(): void {
    if (this.queue.length === 0) return;

    // Send batch message
    this.webview.postMessage({
      type: 'batch',
      messages: this.queue
    });

    this.queue = [];
    this.flushTimeout = undefined;
  }

  dispose(): void {
    if (this.flushTimeout) {
      clearTimeout(this.flushTimeout);
      this.flush(); // Send remaining messages
    }
  }
}
```

### Virtual Scrolling for Large Lists

```typescript
// WebView side implementation
class VirtualList {
  private container: HTMLElement;
  private itemHeight = 24;
  private visibleItems = 50;
  private items: unknown[] = [];

  constructor(container: HTMLElement) {
    this.container = container;
    this.setupScrollHandler();
  }

  setItems(items: unknown[]): void {
    this.items = items;
    this.render();
  }

  private setupScrollHandler(): void {
    this.container.addEventListener('scroll', () => {
      requestAnimationFrame(() => this.render());
    });
  }

  private render(): void {
    const scrollTop = this.container.scrollTop;
    const startIndex = Math.floor(scrollTop / this.itemHeight);
    const endIndex = Math.min(
      startIndex + this.visibleItems,
      this.items.length
    );

    // Only render visible items
    const visibleItems = this.items.slice(startIndex, endIndex);

    // Update DOM with padding for scroll position
    this.container.innerHTML = `
      <div style="height: ${startIndex * this.itemHeight}px"></div>
      ${visibleItems.map(item => this.renderItem(item)).join('')}
      <div style="height: ${(this.items.length - endIndex) * this.itemHeight}px"></div>
    `;
  }

  private renderItem(item: unknown): string {
    return `<div class="item" style="height: ${this.itemHeight}px">${item}</div>`;
  }
}
```

## Theme Integration

### VS Code Theme Variables

```css
/* Use VS Code CSS variables for consistent theming */
body {
  background-color: var(--vscode-editor-background);
  color: var(--vscode-editor-foreground);
  font-family: var(--vscode-font-family);
  font-size: var(--vscode-font-size);
}

.button {
  background-color: var(--vscode-button-background);
  color: var(--vscode-button-foreground);
  border: none;
  padding: 4px 12px;
  cursor: pointer;
}

.button:hover {
  background-color: var(--vscode-button-hoverBackground);
}

.input {
  background-color: var(--vscode-input-background);
  color: var(--vscode-input-foreground);
  border: 1px solid var(--vscode-input-border);
  padding: 4px 8px;
}

.input:focus {
  outline: 1px solid var(--vscode-focusBorder);
}

.error {
  color: var(--vscode-errorForeground);
  background-color: var(--vscode-inputValidation-errorBackground);
  border: 1px solid var(--vscode-inputValidation-errorBorder);
}

.panel {
  background-color: var(--vscode-panel-background);
  border: 1px solid var(--vscode-panel-border);
}
```

### Theme Change Detection

```typescript
// Extension side
function watchThemeChanges(webview: vscode.Webview): vscode.Disposable {
  return vscode.window.onDidChangeActiveColorTheme((theme) => {
    webview.postMessage({
      type: 'theme-changed',
      payload: {
        kind: theme.kind, // 1=Light, 2=Dark, 3=HighContrast
        theme: theme.kind === vscode.ColorThemeKind.Dark ? 'dark' : 'light'
      }
    });
  });
}

// WebView side
window.addEventListener('message', (event) => {
  if (event.data.type === 'theme-changed') {
    document.body.dataset.theme = event.data.payload.theme;
  }
});
```

## Debugging WebViews

### Developer Tools Access

```typescript
// Command to open WebView DevTools
vscode.commands.registerCommand('myExt.openWebviewDevTools', () => {
  vscode.commands.executeCommand('workbench.action.webview.openDeveloperTools');
});
```

### Debug Logging

```typescript
// WebView side - comprehensive error handling
window.onerror = (message, source, lineno, colno, error) => {
  vscode.postMessage({
    type: 'error',
    payload: {
      message: String(message),
      source,
      lineno,
      colno,
      stack: error?.stack
    }
  });
};

window.addEventListener('unhandledrejection', (event) => {
  vscode.postMessage({
    type: 'error',
    payload: {
      message: 'Unhandled Promise rejection',
      reason: String(event.reason),
      stack: event.reason?.stack
    }
  });
});

// Debug logging utility
const debug = {
  log: (...args: unknown[]) => {
    console.log('[WebView]', ...args);
    vscode.postMessage({
      type: 'debug',
      payload: { level: 'log', args: args.map(String) }
    });
  },
  error: (...args: unknown[]) => {
    console.error('[WebView]', ...args);
    vscode.postMessage({
      type: 'debug',
      payload: { level: 'error', args: args.map(String) }
    });
  }
};
```

## Common Patterns

### Singleton Panel Pattern

```typescript
class SingletonWebViewManager {
  private static instance: SingletonWebViewManager;
  private panel: vscode.WebviewPanel | undefined;

  private constructor() {}

  static getInstance(): SingletonWebViewManager {
    if (!SingletonWebViewManager.instance) {
      SingletonWebViewManager.instance = new SingletonWebViewManager();
    }
    return SingletonWebViewManager.instance;
  }

  show(context: vscode.ExtensionContext): void {
    if (this.panel) {
      this.panel.reveal();
      return;
    }

    this.panel = vscode.window.createWebviewPanel(/* ... */);

    this.panel.onDidDispose(() => {
      this.panel = undefined;
    });
  }

  dispose(): void {
    this.panel?.dispose();
  }
}
```

### Multi-Panel Pattern

```typescript
class MultiPanelManager {
  private panels = new Map<string, vscode.WebviewPanel>();

  create(id: string, context: vscode.ExtensionContext): vscode.WebviewPanel {
    if (this.panels.has(id)) {
      const existing = this.panels.get(id)!;
      existing.reveal();
      return existing;
    }

    const panel = vscode.window.createWebviewPanel(
      'myWebview',
      `Panel ${id}`,
      vscode.ViewColumn.One,
      { enableScripts: true }
    );

    panel.onDidDispose(() => {
      this.panels.delete(id);
    });

    this.panels.set(id, panel);
    return panel;
  }

  get(id: string): vscode.WebviewPanel | undefined {
    return this.panels.get(id);
  }

  disposeAll(): void {
    this.panels.forEach(panel => panel.dispose());
    this.panels.clear();
  }
}
```

## Resources

For detailed reference documentation:
- `references/csp-reference.md` - Complete CSP directive reference
- `references/message-patterns.md` - Advanced message passing patterns
- `references/theming-guide.md` - VS Code theme integration guide
