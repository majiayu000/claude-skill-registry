---
name: pr-creation-workflow
description: Generic pull request creation workflow with configurable quality checks and multi-platform integration
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: pr-creation
---

## What I do

I provide a generic PR creation workflow that can be adapted for multiple scenarios:

1. **Identify Target Branch**: Determine which branch PR should merge into (configurable, not hardcoded)
2. **Run Quality Checks**: Execute configurable quality checks (linting, building, testing)
3. **Identify Tracking**: Check for JIRA tickets or git issue references in commits/PLAN.md
4. **Create Pull Request**: Create a PR linked to tracking systems with comprehensive description
5. **Handle Images**: Upload local images and embed in PR description/comments
6. **Merge Confirmation**: Prompt user for merge target after PR creation

## When to use me

Use this framework when:
- You need to create a pull request after completing work
- You want configurable quality checks (not just linting)
- You need PRs linked to JIRA or git issues
- You want to support multiple merge targets (not just `dev`)
- You need image attachments in PRs
- You're building a workflow skill that includes PR creation

This is a **framework skill** - it provides PR creation logic that other skills extend.

## Core Workflow Steps

### Step 1: Identify Target Branch

**Purpose**: Determine the correct base branch for PR

**Detection Methods**:

| Method | Description | Command |
|--------|-------------|----------|
| Ask user | Prompt for target branch | N/A (interactive) |
| Detect default | Get repository default branch | `git symbolic-ref refs/remotes/origin/HEAD` |
| Read config | Check for configured default | Read `.git/config` |

**Implementation**:
```bash
# Method 1: Ask user
read -p "Enter target branch (main/develop/staging/etc.): " TARGET_BRANCH

# Method 2: Detect default
if [ -z "$TARGET_BRANCH" ]; then
  TARGET_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
fi

# Method 3: Use provided default (e.g., from PLAN.md or previous PRs)
# If branch name contains "feature/*", default to develop or main
# If branch name contains "hotfix/*", default to main
# If branch name contains "release/*", default to main or staging
```

**Target Branch Examples**:
- `main` - Main production branch
- `develop` - Development branch
- `staging` - Pre-production branch
- `production` - Production branch (some projects use this instead of `main`)
- `master` - Legacy main branch

**Important**: Don't hardcode to `dev` - different projects use different conventions!

### Step 2: Run Quality Checks

**Purpose**: Verify code quality before creating PR

**Configurable Checks**:

 | Check Type | JavaScript/TypeScript | Python | Java | C# | Other |
|-----------|---------------------|--------|-----|-----|--------|
| Linting | `npm run lint` | `poetry run ruff check` | `mvn checkstyle` | `dotnet format` | Language-specific |
| Building | `npm run build` | N/A (Python doesn't build) | `mvn compile` | `dotnet build` | Language-specific |
| Testing | `npm run test` | `poetry run pytest` | `mvn test` | `dotnet test` | Framework-specific |
| Type Checking | `npm run typecheck` | `mypy .` | N/A | N/A | Language-specific |
| Docstrings | `docstring-generator` | `docstring-generator` | `docstring-generator` | `docstring-generator` | Industry best practice |

**Quality Check Execution**:
```bash
# Linting check (if enabled)
if [ "$RUN_LINTING" = "true" ]; then
  echo "Running linting..."
  if command -v npm &>/dev/null; then
    npm run lint
  elif command -v poetry &>/dev/null; then
    poetry run ruff check .
  fi
fi

# Build check (if enabled)
if [ "$RUN_BUILD" = "true" ]; then
  echo "Running build..."
  if command -v npm &>/dev/null; then
    npm run build
  fi
fi

#### Virtual Environment Detection for Python

**Purpose**: Ensure Python tests and type checks run in isolated virtual environment to prevent system library pollution

**Detection Patterns** (checked in priority order):
- `.venv` - Poetry default
- `venv` - Python standard
- `myvenv` - Custom
- `env` - Alternative
- `virtualenv` - Legacy

**Shell Detection and Activation**:
```bash
# Function to detect and activate virtual environment
activate_venv() {
  # Check for virtual environments in priority order
  for venv_dir in ".venv" "venv" "myvenv" "env" "virtualenv"; do
    if [ -d "$venv_dir" ]; then
      # Check shell type and activate accordingly
      if [ -n "${ZSH_VERSION:-}" ] || [ -n "${BASH_VERSION:-}" ]; then
        if [ -f "$venv_dir/bin/activate" ]; then
          source "$venv_dir/bin/activate"
          echo "✅ Using virtual environment: $venv_dir"
          return 0
        fi
      elif [ -n "${FISH_VERSION:-}" ]; then
        if [ -f "$venv_dir/bin/activate.fish" ]; then
          source "$venv_dir/bin/activate.fish"
          echo "✅ Using virtual environment: $venv_dir (fish)"
          return 0
        fi
      fi
    fi
  done

  # No virtual environment found
  return 1
}
```

**PowerShell Activation** (for Windows):
```powershell
if (Test-Path ".venv") {
  .\.venv\Scripts\Activate.ps1
  Write-Host "✅ Using virtual environment: .venv"
} elseif (Test-Path "venv") {
  .\venv\Scripts\Activate.ps1
  Write-Host "✅ Using virtual environment: venv"
}
```

**Handling Missing Virtual Environments**:
```bash
# Before running Python tests or type checks
if command -v poetry &>/dev/null; then
  if ! activate_venv; then
    echo "⚠️  No virtual environment found"
    if [ -f pyproject.toml ]; then
      read -p "Create virtual environment with 'poetry install'? (y/n): " CREATE_VENV
      if [ "$CREATE_VENV" = "y" ]; then
        echo "Creating virtual environment..."
        poetry install
        source .venv/bin/activate
        echo "✅ Created and activated virtual environment"
      else
        echo "⚠️  Warning: Tests may affect system Python libraries"
      fi
    else
      read -p "Create virtual environment with 'python -m venv .venv'? (y/n): " CREATE_VENV
      if [ "$CREATE_VENV" = "y" ]; then
        echo "Creating virtual environment..."
        python -m venv .venv
        source .venv/bin/activate
        echo "✅ Created and activated virtual environment"
      else
        echo "⚠️  Warning: Tests may affect system Python libraries"
      fi
    fi
  fi
fi
```

# Test check (if enabled)
if [ "$RUN_TESTS" = "true" ]; then
  echo "Running tests..."
  if command -v npm &>/dev/null; then
    npm run test
  elif command -v poetry &>/dev/null; then
    # Ensure virtual environment is active
    activate_venv || true  # Will prompt to create if missing
    poetry run pytest
  elif command -v python &>/dev/null; then
    # Direct Python project without Poetry
    activate_venv || true
    pytest 2>/dev/null || python -m pytest
  fi
fi

# Type check (if enabled)
if [ "$RUN_TYPECHECK" = "true" ]; then
  echo "Running type check..."
  if command -v npm &>/dev/null; then
    npm run typecheck
  elif command -v poetry &>/dev/null; then
    # Ensure virtual environment is active
    activate_venv || true
    poetry run mypy . 2>/dev/null || mypy .
  elif command -v python &>/dev/null; then
    activate_venv || true
    mypy . 2>/dev/null || echo "⚠️  mypy not installed, skipping type check"
  fi
fi

# Docstring check (if enabled) - Industry Best Practice
if [ "$RUN_DOCSTRINGS" = "true" ]; then
  echo "Checking docstrings..."
  if command -v opencode &>/dev/null; then
    opencode --agent docstring-generator "Check for missing docstrings in changed files"
  else
    # Manual docstring check
    UNDOC_COUNT=0
    for file in $(git diff --name-only HEAD~1..HEAD); do
      case "$file" in
        *.py)    UNDOC=$(grep -c 'def ' "$file" - $(grep -c '"""' "$file")) ;;
        *.java)   UNDOC=$(grep -c 'public.*(' "$file" - $(grep -c '/\*\*' "$file")) ;;
        *.ts|tsx) UNDOC=$(grep -c 'function' "$file" - $(grep -c '/\*\*' "$file")) ;;
        *.cs|csx) UNDOC=$(grep -c 'public.*(' "$file" - $(grep -c '///' "$file")) ;;
      esac
      UNDOC_COUNT=$((UNDOC_COUNT + UNDOC))
    done

    if [ "$UNDOC_COUNT" -gt 0 ]; then
      echo "Found $UNDOC_COUNT undocumented items"
    fi
  fi
fi
```

**Quality Check Results**:
```bash
# Store results for PR description
LINT_RESULT="✅ Passed" || "❌ Failed"
BUILD_RESULT="✅ Passed" || "❌ Failed"
TEST_RESULT="✅ Passed" || "❌ Failed"
TYPECHECK_RESULT="✅ Passed" || "❌ Failed"
DOCSTRING_RESULT="✅ Passed" || "❌ Failed (industry best practice)"
```

**Error Handling**:
- If a check fails, ask user if they want to:
  - Fix and retry
  - Continue with failed checks
  - Cancel PR creation

### Step 3: Identify Tracking System

**Purpose**: Determine if PR should link to JIRA ticket or git issue

**Detection Methods**:

| Source | Detection Pattern | Example |
|---------|------------------|----------|
| Commit messages | Regex for JIRA ticket key | `[IBIS-123] Fix bug` |
| PLAN.md | Search for JIRA references | `JIRA Reference: IBIS-456` |
| Branch name | Parse ticket key from branch | `IBIS-101-add-feature` |
| Git config | Read from previous PRs | N/A |

**Detection Logic**:
```bash
# Check commits for JIRA ticket
JIRA_TICKET=$(git log --oneline -1 | grep -oE '[A-Z]+-[0-9]+')

# Check commits for git issue reference
GIT_ISSUE=$(git log --oneline -1 | grep -oE '#[0-9]+')

# Check PLAN.md for tracking references
if [ -f "PLAN.md" ]; then
  PLAN_JIRA=$(grep -oE '[A-Z]+-[0-9]+' PLAN.md | head -1)
  PLAN_ISSUE=$(grep -oE '#[0-9]+' PLAN.md | head -1)
fi

# Determine tracking system
if [ -n "$JIRA_TICKET" ]; then
  TRACKING_SYSTEM="jira"
  TRACKING_ID="$JIRA_TICKET"
elif [ -n "$PLAN_JIRA" ]; then
  TRACKING_SYSTEM="jira"
  TRACKING_ID="$PLAN_JIRA"
elif [ -n "$GIT_ISSUE" ]; then
  TRACKING_SYSTEM="git"
  TRACKING_ID="$GIT_ISSUE"
else
  TRACKING_SYSTEM="none"
  TRACKING_ID=""
fi
```

**Tracking System Types**:

| System | ID Format | Example |
|---------|-----------|----------|
| JIRA | PROJECT-NUM | `IBIS-123` |
| Git Issue | #NUM | `#456` |
| None | N/A | Standalone PR |

### Step 4: Check Git Status

**Purpose**: Verify all changes are committed and branch is ready for PR

**Git Status Checks**:
```bash
# Check if working tree is clean
GIT_STATUS=$(git status --porcelain)

if [ -n "$GIT_STATUS" ]; then
  echo "Warning: You have uncommitted changes:"
  echo "$GIT_STATUS"
  read -p "Commit changes before creating PR? (y/n): " COMMIT_CHANGES
  if [ "$COMMIT_CHANGES" = "y" ]; then
    git add .
    git commit -m "Prepare for PR"
  fi
fi

# Check if branch has remote tracking
CURRENT_BRANCH=$(git branch --show-current)
REMOTE_TRACKING=$(git branch --show-current | grep -q "@" && echo "yes" || echo "no")

if [ "$REMOTE_TRACKING" = "no" ]; then
  echo "Branch does not track remote. Pushing..."
  git push -u origin "$CURRENT_BRANCH"
fi
```

### Step 5: Scan for Images

**Purpose**: Find images that should be attached or referenced in PR

**Image Detection**:
```bash
# Search for common image locations
IMAGES=()

# Check diagrams directory
if [ -d "diagrams" ]; then
  IMAGES+=($(find diagrams -type f \( -name "*.png" -o -name "*.svg" -o -name "*.jpg" -o -name "*.jpeg" \)))
fi

# Check tmp directory
IMAGES+=($(find /tmp -type f \( -name "*.png" -o -name "*.svg" \) -mmin -60 2>/dev/null))

# Check for workflow-related files
IMAGES+=($(find . -maxdepth 2 -type f \( -name "*workflow*.png" -o -name "*diagram*.png" \) 2>/dev/null))

# Display found images
if [ ${#IMAGES[@]} -gt 0 ]; then
  echo "Found images:"
  printf '  - %s\n' "${IMAGES[@]}"
  read -p "Include these images in PR? (y/n): " INCLUDE_IMAGES
else
  INCLUDE_IMAGES="n"
fi
```

### Step 6: Create Pull Request

**Purpose**: Create PR with comprehensive description linked to tracking system

**PR Creation by Tracking System**:

#### JIRA-Linked PR:
```bash
gh pr create \
  --base "$TARGET_BRANCH" \
  --title "feat: <summary> [${TRACKING_ID}]" \
  --body "$(cat <<'EOF'
## Summary
<Bullet points describing changes>

## JIRA Reference
- Ticket: ${TRACKING_ID}
- Link: https://<company>.atlassian.net/browse/${TRACKING_ID}

## Changes
- <Key change 1>
- <Key change 2>
- <Key change 3>

## Quality Checks
- Linting: ${LINT_RESULT}
- Build: ${BUILD_RESULT}
- Tests: ${TEST_RESULT}
- Type Check: ${TYPECHECK_RESULT}

## Files Modified
- \`src/path/to/file1.ts\` - Description
- \`src/path/to/file2.tsx\` - Description
- \`README.md\` - Documentation updates

## Checklist
- [ ] Code follows project style guidelines
- [ ] All quality checks passed
- [ ] Documentation updated
- [ ] Self-reviewed
EOF
)"
```

**Note**: PR title follows Conventional Commits format. Use `git-semantic-commits` for guidance:
- `feat: <summary> [${TRACKING_ID}]` - New feature
- `fix: <summary> [${TRACKING_ID}]` - Bug fix
- `docs: <summary> [${TRACKING_ID}]` - Documentation change
- With scope: `feat(api): add authentication [${TRACKING_ID}]`
- Breaking change: `feat!: breaking API change [${TRACKING_ID}]`

#### Git Issue-Linked PR:
```bash
gh pr create \
  --base "$TARGET_BRANCH" \
  --title "fix: <summary> (#${TRACKING_ID})" \
  --body "$(cat <<'EOF'
## Summary
<Bullet points describing changes>

## Issue Reference
- Resolves #${TRACKING_ID}
- Link: <issue-url>

## Changes
- <Key change 1>
- <Key change 2>

## Quality Checks
- Linting: ${LINT_RESULT}
- Build: ${BUILD_RESULT}
- Tests: ${TEST_RESULT}

## Files Modified
- \`src/path/to/file1.ts\` - Description
- \`src/path/to/file2.tsx\` - Description

## Checklist
- [ ] Code follows project style guidelines
- [ ] All quality checks passed
- [ ] Documentation updated
- [ ] Self-reviewed
EOF
)"
```

**Note**: PR title follows Conventional Commits format. Use `git-semantic-commits` for guidance:
- `fix: <summary> (#${TRACKING_ID})` - Bug fix
- `feat: <summary> (#${TRACKING_ID})` - New feature
- With scope: `fix(ui): resolve layout issue (#${TRACKING_ID})`
- Breaking change: `fix!: breaking API change (#${TRACKING_ID})`

#### Standalone PR (No Tracking):
```bash
gh pr create \
  --base "$TARGET_BRANCH" \
  --title "feat: <summary>" \
  --body "$(cat <<'EOF'
## Summary
<Bullet points describing changes>

## Changes
- <Key change 1>
- <Key change 2>
- <Key change 3>

## Quality Checks
- Linting: ${LINT_RESULT}
- Build: ${BUILD_RESULT}
- Tests: ${TEST_RESULT}
- Type Check: ${TYPECHECK_RESULT}

## Files Modified
- \`src/path/to/file1.ts\` - Description
- \`src/path/to/file2.tsx\` - Description

## Checklist
- [ ] Code follows project style guidelines
- [ ] All quality checks passed
- [ ] Documentation updated
- [ ] Self-reviewed
EOF
)"
```

**Note**: PR title follows Conventional Commits format. Use `git-semantic-commits` for guidance:
- `feat: <summary>` - New feature
- `fix: <summary>` - Bug fix
- `docs: <summary>` - Documentation change
- `refactor: <summary>` - Code refactoring
- With scope: `feat(api): add authentication`
- Breaking change: `feat!: breaking API change`

### Step 7: Handle Images in PR

**Purpose**: Upload local images to hosting platform or reference in PR

**Image Handling Strategy**:

| Image Type | Action |
|-----------|--------|
| Public URL | Embed directly in PR |
| Local file | Upload to external host or attach to tracking system |
| Temp file | Upload or warn user it's temporary |

**Implementation**:
```bash
if [ "$INCLUDE_IMAGES" = "y" ] && [ ${#IMAGES[@]} -gt 0 ]; then
  for image in "${IMAGES[@]}"; do
    if [[ "$image" =~ ^https?:// ]]; then
      # It's already a URL - add to PR
      PR_BODY+="
![Diagram]($image)"
    elif [ -f "$image" ]; then
      # Local file - need to upload
      # Option 1: Upload to JIRA if tracking system is JIRA
      # Option 2: Upload to image hosting service
      # Option 3: Commit to repository (for diagrams)
      echo "Local image: $image"
      echo "This should be uploaded or committed to the repository"
    fi
  done
fi
```

### Step 8: Merge Confirmation

**Purpose**: Ask user to confirm merge target after successful PR creation

**Implementation**:
```bash
# Get PR number
PR_NUMBER=$(gh pr view --json number --jq '.number')
PR_URL=$(gh pr view --json url --jq '.url')

# Display success message
echo ""
echo "✅ Pull request created successfully!"
echo ""
echo "**PR Details:**"
echo "- Number: #$PR_NUMBER"
echo "- Title: <pr-title>"
echo "- Branch: $CURRENT_BRANCH"
echo "- Target: $TARGET_BRANCH"
echo "- URL: $PR_URL"
echo ""

# Ask for merge confirmation
read -p "Would you like to proceed with merging this PR? If yes, please specify target branch (default: $TARGET_BRANCH): " MERGE_CONFIRMATION

if [ "$MERGE_CONFIRMATION" = "y" ]; then
  read -p "Enter target branch (default: $TARGET_BRANCH): " MERGE_TARGET
  MERGE_TARGET=${MERGE_TARGET:-$TARGET_BRANCH}

  # Merge PR
  gh pr merge "$PR_NUMBER" --base "$MERGE_TARGET"
  echo "✅ PR merged into $MERGE_TARGET"

  # Step 9: Update JIRA Ticket Status (if applicable)
  if [ "$TRACKING_SYSTEM" = "jira" ] && [ -n "$TRACKING_ID" ]; then
    read -p "Update JIRA ticket status to Done? (y/n): " UPDATE_JIRA

    if [ "$UPDATE_JIRA" = "y" ]; then
      echo ""
      echo "Updating JIRA ticket status..."
      echo "=========================================="

      # Use jira-status-updater to transition ticket
      # This skill handles:
      # - Detecting JIRA ticket from PR/commits
      # - Querying available transitions
      # - Finding target status (Done/Closed)
      # - Executing status transition
      # - Adding merge comment with details

      # Integration pattern:
      # 1. Extract commit details
      COMMIT_HASH=$(git rev-parse HEAD)
      COMMIT_AUTHOR=$(git log -1 --pretty=%an)
      COMMIT_DATE=$(git log -1 --date=iso8601 --pretty=%aI)

      # 2. Detect JIRA ticket (already have TRACKING_ID)
      JIRA_TICKET="$TRACKING_ID"

      # 3. Get cloud ID
      CLOUD_ID="${ATLASSIAN_CLOUD_ID:-<your-cloud-id>}"

      # 4. Get available transitions
      TRANSITIONS=$(atlassian_getTransitionsForJiraIssue \
        --cloudId "$CLOUD_ID" \
        --issueIdOrKey "$JIRA_TICKET")

      # 5. Find "Done" or "Closed" transition
      TARGET_TRANSITION_ID=$(echo "$TRANSITIONS" | jq -r '.transitions[] | select(.to.name == "Done" or .to.name == "Closed") | .id' | head -1)
      TARGET_TRANSITION_NAME=$(echo "$TRANSITIONS" | jq -r '.transitions[] | select(.to.name == "Done" or .to.name == "Closed") | .to.name' | head -1)

      # 6. Get current status
      TICKET_DETAILS=$(atlassian_getJiraIssue \
        --cloudId "$CLOUD_ID" \
        --issueIdOrKey "$JIRA_TICKET")
      CURRENT_STATUS=$(echo "$TICKET_DETAILS" | jq -r '.fields.status.name')

      # 7. Check if already in target status
      if [ "$CURRENT_STATUS" = "$TARGET_TRANSITION_NAME" ]; then
        echo "✅ Ticket already in target status: $TARGET_TRANSITION_NAME"
      else
        # 8. Execute transition
        if [ -n "$TARGET_TRANSITION_ID" ]; then
          TRANSITION_RESULT=$(atlassian_transitionJiraIssue \
            --cloudId "$CLOUD_ID" \
            --issueIdOrKey "$JIRA_TICKET" \
            --transition "{\"id\": \"$TARGET_TRANSITION_ID\"}")

          if [ $? -eq 0 ]; then
            echo "✅ Successfully transitioned $JIRA_TICKET from $CURRENT_STATUS to $TARGET_TRANSITION_NAME"
          else
            echo "❌ Failed to transition $JIRA_TICKET"
            echo "   Transition ID: $TARGET_TRANSITION_ID"
            echo "   Please check permissions and available transitions"
          fi
        else
          echo "⚠️  No 'Done' or 'Closed' transition available for $JIRA_TICKET"
          echo "   Available transitions:"
          echo "$TRANSITIONS" | jq -r '.transitions[] | "   - \(.to.name)"'
        fi
      fi

      # 9. Add merge comment
      COMMENT_BODY=$(cat <<EOF
## Pull Request Merged

**PR**: #$PR_NUMBER - <pr-title>
**URL**: $PR_URL
**Branch**: $CURRENT_BRANCH → $MERGE_TARGET

### Status Update
✅ Ticket transitioned from **$CURRENT_STATUS** to **$TARGET_TRANSITION_NAME**

### Merge Details
- **Commit**: \`$COMMIT_HASH\`
- **Author**: $COMMIT_AUTHOR
- **Date**: $COMMIT_DATE

### Files Changed
\`\`\`
$(git diff --stat HEAD~1 HEAD)
\`\`\`
EOF
)

      atlassian_addCommentToJiraIssue \
        --cloudId "$CLOUD_ID" \
        --issueIdOrKey "$JIRA_TICKET" \
        --commentBody "$COMMENT_BODY"

      if [ $? -eq 0 ]; then
        echo "✅ Added merge comment to $JIRA_TICKET"
      else
        echo "⚠️  Failed to add comment to $JIRA_TICKET"
      fi

      echo "=========================================="
      echo ""
      echo "🔗 JIRA Ticket: https://<company>.atlassian.net/browse/$JIRA_TICKET"
    fi
  fi
fi
```

## Quality Check Configuration

### JavaScript/TypeScript Projects

| Check | Script | Command | Auto-fix |
|-------|--------|----------|-----------|
| Linting | `npm run lint` | ESLint | `npm run lint -- --fix` |
| Build | `npm run build` | N/A | N/A |
| Test | `npm run test` | Jest/Vitest | N/A |
| Type Check | `npm run typecheck` | TypeScript | N/A |

### Python Projects

| Check | Command | Tool | Auto-fix |
|-------|----------|------|-----------|
| Linting | `poetry run ruff check` | Ruff | `poetry run ruff check --fix` |
| Type Check | `poetry run mypy .` | mypy | N/A |
| Test | `poetry run pytest` | pytest | N/A |

## Best Practices

- **Target Branch**: Don't hardcode to `dev` - ask user or detect default
- **Quality Checks**: Make them configurable - not all projects need all checks
- **Tracking Links**: Always include JIRA/git issue references for traceability
- **PR Descriptions**: Use consistent format with summary, changes, quality checks
- **Image Handling**: Upload local images, don't link to `/tmp/` or local paths
- **Merge Confirmation**: Always ask user before merging
- **Branch Cleanliness**: Ensure working tree is clean before creating PR
- **Commit Quality**: **Use git-semantic-commits for PR title formatting** following Conventional Commits specification
- **PR Titles**: Follow semantic format: `feat: <summary>`, `fix: <summary>`, `docs: <summary>`
- **PR Scopes**: Include scope when relevant: `feat(api): add authentication`, `fix(ui): resolve layout issue`
- **Breaking Changes**: Use `!` indicator: `feat!: breaking API change` or `feat(api)!: breaking change to authentication`
- **Issue Tracking**: **Use git-issue-updater for JIRA ticket updates** with consistent format (user, date, time, PR details)
- **PR Size**: Keep PRs focused and small (< 400 lines changed ideal)
- **Review Checklist**: Include self-review checklist in every PR
- **Virtual Environments**: Always activate Python virtual environments before running tests or type checks to prevent system library pollution
- **Environment Isolation**: Use Poetry's `.venv` or standard `venv` for Python projects, never run tests in system Python

## Common Issues

### Target Branch Not Specified

**Issue**: User doesn't provide target branch and auto-detection fails

**Solution**:
```bash
# Prompt user for target branch
read -p "Enter target branch (main/develop/staging/etc.): " TARGET_BRANCH

# Provide default if available
TARGET_BRANCH=${TARGET_BRANCH:-main}
```

### Quality Checks Fail

**Issue**: Linting, build, or tests fail

**Solution**:
```bash
# Offer to fix automatically
if [ "$RUN_LINTING" = "true" ]; then
  read -p "Linting failed. Run auto-fix? (y/n): " AUTO_FIX
  if [ "$AUTO_FIX" = "y" ]; then
    npm run lint -- --fix
  fi
fi

# Ask if user wants to continue anyway
read -p "Some checks failed. Create PR anyway? (y/n): " CONTINUE_PR
if [ "$CONTINUE_PR" = "n" ]; then
  echo "PR creation cancelled. Please fix issues and retry."
  exit 1
fi
```

### Tracking Not Detected

**Issue**: No JIRA ticket or git issue reference found

**Solution**:
```bash
# Create standalone PR without tracking reference
TRACKING_SYSTEM="none"
TRACKING_ID=""

# Or ask user to provide reference
read -p "Enter JIRA ticket or git issue number (leave blank for none): " USER_TRACKING
if [ -n "$USER_TRACKING" ]; then
  # Parse and use provided tracking
fi
```

### Branch Not Pushed

**Issue**: PR creation fails because branch doesn't exist on remote

**Solution**:
```bash
# Push branch with upstream tracking
git push -u origin $(git branch --show-current)
```

### Image Upload Issues

**Issue**: Local images can't be referenced in PR

**Solution**:
- Commit images to repository (for diagrams)
- Upload to external image hosting
- Upload to JIRA if JIRA ticket exists
- Ask user to handle manually

### Virtual Environment Not Detected

**Issue**: Virtual environment check fails or doesn't detect existing venv

**Solution**:
```bash
# Manually specify virtual environment directory
VENV_DIR=".venv"  # or "venv", "myvenv", etc.

if [ -d "$VENV_DIR" ]; then
  source "$VENV_DIR/bin/activate"
  echo "✅ Manually activated: $VENV_DIR"
else
  echo "❌ Virtual environment not found: $VENV_DIR"
  echo "Available options:"
  ls -la | grep -E 'venv|env' || echo "  No virtual environments found"
fi
```

**Common detection issues**:
- Custom venv location not in standard paths
- venv created with different tool (conda, virtualenvwrapper)
- Shell-specific activation scripts missing
- Permission issues accessing venv directory

### Virtual Environment Activation Fails

**Issue**: `activate_venv` function fails to activate virtual environment

**Solution**:
```bash
# Check virtual environment structure
ls -la .venv/bin/ | grep activate

# Try manual activation
source .venv/bin/activate

# Verify activation
echo $VIRTUAL_ENV  # Should show venv path
which python      # Should show venv python, not system python
```

**If activation still fails**:
```bash
# Recreate virtual environment (Poetry)
rm -rf .venv
poetry install

# Recreate virtual environment (pip)
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Poetry Install Fails

**Issue**: `poetry install` command fails when creating virtual environment

**Solution**:
```bash
# Check Poetry version
poetry --version

# Check pyproject.toml exists
ls -la pyproject.toml

# Try verbose install for debugging
poetry install -vvv

# Common fixes:
# 1. Update Poetry
pip install --upgrade poetry

# 2. Clear Poetry cache
poetry cache clear --all pypi

# 3. Check Python version in pyproject.toml
grep "python" pyproject.toml

# 4. Use explicit Python version
poetry env use $(which python3.11)
```

### Tests Run in System Python

**Issue**: Tests execute in system Python despite virtual environment detection

**Solution**:
```bash
# Verify virtual environment is active
echo $VIRTUAL_ENV

# Check which Python is being used
which python
which pytest

# Force virtual environment activation before tests
if [ -z "${VIRTUAL_ENV:-}" ]; then
  echo "⚠️  Warning: No virtual environment active"
  source .venv/bin/activate
  echo "✅ Activated virtual environment: $VIRTUAL_ENV"
fi

# Now run tests
poetry run pytest
```

**Prevention**: Always use `poetry run pytest` instead of direct `pytest` to ensure Poetry's environment is used.

## Troubleshooting Checklist

Before creating PR:
- [ ] All changes are committed
- [ ] Working tree is clean
- [ ] Branch has remote tracking
- [ ] Target branch is identified (asked user or detected)
- [ ] Quality checks are configured correctly
- [ ] Images are handled (uploaded or committed)
- [ ] Tracking system reference is identified

Before running Python quality checks:
- [ ] Virtual environment detection is enabled for Python projects
- [ ] Virtual environment directory exists (.venv, venv, myvenv, etc.)
- [ ] Virtual environment activation scripts are present
- [ ] Poetry is detected for Poetry projects
- [ ] Shell type is correctly identified (bash/zsh/fish/PowerShell)

After PR creation:
- [ ] PR number is captured
- [ ] PR URL is accessible
- [ ] PR description is complete
- [ ] Quality check status is included
- [ ] Images are properly referenced
- [ ] Tracking reference is included (if applicable)

After JIRA status update (if enabled):
- [ ] JIRA ticket key is valid
- [ ] Cloud ID is configured
- [ ] Status transition was successful
- [ ] Merge comment was added to JIRA
- [ ] Error handling for missing transitions or permissions

## Relevant Commands

```bash
# Get current branch
git branch --show-current

# Get default branch
git symbolic-ref refs/remotes/origin/HEAD

# Check git status
git status

# Check for remote tracking
git branch -vv | grep '*'

# Push branch with upstream
git push -u origin <branch-name>

# Create PR
gh pr create --base <target> --title "Title" --body "Description"

# View PR
gh pr view

# List PRs
gh pr list

# Merge PR
gh pr merge <pr-number>

# Close PR (without merge)
gh pr close <pr-number>

# Virtual Environment Commands

# Detect if virtual environment is active
echo $VIRTUAL_ENV

# Check which Python is being used
which python
which pytest

# Activate virtual environment (bash/zsh)
source .venv/bin/activate

# Activate virtual environment (fish)
source .venv/bin/activate.fish

# Activate virtual environment (PowerShell)
.\.venv\Scripts\Activate.ps1

# Create Poetry virtual environment
poetry install

# Create standard virtual environment
python -m venv .venv

# Run tests in virtual environment
poetry run pytest

# Run type checking in virtual environment
poetry run mypy .

# Run linting in virtual environment
poetry run ruff check .

# Deactivate virtual environment
deactivate

# List all virtual environment directories
ls -la | grep -E 'venv|env'

# Check Poetry environment info
poetry env info
```

## Relevant Skills

Skills that use this PR creation framework:
- `git-pr-creator`: PR creation with JIRA integration and image uploads
- `nextjs-pr-workflow`: Next.js-specific PR workflow with linting and building

Supporting framework skills:
- **Git Frameworks**:
  - `git-semantic-commits`: For semantic commit message formatting and PR title conventions
  - `git-issue-updater`: For consistent issue/ticket update functionality with user, date, time
- **JIRA Integration**:
  - `jira-git-integration`: For JIRA ticket management and comments
  - `jira-status-updater`: For automated JIRA ticket status transitions after PR merge
- **Quality Assurance**:
  - `linting-workflow`: For configurable quality checks
- **Workflow Management**:
  - `ticket-branch-workflow`: For initial ticket-to-branch setup
