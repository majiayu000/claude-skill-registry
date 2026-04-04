---
name: shadow_coder
description: Build parallel architectures safely without breaking current behavior.
metadata:
  short-description: Shadow mode refactors
---

## Purpose
Enable strangler-fig migrations with safe parallel paths.

## Steps
1. Create a parallel path (e.g. `_next_gen/`).
2. Mirror interfaces and add adapters.
3. Validate with tests or benchmarks.
4. Propose a staged migration plan.
