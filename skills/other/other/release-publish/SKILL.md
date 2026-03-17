---
name: release-publish
description: Publish new version to npm with proper QA, version bumping, changelog, git tag, and GitHub Release. Use when shipping a new release of @organon-methodology/tools and @organon-methodology/testing.
protocol_id: PROTO-ORG-11
protocol_file: organon/protocols/PROTOCOLS.md
tools:
  - organon-verify
  - npm-test
  - release-script
  - gh-cli
loads:
  - CLAUDE.md
---

# Release Publish Workflow

> Implements PROTO-ORG-11 from `organon/protocols/PROTOCOLS.md`. End-to-end release workflow from QA to npm publication.

---

## When to Use This Skill

Use this skill when:
- **Shipping a new version** — any planned release of the npm packages
- **After completing a milestone** — new features, bug fixes, or breaking changes ready for users

**Purpose:** Ensure every release goes through proper QA, has correct versioning, and is published via the automated pipeline.

---

## Context Loading

1. Load project constraints:
   - Read `CLAUDE.md` (project invariants and development workflow)

**Note:** The release process is mostly automated. Additional context is only needed for version bump decisions.

---

## Steps

### Step 1: Run Pre-Publish QA

Execute `/pre-publish-qa` first — this runs `organon-verify`, `npm-test`, and `npm-build` checks. **All checks must pass before proceeding.**

If any check fails, fix the issue and re-run QA. Do not skip this step.

### Step 2: Determine Version Bump Type

Review changes since last release to determine the correct bump:

| Bump Type | When to Use | Example |
|-----------|-------------|---------|
| **patch** | Bug fixes only, no new features | Fix a verification gate false positive |
| **minor** | New features, backward-compatible | Add new CLI command, new assertion |
| **major** | Breaking changes to CLI, API, or methodology | Rename a command, change config format |

**Decision heuristic:** When in doubt between patch and minor, choose minor. When in doubt between minor and major, check if existing `organon.config.json` files or CLI invocations would break.

### Step 3: Run Release Script

Use the `release-script` (`scripts/release.mjs`) to bump versions and create the release:

```bash
node scripts/release.mjs <patch|minor|major>
```

The script performs these actions atomically:
1. Validates: git repo, on `master`, clean tree, `gh` CLI available
2. Reads current version from `packages/tools/package.json`
3. Computes next version
4. Updates version in: both `package.json` files, `organon.config.json`, `METHODOLOGY_VERSION` constant
5. Updates `CHANGELOG.md` with new version header + date
6. Git commits as `chore: release v{version}`
7. Creates git tag `v{version}`
8. Pushes commit and tags
9. Creates GitHub Release with auto-generated notes

### Step 4: Verify GitHub Release

Use `gh-cli` to confirm the release exists:
```bash
gh release view v{version}
```

Check that the title, tag, and notes are correct.

### Step 5: Monitor CI Publish

The `.github/workflows/release.yml` workflow triggers automatically when a GitHub Release is published.

```bash
gh run list --workflow=release.yml --limit 1
```

Monitor until the workflow completes successfully. It will:
- Build and test both packages
- Verify version/tag alignment
- Publish `@organon-methodology/testing` then `@organon-methodology/tools` with provenance

### Step 6: Verify npm Availability

After CI completes:
```bash
npm info @organon-methodology/tools version
npm info @organon-methodology/testing version
```

Both should report the new version.

### Step 7: Update README (Major Versions Only)

For major version bumps, check if README.md install instructions need updating:
- Package name changes
- CLI command changes
- Configuration format changes

---

## Version Bump Decision Heuristics

| Change Type | Bump | Example |
|-------------|------|---------|
| Fix typo in CLI output | patch | Error message correction |
| Fix false positive in verification gate | patch | Gate was incorrectly failing |
| Add new CLI command | minor | `organon discover` |
| Add new verification gate | minor | New `imports` gate |
| Add new assertion to `@organon-methodology/testing` | minor | `assertPattern()` |
| New protocol or skill | minor | PROTO-ORG-12 |
| Rename existing CLI command | **major** | `organon validate` → `organon check` |
| Change `organon.config.json` schema | **major** | Rename a config key |
| Remove a verification gate | **major** | Drop `coverage` gate |
| Change methodology version format | **major** | Semver → calver |

---

## Verification

- [ ] Pre-publish QA passed completely (PROTO-ORG-10)
- [ ] Version bump type is appropriate for the changes
- [ ] Release script completed without errors
- [ ] GitHub Release exists with correct tag and notes
- [ ] GitHub Actions publish workflow succeeded (green check)
- [ ] Both packages available on npm at new version
- [ ] README is current (for major version bumps)

---

## Error Recovery

| Failure | Recovery Action |
|---------|-----------------|
| Release script fails: "not clean" | Commit or stash pending changes, then retry. |
| Release script fails: "not on master" | Switch to master: `git checkout master`. |
| Release script fails: "gh not found" | Install GitHub CLI: `brew install gh` or `winget install GitHub.cli`. |
| GitHub Actions publish fails: 401 | `NPM_TOKEN` secret is expired. Regenerate at npmjs.com and update GitHub secret. |
| GitHub Actions publish fails: 403 | Package version may already exist. Check npm for partial publish. |
| Version mismatch in CI | Release script has a bug. Fix the script, delete the tag/release, and re-run. |
| npm shows old version after publish | npm CDN may cache. Wait 5 minutes and retry `npm info`. |
