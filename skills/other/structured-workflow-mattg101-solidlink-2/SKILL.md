---
name: structured-workflow
description: Canonical workflow for clarifying requirements, executing work, and verifying correctness.
trigger: always_on
---

## Canonical Workflow

### 1. Clarify
- Identify objective, scope, and definition of done
- Detect underspecification early
- Ask the minimum number of blocking questions

### 2. Decide
- Choose an approach explicitly
- State assumptions and constraints
- Record tradeoffs where relevant

### 3. Execute
- Implement only what is in scope
- Follow project conventions
- Avoid speculative extensions

### 4. Verify
- Check against acceptance criteria
- Ensure no debug artifacts remain
- Confirm outputs are review-ready

### 5. Sync
- Update local state
- Prepare artifacts for downstream consumers (PRs, docs, tests)

This workflow is mandatory unless a skill explicitly overrides it.

