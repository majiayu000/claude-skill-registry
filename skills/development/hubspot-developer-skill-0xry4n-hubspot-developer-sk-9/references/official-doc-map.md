# HubSpot developer documentation map

Use this as a **navigation index**. Always confirm behavior on the linked page before shipping; paths and product rules change.

## Discovery

- [Documentation index (`llms.txt`)](https://developers.hubspot.com/docs/llms.txt) — HubSpot’s suggested machine-readable index (may require a normal browser session).

## Developer platform core

- [Developer platform overview](https://developers.hubspot.com/docs/apps/developer-platform/overview) — projects, legacy coexistence, feature × auth × distribution matrix.
- [Create an app](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/create-an-app)
- [App configuration (`app-hsmeta.json`)](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/app-configuration)
- [Migrate an app (hub)](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/migrate-an-app/overview)
- [Migrate to latest platform version](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/migrate-an-app/migrate-to-the-latest-platform-version)

## Tooling

- [Install the HubSpot CLI](https://developers.hubspot.com/docs/developer-tooling/local-development/hubspot-cli/install-the-cli)
- [Build with config profiles](https://developers.hubspot.com/docs/developer-tooling/local-development/build-with-config-profiles) — `context.variables` in UI extensions.
- [Quickstart](https://developers.hubspot.com/docs/getting-started/quickstart)
- [Account types (incl. developer test accounts)](https://developers.hubspot.com/docs/getting-started/account-types)

## UI extensions (all extension points)

- [UI extensions overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/overview) — anatomy, `hubspot.fetch()` limits, locations table, testing/linting pointers.
- [UI extensions SDK](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-extensions-sdk) — `hubspot.extend`, `context`, `actions`, hooks, overlays, logging.
- [Fetching data for UI extensions](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/fetching-data) — permitted URLs, signing, local dev proxying.
- [Logging and monitoring](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/logging-and-monitoring) — local logs panel, deployed Monitoring → UI Extensions.
- [UI components overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/overview)
- [Manage UI extension layout](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/manage-ui-extension-layout)
- [Figma design kit](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/figma-design-kit)
- [CRM data components](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/crm-data-components/overview)
- [CRM action components](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/crm-action-components/overview)

### Extension points

- [App cards overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/app-cards/overview) — includes Sensitive Data restrictions section.
- [App cards reference](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/app-cards/reference) — schema, `objectTypes`, scopes, locations.
- [Create an app card](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/app-cards/create-an-app-card)
- [App pages / create app pages](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/app-pages/create-app-pages)
- [Create an app home page](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/create-an-app-home-page)
- [Create a settings page](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/create-a-settings-page)

### Quality and tests

- [Testing UI extensions](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/tools/testing/overview) — `createRenderer`, `@hubspot/ui-extensions/testing`.
- [Linting for UI extensions](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/tools/linting/overview) — `@hubspot/eslint-config-ui-extensions`, ESLint 9.
- [Lint migration (v0.x)](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/tools/linting/migrate)

### Examples

- [UI extensions examples (GitHub)](https://github.com/HubSpot/ui-extensions-examples) — includes [legacy CRM card → UI extension converter](https://github.com/HubSpot/ui-extensions-examples/tree/main/legacy-card-converter).

## Serverless (app projects)

- [Serverless functions overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/serverless-functions/overview)
- [Create serverless functions](https://developers.hubspot.com/docs/apps/developer-platform/add-features/serverless-functions/create-serverless-functions)
- [Serverless function reference](https://developers.hubspot.com/docs/apps/developer-platform/add-features/serverless-functions/reference)
- [Configurable test accounts](https://developers.hubspot.com/docs/apps/developer-platform/add-features/serverless-functions/developer-tooling/local-development/configurable-test-accounts)

CLI: use **`hs project validate`** before **`hs project upload`** when `*-hsmeta.json` schema errors appear. For **`config.endpoint`** / **`methods`** array vs `method`, see bundled **`references/serverless-app-function-hsmeta.md`**.

## Other add-ons (verify against distribution/auth)

- [Agent tools overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/agent-tools/overview)
- [Custom workflow actions](https://developers.hubspot.com/docs/apps/developer-platform/add-features/custom-workflow-actions)
- [App events overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/app-events/overview)
- [App objects overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/app-objects/overview)
- [App objects reference](https://developers.hubspot.com/docs/apps/developer-platform/add-features/app-objects/reference)
- [Add telemetry](https://developers.hubspot.com/docs/apps/developer-platform/add-features/add-telemetry)
- [SCIM](https://developers.hubspot.com/docs/apps/developer-platform/add-features/scim)

## APIs and webhooks

- [CRM API overview / latest](https://developers.hubspot.com/docs/api-reference/latest/overview)
- [Sensitive data (properties API context)](https://developers.hubspot.com/docs/api-reference/latest/crm/properties/sensitive-data)
- [Webhooks v3 guide](https://developers.hubspot.com/docs/api-reference/webhooks-webhooks-v3/guide)
- [Webhooks v4 journal](https://developers.hubspot.com/docs/api-reference/webhooks-webhooks-v4/webhooks-journal)

## CRM concepts

- [Understanding the CRM (object type IDs)](https://developers.hubspot.com/docs/guides/crm/understanding-the-crm)

## Legacy apps

- [Private apps](https://developers.hubspot.com/docs/apps/legacy-apps/private-apps/overview)
- [Public apps](https://developers.hubspot.com/docs/apps/legacy-apps/public-apps/overview)

## CMS (distinct from app UI serverless)

- [Serverless functions for CMS](https://developers.hubspot.com/docs/cms/start-building/features/serverless-functions/getting-started-with-serverless-functions)
