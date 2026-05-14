# UI extensions SDK primer

Summarized from the [UI extensions SDK](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-extensions-sdk). Use the official page for exhaustive signatures and examples.

## Registration

- Call **`hubspot.extend()`** in the extension file (not a default export pattern for the root extension). Subcomponents can be normal React components imported into that file.
- Signature: `hubspot.extend(({ context, actions }) => <Extension ... />)` — omit `context` / `actions` if unused.

## Context (`context`)

High-signal fields (universal):

| Area | Fields |
| --- | --- |
| Placement | `location`: `crm.record.tab` \| `crm.record.sidebar` \| `crm.preview` \| `helpdesk.sidebar` \| `settings` \| `home` |
| Portal | `portal.id`, `portal.timezone`, `portal.dataHostingLocation` (`na1`, `eu1`, …) |
| User | `user.id`, `user.email`, `user.emails`, names, `user.locale`, `user.language` (BCP 47 UI language), `user.teams`, `user.permissions` |
| Config | `variables` — [config profile](https://developers.hubspot.com/docs/developer-tooling/local-development/build-with-config-profiles) variables |

**CRM extension points only** (`crm.record.tab`, `crm.record.sidebar`, `crm.preview`, `helpdesk.sidebar`): `crm.objectId`, `crm.objectTypeId`, `extension.appId`, `extension.appName`, `extension.cardTitle`.

## Actions (`actions`)

**Universal** (all extension points): `addAlert`, `reloadPage`, `copyTextToClipboard`, `closeOverlay`, `openIframeModal`.

**CRM extension points only**: `fetchCrmObjectProperties`, `refreshObjectProperties`, `onCrmPropertiesUpdate`.

Prefer **`useCrmProperties`** over one-off `fetchCrmObjectProperties` when you want automatic updates and formatting (per SDK guidance).

## Hooks

Import from **`@hubspot/ui-extensions`** or **`@hubspot/ui-extensions/crm`** as documented per hook. Commonly cited:

- **`useCrmProperties`** — properties on the current CRM record; supports formatting and refetch.
- **`useAssociations`** — associated records with pagination and formatting options.

There are also hooks for **`useExtensionContext`** and **`useExtensionActions`** to avoid prop drilling.

## Overlays

From SDK behavior documentation:

- Only **one `Modal`** open at a time per extension; opening another closes the first.
- A **`Modal` may open from a `Panel`**, but a **`Panel` cannot open from a `Modal`**.

## `openIframeModal`

Payload includes required `uri`, `height`, `width`, optional `title`, `flush`. Parent page can listen for completion via `window.top.postMessage` with JSON **`{"action":"DONE"}`** or **`{"action":"CANCEL"}`**; the **origin must match** the iframe `uri` domain.

## Clipboard

`copyTextToClipboard` requires **user gesture** (transient activation); do not invoke from `useEffect` on mount.

## Logging

Use the SDK **`logger`** for extension-appropriate logging; the sandbox discourages `console` in production lint rules — see [linting overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/tools/linting/overview) and [logging and monitoring](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/logging-and-monitoring).

## File uploads

No dedicated upload component. Options described in the SDK include **file-type CRM properties** with [CrmPropertyList](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/crm-data-components/crm-property-list), or an **iframe modal** hosting an upload page.

## `hubspot` import

Examples in current docs sometimes use `import { hubspot } from "@hubspot/ui-extensions"` separately from component imports. Match the pattern used in your CLI template and package version.
