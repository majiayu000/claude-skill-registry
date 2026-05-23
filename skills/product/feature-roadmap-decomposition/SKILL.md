---
name: feature-roadmap-decomposition
description: Decomposes a decision-complete PRD into a clear, minimal set of user-meaningful features with explicit dependencies, producing a roadmap-ready structure without prioritization, scheduling, or implementation detail.
---

# Feature & Roadmap Decomposition

## What is it?

This skill converts a decision-complete Product Requirements Document (PRD) into a clean, reviewable feature list suitable for roadmap definition and issue creation.

It identifies what distinct features must exist to deliver the product's goals, while enforcing clear boundaries, independence, and explicit dependencies.

## Why use it?

- Transforms finalized PRDs into structured, roadmap-ready feature lists
- Enforces clear feature boundaries and explicit dependencies
- Provides a reviewable output for product and engineering stakeholders
- Creates a foundation for issue creation and planning workflows
- Maintains strict separation between features and implementation details

Use this skill when a PRD has been finalized, all critical ambiguities have been resolved, and you need to understand the full feature surface of the product before creating issues or plans.

## How to use it?

1. **Ensure the PRD is decision-complete**: All critical ambiguities must be resolved before using this skill
2. **Apply the skill to the PRD**: The skill will analyze the PRD and identify distinct features
3. **Review the feature list**: Verify that each feature has clear boundaries and explicit dependencies
4. **Use the output for roadmap planning**: The resulting feature list can be used directly for issue creation or planning workflows

**Do not use this skill to**:
- Write or modify a PRD
- Detect ambiguity
- Prioritize or schedule work
- Create GitHub issues
- Define tasks, stories, or UX flows

This skill does **not** decide priority, sequencing, ownership, or implementation—those decisions belong to the calling agent or workflow.

---

## What a Feature Is (Strict Definition)

A **feature** is:

- A **user-meaningful capability**
- With a **single primary intent**
- That delivers a **clear outcome**
- And can be described as something that could be “shipped” or “launched”

A feature must be explainable in **one sentence without using “and.”**

---

## End-to-End Flow Rule (Critical)

A feature **may** represent an **end-to-end flow** **only if all conditions below are met**:

1. **Single User Outcome**  
   The flow exists to achieve one primary user goal.

2. **Stable Boundaries**  
   The start and end of the flow are clearly defined and unlikely to change frequently.

3. **Conceptually Shippable**  
   The flow can be launched and reasoned about as a standalone capability.

4. **No Mixed Intents**  
   The flow does not bundle unrelated user goals or capabilities.

If an end-to-end flow hides multiple independent outcomes, it must be split into multiple features.

---

## What a Feature Is NOT

A feature is **not**:

- a task or checklist item
- a UI screen or page
- a backend component
- a technical refactor
- a simple sequence of steps with no independent value
- a bundle of unrelated capabilities

---

## Decomposition Principles

When decomposing a PRD into features, enforce the following principles.

### 1. Outcome-Based

Each feature must map directly to:

- a PRD goal
- a user or system outcome

If a feature does not clearly support a goal, it does not belong.

---

### 2. Single Responsibility

Each feature must do **one primary thing**.

If the description contains “and”, reconsider the boundary.

---

### 3. Independent Value

A feature should be:

- understandable in isolation
- valuable even if other features are delayed
- capable of being reasoned about independently

---

### 4. Explicit Dependencies

If a feature requires another feature to exist first:

- the dependency must be stated explicitly
- dependencies must be logical, not time-based

Avoid hidden or assumed ordering.

---

## Dependency Reasoning

Identify dependencies such as:

- foundational capabilities (e.g., authentication, configuration)
- shared system capabilities
- data model prerequisites
- irreversible ordering constraints

Dependencies should be:

- minimal
- explicit
- directional (A depends on B)

---

## Output Structure

The output of this skill should be **Markdown content only**, suitable for direct inclusion in a roadmap draft.

Recommended structure:

```markdown
# Feature Roadmap (Draft)

- **Feature Name**
  - Description: One-line description of the outcome.
  - Depends on: [Optional list of feature names]

- **Feature Name**
  - Description: ...
```

Descriptions should be concise, neutral, and outcome-focused.

---

## Important Boundaries

This skill **must not**:

- invent new requirements
- change PRD intent
- detect or resolve ambiguity
- prioritize features
- assign owners or timelines
- create issues or flags
- define tasks, stories, or implementation plans

All orchestration and execution decisions belong to the calling agent.

---

## Output Expectations

The output of this skill should be:

- deterministic for the same PRD
- minimal but complete
- easy to review by product and engineering stakeholders
- directly usable as input for issue creation or planning workflows
