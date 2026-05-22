---
name: qa-testing-mobile
description: Mobile app testing strategy and execution for iOS and Android. Cover device matrix, automation frameworks, performance, reliability, and release gates. Use when you need cross platform mobile QA plans or mobile testing automation guidance.
---

# QA Mobile Testing

## When to Use This Skill

Use this skill when you need to:

- Build a mobile test strategy for iOS, Android, or cross-platform apps.
- Create a device matrix based on usage data and risk tiers.
- Choose between automation frameworks (XCUITest, Espresso, Appium, Detox).
- Plan CI integration with device labs (Firebase Test Lab, BrowserStack, AWS Device Farm).
- Define release gates and store submission readiness.

## Scope

- Define mobile test strategy across iOS and Android.
- Plan device matrix, OS coverage, and risk tiers.
- Choose automation frameworks and CI setup.
- Address performance, network, and offline scenarios.
- Define release gates and store readiness checks.

## Ask For Inputs

- Platforms, supported OS versions, and device targets.
- App type (native, cross platform, webview).
- Critical user flows and risk areas.
- Distribution channels and release cadence.
- Existing test tooling, CI, and device lab access.

## Workflow

1. Define test scope and risk matrix.
2. Select device coverage by tier and usage data.
3. Choose automation stack (XCUITest, Espresso, Appium, Detox).
4. Build layered tests: unit, integration, UI, smoke.
5. Add network, offline, and battery impact checks.
6. Define build, signing, and store submission gates.
7. Set flake control and rerun policy.

## Outputs

- Mobile test strategy and device matrix.
- Automation plan and framework selection.
- Test case inventory with priorities.
- Release readiness checklist.
- CI pipeline and reporting plan.

## Quality Checks

- Keep UI tests focused on critical flows.
- Separate device specific bugs from logic regressions.
- Track flake rate and quarantine unstable tests.
- Verify permissions, notifications, and background behavior.

## Templates

- `templates/device-matrix.md` for OS and device coverage.
- `templates/mobile-test-plan.md` for test scope and automation.
- `templates/release-readiness-checklist.md` for release gates.

## Resources

- `resources/framework-comparison.md` for choosing between XCUITest, Espresso, Appium, and Detox.
- `resources/flake-management.md` for flake control guidance.

## Related Skills

- Use [qa-testing-ios](../qa-testing-ios/SKILL.md) for iOS specific depth.
- Use [qa-testing-playwright](../qa-testing-playwright/SKILL.md) for web and webview testing.
- Use [software-mobile](../software-mobile/SKILL.md) for mobile architecture guidance.
