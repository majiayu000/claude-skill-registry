---
name: fujitsu-mainframe
description: Analyzes and assists with Fujitsu mainframe systems including FACOM, PRIMERGY, BS2000/OSD, OSIV/MSP, OSIV/XSP, NetCOBOL, PowerCOBOL, and Fujitsu JCL. Extracts business logic from Fujitsu COBOL programs, analyzes Fujitsu JCL jobs, migrates Fujitsu mainframe applications to modern platforms (Java, cloud, containers), and creates migration strategies. Use when working with Fujitsu mainframe migration, FACOM systems, BS2000, OSIV platforms, NetCOBOL, PowerCOBOL, Fujitsu-specific COBOL extensions, Fujitsu JCL, or when users mention Fujitsu mainframe modernization, analyzing Fujitsu COBOL/JCL, SYMFOWARE database, or planning migration from Fujitsu legacy systems.
---

# Fujitsu Mainframe Analyzer

Analyze and migrate Fujitsu mainframe systems (FACOM, BS2000/OSD, OSIV, NetCOBOL, PowerCOBOL, Fujitsu JCL, SYMFOWARE) to modern Java/cloud platforms.

## Core Capabilities

## 1. Fujitsu COBOL Analysis

Extract NetCOBOL/PowerCOBOL programs, Fujitsu-specific verbs, proprietary file organizations (SAM/PAM/ISAM), SYMFOWARE embedded SQL, screen handling (ACCEPT/DISPLAY with CRT STATUS).

### 2. Fujitsu JCL Analysis

Parse JOB statements, STEP definitions, ASSIGN/FILEDEF statements, conditional execution, cataloged procedures, resource allocation.

### 3. BS2000/OSD System Analysis

Analyze ENTER statements, system commands, file handling (PAM, SAM, ISAM), job variables, SDF processing.

### 4. SYMFOWARE Database Migration

Extract embedded SQL, schemas, stored procedures, transactions. Migrate to PostgreSQL, Oracle, or SQL Server.

### 5. Migration to Modern Platforms

Generate Spring Boot microservices, REST APIs, cloud-native apps (AWS, Azure, GCP), containerized deployments (Docker, Kubernetes), CI/CD pipelines.

## Workflow

### Step 1: Discover Assets

```bash
find . -name "*.cbl" -o -name "*.CBL" -o -name "*.cob"  # COBOL
find . -name "*.ncb" -o -name "*.NCB"  # NetCOBOL
find . -name "*.fjcl" -o -name "*.jcl"  # JCL
find . -name "*.cpy" -o -name "*.CPY"  # Copybooks
find . -name "*.sdf" -o -name "*.SDF"  # SDF files
```

### Step 2: Analyze Structure

Extract divisions, data structures, file definitions, screen definitions, embedded SQL, Fujitsu-specific extensions. Key features:

- File organization: SEQUENTIAL, RELATIVE, INDEXED
- Screen handling: CRT STATUS, screen control
- Database: SYMFOWARE SQL
- Fujitsu verbs: ACCEPT OMITTED, INSPECT extensions
- Error handling: FILE STATUS, DECLARATIVES

### Step 3: Map Dependencies

Build graphs: CALL hierarchies, copybook usage, file dependencies (FACOM), database access (SYMFOWARE), JCL sequences, screen definitions.

### Step 4: Create Migration Strategy

Document architecture, Fujitsu-specific features, Java/cloud design, data migration, roadmap. **Load `references/migration-strategy.md` for detailed framework.**

## Fujitsu-Specific Features

### NetCOBOL Extensions

- Windowing, GUI support (PowerCOBOL)
- Enhanced ACCEPT/DISPLAY with positioning
- Object-oriented: CLASS definitions
- Extended exception handling

### SYMFOWARE Database

- Embedded SQL: SELECT, INSERT, UPDATE, DELETE
- Cursors: DECLARE, OPEN, FETCH, CLOSE
- Transactions: COMMIT, ROLLBACK
- Migration: SYMFOWARE → PostgreSQL (cost), Oracle (enterprise), SQL Server

### File Systems

| Type | Description | Java Equivalent |
| ------ | ------------- |-----------------|
| SAM | Sequential | `BufferedReader`/`Writer` |
| PAM | Partitioned | File directory |
| ISAM | Indexed | Database with index |
| GDG | Versioned | Timestamp naming |

## Quick Patterns

### COBOL → Java Spring Boot

**Load `references/migration-patterns.md` for detailed examples.** Quick overview:

**Fujitsu COBOL:**

```cobol
SELECT EMPFILE ASSIGN TO "EMPDATA"
    ORGANIZATION IS INDEXED
    ACCESS MODE IS RANDOM
    RECORD KEY IS EMP-ID
```

**Java JPA:**

```java
@Entity
@Table(name = "employees")
public class Employee {
    @Id
    private Integer empId;
    private String empName;
    private BigDecimal empSalary;
}
```

### JCL → Shell + Kubernetes

**Fujitsu JCL:**

```jcl
//STEP010  EXEC PGM=VALIDATE
//STEP020  EXEC PGM=PROCESS,COND=(0,EQ,STEP010)
```

**Shell:**

```bash
./validate && ./process
```

**Load `references/migration-patterns.md` for Kubernetes CronJob examples.**

## Data Type Mappings

**Load `references/data-mappings.md` for comprehensive tables.** Critical mappings:

| Fujitsu COBOL | Java | Notes |
| --------------- | ------ |-------|
| `PIC 9(n)` | `int`, `long`, `BigInteger` | Size dependent |
| `PIC S9(n)V9(m)` | `BigDecimal` | **ALWAYS** for decimals |
| `PIC X(n)` | `String` | Alphanumeric |
| `COMP-3` | `BigDecimal` | **NEVER** float/double |
| `OCCURS n` | `List<T>` | Prefer List over array |

| SYMFOWARE | PostgreSQL |
| ----------- | ------------ |
| `CHAR(n)` | `CHAR(n)` |
| `VARCHAR(n)` | `VARCHAR(n)` |
| `DECIMAL(p,s)` | `NUMERIC(p,s)` |
| `TIMESTAMP` | `TIMESTAMP WITH TIME ZONE` |
| `BLOB` | `BYTEA` |
| `CLOB` | `TEXT` |

## Migration Strategies

### Strangler Fig Pattern (Recommended)

Gradually replace functionality. Lower risk, learn and adjust. **Load `references/migration-strategy.md` for detailed steps.**

### Big Bang

Complete rewrite, single cutover. Higher risk, clean architecture. For smaller systems.

### Hybrid

Core services modernized first, periphery later. Balanced risk/reward.

## Output Requirements

### Analysis Report Structure

1. **Executive Summary** - Overview, business impact, recommendation
2. **Current State** - Inventory, architecture, technology, dependencies
3. **Fujitsu Features** - NetCOBOL/PowerCOBOL, SYMFOWARE, file systems, screens, JCL
4. **Target Design** - Architecture, tech stack, microservices, data model, APIs
5. **Migration Plan** - Approach, timeline, resources, risks, costs
6. **Technical Appendix** - Code samples, mappings, utilities, testing

**Load `references/migration-strategy.md` for complete frameworks and templates.**

## Critical Best Practices

1. **ALWAYS use BigDecimal** for COMP-3 and decimals (NEVER float/double)
2. **Preserve business logic** - understand before changing
3. **Test with production data** - validate conversions
4. **Document Fujitsu extensions** - proprietary features need special handling
5. **Plan parallel run** - compare outputs before cutover
6. **Automate testing** - regression suite for validation
7. **Monitor everything** - logging, metrics, alerts
8. **Security first** - authentication, authorization, encryption

## Common Challenges & Solutions

**Fujitsu-Specific Features** → Custom adapters, equivalent libraries, re-implementation
**Screen Handling** → User requirements gathering, modern UX design
**File Processing** → ETL tools, Spring Batch
**Performance** → Caching (Redis), async processing, DB optimization
**Transactions** → Spring @Transactional, Saga pattern

## Reference Files

When detailed information needed:

- **`references/migration-patterns.md`** - Complete code examples for all migration patterns
- **`references/data-mappings.md`** - Comprehensive type mappings, REDEFINES, dates, best practices
- **`references/migration-strategy.md`** - Full framework: assessment, design, testing, cutover, costs

Load these files for in-depth guidance on specific topics.
