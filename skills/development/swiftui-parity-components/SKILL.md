---
name: swiftui-parity-components
description: Implement and verify SwiftUI API parity for Raven UI components. Use when asked to audit missing or mismatched SwiftUI views/modifiers, add parity components, wire examples into `Examples/TodoApp`, validate rendering in a browser (including dark mode), and prepare branch/PR deliverables.
---

# SwiftUI Parity Components

Use this workflow to add high-signal SwiftUI parity components and prove they render correctly in Raven's browser demo.

## 1. Build a Deterministic Gap List

Run the parity report first to avoid guesswork.

```bash
Scripts/swiftui_api_gap_report.py --repo-root . --output-dir Reports/swiftui-api-gap
```

Review:
- `Reports/swiftui-api-gap/gap_report.md`
- `Reports/swiftui-api-gap/gap_report.json`

Select a small, focused set of missing component APIs (typically 2-4) that are actionable in Raven.

## 2. Confirm Existing Raven Coverage

Search Raven sources before coding:

```bash
rg "struct .*: View|public struct|public func|public var" Sources/Raven
```

Check for:
- Missing component types
- Signature mismatches (labels, defaults, generic constraints)
- Modifier behavior discrepancies
- Availability or actor-isolation mismatches

## 3. Implement Components and Runtime Wiring

Add/update APIs under `Sources/Raven/**` and keep behavior aligned with existing rendering architecture.

Guardrails:
- Follow Swift 6.2 concurrency-safe patterns (`@MainActor`, `@Sendable` closures where needed)
- Keep APIs source-compatible with SwiftUI intent where practical
- Reuse existing Raven patterns for VNode/DOM rendering and event plumbing
- Add succinct comments only where behavior is non-obvious

## 4. Add Demo Usage in TodoApp

Render each new parity component in `Examples/TodoApp` so browser validation is concrete.

Typical locations:
- `Examples/TodoApp/Sources/**`
- existing screens or a temporary parity preview section

Ensure new UI is visible without extra setup.

## 5. Build and Serve the WASM Example

Use the example directory to avoid unrelated workspace failures.

```bash
cd Examples/TodoApp
swift build --swift-sdk swift-6.2.3-RELEASE_wasm
swiftly run swift run raven dev --input Examples/TodoApp
```

If `swiftly` is unavailable, document the blocker and use the closest working local command.

## 6. Validate in Browser with Playwright (Light and Dark)

Use Playwright checks against the local dev URL:
- confirm page loads
- confirm each new component is visible and interactive as applicable
- capture dark mode verification (toggle app/theme control if present, otherwise emulate dark scheme)
- inspect console for runtime errors

Record what was validated and any limitations.

## 7. Catch Nearby Discrepancies

While touching related files, fix small SwiftUI parity inconsistencies discovered nearby (naming, signatures, defaults, obvious rendering bugs).

Do not broaden scope into unrelated refactors.

## 8. Branch and PR

Create a branch name prefixed with `codex/` that reflects added components.

Example:
- `codex/add-label-toggle-parity-components`

Then:
1. Commit focused changes.
2. Push branch.
3. Open PR with:
   - components added/fixed
   - TodoApp demo updates
   - build command used
   - browser validation summary (light + dark mode)
   - any known gaps/follow-ups

## Definition of Done

Consider the task complete only when all are true:
- Selected parity components are implemented or mismatches fixed
- TodoApp renders the new APIs in browser
- Validation covered light and dark mode
- No new console/runtime errors in tested path
- Branch and PR are created with reproducible notes
