---
name: review
description: "[Review & Quality] ⚡⚡ Perform comprehensive code review"
argument-hint: [target]
infer: true
---

# Code Review: $ARGUMENTS

Perform a comprehensive code review following EasyPlatform standards.

## Summary

**Goal:** Comprehensive report-driven code review of a PR, file, or branch following EasyPlatform standards.

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Create report file | `plans/reports/code-review-{date}-{slug}.md` |
| 2 | File-by-file review | Read each file, update report with summary/purpose/issues |
| 3 | Holistic review | Re-read report for architecture coherence and layer correctness |
| 4 | Final findings | Critical issues, high priority, architecture recommendations |

**Key Principles:**
- Build report incrementally -- update after EACH file review
- Check: architecture compliance, naming, platform patterns, security, performance
- Logic must be in the LOWEST appropriate layer (Entity > Service > Component)
- Holistic phase: ask "For each architectural decision, WHY this approach over alternatives? Are there trade-offs to document?"

## Review Scope

Target: $ARGUMENTS (can be a PR number, file path, or branch name)

## Review Approach (Report-Driven Two-Phase - CRITICAL)

**⛔ MANDATORY FIRST: Create Todo Tasks for Review Phases**
Before starting, call TodoWrite with:

- [ ] `[Review Phase 1] Create report file` - in_progress
- [ ] `[Review Phase 1] Review file-by-file and update report` - pending
- [ ] `[Review Phase 2] Re-read report for holistic assessment` - pending
- [ ] `[Review Phase 3] Generate final review findings` - pending
Update todo status as each phase completes. This ensures review is tracked.

**Step 0: Create Report File**

- [ ] Create `plans/reports/code-review-{date}-{slug}.md`
- [ ] Initialize with Scope, Files to Review sections

**Phase 1: File-by-File Review (Build Report Incrementally)**
For EACH file, read and **immediately update report** with:

- [ ] File path
- [ ] Change Summary: what was modified/added
- [ ] Purpose: why this change exists
- [ ] Issues Found: naming, typing, responsibility, patterns
- [ ] Continue to next file, repeat

**Phase 2: Holistic Review (Review the Accumulated Report)**
After ALL files reviewed, **re-read the report** to see big picture:

- [ ] Overall technical approach makes sense?
- [ ] Solution architecture coherent as unified plan?
- [ ] New files in correct layers (Domain/Application/Presentation)?
- [ ] Logic in LOWEST appropriate layer?
- [ ] Backend: mapping in Command/DTO (not Handler)?
- [ ] Frontend: constants/columns in Model (not Component)?
- [ ] No duplicated logic across changes?
- [ ] Service boundaries respected?
- [ ] No circular dependencies?

**Phase 3: Generate Final Review Result**
Update report with final sections:

- [ ] Overall Assessment (big picture summary)
- [ ] Critical Issues (must fix before merge)
- [ ] High Priority (should fix)
- [ ] Architecture Recommendations
- [ ] Positive Observations

## Review Checklist

### 1. Architecture Compliance

- [ ] Follows Clean Architecture layers (Domain, Application, Persistence, Service)
- [ ] Uses correct repository pattern (I{Service}RootRepository<T>)
- [ ] CQRS pattern: Command/Query + Handler + Result in ONE file
- [ ] No cross-service direct database access

### 2. Code Quality

- [ ] Single Responsibility Principle
- [ ] No code duplication (DRY)
- [ ] Appropriate error handling with PlatformValidationResult
- [ ] No magic numbers/strings (extract to named constants)
- [ ] Type annotations on all functions
- [ ] No implicit any types
- [ ] Early returns/guard clauses used

### 2.5. Naming Conventions

- [ ] Names reveal intent (WHAT not HOW)
- [ ] Specific names, not generic (`employeeRecords` not `data`)
- [ ] Methods: Verb + Noun (`getEmployee`, `validateInput`)
- [ ] Booleans: is/has/can/should prefix (`isActive`, `hasPermission`)
- [ ] No cryptic abbreviations (`employeeCount` not `empCnt`)

### 3. Platform Patterns

- [ ] Uses platform validation fluent API (.And(), .AndAsync())
- [ ] No direct side effects in command handlers (use entity events)
- [ ] DTO mapping in DTO classes, not handlers
- [ ] Static expressions for entity queries

### 4. Security

- [ ] No hardcoded credentials
- [ ] Proper authorization checks
- [ ] Input validation at boundaries
- [ ] No SQL injection risks

### 5. Performance

- [ ] No O(n²) complexity (use dictionary for lookups)
- [ ] No N+1 query patterns (batch load related entities)
- [ ] Project only needed properties (don't load all then select one)
- [ ] Pagination for all list queries (never get all without paging)
- [ ] Parallel queries for independent operations
- [ ] Appropriate use of async/await

## Output Format

Provide feedback in this format:

**Summary:** Brief overall assessment

**Critical Issues:** (Must fix)

- Issue 1: Description and suggested fix
- Issue 2: Description and suggested fix

**Suggestions:** (Nice to have)

- Suggestion 1
- Suggestion 2

**Positive Notes:**

- What was done well

## See Also

See `code-review` skill for review process guidelines and anti-performative-agreement rules.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
