---
name: screen-time-api-engineer
description: iOS 16+ Screen Time engineering skill for FamilyControls, ManagedSettings, ManagedSettingsUI, ScreenTime, and DeviceActivity/DeviceActivityMonitor extension workflows. Use for app and website blocking, custom shields, shield action handling, schedule-based enforcement, onboarding authorization flows, usage analytics reports, entitlement setup, App Review readiness, debugging, and production hardening.
---

# Screen Time API Engineer

Use this skill to implement and harden Screen Time API apps with a docs-first evidence model.

## Rules
- Use this evidence order for decisions:
  1. Canonical Apple docs and WWDC
  2. Local SDK interfaces/headers
  3. Project-observed implementations (Project Alpha/Project Beta)
  4. Field notes (forums/medium)
- If sources conflict, prefer canonical + SDK behavior.
- Mark uncertain conclusions as inference and include a caveat.

## Quick Start Workflow
1. Identify user goal category.
2. Open matching references from `references/guides`.
3. Cross-check critical API claims in `references/evidence`.
4. If implementation quality or regressions matter, use `references/rundowns`.
5. Produce output with explicit source/confidence labeling.

## Goal to Reference Map
- **Entitlements, signing, distribution approval**:
  - `references/guides/02-authorization-setup.md`
  - `references/guides/19-release-and-app-review-checklist.md`
- **Family activity picker and token handling**:
  - `references/guides/03-familycontrols-selection-and-token-model.md`
  - `references/guides/04-displaying-activity-labels-and-real-app-icons.md`
- **Shield policy and store behavior**:
  - `references/guides/05-managedsettings-enforcement-patterns.md`
  - `references/guides/06-web-blocking-and-webdomain-policy.md`
- **Custom shield UI/action**:
  - `references/guides/07-managedsettingsui-custom-shield-systems.md`
  - `references/guides/08-shield-actions-and-response-strategies.md`
- **Scheduling and monitor callbacks**:
  - `references/guides/09-deviceactivity-scheduling-thresholds-and-errors.md`
  - `references/guides/10-deviceactivity-monitor-extension-playbook.md`
- **Usage analytics reporting**:
  - `references/guides/11-deviceactivity-report-analytics-architecture.md`
- **Web usage control/reporting via ScreenTime framework**:
  - `references/guides/12-screentime-framework-web-usage-reporting.md`
- **Onboarding and permission UX**:
  - `references/guides/13-onboarding-and-permission-ui-blueprints.md`
- **End-to-end implementation reference**:
  - `references/guides/14-app-and-website-blocking-reference-implementation.md`
- **Project deep dives and comparative hardening**:
  - `references/guides/15-project-alpha-implementation-analysis.md`
  - `references/guides/16-project-beta-implementation-analysis.md`
  - `references/rundowns/12-cross-project-rundown.md`
- **Bug prevention, testing, and preflight**:
  - `references/guides/17-hardening-checklist-bug-prevention.md`
  - `references/guides/18-testing-matrix-device-only-edge-cases.md`
  - `references/guides/21-preflight-rundown.md`

## Evidence Files (Use When Verifying API Contracts)
- `references/evidence/01-familycontrols-sdk-signatures.md`
- `references/evidence/02-managedsettings-sdk-signatures.md`
- `references/evidence/03-managedsettingsui-sdk-signatures.md`
- `references/evidence/04-deviceactivity-sdk-signatures.md`
- `references/evidence/05-deviceactivity-report-sdk-signatures.md`
- `references/evidence/06-screentime-framework-headers.md`
- `references/evidence/07-claim-reconciliation.md`
- `references/evidence/00-source-url-inventory.md`

## Output Contract
When using this skill for implementation guidance, include:
1. Chosen API path and why.
2. Risks/failure modes.
3. Validation checklist.
4. Source citations with confidence labels.

## Boundaries
- Do not infer private APIs or unsupported token conversion techniques.
- Do not claim behavior beyond canonical/SDK support without explicit caveats.
- Do not skip extension-signing parity checks when discussing release readiness.
