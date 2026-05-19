# Testing and linting UI extensions

## Testing ([overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/tools/testing/overview))

- HubSpot recommends **Vitest** (other runners possible).
- Entry: **`createRenderer()`** from **`@hubspot/ui-extensions/testing`**, passing an **extension point location** so mocks match `context`, `actions`, and serverless-related mocks for that surface.

Valid locations for the renderer (from docs):

- `'crm.record.tab'`
- `'crm.record.sidebar'`
- `'crm.preview'`
- `'helpdesk.sidebar'`
- `'settings'`
- `'home'`

- **Create a new renderer per test** for isolation.
- Prefer **`findByTestId`** (with HubSpot components’ `testId` prop) over brittle text matchers.
- Familiar helpers: `render`, `find`, `findByTestId`, plus async/wait utilities documented on the same page.

## Linting ([overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/tools/linting/overview))

Extensions run in a **sandboxed web worker** — restricted browser APIs.

- Install **ESLint 9+** and **`@hubspot/eslint-config-ui-extensions`**.
- Flat config example in docs: `import { config } from '@hubspot/eslint-config-ui-extensions'` → `export default [ ...config ]`.
- For `"type": "module"` projects, use `"lint": "eslint ."` in `package.json`.

### Rules you should expect the shared config to enforce (names from docs)

Examples include: **no native browser dialogs**, **no browser storage** in extension code, **no `console`** (use SDK logger), **no DOM access**, **no unsupported HTML elements**, **no invalid extension-point imports**, **no invalid image src**, **no native `fetch` / XHR** (use `hubspot.fetch()`), **no parent imports** outside extension root, **restricted globals**.

For production-grade setups, the doc’s “full config” combines `@eslint/js`, `typescript-eslint`, React, React Hooks, Prettier compatibility, and unused-imports — copy from the official page rather than improvising.

### Upgrading lint major versions

If migrating from **v0.x** of the HubSpot ESLint config, follow the dedicated [migrate](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/tools/linting/migrate) article.

## Local development

- **`hs project dev`** — hot reload against HubSpot.
- **Extension logs panel** — errors, warnings, invalid prop values; optional disable via host browser `localStorage` keys documented in [logging and monitoring](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/logging-and-monitoring) (those keys apply to the HubSpot shell, not in-extension `localStorage` APIs).

## Deployed monitoring

**Development → Monitoring → Logs → UI Extensions** tab: Extension Render, `hubspot.fetch()`, Extension Log (custom logger output), with detail and trace flows.
