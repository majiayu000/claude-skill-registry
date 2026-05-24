---
id: cs-disposable-no-using
title: IDisposable allocated without using — leak on exception
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: csharp
tags: csharp, warning
---

# IDisposable allocated without using — leak on exception

`IDisposable` resources allocated without `using` leak if an exception fires before `Dispose()`. `using var` ensures cleanup even on throw.

## Fix

Wrap in `using var x = new ...;` or `using (var x = ...) { }`.

## Incorrect

```csharp
var stream = new FileStream(path, FileMode.Open);
var data = ReadAll(stream); // if this throws, stream is never disposed
stream.Dispose();
```

## Correct

```csharp
using var stream = new FileStream(path, FileMode.Open);
var data = ReadAll(stream); // disposed on every exit path
```
