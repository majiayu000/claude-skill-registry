---
id: cpp-string-concat-in-loop
title: std::string += inside loop — O(n^2) without reserve()
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: cpp
tags: cpp, warning, complexity-cuts
---

# std::string += inside loop — O(n^2) without reserve()

`std::string::operator+=` past capacity reallocates. Without a `reserve`, repeated concatenation is O(n²). `std::ostringstream` or one `reserve` fixes it.

## Fix

Call `s.reserve(total)` once if size known, or accumulate into a `std::ostringstream` and call `.str()` at the end.

## Incorrect

```cpp
std::string s;
for (const auto& part : parts) {
  s += part;
}
```

## Correct

```cpp
std::ostringstream os;
for (const auto& part : parts) {
  os << part;
}
auto s = os.str();

// Or, if size known:
std::string s;
s.reserve(total_size);
for (const auto& part : parts) s += part;
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
