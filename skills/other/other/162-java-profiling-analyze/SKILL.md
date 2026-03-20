---
name: 162-java-profiling-analyze
description: Use when you need to analyze Java profiling data collected during the detection phase — including interpreting flamegraphs, memory allocation patterns, CPU hotspots, threading issues, systematic problem categorization, evidence documentation with profiling-problem-analysis and profiling-solutions markdown files, or prioritizing fixes using Impact/Effort scoring. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
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

## When to use this skill

- Analyze JFR profile
- Profile analysis
- Performance analysis

## Reference

For detailed guidance, examples, and constraints, see [references/162-java-profiling-analyze.md](references/162-java-profiling-analyze.md).
