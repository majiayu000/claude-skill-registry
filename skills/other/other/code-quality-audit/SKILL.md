---
name: code-quality-audit
description: Use when checking code quality, running security audits, testing coverage, finding SOLID/DRY violations, or setting up quality tools. Use when user says "audit this code", "check security", "run PHPStan", "code quality", "find violations", "SOLID check", "DRY check", "test coverage", "lint this", "security review", "is this production ready", "check for vulnerabilities", "code review", "grade this code". Supports Drupal (PHPStan, PHPMD, Psalm, Semgrep, Trivy, Gitleaks via DDEV) and Next.js (ESLint, Jest, Semgrep, Trivy, Gitleaks). Use proactively before deployment or after significant code changes.
version: 2.7.0
allowed-tools: Read, Bash, Grep, Glob
user-invocable: true
---

# Code Quality Audit

Run quality and security audits for **Drupal** and **Next.js** projects with consistent tooling and reporting.

## Quick Commands

**For direct access, use these commands:**
- `/code-quality:setup` - First-time setup wizard (install and configure tools)
- `/code-quality:audit` - Run full audit (all 22 operations)
- `/code-quality:coverage` - Check test coverage
- `/code-quality:security` - Security scan (10 layers for Drupal, 7 for Next.js)
- `/code-quality:lint` - Code standards check
- `/code-quality:solid` - Architecture and SOLID principles check
- `/code-quality:dry` - Find code duplication
- `/code-quality:tdd` - Start TDD workflow (test watcher mode)
- `/code-quality:review` - Rubric-scored code review (/50 scale with quality gate)
- `/code-quality:generate-review-md` - Generate REVIEW.md for Claude Code's managed Code Review
- `/code-quality:architecture-debate` - Architecture debate (Pragmatist + Purist + Maintainer)

**For conversational workflows, continue reading...**

> **Note — Claude Code's built-in `/simplify`:** Claude Code ships a built-in `/simplify` skill for quick single-pass code review. `/code-quality:review` is different: it runs automated tools (PHPStan/ESLint), scores across 10 rubric categories with a /50 scale, enforces a quality gate (PASS 35+/FAIL), and writes a persisted report. Use `/simplify` for fast ad-hoc feedback; use `/code-quality:review` when you need a structured, scored, and documented assessment.

## When to Use

**Drupal projects:**
- "Setup quality tools" / "Install PHPStan"
- "Run code audit" / "Check code quality"
- "Check coverage" / "What's my coverage?"
- "Find SOLID violations" / "Check complexity"
- "Check duplication" / "DRY check"
- "Lint code" / "Check coding standards"
- "Fix deprecations" / "Run rector"
- "Start TDD" / "RED-GREEN-REFACTOR"
- "Check security" / "Find vulnerabilities" / "OWASP audit"

**Next.js projects:**
- "Setup quality tools" / "Install ESLint"
- "Run code audit" / "Check code quality"
- "Check coverage" / "Run Jest coverage"
- "Find SOLID violations" / "Check complexity" / "Check circular deps"
- "Lint code" / "Run ESLint"
- "Check duplication" / "DRY check"
- "Start TDD" / "Jest watch mode"
- "Check security" / "Find vulnerabilities" / "OWASP audit"

## Quick Reference

### Drupal Scripts
| Task | Script | Details |
|------|--------|---------|
| Setup tools | `scripts/core/install-tools.sh` | See [Drupal Setup](references/operations/drupal-setup.md#operation-1-setup-tools) |
| Full audit | `scripts/core/full-audit.sh` | See [Full Audit](references/operations/drupal-audits.md#operation-2-full-audit) |
| Coverage | `scripts/drupal/coverage-report.sh` | See [Coverage Check](references/operations/drupal-audits.md#operation-3-coverage-check) |
| SOLID check | `scripts/drupal/solid-check.sh` | See [SOLID Check](references/operations/drupal-audits.md#operation-4-solid-check) |
| DRY check | `scripts/drupal/dry-check.sh` | See [DRY Check](references/operations/drupal-audits.md#operation-5-dry-check) |
| Lint check | `scripts/drupal/lint-check.sh` | See [Lint Check](references/operations/drupal-audits.md#operation-11-lint-check) |
| Fix deprecations | `scripts/drupal/rector-fix.sh` | See [Rector Fix](references/operations/drupal-audits.md#operation-12-rector-fix) |
| TDD cycle | `scripts/drupal/tdd-workflow.sh` | See [TDD Workflow](references/operations/drupal-tdd.md) |
| Security audit | `scripts/drupal/security-check.sh` | See [Security Audit](references/operations/drupal-security.md) (10 layers) |

### Next.js Scripts
| Task | Script | Details |
|------|--------|---------|
| Setup tools | `scripts/core/install-tools.sh` | See [Next.js Setup](references/operations/nextjs-setup.md) |
| Full audit | `scripts/core/full-audit.sh` | See [Full Audit](references/operations/nextjs-audits.md#operation-14-full-audit) |
| Coverage | `scripts/nextjs/coverage-report.sh` | See [Coverage Check](references/operations/nextjs-audits.md#operation-16-coverage-check) |
| SOLID check | `scripts/nextjs/solid-check.sh` | See [SOLID Check](references/operations/nextjs-audits.md#operation-19-solid-check) |
| Lint check | `scripts/nextjs/lint-check.sh` | See [Lint Check](references/operations/nextjs-audits.md#operation-15-lint-check) |
| DRY check | `scripts/nextjs/dry-check.sh` | See [DRY Check](references/operations/nextjs-audits.md#operation-17-dry-check) |
| TDD cycle | `scripts/nextjs/tdd-workflow.sh` | See [TDD Workflow](references/operations/nextjs-tdd.md) |
| Security audit | `scripts/nextjs/security-check.sh` | See [Security Audit](references/operations/nextjs-security.md) (7 layers) |

## Before Any Operation

**Drupal:**
1. Locate Drupal root: check `web/core/lib/Drupal.php` or `docroot/core/lib/Drupal.php`
2. Verify DDEV: `ddev describe`
3. Create reports directory: `mkdir -p .reports && echo ".reports/" >> .gitignore`

**Next.js:**
1. Verify npm: `npm --version`
2. Create reports directory: `mkdir -p .reports && echo ".reports/" >> .gitignore`

> **Sandbox users:** If Claude Code sandbox mode is enabled, bash scripts that invoke linters (PHPStan, ESLint, Semgrep, Trivy, Gitleaks) require their binary paths to be whitelisted. Add the tool binaries to your `allowedPaths` in `claude_code_config.json` (e.g., `vendor/bin/phpstan`, `/usr/local/bin/semgrep`). DDEV-proxied commands run inside the container and are unaffected.

## When to Run What

Read `decision-guides/quality-audit-checklist.md` for detailed guidance.

| Context | What to Run | Time |
|---------|-------------|------|
| Pre-commit | `quality:cs` only | ~5s |
| Pre-push | PHPStan + Unit/Kernel tests | ~2min |
| Pre-merge | Full audit | ~10min |
| Weekly | Full audit + HTML reports | ~15min |

## Scope Targeting

To audit specific modules or components instead of the entire project:

**See [Scope Targeting](references/scope-targeting.md)** for three approaches:
1. **Change directory** (recommended) - `cd web/modules/custom/my_module`
2. **Environment variables** - `DRUPAL_MODULES_PATH=path/to/module`
3. **Full scan** (default) - Run from project root

Intelligent detection: Claude detects current directory and user intent.

---

# Operations

All detailed operation instructions have been moved to reference files for better organization.

## Drupal Operations

### Setup & Configuration
- **Operation 1:** [Setup Tools](references/operations/drupal-setup.md#operation-1-setup-tools) - Install PHPStan, PHPMD, PHPCPD, Coder
- **Operation 6:** [Module-Specific Audit](references/operations/drupal-setup.md#operation-6-module-specific-audit) - Scope audit to one module
- **Operation 7:** [Add Composer Scripts](references/operations/drupal-setup.md#operation-7-add-composer-scripts) - Configure quality scripts
- **Operation 8:** [CI Integration](references/operations/drupal-setup.md#operation-8-ci-integration) - Setup GitHub Actions

### Quality Audits
- **Operation 2:** [Full Audit](references/operations/drupal-audits.md#operation-2-full-audit) - Run all quality checks
- **Operation 3:** [Coverage Check](references/operations/drupal-audits.md#operation-3-coverage-check) - Measure test coverage
- **Operation 4:** [SOLID Check](references/operations/drupal-audits.md#operation-4-solid-check) - Find principle violations
- **Operation 5:** [DRY Check](references/operations/drupal-audits.md#operation-5-dry-check) - Detect code duplication
- **Operation 11:** [Lint Check](references/operations/drupal-audits.md#operation-11-lint-check) - Coding standards
- **Operation 12:** [Rector Fix](references/operations/drupal-audits.md#operation-12-rector-fix) - Auto-fix deprecations

### Development Workflows
- **Operation 10:** [TDD Workflow](references/operations/drupal-tdd.md) - RED-GREEN-REFACTOR cycle

### Security
- **Operation 20:** [Security Audit](references/operations/drupal-security.md) - **10 security layers (v2.0.0)**
  - Drush pm:security, Composer audit
  - yousha/php-security-linter, Psalm taint analysis
  - Custom Drupal patterns, Security Review module
  - **Semgrep SAST, Trivy scanner, Gitleaks** (v1.8.0)
  - **Roave Security Advisories** (v2.0.0)

## Next.js Operations

### Setup & Configuration
- **Operation 13:** [Setup Tools](references/operations/nextjs-setup.md) - Install ESLint, Jest, security tools

### Quality Audits
- **Operation 14:** [Full Audit](references/operations/nextjs-audits.md#operation-14-full-audit) - Run all quality checks
- **Operation 15:** [Lint Check](references/operations/nextjs-audits.md#operation-15-lint-check) - ESLint + TypeScript
- **Operation 16:** [Coverage Check](references/operations/nextjs-audits.md#operation-16-coverage-check) - Jest coverage
- **Operation 17:** [DRY Check](references/operations/nextjs-audits.md#operation-17-dry-check) - Detect duplication
- **Operation 19:** [SOLID Check](references/operations/nextjs-audits.md#operation-19-solid-check) - Circular deps, complexity

### Development Workflows
- **Operation 18:** [TDD Workflow](references/operations/nextjs-tdd.md) - RED-GREEN-REFACTOR with Jest

### Security
- **Operation 21:** [Security Audit](references/operations/nextjs-security.md) - **7 security layers (v2.0.0)**
  - npm audit, ESLint security plugins
  - **Semgrep SAST, Trivy scanner, Gitleaks** (v1.8.0)
  - Custom React/Next.js patterns (XSS, eval, navigation)
  - **Socket CLI** (v2.0.0)

## Optional: DAST (Dynamic Testing)

**Pre-production security testing for staging environments**

- **Operation 22:** [DAST Tools](references/operations/dast-tools.md) - **Dynamic security testing (v2.1.0)**
  - OWASP ZAP (full DAST scanner)
  - Nuclei (template-based CVE scanning)
  - Requires running application
  - Use before releases on staging/pre-production

---

## Saving Reports

All reports must follow `schemas/audit-report.schema.json`:

```json
{
  "meta": {
    "project_type": "drupal|nextjs|monorepo",
    "timestamp": "2025-12-19T12:00:00Z",
    "thresholds": { "coverage_minimum": 70, "duplication_max": 5 }
  },
  "summary": {
    "overall_score": "pass|warning|fail",
    "coverage_score": "pass|warning|fail",
    "solid_score": "pass|warning|fail",
    "dry_score": "pass|warning|fail",
    "security_score": "pass|warning|fail"
  },
  "coverage": { "line_coverage": 75.5, "files_analyzed": 45 },
  "solid": { "violations": [] },
  "dry": { "duplication_percentage": 3.2, "clones": [] },
  "security": { "critical": 0, "high": 0, "medium": 3, "low": 5, "issues": [] },
  "recommendations": []
}
```

---

## References

### Core Guidance
- `references/tdd-workflow.md` - RED-GREEN-REFACTOR patterns, test naming, cycle targets
- `references/coverage-metrics.md` - Coverage targets by code type, PCOV vs Xdebug
- `references/dry-detection.md` - Rule of Three, when duplication is OK
- `references/solid-detection.md` - SOLID detection patterns and fixes
- `references/composer-scripts.md` - Ready-to-use composer scripts
- `references/scope-targeting.md` - **Target specific modules/components (NEW in v1.8.0)**

### Operations
- `references/operations/drupal-setup.md` - Drupal setup operations
- `references/operations/drupal-audits.md` - Drupal quality audit operations
- `references/operations/drupal-security.md` - **Drupal security (10 layers, v2.0.0)**
- `references/operations/drupal-tdd.md` - Drupal TDD workflow
- `references/operations/nextjs-setup.md` - Next.js setup operations
- `references/operations/nextjs-audits.md` - Next.js quality audit operations
- `references/operations/nextjs-security.md` - **Next.js security (7 layers, v2.0.0)**
- `references/operations/nextjs-tdd.md` - Next.js TDD workflow

### Online Dev-Guides (Drupal Domain)

For deeper Drupal-specific patterns beyond tool commands, fetch the guide index:

**Index:** `https://camoa.github.io/dev-guides/llms.txt`

Likely relevant topics: solid-principles, dry-principles, security, testing, tdd, js-development, github-actions

Usage: WebFetch the index to discover available topics, then fetch specific topic pages when explaining violations, suggesting fixes, or providing architectural context.

## Decision Guides

- `decision-guides/test-type-selection.md` - Unit vs Kernel vs Functional decision tree
- `decision-guides/quality-audit-checklist.md` - When to run what (pre-commit vs pre-merge)

## Templates

### Drupal
- `templates/drupal/phpstan.neon` - PHPStan 2.x config (extensions auto-load)
- `templates/drupal/phpmd.xml` - PHPMD ruleset for Drupal
- `templates/drupal/phpunit.xml` - PHPUnit config with testsuites
- `templates/ci/github-drupal.yml` - GitHub Actions workflow with security tools

### Next.js
- `templates/nextjs/eslint.config.js` - ESLint v9 flat config with TypeScript + security
- `templates/nextjs/jest.config.js` - Jest config with coverage thresholds
- `templates/nextjs/jest.setup.js` - Jest setup with Testing Library
- `templates/nextjs/.prettierrc` - Prettier config with Tailwind plugin

---

## What's New in v2.1.0

**Phase 3 - Optional DAST Tools (NEW!):**
- ✅ OWASP ZAP (full DAST scanner for pre-production)
- ✅ Nuclei (template-based CVE and misconfiguration scanning)
- ✅ Comprehensive documentation with usage examples
- ✅ CI/CD integration guides (GitHub Actions, GitLab)
- ✅ Pre-release checklist script

**DAST Coverage:**
- Pre-production security testing
- Runtime vulnerability detection
- OWASP Top 10 dynamic testing
- 1000+ CVE templates (Nuclei)

See `references/operations/dast-tools.md` for full documentation.

---

## What's New in v2.0.0

**Progressive Disclosure Refactoring:**
- ✅ SKILL.md: 632 → 234 lines (63% reduction)
- ✅ 9 reference files created with full documentation
- ✅ Plugin-creation-tools compliance (16/16 criteria)

**Phase 1 - Cross-Stack Security Tools:**
- ✅ Semgrep SAST (20,000+ security rules for PHP, React, JS, TS)
- ✅ Trivy scanner (dependency/container/secret scanner)
- ✅ Gitleaks (secret detection with 800+ patterns)

**Phase 2 - Enhancement Tools:**
- ✅ Roave Security Advisories (Drupal - Composer prevention layer)
- ✅ Socket CLI (Next.js - supply chain attack detection)

**Security Coverage:**
- Drupal: 40% → **90%** (10 security layers)
- Next.js: 0% → **85%** (7 security layers)

See `.work-in-progress-v2.0.0.md` for full implementation details.
