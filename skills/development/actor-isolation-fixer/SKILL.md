---
name: Actor Isolation Fixer
description: Fix Swift 6 actor isolation errors in Leavn app - deinit accessing @MainActor properties, nonisolated contexts, concurrent access violations
allowed-tools: Read, Edit, Grep
---

# Actor Isolation Fixer

## Instructions

Fix actor isolation errors systematically:

1. **Error: "main actor-isolated property X cannot be accessed from nonisolated"**
   - **In deinit**: Mark property as `nonisolated(unsafe) private var`
   - **In closure**: Add `@MainActor` to Task or use `await MainActor.run { }`
   - **In method**: Mark method `@MainActor` or `nonisolated`

2. **Common Leavn patterns**:
   ```swift
   // Timer in @MainActor class deinit
   nonisolated(unsafe) private var timer: Timer?

   deinit {
       timer?.invalidate() // Safe - Timer.invalidate() is thread-safe
   }

   // Task property in @MainActor class
   nonisolated(unsafe) private var task: Task<Void, Never>?

   deinit {
       task?.cancel() // Safe - Task.cancel() is thread-safe
   }
   ```

3. **Don't use nonisolated(unsafe) for**:
   - UI properties (views, layers)
   - Mutable state accessed across threads
   - Non-thread-safe types

4. **Safe to use nonisolated(unsafe) for**:
   - Timers (invalidate is thread-safe)
   - Tasks (cancel is thread-safe)
   - Notification observers (removeObserver is thread-safe)

Use this skill when: Actor isolation errors, deinit cannot access properties, concurrent access violations
