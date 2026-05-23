---
name: test-error-child
description: Child skill that deliberately fails - for error propagation test
context: fork
allowed-tools:
  - Write
  - Bash
---

# Error Test Child

**Goal**: Deliberately fail to test error propagation.

## Task

1. Write "STARTING" to `earnings-analysis/test-outputs/error-child-start.txt`
2. Then FAIL by trying to read a non-existent file: `/nonexistent/path/that/does/not/exist.txt`
3. This should cause an error that propagates to parent

The parent skill will check what error message it receives.
