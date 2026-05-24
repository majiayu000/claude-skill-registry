---
id: java-bare-catch-exception
title: catch (Exception) with empty body or log-only — swallows root cause
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: java
tags: java, warning, invariant-guard
---

# catch (Exception) with empty body or log-only — swallows root cause

`catch (Exception e)` with an empty body or just `printStackTrace()` swallows the root cause. The bug lives on, the stack trace evaporates, the production incident has no breadcrumbs.

## Fix

Catch the narrowest exception, rethrow as a domain exception, or handle with a documented fallback. Never swallow silently.

## Incorrect

```java
try {
  riskyCall();
} catch (Exception e) {
  e.printStackTrace(); // swallowed; caller thinks everything is fine
}
```

## Correct

```java
try {
  riskyCall();
} catch (IOException e) {
  // narrow exception, rethrow as domain error with cause preserved
  throw new ReadFailedException("riskyCall failed for " + ctx, e);
}
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
