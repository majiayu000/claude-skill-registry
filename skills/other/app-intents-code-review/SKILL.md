---
name: app-intents-code-review
description: Reviews App Intents code for intent structure, entities, shortcuts, and parameters. Use when reviewing code with import AppIntents, @AppIntent, AppEntity, AppShortcutsProvider, or @Parameter.
---

# App Intents Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| AppIntent protocol, perform(), return types | [references/intent-structure.md](references/intent-structure.md) |
| AppEntity, EntityQuery, identifiers | [references/entities.md](references/entities.md) |
| AppShortcutsProvider, phrases, discovery | [references/shortcuts.md](references/shortcuts.md) |
| @Parameter, validation, dynamic options | [references/parameters.md](references/parameters.md) |

## Review Checklist

- [ ] `perform()` marked with `@MainActor` if accessing UI/main thread resources
- [ ] `perform()` completes within 30-second timeout (no heavy downloads/processing)
- [ ] Custom errors conform to `CustomLocalizedStringResourceConvertible`
- [ ] `EntityQuery.entities(for:)` handles missing identifiers gracefully
- [ ] `EntityStringQuery` used if Siri voice input needed (not plain `EntityQuery`)
- [ ] `suggestedEntities()` returns reasonable defaults for disambiguation
- [ ] `AppShortcut` phrases include `.applicationName` parameter
- [ ] Non-optional `@Parameter` has sensible defaults or uses `requestValue()`
- [ ] `@IntentParameterDependency` not used on iOS 16 targets (crashes)
- [ ] Phrases localized in `AppShortcuts.strings`, not `Localizable.strings`
- [ ] App Intents defined in app bundle, not Swift Package (pre-iOS 17)
- [ ] `isDiscoverable = false` for internal/widget-only intents

## When to Load References

- AppIntent protocol implementation -> intent-structure.md
- Entity queries, identifiers, Spotlight -> entities.md
- App Shortcuts, phrases, discovery -> shortcuts.md
- Parameter validation, dynamic options -> parameters.md

## Review Questions

1. Does `perform()` handle timeout limits for long-running operations?
2. Are entity queries self-contained (no `@Dependency` injection in Siri context)?
3. Do phrases read naturally and include the app name?
4. Are SwiftData models passed by `persistentModelID`, not directly?
5. Would migrating from SiriKit break existing user shortcuts?

## Hard gates (before reporting)

Complete **in order** for each finding you intend to report. Do not advance until the pass condition is satisfied.

1. **Location artifact** — The finding includes `[FILE:LINE]` (or a line range) copied from the current file contents; the path resolves in this repo.
2. **Scope read** — You read the full surrounding type: the `AppIntent` / `AppEntity` / `EntityQuery` / `AppShortcutsProvider` (or equivalent) that contains the flagged code, not only a diff hunk or snippet.
3. **Platform or integration claim** (only if the finding depends on minimum iOS, Swift Package vs app target, `@IntentParameterDependency` availability, SiriKit migration, or `isDiscoverable` / extension placement) — You name one concrete artifact you inspected (for example `IPHONEOS_DEPLOYMENT_TARGET` or target membership in the Xcode project, `Package.swift` `platforms`, entitlements, or where the intent file lives) **or** you drop or downgrade the finding to an open question.
4. **Protocol** — Pre-report steps in [review-verification-protocol](../review-verification-protocol/SKILL.md) are satisfied for this item (no finding if they are not).

Use the issue format `[FILE:LINE] ISSUE_TITLE` for each reported finding. Hard gate 4 is the full pre-report checklist for this skill’s review type.
