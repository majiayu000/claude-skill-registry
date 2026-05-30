---
name: dependency-audit
description: >
  Periodically scan project dependencies for security vulnerabilities,
  outdated packages, and unused dependencies. Produces a prioritized
  action report. Run before every major release and at least once per month.
---

<!--
  TÜRKÇE AÇIKLAMA
  ───────────────
  Bu skill, projenin bağımlılıklarını (npm, pip, vb.) güvenlik açıkları, eski sürümler
  ve kullanılmayan paketler açısından tarar. Bulunan sorunları öncelik sırasına göre
  listeler ve güvenli güncellemeleri otomatik uygular. Her major release öncesi ve
  ayda bir çalıştırılmalıdır.

  NE ZAMAN: Her production release öncesi. Aylık rutin. Yeni CVE duyurulduğunda.
  ÇIKTI:    .agent/audits/dependency-audit-YYYY-MM-DD.md — öncelikli aksiyon raporu.
-->

# Dependency Audit Skill

## When to Trigger

- Before any production release
- Monthly cadence (add to sprint planning)
- After a CVE is publicly announced that might affect your stack
- When a team member says "we should update our packages"
- Before onboarding a new contributor (known-safe baseline)

## Step-by-Step Process

### 1. Detect Package Ecosystem

Identify which package managers are in use:

```
package.json        → npm / yarn / pnpm  (Node.js)
requirements.txt    → pip                (Python)
pyproject.toml      → pip / poetry       (Python)
Gemfile             → bundler            (Ruby)
go.mod              → go modules         (Go)
Cargo.toml          → cargo              (Rust)
```

Run the audit steps for each ecosystem found.

---

### 2. Security Vulnerability Scan

#### Node.js
```bash
npm audit
# or
yarn audit
# or
pnpm audit
```

#### Python
```bash
pip install pip-audit
pip-audit
```

#### General (all ecosystems)
```bash
# If using GitHub: check Security tab → Dependabot alerts
# If using Snyk:
snyk test
```

**Triage each finding:**

| Severity | Action |
|----------|--------|
| Critical | Fix immediately before any other work |
| High | Fix before next release |
| Medium | Schedule for current sprint |
| Low | Track, fix when touching related code |

---

### 3. Outdated Package Scan

#### Node.js
```bash
npm outdated
```

#### Python
```bash
pip list --outdated
```

For each outdated package, check:
1. **How many major versions behind?** (1 minor = low urgency, 2+ major = high urgency)
2. **Is it a direct or transitive dependency?**
3. **Does the changelog mention breaking changes?**

---

### 4. Unused Dependency Detection

#### Node.js
```bash
npx depcheck
```

#### Python
```bash
pip install deptry
deptry .
```

For each unused dependency flagged:
- Verify it's truly unused (some are peer deps or used at runtime via config)
- If confirmed unused, remove from `package.json` / `requirements.txt`
- Re-run the app and tests to confirm nothing breaks

---

### 5. License Compliance Check

Flag any dependencies with licenses that may be incompatible with your project:

```bash
# Node.js
npx license-checker --summary

# Python  
pip install pip-licenses
pip-licenses
```

**License risk tiers:**

| License | Risk |
|---------|------|
| MIT, Apache 2.0, BSD | Safe for most uses |
| LGPL | Generally OK, check linking requirements |
| GPL | Risk if distributing proprietary software |
| AGPL | High risk — requires open-sourcing if used via network |
| Unknown | Must investigate before use |

---

### 6. Produce the Audit Report

Write findings to `.agent/audits/dependency-audit-<YYYY-MM-DD>.md`:

```markdown
# Dependency Audit — <YYYY-MM-DD>

## Summary
- **Critical vulnerabilities:** <N>
- **High vulnerabilities:** <N>
- **Outdated packages:** <N>
- **Unused packages:** <N>
- **License issues:** <N>

## Critical / High — Action Required

### <package-name> @ <version>
- **CVE:** CVE-XXXX-XXXXX
- **Severity:** Critical
- **Description:** <what the vulnerability is>
- **Fix:** Upgrade to <version>
- **Breaking changes:** Yes/No — <details>

## Outdated Packages

| Package | Current | Latest | Urgency | Notes |
|---------|---------|--------|---------|-------|
| express | 4.17.1 | 5.0.0 | High | Major version — review changelog |
| lodash | 4.17.20 | 4.17.21 | Low | Patch only |

## Unused Dependencies (safe to remove)
- `left-pad` — not imported anywhere
- `moment` — replaced by `date-fns` but not removed

## License Issues
- `<package>` uses GPL-3.0 — review with team before next release

## Recommendations
1. <prioritized action>
2. <prioritized action>
```

---

### 7. Execute Safe Fixes

For packages with **patch or minor** updates and **no breaking changes**:

```bash
# Node.js — safe updates only
npm update

# Python
pip install --upgrade <package>
```

After upgrading:
1. Run the full test suite
2. Do a smoke test of the running app
3. Commit with message: `chore: dependency security updates <YYYY-MM-DD>`

For **major version** upgrades, create a separate branch and task.

## Rules

- **Never auto-upgrade major versions** in bulk — do them one at a time.
- **Always run tests after any upgrade** — even patch versions can break things.
- **Keep the audit report** even after fixes — it's a compliance record.
- **Critical vulnerabilities block releases** — no exceptions without explicit sign-off.
- **Unused packages must be removed**, not just ignored — they are attack surface.
