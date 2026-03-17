---
name: code-review
description: Conducts comprehensive code reviews identifying poor practices, inefficiencies, potential bugs, security vulnerabilities, and provides recommendations for making code DRYer and more maintainable. Use when reviewing files, PRs, or code quality.
allowed-tools: Read, Grep, Glob, Task, WebSearch
user-invocable: true
---

# Code Review Skill

<code-review>

Perform a comprehensive code review following this structured approach. Generate a detailed report covering all sections below.

## Review Scope

Determine what to review:
1. If no argument is provided, ask the user what code they want reviewed
2. If the user wants to review the entire codebase, review the entire codebase. If they ask for a specific file or directory, review that file/directory

## Review Process

### Phase 1: Context Gathering

Before reviewing, gather context:
1. Read the target file(s) completely
2. Identify related files (imports, types, tests)
3. Understand the file's role in the broader architecture
4. Check for existing patterns in similar files in the codebase

### Phase 2: Analysis Categories

Analyze the code across these dimensions:

#### 1. Poor Practices
- Anti-patterns specific to the framework (Next.js, React, Supabase)
- Violation of SOLID principles
- Code smells (long functions, deep nesting, magic numbers)
- Improper separation of concerns
- Hardcoded values that should be configurable
- Missing or improper use of TypeScript features
- Callback hell or promise chain issues
- Improper state management patterns

#### 2. Inefficiencies
- Unnecessary re-renders in React components
- Missing memoization opportunities (useMemo, useCallback, React.memo)
- N+1 query patterns in database calls
- Redundant database queries that could be batched
- Inefficient data transformations
- Unnecessary API calls
- Missing caching opportunities
- Inefficient loops or array operations

#### 3. Potential Bugs
- Race conditions in async code
- Missing null/undefined checks
- Type coercion issues
- Off-by-one errors
- Incorrect error handling that swallows errors
- Memory leaks (missing cleanup in useEffect)
- Stale closure issues
- Missing dependency array items in hooks
- Incorrect comparison operators
- Unhandled promise rejections
- Edge cases not covered

#### 4. Security Vulnerabilities
- SQL injection risks
- XSS vulnerabilities
- Missing input validation
- Sensitive data exposure in logs
- Missing authentication/authorization checks
- Insecure direct object references
- Missing CSRF protection
- Hardcoded secrets or credentials
- Improper error messages exposing internals

#### 5. DRY (Don't Repeat Yourself) Violations
- Duplicated code blocks
- Similar functions that could be generalized
- Repeated conditional logic
- Copy-pasted error handling
- Duplicate type definitions
- Repeated validation logic
- Similar UI patterns not abstracted

#### 6. Type Safety Issues
- Use of `any` type
- Missing return types
- Loose type assertions (`as any`, `as unknown`)
- Missing generic constraints
- Incorrect type narrowing
- Missing discriminated unions for state
- Type assertions hiding real type issues

#### 7. Error Handling
- Missing try-catch blocks
- Generic error messages
- Errors not reported to Sentry
- Missing error boundaries for React
- Inconsistent error response formats
- Silent failures
- Missing user feedback on errors

#### 8. Maintainability Concerns
- Missing or outdated comments
- Unclear variable/function names
- Complex logic without explanation
- Missing JSDoc for public APIs
- Overly complex conditionals
- Deep nesting (> 3 levels)
- Functions doing too many things
- Missing abstraction layers

#### 9. Testing Gaps
- Untested edge cases
- Missing error case tests
- Insufficient test coverage indicators
- Hard-to-test code structure
- Missing mocks for external dependencies

#### 10. Consistency Issues
- Inconsistent naming conventions
- Mixed async patterns (callbacks vs promises vs async/await)
- Inconsistent error handling patterns
- Style inconsistencies with codebase patterns
- Inconsistent use of utilities vs raw implementations

### Phase 3: Report Generation

Generate a structured report with these sections:

```markdown
# Code Review Report

## Summary
[Brief overview of the file's purpose and overall code quality assessment]
[Severity summary: X Critical, Y High, Z Medium, W Low]

## Critical Issues
[Issues that could cause bugs, security vulnerabilities, or data loss]

## High Priority
[Significant issues affecting maintainability, performance, or reliability]

## Medium Priority
[Code quality issues that should be addressed]

## Low Priority / Suggestions
[Nice-to-have improvements and minor suggestions]

## Positive Observations
[Good practices and patterns worth noting]

## Recommendations
[Specific, actionable recommendations with code examples where helpful]
```

### Issue Format

For each issue found, provide:
1. **Location**: File path and line number(s)
2. **Category**: Which analysis category it falls under
3. **Severity**: Critical / High / Medium / Low
4. **Description**: Clear explanation of the issue
5. **Impact**: Why this matters
6. **Recommendation**: How to fix it (with code example if applicable)

### Severity Definitions

- **Critical**: Security vulnerabilities, data loss risks, crashes, or bugs affecting core functionality
- **High**: Performance issues, significant maintainability problems, or patterns that will likely cause bugs
- **Medium**: Code quality issues, minor inefficiencies, or violations of best practices
- **Low**: Style suggestions, minor improvements, or nice-to-haves

## Kove-Specific Patterns to Check

When reviewing code in this codebase, verify:

### Server Actions
- Using `'use server'` directive
- Proper Supabase client instantiation (createClient for server)
- Error reporting to Sentry with context
- Proper revalidation after mutations
- Input validation before database operations

### Database Queries
- Using generated types from `database.types.ts`
- Proper RLS policy compliance
- Multi-tenancy with organization_id filtering
- Batch queries instead of N+1 patterns
- Proper use of `.single()` vs `.maybeSingle()`

### React Components
- Proper 'use client' directive when needed
- Using shadcn/ui components correctly
- Proper form handling with React Hook Form + Zod v4
- Loading states with LoadingButton for async actions
- Error boundaries for critical sections

### Supabase Edge Functions
- Using SDK pattern (supabase.functions.invoke)
- Not using raw fetch for edge functions
- Proper error handling with error types

### Validation
- Using Zod v4 patterns (not v3)
- Proper error messages with `{ error: "..." }`
- Using top-level validators (z.email(), z.uuid())

## Output

After completing the review, present the report to the user in a clear, organized format. Prioritize actionable feedback over nitpicks. Focus on issues that have real impact on code quality, security, or maintainability.

If the code is generally good, acknowledge that while still noting any improvements that could be made.

ignore this line

</code-review>
