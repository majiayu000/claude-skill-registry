---
name: improve-pr
description: Comprehensive PR analysis with security review, code quality assessment, and automatic improvements. Use when reviewing PRs for security issues, performance optimizations, or best practices violations. Provides multi-dimensional analysis with safe auto-apply options.
allowed-tools: Bash(gh:*), Bash(git:*), Edit, Write, Read
---

# Improve PR Skill

Performs comprehensive PR analysis combining security review, best practices assessment, and actionable code improvements with auto-apply capability.

## Usage

```
/improve-pr <pr-number>
```

## Workflow

### Step 1: Fetch PR and Checkout Branch

```bash
# Get PR details
PR_INFO=$(gh pr view $ARGUMENTS --json headRefName,baseRefName,files,title,additions,deletions)
HEAD_BRANCH=$(echo $PR_INFO | jq -r '.headRefName')

# Checkout the PR branch
git fetch origin
git checkout $HEAD_BRANCH
git pull origin $HEAD_BRANCH

# Get the diff
gh pr diff $ARGUMENTS

# Get PR checks status
gh pr checks $ARGUMENTS
```

### Step 2: Comprehensive Analysis

Analyze the code across multiple dimensions:

**🔒 Security Analysis**:
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- Authentication/authorization issues
- Secrets in code (API keys, passwords)
- Insecure dependencies
- CSRF protection
- Input validation
- Cryptography weaknesses

**🎨 Code Quality**:
- Extract duplicate code into functions
- Simplify complex conditionals
- Improve variable/function naming
- Add error handling
- Reduce nesting depth
- Apply SOLID principles

**⚡ Performance**:
- Optimize algorithms
- Reduce database queries (N+1 issues)
- Add caching where appropriate
- Lazy load resources
- Parallel processing opportunities

**📖 Readability**:
- Add clarifying comments
- Break down large functions
- Improve code organization
- Use descriptive names

**✨ Best Practices**:
- Follow language idioms
- Use modern syntax
- Apply design patterns
- Follow project conventions

**🧪 Testing Coverage**:
- Missing unit tests
- Untested edge cases
- Error handling tests

### Step 3: Generate Report

See `references/report-template.md` for full template.

Key sections:
- Overview (files, lines, quality rating)
- Security analysis (strengths, issues, warnings)
- Code quality improvements by category
- File-by-file improvements with before/after
- Implementation priority (Critical → Low)
- Testing coverage gaps
- Impact summary

### Step 4: Auto-Apply Options

Present options to user:
- **A)** Apply critical fixes + high priority improvements
- **B)** Apply high priority only (safer)
- **C)** Apply specific improvements (user chooses)
- **D)** Show changes first (don't apply)
- **E)** Post as PR comment for team review

### Step 5: Apply Changes (if selected)

```bash
# For each improvement:
# 1. Use Edit tool to apply the change
# 2. Verify syntax is correct
# 3. Track what was changed

# After all changes:
git add .
git commit -m "🚀 improve: apply AI-suggested improvements

Security fixes:
- [list security fixes]

Code quality:
- [list improvements]

Applied [count] improvements across [count] files."

git push origin $HEAD_BRANCH
```

### Step 6: Verification

```bash
# Run any available tests
if [ -f "package.json" ]; then npm test; fi
if [ -f "pytest.ini" ]; then pytest; fi
if [ -f "Makefile" ]; then make test; fi

# Verify no regressions
git diff --stat
```

## Safety Rules

Before applying ANY improvement:
1. ✅ Verify syntax is valid
2. ✅ Ensure tests still pass (if available)
3. ✅ Preserve original functionality
4. ✅ Check no breaking changes introduced
5. ✅ Validate code compiles/runs
6. ✅ **NEVER auto-apply critical security fixes** - flag for manual review

## Security Priority

**CRITICAL**: Security issues require special handling:
- SQL Injection → **FLAG, don't auto-fix** (needs validation)
- Hardcoded secrets → **FLAG, don't auto-fix** (needs secret rotation)
- XSS vulnerabilities → **FLAG, don't auto-fix** (needs testing)
- Auth issues → **FLAG, don't auto-fix** (needs security review)

For security fixes, provide the fix but **require manual review and application**.

## Output Guidelines

**Be Specific**:
- Include exact line numbers
- Show before/after code
- Explain security impact
- Provide CVE references if applicable

**Be Practical**:
- Focus on high-impact changes
- Consider implementation effort
- Prioritize security over style

**Be Safe**:
- Don't break existing functionality
- Maintain backward compatibility
- Preserve test coverage
- Flag security issues for review

## Priority Levels

| Priority | Icon | Description |
|----------|------|-------------|
| Critical | 🔴 | MUST fix before merge (security vulnerabilities) |
| High | 🟡 | Should implement now (significant improvements) |
| Medium | 🟢 | Consider for this PR (good enhancements) |
| Low | ⚪ | Future enhancement (nice-to-have) |

**Remember**: Security first, quality second, style third. Critical security issues must be flagged but not auto-applied without review.
