---
name: pli-migration-analyzer
description: Analyzes legacy PL/I (Programming Language One) programs to assist with migration to modern Java applications. Extracts business logic, data structures, procedure definitions, and file operations from PL/I code. Generates migration reports and creates Java implementation strategies. Use when working with mainframe migration, PL/I analysis, legacy system modernization, or when users mention PL/I to Java conversion, analyzing .pli/.PLI/.pl1 files, working with PL/I procedures, or planning Java service implementations from PL/I programs.
metadata:
  version: "1.0"
  category: legacy-migration
---

# PL/I Migration Analyzer

Analyzes legacy PL/I programs and generates Java migration strategies. Extracts business logic, data structures, procedures, and dependencies to produce actionable migration plans.

## Workflow

### 1. Discover PL/I Programs

Find PL/I source files in the workspace:

```bash
find . -name "*.pli" -o -name "*.PLI" -o -name "*.pl1"
```

### 2. Analyze Program Structure

For each PL/I program, extract:

- **Entry points**: PROCEDURE OPTIONS(MAIN)
- **Declarations**: DCL statements (FIXED DECIMAL, FIXED BINARY, CHARACTER, BIT, structures)
- **Procedures**: Nested procedures and functions
- **File operations**: OPEN, READ, WRITE, CLOSE statements
- **Exception handling**: ON conditions (ENDFILE, ERROR, etc.)
- **Dependencies**: CALL statements, %INCLUDE directives

Use scripts for automation:

- `extract-structure.py <source_file>` - Extract structural information
- `analyze-dependencies.sh <directory>` - Generate dependency graph
- `estimate-complexity.py <source_file>` - Estimate migration effort

### 3. Map to Java Design

Convert PL/I elements to Java:

- **Structures** → POJOs with appropriate types
- **Procedures** → Service methods
- **File operations** → Java I/O or database operations
- **ON conditions** → try-catch exception handling
- **Arrays** → Lists or arrays (adjust 1-based to 0-based indexing)

**Critical Type Mapping:**

- `FIXED DECIMAL(n,m)` → `BigDecimal` (**NEVER float/double**)
- `FIXED BINARY(n)` → `int`, `long`
- `CHARACTER(n)` → `String`
- `BIT(1)` → `boolean`

### 4. Generate Java Implementation

Create Java classes using:

- `generate-java-classes.py <data_structure_file>` - Generate POJOs from structures

Ensure:

- BigDecimal for all financial calculations
- Proper exception handling (no GO TO)
- Array bounds adjustment (1-based → 0-based)
- String operations adjustment (SUBSTR is 1-based, substring is 0-based)

### 5. Produce Migration Report

Generate comprehensive report with:

1. **Program Overview**: Purpose, entry points, complexity estimate
2. **Dependencies**: Called procedures, included files, external references
3. **Data Structures**: Tables with PL/I types and Java equivalents
4. **Business Logic Summary**: Key algorithms and rules
5. **Java Design**: Proposed classes, methods, packages
6. **Migration Estimate**: Effort in person-days, risk assessment
7. **Action Items**: Prioritized tasks with owners

Use template: `assets/migration-report-template.md`

## Quick Reference

### Common Conversions

**Procedure to Method:**

```pli
CALC_TOTAL: PROCEDURE(qty, price) RETURNS(FIXED DECIMAL(15,2));
    result = qty * price;
    RETURN(result);
END CALC_TOTAL;
```

→

```java
public BigDecimal calcTotal(BigDecimal qty, BigDecimal price) {
    return qty.multiply(price);
}
```

**File I/O to Streams:**

```pli
DO WHILE(¬eof);
    READ FILE(infile) INTO(rec);
    CALL process_record(rec);
END;
```

→

```java
try (BufferedReader reader = Files.newBufferedReader(path)) {
    reader.lines().forEach(this::processRecord);
}
```

### Critical Rules

1. **Use BigDecimal for FIXED DECIMAL** - Float/double lose precision
2. **Arrays are 1-based in PL/I, 0-based in Java** - Adjust loops and indices
3. **Refactor GO TO statements** - Use structured control flow
4. **ON conditions map to try-catch** - Exception handling strategy required
5. **SUBSTR is 1-based** - Java substring is 0-based and end-exclusive

## Detailed References

For comprehensive information:

- **Type mapping & patterns**: [pli-reference.md](references/pli-reference.md) - Complete data type conversions, code patterns, migration checklist, common pitfalls
- **Pseudocode translation**: [pseudocode-pli-rules.md](references/pseudocode-pli-rules.md) - Rules for converting PL/I to pseudocode
- **Transaction handling**: [transaction-handling.md](references/transaction-handling.md) - Database transaction patterns
- **Performance**: [performance-patterns.md](references/performance-patterns.md) - Optimization strategies
- **Messaging**: [messaging-integration.md](references/messaging-integration.md) - Event-driven patterns
- **Testing**: [testing-strategy.md](references/testing-strategy.md) - Test approach and validation

## Output Format

Structure migration reports with these sections:

```markdown
# [Program Name] Migration Analysis

## Executive Summary
High-level overview and recommendations

## Program Overview
Purpose, functionality, complexity metrics

## Dependencies
Procedure calls, file dependencies, external references

## Data Structures
Tables mapping PL/I structures to Java classes

## Business Logic Analysis
Key algorithms, rules, calculations

## Java Design Proposal
Package structure, class design, API interfaces

## Migration Estimate
Effort (person-days), risk level, timeline

## Action Items
Prioritized tasks with acceptance criteria
```
