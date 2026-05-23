---
name: generate-task
description: 'Generate a single worker task prompt using the existing CLEAR + selective CoVe task design standard and the task structure requirements used by swarm-task-planner. Use when you need to create or rewrite one TASK/ file or one task block for a plan.'
argument-hint: "[task title and brief description]"
user-invocable: true
disable-model-invocation: false
---

# Generate Task (Worker Task Prompt)

You generate ONE worker task prompt that will be executed by a worker agent.

You MUST follow the existing canonical task writing standard and structure:

- CLEAR ordering (Context, Objective, Inputs, Requirements, Constraints, Expected Outputs, Acceptance Criteria, Verification Steps, CoVe Checks only if needed, Handoff).
- Task structure requirements and fields (Dependencies, Priority, Complexity, Accuracy Risk, Required Inputs, Can Parallelize With, Reason, Handoff).

Do NOT add any new fields, sections, agents, or mechanisms beyond what is already defined in the referenced task standards.

## Inputs

When invoked, you will be given some combination of:

- a task title and brief description (in $ARGUMENTS)
- optionally: dependencies, repo/file references, constraints, and verification expectations

If critical information is missing, you MUST keep the task executable by:

- stating assumptions under Required Inputs (and how to confirm them), and
- ensuring Verification Steps can confirm correctness, or explicitly indicate what blocks verification.

## Output

Output exactly ONE task prompt in this format:

```markdown
### Task: [Task ID] - [Descriptive Name]

**Dependencies**: [List task IDs or "None"]
**Priority**: [1-N based on dependency depth]
**Complexity**: [Low/Medium/High based on scope, not time]
**Accuracy Risk**: [Low/Medium/High]

## Context
[Only what the worker needs; reference specific files/sections]

## Objective
[One sentence definition of success]

## Required Inputs
- [Files/links/artifacts the worker must read]
- [Assumptions and how to confirm them]

## Requirements
1. [Must do]
2. [Must do]

## Constraints
- [Must not do]
- [Guardrails, scope boundaries]

## Expected Outputs
- [Files created/modified with paths]
- [Artifacts produced]

## Acceptance Criteria
1. [Specific, measurable criterion]
2. [Another verifiable requirement]

## Verification Steps
1. [How to verify criterion 1]
2. [How to verify criterion 2]

## CoVe Checks (ONLY if Accuracy Risk is Medium/High)
- Key claims to verify:
  - [Claim 1]
  - [Claim 2]
- Verification questions (falsifiable):
  1. [Question 1]
  2. [Question 2]
- Evidence to collect:
  - [Commands run, docs referenced, code pointers]
- Revision rule:
  - If any check fails or uncertainty remains, revise and state what changed.

**Can Parallelize With**: [List task IDs that can run concurrently, or "None - blocks on dependencies"]
**Reason**: [Why parallelization is safe; avoid file conflicts]
**Handoff**: [What the worker must report back: summary, evidence, blockers]
```

## Lint Before Final Output

Before returning the task prompt, you MUST lint it using the existing rules:

- Concise: no filler, no duplicated requirements
- Logical: sections in canonical order
- Explicit: objective, outputs, acceptance criteria, verification are concrete
- CoVe: included only when Accuracy Risk is Medium/High, and questions are falsifiable

If any lint check fails, revise the task prompt and re-lint.
