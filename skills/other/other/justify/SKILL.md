---
name: justify
description: 'Post-implementation audit against minimal-intervention standard. Detects additive bias and test tampering. Use after work, before commit or PR.'
version: 1.9.3
alwaysApply: false
category: workflow-methodology
tags:
- justification
- proof-of-work
- anti-additive-bias
- code-review
- iron-law
dependencies:
- imbue:proof-of-work
- leyline:additive-bias-defense
tools: []
usage_patterns:
- post-implementation-review
- pre-commit-audit
- change-justification
complexity: intermediate
model_hint: standard
estimated_tokens: 2800
role: entrypoint
---

> The simplest change that fixes the problem is the
> safest change to merge.
> Adding code is easy. Removing the need for code is
> engineering.

# Justify

## The Additive Bias Problem

AI models are trained to be helpful, which creates
a systematic bias toward *adding* code rather than
*fixing* root causes:

| AI Default Behavior | Correct Behavior |
|---------------------|------------------|
| Add a workaround | Fix the root cause |
| Modify test expectations | Fix the implementation |
| Create a new helper | Use an existing one |
| Add error handling | Prevent the error |
| Add a compatibility shim | Remove the old code |
| Wrap in try/catch | Fix the exception source |

This skill audits changes for these patterns and
requires explicit justification for each.

## When to Use

- After completing implementation work
- Before committing or creating PRs
- When reviewing your own changes for quality
- When scope-guard flags RED/YELLOW zone

## Audit Protocol

### Step 1: Gather the Delta

```bash
# Determine base branch
base=$(git merge-base master HEAD 2>/dev/null \
  || git merge-base main HEAD 2>/dev/null)

# Get change statistics
git diff "$base" --stat
git diff "$base" --shortstat
git diff "$base" --diff-filter=A --name-only  # new files
git diff "$base" --diff-filter=M --name-only  # modified files
git diff "$base" --diff-filter=D --name-only  # deleted files
```

### Step 2: Compute Additive Bias Score

Score each dimension 0-3 (0 = clean, 3 = high bias):

| Signal | Weight | How to Measure |
|--------|--------|----------------|
| Line ratio | 2x | `additions / max(deletions, 1)` |
| New files | 2x | Count of `--diff-filter=A` |
| Test logic changes | 3x | Test assertion/expectation diffs |
| New abstractions | 1x | New classes, functions, modules |
| Workaround patterns | 2x | Try/catch, if/else guards added |

**Line Ratio Scoring:**

| Ratio | Score | Interpretation |
|-------|-------|----------------|
| < 2:1 | 0 | Balanced change |
| 2:1 to 5:1 | 1 | Mildly additive |
| 5:1 to 10:1 | 2 | Additive bias likely |
| > 10:1 | 3 | Strong additive bias |

**Aggregate Score:**

```
bias_score = sum(signal_score * weight) / sum(weights)
```

| Aggregate | Zone | Action |
|-----------|------|--------|
| 0.0 - 0.5 | GREEN | Proceed |
| 0.5 - 1.5 | YELLOW | Justify each signal |
| 1.5 - 2.5 | RED | Rethink approach |
| 2.5+ | STOP | Likely wrong approach |

### Step 3: Iron Law Compliance Check

The Iron Law states: tests drive implementation, not
the other way around. Check for violations:

```bash
# Find test files that were modified
git diff "$base" --name-only | rg "test_|_test\.|spec\." \
  || git diff "$base" --name-only | grep -E "test_|_test\.|spec\."

# For each modified test file, check what changed
git diff "$base" -- <test_file> | rg "^[-+].*assert|^[-+].*expect|^[-+].*should"
```

**Violation patterns (test logic was tampered):**

- Assertion values changed (expected output modified)
- Test cases removed or commented out
- `@skip` or `@pytest.mark.skip` added
- Error expectations weakened (broad exception types)
- Mock return values changed to match new behavior
- Test renamed to no longer describe original behavior

**Each violation requires explicit justification:**

> "I changed this test assertion because the
> *requirement* changed, not because my implementation
> couldn't meet the original requirement."

If the requirement didn't change, the test should not
change. Fix the implementation instead.

### Step 4: Minimal Intervention Analysis

For each changed file, answer:

1. **Was this change necessary?**
   Could the goal be achieved without touching this file?

2. **Was this the minimal change?**
   Could fewer lines achieve the same result?

3. **Did this change add or remove complexity?**
   New functions, classes, or control flow = added
   complexity that needs justification.

4. **Is there a subtraction-first alternative?**
   Could removing code fix the problem instead of
   adding code?

### Step 4.5: Invariant Impact Analysis

Changes can be minimal and still catastrophically wrong
if they silently revise a load-bearing design decision.
For each changed file, check whether it touches a design
invariant:

**What counts as an invariant:**

- Architectural patterns (module boundaries, layer
  separation, data flow direction)
- Data structure choices (why a map vs list, why
  normalized vs denormalized)
- API contracts (public interfaces, protocol formats)
- Error handling strategies (fail-fast vs recovery)
- Concurrency models (single-threaded assumption,
  actor model, shared-nothing)

**Detection heuristic:**

```bash
# Check for structural changes (new modules, moved
# boundaries, changed interfaces)
git diff "$base" --name-only | rg "(interface|abstract|base|core|types|schema|model)" \
  || git diff "$base" --name-only | grep -E "(interface|abstract|base|core|types|schema|model)"

# Check for pattern-breaking changes
git diff "$base" -U5 | rg "(TODO.*refactor|HACK|WORKAROUND|XXX)" \
  || git diff "$base" -U5 | grep -E "(TODO.*refactor|HACK|WORKAROUND|XXX)"
```

**When an invariant conflict is detected:**

Do NOT silently pick a resolution. Present the three
options to the human:

| Option | Description | When Right |
|--------|-------------|------------|
| **Preserve** | Don't add the feature; the invariant pays dividends | Invariant simplifies many things; feature is marginal |
| **Layer** | Add feature inelegantly on top | Feature is needed; invariant is still valuable; imperfection is acceptable |
| **Revise** | Change the invariant itself | Genuine new learning invalidates the original decision |

**Add to Justification Report:**

```markdown
### Invariant Impact: NONE / DETECTED

[If DETECTED:]
- **Invariant**: [name the design decision]
- **Conflict**: [what change clashes with it]
- **Option chosen**: Preserve / Layer / Revise
- **Justification**: [why this option, not the others]
- **Human reviewed**: YES / NO — if NO, flag as
  requiring review before merge
```

**Compounding risk warning:** Bad invariant decisions
accumulate. If this branch has multiple invariant
revisions, flag the entire branch for architectural
review. Each silent invariant change multiplies the
probability of an unsalvageable codebase.

### Step 5: Generate Justification Report

Output a structured report:

```markdown
## Justification Report

**Branch**: feature/xyz
**Base**: master
**Delta**: +N/-M lines, X files changed

### Additive Bias Score: X.X (ZONE)

| Signal | Score | Detail |
|--------|-------|--------|
| Line ratio | N | +A/-D = R:1 |
| New files | N | [list] |
| Test changes | N | [list] |
| New abstractions | N | [list] |
| Workarounds | N | [list] |

### Iron Law Compliance: PASS/FAIL

[List any test logic modifications with justification]

### Change-by-Change Justification

#### file.py (+N/-M)
- **What**: [description]
- **Why**: [root cause this addresses]
- **Alternatives considered**: [what else could work]
- **Why this is minimal**: [why fewer changes won't work]

#### test_file.py (+N/-M)
- **What**: [description]
- **Justification**: [why test logic changed, if it did]
- **Iron Law status**: PASS/VIOLATION

### Risk Assessment

| Factor | Rating |
|--------|--------|
| Lines changed | LOW/MED/HIGH |
| Files touched | LOW/MED/HIGH |
| Test modifications | NONE/JUSTIFIED/VIOLATION |
| New abstractions | NONE/JUSTIFIED/UNNECESSARY |
| Overall merge risk | LOW/MED/HIGH |

### Recommendations

[List any changes that should be reconsidered,
simpler alternatives, or unnecessary additions]
```

## Decision Weights

When evaluating competing approaches, weight
these factors:

| Factor | Weight | Rationale |
|--------|--------|-----------|
| Fewer lines changed | HIGH | Less risk, easier review |
| No new files | HIGH | No new maintenance burden |
| No test logic changes | HIGH | Iron Law compliance |
| Root cause fix | HIGH | Prevents recurrence |
| Removes code | BONUS | Reduces maintenance surface |
| Adds abstraction | PENALTY | Only justified at 3rd use |
| Adds error handling | NEUTRAL | Only at system boundaries |

**The Subtraction Test**: Before accepting any change,
ask: "Could I achieve this by *removing* code instead
of *adding* it?" If yes, prefer the subtractive approach.

## Integration with Proof of Work

Justify extends proof-of-work with change-level
accountability:

- **proof-of-work**: "Did it work?" (evidence)
- **justify**: "Was this the right way?" (reasoning)

Both are required before claiming work is complete.
Run proof-of-work first, then justify.

## Anti-Patterns to Flag

### 1. Test Mutation
Changing test expectations to match broken code.
**Fix**: Revert the test change, fix the implementation.

### 2. Shotgun Addition
Adding code in many files for a single-concern fix.
**Fix**: Find the single point of change.

### 3. Defensive Overengineering
Adding try/catch, null checks, or validation for
scenarios that can't happen in practice.
**Fix**: Trust internal code. Only validate at boundaries.

### 4. Premature Abstraction
Creating a helper/utility/base class for one use case.
**Fix**: Inline the code. Abstract at the 3rd use.

### 5. Compatibility Shim
Adding backward-compatibility code instead of
updating callers.
**Fix**: Update callers directly. Delete dead paths.

### 6. Silent Invariant Revision
Changing an architectural pattern, data structure
choice, or API contract without acknowledging
that a design invariant is being revised.
**Fix**: Name the invariant. Present the 3 options
(preserve, layer, revise) to a human. Do not make
the judgment call yourself — models default to the
"average" of training data, and wrong invariant
decisions compound into unsalvageable codebases.

## Scrutiny Questions (from leyline:additive-bias-defense)

Before justifying any change, apply these questions.
If the answer to questions 4 and 5 is not concrete
evidence, the change is unjustified.

1. **Priority alignment**: Is this a deviation from the
   current priority?
2. **Criticality**: Is it critical to implement at this
   juncture?
3. **Simplicity**: Does a simpler or more elegant
   solution exist?
4. **Evidence**: What evidence proves this is needed
   (not assumed)?
5. **Consequence**: What breaks if we do not add this?

## Burden of Proof Inversion

The default stance is: **this addition should not
exist.** The change must prove its necessity, not the
reviewer must prove it unnecessary.

When generating the Justification Report (Step 5), add
a `Burden of Proof` section:

| Change | Scrutiny Q4 Answer | Scrutiny Q5 Answer | Verdict |
|--------|--------------------|--------------------|---------|
| file.py | [evidence] | [consequence] | justified/needs_evidence/unjustified |

Changes with `unjustified` verdict MUST be removed or
reworked before the report passes.

## The Wise Counsel

> Is what you are doing a deviation of your priority?
> Is it critical to implement at this juncture?
> Rely less on AI and initial lines of thinking.
> Challenge yourself to be better, to think of a more
> elegant implementation or a simpler solution.

## Related Skills

- `imbue:karpathy-principles` - "Surgical Changes" and
  "Goal-Driven Execution" principles invoke this audit
  from a higher-level synthesis
- `leyline:additive-bias-defense` - the contract this
  audit enforces in detail
- `imbue:proof-of-work` - the validation layer this
  audit complements (proof-of-work asks "did it work?",
  justify asks "did it need to exist?")
- See `docs/quality-gates.md#skill-level-quality-gate-composition`
  for the full gate-skill federation graph
