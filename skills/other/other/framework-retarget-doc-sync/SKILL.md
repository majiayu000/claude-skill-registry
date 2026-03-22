---
name: "framework-retarget-doc-sync"
description: "Keep active validation docs aligned with a framework retarget"
domain: "delivery"
confidence: "high"
source: "2026-03-15 net8 doc correction"
---

## Context

Use this when a project changes target frameworks or runtime prerequisites and reviewers rely on authored matrices, smoke guides, or release notes in addition to executable tests.

## Pattern

1. Verify the actual project TFMs from the active `.csproj` files and any runtimeconfig/publish artifacts.
2. Search active reviewer-facing docs for hardcoded framework/version/runtime literals.
3. Update only the live validation artifacts that drive current build, smoke, installer, or approval work.
4. Separate **SDK requirements for local build/test** from **runtime requirements for installed app validation**.
5. Do not churn append-only histories or archival logs just to normalize old literals.

## Why It Matters

Executable checks can be correct while human validation docs still point reviewers at the wrong framework. That creates false review failures and wastes correction cycles.

## PanelNester Example

- Project targets: `net8.0` / `net8.0-windows`
- Active doc fixes:
  - `tests\Phase0-1-Test-Matrix.md`
  - `.squad\smoke-test-guide.md`
- Runtime callout for MSI validation:
  - x64 `.NET 8 Desktop Runtime`
  - `Microsoft Edge WebView2 Runtime`
