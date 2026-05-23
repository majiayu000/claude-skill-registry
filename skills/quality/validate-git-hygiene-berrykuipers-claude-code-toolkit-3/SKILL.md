---
name: validate-git-hygiene
description: Validate git commit messages, branch naming conventions, and check for sensitive files. Returns structured output with commit format validation, branch name compliance, and sensitive file detection (.env, credentials, .pem, .key). Used for git workflow validation and security checks.
---

# Validate Git Hygiene

## Purpose

Validate git repository hygiene including commit message format, branch naming conventions, and sensitive file detection.

## When to Use

- Conductor Phase 2 (Implementation) - Branch validation
- Conductor Phase 4 (PR Creation) - Commit validation
- Pre-commit hooks validation
- Security audits (sensitive file detection)
- Git workflow compliance checks

## Validation Checks

1. **Commit Messages**: Conventional Commits format
2. **Branch Naming**: Standard patterns (feat/*, fix/*, etc.)
3. **Sensitive Files**: Detection of credentials, keys, etc.

## Instructions

### Step 1: Validate Branch Name

```bash
echo "→ Validating branch name..."

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Check against standard patterns
VALID_PATTERNS=(
  "^feat/.*"
  "^fix/.*"
  "^docs/.*"
  "^chore/.*"
  "^refactor/.*"
  "^test/.*"
  "^hotfix/.*"
  "^release/.*"
  "^main$"
  "^master$"
  "^develop$"
  "^development$"
  "^claude/.*"
)

BRANCH_VALID="false"
for pattern in "${VALID_PATTERNS[@]}"; do
  if echo "$CURRENT_BRANCH" | grep -qE "$pattern"; then
    BRANCH_VALID="true"
    break
  fi
done

if [ "$BRANCH_VALID" = "true" ]; then
  echo "✅ Branch name valid: $CURRENT_BRANCH"
  BRANCH_STATUS="valid"
else
  echo "❌ Branch name invalid: $CURRENT_BRANCH"
  echo "   Expected: feat/*, fix/*, docs/*, chore/*, etc."
  BRANCH_STATUS="invalid"
fi
```

### Step 2: Validate Recent Commits

```bash
echo ""
echo "→ Validating recent commit messages..."

# Get last 10 commits (or since main/develop)
COMMITS=$(git log --oneline --no-merges -10 --format="%H %s")

# Conventional commit pattern
COMMIT_PATTERN="^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?!?: .+"

INVALID_COMMITS=()
VALID_COMMITS=0

while IFS= read -r commit; do
  HASH=$(echo "$commit" | cut -d' ' -f1)
  MSG=$(echo "$commit" | cut -d' ' -f2-)

  if echo "$MSG" | grep -qE "$COMMIT_PATTERN"; then
    ((VALID_COMMITS++))
  else
    INVALID_COMMITS+=("$HASH:$MSG")
  fi
done <<< "$COMMITS"

TOTAL_COMMITS=$((VALID_COMMITS + ${#INVALID_COMMITS[@]}))

if [ ${#INVALID_COMMITS[@]} -eq 0 ]; then
  echo "✅ All $VALID_COMMITS commit messages valid"
  COMMITS_STATUS="valid"
else
  echo "❌ ${#INVALID_COMMITS[@]} invalid commit messages found"
  COMMITS_STATUS="invalid"

  # Show first 3 invalid commits
  for i in "${INVALID_COMMITS[@]:0:3}"; do
    HASH=$(echo "$i" | cut -d: -f1)
    MSG=$(echo "$i" | cut -d: -f2-)
    echo "   $HASH: $MSG"
  done
fi
```

### Step 3: Check for Sensitive Files

```bash
echo ""
echo "→ Checking for sensitive files..."

# Patterns for sensitive files
SENSITIVE_PATTERNS=(
  "\.env$"
  "\.env\..+"
  "credentials\.json$"
  "\.pem$"
  "\.key$"
  "\.p12$"
  "id_rsa$"
  "\.ssh/"
  "secret"
  "private.*\.key$"
  "\.pfx$"
)

SENSITIVE_FILES=()

# Check tracked files
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
  while IFS= read -r file; do
    if [ -n "$file" ]; then
      SENSITIVE_FILES+=("$file")
    fi
  done < <(git ls-files | grep -E "$pattern")
done

# Check unstaged/untracked
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
  while IFS= read -r file; do
    # Only files not in .gitignore
    if [ -n "$file" ] && ! git check-ignore -q "$file" 2>/dev/null; then
      SENSITIVE_FILES+=("$file (untracked)")
    fi
  done < <(git status --porcelain | awk '{print $2}' | grep -E "$pattern")
done

if [ ${#SENSITIVE_FILES[@]} -eq 0 ]; then
  echo "✅ No sensitive files detected"
  SENSITIVE_STATUS="clean"
else
  echo "⚠️  ${#SENSITIVE_FILES[@]} potential sensitive files found:"
  SENSITIVE_STATUS="found"

  for file in "${SENSITIVE_FILES[@]:0:5}"; do
    echo "   - $file"
  done
fi
```

### Step 4: Determine Overall Status

```bash
# Aggregate results
if [ "$BRANCH_STATUS" = "valid" ] && [ "$COMMITS_STATUS" = "valid" ] && [ "$SENSITIVE_STATUS" = "clean" ]; then
  OVERALL_STATUS="passing"
  CAN_PROCEED="true"
  STATUS="success"
elif [ "$SENSITIVE_STATUS" = "found" ]; then
  OVERALL_STATUS="sensitive-files"
  CAN_PROCEED="false"
  STATUS="error"
  DETAILS="Sensitive files detected - must be removed or added to .gitignore"
elif [ "$BRANCH_STATUS" = "invalid" ] || [ "$COMMITS_STATUS" = "invalid" ]; then
  OVERALL_STATUS="format-issues"
  CAN_PROCEED="true"
  STATUS="warning"
  DETAILS="Git hygiene issues detected - should be fixed but not blocking"
else
  OVERALL_STATUS="passing"
  CAN_PROCEED="true"
  STATUS="success"
fi
```

### Step 5: Return Structured Output

```json
{
  "status": "$STATUS",
  "gitHygiene": {
    "status": "$OVERALL_STATUS",
    "branch": {
      "name": "$CURRENT_BRANCH",
      "valid": $([ "$BRANCH_STATUS" = "valid" ] && echo 'true' || echo 'false')
    },
    "commits": {
      "total": $TOTAL_COMMITS,
      "valid": $VALID_COMMITS,
      "invalid": ${#INVALID_COMMITS[@]},
      "invalidExamples": $(printf '%s\n' "${INVALID_COMMITS[@]:0:3}" | jq -R -s -c 'split("\n") | map(select(length > 0))')
    },
    "sensitiveFiles": {
      "count": ${#SENSITIVE_FILES[@]},
      "files": $(printf '%s\n' "${SENSITIVE_FILES[@]}" | jq -R -s -c 'split("\n") | map(select(length > 0))')
    }
  },
  "canProceed": $CAN_PROCEED,
  "details": "$DETAILS"
}
```

## Output Format

### All Checks Pass

```json
{
  "status": "success",
  "gitHygiene": {
    "status": "passing",
    "branch": {
      "name": "feat/add-user-profile",
      "valid": true
    },
    "commits": {
      "total": 10,
      "valid": 10,
      "invalid": 0,
      "invalidExamples": []
    },
    "sensitiveFiles": {
      "count": 0,
      "files": []
    }
  },
  "canProceed": true
}
```

### Issues Found

```json
{
  "status": "warning",
  "gitHygiene": {
    "status": "format-issues",
    "branch": {
      "name": "update-settings",
      "valid": false
    },
    "commits": {
      "total": 10,
      "valid": 7,
      "invalid": 3,
      "invalidExamples": [
        "a1b2c3d:updated some stuff",
        "e4f5g6h:WIP",
        "i7j8k9l:fixed bug"
      ]
    },
    "sensitiveFiles": {
      "count": 0,
      "files": []
    }
  },
  "canProceed": true,
  "details": "Git hygiene issues detected - should be fixed but not blocking"
}
```

### Sensitive Files Detected

```json
{
  "status": "error",
  "gitHygiene": {
    "status": "sensitive-files",
    "branch": {
      "name": "feat/api-integration",
      "valid": true
    },
    "commits": {
      "total": 5,
      "valid": 5,
      "invalid": 0,
      "invalidExamples": []
    },
    "sensitiveFiles": {
      "count": 2,
      "files": [
        ".env.production",
        "src/config/credentials.json"
      ]
    }
  },
  "canProceed": false,
  "details": "Sensitive files detected - must be removed or added to .gitignore"
}
```

## Conventional Commit Format

Valid commit message format:

```
<type>(<scope>): <description>

Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
Scope: optional (component, feature, etc.)
Description: imperative, lowercase, no period

Examples:
✅ feat(auth): add user login endpoint
✅ fix: resolve null pointer in settings
✅ docs(readme): update installation instructions
❌ Updated some files
❌ WIP
❌ Fixed bug
```

## Branch Naming Conventions

Valid patterns:

```
feat/*      - New features
fix/*       - Bug fixes
docs/*      - Documentation
chore/*     - Maintenance
refactor/*  - Code refactoring
test/*      - Test additions
hotfix/*    - Critical fixes
release/*   - Release preparation
claude/*    - AI-generated branches

Examples:
✅ feat/user-authentication
✅ fix/settings-crash
✅ claude/implement-validation-011ABC
❌ update-settings
❌ myfeature
```

## Sensitive File Patterns

Detected patterns:
- `.env`, `.env.local`, `.env.production`
- `credentials.json`, `secrets.json`
- `*.pem`, `*.key`, `*.p12`, `*.pfx`
- `id_rsa`, `.ssh/` files
- Files containing "secret", "private"

## Integration with Conductor

### Phase 2: Branch Validation

```markdown
Use `validate-git-hygiene` to check branch name:
- Expected: feat/*, fix/*, etc.
- If invalid: Warning but continue
```

### Phase 4: Pre-PR Validation

```markdown
Use `validate-git-hygiene` to check:
- Commit messages format
- No sensitive files
- If sensitive files: BLOCK - cannot proceed
```

## Fixing Issues

### Branch Name

```bash
# Rename current branch
git branch -m feat/descriptive-name
```

### Commit Messages

```bash
# Amend last commit message
git commit --amend -m "feat: proper commit message"

# Interactive rebase to fix multiple commits
git rebase -i HEAD~5
```

### Sensitive Files

```bash
# Remove from git (keep local)
git rm --cached .env

# Add to .gitignore
echo ".env*" >> .gitignore
git add .gitignore
git commit -m "chore: add .env to .gitignore"
```

## Related Skills

- `create-feature-branch` - Creates properly named branches
- `commit-with-validation` - Commits with validation
- `security-pentest` - Uses for sensitive file detection

## Best Practices

1. **Use conventional commits** - Enables auto-changelog, semantic versioning
2. **Meaningful branch names** - Self-documenting workflow
3. **Never commit secrets** - Use environment variables
4. **Check before push** - Validate locally first
5. **Use .gitignore** - Prevent accidental commits

## Notes

- Sensitive files BLOCK (canProceed: false)
- Branch/commit format issues are warnings (canProceed: true)
- Checks last 10 commits or since main/develop
- Respects .gitignore for file detection
