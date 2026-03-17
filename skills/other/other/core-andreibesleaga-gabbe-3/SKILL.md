---
name: system-lifecycle
description: Orchestrate the full SDLC from Requirement to Code to Test (Traceability).
context_cost: medium
---
# System Lifecycle Skill

## Triggers
- lifecycle
- traceability
- requirement
- golden thread
- definition of done
- verify requirements

## Purpose
To ensure every line of code has a reason (Requirement) and a verification method (Test).

## Capabilities

### 1. The Golden Thread (Traceability)
-   **Link**: `REQ-ID` -> `Design Element` -> `Code Component` -> `Test Case`.
-   **Gap Analysis**: Find requirements with no tests, or code with no requirements.

### 2. Definition of Done (DoD) Enforcement
-   **Checklist**:
    -   [ ] Implementation matches Spec?
    -   [ ] Tests pass?
    -   [ ] Documentation updated?
    -   [ ] Traceability Matrix updated?

### 3. Change Impact Analysis
-   **Query**: "If I change `UserAuth.ts`, what Requirements are affected?"
-   **Action**: Reverse trace from Code -> Req to find impact scope.

## Instructions
1.  **Always ID Requirements**: Use `REQ-001`, `REQ-002` formatting in PRDs.
2.  **Tag Tests**: Add `@req(REQ-001)` annotations to test functions/classes.
3.  **Maintain Matrix**: Update `TRACEABILITY_MATRIX.md` as you code.

## Deliverables
-   `TRACEABILITY_MATRIX.md`: The living map of the system.
-   `impact-analysis.md`: Report on proposed changes.
