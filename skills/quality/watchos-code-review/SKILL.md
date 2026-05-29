---
name: watchos-code-review
description: Reviews watchOS code for app lifecycle, complications (ClockKit/WidgetKit), WatchConnectivity, and performance constraints. Use when reviewing code with import WatchKit, WKExtension, WKApplicationDelegate, WCSession, or watchOS-specific patterns.
---

# watchOS Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| App lifecycle, scenes, background modes, extended runtime | [references/lifecycle.md](references/lifecycle.md) |
| ClockKit, WidgetKit, timeline providers, Smart Stack | [references/complications.md](references/complications.md) |
| WCSession, message passing, file transfer, reachability | [references/connectivity.md](references/connectivity.md) |
| Memory limits, background refresh, battery optimization | [references/performance.md](references/performance.md) |

## Review Checklist

- [ ] SwiftUI App protocol used with `@WKApplicationDelegateAdaptor` for lifecycle events
- [ ] `scenePhase` read from root view (not sheets/modals where it's always `.active`)
- [ ] `WKExtendedRuntimeSession` started only while app is active (not from background)
- [ ] Workout sessions recovered in `applicationDidFinishLaunching` (not just delegate)
- [ ] Background tasks scheduled at least 5 minutes apart; next scheduled before completing current
- [ ] `URLSessionDownloadTask` (not `DataTask`) used for background network requests
- [ ] WidgetKit used instead of ClockKit for watchOS 9+ complications
- [ ] Timeline includes future entries (not just current state); gaps avoided
- [ ] `TimelineEntryRelevance` implemented for Smart Stack prioritization
- [ ] WCSession delegate set before `activate()`; singleton pattern used
- [ ] `isReachable` checked before `sendMessage`; `transferUserInfo` for critical data
- [ ] Received files moved synchronously before delegate callback returns

## When to Load References

- Reviewing app lifecycle, background modes, or extended sessions -> lifecycle.md
- Reviewing complications, widgets, or timeline providers -> complications.md
- Reviewing WCSession, iPhone-Watch communication -> connectivity.md
- Reviewing memory, battery, or performance issues -> performance.md

## Output Format

Report issues using: `[FILE:LINE] ISSUE_TITLE`

Examples:

- `[WatchApp.swift:18] WKExtendedRuntimeSession started while app not active`
- `[ConnectivityManager.swift:42] WCSession.activate() before delegate assignment`
- `[ComplicationTimeline.swift:67] Timeline has no future entries`

## Hard gates (before reporting)

Complete **in order** for each finding you intend to report. Do not advance until the pass condition is satisfied.

1. **Location artifact** — The finding includes `[FILE:LINE]` (or a line range) copied from the current file contents; the path resolves in this repo.
2. **Scope read** — You read the full surrounding unit: the `View` body, `WKApplicationDelegate` / scene method, `TimelineProvider` implementation, `WCSessionDelegate` callback, or workout/background task handler that owns the behavior—not only a diff hunk.
3. **watchOS or pairing claim** (only if the finding depends on background modes, complication/timeline contracts, `WCSession` reachability or transfer semantics, workout or extended runtime rules, or device-specific limits) — You name one concrete artifact you inspected (for example `Info.plist` / target capabilities for background modes, the `WK*` / `WCSession` call order in source, entitlements, or a subsection you read in the matching doc from [Quick Reference](#quick-reference)) **or** you downgrade the item to an open question in [Review Questions](#review-questions).
4. **Protocol** — Pre-report steps in [review-verification-protocol](../review-verification-protocol/SKILL.md) are satisfied for this item (no finding if they are not).

Use the issue format `[FILE:LINE] ISSUE_TITLE` for each reported finding. Hard gate 4 is the full pre-report checklist for this skill’s review type.

## Review Questions

1. Is the app using modern SwiftUI lifecycle with delegate adaptor?
2. Are background tasks completing properly (calling `setTaskCompletedWithSnapshot`)?
3. Is UI update frequency reduced when `isLuminanceReduced` is true?
4. Are WatchConnectivity delegate callbacks dispatching to main thread?
5. Is `TabView` nested within another `TabView`? (Memory leak on watchOS)
