---
name: running-tests
description: Use when asked to run tests in the dd-sdk-ios project — whether a full module suite, a specific test class, or a single test method. Use when choosing between make, xcodebuild, or Xcode MCP for running iOS/tvOS/visionOS tests.
---

# Running Tests in dd-sdk-ios

## Two Approaches

### 1. Makefile — CI workflows, full module suites

Use `make` to replicate CI exactly. Always prefer this for running a full module or all modules.

**Before running:** verify available simulators and pick an appropriate device name:
```bash
xcrun simctl list devices available | grep -E "iPhone|Apple TV"
```

| Goal | Command |
|------|---------|
| All iOS unit tests | `make test-ios-all` |
| One module | `make test-ios SCHEME="<Scheme>"` |
| One module with specific device | `make test-ios SCHEME="<Scheme>" DEVICE="<Device>"` |
| All tvOS unit tests | `make test-tvos-all` |
| UI / integration tests | `make ui-test TEST_PLAN="<Plan>"` |
| Session Replay snapshots | `make sr-snapshot-test` |

**Default devices** (authoritative values from Makefile):
```bash
grep "DEFAULT_" Makefile
```

Always pass `DEVICE=` explicitly if the default simulator is not installed locally. Check `xcrun simctl list devices available` first.

**Module scheme names:** Always read the `Makefile` to get the authoritative list — it changes as modules are added or renamed:
```bash
grep "test-ios-all" Makefile -A 20  # shows all iOS schemes used in CI
```

### 2. Xcode MCP — selective, fast, single test or class

Requires **Xcode 26.3+** with the Xcode MCP server enabled in Claude Code settings.

**Before using Xcode MCP**, verify the setup:
1. Check Xcode version: `xcodebuild -version`
   - If Xcode < 26.3 → ask the user to upgrade Xcode
   - If Xcode ≥ 26.3 → check that `XcodeListWindows` is available
2. If `XcodeListWindows` is unavailable → ask the user to enable the Xcode MCP server in Xcode settings

`RunSomeTests` is limited to targets in the **currently active Xcode scheme**. The MCP has no tool to switch schemes — that must be done manually in Xcode.

**Get the tabIdentifier** (identifies the open Xcode workspace window):
```
XcodeListWindows()  # → tabIdentifier e.g. "windowtab1"
```

**Check available targets first:**
```
GetTestList(tabIdentifier: <tabIdentifier>)
# → lists targets in the active scheme only
```

**If the test is in the active scheme**, run it directly:
```
RunSomeTests(
  tabIdentifier: <tabIdentifier>,
  tests: [{
    targetName: "<targetName from GetTestList>",
    testIdentifier: "<TestClass>/<testMethod>()"
  }]
)
```

**If the test is NOT in the active scheme**, use `xcodebuild -only-testing`:
```bash
xcodebuild test \
  -workspace Datadog.xcworkspace \
  -scheme "<Module> <Platform>" \
  -destination 'platform=<Platform> Simulator,name=<Device>' \
  -only-testing:<TargetName>/<TestClass>/<testMethod>
```

To find which module owns a test:
```
XcodeGrep(tabIdentifier: <tabIdentifier>, pattern: "func <testName>", outputMode: "filesWithMatches")
# path reveals the module: DatadogInternal/Tests/... → scheme "DatadogInternal iOS"
```

## Decision Guide

```
Need to run tests?
├── Full module or CI replication?
│   └── make test-ios SCHEME="<Module> iOS" DEVICE="<Device>"
└── Specific class or method?
    ├── Test is in the active Xcode scheme? (check GetTestList)
    │   └── RunSomeTests
    └── Test is in a different scheme?
        └── xcodebuild -only-testing (or ask user to switch scheme in Xcode)
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Assuming `RunSomeTests` works for any module | It only sees targets in the active Xcode scheme — MCP cannot switch schemes |
| Not knowing which scheme owns the test | Grep for the function — file path reveals the module |
| Running full module when only one test needed | Use `RunSomeTests` or `xcodebuild -only-testing` |
| Running integration tests under feature module scheme | Integration tests use target `DatadogIntegrationTests iOS/tvOS` |
