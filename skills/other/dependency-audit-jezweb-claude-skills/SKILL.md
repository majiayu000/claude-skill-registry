---
name: dependency-audit
description: |
  Comprehensive dependency health auditing for JavaScript/TypeScript projects. Run npm audit, detect outdated packages, check for security advisories, and verify license compliance. Prioritises vulnerabilities by severity and provides actionable fix recommendations.

  Use when: auditing project dependencies, checking for vulnerabilities, updating packages, preparing for release, or investigating "npm audit" warnings. Keywords: audit, vulnerabilities, outdated, security, npm audit, pnpm audit, CVE, GHSA, license.
license: MIT
---

# Dependency Audit

**Status**: Production Ready
**Last Updated**: 2026-02-03
**Scope**: npm, pnpm, yarn projects

---

## Commands

| Command | Purpose |
|---------|---------|
| `/audit-deps` | Run comprehensive dependency audit with prioritised findings |

## Quick Start

```
/audit-deps                    # Full audit
/audit-deps --security-only    # Only security vulnerabilities
/audit-deps --outdated         # Only outdated packages
/audit-deps --fix              # Auto-fix compatible updates
```

---

## What This Skill Audits

### 1. Security Vulnerabilities

```
npm audit / pnpm audit
```

- **Critical** (CVSS 9.0-10.0): Remote code execution, auth bypass
- **High** (CVSS 7.0-8.9): Data exposure, privilege escalation
- **Moderate** (CVSS 4.0-6.9): DoS, info disclosure
- **Low** (CVSS 0.1-3.9): Minor issues

### 2. Outdated Packages

```
npm outdated / pnpm outdated
```

Categories:
- **Major updates**: Breaking changes likely (review changelog)
- **Minor updates**: New features, backwards compatible
- **Patch updates**: Bug fixes, safe to update

### 3. License Compliance

Checks for:
- GPL licenses in commercial projects (copyleft risk)
- Unknown/missing licenses
- License conflicts

### 4. Dependency Health

- Deprecated packages
- Abandoned packages (no updates in 2+ years)
- Packages with open security issues

---

## Output Format

```
═══════════════════════════════════════════════
   DEPENDENCY AUDIT REPORT
═══════════════════════════════════════════════

Project: my-app
Package Manager: pnpm
Total Dependencies: 847 (142 direct, 705 transitive)

───────────────────────────────────────────────
   SECURITY
───────────────────────────────────────────────

🔴 CRITICAL (1)
  lodash@4.17.20
  └─ CVE-2021-23337: Command injection via template()
  └─ Fix: npm update lodash@4.17.21
  └─ Affects: direct dependency

🟠 HIGH (2)
  minimist@1.2.5
  └─ CVE-2021-44906: Prototype pollution
  └─ Fix: Transitive via mkdirp, update parent
  └─ Path: mkdirp → minimist

  node-fetch@2.6.1
  └─ CVE-2022-0235: Exposure of sensitive headers
  └─ Fix: npm update node-fetch@2.6.7

🟡 MODERATE (3)
  [details...]

───────────────────────────────────────────────
   OUTDATED PACKAGES
───────────────────────────────────────────────

Major Updates (review breaking changes):
  react           18.2.0  →  19.1.0   (1 major)
  typescript      5.3.0   →  5.8.0    (5 minor)
  drizzle-orm     0.44.0  →  0.50.0   (6 minor)

Minor Updates (safe, new features):
  @types/node     20.11.0 →  20.14.0
  vitest          1.2.0   →  1.6.0

Patch Updates (recommended):
  [15 packages with patch updates]

───────────────────────────────────────────────
   LICENSE CHECK
───────────────────────────────────────────────

✅ All licenses compatible with MIT

Note: 3 packages use ISC (compatible)

───────────────────────────────────────────────
   SUMMARY
───────────────────────────────────────────────

Security Issues:  6 (1 critical, 2 high, 3 moderate)
Outdated:         23 (3 major, 5 minor, 15 patch)
License Issues:   0

Recommended Actions:
1. Fix critical: npm update lodash
2. Fix high: npm audit fix
3. Review major updates before upgrading

═══════════════════════════════════════════════
```

---

## Agent

The `dep-auditor` agent can:

- Parse npm/pnpm audit JSON output
- Cross-reference CVE databases
- Generate detailed fix recommendations
- Auto-fix safe updates (with confirmation)

---

## CI Integration

### GitHub Actions

```yaml
- name: Audit dependencies
  run: npm audit --audit-level=high
  continue-on-error: true

- name: Check for critical vulnerabilities
  run: |
    CRITICAL=$(npm audit --json | jq '.metadata.vulnerabilities.critical')
    if [ "$CRITICAL" -gt 0 ]; then
      echo "Critical vulnerabilities found!"
      exit 1
    fi
```

### Pre-commit Hook

```bash
#!/bin/sh
npm audit --audit-level=critical || {
  echo "Critical vulnerabilities found. Run 'npm audit fix' or '/audit-deps'"
  exit 1
}
```

---

## Package Manager Commands

| Task | npm | pnpm | yarn |
|------|-----|------|------|
| Audit | `npm audit` | `pnpm audit` | `yarn audit` |
| Audit JSON | `npm audit --json` | `pnpm audit --json` | `yarn audit --json` |
| Fix auto | `npm audit fix` | `pnpm audit --fix` | `yarn audit --fix` |
| Fix force | `npm audit fix --force` | N/A | N/A |
| Outdated | `npm outdated` | `pnpm outdated` | `yarn outdated` |
| Why | `npm explain <pkg>` | `pnpm why <pkg>` | `yarn why <pkg>` |

---

## Known Limitations

- **npm audit fix --force**: May introduce breaking changes (major version bumps)
- **Transitive dependencies**: Some vulnerabilities require updating parent packages
- **False positives**: Some advisories may not apply to your usage
- **Private registries**: May need auth configuration for auditing

---

## Related Skills

- **cloudflare-worker-base**: For Workers projects
- **testing-patterns**: Run tests after updates
- **developer-toolbox**: For commit-helper after fixes

---

**Version**: 1.0.0
**Last Updated**: 2026-02-03
