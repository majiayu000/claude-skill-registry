---
name: riverpod-pull-to-refresh
description: Implement pull-to-refresh with Riverpod using RefreshIndicator and ref.refresh; show spinner on initial load, show previous data during refresh, AsyncValue pattern matching. Use when the user asks about pull-to-refresh, RefreshIndicator with Riverpod, or refreshing async providers.
---

# Riverpod — Pull-to-refresh

## Instructions

Riverpod fits pull-to-refresh well: refresh by invalidating the provider and let AsyncValue handle loading vs data vs error.

### 1. Provider and UI

Define an async provider (e.g. FutureProvider or AsyncNotifierProvider) that fetches data. Display it with **ref.watch(provider)** so you get an **AsyncValue**.

### 2. RefreshIndicator

Wrap your scrollable (ListView, SingleChildScrollView, etc.) in **RefreshIndicator**. In **onRefresh**, call **ref.refresh(provider.future)** so the indicator stays until the new data is loaded:

```dart
RefreshIndicator(
  onRefresh: () => ref.refresh(activityProvider.future),
  child: ListView(
    children: [
      // content
    ],
  ),
)
```

### 3. Loading and error states

Use **AsyncValue** pattern matching:

- **Initial load:** No data and no error → show full-screen spinner.
- **Refresh:** Show the refresh indicator and keep showing previous data (or previous error) until the new result arrives.
- **Data:** `AsyncValue(:final value?)` or similar to show the value.
- **Error:** `AsyncValue(:final error?)` to show the error.

Example (syntax may vary by Riverpod version):

```dart
final activity = ref.watch(activityProvider);
switch (activity) {
  AsyncValue<Activity>(:final value?) => Text(value.activity),
  AsyncValue(:final error?) => Text('Error: $error'),
  _ => const CircularProgressIndicator(),
}
```

Use **valueOrNull** (or equivalent) if your API exposes it for nullable data. See the docs for the exact AsyncValue API in your version.
