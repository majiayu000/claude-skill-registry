---
name: 161-java-profiling-detect
description: Use when you need to set up Java application profiling to detect and measure performance issues — including automated async-profiler v4.0 setup, problem-driven profiling (CPU, memory, threading, GC, I/O), interactive profiling scripts, JFR integration with Java 25 (JEP 518, JEP 520), or collecting profiling data with flamegraphs and JFR recordings. This should trigger for requests such as Improve the code with profiling; Apply Profiling; Refactor the code with profiling; Add profiling support. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
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
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Improve the code with profiling
- Apply Profiling
- Refactor the code with profiling
- Add profiling support

## Workflow

1. **Read profiling setup reference**

Read `references/161-java-profiling-detect.md` and use script templates exactly as provided.

2. **Create profiler workspace and scripts**

Create `profiler/scripts` and `profiler/results`, copy setup/profile scripts verbatim, and make scripts executable.

3. **Run application with profiling compatibility**

Start Java process with required profiling JVM flags and verify target process availability for profiler attachment.

4. **Collect profiling artifacts**

Capture CPU/memory/lock/GC/I/O data and produce timestamped flamegraph and JFR outputs for analysis.

## Reference

For detailed guidance, examples, and constraints, see [references/161-java-profiling-detect.md](references/161-java-profiling-detect.md).
