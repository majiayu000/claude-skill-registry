---
name: dependency-management
description: Use when the Integrator is managing project dependencies, updating packages, resolving version conflicts, auditing for vulnerabilities, or maintaining lock files. Activates when working with package.json, requirements.txt, Cargo.toml, or any dependency configuration.
version: 1.0.0
---

# Dependency Management Expertise

## When This Applies

Apply this guidance when:
- Adding, updating, or removing project dependencies
- Resolving version conflicts between packages
- Auditing dependencies for security vulnerabilities
- Maintaining lock files
- Evaluating new dependencies

## Evaluating New Dependencies

Before adding a dependency, check:

| Criteria | Check |
|----------|-------|
| **Necessity** | Can this be done in 20 lines of code instead? |
| **Maintenance** | Last commit < 6 months ago? Active maintainer? |
| **Popularity** | Downloads/stars indicate community trust |
| **License** | Compatible with project license? |
| **Size** | Reasonable bundle/install size? |
| **Security** | Known vulnerabilities? |
| **Dependencies** | How many transitive deps does it bring? |

### Decision Framework

- **Add it** if: Well-maintained, widely used, saves significant work
- **Skip it** if: Unmaintained, huge dependency tree, simple to implement yourself
- **Ask Architect** if: Major new framework, changes the architecture

## Version Management

### Semantic Versioning

- `^1.2.3` — Allow minor and patch updates (recommended for most deps)
- `~1.2.3` — Allow only patch updates (for stability-critical deps)
- `1.2.3` — Exact version (for known-fragile deps only)

### Update Strategy

1. **Patch updates** (1.2.x): Apply regularly, low risk
2. **Minor updates** (1.x.0): Test thoroughly, check changelogs
3. **Major updates** (x.0.0): Plan carefully, may have breaking changes — create a task for it

## Lock File Management

- **Always commit lock files** (`package-lock.json`, `poetry.lock`, `Cargo.lock`)
- Never manually edit lock files
- Regenerate if corrupted: delete and reinstall
- Review lock file diffs in commits — large changes deserve scrutiny

## Security Auditing

Run security audits regularly:
- **npm**: `npm audit`
- **Python**: `pip-audit` or `safety check`
- **Rust**: `cargo audit`
- **Go**: `govulncheck`

### Vulnerability Response

| Severity | Action |
|----------|--------|
| **Critical** | Update immediately, create hotfix task |
| **High** | Update within current sprint |
| **Medium** | Schedule for next update cycle |
| **Low** | Track, update at convenience |

## Dependency Conflicts

When two packages require incompatible versions:
1. Check if either can be updated to resolve the conflict
2. Check if an alternative package exists without the conflict
3. If unavoidable, document the constraint and workaround
4. Notify Architect if the conflict affects architecture decisions
