---
name: review-code
description: >
  Review code changes following HMIS project standards. Use when reviewing a pull request,
  verifying code changes, or checking code quality. Covers CodeRabbit verification,
  backward compatibility, persistence checks, and project-specific patterns.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
argument-hint: "[file-or-pr]"
---

# Code Review Guidelines

Review code changes following HMIS project standards and patterns.

## Review Checklist

### 1. Backward Compatibility
- No modified existing constructor signatures
- No renamed database columns (e.g., `purcahseRate` is intentional)
- No renamed composite components without checking ALL usage
- Entity properties kept alongside new DTO properties

### 2. AI Suggestion Verification
- **Never accept CodeRabbit/AI suggestions without verification**
- Check for existing implementations before adding null checks
- Verify lazy initialization patterns (e.g., `getBillFinanceDetails()` already handles nulls)
- Search codebase for existing patterns before adding new code

### 3. Persistence Configuration
- `persistence.xml` must NOT contain hardcoded JNDI names
- Must use `${JDBC_DATASOURCE}` and `${JDBC_AUDIT_DATASOURCE}`
- No hardcoded DDL generation paths

### 4. JSF/XHTML Rules
- AJAX update targets must be JSF components (not plain HTML)
- No CSS/jQuery selectors in update/process attributes
- Use `h:outputText` instead of HTML headings
- PrimeFaces button classes, not Bootstrap

### 5. DTO Patterns
- Direct JPQL constructor queries (not entity-to-DTO loops)
- Use `findLightsByJpql()` with explicit cast
- Only persisted fields in JPQL (not derived properties)
- Wrapper types in DTO constructors

### 6. Security
- New privileges added to `Privileges.java` enum (not reordering)
- Privilege checks in controllers and XHTML `rendered` attributes
- No credentials committed to git

### 7. Query Patterns
- `retired = false` included in queries
- `inactive = false` for item filtering where applicable
- Proper null handling for optional relationships (LEFT JOIN)

## Process

1. Read the changed files
2. Check each item in the checklist above
3. Report findings with specific file:line references
4. Suggest fixes for any issues found
