---
name: umbraco-example-generator
description: Generate testable example extensions and run them in the Umbraco backoffice
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Umbraco Example Generator

Generate complete, testable example extensions for the Umbraco backoffice and run them using the Umbraco source's dev infrastructure.

## When to Use

- Creating demonstration extensions
- Building testable extension examples
- Rapid development with hot reload
- Testing extensions without .NET backend

## Related Skills

- **umbraco-unit-testing** - Add unit tests to examples
- **umbraco-mocked-backoffice** - E2E testing patterns
- **umbraco-backoffice** - Extension type blueprints

---

## Quick Start

### 1. Clone Umbraco source (one-time setup)

```bash
git clone https://github.com/umbraco/Umbraco-CMS
cd Umbraco-CMS/src/Umbraco.Web.UI.Client
npm install
```

### 2. Create your extension folder

```
my-extension/
├── index.ts           # REQUIRED - exports manifests
└── my-element.ts      # Your element(s)
```

### 3. Create index.ts (exports manifests)

```typescript
import './my-element.js';

export const manifests = [
  {
    type: 'dashboard',
    alias: 'My.Dashboard',
    name: 'My Dashboard',
    element: 'my-element',
    meta: { label: 'My Dashboard', pathname: 'my-dashboard' },
    conditions: [{ alias: 'Umb.Condition.SectionAlias', match: 'Umb.Section.Content' }]
  }
];
```

### 4. Create your element

```typescript
// my-element.ts
import { LitElement, html, customElement } from '@umbraco-cms/backoffice/external/lit';

@customElement('my-element')
export class MyElement extends LitElement {
  render() {
    return html`<uui-box headline="Hello">It works!</uui-box>`;
  }
}
```

### 5. Run it

```bash
cd Umbraco-CMS/src/Umbraco.Web.UI.Client
VITE_EXTERNAL_EXTENSION=/full/path/to/my-extension npm run dev:external
```

Open `http://localhost:5173` - your extension appears in the Content section.

---

## How It Works

The Umbraco source (`Umbraco-CMS/src/Umbraco.Web.UI.Client`) provides two ways to load extensions:

### 1. Internal Examples (`npm run example`)

Examples placed in the `examples/` folder inside the Umbraco source.

```bash
cd Umbraco-CMS/src/Umbraco.Web.UI.Client
npm run example
# Select from list of examples
```

**How it works**: Sets `VITE_EXAMPLE_PATH` and imports `./examples/{name}/index.ts`

### 2. External Extensions (`npm run dev:external`)

Extensions from **any location** on your filesystem - perfect for developing packages.

```bash
cd Umbraco-CMS/src/Umbraco.Web.UI.Client
VITE_EXTERNAL_EXTENSION=/path/to/your/extension npm run dev:external
```

**How it works**:
1. Sets `VITE_UMBRACO_USE_MSW=on` (mocked APIs)
2. Creates `@external-extension` alias pointing to your extension path
3. Imports `@external-extension/index.ts` and registers exports with `umbExtensionsRegistry`
4. Resolves `@umbraco-cms/backoffice/*` imports from the main project (avoids duplicate element registrations)

### Extension Loading (index.ts)

```typescript
// From Umbraco-CMS/src/Umbraco.Web.UI.Client/index.ts
if (import.meta.env.VITE_EXTERNAL_EXTENSION) {
  const js = await import('@external-extension/index.ts');
  if (js) {
    Object.keys(js).forEach((key) => {
      const value = js[key];
      if (Array.isArray(value)) {
        umbExtensionsRegistry.registerMany(value);
      } else if (typeof value === 'object') {
        umbExtensionsRegistry.register(value);
      }
    });
  }
}
```

**Key point**: Your `index.ts` must export manifests (arrays or objects) that get registered automatically.

---

## Setup

### Prerequisites

Clone and set up the Umbraco source:

```bash
git clone https://github.com/umbraco/Umbraco-CMS
cd Umbraco-CMS/src/Umbraco.Web.UI.Client
npm install
```

### Extension Structure

Your extension needs this minimal structure:

```
my-extension/
├── index.ts              # Exports manifests array (REQUIRED)
├── my-element.ts         # Your element(s)
├── my-context.ts         # Context (if needed)
├── package.json          # Optional - for IDE support and tests
├── tsconfig.json         # Optional - for IDE support
└── README.md             # Documentation
```

### Required: index.ts

Your `index.ts` **must** export manifests that will be registered:

```typescript
import './my-dashboard.element.js';

export const manifests = [
  {
    type: 'dashboard',
    alias: 'My.Dashboard',
    name: 'My Dashboard',
    element: 'my-dashboard',
    weight: 100,
    meta: {
      label: 'My Dashboard',
      pathname: 'my-dashboard'
    },
    conditions: [
      {
        alias: 'Umb.Condition.SectionAlias',
        match: 'Umb.Section.Content'
      }
    ]
  }
];
```

### Optional: package.json (for IDE support)

```json
{
  "name": "my-extension",
  "type": "module",
  "devDependencies": {
    "@umbraco-cms/backoffice": "^17.0.0",
    "typescript": "~5.8.0"
  }
}
```

**Important**: The `@umbraco-cms/backoffice` dependency is only for IDE TypeScript support. At runtime, imports are resolved from the main Umbraco project.

---

## Running Your Extension

### Start the mocked backoffice

```bash
cd /path/to/Umbraco-CMS/src/Umbraco.Web.UI.Client
VITE_EXTERNAL_EXTENSION=/absolute/path/to/my-extension npm run dev:external
```

### Open in browser

Navigate to `http://localhost:5173` - your extension is loaded automatically.

### Hot reload

Changes to your extension files trigger hot reload - no restart needed.

---

## Patterns

### Basic Element

```typescript
// my-dashboard.element.ts
import { LitElement, html, css, customElement } from '@umbraco-cms/backoffice/external/lit';

@customElement('my-dashboard')
export class MyDashboardElement extends LitElement {
  static override styles = css`
    :host {
      display: block;
      padding: var(--uui-size-layout-1);
    }
  `;

  override render() {
    return html`
      <uui-box headline="My Extension">
        <p>Running in the mocked backoffice!</p>
      </uui-box>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'my-dashboard': MyDashboardElement;
  }
}
```

### Element with Context

```typescript
import { html, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { EXAMPLE_MY_CONTEXT } from './my-context.js';

@customElement('example-my-feature-view')
export class ExampleMyFeatureViewElement extends UmbLitElement {
  @state()
  private _value?: string;

  constructor() {
    super();
    this.consumeContext(EXAMPLE_MY_CONTEXT, (context) => {
      this.observe(context.value, (value) => {
        this._value = value;
      });
    });
  }

  override render() {
    return html`
      <uui-box headline="My Feature Example">
        <p>Current value: ${this._value ?? 'Loading...'}</p>
      </uui-box>
    `;
  }
}

export default ExampleMyFeatureViewElement;

declare global {
  interface HTMLElementTagNameMap {
    'example-my-feature-view': ExampleMyFeatureViewElement;
  }
}
```

### Context

```typescript
import { UmbContextToken } from '@umbraco-cms/backoffice/context-api';
import { UmbContextBase } from '@umbraco-cms/backoffice/class-api';
import { UmbStringState } from '@umbraco-cms/backoffice/observable-api';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';

export class ExampleMyContext extends UmbContextBase {
  #value = new UmbStringState('initial');
  readonly value = this.#value.asObservable();

  constructor(host: UmbControllerHost) {
    super(host, EXAMPLE_MY_CONTEXT);
  }

  setValue(value: string) {
    this.#value.setValue(value);
  }

  getValue() {
    return this.#value.getValue();
  }

  public override destroy(): void {
    this.#value.destroy();
    super.destroy();
  }
}

export const EXAMPLE_MY_CONTEXT = new UmbContextToken<ExampleMyContext>(
  'ExampleMyContext'
);

export { ExampleMyContext as api };
```

---

## Adding Tests

### Unit Tests

Add unit tests using `@open-wc/testing`. See **umbraco-unit-testing** skill for full setup.

```bash
npm install --save-dev @open-wc/testing @web/test-runner @web/test-runner-playwright
```

### E2E Tests (Playwright)

Add E2E tests that run against the mocked backoffice. See **umbraco-mocked-backoffice** skill for patterns.

```bash
npm install --save-dev @playwright/test
npx playwright install chromium
```

---

## Examples

### Reference Example

**Location**: `./examples/workspace-feature-toggle/`

A complete standalone example demonstrating:
- Workspace context with `UmbArrayState`
- Workspace view consuming context
- Workspace action executing context methods
- Workspace footer app showing summary
- 38 unit tests + 13 E2E tests

```bash
cd examples/workspace-feature-toggle
npm install
npm test              # Unit tests
npm run test:e2e      # E2E tests (requires mocked backoffice running)
```

### Official Umbraco Examples

**Location**: `Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/`

27 official examples covering all extension types. Run any example:

```bash
cd Umbraco-CMS/src/Umbraco.Web.UI.Client
npm run example
# Select from list
```

---

## Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Directory | kebab-case describing feature | `workspace-context-counter` |
| Alias prefix | `example.` | `example.workspaceView.counter` |
| Element prefix | `example-` | `example-counter-view` |
| Context token | `EXAMPLE_` + SCREAMING_CASE | `EXAMPLE_COUNTER_CONTEXT` |

---

## Troubleshooting

### Extension not appearing

1. Check `index.ts` exports a `manifests` array
2. Verify the path in `VITE_EXTERNAL_EXTENSION` is absolute
3. Check browser console for `📦 Loading external extension from:` message
4. Ensure condition matches the section you're viewing

### Import errors

Imports should use `@umbraco-cms/backoffice/*`. The Vite plugin resolves these from the main project.

### "CustomElementRegistry" already defined

Your extension's `node_modules` is being used instead of the main project's. The `external-extension-resolver` plugin should handle this, but ensure:
- You're using `npm run dev:external`
- Imports use `@umbraco-cms/backoffice/*` not relative paths to node_modules

### Changes not hot reloading

Ensure the file is within the path specified by `VITE_EXTERNAL_EXTENSION`. Only files in that directory tree are watched.
