---
name: "vertical-slice-contract-repair"
description: "How to rescue a cross-layer vertical slice when placeholders and contract drift have diverged"
domain: "architecture"
confidence: "high"
source: "ripley-phase0-1-revision"
---

## Context

Use this when a desktop host, service layer, and frontend were built in parallel, but the first integration review shows they are still speaking slightly different languages.

## Pattern

1. **Name one canonical vocabulary** for message types and failure codes before touching UI polish.
2. **Delete duplicate transport DTOs** when the domain request/response shapes already match the bridge payloads.
3. **Turn placeholders live in dependency order**: native host seam → service call → UI action → result rendering.
4. **Bound failure modes explicitly** so reviewers can gate on stable codes instead of prose (`empty-run`, `invalid-input`, etc.).
5. **Promote skipped tests into real tests** as soon as the seam exists; don’t leave “blocked” markers hanging after the code is live.
6. **Make the solution runnable for reviewers** by ensuring the real projects and test projects are included in the solution entry point.

## Good signs

- The same message names appear in host code, frontend code, and review notes.
- A single import → run → results path works without fake payloads.
- Reviewer-facing tests stop describing the future and start asserting the present.

## Anti-patterns

- Keeping transport-only DTO copies “just in case” when they already mirror domain models
- Fixing UI text while the host still returns `not-ready`
- Adding new Phase 2+ scope before the first vertical slice is actually runnable
