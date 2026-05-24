---
name: pr-fix
description: Fix issues identified in PR reviews, addressing blocking and minor concerns. Use after receiving PR review feedback or when PR has requested changes.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
user-invocable: true
---

# PR Fix

## Purpose

Fix issues identified in PR reviews, addressing both blocking and minor concerns systematically.

## When to Use

- After receiving PR review feedback
- When PR has requested changes
- To address review comments before merge

## Task-Specific Rules

Based on files changed in the PR, load appropriate rules **before fixing**:

| Files Changed                          | Rules to Load                                                                                                              |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `packages/react/src/components/`       | [components.md](../../rules/components.md), [testing.md](../../rules/testing.md), [storybook.md](../../rules/storybook.md) |
| `packages/react/src/hooks/`            | [testing.md](../../rules/testing.md)                                                                                       |
| `packages/core/`, `packages/tailwind/` | [tokens.md](../../rules/tokens.md)                                                                                         |
| `packages/context-engine/`             | [context-engine.md](../../rules/context-engine.md)                                                                         |

**Always also load:** Base rules (workflow, github, linear)

## Fix Process

### Phase 1: Gather Review Context

1. **Fetch PR details:**

   ```
   mcp__github__get_pull_request(owner: "{owner}", repo: "{repo}", pull_number: {pr_number})
   ```

2. **Get review comments:**

   ```
   mcp__github__get_pull_request_reviews(owner: "{owner}", repo: "{repo}", pull_number: {pr_number})
   mcp__github__get_pull_request_comments(owner: "{owner}", repo: "{repo}", pull_number: {pr_number})
   ```

3. **Get changed files:**
   ```
   mcp__github__get_pull_request_files(owner: "{owner}", repo: "{repo}", pull_number: {pr_number})
   ```

### Phase 2: Categorize Issues

1. **Extract all issues from reviews:**
   - Inline comments (file:line specific)
   - General review comments
   - Review verdicts and reasons

2. **Categorize by severity:**

   | Category    | Indicator                                       | Priority   |
   | ----------- | ----------------------------------------------- | ---------- |
   | Blocking ❌ | "must", "required", "blocking", REQUEST_CHANGES | Fix first  |
   | Minor ⚠️    | "consider", "suggestion", "nit", COMMENT        | Fix second |

3. **Create fix plan with TodoWrite:**

   ```
   - [ ] Fix: {blocking issue 1}
   - [ ] Fix: {blocking issue 2}
   - [ ] Fix: {minor issue 1}
   - [ ] Verify all fixes
   ```

4. **WAIT for user confirmation before proceeding**

### Phase 3: Load Context

1. **Read each affected file** (full content, not just diff)

2. **Load relevant rules** based on file paths

3. **Understand the original intent** from PR description

### Phase 4: Fix Issues

1. **Work through todos one at a time:**
   - Mark todo as `in_progress` before starting
   - Mark as `completed` immediately after finishing

2. **For each fix:**
   - Read the specific comment/issue
   - Understand what's being asked
   - Make the change following loaded rules
   - Summarize what was changed

3. **After each fix:**
   - Provide summary with code snippets
   - Include file:line references
   - WAIT for user confirmation

### Phase 5: Verify Fixes

1. **Run checks:**

   ```bash
   yarn typecheck
   yarn lint
   yarn test
   ```

2. **Review against original comments:**
   - Does each fix address the feedback?
   - Any unintended side effects?

3. **Fix any new issues introduced**

## Output Format

After all fixes are complete:

```markdown
## ✅ PR Fixes Complete

### PR: #{pr_number} - {title}

### Issues Addressed

| Issue               | File               | Status   |
| ------------------- | ------------------ | -------- |
| {issue description} | `path/file.tsx:42` | ✅ Fixed |
| {issue description} | `path/file.tsx:78` | ✅ Fixed |

### Changes Made

| File               | Change        |
| ------------------ | ------------- |
| `path/to/file.tsx` | {description} |

### Key Code Changes

{Relevant code snippets with file:line references}

### Verification

- [ ] TypeScript: ✅ No errors
- [ ] Lint: ✅ No warnings
- [ ] Tests: ✅ All passing
- [ ] All review comments addressed: ✅

### Next Steps

{Commit and push, or any remaining items}
```

## Principles to Follow

1. **Address the actual feedback** — Don't assume, read carefully
2. **Follow loaded rules** — Rules files are source of truth
3. **One fix at a time** — Don't batch changes, fix incrementally
4. **Verify each fix** — Ensure it actually addresses the comment
5. **Don't over-fix** — Only change what was requested
