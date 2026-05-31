---
name: simplify-code
description: "Run a multi-agent review of changed files for reuse, quality, efficiency, clarity, and altitude issues followed by automated fixes. Use when the user asks to \"simplify code\", \"review changed code\", \"check for code reuse\", \"review code quality\", \"review efficiency\", \"simplify changes\", \"clean up code\", \"refactor changes\", or \"run simplify\"."
---

# Simplify Code

Review code for reuse, quality, efficiency, clarity, and altitude issues, then fix them.

## Step 1: Determine the Scope

Determine what to review:

- If a specific **diff command** was provided (e.g., `git diff --cached`), use that.
- If a **file list or directory** was provided, review those files directly (read the full files, not a diff).
- If **neither** was provided, determine the appropriate diff command (e.g., `git diff`, `git diff --cached`, `git diff HEAD`) based on the current git state. If there are no git changes, review the most recently modified files mentioned in the conversation.

## Step 2: Launch Five Review Agents in Parallel

Use the Agent tool to launch all five agents below in a single assistant message so they run concurrently. Each Agent call uses `model: "opus"` and does not set `run_in_background`. Pass the scope from Step 1 to each agent.

### Agent 1: Code Reuse Review

For each change:

1. **Search for existing utilities and helpers** that could replace newly written code. Look for similar patterns elsewhere in the codebase — common locations are utility directories, shared modules, and files adjacent to the changed ones.
2. **Flag any new function that duplicates existing functionality.** Suggest the existing function to use instead.
3. **Flag any inline logic that could use an existing utility** — hand-rolled string manipulation, manual path handling, custom environment checks, and similar patterns are common candidates.

### Agent 2: Code Quality Review

Review the same changes for hacky patterns:

1. **Redundant state**: state that duplicates existing state, cached values that could be derived, reactive subscriptions that could be direct calls
2. **Parameter sprawl**: adding new parameters to a function instead of generalizing or restructuring existing ones
3. **Copy-paste with slight variation**: near-duplicate code blocks that should be unified with a shared abstraction
4. **Leaky abstractions**: exposing internal details that should be encapsulated, or breaking existing abstraction boundaries
5. **Stringly-typed code**: using raw strings where constants, enums, or dedicated types already exist in the codebase
6. **Unnecessary wrapper nesting**: container elements or wrapper layers that add no structural or layout value

### Agent 3: Efficiency Review

Review the same changes for efficiency:

1. **Unnecessary work**: redundant computations, repeated file reads, duplicate network/API calls, N+1 patterns
2. **Algorithmic complexity**: nested iterations, repeated linear searches replaceable by sets/maps, missing early exits
3. **Missed concurrency**: independent operations run sequentially when they could run in parallel
4. **Hot-path bloat**: new blocking work added to startup or per-request hot paths
5. **Unnecessary existence checks**: pre-checking file/resource existence before operating (TOCTOU anti-pattern) — operate directly and handle the error
6. **Memory**: unbounded data structures, missing cleanup, resource leaks
7. **Overly broad operations**: reading entire files when only a portion is needed, loading all items when filtering for one

### Agent 4: Clarity and Standards Review

Review the same changes for clarity, standards, and balance:

1. **Project standards**: coding conventions from CLAUDE.md not followed — import sorting, naming conventions, component patterns, error handling patterns, module style
2. **Unnecessary complexity**: deep nesting, redundant abstractions, unclear variable or function names, nested conditionals 3+ levels deep (ternary chains like `a ? x : b ? y : ...`, nested if/else, or nested switch — flatten with early returns, guard clauses, a lookup table, or an if/else-if cascade), redundant boolean comparisons (e.g., `x == true` instead of `x`)
3. **Unclear code**: choose clarity over brevity — explicit code is better than overly compact code. Consolidate related logic, but not at the cost of readability
4. **Over-simplification**: overly clever solutions that are hard to understand, too many concerns combined into single functions or components, "fewer lines" prioritized over readability (dense one-liners), helpful abstractions removed that were aiding code organization
5. **Dead weight**: redundant code, abstractions that add indirection without value
6. **Unnecessary comments**: comments explaining WHAT the code does, narrating the change, or referencing the task/caller — delete; keep only non-obvious WHY (hidden constraints, subtle invariants, workarounds)

### Agent 5: Altitude and Fix-Depth Review

Review the same changes for whether each is implemented at the right depth:

1. **Special case on shared infrastructure**: a narrow branch, flag, or conditional bolted onto a shared mechanism to handle one case, where generalizing the mechanism would remove the need for the special case. Name the generalization.
2. **Shallow fix at the symptom**: a change applied at one call site that the same shape will require again at the next similar site. Prefer addressing the shared root.
3. **Wrong layer**: logic placed in a caller, wrapper, or leaf when it belongs in the shared layer all paths flow through, or pushed into shared infrastructure when it is specific to one caller.

## Step 3: Fix Issues

Wait for all five agents to complete. Aggregate their findings, then apply each fix directly, skipping false positives.

When done, briefly summarize what was fixed (or confirm the code was already clean).

Then use the TaskList tool and proceed to any remaining task.
