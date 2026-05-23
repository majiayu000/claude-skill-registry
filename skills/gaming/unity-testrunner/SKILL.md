---
name: unity-testrunner
description: Unity Test Framework CLI automation and test writing patterns. Masters batchmode execution, NUnit assertions, EditMode/PlayMode testing, and TDD workflows. Use PROACTIVELY for test automation, CI/CD pipelines, or test-driven development in Unity.
requires:
  - csharp-plugin:csharp-code-style
---

# Unity TestRunner - Automated Testing for Unity

## Overview

Unity Test Framework provides NUnit-based testing with CLI automation for batch execution, CI/CD pipelines, and TDD workflows.

**Core Topics**:
- CLI batchmode test execution (EditMode/PlayMode)
- NUnit assertions and test attributes
- Test assembly configuration (asmdef)
- Result parsing and reporting
- CI/CD pipeline integration

**Foundation Required**: `csharp-plugin:csharp-code-style` (naming conventions, code organization)

**Optional Integrations**:
- `unity-vcontainer`: DI-based test mocking
- `unity-unitask`: Async test patterns
- `unity-async`: Coroutine testing utilities

**Learning Path**: Test basics → CLI automation → Advanced patterns → CI/CD integration

## Quick Start

### Basic Test Structure

```csharp
using NUnit.Framework;

[TestFixture]
public class PlayerServiceTests
{
    private PlayerService mPlayerService;

    [SetUp]
    public void SetUp()
    {
        mPlayerService = new PlayerService();
    }

    [Test]
    public void Initialize_WhenCalled_SetsHealthToMax()
    {
        // Arrange
        int expected = 100;

        // Act
        mPlayerService.Initialize();

        // Assert
        Assert.AreEqual(expected, mPlayerService.Health);
    }

    [TearDown]
    public void TearDown()
    {
        mPlayerService = null;
    }
}
```

### CLI Execution (EditMode)

```powershell
& "C:\Program Files\Unity\Hub\Editor\{VERSION}\Editor\Unity.exe" `
  -batchmode `
  -nographics `
  -projectPath "{PROJECT_PATH}" `
  -runTests `
  -testPlatform editmode `
  -testResults "{TEMP}\results.xml" `
  -logFile "{TEMP}\test.log" `
  -quit
```

### CLI Execution (PlayMode)

```powershell
& "C:\Program Files\Unity\Hub\Editor\{VERSION}\Editor\Unity.exe" `
  -batchmode `
  -projectPath "{PROJECT_PATH}" `
  -runTests `
  -testPlatform playmode `
  -testResults "{TEMP}\results.xml" `
  -logFile "{TEMP}\test.log" `
  -quit
```

Note: PlayMode cannot use `-nographics` (requires scene rendering)

## When to Use

### Trigger Conditions (Proactive)
- Test code (*Tests* path .cs files) created or modified
- TDD workflow in progress (test-first development)
- User explicitly requests "run tests", "execute tests"
- CI/CD pipeline configuration needed
- Test failure debugging required

### Non-Trigger Conditions
- General .cs file modifications without test context
- Configuration or asset file changes only
- Build or deployment tasks without test requirements

## Reference Documentation

### [CLI Automation](references/cli-automation.md)
Complete CLI reference and automation:
- Full CLI option reference table
- Unity Hub path detection (Windows/macOS)
- ProjectVersion.txt parsing
- Environment variable configuration
- CI/CD pipeline templates (GitHub Actions)
- Timeout and log management

### [Test Patterns](references/test-patterns.md)
NUnit patterns and best practices:
- NUnit attribute reference ([Test], [SetUp], [TestCase], etc.)
- EditMode test patterns (pure C#, ScriptableObject)
- PlayMode test patterns (MonoBehaviour, Scene loading)
- Async test patterns (UniTask, IEnumerator)
- Test fixture configuration (asmdef-based)
- Mocking strategies (interface-based)

### [Result Parsing](references/result-parsing.md)
Test result processing:
- NUnit XML result format structure
- PowerShell XML parsing snippets
- Result summary extraction
- Failed test detail extraction
- CI/CD reporting integration

## Key Principles

1. **EditMode First**: Use EditMode for pure logic tests (faster, no scene required)
2. **PlayMode for Integration**: Reserve PlayMode for MonoBehaviour and scene tests
3. **Isolate Dependencies**: Use interfaces for testable architecture
4. **Fast Feedback Loop**: Filter tests during development for quick iteration
5. **Automate in CI/CD**: Configure batchmode execution for continuous testing

## Common Patterns

### Test Filtering

```powershell
# Filter by test name (semicolon-separated)
-testFilter "LoginTest;AuthTest"

# Filter by regex pattern
-testFilter ".*Service.*"

# Filter by category
-testCategory "Unit;Integration"

# Filter by assembly
-assemblyNames "Game.Domain.Tests;Game.Service.Tests"
```

### Unity Version Detection

```powershell
# Parse ProjectVersion.txt
$versionFile = Get-Content "{PROJECT_PATH}/ProjectSettings/ProjectVersion.txt"
$version = ($versionFile | Select-String "m_EditorVersion: (.+)").Matches.Groups[1].Value

# Construct Unity Editor path
$unityExe = "C:\Program Files\Unity\Hub\Editor\$version\Editor\Unity.exe"
```

### Test Assembly Identification

```
Priority pattern for finding test assemblies:
1. {AssemblyName}.Tests.asmdef (same folder or Tests subfolder)
2. Tests/{AssemblyName}/*.asmdef
3. Assets/Tests/EditMode/*.asmdef (fallback)

Example:
  Changed: Assets/Scripts/Domain/LoginService.cs
    -> asmdef: Game.Domain.asmdef
    -> Tests: Game.Domain.Tests.asmdef
    -> Filter: -assemblyNames "Game.Domain.Tests"
```

## Exit Codes

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | All tests passed | Display summary |
| 2 | Test failures | Display failed test details |
| 1 | Other errors | Check log file for details |

## Result Summary Format

```
Unity Test Results (EditMode)
-----------------------------------
Passed: 15
Failed: 2
Skipped: 1
Duration: 3.45s

Failed Tests:
  1. LoginServiceTests.LoginWithInvalidCredentials_ThrowsException
     -> Expected: ArgumentException
     -> Actual: No exception thrown

  2. AuthTests.TokenExpiry_ShouldInvalidateSession
     -> Assert.AreEqual failed
     -> Expected: False, Actual: True
```

## Platform Considerations

### Windows
```powershell
$unityExe = "C:\Program Files\Unity\Hub\Editor\{VERSION}\Editor\Unity.exe"
```

### macOS
```bash
unityExe="/Applications/Unity/Hub/Editor/{VERSION}/Unity.app/Contents/MacOS/Unity"
```

### CI/CD Environment
```powershell
# Use environment variable for flexibility
$unityExe = $env:UNITY_EDITOR_PATH
if (-not $unityExe) {
    # Fallback to Unity Hub path
}
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Unity Editor path not found | Set `UNITY_EDITOR_PATH` environment variable |
| ProjectVersion.txt missing | Verify Unity project root location |
| Test timeout | Use `-playerHeartbeatTimeout` option (default: 600s) |
| License error | Verify Unity license activation |

## Integration with Other Skills

- **unity-vcontainer**: Configure DI mocks in test fixtures
- **unity-unitask**: Write async tests with UniTask assertions
- **unity-async**: Test coroutine-based logic
- **unity-performance**: Profile test execution performance
