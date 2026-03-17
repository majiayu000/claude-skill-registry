---
name: algorithm-complexity
description: Consider time and space complexity when writing algorithms Use when optimizing code performance. Performance category skill.
metadata:
  category: Performance
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_algorithm_complexity
---

# Algorithm Complexity

Consider time and space complexity when writing algorithms. Avoid O(n²) operations inside loops (nested iterations over the same data). Use appropriate data structures: HashMaps for O(1) lookups, Sets for membership testing, sorted arrays with binary search for ordered data. Profile before optimizing—but recognize obviously inefficient patterns during code review.