---
name: vscode-extension-refactorer
description: This skill provides expert-level guidance for refactoring VS Code extension code. Use when extracting classes or functions, reducing code duplication, improving type safety, reorganizing module structure, applying design patterns, or optimizing performance. Covers systematic refactoring workflows, code smell detection, safe transformation techniques, and VS Code-specific patterns.
---

# VS Code Extension Refactorer

## Overview

This skill enables systematic and safe refactoring of VS Code extension code. It provides structured workflows for identifying improvement opportunities, applying proven refactoring techniques, and ensuring code quality while maintaining functionality.

## When to Use This Skill

- Extracting classes, methods, or modules from large files
- Reducing code duplication across the codebase
- Improving TypeScript type safety and interfaces
- Reorganizing module structure and dependencies
- Applying design patterns (Manager, Coordinator, Factory, etc.)
- Optimizing performance-critical code paths
- Preparing code for new feature development
- Cleaning up after rapid prototyping

## Refactoring Workflow

### Phase 1: Analysis and Planning

#### Code Smell Detection

| Smell | Indicators | Refactoring |
|-------|------------|-------------|
| Long Method | >50 lines, multiple responsibilities | Extract Method |
| Large Class | >500 lines, >10 public methods | Extract Class |
| Duplicate Code | Similar blocks in 2+ places | Extract Function/Class |
| Feature Envy | Method uses other class data extensively | Move Method |
| Data Clumps | Same parameters passed together | Introduce Parameter Object |
| Primitive Obsession | Overuse of primitives for domain concepts | Replace with Value Object |
| Long Parameter List | >4 parameters | Introduce Parameter Object |
| Divergent Change | Class changes for multiple reasons | Extract Class (SRP) |
| Shotgun Surgery | One change requires many file edits | Move Method, Inline Class |
| God Class | Class knows/does too much | Extract Class, Delegate |

#### Impact Assessment

```typescript
// Before refactoring, assess:
interface RefactoringAssessment {
  // Scope
  filesAffected: string[];
  publicApiChanges: boolean;
  breakingChanges: boolean;

  // Risk
  testCoverage: 'high' | 'medium' | 'low';
  complexity: 'high' | 'medium' | 'low';

  // Dependencies
  internalDependents: string[];
  externalDependents: string[];  // Other extensions, APIs
}
```

### Phase 2: Safe Refactoring Techniques

#### Extract Method

**Before**:
```typescript
async function processTerminals(): Promise<void> {
  // Validation logic (10 lines)
  if (!this.terminals) {
    throw new Error('Terminals not initialized');
  }
  if (this.terminals.size === 0) {
    console.log('No terminals to process');
    return;
  }

  // Processing logic (20 lines)
  for (const [id, terminal] of this.terminals) {
    const state = terminal.getState();
    if (state === 'running') {
      await terminal.sendCommand('status');
      const output = await terminal.waitForOutput();
      this.results.set(id, output);
    }
  }

  // Cleanup logic (10 lines)
  this.results.forEach((result, id) => {
    if (result.includes('error')) {
      this.terminals.get(id)?.restart();
    }
  });
}
```

**After**:
```typescript
async function processTerminals(): Promise<void> {
  this.validateTerminals();
  await this.collectTerminalStatuses();
  this.handleErrorResults();
}

private validateTerminals(): void {
  if (!this.terminals) {
    throw new Error('Terminals not initialized');
  }
  if (this.terminals.size === 0) {
    console.log('No terminals to process');
    return;
  }
}

private async collectTerminalStatuses(): Promise<void> {
  for (const [id, terminal] of this.terminals) {
    const state = terminal.getState();
    if (state === 'running') {
      await terminal.sendCommand('status');
      const output = await terminal.waitForOutput();
      this.results.set(id, output);
    }
  }
}

private handleErrorResults(): void {
  this.results.forEach((result, id) => {
    if (result.includes('error')) {
      this.terminals.get(id)?.restart();
    }
  });
}
```

#### Extract Class

**Before** (God Class):
```typescript
class TerminalManager {
  // Terminal management (proper responsibility)
  private terminals: Map<number, Terminal>;
  createTerminal(): Terminal { }
  disposeTerminal(id: number): void { }

  // UI concerns (wrong place)
  private statusBarItem: vscode.StatusBarItem;
  updateStatusBar(): void { }
  showNotification(msg: string): void { }

  // Persistence concerns (wrong place)
  saveState(): void { }
  loadState(): void { }
  migrateOldState(): void { }

  // Configuration concerns (wrong place)
  getConfig(key: string): unknown { }
  updateConfig(key: string, value: unknown): void { }
}
```

**After** (Single Responsibility):
```typescript
// Core terminal management
class TerminalManager {
  private terminals: Map<number, Terminal>;

  constructor(
    private ui: TerminalUIManager,
    private persistence: TerminalPersistence,
    private config: TerminalConfig
  ) {}

  createTerminal(): Terminal {
    const terminal = new Terminal(this.config.getShellPath());
    this.terminals.set(terminal.id, terminal);
    this.ui.updateStatusBar(this.terminals.size);
    this.persistence.saveState(this.getState());
    return terminal;
  }

  disposeTerminal(id: number): void {
    this.terminals.delete(id);
    this.ui.updateStatusBar(this.terminals.size);
    this.persistence.saveState(this.getState());
  }
}

// UI responsibility
class TerminalUIManager {
  private statusBarItem: vscode.StatusBarItem;

  updateStatusBar(count: number): void { }
  showNotification(msg: string): void { }
}

// Persistence responsibility
class TerminalPersistence {
  saveState(state: TerminalState): void { }
  loadState(): TerminalState { }
  migrateOldState(): void { }
}

// Configuration responsibility
class TerminalConfig {
  getShellPath(): string { }
  get(key: string): unknown { }
  update(key: string, value: unknown): void { }
}
```

#### Replace Conditional with Polymorphism

**Before**:
```typescript
function handleMessage(message: Message): void {
  switch (message.type) {
    case 'create':
      const terminal = createTerminal(message.config);
      sendResponse({ type: 'created', id: terminal.id });
      break;
    case 'write':
      const t = getTerminal(message.id);
      if (t) t.write(message.data);
      break;
    case 'resize':
      const term = getTerminal(message.id);
      if (term) term.resize(message.cols, message.rows);
      break;
    case 'dispose':
      disposeTerminal(message.id);
      sendResponse({ type: 'disposed', id: message.id });
      break;
    default:
      console.warn('Unknown message type:', message.type);
  }
}
```

**After**:
```typescript
interface MessageHandler {
  handle(message: Message): void;
}

class CreateHandler implements MessageHandler {
  handle(message: CreateMessage): void {
    const terminal = this.manager.createTerminal(message.config);
    this.sender.send({ type: 'created', id: terminal.id });
  }
}

class WriteHandler implements MessageHandler {
  handle(message: WriteMessage): void {
    this.manager.getTerminal(message.id)?.write(message.data);
  }
}

class ResizeHandler implements MessageHandler {
  handle(message: ResizeMessage): void {
    this.manager.getTerminal(message.id)?.resize(message.cols, message.rows);
  }
}

class DisposeHandler implements MessageHandler {
  handle(message: DisposeMessage): void {
    this.manager.disposeTerminal(message.id);
    this.sender.send({ type: 'disposed', id: message.id });
  }
}

// Message router
class MessageRouter {
  private handlers = new Map<string, MessageHandler>([
    ['create', new CreateHandler()],
    ['write', new WriteHandler()],
    ['resize', new ResizeHandler()],
    ['dispose', new DisposeHandler()]
  ]);

  route(message: Message): void {
    const handler = this.handlers.get(message.type);
    if (handler) {
      handler.handle(message);
    } else {
      console.warn('Unknown message type:', message.type);
    }
  }
}
```

#### Introduce Parameter Object

**Before**:
```typescript
function createTerminal(
  shell: string,
  cwd: string,
  env: Record<string, string>,
  cols: number,
  rows: number,
  scrollback: number,
  name?: string
): Terminal {
  // ...
}

// Caller must remember order
createTerminal('/bin/bash', '/home', {}, 80, 24, 1000, 'Main');
```

**After**:
```typescript
interface TerminalOptions {
  shell: string;
  cwd: string;
  env?: Record<string, string>;
  dimensions?: {
    cols: number;
    rows: number;
  };
  scrollback?: number;
  name?: string;
}

const DEFAULT_OPTIONS: Partial<TerminalOptions> = {
  env: {},
  dimensions: { cols: 80, rows: 24 },
  scrollback: 1000
};

function createTerminal(options: TerminalOptions): Terminal {
  const opts = { ...DEFAULT_OPTIONS, ...options };
  // ...
}

// Clear, self-documenting call
createTerminal({
  shell: '/bin/bash',
  cwd: '/home',
  name: 'Main'
});
```

### Phase 3: VS Code-Specific Patterns

#### Manager-Coordinator Pattern

Standard pattern for VS Code extensions with multiple concerns:

```typescript
// Coordinator orchestrates managers
class TerminalWebviewManager implements ICoordinator {
  private managers: Map<string, IManager> = new Map();

  constructor(context: vscode.ExtensionContext) {
    // Initialize managers
    this.managers.set('message', new MessageManager(this));
    this.managers.set('ui', new UIManager(this));
    this.managers.set('input', new InputManager(this));
    this.managers.set('performance', new PerformanceManager(this));
  }

  getManager<T extends IManager>(name: string): T {
    return this.managers.get(name) as T;
  }

  async initialize(): Promise<void> {
    for (const manager of this.managers.values()) {
      await manager.initialize();
    }
  }

  dispose(): void {
    // Dispose in reverse order
    const managers = Array.from(this.managers.values()).reverse();
    for (const manager of managers) {
      manager.dispose();
    }
  }
}

// Individual manager interface
interface IManager extends vscode.Disposable {
  initialize(): Promise<void>;
}

// Example manager implementation
class MessageManager implements IManager {
  constructor(private coordinator: ICoordinator) {}

  async initialize(): Promise<void> {
    // Setup message handling
  }

  dispose(): void {
    // Cleanup
  }
}
```

#### Service Locator Pattern

For complex dependency management:

```typescript
class ServiceContainer {
  private services = new Map<string, unknown>();
  private factories = new Map<string, () => unknown>();

  register<T>(key: string, instance: T): void {
    this.services.set(key, instance);
  }

  registerFactory<T>(key: string, factory: () => T): void {
    this.factories.set(key, factory);
  }

  get<T>(key: string): T {
    if (this.services.has(key)) {
      return this.services.get(key) as T;
    }

    const factory = this.factories.get(key);
    if (factory) {
      const instance = factory() as T;
      this.services.set(key, instance);
      return instance;
    }

    throw new Error(`Service not found: ${key}`);
  }
}

// Usage
const container = new ServiceContainer();
container.register('config', new ConfigService());
container.registerFactory('terminal', () => new TerminalService(
  container.get('config')
));
```

#### Disposable Chain Pattern

Proper resource cleanup:

```typescript
class DisposableChain implements vscode.Disposable {
  private chain: vscode.Disposable[] = [];

  add<T extends vscode.Disposable>(disposable: T): T {
    this.chain.push(disposable);
    return disposable;
  }

  addFunction(fn: () => void): void {
    this.chain.push({ dispose: fn });
  }

  dispose(): void {
    // LIFO disposal
    while (this.chain.length) {
      const d = this.chain.pop();
      try {
        d?.dispose();
      } catch (e) {
        console.error('Dispose error:', e);
      }
    }
  }
}

// Usage in extension
export function activate(context: vscode.ExtensionContext) {
  const disposables = new DisposableChain();

  const config = disposables.add(new ConfigService());
  const terminal = disposables.add(new TerminalService(config));
  const ui = disposables.add(new UIService(terminal));

  context.subscriptions.push(disposables);
}
```

### Phase 4: Type Safety Improvements

#### Replace `any` with Proper Types

**Before**:
```typescript
function processMessage(message: any): any {
  if (message.type === 'data') {
    return message.payload.items.map((item: any) => item.value);
  }
  return null;
}
```

**After**:
```typescript
interface DataMessage {
  type: 'data';
  payload: {
    items: Array<{ value: string }>;
  };
}

interface ErrorMessage {
  type: 'error';
  error: string;
}

type Message = DataMessage | ErrorMessage;

function processMessage(message: Message): string[] | null {
  if (message.type === 'data') {
    return message.payload.items.map(item => item.value);
  }
  return null;
}
```

#### Discriminated Unions

**Before**:
```typescript
interface TerminalState {
  status: string;
  data?: string;
  error?: Error;
  progress?: number;
}

// Caller must check multiple fields
function render(state: TerminalState): void {
  if (state.status === 'loading' && state.progress !== undefined) {
    showProgress(state.progress);
  } else if (state.status === 'success' && state.data) {
    showData(state.data);
  } else if (state.status === 'error' && state.error) {
    showError(state.error);
  }
}
```

**After**:
```typescript
type TerminalState =
  | { status: 'idle' }
  | { status: 'loading'; progress: number }
  | { status: 'success'; data: string }
  | { status: 'error'; error: Error };

// Type narrowing with exhaustive check
function render(state: TerminalState): void {
  switch (state.status) {
    case 'idle':
      showIdle();
      break;
    case 'loading':
      showProgress(state.progress); // progress guaranteed
      break;
    case 'success':
      showData(state.data); // data guaranteed
      break;
    case 'error':
      showError(state.error); // error guaranteed
      break;
    default:
      const _exhaustive: never = state;
      throw new Error(`Unhandled state: ${_exhaustive}`);
  }
}
```

#### Generic Constraints

**Before**:
```typescript
class Repository<T> {
  private items: T[] = [];

  add(item: T): void {
    this.items.push(item);
  }

  findById(id: number): T | undefined {
    // Can't access .id because T is unconstrained
    return this.items.find((item: any) => item.id === id);
  }
}
```

**After**:
```typescript
interface Identifiable {
  id: number;
}

class Repository<T extends Identifiable> {
  private items: T[] = [];

  add(item: T): void {
    this.items.push(item);
  }

  findById(id: number): T | undefined {
    return this.items.find(item => item.id === id); // Type-safe
  }

  update(id: number, updates: Partial<Omit<T, 'id'>>): boolean {
    const item = this.findById(id);
    if (item) {
      Object.assign(item, updates);
      return true;
    }
    return false;
  }
}
```

### Phase 5: Verification

#### Refactoring Checklist

- [ ] All tests pass after refactoring
- [ ] No new TypeScript errors introduced
- [ ] Public API maintained (or documented changes)
- [ ] Performance not degraded
- [ ] Memory usage stable
- [ ] No circular dependencies introduced
- [ ] Documentation updated if needed

#### Testing Strategy

```typescript
// Before refactoring: Capture behavior
describe('TerminalManager (before refactor)', () => {
  it('creates terminal with correct config', () => {
    const result = manager.createTerminal(config);
    expect(result).toMatchSnapshot();
  });
});

// After refactoring: Same tests must pass
describe('TerminalManager (after refactor)', () => {
  it('creates terminal with correct config', () => {
    const result = manager.createTerminal(config);
    expect(result).toMatchSnapshot(); // Same snapshot
  });
});
```

## Common Refactoring Scenarios

### Scenario 1: Breaking Up a Large File

```
src/terminal.ts (2000 lines)
↓ Split by responsibility
src/terminal/
├── index.ts           # Public exports
├── TerminalManager.ts # Core management
├── TerminalFactory.ts # Creation logic
├── TerminalState.ts   # State management
├── types.ts           # Interfaces and types
└── utils.ts           # Helper functions
```

### Scenario 2: Reducing Coupling

```typescript
// Before: Tight coupling
class TerminalManager {
  private ui = new UIManager();  // Direct instantiation
  private config = new ConfigManager();
}

// After: Dependency injection
class TerminalManager {
  constructor(
    private ui: IUIManager,
    private config: IConfigManager
  ) {}
}

// Factory handles wiring
function createTerminalManager(): TerminalManager {
  return new TerminalManager(
    new UIManager(),
    new ConfigManager()
  );
}
```

### Scenario 3: Async Refactoring

```typescript
// Before: Callback hell
function loadData(callback: (data: Data) => void): void {
  readFile(path, (err, content) => {
    if (err) throw err;
    parseData(content, (err, parsed) => {
      if (err) throw err;
      validateData(parsed, (err, valid) => {
        if (err) throw err;
        callback(valid);
      });
    });
  });
}

// After: Async/await
async function loadData(): Promise<Data> {
  const content = await readFile(path);
  const parsed = await parseData(content);
  return validateData(parsed);
}
```

## Resources

For detailed reference documentation:
- `references/code-smells.md` - Complete code smell catalog with examples
- `references/design-patterns.md` - VS Code-specific design pattern implementations
- `references/type-patterns.md` - Advanced TypeScript type patterns
