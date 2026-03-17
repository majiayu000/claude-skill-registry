---
name: prove-it
description: |
  Before declaring any task complete, actually verify the outcome. Run the code.
  Test the fix. Check the output. Claude's training optimizes for plausible-looking
  output, not verified-correct output. This skill forces the verification step
  that doesn't come naturally. No victory laps without proof.
allowed-tools: |
  bash: python, node, npm, pytest, jest, cargo, go, make, cat, ls, grep
  file: read
---

# Prove It

<purpose>
Claude generates code by pattern-matching on training data. Something can look
syntactically perfect, follow best practices, and still be wrong. The model
optimizes for "looks right" not "works right." Verification is a separate
cognitive step that must be explicitly triggered. This skill closes the loop
between implementation and proof.
</purpose>

## Why This Matters (Technical Reality)

<technical-honesty>
Claude's limitations that this skill addresses:

**1. Generation vs Execution**
I generate code but don't run it. I predict what it would do based on patterns.
My confidence comes from "this looks like working code I've seen" not from
"I executed this and observed the result."

**2. Training Signal Mismatch**
My training optimizes for plausible next-token prediction, not outcome
verification. Saying "Done!" feels natural. Verifying feels like extra work.
But verification is where correctness actually lives.

**3. Pattern-Matching Blindness**
Code that matches common patterns feels correct. But subtle bugs hide in the
gaps between patterns. Off-by-one errors. Wrong variable names. Missing edge
cases. These "look right" but aren't.

**4. Confidence-Correctness Gap**
High confidence in my output doesn't correlate with actual correctness.
I'm often most confident when I'm most wrong, because the wrong answer
pattern-matched strongly.

**5. No Feedback Loop**
I generate sequentially. I don't naturally go back and check. Without
explicit verification, errors compound silently.
</technical-honesty>

## When To Verify

<triggers>
ALWAYS verify before declaring complete:

**Code Changes:**
- New functions or modules
- Bug fixes
- Refactoring
- Configuration changes
- Build/deploy scripts

**Fixes:**
- "Fixed the bug" - did you reproduce and confirm it's gone?
- "Resolved the error" - did you trigger the error path again?
- "Updated the config" - did you restart and test?

**Claims:**
- Factual statements that matter to the decision
- "This will work because..." - did you prove it?
- "The file contains..." - did you actually read it?
</triggers>

## Instructions

### Step 1: Catch The Victory Lap

Before saying any of these:
- "Done!"
- "That should work"
- "I've implemented..."
- "The fix is..."
- "Complete"

STOP. You haven't verified yet.

### Step 2: Determine Verification Method

| Change Type | Verification |
|-------------|--------------|
| New code | Run it with test input |
| Bug fix | Reproduce original bug, confirm fixed |
| Function change | Call the function, check output |
| Config change | Restart service, test affected feature |
| Build script | Run the build |
| API endpoint | Make a request |
| UI change | Describe what user should see, or screenshot |

### Step 3: Actually Verify

```bash
# Don't just write the test - run it
python -m pytest tests/test_new_feature.py

# Don't just fix the code - prove the fix
python -c "from module import func; print(func(edge_case))"

# Don't just update config - verify it loads
node -e "console.log(require('./config.js'))"
```

### Step 4: Report With Evidence

```
Verified:

What I changed:
  - Added input validation to user_signup()

How I verified:
  - Ran: python -c "from auth import user_signup; user_signup('')"
  - Expected: ValidationError
  - Got: ValidationError("Email required")

Proof that it works. Done.
```

## Verification Patterns

### Pattern 1: The Smoke Test

Minimal test that proves basic functionality:

```bash
# After writing a new function
python -c "from new_module import new_func; print(new_func('test'))"
```

If this crashes, you're not done.

### Pattern 2: The Regression Check

After fixing a bug, trigger the original failure:

```bash
# Bug was: crash on empty input
python -c "from module import func; func('')"
# Should not crash anymore
```

### Pattern 3: The Build Gate

Before claiming code is complete:

```bash
# Does it at least compile/parse?
python -m py_compile new_file.py
npm run build
cargo check
```

### Pattern 4: The Integration Smell Test

After changes that affect multiple components:

```bash
# Start the service
npm run dev &

# Hit the affected endpoint
curl http://localhost:3000/affected-route

# Check for expected response
```

## The Verification Checklist

Before declaring done:

```
[ ] Code runs without syntax errors
[ ] Function produces expected output on happy path
[ ] Edge case handled (empty, null, boundary)
[ ] Original bug/issue no longer reproduces
[ ] No new errors introduced (check logs)
[ ] Build passes (if applicable)
```

## NEVER

- Say "done" without running the code
- Assume it works because it looks right
- Skip verification because you're confident
- Claim a bug is fixed without reproducing it first
- Trust that generated code is correct
- Let pattern-matching substitute for proof

## ALWAYS

- Run new code at least once
- Test the specific thing that was broken
- Show verification output in your response
- Admit when you can't verify (and say why)
- Treat verification as required, not optional

## Examples

### Example 1: Bad (No Verification)

```
User: "Fix the divide by zero error"

*edits code to add check*

Done! Added a check for zero before dividing. The function now returns
None if the divisor is zero.
```

This is a lie. I didn't verify anything.

### Example 1: Good (With Verification)

```
User: "Fix the divide by zero error"

*edits code to add check*

Let me verify the fix:

$ python -c "from math_utils import safe_divide; print(safe_divide(10, 0))"
None

$ python -c "from math_utils import safe_divide; print(safe_divide(10, 2))"
5.0

Verified:
- Division by zero returns None (was: crashed)
- Normal division still works
- Fix confirmed.
```

### Example 2: Admitting Inability To Verify

```
User: "Update the production config"

I've updated config/production.json with the new API endpoint.

Verification status: UNABLE TO VERIFY
- This is production config
- I can't safely test against production
- Recommend: Test in staging first, or have ops verify after deploy

Change is made but unverified. Proceed with caution.
```

### Example 3: Build Verification

```
User: "Add TypeScript types to the utils"

*adds types*

Verifying:

$ npm run typecheck
src/utils.ts - 0 errors

$ npm run build
Build successful - dist/utils.js generated

Verified: Types compile without errors, build passes.
```

<failed-attempts>
What DOESN'T work:

- **"I'll verify later"**: Later never comes. Verify immediately or it won't happen.
- **"It looks right"**: Pattern-matching is not verification. Code that looks perfect can be completely wrong.
- **"The tests will catch it"**: Tests you haven't run don't catch anything. Run them.
- **"It's a small change"**: Small changes cause big breaks. One-character typos crash production.
- **Verifying only the happy path**: The bug is in the edge case you didn't test.
- **Reading the code as verification**: Reading is not running. Execute it.
- **"It worked before"**: Before is not now. Dependencies change. Environments differ.
- **Trusting the type checker**: Types compile doesn't mean logic is correct.
</failed-attempts>

## The Hard Truth

When I say "Done!" without verifying, I'm not reporting a fact. I'm making a
prediction based on pattern-matching. Sometimes that prediction is wrong.

Verification converts prediction into observation. It's the difference between
"this should work" and "this works."

One is a guess. One is proof.

Prove it.
