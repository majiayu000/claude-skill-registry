---
name: dependency-update
description: Safe dependency update workflow. Use when upgrading packages, resolving vulnerability alerts, updating major versions, or auditing dependency health across project ecosystems.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Dependency Update Skill

Safe and systematic dependency updates with vulnerability management, license checking, and rollback planning.

## When to Use

| Trigger | Priority | Description |
|---------|----------|-------------|
| **Security Vulnerability** | Critical | Known CVE in dependency |
| **Monthly Maintenance** | High | Regular update cycle |
| **Major Version** | Medium | New major version available |
| **Pre-Release** | High | Before production deployments |
| **Breaking Bug** | Critical | Bug in current dependency |

---

## Update Strategy

### Update Types

| Type | Risk | Frequency | Testing |
|------|------|-----------|---------|
| **Patch** (x.x.1) | Low | Weekly/Auto | Basic |
| **Minor** (x.1.0) | Low-Medium | Monthly | Standard |
| **Major** (1.0.0) | High | Quarterly | Comprehensive |

### Semantic Versioning

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └── Bug fixes (backward compatible)
  │     └──────── New features (backward compatible)
  └────────────── Breaking changes
```

---

## Prerequisites

Before starting:

- [ ] All tests passing
- [ ] Clean git working directory
- [ ] Recent backup/checkpoint
- [ ] Time for testing and potential rollback
- [ ] Access to changelogs/release notes

---

## Update Process

```
Phase 1: Audit Dependencies
    ↓
Phase 2: Check Vulnerabilities
    ↓
Phase 3: Check License Compatibility
    ↓
Phase 4: Plan Updates
    ↓
Phase 5: Execute Updates
    ↓
Phase 6: Test & Validate
    ↓
Phase 7: Document & Deploy
```

---

## Phase 1: Audit Dependencies

List outdated dependencies using ecosystem-specific tools:

```bash
# Node.js
npm outdated

# Python
pip list --outdated

# Go
go list -u -m all

# Rust
cargo outdated

# Ruby
bundle outdated
```

Create update inventory prioritizing direct dependencies over transitive ones.

---

## Phase 2: Check Vulnerabilities

Run security audits:

```bash
# Node.js: npm audit
# Python: pip-audit or safety check
# Go: govulncheck ./...
# Rust: cargo audit
# Ruby: bundle audit check
```

Prioritize by severity: Critical (hours) → High (days) → Moderate (weeks) → Low (monthly).

---

## Phase 3: Check License Compatibility

Check licenses before adding dependencies:

```bash
# Node.js: npx license-checker --summary
# Python: pip-licenses
```

Avoid: GPL-3.0, AGPL-3.0, SSPL, Unlicensed (require legal review).
Safe: MIT, Apache-2.0, BSD, ISC.

---

## Phase 4: Plan Updates

**Priority**: Security → Patches → Minor → Major

Update strategies:
- **Individual**: Major updates, risky dependencies
- **Batched**: Patches and minor updates together
- **All at once**: Only for fresh projects with comprehensive tests

Create update plan grouping by priority and risk level.

---

## Phase 5: Execute Updates

Create branch: `git checkout -b chore/dependency-updates-YYYY-MM`

Update commands by ecosystem:

```bash
# Individual: npm install pkg@ver | pip install pkg==ver | go get pkg@ver
# Batch: npm update | pip install -U pkg1 pkg2 | go get -u ./... | cargo update
```

Verify lock files updated. Commit with descriptive messages following conventional commits.

---

## Phase 6: Test & Validate

Run comprehensive validation:

```bash
# Tests: npm test | pytest | go test ./... | cargo test
# Types: npm run typecheck | mypy . | cargo check
# Lint: npm run lint | ruff check . | golangci-lint run | cargo clippy
# Build: npm run build | go build ./... | cargo build --release
```

For major updates, verify critical paths manually.

---

## Phase 7: Document & Deploy

Create PR documenting:
- Security fixes with CVE numbers
- Package updates table
- Breaking changes addressed
- Testing checklist completed
- Rollback plan

Deploy: Dev → Staging → Production (with validation at each stage).

---

## Rollback Procedures

### If Tests Fail

```bash
# Reset to before updates
git checkout package.json package-lock.json
npm install
```

### If Production Issues

```bash
# Revert the commit
git revert <update-commit-hash>
npm install
# Deploy revert
```

### Pin Problematic Dependency

```json
// package.json
{
  "dependencies": {
    "problematic-package": "1.2.3"  // Pin to working version
  },
  "resolutions": {
    "problematic-package": "1.2.3"  // Force transitive deps
  }
}
```

---

## Quick Reference

### Commands by Language

| Task | Node.js | Python | Go | Rust |
|------|---------|--------|----|------|
| List outdated | `npm outdated` | `pip list --outdated` | `go list -u -m all` | `cargo outdated` |
| Security audit | `npm audit` | `pip-audit` | `govulncheck ./...` | `cargo audit` |
| Update all | `npm update` | `pip install -U` | `go get -u ./...` | `cargo update` |
| Update one | `npm install pkg@ver` | `pip install pkg==ver` | `go get pkg@ver` | `cargo update -p pkg` |

---

## Checklist

### Pre-Update
- [ ] Tests passing
- [ ] Clean git state
- [ ] Outdated list generated
- [ ] Vulnerabilities checked
- [ ] Licenses checked
- [ ] Update plan created

### During Update
- [ ] Branch created
- [ ] Updates applied
- [ ] Lock files updated
- [ ] Commits atomic and descriptive

### Post-Update
- [ ] All tests pass
- [ ] Type checks pass
- [ ] Lint passes
- [ ] Build succeeds
- [ ] Manual testing done
- [ ] PR created
- [ ] Rollback plan ready

---

## Related Workflows

- [security-audit.md](../../workflows/security-audit.md) - Includes vulnerability scanning
- [code-review.md](../../workflows/code-review.md) - Review updated code
- [troubleshooting.md](../../workflows/troubleshooting.md) - If updates cause issues

---

## Extended Resources

For detailed per-ecosystem commands, verbose examples, and automation configuration, see:
- [references/process.md](references/process.md) - Comprehensive ecosystem-specific processes
