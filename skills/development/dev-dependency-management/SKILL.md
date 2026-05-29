---
name: dev-dependency-management
description: Package and dependency management patterns across ecosystems (npm, pip, cargo, maven). Covers lockfiles, semantic versioning, dependency security scanning, update strategies, monorepo workspaces, transitive dependencies, and avoiding dependency hell.
---

# Dependency Management — Production Patterns

**Modern Best Practices (2025)**: Lockfile-first workflows, automated security scanning (Dependabot, Snyk), semantic versioning, minimal dependencies principle, monorepo workspaces (pnpm, Nx), supply chain security (SBOM, signatures), and reproducible builds.

---

## When to Use This Skill

Claude should invoke this skill when a user requests:

- Adding new dependencies to a project
- Updating existing dependencies safely
- Resolving dependency conflicts or version mismatches
- Auditing dependencies for security vulnerabilities
- Understanding lockfile management and reproducible builds
- Setting up monorepo workspaces (pnpm, npm, yarn)
- Managing transitive dependencies and overrides
- Choosing between similar packages (bundle size, maintenance, security)
- Dependency version constraints and semantic versioning
- Dependency security best practices and supply chain security
- Troubleshooting "dependency hell" scenarios
- Package manager configuration and optimization
- Creating reproducible builds across environments

---

## Quick Reference

| Task | Tool/Command | Key Action | When to Use |
|------|--------------|------------|-------------|
| **Install from lockfile** | `npm ci`, `poetry install`, `cargo build` | Clean install, reproducible | CI/CD, production deployments |
| **Add dependency** | `npm install <pkg>`, `poetry add <pkg>` | Updates lockfile automatically | New feature needs library |
| **Update dependencies** | `npm update`, `poetry update`, `cargo update` | Updates within version constraints | Monthly/quarterly maintenance |
| **Check for vulnerabilities** | `npm audit`, `pip-audit`, `cargo audit` | Scans for known CVEs | Before releases, weekly |
| **View dependency tree** | `npm ls`, `pnpm why`, `pipdeptree` | Shows transitive dependencies | Debugging conflicts |
| **Override transitive dep** | `overrides` (npm), `pnpm.overrides` | Force specific version | Security patch, conflict resolution |
| **Monorepo setup** | `pnpm workspaces`, `npm workspaces` | Shared dependencies, cross-linking | Multi-package projects |
| **Check outdated** | `npm outdated`, `poetry show --outdated` | Lists available updates | Planning update sprints |

---

## Decision Tree: Dependency Management

```text
User needs: [Dependency Task]
    ├─ Adding new dependency?
    │   ├─ Check: Do I really need this? (Can implement in <100 LOC?)
    │   ├─ Check: Is it well-maintained? (Last commit <6 months, >10k downloads/week)
    │   ├─ Check: Bundle size impact? (Use Bundlephobia for JS)
    │   ├─ Check: Security risks? (`npm audit`, Snyk)
    │   └─ If all checks pass → Add with `npm install <pkg>` → Commit lockfile
    │
    ├─ Updating dependencies?
    │   ├─ Security vulnerability? → `npm audit fix` → Test → Deploy immediately
    │   ├─ Routine update?
    │       ├─ Patch versions → `npm update` → Safe, do frequently
    │       ├─ Minor/major → Check CHANGELOG → Test in staging → Update gradually
    │       └─ All at once → [FAIL] RISKY → Update in batches instead
    │
    ├─ Dependency conflict?
    │   ├─ Transitive dependency issue?
    │       ├─ View tree: `npm ls <package>`
    │       ├─ Use overrides sparingly: `overrides` in package.json
    │       └─ Document why override is needed
    │   └─ Peer dependency mismatch?
    │       └─ Check version compatibility → Update parent or child
    │
    ├─ Monorepo project?
    │   ├─ Use pnpm workspaces (fastest, best)
    │   ├─ Shared deps → Root package.json
    │   ├─ Package-specific → Package directories
    │   └─ Use Nx or Turborepo for task caching
    │
    └─ Choosing package manager?
        ├─ New project → **pnpm** (3x faster, 1/3 disk space)
        ├─ Existing npm project → Migrate or stay (check team preference)
        ├─ Python → **Poetry** (apps), pip+venv (simple)
        └─ Data science → **conda** (environment management)
```

---

## Navigation: Core Patterns

### Lockfile Management

**[`resources/lockfile-management.md`](resources/lockfile-management.md)**

Lockfiles ensure reproducible builds by recording exact versions of all dependencies (direct + transitive). Essential for preventing "works on my machine" issues.

- Golden rules (always commit, never edit manually, regenerate on changes)
- Commands by ecosystem (npm ci, poetry install, cargo build)
- Troubleshooting lockfile conflicts
- CI/CD integration patterns

### Semantic Versioning (SemVer)

**[`resources/semver-guide.md`](resources/semver-guide.md)**

Understanding version constraints (`^`, `~`, exact) and how to specify dependency ranges safely.

- SemVer format (MAJOR.MINOR.PATCH)
- Version constraint syntax (caret, tilde, exact)
- Recommended strategies by project type
- Cross-ecosystem version management

### Dependency Security Auditing

**[`resources/security-scanning.md`](resources/security-scanning.md)**

Automated security scanning, vulnerability management, and supply chain security best practices.

- Automated tools (Dependabot, Snyk, GitHub Advanced Security)
- Running audits (npm audit, pip-audit, cargo audit)
- CI integration and alert configuration
- Incident response workflows

### Dependency Selection

**[`resources/dependency-selection-guide.md`](resources/dependency-selection-guide.md)**

Deciding whether to add a new dependency and choosing between similar packages.

- Minimal dependencies principle (best dependency is the one you don't add)
- Evaluation checklist (maintenance, bundle size, security, alternatives)
- Choosing between similar packages (comparison matrix)
- When to reject a dependency

### Update Strategies

**[`resources/update-strategies.md`](resources/update-strategies.md)**

Keeping dependencies up to date safely while minimizing breaking changes and security risks.

- Update strategies (continuous, scheduled, security-only)
- Safe update workflow (check outdated, categorize risk, test, deploy)
- Automated update tools (Dependabot, Renovate, npm-check-updates)
- Handling breaking changes and rollback plans

### Monorepo Management

**[`resources/monorepo-patterns.md`](resources/monorepo-patterns.md)**

Managing multiple related packages in a single repository with shared dependencies.

- Workspace tools (pnpm, npm, yarn workspaces)
- Monorepo structure and organization
- Build optimization (Nx, Turborepo)
- Versioning and publishing strategies

### Transitive Dependencies

**[`resources/transitive-dependencies.md`](resources/transitive-dependencies.md)**

Dealing with dependencies of your dependencies (indirect dependencies).

- Viewing dependency trees (npm ls, pnpm why, pipdeptree)
- Resolving transitive conflicts (overrides, resolutions, constraints)
- Security risks and version conflicts
- Best practices (use sparingly, document, test)

### Ecosystem-Specific Guides

**[`resources/ecosystem-guides.md`](resources/ecosystem-guides.md)**

Language and package-manager-specific best practices.

- Node.js (npm, yarn, pnpm comparison and best practices)
- Python (pip, poetry, conda)
- Rust (cargo), Go (go mod), Java (maven, gradle)
- PHP (composer), .NET (nuget)

### Anti-Patterns

**[`resources/anti-patterns.md`](resources/anti-patterns.md)**

Common mistakes to avoid when managing dependencies.

- Critical anti-patterns (not committing lockfiles, wildcards, ignoring audits)
- Dangerous anti-patterns (never updating, deprecated packages)
- Moderate anti-patterns (overusing overrides, ignoring peer deps)

---

## Navigation: Templates

### Node.js

**[`templates/nodejs/`](templates/nodejs/)**

- [`package-json-template.json`](templates/nodejs/package-json-template.json) - Production-ready package.json with best practices
- `npmrc-template.txt` - Team configuration for npm
- [`pnpm-workspace-template.yaml`](templates/nodejs/pnpm-workspace-template.yaml) - Monorepo workspace setup

### Python

**[`templates/python/`](templates/python/)**

- [`pyproject-toml-template.toml`](templates/python/pyproject-toml-template.toml) - Poetry configuration with best practices

### Automation

**[`templates/automation/`](templates/automation/)**

- [`dependabot-config.yml`](templates/automation/dependabot-config.yml) - GitHub Dependabot configuration
- [`renovate-config.json`](templates/automation/renovate-config.json) - Renovate Bot configuration
- [`audit-checklist.md`](templates/automation/audit-checklist.md) - Security audit workflow
- **[`template-supply-chain-security.md`](templates/automation/template-supply-chain-security.md)** - **NEW** SBOM, provenance, vulnerability management
- [`template-dependency-upgrade-playbook.md`](templates/automation/template-dependency-upgrade-playbook.md) - Upgrade batching, rollout, rollback
- [`template-sbom-vuln-triage-checklist.md`](templates/automation/template-sbom-vuln-triage-checklist.md) - SBOM mapping + vulnerability triage

---

## Supply Chain Security

**[templates/automation/template-supply-chain-security.md](templates/automation/template-supply-chain-security.md)** — Production-grade dependency security.

Related templates:
- [templates/automation/template-dependency-upgrade-playbook.md](templates/automation/template-dependency-upgrade-playbook.md)
- [templates/automation/template-sbom-vuln-triage-checklist.md](templates/automation/template-sbom-vuln-triage-checklist.md)

### Key Sections

- **SBOM Generation** — CycloneDX, SPDX formats; CI/CD integration
- **Provenance & Attestation** — SLSA levels, Sigstore signing, npm provenance
- **Vulnerability Management** — Triage workflow, severity SLAs, scanning tools
- **Upgrade Playbooks** — Batching strategy, rollback procedures
- **Pinning & Reproducibility** — Lockfiles, hash pinning, version constraints

### Do / Avoid

#### GOOD: Do

- Generate SBOM for every release
- Sign release artifacts (Sigstore/cosign)
- Run vulnerability scans in CI/CD
- Fix critical vulnerabilities within 24 hours
- Use lockfiles for reproducible builds
- Verify npm package provenance
- Batch non-security updates by risk level

#### BAD: Avoid

- Publishing without SBOM
- Using unsigned packages in production
- Ignoring vulnerability scanner output
- Updating all dependencies at once
- Using wildcard version ranges (`*`, `>=`)
- Committing without updating lockfile
- Bypassing security gates "just this once"

### Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **No SBOM** | Can't respond to supply chain attacks | Generate SBOM in CI/CD |
| **Unsigned artifacts** | Tampering undetectable | Sign with Sigstore |
| **Floating versions** | Build not reproducible | Use lockfiles + exact versions |
| **All-at-once updates** | Hard to bisect regressions | Batch by risk level |
| **npm install in CI** | Non-deterministic | Use `npm ci` |
| **No audit gate** | Vulnerabilities ship to prod | Gate deployments on audit |

---

## Optional: AI/Automation

> **Note**: AI assists with triage but security decisions need human judgment.

- **Automated PR triage** — Categorize dependency updates by risk
- **Changelog summarization** — Summarize breaking changes in updates
- **Vulnerability correlation** — Link CVEs to affected packages

### Bounded Claims

- AI cannot determine business risk acceptance
- Automated fixes require security team review
- Vulnerability severity context needs human validation

---

## Quick Decision Matrix

| Scenario | Recommendation |
|----------|----------------|
| Adding new dependency | Check Bundlephobia, npm audit, weekly downloads, last commit |
| Updating dependencies | Use `npm outdated`, update in batches, test in staging |
| Security vulnerability found | Use `npm audit fix`, review CHANGELOG, test, deploy immediately |
| Monorepo setup | Use **pnpm workspaces** or Nx/Turborepo for build caching |
| Transitive conflict | Use `overrides` sparingly, document why, test thoroughly |
| Choosing package manager | **pnpm** (fastest), npm (most compatible), yarn (good middle) |
| Python environment | **Poetry** (apps), pip+venv (simple), conda (data science) |

---

## Core Principles

### 1. Always Commit Lockfiles

Lockfiles ensure reproducible builds across environments. Never add them to `.gitignore`.

**Exception**: Don't commit `Cargo.lock` for Rust libraries (only for applications).

### 2. Use Semantic Versioning

Use caret (`^`) for most dependencies, exact versions for mission-critical, avoid wildcards (`*`).

```json
{
  "dependencies": {
    "express": "^4.18.0",  // Allows patches and minors
    "critical-lib": "1.2.3"  // Exact for critical
  }
}
```

### 3. Audit Dependencies Regularly

Run security audits weekly, fix critical vulnerabilities immediately.

```bash
npm audit
npm audit fix
```

### 4. Minimize Dependencies

The best dependency is the one you don't add. Ask: Can I implement this in <100 LOC?

### 5. Update Regularly

Update monthly or quarterly. Don't let technical debt accumulate.

```bash
npm outdated
npm update
```

### 6. Use Overrides Sparingly

Only override transitive dependencies for security patches or conflicts. Document why.

```json
{
  "overrides": {
    "axios": "1.6.0"  // CVE-2023-xxxxx fix
  }
}
```

---

## Related Skills

For complementary workflows and deeper dives:

- [`dev-api-design`](../dev-api-design/SKILL.md) - API versioning strategies, dependency injection patterns
- [`git-workflow`](../git-workflow/SKILL.md) - Git workflows for managing lockfile conflicts, branching strategies
- [`qa-testing-strategy`](../qa-testing-strategy/SKILL.md) - Testing strategies for dependency updates, integration testing
- [`software-security-appsec`](../software-security-appsec/SKILL.md) - OWASP Top 10, cryptography standards, authentication patterns
- [`ops-devops-platform`](../ops-devops-platform/SKILL.md) - CI/CD pipelines, Docker containerization, DevSecOps, deployment automation
- [`docs-codebase`](../docs-codebase/SKILL.md) - Documenting dependency choices, ADRs, changelogs

---

## External Resources

See [`data/sources.json`](data/sources.json) for 82 curated resources:

- **Package managers**: npm, pnpm, Yarn, pip, Poetry, Cargo, Go modules, Maven, Composer
- **Semantic versioning**: SemVer spec, version calculators, constraint references
- **Security tools**: Snyk, Dependabot, GitHub Advanced Security, OWASP Dependency-Check, pip-audit, cargo-audit, Socket.dev, Renovate
- **Lockfile management**: Official docs for package-lock.json, poetry.lock, Cargo.lock, pnpm-lock.yaml
- **Monorepo tools**: pnpm workspaces, npm workspaces, Yarn workspaces, Nx, Turborepo, Lerna, Bazel
- **Analysis tools**: Bundlephobia, npm-check-updates, depcheck, pipdeptree, cargo tree
- **Supply chain security**: SLSA framework, SBOM (CISA), Sigstore, npm provenance, OpenSSF Scorecard
- **Best practices**: npm/Poetry/Cargo guides, ACM Queue articles, dependency hell references
- **Version management**: nvm, pyenv, rustup, asdf
- **Learning resources**: npm guides, Python Packaging User Guide, Rust Book, Monorepo.tools

---

## Usage Notes

**For Claude:**

- Use this skill when users need dependency management guidance
- Reference specific resources based on the task (lockfiles, security, updates)
- Provide ecosystem-specific guidance (Node.js, Python, Rust)
- Always recommend security audits and reproducible builds
- Encourage minimal dependencies and regular updates
- Link to templates for common configurations

**Best Practices:**

- Always commit lockfiles (except Cargo.lock for libraries)
- Use semantic versioning (caret for most deps, exact for critical)
- Audit dependencies weekly (`npm audit`, `pip-audit`, `cargo audit`)
- Update dependencies monthly or quarterly (not all at once)
- Choose package manager based on project needs (pnpm for speed, Poetry for Python apps)
- Document dependency choices in ADRs (Architecture Decision Records)

---

> **Success Criteria:** Dependencies are minimal, well-maintained, secure, reproducible across environments, and regularly audited for vulnerabilities.
