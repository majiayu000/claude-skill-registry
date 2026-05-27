---
name: swift-code-review
description: Reviews Swift code for concurrency safety, error handling, memory management, and common mistakes. Use when reviewing .swift files for async/await patterns, actor isolation, Sendable conformance, or general Swift best practices.
---

# Swift Code Review

## Review Workflow

Follow this sequence **in order**. Do not emit findings until every **Pass** below is satisfied.

1. **Swift / toolchain baseline** — Establish language and tooling context: `Package.swift` `// swift-tools-version` and any per-target Swift language version or `swiftSettings` in the manifest; for Xcode, `SWIFT_VERSION` (or equivalent) in project or target build settings; note if review is single-file only.  
   **Pass:** You state a concrete Swift language version or mode (e.g. Swift 6 language mode, tools 5.10) *before* advice that depends on strict concurrency, migration-only syntax, or SDK availability.

2. **Read surrounding code** — For each changed `.swift` file, read the full enclosing type, function, method, or property that contains the edits, not only the diff hunk.  
   **Pass:** At least one full enclosing symbol (type or member) containing the change was read per changed file.

3. **Scope the checklist** — Using [Quick Reference](#quick-reference), decide which [Review Checklist](#review-checklist) rows and [references](#when-to-load-references) apply; open those reference files; skip rows clearly unrelated to the diff.  
   **Pass:** The review (or working notes) lists which checklist areas you applied, or marks areas N/A with a one-line reason tied to the diff (e.g. “no SwiftUI / @Observable in change”).

4. **Pre-report verification** — Load and follow [review-verification-protocol](../review-verification-protocol/SKILL.md).  
   **Pass:** That skill’s **Hard gates (sequenced)** are satisfied for each finding you will report (full symbol read, usage search before “unused”, caller checked before “missing handling”, severity calibrated, `[FILE:LINE]` proof).

## Hard gates (same sequence, shorter)

| Step | Objective pass condition |
| --- | --- |
| 1 | Swift version/mode (or explicit single-file limitation) recorded before version- or SDK-gated advice. |
| 2 | Full enclosing symbol read per changed file, not diff-only. |
| 3 | Checklist areas + references listed or N/A with diff-tied reason. |
| 4 | `review-verification-protocol` completed for every reported issue. |

## Output format

Report findings as:

```text
[FILE:LINE] ISSUE_TITLE
Severity: Critical | Major | Minor | Informational
Description of the issue and why it matters.
```

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| async/await, actors, Sendable, Task | [references/concurrency.md](references/concurrency.md) |
| @Observable, @ObservationIgnored, @Bindable | [references/observable.md](references/observable.md) |
| throws, Result, try?, typed throws | [references/error-handling.md](references/error-handling.md) |
| Force unwraps, retain cycles, naming | [references/common-mistakes.md](references/common-mistakes.md) |

## Review Checklist

- [ ] No force unwraps (`!`) on runtime data (network, user input, files)
- [ ] Closures stored as properties use `[weak self]`
- [ ] Delegate properties are `weak`
- [ ] Independent async operations use `async let` or `TaskGroup`
- [ ] Long-running Tasks check `Task.isCancelled`
- [ ] Actors have mutable state to protect (no stateless actors)
- [ ] Sendable types are truly thread-safe (beware `@unchecked`)
- [ ] Errors handled explicitly (no empty catch blocks)
- [ ] Custom errors conform to `LocalizedError` with descriptive messages
- [ ] Nested @Observable objects are also marked @Observable
- [ ] @Bindable used for two-way bindings to Observable objects

## When to Load References

- Reviewing async/await, actors, or TaskGroups → concurrency.md
- Reviewing @Observable or SwiftUI state → observable.md
- Reviewing error handling or throws → error-handling.md
- General Swift review → common-mistakes.md

## Review Questions

1. Are async operations that could run concurrently using `async let`?
2. Could actor state change across suspension points (reentrancy bug)?
3. Is `@unchecked Sendable` backed by actual synchronization?
4. Are errors logged and presented with helpful context?
5. Could any closure or delegate create a retain cycle?
