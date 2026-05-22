---
name: refactoring
description: Refactor code to improve maintainability by consolidating redundant logic and applying DRY principles
---

# Refactoring

冗長なロジックや重複している箇所を集約したりすることで保守性を上げる。

## Stragegy

- Check whether the logic can be erased by consolidating into Schema
- Test first. Before starting implementation, check the current tests for the target method cover the all pattern.

## Points of view

The following rules are listed by the order of priorities.

- Is the code in the right place from a DDD perspective?
- Is it possible to remove the logic by changing the schema itself?
- Isn't it against DRY?
- Is it possible to write code with better visibility by cutting it out into a separate method?
- Can loop be improved more? (O(n) > O(n^2) > O(2^n) > O(n!))
