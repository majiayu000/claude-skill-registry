---
name: ln-762-dependency-audit
description: Audits project dependencies for vulnerabilities. Multi-ecosystem support (npm, .NET, Python, Go). CVSS-based severity classification.
---

# Dependency Audit

Audits project dependencies for known security vulnerabilities across multiple package ecosystems.

## Purpose & Scope

- Detect vulnerable dependencies using ecosystem-specific tools
- Support multiple ecosystems: npm, NuGet, pip, Go modules, Bundler, Cargo
- Classify vulnerabilities by severity (Critical/High/Medium/Low)
- Provide fix recommendations with safe auto-fix guidance
- Return normalized report to parent orchestrator (ln-760)

## When to Use

- During project bootstrap (via ln-760-security-setup)
- CI/CD pipeline security checks
- Pre-release security validation
- Regular scheduled audits

---

## Workflow

### Phase 1: Ecosystem Detection

**Step 1: Detect Package Managers**
- Check for `package.json` / `package-lock.json` (npm)
- Check for `*.csproj` / `packages.config` (.NET)
- Check for `requirements.txt` / `Pipfile` / `pyproject.toml` (Python)
- Check for `go.mod` (Go)
- Check for `Gemfile` (Ruby), `Cargo.toml` (Rust), `composer.json` (PHP)

**Step 2: Check Tool Availability**
- For each detected ecosystem, verify audit tool is available
- If tool missing: log warning, skip ecosystem (do not fail)

### Phase 2: Audit Execution

**Step 1: Run Ecosystem Audits**
- Execute audit command for each detected ecosystem
- Prefer JSON output for parsing (see `references/audit_commands.md`)
- Run audits in parallel where possible

**Step 2: Parse Results**
- Normalize findings to common format: package, version, vulnerability ID, severity
- Extract CVSS score if available

### Phase 3: Report Generation

**Step 1: Severity Classification**
- Map CVSS scores to severity per `references/severity_mapping.md`
- Critical: CVSS 9.0-10.0
- High: CVSS 7.0-8.9
- Medium: CVSS 4.0-6.9
- Low: CVSS 0.1-3.9

**Step 2: Group and Sort**
- Group by ecosystem
- Sort by severity (Critical first)
- Include vulnerability count summary

**Step 3: Build Report**
- Include package name, current version, fixed version
- Include vulnerability ID (CVE/GHSA/OSV)
- Do NOT include exploit details

### Phase 4: Fix Recommendations

**Step 1: Classify Fix Type**
- Patch update (safe auto-fix)
- Minor update (usually safe)
- Major update (manual review required)
- No fix available (document and monitor)

**Step 2: Generate Recommendations**
- For each vulnerability: suggest fix command
- Flag breaking changes if major version bump
- Note if fix requires code changes

**Step 3: Return Results**
- Return structured report to orchestrator
- Include summary: packages audited, vulnerabilities found, by severity

---

## Critical Rules

1. **Never auto-fix major versions** - may introduce breaking changes
2. **Verify lock file integrity** - regenerate if corrupted
3. **Respect severity thresholds** - per environment (see `references/severity_mapping.md`)
4. **Document unfixable vulns** - add to known issues with review date
5. **No exploit code** - report IDs only, not exploitation details

---

## Definition of Done

- [ ] All detected ecosystems audited
- [ ] Findings classified by severity with CVSS mapping
- [ ] Fix recommendations provided (safe vs manual)
- [ ] Report in normalized format returned
- [ ] Critical vulnerabilities prominently flagged
- [ ] Lock file integrity verified

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/audit_commands.md` | Ecosystem-specific audit commands |
| `references/severity_mapping.md` | CVSS to severity level mapping |
| `references/ci_integration_guide.md` | CI/CD integration guidance |

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
