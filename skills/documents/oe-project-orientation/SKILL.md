---
name: oe-project-orientation
description: Repo navigation and “where do I start?” guide for OpenEvent-AI. Use when an agent/dev is lost, needs an overview of the project or a subsystem, or needs pointers to the most important docs, entrypoints, scripts, and tests without rescanning the entire codebase.
---

# oe-project-orientation

## Start here (fast orientation)

1. Architecture + run instructions:
   - `README.md`

2. Workflow contracts + known regressions + playbooks:
   - `docs/guides/TEAM_GUIDE.md`

3. Refactor plans and pending cleanup:
   - `docs/internal/BACKEND_REFACTORING_PLAN_DEC_2025.md`
   - `docs/internal/BACKEND_REFACTORING_PLAN_DEC_2025_ADDENDUM.md`
   - `docs/internal/BACKEND_CODE_REVIEW_DEC_2025.md`

4. Test navigation:
   - `tests/TEST_INVENTORY.md`
   - `tests/TEST_MATRIX_detection_and_flow.md`

## Where to debug (by subsystem)

- **Backend router / orchestration:** `backend/workflow_email.py`
- **Steps 1–7 logic:** `backend/workflows/steps/step*/`
- **Q&A engine:** `backend/workflows/qna/`
- **LLM adapter & providers:** `backend/workflows/llm/` and `backend/llm/`
- **Backend API routes:** `backend/api/routes/`
- **Frontend UI:** `atelier-ai-frontend/app/page.tsx`

## Deterministic repro entrypoints (preferred for debugging)

- Dev server wrapper: `scripts/dev_server.sh`
- Site visit trace: `scripts/manual_ux_scenario_I.py` + `scripts/validate_manual_ux_run.py`
- Smoke intake routing: `scripts/manual_smoke_intake.py`

## If you’re still lost

Use the most specific skill that matches the task:
- E2E site visit: `oe-e2e-site-visit`
- Fallback/debug stubs: `oe-trace-and-fallback-triage`
- HIL/billing/deposit: `oe-hil-and-billing-triage`
- Refactors/types/LSP: `oe-lsp-pyright-refactor`
