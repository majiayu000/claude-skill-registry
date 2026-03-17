---
name: java-maintenance
description: Java code maintenance standards including prioritization, refactoring triggers, and compliance verification
user-invocable: false
allowed-tools: Read, Grep, Glob
---

# Java Maintenance Skill

**REFERENCE MODE**: This skill provides reference material. Load specific standards on-demand based on current task.

Java code maintenance standards for identifying, prioritizing, and executing refactoring work. This skill covers compliance checking, maintenance prioritization, and refactoring triggers.

## Prerequisites

This skill applies to all Java projects requiring maintenance or refactoring.

## Workflow

### Step 1: Load Prioritization Framework

**CRITICAL**: Load this standard for any maintenance work.

```
Read: standards/maintenance-prioritization.md
```

This provides foundational rules for:
- High priority: API contract issues, code organization
- Medium priority: Method design, maintainability
- Low priority: Style and conventions

### Step 2: Load Additional Standards (As Needed)

**Refactoring Triggers** (load for code analysis):
```
Read: standards/refactoring-triggers.md
```

Use when: Identifying when code needs refactoring based on metrics and patterns.

**Compliance Checklist** (load for verification):
```
Read: standards/compliance-checklist.md
```

Use when: Verifying code meets all Java development standards.

## Key Rules Summary

### Priority Categories

**High Priority (API/Contract Issues)**
- Missing @NonNull annotations on public APIs
- Inconsistent null safety patterns
- Poor error handling
- Single Responsibility violations

**Medium Priority (Maintainability)**
- Long methods (>50 lines)
- High parameter counts (>4 without objects)
- High cyclomatic complexity (>15)
- Poor naming conventions

**Low Priority (Style)**
- Formatting inconsistencies
- Import organization
- Comment style variations

### Refactoring Triggers
```java
// TRIGGER: Method too long
// Refactor when method exceeds 50 lines

// TRIGGER: Too many parameters
// Refactor when method has >4 parameters
// Use parameter objects

// TRIGGER: High complexity
// Refactor when cyclomatic complexity >15
// Extract methods, use polymorphism
```

### Compliance Verification
```bash
# Run analysis
mvn verify -Pcode-analysis

# Check coverage
mvn jacoco:report

# Run Sonar
mvn sonar:sonar
```

## Related Skills

- `pm-dev-java:java-core` - Core Java patterns
- `pm-dev-java:junit-core` - Test coverage requirements
- `pm-dev-java:javadoc` - Documentation standards

## Standards Reference

| Standard | Purpose |
|----------|---------|
| maintenance-prioritization.md | Priority framework for refactoring |
| refactoring-triggers.md | Metrics and patterns triggering refactoring |
| compliance-checklist.md | Full standards compliance verification |
