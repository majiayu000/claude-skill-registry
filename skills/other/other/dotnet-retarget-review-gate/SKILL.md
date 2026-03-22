---
name: "dotnet-retarget-review-gate"
description: "How to gate a repo-wide .NET target framework retarget without missing hidden TFM dependencies"
domain: "testing"
confidence: "medium"
source: "hicks-net8-downgrade-gate"
---

## Context

Use this when a .NET solution changes target frameworks across app, tests, and packaging.

## Pattern

1. Enumerate every authored project that carries a TFM and write the exact expected replacement values, including `-windows` desktop variants.
2. Search authored tests/docs for hardcoded TFM strings and `bin\Debug\netX...` paths; move them with the project files or they become false failures and stale guidance. Treat acceptance matrices and review checklists as blocking artifacts when they restate framework expectations.
3. For WPF desktop apps, verify the retargeted desktop projects keep the Windows-specific TFM and `UseWPF=true`.
4. Re-run the full solution test baseline and any installer/package build that publishes from the app project.
5. If packaging is framework-dependent, call out the runtime prerequisite change explicitly. If the app depends on WebView2, keep that prerequisite in scope too.

## Good signs

- Every authored `netX` literal has a clear reason to stay or is updated.
- Desktop build, test, and publish still succeed on the retargeted Windows TFM.
- Reviewer evidence includes both regression results and packaging results.

## Anti-patterns

- Reviewing only csproj diffs and ignoring tests that hardcode the old output folder.
- Updating executable tests while leaving acceptance matrices/checklists on the old TFM, which makes the slice look green but leaves reviewers following stale guidance.
- Treating installer success as proof that target machines have the right runtime.
- Forgetting that WPF desktop projects need the Windows-specific target framework, not plain `net8.0`.
