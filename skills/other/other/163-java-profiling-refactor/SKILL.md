---
name: 163-java-profiling-refactor
description: Use when you need to refactor Java code based on profiling analysis findings — including reviewing docs/profiling-problem-analysis and docs/profiling-solutions, identifying specific performance bottlenecks, and implementing targeted code changes to address CPU, memory, or threading issues. This should trigger for requests such as Refactor the code with profiling; Apply profiling; Refactor the code with profiling; Optimize hot path. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java Profiling Workflow / Step 3 / Refactor code to fix issues

Implement refactoring based on profiling analysis: review profiling-problem-analysis-YYYYMMDD.md and profiling-solutions-YYYYMMDD.md, identify specific performance bottlenecks, and refactor code to fix them. Ensure all tests pass after changes.

**What is covered in this Skill?**

- Review analysis notes: docs/profiling-problem-analysis-YYYYMMDD.md, docs/profiling-solutions-YYYYMMDD.md
- Identify specific bottlenecks from the documented findings
- Refactor code to address CPU hotspots, memory leaks, threading issues, or other performance problems
- Run verification: ./mvnw clean verify or mvn clean verify

**Scope:** Changes must pass all tests. Apply fixes incrementally and verify after each significant change.

## Constraints

Verify that changes pass all tests before considering the refactoring complete.

- **MANDATORY**: Run `./mvnw clean verify` or `mvn clean verify` after applying refactoring
- **SAFETY**: If tests fail, fix issues before proceeding
- **BEFORE APPLYING**: Read the analysis and solutions documents for specific recommendations
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Refactor the code with profiling
- Apply profiling
- Refactor the code with profiling
- Optimize hot path
- Performance refactoring

## Workflow

1. **Review profiling analysis artifacts**

Read `docs/profiling-problem-analysis-YYYYMMDD.md` and `docs/profiling-solutions-YYYYMMDD.md` to select target bottlenecks.

2. **Apply targeted performance refactors**

Implement focused code changes for documented CPU, memory, or threading hotspots, incrementally and safely.

3. **Verify behavior and performance build integrity**

Run `./mvnw clean verify` or `mvn clean verify`; if tests fail, fix issues before continuing.

4. **Prepare handoff for verification phase**

Summarize implemented changes and expected metric improvements for Step 4 comparison.

## Reference

For detailed guidance, examples, and constraints, see [references/163-java-profiling-refactor.md](references/163-java-profiling-refactor.md).
