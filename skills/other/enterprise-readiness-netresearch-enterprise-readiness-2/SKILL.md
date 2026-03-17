---
name: enterprise-readiness
description: "Assess and enhance software projects for enterprise-grade security, quality, and automation. This skill should be used when evaluating projects for production readiness, implementing supply chain security (SLSA, signing, SBOMs), hardening CI/CD pipelines, establishing quality gates, reviewing code or PRs, writing documentation (ADRs, changelogs, migration guides), or pursuing OpenSSF Best Practices Badge. Aligned with OpenSSF Scorecard, Best Practices Badge (all levels), SLSA, and S2C2F. By Netresearch."
---

# Enterprise Readiness Assessment

## When to Use

- Evaluating projects for production/enterprise readiness
- Implementing supply chain security (SLSA, signing, SBOMs)
- Hardening CI/CD pipelines
- Establishing quality gates
- Pursuing OpenSSF Best Practices Badge (Passing/Silver/Gold)
- Reviewing code or PRs for quality
- Writing ADRs, changelogs, or migration guides
- Configuring Git hooks or CI pipelines

---

## MANDATORY Requirements

**CRITICAL: The following are NOT optional. Every project MUST have ALL of these. Do not skip any.**

### README Badges (MANDATORY)

Every project README.md MUST display these badges at the top, in this order:

```markdown
<!-- Row 1: CI/Quality -->
[![CI](https://github.com/ORG/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/ORG/REPO/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ORG/REPO/graph/badge.svg)](https://codecov.io/gh/ORG/REPO)

<!-- Row 2: Security (MANDATORY) -->
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/ORG/REPO/badge)](https://securityscorecards.dev/viewer/?uri=github.com/ORG/REPO)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/PROJECT_ID/badge)](https://www.bestpractices.dev/projects/PROJECT_ID)
```

| Badge | URL Pattern | MANDATORY |
|-------|-------------|-----------|
| CI Status | `github.com/ORG/REPO/actions/workflows/ci.yml/badge.svg` | **YES** |
| Codecov | `codecov.io/gh/ORG/REPO/graph/badge.svg` | **YES** |
| OpenSSF Scorecard | `api.securityscorecards.dev/projects/github.com/ORG/REPO/badge` | **YES** |
| OpenSSF Best Practices | `www.bestpractices.dev/projects/PROJECT_ID/badge` | **YES** |

### CI/CD Workflows (MANDATORY)

Every GitHub project MUST have these workflows in `.github/workflows/`:

| Workflow | File | Purpose | MANDATORY |
|----------|------|---------|-----------|
| CI | `ci.yml` | Build, test, lint | **YES** |
| CodeQL | `codeql.yml` | Security scanning | **YES** |
| Scorecard | `scorecard.yml` | OpenSSF Scorecard | **YES** |
| Dependency Review | `dependency-review.yml` | PR CVE check | **YES** |

### CI Must Include (MANDATORY)

| Requirement | Implementation | MANDATORY |
|-------------|----------------|-----------|
| Coverage upload | `codecov/codecov-action` after tests | **YES** |
| Security audit | `composer audit` / `npm audit` / `govulncheck` | **YES** |
| SHA-pinned actions | All actions use full SHA with version comment | **YES** |

### Supply Chain Security (MANDATORY for Releases)

**Supply chain security controls MUST block releases when violated.**

| Control | Implementation | Blocks Release? |
|---------|----------------|-----------------|
| SLSA Provenance | `slsa-github-generator` workflow | **YES** - no release without attestation |
| Signed Tags | `git tag -s` before `gh release create` | **YES** - unsigned tags rejected |
| SBOM Generation | `anchore/sbom-action` or `cyclonedx` | **YES** - SBOM required for compliance |
| Dependency Audit | `composer audit` / `npm audit` fails CI | **YES** - CVEs block merge |

#### Release Workflow Order (MANDATORY)

Supply chain artifacts MUST be generated in this order:

```
1. CI passes (tests, lint, security audit)
     ↓
2. Create SIGNED tag locally: git tag -s vX.Y.Z
     ↓
3. Push signed tag: git push origin vX.Y.Z
     ↓
4. Create release on existing tag: gh release create vX.Y.Z
     ↓
5. SLSA provenance workflow triggers (workflow_run)
     ↓
6. Provenance attestation uploaded to release
     ↓
7. SBOM generated and uploaded
```

**NEVER** use `gh release create` without a pre-existing signed tag - this creates unsigned tags.

#### CI Integration for Supply Chain

Add to `.github/workflows/release.yml`:

```yaml
# Pre-release checks (block release if failed)
- name: Security Audit
  run: |
    composer audit --format=plain || exit 1
    npm audit --audit-level=high || exit 1

# SBOM generation
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    artifact-name: sbom.spdx.json
    output-file: sbom.spdx.json

- name: Upload SBOM to release
  run: gh release upload ${{ github.ref_name }} sbom.spdx.json
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### Verification of Supply Chain Artifacts

Before announcing a release, verify:

- [ ] Release tag is GPG/SSH signed: `git tag -v vX.Y.Z`
- [ ] SLSA provenance exists: `multiple.intoto.jsonl` in release assets
- [ ] SBOM exists: `sbom.spdx.json` or `sbom.cyclonedx.json` in release assets
- [ ] No HIGH/CRITICAL CVEs: `composer audit` / `npm audit` clean

See `references/slsa-provenance.md` for detailed SLSA implementation guide.

### OpenSSF Registration (MANDATORY)

1. **Register at bestpractices.dev**: https://www.bestpractices.dev/en/projects/new
2. **Note the Project ID** assigned after registration
3. **Add badge to README** with correct PROJECT_ID
4. **Run Scorecard workflow** to generate initial score

### Codecov Setup (MANDATORY)

1. **Enable Codecov** for the repository at codecov.io
2. **Collect coverage from ALL test suites** (not just unit tests):

| Test Suite | Coverage Command | Output File | MANDATORY |
|------------|------------------|-------------|-----------|
| Unit | `phpunit -c UnitTests.xml --coverage-clover` | `.Build/coverage/unit.xml` | **YES** |
| Integration | `phpunit -c IntegrationTests.xml --coverage-clover` | `.Build/coverage/integration.xml` | **YES** |
| E2E | `phpunit -c E2ETests.xml --coverage-clover` | `.Build/coverage/e2e.xml` | **YES** |
| Functional | `phpunit -c FunctionalTests.xml --coverage-clover` | `.Build/coverage/functional.xml` | **YES** |
| JavaScript | `npm run test:coverage` | `coverage/lcov.info` | **YES** (if JS exists) |

3. **Upload ALL coverage files** to Codecov:
   ```yaml
   - uses: codecov/codecov-action@SHA # vX.Y.Z
     with:
       token: ${{ secrets.CODECOV_TOKEN }}  # MANDATORY - see below
       files: .Build/coverage/unit.xml,.Build/coverage/integration.xml,.Build/coverage/e2e.xml,coverage/lcov.info
       fail_ci_if_error: false
   ```

### CODECOV_TOKEN (MANDATORY)

**Never rely on tokenless uploads.** They fail for protected branches and are unreliable.

| Requirement | Implementation | Why |
|-------------|----------------|-----|
| Token in secrets | Add `CODECOV_TOKEN` to repo or org secrets | Authentication |
| Token in workflow | `token: ${{ secrets.CODECOV_TOKEN }}` | Required for protected branches |
| Org-level secret | Preferred for consistency across repos | Single point of management |

**Failure without token:**
```
Upload failed: {"message":"Token required because branch is protected"}
```

**Get token from:** https://app.codecov.io/gh/ORG/REPO/settings

**Add as org secret (recommended):**
```bash
# Organization-level (covers all repos)
gh secret set CODECOV_TOKEN --org netresearch --visibility all

# Or repository-level
gh secret set CODECOV_TOKEN --repo OWNER/REPO
```

### JavaScript Coverage (MANDATORY for projects with JS/TS)

When a project contains JavaScript or TypeScript files:

1. **vitest.config.js** MUST include lcov reporter for Codecov:
   ```javascript
   coverage: {
       provider: 'v8',
       reporter: ['text', 'json', 'html', 'lcov'],  // lcov REQUIRED for Codecov
       reportsDirectory: 'coverage',
   }
   ```

2. **CI workflow** MUST include JavaScript test job:
   ```yaml
   - uses: actions/setup-node@SHA # vX.Y.Z
     with:
       node-version: '22'
   - run: npm install
   - run: npm run test:coverage
   ```

3. **Codecov upload** MUST include `coverage/lcov.info`

### Verification Checklist

Before marking enterprise-readiness complete, verify ALL:

- [ ] README has CI badge linking to workflow
- [ ] README has Codecov badge (not "unknown")
- [ ] README has OpenSSF Scorecard badge (correct URL with `api.securityscorecards.dev`)
- [ ] README has OpenSSF Best Practices badge (correct PROJECT_ID, not placeholder)
- [ ] `.github/workflows/ci.yml` exists and uploads coverage
- [ ] `.github/workflows/codeql.yml` exists
- [ ] `.github/workflows/scorecard.yml` exists
- [ ] Codecov shows actual coverage percentage
- [ ] Scorecard shows actual score

**If any badge shows "unknown", "invalid", or placeholder ID - FIX IT. Do not proceed.**

---

## Assessment Workflow

1. **Discovery**: Identify platform (GitHub/GitLab), languages, existing CI/CD
2. **Scoring**: Apply checklists from references based on stack
3. **Badge Assessment**: Check OpenSSF criteria status
4. **Gap Analysis**: List missing controls by severity
5. **Implementation**: Apply fixes using scripts and templates
6. **Verification**: Re-score and compare (see Post-Implementation Verification)

---

## Post-Implementation Verification

**MANDATORY:** After implementing improvements, re-assess the project to verify gains.

### Re-Scoring Workflow

1. **Record baseline score** before making changes (save output)
2. **Implement improvements** following gap analysis priorities
3. **Re-run full assessment** using same criteria
4. **Compare scores** and document delta

### Verification Checklist

| Check | Before | After | Delta |
|-------|--------|-------|-------|
| OpenSSF Scorecard | _/10 | _/10 | +_ |
| Best Practices Badge | Level | Level | Upgrade? |
| Coverage % | _% | _% | +_% |
| Enterprise Score | _/100 | _/100 | +_ |

### Expected Outcomes

| Implementation | Expected Score Impact |
|----------------|----------------------|
| Add CI/CD workflows | +10-15 pts |
| Enable Codecov | +5-10 pts |
| Add CodeQL/Scorecard | +10-15 pts |
| SLSA provenance | +5-10 pts |
| Documentation (SECURITY.md, etc.) | +5-10 pts |

### Verification Commands

```bash
# OpenSSF Scorecard (re-run after changes merged to default branch)
scorecard --repo=github.com/ORG/REPO --format=json

# Coverage (after CI runs)
# Check Codecov dashboard or badge

# Best Practices (update at bestpractices.dev after implementing)
# Re-answer questions that are now satisfied
```

**If score did not improve as expected**, investigate:
- Did CI workflows run successfully?
- Are badges pointing to correct repository?
- Did changes merge to default branch (required for Scorecard)?

---

## Continuous Improvement

Enterprise readiness is not a one-time achievement. Maintain scores over time.

### Scheduled Re-Assessment

| Frequency | Scope | Trigger |
|-----------|-------|---------|
| **Weekly** | Badge status check | Automated (CI) |
| **Monthly** | Scorecard re-run | Scheduled workflow |
| **Quarterly** | Full enterprise assessment | Manual or milestone |
| **Per-release** | Supply chain verification | Release workflow |

### Automated Monitoring

Add badge health check to CI:

```yaml
# .github/workflows/badge-health.yml
name: Badge Health Check
on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6am
  workflow_dispatch:

jobs:
  check-badges:
    runs-on: ubuntu-latest
    steps:
      - name: Check Codecov
        run: |
          BADGE_URL="https://codecov.io/gh/${{ github.repository }}/graph/badge.svg"
          curl -sL "$BADGE_URL" | grep -q "unknown" && echo "::warning::Codecov badge shows unknown" || true

      - name: Check Scorecard
        run: |
          SCORE=$(curl -s "https://api.securityscorecards.dev/projects/github.com/${{ github.repository }}" | jq -r '.score // "N/A"')
          echo "Current Scorecard: $SCORE/10"
          if [ "$SCORE" != "N/A" ] && [ "$(echo "$SCORE < 7" | bc -l)" = "1" ]; then
            echo "::warning::Scorecard dropped below 7.0"
          fi
```

### Regression Detection

Watch for these warning signs:

| Signal | Detection | Response |
|--------|-----------|----------|
| Scorecard drop > 1pt | Weekly check | Investigate changed checks |
| Badge shows "unknown" | CI check | Verify token/configuration |
| CVE in dependency | Dependabot/Renovate | Priority update PR |
| Failed security scan | CI workflow | Block release until fixed |
| Coverage drop > 5% | PR check | Require coverage recovery |

### Dependency Update Cadence

| Update Type | Frequency | Automation |
|-------------|-----------|------------|
| Security patches | Immediate | Auto-merge if tests pass |
| Minor updates | Weekly | Renovate/Dependabot PR |
| Major updates | Monthly review | Manual approval required |

## Dependency CVE Workflow

When assessing enterprise readiness, **always run dependency audit** as part of discovery:

```bash
# PHP/Composer
composer audit

# Node.js
npm audit

# Python
pip-audit

# Go
govulncheck ./...
```

### CVE Handling Best Practice

**Separate dependency updates from code changes:**

| PR Type | Content | Why |
|---------|---------|-----|
| Code changes | Business logic, bug fixes, features | Reviewable, testable in isolation |
| Dependency updates | `composer update`, version bumps | Clear diff, easy rollback if issues |

**Real-world example from t3x-cowriter review:**
- Found 4 CVEs during enterprise assessment
- CVE fixes required `composer update typo3/cms-core typo3/cms-backend`
- Kept separate from code fixes (JS bug, AGENTS.md updates) for clean PR history

### CVE Severity Response

| Severity | Response Time | Action |
|----------|---------------|--------|
| CRITICAL | Immediate | Hotfix PR, expedited review |
| HIGH | 24-48 hours | Priority PR, security review |
| MEDIUM | 1 week | Normal PR cycle |
| LOW | Next release | Batch with other updates |

### CI Integration

Add dependency audit to CI pipeline:

```yaml
# .github/workflows/ci.yml
- name: Security audit
  run: composer audit --format=plain
```

## Reference Files (Load Based on Stack)

| Reference | When to Load |
|-----------|--------------|
| `references/general.md` | Always (universal 60 pts) |
| `references/github.md` | GitHub-hosted projects (40 pts) |
| `references/go.md` | Go projects (20 pts) |
| `references/openssf-badge-silver.md` | Pursuing Silver badge |
| `references/openssf-badge-gold.md` | Pursuing Gold badge |

## Quality & Process References (Language-Agnostic)

| Reference | When to Load |
|-----------|--------------|
| `references/code-review.md` | Code review, PR quality checks |
| `references/documentation.md` | ADRs, API docs, migration guides, changelogs |
| `references/ci-patterns.md` | CI/CD pipelines, Git hooks, quality gates |

### Explicit Content Triggers

When reviewing PRs or code, load `references/code-review.md` for the comprehensive checklist covering test resource management, state mutation, defensive enum handling, documentation accuracy, and defensive code coverage.

When writing ADRs (Architecture Decision Records), load `references/documentation.md` for templates, file organization, and required sections (Context, Decision, Consequences, Alternatives).

When writing changelogs or release notes, load `references/documentation.md` for Keep a Changelog format and conventional commit mapping.

When writing API documentation or migration guides, load `references/documentation.md` for structure patterns and completeness checklists.

When configuring CI/CD pipelines, load `references/ci-patterns.md` for comprehensive pipeline structure, job ordering, and quality gates.

When setting up Git hooks (pre-commit/pre-push), load `references/ci-patterns.md` for the hook division strategy and Lefthook configuration.

When enforcing coverage thresholds, load `references/ci-patterns.md` for threshold tables and enforcement patterns.

When handling signed commits with rebase-only merge, load `references/ci-patterns.md` for the local fast-forward merge workflow.

## Implementation Guides

| Guide | Purpose |
|-------|---------|
| `references/quick-start-guide.md` | Getting started |
| `references/dco-implementation.md` | DCO enforcement |
| `references/signed-releases.md` | Cosign/GPG signing |
| `references/reproducible-builds.md` | Deterministic builds |
| `references/security-hardening.md` | TLS, headers, validation |
| `references/solo-maintainer-guide.md` | N/A criteria justification |
| `references/branch-coverage.md` | Gold 80% branch coverage |

## Automation Scripts

| Script | Purpose |
|--------|---------|
| `scripts/verify-badge-criteria.sh` | Verify OpenSSF badge criteria |
| `scripts/check-coverage-threshold.sh` | Statement coverage check |
| `scripts/check-branch-coverage.sh` | Branch coverage (Gold) |
| `scripts/add-spdx-headers.sh` | Add SPDX headers (Gold) |
| `scripts/verify-signed-tags.sh` | Tag signature verification |
| `scripts/verify-review-requirements.sh` | PR review requirements |

## Document Templates

Templates in `assets/templates/`:
- `GOVERNANCE.md` - Project governance (Silver)
- `ARCHITECTURE.md` - Technical docs (Silver)
- `CODE_OF_CONDUCT.md` - Contributor Covenant v3.0
- `SECURITY_AUDIT.md` - Security audit (Gold)
- `BADGE_EXCEPTIONS.md` - N/A justifications

## CI Workflow Templates

GitHub Actions workflows in `assets/workflows/`:

| Workflow | Purpose |
|----------|---------|
| `scorecard.yml` | OpenSSF Scorecard security analysis |
| `codeql.yml` | Semantic code security scanning |
| `dependency-review.yml` | PR dependency CVE/license check |
| `slsa-provenance.yml` | SLSA Level 3 build attestation |
| `dco-check.yml` | Developer Certificate of Origin |

Copy workflows to `.github/workflows/` and pin action versions with SHA hashes.

## Scoring Interpretation

| Score | Grade | Status |
|-------|-------|--------|
| 90-100 | A | Enterprise Ready |
| 80-89 | B | Production Ready |
| 70-79 | C | Development Ready |
| 60-69 | D | Basic |
| <60 | F | Not Ready |

## Code Review Quick Checklist

Before approving PRs, verify (see `references/code-review.md` for details):

- [ ] **One resource per test** - No duplicate instances
- [ ] **State mutation complete** - Tracking fields updated after operations
- [ ] **Defensive enum handling** - `Valid()` method, `default` case, tested
- [ ] **Documentation accurate** - Claims match benchmarks, trade-offs noted
- [ ] **Platform code marked** - Limitations documented, alternatives provided
- [ ] **Defensive code tested** - Error paths and edge cases covered

## Critical Rules

- **NEVER** interpolate `${{ github.event.* }}` in `run:` blocks (script injection)
- **NEVER** guess action versions - always fetch from GitHub API
- **ALWAYS** use SHA pins for actions with version comments
- **ALWAYS** verify commit hashes against official tags

## Related Skills

| Skill | Purpose |
|-------|---------|
| `go-development` | Go code patterns, Makefile interface, testing |
| `github-project` | Repository setup, branch protection, auto-merge |
| `security-audit` | Deep security audits (OWASP, XXE, SQLi) |
| `git-workflow` | Git branching, commits, PR workflows |

## Resources

- [OpenSSF Scorecard](https://securityscorecards.dev/)
- [Best Practices Badge](https://www.bestpractices.dev/)
- [SLSA Framework](https://slsa.dev/)
- [S2C2F](https://github.com/ossf/s2c2f)

---

> **Contributing:** Improvements to this skill should be submitted to the source repository:
> https://github.com/netresearch/enterprise-readiness-skill
