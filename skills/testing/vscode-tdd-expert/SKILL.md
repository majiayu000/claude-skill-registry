---
name: vscode-tdd-expert
description: This skill provides expert-level guidance for Test-Driven Development (TDD) in VS Code extension development following t-wada methodology. Use when writing tests before implementation, creating comprehensive test suites, implementing Red-Green-Refactor cycles, or improving test coverage for extension components like WebViews, terminal managers, and activation logic.
---

# VS Code Extension TDD Expert

## Overview

This skill enables rigorous Test-Driven Development for VS Code extensions by providing comprehensive knowledge of testing frameworks, TDD workflows, and VS Code-specific testing patterns. It implements t-wada's TDD methodology adapted for extension development contexts.

## When to Use This Skill

- Writing tests before implementing new extension features
- Creating comprehensive test suites for WebView components
- Testing terminal management and lifecycle logic
- Implementing Red-Green-Refactor cycles for VS Code APIs
- Setting up test infrastructure for extension projects
- Debugging flaky or failing tests
- Improving test coverage for existing code

## Core TDD Principles (t-wada Methodology)

### The Three Laws of TDD

1. **Write no production code except to pass a failing test**
2. **Write only enough of a test to fail**
3. **Write only enough production code to pass the test**

### Red-Green-Refactor Cycle

```
┌──────────────────────────────────────────────────────┐
│                   TDD CYCLE                          │
│                                                      │
│   ┌─────────┐    ┌─────────┐    ┌──────────┐       │
│   │   RED   │───▶│  GREEN  │───▶│ REFACTOR │       │
│   │  Write  │    │  Make   │    │  Clean   │       │
│   │ failing │    │   it    │    │   up     │       │
│   │  test   │    │  pass   │    │  code    │       │
│   └─────────┘    └─────────┘    └──────────┘       │
│        ▲                              │             │
│        └──────────────────────────────┘             │
└──────────────────────────────────────────────────────┘
```

### TDD Workflow Commands

```bash
# Red phase - Write failing test
npm run tdd:red

# Green phase - Minimal implementation
npm run tdd:green

# Refactor phase - Improve code
npm run tdd:refactor

# Verify TDD compliance
npm run tdd:quality-gate
```

## VS Code Extension Testing Stack

### Required Dependencies

```json
{
  "devDependencies": {
    "@vscode/test-cli": "^0.0.10",
    "@vscode/test-electron": "^2.4.1",
    "mocha": "^10.7.3",
    "chai": "^5.1.2",
    "sinon": "^19.0.2",
    "sinon-chai": "^4.0.0",
    "@types/mocha": "^10.0.9",
    "@types/chai": "^5.0.1",
    "@types/sinon": "^17.0.3",
    "c8": "^10.1.2"
  }
}
```

### Test Configuration (.vscode-test.js)

```javascript
const { defineConfig } = require('@vscode/test-cli');

module.exports = defineConfig({
  files: 'out/test/**/*.test.js',
  version: 'stable',
  workspaceFolder: './test-fixtures',
  launchArgs: ['--disable-extensions'],
  mocha: {
    timeout: 20000,
    ui: 'bdd',
    color: true
  }
});
```

### Test Directory Structure

```
src/
├── test/
│   ├── unit/                    # Unit tests (no VS Code API)
│   │   ├── utils.test.ts
│   │   └── models.test.ts
│   ├── integration/             # Integration tests (VS Code API mocked)
│   │   ├── terminal.test.ts
│   │   └── webview.test.ts
│   ├── e2e/                     # End-to-end tests (real VS Code)
│   │   ├── activation.test.ts
│   │   └── commands.test.ts
│   ├── fixtures/                # Test data and fixtures
│   │   ├── mock-terminal.ts
│   │   └── sample-data.json
│   └── helpers/                 # Test utilities
│       ├── vscode-mock.ts
│       └── async-helpers.ts
```

## Testing VS Code Extension Components

### 1. Command Testing

```typescript
import * as assert from 'assert';
import * as vscode from 'vscode';
import * as sinon from 'sinon';

suite('Command Tests', () => {
  let sandbox: sinon.SinonSandbox;

  setup(() => {
    sandbox = sinon.createSandbox();
  });

  teardown(() => {
    sandbox.restore();
  });

  test('RED: createTerminal command should create new terminal', async () => {
    // Arrange - Setup expectations
    const createTerminalSpy = sandbox.spy(vscode.window, 'createTerminal');

    // Act - Execute command
    await vscode.commands.executeCommand('extension.createTerminal');

    // Assert - Verify behavior
    assert.strictEqual(createTerminalSpy.calledOnce, true);
  });
});
```

### 2. WebView Testing

```typescript
import { expect } from 'chai';
import * as sinon from 'sinon';
import { WebviewPanel } from 'vscode';
import { MyWebviewProvider } from '../../webview/MyWebviewProvider';

suite('WebView Provider Tests', () => {
  let sandbox: sinon.SinonSandbox;
  let mockPanel: sinon.SinonStubbedInstance<WebviewPanel>;

  setup(() => {
    sandbox = sinon.createSandbox();
    mockPanel = {
      webview: {
        html: '',
        postMessage: sandbox.stub().resolves(true),
        onDidReceiveMessage: sandbox.stub()
      },
      onDidDispose: sandbox.stub(),
      dispose: sandbox.stub()
    } as any;
  });

  teardown(() => {
    sandbox.restore();
  });

  test('RED: should handle message from webview', async () => {
    // Arrange
    const provider = new MyWebviewProvider();
    const message = { type: 'action', data: 'test' };

    // Act
    await provider.handleMessage(message);

    // Assert
    expect(mockPanel.webview.postMessage).to.have.been.calledWith({
      type: 'response',
      success: true
    });
  });
});
```

### 3. Terminal Manager Testing

```typescript
import { expect } from 'chai';
import * as sinon from 'sinon';
import { TerminalManager } from '../../terminals/TerminalManager';

suite('TerminalManager Tests', () => {
  let sandbox: sinon.SinonSandbox;
  let terminalManager: TerminalManager;

  setup(() => {
    sandbox = sinon.createSandbox();
    terminalManager = new TerminalManager();
  });

  teardown(() => {
    sandbox.restore();
    terminalManager.dispose();
  });

  test('RED: should recycle terminal IDs 1-5', async () => {
    // Arrange
    const terminal1 = await terminalManager.createTerminal();
    const terminal2 = await terminalManager.createTerminal();

    // Act - Delete first terminal
    await terminalManager.deleteTerminal(terminal1.id);
    const terminal3 = await terminalManager.createTerminal();

    // Assert - ID should be recycled
    expect(terminal3.id).to.equal(terminal1.id);
  });

  test('RED: should prevent creating more than 5 terminals', async () => {
    // Arrange - Create 5 terminals
    for (let i = 0; i < 5; i++) {
      await terminalManager.createTerminal();
    }

    // Act & Assert
    await expect(terminalManager.createTerminal())
      .to.be.rejectedWith('Maximum terminal limit reached');
  });
});
```

### 4. Configuration Testing

```typescript
import { expect } from 'chai';
import * as vscode from 'vscode';

suite('Configuration Tests', () => {
  const originalConfig: Map<string, any> = new Map();

  setup(async () => {
    // Save original config
    const config = vscode.workspace.getConfiguration('myExtension');
    originalConfig.set('enabled', config.get('enabled'));
  });

  teardown(async () => {
    // Restore original config
    const config = vscode.workspace.getConfiguration('myExtension');
    for (const [key, value] of originalConfig) {
      await config.update(key, value, vscode.ConfigurationTarget.Global);
    }
  });

  test('RED: should read configuration values', () => {
    // Arrange
    const config = vscode.workspace.getConfiguration('myExtension');

    // Act
    const enabled = config.get<boolean>('enabled');

    // Assert
    expect(enabled).to.be.a('boolean');
  });
});
```

### 5. Activation Testing

```typescript
import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Activation Tests', () => {
  test('RED: extension should activate', async () => {
    // Arrange
    const extensionId = 'publisher.extension-name';

    // Act
    const extension = vscode.extensions.getExtension(extensionId);
    await extension?.activate();

    // Assert
    assert.strictEqual(extension?.isActive, true);
  });

  test('RED: should register all commands', async () => {
    // Arrange
    const expectedCommands = [
      'extension.createTerminal',
      'extension.deleteTerminal',
      'extension.togglePanel'
    ];

    // Act
    const commands = await vscode.commands.getCommands();

    // Assert
    for (const cmd of expectedCommands) {
      assert.ok(commands.includes(cmd), `Command ${cmd} not registered`);
    }
  });
});
```

## Mocking VS Code API

### Creating VS Code Mocks

```typescript
// test/helpers/vscode-mock.ts
import * as sinon from 'sinon';

export function createMockExtensionContext(): vscode.ExtensionContext {
  return {
    subscriptions: [],
    workspaceState: {
      get: sinon.stub(),
      update: sinon.stub().resolves(),
      keys: sinon.stub().returns([])
    },
    globalState: {
      get: sinon.stub(),
      update: sinon.stub().resolves(),
      keys: sinon.stub().returns([]),
      setKeysForSync: sinon.stub()
    },
    secrets: {
      get: sinon.stub().resolves(undefined),
      store: sinon.stub().resolves(),
      delete: sinon.stub().resolves(),
      onDidChange: sinon.stub()
    },
    extensionUri: vscode.Uri.file('/mock/extension'),
    extensionPath: '/mock/extension',
    storagePath: '/mock/storage',
    globalStoragePath: '/mock/global-storage',
    logPath: '/mock/logs',
    extensionMode: vscode.ExtensionMode.Test,
    storageUri: vscode.Uri.file('/mock/storage'),
    globalStorageUri: vscode.Uri.file('/mock/global-storage'),
    logUri: vscode.Uri.file('/mock/logs'),
    asAbsolutePath: (path: string) => `/mock/extension/${path}`,
    environmentVariableCollection: {} as any,
    extension: {} as any,
    languageModelAccessInformation: {} as any
  } as vscode.ExtensionContext;
}

export function createMockTerminal(): vscode.Terminal {
  return {
    name: 'Mock Terminal',
    processId: Promise.resolve(12345),
    creationOptions: {},
    exitStatus: undefined,
    state: { isInteractedWith: false },
    sendText: sinon.stub(),
    show: sinon.stub(),
    hide: sinon.stub(),
    dispose: sinon.stub()
  } as unknown as vscode.Terminal;
}
```

### Stubbing VS Code Window

```typescript
// test/helpers/window-stubs.ts
import * as sinon from 'sinon';
import * as vscode from 'vscode';

export function stubWindowMethods(sandbox: sinon.SinonSandbox) {
  return {
    showInformationMessage: sandbox.stub(vscode.window, 'showInformationMessage'),
    showErrorMessage: sandbox.stub(vscode.window, 'showErrorMessage'),
    showWarningMessage: sandbox.stub(vscode.window, 'showWarningMessage'),
    showQuickPick: sandbox.stub(vscode.window, 'showQuickPick'),
    showInputBox: sandbox.stub(vscode.window, 'showInputBox'),
    createTerminal: sandbox.stub(vscode.window, 'createTerminal'),
    createWebviewPanel: sandbox.stub(vscode.window, 'createWebviewPanel')
  };
}
```

## Test Patterns for Common Scenarios

### Testing Async Operations

```typescript
import { expect } from 'chai';

test('RED: should handle async terminal creation', async () => {
  // Arrange
  const manager = new TerminalManager();

  // Act
  const terminal = await manager.createTerminal();

  // Assert
  expect(terminal).to.exist;
  expect(terminal.id).to.be.a('number');
});
```

### Testing Event Emitters

```typescript
import { expect } from 'chai';
import { EventEmitter } from 'vscode';

test('RED: should emit event on terminal creation', async () => {
  // Arrange
  const manager = new TerminalManager();
  const eventSpy = sinon.spy();
  manager.onDidCreateTerminal(eventSpy);

  // Act
  await manager.createTerminal();

  // Assert
  expect(eventSpy).to.have.been.calledOnce;
});
```

### Testing Disposables

```typescript
import { expect } from 'chai';

test('RED: should dispose all resources', () => {
  // Arrange
  const manager = new TerminalManager();
  const terminal = await manager.createTerminal();

  // Act
  manager.dispose();

  // Assert
  expect(manager.getTerminalCount()).to.equal(0);
  expect(manager.isDisposed).to.be.true;
});
```

### Testing Error Handling

```typescript
import { expect } from 'chai';

test('RED: should handle invalid shell path', async () => {
  // Arrange
  const manager = new TerminalManager();
  const invalidPath = '/nonexistent/shell';

  // Act & Assert
  await expect(manager.createTerminal({ shellPath: invalidPath }))
    .to.be.rejectedWith('Shell not found');
});
```

## Coverage Configuration

### c8 Configuration (package.json)

```json
{
  "c8": {
    "include": ["src/**/*.ts"],
    "exclude": ["src/test/**", "**/*.d.ts"],
    "reporter": ["text", "html", "lcov"],
    "all": true,
    "check-coverage": true,
    "branches": 80,
    "functions": 80,
    "lines": 80,
    "statements": 80
  }
}
```

### Coverage Commands

```bash
# Run tests with coverage
npm run test:coverage

# Generate HTML report
npx c8 report --reporter=html

# Check coverage thresholds
npx c8 check-coverage
```

## TDD Quality Gate

### Pre-commit Check Script

```typescript
// scripts/tdd-quality-gate.ts
import { execSync } from 'child_process';

function runTddQualityGate(): boolean {
  const checks = [
    { name: 'Unit Tests', cmd: 'npm run test:unit' },
    { name: 'Coverage Threshold', cmd: 'npx c8 check-coverage' },
    { name: 'Type Check', cmd: 'npm run compile' },
    { name: 'Lint', cmd: 'npm run lint' }
  ];

  for (const check of checks) {
    try {
      console.log(`Running ${check.name}...`);
      execSync(check.cmd, { stdio: 'inherit' });
      console.log(`✅ ${check.name} passed`);
    } catch (error) {
      console.error(`❌ ${check.name} failed`);
      return false;
    }
  }

  return true;
}
```

## Best Practices

### Test Naming Convention

```typescript
// Pattern: should [expected behavior] when [condition]
test('should create terminal with default shell when no options provided', async () => {
  // ...
});

test('should throw error when maximum terminals exceeded', async () => {
  // ...
});

test('should recycle ID when terminal is deleted', async () => {
  // ...
});
```

### Arrange-Act-Assert Pattern

```typescript
test('should update terminal title', async () => {
  // Arrange - Setup test conditions
  const terminal = await manager.createTerminal();
  const newTitle = 'New Title';

  // Act - Execute the operation
  await manager.setTerminalTitle(terminal.id, newTitle);

  // Assert - Verify the result
  expect(terminal.name).to.equal(newTitle);
});
```

### Test Isolation

```typescript
suite('TerminalManager Tests', () => {
  let manager: TerminalManager;

  // Fresh instance for each test
  setup(() => {
    manager = new TerminalManager();
  });

  // Cleanup after each test
  teardown(() => {
    manager.dispose();
  });
});
```

### Avoiding Test Interdependence

```typescript
// BAD - Tests depend on each other
test('should create terminal', () => { /* creates terminal */ });
test('should delete the terminal', () => { /* uses terminal from previous test */ });

// GOOD - Each test is independent
test('should create terminal', () => {
  const terminal = manager.createTerminal();
  expect(terminal).to.exist;
});

test('should delete terminal', () => {
  const terminal = manager.createTerminal();
  manager.deleteTerminal(terminal.id);
  expect(manager.getTerminal(terminal.id)).to.be.undefined;
});
```

## Common Pitfalls and Solutions

### Pitfall: Flaky Async Tests

**Problem**: Tests pass/fail randomly due to timing issues

**Solution**: Use proper async/await and explicit waits

```typescript
// BAD
test('flaky test', () => {
  manager.createTerminal();
  expect(manager.getTerminalCount()).to.equal(1);
});

// GOOD
test('stable test', async () => {
  await manager.createTerminal();
  expect(manager.getTerminalCount()).to.equal(1);
});
```

### Pitfall: Global State Pollution

**Problem**: Tests affect each other through shared state

**Solution**: Reset state in setup/teardown

```typescript
setup(() => {
  // Reset singleton state
  TerminalManager.resetInstance();
});
```

### Pitfall: Incomplete Cleanup

**Problem**: Resources leak between tests

**Solution**: Dispose all resources in teardown

```typescript
teardown(async () => {
  // Dispose all created terminals
  await manager.disposeAll();
  // Clear all event listeners
  manager.removeAllListeners();
});
```

## Resources

For detailed reference documentation, see:
- `references/testing-patterns.md` - VS Code-specific test patterns
- `references/mock-strategies.md` - Mocking VS Code API
- `references/coverage-guide.md` - Coverage configuration and analysis
