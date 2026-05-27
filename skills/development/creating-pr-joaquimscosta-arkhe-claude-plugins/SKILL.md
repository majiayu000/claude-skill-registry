---
name: creating-pr
description: Creates GitHub Pull Requests with existing PR detection, branch pushing, and intelligent title/body generation. Use when user requests to create pull request, open PR, update PR, push for review, ready for review, send for review, get this reviewed, make a PR, share code, request review, create draft PR, submit for review, run /create-pr command, or mentions "PR", "pull request", "merge request", "code review", "GitHub PR", or "draft".
model: haiku
---

# ⚠️ CRITICAL CONSTRAINTS

## No Claude Code Footer Policy

**YOU MUST NEVER add Claude Code attribution to pull requests.**

- ❌ **NO** "🤖 Generated with [Claude Code]" in PR titles or descriptions
- ❌ **NO** "Co-Authored-By: Claude <noreply@anthropic.com>" in PR content
- ❌ **NO** Claude Code attribution, footer, or branding of any kind

Pull requests are public code review documents and must remain clean and professional.

---

# GitHub PR Creation Workflow

Execute GitHub Pull Request workflows with automatic repository detection, branch management, and intelligent PR content generation.

## Usage

This skill is invoked when:
- User runs `/create-pr` or `/git:create-pr` command
- User requests to create a pull request
- User asks to open a PR or push changes for review

## How It Works

This skill handles the complete PR workflow:

1. **Repository Detection** - Detect current repository context (root or submodule)
2. **Branch Validation** - Verify not on protected branch, check for uncommitted changes
3. **Branch Pushing** - Ensure branch exists on remote
4. **Existing PR Detection** - Check if PR already exists for current branch
5. **PR Content Generation** - Create title and description from commits
6. **PR Creation** - Create or update PR using GitHub CLI

## Supported Arguments

Parse arguments from user input:

- **No arguments**: Auto-detect repository and create PR to main branch
- **`<scope>`**: Direct PR for specific repository (root, submodule-name)
- **`--draft`**: Create as draft PR
- **`--base <branch>`**: Target branch (default: main)
- **Combinations**: `<scope> --draft`, `root --base staging`, etc.

## Prerequisites

**GitHub CLI Required**: Must have `gh` installed and authenticated

```bash
# Install GitHub CLI (if not installed)
# macOS: brew install gh
# Linux: See https://cli.github.com/

# Authenticate
gh auth login
```

## PR Creation Workflow Steps

### Step 1: Parse Arguments

Extract scope, draft flag, and base branch from user input:

```bash
# Parse arguments
SCOPE=""
DRAFT_FLAG=""
BASE_BRANCH="main"

# Example parsing:
# "root --draft" → SCOPE="root", DRAFT_FLAG="--draft", BASE_BRANCH="main"
# "--base staging" → SCOPE="", DRAFT_FLAG="", BASE_BRANCH="staging"
# "my-service --draft --base develop" → SCOPE="my-service", DRAFT_FLAG="--draft", BASE_BRANCH="develop"
```

### Step 2: Detect Repository Context

Find monorepo root and determine current repository:

```bash
# Find monorepo root (handles submodules)
if SUPERPROJECT=$(git rev-parse --show-superproject-working-tree 2>/dev/null) && [ -n "$SUPERPROJECT" ]; then
    # We're in a submodule
    MONOREPO_ROOT="$SUPERPROJECT"
else
    # We're in root or standalone repo
    MONOREPO_ROOT=$(git rev-parse --show-toplevel)
fi

# Get current working directory
CURRENT_DIR=$(pwd)

# Determine repository context
if [ -n "$SCOPE" ]; then
    # User specified scope
    if [ "$SCOPE" = "root" ]; then
        REPO_PATH="$MONOREPO_ROOT"
    else
        REPO_PATH="$MONOREPO_ROOT/$SCOPE"
    fi
else
    # Auto-detect from current directory
    # If in submodule, use submodule path
    # If in root, use root path
    if [[ "$CURRENT_DIR" == "$MONOREPO_ROOT" ]]; then
        REPO_PATH="$MONOREPO_ROOT"
    else
        # Find which submodule we're in
        REPO_PATH=$(git -C "$CURRENT_DIR" rev-parse --show-toplevel)
    fi
fi

# Validate repository
if [ ! -d "$REPO_PATH/.git" ]; then
    echo "❌ Error: Not a valid git repository: $REPO_PATH" >&2
    exit 1
fi
```

### Step 3: Validate Branch State

Check current branch and uncommitted changes:

```bash
# Change to repository directory
cd "$REPO_PATH"

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Check if on protected branch
if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
    echo "❌ Cannot create PR from protected branch: $CURRENT_BRANCH" >&2
    echo "" >&2
    echo "Please create a feature branch first:" >&2
    echo "  git checkout -b feature/your-feature-name" >&2
    echo "" >&2
    exit 1
fi

# Check for uncommitted changes
UNCOMMITTED=$(git status --porcelain)
if [ -n "$UNCOMMITTED" ]; then
    echo "❌ Error: You have uncommitted changes" >&2
    echo "" >&2
    echo "Please commit or stash your changes before creating a PR:" >&2
    git status --short
    echo "" >&2
    exit 1
fi

# Check if branch has commits ahead of base
COMMITS_AHEAD=$(git rev-list --count "$BASE_BRANCH..HEAD" 2>/dev/null || echo "0")
if [ "$COMMITS_AHEAD" = "0" ]; then
    echo "❌ Error: No commits to create PR from" >&2
    echo "Current branch '$CURRENT_BRANCH' has no commits ahead of '$BASE_BRANCH'" >&2
    exit 1
fi

echo "ℹ️  Branch: $CURRENT_BRANCH ($COMMITS_AHEAD commits ahead of $BASE_BRANCH)"
```

### Step 4: Push Branch to Remote

Ensure branch exists on remote:

```bash
# Check if branch exists on remote
REMOTE_BRANCH=$(git ls-remote --heads origin "$CURRENT_BRANCH" 2>/dev/null)

if [ -z "$REMOTE_BRANCH" ]; then
    echo "ℹ️  Branch not on remote, pushing..."
    git push -u origin "$CURRENT_BRANCH" || {
        echo "❌ Failed to push branch to remote" >&2
        exit 1
    }
    echo "✅ Branch pushed to origin/$CURRENT_BRANCH"
else
    # Check if local is behind remote
    LOCAL_HASH=$(git rev-parse HEAD)
    REMOTE_HASH=$(git rev-parse "origin/$CURRENT_BRANCH" 2>/dev/null || echo "")

    if [ "$LOCAL_HASH" != "$REMOTE_HASH" ]; then
        echo "ℹ️  Local branch differs from remote, pushing..."
        git push origin "$CURRENT_BRANCH" || {
            echo "❌ Failed to push branch to remote" >&2
            exit 1
        }
        echo "✅ Branch updated on remote"
    else
        echo "ℹ️  Branch already up to date on remote"
    fi
fi
```

### Step 5: Check for Existing PR

Detect if PR already exists for this branch:

```bash
# Check for existing PR using GitHub CLI
EXISTING_PR=$(gh pr view "$CURRENT_BRANCH" --json number,title,url 2>/dev/null || echo "")

if [ -n "$EXISTING_PR" ]; then
    # PR exists - extract info
    PR_NUMBER=$(echo "$EXISTING_PR" | jq -r '.number')
    PR_TITLE=$(echo "$EXISTING_PR" | jq -r '.title')
    PR_URL=$(echo "$EXISTING_PR" | jq -r '.url')

    echo ""
    echo "ℹ️  Existing PR found:"
    echo "  #$PR_NUMBER: $PR_TITLE"
    echo "  $PR_URL"
    echo ""

    # Use AskUserQuestion to ask user what to do
    # Options:
    # 1. Update PR (regenerate title/body and update)
    # 2. View PR in browser (open URL)
    # 3. Cancel (do nothing)

    # If user chooses "Update PR":
    # - Generate new title and body (Steps 6-7)
    # - Update PR using: gh pr edit "$PR_NUMBER" --title "..." --body "..."
    # - Show success message

    # If user chooses "View PR":
    # - Open PR URL in browser: gh pr view --web

    # If user chooses "Cancel":
    # - Exit gracefully
fi
```

### Step 6: Generate PR Title

Analyze commits to create conventional PR title:

```bash
# Get all commits from base branch to current branch
COMMITS=$(git log "$BASE_BRANCH..HEAD" --oneline)
COMMIT_COUNT=$(echo "$COMMITS" | wc -l | tr -d ' ')

echo "ℹ️  Analyzing $COMMIT_COUNT commits..."

# Get the first commit message (most recent)
LATEST_COMMIT=$(git log -1 --pretty=%B)

# Detect commit type from latest commit or analyze all commits
# Try to extract type from conventional commit format
if echo "$LATEST_COMMIT" | grep -qE '^(feat|fix|docs|refactor|test|chore|perf|ci|build):'; then
    # Extract type and description from conventional commit
    COMMIT_TYPE=$(echo "$LATEST_COMMIT" | grep -oE '^[a-z]+' | head -1)
    COMMIT_DESC=$(echo "$LATEST_COMMIT" | sed -E 's/^[a-z]+(\([^)]+\))?:\s*//')
else
    # Analyze changes to determine type
    ALL_COMMITS=$(git log "$BASE_BRANCH..HEAD" --pretty=%B)

    if echo "$ALL_COMMITS" | grep -qi "fix\|bug"; then
        COMMIT_TYPE="fix"
    elif echo "$ALL_COMMITS" | grep -qi "feat\|feature\|add"; then
        COMMIT_TYPE="feat"
    elif echo "$ALL_COMMITS" | grep -qi "docs\|documentation"; then
        COMMIT_TYPE="docs"
    elif echo "$ALL_COMMITS" | grep -qi "refactor"; then
        COMMIT_TYPE="refactor"
    elif echo "$ALL_COMMITS" | grep -qi "test"; then
        COMMIT_TYPE="test"
    else
        COMMIT_TYPE="feat"
    fi

    # Generate description from branch name or commit
    COMMIT_DESC=$(echo "$LATEST_COMMIT" | head -1 | sed 's/^\s*//')
fi

# Generate PR title (capitalize first letter)
PR_TITLE="$COMMIT_TYPE: $COMMIT_DESC"

echo "ℹ️  Generated PR title: $PR_TITLE"
```

### Step 7: Generate PR Body

Create PR description with summary and test plan:

```bash
# Generate PR body with summary from commits
PR_BODY="## Summary

"

# Add commit summaries
if [ "$COMMIT_COUNT" -eq 1 ]; then
    # Single commit - use full message
    PR_BODY+="$LATEST_COMMIT

"
else
    # Multiple commits - list them
    PR_BODY+="This PR includes $COMMIT_COUNT commits:

"
    while IFS= read -r commit; do
        PR_BODY+="- $commit
"
    done <<< "$COMMITS"
    PR_BODY+="
"
fi

# Add test plan section
PR_BODY+="## Test Plan

- [ ] Code builds successfully
- [ ] Tests pass
- [ ] Manual testing completed
- [ ] Documentation updated (if needed)

## Changes

"

# List changed files
CHANGED_FILES=$(git diff --name-only "$BASE_BRANCH..HEAD")
while IFS= read -r file; do
    PR_BODY+="- \`$file\`
"
done <<< "$CHANGED_FILES"

echo ""
echo "Generated PR description:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$PR_BODY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
```

### Step 8: Create PR

Use GitHub CLI to create the PR:

```bash
# IMPORTANT: No Claude Code attribution in PR content

# Build gh pr create command
GH_CMD="gh pr create --title \"$PR_TITLE\" --body \"$PR_BODY\" --base \"$BASE_BRANCH\""

# Add draft flag if specified
if [ "$DRAFT_FLAG" = "--draft" ]; then
    GH_CMD+=" --draft"
fi

# Execute PR creation
eval "$GH_CMD" || {
    echo "❌ Failed to create PR" >&2
    exit 1
}

# Get PR URL
PR_URL=$(gh pr view --json url -q '.url')

echo ""
echo "✅ Pull Request created successfully!"
echo ""
echo "PR URL: $PR_URL"
echo ""
echo "Next steps:"
echo "  - Review PR in browser: gh pr view --web"
echo "  - Check CI status: gh pr checks"
echo "  - Request reviews: gh pr ready (if draft)"
echo ""
```

### Alternative: Update Existing PR

If updating an existing PR (user chose "Update" in Step 5):

```bash
# Update PR title and body
gh pr edit "$PR_NUMBER" --title "$PR_TITLE" --body "$PR_BODY" || {
    echo "❌ Failed to update PR" >&2
    exit 1
}

echo "✅ Pull Request #$PR_NUMBER updated successfully!"
echo "PR URL: $PR_URL"
```

## PR Title Generation Rules

The skill generates PR titles following conventional commit format:

| Detected Pattern | Type | Example Title |
|-----------------|------|---------------|
| "feat:" in commits | `feat` | feat: add user authentication |
| "fix:" in commits | `fix` | fix: resolve login timeout issue |
| "docs:" in commits | `docs` | docs: update API documentation |
| "refactor:" in commits | `refactor` | refactor: optimize database queries |
| "test:" in commits | `test` | test: add integration tests |
| Mentions "bug", "fix" | `fix` | fix: correct calculation error |
| Mentions "feature", "add" | `feat` | feat: implement new feature |
| Default | `feat` | feat: [description from commits] |

## Important Notes

1. **GitHub CLI Required**: Must have `gh` installed and authenticated
   ```bash
   gh auth login
   ```

2. **Branch Protection**: Cannot create PR from main/master branch

3. **Existing PRs**: Automatically detects and offers to update existing PRs

4. **Commit-Based Content**: PR title and body generated from commit messages

5. **Works Anywhere**: Executes from any directory, resolves paths absolutely

6. **Submodule Support**: Can create PRs for both root repository and submodules

7. **Clean PR Content**: No Claude Code attribution in PR titles or descriptions

## GitHub CLI Commands Used

This skill uses the following `gh` commands:

```bash
# Check for existing PR
gh pr view <branch> --json number,title,url

# Create new PR
gh pr create --title "..." --body "..." --base <branch> [--draft]

# Update existing PR
gh pr edit <number> --title "..." --body "..."

# View PR in browser
gh pr view --web

# Check PR status
gh pr checks
```

## Supporting Documentation

For detailed information, see:

- **[WORKFLOW.md](WORKFLOW.md)** - Step-by-step PR creation process including repository detection, branch management, and GitHub CLI integration
- **[EXAMPLES.md](EXAMPLES.md)** - Real-world PR scenarios covering features, bug fixes, drafts, and submodule PRs
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions for GitHub CLI errors, authentication, and branch conflicts
