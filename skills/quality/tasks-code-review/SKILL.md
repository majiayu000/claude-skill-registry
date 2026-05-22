---
name: tasks-code-review
version: 1.0.0
description: Autonomous subagent variant of code-review. Use when reviewing code changes, pull requests, or performing refactoring analysis with focus on patterns, security, and performance.
infer: false
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

> **Skill Variant:** Use this skill for **autonomous, comprehensive code reviews** with structured checklists. For interactive code review discussions with user feedback, use `code-review` instead.

# Code Review Workflow

## When to Use This Skill

- Reviewing pull requests
- Analyzing code for refactoring
- Pre-commit code quality check
- Security and performance audit

## Review Dimensions

### 1. Architecture Compliance

- [ ] Follows Clean Architecture layers
- [ ] Uses correct repository pattern
- [ ] No cross-service boundary violations
- [ ] Proper separation of concerns

### 2. Pattern Adherence

- [ ] CQRS patterns followed (Command/Query/Handler in ONE file)
- [ ] Entity patterns correct (expressions, computed properties)
- [ ] Frontend component hierarchy respected
- [ ] Platform base classes used correctly

### 3. Code Quality

- [ ] Single Responsibility Principle
- [ ] No code duplication
- [ ] Meaningful naming
- [ ] Appropriate abstractions

### 4. Security

- [ ] No SQL injection vulnerabilities
- [ ] Authorization checks present
- [ ] Sensitive data handling
- [ ] Input validation

### 5. Performance

- [ ] N+1 query prevention (eager loading)
- [ ] Proper paging for large datasets
- [ ] Parallel operations where applicable
- [ ] Caching considerations

## Review Process

### Step 1: Understand Context

```bash
# Get changed files
git diff --name-only main...HEAD

# Get full diff
git diff main...HEAD

# Check commit messages
git log main...HEAD --oneline
```

### Step 2: Categorize Changes

```markdown
## Files Changed

### Domain Layer
- `Entity.cs` - New entity

### Application Layer
- `SaveEntityCommand.cs` - New command

### Persistence Layer
- `EntityConfiguration.cs` - EF configuration

### Frontend
- `entity-list.component.ts` - List component
```

### Step 3: Review Each Category

#### Backend Review Checklist

```markdown
## Entity Review
- [ ] Inherits from correct base (RootEntity/RootAuditedEntity)
- [ ] Static expressions for queries
- [ ] Computed properties have empty `set { }`
- [ ] Navigation properties have `[JsonIgnore]`
- [ ] `[TrackFieldUpdatedDomainEvent]` on tracked fields

## Command/Query Review
- [ ] Command + Handler + Result in ONE file
- [ ] Uses service-specific repository
- [ ] Validation uses fluent API
- [ ] No side effects in command handler
- [ ] DTO mapping in DTO class, not handler

## Repository Usage Review
- [ ] Uses `GetQueryBuilder` for reusable queries
- [ ] Uses `WhereIf` for optional filters
- [ ] Parallel tuple queries for count + data
- [ ] Proper eager loading

## Event Handler Review
- [ ] In `UseCaseEvents/` folder
- [ ] Uses `PlatformCqrsEntityEventApplicationHandler<T>`
- [ ] `HandleWhen` is `public override async Task<bool>`
- [ ] Filters by `CrudAction` appropriately
```

#### Frontend Review Checklist

```markdown
## Component Review
- [ ] Correct base class for use case
- [ ] Store provided at component level
- [ ] Loading/error states handled
- [ ] `untilDestroyed()` on subscriptions
- [ ] Track-by in `@for` loops

## Store Review
- [ ] State interface defined
- [ ] `vmConstructor` provides defaults
- [ ] Effects use `observerLoadingErrorState`
- [ ] Immutable state updates

## Form Review
- [ ] `validateForm()` before submit
- [ ] Async validators conditional
- [ ] Dependent validations configured
- [ ] Error messages for all rules

## API Service Review
- [ ] Extends `PlatformApiService`
- [ ] Typed responses
- [ ] Caching where appropriate
```

### Step 4: Security Review

```markdown
## Security Checklist

### Authorization
- [ ] `[PlatformAuthorize]` on controllers
- [ ] Role checks in handlers
- [ ] Data filtered by company/user context

### Input Validation
- [ ] All inputs validated
- [ ] No raw SQL strings
- [ ] File upload validation

### Sensitive Data
- [ ] No secrets in code
- [ ] Passwords hashed
- [ ] PII handled correctly
```

### Step 5: Performance Review

```markdown
## Performance Checklist

### Database
- [ ] Indexes on filtered columns
- [ ] Eager loading for N+1 prevention
- [ ] Paging for large datasets

### API
- [ ] Response size reasonable
- [ ] Parallel operations used
- [ ] Caching for static data

### Frontend
- [ ] Lazy loading for routes
- [ ] Track-by for lists
- [ ] OnPush change detection
```

## Review Report Template

```markdown
# Code Review Report

## Summary
- **PR/Changes**: [Description]
- **Reviewer**: AI
- **Date**: [Date]

## Overall Assessment
[APPROVED | APPROVED WITH COMMENTS | CHANGES REQUESTED]

## Issues Found

### Critical (Must Fix)
1. **[File:Line]**: [Description]

### Major (Should Fix)
1. **[File:Line]**: [Description]

### Minor (Consider Fixing)
1. **[File:Line]**: [Description]

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
```

## Verification Checklist

- [ ] All changed files reviewed
- [ ] Architecture compliance verified
- [ ] Platform patterns followed
- [ ] Security concerns addressed
- [ ] Performance considered
- [ ] Review report generated

## Related

- `code-review`
- `tasks-test-generation`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**
- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
