---
name: suggest-tests
description: Recommend unit tests to add based on git diff changes. Analyzes modified code and prioritizes by risk level.
category: testing
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# Suggest Tests from Git Diff

Inspect the repository for code changes and recommend test additions or updates.

## Inputs
- diffScope: 'branch' or 'commit'
- referenceBranchOrCommit (optional): The reference branch or commit to compare from

## Procedure

### Phase 1 - Parse the Diff
1. Get all changes in this branch compared to the reference (default branch or specified commit)
2. Identify changed or added functions, methods, classes, constants, or modules
3. Ignore comment-only or formatting changes

### Phase 2 - Analyze the Changes
4. For each affected symbol:
   - Determine change type: added | modified | deleted | refactored
   - Detect whether the logic, signature, or control flow changed
   - Cross-reference coverage data if provided
5. Prioritize recommendations:
   - **HIGH**: New code or core logic changes with missing or low test coverage
   - **MEDIUM**: Modified parameters, return types, or conditionals
   - **LOW**: Trivial changes with existing adequate coverage
6. Flag risky changes (input validation, deserialization, external calls, etc.)

### Phase 3 - Output Recommendations

Return Markdown structured as follows:

```markdown
# Test Recommendations

## Risk Level High
**functionName**
- location: src/path/to/file.ts
- change type: modified
- reason: Description of why this needs tests
- suggested tests:
  - Test case description 1
  - Test case description 2

## Risk Level Medium
...

## Risk Level Low
...
```

## Constraints
- Analyze only within the given code. Do not invent missing context or external APIs
- Be deterministic and concise
- Return only recommendations

## Skill Chaining

### After Analysis

| Chain To | When | Action |
|----------|------|--------|
| unit-test-workflow | HIGH risk identified | Generate comprehensive tests |
| property-based-testing | Serialization patterns | Add PBT coverage |

### Chains From

| Source | Condition |
|--------|-----------|
| tdd | After REFACTOR phase |
| workflow-orchestrator | Code review context |

### Terminal Chain

After completion: **repo-hygiene** (clean analysis artifacts)

### Testing Pipeline Position

suggest-tests is step 2 in the testing pipeline:

```
tdd → suggest-tests → unit-test-workflow → property-based-testing → repo-hygiene
         ↑
     (you are here)
```