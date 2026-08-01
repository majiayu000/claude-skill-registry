---
name: i18n-curator
description: 'Curate CRM Orbit UI i18n strings and mappings. Use when adding or editing
  user-facing copy, auditing en.json, or keeping i18n/events.ts and i18n/enums.ts
  in sync with new keys. Scope: CRMOrbit/i18n/en'
---

---
name: i18n-curator
description: Curate CRM Orbit UI i18n strings and mappings. Use when adding or editing user-facing copy, auditing en.json, or keeping i18n/events.ts and i18n/enums.ts in sync with new keys. Scope: CRMOrbit/i18n/en.json and mapping files.
---

# I18n Curator

## Overview

Maintain consistent, stable translation keys and UI copy while keeping backend
data locale-neutral.

## Workflow

1) Identify needed keys
- Ensure UI uses `t("key")` and remove hard-coded strings.
- Prefer stable, semantic keys (no UI text in keys).

2) Update `en.json`
- Keep casing consistent (Title Case for labels, sentence case for messages).
- Avoid abbreviations that hurt translation.
- Keep placeholders consistent (`{name}`, `{count}`).

3) Update mapping files
- If adding enums/status/type/event keys, update:
  - `CRMOrbit/i18n/enums.ts`
  - `CRMOrbit/i18n/events.ts`

4) Validate
- Scan for missing keys and dead keys.
- Confirm no translated strings are persisted in domain state or events.

## Guardrails

- Keys are stable once released.
- No translated strings in Automerge, events, reducers, persistence.
- If other locales must be updated, ask before editing.
- Per the coding guidelines, files in **/views/**/*.{ts,tsx} must be "read-only projections that subscribe to Automerge changes — never mutate domain state, apply business logic, emit events, or localize strings directly."
