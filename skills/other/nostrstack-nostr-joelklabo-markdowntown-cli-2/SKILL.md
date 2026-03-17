---
name: nostrstack-nostr
description: "Nostr-specific workflows in nostrstack: identifier parsing, event/profile landing pages, relay fetch/caching rules, NIP-05 identity resolution, and reference rendering. Use when working on Nostr event handling, NIP-05 lookups, or /nostr/:id UI/API behavior."
---

# Nostr workflows

Use this skill for Nostr identifiers, events, and reference resolution.

## Workflow

- Read `references/ids-and-api.md` for identifier and API contract rules.
- Read `references/references.md` for tag/mention resolution behavior.
- Consult `references/identity-resolution.md` for NIP-05 flows.

## Guardrails

- Accept `nostr:`-prefixed identifiers and multiple bech32 types.
- Enforce relay caps, timeouts, and cache TTLs from config.
- Keep all rendered content safe and link references to `/nostr/<id>`.
