---
name: plan2json
description: Convert feature requirements into structured end-to-end test cases as JSON.
argument-hint: <spec-file>
disable-model-invocation: true
allowed-tools: Read, Write
---

# Plan to JSON

You are creating the foundation for an autonomous development process. Your job is to convert a project specification into a comprehensive feature list that serves as the single source of truth for what needs to be built.

## Input

Read the file at `$1` to get the complete project specification. Read it carefully before proceeding.

## Output: feature_list.json

Based on the spec file, create `feature_list.json` with detailed end-to-end test cases.

### Format

```json
[
  {
    "category": "functional",
    "description": "Brief description of the feature and what this test verifies",
    "steps": [
      "Step 1: Navigate to relevant page",
      "Step 2: Perform action",
      "Step 3: Verify expected result"
    ],
    "passes": false
  },
  {
    "category": "style",
    "description": "Brief description of UI/UX requirement",
    "steps": [
      "Step 1: Navigate to page",
      "Step 2: Take screenshot",
      "Step 3: Verify visual requirements"
    ],
    "passes": false
  }
]
```

### Requirements

- **Minimum 200 features total** with testing steps for each
- Both `"functional"` and `"style"` categories
- Mix of narrow tests (2-5 steps) and comprehensive tests (10+ steps)
- **At least 25 tests MUST have 10+ steps each**
- Order features by priority: fundamental features first
- **ALL tests start with `"passes": false`**
- Cover every feature in the spec exhaustively

Write the JSON array to `feature_list.json` in the current working directory.
