---
name: plan
description: Use when the user wants to plan a feature, design an implementation approach, or break down a complex task before coding.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Plan
argument-hint: "[feature or task description]"
---

Create an implementation plan for: **$ARGUMENTS**

## Steps

1. **Understand the requirement** — break down what needs to be built

2. **Explore the codebase** — find related code, patterns, and conventions

3. **Identify all changes needed:**
   - New files to create
   - Existing files to modify
   - Tests to add
   - Config changes

4. **Map dependencies** — what must be done before what

5. **Output structured plan:**

```
## Implementation Plan: [feature]

### Overview
[1-2 sentence description of what will be built]

### Tasks

#### Phase 1: [Foundation]
- [ ] Task 1: [description]
  - Files: [file1, file2]
  - Pattern: follow [existing-file] as reference
- [ ] Task 2: [description]
  - Files: [file1]
  - Depends on: Task 1

#### Phase 2: [Core Logic]
- [ ] Task 3: [description]
  - Files: [file1, file2, file3]
  - Depends on: Task 1, Task 2

#### Phase 3: [Testing & Polish]
- [ ] Task 4: Write tests
  - Files: [test files]
  - Depends on: Phase 2
- [ ] Task 5: Update docs
  - Files: [CLAUDE.md, README]

### Files Map
| File | Action | Purpose |
|------|--------|---------|
| [path] | Create/Modify | [what changes] |

### Reference Code
- [existing-file] → follow this pattern for [X]
- [existing-file] → follow this pattern for [Y]

### Risks
- [potential issues and mitigations]

### Estimated Scope
- [X] files to create
- [Y] files to modify
- [Z] tests to add
```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
