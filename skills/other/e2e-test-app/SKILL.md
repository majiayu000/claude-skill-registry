---
name: e2e-test-app
description: End-to-end test the mobile app using Maestro - includes smoke testing, full test suites, or targeted feature testing. Use when the user wants to smoke test, E2E test, run Maestro tests, test the app, verify critical paths, or check if the app works.
---

# E2E Test App

This skill provides comprehensive end-to-end testing for the mobile app using Maestro, supporting smoke tests, full regression suites, and targeted feature testing.

## Testing Strategies

### Smoke Test (Fast - ~5-10 minutes)

Quick verification that critical paths work:
- App launches without crashing
- User can log in
- Dashboard loads
- Navigation works
- Core features are accessible

**Use when:** Validating a build, quick sanity check, pre-release verification

### Regression Test (Complete - ~30-60 minutes)

Full test suite covering all features:
- All authentication flows
- All navigation paths
- All feature areas
- Edge cases and error handling

**Use when:** Major releases, significant changes, comprehensive validation

### Targeted Test (Custom - varies)

Test specific feature areas:
- Auth flows only
- Portfolio features only
- Contribution flows only
- Specific user journeys

**Use when:** Working on specific features, debugging issues, focused validation

## Quick Reference

**Most Common Commands:**

```bash
# Smoke test (quick validation)
maestro test --debug-output test/test-results --include-tags smoke maestro/

# Run specific failing test
maestro test --debug-output test/test-results maestro/flows/dashboard/SingleDefconDashboard.yml

# View current screen state
maestro hierarchy

# Open test artifacts
open test/test-results/.maestro/tests/$(ls -t test/test-results/.maestro/tests/ | head -1)/
```

## Prerequisites

Before running tests, ensure:

- Maestro CLI is installed (`brew tap mobile-dev-inc/tap && brew install maestro`)
- You're in the mobile app workspace
- iOS Simulator or Android Emulator is available (or physical device connected)

## Quick Start

### Smoke Test (Recommended for quick validation)

```bash
# iOS
npm run ios:release
maestro test --debug-output test/test-results --include-tags smoke maestro/

# Android
npm run android:release
maestro test --debug-output test/test-results --include-tags smoke maestro/
```

### Run All Tests (Full Regression)

```bash
# iOS
npm run ios:release
maestro test --debug-output test/test-results maestro/

# Android
npm run android:release
maestro test --debug-output test/test-results maestro/
```

### Run Targeted Tests

```bash
# Test specific feature area (add --debug-output for debugging)
maestro test --debug-output test/test-results maestro/flows/auth/        # Auth only
maestro test --debug-output test/test-results maestro/flows/dashboard/   # Dashboard only
maestro test --debug-output test/test-results maestro/flows/portfolio/   # Portfolio only
```

## Step-by-Step Workflow

### 1. Build the Release App

**iOS:**

```bash
npm run ios:release
```

This builds the iOS app in Release configuration.

**Android:**

```bash
npm run android:release
```

This builds the Android app in release variant.

### 2. Start Device (if needed)

**iOS Simulator:**

```bash
xcrun simctl boot "iPhone 16 Pro"  # or your preferred simulator
```

**Android Emulator:**

```bash
emulator -avd Pixel_8_API_34  # or your preferred AVD
```

### 3. Run All Maestro Tests

From the project root:

```bash
maestro test --debug-output test/test-results maestro/
```

This runs all flows in `maestro/flows/**` excluding flows tagged with:

- `ignore`
- `util`
- `singleSepIra`

The `--debug-output` flag captures screenshots, logs, and AI reports to `test/test-results/` for debugging.

### 4. Run Specific Test Suites

**Auth flows only:**

```bash
maestro test --debug-output test/test-results maestro/flows/auth/
```

**Dashboard flows only:**

```bash
maestro test --debug-output test/test-results maestro/flows/dashboard/
```

**Profile flows only:**

```bash
maestro test --debug-output test/test-results maestro/flows/profile/
```

**Portfolio flows only:**

```bash
maestro test --debug-output test/test-results maestro/flows/portfolio/
```

**Contribution flows only:**

```bash
maestro test --debug-output test/test-results maestro/flows/contribution/
```

**Onboarding flows only:**

```bash
maestro test --debug-output test/test-results maestro/flows/onboarding/
```

## Test Organization

Tests are organized by feature area:

- `maestro/flows/auth/` - Authentication and login flows
- `maestro/flows/dashboard/` - Dashboard and account views
- `maestro/flows/profile/` - Profile, settings, and statements
- `maestro/flows/portfolio/` - Portfolio management and changes
- `maestro/flows/contribution/` - Contribution changes and pay periods
- `maestro/flows/onboarding/` - New user onboarding flows
- `maestro/utils/` - Shared utility flows (not run directly)

## Common Options

### Run with Continuous Mode

Watch for changes and re-run tests:

```bash
maestro test --continuous maestro/
```

### Run with Device Selection

Specify a particular device:

```bash
maestro test --device "iPhone 16 Pro" maestro/
```

### Run with Tags

Include specific tagged flows:

```bash
maestro test --debug-output test/test-results --include-tags smoke maestro/
```

Exclude specific tagged flows:

```bash
maestro test --debug-output test/test-results --exclude-tags slow maestro/
```

### Generate Report

Generate JUnit XML report:

```bash
maestro test --format junit --output report.xml maestro/
```

## Troubleshooting

### Build Fails

If the release build fails:

1. Clean the build: `npm run nuke:ios` (iOS) or clean Android build folder
2. Update dependencies: `npm install && npm run pod-install` (iOS)
3. Rebuild: `npm run ios:release` or `npm run android:release`

### Maestro Can't Find App

If Maestro can't detect the app:

1. Ensure the app is installed on the device/simulator
2. Check that the app is running in Release mode
3. Verify the device is connected: `maestro test --device` lists devices

### Tests Fail

If tests fail unexpectedly:

1. Check if the app is in the correct state (logged out, correct environment)
2. Review the Maestro output for specific failure details
3. **Always run individual failing tests to isolate issues:**
   ```bash
   maestro test --debug-output test/test-results maestro/flows/dashboard/SingleDefconDashboard.yml
   ```
4. Review screenshots and AI reports from `test/test-results/`
5. Enable Maestro Studio for interactive debugging: `maestro studio`

See the **Reporting Test Results** section below for detailed analysis commands.

#### Debugging with Test Output Directory

For detailed debugging of failing tests, use the `--debug-output` flag to capture artifacts:

```bash
maestro test --debug-output test/test-results --include-tags smoke maestro/
```

This creates a test output directory (`test/test-results/` - already in `.gitignore`) containing:
- **AI analysis reports** - HTML reports with failure analysis (when available)
- **Command logs** - JSON files with all commands executed and their status
- **maestro.log** - Detailed execution logs
- **Screenshots** - Captured on failures (if available)

**Accessing test artifacts:**

1. Default location: `~/.maestro/tests/<datetime>/`
2. Custom location: `test/test-results/` (recommended, already gitignored)
3. View the most recent test:
   ```bash
   ls -lt test/test-results/.maestro/tests/ | head -5
   ```

4. Open all AI reports from latest test:
   ```bash
   open test/test-results/.maestro/tests/<timestamp>/ai-report-*.html
   ```

5. Open failure screenshots from latest test:
   ```bash
   open test/test-results/.maestro/tests/<timestamp>/screenshot-❌-*.png
   ```

6. Check command execution:
   ```bash
   cat test/test-results/.maestro/tests/<timestamp>/commands-(<FlowName>).json
   ```

**Useful debugging commands:**

```bash
# View current screen hierarchy
maestro hierarchy

# View logs from most recent test
cat test/test-results/.maestro/tests/$(ls -t test/test-results/.maestro/tests/ | head -1)/maestro.log

# Or from default location
cat ~/.maestro/tests/$(ls -t ~/.maestro/tests/ | head -1)/maestro.log
```

**Reference:** [Maestro Test Output Directory Documentation](https://docs.maestro.dev/cli/test-output-directory)

### Slow Tests

If tests are running slowly:

1. Use a faster simulator/emulator
2. Run specific test suites instead of all tests
3. Check for network latency issues
4. Ensure your machine has sufficient resources

## Platform-Specific Notes

### iOS

- Release builds are signed with development certificates by default
- If you encounter signing issues, check `ios/Guideline.xcworkspace` settings
- Simulator must be booted before running tests

### Android

- Release variant may require keystore configuration for some features
- Ensure USB debugging is enabled for physical devices
- Emulator should have sufficient RAM allocated (4GB+)

## Integration with CI/CD

This workflow can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Build Release
  run: npm run ios:release

- name: Run Maestro Tests
  run: maestro test maestro/
```

## Reporting Test Results

After running tests, always provide a clear summary using this format:

### Test Summary Format

When reporting test results to the user, use this template:

```
**[Test Type] Results:**

✅ **PASSED:** TestName1 (duration)
✅ **PASSED:** TestName2 (duration)
❌ **FAILED:** TestName3 (duration) - Failure reason

X/Y Tests Passed (percentage%)

**Test Artifacts:**
- 📊 **AI Reports:** Opened in browser / available in test/test-results/
- 📸 **Screenshots:** Opened (for failures) / available in test/test-results/
- 📝 **Logs:** Available in test/test-results/.maestro/tests/<timestamp>/
```

**Example Report:**

```
**Smoke Test Results:**

❌ **FAILED:** DashboardAccountsScreens (1m 6s) - "Balance" not visible
❌ **FAILED:** SingleDefconDashboard (59s) - "20\d{2} savings" not visible
❌ **FAILED:** portfolioMultipleAccounts (1m 3s) - "Change portfolio" not visible

0/3 Tests Passed (0%)

**Test Artifacts:**
- 📊 **AI Reports:** Opened in browser
- 📸 **Screenshots:** All 3 failure screenshots opened
- 📝 **Logs:** Available in test/test-results/.maestro/tests/2026-02-13_095538/

**Next Steps:**
Run individual failing tests to isolate issues:
```bash
maestro test --debug-output test/test-results maestro/flows/dashboard/SingleDefconDashboard.yml
```
```

### Running Individual Failing Tests

**IMPORTANT:** When reporting test failures, always include the command to run each failing test individually.

When tests fail, run them individually to isolate the issue:

```bash
# Run a specific failing test
maestro test --debug-output test/test-results maestro/flows/dashboard/SingleDefconDashboard.yml

# Run another failing test
maestro test --debug-output test/test-results maestro/flows/portfolio/portfolioMultipleAccounts.yml
```

**Example commands for common failing tests:**

```bash
# Dashboard tests
maestro test --debug-output test/test-results maestro/flows/dashboard/SingleDefconDashboard.yml
maestro test --debug-output test/test-results maestro/flows/dashboard/MultipleDefconDashboard.yml
maestro test --debug-output test/test-results maestro/flows/dashboard/DashboardAccountsScreens.yml

# Auth tests
maestro test --debug-output test/test-results maestro/flows/auth/LoginWithGustoWelcome.yml
maestro test --debug-output test/test-results maestro/flows/auth/forgotPassword.yml

# Portfolio tests
maestro test --debug-output test/test-results maestro/flows/portfolio/portfolioMultipleAccounts.yml
maestro test --debug-output test/test-results maestro/flows/portfolio/changePortfolioSingleDefcon.yml
```

### Analyzing Test Artifacts

After a test run, always check:

1. **Screenshots** - Visual state when test failed
   ```bash
   open test/test-results/.maestro/tests/$(ls -t test/test-results/.maestro/tests/ | head -1)/screenshot-❌-*.png
   ```

2. **AI Reports** - Automated analysis of failures
   ```bash
   open test/test-results/.maestro/tests/$(ls -t test/test-results/.maestro/tests/ | head -1)/ai-report-*.html
   ```

3. **Command Logs** - Step-by-step execution
   ```bash
   cat test/test-results/.maestro/tests/$(ls -t test/test-results/.maestro/tests/ | head -1)/commands-*.json | jq
   ```

4. **Maestro Logs** - Detailed debug output
   ```bash
   cat test/test-results/.maestro/tests/$(ls -t test/test-results/.maestro/tests/ | head -1)/maestro.log | grep -i error
   ```

## Related Commands

- `maestro studio` - Interactive test editor and debugger
- `maestro record` - Record user interactions as a flow
- `maestro download-samples` - Download sample flows
- `maestro hierarchy` - View current screen hierarchy
