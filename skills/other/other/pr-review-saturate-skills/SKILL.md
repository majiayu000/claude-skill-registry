---
name: pr-review
description: Performs comprehensive code reviews checking for bugs, security issues, performance problems, testing gaps, and code quality. Accepts branch names or PR URLs (GitHub/Azure DevOps) to automatically checkout and review. Use when reviewing PRs, pull requests, code changes, commits, diffs, or when asked to review code, check code, audit changes, review my changes, check PR, review branch, or perform code review.
compatibility: Basic tools - grep, file reading. Optional: gh CLI for GitHub PRs, az CLI for Azure DevOps PRs
allowed-tools: Read Grep Glob Bash
argument-hint: "[branch-name or PR URL]"
metadata:
  author: Saturate
  version: "2.0"
---

# Code Review

Review code like a senior engineer - thorough but practical. Focus on things that actually matter. Don't waste time on style nitpicks a linter should catch.

## Arguments

The skill accepts optional arguments to determine what to review:

**No arguments:** Ask user if they want to review the current branch

**Branch name:** Checkout the branch and review it
- Example: `/pr-review feat/redirect`
- Example: `/pr-review feature/add-auth`

**PR URL:** Supports GitHub and Azure DevOps PR URLs
- Example: `/pr-review https://github.com/owner/repo/pull/123`
- Example: `/pr-review https://dev.azure.com/org/project/_git/repo/pullrequest/456`
- Platform-specific integration details are in reference files (loaded only when needed)

## Step 0: Read Project Guidelines

**Before reviewing code, read project-specific guidelines:**

1. Check for `CLAUDE.md` in the repository root
2. Check for global guidelines at `~/.claude/CLAUDE.md`
3. Extract key rules to check during review:
   - Type safety requirements (no casts, no `any`, etc.)
   - Testing requirements
   - Code style preferences
   - Backward compatibility rules

**Common patterns to extract:**
```text
# Look for type safety rules
grep -i "never cast\|no any\|no type assertion" CLAUDE.md ~/.claude/CLAUDE.md

# Look for testing requirements
grep -i "test\|coverage" CLAUDE.md ~/.claude/CLAUDE.md

# Look for git/commit rules
grep -i "commit\|backward compat" CLAUDE.md ~/.claude/CLAUDE.md
```

If no CLAUDE.md exists, proceed with general best practices only.

## Step 1: Determine What to Review

**Before any checkout, save current state:**
```text
original_branch=$(git branch --show-current)
git stash push -m "pr-review: temporary stash" 2>/dev/null && stashed=true || stashed=false
```

**If no arguments provided:**
1. Check current git branch: `git branch --show-current`
2. Ask user: "Review current branch `{branch-name}`?" (Yes/No)
3. If No, ask: "Which branch or PR URL should I review?"
4. Proceed based on response

**If arguments provided:**

**1. Detect if URL:**
```text
if [[ "$args" =~ ^https?:// ]]; then
  # It's a URL, determine platform
  if [[ "$args" =~ github\.com ]]; then
    # GitHub PR detected - READ references/github-pr-integration.md for implementation
    # Follow the complete workflow in that file to:
    # - Extract owner, repo, PR number from URL
    # - Use gh CLI to get branch name
    # - Checkout branch for review
  elif [[ "$args" =~ dev\.azure\.com|visualstudio\.com ]]; then
    # Azure DevOps PR detected - READ references/azure-pr-integration.md for implementation
    # Follow the complete workflow in that file to:
    # - Extract org, project, repo, PR number from URL
    # - Use az CLI to get branch name
    # - Checkout branch for review
  else
    echo "❌ Unsupported PR URL. Supports GitHub and Azure DevOps only."
    exit 1
  fi
fi
```

**2. If not URL, treat as branch name:**
```text
# Fetch latest changes
git fetch origin

# Checkout branch
if git rev-parse --verify "$args" &> /dev/null; then
  git checkout "$args"
  git pull origin "$args"
else
  git checkout -b "$args" "origin/$args" 2>/dev/null || {
    echo "❌ Branch '$args' not found locally or on remote"
    exit 1
  }
fi
```

**3. Verify we're on a branch (not detached HEAD):**
```text
current_branch=$(git branch --show-current)
if [ -z "$current_branch" ]; then
  echo "❌ Detached HEAD state - cannot review"
  exit 1
fi
```

## Step 2: Scope the Review to the Diff

**After checkout, get exactly what changed — this is your review target, not the whole codebase:**

```text
# Detect base branch
base=$(git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}')
base=${base:-main}

# Get the full diff
git diff "origin/$base...HEAD"

# Get changed file list (use this to decide which files to read)
git diff --name-only "origin/$base...HEAD"

# Understand the commit history
git log "origin/$base...HEAD" --oneline
```

**Only read and review files that appear in `git diff --name-only`.** Do not explore the full codebase. Check the diff first to understand what changed, then read specific files only when you need more context than the diff provides (e.g. to understand how a changed function is called).

## Review Checklist

Use this checklist to guide your review. Need examples of what to look for? Check out [references/common-issues.md](references/common-issues.md) for code patterns.

### PR Quality (Review First)
- [ ] Title is clear and descriptive (not "fix bug" or "update code")
- [ ] Description explains WHY, not just WHAT
- [ ] Complex changes have explanation or context
- [ ] Visual changes include screenshots/recordings
- [ ] Breaking changes are clearly marked
- [ ] Related issues/tickets are linked (GitHub) or work items linked (Azure DevOps)
- [ ] Work items are appropriate for the changes (Azure DevOps)
- [ ] Description helps reviewers understand impact
- [ ] PR size is reasonable — flag if >500 lines changed, suggest splitting if it mixes unrelated concerns

### Security (Critical)
- [ ] Input validation and sanitization
- [ ] SQL injection, XSS, command injection risks
- [ ] Auth checks in place and correct
- [ ] Sensitive data handling (passwords, tokens, PII)
- [ ] Dependency vulnerabilities

### Bugs & Logic (Critical)
- [ ] Null/undefined handling
- [ ] Edge cases (empty arrays, null values, boundaries)
- [ ] Error handling in place
- [ ] Race conditions or concurrency issues
- [ ] State management issues

### Performance (Important)
- [ ] Algorithm complexity (watch for O(n²) where O(n) exists)
- [ ] N+1 query problems
- [ ] Memory leaks (listeners, subscriptions, closures)
- [ ] Blocking operations that should be async

### Testing (Important)
- [ ] Changes covered by tests
- [ ] Tests verify actual behavior
- [ ] Edge cases tested
- [ ] Error conditions tested

### Code Quality
- [ ] Code is understandable
- [ ] No unnecessary complexity or clever code
- [ ] Duplication worth extracting
- [ ] Names match what they do
- [ ] **Follows project guidelines in CLAUDE.md (if present)**
- [ ] **No type casts or non-null assertions - use type narrowing instead**
- [ ] No "any" types - use proper types or "unknown" with narrowing

### Accessibility (Important — UI changes only)
- [ ] Interactive elements are keyboard accessible (focusable, operable without mouse)
- [ ] Images have meaningful alt text (or `alt=""` if decorative)
- [ ] Color is not the only way information is conveyed
- [ ] Form inputs have associated labels
- [ ] Focus is managed correctly after dynamic content changes (modals, toasts, route changes)
- [ ] ARIA attributes are used correctly — prefer semantic HTML over ARIA when possible

### Dependencies (Important — if packages were added or updated)
- [ ] New packages are justified — is there a simpler built-in alternative?
- [ ] Package is actively maintained and not abandoned
- [ ] No known security vulnerabilities (`npm audit` / `dotnet list package --vulnerable`)
- [ ] Bundle size impact is acceptable for frontend packages

> For a deeper dependency evaluation, invoke the `evaluating-dependencies` skill on any new packages added in this PR.

### Architecture
- [ ] Fits existing patterns (or has good reason not to)
- [ ] No breaking changes without migration
- [ ] Avoids unnecessary coupling
- [ ] Database migrations are safe: non-destructive, backwards-compatible while old code may still run (avoid column renames/drops without a transition period, ensure nullable or defaulted new columns)

## Step 3: Restore Original State

After completing the review, return to where the user was:

```text
git checkout "$original_branch"
[ "$stashed" = "true" ] && git stash pop
```

## Output Format

Structure your review like this (see [references/review-template.md](references/review-template.md) for detailed examples):

- **Summary:** One line verdict (Good to merge / Has issues / Needs work)
- **PR Quality:** Evaluate title, description, screenshots (review this first)
- **Critical:** Security, data loss, crashes - must fix before merge
- **Important:** Bugs, performance, missing tests - should fix
- **Minor:** Quality improvements - nice to have
- **Questions:** Things to clarify with the author
- **Prevent This:** Suggest tooling/config to catch these issues automatically in the future
- **Positive Notes:** Briefly acknowledge what's done well

## Guidelines

- **Check CLAUDE.md first** - Read project guidelines before reviewing code
- Be specific: file:line, what's wrong, why it matters, how to fix
- Skip style issues that linters catch
- Explain impact, not just "this is wrong"
- Consider trade-offs - sometimes simple is better than perfect
- Briefly note if something is done well, but keep it short
- **Flag project guideline violations as Important or Critical**

### Checking Project Guidelines

**How to flag guideline violations:**
```markdown
### Important

**3. Type cast violates CLAUDE.md guideline**
**File:** `app.vue:28`
**Guideline:** "Never cast types - always narrow them"
**Current:**
\`\`\`typescript
const redirect = content.entry.item as IRedirect
\`\`\`
**Issue:** Type assertion bypasses TypeScript safety checks
**Fix:** Use discriminated union or type guard
```

### Evaluating PR Quality

**Title:**
- ❌ Bad: "fix", "update", "changes", "wip"
- ✅ Good: "Fix OAuth redirect loop in Safari", "Add rate limiting to auth endpoints"

**Description:**
- Should explain WHY, not just list what changed (diff shows that)
- Complex logic needs context: "Chose X over Y because..."
- Breaking changes must be highlighted
- For UI changes: screenshots/videos are expected
- Link related issues (GitHub): "Fixes #123", "Related to #456"
- Link work items (Azure DevOps): Should have appropriate work items linked

**Work Items (Azure DevOps only):**
- PRs should link to relevant work items (User Stories, Bugs, Tasks)
- Bug fixes → should link to Bug work item
- Features → should link to User Story or Feature work item
- No work items linked → ask if one should be created/linked
- Wrong work item type → suggest appropriate type

**When to ask for improvements:**
- Title is vague or uninformative
- No description on non-trivial changes
- UI changes without screenshots
- Breaking changes not called out
- Missing context on non-obvious decisions
- No work items linked (Azure DevOps) when they should be

**Example feedback:**
```
## PR Quality

**Title:** ⚠️ Too generic. Consider: "Fix race condition in payment processing"

**Description:** ❌ Missing context. Why did we switch from polling to SSE? What problem did it solve? Add:
- What was broken/slow before
- Why this approach vs alternatives
- Performance impact (if relevant)

**Screenshots:** ❌ This changes the checkout UI but has no screenshots. Add before/after screenshots.
```

### Suggesting Future Mitigations

Only suggest mitigations for recurring patterns or critical issues. Don't suggest tools for one-off mistakes. Focus on automatable checks, not process changes.

**TypeScript configuration:**
- Type safety issues (`any`, implicit types) → Suggest `strict: true`, `noImplicitAny`, `strictNullChecks` in tsconfig.json
- Missing null checks → Suggest `strictNullChecks: true`

**Linting rules:**
- Code quality patterns ESLint could catch → Suggest specific ESLint rules
- Framework-specific issues → Suggest framework ESLint plugins (react-hooks, vue, etc.)
- Formatting inconsistencies → Suggest Prettier in pre-commit hook

**Pre-commit hooks:**
- Secrets/credentials committed → Suggest trufflehog or git-secrets
- Test failures → Suggest running tests before commit
- Type errors → Suggest tsc --noEmit check

**CI/CD checks:**
- Security vulnerabilities → Suggest npm audit / dependency scanning
- Missing tests → Suggest coverage thresholds
- Build errors → Ensure build runs in CI

## References

Need more guidance? Check these out:

- **[Review Template](references/review-template.md)** - What your review output should look like, with severity categories and example issues
- **[Common Issues](references/common-issues.md)** - Quick reference of problems that come up often in reviews, with good/bad code examples
