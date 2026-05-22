---
name: release
description: Create versioned releases - bump version via PR, tag, create GitHub release. CI publishes to npm.
---

# Release Skill

Create versioned releases with proper git tagging and GitHub release creation. The workflow is:

1. **Bump version** via PR (respects branch protection)
2. **Create tag** on the merged commit
3. **Create GitHub release** with notes
4. **CI publishes** to npm automatically

## When to Use

- After completing features/fixes ready for release
- When creating patch/minor/major version bumps
- For pre-release versions (alpha, beta, rc)
- When auditing what changes would be in a release (`--dry-run`)

**Prerequisites:**
- All related kspec tasks should be completed before release
- Run `npm test` locally to verify tests pass
- Ensure you're on `main` with a clean working tree

## Arguments

```
/release [patch|minor|major|X.Y.Z] [options]
```

| Argument | Description |
|----------|-------------|
| `patch` | Bug fixes, backwards-compatible (0.1.1 -> 0.1.2) |
| `minor` | New features, backwards-compatible (0.1.1 -> 0.2.0) |
| `major` | Breaking changes (0.1.1 -> 1.0.0) |
| `X.Y.Z` | Explicit version number |
| (none) | Auto-detect from commits since last tag |

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview only - NO changes to git, tags, PRs, or GitHub |
| `--prerelease <type>` | Create prerelease (alpha, beta, rc) |

## Workflow

### Phase 1: Detect Context

Gather information about current state:

```bash
# Get current branch
git branch --show-current

# Check for uncommitted changes
git status --porcelain

# Get current version from package.json
node -p "require('./package.json').version"

# Get last tag
git describe --tags --abbrev=0 2>/dev/null || echo "no-tags"

# Get commits since last tag
git log $(git describe --tags --abbrev=0 2>/dev/null)..HEAD --oneline
```

**Context to gather:**
- Current branch (must be `main`)
- Working tree status (must be clean)
- Current version in package.json
- Last tag (e.g., v0.1.1)
- Commits since last tag (count and list)

### Phase 2: Validate Constraints

All constraints must pass before proceeding:

| Constraint | Check | Error Message |
|------------|-------|---------------|
| On main branch | `git branch --show-current` = main | "Must be on main branch. Currently on: {branch}" |
| Clean working tree | `git status --porcelain` is empty | "Working tree must be clean. Commit or stash changes first." |
| Up to date with origin | After `git fetch`, local matches remote | "Local main is behind origin. Run: git pull" |
| Has releasable changes | At least one commit since last tag | "No changes since last tag {tag}. Nothing to release." |
| Tag doesn't exist | `git tag -l v{version}` is empty | "Tag v{version} already exists." |

**Dry-run behavior:** In dry-run mode, validation failures are reported but the preview continues. In normal mode, ANY validation failure stops execution immediately.

### Phase 3: Determine Version

If version type not specified, auto-detect from ALL commits since last tag:

```bash
# Get all commit messages since last tag (not just merges)
git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%s%n%b"
```

**Auto-detection rules (conventional commits):**

| Pattern | Bump | Notes |
|---------|------|-------|
| `BREAKING CHANGE:` in body | major | Check commit body, not just subject |
| `feat!:` or `fix!:` (with `!`) | major | The `!` suffix indicates breaking |
| `feat:` or `feat(scope):` | minor | Scope is ignored for detection |
| `fix:`, `perf:`, `refactor:`, `chore:` | patch | Any maintenance work |

**Resolution order:**
1. If ANY commit has breaking change indicator -> major
2. Else if ANY commit starts with `feat:` -> minor
3. Else -> patch

**Prerelease handling (`--prerelease <type>`):**

| Current | Flag | Result | Rule |
|---------|------|--------|------|
| 0.1.1 | `--prerelease alpha` | 0.1.2-alpha.0 | Bump patch, add prerelease |
| 0.1.2-alpha.0 | `--prerelease alpha` | 0.1.2-alpha.1 | Same type: increment counter |
| 0.1.2-alpha.1 | `--prerelease beta` | 0.1.2-beta.0 | New type: reset counter to 0 |
| 0.1.2-rc.0 | (no flag) | 0.1.2 | Stable release: drop prerelease suffix |

**Prerelease rules:**
1. Same prerelease type -> increment counter (alpha.0 -> alpha.1)
2. Different prerelease type -> reset counter (alpha.1 -> beta.0)
3. No prerelease flag on prerelease version -> promote to stable

### Phase 4: Analyze Changes for Release Notes

Parse commits and categorize them for user-friendly release notes.

**Commit selection:**
- Prefer merge commits (contain `(#N)` PR reference) to avoid duplicates
- If no merge commits, include all commits matching conventional patterns
- Deduplicate by checking if a commit's changes are already in a merge commit

**Categorization (commit type -> section):**

| Commit Type | Release Notes Section |
|-------------|----------------------|
| `feat:` | Features & Additions |
| `fix:` | Bug Fixes |
| `perf:` | Performance |
| `refactor:`, `chore:`, `build:` | Other Changes |
| `test:`, `ci:`, `docs:` | (excluded unless user-facing) |

**kspec integration:**
```bash
# Extract completed task references from commit trailers
git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%b" | grep -E "^Task: @" | sort -u
```

Completed tasks provide context for what was accomplished in this release.

### Phase 5: Preview (--dry-run)

For `--dry-run`, show comprehensive preview. **No changes are made** - no PRs, no tags, no releases.

```
## Release Preview (DRY RUN)

**Version bump:** 0.1.1 -> 0.1.2 (patch)
**Detection:** Auto-detected from 5 commits (3 fix, 2 chore)

### Validation
- [x] On main branch
- [x] Working tree clean
- [x] Up to date with origin
- [x] Has 5 commits since v0.1.1
- [x] Tag v0.1.2 does not exist

### Release Notes Preview

Bug fixes and improvements for kspec CLI.

#### Features & Additions
- Add JSON output mode for task list

#### Bug Fixes
- Fix author attribution for auto-generated notes
- Increase timeout for ref resolution

### Actions (dry-run: NOT executed)
1. Create version bump PR (package.json -> 0.1.2)
2. Wait for CI, then merge PR
3. Create tag: v0.1.2
4. Push tag to origin
5. Create GitHub release with notes above
6. CI will publish to npm

To execute: run `/release` without --dry-run
```

### Phase 6: Bump Version (PR)

**Before creating the tag**, update package.json via PR:

```bash
VERSION="0.1.2"  # calculated version

# Create branch for version bump
git checkout -b release/v$VERSION

# Update version without creating a tag
npm version $VERSION --no-git-tag-version

# Commit and push
git add package.json package-lock.json
git commit -m "chore: bump version to $VERSION"
git push -u origin release/v$VERSION

# Create PR
gh pr create --title "chore: bump version to $VERSION" --body "Prepare release v$VERSION"

# Wait for CI to pass, then merge
gh pr merge --merge --delete-branch
```

**Why version bump first?**
- The tagged commit has the correct version in package.json
- CI publishes exactly what's in package.json
- No out-of-sync state between git tag and package version

### Phase 7: Create Tag and Release

After the version PR is merged:

```bash
# Pull the merged version bump
git checkout main && git pull

# Create annotated tag (v prefix is convention for npm/semver)
git tag -a "v$VERSION" -m "Release v$VERSION"

# Push tag to origin
git push origin "v$VERSION"

# Create GitHub release (gh uses current repo automatically)
gh release create "v$VERSION" \
  --title "v$VERSION" \
  --notes "$(cat <<'EOF'
Brief summary of this release.

### Features & Additions
- Feature description

### Bug Fixes
- Fix description

### Other Changes
- Change description

**Full Changelog**: compare/v{previous}...v{version}
EOF
)"
```

**Tag naming:** Always use `v` prefix (e.g., `v0.1.2`) for consistency with npm versioning conventions and GitHub release detection.

**CI behavior:**
- Triggers on `release.published` event (within 1-2 minutes)
- Runs tests and publishes to npm with provenance
- Monitor progress at the repo's Actions tab

### Phase 8: Report Summary

After successful release:

```
## Release Complete

**Version:** v0.1.2
**Tag:** v0.1.2
**Commit:** abc1234

### Completed
- [x] Version PR created and merged
- [x] Tag created and pushed
- [x] GitHub release created
- [ ] CI publishing to npm... (check Actions tab)

**Release:** {repo}/releases/tag/v0.1.2
**CI Status:** {repo}/actions
```

## Release Notes Format

Generate **friendly, user-facing release notes** (not raw commit dumps):

```markdown
Brief high-level summary of what this release brings (1-2 sentences).

### Features & Additions
- Feature description in plain language
- Another feature

### Bug Fixes
- Fixed issue with X when Y happened
- Resolved problem where Z

### Performance
- Improved speed of X operation

### Other Changes
- Updated internal handling of Y
- Refactored Z for maintainability

**Full Changelog**: {repo}/compare/v0.1.1...v0.1.2
```

**Writing guidelines:**
- Write in past tense ("Fixed", "Added", "Improved")
- Focus on user impact, not implementation details
- Group related changes together
- Omit test-only and CI-only changes
- Use repo-relative URLs (GitHub auto-links them)

## Error Handling

| Error | Recovery |
|-------|----------|
| Not on main | `git checkout main && git pull` |
| Dirty working tree | Commit or stash changes first |
| Behind origin | `git pull origin main` |
| No changes | Nothing to release since last tag |
| Tag exists | Choose different version or `git tag -d v{version}` then `git push origin --delete v{version}` |
| PR merge fails | Check CI status, fix issues, retry merge |
| `gh` not installed | Install GitHub CLI: https://cli.github.com/ |
| `gh` not authenticated | Run `gh auth login` |
| `gh` API rate limit | Wait and retry, or use `--limit` flag |

### Rollback Procedure

If something goes wrong after partial release:

**If tag was pushed but release failed:**
```bash
# Delete remote tag
git push origin --delete v$VERSION
# Delete local tag
git tag -d v$VERSION
# Fix issue and retry
```

**If release was created but CI publish failed:**
```bash
# Option 1: Delete and retry
gh release delete v$VERSION --yes
git push origin --delete v$VERSION
git tag -d v$VERSION
# Fix issue and retry from Phase 6

# Option 2: Manually trigger publish
# Go to Actions tab, run publish workflow manually
```

**If version PR was merged but you need to abort:**
```bash
# Revert the version bump
git revert HEAD
git push origin main
# The tag was never created, so nothing else to clean up
```

## Examples

### Standard patch release
```
User: /release patch
Agent: [Validates state]
Agent: [Creates version bump PR, waits for CI, merges]
Agent: [Creates v0.1.2 tag, pushes, creates GH release]

Release v0.1.2 created successfully.
- Version PR: #122 (merged)
- Tag: v0.1.2
- Release: {repo}/releases/tag/v0.1.2
- CI publishing to npm...
```

### Auto-detect version
```
User: /release
Agent: [Analyzes 5 commits: 2 feat, 3 fix]
Detected: feat commits present -> minor bump (0.1.1 -> 0.2.0)
[Proceeds with release]
```

### Preview only
```
User: /release --dry-run
Agent: [Shows full preview, makes NO changes]
```

### Pre-release
```
User: /release minor --prerelease alpha
Agent: [Creates v0.2.0-alpha.0]
```

### Explicit version
```
User: /release 1.0.0
Agent: [Creates v1.0.0 - useful for major milestones]
```

## Key Principles

- **Version bump first**: PR before tag ensures package.json matches release
- **Validation first**: Check all constraints before any changes
- **Dry-run is safe**: Preview makes zero changes
- **Friendly release notes**: Write for users, not developers
- **Branch protection compatible**: All changes via PR
- **CI handles publishing**: Skill creates release, CI publishes to npm
- **kspec integration**: Complete tasks before release, reference them in commits

## Troubleshooting

### npm Trusted Publishers OIDC Failures

If npm publish fails with "Access token expired or revoked" + 404:

**Root cause:** Older npm versions (10.8.x bundled with Node 18) have bugs with OIDC authentication for trusted publishers.

**Fix:** Ensure the publish workflow installs `npm@latest`:
```yaml
- name: Install latest npm
  run: npm install -g npm@latest && npm --version
```

npm 11.x+ has the necessary fixes.

### PR Merge Blocked

If the version bump PR can't merge:

1. Check CI status - tests must pass
2. Check for merge conflicts - rebase if needed
3. Check branch protection rules - ensure you have merge permissions

### Tag Already Exists

If you need to re-release the same version:

```bash
# Delete existing tag (local and remote)
git tag -d v0.1.2
git push origin --delete v0.1.2

# Delete GitHub release if it exists
gh release delete v0.1.2 --yes

# Now retry the release
```

## Related Skills

- `/pr` - Create pull requests (used internally by this skill)
- `/audit` - Pre-release codebase review
- `/kspec` - Task completion tracking
