---
name: pull-request
description: "Creates comprehensive GitHub Pull Requests with authentication validation and structured documentation. Triggers on keywords: pull request, PR, create PR, open PR"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
  - Write
---

# Pull Request Creator

Creates a comprehensive GitHub Pull Request with authentication validation and structured documentation.

## Usage
```
/pull-request [target_branch] [gh_user]
```

**Arguments**:
- `target_branch`: Base branch for PR (default: `main`)
- `gh_user`: Expected GitHub username (default: `$GH_USER` env var)

**Examples**:
```
/pull-request                    # Uses main, $GH_USER
/pull-request master             # Target master branch
/pull-request main my-username   # Explicit user override
```

---

## Workflow Steps

### Step 1: Authentication Verification (CRITICAL - DO FIRST)

**INSTRUCTION**: Verify GitHub CLI authentication before any other operation.

```bash
ROOT=$(git rev-parse --show-toplevel)
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Get authenticated user
echo "Checking GitHub authentication..."
GH_AUTH_OUTPUT=$(gh auth status 2>&1)
echo "$GH_AUTH_OUTPUT"

# Extract authenticated username
AUTH_USER=$(echo "$GH_AUTH_OUTPUT" | grep -oE "Logged in to github.com account [^ ]+ " | sed 's/Logged in to github.com account //' | tr -d ' ' || echo "")
# Alternative extraction if format differs
if [ -z "$AUTH_USER" ]; then
  AUTH_USER=$(echo "$GH_AUTH_OUTPUT" | grep -oE "account [^(]+" | head -1 | sed 's/account //' | tr -d ' ')
fi

echo "Authenticated as: $AUTH_USER"
```

**Validation Logic**:
1. Extract `AUTH_USER` from `gh auth status` output
2. Determine expected user:
   - If `gh_user` argument provided -> use it
   - Else if `$GH_USER` env var set -> use it
   - Else -> skip user validation (proceed with warning)
3. Compare `AUTH_USER` with expected user
4. **If mismatch**: STOP immediately with error:
   ```
   ERROR: GitHub authentication mismatch
   - Authenticated as: <AUTH_USER>
   - Expected user: <EXPECTED_USER>

   Please run: gh auth login
   Or switch accounts: gh auth switch
   ```
5. **If match**: Proceed with success message

---

### Step 2: Pre-Flight Validation

```bash
# Check not on protected branch
if [ "$BRANCH" = "master" ] || [ "$BRANCH" = "main" ]; then
  echo "ERROR: Cannot create PR from protected branch: $BRANCH"
  exit 1
fi

# Determine target branch
TARGET="${1:-main}"  # Default to main

# Verify target exists on remote
if ! git -C "$ROOT" rev-parse --verify "origin/$TARGET" >/dev/null 2>&1; then
  echo "ERROR: Target branch 'origin/$TARGET' does not exist"
  echo "Available remote branches:"
  git -C "$ROOT" branch -r | grep -v HEAD
  exit 1
fi

# Check for uncommitted changes
if [ -n "$(git -C "$ROOT" status --porcelain)" ]; then
  echo "WARNING: Uncommitted changes detected"
  git -C "$ROOT" status --short
fi
```

---

### Step 3: Context Gathering

#### 3.1 Fetch Latest Target
```bash
echo "Fetching latest $TARGET from origin..."
git -C "$ROOT" fetch origin "$TARGET"
```

#### 3.2 Gather Commit Information
```bash
echo "Commits on this branch (since $TARGET):"
echo "========================================"
git -C "$ROOT" log "origin/$TARGET..HEAD" --oneline
echo ""

COMMITS_AHEAD=$(git -C "$ROOT" rev-list --count "origin/$TARGET..HEAD")
echo "Total commits: $COMMITS_AHEAD"
```

#### 3.3 Gather File Changes
```bash
echo ""
echo "Files changed (summary):"
echo "========================"
git -C "$ROOT" diff "origin/$TARGET...HEAD" --stat
echo ""

echo "Detailed diff:"
echo "=============="
git -C "$ROOT" diff "origin/$TARGET...HEAD"
```

#### 3.4 Check for CHANGELOG
```bash
CWD_FROM_ROOT=${PWD#$ROOT/}

# Search for CHANGELOG files
for changelog in "CHANGELOG.md" "changelog.md" "CHANGES.md"; do
  CHANGELOG_PATH="$CWD_FROM_ROOT/$changelog"
  if git -C "$ROOT" ls-files "$CHANGELOG_PATH" 2>/dev/null | grep -q .; then
    echo ""
    echo "CHANGELOG found: $CHANGELOG_PATH"
    echo "Recent entries:"
    git -C "$ROOT" show "HEAD:$CHANGELOG_PATH" 2>/dev/null | head -80
    break
  fi
done
```

#### 3.5 Check Remote Status
```bash
echo ""
echo "Remote tracking status:"
git -C "$ROOT" status -sb
```

---

### Step 4: Analyze & Draft PR

**INSTRUCTION**: Analyze all gathered context to create a comprehensive PR.

#### 4.1 Analysis Checklist
- [ ] Review all commits since target branch
- [ ] Identify version bumps (CHANGELOG, package.json, pyproject.toml)
- [ ] Identify spec files modified/added
- [ ] Categorize changes by type (features, fixes, refactors, docs)
- [ ] Identify affected components/modules
- [ ] Detect breaking changes
- [ ] Extract ticket/issue references from commit messages or branch name

#### 4.2 PR Title Generation

**Format**: `<type>(<scope>): <concise description>`

**Type Classification** (from changes):
| Type | When to Use |
|------|-------------|
| `feat` | New functionality |
| `fix` | Bug fixes |
| `refactor` | Code restructuring |
| `docs` | Documentation only |
| `test` | Test additions/fixes |
| `chore` | Maintenance tasks |
| `perf` | Performance improvements |

**Scope**: Derive scope from primary modified paths. Use consistent naming (e.g., component/subcomponent). Omit scope if changes span unrelated areas.

#### 4.3 PR Body Template

**CRITICAL**: Use this EXACT structure for the PR body.

```markdown
## Summary

<1-3 sentence overview explaining WHAT this PR does and WHY>

<Bulleted list of key changes/improvements>

### Root Cause (if applicable)
<What problem was being solved - include error traces, user reports, or investigation findings>

### Key Changes
<Detailed breakdown organized by component/area>

**Component 1:**
- Change description with context

**Component 2:**
- Change description with context

## Test Plan

- [ ] <Specific test case 1>
- [ ] <Specific test case 2>
- [ ] Run existing test suite: `pytest <path>`
- [ ] Deploy to staging environment
- [ ] Verify in staging with sample data

## Files Changed

**Category 1 (e.g., Core Logic):**
- `path/to/file.py` - Brief description of changes

**Category 2 (e.g., Configuration):**
- `path/to/config.json` - Brief description of changes

**Category 3 (e.g., Documentation):**
- `path/to/spec.md` - Brief description of changes

## Related

- **Spec**: `path/to/spec.md` (if applicable)
- **Ticket**: [TICKET-123](link) (if applicable)
- **Trace**: `trace-id` (if applicable)
- **Previous PR**: `#123` (if applicable)

Generated with [Claude Code](https://claude.com/claude-code)
```

---

### Step 5: Create Pull Request

#### 5.1 Push Branch if Needed
```bash
# Check if branch needs to be pushed
UPSTREAM=$(git -C "$ROOT" rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null || echo "")

if [ -z "$UPSTREAM" ]; then
  echo "Pushing branch to origin with upstream tracking..."
  git -C "$ROOT" push -u origin "$BRANCH"
else
  # Check if local is ahead of remote
  LOCAL_SHA=$(git -C "$ROOT" rev-parse HEAD)
  REMOTE_SHA=$(git -C "$ROOT" rev-parse "@{upstream}" 2>/dev/null || echo "")

  if [ "$LOCAL_SHA" != "$REMOTE_SHA" ]; then
    echo "Pushing latest commits to origin..."
    git -C "$ROOT" push origin "$BRANCH"
  else
    echo "Branch is up-to-date with remote"
  fi
fi
```

#### 5.2 Create PR with gh CLI

**CRITICAL FORMATTING RULES**:
1. Use HEREDOC for body to preserve multi-line formatting
2. Escape or backtick-wrap `#` characters that could be interpreted as issue references
   - Headers (`## Summary`) are OK - GitHub interprets these correctly
   - Standalone `#123` without context MUST be escaped: `\#123` or wrapped: `` `#123` ``
3. Wrap code paths in backticks to prevent interpretation

```bash
gh pr create \
  --base "$TARGET" \
  --title "<GENERATED_TITLE>" \
  --body "$(cat <<'EOF'
<GENERATED_PR_BODY>
EOF
)"
```

---

### Step 6: Report Results

After PR creation, output:

```
========================================
PR CREATED
========================================

PR URL: <URL from gh pr create>
Branch: <BRANCH> -> <TARGET>
Title: <PR_TITLE>

Summary:
- <Key point 1>
- <Key point 2>
- <Key point 3>

Files included: <N> files changed

Next steps:
1. Review PR: <URL>
2. Request reviewers if needed: gh pr edit --add-reviewer <user>
3. Monitor CI checks
========================================
```

---

## Design Decisions

1. **Authentication-First Approach**
   - Validates GitHub auth BEFORE any other operation
   - Prevents wasted effort if credentials are wrong
   - Supports both argument override and env var default

2. **Default to `main` (not `master`)**
   - Modern GitHub default is `main`
   - Override available via argument for legacy repos

3. **HEREDOC for PR Body**
   - Preserves markdown formatting correctly
   - Handles multi-line content without escaping issues
   - Single-quoted `'EOF'` prevents variable expansion in body

4. **Comprehensive Context Gathering**
   - Analyzes full diff, not just commit messages
   - Checks CHANGELOG for version context
   - Reviews specs for documentation links

5. **Structured PR Template**
   - Consistent format for all PRs
   - Sections optimized for reviewer experience
   - Test plan with actionable checkboxes

6. **Claude Code Attribution**
   - Footer indicates AI-assisted PR creation
   - Links to Claude Code for transparency

---

## Edge Cases

### No Commits Ahead of Target
```
WARNING: No commits ahead of $TARGET
Branch may already be merged or rebased.
```
Prompt user to verify before proceeding.

### Branch Already Has Open PR
Check with `gh pr list --head $BRANCH` and warn if PR exists:
```
WARNING: Open PR already exists for this branch
PR #123: <title>
URL: <url>

Would you like to update the existing PR instead?
```

### Target Branch Not Found
```
ERROR: Target branch 'origin/$TARGET' not found
Available branches:
- origin/main
- origin/master
- origin/develop

Please specify correct target: /pull-request <branch>
```

---

## Safety Checks Summary

- Verify GitHub authentication matches expected user
- Confirm not on protected branch
- Verify target branch exists
- Check for uncommitted changes (warn, don't block)
- Push branch before PR creation
- Use HEREDOC for safe body formatting
