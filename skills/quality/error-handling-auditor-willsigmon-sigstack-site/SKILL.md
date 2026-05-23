---
name: Error Handling Auditor
description: Find and fix unsafe error handling in Leavn - try! force unwraps, empty catch blocks, silent try? failures
allowed-tools: Read, Edit, Grep
---

# Error Handling Auditor

Fix unsafe error handling:

1. **Find try! force unwraps**: Replace with do-catch + fallback
2. **Find empty catch {}**: Add `AppLog.error("Context: \(error)")`
3. **Find silent try?**: Add logging for important failures

Patterns:
```swift
// Fix try!
do {
    result = try riskyOperation()
} catch {
    AppLog.error("Operation failed: \(error)")
    result = fallbackValue
}

// Fix empty catch
} catch {
    AppLog.error("Failed to save: \(error)", category: .persistence)
}
```

Use when: Crash risks, silent failures, debugging issues, error handling audit
