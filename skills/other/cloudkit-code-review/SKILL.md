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
