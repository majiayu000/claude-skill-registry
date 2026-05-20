# UI extensions runtime (sandbox, fetch, locations)

Summarized from the [UI extensions overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/overview) and related pages. Re-read the official docs when limits or locations change.

## Runtime model

1. HubSpot loads the extension in a **secure, sandboxed** environment (see also [linting overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/tools/linting/overview): extensions run in a **sandboxed web worker** — no DOM, no `window`/`document` patterns, no native `fetch` in extension code; use `hubspot.fetch()` and HubSpot components).
2. **`hubspot.extend()`** registers the extension and receives **`context`** and **`actions`** (see [UI extensions SDK](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-extensions-sdk)).
3. **CRM data** via SDK **hooks** (e.g. `useCrmProperties`, `useAssociations`) or CRM components; **external** data via **`hubspot.fetch()`** with app-configured permitted URLs (see [fetching data](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/fetching-data)).

## `hubspot.fetch()` limits (documented)

From the UI extensions overview:

| Constraint | Value |
| --- | --- |
| Default timeout | **15 seconds** |
| Maximum timeout | **120 seconds** (2 minutes) via the `timeout` option |
| Request payload | **1 MB** |
| Response payload | **1 MB** |
| Concurrency | Up to **20** concurrent `hubspot.fetch()` requests **per account** |
| Headers | **No custom** request/response headers except **`Authorization`** |

Design retries, backoff, and small JSON payloads accordingly.

## Sensitive Data scopes

Apps using [Sensitive Data scopes](https://developers.hubspot.com/docs/api-reference/latest/crm/properties/sensitive-data) **may include app cards** but **cannot** use `hubspot.fetch()` or serverless functions in that configuration. See [app cards overview — Sensitive Data](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/app-cards/overview#sensitive-data-scopes).

## Supported `location` values (card / extension config)

| Location value | Where it appears |
| --- | --- |
| `crm.record.tab` | Middle column of CRM record pages (tabs / custom tabs). With `objectTypes` including companies, also **sales workspace target accounts preview**. |
| `crm.record.sidebar` | Right sidebar on CRM records. With deals, also **sales workspace deals sidebar**. **CRM data components are not allowed** in the sidebar. |
| `crm.preview` | CRM **preview** panel (records, index, board, lists), for the `objectTypes` you configure. |
| `helpdesk.sidebar` | Help desk ticket sidebars and ticket preview. Requires **`tickets`** in app scopes and **`tickets`** in the card `objectTypes`. |
| `home` | [App home page](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/create-an-app-home-page). |
| `settings` | [App settings page](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/create-a-settings-page). |

Object coverage, scope pairing, and layout quirks (e.g. middle-column customization) are detailed in the [app cards reference](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/app-cards/reference#supported-locations).

## CRM data components placement

CRM data components load from the **current CRM record** and, per the [UI components overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/overview), are intended for the **middle column** of CRM records. Do not plan sidebar-only experiences that rely on them.

## Legacy CRM cards

HubSpot publishes a **[Legacy CRM Card to UI Extension Converter](https://github.com/HubSpot/ui-extensions-examples/tree/main/legacy-card-converter)** example for parity-style migrations.

## Property update listener caveat

`onCrmPropertiesUpdate` reflects changes made **from the HubSpot UI**, not all API-driven updates — design polling or refetch strategies if external systems change properties without UI interaction ([SDK](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-extensions-sdk)).
