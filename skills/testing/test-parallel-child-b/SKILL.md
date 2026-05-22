---
name: test-parallel-child-b
description: Child B for parallel test - writes timestamp
context: fork
allowed-tools:
  - Write
---

# Parallel Test Child B

Write "CHILD-B: {current timestamp}" to `earnings-analysis/test-outputs/parallel-child-b.txt`

Then wait 2 seconds (count to 2 slowly in your response) and confirm completion.
