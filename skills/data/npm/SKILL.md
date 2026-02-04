---
name: npm
description: Full patch release with npm publish and GitHub Release. Flags: --quick (no GH release), --ci (Actions), --only (local).
---

# /sw:npm - NPM Release Automation

You are the NPM Release Assistant. Your job is to automate the patch version release process.

## STOP! READ THIS FIRST - MANDATORY GITHUB RELEASE

**FOR DEFAULT MODE (no flags): GitHub Release creation is MANDATORY!**

The workflow is NOT complete until you run `gh release create`.

**DEFAULT MODE requires ALL these steps - none are optional:**
1. Auto-commit → 2. Push → 3. Version bump → 4. Build → 5. npm publish → 6. Push tag → **7. `gh release create`** → 8. Verify release exists

**AFTER npm publish and pushing tags, you MUST:**
```bash
gh release create "v$NEW_VERSION" --title "v$NEW_VERSION" --notes-file /tmp/release-notes.md --latest
gh release view "v$NEW_VERSION"  # VERIFY it exists!
```

---

## CRITICAL: Prerelease Version Handling

**⚠️ NEVER use `npm version patch` on prerelease versions!**

`npm version patch` converts `1.0.0-rc.1` → `1.0.0` (WRONG!)

**CORRECT behavior:**
- `1.0.0-rc.1` → `1.0.0-rc.2` (increment prerelease)
- `1.0.0-beta.5` → `1.0.0-beta.6` (increment prerelease)
- `1.0.0` → `1.0.1` (increment patch - stable version)

**Use `--stable` flag ONLY when intentionally promoting to stable release!**

### Version Detection Algorithm

```bash
# Get current version
CURRENT=$(node -p "require('./package.json').version")

# Check if it's a prerelease (contains hyphen: 1.0.0-rc.1, 1.0.0-beta.2, etc.)
if [[ "$CURRENT" == *"-"* ]]; then
  IS_PRERELEASE=true
else
  IS_PRERELEASE=false
fi
```

### Version Bump Command Selection

| Current Version | Flag | Command | Result |
|-----------------|------|---------|--------|
| `1.0.0-rc.1` | (none) | `npm version prerelease` | `1.0.0-rc.2` |
| `1.0.0-rc.5` | `--stable` | `npm version patch` | `1.0.1` |
| `1.0.0` | (none) | `npm version patch` | `1.0.1` |
| `1.0.0` | `--stable` | `npm version patch` | `1.0.1` |

**Rule**: If prerelease AND no `--stable` flag → use `npm version prerelease`

## Command Modes

| Command | Flow | Use Case |
|---------|------|----------|
| `/sw:npm` | Auto-commit → **PUSH** → Bump → Build → **Publish** → Push tag → **GH Release** | **DEFAULT: FULL RELEASE** |
| `/sw:npm --quick` | Auto-commit → **PUSH** → Bump → Build → **Publish locally** → NO GH release | **QUICK: Save + Local Release** |
| `/sw:npm --ci` | Bump → Push → **CI publishes + GH Release** | Let GitHub Actions handle everything |
| `/sw:npm --only` | Bump → Build → **Publish locally** → NO push | Quick local release, push later |
| `/sw:npm --only --local` | **Bump ONLY** → NO build, NO publish, NO git | FASTEST: Local testing only |
| `/sw:npm --stable` | Same as default, but promotes prerelease to stable | **PROMOTE TO STABLE** |

## Detecting Mode

Check flags in the command invocation:

```
--quick        → QUICK MODE: save (commit+push) + local npm publish (NO GH workflow trigger)
--ci           → CI MODE: push to git, GitHub Actions publishes (requires clean working tree)
--only --local → Version bump ONLY (no build, no publish, no git) - FASTEST
--only         → Direct publish to npm (bypass CI), no git push
--stable       → Force promote prerelease to stable (use with any mode)
(no flags)     → DEFAULT: INSTANT RELEASE (auto-commit, push, build, publish, push tag)
```

**Flag Detection Order:**
1. Check for `--stable` flag → Set PROMOTE_TO_STABLE=true (affects version bump command)
2. Check for `--quick` flag → QUICK MODE (save + local publish, NO GH workflow)
3. Check for `--ci` flag → CI MODE (GitHub Actions publishes)
4. Check for `--only` flag
5. If `--only` present, check for `--local` flag → LOCAL MODE (fastest)
6. If `--only` only → DIRECT MODE
7. No flags → **DEFAULT: INSTANT RELEASE** (auto-commit dirty, push, build, publish)

**If `--quick`**: Use QUICK MODE (section "Quick Mode Workflow")
**If `--ci`**: Use CI MODE (section "CI Mode Workflow")
**If `--only --local`**: Use LOCAL MODE (section "Local Mode Workflow") - FASTEST!
**If `--only` only**: Use DIRECT MODE (section "Direct Mode Workflow")
**If no flags**: Use DEFAULT MODE = INSTANT RELEASE (section "Default Mode Workflow")

---

## DEFAULT MODE WORKFLOW (no flags) - INSTANT RELEASE

This is the **default** workflow when no flags are provided. Auto-commits any dirty changes, syncs git FIRST, then publishes to npmjs.org. One command does everything!

**Use case**: You made changes and want to release immediately. No manual steps needed.

**CRITICAL ORDER**: Git sync FIRST, then release. This ensures:
- Your code is safe on remote before any release operations
- If npm publish fails, git is already synced (clean state)
- No risk of local-only commits that could be lost

### 1. Pre-flight Check (Minimal)

```bash
# Verify we're on develop branch
git rev-parse --abbrev-ref HEAD

# Get current version
node -p "require('./package.json').version"
```

**STOP if**: Not on `develop` branch (ask user to switch)

### 2. Auto-Commit Dirty Changes (if any)

```bash
# Check for uncommitted changes
git status --porcelain
```

If dirty, generate smart commit message and commit:

```bash
git add -A
git commit -m "[auto-generated message based on changed files]"
```

**Message generation rules:**
- `src/**` changes → `fix: update implementation`
- `plugins/**` changes → `feat(plugins): update plugin`
- `.specweave/**` changes → `chore: update specweave config`
- `*.md` changes → `docs: update documentation`
- Mixed → `chore: update code and documentation`

### 3. PUSH DIRTY COMMIT TO REMOTE FIRST! (CRITICAL!)

**BEFORE any release operations, sync git:**

```bash
# Push dirty commit to remote FIRST - ensures code is safe before release
git push origin develop
```

**Why this order?**
- ✅ Your changes are safely on GitHub BEFORE release starts
- ✅ If npm publish fails later, git is already synced
- ✅ No risk of "released but not pushed" state
- ✅ Clean recovery if anything fails mid-release

### 4. Smart Version Bump (Prerelease-Aware!)

**CRITICAL: Detect prerelease and bump correctly!**

```bash
# Get current version
CURRENT=$(node -p "require('./package.json').version")
echo "Current version: $CURRENT"

# Check if prerelease (contains hyphen like 1.0.0-rc.1, 1.0.0-beta.2)
if [[ "$CURRENT" == *"-"* ]]; then
  echo "Detected PRERELEASE version"
  # Check for --stable flag in command args
  if [[ "--stable flag was passed" ]]; then
    echo "Promoting to stable (--stable flag)"
    npm version patch -m "chore: release stable version %s"
  else
    echo "Incrementing prerelease number"
    npm version prerelease -m "chore: bump version to %s"
  fi
else
  echo "Detected STABLE version"
  npm version patch -m "chore: bump version to %s"
fi
```

**Examples:**
- `1.0.0-rc.1` → `1.0.0-rc.2` (prerelease increment, DEFAULT)
- `1.0.0-rc.5` + `--stable` → `1.0.1` (promote to stable, EXPLICIT)
- `1.0.0` → `1.0.1` (patch increment)

This creates a NEW commit + tag locally.

### 5. Build Package

```bash
npm run rebuild
```

### 6. Publish to NPM (with explicit registry!)

```bash
# CRITICAL: Always specify registry to avoid ~/.npmrc redirecting to private feeds!
npm publish --registry https://registry.npmjs.org
```

### 7. Push Version Commit + Tag

```bash
# Push the version bump commit and tag
git push origin develop --follow-tags
```

### 8. MANDATORY: Create GitHub Release

**THIS STEP IS REQUIRED - DO NOT SKIP!**

The release is incomplete without a GitHub Release on the repository's Releases page.

```bash
# Get the new version
NEW_VERSION=$(node -p "require('./package.json').version")

# Extract release notes from CHANGELOG.md (if available)
if [ -f CHANGELOG.md ] && grep -q "## \[$NEW_VERSION\]" CHANGELOG.md; then
  # Extract notes between current version header and next version header
  awk "/## \[$NEW_VERSION\]/{flag=1; next} /^## \[/{flag=0} flag" CHANGELOG.md > /tmp/release-notes.md
else
  # Generate minimal release notes from recent commits
  echo "## What's Changed" > /tmp/release-notes.md
  echo "" >> /tmp/release-notes.md
  LAST_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
  if [ -n "$LAST_TAG" ]; then
    git log --oneline "$LAST_TAG"..HEAD~1 --no-merges | head -10 | sed 's/^[a-f0-9]* /- /' >> /tmp/release-notes.md
  else
    git log --oneline -10 --no-merges | sed 's/^[a-f0-9]* /- /' >> /tmp/release-notes.md
  fi
fi

# Create GitHub release (prerelease if version contains -rc, -beta, -alpha)
if [[ "$NEW_VERSION" == *"-rc"* ]] || [[ "$NEW_VERSION" == *"-beta"* ]] || [[ "$NEW_VERSION" == *"-alpha"* ]]; then
  gh release create "v$NEW_VERSION" \
    --title "v$NEW_VERSION" \
    --notes-file /tmp/release-notes.md \
    --prerelease
else
  gh release create "v$NEW_VERSION" \
    --title "v$NEW_VERSION" \
    --notes-file /tmp/release-notes.md \
    --latest
fi

# VERIFY the release was created (MANDATORY check!)
gh release view "v$NEW_VERSION" --json tagName,url
```

**What this does**:
- Extracts release notes from CHANGELOG.md (or generates from commits)
- Creates GitHub Release with proper title and notes
- Marks prereleases appropriately (rc, beta, alpha)
- Marks stable releases as "latest"
- **Verifies the release exists** (if this fails, re-run `gh release create`)

**If `gh release create` fails**: Check `gh auth status` and ensure you have write access to the repo.

### 9. Report Results

```markdown
✅ **Full patch release complete!**

📦 **Version**: vX.Y.Z
🔗 **NPM**: https://www.npmjs.com/package/specweave
🏷️ **GitHub Release**: https://github.com/anton-abyzov/specweave/releases/tag/vX.Y.Z

**What happened**:
- ✅ Dirty changes auto-committed
- ✅ Pushed to GitHub (code safe!)
- ✅ Version bumped to X.Y.Z
- ✅ Package built
- ✅ Published to npmjs.org
- ✅ Version tag pushed to GitHub
- ✅ GitHub Release created with release notes

**Verify**: `npm view specweave version --registry https://registry.npmjs.org`
```

## Default Mode Success Criteria

✅ Any dirty changes auto-committed
✅ **Dirty commit pushed to remote FIRST**
✅ Version bumped in package.json
✅ Git commit and tag created
✅ Package rebuilt
✅ Published to npmjs.org (explicit registry!)
✅ Version commit + tag pushed to GitHub
✅ **GitHub Release created with release notes**

---

## QUICK MODE WORKFLOW (--quick flag) - SAVE + LOCAL RELEASE

Use this workflow when `--quick` flag is detected. This combines `/sw:save` behavior with local npm publish. **NO GitHub workflow trigger** - everything happens locally.

**Use case**: You want to quickly save your work AND release a new patch version without waiting for GitHub Actions. Perfect for:
- Hotfixes that need immediate npm availability
- Iterative releases during active development
- When GitHub Actions are slow or unavailable

**Key difference from DEFAULT mode**: Does NOT push the version tag, so GitHub Actions release workflow is NOT triggered.

### 1. Pre-flight Check

```bash
# Verify we're on develop branch
git rev-parse --abbrev-ref HEAD

# Get current version
node -p "require('./package.json').version"
```

**STOP if**: Not on `develop` branch (ask user to switch)

### 2. Auto-Commit Dirty Changes (if any)

```bash
# Check for uncommitted changes
git status --porcelain
```

If dirty, generate smart commit message and commit:

```bash
git add -A
git commit -m "[auto-generated message based on changed files]"
```

### 3. Push Dirty Commit to Remote

```bash
# Push dirty commit to remote - ensures code is safe before release
git push origin develop
```

### 4. Smart Version Bump (Prerelease-Aware!)

```bash
CURRENT=$(node -p "require('./package.json').version")

if [[ "$CURRENT" == *"-"* ]]; then
  # Prerelease: bump prerelease number (1.0.0-rc.1 → 1.0.0-rc.2)
  npm version prerelease -m "chore: bump version to %s"
else
  # Stable: bump patch (1.0.0 → 1.0.1)
  npm version patch -m "chore: bump version to %s"
fi
```

This creates a NEW commit + tag locally.

### 5. Build Package

```bash
npm run rebuild
```

### 6. Publish to NPM Locally

```bash
# Publish directly to npmjs.org (NO GitHub Actions!)
npm publish --registry https://registry.npmjs.org
```

### 7. Push Version Commit ONLY (NO tag!)

```bash
# Push ONLY the version commit, NOT the tag
# This prevents GitHub Actions release workflow from triggering
git push origin develop
```

**CRITICAL**: Do NOT use `--follow-tags`! We want local npm publish only.

### 8. Report Results

```markdown
✅ **Quick release complete!**

📦 **Version**: vX.Y.Z
🔗 **NPM**: https://www.npmjs.com/package/specweave
🏷️ **Git Tag**: vX.Y.Z (local only - NOT pushed)

**What happened**:
- ✅ Dirty changes auto-committed
- ✅ Pushed to GitHub (code safe!)
- ✅ Version bumped to X.Y.Z
- ✅ Package built
- ✅ Published to npmjs.org (locally)
- ⏭️ Tag NOT pushed (no GitHub Actions triggered)

**Verify**: `npm view specweave version --registry https://registry.npmjs.org`

**If you want to push the tag later** (triggers GH release):
`git push origin vX.Y.Z`
```

## Quick Mode Success Criteria

✅ Any dirty changes auto-committed
✅ Dirty commit pushed to remote
✅ Version bumped in package.json
✅ Git commit and tag created locally
✅ Package rebuilt
✅ Published to npmjs.org (explicit registry!)
✅ Version commit pushed to GitHub
⏭️ Tag NOT pushed (no GitHub Actions)

---

## CI MODE WORKFLOW (--ci flag)

Use this workflow when `--ci` flag is detected. Push to git and let GitHub Actions handle npm publish.

### 1. Pre-flight Checks

```bash
# Verify we're on develop branch
git rev-parse --abbrev-ref HEAD

# Check for uncommitted changes
git status --porcelain

# Verify current version
node -p "require('./package.json').version"
```

**STOP if**:
- Not on `develop` branch (ask user to switch)
- Uncommitted changes exist (ask user to commit first)

### 2. Smart Version Bump (Prerelease-Aware!)

```bash
CURRENT=$(node -p "require('./package.json').version")

if [[ "$CURRENT" == *"-"* ]]; then
  # Prerelease: bump prerelease number
  npm version prerelease -m "chore: bump version to %s"
else
  # Stable: bump patch
  npm version patch -m "chore: bump version to %s"
fi
```

### 3. Extract New Version

```bash
# Get the new version
node -p "require('./package.json').version"
```

### 4. Push to GitHub

```bash
# Push commit and tag to trigger GitHub Actions
git push origin develop --follow-tags
```

### 5. Report Results

```markdown
✅ Release initiated successfully!

📦 **Version**: vX.Y.Z
🔗 **Tag**: https://github.com/anton-abyzov/specweave/releases/tag/vX.Y.Z
⏳ **GitHub Actions**: https://github.com/anton-abyzov/specweave/actions

**Next steps**:
1. Monitor GitHub Actions workflow (1-2 minutes)
2. Verify npm publish: https://www.npmjs.com/package/specweave
3. Check GitHub release notes
```

## CI Mode Success Criteria

✅ Version bumped in package.json
✅ Git commit created
✅ Git tag created
✅ Changes pushed to GitHub
✅ GitHub Actions workflow triggered

---

## DIRECT MODE WORKFLOW (--only flag)

Use this workflow when `--only` flag is detected. This publishes directly to npm WITHOUT git push or GitHub Actions.

### 1. Pre-flight Checks (Same as Default)

```bash
# Verify we're on develop branch
git rev-parse --abbrev-ref HEAD

# Check for uncommitted changes
git status --porcelain

# Verify current version
node -p "require('./package.json').version"
```

**STOP if**:
- Not on `develop` branch (ask user to switch)
- Uncommitted changes exist (ask user to commit first)

### 2. Smart Version Bump (Prerelease-Aware!)

```bash
CURRENT=$(node -p "require('./package.json').version")

if [[ "$CURRENT" == *"-"* ]]; then
  # Prerelease: bump prerelease number (1.0.0-rc.1 → 1.0.0-rc.2)
  npm version prerelease -m "chore: bump version to %s"
else
  # Stable: bump patch (1.0.0 → 1.0.1)
  npm version patch -m "chore: bump version to %s"
fi
```

### 3. Extract New Version

```bash
# Get the new version
node -p "require('./package.json').version"
```

### 4. Build Package

```bash
# Build the package before publishing
npm run rebuild
```

### 5. Publish to NPM Directly

```bash
# Publish directly to npmjs.org (bypasses GitHub Actions)
# CRITICAL: Always specify registry to avoid ~/.npmrc redirecting to private feeds!
npm publish --registry https://registry.npmjs.org
```

### 6. Report Results (Direct Mode)

```markdown
✅ **Published directly to npm!**

📦 **Version**: vX.Y.Z
🔗 **NPM**: https://www.npmjs.com/package/specweave
🏷️ **Git Tag**: vX.Y.Z (local only)

**What happened**:
- ✅ Version bumped and committed locally
- ✅ Git tag created locally
- ✅ Package built (npm run rebuild)
- ✅ Published to npm directly
- ⏸️ Git NOT pushed (use `git push origin develop --follow-tags` later if needed)

**Verify**:
- Check npm: https://www.npmjs.com/package/specweave
- Verify version: `npm view specweave version`

**Note**: Local release only. Push to GitHub manually when ready:
`git push origin develop --follow-tags`
```

## Direct Mode Success Criteria

✅ Version bumped in package.json
✅ Git commit created locally
✅ Git tag created locally
✅ Package rebuilt
✅ Published to npm directly
⏸️ Git NOT pushed (manual sync later)

---

## LOCAL MODE WORKFLOW (--only --local flags) - FASTEST!

Use this workflow when BOTH `--only` AND `--local` flags are detected. This is the **fastest possible** version bump - NO npm publish, NO git operations, NO build. Just increment the version number for local testing.

**Use case**: You need to quickly test a new version locally without publishing anywhere. Perfect for:
- Testing version-dependent features
- Local development iterations
- Quick version bumps before a real release

### 1. Minimal Pre-flight Check

```bash
# Just verify current version (no git checks needed!)
node -p "require('./package.json').version"
```

**NO git checks** - we're not committing or pushing anything!

### 2. Smart Version Bump (NO git commit, NO tag)

```bash
CURRENT=$(node -p "require('./package.json').version")

if [[ "$CURRENT" == *"-"* ]]; then
  # Prerelease: bump prerelease number (1.0.0-rc.1 → 1.0.0-rc.2)
  npm version prerelease --no-git-tag-version
else
  # Stable: bump patch (1.0.0 → 1.0.1)
  npm version patch --no-git-tag-version
fi
```

**What this does**:
- Updates `package.json` version ONLY
- Updates `package-lock.json` version ONLY
- Respects prerelease versions!
- NO git commit created
- NO git tag created
- INSTANT (< 1 second)

### 3. Report Results (Local Mode)

```markdown
⚡ **FAST local version bump!**

📦 **Version**: X.Y.Z → X.Y.(Z+1)

**What happened**:
- ✅ package.json version bumped
- ✅ package-lock.json updated
- ⏭️ NO git commit (use `git add . && git commit` later)
- ⏭️ NO git tag (use `git tag vX.Y.Z` later)
- ⏭️ NO npm publish (use `npm publish` later)
- ⏭️ NO build (use `npm run rebuild` later)

**Next steps when ready to release**:
1. Build: `npm run rebuild`
2. Test: `npm test`
3. Commit: `git add . && git commit -m "chore: bump version to X.Y.Z"`
4. Tag: `git tag vX.Y.Z`
5. Publish: `npm publish --registry https://registry.npmjs.org`
6. Push: `git push origin develop --follow-tags`

**Or use**: `/sw:npm` (no flags) for full instant release
```

## Local Mode Success Criteria

✅ Version bumped in package.json
✅ Version bumped in package-lock.json
⏭️ NO git commit
⏭️ NO git tag
⏭️ NO npm publish
⏭️ NO build

**Time**: < 1 second

---

## Quick Reference

```bash
# DEFAULT: Full release (auto-commits dirty, publishes, pushes + tag, GH release)
/sw:npm

# QUICK: Save + local release (auto-commits, pushes, publishes - NO GH release)
/sw:npm --quick

# CI release (GitHub Actions handles npm publish) - requires clean tree
/sw:npm --ci

# Quick local publish, sync git later
/sw:npm --only

# FASTEST: Version bump only (no publish, no git, no build)
/sw:npm --only --local

# PROMOTE prerelease to stable (1.0.0-rc.5 → 1.0.1)
/sw:npm --stable
```

| Scenario | Command | Prerelease Handling | Git Pushed | Tag Pushed | GH Release |
|----------|---------|---------------------|------------|------------|------------|
| **FULL RELEASE** | (no flags) | `rc.1`→`rc.2` (smart) | ✅ Yes | ✅ Yes | ✅ Yes |
| **QUICK RELEASE** | `--quick` | `rc.1`→`rc.2` (smart) | ✅ Yes | ❌ No | ❌ No |
| CI release | `--ci` | `rc.1`→`rc.2` (smart) | ✅ Yes | ✅ Yes | ✅ (via CI) |
| Local publish | `--only` | `rc.1`→`rc.2` (smart) | ❌ No | ❌ No | ❌ No |
| Local bump | `--only --local` | `rc.1`→`rc.2` (smart) | ❌ No | ❌ No | ❌ No |
| **PROMOTE** | `--stable` | `rc.X`→`X.Y.Z+1` | ✅ Yes | ✅ Yes | ✅ Yes |
