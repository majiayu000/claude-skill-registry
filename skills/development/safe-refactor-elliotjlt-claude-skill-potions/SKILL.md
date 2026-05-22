---
name: safe-refactor
description: |
  When refactoring, rewriting, or migrating critical code paths, orchestrate a
  safe cycle: assess risks → implement → verify → document. Chains pre-mortem
  and prove-it with built-in implementation phase. Prevents "refactor broke
  production" disasters. Activates on "refactor", "rewrite", "migrate", or
  "clean up" for non-trivial code.
allowed-tools: |
  bash: git, grep, find, npm, pytest, jest
  file: read, write
---

# Safe Refactor

<purpose>
An elixir for risky code changes. Refactors feel safe ("I'm just cleaning up")
but they're where bugs hide. This chains risk assessment → careful implementation
→ verification → documentation. The ceremony slows you down just enough to
catch problems before production does.
</purpose>

## Prerequisites

This elixir works best with these skills installed:

| Skill | Purpose | If Missing |
|-------|---------|------------|
| pre-mortem | Risk assessment before starting | Falls back to built-in checklist |
| prove-it | Verification enforcement | Falls back to built-in verification |
| retrospective | Document learnings | Skipped (optional phase) |

## When To Activate

<triggers>
- "Refactor this"
- "Clean up this code"
- "Rewrite this to be more..."
- "Migrate from X to Y"
- "Replace this implementation"
- Large-scale find-and-replace
- Changing shared utilities or core abstractions
- Touching code you didn't write
</triggers>

## Instructions

### Phase 1: Assess Risk

<phase_risk>
**If pre-mortem skill installed:** Invoke it now.

**If not installed, evaluate:**

```markdown
## Refactor Risk Assessment

**What's changing:**
- [ ] Files affected: [list them]
- [ ] Functions/classes modified: [list them]
- [ ] Estimated lines changed: [number]

**Risk factors:**
- [ ] Touches shared/core code (used by multiple features)
- [ ] Affects data persistence (database, files, cache)
- [ ] Changes public API/interfaces
- [ ] Lacks test coverage
- [ ] Written by someone else / unfamiliar code
- [ ] Production-critical path

**Risk level:** [Low / Medium / High / Abort]
```

**GATE:** Do not proceed if:
- Risk is "Abort"
- More than 3 risk factors checked AND no tests exist
- You can't list all affected files

If high risk: Consider breaking into smaller refactors.
</phase_risk>

### Phase 2: Prepare

<phase_prepare>
Before touching code:

1. **Ensure tests exist** (or write them first)
   ```
   - [ ] Existing tests cover the behavior being preserved
   - [ ] If no tests: write characterization tests NOW
   ```

2. **Create escape hatch**
   ```bash
   git stash  # or commit current state
   git checkout -b refactor/[description]
   ```

3. **Document current behavior**
   ```
   Before: [How it works now]
   After: [How it should work - must be identical externally]
   ```

**GATE:** Do not proceed without:
- Tests that verify current behavior
- Clean git state (can revert easily)
- Clear before/after behavior description
</phase_prepare>

### Phase 3: Implement

<phase_implement>
**Rules for safe refactoring:**

1. **One thing at a time**
   - Don't mix refactoring with feature changes
   - Don't fix bugs you discover (note them, fix separately)
   - Don't "while I'm here" other improvements

2. **Small commits**
   ```bash
   # Good: multiple small commits
   git commit -m "Extract helper function"
   git commit -m "Rename variables for clarity"
   git commit -m "Move file to new location"

   # Bad: one giant commit
   git commit -m "Refactor everything"
   ```

3. **Run tests frequently**
   - After each logical change
   - Before each commit
   - If tests fail: revert and try smaller steps

4. **Preserve behavior exactly**
   - No "improvements" to logic
   - No fixing edge cases (that's a separate change)
   - External behavior must be identical
</phase_implement>

### Phase 4: Verify

<phase_verify>
**If prove-it skill installed:** Invoke it now.

**If not installed:**

```markdown
## Refactor Verification

**Automated checks:**
- [ ] All existing tests pass
- [ ] No new linter errors
- [ ] Type checking passes (if applicable)

**Manual verification:**
- [ ] Tested the primary use case manually
- [ ] Checked one edge case
- [ ] Compared behavior before/after for critical paths

**Regression check:**
- [ ] git diff shows only intended changes
- [ ] No accidental behavior changes
- [ ] No debug code left in
```

**GATE:** Do not merge until all checks pass.

If verification fails:
```bash
git revert HEAD  # or reset to before refactor
# Start over with smaller scope
```
</phase_verify>

### Phase 5: Document (Optional)

<phase_document>
**If retrospective skill installed:** Invoke for significant refactors.

For large refactors, capture:
- What was refactored and why
- Any tricky parts or gotchas discovered
- Patterns that emerged (potential future skills)
</phase_document>

## Output Format

```markdown
## Safe Refactor: [Description]

### Risk Assessment
- Risk level: [Low/Medium/High]
- Files affected: [count]
- Risk factors: [list]

### Preparation
- [x] Tests verified/written
- [x] Branch created: refactor/[name]
- [x] Current behavior documented

### Implementation
- Commits: [count]
- Approach: [brief description]

### Verification
- [x] Tests pass
- [x] Manual verification complete
- [x] No regressions detected

### Learnings (if significant)
[What you'd do differently]
```

## NEVER

- Refactor and add features in the same change
- Skip the risk assessment ("it's just a small cleanup")
- Make large changes without test coverage
- Commit all changes in one giant commit
- "Fix" bugs discovered during refactoring (note them separately)
- Proceed when tests are failing

## ALWAYS

- Assess risk before starting
- Ensure tests exist (write them if needed)
- Work on a branch with escape hatch ready
- Make small, incremental commits
- Run tests after each logical change
- Verify behavior is preserved exactly

## Example

**User:** "Refactor the authentication module to use the new token format"

**Phase 1 - Risk Assessment:**
> Refactor Risk Assessment:
> - Files affected: auth.ts, token.ts, middleware.ts, 12 test files
> - Risk factors: ✓ Core code, ✓ Production-critical, ✓ Written by someone else
> - Risk level: **High**
>
> Recommendation: Break into smaller refactors:
> 1. First: Add new token format support alongside old
> 2. Second: Migrate consumers one by one
> 3. Third: Remove old format

**Phase 2 - Prepare:**
> - [x] Existing tests cover token generation and validation
> - [x] Created branch: refactor/token-format-v2
> - [x] Documented: Old format is JWT with RS256, new format adds `typ` header

**Phase 3 - Implement:**
> Making changes incrementally...
> - Commit 1: "Add TokenV2 class with new format"
> - Commit 2: "Add feature flag for token format"
> - Commit 3: "Update token generation to use flag"
> - Tests passing after each commit ✓

**Phase 4 - Verify:**
> - [x] All 47 auth tests pass
> - [x] Manual test: login flow works with both formats
> - [x] Manual test: token refresh works
> - [x] git diff shows only intended changes
>
> Ready to merge.
