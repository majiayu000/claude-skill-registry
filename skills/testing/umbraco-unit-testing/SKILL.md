---
name: umbraco-unit-testing
description: Unit and component testing for Umbraco backoffice extensions using @open-wc/testing
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Unit Testing

## What is it?

Unit testing for Umbraco backoffice extensions using `@open-wc/testing` - a testing framework designed for Web Components and Lit elements. This is the fastest and most isolated testing approach.

## When to Use

- Testing context logic and state management
- Testing Lit element rendering and shadow DOM
- Testing observable subscriptions and state changes
- Testing controllers and utility functions
- Fast feedback during development

## Related Skills

- **umbraco-testing** - Master skill for testing overview
- **umbraco-msw-testing** - Add API mocking to unit tests

## Documentation

- **@open-wc/testing**: https://open-wc.org/docs/testing/testing-package/
- **Web Test Runner**: https://modern-web.dev/docs/test-runner/overview/

---

## Setup

### Dependencies

Add to `package.json`:

```json
{
  "devDependencies": {
    "@open-wc/testing": "^4.0.0",
    "@web/dev-server-esbuild": "^1.0.0",
    "@web/dev-server-import-maps": "^0.2.0",
    "@web/test-runner": "^0.18.0",
    "@web/test-runner-playwright": "^0.11.0"
  },
  "scripts": {
    "test": "web-test-runner",
    "test:watch": "web-test-runner --watch"
  }
}
```

Then run:
```bash
npm install
npx playwright install chromium
```

### Configuration

Create `web-test-runner.config.mjs` in the project root:

```javascript
import { esbuildPlugin } from '@web/dev-server-esbuild';
import { playwrightLauncher } from '@web/test-runner-playwright';
import { importMapsPlugin } from '@web/dev-server-import-maps';

export default {
  rootDir: '.',
  files: ['./src/**/*.test.ts', '!**/node_modules/**'],
  nodeResolve: {
    exportConditions: ['development'],
    preferBuiltins: false,
    browser: false,
  },
  browsers: [playwrightLauncher({ product: 'chromium' })],
  plugins: [
    importMapsPlugin({
      inject: {
        importMap: {
          imports: {
            '@umbraco-cms/backoffice/external/lit': '/node_modules/lit/index.js',
            // CRITICAL: Use dist-cms, NOT dist/packages
            '@umbraco-cms/backoffice/lit-element':
              '/node_modules/@umbraco-cms/backoffice/dist-cms/packages/core/lit-element/index.js',
            // CRITICAL: libs are at dist-cms/libs/, NOT dist-cms/packages/
            '@umbraco-cms/backoffice/element-api':
              '/node_modules/@umbraco-cms/backoffice/dist-cms/libs/element-api/index.js',
            '@umbraco-cms/backoffice/observable-api':
              '/node_modules/@umbraco-cms/backoffice/dist-cms/libs/observable-api/index.js',
            '@umbraco-cms/backoffice/context-api':
              '/node_modules/@umbraco-cms/backoffice/dist-cms/libs/context-api/index.js',
            '@umbraco-cms/backoffice/controller-api':
              '/node_modules/@umbraco-cms/backoffice/dist-cms/libs/controller-api/index.js',
            '@umbraco-cms/backoffice/class-api':
              '/node_modules/@umbraco-cms/backoffice/dist-cms/packages/core/class-api/index.js',
            // Add other imports as needed
          },
        },
      },
    }),
    esbuildPlugin({
      ts: true,
      tsconfig: './tsconfig.json',
      target: 'auto',
      json: true,
    }),
  ],
  testRunnerHtml: (testFramework) =>
    `<html lang="en-us">
      <head>
        <meta charset="UTF-8" />
      </head>
      <body>
        <script type="module" src="${testFramework}"></script>
      </body>
    </html>`,
};
```

### Import Path Reference

| Type | Location | Example |
|------|----------|---------|
| **Libs** (low-level APIs) | `dist-cms/libs/` | `element-api`, `observable-api` |
| **Packages** (features) | `dist-cms/packages/` | `core/lit-element`, `core/class-api` |

**Common mistake**: Using `dist/packages` instead of `dist-cms` causes 404 errors.

---

## Alternative: Mock-Based Approach (Simpler)

For simpler unit tests that don't need the full Umbraco context system, mock the Umbraco imports entirely. This approach:
- Avoids complex import map configuration
- Runs faster (no loading Umbraco packages)
- Tests logic in true isolation
- Works well for testing types, constants, and observable patterns

### Simplified Configuration

```javascript
// web-test-runner.config.mjs
import { esbuildPlugin } from '@web/dev-server-esbuild';
import { importMapsPlugin } from '@web/dev-server-import-maps';
import { playwrightLauncher } from '@web/test-runner-playwright';

export default {
  files: 'src/**/*.test.ts',
  nodeResolve: true,
  browsers: [playwrightLauncher({ product: 'chromium' })],
  plugins: [
    esbuildPlugin({ ts: true }),
    importMapsPlugin({
      inject: {
        importMap: {
          imports: {
            // Map Umbraco imports to local mocks
            '@umbraco-cms/backoffice/external/lit': '/src/__mocks__/lit.js',
            '@umbraco-cms/backoffice/observable-api': '/src/__mocks__/observable-api.js',
            '@umbraco-cms/backoffice/class-api': '/src/__mocks__/class-api.js',
            // Add others as needed
          },
        },
      },
    }),
  ],
};
```

### Mock Files

Create `src/__mocks__/observable-api.js`:

```javascript
export class UmbStringState {
  #value;
  #subscribers = [];

  constructor(initialValue) {
    this.#value = initialValue;
  }

  getValue() { return this.#value; }

  setValue(value) {
    this.#value = value;
    this.#subscribers.forEach(cb => cb(value));
  }

  asObservable() {
    return {
      subscribe: (callback) => {
        this.#subscribers.push(callback);
        callback(this.#value);
        return { unsubscribe: () => {
          const idx = this.#subscribers.indexOf(callback);
          if (idx > -1) this.#subscribers.splice(idx, 1);
        }};
      }
    };
  }

  destroy() { this.#subscribers = []; }
}
```

Create `src/__mocks__/lit.js`:

```javascript
export const html = (strings, ...values) => ({ strings, values });
export const css = (strings, ...values) => ({ strings, values });
export const nothing = Symbol('nothing');
export const customElement = (name) => (target) => target;
export const state = () => (target, propertyKey) => {};
```

### Testing with Mocks

```typescript
import { expect } from '@open-wc/testing';
import { OUR_ENTITY_TYPE } from './types.js';

describe('Entity Types', () => {
  it('should define entity type', () => {
    expect(OUR_ENTITY_TYPE).to.equal('our-entity');
  });
});
```

### When to Use Each Approach

| Scenario | Approach |
|----------|----------|
| Testing types, constants, pure functions | Mock-based (simpler) |
| Testing observable state patterns | Mock-based (simpler) |
| Testing Lit elements with shadow DOM | Full Umbraco imports |
| Testing context consumption between elements | Full Umbraco imports |
| Testing with UUI components | Full Umbraco imports |

### Working Example

See **tree-example** in `umbraco-backoffice/examples/tree-example/Client/`:
- `web-test-runner.config.mjs` - Mock-based configuration
- `src/__mocks__/` - Mock implementations
- `src/**/*.test.ts` - Unit tests using mocks

### Directory Structure

```
my-extension/
├── src/
│   ├── my-context.ts
│   ├── my-context.test.ts      # Test alongside source
│   ├── my-element.ts
│   └── my-element.test.ts
├── web-test-runner.config.mjs
├── package.json
└── tsconfig.json
```

---

## Patterns

### Basic Test Structure

```typescript
import { expect, fixture, defineCE } from '@open-wc/testing';
import { html } from 'lit';

describe('MyFeature', () => {
  beforeEach(async () => {
    // Setup for each test
  });

  afterEach(() => {
    // Cleanup after each test
  });

  it('should do something', async () => {
    // Arrange, Act, Assert
  });
});
```

### Key Utilities

**`fixture()`** - Create and wait for element:
```typescript
const element = await fixture(html`<my-element></my-element>`);

// With parent node (for context consumption)
const element = await fixture(html`<my-element></my-element>`, {
  parentNode: hostElement,
});
```

**`defineCE()`** - Define custom element with unique tag:
```typescript
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

class TestHostElement extends UmbLitElement {}
const testHostTag = defineCE(TestHostElement);

const host = await fixture(`<${testHostTag}></${testHostTag}>`);
```

**`expect()`** - Chai assertions:
```typescript
expect(value).to.equal(5);
expect(value).to.be.true;
expect(array).to.have.length(3);
expect(element.shadowRoot?.textContent).to.include('Hello');
```

### Testing Contexts

```typescript
import { expect, fixture, defineCE } from '@open-wc/testing';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { MyContext } from './my-context.js';

class TestHostElement extends UmbLitElement {}
const testHostTag = defineCE(TestHostElement);

describe('MyContext', () => {
  let hostElement: UmbLitElement;
  let context: MyContext;

  beforeEach(async () => {
    hostElement = await fixture(`<${testHostTag}></${testHostTag}>`);
    context = new MyContext(hostElement);
  });

  it('initializes with default value', (done) => {
    context.value.subscribe((value) => {
      expect(value).to.equal(0);
      done();
    });
  });

  it('increments value', (done) => {
    let callCount = 0;
    context.value.subscribe((value) => {
      callCount++;
      if (callCount === 1) {
        expect(value).to.equal(0);
        context.increment();
      } else if (callCount === 2) {
        expect(value).to.equal(1);
        done();
      }
    });
  });
});
```

### Testing Lit Elements

```typescript
import { expect, fixture } from '@open-wc/testing';
import { html } from 'lit';
import './my-element.js';
import type { MyElement } from './my-element.js';

describe('MyElement', () => {
  let element: MyElement;

  beforeEach(async () => {
    element = await fixture(html`<my-element></my-element>`);
  });

  it('renders with default content', async () => {
    expect(element.shadowRoot?.textContent).to.include('Default Value');
  });

  it('updates display when property changes', async () => {
    element.value = 'New Value';
    await element.updateComplete;
    expect(element.shadowRoot?.textContent).to.include('New Value');
  });
});
```

### Testing Elements with Context

```typescript
import { expect, fixture, defineCE } from '@open-wc/testing';
import { html } from 'lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { MyContext } from './my-context.js';
import './my-view.js';

class TestHostElement extends UmbLitElement {}
const testHostTag = defineCE(TestHostElement);

describe('MyView', () => {
  let element: MyViewElement;
  let context: MyContext;
  let hostElement: UmbLitElement;

  beforeEach(async () => {
    // 1. Create host element
    hostElement = await fixture(`<${testHostTag}></${testHostTag}>`);

    // 2. Create context on host
    context = new MyContext(hostElement);

    // 3. Create element as child of host
    element = await fixture(html`<my-view></my-view>`, {
      parentNode: hostElement,
    });
    await element.updateComplete;
  });

  it('displays value from context', async () => {
    expect(element.shadowRoot?.textContent).to.include('Value: 0');
  });

  it('updates when context changes', async () => {
    context.increment();
    await element.updateComplete;
    expect(element.shadowRoot?.textContent).to.include('Value: 1');
  });
});
```

### Testing UI Interactions

UUI components use shadow DOM, so events need `composed: true`:

```typescript
// Clicking buttons
it('button click triggers action', async () => {
  const button = element.shadowRoot?.querySelector('uui-button') as HTMLElement;
  button.dispatchEvent(new MouseEvent('click', { bubbles: true, composed: true }));
  await element.updateComplete;
  expect(element.shadowRoot?.textContent).to.include('clicked');
});

// Toggling uui-toggle
it('toggle changes state', async () => {
  const toggle = element.shadowRoot?.querySelector('uui-toggle') as HTMLElement;
  toggle.dispatchEvent(new Event('change', { bubbles: true }));
  await element.updateComplete;
  expect(element.shadowRoot?.textContent).to.include('toggled');
});
```

### Observable State Behavior

**Important**: State objects only emit when values change:

```typescript
// This WILL emit twice (values different)
state.setValue(0);
state.setValue(1);

// This emits ONCE (same value - no second emission)
state.setValue(0);
state.setValue(0);
```

Testing no-op operations:
```typescript
it('does not go below 0', (done) => {
  let callCount = 0;
  context.count.subscribe((value) => {
    callCount++;
    if (callCount === 1) {
      expect(value).to.equal(0);
      context.decrement(); // Try to go below 0
      setTimeout(() => {
        expect(callCount).to.equal(1); // No second emission
        done();
      }, 50);
    }
  });
});
```

---

## Examples

### Complete Context Test

```typescript
import { expect, fixture, defineCE } from '@open-wc/testing';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { html } from '@umbraco-cms/backoffice/external/lit';
import { CounterContext } from './counter-context.js';
import './counter-view.js';

class TestHostElement extends UmbLitElement {}
const testHostTag = defineCE(TestHostElement);

describe('CounterContext', () => {
  let element: UmbLitElement;
  let context: CounterContext;

  beforeEach(async () => {
    element = await fixture(`<${testHostTag}></${testHostTag}>`);
    context = new CounterContext(element);
  });

  it('initializes with 0', (done) => {
    context.counter.subscribe((value) => {
      expect(value).to.equal(0);
      done();
    });
  });

  it('increments', (done) => {
    let callCount = 0;
    context.counter.subscribe((value) => {
      callCount++;
      if (callCount === 1) {
        context.increment();
      } else if (callCount === 2) {
        expect(value).to.equal(1);
        done();
      }
    });
  });

  it('resets to 0', (done) => {
    let callCount = 0;
    context.counter.subscribe((value) => {
      callCount++;
      if (callCount === 1) {
        context.increment();
        context.increment();
      } else if (callCount === 3) {
        context.reset();
      } else if (callCount === 4) {
        expect(value).to.equal(0);
        done();
      }
    });
  });
});

describe('CounterView', () => {
  let element: CounterViewElement;
  let context: CounterContext;
  let hostElement: UmbLitElement;

  beforeEach(async () => {
    hostElement = await fixture(`<${testHostTag}></${testHostTag}>`);
    context = new CounterContext(hostElement);
    element = await fixture(html`<counter-view></counter-view>`, {
      parentNode: hostElement,
    });
    await element.updateComplete;
  });

  it('shows initial value', async () => {
    expect(element.shadowRoot?.textContent).to.include('Count: 0');
  });

  it('reflects changes', async () => {
    context.increment();
    await element.updateComplete;
    expect(element.shadowRoot?.textContent).to.include('Count: 1');
  });
});
```

---

## Running Tests

```bash
# Run all unit tests
npm test

# Run in watch mode
npm run test:watch

# Run specific file
npx web-test-runner src/my-element.test.ts

# Run with coverage
npx web-test-runner --coverage
```

---

## Troubleshooting

### 404 errors for imports

Check import map paths. Use `dist-cms/libs/` for APIs and `dist-cms/packages/` for features.

### Element not defined

Ensure you import the element file before using it in tests:
```typescript
import './my-element.js'; // Side effect import registers element
```

### Context not available

Element must be child of host with context:
```typescript
element = await fixture(html`<my-element></my-element>`, {
  parentNode: hostElement, // Host must have context
});
```

### Observable tests hang

Use `done()` callback for async subscriptions:
```typescript
it('test', (done) => {
  observable.subscribe((value) => {
    expect(value).to.equal(expected);
    done(); // Signal completion
  });
});
```

### updateComplete not waiting

Ensure you await it:
```typescript
element.value = 'new';
await element.updateComplete; // Must await
expect(element.shadowRoot?.textContent).to.include('new');
```
