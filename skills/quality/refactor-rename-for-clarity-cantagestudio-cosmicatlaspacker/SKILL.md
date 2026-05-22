---
name: refactor-rename-for-clarity
description: "[Code Quality] Performs systematic renaming to improve code clarity: variables, functions, classes, files. Use when names are unclear, misleading, or inconsistent with their purpose."
---

# Refactor: Rename for Clarity

Improve code readability through better naming.

## Naming Principles

### 1. Names Should Reveal Intent
```swift
// BAD: let d: Int
// GOOD: let elapsedDays: Int
```

### 2. Names Should Be Searchable
```swift
// BAD: if status == 1 { }
// GOOD: if status == .active { }
```

### 3. Names Should Match Abstraction Level
```swift
// BAD: func getFromNetworkAndParseJSON()
// GOOD: func fetchUserProfile()
```

## Common Patterns

| Bad Name | Better Name | Why |
|----------|-------------|-----|
| data | userResponse | Specific type |
| temp | previousValue | Purpose clear |
| flag | isEnabled | Boolean pattern |
| doIt() | submitForm() | Action + target |