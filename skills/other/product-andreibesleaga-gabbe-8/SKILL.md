---
name: req-elicitation
description: Structured requirements elicitation for new products or features. Derives complete, verifiable requirements from stakeholder goals using IEEE 29148, IREB, and EARS standards. Handles both greenfield products and additions to existing systems.
triggers: [elicit requirements, gather requirements, what are the requirements, new product requirements, user needs, stakeholder goals, write PRD, requirements from scratch]
context_cost: medium
---

# Requirements Elicitation Skill

## Goal

Produce a complete, high-quality set of requirements for a system or feature by
systematically working from stakeholder goals → use cases → functional requirements →
quality requirements → constraints. Output feeds directly into PRD_TEMPLATE.md and
EARS_REQUIREMENTS.md.

---

## When to Use

- **Scenario 1 (New Product)**: No existing requirements. Starting from user goals, business objectives, or a concept description.
- **Scenario 2 (New Feature)**: Requirements for a specific addition to an existing system (must align with existing constraints and architecture).

---

## Step 0 — Strategic Context (Optional)

```
Check for existing strategic documents in docs/strategic/ (e.g., BUSINESS_CASE.md, EMPATHY_MAP.md, PROBLEM_STATEMENT.md) created during Step 0.
If they exist, read them to understand the "Why" and "Who" before proceeding to stakeholder identification.
```

---

## Step 1 — Stakeholder Identification

```
For every system, find:

Direct users:    Who operates the system? (end user, admin, operator, API consumer)
Indirect users:  Who is affected by outputs? (manager, auditor, regulator, end customer)
System owners:   Who funds/maintains/is accountable for the system?
External systems: Other systems that interact (upstream, downstream, third-party)
Regulators:      Any compliance authority with requirements over this system?

Fill: templates/product/STAKEHOLDER_REGISTER_TEMPLATE.md

Key question per stakeholder: "What must the system do for you to consider it successful?"
```

---

## Step 2 — Goal Decomposition (WHY before WHAT)

```
Start with business goals, decompose to system goals, then to requirements:

Business goal → System goal → Feature → Requirement

Example:
  Business goal:  "Increase customer retention by 20%"
  System goal:    "Users can track their order status in real-time"
  Feature:        "Order tracking page"
  Requirements:   [WHEN order status changes, system SHALL notify user via email]
                  [WHEN user opens order page, system SHALL display current status]

Techniques:
  Goal-oriented:  i* (i-star) framework — identify softgoals and hardgoals
  Use-case-based: Use cases from actor-goal pairs
  Story-mapping:  User journey → activities → tasks → requirements

Decomposition test: "Could this goal be met by different features?" YES → it's a goal, not a requirement.
```

---

## Step 3 — Scope Boundary (What is OUT)

```
Before writing requirements, explicitly define scope:

In scope: [list features explicitly included]
Out of scope: [list things explicitly excluded — prevents scope creep]

Example out-of-scope items:
  - Mobile native application (web only in v1)
  - Third-party API integrations beyond [specific list]
  - Reporting/analytics features
  - Multi-language/i18n support

Boundary markers reduce ambiguity and prevent implicit requirements.
```

---

## Step 4 — Use Case / User Story Enumeration

```
For each actor-goal pair, write:

Use Case format (functional complexity):
  Name:       [verb + noun — "Place Order"]
  Actor:      [Authenticated Customer]
  Goal:       [Successfully complete a purchase]
  Trigger:    [Customer clicks "Checkout"]
  Main flow:  [numbered steps]
  Extensions: [alternative paths — failures, exceptions]
  Postcondition: [system state after success]

User Story format (agile/lightweight):
  As a [actor], I want to [action] so that [benefit].
  Acceptance Criteria (Given/When/Then):
    GIVEN [precondition]
    WHEN [action]
    THEN [expected outcome]
    AND [additional assertion]
```

---

## Step 5 — EARS Requirements (Formal Specification)

```
Convert use cases into EARS syntax. Cover all 5 EARS patterns:

Ubiquitous (always true — system invariants):
  "The [system] shall [capability/constraint]."
  Use for: security invariants, data invariants, business rules

Event-Driven (trigger → response):
  "WHEN [trigger event] the [system] shall [response]."
  Use for: user actions, external events, time-based triggers

State-Driven (condition that must hold):
  "WHILE [system is in state] the [system] shall [behavior]."
  Use for: operating modes, session states, system health states

Optional Feature (configurable capability):
  "WHERE [feature/configuration is active] the [system] shall [behavior]."
  Use for: multi-tenant variations, licensed features, environment differences

Unwanted Behavior (defensive requirements):
  "IF [unwanted condition occurs] THEN the [system] shall [protective response]."
  Use for: error handling, security violations, resource exhaustion

EARS Quality Test per requirement:
  ✓ Contains exactly one "shall"
  ✓ Subject is the system (not a person or process)
  ✓ Single behavior per requirement
  ✓ Measurable — can write a test that proves pass/fail
  ✓ Implementation-agnostic — no "using X technology"
```

---

## Step 6 — Quality Requirements (Non-Functional)

```
For each quality attribute, use Quality Attribute Scenario (QAS) format:
  Source:    [who/what stimulates]
  Stimulus:  [what happens]
  Environment: [under what conditions]
  Artifact:  [what part of system is stimulated]
  Response:  [what the system does]
  Measure:   [how we know the response is acceptable]

Key quality categories (ISO 25010):
  Performance efficiency:  Response time, throughput, resource utilization
  Reliability:             Availability, fault tolerance, recoverability
  Usability:               Learnability, accessibility, error prevention
  Security:                Confidentiality, integrity, non-repudiation, authentication
  Maintainability:         Modularity, reusability, modifiability, testability
  Portability:             Adaptability, installability, replaceability
  Compatibility:           Coexistence, interoperability

Fill: templates/architecture/QUALITY_ATTRIBUTES_TEMPLATE.md
```

---

## Step 7 — Constraints

```
Document ALL constraints — things the system MUST or MUST NOT do regardless of design:

Technical constraints:
  - Must integrate with [existing system] using [specific protocol]
  - Must operate on [specific platform/OS/runtime]
  - Must fit within [budget/resource limit]

Regulatory constraints:
  - Must comply with [GDPR/HIPAA/PCI-DSS/SOC2]
  - Data must remain in [geographic region]
  - Must meet [accessibility standard]

Business constraints:
  - Must be delivered by [date]
  - Must support [N] concurrent users from day one
  - Cannot replace [existing system] before [date]

Constraints are non-negotiable. Flag any constraint that seems unreasonable for human decision.
```

---

## Step 8 — Ambiguity Resolution

```
For every requirement, test for ambiguity signals:

Red flags:
  □ Subjective adjectives: "fast", "easy", "flexible", "robust", "user-friendly"
  □ Incomplete comparatives: "better than", "improved", "more secure"
  □ Vague frequency: "often", "frequently", "sometimes", "as needed"
  □ Undefined pronouns: "it", "they", "this" without clear referent
  □ Passive voice hiding actor: "data shall be validated" (by whom? when?)
  □ Options without criteria: "the system may also..." (when exactly?)

Replacement patterns:
  "fast" → "p99 response time < 500ms under 100 concurrent users"
  "user-friendly" → "a new user shall complete [task] in < 3 minutes without training"
  "secure" → list specific security controls (authentication, authorization, encryption)
  "highly available" → "99.9% uptime measured monthly, < 4.38 hours downtime/month"

Ask clarifying questions. Do NOT proceed with ambiguous requirements.
```

---

## Step 9 — Traceability Setup

```
Assign unique IDs to all requirements:
  Functional:    FR-NNN
  Non-Functional: NFR-NNN (or QR-NNN for quality requirements)
  Constraint:    CON-NNN

Create initial traceability matrix:
  Stakeholder → Business Goal → Use Case → FR-NNN

This matrix is used in req-review.skill to verify completeness.
```

---

## Output Format

```
Produce:
  1. docs/requirements/PRD.md (from templates/product/PRD_TEMPLATE.md)
  2. docs/requirements/EARS_REQUIREMENTS.md
     Format:
       ## Functional Requirements
       | ID | EARS Statement | Source (Use Case) | Priority |
       |FR-001| WHEN user submits login form... | UC-003 | MUST |

  3. docs/requirements/QUALITY_ATTRIBUTES.md (from templates/architecture/QUALITY_ATTRIBUTES_TEMPLATE.md)
  4. docs/stakeholders/STAKEHOLDER_REGISTER.md (from templates/product/STAKEHOLDER_REGISTER_TEMPLATE.md)

Priority levels (MoSCoW):
  MUST:   System cannot go live without this
  SHOULD: Expected but not blocking launch
  COULD:  Desirable if time/resources allow
  WONT:   Explicitly out of scope for this version
```

---

## Constraints

- Never skip stakeholder identification — hidden stakeholders = missed requirements
- Every FR must be traceable to a use case or user story
- Every QAS must have a measurable Response Measure — no "fast as possible"
- Ambiguous requirements must be resolved before writing EARS — never carry ambiguity forward
- Requirements must be implementation-agnostic — no technology mentions in FR/QR
- All MUST requirements must be testable — if you cannot write a test, the requirement is invalid
