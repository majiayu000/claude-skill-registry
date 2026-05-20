---
name: code-review
description: Conduct standardized code reviews using the project's quality checklist. Provides structured feedback with severity levels and actionable recommendations.
allowed-tools: Read, Grep, Glob
---

# Code Review Skill

## Purpose

Guide agents through conducting thorough, standardized code reviews that catch issues before merge while avoiding nitpicking and false positives.

## When to Use This Skill

- Before merging feature branches
- After significant refactors
- When reviewing code from other agents
- When user requests formal review

## Code Review Checklist

### Security & Auth
- [ ] All mutations check `ctx.auth.getUserIdentity()`
- [ ] No API keys or secrets in code
- [ ] User inputs validated and sanitized
- [ ] RLS policies in place (when applicable)

### Performance & Bandwidth
- [ ] No unbounded `.collect()` calls
- [ ] Queries use `.take(limit)` with reasonable limits
- [ ] Stats aggregation used for counts (not loading full lists)
- [ ] Conditional loading with `"skip"` for expensive queries
- [ ] Batch operations with `hasMore` pattern for large deletions

### TypeScript & Type Safety
- [ ] No `any` types or `@ts-ignore`
- [ ] Proper interfaces defined
- [ ] Convex IDs typed as `Id<"tableName">`
- [ ] Optional chaining used appropriately

### Code Quality
- [ ] No `console.log` statements (use proper logging)
- [ ] Error handling with try-catch for async
- [ ] Functions under 50 lines (extract if longer)
- [ ] Meaningful variable names
- [ ] Comments explain "why", not "what"

### React/Frontend (if applicable)
- [ ] Effects have cleanup functions
- [ ] Dependencies array complete
- [ ] No infinite render loops
- [ ] Expensive calculations memoized

### Production Readiness
- [ ] No TODO comments without GitHub issues
- [ ] No debug statements
- [ ] No hardcoded test data
- [ ] Follows existing patterns and conventions

## Review Process

### Step 1: Understand Scope

Before reviewing, clarify:
- What files were changed?
- What's the purpose of this change?
- What's the expected behavior?

### Step 2: Read the Code (Not the Docs)

**CRITICAL:** Don't trust documentation or commit messages. Read the actual implementation.

For each file:
1. **Read the entire file** (not just the diff)
2. **Understand context** - How does this fit into the broader system?
3. **Check integration points** - What other code depends on this?

### Step 3: Apply the Checklist

Go through each category systematically. Don't skip categories even if they seem irrelevant.

### Step 4: Assign Severity Levels

**CRITICAL** - Security, data loss, crashes
- Must fix before merge
- Examples: Missing auth check, SQL injection, unbounded query

**HIGH** - Bugs, performance issues, bad UX
- Should fix before merge
- Examples: Type errors, poor error handling, bandwidth violations

**MEDIUM** - Code quality, maintainability
- Fix or create follow-up task
- Examples: Long functions, unclear naming, missing comments

**LOW** - Style, minor improvements
- Optional, nice-to-have
- Examples: Formatting inconsistencies, redundant code

### Step 5: Provide Structured Feedback

Use this output format:

```markdown
### ✅ Looks Good
- [Positive observation 1]
- [Positive observation 2]
- [Positive observation 3]

### ⚠️ Issues Found
- **[SEVERITY]** [file.ts:line](file.ts:line) - [Issue description]
  - Fix: [Specific recommendation]
  - Why: [Rationale for why this matters]

### 📊 Summary
- Files reviewed: X
- Critical issues: X
- High priority: X
- Medium priority: X
- Low priority: X
```

## Example Review

```markdown
# Code Review: SAM.gov Ingestion Feature

## Files Reviewed
- convex/ingestion/samGov.ts
- convex/schema.ts
- types.ts

---

### ✅ Looks Good
- Rate limiting properly implemented with 10req/sec throttle
- TypeScript interfaces well-defined for SAM.gov API responses
- Deduplication logic handles edge cases correctly

### ⚠️ Issues Found

**Security & Auth**
- **CRITICAL** [samGov.ts:45](convex/ingestion/samGov.ts:45) - API key hardcoded in source
  - Fix: Move to environment variable or Convex secrets
  - Why: Exposes credentials to anyone with repo access

**Performance & Bandwidth**
- **HIGH** [samGov.ts:120](convex/ingestion/samGov.ts:120) - Using `.collect()` without limit
  - Fix: Replace with `.take(1000)` or implement pagination
  - Why: Could exceed Convex bandwidth limits on large datasets

**TypeScript & Type Safety**
- **MEDIUM** [samGov.ts:88](convex/ingestion/samGov.ts:88) - Response typed as `any`
  - Fix: Use `SamGovApiResponse` interface from types.ts
  - Why: Loses type safety, can miss breaking API changes

**Code Quality**
- **LOW** [samGov.ts:200](convex/ingestion/samGov.ts:200) - Function `processOpportunities` is 85 lines
  - Fix: Extract validation, transformation, and storage into separate functions
  - Why: Improves readability and testability

### 📊 Summary
- Files reviewed: 3
- Critical issues: 1
- High priority: 1
- Medium priority: 1
- Low priority: 1

**Recommendation:** Address CRITICAL and HIGH issues before merge. MEDIUM and LOW can be handled in follow-up.
```

## Red Flags That Must Be Flagged

### Security Issues (Always CRITICAL)
- Missing auth checks in mutations
- Hardcoded secrets or API keys
- SQL/NoSQL injection vulnerabilities
- Unvalidated user input
- Missing CSRF protection

### Bandwidth Violations (HIGH or CRITICAL)
- Unbounded `.collect()` calls
- Missing `.take()` limits
- Loading full tables to count rows
- Not using stats aggregation for counts
- Missing conditional loading with `"skip"`

### Type Safety Violations (MEDIUM or HIGH)
- `any` types without justification
- `@ts-ignore` comments
- Unsafe type assertions
- Missing null checks
- Untyped Convex IDs

## What NOT to Flag

### Acceptable Patterns
- ✅ Different coding style if it follows project conventions
- ✅ Alternative implementation that achieves same goal
- ✅ Missing optimization for non-bottleneck code
- ✅ Simplified error handling for internal functions

### False Positives to Avoid
- ❌ "This could be refactored" without clear benefit
- ❌ "Should use library X" when Y is project standard
- ❌ "Missing unit tests" (unless project has test requirement)
- ❌ Subjective preferences not in project conventions

## Communication Guidelines

### Be Specific
❌ "This function is too complex"
✅ "Function `processOpportunities` at line 200 is 85 lines. Consider extracting validation logic into `validateOpportunity()` and transformation into `transformToCanonical()`"

### Provide Context
❌ "Fix auth"
✅ "Missing `ctx.auth.getUserIdentity()` check allows unauthenticated users to call this mutation"

### Suggest Concrete Fixes
❌ "Handle errors better"
✅ "Wrap API call in try-catch and return `{success: false, error: message}` on failure"

### Balance Criticism with Recognition
Every review should start with "✅ Looks Good" section highlighting what was done well.

## Invocation

The user invokes this skill by typing `/code-review` followed by files or directories to review.

**Usage:**
```
/code-review [files-or-directories]
```

**Examples:**
```
/code-review convex/ingestion/samGov.ts
/code-review convex/
/code-review components/AdminView.tsx types.ts
```

If no files specified, review all modified files in current git diff.

## Notes

- **Read the code, not the comments** - Comments can be outdated
- **Check integration points** - How does this affect other code?
- **Verify against project patterns** - See CLAUDE.md, GEMINI.md, CODEX.md
- **Don't be a nitpicker** - Focus on issues that matter
- **Always provide specific file:line references** - Makes fixes easier
