---
name: creating-commit
description: Creates context-aware git commits with smart pre-commit checks, submodule support, and conventional commit message generation. Use when user requests to commit changes, stage and commit, check in code, save work, save changes, push my code, finalize changes, add to git, create commits, run /commit command, or mentions "git commit", "commit message", "conventional commits", "stage files", "git add", or needs help with commits.
---

# ⚠️ CRITICAL CONSTRAINTS

## No Claude Code Footer Policy

**YOU MUST NEVER add Claude Code attribution to git commits.**

- ❌ **NO** "🤖 Generated with [Claude Code]" in commit messages
- ❌ **NO** "Co-Authored-By: Claude <noreply@anthropic.com>" in commit messages
- ❌ **NO** Claude Code attribution, footer, or branding of any kind

Git commits are permanent project history and must remain clean and professional.

---

# Git Commit Workflow

Execute intelligent git commit workflows with automatic repository detection, smart pre-commit checks, and conventional commit message generation.

## Usage

This skill is invoked when:
- User runs `/commit` command
- User requests to commit changes
- User asks to create a git commit

## How It Works

This skill handles the complete commit workflow:

1. **Repository Detection** - Automatically detects root repository and submodules
2. **Change Analysis** - Identifies modified files and determines scope
3. **Pre-commit Checks** - Runs appropriate checks based on file types
4. **Commit Message Generation** - Creates conventional commit messages with emojis
5. **Submodule Handling** - Prompts to update submodule references in root repository

## Supported Arguments

Parse arguments from user input:

- **No arguments**: Interactive mode (auto-detect changes)
- **`<scope>`**: Direct commit to specific repository (root, submodule-name)
- **`--no-verify`**: Skip all pre-commit checks
- **`--full-verify`**: Run full builds (backend + frontend)
- **`<scope> --no-verify`**: Combine scope with flags

## Commit Workflow Steps

### Step 1: Parse Arguments

Extract scope and flags from user input:

```bash
# Parse arguments
SCOPE=""
FLAG=""

# Example parsing logic (adapt to user input):
# "root --no-verify" → SCOPE="root", FLAG="--no-verify"
# "plan" → SCOPE="plan", FLAG=""
# "--full-verify" → SCOPE="", FLAG="--full-verify"
```

### Step 2: Detect Repositories with Changes

Find monorepo root and detect all repositories with uncommitted changes:

```bash
# Find monorepo root (works from submodules too)
if SUPERPROJECT=$(git rev-parse --show-superproject-working-tree 2>/dev/null) && [ -n "$SUPERPROJECT" ]; then
    # We're in a submodule
    MONOREPO_ROOT="$SUPERPROJECT"
else
    # We're in root or standalone repo
    MONOREPO_ROOT=$(git rev-parse --show-toplevel)
fi

# Detect repositories with changes
REPOS_WITH_CHANGES=()

# Check root repository
if git -C "$MONOREPO_ROOT" status --porcelain | grep -q .; then
    REPOS_WITH_CHANGES+=("root")
fi

# Check for submodules and their changes
git -C "$MONOREPO_ROOT" submodule foreach --quiet 'echo $name' | while read -r submodule; do
    SUBMODULE_PATH="$MONOREPO_ROOT/$submodule"
    if git -C "$SUBMODULE_PATH" status --porcelain | grep -q .; then
        REPOS_WITH_CHANGES+=("$submodule")
    fi
done
```

### Step 3: Select Target Repository

If no scope specified, select repository interactively or automatically:

```bash
# If only one repository has changes, auto-select it
if [ ${#REPOS_WITH_CHANGES[@]} -eq 1 ]; then
    SCOPE="${REPOS_WITH_CHANGES[0]}"
    echo "ℹ️  Auto-selected: $SCOPE (only repository with changes)"
elif [ ${#REPOS_WITH_CHANGES[@]} -gt 1 ]; then
    # Multiple repositories - ask user to select
    echo "Found changes in:"
    for i in "${!REPOS_WITH_CHANGES[@]}"; do
        REPO="${REPOS_WITH_CHANGES[$i]}"
        REPO_PATH=$([ "$REPO" = "root" ] && echo "$MONOREPO_ROOT" || echo "$MONOREPO_ROOT/$REPO")
        CHANGE_COUNT=$(git -C "$REPO_PATH" status --porcelain | wc -l | tr -d ' ')
        echo "$((i+1)). $REPO ($CHANGE_COUNT files modified)"
    done

    # Use AskUserQuestion tool to let user select repository
    # Set SCOPE to selected repository name
fi
```

### Step 4: Resolve Repository Path

Convert scope to absolute path:

```bash
# Resolve scope to repository path
if [ "$SCOPE" = "root" ]; then
    REPO_PATH="$MONOREPO_ROOT"
else
    # Submodule or custom scope
    REPO_PATH="$MONOREPO_ROOT/$SCOPE"
fi

# Validate repository exists
if [ ! -d "$REPO_PATH/.git" ]; then
    echo "❌ Error: Not a valid git repository: $REPO_PATH" >&2
    exit 1
fi
```

### Step 5: Check Branch Protection

Validate not on protected branch (main branch for root only):

```bash
# Get current branch
CURRENT_BRANCH=$(git -C "$REPO_PATH" rev-parse --abbrev-ref HEAD)

# Check branch protection (only enforce for root repository)
if [ "$CURRENT_BRANCH" = "main" ] && [ "$SCOPE" = "root" ]; then
    echo "❌ Cannot commit to protected branch: main" >&2
    echo "" >&2
    echo "The main branch requires pull requests." >&2
    echo "Please create a feature branch first:" >&2
    echo "" >&2
    echo "  git checkout -b feature/your-feature-name" >&2
    echo "" >&2
    exit 1
fi
```

### Step 6: Stage Files

Stage all unstaged changes or use already-staged files:

```bash
# Check if there are already staged files
STAGED_FILES=$(git -C "$REPO_PATH" diff --cached --name-only)

if [ -z "$STAGED_FILES" ]; then
    # No staged files - stage all changes
    echo "Staging all changes..."
    git -C "$REPO_PATH" add -A

    # Verify staging worked
    STAGED_FILES=$(git -C "$REPO_PATH" diff --cached --name-only)
    if [ -z "$STAGED_FILES" ]; then
        echo "❌ No changes to commit" >&2
        exit 1
    fi
else
    echo "ℹ️  Using already staged files"
fi

# Show what will be committed
git -C "$REPO_PATH" status --short
```

### Step 7: Run Pre-commit Checks

Execute pre-commit checks based on changed file types and flags:

```bash
# Skip checks if --no-verify flag is set
if [ "$FLAG" = "--no-verify" ]; then
    echo "⚠️  Skipping pre-commit checks (--no-verify flag)"
elif [ "$SCOPE" = "plan" ] || [[ "$SCOPE" == *"doc"* ]]; then
    echo "ℹ️  Skipping checks for documentation repository"
elif [ "$FLAG" = "--full-verify" ]; then
    # Full build verification
    echo "Running full build verification..."

    if [ -d "$MONOREPO_ROOT/backend" ]; then
        echo "Building backend..."
        (cd "$MONOREPO_ROOT/backend" && ./gradlew build test) || {
            echo "❌ Backend build failed" >&2
            exit 1
        }
    fi

    if [ -d "$MONOREPO_ROOT/frontend" ]; then
        echo "Building frontend..."
        (cd "$MONOREPO_ROOT/frontend" && npm run build) || {
            echo "❌ Frontend build failed" >&2
            exit 1
        }
    fi

    echo "✅ Full build verification passed"
else
    # Smart detection - run checks based on file types
    CHANGED_FILES=$(git -C "$REPO_PATH" diff --cached --name-only)

    # Detect Kotlin files
    if echo "$CHANGED_FILES" | grep -q '\.kt$'; then
        echo "Running backend checks (Kotlin files detected)..."
        if [ -f "$MONOREPO_ROOT/backend/gradlew" ]; then
            (cd "$MONOREPO_ROOT/backend" && ./gradlew detekt) || {
                echo "❌ Kotlin checks failed" >&2
                exit 1
            }
        fi
    fi

    # Detect TypeScript/JavaScript files
    if echo "$CHANGED_FILES" | grep -qE '\.(ts|tsx|js|jsx)$'; then
        echo "Running frontend checks (TypeScript files detected)..."
        if [ -f "$MONOREPO_ROOT/frontend/package.json" ]; then
            (cd "$MONOREPO_ROOT/frontend" && npx tsc --noEmit) || {
                echo "❌ TypeScript checks failed" >&2
                exit 1
            }
        fi
    fi

    # Detect Python files
    if echo "$CHANGED_FILES" | grep -q '\.py$'; then
        echo "Running Python checks..."
        # Add Python linting if configured (e.g., pylint, flake8)
    fi

    # Detect Rust files
    if echo "$CHANGED_FILES" | grep -q '\.rs$'; then
        echo "Running Rust checks..."
        if [ -f "$REPO_PATH/Cargo.toml" ]; then
            (cd "$REPO_PATH" && cargo check) || {
                echo "❌ Rust checks failed" >&2
                exit 1
            }
        fi
    fi

    echo "✅ Pre-commit checks passed"
fi
```

### Step 8: Generate Commit Message

Analyze changes and create conventional commit message:

```bash
# Detect commit type from changed files
DIFF_STAT=$(git -C "$REPO_PATH" diff --cached --stat)

# Simple heuristic based on file patterns
if echo "$DIFF_STAT" | grep -q "test\|spec"; then
    COMMIT_TYPE="test"
    EMOJI="✅"
elif echo "$DIFF_STAT" | grep -q "\.md\|README\|docs/"; then
    COMMIT_TYPE="docs"
    EMOJI="📝"
elif echo "$DIFF_STAT" | grep -qE "build\.gradle|package\.json|pom\.xml|Cargo\.toml"; then
    COMMIT_TYPE="build"
    EMOJI="🏗️"
elif echo "$DIFF_STAT" | grep -qE "\.github|\.gitlab|Jenkinsfile|\.circleci"; then
    COMMIT_TYPE="ci"
    EMOJI="👷"
elif echo "$DIFF_STAT" | grep -q "refactor"; then
    COMMIT_TYPE="refactor"
    EMOJI="♻️"
elif echo "$DIFF_STAT" | grep -q "fix\|bug"; then
    COMMIT_TYPE="fix"
    EMOJI="🐛"
else
    # Default to feat for most changes
    COMMIT_TYPE="feat"
    EMOJI="✨"
fi

# Analyze the actual changes to generate a meaningful description
CHANGED_FILES_LIST=$(git -C "$REPO_PATH" diff --cached --name-only)
ADDITIONS=$(git -C "$REPO_PATH" diff --cached --numstat | awk '{sum+=$1} END {print sum}')
DELETIONS=$(git -C "$REPO_PATH" diff --cached --numstat | awk '{sum+=$2} END {print sum}')

# Generate commit message based on changes
# You should analyze the diff and create a concise, meaningful message
# For now, this is a template - Claude should intelligently describe the changes
COMMIT_SUBJECT="$COMMIT_TYPE: [brief description of changes]"
COMMIT_BODY="[optional detailed explanation]

Changes:
$CHANGED_FILES_LIST

$ADDITIONS additions, $DELETIONS deletions"

# Present commit message to user for approval
echo ""
echo "Suggested commit message:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$EMOJI $COMMIT_SUBJECT"
echo ""
echo "$COMMIT_BODY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Use AskUserQuestion tool to confirm or let user edit the message
```

### Step 9: Create Commit

Execute git commit with the approved message:

```bash
# IMPORTANT: No Claude Code footer in commit messages
# Create commit with clean message only

git -C "$REPO_PATH" commit -m "$COMMIT_SUBJECT" -m "$COMMIT_BODY" || {
    echo "❌ Commit failed" >&2
    exit 1
}

# Get commit hash
COMMIT_HASH=$(git -C "$REPO_PATH" rev-parse --short HEAD)

echo "✅ Commit created: $COMMIT_HASH"
echo ""
git -C "$REPO_PATH" log -1 --oneline
```

### Step 10: Handle Submodule References (if applicable)

If committed to a submodule, prompt to update root repository:

```bash
# If we committed to a submodule, check if root needs update
if [ "$SCOPE" != "root" ]; then
    # Check if submodule reference changed in root
    SUBMODULE_REF_CHANGED=$(git -C "$MONOREPO_ROOT" status --porcelain | grep "^ M $SCOPE$")

    if [ -n "$SUBMODULE_REF_CHANGED" ]; then
        echo ""
        echo "ℹ️  Submodule reference changed in root repository"
        echo ""

        # Use AskUserQuestion to ask if they want to commit the submodule reference
        # If yes:
        # git -C "$MONOREPO_ROOT" add "$SCOPE"
        # git -C "$MONOREPO_ROOT" commit -m "build: update $SCOPE submodule reference"
    fi
fi
```

## Commit Type Detection

The skill automatically detects commit types based on file patterns:

| Pattern | Type | Emoji |
|---------|------|-------|
| test/spec files | `test` | ✅ |
| .md/README/docs/ | `docs` | 📝 |
| build files (package.json, Cargo.toml, etc.) | `build` | 🏗️ |
| CI/CD files (.github, Jenkinsfile) | `ci` | 👷 |
| Files with "refactor" | `refactor` | ♻️ |
| Files with "fix" or "bug" | `fix` | 🐛 |
| Default | `feat` | ✨ |

## Pre-commit Check Matrix

| File Type | Check Command | When |
|-----------|--------------|------|
| `*.kt` | `./gradlew detekt` | Unless --no-verify |
| `*.ts`, `*.tsx` | `npx tsc --noEmit` | Unless --no-verify |
| `*.py` | Configurable linting | Unless --no-verify |
| `*.rs` | `cargo check` | Unless --no-verify |
| Documentation (`*.md`) | Skip checks | Always |
| Full verify flag | `./gradlew build test && npm run build` | When --full-verify |

## Important Notes

- **Multi-repo/Submodule Support**: Automatically detects and handles monorepo structures
- **Branch Protection**: Prevents commits to main branch in root repository
- **Smart Checks**: Only runs checks relevant to changed file types
- **No External Dependencies**: All logic uses git commands and Bash tool
- **Clean Commit History**: No Claude Code attribution in commit messages

## Supporting Documentation

For detailed information, see:

- **[WORKFLOW.md](WORKFLOW.md)** - Step-by-step commit process including repository detection, pre-commit checks, and submodule handling
- **[EXAMPLES.md](EXAMPLES.md)** - Real-world commit scenarios covering features, bug fixes, submodules, and verification modes
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions for pre-commit failures and submodule conflicts
