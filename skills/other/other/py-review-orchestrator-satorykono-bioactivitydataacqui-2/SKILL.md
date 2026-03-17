---
name: py-review-orchestrator
description: Execute BioETL hierarchical code review orchestration (L1/L2/L3) across sectors S1-S8 with delegated sub-reviews, scoring, and consolidated reporting in reports/review/FINAL-REVIEW.md. Use when a full-project audit or broad multi-layer review is requested.
---

# py-review-orchestrator

## Objective
Run the role-specific workflow as defined in the py-review-orchestrator profile.

## Source Of Truth
- Primary profile: `../../agents/py-review-orchestrator.md`
- Team orchestration: `../../agents/ORCHESTRATION.md`
- Shared project context: `../../../.ai/memory/agent-memory.md`

## Workflow
1. Open and follow `../../agents/py-review-orchestrator.md`.
2. Execute hierarchical review orchestration (Wave 1, then Wave 2) and respect sector dependencies.
3. Aggregate sector reports into `reports/review/FINAL-REVIEW.md` with complete critical/high issue rollup.
4. Keep scoring and status thresholds aligned with the profile and BioETL rules.
