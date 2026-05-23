---
name: multi-repository-orchestrator
description: Coordinate development workflows across multiple Git repositories with synchronized branching, batch commits, cross-repo operations, and monorepo-like workflows for microservices and multi-package projects.
license: MIT
tags: [multi-repo, git, orchestration, microservices, monorepo, coordination]
---

# Multi-Repository Orchestrator

Manage development workflows seamlessly across multiple Git repositories.

## Overview

Many modern projects span multiple repositories:
- Microservices architectures
- Frontend + Backend + Shared libraries
- Multi-package monorepos split across repos
- Infrastructure + Application code
- Documentation + Code repositories

This skill provides tools and patterns to orchestrate changes, commits, and workflows across multiple repositories as if they were one.

## When to Use

Use this skill when:
- Working with microservices split across repos
- Maintaining frontend/backend in separate repositories
- Managing shared libraries used by multiple repos
- Coordinating infrastructure and application code
- Synchronizing changes across dependent projects
- Running tests across multiple repositories
- Deploying multi-repo applications
- Maintaining consistency across project family

## Repository Discovery

### Auto-Discovery Pattern

```bash
#!/bin/bash
# discover-repos.sh - Find all related repositories

BASE_DIR="${1:-.}"
WORKSPACE_FILE=".workspace"

# Find all git repositories
find "$BASE_DIR" -name ".git" -type d | while read git_dir; do
    REPO_DIR=$(dirname "$git_dir")
    REPO_NAME=$(basename "$REPO_DIR")

    # Get remote URL
    cd "$REPO_DIR"
    REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "none")

    echo "$REPO_NAME|$REPO_DIR|$REMOTE_URL"
done | tee "$WORKSPACE_FILE"

echo ""
echo "Discovered $(wc -l < $WORKSPACE_FILE) repositories"
echo "Workspace file: $WORKSPACE_FILE"
```

### Manual Workspace Configuration

```yaml
# workspace.yaml - Define multi-repo workspace

workspace:
  name: my-microservices
  base_dir: ~/projects

repositories:
  - name: api-gateway
    path: ./api-gateway
    url: https://github.com/org/api-gateway
    category: backend

  - name: user-service
    path: ./user-service
    url: https://github.com/org/user-service
    category: backend

  - name: frontend
    path: ./frontend
    url: https://github.com/org/frontend
    category: frontend

  - name: shared-lib
    path: ./shared-lib
    url: https://github.com/org/shared-lib
    category: library

  - name: infrastructure
    path: ./infrastructure
    url: https://github.com/org/infrastructure
    category: infra
```

## Synchronized Branching

### Create Branches Across Repos

```bash
#!/bin/bash
# sync-branch-create.sh - Create same branch in multiple repos

BRANCH_NAME="$1"
REPOS_FILE="${2:-.workspace}"

if [ -z "$BRANCH_NAME" ]; then
    echo "Usage: $0 <branch-name> [repos-file]"
    exit 1
fi

echo "=== Creating branch: $BRANCH_NAME ==="
echo ""

while IFS='|' read -r name path url; do
    echo "Repository: $name"
    cd "$path" || continue

    # Get current branch
    CURRENT=$(git branch --show-current)

    # Create and checkout new branch
    if git checkout -b "$BRANCH_NAME" 2>/dev/null; then
        echo "  ✓ Created and checked out $BRANCH_NAME"
    else
        # Branch might already exist
        if git checkout "$BRANCH_NAME" 2>/dev/null; then
            echo "  ✓ Checked out existing $BRANCH_NAME"
        else
            echo "  ✗ Failed to create/checkout $BRANCH_NAME"
        fi
    fi

    cd - > /dev/null
    echo ""
done < "$REPOS_FILE"

echo "✓ Branch creation complete"
```

### Claude-Compatible Multi-Repo Branching

```bash
#!/bin/bash
# claude-multi-branch.sh - Create Claude-formatted branches across repos

FEATURE="$1"
SESSION_ID="${2:-$(date +%s)}"
REPOS_FILE="${3:-.workspace}"

if [ -z "$FEATURE" ]; then
    echo "Usage: $0 <feature-name> [session-id] [repos-file]"
    exit 1
fi

while IFS='|' read -r name path url; do
    echo "=== $name ==="
    cd "$path" || continue

    # Claude branch format
    BRANCH="claude/${FEATURE}-${name}-${SESSION_ID}"

    git checkout main 2>/dev/null || git checkout master 2>/dev/null
    git pull

    if git checkout -b "$BRANCH"; then
        echo "✓ Created: $BRANCH"
    fi

    cd - > /dev/null
done < "$REPOS_FILE"
```

## Batch Operations

### Batch Status Check

```bash
#!/bin/bash
# multi-status.sh - Check status across all repos

REPOS_FILE="${1:-.workspace}"

echo "=== Repository Status ==="
echo ""

while IFS='|' read -r name path url; do
    cd "$path" || continue

    BRANCH=$(git branch --show-current)
    STATUS=$(git status --porcelain)
    UNPUSHED=$(git log origin/$BRANCH..$BRANCH --oneline 2>/dev/null | wc -l)

    echo "📁 $name"
    echo "   Branch: $BRANCH"

    if [ -z "$STATUS" ]; then
        echo "   Status: ✓ Clean"
    else
        CHANGES=$(echo "$STATUS" | wc -l)
        echo "   Status: ⚠️  $CHANGES file(s) changed"
    fi

    if [ "$UNPUSHED" -gt 0 ]; then
        echo "   Commits: ⚠️  $UNPUSHED unpushed"
    else
        echo "   Commits: ✓ Synced"
    fi

    echo ""
    cd - > /dev/null
done < "$REPOS_FILE"
```

### Batch Commit

```bash
#!/bin/bash
# multi-commit.sh - Commit changes across all repos

COMMIT_MSG="$1"
REPOS_FILE="${2:-.workspace}"

if [ -z "$COMMIT_MSG" ]; then
    echo "Usage: $0 <commit-message> [repos-file]"
    exit 1
fi

echo "=== Committing to all repositories ==="
echo "Message: $COMMIT_MSG"
echo ""

while IFS='|' read -r name path url; do
    cd "$path" || continue

    # Check if there are changes
    if [ -n "$(git status --porcelain)" ]; then
        echo "📁 $name"

        # Show what will be committed
        git status --short

        # Commit
        git add .
        if git commit -m "$COMMIT_MSG"; then
            echo "  ✓ Committed"
        else
            echo "  ✗ Commit failed"
        fi
        echo ""
    else
        echo "📁 $name - No changes"
    fi

    cd - > /dev/null
done < "$REPOS_FILE"

echo "✓ Batch commit complete"
```

### Batch Push with Retry

```bash
#!/bin/bash
# multi-push.sh - Push all repos with retry logic

REPOS_FILE="${1:-.workspace}"
MAX_RETRIES=4

push_with_retry() {
    local repo_name="$1"
    local branch="$2"

    for attempt in $(seq 1 $MAX_RETRIES); do
        if git push -u origin "$branch" 2>&1; then
            echo "  ✓ Pushed successfully"
            return 0
        else
            if [ $attempt -lt $MAX_RETRIES ]; then
                DELAY=$((2 ** attempt))
                echo "  ⚠️  Push failed (attempt $attempt/$MAX_RETRIES), retrying in ${DELAY}s..."
                sleep $DELAY
            fi
        fi
    done

    echo "  ✗ Push failed after $MAX_RETRIES attempts"
    return 1
}

echo "=== Pushing all repositories ==="
echo ""

FAILED_REPOS=()

while IFS='|' read -r name path url; do
    cd "$path" || continue

    BRANCH=$(git branch --show-current)
    UNPUSHED=$(git log origin/$BRANCH..$BRANCH --oneline 2>/dev/null | wc -l)

    if [ "$UNPUSHED" -gt 0 ]; then
        echo "📁 $name ($UNPUSHED commits)"
        if ! push_with_retry "$name" "$BRANCH"; then
            FAILED_REPOS+=("$name")
        fi
        echo ""
    else
        echo "📁 $name - Nothing to push"
    fi

    cd - > /dev/null
done < "$REPOS_FILE"

if [ ${#FAILED_REPOS[@]} -gt 0 ]; then
    echo "⚠️  Failed repositories:"
    printf '  - %s\n' "${FAILED_REPOS[@]}"
    exit 1
else
    echo "✓ All repositories pushed successfully"
fi
```

## Cross-Repository Operations

### Find File Across Repos

```bash
#!/bin/bash
# find-file.sh - Search for file across all repositories

PATTERN="$1"
REPOS_FILE="${2:-.workspace}"

if [ -z "$PATTERN" ]; then
    echo "Usage: $0 <filename-pattern> [repos-file]"
    exit 1
fi

echo "=== Searching for: $PATTERN ==="
echo ""

while IFS='|' read -r name path url; do
    cd "$path" || continue

    MATCHES=$(find . -name "$PATTERN" ! -path "*/node_modules/*" ! -path "*/.git/*")

    if [ -n "$MATCHES" ]; then
        echo "📁 $name"
        echo "$MATCHES" | sed 's/^/   /'
        echo ""
    fi

    cd - > /dev/null
done < "$REPOS_FILE"
```

### Grep Across Repos

```bash
#!/bin/bash
# multi-grep.sh - Search for pattern in all repos

PATTERN="$1"
REPOS_FILE="${2:-.workspace}"

if [ -z "$PATTERN" ]; then
    echo "Usage: $0 <search-pattern> [repos-file]"
    exit 1
fi

echo "=== Searching for pattern: $PATTERN ==="
echo ""

while IFS='|' read -r name path url; do
    cd "$path" || continue

    if git grep -n "$PATTERN" 2>/dev/null; then
        echo ""
        echo "--- Found in: $name ---"
        git grep -n --heading --break "$PATTERN"
        echo ""
    fi

    cd - > /dev/null
done < "$REPOS_FILE"
```

### Dependency Analysis

```bash
#!/bin/bash
# analyze-dependencies.sh - Find dependencies between repos

REPOS_FILE="${1:-.workspace}"

echo "=== Cross-Repository Dependencies ==="
echo ""

# Build list of package names
declare -A PACKAGES
while IFS='|' read -r name path url; do
    cd "$path" || continue

    # Check for package.json
    if [ -f "package.json" ]; then
        PKG_NAME=$(jq -r '.name' package.json 2>/dev/null)
        PACKAGES["$PKG_NAME"]="$name"
    fi

    cd - > /dev/null
done < "$REPOS_FILE"

# Check dependencies
while IFS='|' read -r name path url; do
    cd "$path" || continue

    if [ -f "package.json" ]; then
        echo "📁 $name"

        # Check dependencies
        for pkg_name in "${!PACKAGES[@]}"; do
            if jq -e ".dependencies[\"$pkg_name\"] // .devDependencies[\"$pkg_name\"]" package.json > /dev/null 2>&1; then
                VERSION=$(jq -r ".dependencies[\"$pkg_name\"] // .devDependencies[\"$pkg_name\"]" package.json)
                echo "   → depends on ${PACKAGES[$pkg_name]} ($pkg_name@$VERSION)"
            fi
        done
        echo ""
    fi

    cd - > /dev/null
done < "$REPOS_FILE"
```

## Testing & Building

### Run Tests Across Repos

```bash
#!/bin/bash
# multi-test.sh - Run tests in all repositories

REPOS_FILE="${1:-.workspace}"
TEST_CMD="${2:-npm test}"

echo "=== Running Tests Across Repositories ==="
echo "Command: $TEST_CMD"
echo ""

FAILED_REPOS=()

while IFS='|' read -r name path url; do
    echo "📁 Testing: $name"
    cd "$path" || continue

    if eval "$TEST_CMD" 2>&1 | tee "/tmp/$name-test.log"; then
        echo "  ✓ Tests passed"
    else
        echo "  ✗ Tests failed"
        FAILED_REPOS+=("$name")
    fi

    echo ""
    cd - > /dev/null
done < "$REPOS_FILE"

# Summary
echo "=== Test Summary ==="
if [ ${#FAILED_REPOS[@]} -eq 0 ]; then
    echo "✓ All tests passed!"
else
    echo "✗ Tests failed in:"
    printf '  - %s\n' "${FAILED_REPOS[@]}"
    exit 1
fi
```

### Parallel Build

```bash
#!/bin/bash
# multi-build.sh - Build all repos in parallel

REPOS_FILE="${1:-.workspace}"
BUILD_CMD="${2:-npm run build}"
MAX_PARALLEL=3

echo "=== Building Repositories ==="
echo "Command: $BUILD_CMD"
echo "Max parallel: $MAX_PARALLEL"
echo ""

ACTIVE_JOBS=0
declare -A JOB_PIDS

while IFS='|' read -r name path url; do
    # Wait if at max parallel
    while [ $ACTIVE_JOBS -ge $MAX_PARALLEL ]; do
        wait -n
        ACTIVE_JOBS=$((ACTIVE_JOBS - 1))
    done

    # Start build in background
    (
        echo "📁 Building: $name"
        cd "$path" || exit 1

        if eval "$BUILD_CMD" > "/tmp/$name-build.log" 2>&1; then
            echo "  ✓ $name built successfully"
        else
            echo "  ✗ $name build failed"
            echo "  Log: /tmp/$name-build.log"
        fi
    ) &

    JOB_PIDS["$name"]=$!
    ACTIVE_JOBS=$((ACTIVE_JOBS + 1))
done < "$REPOS_FILE"

# Wait for all builds
wait

echo ""
echo "✓ All builds complete"
```

## Advanced Workflows

### Coordinated Feature Development

```bash
#!/bin/bash
# feature-workflow.sh - Coordinate feature across repos

FEATURE="$1"
REPOS="$2"  # Comma-separated list or "all"

# 1. Create feature branches
echo "=== Step 1: Creating feature branches ==="
./claude-multi-branch.sh "$FEATURE"

# 2. Make changes (interactive or scripted)
echo ""
echo "=== Step 2: Make your changes ==="
echo "Make changes in the repositories, then run this script again"
read -p "Changes complete? (y/n) " -n 1 -r
echo

[[ ! $REPLY =~ ^[Yy]$ ]] && exit 0

# 3. Run tests
echo ""
echo "=== Step 3: Running tests ==="
./multi-test.sh

# 4. Commit changes
echo ""
echo "=== Step 4: Committing changes ==="
read -p "Commit message: " commit_msg
./multi-commit.sh "$commit_msg"

# 5. Push to remote
echo ""
echo "=== Step 5: Pushing to remote ==="
./multi-push.sh

# 6. Create PRs
echo ""
echo "=== Step 6: Creating pull requests ==="
./multi-pr.sh "$FEATURE"

echo ""
echo "✓ Feature workflow complete!"
```

### Multi-Repo PR Creation

```bash
#!/bin/bash
# multi-pr.sh - Create PRs for all repos

FEATURE="$1"
BASE_BRANCH="${2:-main}"
REPOS_FILE="${3:-.workspace}"

while IFS='|' read -r name path url; do
    cd "$path" || continue

    BRANCH=$(git branch --show-current)

    # Skip if on base branch
    if [ "$BRANCH" = "$BASE_BRANCH" ]; then
        echo "📁 $name - On base branch, skipping"
        continue
    fi

    # Check if there are changes
    if [ -z "$(git log origin/$BASE_BRANCH..$BRANCH --oneline)" ]; then
        echo "📁 $name - No changes, skipping"
        continue
    fi

    echo "📁 Creating PR for: $name"

    # Create PR
    gh pr create \
        --base "$BASE_BRANCH" \
        --head "$BRANCH" \
        --title "feat($name): $FEATURE" \
        --body "Part of $FEATURE feature implementation in $name repository." \
        2>&1 | grep -E "(Creating pull request|https://)"

    echo ""
    cd - > /dev/null
done < "$REPOS_FILE"
```

## Best Practices

### ✅ DO

1. **Use workspace files** to define repository collections
2. **Batch operations** for efficiency
3. **Check status** before batch commits
4. **Test before pushing** across all repos
5. **Use retry logic** for network operations
6. **Maintain consistency** in branch naming
7. **Track dependencies** between repositories
8. **Document relationships** in workspace config

### ❌ DON'T

1. **Don't assume** all repos need same changes
2. **Don't skip** individual repo status checks
3. **Don't force push** without careful consideration
4. **Don't ignore** test failures in any repo
5. **Don't commit** unrelated changes together
6. **Don't break** cross-repo dependencies
7. **Don't forget** to update shared libraries first
8. **Don't over-parallelize** (3-5 concurrent max)

## Quick Reference

```bash
# Discover repositories
./discover-repos.sh ~/projects

# Create branches across all repos
./sync-branch-create.sh feature-name

# Check status
./multi-status.sh

# Batch commit
./multi-commit.sh "feat: Add new feature"

# Batch push with retry
./multi-push.sh

# Run tests
./multi-test.sh

# Create PRs
./multi-pr.sh feature-name

# Search across repos
./multi-grep.sh "searchPattern"
```

---

**Version**: 1.0.0
**Author**: Harvested from multi-repository management patterns
**Last Updated**: 2025-11-18
**License**: MIT
**Key Principle**: Coordinate across repositories without losing sight of individual repo needs.
