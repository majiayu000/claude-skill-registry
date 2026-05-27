---
name: debug-log-patterns
description: Language-specific debug logging patterns and best practices. Reference when adding instrumentation for Dart/Flutter, Kotlin/Android, Swift/iOS, or JavaScript/TypeScript applications.
---

# Debug Log Patterns

## Overview

This skill provides copy-paste-ready logging patterns for common debugging scenarios across multiple languages. Use these patterns when instrumenting code during PDCA debug cycles.

## Supported Languages

| Language | File | Primary Use Case |
|----------|------|------------------|
| Dart/Flutter | `references/dart-flutter.md` | Flutter mobile/web apps |
| Kotlin/Android | `references/kotlin-android.md` | Native Android apps |
| Swift/iOS | `references/swift-ios.md` | Native iOS apps |
| JavaScript/TypeScript | `references/javascript-typescript.md` | Web apps, Node.js, React Native |

## Universal Conventions

### Log Format Standard

All logs should follow this format for consistency:
```
[ClassName] methodName: description key=value
```

### Log Levels

| Level | When to Use |
|-------|-------------|
| DEBUG/TRACE | Detailed flow tracing, variable values |
| INFO | Significant events, state transitions |
| WARN | Unexpected but recoverable situations |
| ERROR | Failures that affect functionality |

### Common Patterns (All Languages)

#### Pattern: Method Entry/Exit
```
[ClassName] methodName: ENTER params=(param1, param2)
[ClassName] methodName: EXIT result=value
```

#### Pattern: Conditional Branch
```
[ClassName] methodName: condition branch=TAKEN/SKIPPED reason=why
```

#### Pattern: Loop Iteration
```
[ClassName] methodName: loop iteration=N/total item=current
```

#### Pattern: State Transition
```
[ClassName] methodName: state from=oldState to=newState trigger=event
```

#### Pattern: Async Operation
```
[ClassName] operationName: START
[ClassName] operationName: SUCCESS result=summary
[ClassName] operationName: ERROR error=message
```

## Quick Selection Guide

**Debugging Flutter/Dart app?**
-> See `references/dart-flutter.md`

**Debugging Android native (Kotlin)?**
-> See `references/kotlin-android.md`

**Debugging iOS native (Swift)?**
-> See `references/swift-ios.md`

**Debugging web/Node.js/React?**
-> See `references/javascript-typescript.md`

## Best Practices

1. **Be specific** - Include actual values, not just "value changed"
2. **Be consistent** - Use the same format throughout the codebase
3. **Be temporary** - Remove debug logs after issue is resolved
4. **Be contextual** - Include enough info to understand without seeing code
5. **Be careful with sensitive data** - Never log passwords, tokens, PII

## References

- `references/dart-flutter.md` - Dart/Flutter logging patterns
- `references/kotlin-android.md` - Kotlin/Android logging patterns
- `references/swift-ios.md` - Swift/iOS logging patterns
- `references/javascript-typescript.md` - JavaScript/TypeScript logging patterns
