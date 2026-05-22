---
name: branch-review
description: Review code changes on a feature branch compared to a base branch (default: master). Checks for pattern consistency, code duplication, unnecessary variables, and proper use of existing utilities. Use when you want a thorough code review before merging.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - Task
  - TodoWrite
user-invocable: true
---

# Branch Code Review

Review code changes on a feature branch, checking for:
- Pattern consistency with existing codebase
- Code duplication that should be factored out
- Unnecessary temporary variables
- Proper use of existing functions and utilities
- Potential N+1 query patterns or looped API calls
- Type safety issues (avoiding `as any` casts)
- Error handling consistency

## Usage

```
/branch-review [base-branch]
```

**Arguments:**
- `base-branch` (optional): The branch to compare against. Defaults to `master`.

## Review Process

### Step 1: Gather Context

First, get an overview of the changes:

```bash
# Get summary of changed files
git diff [base-branch]...HEAD --stat

# Get the detailed diff
git diff [base-branch]...HEAD
```

### Step 2: Read Changed Files

For each significantly changed file, read the full file to understand context:
- Use the `Read` tool to examine new/modified files
- Look at surrounding code to understand existing patterns
- Check imports and dependencies

### Step 3: Pattern Analysis

Compare new code against existing patterns in the codebase:

1. **Store Modules**: Check if new store modules follow `vuex-module-decorators` patterns
2. **API Clients**: Verify API methods follow existing error handling patterns
3. **Vue Components**: Ensure components follow existing structure (props, computed, methods order)
4. **Backend Models**: Check Girder plugin patterns (ProxiedModel, @autoDescribeRoute, etc.)

### Step 4: Issue Categories

Organize findings into categories:

| Category | Description |
|----------|-------------|
| **Pattern Consistency** | Code that doesn't follow established patterns |
| **Code Duplication** | Logic that should be extracted to shared utilities |
| **Unnecessary Variables** | Temporary variables used only once |
| **Missing Abstractions** | Opportunities to use existing utilities |
| **Performance Issues** | N+1 queries, looped API calls, missing batch endpoints |
| **Type Safety** | `as any` casts, missing types, unsafe assertions |
| **Error Handling** | Inconsistent or duplicate error handling |

### Step 5: Provide Actionable Feedback

For each issue:
1. Quote the specific code location (`file:line`)
2. Explain why it's an issue
3. Provide a concrete suggestion or code example
4. Note the severity (must fix vs. nice to have)

## Example Output Format

```markdown
## Code Review: [branch-name]

### Overall Assessment
[Brief summary of code quality and main concerns]

### Issues to Address

#### 1. [Issue Title]
**File:** `src/store/example.ts:42`
**Severity:** High/Medium/Low

**Current code:**
```typescript
// problematic code
```

**Suggestion:**
```typescript
// improved code
```

**Rationale:** [Why this change improves the code]

---

### Minor Observations
- [Small improvements that aren't blocking]

### Questions for Clarification
- [Anything that needs discussion]

### Summary Table
| Category | Status |
|----------|--------|
| Pattern Consistency | ✅/⚠️ |
| Code Duplication | ✅/⚠️ |
| ...etc |
```

## Codebase-Specific Guidelines

When reviewing this codebase, pay special attention to:

1. **Batch API Calls**: Never loop and make individual API calls. Use batch endpoints.
2. **Store vs API Error Handling**: Errors should be caught in store actions, not API methods.
3. **TypeScript Types**: Avoid `as any`. Extend interfaces if needed.
4. **Vue Patterns**: Use `vuex-module-decorators` style (@Module, @Action, @Mutation).
5. **Utility Functions**: Check `src/utils/` before creating new helpers.

See [CLAUDE.md](../../../CLAUDE.md) for complete coding guidelines.
