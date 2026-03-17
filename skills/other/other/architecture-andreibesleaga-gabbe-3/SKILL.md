---
name: arch-review
description: Systematic review of existing architecture using ATAM-lite methodology. Evaluates architectural fitness against quality attribute scenarios, identifies risks, sensitivity points, tradeoffs, and anti-patterns. Produces structured review report with findings and recommendations.
triggers: [review architecture, audit architecture, architecture analysis, architecture assessment, arch review, evaluate architecture, is the architecture good, architecture problems, existing architecture]
context_cost: high
---

# Architecture Review Skill

## Goal

Evaluate an existing architecture for fitness against its stated requirements,
identify risks and anti-patterns, and produce a structured review report with
concrete recommendations. Based on ATAM (Architecture Tradeoff Analysis Method)
adapted for single-agent use.

---

## When to Use

- **Scenario 2 (Review existing)**: Architecture exists — documented or inferred from code.
- Before major changes: "Is this architecture adequate for the new requirements?"
- After significant growth: "Is this architecture still appropriate?"
- Before technology migration: "What architectural problems must we solve?"
- Due diligence: "Is this architecture sound before we commit to it?"

---

## Step 1 — Understand the Architecture Inputs

```
Gather before starting the review:

Architectural artifacts (work with whatever exists):
  □ Architecture document, README, or description
  □ Diagrams (any level — C4, UML, whiteboard photo, etc.)
  □ Requirements, PRD, or feature descriptions
  □ Codebase structure (actual source of truth if docs are outdated)
  □ Deployment configuration (shows actual runtime structure)
  □ ADRs or documented decisions

If artifacts are sparse or missing:
  → Reverse-engineer the architecture from the codebase
  → Use tools: dependency graphs, import analysis, directory structure
  → Document what you find — the architecture review creates the documentation

Key questions to answer in this step:
  1. What business/user goals does this system serve?
  2. What is the system's domain and boundaries?
  3. What are the stated or implied quality requirements?
  4. What architectural style appears to be in use?
```

---

## Step 2 — Reconstruct Architecture Description

```
If no architecture documentation exists, create a description from code/config:

System Context:
  - What are the external actors (users, systems)?
  - What are the major integration points?
  Create: System Context diagram (C4 Level 1)

Component Inventory:
  - What are the major components/services/modules?
  - What does each one do?
  - How do they communicate?
  Create: Container/Component diagram

Data Flows:
  - Where does data enter the system?
  - How does it flow between components?
  - Where is it stored?

Interface Inventory:
  - What interfaces exist between components?
  - What protocols are used?
  - What contracts are enforced?

Fill: templates/architecture/ARCHITECTURE_VIEWS_TEMPLATE.md with the reconstructed architecture.
This becomes the baseline for the review.
```

---

## Step 3 — Quality Attribute Scenario Analysis (ATAM core)

```
Identify or derive Quality Attribute Scenarios (QAS):
  Source: PRD, SPEC, stakeholder interviews, SLOs, implicit system behavior

For each QAS, evaluate: does the architecture satisfy it?

Evaluation framework:
  SATISFIED: Architecture demonstrably meets this QAS
  PARTIALLY: Architecture meets it under some conditions but not all
  AT RISK: Architecture may not meet this under stress/failure conditions
  VIOLATED: Architecture structurally cannot meet this QAS

Example QAS evaluation:
  QAS: "WHEN 10,000 concurrent users access the search feature,
        the system SHALL return results in < 2 seconds."
  Evaluation: AT RISK — current architecture uses synchronous database queries
              without caching. Under 10k users this will likely exceed 2s.
  Evidence: [describe the structural reason]
  Mitigation: [what architectural change would address this]
```

---

## Step 4 — Identify Architecture Smells

```
Check for common architecture anti-patterns:

Structural smells:
  □ God Component: one component with too many responsibilities
    Signs: > 30% of all code in one module, imports from everywhere
  □ Inappropriate Intimacy: components know too much about each other's internals
    Signs: direct access to internal data structures, bypass of interfaces
  □ Cyclic Dependencies: Component A → B → C → A
    Signs: circular import graphs, cannot test one without the other
  □ Bottleneck Component: single component that all others depend on
    Signs: high afferent coupling (many components depend on this one)
  □ Scattered Functionality: one feature spread across many unrelated components
    Signs: a single user action triggers changes in 10+ components
  □ Hidden Coupling: components appear independent but share implicit state
    Signs: shared mutable global state, shared database tables with mixed access

Layering smells:
  □ Layer Skipping: presentation layer directly accessing data layer
  □ Layer Inversion: inner layer (domain) importing outer layer (infrastructure)
  □ Fat Layer: all logic in one layer (fat controller, fat database)

Deployment smells:
  □ Deployment Monolith: one deployment unit but logically many services
  □ Chatty Services: services making many fine-grained calls to each other
  □ Data Coupling: services sharing the same database tables

Communication smells:
  □ Synchronous Overuse: everything synchronous even where async is needed
  □ Missing Circuit Breakers: no fault isolation for external dependencies
  □ Implicit Contracts: components communicate without defined interfaces
```

---

## Step 5 — ATAM Analysis: Sensitivity Points and Tradeoffs

```
Sensitivity Point: a design decision that has high leverage over a quality attribute.
  "If we change X, quality attribute Y changes significantly."
  Example: "The synchronous API call chain is a sensitivity point for latency."

Tradeoff Point: a design decision that affects two quality attributes in opposing directions.
  "Changing X improves quality attribute A but degrades quality attribute B."
  Example: "Adding encryption improves security but degrades performance."

Risk: an architectural decision that may lead to a quality attribute not being met.
  "The current design is at risk of not meeting the 99.9% availability requirement
   because there is a single point of failure in the message queue."

Non-Risk: a well-founded decision where the reasoning is sound.
  "The synchronous authentication check is a non-risk because it adds < 10ms
   latency and eliminates the complexity of async session management."

Document all four in templates/architecture/ARCHITECTURE_REVIEW_TEMPLATE.md
```

---

## Step 6 — Architecture Fitness Functions

```
Fitness functions: automated or manual checks that verify the architecture
is behaving as intended.

Examples:
  Dependency fitness: "No module in presentation/ imports from database/"
  Coverage fitness:   "Test coverage never drops below 96%"
  Complexity fitness: "No function exceeds cyclomatic complexity of 10"
  Performance fitness:"p99 response time < 500ms measured in CI"
  Availability fitness:"Error rate < 0.1% measured over 1-hour window"

For each identified risk, define a fitness function that would detect the risk
if it materializes.

Categorize:
  Existing (currently measured): [list]
  Missing but needed:            [list — these are recommendations]
```

---

## Step 7 — Recommendations

```
For each finding, provide a concrete recommendation:

Structure recommendations by priority:
  CRITICAL: Architecture cannot meet stated goals — must fix before launch
  HIGH:     Architecture will degrade over time or cause significant problems
  MEDIUM:   Architecture has smells that increase maintenance cost and risk
  LOW:      Improvement opportunities that would reduce complexity

Recommendation format:
  Finding: [description of the problem]
  Severity: CRITICAL / HIGH / MEDIUM / LOW
  Evidence: [where in the architecture this is visible]
  Risk: [what will happen if not addressed]
  Recommendation: [specific architectural change]
  Effort: [rough estimate: hours / days / weeks / sprint]
  ADR Needed: YES/NO

For CRITICAL recommendations: propose concrete migration path (not just "refactor it")
```

---

## Output Format

Fill `templates/architecture/ARCHITECTURE_REVIEW_TEMPLATE.md`:

```markdown
# Architecture Review Report

**System**: [system name]
**Review Date**: [YYYY-MM-DD]
**Architecture Version/Commit**: [reference]
**Reviewer**: [agent/human]

## Executive Summary
Architecture fitness: SOUND / AT RISK / INADEQUATE
[3-5 sentence summary]

## Quality Attribute Assessment
| QAS ID | Stimulus | Quality Attr | Verdict | Evidence |
|--------|----------|--------------|---------|----------|
| QAS-001 | ... | Performance | AT RISK | [reason] |

## Architecture Smells Found
| Smell | Location | Severity | Recommendation |

## Sensitivity Points
[Design decisions with high leverage over quality attributes]

## Tradeoff Points
[Design decisions balancing competing quality attributes]

## Risks
[Decisions that may lead to quality attribute violations]

## Fitness Functions
| Fitness Function | Status | Tool/Method |
|-----------------|--------|-------------|
| [name] | EXISTING/MISSING | [how to measure] |

## Recommendations
| Priority | Finding | Recommendation | Effort |

## Architecture Diagram (as-found)
[Diagrams created during review]
```

---

## Constraints

- Review the architecture AS IT EXISTS, not as it was intended to be
- If code contradicts documentation, the code is the truth
- Every recommendation must include a migration path (not just identification of a problem)
- CRITICAL findings must be presented to human before the review is complete
- Do not redesign the entire system in a review — focus on targeted improvements
- Performance and reliability risks require evidence from load characteristics, not just structural analysis
