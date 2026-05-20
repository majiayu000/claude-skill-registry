---
version: 1.2.0
name: dev-verification-backend
description: >
  Post-change verification for C#/.NET backend code — build, Roslyn analyzers,
  dotnet format, xUnit tests with coverage, NuGet vulnerability scan, and diff review.
  Invoked via /dev-verify (unified entry point) — not directly.
disable-model-invocation: true
user-invocable: false
argument-hint: "[--quick | --full | --fix]"
---

# Verification Loop — Backend (.NET)

Run a comprehensive quality check on C#/.NET code after changes.

> **Stack:** C#/.NET (ASP.NET Core, EF Core)

## When to Use

- After completing a feature or significant backend code change
- Before creating a PR
- After refactoring services, repositories, or API endpoints
- When you want to ensure quality gates pass

## Verification Phases

### Phase 1: Build

```bash
dotnet build --no-restore /bl:build.binlog 2>&1 | tail -20
```

If build fails, **STOP and fix** before continuing. If the failure is non-trivial (MSBuild errors, target failures, complex compilation issues), proceed to Phase 1b.

### Phase 1b: Build Diagnosis (on failure only)

When Phase 1 build fails with non-trivial errors:

1. **Read** `.claude/skills/dev-dotnet-build/SKILL.md` for MSBuild diagnosis knowledge
2. **Analyze** the binlog if the error involves MSBuild targets, property evaluation, or NuGet:
   ```bash
   dotnet msbuild build.binlog -v:detailed 2>&1 | grep -i "error\|failed\|not up.to.date" | head -30
   ```
3. **Optionally spawn** the `dotnet-build-resolver` agent for autonomous fix attempts:
   - Spawn when: multiple compilation errors, MSBuild configuration issues, or package resolution failures
   - Don't spawn when: single obvious typo or missing semicolon
   - The agent will attempt up to 3 fix iterations and report results

After build succeeds (or after agent resolves errors), continue to Phase 2.

### Phase 2: Static Analysis (Roslyn Analyzers)

```bash
dotnet build /p:TreatWarningsAsErrors=true 2>&1 | head -30
```

Report all analyzer warnings. Fix critical ones before continuing.

### Phase 3: Format Check

```bash
dotnet format --verify-no-changes 2>&1 | head -30
# If --fix flag: dotnet format
```

Checks formatting against `.editorconfig` rules.

### Phase 4: Test Suite

```bash
dotnet test --collect:"XPlat Code Coverage" --results-directory ./TestResults 2>&1 | tail -50
# For specific project: dotnet test tests/MyProject.Tests/
```

Report:
```
Total tests: X
Passed: X
Failed: X
Coverage: X%
```

### Phase 4b: Aspire Runtime Check (Optional)

If the project uses .NET Aspire and the AppHost is running, verify runtime health after tests pass:

**Step 1 — Resource health:**
```
mcp__aspire__list_resources
```
Verify all resources report `Running` / `Healthy`. Flag any `Failed` or `Degraded` resources.

**Step 2 — Console errors:**
```
mcp__aspire__list_console_logs  resourceName: "api"
```
Scan for `Error`, `Exception`, `FATAL`, or stack traces in the console output. These indicate runtime failures that unit tests don't catch — DI registration errors, startup crashes, middleware failures, or unhandled exceptions.

**Step 3 — Structured log errors:**
```
mcp__aspire__list_structured_logs  resourceName: "api"
```
Filter for `Error` and `Warning` severity entries. Check for:
- Failed dependency injection resolutions
- Configuration binding errors
- Event store connection failures
- Projection catch-up errors

Report any errors found as verification failures.

Skip this phase if Aspire is not part of the project or the AppHost is not running.

### Phase 5: Event Sourcing Checks

Projects using `EventSourcing` need two additional checks:

#### 5a: Analyzer Package

Verify `EventSourcing.Analyzers` is referenced alongside the ES library:

```bash
dotnet list package | grep -i "EventSourcing" 2>&1
```

If `EventSourcing` is present but `EventSourcing.Analyzers` is not, flag it.

#### 5b: Code Generation Verification

After any changes to aggregates, events, or domain model types, the generated code must be in sync. Run:

```bash
# Find the solution file
SLN=$(find . -maxdepth 3 -name "*.sln" | head -1)

# Run code generation
dotnet run --project $(dirname "$SLN")/src/*/AppHost/ -- faes generate "$SLN" 2>&1 || \
  dotnet tool run faes -- generate "$SLN" 2>&1 || \
  echo "[SKIP] No faes tool found"
```

After generation, check for uncommitted changes to `.Generated.cs` files:

```bash
git diff --name-only -- '*.Generated.cs'
```

If any `.Generated.cs` files have changed, this means the generated code was **out of sync** with the domain model. Report which files changed and flag as a verification failure — the generated files must be committed alongside the domain changes.

**When to skip:** If no `.cs` files under a `Domain` directory were changed in this session, skip this phase.

#### 5c: Projection Consistency

Check that projections are up to date with their event handlers. After code gen runs, verify:

```bash
# Check for any projection files that reference events not handled
# Look for projections that may need updating
git diff --name-only -- '*Projection*.cs' '*Projection*.Generated.cs'
```

If projection files changed after code gen, flag them for review — a new event type may need to be handled in existing projections.

### Phase 6: Security Scan

```bash
# Check for secrets in tracked files
git diff --cached --name-only | xargs grep -l "password\|secret\|apikey\|connectionstring" 2>/dev/null | head -10

# Check for hardcoded connection strings
grep -rn "Server=\|Data Source=\|mongodb://" --include="*.cs" --include="*.json" . 2>/dev/null | grep -v "appsettings.Development" | head -10

# NuGet dependency vulnerabilities
dotnet list package --vulnerable 2>&1 | head -20

# Deprecated packages
dotnet list package --deprecated 2>&1 | head -20
```

### Phase 7: Diff Review

```bash
git diff --stat
git diff HEAD~1 --name-only
```

Review each changed file for:
- Unintended changes
- Missing error handling or null checks
- Missing `async/await` patterns
- EF Core N+1 query patterns (missing `.Include()`)
- Unparameterized SQL (`ExecuteSqlRawAsync` with string concatenation)
- Missing authorization on new endpoints

## Output Format

```
VERIFICATION REPORT — Backend (.NET)
=====================================

Build:       [PASS/FAIL]
Build Diag:  [PASS/SKIP/FIXED] (binlog analysis)
Analyzers:   [PASS/FAIL] (X warnings)
Format:      [PASS/FAIL]
Tests:       [PASS/FAIL] (X/Y passed, Z% coverage)
Aspire:      [PASS/SKIP] (resource health)
ES Analyzers:  [PASS/SKIP/WARN] (package check)
ES CodeGen:    [PASS/SKIP/FAIL] (generated files in sync)
Projections:   [PASS/SKIP/WARN] (projection consistency)
Security:    [PASS/FAIL] (X issues)
Diff:        [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
2. ...
```

## Flags

| Flag | Behavior |
|------|----------|
| `--quick` | Build + analyzers only (skip tests, security) |
| `--full` | All phases (default) |
| `--fix` | Auto-fix formatting (`dotnet format`) |

## Cleanup

After all verification phases complete (pass or fail), clean up generated artifacts:

```bash
# Remove binlog (can be large, contains sensitive info)
rm -f build.binlog
```

## CI Alignment

These verification phases mirror what GitHub Actions CI runs: `dotnet restore`, `dotnet build --configuration Release`, `dotnet test`. Running this locally catches the same issues CI would flag, avoiding failed PR checks.
