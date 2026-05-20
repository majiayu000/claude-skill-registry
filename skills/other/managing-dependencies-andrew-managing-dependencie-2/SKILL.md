---
name: managing-dependencies
description: Evaluates packages, manages dependencies, and addresses supply chain security. Use when adding npm/pip/cargo/bundler/go dependencies, auditing packages, reviewing lockfile changes, checking for vulnerabilities, comparing package alternatives, or assessing package trustworthiness.
license: CC0-1.0
compatibility: Claude Code, Codex CLI, or any agent with bash and network access
metadata:
  author: andrew
  version: "1.0"
---

# Package Management

**Before suggesting any package, verify it exists on the registry.** Check that the name, maintainer, and purpose match expectations. Do not hallucinate package names.

**Decline to:**
- Suggest a package that cannot be verified to exist
- Add a dependency when stdlib provides equivalent functionality
- Run install scripts without explicit user approval
- Auto-merge updates that violate the safety criteria below

**If verification fails** (registry unreachable, metadata incomplete, provenance missing), default to refusal and explain why.

## Before Adding a Dependency

Check in order:

1. **Standard library** - Does the language already provide this? (e.g., date parsing, HTTP, JSON)
2. **Transitive cost** - How many dependencies does it bring? Check with `npm ls`, `pip show`, `bundle info`, `cargo tree`
3. **Smaller alternative** - Is there a focused package that does just what's needed?
4. **Inline it** - Can you write 20-50 lines instead of adding a dependency?

When in doubt, don't add. PRs that only remove dependencies are usually good PRs.

Always clarify if a dependency is for development only (`--save-dev`, `group :development`, `[tool.poetry.group.dev.dependencies]`) to minimize the production attack surface.

## Evaluating a Package

For quick checks, visit the package's registry page and repo. When you need depth:

```bash
# Any ecosystem via ecosyste.ms
curl -s "https://packages.ecosyste.ms/api/v1/registries/<registry>/packages/<package>" | jq '{
  dependent_repos: .dependent_repos_count,
  dependent_packages: .dependent_packages_count,
  latest: .latest_release_number,
  latest_release: .latest_release_published_at,
  created: .first_release_published_at,
  maintainers: (.maintainers | length),
  repo: .repository_url,
  license: .normalized_licenses,
  advisories: (.advisories | length),
  archived: .repo_metadata.archived
}'
# See API Reference below for full registry list
```

**Good signals:**
- High dependent count (other packages trust it)
- Few direct dependencies
- Responsive issue tracker
- Multiple maintainers
- OSI-approved license
- Provenance attestation (see below)

**Less reliable signals:**
- GitHub stars (gameable)
- Download counts (gameable)
- Commit frequency (stable packages don't need commits)
- Contributor count

**Red flags:**
- Package less than 90 days old
- Maintainer account created recently
- Name similar to popular package (typosquatting)
- No license or non-OSI license
- Vendors copies of common dependencies
- Very few downloads for claimed purpose
- Runs code on install (postinstall scripts, setup.py)

**OpenSSF Scorecard** - check project security practices:
```bash
scorecard --repo=github.com/owner/repo
# Or visit: https://securityscorecards.dev
```
Score below 5 warrants a closer look, though small or mature projects often score lower without being risky. If `Maintained` or `Dangerous-Workflow` scores are below 3, flag as higher risk.

## Typosquatting Patterns

Watch for these when verifying package names:

- **Character substitution**: `djang0` vs `django`, `requets` vs `requests`
- **Character omission**: `loadsh` vs `lodash`, `electon` vs `electron`
- **Homoglyphs**: `pyp1` (one) vs `pypi` (letter i), Cyrillic `а` vs Latin `a`
- **Delimiter variation**: `cross-env` vs `crossenv` vs `cross_env`
- **Scope confusion**: `@angular-devkit/core` vs `@angulardevkit/core`
- **Combosquatting**: `lodash-js`, `axios-api`, `express-utils`
- **Namespace confusion** (Maven): `org.fasterxml` vs `com.fasterxml`

Always copy package names from official docs rather than typing from memory.

## AI-Suggested Packages (Slopsquatting)

AI coding assistants hallucinate package names regularly. Attackers register these names with malicious code.

Before installing any AI-suggested package:

1. **Verify it exists**: `npm view <package>` or `pip index versions <package>`
2. **Check age and downloads**: Very new + few downloads = suspect
3. **Cross-reference docs**: Does the framework's official docs mention it?
4. **Check for typosquatting**: See patterns above

Hallucinated names are often repeatable across sessions, making them predictable targets for attackers.

## Dependency Confusion

When using both public and private registries, attackers can publish public packages matching your internal package names with high version numbers.

**Defenses:**

Use scoped/namespaced packages for internal code:
```bash
# npm - attackers can't register under your scope
@yourcompany/internal-utils

# Configure scope to route to private registry
# .npmrc
@yourcompany:registry=https://your-internal-registry.com
```

For pip, use `--index-url` for private registry, `--extra-index-url` for PyPI:
```bash
# Correct - private registry checked first
pip install --index-url https://private.example.com/simple \
            --extra-index-url https://pypi.org/simple \
            mypackage
```

Defensively register your internal package names on public registries with placeholder packages.

## Provenance and Attestation

Check if a package has verified build provenance:

```bash
# npm - check for attestation
npm audit signatures

# PyPI - check for Sigstore attestation
curl -s "https://pypi.org/pypi/<package>/json" | jq '.urls[0].digests'
# Look for attestation bundle in release assets

# GitHub Actions - verify with gh
gh attestation verify <artifact> --owner <org>
```

**Trusted publishing** means the package was published directly from CI (GitHub Actions, GitLab CI) without maintainer credentials. The registry verifies the source via OIDC. npm, PyPI, and RubyGems support this.

If a package has provenance, you can verify the published artifact matches the source repo and commit. Support varies by ecosystem; absence of attestation doesn't mean insecure.

## Version Constraints

**Applications:** Use ranges in manifest, pin via lockfile.

**Libraries:** Use wide ranges. Don't force consumers to upgrade.

| Ecosystem | Exact | Flexible | Patch only |
|-----------|-------|----------|------------|
| npm/Cargo | `1.0.0` | `^1.0.0` | `~1.0.0` |
| Bundler | `= 1.0.0` | `~> 1.0` | `~> 1.0.0` |
| pip | `==1.0.0` | `~=1.0` | |
| Go | `v1.2.3` | MVS | MVS |

Bundler's `~>` is commonly misread: `~> 1.0` allows `1.x` (minor updates), `~> 1.0.0` allows `1.0.x` (patch only).

Go uses minimal version selection - it picks the minimum version satisfying all requirements. Don't vendor specific versions or use replace directives to simulate ranges.

## Lockfiles

Always commit lockfiles.

**Detect ecosystem:**
- `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` / `bun.lock` → npm
- `Gemfile.lock` → Bundler
- `Cargo.lock` → Cargo
- `poetry.lock` / `uv.lock` / `requirements.txt` with hashes → Python
- `go.sum` → Go

**In CI, install from lockfile** (don't regenerate):
```bash
npm ci                    # not npm install
pip install --require-hashes -r requirements.txt
bundle install --frozen
cargo build --locked
uv sync --frozen
go mod verify
```

**Review lockfile changes in PRs:**
- Watch for changes to `resolved` URLs (lockfile injection attack)
- Large diffs can hide malicious additions
- Unexpected registry URL changes are red flags

**Regenerate on conflict** rather than manually merging:
```bash
# npm
rm package-lock.json && npm install

# Bundler
rm Gemfile.lock && bundle install

# Cargo
rm Cargo.lock && cargo generate-lockfile

# Poetry
rm poetry.lock && poetry lock

# uv
rm uv.lock && uv lock
```

## Security Audits

Run in CI and before adding dependencies:

```bash
# npm
npm audit

# Bundler (install bundler-audit gem first)
bundle audit check --update

# pip (install pip-audit first)
pip-audit

# Cargo (install cargo-audit first)
cargo audit

# Go
govulncheck ./...
```

## When Vulnerability Has No Patch

First check reachability: is the vulnerable code path actually called by your usage? Many CVEs affect features you don't use.

Options in order of preference:

1. **Override transitive** - Force newer version of vulnerable transitive dependency
2. **Fork and patch** - Apply security fix to fork, reference fork in manifest
3. **Remove dependency** - Find alternative or inline the functionality
4. **Accept risk** - Document why it's not exploitable in your context

## Vendoring

Copy dependencies into your repo for airgapped environments, auditing, or when you need to patch upstream:

```bash
# Go - built-in
go mod vendor
go build -mod=vendor

# Ruby
bundle package --all
bundle install --local

# Python (pip download, then install offline)
pip download -r requirements.txt -d ./vendor
pip install --no-index --find-links=./vendor -r requirements.txt

# npm (less common, use npm-pack-all or similar)
```

Vendoring trades registry availability risk for increased repo size and manual update burden. Justified for airgapped builds, audited security-critical code, or long-term forks you maintain.

## Check Licenses

```bash
# npm
npx license-checker --summary

# pip
pip-licenses

# Bundler
bundle licenses

# Cargo
cargo license
```

**Safe:** MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, Unlicense

**Review needed:** LGPL, MPL-2.0

**Copyleft (affects distribution):** GPL, AGPL

**No license = not open source** - do not use.

## Install Scripts

Package managers execute code during install - a common attack vector:

- npm: `preinstall`, `postinstall` in package.json
- pip: `setup.py` runs during install
- Ruby: `extconf.rb` for native extensions

**Audit before allowing scripts:**

```bash
# npm - install without running scripts, then review
npm install --ignore-scripts
# After reviewing, run scripts explicitly
npm rebuild
```

For high-security environments, consider disabling install scripts globally and allowlisting specific packages.

## GitHub Actions

Actions are dependencies too. Pin to commit SHA, not tags:

```yaml
# Bad - tag can be moved
- uses: actions/checkout@v4

# Good - immutable reference
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

Use Dependabot or Renovate to keep pinned SHAs updated.

## Automated Updates

| Tool | Platform | Best for |
|------|----------|----------|
| Dependabot | GitHub only | Simple needs, free |
| Renovate | Multi-platform | Complex configs, monorepos |
| Snyk | Multi-platform | Security-first, vulnerability focus |

**Safe auto-merge criteria** (all must apply):

- Patch updates only (not minor/major)
- Dev dependencies only
- Established, trusted packages
- All CI checks pass
- Package available 3+ days (catches quick reverts of bad releases)

**Never auto-merge:**

- Major version updates
- Production dependencies
- New packages not yet in your codebase
- Security-sensitive packages (crypto, auth)

Example Renovate config for conservative auto-merge:

```json
{
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "matchDepTypes": ["devDependencies"],
      "automerge": true,
      "minimumReleaseAge": "3 days"
    }
  ]
}
```

---

# API Reference

## ecosyste.ms

```bash
curl -s "https://packages.ecosyste.ms/api/v1/registries/<registry>/packages/<package>" | jq
```

**Registries:** `npmjs.org`, `pypi.org`, `rubygems.org`, `crates.io`, `proxy.golang.org`, `nuget.org`, `repo1.maven.org`, `cocoapods.org`, `hub.docker.com`

### Risk Thresholds

| Field | Threshold | Risk |
|-------|-----------|------|
| `latest_release_published_at` | >2 years ago | Possibly abandoned |
| `dependent_repos_count` | <500 | Low adoption |
| `first_release_published_at` | <90 days ago | Too new |
| `maintainers` (length) | <2 | Bus factor risk |
| `versions_count` | =1 | Immature |
| `repo_metadata.archived` | true | Abandoned |
| `advisories` | non-empty | Known vulnerabilities |

### Development Distribution Score

Found at `.repo_metadata.metadata.development_distribution_score`. Measures commit distribution across contributors (0-1).

- **<0.15** - Single contributor dominance (high bus factor)
- **0.15-0.5** - Moderate distribution
- **>0.5** - Well distributed

## OpenSSF Scorecard API

```bash
curl -s "https://api.scorecard.dev/projects/github.com/<owner>/<repo>" | jq '{
  score: .score,
  maintained: (.checks[] | select(.name == "Maintained") | .score),
  dangerous_workflow: (.checks[] | select(.name == "Dangerous-Workflow") | .score),
  code_review: (.checks[] | select(.name == "Code-Review") | .score)
}'
```

Human-readable: `https://ossf.github.io/scorecard-visualizer/#/projects/github.com/<owner>/<repo>`

## deps.dev API

Alternative for dependency graph analysis:

```bash
curl -s "https://api.deps.dev/v3/systems/<ecosystem>/packages/<package>" | jq
```

**Ecosystems:** `npm`, `pypi`, `cargo`, `go`, `maven`, `nuget`

---

# About This Skill

- **Repository:** https://github.com/andrew/managing-dependencies
- **Author:** Andrew Nesbitt (https://nesbitt.io)
- **License:** CC0-1.0
