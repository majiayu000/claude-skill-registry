---
name: analyze-deps
description: Analyze dependencies for updates, breaking changes, deprecations, and migration paths. Generates actionable reports with codebase impact assessment.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebSearch
  - WebFetch
  - Write
user-invocable: true
---

# Analyze Dependencies

## Purpose

On-demand dependency analysis that checks for available updates, breaking changes, deprecations, and maps impact against the codebase. Generates actionable reports with migration guidance.

## When to Use

- Auditing dependencies before a major release
- Checking for security vulnerabilities
- Planning dependency upgrades
- Finding deprecated packages that need replacement

## Input Options

```bash
# Single package
/analyze-deps @radix-ui/react-dialog

# Specific workspace
/analyze-deps packages/react

# All workspaces
/analyze-deps all
```

## Analysis Flow

```
Input (package or workspace)
    │
    ▼
┌─────────────────────────────────────┐
│ 1. Resolve package.json(s)          │
│    - Single package → find in deps  │
│    - Workspace → read its pkg.json  │
│    - All → glob all package.jsons   │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ 2. npm Registry Fetch               │
│    - Current vs latest versions     │
│    - Classify: patch/minor/major    │
│    - Check deprecation status       │
│    - Get suggested replacements     │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ 3. Changelog & Migration Research   │
│    (Only for packages with updates) │
│    - GitHub releases API            │
│    - CHANGELOG.md fallback          │
│    - WebSearch for migration guides │
│    - Official docs for breaking     │
│      changes                        │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ 4. Codebase Impact Scan             │
│    - Find all imports               │
│    - Trace usage patterns           │
│    - Map against breaking changes   │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ 5. Generate Report                  │
│    - Markdown file in reports/deps/ │
│    - Upgrade recommendations        │
│    - Risk assessment                │
└─────────────────────────────────────┘
```

## Process

### Phase 1: Resolve Target Dependencies

**Parse input to determine scope:**

| Input Type     | Detection                             | Action                                |
| -------------- | ------------------------------------- | ------------------------------------- |
| Single package | Starts with `@` or no `/`             | Find in all package.json dependencies |
| Workspace path | Contains `/` (e.g., `packages/react`) | Read that workspace's package.json    |
| `all`          | Literal string "all"                  | Glob all `**/package.json` files      |

**For single package:**

```
Use Grep tool:
Grep(pattern: "{package-name}", glob: "**/package.json")
```

**For workspace:**

```
Use Read tool:
Read(file_path: "{workspace}/package.json")
```

**For all:**

```
Use Glob tool:
Glob(pattern: "**/package.json")
Note: node_modules is excluded by default
```

**Extract dependencies:**

- `dependencies`
- `devDependencies`
- `peerDependencies` (note as peer)

### Phase 2: Query npm Registry

**For each dependency, fetch registry info:**

```bash
npm view {package-name} --json
```

**Error handling for npm commands:**

| Error Type      | Detection                          | Action                                       |
| --------------- | ---------------------------------- | -------------------------------------------- |
| Network timeout | Command hangs > 30s                | Use `timeout 30` prefix, note as "timed out" |
| 404 Not Found   | Exit code 1, "Not found" in output | Note as "package not found in registry"      |
| 401/403 Auth    | "ENEEDAUTH" or "E403"              | Note as "private package, auth required"     |
| Rate limited    | "ETOOMANYREQS"                     | Wait and retry, or note as "rate limited"    |

**Example with timeout:**

```bash
timeout 30 npm view {package-name} --json 2>/dev/null || echo '{"error": "fetch failed"}'
```

**Extract:**
| Field | Purpose |
|-------|---------|
| `version` | Latest version available |
| `deprecated` | Deprecation message (if any) |
| `time` | Release dates for versions |
| `repository` | GitHub URL for changelog lookup |

**Classify version bump:**

| Type  | Criteria          | Risk   |
| ----- | ----------------- | ------ |
| Patch | `1.0.0` → `1.0.1` | Low    |
| Minor | `1.0.0` → `1.1.0` | Medium |
| Major | `1.0.0` → `2.0.0` | High   |

**Emoji usage:** Always use actual Unicode emojis in reports, NOT GitHub shortcodes:

- Use `🔴` not `:red_circle:`
- Use `🟡` not `:yellow_circle:`
- Use `🟢` not `:green_circle:`
- Use `✅` not `:white_check_mark:`

**Flag deprecated packages immediately** — these are priority items.

**Security vulnerability check:**

Run npm audit to identify known vulnerabilities:

```bash
npm audit --json
```

**Handling audit results:**

- Packages with vulnerabilities should be flagged with 🔴 High risk regardless of version bump type
- Include vulnerability severity (critical, high, moderate, low) in the report
- Link to advisory details when available

**Note:** Security issues take priority over all other risk factors.

### Phase 3: Research Breaking Changes

**Only for packages with available updates (prioritize major bumps).**

**Research sources (in order):**

1. **GitHub Releases API**

   ```
   https://api.github.com/repos/{owner}/{repo}/releases
   ```

   - Look for release notes between current and latest version
   - Extract breaking changes, migration notes

2. **CHANGELOG.md**

   ```
   https://raw.githubusercontent.com/{owner}/{repo}/main/CHANGELOG.md
   ```

   - Parse for version headers
   - Extract changes between current and latest

   **Branch fallback order:**
   1. Try `main` branch first
   2. Fall back to `master` if 404
   3. Use repository's default branch from API metadata as final fallback

   ```
   https://raw.githubusercontent.com/{owner}/{repo}/main/CHANGELOG.md
   # If 404, try:
   https://raw.githubusercontent.com/{owner}/{repo}/master/CHANGELOG.md
   ```

3. **WebSearch for migration guides**
   ```
   "{package-name} v{from} to v{to} migration guide"
   "{package-name} v{to} breaking changes"
   "{package-name} upgrade guide official"
   ```

**Security research triggers:**

Not every package needs security research. Search for security issues when:

1. Package is flagged by `npm audit` - deep search required
2. Major version bump - include security in migration research
3. Package hasn't been updated in 2+ years - search for known issues

**Security search queries (when triggered):**

```
"{package-name} CVE"
"{package-name} security vulnerability"
"{package-name} v{current-version} security advisory"
"{package-name} v{latest-version} security advisory"
```

Check both current AND latest version for vulnerabilities - upgrading isn't always safer.

4. **Official documentation**
   - Check package homepage for upgrade guides
   - Look for migration documentation

**Search priority:**

- Official documentation > GitHub releases > Release notes > Community guides
- Avoid outdated blog posts (check dates)
- Prefer sources from package maintainers

**Document for each package:**

- Breaking changes list
- Migration steps (if found)
- Links to official guides

### Phase 4: Codebase Impact Scan

**Only scan for impact when breaking changes exist.**

If no breaking changes were found in Phase 3, skip this phase entirely. There's no need to list all files using a package when everything is compatible.

**When breaking changes exist:**

```
Use Grep tool to find import statements:
Grep(pattern: "from ['\"]package-name", glob: "**/*.{ts,tsx}")

Use Grep tool to find require statements:
Grep(pattern: "require\\(['\"]package-name", glob: "**/*.{js,ts}")
```

**Map against breaking changes only:**

- For each breaking change found in Phase 3
- Check if our codebase uses the affected API
- Only note files that use affected APIs

**Output (only when impact exists):**

```markdown
**Impacted files:**
| File | Line | Impact |
|------|------|--------|
| `packages/react/src/components/modal.tsx` | 12 | Uses deprecated `open` prop |
```

**If no files are impacted by breaking changes:**

```markdown
**Impact:** None. Our codebase does not use any affected APIs.
```

**IMPORTANT:** Do NOT list all files that import the package. Only list files that need changes due to breaking changes or deprecated APIs.

### Phase 5: Generate Report

**Location:** `reports/deps/{target}-{YYYY-MM-DD}.md`

Where `{target}` is:

- Package name (sanitized): `radix-ui-react-dialog`
- Workspace name: `packages-react`
- `all-workspaces` for full scan

**Report structure:**

````markdown
# Dependency Analysis: {target}

Generated: {YYYY-MM-DD HH:mm}
Scope: {description of what was analyzed}

## Summary

| Metric            | Count |
| ----------------- | ----- |
| Packages analyzed | X     |
| Up to date        | X     |
| Updates available | X     |
| Deprecated        | X     |
| Security issues   | X     |

## Risk Overview

| Risk      | Count | Action                          |
| --------- | ----- | ------------------------------- |
| 🔴 High   | X     | Requires migration planning     |
| 🟡 Medium | X     | Review changelog before upgrade |
| 🟢 Low    | X     | Safe to upgrade                 |

## Updates Available

| Package   | Current | Latest | Type  | Deprecated             | Risk      |
| --------- | ------- | ------ | ----- | ---------------------- | --------- |
| package-a | 1.0.0   | 4.0.0  | major | No                     | 🔴 High   |
| package-b | 2.1.0   | 3.0.0  | major | Yes → use package-b-v2 | 🔴 High   |
| package-c | 1.2.0   | 1.5.0  | minor | No                     | 🟡 Medium |
| package-d | 3.0.0   | 3.0.5  | patch | No                     | 🟢 Low    |

## Up to Date

| Package   | Version |
| --------- | ------- |
| package-e | 2.0.0   |
| package-f | 1.5.0   |

---

## Security

{If no vulnerabilities found:}
✅ No known vulnerabilities found in current or target versions.

{If vulnerabilities exist:}
⚠️ {X} packages have security considerations

| Package  | Current | Target  | Current Vulnerabilities  | Target Vulnerabilities    | Recommendation                  |
| -------- | ------- | ------- | ------------------------ | ------------------------- | ------------------------------- |
| lodash   | 4.17.20 | 4.17.21 | 🔴 CVE-2021-23337 (High) | ✅ None                   | Upgrade to fix                  |
| some-pkg | 1.0.0   | 2.0.0   | ✅ None                  | 🟡 CVE-2024-1234 (Medium) | Stay on 1.0.0 or wait for patch |
| another  | 3.0.0   | 4.0.0   | 🔴 CVE-2023-111 (High)   | ✅ Fixed                  | Upgrade to 3.0.5+               |

**Legend:**

- 🔴 High/Critical severity - immediate action required
- 🟡 Medium severity - plan remediation
- 🟢 Low severity - address when convenient
- ✅ None - no known vulnerabilities

**Recommendation types:**

- **Upgrade to fix** - current version has vulnerability, latest is clean
- **Stay on current** - latest version introduced new vulnerability
- **Upgrade to specific version** - skip problematic versions, target safe one
- **Monitor** - low severity, no immediate action needed

---

## Detailed Analysis

### package-a: 1.0.0 → 4.0.0 (major) 🔴

**Security:**

- Current version: 🔴 CVE-2021-23337 - Prototype Pollution (High)
  - Advisory: https://nvd.nist.gov/vuln/detail/CVE-2021-23337
  - Fixed in: 4.0.0
- Target version: ✅ No known vulnerabilities

**Breaking changes:**

- `OldComponent` removed, use `NewComponent` instead
- `legacyProp` renamed to `modernProp`
- Minimum Node version now 18+

**Migration guide:** [Official Migration Guide](link)

**Impacted files:**
| File | Line | Impact |
|------|------|--------|
| `packages/react/src/thing.tsx` | 15 | Uses `OldComponent` |
| `apps/docs/src/example.tsx` | 42 | Uses `legacyProp` |

**Migration steps:**

1. Replace `OldComponent` with `NewComponent` in `thing.tsx`
2. Rename `legacyProp` to `modernProp` in `example.tsx`
3. Verify Node version >= 18 in CI

---

### package-b: 2.1.0 → 3.0.0 (major, deprecated) 🔴

**⚠️ Deprecated:** This package is deprecated. Use `package-b-v2` instead.

**Replacement:** [@scope/package-b-v2](npm-link)

**Migration guide:** [Migration from v2 to v3](link)

**Impacted files:**
| File | Line | Impact |
|------|------|--------|
| `packages/core/src/util.ts` | 8 | Must migrate to new package |

**Migration steps:**

1. Install replacement: `yarn add @scope/package-b-v2`
2. Update imports in `util.ts`
3. Remove old package: `yarn remove package-b`

---

### package-c: 1.2.0 → 1.5.0 (minor) 🟡

**Breaking changes:** None

**Impact:** None. Safe to upgrade.

**Migration steps:**

```bash
yarn upgrade package-c@^1.5.0
```
````

---

## Recommendations

### 🚨 Security Vulnerabilities (Address Immediately)

1. **package-a** — CVE-2021-23337 (High) in current version
   - Action: Upgrade to 4.0.0
   - Effort: Medium (has breaking changes, 2 files affected)

### ⚠️ Deprecated Packages

2. **package-b** — Deprecated, migrate to `package-b-v2`
   - Effort: Low (1 file affected)
   - Risk: Package may stop receiving security updates

### 📋 Plan Migration

3. **package-a** — Major version bump with breaking changes
   - Effort: Medium (2 files affected)
   - Suggest: Create dedicated PR for this migration

### ✅ Safe to Upgrade

4. **package-c** — Minor version (new features, no breaking changes)
5. **package-d** — Patch version (bug fixes only)

---

## Next Steps

- [ ] Address deprecated packages first (security risk)
- [ ] Create migration PR for package-a
- [ ] Batch upgrade patch/minor versions

---

_Report generated by analyze-deps skill_

```

## Error Handling

| Situation | Action |
|-----------|--------|
| npm registry unreachable | Note package as "unable to check", continue with others |
| No changelog found | Note as "changelog not found, manual review needed" |
| GitHub API rate limited | Use WebSearch fallback for breaking changes |
| Package not in registry | Note as "private or unpublished package" |

## Principles

1. **Prioritize by risk** — Security > Deprecated > Major > Minor > Patch
2. **Research thoroughly** — Don't recommend upgrades without understanding impact
3. **Only show impacted files** — Don't list all usage; only files that need changes due to breaking changes
4. **Provide actionable steps** — Every issue should have a clear resolution path
5. **Use official sources** — Prefer maintainer docs over random blog posts
6. **Use Unicode emojis** — Always use actual emoji characters (🔴 🟡 🟢 ✅), not shortcodes
```
