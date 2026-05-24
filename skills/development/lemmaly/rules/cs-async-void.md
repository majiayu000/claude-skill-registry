---
id: cs-async-void
title: async void — exceptions are unobserved and crash the process
severity: error
impact: CRITICAL
impactDescription: Will break or scale-fail in production
language: csharp
tags: csharp, error, invariant-guard
---

# async void — exceptions are unobserved and crash the process

`async void` cannot be awaited. Exceptions raised inside are unobserved and crash the process — they bypass `try/catch` at the call site. The only legitimate use is true event handlers (e.g. `OnClick`).

## Fix

Return Task. async void is only acceptable for true event handlers (OnClick, etc.).

## Incorrect

```csharp
public async void DoWork() {
  await Task.Delay(100);
  throw new Exception("boom"); // crashes the process
}
```

## Correct

```csharp
public async Task DoWork() {
  await Task.Delay(100);
  throw new Exception("boom"); // caller can await + catch
}

// Event handlers stay async void with a try/catch at the boundary:
private async void OnClick(object s, EventArgs e) {
  try { await DoWorkAsync(); }
  catch (Exception ex) { _log.LogError(ex, "OnClick failed"); }
}
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
