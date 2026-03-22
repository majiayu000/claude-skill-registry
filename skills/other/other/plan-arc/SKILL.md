---
name: plan-arc
description: Design the proposed architecture for a task before implementation planning. Use when user says "plan arc", "design architecture", "propose architecture", or wants to define the target system shape before making a plan.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Designing proposed architecture...'"
          once: true
---

# Architecture Design Skill

Design the proposed architecture for a task — what the system should look like when the work is done. Produces a standalone architecture document that requirements can validate against and implementation plans can build from.

## When to Use

- User says "plan arc", "design architecture", "propose architecture"
- User has a task or requirements and wants to define the target architecture before planning implementation
- Before `/make-plan` to establish the architectural vision
- Before or after `/make-req` to give requirements a concrete shape to validate against

## Core Principles

- **Design the target state.** The deliverable is a proposed architecture — what the system should look like after the task is complete. Current architecture is explored as input, not as the output.
- **Architecture is the shape, not the steps.** This skill defines what components exist, how they relate, and where boundaries fall. It does not define implementation order, test strategy, or migration steps — that's `/make-plan`.
- **Multiple lenses when warranted.** Different aspects of the task may need different architectural perspectives. Use as many lenses as the task demands — no more, no fewer.
- **Reviewable and refinable.** The output is a standalone document meant to be discussed, challenged, and revised before anyone starts planning implementation.

## Critical Constraints

**NEVER:**
- Modify any source code files
- Include implementation steps, migration strategies, or test plans
- Create files outside `temp/plan-arc/`
- Diagram systems unrelated to the task

**ALWAYS:**
- Use subagents for parallel exploration of the current codebase
- Ground the proposed design in understanding of what exists today
- LOAD the `/mermaid` skill before creating any diagram
- LOAD each `/arch-lens-*` skill before creating its diagram
- Write to `temp/plan-arc/` directory

---

## Workflow

### Step 1: Understand the Task

Read the task description, requirements document, or user-provided context. Identify:

- What the task needs to achieve
- What areas of the system are likely affected
- What architectural questions the design must answer

### Step 2: Explore the Current Architecture

Launch parallel Explore subagents to understand the systems the task will touch:

- **Component boundaries** — What modules, services, or packages exist in the affected area?
- **Relationships** — How do these components communicate, depend on, or reference each other?
- **Patterns and conventions** — What architectural patterns does the existing code follow?
- **Data** — What data flows through the affected area? Where is it stored, read, transformed?
- **Extension points** — Where does the current architecture anticipate change? Where is it rigid?

The number and focus of subagents depends on the task.

### Step 3: Design the Proposed Architecture

Based on the task goals and current system understanding, design the target architecture. Consider:

- What new components are needed?
- What existing components need to change?
- What can remain as-is?
- Where should boundaries fall?
- How should new components integrate with existing ones?
- What patterns from the existing codebase should the design follow or intentionally depart from?

This is the creative step. The design should be the right architecture for the task — not the easiest to implement, not the most conservative change.

### Step 4: Select Lenses and Create Diagrams

Choose the architecture lenses that best communicate the proposed design:

| If the design involves... | Consider Lens |
|---------------------------|---------------|
| Adding/modifying containers, services, or integrations | C4 Container |
| Changing workflow logic, state machines, or decision flow | Process Flow |
| Altering data storage, transformations, or information flow | Data Lineage |
| Restructuring modules, changing dependencies, or layering | Module Dependency |
| Adding/modifying parallel execution or thread handling | Concurrency |
| Changing error handling, retry logic, or recovery paths | Error/Resilience |
| Modifying repository patterns or data access | Repository Access |
| Changing CLI commands, config, or monitoring | Operational |
| Adding/modifying validation, trust boundaries, or isolation | Security |
| Changing build tools, test framework, or quality gates | Development |
| Affecting multiple user journeys or cross-component flows | Scenarios |
| Modifying state contracts, field lifecycles, or resume logic | State Lifecycle |
| Changing deployment topology or infrastructure | Deployment |

For each selected lens:

1. LOAD the corresponding `/arch-lens-*` skill using the Skill tool
2. Follow that skill's conventions for diagram structure and styling
3. Diagrams show the **proposed state** — annotate new components with `★` prefix and modified components with `●` prefix. Use `newComponent` class for new elements.

### Step 5: Write Output

Save to: `temp/plan-arc/arc_{topic}_{YYYY-MM-DD_HHMMSS}.md`

---

## Output Template

```markdown
# Proposed Architecture: {Task/Topic}

**Date:** {YYYY-MM-DD}
**Task:** {Brief description of the task or reference to requirements}

## Summary

{What this architecture proposes and why. What are the key design decisions? How does the proposed system differ from what exists today?}

## Current State

{Brief description of the relevant current architecture — enough context to understand what's changing and why. Not a full system map — just what the reader needs to evaluate the proposal.}

## Proposed Design

### {Lens Name} View

**Question:** {The primary question this lens answers}

{Mermaid diagram showing the proposed state, using ★ for new and ● for modified components}

**Design Rationale:**
- {Why this structure was chosen}
- {What alternatives were considered and why this is preferred}

---

{Repeat for each lens used}

---

## Changes from Current State

| Component | Change | Rationale |
|-----------|--------|-----------|
| {name} | New / Modified / Removed | {Why} |

## Architectural Decisions

{Key decisions embedded in this design and the reasoning behind them. These are the things a reviewer should challenge or confirm.}

## Open Questions

{Decisions that could go either way, areas needing input, or uncertainties that should be resolved before implementation planning.}
```

## Output Quality Checks

Before finalizing, verify:

- The proposed design addresses the task goals
- Every new component is integrated — nothing is introduced but left unconnected
- The design follows existing codebase patterns where appropriate and explicitly justifies departures
- Diagrams use arch-lens skill conventions with proper `★`/`●` annotations
- A reader could evaluate whether this is the right architecture without needing to see the codebase
- Open questions are genuine design decisions, not implementation details

## Related Skills

- **`/verify-proposed-diag`** — Verify the proposed architecture diagrams against the codebase. Run after `/plan-arc` to validate existing components, connection directionality, and integration points.
- **`/make-req`** — Decompose requirements before or after architecture design
- **`/make-plan`** — Create implementation plans from the proposed architecture
- **`/mermaid`** — MUST BE LOADED before creating any diagram
- **`/verify-diag`** — For verifying diagrams that document current state only (no proposed elements)
