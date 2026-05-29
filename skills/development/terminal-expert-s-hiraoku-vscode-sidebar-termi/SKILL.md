---
name: terminal-expert
description: This skill provides unified expert-level guidance for terminal implementation in VS Code extensions. Covers xterm.js API and addons, VS Code terminal architecture, PTY integration, session persistence, input handling (keyboard/IME/mouse), shell integration with OSC sequences, and performance optimization. Use when implementing any terminal-related features.
---

# Terminal Expert

## Overview

This skill provides comprehensive knowledge for implementing terminal features in VS Code extensions. It unifies xterm.js implementation details with VS Code's terminal architecture patterns, ensuring consistency with the official VS Code terminal implementation.

## When to Use This Skill

- Creating and configuring xterm.js Terminal instances
- Implementing terminal addons (fit, webgl, serialize, search, etc.)
- Integrating with VS Code WebViews
- Implementing PTY (pseudo-terminal) process management
- Creating terminal session persistence and restoration
- Handling keyboard input, IME composition, and mouse events
- Implementing shell integration with OSC 633 sequences
- Optimizing terminal performance (GPU acceleration, buffering)
- Managing terminal lifecycle and resource cleanup

## Quick Reference

### Essential Addons

| Addon | Package | Purpose | Loading |
|-------|---------|---------|---------|
| FitAddon | `@xterm/addon-fit` | Auto-resize to container | Always |
| WebglAddon | `@xterm/addon-webgl` | GPU acceleration (30%+ perf) | Lazy |
| SerializeAddon | `@xterm/addon-serialize` | Session persistence | Lazy |
| SearchAddon | `@xterm/addon-search` | Find in terminal | Lazy |
| Unicode11Addon | `@xterm/addon-unicode11` | Extended Unicode | Config |
| WebLinksAddon | `@xterm/addon-web-links` | Clickable URLs | Config |
| ImageAddon | `@xterm/addon-image` | Inline images | Config |

### Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Terminal creation | <500ms | Including PTY spawn |
| Session restore | <3s | 1000 lines scrollback |
| Terminal disposal | <100ms | Full cleanup |
| Resize handling | 100ms debounce | Prevents excessive calls |
| Output buffering | 16ms flush | ~60fps rendering |

---

## xterm.js Implementation

### Basic Terminal Setup

```typescript
import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import { WebglAddon } from '@xterm/addon-webgl';

class TerminalManager {
  private terminal: Terminal;
  private fitAddon: FitAddon;
  private container: HTMLElement;

  constructor(container: HTMLElement) {
    this.container = container;
    this.terminal = this.createTerminal();
    this.fitAddon = new FitAddon();
  }

  private createTerminal(): Terminal {
    return new Terminal({
      // Appearance
      fontFamily: '"Cascadia Code", "Fira Code", monospace',
      fontSize: 14,
      lineHeight: 1.2,
      cursorStyle: 'block',
      cursorBlink: true,

      // Behavior
      scrollback: 5000,
      altClickMovesCursor: true,

      // Performance
      fastScrollModifier: 'alt',
      smoothScrollDuration: 0,

      // Theme
      theme: {
        background: '#1e1e1e',
        foreground: '#d4d4d4',
        cursor: '#d4d4d4',
        selectionBackground: '#264f78'
      }
    });
  }

  initialize(): void {
    this.terminal.loadAddon(this.fitAddon);
    this.terminal.open(this.container);
    this.fitAddon.fit();
    this.setupResizeObserver();
  }

  private setupResizeObserver(): void {
    const resizeObserver = new ResizeObserver(() => {
      requestAnimationFrame(() => this.fitAddon.fit());
    });
    resizeObserver.observe(this.container);
  }
}
```

### WebGL Renderer with Fallback

```typescript
class RenderingManager {
  private webglAddon: WebglAddon | undefined;
  private terminal: Terminal;

  enableWebGL(): boolean {
    try {
      this.webglAddon = new WebglAddon();
      this.webglAddon.onContextLoss(() => {
        console.warn('WebGL context lost, falling back to canvas');
        this.disableWebGL();
      });
      this.terminal.loadAddon(this.webglAddon);
      return true;
    } catch (error) {
      console.warn('WebGL not available:', error);
      return false;
    }
  }

  disableWebGL(): void {
    this.webglAddon?.dispose();
    this.webglAddon = undefined;
  }
}
```

### Session Persistence with SerializeAddon

```typescript
import { SerializeAddon } from '@xterm/addon-serialize';

class ScrollbackManager {
  private serializeAddon: SerializeAddon;
  private terminal: Terminal;

  constructor(terminal: Terminal) {
    this.terminal = terminal;
    this.serializeAddon = new SerializeAddon();
    this.terminal.loadAddon(this.serializeAddon);
  }

  saveScrollback(options?: { scrollback?: number }): string {
    return this.serializeAddon.serialize({
      scrollback: options?.scrollback ?? 1000,
      excludeModes: true,
      excludeAltBuffer: true
    });
  }

  restoreScrollback(content: string): void {
    this.terminal.write(content);
  }
}
```

### Output Buffering for High-Frequency Output

```typescript
class OutputBuffer {
  private terminal: Terminal;
  private buffer: string = '';
  private flushScheduled = false;
  private flushInterval: number;

  constructor(terminal: Terminal, flushInterval: number = 16) {
    this.terminal = terminal;
    this.flushInterval = flushInterval;
  }

  write(data: string): void {
    this.buffer += data;

    // Detect high-frequency output
    if (this.buffer.length > 10000) {
      this.flushInterval = 4; // 250fps for AI agents
    }

    this.scheduleFlush();
  }

  private scheduleFlush(): void {
    if (!this.flushScheduled) {
      this.flushScheduled = true;
      setTimeout(() => this.flush(), this.flushInterval);
    }
  }

  private flush(): void {
    if (this.buffer.length > 0) {
      this.terminal.write(this.buffer);
      this.buffer = '';
    }
    this.flushScheduled = false;

    // Reset to normal frequency after idle
    if (this.buffer.length === 0) {
      this.flushInterval = 16;
    }
  }
}
```

---

## VS Code Integration

### Multi-Process Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Main Process (Electron)                                      │
└───────────────────┬─────────────────────────────────────────┘
        ┌───────────┼───────────┬──────────────────┐
        ▼           ▼           ▼                  ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Renderer     │ │ Extension    │ │ PTY Host     │ │ Shared       │
│ Process      │ │ Host Process │ │ Process      │ │ Process      │
├──────────────┤ ├──────────────┤ ├──────────────┤ ├──────────────┤
│ - Workbench  │ │ - Extension  │ │ - PtyService │ │ - Extension  │
│ - XtermTerm  │ │   execution  │ │ - node-pty   │ │   mgmt       │
│ - UI         │ │ - ExtHost    │ │ - Shell      │ │              │
└──────────────┘ │   Terminal   │ │   processes  │ └──────────────┘
                 └──────────────┘ └──────────────┘
```

### PTY Integration Pattern

```typescript
import * as pty from 'node-pty';

class TerminalProcess {
  private _ptyProcess: pty.IPty;

  constructor(
    shellPath: string,
    args: string[],
    cwd: string,
    cols: number,
    rows: number,
    env: { [key: string]: string }
  ) {
    this._ptyProcess = pty.spawn(shellPath, args, {
      name: 'xterm-256color',
      cols,
      rows,
      cwd,
      env
    });

    this._ptyProcess.onData(data => this._onData.fire(data));
    this._ptyProcess.onExit(({ exitCode }) => this._onExit.fire(exitCode));
  }

  write(data: string): void {
    this._ptyProcess.write(data);
  }

  resize(cols: number, rows: number): void {
    if (cols < 1 || rows < 1) return; // Prevent native exceptions
    this._ptyProcess.resize(cols, rows);
  }

  shutdown(): void {
    this._ptyProcess.kill();
  }
}
```

### Flow Control (Critical for Performance)

```typescript
class FlowControlledProcess {
  private _unacknowledgedCharCount = 0;
  private _isPaused = false;
  private readonly HIGH_WATERMARK = 100000;
  private readonly LOW_WATERMARK = 5000;

  handleData(data: string): void {
    this._unacknowledgedCharCount += data.length;

    if (!this._isPaused && this._unacknowledgedCharCount > this.HIGH_WATERMARK) {
      this._ptyProcess.pause();
      this._isPaused = true;
    }

    this._onData.fire(data);
  }

  acknowledge(charCount: number): void {
    this._unacknowledgedCharCount -= charCount;

    if (this._isPaused && this._unacknowledgedCharCount <= this.LOW_WATERMARK) {
      this._ptyProcess.resume();
      this._isPaused = false;
    }
  }
}
```

---

## Input Handling

### Keyboard Input Flow

```
User Keypress → Browser KeyboardEvent → Custom key event handler
  → Check VS Code keybindings
  ├─→ [Match] → Execute command, preventDefault
  └─→ [No Match] → Pass to xterm.js → Emits onData → Write to PTY
```

### Custom Key Handler

```typescript
terminal.attachCustomKeyEventHandler((event: KeyboardEvent) => {
  // Ctrl+C for copy (when selection exists)
  if (event.ctrlKey && event.key === 'c' && terminal.hasSelection()) {
    navigator.clipboard.writeText(terminal.getSelection());
    return false;
  }

  // Ctrl+V for paste
  if (event.ctrlKey && event.key === 'v') {
    navigator.clipboard.readText().then(text => terminal.paste(text));
    return false;
  }

  // Custom shortcuts
  if (event.ctrlKey && event.key === 'l') {
    terminal.clear();
    return false;
  }

  return true; // Let xterm.js handle
});
```

### IME Composition (CJK Input)

```typescript
class IMEHandler {
  private _composing = false;

  handleCompositionStart(): void {
    this._composing = true;
  }

  handleCompositionEnd(text: string): void {
    this._composing = false;
    this._pty.write(text);
  }

  handleKeyDown(event: KeyboardEvent): boolean {
    if (this._composing) return false; // Don't process during composition
    return true;
  }
}
```

---

## Shell Integration (OSC 633)

### Protocol

```
OSC 633 ; A ST    → Prompt start
OSC 633 ; B ST    → Command line start
OSC 633 ; C ST    → Command execution start
OSC 633 ; D [; <ExitCode>] ST    → Command finished
OSC 633 ; P ; <Property>=<Value> ST    → Set property
```

### Shell Integration Addon

```typescript
class ShellIntegrationAddon implements ITerminalAddon {
  activate(terminal: Terminal): void {
    terminal.parser.registerOscHandler(633, data => {
      const [code, ...params] = data.split(';');
      switch (code) {
        case 'A': this._handlePromptStart(); return true;
        case 'B': this._handleCommandStart(); return true;
        case 'C': this._handleExecutionStart(); return true;
        case 'D':
          const exitCode = params[0] ? parseInt(params[0]) : undefined;
          this._handleCommandFinished(exitCode);
          return true;
      }
      return false;
    });
  }
}
```

---

## Lifecycle Management

### DisposableStore Pattern (from VS Code)

```typescript
abstract class Disposable implements IDisposable {
  private readonly _store = new DisposableStore();
  private _isDisposed = false;

  protected _register<T extends IDisposable>(disposable: T): T {
    if (this._isDisposed) {
      disposable.dispose();
      return disposable;
    }
    return this._store.add(disposable);
  }

  dispose(): void {
    if (this._isDisposed) return;
    this._isDisposed = true;
    this._store.dispose();
  }
}

class DisposableStore implements IDisposable {
  private readonly _toDispose = new Set<IDisposable>();

  add<T extends IDisposable>(disposable: T): T {
    this._toDispose.add(disposable);
    return disposable;
  }

  dispose(): void {
    // LIFO order for safety
    const items = Array.from(this._toDispose).reverse();
    this._toDispose.clear();
    items.forEach(item => item.dispose());
  }
}
```

---

## VS Code WebView Integration

### Complete Integration Example

```typescript
class XtermVSCodeIntegration {
  private terminal: Terminal;
  private vscode: any;
  private fitAddon: FitAddon;

  constructor(container: HTMLElement) {
    this.vscode = acquireVsCodeApi();
    this.terminal = new Terminal({
      fontFamily: 'var(--vscode-editor-font-family)',
      fontSize: 14,
      theme: this.getVSCodeTheme()
    });

    this.fitAddon = new FitAddon();
    this.terminal.loadAddon(this.fitAddon);
    this.terminal.open(container);
    this.fitAddon.fit();

    this.setupCommunication();
  }

  private getVSCodeTheme(): ITheme {
    const style = getComputedStyle(document.body);
    return {
      background: style.getPropertyValue('--vscode-terminal-background').trim() ||
                  style.getPropertyValue('--vscode-editor-background').trim(),
      foreground: style.getPropertyValue('--vscode-terminal-foreground').trim(),
      cursor: style.getPropertyValue('--vscode-terminalCursor-foreground').trim(),
      selectionBackground: style.getPropertyValue('--vscode-terminal-selectionBackground').trim()
    };
  }

  private setupCommunication(): void {
    // Send input to extension
    this.terminal.onData(data => {
      this.vscode.postMessage({ type: 'input', data });
    });

    // Receive output from extension
    window.addEventListener('message', event => {
      const message = event.data;
      switch (message.type) {
        case 'output': this.terminal.write(message.data); break;
        case 'resize': this.terminal.resize(message.cols, message.rows); break;
        case 'clear': this.terminal.clear(); break;
        case 'focus': this.terminal.focus(); break;
      }
    });

    this.vscode.postMessage({ type: 'ready' });
  }
}
```

---

## ANSI Escape Sequences Reference

```typescript
const ANSI = {
  // Cursor movement
  cursorUp: (n: number) => `\x1b[${n}A`,
  cursorDown: (n: number) => `\x1b[${n}B`,
  cursorPosition: (row: number, col: number) => `\x1b[${row};${col}H`,

  // Erase
  eraseLine: '\x1b[2K',
  eraseScreen: '\x1b[2J',

  // Text formatting
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  italic: '\x1b[3m',
  underline: '\x1b[4m',

  // Colors
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',

  // 256 colors
  fg256: (n: number) => `\x1b[38;5;${n}m`,
  bg256: (n: number) => `\x1b[48;5;${n}m`,

  // True color (24-bit)
  fgRGB: (r: number, g: number, b: number) => `\x1b[38;2;${r};${g};${b}m`,
  bgRGB: (r: number, g: number, b: number) => `\x1b[48;2;${r};${g};${b}m`,

  // Screen modes
  alternateScreen: '\x1b[?1049h',
  normalScreen: '\x1b[?1049l',
  hideCursor: '\x1b[?25l',
  showCursor: '\x1b[?25h'
};
```

---

## References

For detailed reference documentation:
- `references/xterm-api.md` - Complete xterm.js API reference
- `references/vscode-terminal.md` - VS Code terminal source reference
- `references/escape-sequences.md` - ANSI escape sequence reference

For implementation reference:
- VS Code Repository: https://github.com/microsoft/vscode
- Terminal source: `src/vs/workbench/contrib/terminal/`
- xterm.js: https://github.com/xtermjs/xterm.js
