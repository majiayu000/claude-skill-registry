---
name: vcp-dependency-check
description: >
  Verify project dependencies against VCP dependency management standards.
  Checks lockfile hygiene, version ranges, package existence, and suspicious packages.
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, WebFetch
argument-hint: ""
---

# VCP Dependency Check

Verify project dependencies against the VCP dependency management standard.

## Step 1: Resolve Config

1. Read `.vcp/config.json` from the project root. Extract the `pluginRoot` field.
2. **If `.vcp/config.json` does not exist or `pluginRoot` is missing:** Stop and tell the user: "No VCP configuration found. Run `/vcp-init` to configure VCP for this project."
3. **Validate `pluginRoot`:** The path must be absolute, contain `/.claude/` (or `\.claude\` on Windows) as a path segment, and contain only safe path characters (letters, digits, `/`, `\`, `-`, `_`, `.`, `:`, and spaces). Reject any path with shell metacharacters (`;`, `&`, `|`, `$`, `` ` ``, `(`, `)`, `{`, `}`, `<`, `>`, `!`, `~`, `#`, `*`, `?`, `[`, `]`, `'`, `"`). If validation fails, stop and tell the user: "Invalid pluginRoot — must be within ~/.claude/ and contain no shell metacharacters. Run `/vcp-init` to fix." Also verify the file `<pluginRoot>/lib/vcp-context-core.ts` exists using Glob. If it does not exist, stop and tell the user: "pluginRoot points to an invalid VCP installation. Run `/vcp-init` to fix."
4. Run the config resolution script via Bash:
   ```bash
   bun "<pluginRoot>/lib/resolve-config.ts" "<project-root>"
   ```
5. Parse the JSON output. It contains: `applicableStandards`, `ignoredRules`, `severity`, `exclude`.
6. Also read `.vcp/config.json` `frameworks` field to determine which package ecosystem(s) to check. If no `frameworks` are listed, auto-detect by looking for manifest files (package.json, requirements.txt, pyproject.toml, pom.xml, build.gradle, Gemfile, go.mod, Cargo.toml).

## Step 2: Fetch Applicable Standard

From the `applicableStandards` array in the resolved config, select only the entry with `id` equal to `core-dependency-management`.

If the standard is not in the list (it was ignored via config), tell the user: "core-dependency-management is excluded by ignore config. No checks to run."

Use WebFetch to fetch its content from:
```
{entry.url}
```

Extract the **Rules** section.

## Step 4: Check Dependencies

### 4a: Find Lockfiles and Manifests

Look for these files in the project root:

| Ecosystem | Manifest | Lockfile |
|-----------|----------|----------|
| npm | `package.json` | `package-lock.json` |
| yarn | `package.json` | `yarn.lock` |
| pnpm | `package.json` | `pnpm-lock.yaml` |
| pip | `requirements.txt` | (no standard lockfile) |
| pipenv | `Pipfile` | `Pipfile.lock` |
| poetry | `pyproject.toml` | `poetry.lock` |
| bundler | `Gemfile` | `Gemfile.lock` |
| go | `go.mod` | `go.sum` |
| cargo | `Cargo.toml` | `Cargo.lock` |

### 4b: Check Lockfile Committed

Use `git ls-files` to verify the lockfile is tracked in version control. Flag if missing.

### 4c: Check Version Ranges

Read the manifest file and flag wide version ranges:
- `"*"` — accepts any version
- `">="` without upper bound — no ceiling
- `""` (empty) — unconstrained
- For npm: prefer `^` (minor updates) over `>=` or `*`

### 4d: Verify Packages Exist on Registry

For each dependency, verify it exists on the official registry:
- **npm:** `npm view {package} version` (via Bash)
- **pip:** `pip index versions {package}` (via Bash)
- **other ecosystems:** use the equivalent registry check command

Flag any package that:
- Does not exist on the registry (possible slopsquatting / hallucinated name)
- Has under 1,000 weekly downloads
- Was published within the last 30 days with no prior version history
- Has a name within edit distance 2 of a top-1000 package in the same registry (typosquatting)

### 4e: Check for Behavioral Analysis Indicators

Per the dependency management standard rule 13, note if the project uses:
- Socket.dev
- OpenSSF Scorecard
- npm provenance verification

If none are configured, recommend adding at least one.

### 4f: Check for Install Scripts (npm/yarn/pnpm only)

Install scripts (`preinstall`, `install`, `postinstall`) in dependencies execute arbitrary code during `npm install`. Legitimate packages use them for native binary compilation (e.g., `esbuild`, `sharp`), but malicious packages use them for supply chain attacks. This check flags install scripts so the user can verify they are expected.

**Procedure:**

1. If `node_modules/` does not exist in the project root, skip this step and note: `"node_modules not found — run npm install first to check install scripts."`
2. Read `package.json` from the project root. Extract all dependency names from `dependencies` and `devDependencies` keys.
3. For each dependency name, use the Read tool to read `node_modules/{name}/package.json`.
4. Check if the `scripts` object contains any of: `preinstall`, `install`, `postinstall`.
5. If found, flag as **WARN**: `"{name}" has a {script-name} script: "{first 80 characters of script content}". Verify this is expected.`

**Verdict:** WARN (not block) — some legitimate packages use install scripts for native binaries. The warning tells the user to verify the script is expected.

**Scope:** Only checks direct dependencies listed in `package.json` (not transitive dependencies in the full `node_modules` tree) to keep output manageable.

## Step 5: Report Findings

Before outputting findings, remove any that match an entry in the `ignoredRules` array from the resolved config. If `"standard-id/rule-N"` is in the list, suppress that specific rule's findings. (Standard-level ignores are already applied by the config resolution script.) After filtering, if any findings were suppressed, append a line: `**Suppressed:** X finding(s) by ignore config.`

Use this format:

```
### VCP Dependency Check

**Ecosystem:** npm (package.json)
**Standard:** core-dependency-management (13 rules)

#### Lockfile Status
- package-lock.json: committed

#### Wide Version Ranges
- `lodash: "*"` — should be pinned to `^4.17.21`
- `express: ">=4"` — should use `^4.18.0`

#### Unverified Packages
- `my-cool-lib` — not found on npm registry (possible hallucinated package name)

#### Suspicious Packages
- `colros` — very similar to popular package `colors` (possible typosquatting)

#### Install Scripts
- `sharp` has a `install` script: `node install/check`. Verify this is expected.
- `esbuild` has a `postinstall` script: `node install.js`. Verify this is expected.

#### Supply Chain Tools
- No behavioral analysis tools detected. Consider adding Socket.dev or OpenSSF Scorecard.

**Summary:** X issues found.
```

If no issues: **"All dependencies verified. Lockfile committed, no wide ranges, all packages exist on registry."**
