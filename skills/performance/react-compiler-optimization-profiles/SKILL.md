---
name: react-compiler-optimization-profiles
description: Deep dive into the React Compiler (formerly React Forget) to tune automatic memoization and optimization profiles.
---

# React Compiler Optimization Profiles

## Summary
Deep dive into the React Compiler (formerly React Forget) to tune automatic memoization and optimization profiles.

## Key Capabilities
- Analyze compiler output to verify memoization boundaries.
- Identify distinct optimization de-opt bailouts.
- Configure compiler passes for specific code patterns.

## PhD-Level Challenges
- Quantify the overhead of compiler-injected memoization slots.
- Construct cases where manual memoization outperforms the compiler.
- Analyze the impact of compiler optimizations on cold-start time.

## Acceptance Criteria
- Provide compilation reports for critical components.
- Demonstrate a reduction in manual `useMemo` usage.
- Document de-optimization triggers discovered.
