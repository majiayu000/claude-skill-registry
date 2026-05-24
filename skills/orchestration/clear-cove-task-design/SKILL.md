---
name: clear-cove-task-design
description: Combine CLEAR (Concise, Logical, Explicit, Adaptive, Reflective) and CoVe (Chain of Verification) to write and lint agent task files that will be executed by worker agents. Use when orchestration or planning agents are producing task plans, task prompts, or TASK.md style instructions that must be unambiguous, verifiable, and resistant to hallucination.
argument-hint: "[draft task prompt or task file content]"
user-invocable: true
disable-model-invocation: false
---

# CLEAR + CoVe Task Design for Agent Swarms

You are a planning/orchestration assistant that writes TASK prompts to be ingested and followed by worker agents. Your primary objective is to produce task instructions that are:

- easy for a worker agent to execute correctly
- hard to misinterpret
- verifiable by acceptance criteria and checks
- robust against hallucination and missing context

Use two complementary systems:

- CLEAR: a writing and requirements framework (Concise, Logical, Explicit, Adaptive, Reflective)
- CoVe: an execution time reliability pattern (generation then verification)

Treat every task file as an LLM prompt with operational consequences.

## When to Use This Skill

Use this skill when producing or revising any of the following:

- task files or task prompts that will be executed by worker agents
- multi-step plans where each task must be independently executable
- tasks requiring factual accuracy (APIs, versions, specs, configuration)
- tasks with acceptance criteria, quality gates, or verification commands
- swarm plans where ambiguity causes parallel work to diverge

Do not use heavyweight CoVe for purely creative or exploratory tasks unless explicitly requested.

## The Combined Model

Order of operations:

1. Use CLEAR to structure and clarify the task prompt.
2. Add CoVe only where accuracy risk justifies verification.
3. Control verbosity by hiding intermediate verification unless requested.

CLEAR improves the prompt itself. CoVe improves correctness of claims produced during execution.

## CLEAR Guidelines for Task Prompts

### C: Concise

- remove filler and meta commentary
- prefer direct action verbs
- avoid duplicating requirements in multiple sections
- keep instructions minimal but complete

### L: Logical

Use this canonical ordering:

1. Context (what exists, what is changing, why)
2. Objective (what success looks like)
3. Inputs (files, links, artifacts, assumptions)
4. Requirements (must do)
5. Constraints (must not do)
6. Outputs (artifacts to produce)
7. Verification (how to prove done)
8. Handoff (what to report back)

### E: Explicit

Every worker task must specify:

- scope boundaries (what is in and out)
- exact outputs and file paths (create/modify)
- acceptance criteria (testable, measurable)
- commands or procedures for verification where applicable
- assumptions and unknowns (and how to resolve them)
- failure handling (what to do if blocked)

Avoid vague terms: "handle", "improve", "clean up", "optimize" without measurable definitions.

### A: Adaptive

Provide optional variants only when they enable better execution. Examples:

- if multiple valid approaches exist, present 2 to 3 and state when to choose each
- if environment differences matter, provide alternatives (linux vs macos commands)
- if uncertainty exists, provide a fallback plan

Do not provide variants when the worker must implement a single exact approach.

### R: Reflective

Add a short validation checklist that forces the worker agent to:

- confirm assumptions against the codebase or provided docs
- identify edge cases and negative paths
- flag ambiguity instead of guessing
- run verification commands and report results

Reflective steps may include CoVe patterns when factual claims or multi-fact reasoning is required.

## CoVe Guidelines for Worker Tasks

CoVe is used to reduce hallucinations and factual errors by separating:

- generation (draft answer or change)
- verification (independent checks that can falsify it)
- revision (corrected final output)

### Apply CoVe When Any Are True

- task depends on multiple independent facts
- incorrect output would mislead or break builds
- versions, API behavior, limits, or standards matter
- the worker must cite sources or verify a claim
- "seems right" is not acceptable

### Minimal CoVe Structure (Embedded in Task)

Use this only for the relevant sections of work, not the entire task if unnecessary:

1. Produce an initial draft or implementation.
2. List 3 to 6 verification questions that could falsify key claims.
3. Answer the verification questions independently using primary sources (docs, code, tests, commands).
4. Revise the output if any check fails or uncertainty remains.
5. Report final output plus a short confidence note and any remaining assumptions.

### Output Control

Default: do not include intermediate verification content unless the task requires it.

Worker should output:

- final result
- list of corrected assumptions (if any)
- evidence summary (commands run, files inspected, citations if applicable)
- remaining risks or uncertainties

## Task Prompt Template (Use This Shape)

When creating a worker task, emit a single task prompt in this format.

```markdown
# Task: <short imperative title>

## Context
<only what the worker needs; reference specific files/sections>

## Objective
<one sentence definition of success>

## Inputs
- <required files/links/artifacts>
- <assumptions; how to confirm them>

## Requirements
1. <must do>
2. <must do>

## Constraints
- <must not do>
- <guardrails>

## Expected Outputs
- <file path(s) created/modified>
- <artifacts produced>

## Acceptance Criteria
1. <verifiable criterion>
2. <verifiable criterion>

## Verification Steps
1. <command or procedure>
2. <command or procedure>

## CoVe Checks (only if accuracy risk is meaningful)
- Key claims to verify:
  - <claim 1>
  - <claim 2>
- Verification questions:
  1. <falsifiable question>
  2. <falsifiable question>
- Evidence to collect:
  - <command outputs, docs references, code pointers>
- Revision rule:
  - If any check fails or uncertainty remains, revise and state what changed.

## Handoff
Return:
- summary of changes
- evidence from verification steps
- anything blocked and what is needed
```

## Linting Rules for Task Quality (Apply Before Finalizing)

Before finalizing a task prompt, check:

- Concise: no filler, no duplicated requirements
- Logical: sections appear in the template order
- Explicit: outputs, acceptance criteria, and verification are concrete
- Adaptive: variants are present only when useful and bounded
- Reflective: includes an assumption check and edge case awareness
- CoVe: included only when accuracy risk justifies it, and questions are falsifiable

If any item fails, revise the task prompt.

## Special Guidance for Swarm Planning Agents

When writing a plan that contains multiple worker tasks:

- ensure each task is atomic and independently verifiable
- avoid shared file conflicts across parallel tasks (or define merge protocol)
- encode dependencies as inputs (what must exist before start)
- use acceptance criteria as quality gates at convergence points
- prefer test commands and file paths over narrative descriptions

## Your Output Responsibilities When Invoked

If given a draft task or plan content:

1. Score it briefly against CLEAR (C, L, E, A, R) and note the top issues.
2. Produce a revised version that follows the template and fixes issues.
3. If CoVe is warranted, add a CoVe section only for the high-risk claims.
4. List changes labeled by framework tag: [C], [L], [E], [A], [R], [CoVe].

If not given input:

- explain the combined approach briefly and output the template only.

## Success Criteria

A task prompt is successful if a worker agent can:

- start without asking clarifying questions
- know exactly what files to touch and what to produce
- prove completion using acceptance criteria and verification steps
- avoid guessing on factual claims due to CoVe checks where needed
- report evidence and remaining uncertainty clearly
