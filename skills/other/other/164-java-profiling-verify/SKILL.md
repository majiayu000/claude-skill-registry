---
name: 164-java-profiling-verify
description: Use when you need to verify Java performance optimizations by comparing profiling results before and after refactoring — including baseline validation, post-refactoring report generation, quantitative before/after metrics comparison, side-by-side flamegraph analysis, regression detection, or creating profiling-comparison-analysis and profiling-final-results documentation. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java Profiling Workflow / Step 4 / Verify results

Verify performance optimizations through rigorous before/after comparison: ensure baseline and post-refactoring profiling data use identical test conditions, generate post-refactoring reports, compare metrics (memory, CPU, GC, threading), perform side-by-side flamegraph analysis, document findings in profiling-comparison-analysis-YYYYMMDD.md and profiling-final-results-YYYYMMDD.md, and validate success criteria.

**What is covered in this Skill?**

- Pre-refactoring baseline: run profiler with same load before changes
- Post-refactoring: generate new reports with identical test conditions
- Comparison: memory (leaks, allocations, GC), CPU (hotspots, contention), visual flamegraph comparison
- Documentation: profiler/docs/profiling-comparison-analysis-YYYYMMDD.md, profiler/docs/profiling-final-results-YYYYMMDD.md
- File naming: baseline/after suffixes, timestamp-based organization
- Validation: verify reports exist, compare metrics, identify regressions

**Scope:** Identical test conditions are critical. Document test scenarios. Validate application runs with refactored code before generating new reports.

## Constraints

Use identical test conditions between baseline and post-refactoring. Verify both report sets are complete. Document test scenarios.

- **CONSISTENCY**: Use identical test conditions and load patterns for baseline and post-refactoring
- **VALIDATE**: Ensure both baseline and post-refactoring reports exist and are non-empty before comparison
- **DOCUMENT**: Record test scenarios and load patterns for reproduction
- **BEFORE APPLYING**: Read the reference for comparison templates and validation steps

## When to use this skill

- Verify performance fix
- Performance benchmark

## Reference

For detailed guidance, examples, and constraints, see [references/164-java-profiling-verify.md](references/164-java-profiling-verify.md).
