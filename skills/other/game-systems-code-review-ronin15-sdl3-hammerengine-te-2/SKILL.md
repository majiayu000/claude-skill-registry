---
name: game-systems-code-review
description: Review code changes for game/engine systems with a focused Game Systems Engineer mindset. Use when the user asks to review code, check consistency, or validate changes against AGENTS.md standards, especially for C++ engine, threading, performance, or systems behavior.
---

# Game Systems Code Review

## Overview

Perform focused code reviews for game/engine systems, emphasizing correctness, performance, threading safety, and adherence to AGENTS.md standards.

## Workflow

### 1. Intake and scope

- Ask for the diff/PR scope if not provided, or identify it via `git diff`/targeted files.
- Confirm the standards source: read `AGENTS.md` in the repo root for required patterns and constraints.
- Identify the subsystem(s) involved (engine loop, AI, input, resource, world, etc.).

### 2. Review focus areas (Game Systems Engineer lens)

- **Correctness and regressions**: fixed timestep behavior, update/render sequencing, deterministic ordering.
- **Threading and safety**: no background rendering, no static vars in threaded code, ThreadSystem usage.
- **Performance**: avoid per-frame allocations, reuse buffers, reserve capacity, batch where expected.
- **API and ownership**: `std::string_view` vs `std::string`, RAII, smart pointers, lifetime safety.
- **Consistency with architecture**: manager patterns, buffer swaps, event batching, camera usage.
- **Platform pitfalls**: SDL subsystem cleanup pattern, cross-platform guards, SDL boundary usage.
- **Style and naming**: Allman braces, C++20, naming conventions, header/inline rules.

### 3. Findings output format

Use a code-review-first response:

- Findings ordered by severity with file/line references.
- Call out behavior regressions, race risks, or perf traps before style issues.
- If no findings, say so explicitly and mention remaining risks or testing gaps.
- Include open questions/assumptions after findings.
- Provide a brief change summary only after findings.

### 4. Testing suggestions

Recommend targeted tests relevant to the changes (unit, system, or scripts). Do not run tests unless asked.

## Notes

- Prefer minimal, concrete recommendations over broad refactors.
- Avoid modifying code; focus on review and guidance.
- If the user only says “review my changes,” ask which files/PR or use `git diff` to scope.
