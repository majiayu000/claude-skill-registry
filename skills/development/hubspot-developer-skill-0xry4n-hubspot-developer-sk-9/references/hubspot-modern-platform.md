# HubSpot modern developer platform notes

## Platform model

Modern HubSpot apps are created, configured, and deployed as projects. The project contains app configuration, assets, source code, UI extension definitions, and deployable app features. The HubSpot CLI is the normal creation and deployment path.

Use the project model for apps that need UI inside HubSpot, Marketplace readiness, OAuth-style app distribution, app settings, app home pages, or structured extension deployment.

Legacy private apps and public apps still exist and may be appropriate for simple API-token usage or maintenance work, but do not default to legacy patterns for new HubSpot-hosted app experiences.

## Current concepts to preserve

- Developer platform apps are file-based and CLI-managed.
- UI extensions are React-based and run in a HubSpot sandbox.
- Extension placement is defined by `location` in `*-hsmeta.json`.
- App cards can appear on CRM records, preview panels, help desk surfaces, and selected workspace sidebars depending on current supported locations.
- App pages provide app-owned full-page experiences, including home and additional routed pages.
- Settings pages provide HubSpot-hosted configuration UI.
- `@hubspot/ui-extensions` provides base UI components.
- CRM packages provide data and action components for CRM-specific extension use.
- `hubspot.extend()` registers extension entrypoints.
- `hubspot.fetch()` is for external service requests and is limited by timeout, payload, concurrency, header, and security rules (numeric limits summarized in `references/ui-extensions-runtime.md`).
- [Config profiles](https://developers.hubspot.com/docs/developer-tooling/local-development/build-with-config-profiles) expose variables to extensions as `context.variables`.

## Common commands

Do not assume exact command flags without checking the latest docs or project CLI help. Common commands include:

```bash
hs init
hs auth
hs project create
hs project add
hs project dev
hs project upload
hs project install-deps
```

`hs project install-deps` installs dependencies for subfolders that contain their own `package.json` (for example `src/app/cards/`). See the [app cards reference](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensions/extension-points/app-cards/reference).

For an existing project, inspect available scripts and run CLI help when uncertain:

```bash
hs project --help
hs project add --help
cat package.json
find src/app -maxdepth 3 -type f
```

## Platform version handling

The modern docs reference platform versions such as `2025.2` and `2026.03`. Do not hard-code version-specific assumptions into reusable code unless the project already declares that version. Read the app/project configuration first.

## Migration notes

When migrating a legacy app or card:

1. Identify legacy card data source, auth model, action endpoints, and object placements.
2. Map the old card to a modern UI extension app card when the UI belongs on records or preview panels.
3. Replace iframe or legacy external-render assumptions with HubSpot UI extension components where possible.
4. Replace arbitrary browser APIs with APIs allowed by the UI extensions sandbox.
5. Move configuration into `*-hsmeta.json` files.
6. Recheck scopes and Marketplace requirements.

