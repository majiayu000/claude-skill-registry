---
name: test-parallel-child-a
description: Child A for parallel test - writes timestamp
context: fork
allowed-tools:
  - Write
---

# Parallel Test Child A

Write "CHILD-A: {current timestamp}" to `earnings-analysis/test-outputs/parallel-child-a.txt`

Then wait 2 seconds (count to 2 slowly in your response) and confirm completion.
