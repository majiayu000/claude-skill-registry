---
name: describe-progress-file
description: Structure and field ownership for progress.yaml. Load when reading or updating phase progress state.
user-invocable: false
---

## progress.yaml

Machine-readable state of the Phase. Structure:

```yaml
phase:
  id: NNNN
  slug: short-slug
  title: Title
  status: planned|building|review|complete

steps:
  - id: S001
    title: Short title
    implemented: false
    reviewed: false
    notes: ""
    touched: []
```

**Status transitions**:
- `planned` → `building` (when Builder starts)
- `building` → `review` (when all steps implemented)
- `review` → `building` (if Overseer requests fixes)
- `review` → `complete` (when Overseer approves)

**Field ownership**:
- `implemented`: Set by Builder when step is done
- `reviewed`: Set only by Overseer
- `notes`: Updated by whoever completes the step
- `touched`: List of files meaningfully modified