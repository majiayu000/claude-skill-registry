---
name: powershell-7
description: 'PowerShell 7 best practices, performance patterns, and cross-platform development. Use when writing PowerShell scripts, modules, functions, or tests. Covers advanced functions, error handling, collections, security, module development, Pester testing, and PSScriptAnalyzer. Triggers on "PowerShell", "pwsh", "ps1", "Pester", "PSScriptAnalyzer", "PowerShell module".'
license: MIT
metadata:
  version: '1.0.0'
  last_updated: '2025-07-16'
---

# PowerShell 7 Skill Baseline

Project-agnostic PowerShell 7 patterns for reliable, performant, cross-platform scripts and modules. Optimized for AI-assisted code generation with progressive disclosure — core patterns inline, detailed references loaded on demand.

## When to Use This Skill

- Writing or reviewing PowerShell 7 functions, scripts, or modules
- Generating Pester 5+ tests for PowerShell code
- Optimizing performance (collections, strings, lookups)
- Building cross-platform PowerShell (Windows, Linux, macOS)
- Configuring PSScriptAnalyzer rules
- Migrating from Windows PowerShell 5.1 to PowerShell 7

## Bundled Resources

Load these on demand when deeper context is needed:

| Resource | Path | Use When |
|----------|------|----------|
| Performance benchmarks | `references/performance.md` | Optimizing collections, strings, objects, file I/O |
| Error handling tiers | `references/error-handling.md` | Implementing typed exceptions, resource cleanup |
| Cross-platform guide | `references/cross-platform.md` | Path handling, platform detection, OS differences |
| Module development | `references/module-development.md` | Creating manifests, loaders, publishing modules |
| Pester 5 testing | `references/testing.md` | Test structure, mocking, assertions, organization |
| Anti-patterns & migration | `references/anti-patterns.md` | Code review, 5.1→7 migration checklist |
| PSScriptAnalyzer config | `templates/PSScriptAnalyzerSettings.psd1` | Drop-in analyzer configuration |

---

## 1. Function Template (CRITICAL)

Every function **must** use `[CmdletBinding()]` — non-negotiable.

```powershell
function Get-ConfigData {
    [CmdletBinding()]
    [OutputType([pscustomobject])]
    param(
        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$Path,

        [Parameter()]
        [ValidateSet('JSON', 'YAML', 'PSD1')]
        [string]$Format = 'JSON'
    )

    process {
        try {
            if (-not (Test-Path -LiteralPath $Path)) {
                throw [System.IO.FileNotFoundException]::new(
                    "Configuration file not found: $Path"
                )
            }
            $content = Get-Content -LiteralPath $Path -Raw -ErrorAction Stop
            switch ($Format) {
                'JSON' { $content | ConvertFrom-Json }
                'PSD1' { Import-PowerShellDataFile -LiteralPath $Path }
            }
        }
        catch {
            $PSCmdlet.ThrowTerminatingError($PSItem)
        }
    }
}
```

### State-Changing (ShouldProcess)

```powershell
function Remove-CacheData {
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'High')]
    param(
        [Parameter(Mandatory)]
        [ValidateScript({ Test-Path $_ -PathType Container })]
        [string]$CachePath
    )

    process {
        if ($PSCmdlet.ShouldProcess($CachePath, 'Remove all cache files')) {
            Remove-Item -Path (Join-Path $CachePath '*') -Recurse -Force
        }
    }
}
```

### Pipeline (begin/process/end)

```powershell
function ConvertTo-NormalizedRecord {
    [CmdletBinding()]
    [OutputType([pscustomobject])]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [object]$InputObject,

        [ValidateNotNullOrEmpty()]
        [string]$Prefix = 'REC'
    )

    begin { $count = 0 }
    process {
        $count++
        [pscustomobject]@{
            Id    = '{0}-{1:D4}' -f $Prefix, $count
            Name  = $InputObject.Name
            Value = $InputObject.Value
        }
    }
    end { Write-Verbose "Converted $count records" }
}
```

### Key Rules

- Always `[CmdletBinding()]` — enables `-Verbose`, `-ErrorAction`, common parameters
- Always `[OutputType()]` — documents return type for callers and tooling
- Validate every parameter — `[ValidateNotNullOrEmpty()]`, `[ValidateSet()]`, `[ValidateRange()]`, `[ValidateScript()]`, `[ValidatePattern()]`
- Use `SupportsShouldProcess` for any function that modifies state
- Pass `-WhatIf:$WhatIfPreference` explicitly to called cmdlets

---

## 2. Error Handling (CRITICAL)

> **Full reference**: `references/error-handling.md` — typed exceptions, ErrorRecord construction, resource cleanup

### Essential Pattern (Every Function)

```powershell
process {
    try {
        $result = Get-Item -LiteralPath $ResourceId -ErrorAction Stop
        $result
    }
    catch {
        $PSCmdlet.ThrowTerminatingError($PSItem)
    }
}
```

### Typed Exceptions

```powershell
throw [System.IO.FileNotFoundException]::new("Config not found: $path")
throw [System.ArgumentException]::new("Invalid format: $format")

try { Get-Resource -ResourceId $id }
catch [System.IO.FileNotFoundException] { Write-Warning "Missing: $($PSItem.Exception.Message)" }
catch { Write-Error "Unexpected: $($PSItem.Exception.Message)" }
```

### Key Rules

- `-ErrorAction Stop` inside `try` — converts non-terminating to terminating
- `$PSCmdlet.ThrowTerminatingError($PSItem)` — error points at caller, not internals
- Bare `throw` re-throws preserving original stack trace
- Never empty catch blocks — at minimum log the error
- Include context: what failed, what value, what to do next

---

## 3. Performance Quick Reference (CRITICAL)

> **Full reference**: `references/performance.md` — complete benchmarks, file processing, additional tips

| Pattern | Fast | Avoid |
|---------|------|-------|
| Collections | `$r = foreach (...) { ... }` or `List<T>.Add()` | `+= @()` in loops |
| Strings | `-join` or `StringBuilder` | `+=` string concat in loops |
| Objects | `[pscustomobject]@{}` | `New-Object PSObject` |
| Lookups | Hashtable `$h[$key]` — O(1) | `Where-Object` per lookup — O(n) |
| Output suppress | `$null = expr` | `Out-Null` in loops |
| File read | `[IO.File]::ReadLines()` for large files | `Get-Content` line-by-line piped |

### Collections Benchmark

| Method | 10K items | 100K items |
|--------|-----------|------------|
| Direct loop assignment | 1x | 1x |
| `List<T>.Add()` | ~4x | ~124x |
| `+= operator` | ~15x | ~18,000x |

---

## 4. Data Structures (CRITICAL)

```powershell
# Arrays — guarantee array from pipeline
$results = @(Get-ChildItem -Path $dir -Filter '*.log')
[string[]]$names = 'Alice', 'Bob', 'Carol'

# Ordered hashtable
$config = [ordered]@{ Name = 'MyApp'; Version = '1.0.0'; Debug = $false }

# PSCustomObject — fastest creation, preserves property order
$record = [pscustomobject]@{ Id = 1; Name = 'Test'; Status = 'Active' }

# Check property existence (works even if value is $null)
if ($record.psobject.Properties.Match('Status').Count) { <# exists #> }
```

**Array Gotchas**: Out-of-bounds returns `$null` silently. Indexing `$null` throws `RuntimeException`. `-1` index gets last item. `$data[0..-1]` does NOT enumerate all items.

---

## 5. Cross-Platform (HIGH)

> **Full reference**: `references/cross-platform.md` — platform detection, differences table, removed aliases

```powershell
# ALWAYS: Join-Path for path construction
$configPath = Join-Path $PSScriptRoot 'config' | Join-Path -ChildPath 'settings.json'

# Platform-specific config
$configDir = if ($IsWindows) { Join-Path $env:APPDATA 'MyTool' }
             else { Join-Path $HOME '.config' 'mytool' }
```

**Key Rules**: Never hardcode `\` or `/`. Module names must match filename case on Linux/macOS. `SecureString` is NOT encrypted on non-Windows — use `SecretManagement`. Aliases `ls`, `cp`, `mv`, `rm` removed on non-Windows.

---

## 6. Security (HIGH)

```powershell
# PSCredential parameter (never hardcode secrets)
param([Parameter(Mandatory)] [PSCredential]$Credential)

# SecretManagement module
$apiKey = Get-Secret -Name 'ApiKey' -Vault 'MyVault'

# Use -LiteralPath for user-provided paths (prevents wildcard injection)
Get-Content -LiteralPath $userProvidedPath
```

**Key Rules**: Never `Invoke-Expression` with user input. Escape regex: `[regex]::Escape($userInput)`. Never interpolate user input into SQL. Use `[ValidateSet()]`, `[ValidateRange()]`, `[ValidateScript()]` on all parameters.

---

## 7. Strings, Control Flow & Pipeline (HIGH)

```powershell
# String interpolation (double quotes) vs literal (single quotes)
"Hello, $userName"                                    # Expands variable
'No $expansion here'                                  # Literal
"Count: $($processes.Count)"                          # Subexpression
'User {0} at {1:yyyy-MM-dd}' -f $name, (Get-Date)   # Format operator

# $null comparisons — ALWAYS $null on the left
if ($null -eq $value) { <# null #> }

# PS 7+ operators
$status = $isActive ? 'Active' : 'Inactive'           # Ternary
$value = $config.Setting ?? 'default'                  # Null-coalescing
$config.Timeout ??= 30                                 # Null-coalescing assignment

# Splatting — preferred for 3+ parameters
$params = @{ Path = $source; Destination = $dest; Force = $true }
Copy-Item @params

# Pipeline: pipe at end of line (never backtick continuation)
Get-Process |
    Where-Object CPU -GT 100 |
    Sort-Object CPU -Descending |
    Select-Object -First 10
```

---

## 8. Style & Conventions (MEDIUM)

| Element | Convention | Example |
|---------|-----------|---------|
| Functions | Verb-Noun (approved verbs) | `Get-UserProfile` |
| Parameters | PascalCase | `$OutputPath` |
| Local variables | camelCase | `$itemCount` |
| Script scope | `$script:PascalCase` | `$script:CacheData` |
| Constants | UPPER_SNAKE_CASE | `$MAX_RETRIES` |

**Formatting**: 4-space indent, OTBS braces, max 115 chars/line, UTF-8 with BOM.
**Output streams**: `Write-Verbose` (debug), `Write-Information` (info), `Write-Warning` (warn), `Write-Error` (error). Never `Write-Host` in module functions.
**Aliases**: Always full cmdlet names in scripts — `Get-ChildItem` not `gci`, `Where-Object` not `?`.

---

## 9. PSScriptAnalyzer (MEDIUM)

> **Ready-to-use config**: `templates/PSScriptAnalyzerSettings.psd1`

| Severity | Key Rules |
|----------|-----------|
| Error | `AvoidUsingPlainTextForPassword`, `UsePSCredentialType`, `AvoidConvertToSecureStringWithPlainText` |
| Warning | `AvoidUsingCmdletAliases`, `AvoidUsingWriteHost`, `AvoidUsingPositionalParameters`, `AvoidUsingInvokeExpression`, `AvoidUsingEmptyCatchBlock`, `UseApprovedVerbs`, `UseShouldProcessForStateChangingFunctions` |

---

## Decision Matrix

| Situation | Pattern | Priority |
|-----------|---------|----------|
| New function | `[CmdletBinding()]` + `[OutputType()]` + param validation | CRITICAL |
| Building a collection | `$r = foreach (...) { ... }` | CRITICAL |
| Error handling | `try { -ErrorAction Stop } catch { ThrowTerminatingError }` | CRITICAL |
| User-provided paths | `-LiteralPath` + `Join-Path` | CRITICAL |
| 3+ parameters | Splatting `@params` | HIGH |
| State-changing operation | `SupportsShouldProcess` | HIGH |
| Secrets/credentials | `[PSCredential]` or `SecretManagement` | HIGH |
| Cross-platform paths | `Join-Path` (never hardcode separators) | HIGH |
| String assembly in loops | `-join` or `StringBuilder` | HIGH |
| Creating test file | Mirror source path, Describe/Context/It | HIGH |

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `catch` block not triggered | Missing `-ErrorAction Stop` | Add `-ErrorAction Stop` to cmdlet in `try` |
| Module functions not exported | `FunctionsToExport = '*'` or missing | List functions explicitly in manifest |
| Test can't find function | Missing `BeforeAll { . script.ps1 }` | Dot-source the function file in `BeforeAll` |
| Path fails on Linux | Hardcoded `\` separator | Use `Join-Path` |
| `$result.Count` returns nothing | `$result` is scalar, not array | Wrap: `$result = @(...)` |
| Mock not intercepting calls | Function is in different module scope | Use `Mock -ModuleName ModuleName` |

---

## Related Skills

- **pester-test-runner** — Run, debug, and manage Pester tests
- **invoke-build** — Build task management with InvokeBuild
- **git-commit** — Conventional commit workflow

---

## References

### Microsoft Learn — Deep Dives

- [Arrays](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-arrays?view=powershell-7.5) | [Hashtables](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-hashtable?view=powershell-7.5) | [PSCustomObject](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-pscustomobject?view=powershell-7.5)
- [String Substitution](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-string-substitutions?view=powershell-7.5) | [Exceptions](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-exceptions?view=powershell-7.5) | [$null](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-null?view=powershell-7.5)
- [If Statement](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-if?view=powershell-7.5) | [Switch Statement](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-switch?view=powershell-7.5) | [ShouldProcess](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-shouldprocess?view=powershell-7.5)

### Microsoft Learn — Performance and Platform

- [Performance Considerations](https://learn.microsoft.com/en-us/powershell/scripting/dev-cross-plat/performance/script-authoring-considerations?view=powershell-7.5) | [Differences from Windows PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell?view=powershell-7.4)
- [Unix Support](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/unix-support?view=powershell-7.5) | [PSScriptAnalyzer Rules](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules-recommendations?view=ps-modules) | [Module Manifest Guide](https://learn.microsoft.com/en-us/powershell/scripting/developer/module/how-to-write-a-powershell-module-manifest?view=powershell-7.5)

### Community

- [PoshCode Practice and Style Guide](https://poshcode.gitbook.io/powershell-practice-and-style) | [PSScriptAnalyzer](https://github.com/PowerShell/PSScriptAnalyzer) | [Pester Documentation](https://pester.dev/docs/quick-start)
