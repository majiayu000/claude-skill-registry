---
name: hunting-bugs
description: Audits codebases for common bug patterns and anti-patterns including timezone issues, null safety, type coercion, async handling, and performance problems. Searches for known problematic patterns and provides actionable fixes. Use when asked to find bugs, audit for issues, check for common problems, or hunt for bugs in codebase.
compatibility: Requires Read, Grep, Glob tools for code analysis
allowed-tools: Read, Grep, Glob, Bash
metadata:
  author: Saturate
  version: "1.0"
---

You are hunting for bugs in a codebase by searching for known problematic patterns. Follow these steps:

## Progress Checklist

Copy this checklist to track your progress:

```
Bug Hunt Progress:
- [ ] Step 1: Parsed arguments and determined scope
- [ ] Step 2: Loaded bug patterns from reference
- [ ] Step 3: Searched codebase for each pattern
- [ ] Step 4: Analyzed findings and confirmed bugs
- [ ] Step 5: Generated report with fixes
```

## Step 1: Parse Arguments and Determine Scope

**User input format:**

Users invoke with: `/bug-hunt [options]`

**Supported arguments:**
- `--category <name>` - Focus on specific category (timezone, null-safety, type-coercion, async, state, performance)
- `--severity <level>` - Only show bugs of this severity or higher (high, medium, low)
- `--path <pattern>` - Limit search to specific path (e.g., `src/**/*.ts`)
- No arguments - Scan entire codebase for all patterns

**Determine search scope:**

```bash
# Default scope
search_path="."
categories="all"
min_severity="low"

# Parse user arguments
# Set search_path if --path provided
# Set categories if --category provided
# Set min_severity if --severity provided
```

## Step 2: Load Bug Patterns

Read the appropriate bug pattern library based on the codebase:

**Primary (always check):**
- [typescript-javascript.md](references/typescript-javascript.md) - TypeScript/JavaScript patterns including:
  - Timezone/date handling bugs (toISOString issues)
  - TypeScript type safety (`any` usage, type assertions, non-null assertions)
  - Null/undefined safety
  - Async/promise handling

**Framework-specific (check if applicable):**
- [react.md](references/react.md) - React-specific patterns (hooks, state, performance)
- [vue.md](references/vue.md) - Vue-specific patterns (reactivity, lifecycle, composition API)

Each pattern includes:
- Search pattern (regex or string)
- Why it's problematic
- How to fix it
- Severity level
- Code examples

## Step 3: Search Codebase Systematically

For each pattern in the loaded reference files, search the codebase.

### Search Strategy

**Use Grep with file type filters:**
```bash
# Example: Search for toISOString date formatting bug
grep -r "toISOString().split" --include="*.ts" --include="*.tsx" --exclude-dir="node_modules"
```

**Focus on high-impact patterns first:**

1. **TypeScript type safety** - `any`, unsafe casts, non-null assertions
2. **Timezone bugs** - `.toISOString().split()` in date formatting
3. **Async errors** - Missing await, no try/catch
4. **Null safety** - Deep property access without optional chaining

**For each pattern match:**
- Note file path and line numbers
- Capture code snippet showing the issue
- Read surrounding context to understand intent

## Step 4: Analyze Findings and Confirm Bugs

**Important:** Not every pattern match is a bug. Analyze each finding:

### Confirmation Criteria

**Read the code context:**
- What is this code trying to accomplish?
- Is this pattern actually problematic in this context?
- Is there existing handling that makes this safe?

**Filter out false positives:**
- Code in comments or strings
- Test/mock code that intentionally uses patterns
- Code with compensating controls
- Patterns used correctly in specific contexts

**Confirm real bugs:**
- Pattern causes incorrect behavior
- Missing error handling leads to crashes
- Performance impact is measurable
- User experience is negatively affected

### Severity Assessment

**High Severity:**
- Causes data loss or corruption
- Breaks core functionality
- Affects all users
- Security vulnerability

**Medium Severity:**
- Affects subset of users (e.g., specific timezones)
- Causes incorrect behavior in edge cases
- Performance degradation
- Poor user experience

**Low Severity:**
- Minor inconsistencies
- Potential future issues
- Code quality concerns
- Could be problematic if code evolves

## Step 5: Generate Report with Fixes

Create a comprehensive bug report:

### Report Structure

```markdown
# Bug Hunt Report

**Date:** {date}
**Scope:** {search scope}
**Patterns Checked:** {number} patterns across {categories}
**Bugs Found:** {total count}

---

## Summary

Found {count} bugs across {categories}:
- High severity: {count}
- Medium severity: {count}
- Low severity: {count}

---

## High Severity Issues

### 1. {Bug Title} - {Category}

**Location:** `{file}:{lines}`

**Severity:** High

**Description:**
{What the bug is and why it's problematic}

**Current Code:**
```{language}
{problematic code snippet}
```

**Issue:**
{Specific problem - e.g., "Converts local date to UTC, causing date to shift for users in positive UTC offset timezones"}

**Impact:**
{Who/what is affected - e.g., "Users in CET/CEST see dates off by 1 day"}

**Fix:**
```{language}
{corrected code snippet}
```

**Explanation:**
{Why this fix works}

**Testing:**
{How to verify the fix}

---

## Medium Severity Issues

{Repeat structure for each medium severity bug}

---

## Low Severity Issues

{Repeat structure for each low severity bug}

---

## Prevention

{Suggestions for preventing these bugs in the future:}
- Add linting rules
- Add unit tests for edge cases
- Document patterns to avoid
- Add type guards
- Use stricter TypeScript settings

---

## Statistics by Category

| Category | High | Medium | Low | Total |
|----------|------|--------|-----|-------|
| Timezone | X | X | X | X |
| Null Safety | X | X | X | X |
| Type Coercion | X | X | X | X |
| Async | X | X | X | X |
| State | X | X | X | X |
| Performance | X | X | X | X |
```

## Example Report Entry

Here's how to document a finding (using the real timezone bug example):

```markdown
### Date Filter Timezone Bug - Timezone/Date Handling

**Location:** `stores/searchStore.ts:356-369`

**Severity:** High

**Description:**
Date filters use `toISOString().split('T')[0]` to format dates, which converts local dates to UTC before formatting. This causes dates to shift to the previous day for users in positive UTC offset timezones.

**Current Code:**
```typescript
const startDate = filters.startDate?.toISOString().split('T')[0];
const endDate = filters.endDate?.toISOString().split('T')[0];
```

**Issue:**
When a user in a positive UTC offset timezone (e.g., CET UTC+1) selects February 1st, the date is converted to UTC (January 31st 23:00) before formatting, resulting in "2024-01-31" being sent to the API instead of "2024-02-01".

**Impact:**
Users in timezones with positive UTC offsets see and send incorrect dates to the API, receiving data for the wrong day.

**Fix:**
```typescript
const formatLocalDate = (date: Date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const startDate = filters.startDate ? formatLocalDate(filters.startDate) : undefined;
const endDate = filters.endDate ? formatLocalDate(filters.endDate) : undefined;
```

**Explanation:**
Uses local timezone methods (`getFullYear()`, `getMonth()`, `getDate()`) instead of UTC conversion. The date stays in the user's local timezone throughout the formatting process.

**Testing:**
1. Set system timezone to CET (UTC+1)
2. Select February 1st in date picker
3. Verify API receives "2024-02-01" not "2024-01-31"
4. Check browser console for formatted date string
```

## Tips for Effective Bug Hunting

1. **Start with high-impact patterns** - Focus on bugs that affect all users first
2. **Read the context** - Don't just flag patterns, understand what the code does
3. **Provide actionable fixes** - Show exactly how to fix it, not just what's wrong
4. **Explain the impact** - Help developers prioritize by explaining consequences
5. **Suggest tests** - Include test cases that would catch these bugs
6. **Be specific** - Reference exact files, lines, and code snippets
7. **Group similar issues** - If the same pattern appears multiple times, note it
8. **Check for existing fixes** - Some bugs might already have workarounds

## When to Skip Patterns

Don't report issues in:
- Test files (unless the test itself is buggy)
- Mock/stub code
- Third-party dependencies (node_modules)
- Generated code
- Code with compensating controls already in place
- Intentional patterns (e.g., `==` for null/undefined check)

## Reference Materials

**Pattern libraries:**
- [typescript-javascript.md](references/typescript-javascript.md) - Core TypeScript/JS patterns (always use)
- [react.md](references/react.md) - React-specific patterns (if React codebase)
- [vue.md](references/vue.md) - Vue-specific patterns (if Vue codebase)
