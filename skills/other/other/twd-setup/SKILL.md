---
name: twd-setup
description: TWD project setup guide — helps AI agents install and configure TWD (Test While Developing), an in-browser validation system, in a new or existing project. Use when setting up TWD, configuring Vite, or troubleshooting TWD initialization.
---

# TWD Project Setup Guide

You are helping set up **TWD (Test While Developing)**, an in-browser validation system for SPAs. Follow these steps carefully.

**Supported frameworks:** React, Vue, Angular, Solid.js, Astro (with React), React Router (Framework Mode)
**Not compatible with:** Next.js App Router, SSR-first architectures

## Security Context

- **Package provenance**: `twd-js` and `twd-relay` are published on npm by maintainer `brikev`. Source code: [BRIKEV/twd](https://github.com/BRIKEV/twd) and [BRIKEV/twd-relay](https://github.com/BRIKEV/twd-relay). License: MIT.
- **Dev-only scope**: All TWD code is guarded by `import.meta.env.DEV` and is tree-shaken out of production builds. TWD never runs in production.
- **Network scope (twd-relay)**: twd-relay operates exclusively on `localhost` via a WebSocket on the local Vite dev server. It makes no external network connections.

> **Note:** This skill provides user-directed setup guidance. The code blocks below are instructions for the developer to follow — they are not autonomously executed commands. This skill has no tool access and cannot run commands on its own.

## Step 1: Install TWD

```bash
npm install twd-js
```

## Step 2: Initialize Mock Service Worker

Required for API mocking. Run this in the project root:

```bash
npx twd-js init public
```

This copies `mock-sw.js` to the `public/` directory. If the public directory has a different name (e.g., `static/`), use that path instead.

## Step 3: Configure Entry Point

TWD should only load in development mode. Choose the setup based on the framework:

### Bundled Setup (Recommended — all frameworks)

```typescript
// src/main.ts (or main.tsx)
if (import.meta.env.DEV) {
  const { initTWD } = await import('twd-js/bundled');
  const tests = import.meta.glob("./**/*.twd.test.ts");

  initTWD(tests, {
    open: true,
    position: 'left',
    serviceWorker: true,
    serviceWorkerUrl: '/mock-sw.js',
  });
}
```

**initTWD options:**
- `open` (boolean) — sidebar open by default. Default: `true`
- `position` (`"left"` | `"right"`) — sidebar position. Default: `"left"`
- `serviceWorker` (boolean) — enable API mocking. Default: `true`
- `serviceWorkerUrl` (string) — service worker path. Default: `'/mock-sw.js'`
- `theme` (object) — custom theme. See TWD theming docs.

### Standard Setup (React only — more control)

```tsx
// src/main.tsx
import { createRoot } from 'react-dom/client';

if (import.meta.env.DEV) {
  const testModules = import.meta.glob("./**/*.twd.test.ts");
  const { initTests, twd, TWDSidebar } = await import('twd-js');
  initTests(testModules, <TWDSidebar open={true} position="left" />, createRoot);
  twd.initRequestMocking().catch(console.error);
}
```

### Framework-Specific Notes

**Vue:**
```typescript
// src/main.ts
import { createApp } from 'vue';
import App from './App.vue';

if (import.meta.env.DEV) {
  const { initTWD } = await import('twd-js/bundled');
  const tests = import.meta.glob("./**/*.twd.test.ts");
  initTWD(tests, { open: true, position: 'left' });
}

createApp(App).mount('#app');
```

**Angular:**
```typescript
// src/main.ts
import { isDevMode } from '@angular/core';

if (isDevMode()) {
  const { initTWD } = await import('twd-js/bundled');
  // Angular may not support import.meta.glob — define tests manually:
  const tests = {
    './twd-tests/feature.twd.test.ts': () => import('./twd-tests/feature.twd.test'),
  };
  initTWD(tests, { open: true, position: 'left' });
}
```

**Solid.js:**
```tsx
// src/main.tsx
if (import.meta.env.DEV) {
  const { initTWD } = await import('twd-js/bundled');
  const tests = import.meta.glob("./**/*.twd.test.ts");
  initTWD(tests, { open: true, position: 'left' });
}
```

## Step 4: Add Vite HMR Plugin (Recommended)

Prevents test entries from duplicating during hot module replacement:

```typescript
// vite.config.ts
import { twdHmr } from 'twd-js/vite-plugin';

export default defineConfig({
  plugins: [
    // ... other plugins
    twdHmr(),
  ],
});
```

## Step 5: Write a First Test

Create a `src/twd-tests/` folder for all TWD tests. For larger projects, organize by domain (e.g., `src/twd-tests/auth/`, `src/twd-tests/dashboard/`).

```typescript
// src/twd-tests/app.twd.test.ts
import { twd, screenDom } from "twd-js";
import { describe, it } from "twd-js/runner";

describe("App", () => {
  it("should render the main heading", async () => {
    await twd.visit("/");
    const heading = screenDom.getByRole("heading", { level: 1 });
    twd.should(heading, "be.visible");
  });
});
```

**Folder structure example:**
```
src/twd-tests/
  app.twd.test.ts          # General app tests
  auth/
    login.twd.test.ts      # Auth-related tests
    register.twd.test.ts
  dashboard/
    overview.twd.test.ts   # Dashboard domain tests
  mocks/
    users.ts               # Shared mock data
```

## Step 6: Run the App

```bash
npm run dev
```

The TWD sidebar should appear in the browser. Click it to view and run tests.

## Optional: AI Remote Testing (twd-relay)

twd-relay enables AI agents to trigger in-browser test runs from the CLI. It is **optional** and only needed for AI-assisted workflows.

- **Localhost only**: twd-relay communicates via WebSocket on the local Vite dev server (`localhost`). It makes no external network connections.
- **Dev dependency**: Installed with `--save-dev` and guarded by `import.meta.env.DEV` — never included in production builds.

```bash
npm install --save-dev twd-relay
```

**Vite plugin setup (recommended):**

```typescript
// vite.config.ts
import { twdRemote } from 'twd-relay/vite';
import type { PluginOption } from 'vite';

export default defineConfig({
  plugins: [
    // ... other plugins
    twdRemote() as PluginOption,
  ],
});
```

**Connect browser client:**

```typescript
// Add inside your import.meta.env.DEV block, after initTWD:
import { createBrowserClient } from 'twd-relay/browser';
const client = createBrowserClient();
client.connect();
```

**Run tests from CLI:**

```bash
npx twd-relay run
```

## Step 7: Generate AI Coding Tool Configuration

After setup, generate a project instructions file so AI tools automatically write TWD tests when implementing features. This is critical for long-term adoption — without it, each new conversation starts without TWD context.

### Claude Code (`CLAUDE.md`)

Create a `CLAUDE.md` in the project root with TWD workflow instructions. Adapt the content based on the project's framework, structure, and existing configuration.

The file should include:

1. **Project overview** — framework, key dependencies, project description
2. **Commands** — how to run dev server, build, etc.
3. **Architecture** — routing, API layer, styling, key directories
4. **TWD testing section** covering:
   - Test file location and naming convention (`src/twd-tests/*.twd.test.ts`)
   - Key TWD imports:
     ```typescript
     import { twd, userEvent, screenDom, expect } from "twd-js";
     import { describe, it, beforeEach } from "twd-js/runner";
     ```
   - Test patterns: `twd.visit()`, `twd.mockRequest()`, `screenDom.*`, `userEvent.*`
   - Mock data location (`src/twd-tests/mocks/`)
5. **Development workflow rule** — instruct the AI to always write TWD tests when implementing new features

Example workflow section:
```markdown
## Development Workflow

When implementing a new feature:
1. Write the feature code (components, API layer, routes, navigation)
2. Write TWD tests in `src/twd-tests/` following existing test patterns
3. Add mock data in `src/twd-tests/mocks/` for API responses
4. Run and validate TWD tests pass before considering the task complete

TWD tests run in the browser during development — no separate test command needed.
```

### Other AI Coding Tools

The same workflow instructions can be adapted for other tools. The content is nearly identical — only the filename changes:

| Tool | File |
|------|------|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurfrules` |
| Cline | `.clinerules` |

When the developer specifies which tool they use, generate the appropriate file. If not specified, default to `CLAUDE.md`.

## Troubleshooting

### Tests Not Loading
- Verify `import.meta.env.DEV` is true (dev mode)
- Check file naming: must be `*.twd.test.ts` or `*.twd.test.tsx`
- Ensure the `initTWD`/`initTests` call is in the main entry file
- Check the glob pattern matches your test file locations

### Mock Service Worker Issues
- Run `npx twd-js init public` to install the service worker
- With standard setup: ensure `twd.initRequestMocking()` is called
- Check browser console for service worker registration errors

### Test Duplication on HMR
- Add `twdHmr()` plugin to Vite config

### Sidebar Not Appearing
- Confirm you're in development mode
- Check browser console for initialization errors
- Ensure the entry point code runs before the app renders
