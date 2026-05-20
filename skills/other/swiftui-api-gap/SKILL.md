---
name: swiftui-api-gap
description: Generate and maintain deterministic SwiftUI-vs-Raven API parity reports and automation. Use when users ask to audit missing SwiftUI components/APIs, refresh coverage reports, reduce report noise, tune matching logic (owner-qualified names, constructors, operators), or update the weekly GitHub Actions PR workflow that publishes Reports/swiftui-api-gap/gap_report.md.
---

# SwiftUI API Gap

## Overview

Use this skill to keep Raven's SwiftUI parity tracking deterministic, actionable, and automated.

Primary implementation files:
- `Scripts/swiftui_api_gap_report.py`
- `.github/workflows/swiftui-api-gap-report.yml`
- `Documentation/SwiftUI-API-Gap-Automation.md`

Primary artifact:
- `Reports/swiftui-api-gap/gap_report.md`

## Workflow

1. Run report generation.
```bash
Scripts/swiftui_api_gap_report.py --repo-root . --output-dir Reports/swiftui-api-gap
```

2. Validate outputs exist.
```bash
ls -lh Reports/swiftui-api-gap
```

3. Check report quality quickly.
- Confirm summary section has counts and coverage.
- Confirm named APIs are separate from operator-like overloads.
- Confirm constructor coverage is owner-qualified (`Type.init`) and not globally skipped.

4. If asked to improve actionability, prioritize:
- Owner-qualified matching for members (`Type.func`, `Type.var`, `Type.init`).
- Noise separation for operator-like signatures.
- Stable high-signal lists for components/modifiers.
- Clear markdown sections that humans can triage.

## Automation

Weekly workflow:
- `.github/workflows/swiftui-api-gap-report.yml`
- Runs Monday via cron.
- Uses macOS runner compatible with Swift/Xcode tooling.
- Uploads artifact bundle.
- Opens/updates PR with refreshed report.

When editing automation:
1. Keep `Reports/swiftui-api-gap/gap_report.md` in `add-paths` for PR commits.
2. Keep workflow `permissions` at least:
   - `contents: write`
   - `pull-requests: write`
3. Keep `workflow_dispatch` so maintainers can run immediately.

## Matching Rules

Use these rules unless user asks to change methodology:
- Source of truth: `swift-api-digester` against Apple `SwiftUI` module.
- Build SwiftUI inventory from digester output.
- Build Raven inventory from public declarations under `Sources/Raven/**/*.swift`.
- Match by owner-qualified member names when possible.
- Keep constructors scored by owner (`Type.init`) unless upgraded to full signature matching.
- Keep operator overloads summarized separately from named actionable APIs.

## Troubleshooting

- If skill tooling scripts fail with missing `yaml`, use repo venv:
```bash
venv/bin/python -m pip install pyyaml
```

- If report looks noisy, inspect:
  - `missing.operator_like` in `gap_report.json`
  - owner context fields in high-signal sections

- If workflow cannot be triggered remotely, ensure workflow file is committed to default branch first.
