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

## Assessment Workflow

1. **Discovery**: Identify platform (GitHub/GitLab), languages, existing CI/CD
2. **Scoring**: Apply checklists from references based on stack
3. **Badge Assessment**: Check OpenSSF criteria status
4. **Gap Analysis**: List missing controls by severity
5. **Implementation**: Apply fixes using scripts and templates

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
- `CODE_OF_CONDUCT.md` - Contributor Covenant
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
