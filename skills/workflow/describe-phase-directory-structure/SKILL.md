---
name: describe-phase-directory-structure
description: Phase directory layout, naming conventions, and required files. Load when creating or navigating phase directories.
user-invocable: false
---

## Phase Directory Structure
```
.ushabti/phases/NNNN-short-slug/
├── phase.md        # Intent, scope, acceptance criteria
├── steps.md        # Ordered implementation steps
├── progress.yaml   # Machine-tracked state
└── review.md       # Review findings
```

**Naming**: Phase IDs are zero-padded and sequential (0001, 0002, ...). Slugs are short, lowercase, hyphenated, and descriptive.

Example: `0003-http-client-retry`