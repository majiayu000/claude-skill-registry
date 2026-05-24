---
id: cpp-raw-new
title: Raw `new` outside of smart-pointer ctor — manual delete, exception-unsafe
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: cpp
tags: cpp, warning, invariant-guard
---

# Raw `new` outside of smart-pointer ctor — manual delete, exception-unsafe

Raw `new` requires a matching `delete` on every exit path. If an exception fires between `new` and `delete`, the memory leaks. Smart pointers (`unique_ptr`, `shared_ptr`) destruct automatically.

## Fix

Use `std::make_unique<T>(...)` or `std::make_shared<T>(...)`. Reserve raw `new` for placement-new or interop with C APIs.

## Incorrect

```cpp
Widget* w = new Widget(42);
configure(w);   // if this throws, w leaks
delete w;
```

## Correct

```cpp
auto w = std::make_unique<Widget>(42);
configure(w.get()); // destructs on every exit path, including throw
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
