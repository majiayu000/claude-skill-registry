# App card configuration notes

Condensed from the [app cards reference](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/app-cards/reference). Prefer the live doc for the full field list and screenshots.

## Project layout (typical)

Under `src/app/cards/` (or the path your CLI generated):

- One **`*-hsmeta.json`** per card (schema + `config`).
- One **React entry** (`.jsx` / `.tsx`) per card, path referenced by `entrypoint`.
- A shared **`package.json`** for all cards in that directory.

Install dependencies with:

```bash
hs project install-deps
```

(from project root; see reference article for details).

## Minimal schema shape

```json
{
  "uid": "example-card",
  "type": "card",
  "config": {
    "name": "Hello Example App",
    "description": "A description of the card's purpose.",
    "location": "crm.record.tab",
    "entrypoint": "/app/cards/ExampleCard.jsx",
    "objectTypes": ["contacts"]
  }
}
```

## Required / notable `config` fields

| Field | Notes |
| --- | --- |
| `uid` | Stable ID; HubSpot uses it so you can rename display `name` without losing placement/state. |
| `type` | Must be `card`. |
| `config.name` | Card title in HubSpot. |
| `config.entrypoint` | Path to React file. |
| `config.location` | Single value: `crm.record.tab` \| `crm.record.sidebar` \| `crm.preview` \| `helpdesk.sidebar`. |
| `config.objectTypes` | Array of CRM object types the card targets (see table below). |
| `config.previewImage` | Optional: `{ "file": "...", "altText": "..." }` — png/jpeg/jpg/gif, max **5 MB**. |

## `objectTypes` and scopes (standard objects)

From the reference doc: standard object type strings are **case-insensitive**; singular and plural are accepted (e.g. `CONTACT` or `contacts`).

| CRM object | Example `objectType` | Scope to add |
| --- | --- | --- |
| Contacts | `CONTACT` | `crm.objects.contacts.read` |
| Companies | `COMPANY` | `crm.objects.companies.read` |
| Deals | `DEALS` | `crm.objects.deals.read` |
| Tickets | `TICKETS` | `tickets` |
| Orders | `ORDERS` | `crm.objects.orders.read` |
| Carts | `CARTS` | `crm.objects.carts.read` |
| Custom objects | `p_objectName` (**case sensitive**) or wildcard `p_*` | `crm.objects.custom.read` |
| App objects | `app_object_uid` | [App object scopes](https://developers.hubspot.com/docs/apps/developer-platform/add-features/app-objects/reference#scopes) |

### Data model builder objects

Additional types (appointments, courses, listings, services, projects) require activation in the [data model builder](https://knowledge.hubspot.com/data-management/use-the-data-model-builder); see the reference table for exact `objectTypes` values and scopes.

## Location-specific rules (high impact)

- **`crm.record.sidebar`**: **cannot** use [CRM data components](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/ui-components/crm-data-components/overview). Use standard components + hooks/actions instead.
- **`helpdesk.sidebar`**: App `scopes` must include **`tickets`** and card `objectTypes` must include **`tickets`**. User must [customize help desk sidebar](https://knowledge.hubspot.com/help-desk/customize-the-right-sidebar-of-help-desk) to surface the card.
- **`crm.record.tab`**: If the middle column was customized previously, users may need to [customize the record view](https://knowledge.hubspot.com/object-settings/customize-records) to show new extensions.

## Knowledge-base links (end-user setup)

- [Customize record previews](https://knowledge.hubspot.com/object-settings/customize-record-previews) — relevant to `crm.preview`.
