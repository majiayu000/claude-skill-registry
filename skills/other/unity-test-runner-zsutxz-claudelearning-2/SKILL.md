---
name: unity-test-runner
description: Execute and analyze Unity Test Framework tests from the command line. This skill automates test execution for Unity projects by detecting the Unity Editor, configuring test parameters (EditMode/PlayMode), running tests via CLI, parsing XML results, and generating detailed failure reports. Use this when running Unity tests, validating game logic, or debugging test failures.
---

# Unity Test Runner

## Overview

This skill enables automated execution and analysis of Unity Test Framework tests directly from the command line. It handles the complete test workflow: detecting Unity Editor installations across platforms (Windows/macOS/Linux), configuring test parameters, executing tests in EditMode or PlayMode, parsing NUnit XML results, and generating detailed failure reports with actionable insights.

## When to Use This Skill

Use this skill when:
- Executing Unity Test Framework tests from command line
- Running PlayMode or EditMode tests for game logic validation
- Analyzing test failures and generating failure reports
- Integrating Unity tests into CI/CD pipelines
- Debugging test failures with detailed stack traces and file locations
- Validating Unity project changes before commits

**Example user requests:**
- "Run all Unity tests in my project"
- "Execute PlayMode tests and show me the results"
- "Run tests in the Combat category"
- "Check if my Unity tests are passing"
- "Run EditMode tests only"

## Workflow

Follow this workflow when the skill is invoked:

### 1. Detect Unity Editor Installation

Use the `find-unity-editor.js` script to automatically locate the Unity Editor:

```bash
node scripts/find-unity-editor.js --json
```

**Script behavior:**
- Scans platform-specific default installation paths
- Detects all installed Unity versions
- Returns the latest version by default
- Can target specific version with `--version <version>` flag

**Output:**
```json
{
  "found": true,
  "editorPath": "C:\\Program Files\\Unity\\Hub\\Editor\\2021.3.15f1\\Editor\\Unity.exe",
  "version": "2021.3.15f1",
  "platform": "win32",
  "allVersions": ["2021.3.15f1", "2020.3.30f1"]
}
```

**If multiple versions are found:**
1. Present all available versions to the user
2. Ask user to confirm which version to use
3. Or use the latest version by default

**If no Unity Editor is found:**
- Report error with searched paths
- Ask user to provide Unity Editor path manually
- Store the path for future use

### 2. Verify Unity Project Path

Confirm the current directory contains a valid Unity project using cross-platform checks:

```typescript
// Use Read tool to check for Unity project indicators
Read({ file_path: "ProjectSettings/ProjectVersion.txt" })

// Use Glob to verify Assets directory exists
Glob({ pattern: "Assets/*", path: "." })
```

**Validation steps:**
1. Verify `Assets/` directory exists
2. Verify `ProjectSettings/ProjectVersion.txt` exists
3. Read `ProjectVersion.txt` to get Unity version
4. Warn if Editor version doesn't match project version

**Example ProjectVersion.txt:**
```
m_EditorVersion: 2021.3.15f1
m_EditorVersionWithRevision: 2021.3.15f1 (e8e88743f9e5)
```

### 3. Configure Test Settings

Determine test execution parameters. Use `AskUserQuestion` tool if parameters are not specified:

**Required settings:**
- **Test Mode**: EditMode, PlayMode, or Both
- **Test Platform**: EditMode tests use "EditMode", PlayMode can specify platform (e.g., "StandaloneWindows64", "Android", "iOS")

**Optional settings:**
- **Test Categories**: Semicolon-separated list (e.g., "Combat;AI;Physics")
- **Test Filter**: Regex pattern or semicolon-separated test names
- **Results Output Path**: Default to `TestResults.xml` in project root

**Configuration example:**
```typescript
AskUserQuestion({
  questions: [{
    question: "Which test mode should be executed?",
    header: "Test Mode",
    multiSelect: false,
    options: [
      { label: "EditMode Only", description: "Fast unit tests without Play Mode" },
      { label: "PlayMode Only", description: "Full Unity engine tests" },
      { label: "Both Modes", description: "Run all tests (slower)" }
    ]
  }]
})
```

### 4. Execute Tests via Command Line

Build and execute the Unity command line test command:

**Command structure:**
```bash
<UnityEditorPath> -runTests -batchmode -projectPath <ProjectPath> \
  -testPlatform <EditMode|PlayMode> \
  -testResults <OutputPath> \
  [-testCategory <Categories>] \
  [-testFilter <Filter>] \
  -logFile -
```

**Example commands:**

**EditMode tests:**
```bash
"C:\Program Files\Unity\Hub\Editor\2021.3.15f1\Editor\Unity.exe" \
  -runTests -batchmode \
  -projectPath "D:\Projects\MyGame" \
  -testPlatform EditMode \
  -testResults "TestResults-EditMode.xml" \
  -logFile -
```

**PlayMode tests with category filter:**
```bash
"C:\Program Files\Unity\Hub\Editor\2021.3.15f1\Editor\Unity.exe" \
  -runTests -batchmode \
  -projectPath "D:\Projects\MyGame" \
  -testPlatform PlayMode \
  -testResults "TestResults-PlayMode.xml" \
  -testCategory "Combat;AI" \
  -logFile -
```

**Execution notes:**
- Use `Bash` tool with `run_in_background: true` for long-running tests
- Set timeout appropriately (default: 5-10 minutes, adjust based on test count)
- Monitor output for progress indicators
- Capture both stdout and stderr

**Example execution:**
```typescript
Bash({
  command: `"${unityPath}" -runTests -batchmode -projectPath "${projectPath}" -testPlatform EditMode -testResults "TestResults.xml" -logFile -`,
  description: "Execute Unity EditMode tests",
  timeout: 300000, // 5 minutes
  run_in_background: true
})
```

### 5. Parse Test Results

After tests complete, parse the NUnit XML results using `parse-test-results.js`:

```bash
node scripts/parse-test-results.js TestResults.xml --json
```

**Script output:**
```json
{
  "summary": {
    "total": 10,
    "passed": 7,
    "failed": 2,
    "skipped": 1,
    "duration": 12.345
  },
  "failures": [
    {
      "name": "TestPlayerTakeDamage",
      "fullName": "Tests.Combat.PlayerTests.TestPlayerTakeDamage",
      "message": "Expected: 90\n  But was: 100",
      "stackTrace": "at Tests.Combat.PlayerTests.TestPlayerTakeDamage () [0x00001] in Assets/Tests/Combat/PlayerTests.cs:42",
      "file": "Assets/Tests/Combat/PlayerTests.cs",
      "line": 42
    }
  ],
  "allTests": [...]
}
```

**Result analysis:**
1. Extract test summary statistics
2. Identify all failed tests
3. Extract file paths and line numbers from stack traces
4. Categorize failures by type (assertion, exception, timeout)

### 6. Analyze Test Failures

For each failed test, analyze the failure using `references/test-patterns.json`:

**Analysis steps:**

1. **Load test patterns database:**
```typescript
Read({ file_path: "references/test-patterns.json" })
```

2. **Match failure message against patterns:**
   - Assertion failures: `Expected: <X> But was: <Y>`
   - Null reference failures: `Expected: not null But was: <null>`
   - Timeout failures: `TimeoutException|Test exceeded time limit`
   - Threading errors: `Can't be called from.*main thread`
   - Object lifetime issues: `has been destroyed|MissingReferenceException`

3. **Determine failure category:**
   - ValueMismatch: Incorrect assertion value
   - NullValue: Unexpected null reference
   - Performance: Timeout or slow execution
   - TestSetup: Setup/TearDown failure
   - ObjectLifetime: Destroyed object access
   - Threading: Wrong thread execution

4. **Generate fix suggestions:**
   - Load common solutions from test-patterns.json
   - Match solutions to failure pattern
   - Provide concrete code examples

**Example failure analysis:**

```markdown
**Test**: Tests.Combat.PlayerTests.TestPlayerTakeDamage
**Location**: Assets/Tests/Combat/PlayerTests.cs:42
**Result**: FAILED

**Failure Message**:
Expected: 90
  But was: 100

**Analysis**:
- Category: ValueMismatch (Assertion Failure)
- Pattern: Expected/actual value mismatch
- Root Cause: Player health not decreasing after TakeDamage() call

**Possible Causes**:
1. TakeDamage() method not implemented correctly
2. Player health not initialized properly
3. Damage value passed incorrectly

**Suggested Solutions**:
1. Verify TakeDamage() implementation:
   ```csharp
   public void TakeDamage(int damage) {
       health -= damage; // Ensure this line exists
   }
   ```

2. Check test setup:
   ```csharp
   [SetUp]
   public void SetUp() {
       player = new Player();
       player.Health = 100; // Ensure proper initialization
   }
   ```

3. Verify test assertion:
   ```csharp
   player.TakeDamage(10);
   Assert.AreEqual(90, player.Health); // Expected: 90
   ```
```

### 7. Generate Test Report

Create a comprehensive test report for the user:

**Report structure:**

```markdown
# Unity Test Results

## Summary
- **Total Tests**: 10
- **✓ Passed**: 7 (70%)
- **✗ Failed**: 2 (20%)
- **⊘ Skipped**: 1 (10%)
- **Duration**: 12.35s

## Test Breakdown
- **EditMode Tests**: 5 passed, 1 failed
- **PlayMode Tests**: 2 passed, 1 failed

## Failed Tests

### 1. Tests.Combat.PlayerTests.TestPlayerTakeDamage
**Location**: Assets/Tests/Combat/PlayerTests.cs:42

**Failure**: Expected: 90, But was: 100

**Analysis**: Player health not decreasing after TakeDamage() call.

**Suggested Fix**: Verify TakeDamage() implementation decreases health correctly.

---

### 2. Tests.AI.EnemyTests.TestEnemyChasePlayer
**Location**: Assets/Tests/AI/EnemyTests.cs:67

**Failure**: TimeoutException - Test exceeded time limit (5s)

**Analysis**: Infinite loop or missing yield in coroutine test.

**Suggested Fix**: Add `[UnityTest]` attribute and use `yield return null` in test loop.

---

## Next Steps
1. Review failed test locations and fix implementation
2. Re-run tests after fixes by re-invoking the skill
3. Consider adding more assertions for edge cases
```

**Report delivery:**
- Present report in formatted Markdown
- Highlight critical failures
- Provide file:line references for quick navigation
- Offer to help fix specific failures if user requests

## Best Practices

When using this skill:

1. **Run EditMode tests first** - They're faster and catch basic logic errors
   - Reserve PlayMode tests for Unity-specific features
   - Use EditMode for pure C# logic and data structures

2. **Use test categories** - Filter tests for faster iteration
   - `-testCategory "Combat"` runs only Combat tests
   - Helpful during active development of specific features

3. **Monitor test duration** - Set appropriate timeouts
   - EditMode: 1-3 minutes typical
   - PlayMode: 5-15 minutes typical
   - Adjust timeout based on test count

4. **Check Unity version compatibility** - Ensure Editor matches project version
   - Mismatched versions may cause test failures
   - Test results may be inconsistent across versions

5. **Parse results immediately** - Don't wait for manual review
   - Automated parsing catches issues faster
   - Provides actionable file:line information

6. **Analyze failure patterns** - Look for common causes
   - Similar failures often indicate systemic issues
   - Fix root cause instead of individual symptoms

7. **Preserve test results** - Keep XML files for debugging
   - Results contain full stack traces
   - Useful for comparing test runs

8. **Handle long-running tests** - Use background execution
   - Monitor progress with `BashOutput` tool
   - Provide status updates to user

## Resources

### scripts/find-unity-editor.js

Cross-platform Unity Editor path detection script. Automatically scans default installation directories for Windows, macOS, and Linux, detects all installed Unity versions, and returns the latest version or a specific requested version.

**Usage:**
```bash
# Find latest Unity version
node scripts/find-unity-editor.js --json

# Find specific version
node scripts/find-unity-editor.js --version 2021.3.15f1 --json
```

**Output**: JSON with Unity Editor path, version, platform, and all available versions.

### scripts/parse-test-results.js

NUnit XML results parser for Unity Test Framework output. Extracts test statistics, failure details, stack traces, and file locations from XML results.

**Usage:**
```bash
# Parse test results with JSON output
node scripts/parse-test-results.js TestResults.xml --json

# Parse with formatted console output
node scripts/parse-test-results.js TestResults.xml
```

**Output**: JSON with test summary, failure details including file paths and line numbers, and full test list.

### references/test-patterns.json

Comprehensive database of Unity testing patterns, NUnit assertions, common failure patterns, and best practices. Includes:
- NUnit assertion reference (equality, collections, exceptions, Unity-specific)
- Common failure patterns with regex matching
- Failure categories and root cause analysis
- Solution templates with code examples
- EditMode vs PlayMode guidance
- Unity-specific testing patterns (coroutines, scenes, prefabs, physics)
- Testing best practices

**Usage**: Load this file when analyzing test failures to match failure messages against patterns and generate fix suggestions.
