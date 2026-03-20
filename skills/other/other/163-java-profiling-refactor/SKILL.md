---
name: 163-java-profiling-refactor
description: Use when you need to refactor Java code based on profiling analysis findings — including reviewing docs/profiling-problem-analysis and docs/profiling-solutions, identifying specific performance bottlenecks, and implementing targeted code changes to address CPU, memory, or threading issues. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
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

## When to use this skill

- Refactor performance
- Optimize hot path
- Performance refactoring

## Reference

For detailed guidance, examples, and constraints, see [references/163-java-profiling-refactor.md](references/163-java-profiling-refactor.md).
