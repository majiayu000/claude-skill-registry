---
description: Full patch release with npm publish and GitHub Release. Flags: --quick (no GH release), --ci (Actions), --only (local).
user-invokable: false
---

# /sw:npm - NPM Release Automation

You are the NPM Release Assistant. Your job is to automate the patch version release process.

## STOP! READ THIS FIRST - MANDATORY GITHUB RELEASE

**FOR DEFAULT MODE (no flags): GitHub Release creation is MANDATORY!**

The workflow is NOT complete until you run `gh release create`.

**DEFAULT MODE requires ALL these steps - none are optional:**
1. Auto-commit -> 2. Push -> 3. Version bump -> 4. Build -> 5. npm publish -> 6. Push tag -> **7. `gh release create`** -> 8. Verify release exists

**AFTER npm publish and pushing tags, you MUST:**
```bash
gh release create "v$NEW_VERSION" --title "v$NEW_VERSION" --notes-file /tmp/release-notes.md --latest
gh release view "v$NEW_VERSION"  # VERIFY it exists!
```

---

## CRITICAL: Prerelease Version Handling

**NEVER use `npm version patch` on prerelease versions!**

`npm version patch` converts `1.0.0-rc.1` -> `1.0.0` (WRONG!)

**CORRECT behavior:**
- `1.0.0-rc.1` -> `1.0.0-rc.2` (increment prerelease)
- `1.0.0-beta.5` -> `1.0.0-beta.6` (increment prerelease)
- `1.0.0` -> `1.0.1` (increment patch - stable version)

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

**Rule**: If prerelease AND no `--stable` flag -> use `npm version prerelease`

## Command Modes

| Command | Flow | Use Case |
|---------|------|----------|
| `/sw:npm` | Auto-commit -> **PUSH** -> Bump -> Build -> **Publish** -> Push tag -> **GH Release** | **DEFAULT: FULL RELEASE** |
| `/sw:npm --quick` | Auto-commit -> **PUSH** -> Bump -> Build -> **Publish locally** -> NO GH release | **QUICK: Save + Local Release** |
| `/sw:npm --ci` | Bump -> Push -> **CI publishes + GH Release** | Let GitHub Actions handle everything |
| `/sw:npm --only` | Bump -> Build -> **Publish locally** -> NO push | Quick local release, push later |
| `/sw:npm --only --local` | **Bump ONLY** -> NO build, NO publish, NO git | FASTEST: Local testing only |
| `/sw:npm --stable` | Same as default, but promotes prerelease to stable | **PROMOTE TO STABLE** |

## Detecting Mode

Check flags in the command invocation:

```
--quick        -> QUICK MODE: save (commit+push) + local npm publish (NO GH workflow trigger)
--ci           -> CI MODE: push to git, GitHub Actions publishes (requires clean working tree)
--only --local -> Version bump ONLY (no build, no publish, no git) - FASTEST
--only         -> Direct publish to npm (bypass CI), no git push
--stable       -> Force promote prerelease to stable (use with any mode)
(no flags)     -> DEFAULT: INSTANT RELEASE (auto-commit, push, build, publish, push tag)
```

**Flag Detection Order:**
1. Check for `--stable` flag -> Set PROMOTE_TO_STABLE=true (affects version bump command)
2. Check for `--quick` flag -> QUICK MODE (save + local publish, NO GH workflow)
3. Check for `--ci` flag -> CI MODE (GitHub Actions publishes)
4. Check for `--only` flag
5. If `--only` present, check for `--local` flag -> LOCAL MODE (fastest)
6. If `--only` only -> DIRECT MODE
7. No flags -> **DEFAULT: INSTANT RELEASE** (auto-commit dirty, push, build, publish)

**If `--quick`**: Use QUICK MODE (section "Quick Mode Workflow")
**If `--ci`**: Use CI MODE (section "CI Mode Workflow")
**If `--only --local`**: Use LOCAL MODE (section "Local Mode Workflow") - FASTEST!
**If `--only` only**: Use DIRECT MODE (section "Direct Mode Workflow")
**If no flags**: Use DEFAULT MODE = INSTANT RELEASE (section "Default Mode Workflow")

---

## STEP 0: REPOSITORY DISCOVERY (Multi-Repo Aware) — ALWAYS RUN FIRST!

**This step runs BEFORE any workflow mode.** It determines which npm package to release.

### Detection Logic

```bash
# Check if we're in an umbrella repo with nested repositories
if [ -d "repositories" ]; then
  UMBRELLA=true
else
  UMBRELLA=false
fi
```

### If NOT an umbrella repo (`UMBRELLA=false`)

Operate on CWD as normal. Set:
```bash
UMBRELLA_ROOT=""
PKG_DIR="."
PKG_NAME=$(node -p "require('./package.json').name")
PKG_VERSION=$(node -p "require('./package.json').version")
```

### If umbrella repo (`UMBRELLA=true`)

```bash
UMBRELLA_ROOT="$(pwd)"
```

Scan for all publishable npm packages:

```bash
# Find all package.json files under repositories/ (skip node_modules)
# For each one, check:
#   1. Has "name" field
#   2. Has "version" field
#   3. NOT "private": true
# Collect: directory path, package name, version
```

**Scanning script:**
```bash
PUBLISHABLE=()
for pkg in $(find repositories -name "package.json" -not -path "*/node_modules/*" -not -path "*/docs-site/*" -maxdepth 4); do
  IS_PRIVATE=$(node -p "try { require('./$pkg').private || false } catch(e) { true }")
  if [ "$IS_PRIVATE" = "false" ]; then
    NAME=$(node -p "require('./$pkg').name")
    VERSION=$(node -p "require('./$pkg').version")
    DIR=$(dirname "$pkg")
    PUBLISHABLE+=("$DIR|$NAME|$VERSION")
  fi
done
```

**Decision:**

| Found | Action |
|-------|--------|
| **0 packages** | STOP with error: "No publishable npm packages found under repositories/" |
| **1 package** | Auto-select it, report: "Auto-selected `$PKG_NAME` (only publishable package)" |
| **2+ packages** | **Smart selection** — check which repos have changes first (see below) |

### Smart Selection for 2+ Packages

When multiple publishable packages are found, check each one for **changes** (dirty files OR unpushed commits):

```bash
# For each publishable package, check if it has changes
CHANGED=()
for entry in "${PUBLISHABLE[@]}"; do
  DIR=$(echo "$entry" | cut -d'|' -f1)
  NAME=$(echo "$entry" | cut -d'|' -f2)
  VERSION=$(echo "$entry" | cut -d'|' -f3)
  cd "$UMBRELLA_ROOT/$DIR"

  DIRTY=$(git status --porcelain)
  AHEAD=$(git rev-list @{u}..HEAD --count 2>/dev/null || echo "0")

  if [ -n "$DIRTY" ] || [ "$AHEAD" -gt 0 ]; then
    CHANGED+=("$DIR|$NAME|$VERSION")
  fi
  cd "$UMBRELLA_ROOT"
done
```

| Changed repos | Action |
|---------------|--------|
| **Exactly 1** has changes | Auto-select it, report: "Auto-selected `$NAME` (only repo with changes)" |
| **0** have changes | Ask user to choose from ALL publishable packages |
| **2+** have changes | Ask user to choose from ONLY the repos with changes |

**AskUserQuestion format (when asking is needed):**

```
Question: "Which npm package do you want to release?"
Header: "Package"
Options:
  - label: "$NAME1 (v$VERSION1)"
    description: "Path: $DIR1 — [has uncommitted changes | has N unpushed commits | no changes]"
  - label: "$NAME2 (v$VERSION2)"
    description: "Path: $DIR2 — [has uncommitted changes | has N unpushed commits | no changes]"
  ... (one per candidate package)
```

**Note**: When 0 repos have changes, show all publishable packages. When 2+ have changes, show only those with changes.

### After Selection

```bash
# Navigate to the selected package directory
cd "$PKG_DIR"

# Set variables for use throughout the workflow
PKG_NAME=$(node -p "require('./package.json').name")
PKG_VERSION=$(node -p "require('./package.json').version")
REPO_URL=$(node -p "try { const r = require('./package.json').repository; typeof r === 'string' ? r : r?.url?.replace(/\\.git$/, '') || '' } catch(e) { '' }")
GH_REPO=$(echo "$REPO_URL" | sed 's|https://github.com/||')

# Detect current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Validate branch is release-eligible (not a feature branch)
if [[ "$BRANCH" != "main" && "$BRANCH" != "develop" && "$BRANCH" != "master" ]]; then
  echo "WARNING: Current branch '$BRANCH' is not a standard release branch (main/develop/master)"
  # STOP and ask user to confirm before proceeding
fi

# Detect build command from package.json scripts
if node -p "Object.keys(require('./package.json').scripts||{}).includes('rebuild')" | grep -q true; then
  BUILD_CMD="npm run rebuild"
elif node -p "Object.keys(require('./package.json').scripts||{}).includes('build')" | grep -q true; then
  BUILD_CMD="npm run build"
else
  BUILD_CMD=""
  echo "WARNING: No build or rebuild script found — skip build step"
fi
```

**CRITICAL**: All subsequent commands in the chosen workflow run from `$PKG_DIR` as CWD.

**Report the selection** before proceeding to the workflow:
```
Selected package: $PKG_NAME v$PKG_VERSION
Directory: $PKG_DIR
Repository: $REPO_URL
Branch: $BRANCH
Build command: $BUILD_CMD
Mode: [DEFAULT|QUICK|CI|DIRECT|LOCAL]
```

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
# Verify we're on a release-eligible branch
git rev-parse --abbrev-ref HEAD

# Get current version
node -p "require('./package.json').version"
```

**STOP if**: Not on a release-eligible branch (`main`, `develop`, or `master`) — already validated in Step 0

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
- `src/**` changes -> `fix: update implementation`
- `plugins/**` changes -> `feat(plugins): update plugin`
- `.specweave/**` changes -> `chore: update specweave config`
- `*.md` changes -> `docs: update documentation`
- Mixed -> `chore: update code and documentation`

### 3. PUSH DIRTY COMMIT TO REMOTE FIRST! (CRITICAL!)

**BEFORE any release operations, sync git:**

```bash
# Push dirty commit to remote FIRST - ensures code is safe before release
git push origin $BRANCH
```

**Why this order?**
- Your changes are safely on GitHub BEFORE release starts
- If npm publish fails later, git is already synced
- No risk of "released but not pushed" state
- Clean recovery if anything fails mid-release

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
- `1.0.0-rc.1` -> `1.0.0-rc.2` (prerelease increment, DEFAULT)
- `1.0.0-rc.5` + `--stable` -> `1.0.1` (promote to stable, EXPLICIT)
- `1.0.0` -> `1.0.1` (patch increment)

This creates a NEW commit + tag locally.

### 5. Build Package

```bash
# Uses detected build command (rebuild if available, else build)
# If $BUILD_CMD is empty, skip this step and warn user
$BUILD_CMD
```

### 6. Publish to NPM (with explicit registry!)

```bash
# CRITICAL: Always specify registry to avoid ~/.npmrc redirecting to private feeds!
npm publish --registry https://registry.npmjs.org
```

### 7. Push Version Commit + Tag

```bash
# Push the version bump commit and tag
git push origin $BRANCH --follow-tags
```

### 8. MANDATORY: Create GitHub Release

**THIS STEP IS REQUIRED - DO NOT SKIP!**

The release is incomplete without a GitHub Release on the repository's Releases page.

```bash
# Get the new version
NEW_VERSION=$(node -p "require('./package.json').version")

# Extract release notes from CHANGELOG.md (if available and not a placeholder)
if [ -f CHANGELOG.md ] && grep -q "## \[$NEW_VERSION\]" CHANGELOG.md && ! grep -A5 "## \[$NEW_VERSION\]" CHANGELOG.md | grep -q "TODO: Describe your changes here"; then
  # Extract notes between current version header and next version header
  awk "/## \[$NEW_VERSION\]/{flag=1; next} /^## \[/{flag=0} flag" CHANGELOG.md > /tmp/release-notes.md
else
  # Generate release notes from recent commits (CHANGELOG missing or has TODO placeholder)
  echo "### Changes" > /tmp/release-notes.md
  echo "" >> /tmp/release-notes.md
  LAST_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
  if [ -n "$LAST_TAG" ]; then
    git log --oneline "$LAST_TAG"..HEAD~1 --no-merges | head -15 | sed 's/^[a-f0-9]* /- /' >> /tmp/release-notes.md
  else
    git log --oneline -15 --no-merges | sed 's/^[a-f0-9]* /- /' >> /tmp/release-notes.md
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
**Full patch release complete!**

**Version**: vX.Y.Z
**NPM**: https://www.npmjs.com/package/$PKG_NAME
**GitHub Release**: https://github.com/$GH_REPO/releases/tag/vX.Y.Z

**What happened**:
- Dirty changes auto-committed
- Pushed to GitHub (code safe!)
- Version bumped to X.Y.Z
- Package built
- Published to npmjs.org
- Version tag pushed to GitHub
- GitHub Release created with release notes

**Verify**: `npm view $PKG_NAME version --registry https://registry.npmjs.org`
```

## Default Mode Success Criteria

- Any dirty changes auto-committed
- **Dirty commit pushed to remote FIRST**
- Version bumped in package.json
- Git commit and tag created
- Package rebuilt
- Published to npmjs.org (explicit registry!)
- Version commit + tag pushed to GitHub
- **GitHub Release created with release notes**
- **Umbrella sync**: all sibling repos committed+pushed, umbrella repo committed+pushed

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
# Verify we're on a release-eligible branch
git rev-parse --abbrev-ref HEAD

# Get current version
node -p "require('./package.json').version"
```

**STOP if**: Not on a release-eligible branch (`main`, `develop`, or `master`) — already validated in Step 0

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
git push origin $BRANCH
```

### 4. Smart Version Bump (Prerelease-Aware!)

```bash
CURRENT=$(node -p "require('./package.json').version")

if [[ "$CURRENT" == *"-"* ]]; then
  # Prerelease: bump prerelease number (1.0.0-rc.1 -> 1.0.0-rc.2)
  npm version prerelease -m "chore: bump version to %s"
else
  # Stable: bump patch (1.0.0 -> 1.0.1)
  npm version patch -m "chore: bump version to %s"
fi
```

This creates a NEW commit + tag locally.

### 5. Build Package

```bash
# Uses detected build command; skip if $BUILD_CMD is empty
$BUILD_CMD
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
git push origin $BRANCH
```

**CRITICAL**: Do NOT use `--follow-tags`! We want local npm publish only.

### 8. Report Results

```markdown
**Quick release complete!**

**Version**: vX.Y.Z
**NPM**: https://www.npmjs.com/package/$PKG_NAME
**Git Tag**: vX.Y.Z (local only - NOT pushed)

**What happened**:
- Dirty changes auto-committed
- Pushed to GitHub (code safe!)
- Version bumped to X.Y.Z
- Package built
- Published to npmjs.org (locally)
- Tag NOT pushed (no GitHub Actions triggered)

**Verify**: `npm view $PKG_NAME version --registry https://registry.npmjs.org`

**If you want to push the tag later** (triggers GH release):
`git push origin vX.Y.Z`
```

## Quick Mode Success Criteria

- Any dirty changes auto-committed
- Dirty commit pushed to remote
- Version bumped in package.json
- Git commit and tag created locally
- Package rebuilt
- Published to npmjs.org (explicit registry!)
- Version commit pushed to GitHub
- Tag NOT pushed (no GitHub Actions)
- **Umbrella sync**: all sibling repos committed+pushed, umbrella repo committed+pushed

---

## CI MODE WORKFLOW (--ci flag)

Use this workflow when `--ci` flag is detected. Push to git and let GitHub Actions handle npm publish.

### 1. Pre-flight Checks

```bash
# Verify we're on a release-eligible branch
git rev-parse --abbrev-ref HEAD

# Check for uncommitted changes
git status --porcelain

# Verify current version
node -p "require('./package.json').version"
```

**STOP if**:
- Not on a release-eligible branch — already validated in Step 0
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
git push origin $BRANCH --follow-tags
```

### 5. Report Results

```markdown
Release initiated successfully!

**Version**: vX.Y.Z
**Tag**: https://github.com/$GH_REPO/releases/tag/vX.Y.Z
**GitHub Actions**: https://github.com/$GH_REPO/actions

**Next steps**:
1. Monitor GitHub Actions workflow (1-2 minutes)
2. Verify npm publish: https://www.npmjs.com/package/$PKG_NAME
3. Check GitHub release notes
```

## CI Mode Success Criteria

- Version bumped in package.json
- Git commit created
- Git tag created
- Changes pushed to GitHub
- GitHub Actions workflow triggered

---

## DIRECT MODE WORKFLOW (--only flag)

Use this workflow when `--only` flag is detected. This publishes directly to npm WITHOUT git push or GitHub Actions.

### 1. Pre-flight Checks (Same as Default)

```bash
# Verify we're on a release-eligible branch
git rev-parse --abbrev-ref HEAD

# Check for uncommitted changes
git status --porcelain

# Verify current version
node -p "require('./package.json').version"
```

**STOP if**:
- Not on a release-eligible branch — already validated in Step 0
- Uncommitted changes exist (ask user to commit first)

### 2. Smart Version Bump (Prerelease-Aware!)

```bash
CURRENT=$(node -p "require('./package.json').version")

if [[ "$CURRENT" == *"-"* ]]; then
  # Prerelease: bump prerelease number (1.0.0-rc.1 -> 1.0.0-rc.2)
  npm version prerelease -m "chore: bump version to %s"
else
  # Stable: bump patch (1.0.0 -> 1.0.1)
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
# Build the package before publishing; skip if $BUILD_CMD is empty
$BUILD_CMD
```

### 5. Publish to NPM Directly

```bash
# Publish directly to npmjs.org (bypasses GitHub Actions)
# CRITICAL: Always specify registry to avoid ~/.npmrc redirecting to private feeds!
npm publish --registry https://registry.npmjs.org
```

### 6. Report Results (Direct Mode)

```markdown
**Published directly to npm!**

**Version**: vX.Y.Z
**NPM**: https://www.npmjs.com/package/$PKG_NAME
**Git Tag**: vX.Y.Z (local only)

**What happened**:
- Version bumped and committed locally
- Git tag created locally
- Package built ($BUILD_CMD)
- Published to npm directly
- Git NOT pushed (use `git push origin $BRANCH --follow-tags` later if needed)

**Verify**:
- Check npm: https://www.npmjs.com/package/$PKG_NAME
- Verify version: `npm view $PKG_NAME version`

**Note**: Local release only. Push to GitHub manually when ready:
`git push origin $BRANCH --follow-tags`
```

## Direct Mode Success Criteria

- Version bumped in package.json
- Git commit created locally
- Git tag created locally
- Package rebuilt
- Published to npm directly
- Git NOT pushed (manual sync later)

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
  # Prerelease: bump prerelease number (1.0.0-rc.1 -> 1.0.0-rc.2)
  npm version prerelease --no-git-tag-version
else
  # Stable: bump patch (1.0.0 -> 1.0.1)
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
**FAST local version bump!**

**Version**: X.Y.Z -> X.Y.(Z+1)

**What happened**:
- package.json version bumped
- package-lock.json updated
- NO git commit (use `git add . && git commit` later)
- NO git tag (use `git tag vX.Y.Z` later)
- NO npm publish (use `npm publish` later)
- NO build (use `$BUILD_CMD` later)

**Next steps when ready to release**:
1. Build: `$BUILD_CMD`
2. Test: `npm test`
3. Commit: `git add . && git commit -m "chore: bump version to X.Y.Z"`
4. Tag: `git tag vX.Y.Z`
5. Publish: `npm publish --registry https://registry.npmjs.org`
6. Push: `git push origin $BRANCH --follow-tags`

**Or use**: `/sw:npm` (no flags) for full instant release
```

## Local Mode Success Criteria

- Version bumped in package.json
- Version bumped in package-lock.json
- NO git commit
- NO git tag
- NO npm publish
- NO build

**Time**: < 1 second

---

## FINAL STEP: UMBRELLA SYNC (Multi-Repo) — RUNS AFTER EVERY MODE

**Skip this step ONLY for `--only --local` mode.** For ALL other modes, this runs as the very last step.

When operating inside an umbrella repo (`UMBRELLA=true` from Step 0), the release workflow only commits+pushes the **selected package repo**. But the umbrella typically has:
- **Sibling repos** with their own uncommitted/unpushed work
- **The umbrella repo itself** with `.specweave/` increments, docs, and config changes

**All of these must be synced.** Otherwise the user sees dirty files after the release.

### Umbrella Sync Procedure

```bash
# Save the release repo path
RELEASE_REPO_DIR="$PKG_DIR"

# Navigate to umbrella root
cd "$UMBRELLA_ROOT"   # The original CWD where repositories/ was detected

# 1. Sync ALL sibling repos under repositories/
for repo_dir in repositories/*/*/; do
  # Skip if no .git directory (not a git repo)
  [ -d "$repo_dir/.git" ] || continue

  # Skip the repo we already released (already pushed)
  [ "$(cd "$repo_dir" && pwd)" = "$(cd "$RELEASE_REPO_DIR" && pwd)" ] && continue

  cd "$repo_dir"
  REPO_NAME=$(basename "$repo_dir")
  REPO_BRANCH=$(git rev-parse --abbrev-ref HEAD)

  # Check for dirty files
  if [ -n "$(git status --porcelain)" ]; then
    git add -A
    git commit -m "sync $REPO_NAME changes"
    echo "Committed dirty changes in $REPO_NAME"
  fi

  # Check for unpushed commits
  AHEAD=$(git rev-list @{u}..HEAD --count 2>/dev/null || echo "0")
  if [ "$AHEAD" -gt 0 ]; then
    git push origin "$REPO_BRANCH"
    echo "Pushed $AHEAD commit(s) in $REPO_NAME -> $REPO_BRANCH"
  fi

  cd "$UMBRELLA_ROOT"
done

# 2. Sync the umbrella repo itself
if [ -d ".git" ]; then
  if [ -n "$(git status --porcelain)" ]; then
    git add -A
    git commit -m "sync umbrella after release"
  fi

  UMBRELLA_BRANCH=$(git rev-parse --abbrev-ref HEAD)
  AHEAD=$(git rev-list @{u}..HEAD --count 2>/dev/null || echo "0")
  if [ "$AHEAD" -gt 0 ]; then
    git push origin "$UMBRELLA_BRANCH"
    echo "Pushed umbrella repo -> $UMBRELLA_BRANCH"
  fi
fi
```

### Report Sync Results

After syncing, append to the release report:

```markdown
**Umbrella sync**:
- [repo-name]: [committed N files | already clean] + [pushed N commits | up to date]
- ... (one line per repo)
- umbrella: [committed N files | already clean] + [pushed | up to date]
```

### When NOT in an umbrella (`UMBRELLA=false`)

Skip this step entirely — there's only one repo and it was already pushed.

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

# PROMOTE prerelease to stable (1.0.0-rc.5 -> 1.0.1)
/sw:npm --stable
```

| Scenario | Command | Prerelease Handling | Git Pushed | Tag Pushed | GH Release | Umbrella Sync |
|----------|---------|---------------------|------------|------------|------------|---------------|
| **FULL RELEASE** | (no flags) | `rc.1`->`rc.2` (smart) | Yes | Yes | Yes | Yes |
| **QUICK RELEASE** | `--quick` | `rc.1`->`rc.2` (smart) | Yes | No | No | Yes |
| CI release | `--ci` | `rc.1`->`rc.2` (smart) | Yes | Yes | Yes (via CI) | Yes |
| Local publish | `--only` | `rc.1`->`rc.2` (smart) | No | No | No | Yes |
| Local bump | `--only --local` | `rc.1`->`rc.2` (smart) | No | No | No | No |
| **PROMOTE** | `--stable` | `rc.X`->`X.Y.Z+1` | Yes | Yes | Yes | Yes |
