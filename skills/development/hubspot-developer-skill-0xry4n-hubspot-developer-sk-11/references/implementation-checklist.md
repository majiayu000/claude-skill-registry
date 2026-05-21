# Implementation checklist

## Before coding

- Confirm whether the target is app card, app page, settings page, serverless function, OAuth/API configuration, or migration.
- Confirm platform version from existing project configuration or latest docs (affects serverless and other features — see `references/serverless-and-enterprise.md`).
- Confirm required CRM object types and **`location`** (sidebar cards **cannot** use CRM data components — see `references/app-cards-metadata.md`).
- Confirm required scopes and whether any Sensitive Data scopes are involved (if yes, **`hubspot.fetch()`** and **serverless functions** are disallowed for app cards per current docs).
- Confirm Marketplace distribution requirements and the [feature matrix](https://developers.hubspot.com/docs/apps/developer-platform/overview) for your auth model.
- Confirm local developer account and test account setup.
- If using external HTTP: confirm **`hubspot.fetch()`** payload/timeout/concurrency budgets (`references/ui-extensions-runtime.md`).

## Code review checklist

- Uses modern developer platform project structure.
- Uses generated CLI structure or accurately mirrors current docs.
- Uses `*-hsmeta.json` for extension registration.
- Uses `hubspot.extend()` in the extension entrypoint.
- Uses React or TypeScript. Prefer TypeScript for new work.
- Uses `@hubspot/ui-extensions` components for UI.
- Uses CRM hooks/components for CRM data where available.
- Uses `hubspot.fetch()` only for external requests (not native `fetch`; ESLint should catch this — `references/testing-and-linting.md`).
- Handles loading, empty, error, and permission states.
- Handles missing external configuration gracefully.
- Keeps scopes minimal.
- Does not use unsupported browser APIs or DOM patterns in UI extensions (sandboxed web worker).
- Keeps payloads and response sizes within limits.
- Avoids sensitive data leakage to external services.
- If app objects or other gated features appear: confirms HubSpot **access / approval** and correct distribution model (`references/marketplace-and-gated-features.md`).
- Serverless **`app-function`** metadata: **`uid`** unique; **`config.endpoint`** present when HTTP exposure is required; **`methods`** array schema satisfied (`references/serverless-app-function-hsmeta.md`).

## Testing checklist

Run available commands from the project. Common checks:

```bash
npm install
hs project install-deps
npm run lint
npm run typecheck
npm test
hs project validate
hs project dev
hs project upload
```

For **`app-function`** `*-hsmeta.json` files, run **`hs project validate`** before upload; fix **`config.endpoint`** and use **`endpoint.methods`** (array), not a singular **`method`**, when the validator requires it (`references/serverless-app-function-hsmeta.md`).

Where UI extension unit tests exist, prefer **`createRenderer`** from `@hubspot/ui-extensions/testing` with the correct extension point string (`references/testing-and-linting.md`).

Only run commands that exist in the project or are supported by the installed CLI. When a command is missing, state that it was unavailable and what was checked instead.

## Debugging checklist

- Read local dev console output.
- Read HubSpot extension logs panel during local development.
- Check deployed extension render logs.
- Check fetch logs for external request failures.
- Verify app installation in the target test account.
- Verify extension placement and object type configuration.
- Verify Super Admin or layout customization permissions when cards are not visible.

## Final response checklist for coding agents

Report:

- What extension type was built or changed.
- Files changed.
- Commands run and results.
- Scopes or permissions required.
- Manual testing steps inside HubSpot.
- Known limitations or docs assumptions.

