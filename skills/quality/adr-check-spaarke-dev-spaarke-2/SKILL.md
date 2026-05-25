---
description: Validate code changes against Architecture Decision Records (ADRs)
alwaysApply: false
---

# ADR Check

> **Category**: Quality
> **Last Updated**: December 24, 2025

---

## Purpose

Validate code changes against Spaarke's Architecture Decision Records (ADRs) before committing. This skill helps developers identify architectural violations early, ensuring code aligns with established constraints.

---

## Applies When

- Developer asks to "check ADRs", "validate architecture", or "review changes against ADRs"
- Before creating a pull request
- After making significant code changes
- When reviewing code for architectural compliance
- NOT for general code review (use `code-review` skill instead)

---

## Workflow

### Step 1: Identify Scope

Determine what code to validate:

1. **If files specified**: Check those specific files
2. **If no files specified**: Check recent git changes
   ```bash
   git status --short
   git diff --name-only HEAD~1
   ```
3. **If scope unclear**: Ask developer to clarify

### Step 2: Load ADR Context

1. Use the ADR index as the source of truth: `docs/reference/adr/README-ADRs.md`
2. Use `references/adr-validation-rules.md` for grep/pattern-based checks (where available)

Quick reference of key constraints:

| ADR | Key Constraint | Check For |
|-----|----------------|-----------|
| ADR-001 | No Azure Functions | `Microsoft.Azure.Functions`, `[FunctionName]` |
| ADR-002 | Thin plugins | `HttpClient` in plugins, >50ms operations |
| ADR-006 | PCF over webresources | New `.js` files in webresources |
| ADR-007 | Graph isolation | `Microsoft.Graph` outside Infrastructure |
| ADR-008 | Endpoint filters | Global `UseAuthorization` middleware |
| ADR-009 | Redis-first | `IMemoryCache` for cross-request caching |
| ADR-010 | DI minimalism | Interfaces with single implementation |
| ADR-021 | Fluent v9 design system | `@fluentui/react` (v8), hard-coded colors, missing FluentProvider |

Note: This table is not exhaustive. Validate against the full ADR index in `docs/reference/adr/README-ADRs.md`.

### Step 3: Run Validation Checks

For each applicable ADR:
1. Search codebase using grep/find patterns from `references/adr-validation-rules.md`
2. Categorize findings as Compliant, Warning, or Violation
3. Note specific file paths and line numbers

### Step 4: Generate Report

Output structured report using the format in Output Format section.

### Step 5: Suggest Fixes

For each violation:
1. Explain why it violates the ADR
2. Provide concrete fix with code example
3. Reference the ADR document for full context

---

## Conventions

- Always check all ADRs in the current ADR index (`docs/reference/adr/README-ADRs.md`)
- Report warnings for potential issues that need human judgment
- Provide specific file paths and line numbers for violations
- Reference ADR documents by full path: `/docs/reference/adr/ADR-XXX-*.md`
- Suggest running ArchTests after fixes: `dotnet test tests/Spaarke.ArchTests/Spaarke.ArchTests.csproj`

---

## Resources

| Resource | Purpose |
|----------|---------|
| `references/adr-validation-rules.md` | Detailed validation rules and grep patterns for each ADR |

---

## Output Format

```markdown
## ADR Validation Report

**Scope:** [files/changes being validated]
**Date:** [timestamp]

### ✅ Compliant ADRs

- ADR-001: Minimal API + BackgroundService
- ADR-007: Graph isolation
- [list all compliant ADRs]

### ⚠️ Warnings (Review Required)

- **ADR-010:** Found [N] interfaces with single implementation
  - `src/server/Services/IFooService.cs` → `FooService.cs`
  - **Recommendation:** Consider registering `FooService` directly unless testing seam needed

### ❌ Violations (Must Fix)

- **ADR-007:** Graph types found outside Infrastructure layer
  - **File:** `src/server/api/Sprk.Bff.Api/Api/FileAccessEndpoints.cs:42`
  - **Code:** `Microsoft.Graph.DriveItem item = ...`
  - **Fix:** Replace with `FileHandleDto` and route through `SpeFileStore`

### Summary

| Status | Count |
|--------|-------|
| ✅ Compliant | [N] |
| ⚠️ Warnings | [N] |
| ❌ Violations | [N] |

### Next Steps

1. Fix violations listed above
2. Review warnings with team if needed
3. Re-run validation: invoke `adr-check` skill
4. Run NetArchTest: `dotnet test tests/Spaarke.Bff.Api.ArchTests/`
```

---

## Examples

### Example 1: Check recent changes

**Input:**
```
Developer: "Check my changes against ADRs before I commit"
```

**Output:**
Claude runs `git diff --name-only`, identifies changed files, validates each against ADRs, and produces a structured report.

### Example 2: Check specific file

**Input:**
```
Developer: "Validate src/server/api/Sprk.Bff.Api/Api/DocumentsEndpoints.cs against ADRs"
```

**Output:**
Claude focuses validation on the specified file, checking for Graph types, authorization patterns, caching usage, etc.

### Example 3: Full project scan

**Input:**
```
Developer: "Run a full ADR compliance check on the solution"
```

**Output:**
Claude scans all source directories, producing a comprehensive report across all ADRs.

---

## Error Handling

| Situation | Response |
|-----------|----------|
| No files specified and no git changes | Ask developer what to validate |
| File path doesn't exist | Report error, ask for correct path |
| Unclear whether finding is violation or warning | Report as warning, explain uncertainty |

---

## Related Skills

- `code-review` - General code quality review (not architecture-focused)
- `push-to-github` - Include ADR check as part of PR creation
- `ci-cd` - CI pipeline status and ADR validation in CI

---

## CI/CD Integration

### Local vs CI ADR Validation

This skill performs **local** ADR validation. The same checks run in CI via GitHub Actions:

| Location | Tool | When |
|----------|------|------|
| Local | This skill (`/adr-check`) | Before commit/push |
| CI | NetArchTest (`Spaarke.ArchTests`) | On every PR and push to master |
| Weekly | `adr-audit.yml` workflow | Monday 9 AM UTC |

### CI Pipeline ADR Checks

The `sdap-ci.yml` workflow runs ADR tests in the `code-quality` job:

```yaml
- name: ADR architecture tests (NetArchTest)
  run: dotnet test tests/Spaarke.ArchTests/Spaarke.ArchTests.csproj
```

**Results appear in two places:**
1. **PR Comments**: `adr-pr-comment` job posts violations as PR comments
2. **Test Results**: Uploaded as workflow artifact `adr-test-results`

### Weekly ADR Audit

The `adr-audit.yml` workflow runs weekly and:
- Creates/updates GitHub issue with `architecture` and `adr-audit` labels
- Groups violations by ADR number
- Auto-closes issue when all violations resolved
- Provides remediation guidance

### Troubleshooting CI ADR Failures

```powershell
# View PR ADR check status
gh pr checks | grep -i "code-quality"

# View ADR test results
gh run view {run-id} --log --job=code-quality

# Download test results artifact
gh run download {run-id} --name adr-test-results

# Trigger ADR audit manually
gh workflow run adr-audit.yml
```

### Local Validation Before Push

**RECOMMENDED**: Run this skill before pushing to catch violations early:

```
1. Make code changes
2. Run /adr-check (this skill)
3. Fix any violations
4. Run NetArchTest locally for additional validation:
   dotnet test tests/Spaarke.ArchTests/Spaarke.ArchTests.csproj
5. Push changes
6. CI will re-run same checks
```

---

## Tips for AI

- Be thorough: check all ADRs in the ADR index even when changes seem small
- Be thorough: check all ADRs in the ADR index, even when changes seem small
- Be specific: always include file paths and line numbers
- Be actionable: provide concrete fixes, not just problem descriptions
- When in doubt, report as warning rather than skipping
- Encourage running automated NetArchTest for additional validation
