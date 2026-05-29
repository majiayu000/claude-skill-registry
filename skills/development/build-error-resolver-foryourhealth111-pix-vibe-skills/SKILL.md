---
name: build-error-resolver
description: Compatibility alias for build-specific error resolution. Use this when VCO routes to build-error-resolver but the upstream agent is unavailable in the current runtime.
---

# build-error-resolver (Compatibility Alias)

## Purpose

Provide a stable local entrypoint for VCO `build-error-resolver` routes.
This skill preserves routing compatibility across environments where the
`everything-claude-code:build-error-resolver` agent may not be available.

## Resolution Order

1. Prefer `everything-claude-code:build-error-resolver` when available.
2. If unavailable, delegate to local `error-resolver` workflow.
3. If both are unavailable, use systematic-debugging for root-cause isolation.

## Minimal Workflow

1. Capture the exact failing command and full stderr/stdout.
2. Classify failure type:
   - dependency/setup mismatch
   - compile/type/lint failure
   - env/config mismatch
   - test/runtime failure
3. Apply smallest fix that addresses root cause.
4. Re-run the original failing command to verify.
5. Report evidence: command, output, and final status.
