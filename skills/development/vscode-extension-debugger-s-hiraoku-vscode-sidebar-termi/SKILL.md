---
name: vscode-extension-debugger
description: This skill provides expert-level guidance for debugging and fixing bugs in VS Code extensions. Use when investigating runtime errors, fixing memory leaks, resolving WebView issues, debugging activation problems, fixing TypeScript type errors, or troubleshooting extension communication failures. Covers systematic debugging workflows, common bug patterns, root cause analysis, and prevention strategies.
---

# VS Code Extension Debugger

## Overview

This skill enables systematic debugging and bug fixing for VS Code extensions. It provides structured workflows for identifying root causes, analyzing error patterns, and implementing robust fixes while preventing regressions.

## When to Use This Skill

- Investigating runtime errors or crashes in extensions
- Fixing memory leaks and dispose handler issues
- Resolving WebView rendering or communication failures
- Debugging extension activation or deactivation problems
- Troubleshooting message passing between Extension and WebView
- Fixing TypeScript compilation errors
- Resolving race conditions and async operation issues
- Debugging terminal-related functionality

## Debugging Workflow

### Phase 1: Bug Triage and Reproduction

1. **Gather Information**
   - Error messages and stack traces
   - Steps to reproduce
   - Environment details (VS Code version, OS, extension version)
   - Frequency (always, intermittent, specific conditions)

2. **Classify Bug Type**

   | Category | Symptoms | Priority |
   |----------|----------|----------|
   | Crash | Extension host crash, unhandled rejection | P0 |
   | Memory Leak | Increasing memory usage over time | P0 |
   | Data Loss | State not persisted, data corruption | P0 |
   | Functionality | Feature not working as expected | P1 |
   | Performance | Slow response, UI lag | P1 |
   | UI/UX | Visual glitches, incorrect display | P2 |

3. **Create Minimal Reproduction**
   - Isolate the failing scenario
   - Document exact steps
   - Identify triggering conditions

### Phase 2: Root Cause Analysis

#### Error Analysis Strategy

```typescript
// Add strategic logging for investigation
console.log('[DEBUG] State before operation:', JSON.stringify(state));
try {
  await problematicOperation();
} catch (error) {
  console.error('[DEBUG] Error details:', {
    message: error.message,
    stack: error.stack,
    context: currentContext
  });
  throw error;
}
```

#### Common Root Cause Patterns

**1. Dispose Handler Issues**
```typescript
// Bug: Missing dispose registration
const listener = vscode.workspace.onDidChangeConfiguration(...);
// listener never disposed!

// Fix: Always register disposables
context.subscriptions.push(
  vscode.workspace.onDidChangeConfiguration(...)
);
```

**2. Race Conditions**
```typescript
// Bug: Concurrent operations conflict
async function createTerminal() {
  if (isCreating) return; // Insufficient guard
  isCreating = true;
  // ... creation logic
}

// Fix: Use atomic operation pattern
private creationPromise: Promise<void> | null = null;

async function createTerminal(): Promise<void> {
  if (this.creationPromise) {
    return this.creationPromise;
  }
  this.creationPromise = this.doCreateTerminal();
  try {
    await this.creationPromise;
  } finally {
    this.creationPromise = null;
  }
}
```

**3. WebView Message Timing**
```typescript
// Bug: Message sent before WebView ready
panel.webview.postMessage({ type: 'init', data });

// Fix: Wait for ready signal
panel.webview.onDidReceiveMessage(msg => {
  if (msg.type === 'ready') {
    panel.webview.postMessage({ type: 'init', data });
  }
});
```

**4. Null/Undefined Reference**
```typescript
// Bug: Assuming object exists
const terminal = this.terminals.get(id);
terminal.write(data); // Crash if undefined!

// Fix: Defensive access with early return
const terminal = this.terminals.get(id);
if (!terminal) {
  console.warn(`Terminal ${id} not found`);
  return;
}
terminal.write(data);
```

**5. Async/Await Errors**
```typescript
// Bug: Unhandled promise rejection
someAsyncFunction(); // No await, no catch!

// Fix: Proper error handling
try {
  await someAsyncFunction();
} catch (error) {
  vscode.window.showErrorMessage(`Operation failed: ${error.message}`);
}
```

### Phase 3: Fix Implementation

#### Fix Implementation Checklist

- [ ] Identify all affected code paths
- [ ] Consider edge cases and error scenarios
- [ ] Maintain backward compatibility
- [ ] Add defensive null checks
- [ ] Ensure proper error handling
- [ ] Register all disposables
- [ ] Add logging for debugging
- [ ] Consider performance impact

#### Safe Fix Patterns

**Pattern 1: Guard Clause**
```typescript
async function processTerminal(id: number): Promise<void> {
  // Early validation
  if (id < 1 || id > MAX_TERMINALS) {
    throw new Error(`Invalid terminal ID: ${id}`);
  }

  const terminal = this.getTerminal(id);
  if (!terminal) {
    console.warn(`Terminal ${id} not found, skipping`);
    return;
  }

  // Safe to proceed
  await terminal.process();
}
```

**Pattern 2: Try-Catch-Finally**
```typescript
async function safeOperation(): Promise<void> {
  const resource = await acquireResource();
  try {
    await performOperation(resource);
  } catch (error) {
    await handleError(error);
    throw error; // Re-throw after logging
  } finally {
    await releaseResource(resource); // Always cleanup
  }
}
```

**Pattern 3: Timeout Protection**
```typescript
async function operationWithTimeout<T>(
  operation: Promise<T>,
  timeoutMs: number
): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error('Operation timed out')), timeoutMs)
  );
  return Promise.race([operation, timeout]);
}
```

### Phase 4: Verification

#### Testing Strategy

1. **Unit Test the Fix**
```typescript
describe('Bug Fix: Terminal creation race condition', () => {
  it('should handle concurrent creation requests', async () => {
    const manager = new TerminalManager();

    // Simulate concurrent requests
    const results = await Promise.all([
      manager.createTerminal(),
      manager.createTerminal(),
      manager.createTerminal()
    ]);

    // Verify only expected terminals created
    expect(manager.getTerminalCount()).toBe(expectedCount);
  });
});
```

2. **Integration Test**
   - Test the actual user workflow
   - Verify fix in different scenarios
   - Check for regressions

3. **Manual Verification**
   - Follow original reproduction steps
   - Verify error no longer occurs
   - Test related functionality

## Common Bug Categories

### Memory Leaks

**Detection**
```typescript
// Add disposal tracking
class ResourceManager implements vscode.Disposable {
  private disposables: vscode.Disposable[] = [];
  private disposed = false;

  register(disposable: vscode.Disposable): void {
    if (this.disposed) {
      disposable.dispose();
      console.warn('Attempted to register after disposal');
      return;
    }
    this.disposables.push(disposable);
  }

  dispose(): void {
    if (this.disposed) return;
    this.disposed = true;

    // LIFO disposal order
    while (this.disposables.length) {
      const d = this.disposables.pop();
      try {
        d?.dispose();
      } catch (e) {
        console.error('Dispose error:', e);
      }
    }
  }
}
```

**Common Causes**
- Event listeners not removed
- Timers not cleared
- WebView panels not disposed
- File watchers not stopped

### WebView Issues

**Communication Failures**
```typescript
// Implement message queue for reliability
class MessageQueue {
  private queue: Message[] = [];
  private ready = false;

  setReady(): void {
    this.ready = true;
    this.flush();
  }

  send(message: Message): void {
    if (this.ready) {
      this.webview.postMessage(message);
    } else {
      this.queue.push(message);
    }
  }

  private flush(): void {
    while (this.queue.length) {
      this.webview.postMessage(this.queue.shift()!);
    }
  }
}
```

**Rendering Problems**
- Check CSP (Content Security Policy)
- Verify resource URIs use webview.asWebviewUri()
- Ensure styles load correctly
- Check for JavaScript errors in WebView DevTools

### Activation Issues

**Debugging Activation**
```typescript
export async function activate(context: vscode.ExtensionContext) {
  console.log('[Extension] Activation started');

  try {
    // Initialize services
    await initializeServices(context);
    console.log('[Extension] Services initialized');

    // Register commands
    registerCommands(context);
    console.log('[Extension] Commands registered');

    console.log('[Extension] Activation complete');
  } catch (error) {
    console.error('[Extension] Activation failed:', error);
    vscode.window.showErrorMessage(
      `Extension activation failed: ${error.message}`
    );
    throw error;
  }
}
```

**Common Causes**
- Incorrect activation events in package.json
- Exceptions during initialization
- Missing dependencies
- Circular imports

### TypeScript Errors

**Type Safety Fixes**
```typescript
// Bug: Implicit any and unsafe access
function processData(data) {
  return data.items.map(item => item.value);
}

// Fix: Explicit types and null safety
interface DataItem {
  value: string;
}

interface Data {
  items?: DataItem[];
}

function processData(data: Data): string[] {
  return data.items?.map(item => item.value) ?? [];
}
```

## Debugging Tools

### VS Code Built-in

1. **Extension Development Host**
   - F5 to launch debug session
   - Set breakpoints in extension code
   - Inspect variables and call stack

2. **Developer Tools**
   - Help > Toggle Developer Tools
   - Console for extension host logs
   - Network tab for WebView resources

3. **WebView Developer Tools**
   - Command Palette: "Developer: Open WebView Developer Tools"
   - Debug WebView JavaScript
   - Inspect DOM and styles

### Extension-Specific Debug Panel

```typescript
// Terminal State Debug Panel (Ctrl+Shift+D)
// Monitors: system state, terminal info, performance metrics
```

### Logging Best Practices

```typescript
// Structured logging with context
const logger = {
  debug: (component: string, message: string, data?: object) => {
    if (debugEnabled) {
      console.log(`[${component}] ${message}`, data ?? '');
    }
  },
  error: (component: string, message: string, error: Error) => {
    console.error(`[${component}] ${message}:`, {
      message: error.message,
      stack: error.stack
    });
  }
};
```

## Prevention Strategies

### Code Review Checklist

- [ ] All disposables registered in subscriptions
- [ ] Async operations have error handling
- [ ] Null checks for optional data
- [ ] No race conditions in concurrent operations
- [ ] WebView messages validated
- [ ] Timeouts for long-running operations
- [ ] Graceful degradation on failures

### Testing Requirements

- Unit tests for fixed functionality
- Regression tests for bug scenarios
- Integration tests for affected workflows
- Memory leak tests for resource management

## Resources

For detailed reference documentation:
- `references/common-bugs.md` - Catalog of common VS Code extension bugs
- `references/debugging-tools.md` - Comprehensive debugging tool guide
- `references/fix-patterns.md` - Proven fix implementation patterns
