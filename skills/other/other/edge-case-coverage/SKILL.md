---
name: edge-case-coverage
description: "Test boundary conditions: empty arrays, null/undefined, zero, negative numbers, maximum values Use when writing and organizing tests. Testing category skill."
metadata:
  category: Testing
  priority: high
  is-built-in: true
  session-guardian-id: builtin_edge_case_coverage
---

# Edge Case Coverage

Test boundary conditions: empty arrays, null/undefined, zero, negative numbers, maximum values. Test error cases: network failures, invalid input, missing data, timeout. Test concurrency issues if applicable. Consider: What if the list is empty? What if the user doesn't exist? What if the API is down? Edge cases often reveal bugs that happy-path testing misses.