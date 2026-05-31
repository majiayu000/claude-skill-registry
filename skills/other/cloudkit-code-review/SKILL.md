---
name: cloudkit-code-review
description: Reviews CloudKit code for container setup, record handling, subscriptions, and sharing patterns. Use when reviewing code with import CloudKit, CKContainer, CKRecord, CKShare, or CKSubscription.
---

# CloudKit Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| CKContainer, databases, zones, entitlements | [references/container-setup.md](references/container-setup.md) |
| CKRecord, references, assets, batch operations | [references/records.md](references/records.md) |
| CKSubscription, push notifications, silent sync | [references/subscriptions.md](references/subscriptions.md) |
| CKShare, participants, permissions, acceptance | [references/sharing.md](references/sharing.md) |

## Review Checklist

- [ ] Account status checked before private/shared database operations
- [ ] Custom zones used (not default zone) for production data
- [ ] All CloudKit errors handled with `retryAfterSeconds` respected
- [ ] `serverRecordChanged` conflicts handled with proper merge logic
- [ ] `CKErrorPartialFailure` parsed for individual record errors
- [ ] Batch operations used (`CKModifyRecordsOperation`) not individual saves
- [ ] Large binary data stored as `CKAsset` (records have 1MB limit)
- [ ] Record keys type-safe (enums) not string literals
- [ ] UI updates dispatched to main thread from callbacks
- [ ] `CKAccountChangedNotification` observed for account switches
- [ ] Subscriptions have unique IDs to prevent duplicates
- [ ] CKShare uses custom zone (sharing requires custom zones)

## When to Load References

- Reviewing container/database setup or zones -> container-setup.md
- Reviewing record CRUD or relationships -> records.md
- Reviewing push notifications or sync triggers -> subscriptions.md
- Reviewing sharing or collaboration features -> sharing.md

## Output Format

Report issues using: `[FILE:LINE] ISSUE_TITLE`

Examples:
- `[AppDelegate.swift:24] CKContainer not in custom zone`
- `[SyncManager.swift:156] Unhandled CKErrorPartialFailure`
- `[DataStore.swift:89] Missing retryAfterSeconds backoff`

## Review Questions

1. What happens when the user is signed out of iCloud?
2. Does error handling respect rate limiting (`retryAfterSeconds`)?
3. Are conflicts resolved or does data get overwritten silently?
4. Is the schema deployed to production before App Store release?
5. Are shared records in custom zones (required for CKShare)?

## Hard gates (before reporting)

Complete **in order** for each finding you intend to report. Do not advance until the pass condition is satisfied.

1. **Location artifact** — The finding includes `[FILE:LINE]` (or a line range) copied from the current file contents; the path resolves in this repo.
2. **Scope read** — You read the full surrounding unit: the type or function that owns the CloudKit work (for example the `CKOperation` subclass usage, completion handler chain, or `CKRecord` lifecycle), not only a diff hunk or isolated snippet.
3. **CloudKit or deployment claim** (only if the finding depends on container identifiers, public vs private database choice, custom zone requirement, iCloud account state, entitlements, or production schema) — You name one concrete artifact you inspected (for example `com.apple.developer.icloud-container-environment` or container ID in the entitlements file, `CKContainer.default()` vs custom identifier in source, `Info.plist` / target capability, or evidence that schema is deployed) **or** you downgrade the item to an open question in [Review Questions](#review-questions).
4. **Protocol** — Pre-report steps in [review-verification-protocol](../review-verification-protocol/SKILL.md) are satisfied for this item (no finding if they are not).

Use the issue format `[FILE:LINE] ISSUE_TITLE` for each reported finding. Hard gate 4 is the full pre-report checklist for this skill’s review type.
