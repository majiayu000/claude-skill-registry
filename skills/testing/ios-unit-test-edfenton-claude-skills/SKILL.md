---
name: ios-unit-test
description: Run iOS unit/UI tests, report results, and optionally fix failures.
argument-hint: "[--scheme <name>] [--project <path>] [--configuration NonProd|Prod] [--no-fix]"
allowed-tools: Bash, Read, Glob, Grep, Write
---

## Purpose

Run iOS tests, report failures with enough detail to debug, then (with approval) fix issues and re-run to confirm.

## Arguments

- `--scheme <name>` — Xcode scheme (inferred from xcodebuild -list if omitted)
- `--project <path>` — Path to .xcodeproj or .xcworkspace (auto-detected if omitted)
- `--configuration <config>` — Build configuration (default: NonProd)
- `--no-fix` — Report only, don't offer to fix

## Workflow

### 1. Run tests

```bash
xcodebuild \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -configuration NonProd \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro' \
  test
```

Use `xcodebuild -list` to discover schemes if not specified. Simulator names vary by Xcode version — use `xcrun simctl list devices available` to find available simulators.

**Note:** Tests use Swift Testing framework (`import Testing`, `@Test`, `#expect`), not XCTest.

### 2. Report results

Include:

- Pass/fail/skip counts
- Each failing test: target, file, test name, assertion/error message
- If test target won't build, include build errors

### 3–4. Approval gate, fix and confirm

See `/shared-review-workflow` for approval gate protocol, fix constraints, and severity definitions. Group iOS failures by area (view model, persistence, notifications, UI).

## Reference

For xcodebuild patterns and common fixes, see `reference/ios-unit-test-reference.md`
