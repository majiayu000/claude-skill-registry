---
name: test-arguments
description: Test $ARGUMENTS substitution in skill content
context: fork
allowed-tools:
  - Write
---

# Arguments Substitution Test

**Goal**: Test if $ARGUMENTS gets replaced with passed arguments.

## Received Arguments

Raw: $ARGUMENTS

## Task

Write the following to `earnings-analysis/test-outputs/arguments-result.txt`:

```
TEST: $ARGUMENTS substitution
DATE: {current date}

ARGUMENTS RECEIVED: $ARGUMENTS

SUBSTITUTION WORKED: [YES if you see actual args above, NO if you see literal "$ARGUMENTS"]
```

If no arguments were passed, note that too.
