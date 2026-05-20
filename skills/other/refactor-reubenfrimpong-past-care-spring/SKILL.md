---
name: refactor
description: Refactor code following PastCare best practices and conventions
disable-model-invocation: true
argument-hint: [file or component to refactor]
---

# Code Refactoring Skill

Refactor the specified code while maintaining functionality and following project conventions.

## Refactoring Target
$ARGUMENTS

## Process

1. **Read and Understand**
   - Read the file(s) to be refactored
   - Understand the current functionality
   - Identify tests that cover this code

2. **Identify Improvements**
   - Code smells (duplication, long methods, large classes)
   - Naming issues (unclear variable/method names)
   - Security issues (tenant isolation, missing @Transactional)
   - Performance issues (N+1 queries, unnecessary computation)
   - Style violations (see best practices below)

3. **Plan Changes**
   - List specific changes to make
   - Ensure changes don't break functionality
   - Consider backward compatibility

4. **Apply Changes**
   - Make incremental changes
   - Keep commits atomic
   - Run tests after each significant change

5. **Verify**
   - Run `./mvnw compile` (backend)
   - Run `./mvnw test` (backend tests)
   - Run `ng build` (frontend)
   - Run `ng test --watch=false` (frontend tests)

## Backend Refactoring Guidelines

### Security Patterns
```java
// Ensure @Transactional on all tenant-scoped queries
@Transactional(readOnly = true)
public List<EntityResponse> getAll() {
    return repository.findAll().stream()...
}

// Custom @Query MUST include church filter
@Query("SELECT e FROM Entity e WHERE e.church.id = :churchId AND ...")
```

### Date/Time
```java
// Use Instant for timestamps
private Instant createdAt;  // ✅
private LocalDateTime createdAt;  // ❌
```

### Percentage Calculations
```java
// Always cap at 100%
double rate = total > 0 ? Math.min((count * 100.0 / total), 100.0) : 0.0;
```

## Frontend Refactoring Guidelines

### Component Structure
- Mobile-first CSS
- Use CSS variables for theming
- Follow BEM naming (.block__element--modifier)

### Colors (use exact values)
- Primary: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- Success: `#10b981`
- Danger: `#ef4444`
- Text: `#1f2937`

### Spacing
- Primary gap: `1rem`
- Border-radius: cards `1rem`, inputs `0.75rem`

### Forms
- Implement backend field error handling
- Use signals for reactive state
- Clear errors on dialog close

## Rules

- NEVER change functionality without tests proving it works
- NEVER introduce security vulnerabilities
- NEVER remove @Transactional from tenant-scoped queries
- NEVER change table/column names (breaks production)
- ALWAYS run tests after refactoring
- ALWAYS preserve existing public APIs unless explicitly changing
