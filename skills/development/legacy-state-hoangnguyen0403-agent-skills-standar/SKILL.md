---
name: Android Legacy State
description: Standards for State integration with Views using Coroutines and Lifecycle
metadata:
  labels: [android, state, views, lifecycle]
  triggers:
    files: ['**/*Fragment.kt', '**/*Activity.kt']
    keywords: ['repeatOnLifecycle', 'launchWhenStarted']
---

# Android Legacy State Standards

## **Priority: P1**

## Implementation Guidelines

### Flow Consumption

- **Rule**: ALWAYS use `repeatOnLifecycle(Lifecycle.State.STARTED)` to collect flows in Views.
- **Why**: Prevents crashes (collecting while view is destroyed) and saves resources (stops collecting in background).

### LiveData vs Flow

- **New Code**: Use `StateFlow` exclusively.
- **Legacy**: If using LiveData, observe with `viewLifecycleOwner` (Fragment), NOT `this`.

## Anti-Patterns

- **launchWhenX**: `**Deprecated**: Use repeatOnLifecycle.`
- **observe(this)**: `**Leak Risk**: Use viewLifecycleOwner in Fragments.`

## References

- [Flow Consumption Template](references/implementation.md)
