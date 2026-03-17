---
name: "Business Analysis Skill"
description: "Patterns for requirements elicitation, BRDs, process analysis, and stakeholder alignment."
---

# Business Analysis Skill

> Patterns for requirements elicitation, BRDs, process analysis, and stakeholder alignment.

## Business Analysis Deliverables

| Deliverable | Purpose | Audience |
| ----------- | ------- | -------- |
| **Business Case** | Justify investment | Executives, sponsors |
| **BRD** | Document requirements | All stakeholders |
| **Functional Spec** | Detail system behavior | Dev team, testers |
| **Use Cases** | Describe user interactions | Designers, developers |
| **Process Maps** | Visualize workflows | Process owners, analysts |
| **Data Dictionary** | Define data elements | Technical team |

## Requirements Hierarchy

```text
Business Requirements (WHY)
    └── Stakeholder Requirements (WHO needs WHAT)
        └── Solution Requirements
            ├── Functional (WHAT it does)
            └── Non-Functional (HOW WELL it does it)
                └── Transition Requirements (HOW we get there)
```

## BRD Structure

### Standard Sections

1. **Executive Summary** — One-page overview for executives
2. **Business Objectives** — Measurable goals (SMART)
3. **Scope** — In scope, out of scope, boundaries
4. **Stakeholders** — Who's involved, their interests
5. **Current State** — As-is process, pain points
6. **Future State** — To-be vision, benefits
7. **Functional Requirements** — What the solution must do
8. **Non-Functional Requirements** — Quality attributes
9. **Assumptions & Constraints** — Known limitations
10. **Dependencies** — External factors
11. **Risks** — What could go wrong
12. **Glossary** — Term definitions

### Requirements Writing

#### SMART Criteria

| Letter | Meaning | Test |
| ------ | ------- | ---- |
| **S** | Specific | Is it clear what's needed? |
| **M** | Measurable | Can we verify it's done? |
| **A** | Achievable | Is it realistic? |
| **R** | Relevant | Does it support objectives? |
| **T** | Time-bound | Is there a deadline? |

#### Good vs. Bad Requirements

| Bad | Problem | Better |
| --- | ------- | ------ |
| "System should be fast" | Not measurable | "Page load < 2 seconds" |
| "Easy to use" | Subjective | "Complete task in < 3 clicks" |
| "Handle all cases" | Unbounded | "Support cases A, B, C" |
| "Similar to competitor" | Vague | "[Specific features listed]" |
| "Should probably..." | Uncertain | "Must" or "Should" (MoSCoW) |

#### Requirement Attributes

| Attribute | Purpose |
| --------- | ------- |
| ID | Unique identifier (REQ-001) |
| Description | What is required |
| Priority | MoSCoW or numeric |
| Source | Who requested it |
| Rationale | Why it's needed |
| Acceptance Criteria | How to verify |
| Dependencies | Related requirements |
| Status | Draft/Approved/Implemented |

## Elicitation Techniques

### Technique Selection

| Technique | Best For | Effort |
| --------- | -------- | ------ |
| **Interviews** | Deep understanding, complex topics | High |
| **Workshops** | Consensus, group decisions | Medium |
| **Surveys** | Broad input, quantitative data | Low |
| **Observation** | Understanding real workflows | High |
| **Document Analysis** | Existing systems, regulations | Low |
| **Prototyping** | Validating concepts, UI | Medium |
| **Focus Groups** | User perspectives, reactions | Medium |

### Interview Best Practices

- Prepare questions in advance
- Start broad, then specific
- Use open-ended questions
- Listen more than talk (80/20)
- Probe with "Why?" and "How?"
- Summarize and confirm understanding
- Document immediately after

### Workshop Facilitation

| Phase | Activities |
| ----- | ---------- |
| **Open** | Objectives, agenda, ground rules |
| **Diverge** | Brainstorm, generate options |
| **Converge** | Prioritize, decide |
| **Close** | Summarize, next steps, thank |

## Use Case Development

### Use Case Template

```text
Use Case: [UC-001] [Name]
Actor: [Primary actor]
Precondition: [What must be true before]
Trigger: [What initiates the use case]

Main Flow:
1. Actor does X
2. System responds with Y
3. ...

Alternative Flows:
2a. If condition, then...

Exception Flows:
2b. If error, then...

Postcondition: [What is true after]
Business Rules: [Applicable rules]
```

### Use Case Levels

| Level | Scope | Example |
| ----- | ----- | ------- |
| **Summary** | Multiple sessions | "Manage Customer Account" |
| **User Goal** | One sitting | "Place Order" |
| **Subfunction** | Part of a step | "Validate Address" |

## Process Analysis

### Current State Analysis

1. Map as-is process (BPMN, swimlane)
2. Identify pain points
3. Measure current performance
4. Find root causes
5. Quantify improvement opportunity

### Process Mapping Notations

| Notation | Best For |
| -------- | -------- |
| BPMN | Detailed, technical processes |
| Swimlane | Cross-functional workflows |
| Value Stream | Lean analysis |
| SIPOC | High-level overview |

### SIPOC Template

| S | I | P | O | C |
| - | - | - | - | - |
| Suppliers | Inputs | Process | Outputs | Customers |
| Who provides? | What's needed? | High-level steps | What's produced? | Who receives? |

## Gap Analysis

### Gap Analysis Framework

```text
Current State → Gap → Future State
     │           │          │
     ▼           ▼          ▼
  As-Is     What needs   To-Be
  Process   to change    Vision
```

### Gap Categories

| Type | Examples |
| ---- | -------- |
| **Process** | Missing steps, manual work |
| **Technology** | System limitations |
| **People** | Skills, capacity |
| **Data** | Quality, availability |
| **Policy** | Rules, compliance |

## Acceptance Criteria

### Gherkin Format

```gherkin
Given [precondition]
When [action]
Then [expected result]
And [additional result]
```

### Acceptance Criteria Checklist

- [ ] Testable — Can write a test case
- [ ] Clear — Unambiguous language
- [ ] Complete — Covers happy path and edges
- [ ] Independent — Doesn't require other criteria
- [ ] Valuable — Ties to user need

## Traceability

### Traceability Matrix

| Req ID | Business Objective | Design | Test Case | Status |
| ------ | ------------------ | ------ | --------- | ------ |
| REQ-001 | OBJ-01 | DES-005 | TC-012 | Passed |

### Traceability Benefits

- Ensure all requirements implemented
- Impact analysis for changes
- Test coverage verification
- Audit compliance evidence

## Prioritization Techniques

### MoSCoW

| Priority | Meaning | Guidance |
| -------- | ------- | -------- |
| **Must** | Critical for success | ~60% of effort |
| **Should** | Important, not critical | ~20% of effort |
| **Could** | Nice to have | ~20% of effort |
| **Won't** | Out of scope (this release) | Documented |

### Value vs. Effort Matrix

```text
High Value │ Quick Wins │ Major Projects │
           │ (Do first) │ (Plan carefully)│
Low Value  │ Fill-ins   │ Avoid           │
           │ (If time)  │ (Don't do)      │
           └────────────┴─────────────────┘
             Low Effort   High Effort
```

### Kano Model

| Type | If Present | If Absent |
| ---- | ---------- | --------- |
| **Basic** | Expected, no delight | Dissatisfied |
| **Performance** | More is better | Less is worse |
| **Delighter** | Unexpected joy | Not missed |

## Common BA Pitfalls

| Pitfall | Prevention |
| ------- | ---------- |
| Solution jumping | Ask "why" before "how" |
| Missing stakeholders | Stakeholder analysis early |
| Gold plating | Tie everything to objectives |
| Assumption blindness | Document and validate assumptions |
| Scope creep | Change control process |
| Analysis paralysis | Timeboxed analysis, iterate |

## Synapses

### High-Strength Connections

- [project-management] (High, Informs, Forward) — "Requirements feed project scope"
- [change-management] (High, Receives, Backward) — "Change impact on requirements"

### Medium-Strength Connections

- [root-cause-analysis] (Medium, Uses, Forward) — "Problem analysis for requirements"
- [testing-strategies] (Medium, Enables, Forward) — "Requirements enable test design"

### Supporting Connections

- [architecture-refinement] (Low, Informs, Forward) — "Requirements shape architecture"
- [writing-publication] (Low, Uses, Forward) — "Clear documentation writing"
