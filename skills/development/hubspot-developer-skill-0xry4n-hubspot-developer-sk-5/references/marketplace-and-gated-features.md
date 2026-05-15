# Marketplace, app objects, and gated capabilities

## Developer platform feature matrix

The authoritative **feature × authentication × distribution** matrix lives on the [developer platform overview](https://developers.hubspot.com/docs/apps/developer-platform/overview) and in [app configuration](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/app-configuration). Always reconcile Marketplace listing requirements with that matrix before architecture sign-off.

## App objects (gated + OAuth-heavy)

- [App objects reference](https://developers.hubspot.com/docs/apps/developer-platform/add-features/app-objects/reference) — `app-objects/` and `app-object-associations/` directories, `*-hsmeta.json` definitions, property schema, settings blocks (`hasRecordPage`, `allowsUserCreatedRecords`, `hasEngagements`, etc.).
- **Access requires HubSpot approval** — the reference doc directs partners to submit HubSpot’s **[in-app access request form](https://app.hubspot.com/l/developer-overview/appObjectsEventsRequest)** (also linked from the overview). Do not promise app-object timelines without customer/partner program alignment.

### App cards on app objects

The app cards reference documents **`objectTypes`** values for standard CRM objects, custom objects (`p_*`), and **app objects** via **`app_object_uid`**, with scopes cross-linked to the app objects reference.

## App events

See [app events overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/app-events/overview). Distribution and approval constraints follow HubSpot’s current program rules (verify on page).

## Agent tools

See [agent tools overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/agent-tools/overview). Feature availability interacts with the same distribution/auth matrix as the rest of the platform.

## Webhooks v3 vs v4

- [Webhooks v3](https://developers.hubspot.com/docs/api-reference/webhooks-webhooks-v3/guide) — widely available in matrix combinations.
- [Webhooks v4](https://developers.hubspot.com/docs/api-reference/webhooks-webhooks-v4/webhooks-journal) — check matrix: not available for static-token private in the published overview table.

## Marketplace technical review

When preparing a listing, combine:

- [App configuration](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/app-configuration) — scopes, auth URLs, distribution.
- UI extension UX: loading, empty, error, uninstall/reinstall, sensitive data paths.
- Security review of `hubspot.fetch()` targets, serverless endpoints (if any), and OAuth token handling.
