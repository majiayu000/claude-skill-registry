---
name: analyze
description: Run code analyzers (unused packages, code quality, security). Use when user wants to analyze the codebase or runs /analyze.
allowed-tools: Bash, Read
---

# Code Analyzer

Run analysis tools on the codebase.

## Usage

```
/analyze              # Run all analyzers
/analyze packages     # Unused NuGet packages only
/analyze quality      # Code quality only
/analyze security     # Security vulnerabilities only
```

## Arguments

- `$ARGUMENTS` - Analyzer type to run
  - Empty or `all` - Run all analyzers
  - `packages` - Detect unused NuGet packages (dotnet-unused)
  - `quality` - Check code style and Roslyn warnings
  - `security` - Scan for known CVEs and deprecated packages

## Process

### Step 1: Ensure Tools Are Installed

Run `dotnet tool restore` if tools are not available.

### Step 2: Execute Analyzer(s)

Based on `$ARGUMENTS`:

| Argument | Script |
|----------|--------|
| (empty) / `all` | `./tools/analyzers/run-all.sh` |
| `packages` | `./tools/analyzers/unused-packages/analyze.sh` |
| `quality` | `./tools/analyzers/code-quality/analyze.sh` |
| `security` | `./tools/analyzers/security/analyze.sh` |

### Step 3: Report Results

Summarize findings:
- Number of issues found per category
- Actionable recommendations

## Output Format

```
=== Analysis Results ===

Unused Packages: X issues
  - ProjectName: PackageName

Code Quality: X warnings
  - File:Line - Warning description

Security: X vulnerabilities
  - PackageName - CVE-XXXX-XXXXX (severity)

Recommendations:
  1. Remove unused package X from project Y
  2. Fix warning Z in file W
```
