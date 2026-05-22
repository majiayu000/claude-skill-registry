---
name: code-review
description: Use for QUICK PR reviews with structured checklists (architecture, patterns, security, performance). Provides step-by-step review process, git diff commands, and review report templates. Best for pull request reviews and pre-commit checks. NOT for deep refactoring analysis (use code-review instead).
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

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

## Common Issues to Flag

### :x: Anti-Patterns

```csharp
// Issue: Side effect in command handler
await notificationService.SendAsync(...);

// Issue: Wrong repository type
IPlatformRootRepository<Entity>  // Should be service-specific

// Issue: DTO mapping in handler
var entity = new Entity { Name = request.Name };  // Should use DTO.MapToEntity()

// Issue: Missing eager loading
var items = await repo.GetAllAsync(...);  // Missing relations
items.ForEach(i => Console.WriteLine(i.Related.Name));  // N+1!
```

```typescript
// Issue: No loading state
this.api.getItems().subscribe(items => this.items = items);

// Issue: Direct mutation
this.state.items.push(newItem);

// Issue: Missing cleanup
this.data$.subscribe(...);  // Missing untilDestroyed()
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

## Strengths

1. [Positive point 1]
2. [Positive point 2]

## Issues Found

### Critical (Must Fix)

1. **[File:Line]**: [Description]
    - Problem: [Explanation]
    - Suggestion: [Fix]

### Major (Should Fix)

1. **[File:Line]**: [Description]

### Minor (Consider Fixing)

1. **[File:Line]**: [Description]

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]
```

## Review Commands

```bash
# Find potential issues
grep -r "new Entity {" --include="*.cs"  # DTO mapping in handler
grep -r "SendAsync\|NotifyAsync" --include="*CommandHandler.cs"  # Side effects
grep -r "IPlatformRootRepository" --include="*.cs"  # Generic repository

# Check patterns
grep -r "observerLoadingErrorState" --include="*.ts"  # Loading tracking
grep -r "untilDestroyed" --include="*.ts"  # Subscription cleanup
```

## Verification Checklist

- [ ] All changed files reviewed
- [ ] Architecture compliance verified
- [ ] Platform patterns followed
- [ ] Security concerns addressed
- [ ] Performance considered
- [ ] Review report generated
