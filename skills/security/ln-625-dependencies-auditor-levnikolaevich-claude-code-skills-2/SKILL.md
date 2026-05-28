---
name: ln-625-dependencies-auditor
description: "Dependencies audit worker (L3). Checks outdated packages, unused deps, reinvented wheels, vulnerability scan (CVE/CVSS). Supports mode: full | vulnerabilities_only."
allowed-tools: Read, Grep, Glob, Bash
---

# Dependencies & Reuse Auditor (L3 Worker)

Specialized worker auditing dependency management, code reuse, and security vulnerabilities.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline** (full audit mode)
- **Worker in ln-760 security-setup pipeline** (vulnerabilities_only mode)
- Audit **dependencies and reuse** (Categories 7+8: Medium Priority)
- Check outdated packages, unused deps, wheel reinvention, **CVE vulnerabilities**
- Calculate compliance score (X/10)

## Parameters

| Param | Values | Default | Description |
|-------|--------|---------|-------------|
| mode | `full` / `vulnerabilities_only` | `full` | `full` = all 5 checks, `vulnerabilities_only` = only CVE scan |

## Inputs (from Coordinator)

Receives `contextStore` with tech stack, package manifest paths, codebase root.

**From ln-620 (codebase-auditor):** mode=full (default)
**From ln-760 (security-setup):** mode=vulnerabilities_only

## Workflow

1) Parse context + mode parameter
2) Run dependency checks (based on mode)
3) Collect findings
4) Calculate score
5) Return JSON

---

## Audit Rules (5 Checks)

### 1. Outdated Packages
**Mode:** full only

**Detection:**
- Run `npm outdated --json` (Node.js)
- Run `pip list --outdated --format=json` (Python)
- Run `cargo outdated --format=json` (Rust)

**Severity:**
- **HIGH:** Major version behind (security risk)
- **MEDIUM:** Minor version behind
- **LOW:** Patch version behind

**Recommendation:** Update to latest version, test for breaking changes

**Effort:** S-M (update version, run tests)

### 2. Unused Dependencies
**Mode:** full only

**Detection:**
- Parse package.json/requirements.txt
- Grep codebase for `import`/`require` statements
- Find dependencies never imported

**Severity:**
- **MEDIUM:** Unused production dependency (bloats bundle)
- **LOW:** Unused dev dependency

**Recommendation:** Remove from package manifest

**Effort:** S (delete line, test)

### 3. Available Features Not Used
**Mode:** full only

**Detection:**
- Check for axios when native fetch available (Node 18+)
- Check for lodash when Array methods sufficient
- Check for moment when Date.toLocaleString sufficient

**Severity:**
- **MEDIUM:** Unnecessary dependency (increases bundle size)

**Recommendation:** Use native alternative

**Effort:** M (refactor code to use native API)

### 4. Custom Implementations
**Mode:** full only

**Detection:**
- Grep for custom sorting algorithms
- Check for hand-rolled validation (vs validator.js)
- Find custom date parsing (vs date-fns/dayjs)

**Severity:**
- **HIGH:** Custom crypto (security risk)
- **MEDIUM:** Custom utilities with well-tested alternatives

**Recommendation:** Replace with established library

**Effort:** M (integrate library, replace calls)

### 5. Vulnerability Scan (CVE/CVSS)
**Mode:** full AND vulnerabilities_only

**Detection:**
- Detect ecosystems: npm, NuGet, pip, Go, Bundler, Cargo, Composer
- Run audit commands per `references/vulnerability_commands.md`
- Parse results with CVSS mapping per `shared/references/cvss_severity_mapping.md`

**Severity:**
- **CRITICAL:** CVSS 9.0-10.0 (immediate fix required)
- **HIGH:** CVSS 7.0-8.9 (fix within 48h)
- **MEDIUM:** CVSS 4.0-6.9 (fix within 1 week)
- **LOW:** CVSS 0.1-3.9 (fix when convenient)

**Fix Classification:**
- Patch update (x.x.Y) → safe auto-fix
- Minor update (x.Y.0) → usually safe
- Major update (Y.0.0) → manual review required
- No fix available → document and monitor

**Recommendation:** Update to fixed version, verify lock file integrity

**Effort:** S-L (depends on breaking changes)

---

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

**Note:** When mode=vulnerabilities_only, score based only on vulnerability findings.

## Output Format

```json
{
  "category": "Dependencies & Reuse",
  "mode": "full",
  "score": 7,
  "total_issues": 12,
  "critical": 1,
  "high": 3,
  "medium": 5,
  "low": 3,
  "checks": [
    {"id": "outdated_packages", "name": "Outdated Packages", "status": "failed", "details": "2 packages behind major versions"},
    {"id": "unused_deps", "name": "Unused Dependencies", "status": "warning", "details": "4 unused dev dependencies"},
    {"id": "available_natives", "name": "Available Natives", "status": "passed", "details": "No unnecessary polyfills"},
    {"id": "custom_implementations", "name": "Custom Implementations", "status": "warning", "details": "2 custom utilities found"},
    {"id": "vulnerability_scan", "name": "Vulnerability Scan (CVE)", "status": "failed", "details": "1 critical, 2 high vulnerabilities"}
  ],
  "findings": [
    {
      "severity": "CRITICAL",
      "location": "package.json",
      "issue": "lodash@4.17.15 has CVE-2021-23337 (CVSS 7.2)",
      "principle": "Security / Vulnerability Management",
      "recommendation": "Update to lodash@4.17.21",
      "effort": "S",
      "fix_type": "patch"
    },
    {
      "severity": "HIGH",
      "location": "package.json:15",
      "issue": "express v4.17.0 (current: v4.19.2, 2 major versions behind)",
      "principle": "Dependency Management / Security Updates",
      "recommendation": "Update to v4.19.2 for security fixes",
      "effort": "M"
    }
  ]
}
```

## Reference Files

| File | Purpose |
|------|---------|
| `references/vulnerability_commands.md` | Ecosystem-specific audit commands |
| `references/ci_integration_guide.md` | CI/CD integration guidance |
| `shared/references/cvss_severity_mapping.md` | CVSS to severity level mapping |
| `shared/references/audit_scoring.md` | Audit scoring formula |
| `shared/references/audit_output_schema.md` | Audit output schema |

---
**Version:** 4.0.0
**Last Updated:** 2026-02-05
