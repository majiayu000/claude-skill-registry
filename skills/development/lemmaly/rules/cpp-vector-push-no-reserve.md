---
id: cpp-vector-push-no-reserve
title: vector push_back in loop without reserve() — log-amortized reallocation
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: cpp
tags: cpp, info, complexity-cuts
---

# vector push_back in loop without reserve() — log-amortized reallocation

`std::vector::push_back` past the current capacity doubles the backing array and copies/moves every element. Calling `reserve(n)` first does one allocation.

## Fix

Call `v.reserve(n)` before the loop when n is known.

## Incorrect

```cpp
std::vector<int> v;
for (int i = 0; i < n; ++i) {
  v.push_back(compute(i)); // reallocates log(n) times
}
```

## Correct

```cpp
std::vector<int> v;
v.reserve(n);
for (int i = 0; i < n; ++i) {
  v.push_back(compute(i));
}
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
