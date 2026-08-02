---
name: ground-latest
description: 'Ground every version, stack, and best-practice choice in what is current today, read from the release channel rather than from recall. Use when starting a new codebase or service, scaffolding a project, migrating or refactoring an existing one, picking a language edition, runtime, framework, or dependency, or when the user asks for the latest, current, LTS, or modern way.'
---

# Ground Latest

Training data ages. Every version, stack, and practice this change pins gets read from the release channel today, not recalled.

This skill decides **what to pin**. `source-driven` decides how to use what is already pinned; `deps-upgrade` runs an upgrade campaign over dependencies already chosen.

## Do this

1. List every choice this change pins: language edition, runtime, each framework and dependency, build and test tooling, and the platform baseline. That list is the grounding set.
2. Look each one up at its own release channel today: the project release page, changelog, or registry metadata. For support windows and LTS tracks, query `https://endoflife.date/api/v1/products/<product>/`. Recall is not a source.
3. Record per entry: current stable, current LTS if the project runs an LTS track, release date, and end-of-support date.
4. Pin the latest stable LTS where the project offers one, otherwise the latest stable. An existing repo pin or version floor wins over the pick; name which one applied.
5. Drop pre-release, deprecated, and unmaintained choices (no release or security fix in 12 months), and name the maintained replacement you pinned instead.
6. Read the chosen version's current recommended pattern before writing against it. Renamed APIs and replaced defaults are where recalled code breaks.
7. Leave the grounded set in the change (plan, ADR, or PR body) with versions, dates, and links, so the next reader sees when it was grounded.

## Verify

- [ ] Every pinned choice has a version read from its release channel today, with a link.
- [ ] LTS versus latest-stable was decided per project, and any repo floor that overrode the pick is named.
- [ ] No pre-release, deprecated, or unmaintained choice survived; each replacement is named.
- [ ] The grounded set is written into the change, dated.
