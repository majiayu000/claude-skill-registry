---
name: sketch-release-ops
description: Release readiness and monitoring workflow for Sketch Magic. Use when preparing launch checklists, verifying telemetry, or validating health endpoints before a public release.
---

# Sketch Release Ops

## Overview
Provide a consistent launch checklist, telemetry expectations, and post-launch watchlist.

## Workflow
1. **Run release checklist** from `references/release-ops.md`.
2. **Verify telemetry** (`ENABLE_TELEMETRY` + `NEXT_PUBLIC_ENABLE_TELEMETRY`).
3. **Confirm health endpoints**: `/health` and `/api/health`.
4. **Run mobile smoke** on iOS + Android (if possible).
5. **Capture evidence**: logs, proof video, and QA screenshots.

## References
- `references/release-ops.md`
