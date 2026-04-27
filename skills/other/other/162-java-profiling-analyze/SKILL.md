---
name: 162-java-profiling-analyze
description: Use when you need to analyze Java profiling data collected during the detection phase — including interpreting flamegraphs, memory allocation patterns, CPU hotspots, threading issues, systematic problem categorization, evidence documentation with profiling-problem-analysis and profiling-solutions markdown files, or prioritizing fixes using Impact/Effort scoring. This should trigger for requests such as Analyze JFR profile; Analyze the profile; Analyze the performance; Analyze the memory. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java Profiling Workflow / Step 2 / Analyze profiling data

Analyze profiling results systematically: inventory results (flamegraphs, JFR, GC logs, thread dumps), identify problems (memory leaks, CPU hotspots, threading issues), document findings using standardized templates (profiling-problem-analysis-YYYYMMDD.md, profiling-solutions-YYYYMMDD.md), prioritize using Impact/Effort scores, and correlate multiple profiling files for validation.

**What is covered in this Skill?**

- Inventory: scan profiler/results/ for allocation-flamegraph, heatmap-cpu, memory-leak, *.jfr, *.log, *.txt
- Problem identification: memory (leaks, excessive allocations, GC pressure), performance (CPU hotspots, blocking), threading (deadlocks, contention, pool saturation)
- Documentation: docs/profiling-problem-analysis-YYYYMMDD.md, docs/profiling-solutions-YYYYMMDD.md
- Prioritization: Impact (1–5) / Effort (1–5), focus on high priority first
- Tools: async-profiler, JFR, JProfiler/YourKit, GCViewer, flamegraphs, heatmaps

**Scope:** Validate profiling results represent realistic load scenarios. Cross-reference multiple files. Include quantitative metrics.

## Constraints

Validate profiling results represent realistic load before analysis. Document assumptions and limitations. Cross-reference multiple files.

- **VALIDATE**: Ensure profiling results represent realistic load scenarios before analysis
- **DOCUMENT**: Record assumptions and limitations in analysis reports
- **CROSS-REFERENCE**: Use multiple profiling files to validate findings
- **BEFORE APPLYING**: Read the reference for problem analysis and solutions templates
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Analyze JFR profile
- Analyze the profile
- Analyze the performance
- Analyze the memory
- Analyze the threading
- Analyze the GC
- Analyze the profiling
- Analyze the profiling
- Performance analysis

## Workflow

1. **Read analysis reference and inventory inputs**

Read `references/162-java-profiling-analyze.md` and inventory profiling artifacts in `profiler/results/`.

2. **Validate data quality and assumptions**

Confirm datasets represent realistic load conditions and record assumptions/limitations before drawing conclusions.

3. **Identify and prioritize bottlenecks**

Analyze memory/CPU/threading findings, cross-reference multiple files, and prioritize issues by Impact/Effort.

4. **Document findings and solution options**

Create `docs/profiling-problem-analysis-YYYYMMDD.md` and `docs/profiling-solutions-YYYYMMDD.md` with quantitative evidence.

## Reference

For detailed guidance, examples, and constraints, see [references/162-java-profiling-analyze.md](references/162-java-profiling-analyze.md).
