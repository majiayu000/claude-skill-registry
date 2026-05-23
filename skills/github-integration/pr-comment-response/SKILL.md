---
name: pr-comment-response
description: Respond to PR review comments by verifying bug reports with failing tests before fixing code — never blindly trust a reviewer
---

# PR Comment Response

Respond to pull request review comments using a test-driven, verify-first approach. Never blindly accept reviewer suggestions — prove they're right with a failing test before changing code.

## When to Use

- After receiving code review comments on a PR
- When a reviewer claims code has a bug, edge case, or incorrect behavior
- When you need to systematically work through multiple PR comments
- Invoke with: `/pr-comment-response <PR-number>`

## Core Principle

**Reviewers can be wrong.** Treat every bug claim as a hypothesis, not a fact. The workflow is:

1. Read the comment
2. Understand the claim
3. Write a test that would fail if the claim is true
4. Run the test — does it actually fail?
5. Only fix code if the test fails
6. If the test passes, the reviewer was wrong — respond with evidence

## Workflow

### Step 1: Fetch PR Comments

```bash
# Get all review comments on the PR
gh pr view <PR-number> --json reviews,comments
gh api repos/{owner}/{repo}/pulls/<PR-number>/comments
```

Collect every comment. Categorize each one:

| Category | Action |
|----------|--------|
| **Bug report** | Full verify-first workflow (Steps 2-6) |
| **Style/naming suggestion** | Evaluate on merit, apply if reasonable |
| **Question / clarification** | Reply with explanation |
| **Refactor suggestion** | Evaluate, apply if it improves clarity without risk |
| **Nitpick** | Apply if trivial and correct |

**Focus the verify-first workflow on bug reports and correctness claims.** These are the comments where blind trust is most dangerous.

### Step 2: Analyze Each Bug Claim

For each comment claiming a bug or incorrect behavior:

1. **Read the code** the comment refers to — understand it fully before proceeding
2. **Identify the claim** — what specific behavior does the reviewer say is wrong?
3. **Identify the trigger** — what input, state, or condition would expose the bug?
4. **Assess plausibility** — does the claim make logical sense given the code?

Document your analysis before writing any test:

```markdown
### Comment: [reviewer quote or summary]
- **File**: path/to/file.rs:LINE
- **Claim**: [what the reviewer says is wrong]
- **Trigger condition**: [input/state that would expose the bug]
- **Plausibility**: [high/medium/low — your initial assessment and why]
```

### Step 3: Write a Failing Test

Write a test that **directly targets the claimed bug**. The test should:

- Use the exact trigger condition the reviewer described (or a minimal reproduction)
- Assert the **correct** behavior (what the code *should* do)
- Be placed in the appropriate test module for the file under review
- Have a clear, descriptive name describing **the behavior being tested** — never reference the PR comment, reviewer, or call it a "regression test"

```rust
#[test]
fn handles_empty_input_without_panic() {
    let result = function_under_review(&[]);
    assert!(result.is_ok(), "empty input should not panic");
}
```

**Do NOT touch the production code yet.**

### Step 4: Run the Test

```bash
cargo test <test_name> -- --nocapture
```

**Two outcomes:**

#### Test FAILS — Reviewer was right

The bug is confirmed. Proceed to Step 5.

Record:
```markdown
- **Verdict**: CONFIRMED — test fails with: [error message]
```

#### Test PASSES — Reviewer was wrong

The code already handles this case correctly. **Do not change the code.**

**Delete the verification test.** It served its purpose — proving the reviewer's claim was wrong. Keeping it adds noise without value since it tests behavior that already works and wasn't at risk.

Record:
```markdown
- **Verdict**: NOT REPRODUCED — test passes, code already handles this correctly
- **Verification test**: removed (served its diagnostic purpose)
- **Response**: [draft reply to reviewer explaining why the code is correct]
```

Skip to Step 6 for this comment.

### Step 5: Fix the Code (Only After Confirmed Failure)

Now — and only now — fix the production code:

1. Make the **minimal change** needed to pass the test
2. Run the specific test to confirm it passes
3. Run the full test suite to check for regressions

```bash
# Confirm the fix
cargo test <test_name> -- --nocapture

# Check for regressions
cargo test
```

If the full suite passes, the fix is good. If new failures appear, investigate — the fix may have been too broad or revealed a deeper issue.

### Step 6: Respond to the Reviewer

Draft responses for each comment:

**For confirmed bugs:**
```markdown
Good catch! Confirmed — added a test (`test_name`) that reproduces this.
Fixed in [commit SHA]. The issue was [brief explanation].
```

**For unconfirmed claims:**
```markdown
I investigated this and wrote a test targeting the scenario you described.
The test passes against the current code — [brief explanation of why the code is correct].
Let me know if I'm missing something.
```

**For non-bug comments (style, refactor, questions):**
Address directly without the test workflow.

## Handling Multiple Comments

When a PR has many comments:

1. **Triage first** — categorize all comments before acting on any
2. **Prioritize bug claims** — handle these with full verify-first workflow
3. **Batch style/nitpick fixes** — apply these together in one pass
4. **Group related comments** — if multiple comments point at the same underlying issue, write one comprehensive test

## Output Format

After processing all comments, produce a summary:

```markdown
## PR Comment Response Summary — PR #<number>

### Bug Claims Investigated

| # | Comment | File | Verdict | Test | Fix |
|---|---------|------|---------|------|-----|
| 1 | [summary] | path:line | CONFIRMED | test_name (kept) | commit SHA |
| 2 | [summary] | path:line | NOT REPRODUCED | verified & removed | N/A |

### Other Changes

- [Style fix]: renamed `foo` to `bar` per reviewer suggestion
- [Refactor]: extracted helper function for clarity
- [Reply]: explained why X is intentional

### Test Results

- New tests added: N
- All tests passing: yes/no
- Regressions found: none / [details]
```

## Anti-Patterns to Avoid

- **Blind application**: Never change code just because a reviewer said to
- **Skipping the test**: Always write the test before fixing, even if the bug seems obvious
- **Fixing without failing**: If your test passes, the "bug" isn't a bug — don't fix it
- **Over-scoping fixes**: Fix only what the test proves is broken, nothing more
- **Keeping diagnostic tests**: If a verification test passes (reviewer was wrong), delete it — it was a diagnostic tool, not a valuable test. Tests that merely confirm already-working behavior add noise.
- **Naming tests after the review**: Never name a test "regression_for_pr_comment" or similar. Name it after the behavior it verifies.
- **Arguing without evidence**: If you disagree with a reviewer, show a passing test, don't just assert correctness

## Related Skills

- `/test-strategy` - Choose appropriate test type (unit, property, fuzz, Kani)
- `/security-reviewer` - For security-related review comments
- `/bench-compare` - If reviewer flags a performance issue
