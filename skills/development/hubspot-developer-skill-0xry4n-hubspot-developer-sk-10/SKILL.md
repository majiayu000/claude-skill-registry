---
name: hubspot-developer-skill
description: HubSpot developer platform assistant for CRM APIs, UI extensions, serverless
  functions, webhooks, app metadata, testing, and Marketplace readiness.
---

# HubSpot Developer Skill

## Purpose

Use this skill to design, implement, or review [HubSpot developer platform](https://developers.hubspot.com/docs/apps/developer-platform/overview) apps and UI extensions. Prefer the **project-based developer platform** over legacy private/public apps unless the user only needs a simple REST token or explicitly maintains legacy code.

Platform apps are **file-defined**, **CLI-managed** projects: configuration, assets, and source live in the repo; `hs project dev` / `hs project upload` drive local and deployed behavior. UI extensions are **React or TypeScript** bundles registered by `*-hsmeta.json` and rendered inside HubSpot’s **sandboxed** runtime (web worker constraints; use HubSpot APIs and components, not the full browser surface) via `hubspot.extend()`.

## Official documentation (start here)

HubSpot’s docs move quickly. Prefer **current** pages over memory or old blog posts. For a wider link set grouped by topic, use `references/official-doc-map.md`.

| Topic | URL |
| --- | --- |
| Developer platform overview | https://developers.hubspot.com/docs/apps/developer-platform/overview |
| Create an app | https://developers.hubspot.com/docs/apps/developer-platform/build-apps/create-an-app |
| App configuration (`app-hsmeta.json`) | https://developers.hubspot.com/docs/apps/developer-platform/build-apps/app-configuration |
| Migrate an app | https://developers.hubspot.com/docs/apps/developer-platform/build-apps/migrate-an-app/overview |
| Migrate to latest platform version | https://developers.hubspot.com/docs/apps/developer-platform/build-apps/migrate-an-app/migrate-to-the-latest-platform-version |
| Quickstart | https://developers.hubspot.com/docs/getting-started/quickstart |
| HubSpot CLI | https://developers.hubspot.com/docs/developer-tooling/local-development/hubspot-cli/install-the-cli |
| Config profiles (`context.variables`) | https://developers.hubspot.com/docs/developer-tooling/local-development/build-with-config-profiles |
| **UI extensions overview** (fetch limits, locations, workflow) | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/overview |
| **UI extensions SDK** (context, actions, hooks, overlays) | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-extensions-sdk |
| Fetching data (permitted URLs, signing, proxy) | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/fetching-data |
| Logging and monitoring | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/logging-and-monitoring |
| Testing UI extensions | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/tools/testing/overview |
| Linting UI extensions | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/tools/linting/overview |
| **UI extension components (standard + CRM)** | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/overview |
| CRM data components | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/crm-data-components/overview |
| CRM action components | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/crm-action-components/overview |
| Manage UI extension layout | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/manage-ui-extension-layout |
| App cards overview | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/app-cards/overview |
| **App cards reference** (schema, scopes, locations) | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/app-cards/reference |
| App pages | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/app-pages/create-app-pages |
| App home page | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/create-an-app-home-page |
| Settings pages | https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/create-a-settings-page |
| Serverless functions | https://developers.hubspot.com/docs/apps/developer-platform/add-features/serverless-functions/overview |
| Serverless reference | https://developers.hubspot.com/docs/apps/developer-platform/add-features/serverless-functions/reference |
| Agent tools | https://developers.hubspot.com/docs/apps/developer-platform/add-features/agent-tools/overview |
| App objects reference | https://developers.hubspot.com/docs/apps/developer-platform/add-features/app-objects/reference |
| Webhooks v3 | https://developers.hubspot.com/docs/api-reference/webhooks-webhooks-v3/guide |
| Webhooks v4 | https://developers.hubspot.com/docs/api-reference/webhooks-webhooks-v4/webhooks-journal |
| REST APIs | https://developers.hubspot.com/docs/api-reference/latest/overview |
| Sensitive data (properties) | https://developers.hubspot.com/docs/api-reference/latest/crm/properties/sensitive-data |
| Legacy private apps | https://developers.hubspot.com/docs/apps/legacy-apps/private-apps/overview |
| Legacy public apps | https://developers.hubspot.com/docs/apps/legacy-apps/public-apps/overview |

**Documentation index:** HubSpot publishes a machine-oriented index at `https://developers.hubspot.com/docs/llms.txt` for discovering pages; if that endpoint is blocked or returns a login wall, use the table above, `references/official-doc-map.md`, and “See also” links in the docs.

**Examples repo:** https://github.com/HubSpot/ui-extensions-examples (includes [legacy card converter](https://github.com/HubSpot/ui-extensions-examples/tree/main/legacy-card-converter)).

## Distribution, authentication, and features

From the [developer platform overview](https://developers.hubspot.com/docs/apps/developer-platform/overview), **what you can ship depends on** [distribution](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/app-configuration#distribution) and [authentication](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/app-configuration#authentication) (static token vs OAuth; private vs Marketplace). Use the official docs for the live matrix; at a high level:

- **API calls**, **agent tools**, **app cards**, **app pages**, **app settings**, **custom workflow actions**, **telemetry**, and **webhooks v3** are broadly available across common private app setups; **webhooks v4**, **app events**, and **app objects** lean toward OAuth / Marketplace-style distribution in the documented matrix.
- **Serverless functions** and **SCIM** are documented with tighter pairing to static-token / private patterns in that matrix—verify before promising architecture.
- **Public functions for CMS** follow the CMS serverless path (see CMS docs), not the same shape as app project serverless functions.

When choosing features, read **app configuration** and the overview table together so you do not design OAuth-only features (e.g. certain webhook or app-object flows) for a static-token-only app.

## First decision (task routing)

1. **Only scripted API access** for internal automation: a [legacy private app](https://developers.hubspot.com/docs/apps/legacy-apps/private-apps/overview) token may suffice; still mention developer platform for anything that might grow UI or Marketplace.
2. **In-portal UI, cards, app home, settings, OAuth, Marketplace**: use a **developer platform** project.
3. **Context beside a record, ticket, preview, or supported sidebar**: **app card** (UI extension).
4. **Dashboard / multi-step / full-width app experience**: **app pages**.
5. **In-app configuration** (API keys, mapping, toggles): **settings page** UI extension.
6. **External HTTP from the extension**: `hubspot.fetch()` only with allowed URLs, size/time limits, and security docs understood first.

**Hard limits to internalize** (see [UI extensions overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/overview) and `references/ui-extensions-runtime.md`): default **15s** fetch timeout (up to **120s**), **1 MB** request/response bodies, **20** concurrent fetches per account, **no custom headers** except `Authorization`, **no native `fetch`** in extension code (lint enforces this).

## UI extension components (`@hubspot/ui-extensions`)

Follow the [UI extension components overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/overview).

### Package version

Install or upgrade the SDK in the **extension directory** that owns the card, settings, or page bundle (often under `src/app/cards`, `settings`, or `pages`—match your repo):

```bash
npm i @hubspot/ui-extensions@latest
```

### Two import surfaces

- **Standard components** (layout, forms, text, charts, modals, etc.): from `@hubspot/ui-extensions`. They do not fetch CRM data by themselves; you compose them with hooks, props, or `hubspot.fetch()`.
- **CRM data** and **CRM action** components: from `@hubspot/ui-extensions/crm`.

```tsx
import { Alert, Text, Flex, Button } from "@hubspot/ui-extensions";
import { CrmAssociationPivot, CrmActionLink } from "@hubspot/ui-extensions/crm";
```

### CRM-specific behavior

- **CRM data components** load from the **current CRM record** context. Official docs state they are restricted to the **middle column** of CRM records—do not plan sidebar-only layouts for them without verifying current placement rules.
- **CRM action components** (e.g. action button, link, card actions) expose the same underlying CRM actions through different UI shapes—pick by UX, not by capability difference.

For layout, use **Flex**, **Box**, **Inline**, **Spacer**, **AutoGrid**, etc., per [manage UI extension layout](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/manage-ui-extension-layout). Prefer HubSpot primitives over ad hoc HTML/CSS that fights the sandbox.

**Design reference:** [Figma design kit](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/figma-design-kit) (linked from the components overview).

## Core app workflow

1. Clarify **audience**, **account type**, and **Marketplace vs private**.
2. Read **platform version** from `app-hsmeta.json` / project docs (e.g. `2025.2`, `2026.03`—never assume from memory).
3. Scaffold with **HubSpot CLI** (`hs project create`, `hs project add`); treat generated layout as the default.
4. Keep **`app-hsmeta.json`** and each extension’s **`*-hsmeta.json`** as the source of truth for UIDs, types, `location`, `entrypoint`, `objectTypes`, and display metadata.
5. Implement UI in **React/TSX**; register with **`hubspot.extend()`** in the entrypoint.
6. Prefer **CRM hooks and CRM components** for HubSpot-hosted CRM data; use **`hubspot.fetch()`** only for allowed external URLs.
7. Develop with **`hs project dev`**; upload with **`hs project upload`** when validating deployed behavior.
8. Use **extension logs**, **render logs**, and **fetch logs** before calling work “done.”
9. For Marketplace, add a **review pass**: scopes, sensitive data, errors, install/uninstall, empty states, and security.

## Modern UI extension anatomy

- **`*-hsmeta.json`**: extension type, HubSpot **location**, display metadata, **objectTypes** (for CRM surfaces), **entrypoint** path.
- **Entrypoint**: `hubspot.extend(({ context, actions }) => …)` (see current samples for exact typing imports your project uses).
- **React tree**: standard + CRM components; loading / empty / error / permission states.
- **Optional** `hubspot.fetch()` to partner backends; optional **serverless functions** where docs allow for your auth model.

## App-function `*-hsmeta.json` (serverless) and `hs project upload`

`app-function` components use **`"type": "app-function"`** and **`config.entrypoint`** (see [serverless reference](https://developers.hubspot.com/docs/apps/developer-platform/add-features/serverless-functions/reference)). **`hs project validate`** / **`hs project upload`** may fail if HTTP-oriented functions omit **`config.endpoint`**.

**Common validation errors (real CLI output):**

- **`Missing required field: 'config.endpoint'`** — add an `endpoint` object under `config` for functions that receive inbound HTTP (for example OAuth callback routes).
- **`Missing required field: 'config.endpoint.methods'`** plus **`additionalProperty: method`** — the schema expects **`methods`** (array of verbs, e.g. `["GET"]`, `["POST"]`), not a singular **`method`** field. Remove `method` and use `methods` instead.

Always run **`hs project validate`** after editing function metadata; if the validator disagrees with an older doc example, follow the **validator** for your installed **`hs --version`**. Details and examples: `references/serverless-app-function-hsmeta.md`.

## File layout rules

CLI templates evolve. After `hs project add`, **mirror the generated paths** instead of inventing filenames. Commonly you will see extension code under paths such as `src/app/cards/` with a shared `package.json` per feature area; **confirm on disk** before advising moves or imports.

Do not conflate **legacy CRM cards** (iframe / external patterns) with **modern UI extension app cards**; migrations should be called out explicitly in plans and commits.

## Security and sensitive data

- Request the **smallest** scope set that satisfies the workflow.
- **Sensitive Data** scopes carry extra restrictions (e.g. interactions with `hubspot.fetch()` and serverless functions). Treat docs as law: if the app needs both sensitive CRM surfaces and external calls, you may need **product splits** or a **different flow**—validate in current HubSpot documentation before implementation.

## Required agent behavior

1. **Read the repo first**: `src/app/app-hsmeta.json`, extension metadata, `package.json`, lockfile, and CLI version.
2. **Classify** legacy vs developer platform and static vs OAuth.
3. **Smallest coherent change**; keep generated structure unless there is a documented reason to diverge.
4. **Verify APIs** against official pages (links in this file) when outputting config shapes, component names, or limits.
5. **Report** what was changed, commands run, scopes, manual HubSpot test steps, and doc assumptions.

## Bundled reference files

Use these for deeper patterns without duplicating them entirely in chat:

- `references/official-doc-map.md` — **curated doc index** by topic (platform, UI, serverless, APIs, legacy).
- `references/ui-extensions-runtime.md` — sandbox, **`hubspot.fetch()` limits**, `location` values, Sensitive Data, CRM data placement.
- `references/ui-extensions-sdk-primer.md` — **`context` / `actions`**, hooks vs props, overlays, iframe modal, clipboard, logging.
- `references/app-cards-metadata.md` — card **`*-hsmeta.json`** fields, **`objectTypes` + scopes**, sidebar vs CRM data components, help desk.
- `references/serverless-and-enterprise.md` — **2026.03** serverless, **Enterprise install**, dev test accounts, vs CMS serverless.
- `references/serverless-app-function-hsmeta.md` — **`config.endpoint`**, **`methods` vs `method`**, **`hs project validate`** / upload failures.
- `references/testing-and-linting.md` — **`createRenderer`**, `@hubspot/ui-extensions/testing`, **`@hubspot/eslint-config-ui-extensions`**, monitoring.
- `references/marketplace-and-gated-features.md` — matrix reminders, **app objects approval**, webhooks v3/v4, listing readiness.
- `references/hubspot-modern-platform.md` — platform concepts, CLI commands, migration outline.
- `references/ui-extension-design.md` — extension-point choice, UX, data loading, sensitive data.
- `references/implementation-checklist.md` — before coding, review, testing, debugging.
- `references/examples.md` — minimal shapes and **prompt recipes** for agents.
