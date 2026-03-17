---
name: cobol-migration-analyzer
description: Analyzes legacy COBOL programs and JCL jobs to assist with migration to modern Java applications. Extracts business logic, identifies dependencies, generates migration reports, and creates Java implementation strategies. Use when working with mainframe migration, COBOL analysis, legacy system modernization, JCL workflows, or when users mention COBOL to Java conversion, analyzing .cbl/.CBL/.cob files, working with copybooks, or planning Java service implementations from COBOL programs.
metadata:
  version: "1.0"
  category: legacy-migration
---

# COBOL Migration Analyzer

Analyze legacy COBOL programs and JCL scripts for migration to Java. Extract business logic, data structures, and dependencies to generate actionable migration strategies.

## Core Capabilities

## 1. COBOL Program Analysis

Extract COBOL divisions (IDENTIFICATION, ENVIRONMENT, DATA, PROCEDURE), Working-Storage variables, file definitions (FD), business logic paragraphs, PERFORM statements, CALL hierarchies, embedded SQL, and error handling patterns.

### 2. JCL Job Analysis

Parse JCL job steps, program invocations, data dependencies (DD statements), conditional logic (COND, IF/THEN/ELSE), return codes, and resource requirements.

### 3. Copybook Processing

Extract record layouts with level numbers, REDEFINES clauses, group items, OCCURS clauses, and picture clauses. Generate Java POJOs from copybook structures.

### 4. Dependency Mapping

Build complete dependency graphs showing CALL hierarchies, copybook usage, file dependencies, database table access, and shared utility references across the codebase.

## Workflow

### Step 1: Discover COBOL Assets

Find COBOL programs, JCL jobs, and copybooks:

```bash
find . -name "*.cbl" -o -name "*.CBL" -o -name "*.cob"
find . -name "*.jcl" -o -name "*.JCL"
find . -name "*.cpy" -o -name "*.CPY"
```

Use `scripts/analyze-dependencies.sh` or `scripts/analyze-dependencies.ps1` to generate dependency graph.

### Step 2: Extract Structure

Use `scripts/extract-structure.py` to parse COBOL programs and extract divisions, variables, paragraphs, and dependencies in JSON format.

### Step 3: Generate Java Code

Use `scripts/generate-java-classes.py` to convert copybooks to Java POJOs with appropriate data types and Bean Validation annotations.

### Step 4: Estimate Complexity

Use `scripts/estimate-complexity.py` to calculate migration complexity based on LOC, external calls, file operations, SQL statements, and control flow.

### Step 5: Create Migration Strategy

Document program overview, dependencies, data structures, business logic patterns, proposed Java design, migration estimate, and action items.

## Quick Reference

### COBOL to Java Type Mapping

| COBOL Picture | Java Type | Notes |
| --------------- | ----------- |-------|
| `PIC 9(n)` | `int`, `long`, `BigInteger` | Unsigned numeric |
| `PIC S9(n)` | `int`, `long`, `BigInteger` | Signed numeric |
| `PIC 9(n)V9(m)` | `BigDecimal` | Unsigned decimal |
| `PIC S9(n)V9(m)` | `BigDecimal` | Signed decimal |
| `PIC S9(n)V9(m) COMP-3` | `BigDecimal` | **Packed decimal - critical precision!** |
| `PIC S9(n) COMP` / `BINARY` | `int`, `long` | Binary storage |
| `PIC S9(n) COMP-1` | `float` | Single precision (avoid for financial) |
| `PIC S9(n) COMP-2` | `double` | Double precision (avoid for financial) |
| `PIC X(n)` | `String` | Alphanumeric/character |
| `PIC A(n)` | `String` | Alphabetic only |
| `PIC N(n)` | `String` | National/Unicode |
| `OCCURS n` | `List<T>` or `T[]` | Fixed arrays/tables |
| `OCCURS n DEPENDING ON` | `List<T>` | Variable-length arrays |
| `88 level` | `enum` or constants | Condition names |
| `INDEX` | `int` | Table index (1-based in COBOL) |

### Common Pattern Conversions

- **File I/O**: `READ...AT END` → `BufferedReader` with try-with-resources or NIO streams
- **File updates**: `REWRITE` → Update operations in DB or file systems
- **Table lookup**: `SEARCH` → Linear search with streams
- **Binary search**: `SEARCH ALL` → `Collections.binarySearch()` or `stream().filter().findFirst()`
- **String operations**: `STRING/UNSTRING` → `StringBuilder` or `String.split()`
- **Inspection**: `INSPECT` → `String.replace()`, `replaceAll()`, or regex
- **CALL statements**: → Method calls or service invocations
- **EVALUATE**: → `switch` statement (Java 14+ with enhanced switch)
- **Date arithmetic**: `FUNCTION INTEGER-OF-DATE` → `LocalDate` operations
- **ACCEPT DATE/TIME**: → `LocalDate.now()`, `LocalTime.now()`
- **Condition names (Level 88)**: → `enum` or typed constants
- **Computed GO TO**: → Strategy pattern or switch statement
- **REDEFINES**: → Union types, ByteBuffer views, or separate accessor classes
- **COPY statements**: → Package imports or shared entity classes

### Example: Copybook to Java POJO

**COBOL Copybook:**

```cobol
01  EMPLOYEE-RECORD.
    05  EMP-ID        PIC 9(6).
    05  EMP-NAME      PIC X(30).
    05  EMP-SALARY    PIC S9(7)V99 COMP-3.
```

**Generated Java:**

```java
public class EmployeeRecord {
    private int empId;
    private String empName;
    private BigDecimal empSalary;
    // getters/setters
}
```

## Migration Considerations

**Critical Patterns:**

1. **ALWAYS** use `BigDecimal` for COMP-3 and numeric with decimals (never float/double)
2. **Preserve precision**: Use `BigDecimal` with exact scale for financial calculations
3. **1-based indexing**: Document that COBOL arrays start at 1, Java at 0
4. **Implicit conversions**: Make COBOL's automatic numeric↔string conversions explicit
5. **REDEFINES**: Model as union type, ByteBuffer overlay, or separate view classes
6. **Computed GO TO**: Refactor to strategy pattern or switch statement
7. **ALTER statement**: Refactor to structured control flow (if/while/switch)
8. **PERFORM THRU**: Map to single method containing full paragraph range
9. **BY REFERENCE vs BY CONTENT**: Document parameter passing semantics
10. **Test rigorously**: Validate with production data samples, especially for COMP-3

**Output Requirements:**

- Program overview and type classification
- Complete dependency graph (CALL tree, copybooks, files, DB tables)
- Data structure mapping (copybooks → Java classes)
- Business logic summary (key paragraphs → methods)
- Proposed Java architecture (services, repositories, entities)
- Migration effort estimate (complexity score, LOC, risk factors)
- Prioritized action items

## Advanced Topics

For detailed conversion rules and patterns, see:

- **[pseudocode-cobol-rules.md](references/pseudocode-cobol-rules.md)** - Comprehensive COBOL to pseudocode conversion rules including data types, statements, file operations, string operations, table operations, program control, translation patterns, and common gotchas
- **[pseudocode-common-rules.md](references/pseudocode-common-rules.md)** - Common pseudocode syntax and conventions applicable to all languages
- **[transaction-handling.md](references/transaction-handling.md)** - Transaction management and rollback strategies for CICS/IMS to Java
- **[messaging-integration.md](references/messaging-integration.md)** - Message queue and async patterns (MQ, CICS queues to JMS/Kafka)
- **[performance-patterns.md](references/performance-patterns.md)** - Batch processing optimization and memory management
- **[testing-strategy.md](references/testing-strategy.md)** - Comprehensive testing including unit, integration, parallel validation, and data-driven testing

## Tools and Scripts

All scripts support cross-platform execution (Windows PowerShell, bash):

- `analyze-dependencies.sh/ps1` - Generate dependency graph
- `extract-structure.py` - Parse COBOL structure to JSON
- `generate-java-classes.py` - Convert copybooks to Java POJOs
- `estimate-complexity.py` - Calculate migration complexity score

Scripts use standard libraries only and output JSON for easy integration with CI/CD pipelines.
