---
name: feature-orchestrator
description: Generate the required feature plan file skeleton and enforce section outputs plus Touched YES/NO gates for Zeus projects. Use when starting any new feature, enhancement, or significant change in any project. Triggers on "new feature", "build", "implement", "add functionality", "create feature", "feature plan".
---

## UNIVERSAL HARD CONSTRAINTS (APPLIES TO EVERY ACTION)

DO NOT ASSUME. If you do not have explicit evidence, STOP and verify.
DO NOT LIE. Never fabricate file paths, data, responses, or outcomes.
DO NOT DECEIVE. Never claim something works without proof. Never hide uncertainty.

Before ANY action:
1. Verify the current state exists as you believe it does.
2. If uncertain, STOP and ask.
3. If you cannot verify, explicitly state what you cannot verify.

Violations of these constraints are unacceptable regardless of urgency.

---

# Feature Plan Orchestrator (Zeus)

## Output target
Write ONLY into: `/projects/{project_name}/FEATURE_PLAN.md`

## Rules
- No code changes in this step.
- Every section below MUST exist in the plan.
- Each section MUST include: `Touched: YES/NO` + a 1-2 sentence proof.
- If `Touched: YES`, include the required checklist items for that section.
- Align with Zeus SSoT and project structure.

## Required Plan Sections (in this exact order)
1. Feature Summary (3-5 bullets)
2. Ownership Decision (Zeus project template vs external repo)
3. Touchpoints Inventory (routes/handlers, types, auth path, tables/columns, schema changes YES/NO)
4. Department Assignments (which department leads each phase)
5. Agent Workflow Integration (handoffs + validation gates)
6. Auth & Permissions (MUST follow @auth-locked)
7. Supabase Access Pattern (MUST follow @supabase-patterns)
8. Schema Trace End-to-End (MUST follow @schema-trace)
9. Files to Read / Files to Edit
10. Routes Affected
11. Types Reused / Created
12. Tables Touched / Columns Touched
13. Backend Artifacts Staging (MUST follow @workflow-documentation and @quality-gate-management)
14. Tests & Commands
15. Risks / Open Questions
16. Checklist (initial draft - finalized in approval gate)

## Required Context Checks
- Confirm project folder exists under `/projects/{project_name}/`.
- Confirm project SSoT structure in `/projects/README.md`.
- Follow SSoT authority and CR rules in `/company/SSOT_CONSTITUTION.md`.

## Stop Conditions
STOP and escalate if:
- Project folder is missing or unknown.
- SSoT rules conflict with requested output.
- Required dependency skills are missing.
