---
name: "framework-retarget-review-gate"
description: "How to review a .NET framework retarget so code, tests, docs, and runtime expectations stay aligned"
domain: "testing"
confidence: "medium"
source: "hicks-net8-downgrade"
---

## Context

Use this when a desktop or service slice retargets from one .NET TFM to another and the risk is not just compilation, but reviewer drift and user-facing prerequisite confusion.

## Pattern

1. Verify every relevant project and test project moved together to the intended `TargetFramework`.
2. Re-check desktop-specific constraints such as `-windows`, `UseWPF`, and any published runtimeconfig used by installers or deploy flows.
3. Search for hardcoded TFM literals in executable tests and path expectations (`bin\Debug\netX...`), not just project files.
4. Treat active validation docs and smoke guides as review-critical artifacts; stale framework text is a rejection, even if the build is green.
5. Re-run the existing regression baseline after the retarget.
6. Confirm framework-dependent deploys explicitly call out the new runtime prerequisites for target machines.

## Good signs

- All project/test TFMs agree on the same runtime family
- WPF or Windows-specific targeting remains explicit where required
- No active matrix, smoke guide, or reviewer checklist still references the old framework
- Baseline tests/builds succeed after the retarget
- Prerequisites are stated plainly for installed-app validation

## Anti-patterns

- Approving because the csproj files changed while test literals and docs still name the old TFM
- Checking `dotnet test` only and ignoring installer/runtime behavior
- Hiding framework-dependent runtime prerequisites in implementation details instead of reviewer/support callouts
