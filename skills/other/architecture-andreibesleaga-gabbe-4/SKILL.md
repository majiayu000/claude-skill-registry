---
name: legacy-modernization
description: Analyze, document, and modernize legacy systems (COBOL, Mainframe, Fortran).
context_cost: medium
---
# Legacy Modernization Skill

## Triggers
- legacy code
- cobol
- mainframe
- fortran
- ibm z
- jcl
- db2
- cics
- modernization
- rewrite
- migration

## Purpose
To respect the critical nature of legacy systems while safely guiding them toward modernization. **Rule #1: Do no harm.**

## Capabilities

### 1. Code Analysis (The Archaeologist)
-   **Explain Logic**: Translate COBOL/Fortran business logic into plain English or Pseudocode.
-   **Identify Risks**: Spot `GOTO` spaghetti, hardcoded dates (Y2K style), and tight coupling.
-   **Data Mapping**: Map VSAM/Copybooks to JSON/SQL schemas.

### 2. Modernization Patterns
-   **API Wrapping (The Facade)**: Create a REST/gRPC wrapper around the legacy core.
-   **Strangler Fig**: Incrementally replace functions with microservices.
-   **Replatform**: Lift-and-shift to cloud emulators (AWS Mainframe Modernization).

### 3. Testing Legacy
-   **Characterization Tests**: "Lock down" current behavior before changing ANYTHING.
-   **Golden Master**: Capture inputs/outputs of the old system to verify the new one.

## Instructions
1.  **Assume Importance**: If it's running, it's making money. Treat legacy code with reverence.
2.  **No Big Bang**: Never suggest a full rewrite from scratch unless the system is < 10k LOC.
3.  **Document First**: most legacy failures happen because nobody knows *what* the code does.

## Deliverables
-   `legacy-analysis.md`: Explanation of flow.
-   `wrapper-api.yaml`: OpenAPI spec for the legacy system.
-   `strangler-plan.md`: Step-by-step migration path.
