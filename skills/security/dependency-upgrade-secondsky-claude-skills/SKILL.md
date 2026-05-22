---
name: dependency-upgrade
description: "Secure dependency upgrades with supply chain protection, cooldowns, and staged rollout. Use when upgrading deps, configuring security policies, or preventing supply chain attacks."
license: MIT
---

# Dependency Upgrade

Manage dependency upgrades with supply chain security, compatibility analysis, staged rollout, and comprehensive testing across all major package managers.

## When to Use This Skill

- Upgrading major framework or library versions
- Configuring supply chain attack prevention (cooldown, script blocking, lockfile hardening)
- Setting up secure package manager configuration
- Resolving dependency conflicts or peer dependency issues
- Planning incremental upgrade paths with testing
- Automating dependency updates with Renovate, Dependabot, or Snyk
- Auditing dependencies for vulnerabilities
- Setting up CI/CD dependency security workflows

## Two Modes of Operation

**Interactive** — Walk through setup questions to generate tailored config. Use for fresh setup.

**Default** — Apply recommended defaults immediately: 7-day cooldown, block all scripts, frozen-lockfile, lockfile-lint, Dependabot with cooldown. Customization optional.

## Interactive Setup Flow

When the user wants tailored configuration, walk through these decisions. Skip this section entirely if using default mode.

### Tier 1: Required Decisions

Always ask these 3 questions before generating any config:

**1. Package Manager**

"Which package manager does this project use?"

| Answer | Generates |
|--------|-----------|
| npm | `.npmrc` |
| Bun | `bunfig.toml` |
| pnpm | `pnpm-workspace.yaml` |
| Yarn | `.yarnrc.yml` |
| Deno | `deno.json` config |

**2. Cooldown Period**

"How many days should newly published packages age before install? This prevents supply chain attacks where malicious packages are discovered and unpublished within days."

| Option | Days | Use Case |
|--------|------|----------|
| Aggressive | 3 | Catches most typosquatting |
| Recommended | 7 | Good balance for most projects |
| Conservative | 14 | Critical/production systems |
| Paranoid | 21 | Matches Snyk's built-in default |
| Custom | N | User specifies |

**3. Post-Install Script Policy**

"How should lifecycle scripts (postinstall, preinstall) be handled? These are the #1 attack vector for supply chain attacks."

| Option | Behavior |
|--------|----------|
| Block all (recommended) | `--ignore-scripts` + allow-git=none |
| Allowlist | Block by default, allow specific trusted packages |
| Review only | Warn but don't block |

### Tier 2: Security Tooling (Offer as Batch)

"Which of these security features would you like to configure? Select any that apply."

**4. CI/CD Automation Tool**

| Answer | Generates |
|--------|-----------|
| Dependabot | `.github/dependabot.yml` with cooldown |
| Renovate | `renovate.json` with minimumReleaseAge |
| Snyk | No config needed (21-day cooldown built-in) |
| None | Skip |

**5. Automerge Policy**

| Option | Behavior |
|--------|----------|
| None | All updates require manual review |
| Minor+Patch only | Auto-merge safe updates, review majors |
| All with approval | Auto-merge after team approval |

**6. Update Schedule**

| Option | Config Value |
|--------|-------------|
| Daily | `"daily"` |
| Weekly (default) | `"weekly"` |
| Biweekly | `"biweekly"` |
| Monthly | `"monthly"` |

**7. Install-Time Auditing**

| Option | Installs |
|--------|----------|
| npq | Pre-install package auditor (open source) |
| Socket Firewall (sfw) | Real-time malicious package blocker |
| Both | Both tools with shell aliases |
| None | Skip |

**8. Lockfile Validation**

| Option | Behavior |
|--------|----------|
| Yes (recommended) | Adds `lockfile-lint` + CI script |
| No | Skip |

### Tier 3: Advanced Options (Only If User Opts In)

"Would you like to configure any advanced options?"

**9. Dev Containers** — Generate hardened `.devcontainer/devcontainer.json` (Yes/No)

**10. Secrets Manager** — 1Password CLI / Infisical / None

**11. pnpm Trust Policy** — Enable `trustPolicy: no-downgrade` (pnpm 10.21+ only, Yes/No)

**12. Cooldown Exclusions** — Package names that bypass cooldown (e.g., `@types/react`, `typescript`, `esbuild`)

## Security-First Upgrade Principles

1. **Cooldown before installing** — Wait 7 days for new package versions to be vetted by the community
2. **Block post-install scripts** — Prevent arbitrary code execution during `npm install`
3. **Freeze lockfiles in CI** — Use deterministic installs (`npm ci`, `--frozen-lockfile`)
4. **Validate lockfile integrity** — Use `lockfile-lint` to detect injection
5. **Audit before trusting** — Use `npq` or `sfw` to check packages before installing
6. **Upgrade incrementally** — One major version at a time with testing between each
7. **Never blindly upgrade** — Avoid `npm update` or `npm-check-updates -u` without review

## Cooldown Period: Prevent Supply Chain Attacks

Newly published packages may contain malicious code discovered within hours. Configure a cooldown period to delay installation.

### Quick Setup

**npm** (`.npmrc`):
```ini
min-release-age=7
```

**Bun** (`bunfig.toml`):
```toml
[install]
minimumReleaseAge = 604800  # 7 days in seconds
minimumReleaseAgeExcludes = ["@types/bun", "typescript"]
```

**pnpm** (`pnpm-workspace.yaml`):
```yaml
minimumReleaseAge: 10080  # 7 days in minutes
minimumReleaseAgeExclude:
  - '@types/react'
  - typescript
```

**Yarn** (`.yarnrc.yml`):
```yaml
npmMinimalAgeGate: "7d"
npmPreapprovedPackages:
  - "@types/react"
  - "typescript"
```

Load `references/cooldown-config-guide.md` for detailed per-PM configuration, CI tool integration, and exclusion patterns.

Use `templates/<pm>-security.tmpl` for copy-paste ready config files.

## Disable Post-Install Scripts

Post-install scripts are the most common supply chain attack vector (Shai-Hulud, Nx, event-stream incidents).

### Quick Setup

**npm**:
```bash
npm config set ignore-scripts true
npm config set allow-git none
```

**Bun**: Disabled by default. Allow specific packages in `package.json`:
```json
{ "trustedDependencies": ["esbuild", "sharp"] }
```

**pnpm (10.0+)**: Disabled by default. Allow specific packages in `pnpm-workspace.yaml`:
```yaml
allowBuilds:
  esbuild: true
strictDepBuilds: true  # Hard error on unreviewed scripts
```

Load `references/package-manager-security.md` for full per-PM hardening including pnpm `trustPolicy`, `blockExoticSubdeps`, and `@lavamoat/allow-scripts`.

## Deterministic & Frozen Installs

Always use frozen install commands in CI to ensure reproducible builds:

| Package Manager | Command | What It Does |
|----------------|---------|-------------|
| npm | `npm ci` | Deletes node_modules, installs exact lockfile versions |
| Bun | `bun install --frozen-lockfile` | Fails if lockfile is out of sync |
| pnpm | `pnpm install --frozen-lockfile` | Fails if lockfile is out of sync |
| Yarn | `yarn install --immutable --immutable-cache` | Validates lockfile and cache |
| Deno | `deno install --frozen` | Frozen installation |

Commit all lockfiles to version control: `package-lock.json`, `bun.lock`, `pnpm-lock.yaml`, `yarn.lock`, `deno.lock`.

## Lockfile Validation

Install and configure `lockfile-lint` to detect lockfile injection attacks:

```bash
npm install --save-dev lockfile-lint
```

```json
{
  "scripts": {
    "lint:lockfile": "lockfile-lint --path package-lock.json --type npm --allowed-hosts npm --validate-https",
    "preinstall": "npm run lint:lockfile"
  }
}
```

Note: `lockfile-lint` does not currently support Bun's `bun.lock` / `bun.lockb` formats.

## Pre-Install Security Auditing

### npq — Pre-Install Auditor

```bash
npm install -g npq
npq install <package>          # Audit before installing
npq install <package> --dry-run # Audit without installing

# Shell alias for seamless use
alias npm='npq-hero'

# Use with other PMs
NPQ_PKG_MGR=pnpm npq install <package>
NPQ_PKG_MGR=bun npq install <package>
```

### Socket Firewall (sfw) — Real-Time Blocker

```bash
npm install -g sfw
sfw npm install <package>      # Blocks malicious packages
sfw pnpm add <package>
sfw yarn add <package>
```

Load `references/supply-chain-security.md` for full comparison of npq vs sfw and what each validates.

## Dependency Analysis

```bash
# Audit for vulnerabilities
bun audit       # Bun
npm audit       # npm
yarn audit      # Yarn

# Check for outdated packages
bun outdated
npm outdated

# Interactive upgrade (safe — review each)
bunx npm-check-updates --interactive

# Analyze dependency tree
npm ls <package-name>
yarn why <package-name>
```

## Staged Upgrade Strategy

Upgrade one dependency at a time with testing between each:

```bash
# 1. Create feature branch
git checkout -b upgrade/<package>-<version>

# 2. Upgrade single package
bun add <package>@<version>

# 3. Test immediately
bun test && bunx tsc --noEmit && bun run build

# 4. Commit and continue
git add -A && git commit -m "chore: upgrade <package> to <version>"
```

Load `references/staged-upgrades.md` for codemod automation, custom migration scripts, and peer dependency handling.

Load `references/compatibility-matrix.md` for version compatibility tables (React 18/19, Next.js 13-15, TypeScript, Tailwind 3/4).

## Automated Updates with Cooldown

Configure CI/CD tools to respect cooldown periods:

### Dependabot (`.github/dependabot.yml`)

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    cooldown:
      default-days: 7
```

### Renovate (`renovate.json`)

```json
{
  "extends": ["config:base"],
  "minimumReleaseAge": "7 days",
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "minimumReleaseAge": "14 days"
    }
  ]
}
```

### Snyk

Snyk includes a built-in 21-day cooldown for upgrade PRs. No configuration needed.

Use `templates/dependabot-security.tmpl` or `templates/renovate-security.tmpl` for complete config files.

## Publishing Security

For package maintainers:

```bash
# Enable 2FA
npm profile enable-2fa auth-and-writes

# Publish with provenance (cryptographic build proof)
npm publish --provenance

# Trusted publishing via OIDC (eliminates long-lived tokens)
# Configure on npmjs.com, then:
# In GitHub Actions: permissions: id-token: write
```

Load `references/supply-chain-security.md` for full publishing security guide including OIDC setup and dependency tree reduction.

## Dev Environment Hardening

Isolate dependency execution from the host system:

- **Dev containers** — limit blast radius of malicious packages
- **Secrets management** — use 1Password CLI or Infisical instead of plaintext `.env` files
- **Dependency tree reduction** — replace common packages with native JS

Use `templates/devcontainer-security.tmpl` for a hardened dev container config.

Load `references/secrets-and-containers.md` for dev container setup, secrets management, and dependency reduction patterns.

## Testing Strategy

Run tests at every level after each upgrade:

```bash
# 1. Static analysis (fastest)
bunx tsc --noEmit && bun run lint

# 2. Unit tests
bun test

# 3. Build check
bun run build

# 4. Integration / E2E (after major upgrades)
bun run test:e2e
```

Load `references/testing-strategy.md` for full testing pyramid, CI integration, and bundle analysis.

## Rollback Plan

```bash
#!/bin/bash
git stash
git checkout -b upgrade/<package>

bun add <package>@latest

if bun test && bun run build; then
  git add package.json bun.lock
  git commit -m "chore: upgrade <package>"
else
  echo "Upgrade failed, rolling back"
  git checkout main
  git branch -D upgrade/<package>
  bun install
fi
```

## Upgrade Checklist

```markdown
Pre-Upgrade:
- [ ] Review current dependency versions
- [ ] Read changelogs for breaking changes
- [ ] Create feature branch
- [ ] Tag current state (git tag pre-upgrade)
- [ ] Run full test suite (baseline)
- [ ] Verify cooldown period is configured

Security Pre-Checks:
- [ ] Post-install scripts are disabled
- [ ] Lockfile validation is active
- [ ] Install auditing tools configured (if applicable)
- [ ] CI uses frozen-lockfile install

During Upgrade:
- [ ] Upgrade one dependency at a time
- [ ] Respect cooldown period (don't force latest)
- [ ] Update peer dependencies
- [ ] Fix TypeScript errors
- [ ] Run test suite after each upgrade
- [ ] Check bundle size impact

Post-Upgrade:
- [ ] Full regression testing
- [ ] Performance testing
- [ ] Update documentation
- [ ] Deploy to staging
- [ ] Monitor for errors
- [ ] Deploy to production
```

## Common Pitfalls

- Upgrading all dependencies at once (use incremental upgrades)
- Blindly running `npm update` or `npm-check-updates -u` without review
- Not testing after each individual upgrade
- Ignoring peer dependency warnings
- Forgetting to update or commit the lock file
- Not reading breaking change notes in changelogs
- Skipping major versions instead of stepping through them
- Not having a rollback plan
- Trusting npmjs.org displayed source code (can differ from actual tarball)
- Leaving post-install scripts enabled (most common attack vector)
- Not configuring a cooldown period for new package versions

## When to Load References

Load these reference files when the user needs detailed information beyond the quick-reference in SKILL.md:

| Load This File | When |
|---------------|------|
| `references/cooldown-config-guide.md` | Configuring cooldown for a specific PM, CI tool integration, or exclusion patterns |
| `references/package-manager-security.md` | Full per-PM hardening guide including pnpm trust policy, blockExoticSubdeps, cross-PM cheat sheet |
| `references/supply-chain-security.md` | Understanding attack vectors, incident history, npq vs sfw comparison, publisher security (2FA, provenance, OIDC) |
| `references/secrets-and-containers.md` | Setting up dev containers, secrets management with 1Password/Infisical |
| `references/compatibility-matrix.md` | Checking version compatibility for React, Next.js, TypeScript, Tailwind upgrades |
| `references/staged-upgrades.md` | Codemod automation, custom migration scripts, peer dependency handling, workspace upgrades |
| `references/testing-strategy.md` | Full testing pyramid, CI integration, bundle analysis, performance testing |

## Template Files

Ready-to-use config files in `templates/`:

| Template | Purpose |
|----------|---------|
| `npmrc-security.tmpl` | Secure `.npmrc` with scripts disabled + cooldown |
| `bunfig-security.tmpl` | Secure `bunfig.toml` with cooldown + exclusions |
| `pnpm-workspace-security.tmpl` | Secure `pnpm-workspace.yaml` with cooldown, allowBuilds, trustPolicy |
| `yarnrc-security.tmpl` | Secure `.yarnrc.yml` with age gate + preapproved packages |
| `dependabot-security.tmpl` | Dependabot config with 7-day cooldown |
| `renovate-security.tmpl` | Renovate config with minimumReleaseAge + automerge rules |
| `devcontainer-security.tmpl` | Hardened dev container with security options |
