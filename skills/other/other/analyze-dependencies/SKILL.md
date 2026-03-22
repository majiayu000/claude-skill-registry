---
name: analyze-dependencies
description: Audit project dependencies for risk when the user asks to check dependencies, audit packages, review dependency health, check for vulnerabilities, or assess supply chain risk
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[package manager file or specific dependency to analyze]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: analysis, dependencies, maintenance
---

# Analyze Dependencies

## Overview

Audit the project's dependency tree across five risk dimensions: freshness, vulnerabilities, bundle impact, license compliance, and maintenance status. Produce a risk-scored report with actionable recommendations for each dependency.

## Workflow

1. **Read project context** — Check `.chalk/docs/engineering/` for:
   - Architecture docs (to understand which dependencies are critical path)
   - Previous dependency audits
   - Any documented dependency policies or license requirements

2. **Locate dependency manifests** — Scan the project for:
   - `package.json` / `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` (Node.js)
   - `pyproject.toml` / `requirements.txt` / `Pipfile` / `poetry.lock` (Python)
   - `pubspec.yaml` / `pubspec.lock` (Dart/Flutter)
   - `Cargo.toml` / `Cargo.lock` (Rust)
   - `go.mod` / `go.sum` (Go)
   - `Gemfile` / `Gemfile.lock` (Ruby)
   - `pom.xml` / `build.gradle` (Java/Kotlin)
   - If `$ARGUMENTS` specifies a file, focus on that manifest

3. **Inventory dependencies** — For each manifest, list:
   - Direct dependencies (production)
   - Direct dev dependencies
   - Note the declared version constraints (exact, range, caret, tilde)

4. **Assess freshness** — For each dependency:
   - Current installed version vs. latest available version
   - Run the appropriate command: `npm outdated`, `pip list --outdated`, `pub outdated`, etc.
   - Classify the gap:
     - **Current**: on latest or within one minor version
     - **Stale**: one or more minor versions behind
     - **Outdated**: one or more major versions behind
     - **Abandoned**: no release in 2+ years

5. **Check for vulnerabilities** — Run the appropriate audit command:
   - `npm audit` / `yarn audit` / `pnpm audit`
   - `pip audit` or `safety check`
   - `cargo audit`
   - `bundle audit`
   - Record: CVE ID, severity (critical/high/medium/low), affected version range, fix available (yes/no)
   - Check transitive dependencies, not just direct ones

6. **Evaluate bundle impact** — Where applicable:
   - For Node.js: check package size, number of transitive dependencies, tree-shakeability
   - For frontend projects: note if a large library is used for a small feature (e.g., lodash for one function)
   - Flag dependencies that pull in disproportionately large sub-dependency trees

7. **Check license compliance** — For each dependency:
   - Identify the license (MIT, Apache-2.0, GPL, LGPL, AGPL, BSD, ISC, etc.)
   - Flag copyleft licenses (GPL, AGPL, LGPL) that may have viral implications
   - Flag unlicensed or custom-licensed packages
   - Flag license changes between the installed version and latest version
   - Note: MIT, Apache-2.0, BSD, ISC are generally permissive and low risk

8. **Assess maintenance status** — For each dependency, check:
   - Last publish date
   - Open issues and PRs (especially security-related)
   - Number of maintainers (bus factor)
   - Whether the project is archived or deprecated
   - Classify: **Active** (regular releases, responsive maintainers), **Maintained** (occasional releases, issues addressed), **Minimal** (rare updates, issues pile up), **Unmaintained** (no activity in 12+ months)

9. **Score each dependency** — Assign a risk score based on all dimensions:
   - **Low**: Current, no vulnerabilities, permissive license, actively maintained
   - **Medium**: Stale or one minor concern (e.g., slightly outdated, minimal maintenance)
   - **High**: Outdated or multiple concerns (known vulnerability with fix available, copyleft license, large bundle impact)
   - **Critical**: Known exploitable vulnerability, abandoned with no alternative, or license violation

10. **Generate recommendations** — For each dependency with medium or higher risk:
    - **Update**: Newer version fixes the issue. Note any breaking changes.
    - **Replace**: Better-maintained alternative exists. Name the alternative.
    - **Remove**: Dependency is unused or its functionality can be inlined.
    - **Monitor**: Risk is acceptable for now but should be tracked.
    - **Immediate Action**: Critical vulnerability or license violation requiring urgent attention.

11. **Determine the next file number** — List files in `.chalk/docs/engineering/` matching `*_dependency_audit*`. Find the highest number and increment by 1.

12. **Write the report** — Save to `.chalk/docs/engineering/<n>_dependency_audit.md`.

13. **Confirm** — Summarize: total dependencies analyzed, risk distribution, critical items requiring immediate attention.

## Filename Convention

```
<number>_dependency_audit.md
```

Examples:
- `5_dependency_audit.md`
- `9_dependency_audit.md`

## Dependency Audit Format

```markdown
# Dependency Audit

Last updated: <YYYY-MM-DD>
Package manager: <npm / pip / pub / cargo / etc.>
Manifest: <path to manifest file>

## Summary

| Risk Level | Count | Action Required |
|------------|-------|-----------------|
| Critical | <n> | Immediate action |
| High | <n> | Plan remediation this sprint |
| Medium | <n> | Schedule for next maintenance window |
| Low | <n> | No action needed |
| **Total** | **<n>** | |

## Vulnerability Summary

| CVE | Severity | Package | Installed | Fixed In | Transitive? |
|-----|----------|---------|-----------|----------|-------------|
| CVE-XXXX-XXXXX | Critical | <name> | <version> | <version> | No |

## Critical & High Risk Dependencies

### <package-name> — CRITICAL

| Dimension | Status | Detail |
|-----------|--------|--------|
| Freshness | Outdated | Installed: 2.1.0, Latest: 4.0.0 |
| Vulnerabilities | CVE-XXXX-XXXXX (High) | RCE via crafted input |
| Bundle Impact | 450KB | Pulls in 23 transitive deps |
| License | MIT | No issues |
| Maintenance | Unmaintained | Last release: 2022-01-15 |

**Risk**: <Why this is critical>
**Recommendation**: Replace with `<alternative>`. Migration guide: <link or steps>.

### <package-name> — HIGH

| Dimension | Status | Detail |
|-----------|--------|--------|
| ... | ... | ... |

**Risk**: <explanation>
**Recommendation**: <action>

## Medium Risk Dependencies

| Package | Version | Risk Factors | Recommendation |
|---------|---------|-------------|----------------|
| <name> | <ver> | Stale (3 minor behind), minimal maintenance | Update to <ver> |

## Low Risk Dependencies

| Package | Version | License | Last Updated |
|---------|---------|---------|-------------|
| <name> | <ver> | MIT | 2024-11-01 |

## License Compliance

| License | Count | Packages | Risk |
|---------|-------|----------|------|
| MIT | <n> | <list> | None |
| Apache-2.0 | <n> | <list> | None |
| GPL-3.0 | <n> | <list> | Copyleft — review required |
| Unlicensed | <n> | <list> | Unknown — investigate |

## Recommendations Summary

### Immediate Action
1. <package>: <action and reason>

### This Sprint
1. <package>: <action and reason>

### Next Maintenance Window
1. <package>: <action and reason>

### Monitor
1. <package>: <what to watch for>
```

## Risk Scoring Matrix

| Dimension | Low | Medium | High | Critical |
|-----------|-----|--------|------|----------|
| Freshness | Current or 1 minor behind | 2+ minor behind | 1+ major behind | Abandoned (2+ years) |
| Vulnerabilities | None known | Low severity | High severity, fix available | Critical severity or no fix |
| Bundle Impact | < 50KB, few transitive | 50-200KB | 200KB-1MB | > 1MB or 50+ transitive deps |
| License | MIT, BSD, ISC, Apache-2.0 | LGPL | GPL | AGPL or unlicensed |
| Maintenance | Active (monthly releases) | Maintained (quarterly) | Minimal (yearly) | Unmaintained or archived |

The overall risk score for a dependency is the highest score across all dimensions.

> **Note:** These risk levels assume distributed, proprietary software. Adjust based on your project's distribution model — for internal-only tools, even copyleft licenses may be low risk. For dynamically linked libraries, LGPL is often low risk.

## Anti-patterns

- **Only checking for vulnerabilities, ignoring staleness** — A dependency with no CVEs but abandoned for 3 years is a ticking time bomb. When a vulnerability is discovered, there will be no one to patch it. Staleness is a leading indicator of future risk.
- **Not checking transitive dependencies** — Your project may have 20 direct dependencies but 200 transitive ones. A critical vulnerability in a transitive dependency is just as exploitable. Always audit the full tree.
- **Ignoring license issues** — Using a GPL library in a proprietary product can create legal exposure. License compliance is not optional, and "we will deal with it later" becomes expensive when a customer or investor asks.
- **Only auditing production dependencies** — Dev dependencies run in your CI/CD pipeline and developer machines. A compromised dev dependency can inject malicious code into your build artifacts. Audit everything.
- **Treating the audit as a one-time activity** — Dependencies change constantly. New vulnerabilities are disclosed daily. Schedule regular audits (at least monthly) and integrate `npm audit` / `pip audit` into CI.
- **Recommending updates without checking breaking changes** — "Just update to latest" is not actionable advice. Check the changelog for breaking changes, especially across major versions, and note migration effort in the recommendation.
- **Ignoring bundle impact in frontend projects** — A 2MB dependency for a single utility function destroys load time. Always consider whether the functionality can be achieved with a smaller package or inlined code.
