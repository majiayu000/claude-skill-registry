---
name: test-model-field
description: Test if model: field in skill frontmatter works
context: fork
model: haiku
allowed-tools:
  - Write
---

# Test Model Field

**Goal**: Verify that `model: haiku` in frontmatter actually uses haiku model.

## Task

1. Report which model you are (check your system info if available)
2. Write a simple response to confirm you're running
3. Write results to: `earnings-analysis/test-outputs/model-field-result.txt`

Include:
- Your model name/ID if you can determine it
- Confirmation the skill executed
- Any observable differences (haiku is faster, less verbose than opus/sonnet)
