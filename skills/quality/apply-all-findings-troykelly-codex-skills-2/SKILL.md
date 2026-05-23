---
name: apply-all-findings
description: Use after code review - implement ALL findings; any finding not fixed MUST have tracking issue created; no finding disappears without trace
---

# Apply All Findings

## Overview

Address EVERY finding from code review. Findings are either FIXED or DEFERRED with tracking issues.

**Core principle:** Minor issues accumulate into major problems.

**The rule:** If it was worth noting, it's worth tracking.

**ABSOLUTE REQUIREMENT:** Every finding results in ONE of:
1. **Fixed in this PR** (verified)
2. **Tracking issue created** (linked in review artifact)

There is NO third option. "Won't fix without tracking" is NOT permitted.

## Why All Findings

### Minor Issues Compound

```
1 unclear variable name +
1 missing null check +
1 inconsistent style +
1 outdated comment =
Confusing, fragile code
```

### Selective Fixing Creates Precedent

```
"This minor issue can wait" →
"That minor issue can wait too" →
"We don't fix minor issues" →
Technical debt mountain
```

### Thoroughness Builds Quality Culture

```
Every finding addressed →
High standards maintained →
Quality becomes habit
```

## The Process

### Step 1: Gather All Findings

From `comprehensive-review`, you have:

```markdown
### Findings

1. [Critical] SQL injection in findUser()
2. [Major] N+1 query in getOrders()
3. [Minor] Variable 'x' should be renamed
4. [Minor] Missing JSDoc on helper()
5. [Minor] Inconsistent quote style
```

### Step 2: Create Checklist

Every finding becomes a todo:

```markdown
- [ ] Fix SQL injection in findUser()
- [ ] Fix N+1 query in getOrders()
- [ ] Rename variable 'x' to descriptive name
- [ ] Add JSDoc to helper()
- [ ] Fix quote style to use single quotes
```

### Step 3: Address Systematically

Work through the list. For each finding:

#### If Fixable:

1. Fix the issue
2. Verify the fix
3. Check off the item
4. Move to next finding

#### If Not Fixable in This PR:

1. Verify valid deferral reason (see `deferred-finding` skill)
2. Create tracking issue with full documentation
3. Add tracking issue to review artifact
4. Mark as DEFERRED (not unaddressed)
5. Move to next finding

```bash
# Create tracking issue for deferred finding
gh issue create \
  --title "[Finding] [Description] (from #123)" \
  --label "review-finding,depth:1" \
  --body "[Full deferred-finding template]"

# Create spawned-from label if needed
gh label create "spawned-from:#123" --color "C2E0C6" 2>/dev/null || true
gh issue edit [NEW_ISSUE] --add-label "spawned-from:#123"
```

### Step 4: Verify All Complete

Before considering done:

```bash
# Re-run linting
pnpm lint

# Re-run tests
pnpm test

# Re-run type check
pnpm typecheck
```

All checks must pass.

### Step 5: Update Review Artifact

After all findings addressed, update artifact in issue comment:

1. All FIXED findings marked ✅ FIXED
2. All DEFERRED findings have tracking issue # linked
3. "Unaddressed: 0" in summary
4. "Review Status: COMPLETE"

## Addressing by Type

### Critical/Major Findings

These require code changes:

```typescript
// Finding: SQL injection in findUser()
// Before
return db.query(`SELECT * FROM users WHERE username = '${username}'`);

// After
return db.query('SELECT * FROM users WHERE username = ?', [username]);
```

### Minor: Naming

```typescript
// Finding: Variable 'x' should be renamed
// Before
const x = users.filter(u => u.active);

// After
const activeUsers = users.filter(user => user.isActive);
```

### Minor: Documentation

```typescript
// Finding: Missing JSDoc on helper()
// Before
function helper(data: Data): Result {

// After
/**
 * Transforms raw data into the expected result format.
 *
 * @param data - Raw data from the API
 * @returns Transformed result ready for display
 */
function helper(data: Data): Result {
```

### Minor: Style

```typescript
// Finding: Inconsistent quote style
// Before
const name = "Alice";
const greeting = 'Hello';

// After (using project standard: single quotes)
const name = 'Alice';
const greeting = 'Hello';
```

## Handling Deferrals

### Valid Deferral Reasons

| Reason | Example | Requires |
|--------|---------|----------|
| Out of scope | Architectural change | Tracking issue |
| External dependency | Infrastructure change | Tracking issue |
| Breaking change | Major version bump | Tracking issue |
| Separate concern | Independent feature | Tracking issue |

### NOT Valid Deferral Reasons

| Excuse | Reality | Action |
|--------|---------|--------|
| "It's minor" | Minor compounds | Fix now |
| "Takes too long" | Debt takes longer | Fix now |
| "Good enough" | Never enough | Fix now |
| "Not important" | Then why note it? | Fix now |
| "Do it later" | Without tracking? No. | Fix or create issue |

### Deferral MUST Create Issue

**ABSOLUTE:** No deferral without tracking issue.

```bash
# WRONG - Deferred without tracking
"We'll fix the SQL injection later"  # NO

# RIGHT - Deferred with tracking
gh issue create --title "[Finding] SQL injection in findUser (from #123)" ...
# Then link #456 in review artifact
```

## Verification

After addressing all findings:

### Run All Checks

```bash
# Linting
pnpm lint

# Type checking
pnpm typecheck

# Tests
pnpm test

# Build
pnpm build
```

### Review the Diff

```bash
git diff
```

Verify:
- All findings addressed
- No unrelated changes
- Tests updated if behavior changed

### Self-Review Again

Quick pass through 7 criteria to ensure fixes didn't introduce new issues.

## Checklist

Before moving on from review:

- [ ] All critical findings addressed
- [ ] All major findings addressed
- [ ] All minor findings addressed
- [ ] Any deferred finding has tracking issue created
- [ ] Tracking issues linked in review artifact
- [ ] All automated checks pass
- [ ] Fixes reviewed for correctness
- [ ] No new issues introduced
- [ ] Review artifact updated with final status
- [ ] "Unaddressed: 0" confirmed

## Common Pushback (Rejected)

| Pushback | Response |
|----------|----------|
| "We can fix minors later" | Without tracking? No. Create issue or fix now. |
| "This is slowing us down" | Debt slows you down more. |
| "It's not important" | Then why was it noted? |
| "Good enough" | Good enough is never enough. |
| "The reviewer is being picky" | Attention to detail is valuable. |

## Integration

This skill is called by:
- `issue-driven-development` - Step 10

This skill follows:
- `comprehensive-review` - Generates the findings

This skill uses:
- `deferred-finding` - For creating tracking issues

This skill ensures:
- No accumulated minor issues
- Consistent quality standards
- Complete reviews, not partial
- All deferrals tracked in GitHub
