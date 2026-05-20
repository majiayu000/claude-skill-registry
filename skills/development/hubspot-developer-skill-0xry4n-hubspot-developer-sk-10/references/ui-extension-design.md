# UI extension design guidance

## Runtime expectations

UI extensions run in HubSpot’s **sandboxed web worker** environment, not a full browser tab. That implies no DOM manipulation, no native `fetch`, and no `localStorage` inside extension code; HubSpot provides **`hubspot.fetch()`**, components, hooks, **`logger`**, and ESLint rules to keep code compatible (`references/testing-and-linting.md`, `references/ui-extensions-runtime.md`).

## Choose the right extension point

Use an app card when users need contextual information or actions beside a CRM record, preview, help desk ticket, or supported workspace object.

Use an app home page when users need a dashboard, workflow hub, analytics view, onboarding surface, or full-screen cross-object experience.

Use a settings page when users need to configure API keys, OAuth connections, feature toggles, property mappings, routing rules, sync settings, or integration preferences.

Do not force complex workflows into a small CRM card. Use cards for quick context and actions, then open overlays or link into app pages for larger flows when supported.

## UI principles

- Start with the user's HubSpot job, not the external system's data model.
- Keep record cards short, contextual, and action-oriented.
- Use progressive disclosure for secondary details.
- Prefer native HubSpot UI extension components over custom layout tricks.
- Show loading, empty, error, and permission states.
- Make actions reversible or confirm destructive operations.
- Clearly explain missing setup, missing scopes, failed external services, and unsupported objects.
- Avoid duplicating fields HubSpot already shows unless the extension adds useful interpretation or cross-system context.

## Data loading pattern

Use CRM hooks and CRM components for HubSpot CRM data when possible. Use `hubspot.fetch()` for external systems.

Before using `hubspot.fetch()`:

1. Confirm the external URL is permitted by configuration.
2. Confirm request signing or validation requirements.
3. Keep request and response payloads small.
4. Design for timeout and retry behavior.
5. Avoid custom headers other than supported authorization behavior.
6. Avoid sending sensitive CRM data unless explicitly necessary and allowed.

## Sensitive data rule

Apps using Sensitive Data scopes can include app cards, but current docs restrict use of `hubspot.fetch()` and serverless functions in that context. Treat this as a hard design constraint unless official docs checked during the current task say otherwise.

## Good card structure

A strong app card usually has:

- A concise title matching the user's workflow.
- A summary/status row.
- One primary action.
- One to three secondary details.
- A details area only when needed.
- Clear error and setup prompts.

## Poor card patterns

Avoid:

- Raw JSON dumps.
- Large tables inside narrow sidebar cards.
- Hidden failures with no user message.
- External brand UI that clashes with HubSpot components.
- Multiple unrelated workflows in one card.
- Fetching data that the current record context does not need.

