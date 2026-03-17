---
name: iOS Performance
description: Standards for Instruments, Memory Management, and Optimization.
metadata:
  labels: [ios, performance, instruments, leaks]
  triggers:
    files: ['**/*.swift']
    keywords: [Instruments, Allocations, Leaks, dequeueReusableCell]
---

# iOS Performance Standards

## **Priority: P0**

## Implementation Guidelines

### Diagnostic Tools

- **Instruments**: Regularly use **Allocations** and **Leaks** to detect memory issues.
- **Time Profiler**: Identify heavy CPU tasks and Main Thread stalls.
- **Network instrument**: Analyze request payload sizes and frequency.

### Optimization

- **Table/Collection Views**: Always use `dequeueReusableCell` and keep `cellForRowAt` logic lightweight.
- **Image Caching**: Use `SDWebImage` or `Kingfisher` for remote assets to prevent redundant fetching and main-thread decoding. (Note: `AsyncImage` lacks built-in caching; prioritize third-party for lists).
- **Background threads**: Offload expensive work (parsing, encryption) from the Main thread using GCD or Tasks.

### Diagnostics

- **Compiler Warnings**: Enable `SWIFT_TREAT_WARNINGS_AS_ERRORS` in Release builds.
- **Static Analyzer**: Use Xcode's "Analyze" (Product > Analyze) to find logic errors.

## Anti-Patterns

- **CPU work on Main Thread**: `**No parsing/processing on Main**: Use background thread.`
- **Force Cache Flushes**: `**No redundant cache clears**: Let the system handle low-memory warnings via AppDelegate.`
- **Retain Cycles**: `**Check for cycles in Instruments**: Use the Leaks instrument frequently.`

## References

- [Profiling & Optimization](references/implementation.md)
