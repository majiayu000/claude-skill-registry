---
name: riverpod-select
description: Reduce rebuilds with ref.watch(provider.select(...)); select a subset of state so widgets rebuild only when that part changes. Use when optimizing performance or when a widget uses only one field of a large object. Use this skill when the user asks about select, reducing rebuilds, or optimizing Riverpod watch.
---

# Riverpod — Reducing rebuilds with select

## Instructions

By default, **ref.watch(provider)** rebuilds whenever the provider's value changes (by reference/equality). If you only use a subset of the state (e.g. one field of a User), the widget still rebuilds when other fields change.

Use **select** to watch only a part of the state. Rebuilds happen only when the **selected** value changes (by ==).

### Syntax

```dart
// Rebuild only when firstName changes
String name = ref.watch(provider.select((it) => it.firstName));
return Text('Hello $name');
```

You can call select multiple times for different properties. The selected value should be **immutable**; mutating a returned List/object in place will not trigger a rebuild.

### Async providers: selectAsync

For async providers you often use **ref.watch(provider.future)**. To select on the resolved data instead of the whole AsyncValue, use **selectAsync** (when available): it applies a select on the data and returns a Future. See the Riverpod docs for the exact API in your version.

### When to use

- Only when the "other" properties change often and you have measured that rebuilds are a bottleneck. Select adds a small cost and extra complexity. Prefer normal watch unless you need the optimization.
