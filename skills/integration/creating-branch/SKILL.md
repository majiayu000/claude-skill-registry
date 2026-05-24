---
name: creating-branch
description: Creates feature branches with optimized short naming, auto-incrementing, and commit type detection (feat/fix/refactor). Supports manual descriptions and auto-generation from uncommitted git changes. Use when user requests to create branch, start new branch, make branch, checkout new branch, switch branch, new task, start working on, begin work on feature, begin feature, create feature branch, run /create-branch command, or mentions "branch", "feature", "new feature", "feat", "fix", or "checkout".
---

# Git Branch Creation Workflow

Execute feature branch creation with intelligent naming, automatic type detection, and sequential numbering.

## Usage

This skill is invoked when:
- User runs `/create-branch` or `/git:create-branch` command
- User requests to create a new feature branch
- User asks to start a new branch for a task

## Two Operation Modes

### Mode 1: With Description (Manual)

The command takes a description and automatically detects the commit type.

**Format**: `/create-branch <description>`

**Examples**:
```bash
/create-branch add user authentication
→ Creates: feat/001-user-authentication

/create-branch fix login bug
→ Creates: fix/002-login-bug

/create-branch refactor auth service
→ Creates: refactor/003-auth-service

/create-branch remove deprecated code
→ Creates: chore/004-remove-deprecated

/create-branch document api endpoints
→ Creates: docs/005-document-api
```

### Mode 2: Auto-Generate from Changes (No Arguments)

When no arguments provided, analyze uncommitted changes to generate branch name automatically.

**Format**: `/create-branch` (no arguments)

**Process**:
1. Check for uncommitted changes (both staged and unstaged)
2. If no changes exist, display error and require description
3. If changes exist, analyze to generate description
4. Create branch with auto-generated name

**Examples**:
```bash
# After modifying authentication files
/create-branch
→ Auto-detected from changes: feat/006-authentication-system
→ (based on: login.py, auth_service.ts, user_model.py)

# After fixing payment bug
/create-branch
→ Auto-detected from changes: fix/007-payment-processing
→ (based on: payment.js, checkout.py)
```

## Commit Type Detection

The workflow automatically detects commit types from keywords in the description:

| Type | Keywords |
|------|----------|
| **feat** | add, create, implement, new, update, improve |
| **fix** | fix, bug, resolve, correct, repair |
| **refactor** | refactor, rename, reorganize |
| **chore** | remove, delete, clean, cleanup |
| **docs** | docs, document, documentation |

If no keyword is detected, defaults to `feat`.

## Branch Naming Format

**Pattern**: `{type}/{number}-{keyword1}-{keyword2}`

**Components**:
- **type**: Auto-detected commit type (feat, fix, refactor, chore, docs)
- **number**: Auto-incremented 3-digit number (001, 002, 003...)
- **keywords**: First 2-3 meaningful words from description (lowercase, hyphenated)

**Examples**:
- Input: "add user authentication system"
- Output: `feat/001-user-authentication`

- Input: "fix null pointer in login"
- Output: `fix/002-null-pointer`

## Branch Creation Workflow Steps

### Step 1: Determine Operation Mode

Check if user provided a description:

```bash
# If user provided description
if [ -n "$DESCRIPTION" ]; then
    MODE="manual"
    # Proceed to Step 3 (type detection)
else
    MODE="auto-generate"
    # Proceed to Step 2 (analyze changes)
fi
```

### Step 2: Auto-Generate Description from Changes (Mode 2 Only)

If no description provided, analyze uncommitted changes:

```bash
# Check for uncommitted changes
UNSTAGED=$(git diff --name-status)
STAGED=$(git diff --cached --name-status)
UNTRACKED=$(git ls-files --others --exclude-standard)

# Combine all changes
ALL_CHANGES=$(echo -e "$UNSTAGED\n$STAGED\n$UNTRACKED" | grep -v '^$')

if [ -z "$ALL_CHANGES" ]; then
    # No changes detected
    echo "❌ Error: No uncommitted changes detected." >&2
    echo "" >&2
    echo "To create a branch, either:" >&2
    echo "1. Make some changes first, then run /create-branch" >&2
    echo "2. Provide a description: /create-branch <description>" >&2
    echo "" >&2
    echo "Examples:" >&2
    echo "  /create-branch add user authentication" >&2
    echo "  /create-branch fix payment bug" >&2
    echo "" >&2
    exit 1
fi

# Analyze changes to generate description
# You should intelligently analyze the file paths and change types
# to determine the purpose and commit type

# Example analysis logic:
# - If mostly new files (A status): feat
# - If modifying error handling files: fix
# - If in docs/ or README: docs
# - Extract common theme from file paths (e.g., "auth", "payment", "api")

# For demonstration, here's a simple template:
# You should replace this with intelligent analysis based on actual files

# Extract first few changed files for display
SAMPLE_FILES=$(echo "$ALL_CHANGES" | head -5 | awk '{print $NF}' | tr '\n' ', ' | sed 's/,$//')

# Generate description based on analysis
# This should be intelligent - for now using placeholder
DESCRIPTION="add feature based on changes"  # Replace with actual analysis
echo "ℹ️  Auto-detected description: $DESCRIPTION"
echo "ℹ️  Based on changes in: $SAMPLE_FILES"
```

### Step 3: Extract Commit Type from Description

Detect commit type from keywords:

```bash
# Convert description to lowercase for matching
DESC_LOWER=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]')

# Detect type from first word or keywords
if echo "$DESC_LOWER" | grep -qE '^(add|create|implement|new|update|improve)'; then
    COMMIT_TYPE="feat"
elif echo "$DESC_LOWER" | grep -qE '^(fix|bug|resolve|correct|repair)'; then
    COMMIT_TYPE="fix"
elif echo "$DESC_LOWER" | grep -qE '^(refactor|rename|reorganize)'; then
    COMMIT_TYPE="refactor"
elif echo "$DESC_LOWER" | grep -qE '^(remove|delete|clean)'; then
    COMMIT_TYPE="chore"
elif echo "$DESC_LOWER" | grep -qE '^(docs?|document)'; then
    COMMIT_TYPE="docs"
elif echo "$DESC_LOWER" | grep -qE '^(test)'; then
    COMMIT_TYPE="test"
elif echo "$DESC_LOWER" | grep -qE '^(perf|performance|optimize)'; then
    COMMIT_TYPE="perf"
elif echo "$DESC_LOWER" | grep -qE '^(build|ci)'; then
    COMMIT_TYPE="build"
else
    # Default to feat
    COMMIT_TYPE="feat"
fi

echo "ℹ️  Detected type: $COMMIT_TYPE"
```

### Step 4: Extract Keywords from Description

Remove type keyword and extract meaningful words:

```bash
# Remove type keywords from description
CLEANED_DESC=$(echo "$DESC_LOWER" | sed -E 's/^(add|create|implement|new|update|improve|fix|bug|resolve|correct|repair|refactor|rename|reorganize|remove|delete|clean|docs?|document|test|perf|performance|optimize|build|ci)\s*//')

# Remove common filler words
FILTERED=$(echo "$CLEANED_DESC" | sed -E 's/\b(the|a|an|for|to|in|on|at|with|from|of|and|or)\b//g')

# Extract first 2-3 meaningful words
KEYWORDS=$(echo "$FILTERED" | tr -s ' ' | awk '{for(i=1; i<=3 && i<=NF; i++) printf "%s%s", $i, (i<3 && i<NF ? "-" : "")}')

# Sanitize: lowercase, replace spaces with hyphens, remove special chars
BRANCH_SUFFIX=$(echo "$KEYWORDS" | tr ' ' '-' | tr -cd '[:alnum:]-' | tr '[:upper:]' '[:lower:]')

echo "ℹ️  Keywords: $BRANCH_SUFFIX"
```

### Step 5: Find Next Sequential Number

Scan existing branches to find next available number:

```bash
# Get all branches matching the commit type pattern
EXISTING_BRANCHES=$(git branch --list "$COMMIT_TYPE/*" | sed 's/^[* ]*//')

# Extract numbers from branch names
NUMBERS=$(echo "$EXISTING_BRANCHES" | grep -oE "$COMMIT_TYPE/[0-9]+" | grep -oE '[0-9]+' | sort -n)

# Find highest number
if [ -z "$NUMBERS" ]; then
    # No existing branches of this type
    NEXT_NUMBER=1
else
    HIGHEST=$(echo "$NUMBERS" | tail -1)
    NEXT_NUMBER=$((HIGHEST + 1))
fi

# Format as 3-digit number
BRANCH_NUMBER=$(printf "%03d" "$NEXT_NUMBER")

echo "ℹ️  Next number: $BRANCH_NUMBER"
```

### Step 6: Generate Branch Name

Combine type, number, and keywords:

```bash
# Build branch name
BRANCH_NAME="$COMMIT_TYPE/$BRANCH_NUMBER-$BRANCH_SUFFIX"

echo ""
echo "Branch name: $BRANCH_NAME"
echo ""
```

### Step 7: Create Branch

Create and checkout the new branch:

```bash
# Create and checkout branch
git checkout -b "$BRANCH_NAME" || {
    echo "❌ Failed to create branch" >&2
    exit 1
}

echo "✅ Created and checked out branch: $BRANCH_NAME"
```

### Step 8: Create Feature Directory (Optional)

If spec-kit is installed (`.specify/` directory exists), create feature directory:

```bash
# Check if .specify/ directory exists (spec-kit indicator)
REPO_ROOT=$(git rev-parse --show-toplevel)

if [ -d "$REPO_ROOT/.specify" ]; then
    # spec-kit is installed - create feature directory
    FEATURE_DIR="$REPO_ROOT/.specify/features/$BRANCH_NAME"
    mkdir -p "$FEATURE_DIR"

    echo "ℹ️  Created feature directory: .specify/features/$BRANCH_NAME"
    echo ""
    echo "You can now add:"
    echo "  - spec.md (feature specification)"
    echo "  - plan.md (implementation plan)"
    echo "  - notes.md (development notes)"
else
    echo "ℹ️  Skipping feature directory (spec-kit not installed)"
fi
```

### Step 9: Display Success Summary

Show final summary:

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Branch created successfully!"
echo ""
echo "Branch: $BRANCH_NAME"
echo "Type: $COMMIT_TYPE"

if [ "$MODE" = "auto-generate" ]; then
    echo "Auto-detected from: $SAMPLE_FILES"
fi

echo ""
echo "Next steps:"
echo "  - Make your changes"
echo "  - Commit with: /commit"
echo "  - Create PR with: /create-pr"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
```

## Keyword Filtering

Common filler words are automatically removed:

| Filtered Words |
|----------------|
| the, a, an |
| for, to, in, on, at |
| with, from, of |
| and, or, but |
| is, are, was, were |
| this, that, these, those |

## Branch Number Sequencing Examples

| Existing Branches | Type | Next Number |
|-------------------|------|-------------|
| None | `feat` | `001` |
| feat/001-auth | `feat` | `002` |
| feat/001-auth, feat/002-api | `feat` | `003` |
| fix/001-bug | `fix` | `001` (different type) |
| feat/005-feature | `feat` | `006` (continues from highest) |

## Important Notes

1. **Sequential Numbering**: Automatically finds next available number by scanning existing branches of the same type

2. **Keyword Extraction**: Filters out common words and keeps only meaningful terms

3. **Short Names**: Uses first 2-3 meaningful words only (avoids long branch names)

4. **Lowercase Convention**: All branch names are lowercase with hyphens

5. **Conventional Commits**: Aligns with conventional commit types for consistency

6. **No Duplicates**: Increments number automatically

7. **Works Anywhere**: Executes from any directory in the project

8. **Monorepo Support**: Works in both root repository and submodules

9. **Spec-Kit Integration**: Optionally creates feature directories when spec-kit is detected

## Supporting Documentation

For detailed information, see:

- **[WORKFLOW.md](WORKFLOW.md)** - Step-by-step branch creation process with detailed explanations
- **[EXAMPLES.md](EXAMPLES.md)** - Real-world examples covering all branch types and scenarios
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
