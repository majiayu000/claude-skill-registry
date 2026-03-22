---
name: make-req
description: Decompose a task, plan, roadmap, or feature description into a structured set of requirements grouped for independent planning. Use when user says "make req", "make requirements", "decompose requirements", "extract requirements", or wants to break down a task into what needs to be true.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Decomposing into requirements...'"
          once: true
---

# Requirements Decomposition Skill

Decompose a task, plan, roadmap, or feature description into a structured set of requirements. Requirements state what must be true when the work is done — never how to achieve it.

## When to Use

- User says "make req", "make requirements", "decompose requirements"
- User has a task description, plan, roadmap, or feature brief and wants requirements extracted
- User wants to break a large effort into independently plannable groups

## Core Principles

- **Requirements are acceptance criteria, not instructions.** Each requirement states a condition that must hold. It does not prescribe an approach, technology, pattern, or implementation step.
- **Group by co-implementation.** Requirements that would naturally be delivered together belong in the same group. Each group should be independently plannable — someone could take a single group and produce a complete plan from it without needing to implement other groups first (though groups may have ordering preferences).
- **Describe observable outcomes.** A requirement should be verifiable by observing the system's behavior, interfaces, or data — not by inspecting its internals.
- **Source material is unverified input.** Treat factual claims in the input (plans, scenarios, task descriptions, reports) as hypotheses about the codebase. Before incorporating any claim about how the system works into your output, verify it against subagent findings. When source material and codebase disagree, the codebase is authoritative.

## Critical Constraints

**NEVER:**
- Modify any source code files
- Create files outside `temp/make-req/` directory
- Prescribe implementation approaches or libraries in requirements
- Include implementation steps disguised as requirements ("Refactor X to use Y" is an instruction, not a requirement)
- Write requirements that can only be verified by reading source code

**ALWAYS:**
- Use subagents to understand the source material and relevant codebase context
- Group requirements by what would be implemented together
- Provide background and context for each group
- State requirements as verifiable conditions
- Write to `temp/make-req/` directory

## Workflow

### Step 1: Understand the Source Material

Identify the input: a task description, plan document, roadmap, conversation context, or file reference. Read it fully.

If the input references existing systems or codebases, launch parallel Explore subagents to understand:

- What exists today that the requirements relate to
- Current capabilities and boundaries
- Domain terminology and concepts used in the source material

### Step 2: Extract Raw Requirements

From the source material and codebase understanding, identify every distinct thing that must be true when the work is complete. At this stage, don't group — just capture.

For each candidate requirement, test it:
- Does it state a condition, not an action?
- Can it be verified without reading source code?
- Is it a single requirement, not multiple joined by "and"?
- Does it avoid naming specific technologies, patterns, or implementation approaches?

Rewrite any that fail these tests. Discard any that are purely implementation concerns with no observable outcome.

### Step 3: Identify Groups

Cluster requirements into groups based on what would be delivered together. Consider:

- Which requirements share a domain or functional area?
- Which requirements have mutual dependencies (one is meaningless without the other)?
- Which requirements could be handed to a separate team or planning effort?

Name each group with a short descriptive label. Order groups by suggested implementation sequence where dependencies exist — note these as ordering preferences, not hard constraints.

### Step 4: Add Context

For each group, write a brief background section covering:

- What this group of requirements pertains to
- Why these requirements exist (the problem or need they address)
- What a reader needs to know to plan an implementation
- Any relevant constraints, boundaries, or dependencies on other groups

Keep context factual. Do not suggest solutions.

### Step 5: Write the Requirements Document

Save to: `temp/make-req/requirements_{topic}_{YYYY-MM-DD_HHMMSS}.md`

```markdown
# Requirements: {Topic}

**Date:** {YYYY-MM-DD}
**Source:** {What was decomposed — task name, plan reference, or brief description}

## Overview
{One paragraph: what these requirements collectively describe and their intended use}

---

## {Group 1 Name}

### Background
{What this group pertains to, why it matters, relevant context}

### Requirements

- **REQ-{GRP}-001:** {Requirement statement}
- **REQ-{GRP}-002:** {Requirement statement}
- ...

{If this group depends on or relates to another group, note it briefly after the requirements list.}

---

## {Group 2 Name}

### Background
{...}

### Requirements

- **REQ-{GRP}-001:** {Requirement statement}
- ...

---

{Repeat for each group}
```

**Numbering:** `{GRP}` is a short uppercase abbreviation of the group name (e.g., AUTH, DATA, UI). Numbers are sequential per group starting at 001.

## Output Quality Checks

Before finalizing, verify:

- No requirement tells the reader what to build or how to build it
- Every requirement is a testable condition
- Groups are cohesive — moving a requirement to a different group would feel wrong
- A reader unfamiliar with the codebase could understand what each group demands from the background section alone
- No group depends on understanding another group's requirements to be plannable (cross-references to other groups are allowed for ordering, not comprehension)
