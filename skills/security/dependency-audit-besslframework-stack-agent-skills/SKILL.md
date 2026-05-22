---
name: dependency-audit
description: |
  Scans package.json, requirements.txt, go.mod, Cargo.toml, or Gemfile and produces
  a report covering outdated packages, known CVEs, unused dependencies, license
  conflicts, and size impact. Falls back to manual analysis when audit tools are missing.
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Write
---

# Dependency Audit

Find the problems hiding in your dependency files before they find you.

---

## Why This Exists

Most projects accumulate dependencies faster than they review them. A package added six months ago might now have a critical CVE. Another one might account for 40% of your bundle size while being used in exactly one file. A third might have switched to a license that conflicts with yours. These things go unnoticed until they become incidents.

This skill reads your dependency files, runs the audit tools available on your system, and fills in the gaps with manual analysis when those tools are missing.

---

## Commands

### `/dependency-audit`

Scan the current project root. Auto-detects the package manager.

### `/dependency-audit [path]`

Scan a specific dependency file.

```
/dependency-audit packages/api/package.json
/dependency-audit backend/requirements.txt
```

### `/dependency-audit --fix`

Run the audit, then suggest and apply safe updates. "Safe" means: patch versions only, no breaking changes, and the existing test suite passes afterward.

---

## Supported Ecosystems

| File | Package Manager | Audit Tool |
|---|---|---|
| `package.json` / `package-lock.json` | npm / yarn / pnpm | `npm audit`, `yarn audit`, `pnpm audit` |
| `requirements.txt` / `Pipfile` / `pyproject.toml` | pip / pipenv / poetry | `pip-audit`, `safety check` |
| `go.mod` | Go modules | `govulncheck`, `go list -m -u all` |
| `Cargo.toml` / `Cargo.lock` | Cargo | `cargo audit` |
| `Gemfile` / `Gemfile.lock` | Bundler | `bundle audit` |

---

## How It Works

### Step 1: Detect ecosystem

Search the project root (or given path) for dependency files:

```bash
ls package.json package-lock.json yarn.lock pnpm-lock.yaml \
   requirements.txt Pipfile pyproject.toml \
   go.mod go.sum \
   Cargo.toml Cargo.lock \
   Gemfile Gemfile.lock 2>/dev/null
```

If multiple ecosystems exist (monorepo), audit each one separately.

### Step 2: Check available tools

For each detected ecosystem, check if the audit tool is installed:

```bash
which npm && npm --version
which pip-audit
which govulncheck
which cargo-audit
which bundle-audit
```

If a tool is missing, note it in the report and fall back to manual analysis (reading lock files and checking versions against known vulnerability databases via the dependency file itself).

### Step 3: Run audit tools

For each ecosystem where tools are available:

**Node.js:**
```bash
npm audit --json 2>/dev/null || echo "npm audit unavailable"
npm outdated --json 2>/dev/null
npx depcheck --json 2>/dev/null  # unused deps
```

**Python:**
```bash
pip-audit --format json 2>/dev/null || safety check --json 2>/dev/null
pip list --outdated --format json 2>/dev/null
```

**Go:**
```bash
govulncheck ./... 2>/dev/null
go list -m -u all 2>/dev/null
```

**Rust:**
```bash
cargo audit --json 2>/dev/null
cargo outdated --format json 2>/dev/null
```

**Ruby:**
```bash
bundle audit check 2>/dev/null
bundle outdated 2>/dev/null
```

### Step 4: Manual analysis (when tools are missing)

If audit tools are not installed, do what we can with what we have:

1. Read the dependency file and lock file
2. For each dependency, check if the specified version is significantly behind (major version difference)
3. Look for packages known to be problematic (from common knowledge)
4. Check for obvious license issues by reading license fields in lock files
5. Flag any dependency pinned to a specific commit hash or URL (supply chain risk)

### Step 5: Unused dependency detection

For Node.js projects (with or without depcheck):

```bash
# Get all dependencies from package.json
# Grep for each one across source files
# If a dependency appears nowhere in src/, flag it
grep -r "require\|import.*from" src/ --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx"
```

This has false positives (babel plugins, webpack loaders, bin scripts). Note those caveats in the output.

### Step 6: Size impact (Node.js only)

For each dependency listed in `package.json`:

```bash
# If node_modules exists, check installed size
du -sh node_modules/[package-name] 2>/dev/null
```

Sort by size, flag anything over 5MB.

### Step 7: License check

Read license fields from lock files or `node_modules/[pkg]/package.json`. Flag:

- GPL in an MIT/Apache project (viral license)
- AGPL in a SaaS project
- No license specified (legally risky)
- License changed between versions

---

## Output Format

```markdown
# Dependency Audit: [project name]

**Scanned**: [file path]
**Ecosystem**: [Node.js / Python / Go / Rust / Ruby]
**Date**: [date]
**Total dependencies**: [N direct, M transitive]

---

## Vulnerabilities

| Package | Installed | Severity | CVE | Description | Fix Version |
|---|---|---|---|---|---|
| lodash | 4.17.15 | High | CVE-2021-23337 | Prototype pollution in zipObjectDeep | 4.17.21 |
| axios | 0.21.0 | Medium | CVE-2021-3749 | ReDoS via crafted request | 0.21.2 |

**Total**: 2 high, 1 medium, 0 low

## Outdated

| Package | Current | Latest | Type | Semver Jump |
|---|---|---|---|---|
| react | 17.0.2 | 18.2.0 | major | 17 -> 18 |
| typescript | 4.9.5 | 5.3.3 | major | 4 -> 5 |
| eslint | 8.40.0 | 8.56.0 | minor | safe update |

## Unused (Possibly)

| Package | Last import found | Notes |
|---|---|---|
| moment | None in src/ | Consider removing. 290KB gzipped. |
| @types/lodash | None in src/ | May be used indirectly via other @types |

*Note: Babel plugins, PostCSS plugins, and CLI tools often appear unused because they're loaded by config, not imported.*

## License Concerns

| Package | License | Concern |
|---|---|---|
| some-package | GPL-3.0 | Viral license in MIT project |
| another-pkg | UNLICENSED | No license declared |

## Size Impact (Top 10)

| Package | Installed Size | % of node_modules |
|---|---|---|
| @next/swc-darwin-arm64 | 38MB | 12% |
| typescript | 22MB | 7% |
| esbuild | 9MB | 3% |

---

## Recommendations

1. **Update immediately**: lodash 4.17.15 -> 4.17.21 (CVE fix, patch version)
2. **Update soon**: axios 0.21.0 -> 0.21.2 (CVE fix, patch version)
3. **Evaluate**: react 17 -> 18 upgrade (breaking changes likely)
4. **Remove**: moment (unused, large bundle impact)
5. **Investigate**: some-package GPL license compatibility
```

---

## The --fix Flag

When the user runs `/dependency-audit --fix`:

1. Run the full audit first
2. Identify safe updates: patch version bumps with no breaking changes
3. Show the user what will be updated:
   ```
   Safe updates found:
     lodash 4.17.15 -> 4.17.21 (CVE fix)
     axios 0.21.0 -> 0.21.4
     eslint 8.40.0 -> 8.56.0

   Apply these updates?
   ```
4. On confirmation, run the appropriate update command:
   ```bash
   npm install lodash@4.17.21 axios@0.21.4 eslint@8.56.0
   ```
5. Run the test suite:
   ```bash
   npm test
   ```
6. If tests pass, report success. If tests fail, revert and report which package caused the failure.

Never auto-apply major version updates. Those require manual review.

---

## Important Constraints

- Always show what tools are and are not available before presenting results. If `npm audit` is missing but `depcheck` works, say so. The user should know which sections are from real tools and which are from manual analysis.
- Do not treat manual analysis results with the same confidence as tool results. Mark them as "estimated" or "manual check."
- The unused dependency check has known false positives. Always include the caveat.
- Size numbers from `du` include sub-dependencies and may overcount.
- For monorepos, run against each workspace separately and present results per workspace.
