---
name: "cross-layer-kickoff-review"
description: "How to gate a multi-agent kickoff batch before calling it a real vertical slice"
domain: "testing"
confidence: "high"
source: "hicks-phase0-1-review"
---

## Context

Use this when host, services, and web UI are being built in parallel and the team wants an honest readiness verdict instead of placeholder optimism.

## Pattern

1. Verify the toolchain first: if the solution does not build or tests cannot run, the batch is not review-complete.
2. Compare the host and Web UI message vocabulary directly: request names, response names, capability labels, and seeded constants must agree exactly.
3. Separate placeholder seams from integrated seams. A scaffold page or stub handler is useful, but it does not satisfy a vertical-slice success criterion.
4. Check the first failure contract, not just the happy path. Empty input, unsupported messages, and unplaced-reason codes should already be stable enough to assert against.
5. Trace each claimed success criterion to one real code path, not just prose or helper tests.

## Good signs

- One real request can leave the UI, cross the bridge, hit application logic, and return shaped data without a placeholder response.
- Seeded material/settings values match across host, services, and web contracts.
- Review evidence includes at least one runnable verification command, not just static inspection.

## Anti-patterns

- Declaring a vertical slice complete while file-open/import/nesting still return `not-ready`
- Letting host and UI invent different bridge names during parallel work
- Treating spec-helper tests as proof that the implemented seam already works
