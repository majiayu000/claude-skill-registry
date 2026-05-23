---
name: planner-rt-ica
description: Identify required inputs, dependencies, and uncertainty during planning. Use when generating plans or task graphs under incomplete information. Does not block plan generation; instead localizes gaps and creates unblock dependencies.
argument-hint: "[optional-scope-or-task-id]"
disable-model-invocation: false
user-invocable: false
---

# Planner RT-ICA (Planning-Phase Input Completeness Analysis)

## Role

This skill adapts RT-ICA for **planning contexts**.

Its purpose is NOT to block planning.
Its purpose is to prevent invented requirements while still allowing a correct
dependency-first plan to be produced.

This skill runs as a **pre-pass** before task decomposition and task writing.

---

## Core Principles

1. **No invention**

   - Never fabricate requirements, constraints, interfaces, or acceptance criteria.
   - Missing information must be surfaced explicitly.

2. **Localize uncertainty**

   - Missing inputs block _only the tasks that depend on them_, not the entire plan.

3. **Plan must still exist**

   - The planner must always be able to emit:
     - a dependency graph,
     - task skeletons,
     - and explicit unblock paths.

4. **Execution safety**
   - Any task with missing critical inputs must be marked such that worker agents
     will BLOCK rather than assume.

---

## Inputs Analyzed

For the given planning scope (entire plan or a specific task/workstream), identify
whether the following are PRESENT, PARTIAL, or MISSING:

- Functional intent (what outcome is desired)
- Scope boundaries (in-scope / out-of-scope)
- External interfaces (APIs, CLIs, files, services)
- Constraints (performance, security, compliance, environment)
- Existing system context (repo, architecture, runtime)
- Verification expectations (how correctness will be proven)

---

## Output Contract (Planning-Oriented)

Produce a structured analysis with the following sections:

### 1. Completeness Summary

- APPROVED-FOR-PLANNING
- APPROVED-WITH-GAPS
- BLOCKED-FOR-PLANNING (only if literally no planning signal exists)

> APPROVED-WITH-GAPS is the expected and normal outcome for brownfield,
> refactor, and discovery scenarios.

---

### 2. Missing Inputs (By Dependency)

For each missing or partial input, emit:

- Input name
- Affected tasks or workstreams
- Impact if assumed incorrectly
- Whether the input is:
  - required before execution
  - required before detailed design
  - optional / refinement-level

---

### 3. Required Unblock Actions

For each missing input, specify one of:

- Direct question to user
- Discovery task (e.g. repo scan, architecture trace)
- Validation spike / investigation task

These MUST be expressible as planner tasks.

---

### 4. Planning Annotations to Apply

The planner MUST apply the following annotations downstream:

- Add explicit **Dependencies** on unblock tasks
- Populate **Required Inputs** fields in task blocks
- Elevate **Accuracy Risk** for affected tasks
- Add **Unblock Questions** sections to tasks that cannot execute yet

---

## Behavioral Rules for the Planner

When this skill reports missing inputs:

- The planner MUST:

  - create explicit input-collection or discovery tasks,
  - wire them as dependencies,
  - allow unaffected tasks to proceed in parallel.

- The planner MUST NOT:
  - invent placeholder values,
  - silently downgrade requirements,
  - remove tasks to avoid uncertainty.

---

## Relationship to RT-ICA (Execution)

This skill does NOT replace rt-ica.

- `planner-rt-ica`:

  - Enables safe planning under uncertainty.
  - Localizes gaps.
  - Produces unblock paths.

- `rt-ica`:
  - Is used before delegating execution to worker agents.
  - Blocks execution if required inputs remain missing.

Any task produced under APPROVED-WITH-GAPS MUST still pass `rt-ica`
before being executed by a specialist agent.

---

## Success Criteria

This skill is successful if:

- A dependency-correct plan can be produced without invented facts.
- Every missing input is visible, localized, and actionable.
- No worker task can execute without required inputs being explicit.
