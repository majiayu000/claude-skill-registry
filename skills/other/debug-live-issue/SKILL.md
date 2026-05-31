---
name: debug-live-issue
description: Debug production-like issues in this repository with disciplined evidence gathering. Use when fixing failing workflows, regressions, flaky behavior, or data inconsistencies across hooks, API, DB, websocket, and UI.
---

# Debug Live Issue

Use this workflow for incident-style debugging.

## Steps
- Capture symptom, expected behavior, and reproducible path.
- Isolate subsystem first: hook ingestion, API route, DB state, websocket, or UI rendering.
- Reproduce with minimal surface area.
- Prove root cause before changing code.
- Apply minimal fix and re-verify.

## Evidence standards
- Prefer direct logs, API responses, DB state checks, and deterministic repro steps.
- Avoid speculative fixes without root-cause evidence.
- If not fully reproducible, state uncertainty and strongest hypothesis.

## References
- Investigation template: `references/investigation-template.md`
