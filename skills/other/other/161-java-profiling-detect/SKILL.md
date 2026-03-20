---
name: 161-java-profiling-detect
description: Use when you need to set up Java application profiling to detect and measure performance issues — including automated async-profiler v4.0 setup, problem-driven profiling (CPU, memory, threading, GC, I/O), interactive profiling scripts, JFR integration with Java 25 (JEP 518, JEP 520), or collecting profiling data with flamegraphs and JFR recordings. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java Profiling Workflow / Step 1 / Collect data to measure potential issues

Set up the Java profiling detection phase: automated environment setup with async-profiler v4.0, problem-driven interactive profiling scripts, and comprehensive data collection for CPU hotspots, memory leaks, lock contention, GC issues, and I/O bottlenecks. Uses JEP 518 (Cooperative Sampling) and JEP 520 (Method Timing) for reduced overhead.

**What is covered in this Skill?**

- Run application with profiling JVM flags (run-java-process-for-profiling.sh)
- Interactive profiling script (profiler/scripts/profile-java-process.sh) — copy exact template
- Directory structure: profiler/scripts/, profiler/results/, profiler/current/
- Automated OS/architecture detection and async-profiler download
- CPU, memory, lock, GC, I/O profiling modes
- Flamegraph and JFR output with timestamped results

**Scope:** Use the exact bash script templates without modification or interpretation.

## Constraints

Copy bash scripts exactly from templates. Ensure JVM flags are applied for profiling compatibility. Verify Java processes are running before attaching profiler.

- **CRITICAL**: Copy the bash script templates exactly — do not modify, interpret, or enhance
- **SETUP**: Create profiler directory structure: profiler/scripts, profiler/results
- **EXECUTABLE**: Make scripts executable with chmod +x
- **BEFORE APPLYING**: Read the reference for exact script templates and setup instructions

## When to use this skill

- Review Java code for profiling
- Add profiling support

## Reference

For detailed guidance, examples, and constraints, see [references/161-java-profiling-detect.md](references/161-java-profiling-detect.md).
