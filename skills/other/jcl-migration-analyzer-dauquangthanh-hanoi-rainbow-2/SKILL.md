---
name: jcl-migration-analyzer
description: Analyzes legacy JCL (Job Control Language) scripts to assist with migration to modern workflow orchestration and batch processing systems. Extracts job flows, step sequences, data dependencies, conditional logic, and program invocations. Generates migration reports and creates implementation strategies for Spring Batch, Apache Airflow, or shell scripts. Use when working with mainframe job migration, JCL analysis, batch workflow modernization, or when users mention JCL conversion, analyzing .jcl/.JCL files, working with job steps, procedures, or planning workflow orchestration from JCL jobs.
metadata:
  version: "1.0"
  category: legacy-migration
---

# JCL Migration Analyzer

Analyzes legacy JCL scripts for migration to modern batch processing and workflow orchestration systems like Spring Batch, Apache Airflow, Kubernetes Jobs, or shell scripts.

## Overview

This skill provides comprehensive analysis and migration planning for JCL (Job Control Language) batch processing systems. It extracts job structures, converts JCL constructs to modern workflow patterns, maps data dependencies, and generates implementation-ready migration strategies.

**Key Migration Focus**: JCL to modern orchestration with proper handling of COND logic inversion, data dependencies (DD statements), GDG generations, procedures (PROCs), and batch workflow patterns.

## When to Use This Skill

Use this skill when:

- Analyzing JCL job files (.jcl, .JCL) for modernization
- Planning migration from mainframe batch processing to modern workflow systems
- Converting JCL job steps to Spring Batch, Apache Airflow, or shell scripts
- Understanding JCL COND logic and conditional execution patterns
- Mapping JCL data sets (DD statements) to modern file operations
- Extracting JCL procedures (PROCs) and symbolic parameters
- Generating workflow definitions for orchestration platforms
- Estimating complexity and effort for JCL migration projects
- Creating migration documentation and strategy reports
- Modernizing mainframe batch jobs to cloud-native workflows
- User mentions: JCL analysis, mainframe job migration, batch workflow conversion, COND logic, job steps, procedures, workflow orchestration

## Core Capabilities

### 1. Job Analysis

Extract job structure (JOB card), step sequences, program invocations (EXEC PGM/PROC), conditional logic (COND, IF/THEN/ELSE), return codes, data sets (DD statements), resource requirements, and symbolic parameters.

### 2. Data Dependency Mapping

Extract input/output datasets, temporary datasets, GDG handling, concatenation, DISP parameters, and data flow between steps.

### 3. Procedure Analysis

Parse PROC definitions, symbolic parameters, PROC overrides, nested procedures, INCLUDE statements, and JCLLIB references.

### 4. Workflow Migration

Generate Spring Batch jobs, Apache Airflow DAGs, Kubernetes Jobs, shell scripts, AWS Step Functions, or Azure Logic Apps.

### 5. Conditional Logic Translation

**CRITICAL**: COND logic is INVERTED! Map COND parameters, IF/THEN/ELSE, return codes, step bypassing, and restart logic to modern constructs.

## Workflow

### Step 1: Discover JCL Assets

Find JCL jobs and procedures in the workspace:

```bash
find . -name "*.jcl" -o -name "*.JCL"
find . -name "*.proc" -o -name "*.PROC"
```

Use `scripts/analyze-dependencies.sh` or `scripts/analyze-dependencies.ps1` to generate dependency graph in JSON format.

### Step 2: Extract Structure

Use `scripts/extract-structure.py` to parse JCL files and extract:

- Job cards and parameters
- Step sequences and execution order
- Program/procedure invocations
- DD statements with DISP parameters
- COND and IF/THEN/ELSE logic
- Symbolic parameters

Output format: JSON with job structure, steps, and dependencies.

### Step 3: Analyze Conditional Logic

**CRITICAL**: Identify and document COND logic (which is INVERTED):

- `COND=(0,NE)` → Run if previous RC ≠ 0 (run on ERROR)
- `COND=(0,EQ)` → Skip if previous RC = 0 (skip on SUCCESS)
- IF/THEN/ELSE uses normal logic (not inverted)

Create truth tables for complex conditional logic to avoid errors in migration.

### Step 4: Map Data Dependencies

Track data flow between steps:

- Input datasets (DISP=SHR or OLD)
- Output datasets (DISP=NEW, CATLG)
- Temporary datasets (&&TEMP)
- GDG generations (GDG(0), GDG(+1))
- Dataset concatenations

### Step 5: Estimate Complexity

Use `scripts/estimate-complexity.py` to calculate migration complexity based on:

- Number of job steps
- Conditional logic complexity (COND/IF/THEN/ELSE)
- Number of procedures (PROCs)
- Data dependency complexity
- Number of programs invoked
- GDG usage patterns

### Step 6: Choose Target Platform

Select migration target based on requirements:

- **Spring Batch**: Java-based batch processing with comprehensive features
- **Apache Airflow**: Python-based workflow orchestration with rich UI
- **Shell Scripts**: Simple, lightweight for basic sequential processing
- **Kubernetes Jobs**: Container-based batch processing
- **AWS Step Functions**: Serverless workflow orchestration
- **Azure Logic Apps**: Cloud-based workflow integration

### Step 7: Generate Migration Strategy

Create comprehensive migration report with:

1. **Job Overview**: Purpose, schedule, dependencies
2. **Step Sequence**: Detailed breakdown of each step
3. **Data Flow Diagram**: Input/output dependencies
4. **Conditional Logic Map**: COND translations (with inversion notes)
5. **Target Implementation**: Workflow definition in chosen platform
6. **Migration Estimate**: Effort, complexity score, risk assessment
7. **Action Items**: Prioritized tasks with acceptance criteria

Use template: `assets/migration-report-template.md`

## Quick Reference

### Critical: COND Logic is INVERTED

**JCL COND (inverted):**

```jcl
//STEP020 EXEC PGM=PROG2,COND=(0,NE)
```

Means: "Run if previous RC ≠ 0" → **Run on ERROR!**

**Modern (normal logic):**

```bash
if [ $rc -ne 0 ]; then run_prog2; fi
```

**JCL IF/THEN (normal logic):**

```jcl
//IF1 IF RC = 0 THEN
//STEP020 EXEC PGM=PROG2
//ENDIF
```

**Modern:**

```bash
if [ $rc -eq 0 ]; then run_prog2; fi
```

### Code Patterns

**Simple Sequential:**

```jcl
//STEP010 EXEC PGM=PROG1
//INPUT   DD DSN=INPUT.FILE,DISP=SHR
//OUTPUT  DD DSN=OUTPUT.FILE,DISP=(NEW,CATLG)
//STEP020 EXEC PGM=PROG2
//INPUT   DD DSN=OUTPUT.FILE,DISP=SHR
```

```bash
#!/bin/bash
set -e
prog1 --input="input.file" --output="output.file" || exit 8
prog2 --input="output.file" || exit 8
```

**Conditional (COND - inverted!):**

```jcl
//STEP010 EXEC PGM=VALIDATE
//STEP020 EXEC PGM=PROCESS,COND=(0,NE)
```

```bash
validate_data
rc=$?
if [ $rc -ne 0 ]; then process_data; fi  # INVERTED!
```

**IF/THEN/ELSE (normal logic):**

```jcl
//STEP010 EXEC PGM=VALIDATE
//IF1 IF RC = 0 THEN
//STEP020 EXEC PGM=PROCESSOK
//ELSE
//STEP030 EXEC PGM=PROCESSERR
//ENDIF
```

```bash
validate_data
rc=$?
if [ $rc -eq 0 ]; then processok; else processerr; fi
```

**Procedure:**

```jcl
//MYPROC PROC MEMBER=,INFILE=
//STEP1  EXEC PGM=PROG1
//SYSIN  DD DSN=&MEMBER,DISP=SHR
//       PEND
```

```bash
function myproc() {
    prog1 --sysin="$1" --input="$2"
}
myproc "test.data" "prod.file"
```

### Target Platforms

**Spring Batch:**

```java
@Bean
public Job job() {
    return jobBuilderFactory.get("job")
        .start(step1()).next(step2())
        .on("FAILED").to(errorStep())
        .from(step2()).on("*").to(step3())
        .end().build();
}
```

**Airflow DAG:**

```python
with DAG('job', schedule_interval='@daily') as dag:
    step1 = BashOperator(task_id='step1', bash_command='prog1.sh')
    step2 = BashOperator(task_id='step2', bash_command='prog2.sh')
    step1 >> step2
```

## Key Patterns

**Error Handling:** COND-based → `if [ $rc -ne 0 ]; then error_handler; fi`
**GDG:** `GDG(0)` → `get_latest_generation`, `GDG(+1)` → `create_new_generation`
**Concatenation:** Multiple DD → `cat file1 file2 file3 | process`
**Restart:** COND restart → checkpoint files (`touch .checkpoint_step`)

### Return Code Reference

| RC | Meaning | Action |
| ---- | --------- |--------|
| 0 | Success | Continue |
| 4 | Warning | Continue (informational) |
| 8 | Error | May continue based on COND |
| 12 | Severe Error | Typically stop |
| 16 | Fatal Error | Abort job |

## Migration Checklist

- [ ] Extract job structure, list steps in order, identify programs/procedures, document COND/IF logic
- [ ] Map input/output datasets, identify temp datasets, document GDG usage, track data dependencies
- [ ] Convert COND to normal logic (**INVERT!**), translate IF/THEN/ELSE, handle error paths
- [ ] Choose target (Spring Batch/Airflow/shell), define job structure, implement steps, add monitoring
- [ ] Test normal path, error conditions, conditional branches with production-like data
- [ ] Document job purpose, schedule, dependencies, special requirements

## Critical Tips

1. **COND is INVERTED** - step runs when condition is FALSE! Draw truth tables if needed.
2. **Return codes**: 0=success, 4=warning (OK), 8+=error
3. **Data dependencies**: Carefully map to avoid race conditions
4. **Restart capability**: Implement checkpointing if needed
5. **Monitoring**: Add logging and alerting to modern workflows

## Output Structure

Provide: Job overview, step sequence, data flow, conditional logic, migration target, workflow definition, migration estimate, action items.

## Advanced Topics

For detailed conversion rules and patterns, see:

- **[pseudocode-jcl-rules.md](references/pseudocode-jcl-rules.md)** - Comprehensive JCL to pseudocode conversion rules including element mapping, return codes, DISP parameters, translation patterns, and COND logic handling
- **[pseudocode-common-rules.md](references/pseudocode-common-rules.md)** - Common pseudocode syntax and conventions applicable to all languages
- **[testing-strategy.md](references/testing-strategy.md)** - Comprehensive testing approach including unit tests, integration tests, parallel validation, and data-driven testing for migrated workflows
- **[transaction-handling.md](references/transaction-handling.md)** - Transaction management, rollback strategies, and ACID compliance for batch jobs
- **[messaging-integration.md](references/messaging-integration.md)** - Message queue integration patterns (MQ, JMS, Kafka) for event-driven workflows
- **[performance-patterns.md](references/performance-patterns.md)** - Batch processing optimization, memory management, parallel processing, and performance tuning

## Tools and Scripts

All scripts support cross-platform execution (Windows PowerShell, bash):

- `analyze-dependencies.sh/ps1` - Generate dependency graph in JSON format showing job-to-job, job-to-dataset, and procedure dependencies
- `extract-structure.py` - Parse JCL files and extract structure (job cards, steps, DD statements, COND logic) to JSON
- `generate-java-classes.py` - Generate Java POJOs from data structures for Spring Batch item readers/writers
- `estimate-complexity.py` - Calculate migration complexity score based on steps, conditional logic, procedures, and data dependencies

Scripts use standard libraries only and output JSON for easy integration with CI/CD pipelines and migration tracking tools.

## Integration

Works with job schedulers (Control-M, cron), workflow platforms (Spring Batch, Airflow, K8s), monitoring tools, version control, and CI/CD pipelines.
