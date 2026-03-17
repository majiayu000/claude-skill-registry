---
name: pester
description: PowerShell TDD testing framework guidance for Pester v5+. Use when writing, structuring, or debugging PowerShell unit tests; mocking cmdlets, native commands (bash, git, curl), or .NET types; isolating tests with TestDrive/TestRegistry; capturing output streams; generating code coverage or JUnit/NUnit reports for CI/CD; running parameterized or tagged tests; or troubleshooting Pester Discovery vs Run phase issues.
---

# Pester Unit Testing for PowerShell

Pester is PowerShell's ubiquitous test and mock framework. Pester 5+ uses a two-phase execution model (Discovery → Run) that requires specific patterns for reliable tests.

## TDD Cycle

1. **Red** – Write a failing test describing expected behavior
2. **Green** – Implement minimal code to pass
3. **Refactor** – Clean up while keeping tests green

## Test File Structure

Test files use `*.Tests.ps1` naming convention. Place alongside source files:

```
src/
├── Get-Widget.ps1
└── Get-Widget.Tests.ps1
```

### Basic Template

```powershell
BeforeAll {
    . $PSCommandPath.Replace('.Tests.ps1', '.ps1')
}

Describe 'Get-Widget' {
    Context 'when called with valid ID' {
        It 'returns widget object' {
            $result = Get-Widget -Id 42
            $result.Id | Should -Be 42
        }
    }

    Context 'when widget does not exist' {
        It 'throws not found error' {
            { Get-Widget -Id 9999 } | Should -Throw -ErrorId 'WidgetNotFound'
        }
    }
}
```

## Block Hierarchy

| Block | Purpose | Scope |
|-------|---------|-------|
| `Describe` | Top-level grouping (1 per function/feature) | Container |
| `Context` | Scenario grouping ("when X", "with Y") | Sub-container |
| `It` | Single test case with assertions | Test |
| `BeforeAll` | Run once before all tests in block | Setup |
| `BeforeEach` | Run before each `It` | Per-test setup |
| `AfterEach` | Run after each `It` (guaranteed) | Per-test cleanup |
| `AfterAll` | Run once after all tests (guaranteed) | Final cleanup |

## Discovery vs Run Phase (Critical)

Pester 5 executes in two phases:

1. **Discovery** – Scans to find all tests (does NOT run `It` blocks)
2. **Run** – Executes tests with setup/teardown

**Rule**: Put ALL code inside `It`, `BeforeAll`, `BeforeEach`, `AfterEach`, `AfterAll`, or `BeforeDiscovery`.

```powershell
# ❌ WRONG - runs during Discovery, $data is null in Run phase
$data = Get-ExpensiveData
Describe 'Tests' {
    It 'works' { $data | Should -Not -BeNull }  # FAILS!
}

# ✅ CORRECT - use BeforeAll
Describe 'Tests' {
    BeforeAll { $script:data = Get-ExpensiveData }
    It 'works' { $script:data | Should -Not -BeNull }
}
```

For dynamic test generation, use `BeforeDiscovery`:

```powershell
BeforeDiscovery {
    $testCases = @('file1.ps1', 'file2.ps1')
}

Describe 'Validate <_>' -ForEach $testCases {
    BeforeAll { $file = $_ }
    It 'has valid syntax' { ... }
}
```

## Mocking

Mock any PowerShell command within test scope:

```powershell
Describe 'Send-Report' {
    BeforeAll {
        Mock Send-MailMessage {}
        Mock Get-Date { return [DateTime]'2024-01-15' }
    }

    It 'sends email with correct subject' {
        Send-Report -Title 'Summary'
        Should -Invoke Send-MailMessage -Times 1 -ParameterFilter {
            $Subject -like '*Summary*'
        }
    }
}
```

### Parameter Filters

Create conditional mocks for different inputs:

```powershell
Mock Get-Service { @{ Status = 'Running' } } -ParameterFilter { $Name -eq 'BITS' }
Mock Get-Service { @{ Status = 'Stopped' } } -ParameterFilter { $Name -eq 'Spooler' }
Mock Get-Service { @{ Status = 'Unknown' } }  # Default fallback
```

### Mocking Native Commands (bash, git, curl)

Native commands work via `$args`:

```powershell
Describe 'Git Operations' {
    BeforeAll { Mock git { 'mocked-output' } }

    It 'calls git with correct args' {
        Invoke-GitPush -Branch 'main'
        Should -Invoke git -ParameterFilter {
            $args[0] -eq 'push' -and $args[1] -eq 'origin'
        }
    }
}
```

### Module Internals

Use `-ModuleName` for functions inside modules:

```powershell
Mock Get-InternalData { 'mocked' } -ModuleName MyModule
```

Use `InModuleScope` for private/non-exported functions:

```powershell
InModuleScope MyModule {
    Mock Write-Log {}
    Invoke-PrivateFunction
    Should -Invoke Write-Log
}
```

## Test Isolation

### TestDrive (Filesystem)

Temporary PSDrive auto-cleaned per block:

```powershell
Describe 'File Processing' {
    BeforeAll {
        Set-Content 'TestDrive:\config.json' -Value '{"key":"value"}'
    }

    It 'reads config' {
        $cfg = Get-Content 'TestDrive:\config.json' | ConvertFrom-Json
        $cfg.key | Should -Be 'value'
    }
}
```

Use `$TestDrive` for .NET APIs requiring full paths:
```powershell
$path = Join-Path $TestDrive 'file.txt'
[System.IO.File]::WriteAllText($path, 'content')
```

### TestRegistry (Windows)

Temporary registry hive:

```powershell
BeforeAll {
    New-Item -Path 'TestRegistry:\MyApp'
    New-ItemProperty -Path 'TestRegistry:\MyApp' -Name 'Setting' -Value 'Test'
}
```

### Environment Variables

Save and restore manually:

```powershell
BeforeEach {
    $script:oldEnv = $env:MY_VAR
    $env:MY_VAR = 'test-value'
}

AfterEach {
    $env:MY_VAR = $script:oldEnv
}
```

## Output Capture

### Stream Redirection

| Stream | Command | Capture |
|--------|---------|---------|
| 1 (Success) | Write-Output | Direct assignment |
| 2 (Error) | Write-Error | `2>&1` or `-ErrorVariable` |
| 3 (Warning) | Write-Warning | `3>&1` |
| 4 (Verbose) | Write-Verbose | `4>&1` with `-Verbose` |
| 6 (Information) | Write-Host | `6>&1` |

```powershell
It 'captures Write-Host' {
    $result = MyFunction 6>&1
    $result | Should -Contain 'expected message'
}
```

### ANSI Color Stripping

```powershell
function Remove-AnsiCodes {
    param([string]$Text)
    $Text -replace '\x1b\[[0-9;]*[a-zA-Z]', ''
}

$clean = Remove-AnsiCodes $coloredOutput
```

Or configure Pester: `$config.Output.RenderMode = 'Plaintext'`

## Parameterized Tests

Use `-ForEach` or `-TestCases`:

```powershell
Describe 'Add-Numbers' {
    It 'adds <a> + <b> = <expected>' -TestCases @(
        @{ a = 2; b = 3; expected = 5 }
        @{ a = -1; b = 1; expected = 0 }
    ) {
        Add-Numbers $a $b | Should -Be $expected
    }
}
```

## Running Specific Tests

### Tags

```powershell
It 'slow test' -Tag 'Integration', 'Slow' { ... }

# Run only tagged tests
Invoke-Pester -TagFilter 'Unit' -ExcludeTagFilter 'Slow'
```

### Name Filters

```powershell
Invoke-Pester -FullNameFilter '*Get-Widget*returns*'
```

### Skip

```powershell
It 'admin only' -Skip:(-not (Test-IsAdmin)) { ... }
```

## Code Coverage

```powershell
$config = New-PesterConfiguration
$config.CodeCoverage.Enabled = $true
$config.CodeCoverage.Path = './src'
$config.CodeCoverage.OutputFormat = 'JaCoCo'
$config.CodeCoverage.OutputPath = 'coverage.xml'
$config.CodeCoverage.CoveragePercentTarget = 80

Invoke-Pester -Configuration $config
```

## CI Reports (JUnit/NUnit)

```powershell
$config = New-PesterConfiguration
$config.TestResult.Enabled = $true
$config.TestResult.OutputFormat = 'JUnitXml'  # or NUnitXml
$config.TestResult.OutputPath = 'test-results.xml'
$config.Run.Exit = $true  # Exit code for CI

Invoke-Pester -Configuration $config
```

## Additional Resources

- [references/anti-patterns.md](references/anti-patterns.md) - Common mistakes and pitfalls with solutions
- [references/mocking-patterns.md](references/mocking-patterns.md) - Advanced mocking scenarios (APIs, databases, native commands)
- [references/ci-integration.md](references/ci-integration.md) - GitHub Actions, Azure DevOps, GitLab CI, Jenkins examples

## Common Anti-Patterns

See [references/anti-patterns.md](references/anti-patterns.md) for detailed examples.

**Quick checklist:**
- ❌ Code outside Pester blocks
- ❌ Tests depending on each other
- ❌ Using `foreach` instead of `-ForEach`
- ❌ Mocking the function under test
- ❌ Over-specifying mock interactions
- ❌ Global variables in tests

## Assertion Quick Reference

| Assertion | Description |
|-----------|-------------|
| `Should -Be` | Case-insensitive equality |
| `Should -BeExactly` | Case-sensitive equality |
| `Should -BeTrue` / `-BeFalse` | Boolean |
| `Should -BeNullOrEmpty` | Null/empty check |
| `Should -BeOfType` | Type checking |
| `Should -Contain` | Collection contains |
| `Should -Match` | Regex (case-insensitive) |
| `Should -BeLike` | Wildcard match |
| `Should -Throw` | Exception expected |
| `Should -Exist` | Path exists |
| `Should -HaveCount` | Collection count |
| `Should -Invoke` | Mock was called |

Full assertion list: `Get-ShouldOperator`
