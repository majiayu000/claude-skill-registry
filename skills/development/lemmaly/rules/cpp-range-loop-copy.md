---
id: cpp-range-loop-copy
title: Range-for `auto x` copies each element — use `const auto&` for non-trivial types
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: cpp
tags: cpp, info
---

# Range-for `auto x` copies each element — use `const auto&` for non-trivial types

`for (auto x : container)` copies each element into `x`. For non-trivial types (`std::string`, `std::vector<…>`, custom types) this is expensive. `const auto&` borrows, `auto&` mutates in place.

## Fix

Prefer `for (const auto& x : container)` unless you intentionally need a copy.

## Incorrect

```cpp
for (auto s : large_strings) {
  process(s); // s is a fresh copy each iteration
}
```

## Correct

```cpp
for (const auto& s : large_strings) {
  process(s); // reference, no copy
}
```
