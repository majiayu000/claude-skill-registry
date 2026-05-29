---
name: 52-execute-refactor-150
description: "[52] EXECUTE. Three-stage refactoring workflow: (1) iterative research of refactor/modularization options, (2) plan + risk/edge-case analysis + Scope150 validation, then implement with tests after user confirmation, and (3) apply Scout105 cleanup protocol. Use when asked to refactor, modularize, or restructure code safely."
---

# Execute-Refactor 150 Protocol

## Overview

Run in three stages:
1. Research refactor options (iterative, no code changes).
2. Plan + confirm + implement with tests and validation.
3. Apply Scout105 cleanup (objective, small, user-approved).

## Stage 1 — Research refactor options (iterative)

1. **Create or reuse investigation log** at `.temp/INVESTIGATION.md`.
   - If the file does not exist, create it and add the template below.
   - Keep all research notes in this file only (no scattered notes in chat).

2. **Define the core question** (the refactor goal).
   - Write a single sentence: “We need to refactor X to achieve Y.”
   - Example: “Refactor SermonCard to reduce duplication and isolate date logic.”

3. **Define scope (Scope150)**.
   - **Core (100%)**: list files and behaviors you will directly change.
   - **Boundary (50%)**: list callers, dependent modules, tests, configs, and data flow.
   - If unsure, add a “to verify” bullet and resolve it during observations.

4. **Perform observations (search/read) in ordered layers**.
   - **Interface layer**: find entry points (routes, public APIs, UI entry points).
   - **Domain layer**: identify entities, i18n keys, enums, types.
   - **Pattern layer**: locate hooks, services, clients, shared utilities.
   - **Usage layer**: trace imports and call sites.
   - For each layer, read the minimum number of files that explain the behavior.

5. **Record findings in the log with sources**.
   - Each fact must include a source (file path + line reference or command).
   - Separate facts from hypotheses. Do not mix them.

6. **Generate hypotheses and refactor options**.
   - For each option, note: goal, steps, benefits, risks, and test impact.
   - Prefer at least 2 options so tradeoffs are explicit.

7. **Decide if more research is needed**.
   - If user says “research more”, expand scope or inspect new files.
   - Update the log with new branches and continue Stage 1.

8. **Stop before implementation**.
   - End Stage 1 with: options summary, remaining unknowns, and a recommended path.

### Investigation log template

```
# Investigation Log: <short topic>

## Core question
- ...

## Scope
- Core (100%):
  - ...
- Boundary (50%):
  - ...

## Findings
- <fact> (source: file path / command)
  - Subfinding

## Hypotheses
- H1: ...
  - Prediction: ...
  - Test: ...
  - Status: pending/confirmed/rejected

## Refactor options
- Option A: ... (pros/cons)
- Option B: ... (pros/cons)

## Next branches
- ...
```

## Stage 2 — Plan, confirm, implement

1. **Write a refactor plan**.
   - Break into ordered steps with file-level granularity.
   - Include expected intermediate states (what should still pass after each step).

2. **List risks and edge cases**.
   - Identify behavior changes, API contract risks, and hidden coupling.
   - Explicitly note any breaking-change risk.

3. **Define a validation checklist**.
   - Tests to run (unit/integration).
   - Manual checks if needed (UI flows, API calls).
   - Expected outputs and what would indicate failure.

4. **Perform Scope150 validation planning**.
   - Core (100%): ensure each planned change has a test or validation step.
   - Boundary (50%): list all callers/integrations/tests to be checked.

5. **Ask for user confirmation before editing**.
   - Provide plan, risks, and validation checklist.
   - Do not edit until the user approves.

6. **Implement the refactor**.
   - Follow the plan in order.
   - Keep changes minimal and reversible.

7. **Add or update tests**.
   - Cover changed logic and any new boundaries.
   - Avoid brittle tests; prefer behavior-based assertions.

8. **Run validation**.
   - Execute all tests from the checklist.
   - Record results and fix failures before moving to Stage 3.

## Stage 3 — Scout105 cleanup protocol

Apply only **objective** cleanup after a Key Point (phase complete). Do not add features.

### Trigger (Key Point)
- Apply only after a milestone where the user would see complete value.
- Do not run per-file; run once per phase.

### Allowed cleanup categories (objective only)
- **Unused code**: unused imports/vars/fields (provable by grep/IDE).
- **Typos**: spelling errors in comments/strings (spellcheckable).
- **Formatting inconsistencies**: breaks the file’s own pattern.
- **Dead code**: commented debug lines or unreachable code.
- **Obviously wrong logic**: provably incorrect (duplicate checks, impossible types).

### Constraints
- Only in files already touched by the primary task.
- Remove garbage only; no new features or refactors.
- Each cleanup must take ≤ 30 seconds to verify + fix.
- Total cleanup time ≤ 5% of primary task time.
- Must be objectively measurable; if not measurable, skip.
- Require user approval before executing cleanup.

### Scout105 report (present to user)

```
✅ Key Point complete: <brief summary>

Scout105 opportunities:
- <file>: <item> (category, evidence)
- <file>: <item> (category, evidence)

Run Scout105 cleanup? [Yes / Skip / Selective]
```

### Execution
- If approved, apply all selected cleanups in batch.
- Run tests/build to validate no regression.
- If failures occur, revert or investigate causality before proceeding.

## Output expectations

- Stage 1: Provide refactor options + log path + remaining branches + recommended path.
- Stage 2: Provide plan, risks, validation checklist, and request confirmation.
- Stage 3: Provide Scout105 report, decision, and validation result.
