---
name: ship-it
description: Prepare current branch for production deployment (Test, Lint, Build, PR).
disable-model-invocation: true
---

# Ship It Workflow

Execute this sequence to get code ready for production. **Stop if ANY step fails.**

# Required Agents

- **MANDATORY:** `@qa-engineer` - Runs tests
- **MANDATORY:** `@security-auditor` - Security scan
- `@tech-lead` - (Optional) Final architecture review

# Pre-Flight Checks

## Check 1: Git Status

```bash
git status
```

**Error Handling:**
- If not a git repo: "❌ Not a git repository. Cannot ship."
- If no changes: "❌ No changes to ship. Branch is clean."
- If uncommitted changes: Warn and ask to commit first

## Check 2: Branch Name

```bash
git branch --show-current
```

**Error Handling:**
- If on `main`/`master`: "❌ Cannot ship from main branch. Create a feature branch."
- Suggest: `git checkout -b feature/[name]`

## Check 3: Remote Configured

```bash
git remote -v
```

**Error Handling:**
- If no remote: "⚠️ No remote configured. Add one with: git remote add origin [url]"

# Execution Pipeline

## Step 1: Polish Code

Run `/polish` skill first:
```
/polish
```

**Error Handling:**
- If polish fails: Ask "Continue anyway? (Yes/No)"
- If No: Abort

## Step 2: Lint & Type Check

**JavaScript/TypeScript:**
```bash
# ESLint
if npm list eslint >/dev/null 2>&1; then
  echo "Running ESLint..."
  npx eslint . --max-warnings 0
fi

# TypeScript
if [ -f "tsconfig.json" ]; then
  echo "Running TypeScript compiler..."
  npx tsc --noEmit
fi
```

**Python:**
```bash
# Ruff
if command -v ruff >/dev/null 2>&1; then
  echo "Running Ruff..."
  ruff check .
fi

# MyPy
if command -v mypy >/dev/null 2>&1; then
  echo "Running MyPy..."
  mypy .
fi
```

**Error Handling:**
- If lint fails:
  ```
  ❌ Lint Failed
  
  Errors:
  [Show errors]
  
  Options:
  1. Fix manually
  2. Run /polish to auto-fix
  3. Skip lint (not recommended)
  
  Your choice?
  ```
- If type check fails: STOP and show errors

## Step 3: Run Tests

**Call `@qa-engineer`:**
```
@qa-engineer Run tests for changed files in current branch
```

**Test Commands:**
```bash
# JavaScript/TypeScript
if [ -f "package.json" ]; then
  if grep -q '"test"' package.json; then
    npm test
  fi
fi

# Python
if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
  pytest
fi
```

**Error Handling:**
- If tests fail:
  ```
  ❌ Tests Failed
  
  Failed Tests:
  [Show failures]
  
  🚫 DEPLOYMENT BLOCKED
  
  Fix tests before shipping.
  ```
  - STOP execution
  - Exit

- If no tests exist:
  ```
  ⚠️ No tests found!
  
  Proceed without tests? (Yes/No)
  ```
  - If No: STOP

## Step 4: Security Audit

**Call `@security-auditor`:**
```
@security-auditor Scan changed files for security vulnerabilities
```

**Security Checks:**
1. Hardcoded secrets (API keys, passwords)
2. SQL injection risks
3. XSS vulnerabilities
4. CSRF protection
5. Authentication/authorization issues

**Error Handling:**
- If CRITICAL issues found:
  ```
  🚨 CRITICAL SECURITY ISSUES
  
  [Show issues]
  
  🚫 DEPLOYMENT BLOCKED
  
  Fix security issues before shipping.
  ```
  - STOP execution
  - Exit

- If HIGH/MEDIUM issues:
  ```
  ⚠️ Security Warnings
  
  [Show issues]
  
  Proceed anyway? (Yes/No)
  ```

## Step 5: Build Check

**JavaScript/TypeScript:**
```bash
if grep -q '"build"' package.json; then
  echo "Running build..."
  npm run build
fi
```

**Python:**
```bash
# Check if package can be built
if [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
  python -m build --check
fi
```

**Error Handling:**
- If build fails:
  ```
  ❌ Build Failed
  
  Errors:
  [Show build errors]
  
  🚫 DEPLOYMENT BLOCKED
  
  Fix build errors before shipping.
  ```
  - STOP execution

## Step 6: Generate Summary

Create concise summary of changes:

```bash
# Get changed files
git diff --name-only main...HEAD

# Get commit messages
git log main...HEAD --oneline

# Generate summary
[Analyze commits and files to create human-readable summary]
```

**Summary Format:**
```
## Changes

### Features
- Added user profile editing
- Implemented email notifications

### Fixes
- Fixed login redirect issue
- Resolved database connection timeout

### Technical
- Refactored auth middleware
- Updated dependencies

### Tests
- Added 12 new tests
- All tests passing
```

## Step 7: Create Pull Request

**Check if `gh` CLI is available:**
```bash
if command -v gh >/dev/null 2>&1; then
  # Use GitHub CLI
  gh pr create --title "[Title]" --body "[Summary]"
else
  # Provide manual instructions
  echo "Push branch and create PR manually"
fi
```

**PR Title:** Auto-generate from branch name or commits
- Example: `feature/user-profile` → "Feature: User Profile"

**PR Body:** Use generated summary

**Error Handling:**
- If `gh` not installed:
  ```
  ℹ️ GitHub CLI not found
  
  Manual Steps:
  1. Push branch: git push origin [branch-name]
  2. Create PR at: [GitHub URL]
  
  Copy this as PR description:
  [Summary]
  ```

- If PR creation fails:
  ```
  ❌ Failed to create PR
  
  Error: [Error message]
  
  Push manually:
  git push origin [branch-name]
  
  Then create PR on GitHub.
  ```

## Step 8: Final Checks

**Success:**
```
🚀 Ready to Ship!

✅ Checklist:
- [x] Code polished
- [x] Lint passed
- [x] Type check passed
- [x] 15/15 tests passed
- [x] Security scan: No issues
- [x] Build successful
- [x] PR created: #123

🔗 PR Link: [URL]

➡️ Next Steps:
1. Request review from team
2. Address feedback
3. Merge when approved
4. Deploy to production

🎉 Ready to merge!
```

**With Warnings:**
```
⚠️ Ready to Ship (with warnings)

✅ Checklist:
- [x] Code polished
- [x] Lint passed
- [x] Type check passed
- [x] 15/15 tests passed
- [ ] Security scan: 2 medium issues
- [x] Build successful
- [x] PR created: #123

⚠️ Warnings:
- Security: 2 medium issues (review recommended)

🔗 PR Link: [URL]

➡️ Action Required:
Review security warnings before merging.
```

# Error Recovery

**If any step fails:**
1. Stop execution
2. Show error details
3. Suggest fixes
4. Offer to retry after fixes

**Recovery Options:**
```
❌ Ship Failed at: [Step Name]

Options:
1. Fix the issue manually
2. Skip this step (not recommended)
3. Abort and try later

Your choice?
```

# Success Criteria

- [ ] All lint checks passed
- [ ] All type checks passed
- [ ] All tests passed
- [ ] Security scan completed (no critical issues)
- [ ] Build successful
- [ ] PR created
- [ ] Summary provided
- [ ] User knows next steps
