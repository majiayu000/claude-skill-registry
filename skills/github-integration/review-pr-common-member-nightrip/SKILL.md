---
name: review-pr
description: Review the current PR's changes for code quality, security, and Rails best practices. Ideal for triggering a thorough review from GitHub Mobile.
disable-model-invocation: true
argument-hint: "[pr-number or leave empty for current branch]"
---

# PR Code Review

**Target:** $ARGUMENTS

Perform a thorough code review of the PR changes. Follow each step below.

---

## Step 1: Identify the PR

If a PR number was provided, fetch its details:
```bash
gh pr view $ARGUMENTS
gh pr diff $ARGUMENTS
```

If no argument given, review the current branch's uncommitted or recently committed changes:
```bash
git log main..HEAD --oneline
git diff main..HEAD
```

List files changed:
```bash
gh pr view $ARGUMENTS --json files --jq '.files[].path' 2>/dev/null || git diff main..HEAD --name-only
```

---

## Step 2: Read the Changed Files

For each changed file, read the full file (not just the diff) to understand context:
- Models → check validations, associations, business logic
- Controllers → check authentication, authorization, strong params
- Views → check for XSS, user data rendering, Turbo integration
- Migrations → check data integrity, indexes, reversibility
- Specs → check coverage, edge cases, factory usage

---

## Step 3: Review Against Checklist

### Rails Best Practices
- [ ] Controllers are thin (business logic in models)
- [ ] `before_action :authenticate_user!` on all sensitive actions
- [ ] Strong parameters used (`permit` with explicit fields)
- [ ] Scopes and class methods used instead of complex queries in controllers
- [ ] Geocoder triggered via `after_validation :geocode` (not in controllers)
- [ ] Turbo Streams used for real-time updates (not custom AJAX)

### Code Quality
- [ ] Methods are short and focused (single responsibility)
- [ ] No duplication — DRY where it makes sense
- [ ] Variable/method names are clear and descriptive
- [ ] No dead code or unused variables

### Testing (SDD)
- [ ] New features have corresponding specs in `spec/`
- [ ] Specs cover happy path AND error cases
- [ ] Factories used (not fixtures), from `spec/factories/`
- [ ] System specs cover user-facing flows

### Security
- [ ] No secrets hardcoded in source code
- [ ] No `html_safe` or `raw` on user input without sanitization
- [ ] No SQL string interpolation (use placeholders)
- [ ] Authorization: users can only access their own resources

---

## Step 4: Run Automated Checks

```bash
# Security scan (if code was checked out)
bin/brakeman --no-pager 2>/dev/null || echo "Brakeman not available in this context"
```

---

## Step 5: Write Review Summary

Structure the feedback as:

**Summary**
One paragraph describing what the PR does and overall assessment.

**Issues Found** (if any)
- 🔴 **MUST FIX** — Critical bugs or security issues
- 🟡 **SHOULD FIX** — Code quality or convention issues
- 🟢 **CONSIDER** — Minor improvements or suggestions

**Looks Good**
Highlight what's done well.

**Verdict**
- ✅ Approved — ready to merge
- ⚠️ Needs changes — address issues above before merging
