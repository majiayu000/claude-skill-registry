---
name: github-pull-request
description: Creates, updates, and merges GitHub pull requests using GitHub CLI. Handles the complete PR lifecycle including validation, creation, labeling, review, squash merge, and automatic semantic versioning with git tags. Use when user wants to create a PR, update existing PR, merge with squash, manage PR workflow, or create releases with version tags. Requires GitHub CLI (gh) installed and authenticated. Works with project-specific conventions for JordiNodeJS/thesimpsonsapi.
---

# GitHub Pull Request Management

This skill manages the complete lifecycle of GitHub pull requests for the **thesimpsonsapi** project using GitHub CLI (`gh`). It handles PR creation, updates, labeling, validation, squash merging, and automatic release tagging with semantic versioning.

## Project Context

- **Repository**: JordiNodeJS/thesimpsonsapi
- **Default assignee**: JordiNodeJS
- **Default base branch**: main
- **Merge strategy**: squash and merge
- **Package manager**: pnpm
- **Release strategy**: Semantic Versioning (MAJOR.MINOR.PATCH)

## Quick Start: Merge with Release Tag

The most common workflow - merge a PR and automatically create a version-tagged release:

```bash
# Merge PR #42 and create release v1.2.0
./scripts/merge-and-release.sh 42

# Preview what would happen
./scripts/merge-and-release.sh 42 --dry-run

# Just merge, don't create release
./scripts/merge-and-release.sh 42 --no-tag
```

See [Release Tagging Guide](docs/RELEASE_TAGGING.md) for detailed information.

## When to Use This Skill

Use this skill when the user requests:

✅ **PR Creation**

- "Create a pull request"
- "Open a PR for my changes"
- "Make a PR with title X"
- "Create draft PR"

✅ **PR Management**

- "Add labels to the PR"
- "Assign reviewers"
- "Update PR description"

✅ **PR Merging**

- "Squash and merge the PR"
- "Merge PR #123"
- "Merge my pull request"

✅ **PR Merging with Release Tag**

- "Merge and create release tag"
- "Merge PR and bump version"
- "Create release after merge"
- "Merge PR with semantic versioning"

❌ **Do NOT use when**

- Uncommitted changes exist (guide user to commit first)
- Branch not pushed to remote (guide user to push)
- GitHub CLI not installed (provide installation instructions)
- GitHub CLI not authenticated (guide through `gh auth login`)

## Prerequisites

### 1. GitHub CLI Installation

Check installation:

```bash
gh --version
```

Installation commands:

- **Windows**: `winget install --id GitHub.cli`
- **macOS**: `brew install gh`
- **Linux**: See https://github.com/cli/cli/blob/trunk/docs/install_linux.md

### 2. Authentication

```bash
# Check auth status
gh auth status

# Authenticate if needed
gh auth login
```

### 3. Repository Status

```bash
# Verify git repository
git status

# Get current branch
git branch --show-current

# Verify branch is pushed
git rev-parse --abbrev-ref @{u}

# Check for uncommitted changes
git status --porcelain
```

---

## Part 1: Creating Pull Requests

### Step 1: Local Validations

**IMPORTANT**: Always run these validations before creating a PR:

```bash
# 1. Fix linting issues
pnpm lint:fix

# 2. Run tests (if configured)
pnpm test

# 3. Build project
pnpm build
```

If any validation fails:

- Mark PR with appropriate label (`ci/failed`, `status/blocked`)
- Comment the errors in PR
- Do NOT proceed to auto-merge

### Step 2: Detect Current Branch and Check Existing PR

```bash
# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Check if PR already exists for this branch
gh pr list --head "$BRANCH" --json number,url,state
```

If PR exists: update it instead of creating new one.

### Step 3: Generate PR Content

**⚠️ CRITICAL: UTF-8 and Encoding Issues**

GitHub CLI on Windows can have issues with UTF-8 characters and emojis. Follow these rules:

1. **ALWAYS use `--body-file` instead of `--body`**
2. **NEVER use emojis** (✅, 🚀, etc.) - they appear as �
3. **Use text-based checkmarks**: `- [x] Done` instead of ✅
4. **Create temporary files** with UTF-8 encoding

#### Create PR Body File

Create `.pr-body-temp.md`:

```markdown
## Summary

Brief description of changes (2-4 lines).

## Changes Made

- Change 1
- Change 2
- Change 3

## Context and References

- Project State: [.github/project/PROJECT-STATE.md](.github/project/PROJECT-STATE.md)
- Related Prompts: [.github/prompts/](.github/prompts/)
- Documentation: [docs/](docs/)

## Validation Steps

To test locally:

1. Clone and checkout branch
2. Run `pnpm install`
3. Run `pnpm lint:fix && pnpm build`
4. Test functionality

## Pre-merge Checklist

- [x] ESLint passes
- [x] Build successful
- [x] Tests pass (if applicable)
- [x] Documentation updated
- [x] No console errors
- [ ] Accessibility verified
- [ ] Performance tested
```

### Step 4: Create or Update PR

**Creating new PR:**

```bash
# Create PR using body file (CORRECT)
gh pr create \
  --title "feat(scope): brief description" \
  --body-file .pr-body-temp.md \
  --base main \
  --assignee JordiNodeJS

# NEVER use --body with multiline (INCORRECT)
# gh pr create --body "Line 1\nLine 2"  # \n appears as literal text
```

**Updating existing PR:**

```bash
# Update PR content
gh pr edit <pr-number> \
  --title "updated title" \
  --body-file .pr-body-temp.md
```

**Clean up temporary file:**

```bash
rm .pr-body-temp.md
```

### Step 5: Add Labels

**Project-specific labels by branch type:**

- `feat/*` → `type/feature`, `status/ready-for-review`, `priority/medium`
- `fix/*` → `type/bugfix`, `status/ready-for-review`, `priority/medium`
- `refactor/*` → `type/refactor`, `status/ready-for-review`, `priority/medium`
- `docs/*` → `type/docs`, `status/ready-for-review`, `priority/low`

**Additional labels:**

- `area/<area>` - For specific area (e.g., `area/header`)
- `ci/required` - For PRs requiring CI checks
- `auto-changelog` - For automatic changelog generation

```bash
# List existing labels
gh label list

# Create label if missing
gh label create "type/feature" --color "0E8A16" --description "New feature"

# Add labels to PR
gh pr edit <pr-number> --add-label "type/feature,status/ready-for-review,priority/medium"
```

### Step 6: Add Context Comment

**IMPORTANT**: Use `--body-file` for comments too!

Create `.pr-comment-temp.md`:

```markdown
## Validation Results

- [x] ESLint: PASSED
- [x] Build: PASSED
- [x] Tests: PASSED

## Context Extracted

Relevant files:

- .github/project/PROJECT-STATE.md
- docs/ARCHITECTURE.md

## Next Steps

1. Review changes
2. Verify functionality
3. Approve if ready
```

Add comment:

```bash
# CORRECT - Using body-file
gh pr comment <pr-number> --body-file .pr-comment-temp.md
rm .pr-comment-temp.md

# INCORRECT - \n literals don't work
# gh pr comment <pr-number> --body "Line 1\nLine 2"
```

### Step 7: Request Review

```bash
# Add reviewer
gh pr edit <pr-number> --add-reviewer JordiNodeJS

# Or request review
gh pr review <pr-number> --request-review JordiNodeJS
```

---

## Pre-Merge Code Quality Checklist

### ⚠️ SonarQube/Code Quality Validation (CRITICAL GATE)

**Before creating a PR or merging, ALWAYS run SonarLint analysis on modified files:**

#### Why This Matters

SonarQube detects:

- Type safety issues (`any` types, implicit conversions)
- Error handling problems (wrong exception types, untyped catch blocks)
- Security hotspots
- Performance issues
- Maintainability concerns

**Lesson learned**: PR #14 had 9 SonarQube issues that delayed merge. Type errors in test mocks and hooks violated code quality gates.

#### Severity Matrix (Pre-Merge Decision Tree)

| Severity        | Examples                                       | Action         | Timeline                                    |
| --------------- | ---------------------------------------------- | -------------- | ------------------------------------------- |
| 🔴 **BLOCKER**  | Unused imports, type mismatches, `any` types   | **MUST FIX**   | Before merge                                |
| 🟠 **CRITICAL** | Untyped `catch` blocks, missing error handling | **MUST FIX**   | Before merge                                |
| 🟡 **MAJOR**    | `instanceof` checks, hardcoded strings         | **Should fix** | Before merge (can defer with justification) |
| 🔵 **MINOR**    | Code style, naming conventions                 | **Can defer**  | In next iteration                           |
| ⚪ **INFO**     | Documentation, comments                        | **Optional**   | Per team preference                         |

#### Quick SonarLint Analysis Workflow

```bash
# 1. Get modified files in your PR
git diff --name-only main...$(git rev-parse --abbrev-ref HEAD) | grep -E "\.(ts|tsx)$"

# 2. Run SonarLint analysis on each file
# - Open VS Code
# - Open each modified file
# - Use SonarLint extension to see issues (Problems panel)
# OR use the sonarqube_analyze_file tool

# 3. Fix all BLOCKER and CRITICAL issues before PR

# 4. If MAJOR issues can't be fixed:
#    - Add comment in PR explaining why
#    - Get approval from reviewer
#    - Add label "tech-debt/approved" to PR
```

#### Common Issues and Fast Fixes

**Issue: `as any` type casting**

```typescript
// ❌ WRONG - SonarQube: "Avoid using 'any' type"
prismaMock.character.findMany.mockResolvedValue(mockNames as any);

// ✅ CORRECT - Use type-safe casting
const mockNames: Character[] = [{ id: 1, name: "Homer", ... }];
prismaMock.character.findMany.mockResolvedValue(mockNames);
// OR if impossible:
prismaMock.character.findMany.mockResolvedValue(mockNames as unknown as Character[]);
```

**Issue: Untyped `catch` block**

```typescript
// ❌ WRONG - SonarQube: "Catch block missing error type"
} catch (error) {
  console.error("Error:", error); // error is untyped
}

// ✅ CORRECT - Type the error
} catch (error) {
  if (error instanceof Error) {
    console.error("Error:", error.message);
  }
}
```

**Issue: Window object without globalThis**

```typescript
// ❌ WRONG - SonarQube: "Prefer globalThis over window"
if (typeof window !== "undefined") {
  window.localStorage.setItem(key, value);
}

// ✅ CORRECT - Use globalThis
if (globalThis.window !== undefined) {
  globalThis.window.localStorage.setItem(key, value);
}
```

**Issue: Wrong error type**

```typescript
// ❌ WRONG - SonarQube: "Use TypeError for type checks"
if (typeof x !== "number") {
  throw new Error("Expected number");
}

// ✅ CORRECT - Use specific error type
if (typeof x !== "number") {
  throw new TypeError(`Expected number, got ${typeof x}`);
}
```

**Issue: Unused imports**

```typescript
// ❌ WRONG - SonarQube: "Remove unused import"
import { getCurrentUser } from "@/auth"; // Not used in this file
import { getCurrentUserOptional } from "@/auth";

// ✅ CORRECT - Remove only what's not used
import { getCurrentUserOptional } from "@/auth";
```

#### Mock Data Type Correctness

When creating mock data for tests, ensure ALL required fields match the schema:

```typescript
// ❌ WRONG - Missing required fields
const mockCharacter = {
  id: 1,
  name: "Homer",
  imageUrl: null,
};
// Error: "Property 'externalId' is missing"

// ✅ CORRECT - Include all required fields
const mockCharacter = {
  id: 1,
  name: "Homer",
  externalId: 1,
  occupation: null,
  imageUrl: null,
};
```

#### PR Label for Code Quality

Add `quality/verified` label after SonarLint passes:

```bash
gh pr edit <pr-number> --add-label "quality/verified"
```

---

## Part 2: Merging Pull Requests

### Step 1: Verify PR State

```bash
# Get PR state and mergability
gh pr view <pr-number> --json state,mergeable,mergeStateStatus,headRefName

# Check CI status
gh pr checks <pr-number>

# List reviews
gh pr review <pr-number> --list
```

### Step 2: Handle Different States

**States and Actions:**

| State              | Status          | Action                                         |
| ------------------ | --------------- | ---------------------------------------------- |
| OPEN + CLEAN       | All checks pass | Proceed to merge                               |
| OPEN + CONFLICTING | Has conflicts   | Report conflicts, add `status/conflicts` label |
| OPEN + BEHIND      | Behind base     | Update branch, re-verify                       |
| OPEN + UNSTABLE    | Checks failing  | Add `ci/failed` label, wait                    |
| CLOSED             | Already closed  | Report status                                  |
| MERGED             | Already merged  | Report status                                  |

**Handle conflicts:**

```bash
# If conflicts detected
gh pr edit <pr-number> --add-label "status/conflicts"

# Comment with resolution steps
echo "## Merge Conflicts Detected

To resolve:
1. git checkout <branch>
2. git pull origin main
3. Resolve conflicts
4. git push

Then re-request merge." > .pr-conflict-comment.md

gh pr comment <pr-number> --body-file .pr-conflict-comment.md
rm .pr-conflict-comment.md
```

**Update if behind:**

```bash
# Checkout branch
git checkout <branch>

# Update from main
git pull origin main

# Push updates
git push

# Re-verify
gh pr checks <pr-number>
```

### Step 3: Squash and Merge

**Only proceed if:**

- ✅ State is OPEN
- ✅ mergeStateStatus is CLEAN
- ✅ All CI checks pass
- ✅ Required approvals received

```bash
# Squash and merge with automatic branch deletion
gh pr merge <pr-number> --squash --delete-branch

# Get merge commit hash
MERGE_COMMIT=$(gh pr view <pr-number> --json mergeCommit --jq .mergeCommit.oid)
```

### Step 4: Post-merge Cleanup

```bash
# Switch to main
git checkout main

# Update local main
git pull origin main

# Delete local branch if still exists
git branch -D <branch-name>

# Verify remote branch deletion
gh pr view <pr-number> --json headRefName,headRefOid
```

---

## Complete Workflow Examples

### Example 1: Create PR and Label

**User Request:**

> "Create a PR for my header changes and label it"

**Actions:**

```bash
# 1. Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
# Output: feat/simpsons-theme-header

# 2. Run validations
pnpm lint:fix && pnpm build

# 3. Check existing PR
gh pr list --head "$BRANCH"
# Output: (empty - no existing PR)

# 4. Create body file
cat > .pr-body-temp.md << 'EOF'
## Summary

Added themed header component that changes appearance based on current route.

## Changes Made

- Created SimpsonsHeader component with route-specific themes
- Added animated elements (clouds, donuts, TV, books)
- Integrated into main layout
- Dark mode compatible

## Context and References

- Project State: [.github/project/PROJECT-STATE.md](.github/project/PROJECT-STATE.md)

## Validation Steps

1. Run `pnpm dev`
2. Navigate to different routes (/characters, /episodes, /diary, /collections)
3. Verify theme changes and animations

## Pre-merge Checklist

- [x] ESLint passes
- [x] Build successful
- [x] Dark mode tested
- [x] Animations working
EOF

# 5. Create PR
gh pr create \
  --title "feat: add themed header component" \
  --body-file .pr-body-temp.md \
  --base main \
  --assignee JordiNodeJS

# Output: https://github.com/JordiNodeJS/thesimpsonsapi/pull/123

# 6. Add labels
gh pr edit 123 --add-label "type/feature,status/ready-for-review,priority/medium,area/header"

# 7. Clean up
rm .pr-body-temp.md
```

**Output:**

```markdown
- pr_number: 123
- pr_url: https://github.com/JordiNodeJS/thesimpsonsapi/pull/123
- branch: feat/simpsons-theme-header
- merge_commit: null
- deleted_remote_branch: false
- deleted_local_branch: false
- warnings: []
- errors: []
```

---

### Example 2: Squash and Merge PR

**User Request:**

> "Squash and merge PR #123"

**Actions:**

```bash
# 1. Check PR state
gh pr view 123 --json state,mergeable,mergeStateStatus
# Output: {"state":"OPEN","mergeable":"MERGEABLE","mergeStateStatus":"CLEAN"}

# 2. Verify checks
gh pr checks 123
# Output: All checks pass

# 3. Check reviews
gh pr review 123 --list
# Output: Approved by JordiNodeJS

# 4. Squash and merge
gh pr merge 123 --squash --delete-branch

# 5. Get merge commit
MERGE_COMMIT=$(gh pr view 123 --json mergeCommit --jq .mergeCommit.oid)

# 6. Cleanup
git checkout main
git pull origin main
git branch -D feat/simpsons-theme-header
```

**Output:**

```markdown
- pr_number: 123
- pr_url: https://github.com/JordiNodeJS/thesimpsonsapi/pull/123
- branch: feat/simpsons-theme-header
- merge_commit: abc123def456789...
- deleted_remote_branch: true
- deleted_local_branch: true
- warnings: []
- errors: []
```

---

### Example 3: Handle Conflicts

**User Request:**

> "Merge PR #124"

**Actions:**

````bash
# 1. Check state
gh pr view 124 --json mergeStateStatus
# Output: {"mergeStateStatus":"CONFLICTING"}

# 2. Add conflicts label
gh pr edit 124 --add-label "status/conflicts"

# 3. Create conflict resolution comment
cat > .pr-conflict-comment.md << 'EOF'
## Merge Conflicts Detected

This PR has conflicts that need to be resolved.

### Resolution Steps

1. Update your local branch:
   ```bash
   git checkout feat/branch-name
   git pull origin main
````

2. Resolve conflicts in your editor

3. Commit the resolution:

   ```bash
   git add .
   git commit -m "fix: resolve merge conflicts"
   git push
   ```

4. Re-request merge after conflicts are resolved

### Files with conflicts

Run `git status` to see conflicting files.
EOF

gh pr comment 124 --body-file .pr-conflict-comment.md
rm .pr-conflict-comment.md

````

**Output:**

```markdown
- pr_number: 124
- pr_url: https://github.com/JordiNodeJS/thesimpsonsapi/pull/124
- branch: feat/branch-with-conflicts
- merge_commit: null
- deleted_remote_branch: false
- deleted_local_branch: false
- warnings: ["Merge conflicts detected"]
- errors: ["Cannot merge: CONFLICTING state"]
````

---

## PR Title Conventions

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

Examples:
feat(header): add themed header component
fix(auth): resolve login timeout issue
docs(readme): update installation steps
style(layout): format with prettier
refactor(api): simplify database queries
test(auth): add unit tests for login
chore(deps): update dependencies
```

**Types:**

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance
- `perf:` Performance
- `ci:` CI/CD
- `build:` Build system

---

## Troubleshooting

### Issue 1: GitHub CLI Not Installed

**Error:**

```
gh: command not found
```

**Solution:**

```bash
# Windows
winget install --id GitHub.cli

# Verify
gh --version
```

### Issue 2: Not Authenticated

**Error:**

```
To authenticate, please run: gh auth login
```

**Solution:**

```bash
gh auth login
# Follow interactive prompts
```

### Issue 3: Branch Not Pushed

**Error:**

```
fatal: The current branch has no upstream branch
```

**Solution:**

```bash
git push -u origin <branch-name>
```

### Issue 4: Validation Failures

**Error:**

```
ESLint errors found
```

**Solution:**

```bash
# Fix automatically
pnpm lint:fix

# Or manually fix errors
# Then commit and push
```

### Issue 5: PR Already Exists

**Error:**

```
A pull request for branch "feat/x" already exists: #123
```

**Solution:**

```bash
# Update existing PR instead
gh pr edit 123 --title "new title" --body-file .pr-body-temp.md
```

---

## Quick Reference Commands

### PR Creation

```bash
gh pr create --title "..." --body-file body.md --base main --assignee JordiNodeJS
gh pr list --head <branch>
gh pr edit <pr> --title "..." --body-file body.md
```

### PR Management

```bash
gh pr view <pr>
gh pr edit <pr> --add-label "label1,label2"
gh pr edit <pr> --add-reviewer username
gh pr comment <pr> --body-file comment.md
```

### PR Merging

```bash
gh pr view <pr> --json state,mergeable,mergeStateStatus
gh pr checks <pr>
gh pr review <pr> --list
gh pr merge <pr> --squash --delete-branch
```

### Cleanup

```bash
git checkout main
git pull origin main
git branch -D <local-branch>
```

---

## Part 2b: Release Versioning and Git Tags

### Automatic Release Tag Creation

After a PR is successfully merged, a release tag should be created using semantic versioning.

#### Step 1: Determine Version Number

The version follows Semantic Versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (non-breaking)
- **PATCH**: Bug fixes

```bash
# Get current version from git tags
CURRENT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")

# Parse current version
CURRENT_VERSION=${CURRENT_TAG#v}  # Remove 'v' prefix
MAJOR=$(echo $CURRENT_VERSION | cut -d. -f1)
MINOR=$(echo $CURRENT_VERSION | cut -d. -f2)
PATCH=$(echo $CURRENT_VERSION | cut -d. -f3)

# Determine next version based on PR type
# Check PR title for type prefix
if [[ "$PR_TITLE" == feat* ]] || [[ "$PR_TITLE" == feature* ]]; then
  # New feature = MINOR bump
  NEXT_VERSION="v$MAJOR.$((MINOR+1)).0"
elif [[ "$PR_TITLE" == fix* ]] || [[ "$PR_TITLE" == bugfix* ]] || [[ "$PR_TITLE" == patch* ]]; then
  # Bug fix = PATCH bump
  NEXT_VERSION="v$MAJOR.$MINOR.$((PATCH+1))"
else
  # Default to PATCH bump
  NEXT_VERSION="v$MAJOR.$MINOR.$((PATCH+1))"
fi
```

#### Step 2: Create Release Tag

After PR merge is confirmed:

```bash
# Get PR number and merge commit
PR_NUMBER=$1  # Passed from merge workflow
MERGE_COMMIT=$(gh pr view $PR_NUMBER --json mergeCommit --jq '.mergeCommit.oid')
PR_TITLE=$(gh pr view $PR_NUMBER --json title --jq '.title')

# Calculate new version
CURRENT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
CURRENT_VERSION=${CURRENT_TAG#v}
MAJOR=$(echo $CURRENT_VERSION | cut -d. -f1)
MINOR=$(echo $CURRENT_VERSION | cut -d. -f2)
PATCH=$(echo $CURRENT_VERSION | cut -d. -f3)

if [[ "$PR_TITLE" == feat* ]]; then
  NEXT_VERSION="v$MAJOR.$((MINOR+1)).0"
else
  NEXT_VERSION="v$MAJOR.$MINOR.$((PATCH+1))"
fi

# Fetch latest from main
git fetch origin main
git checkout main
git pull origin main

# Create annotated tag with release notes
cat > .release-notes.md << EOF
# Release $NEXT_VERSION

Merged PR #$PR_NUMBER: $PR_TITLE

**Merge Commit**: $MERGE_COMMIT

## What's New

See PR #$PR_NUMBER for full details of changes included in this release.

**Date**: $(date -u +'%Y-%m-%dT%H:%M:%SZ')
EOF

# Create tag
git tag -a "$NEXT_VERSION" -F .release-notes.md

# Push tag to remote
git push origin "$NEXT_VERSION"

# Clean up temp file
rm .release-notes.md
```

#### Step 3: Create GitHub Release

```bash
# After tag is pushed, create GitHub release
gh release create "$NEXT_VERSION" \
  --title "Release $NEXT_VERSION" \
  --notes-file .release-notes.md

# Or with inline notes
gh release create "$NEXT_VERSION" \
  --title "Release $NEXT_VERSION" \
  --notes "Merged PR #$PR_NUMBER: $PR_TITLE"
```

#### Full Merge with Release Tag Workflow

**Automated approach (RECOMMENDED):**

```bash
# Use the automated merge-and-release script
./scripts/merge-and-release.sh 42

# Output shows:
# ℹ Title: feat(header): add themed header
# ℹ Branch: feat/simpsons-header
# ℹ Current version: v1.0.0
# ℹ Bump type: MINOR
# ℹ Next version: v1.1.0
# ✓ PR merged successfully
# ✓ Tag v1.1.0 created locally
# ✓ Tag pushed to remote
# ✓ GitHub release created
# ✓ All steps completed successfully!
```

**Manual approach (if needed):**

```bash
#!/bin/bash

# Complete workflow: Merge PR and create release tag

PR_NUMBER=$1
if [ -z "$PR_NUMBER" ]; then
  echo "Usage: merge-with-tag.sh <PR_NUMBER>"
  exit 1
fi

echo "Processing PR #$PR_NUMBER for merge and release..."

# 1. Verify PR is ready
echo "Step 1: Verifying PR state..."
PR_STATE=$(gh pr view $PR_NUMBER --json state --jq '.state')
if [ "$PR_STATE" != "OPEN" ]; then
  echo "Error: PR #$PR_NUMBER is not OPEN (state: $PR_STATE)"
  exit 1
fi

# 2. Check if mergeable
echo "Step 2: Checking merge status..."
MERGE_STATUS=$(gh pr view $PR_NUMBER --json mergeStateStatus --jq '.mergeStateStatus')
if [ "$MERGE_STATUS" != "CLEAN" ]; then
  echo "Error: PR has conflicts or checks failing (status: $MERGE_STATUS)"
  exit 1
fi

# 3. Get PR info
PR_TITLE=$(gh pr view $PR_NUMBER --json title --jq '.title')
PR_BODY=$(gh pr view $PR_NUMBER --json body --jq '.body')
echo "Step 3: PR Title: $PR_TITLE"

# 4. Squash and merge
echo "Step 4: Merging PR #$PR_NUMBER..."
gh pr merge $PR_NUMBER --squash --delete-branch
MERGE_COMMIT=$(git rev-parse HEAD~0)  # Get latest commit after merge

# 5. Calculate version
echo "Step 5: Calculating new version..."
CURRENT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
CURRENT_VERSION=${CURRENT_TAG#v}
MAJOR=$(echo $CURRENT_VERSION | cut -d. -f1)
MINOR=$(echo $CURRENT_VERSION | cut -d. -f2)
PATCH=$(echo $CURRENT_VERSION | cut -d. -f3)

if [[ "$PR_TITLE" == feat* ]]; then
  NEXT_VERSION="v$MAJOR.$((MINOR+1)).0"
else
  NEXT_VERSION="v$MAJOR.$MINOR.$((PATCH+1))"
fi

echo "Version progression: $CURRENT_TAG -> $NEXT_VERSION"

# 6. Create release tag
echo "Step 6: Creating release tag $NEXT_VERSION..."
git tag -a "$NEXT_VERSION" -m "Release $NEXT_VERSION

Merged PR #$PR_NUMBER: $PR_TITLE
Merge Commit: $MERGE_COMMIT

Release Date: $(date -u +'%Y-%m-%d %H:%M:%S UTC')"

# 7. Push tag
echo "Step 7: Pushing tag to remote..."
git push origin "$NEXT_VERSION"

# 8. Create GitHub release
echo "Step 8: Creating GitHub Release..."
gh release create "$NEXT_VERSION" \
  --title "Release $NEXT_VERSION" \
  --notes "Merged PR #$PR_NUMBER: $PR_TITLE

**Merge Commit**: $MERGE_COMMIT

See PR #$PR_NUMBER for full details."

echo ""
echo "✓ PR #$PR_NUMBER merged and release $NEXT_VERSION created!"
echo "Release URL: https://github.com/JordiNodeJS/thesimpsonsapi/releases/tag/$NEXT_VERSION"
```

#### Usage Examples

**Example 1: Merge feature PR and create minor release**

```bash
# PR #42 with title "feat(header): add themed header"
./merge-with-tag.sh 42

# Output:
# Processing PR #42 for merge and release...
# Step 1: Verifying PR state... OK
# Step 2: Checking merge status... CLEAN
# Step 3: PR Title: feat(header): add themed header
# Step 4: Merging PR #42...
# Step 5: Calculating new version...
# Version progression: v1.0.0 -> v1.1.0
# Step 6: Creating release tag v1.1.0...
# Step 7: Pushing tag to remote...
# Step 8: Creating GitHub Release...
# ✓ PR #42 merged and release v1.1.0 created!
```

**Example 2: Merge bugfix PR and create patch release**

```bash
# PR #45 with title "fix(auth): resolve login timeout"
./merge-with-tag.sh 45

# Output shows:
# Version progression: v1.1.0 -> v1.1.1
# Release v1.1.1 created
```

---

## Output Format

Always return results in this Markdown format:

### For PR Creation

```markdown
- pr_number: <number>
- pr_url: <url>
- branch: <branch-name>
- merge_commit: null
- deleted_remote_branch: false
- deleted_local_branch: false
- warnings: [<list>]
- errors: [<list>]
```

### For PR Merge with Release Tag

```markdown
- pr_number: <number>
- pr_url: <url>
- branch: <branch-name>
- merge_commit: <hash>
- deleted_remote_branch: true
- deleted_local_branch: true
- previous_version: <version>
- new_version: <version>
- release_tag: <tag>
- release_url: <url>
- release_date: <ISO date>
- warnings: [<list>]
- errors: [<list>]
```

---

## Part 3: Revert and Rollback Workflows

### Reverting a Merged PR

When a merged PR causes issues and needs to be undone:

**Step 1: Identify the merge commit**

```bash
# Get merge commit from PR
gh pr view <pr-number> --json mergeCommit --jq .mergeCommit.oid

# Or find in git log
git log --oneline -10
```

**Step 2: Create revert commit**

```bash
# Checkout main and ensure it's up to date
git checkout main
git pull origin main

# Revert the merge commit (use -m 1 for the first parent)
git revert -m 1 <merge-commit-hash>

# This opens editor for commit message, or use:
git revert -m 1 <merge-commit-hash> --no-edit
```

**Step 3: Push revert and create PR**

```bash
# Create revert branch
git checkout -b revert/pr-<pr-number>

# Push
git push -u origin revert/pr-<pr-number>

# Create revert PR
cat > .pr-body-temp.md << 'EOF'
## Revert PR #<pr-number>

This reverts the changes from PR #<pr-number> due to:
- [ ] Production issue
- [ ] Breaking change
- [ ] Performance regression
- [ ] Other: ___

### Original PR
- PR: #<pr-number>
- Merge Commit: <hash>

### What was reverted
Brief description of what was undone.

### Next Steps
- [ ] Investigate root cause
- [ ] Fix issue in new branch
- [ ] Create new PR with fix
EOF

gh pr create \
  --title "revert: PR #<pr-number> - <original-title>" \
  --body-file .pr-body-temp.md \
  --base main

rm .pr-body-temp.md
```

### Rollback to Specific Commit

For emergency rollbacks to a known good state:

```bash
# DANGER: This rewrites history - only use in emergencies
# First, identify the good commit
git log --oneline -20

# Create rollback branch from good commit
git checkout -b rollback/<date> <good-commit-hash>

# Push and create emergency PR
git push -u origin rollback/<date>

gh pr create \
  --title "EMERGENCY ROLLBACK to <commit>" \
  --body "Emergency rollback due to critical production issue." \
  --base main \
  --label "priority/critical,status/emergency"
```

### Recovering from Failed Merge

If a merge fails or creates issues:

```bash
# If merge not yet pushed, abort it
git merge --abort

# If merge pushed but not deployed
# Create revert immediately
git revert HEAD --no-edit
git push

# If already deployed and causing issues
# 1. Revert in production
# 2. Investigate locally
# 3. Create fix PR
```

---

## Part 4: Automated Changelog Generation

### Generating Changelog from PRs

```bash
# Get merged PRs since last release
gh pr list \
  --state merged \
  --base main \
  --json number,title,labels,mergedAt,author \
  --jq '.[] | "- \(.title) (#\(.number)) @\(.author.login)"'
```

### Structured Changelog Generation

```bash
# Generate categorized changelog
cat > generate-changelog.sh << 'SCRIPT'
#!/bin/bash

echo "# Changelog"
echo ""
echo "## $(date +%Y-%m-%d)"
echo ""

# Features
echo "### Features"
gh pr list --state merged --base main --label "type/feature" --json number,title \
  --jq '.[] | "- \(.title) (#\(.number))"' 2>/dev/null || echo "No features"
echo ""

# Bug Fixes
echo "### Bug Fixes"
gh pr list --state merged --base main --label "type/bugfix" --json number,title \
  --jq '.[] | "- \(.title) (#\(.number))"' 2>/dev/null || echo "No bug fixes"
echo ""

# Documentation
echo "### Documentation"
gh pr list --state merged --base main --label "type/docs" --json number,title \
  --jq '.[] | "- \(.title) (#\(.number))"' 2>/dev/null || echo "No docs changes"
echo ""

# Other
echo "### Other Changes"
gh pr list --state merged --base main --json number,title,labels \
  --jq '.[] | select(.labels | map(.name) | any(startswith("type/")) | not) | "- \(.title) (#\(.number))"' 2>/dev/null || echo "No other changes"
SCRIPT

chmod +x generate-changelog.sh
./generate-changelog.sh > CHANGELOG_NEW.md
```

### Add Changelog Label to PRs

```bash
# Add auto-changelog label for CI to generate changelog
gh pr edit <pr-number> --add-label "auto-changelog"
```

---

## Part 5: Conflict Resolution Workflow

### Detecting Conflicts Before They Happen

```bash
# Check if branch is behind main
git fetch origin main

# Show commits that main has but branch doesn't
git log HEAD..origin/main --oneline

# Show files that would conflict
git diff --name-only HEAD origin/main
```

### Resolving Merge Conflicts

**Step 1: Update local branch**

```bash
# Fetch latest main
git fetch origin main

# Attempt merge
git merge origin/main
```

**Step 2: Identify conflicting files**

```bash
# List files with conflicts
git diff --name-only --diff-filter=U

# Or use status
git status --short | grep "^UU"
```

**Step 3: Resolve conflicts**

For each conflicting file:

```bash
# Open in editor - look for conflict markers:
# <<<<<<< HEAD
# (your changes)
# =======
# (main's changes)
# >>>>>>> origin/main

# After manual resolution, mark as resolved
git add <resolved-file>
```

**Step 4: Complete merge**

```bash
# Commit the merge
git commit -m "fix: resolve merge conflicts with main"

# Push updated branch
git push

# Remove conflicts label if present
gh pr edit <pr-number> --remove-label "status/conflicts"

# Add ready label
gh pr edit <pr-number> --add-label "status/ready-for-review"
```

### Conflict Resolution Strategies

| Scenario                     | Strategy                                        |
| ---------------------------- | ----------------------------------------------- |
| **Simple text conflicts**    | Manual merge, keep both changes                 |
| **Lock file conflicts**      | Regenerate: `rm pnpm-lock.yaml && pnpm install` |
| **Package.json conflicts**   | Merge manually, then `pnpm install`             |
| **Auto-generated files**     | Regenerate after merging source                 |
| **Large structural changes** | Consider rebasing instead of merging            |

### Rebasing Instead of Merging

For cleaner history:

```bash
# Ensure you're on your feature branch
git checkout <feature-branch>

# Rebase onto main
git rebase origin/main

# If conflicts occur, resolve each one
# Then continue rebase
git add <resolved-file>
git rebase --continue

# Or abort if too complex
git rebase --abort

# Force push (only if branch is yours alone!)
git push --force-with-lease
```

---

## Part 6: Branch Protection Verification

### Check Protection Rules

```bash
# View branch protection rules
gh api repos/{owner}/{repo}/branches/main/protection \
  --jq '{
    requiredReviews: .required_pull_request_reviews.required_approving_review_count,
    dismissStale: .required_pull_request_reviews.dismiss_stale_reviews,
    requireCodeOwners: .required_pull_request_reviews.require_code_owner_reviews,
    requiredChecks: .required_status_checks.contexts,
    enforceAdmins: .enforce_admins.enabled
  }'
```

### Pre-merge Protection Checklist

```bash
# Create comprehensive pre-merge check
cat > .pr-premerge-check.sh << 'SCRIPT'
#!/bin/bash
PR_NUMBER=$1

echo "Pre-merge Protection Check for PR #$PR_NUMBER"
echo "============================================="

# Check CI status
echo -n "CI Status: "
gh pr checks $PR_NUMBER --json name,state --jq '.[] | "\(.name): \(.state)"'

# Check review status
echo -n "Reviews: "
gh pr view $PR_NUMBER --json reviews --jq '.reviews | group_by(.state) | map({state: .[0].state, count: length})'

# Check merge status
echo -n "Merge Status: "
gh pr view $PR_NUMBER --json mergeable,mergeStateStatus --jq '"\(.mergeable) - \(.mergeStateStatus)"'

# Check if ahead/behind
echo -n "Branch Status: "
gh pr view $PR_NUMBER --json commits --jq '"Commits: \(.commits | length)"'

echo ""
echo "Ready to merge: $(gh pr view $PR_NUMBER --json mergeStateStatus --jq '.mergeStateStatus == "CLEAN"')"
SCRIPT

chmod +x .pr-premerge-check.sh
```

---

## Configuration

### Customizable Project Settings

The following values are project-specific and can be changed:

```bash
# Repository owner (change for forks)
OWNER="JordiNodeJS"

# Repository name
REPO="thesimpsonsapi"

# Default assignee
DEFAULT_ASSIGNEE="JordiNodeJS"

# Default base branch
DEFAULT_BASE="main"

# Package manager
PKG_MANAGER="pnpm"
```

To use in commands:

```bash
# Example: Create PR with custom owner
gh pr create \
  --repo "$OWNER/$REPO" \
  --title "feat: new feature" \
  --body-file .pr-body-temp.md \
  --base "$DEFAULT_BASE" \
  --assignee "$DEFAULT_ASSIGNEE"
```

---

## Related Resources

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub CLI PR Commands](https://cli.github.com/manual/gh_pr)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Release Tagging Guide](docs/RELEASE_TAGGING.md)
- [Automated Script](scripts/merge-and-release.sh)
- [Project Prompts](.github/prompts/)
- [Project State](.github/project/PROJECT-STATE.md)
