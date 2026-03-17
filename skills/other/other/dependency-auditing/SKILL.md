---
name: dependency-auditing
description: "Use when auditing supply chain security. Covers dependency scanning tools, CVE triage workflows, SBOM generation, license compliance, and Dependabot/Renovate configuration."
---

# Dependency Auditing

## The Principle

```
EVERY DEPENDENCY IS AN ATTACK SURFACE.
Audit proactively, not after the breach.
```

Your app's security is only as strong as its weakest transitive dependency.

## Tool Selection by Ecosystem

| Ecosystem | Audit Tool | Lock File | Notes |
|-----------|-----------|-----------|-------|
| npm/yarn | `npm audit` / `yarn audit` | package-lock.json / yarn.lock | Built-in, JSON output for CI |
| pnpm | `pnpm audit` | pnpm-lock.yaml | Same flags as npm audit |
| Python (pip) | `pip-audit` | requirements.txt / poetry.lock | Queries OSV database |
| Python (pipenv) | `pipenv check` | Pipfile.lock | Uses Safety DB |
| Rust | `cargo audit` | Cargo.lock | RustSec advisory DB |
| Go | `govulncheck` | go.sum | Official Go tool, call-graph aware |
| Ruby | `bundler-audit` | Gemfile.lock | Ruby Advisory DB |
| Java/Kotlin | OWASP Dependency-Check / `gradle dependencyCheckAnalyze` | build.gradle.lock | NVD database |
| .NET | `dotnet list package --vulnerable` | packages.lock.json | Built-in since .NET 6 |

```bash
# Quick audit commands
npm audit --production          # Skip devDependencies
pip-audit -r requirements.txt   # Python
cargo audit                     # Rust
govulncheck ./...               # Go (analyzes actual call graph)
bundler-audit check --update    # Ruby (update advisory DB first)
```

## CVE Triage Workflow

### Step 1: Severity Assessment

| CVSS Score | Severity | SLA |
|------------|----------|-----|
| 9.0-10.0 | Critical | Fix within 24 hours |
| 7.0-8.9 | High | Fix within 7 days |
| 4.0-6.9 | Medium | Fix within 30 days |
| 0.1-3.9 | Low | Fix within 90 days or accept |

### Step 2: Exploitability Analysis

Not all CVEs are exploitable in your context. Ask:

1. **Is the vulnerable code path reachable?** (`govulncheck` does this automatically for Go)
2. **Is the vulnerable feature used?** (e.g., XML parsing CVE irrelevant if you only parse JSON)
3. **Is it exposed to untrusted input?** (internal-only service vs public API)
4. **Are there existing mitigations?** (WAF, input validation, sandboxing)

### Step 3: Decision Matrix

| Exploitable? | Upgrade Available? | Action |
|:---:|:---:|--------|
| Yes | Yes | Upgrade immediately |
| Yes | No | Apply workaround, monitor for patch, consider replacing dependency |
| No | Yes | Upgrade in next scheduled maintenance |
| No | No | Document risk acceptance with justification, set review date |

### Step 4: Response Options

| Response | When |
|----------|------|
| **Upgrade** | Patch version available, minimal breaking changes |
| **Patch** | Fork and patch if maintainer is unresponsive (last resort) |
| **Replace** | Dependency is unmaintained, better alternatives exist |
| **Mitigate** | Can't upgrade yet; add compensating controls (WAF rule, input validation) |
| **Accept** | Low risk, not exploitable in context; document and review quarterly |

## SBOM Generation

Software Bill of Materials -- inventory of all components in your software.

### Why SBOM Matters
- Required by US Executive Order 14028 for government contracts
- Enables rapid response when new CVEs drop (search your SBOM)
- License compliance auditing at scale

### Tools and Formats

| Tool | Format | Best For |
|------|--------|----------|
| `syft` (Anchore) | CycloneDX, SPDX | Container images, multi-ecosystem |
| `cdxgen` | CycloneDX | JS/Java/Python, CI-friendly |
| `trivy` | CycloneDX, SPDX | Container + filesystem scanning |
| `sbom-tool` (Microsoft) | SPDX | .NET ecosystems |

```bash
# Generate SBOM with syft
syft . -o cyclonedx-json > sbom.json
syft . -o spdx-json > sbom.spdx.json

# Scan container image
syft myimage:latest -o cyclonedx-json > sbom.json

# Scan SBOM for vulnerabilities
grype sbom:./sbom.json
```

## License Compliance

### License Categories

| Category | Licenses | Policy |
|----------|----------|--------|
| Permissive (safe) | MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC | Allow |
| Weak copyleft (review) | LGPL-2.1, LGPL-3.0, MPL-2.0 | Allow with conditions (dynamic linking OK, modifications must share) |
| Strong copyleft (restrict) | GPL-2.0, GPL-3.0, AGPL-3.0 | Block for proprietary software |
| No license | Unlicensed | Block (no license = all rights reserved) |

### Scanning Tools

```bash
# npm
npx license-checker --onlyAllow "MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC"

# Python
pip install pip-licenses
pip-licenses --fail-on "GPL-2.0;GPL-3.0;AGPL-3.0"

# Multi-ecosystem
licensee detect .
```

## Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 10
    groups:
      dev-dependencies:
        dependency-type: "development"
        update-types: ["minor", "patch"]
      production-minor-patch:
        dependency-type: "production"
        update-types: ["minor", "patch"]
    # Major production upgrades get individual PRs
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]
    # Except security updates -- always allow
    security-updates:
      open-pull-requests-limit: 20

  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      all-minor-patch:
        update-types: ["minor", "patch"]

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Renovate Configuration

```json5
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "schedule": ["before 7am on Monday"],
  "timezone": "America/New_York",
  "packageRules": [
    {
      "description": "Automerge non-major dev dependencies",
      "matchDepTypes": ["devDependencies"],
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true,
      "automergeType": "pr"
    },
    {
      "description": "Group non-major production patches",
      "matchDepTypes": ["dependencies"],
      "matchUpdateTypes": ["minor", "patch"],
      "groupName": "production dependencies (non-major)"
    },
    {
      "description": "Pin GitHub Actions digests",
      "matchManagers": ["github-actions"],
      "pinDigests": true
    }
  ],
  "vulnerabilityAlerts": {
    "enabled": true,
    "labels": ["security"]
  }
}
```

## CI Integration

### Pipeline Placement

```
PR opened → lint → test → dependency audit → SBOM → build → deploy
```

### GitHub Actions Example

```yaml
- name: Audit dependencies
  run: npm audit --audit-level=critical
  # Fails on critical only; high/medium are warnings

- name: Check licenses
  run: npx license-checker --onlyAllow "MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC"

- name: Generate SBOM
  run: syft . -o cyclonedx-json > sbom.json

- name: Scan SBOM
  run: grype sbom:./sbom.json --fail-on critical
```

### Severity Gating Strategy

| Severity | PR Check | Action |
|----------|----------|--------|
| Critical | Block merge | Must fix before merge |
| High | Warn (annotation) | Fix within sprint |
| Medium | Info only | Track in backlog |
| Low | Silent | Quarterly review |

## Supply Chain Attack Patterns

| Attack | Description | Mitigation |
|--------|-------------|------------|
| **Typosquatting** | `lodsah` instead of `lodash` | Verify package name carefully, use lock files |
| **Dependency confusion** | Public package name matches internal name | Scope private packages (`@company/pkg`), registry configuration |
| **Maintainer compromise** | Legitimate maintainer account hijacked | Pin exact versions, review changelogs before upgrade |
| **Malicious postinstall** | Package runs code on `npm install` | `--ignore-scripts`, review install scripts |
| **Protestware** | Maintainer inserts destructive/political code | Pin versions, review diffs, monitor advisories |
| **Star jacking** | Fake GitHub stars to build trust | Check actual download counts, contributor history |

### Defensive Measures

```bash
# npm: disable install scripts by default
npm config set ignore-scripts true
# Explicitly allow for known packages
npx --allow-scripts=node-gyp npm install

# Use lock files (always commit them)
npm ci          # Install from lock file exactly (not npm install)
yarn install --frozen-lockfile
pip install --require-hashes -r requirements.txt
```

## Pinning vs Floating Versions

| Strategy | Syntax | Pros | Cons |
|----------|--------|------|------|
| Exact pin | `1.2.3` | Deterministic, safe | Must manually update |
| Tilde (patch) | `~1.2.3` | Auto-patch updates | Minor risk from patches |
| Caret (minor) | `^1.2.3` | Auto-minor updates | Breaking changes happen despite semver |
| Range | `>=1.2.3 <2.0.0` | Flexible | Unpredictable |

**Recommendation**:
- **Libraries**: Use caret (`^`) for flexibility; consumers resolve versions
- **Applications**: Use exact pins or lock files for determinism
- **CI/CD (GitHub Actions)**: Pin to SHA digests, not tags (tags can be moved)

```yaml
# Bad: tag can be force-pushed
- uses: actions/checkout@v4

# Good: SHA is immutable
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

## Gotchas

- `npm audit` reports vulnerabilities in devDependencies that never ship to production; use `--production` or `--omit=dev` to filter
- `govulncheck` is call-graph aware (only reports reachable vulns); other tools report all vulns in dependency tree regardless of reachability
- CVSS scores don't account for YOUR context; a CVSS 9.8 in a function you never call is lower risk than a CVSS 6.0 in code you expose to the internet
- Transitive dependencies are where most vulnerabilities hide; direct deps are usually well-maintained
- Lock files must be committed to git; without them, `npm install` on CI may resolve different versions than local
- `pip-audit` requires a lock file or `--strict` for reproducible results; bare `requirements.txt` with ranges is insufficient
- License scanning misses dual-licensed packages and license changes between versions; verify manually for critical dependencies
- Dependabot/Renovate automerge should only be enabled for dev dependencies with good test coverage

## Cross-References

- **security:security-analysis** -- SAST scanning, vulnerability detection, threat modeling
- **security:secrets-management** -- preventing secrets from leaking into dependencies
- **migration:dependency-upgrade** -- strategies for upgrading major dependency versions
