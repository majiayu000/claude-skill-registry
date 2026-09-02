---
name: how
description: 'Use when the user asks "how does X work" and wants an architecture walkthrough of the code path or subsystem, including its gotchas. Don''t use for tasks that require source or remote-system changes.'
---

# How

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks to explain how a code path or subsystem works |
| Authority | Read-only: no file, VCS, credential, paid, published, deployed, or remote mutation |
| Side effect | Chat output only; read-only investigation |
| Done | Grounded architecture walkthrough and gotchas returned |

## Inputs

- Target: the specific code path, function, module, class, or subsystem the user names. Required.
- User question: the full natural-language phrasing of the how request. Required.

## Procedure

1. Identify the named target and confirm the scope implied by the user's phrasing. If the target is ambiguous, ask one clarifying question before proceeding.
2. Locate the entry point of the target in the codebase. Use structural read operations (declaration-only summaries, line-range reads) to identify the primary file and its dependencies. Do not open every file blindly.
3. Trace the control flow from the entry point: identify which functions, classes, or modules are called, in what order, and under what conditions. Map data that flows through the path.
4. Identify architectural seams: where the code delegates to an external library, makes a system call, crosses a process or network boundary, or performs I/O.
5. For each major step, note the behavior that a caller or newcomer would find surprising: implicit assumptions, edge conditions handled silently, global state relied upon, error paths that behave differently from happy paths, and performance characteristics that are not obvious from signatures alone.
6. Turn the findings into a grounded walkthrough of the architecture as it exists, not as intended or documented. Cite concrete files and line ranges for key decisions.
7. Return a structured chat report containing the walkthrough and gotchas.

## Failure and recovery
- Target not found: the named path, symbol, or module does not exist in the codebase. Return `no-evidence` and state exactly which target was not found. Do not guess or infer the target's location.
- Ambiguous target: the name matches multiple distinct locations. Ask the user to specify which one they mean. Do not proceed on multiple targets simultaneously.
- Insufficient evidence: the target exists but its implementation is behind an opaque boundary (binary blob, generated code without source, external service). State that the evidence is unavailable and end with `inconclusive`.

## Output
A grounded architecture walkthrough describing:

- The entry point and control flow
- Data that moves through the path
- Architectural seams and their consequences
- Gotchas: surprising behaviors, silent edge cases, and non-obvious assumptions

Output ends with `done` or one of the named failure states: `no-evidence`, `inconclusive`.
