---
name: update_kit
description: Update this documentation kit safely from upstream.
---

## Purpose
Keep the automation kit aligned with upstream changes using merge protocol.

## Steps
1. Read `.agent-docs/memory/KIT_VERSION.md` to capture current version.
2. Compare to upstream release or commit.
3. If updates exist, apply `non_destructive_bootstrap` to refresh templates.
4. Run `skills_auditor` and `skills_sync` for skill alignment.
5. Refresh `.agent-docs/memory/INDEX.md` and `INDEX.json`.
6. Record actions and evidence in the Action Log.
7. Update `KIT_VERSION.md` with the new version details.
8. Use the update kit checklist for completeness.

## Guardrails
- Never overwrite user-owned content; use merge protocol markers.
- Preserve fixed agents and local overrides.
