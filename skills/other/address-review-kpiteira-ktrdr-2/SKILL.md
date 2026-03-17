---
name: address-review
description: Use when addressing PR review comments from Copilot, Claude, or human reviewers. Critically assesses each comment, recommends action (implement/push-back/discuss), and executes appropriately.
---

# Address PR Review Comments

Load this skill when:
- A PR has review comments that need addressing
- User says "address review", "check PR comments", "handle review feedback"
- After pushing code and wanting to check for automated reviewer feedback

---

## Core Principle: Critical Assessment First

**DO NOT blindly implement every suggestion.** Review comments—especially from automated reviewers like Copilot—vary widely in quality. Your job is to:

1. **Assess** each comment critically
2. **Decide** whether it improves the code
3. **Act** appropriately (implement, push back, or discuss)

This aligns with CLAUDE.md: *"Push back if something feels wrong"*

---

## Workflow

### Step 1: Fetch ALL Review Comments (FULL CONTENT)

**IMPORTANT**: Reviews come from TWO different GitHub APIs. You must check BOTH:

```bash
# Get PR number and repo info from current branch
PR_NUMBER=$(gh pr view --json number -q '.number' 2>/dev/null)
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')

# 1. Fetch inline review comments (Copilot posts line-specific comments here)
gh api "repos/$REPO/pulls/$PR_NUMBER/comments" --jq '.[] | {user: .user.login, file: .path, line: .line, body: .body}'

# 2. Fetch general PR comments (Claude GitHub Action posts here)
gh api "repos/$REPO/issues/$PR_NUMBER/comments" --jq '.[] | {user: .user.login, body: .body}'
```

**⚠️ DO NOT TRUNCATE**: Claude's reviews can be 2000+ characters with important details in "Areas for Improvement" sections. Never use `.body[:500]` or similar truncation - always fetch the FULL `.body` content.

**Why two sources?**
- **Pull request review comments** (`/pulls/.../comments`): Comments attached to specific code lines during a review. Copilot typically posts here.
- **Issue comments** (`/issues/.../comments`): General PR-level comments not attached to specific lines. Claude (via GitHub Actions) typically posts here.

> **Note:** `gh pr view --comments` only shows issue comments, not inline review comments. Use the API calls above to get both.

### Step 2: Assess Each Comment

For each comment, evaluate:

| Question | Assessment |
|----------|------------|
| Does this fix a real bug? | High value if yes |
| Does this improve readability significantly? | Medium value if yes |
| Does this improve maintainability? | Medium value if yes |
| Is this a style nitpick with no functional benefit? | Low value |
| Could this suggestion make things worse? | Negative value - push back |
| Is this context-dependent and the reviewer lacks context? | Discuss or push back |

### Step 3: Categorize

Assign each comment to one of:

#### IMPLEMENT
- Fixes actual bugs
- Prevents real security issues
- Significantly improves clarity
- Adds missing error handling that matters

#### PUSH BACK
- Style nitpicks with no functional benefit
- Suggestions that reduce debuggability (e.g., combining assertions)
- Over-engineering for hypothetical scenarios
- Changes that contradict project patterns
- Automated suggestions that lack context

#### DISCUSS
- Architectural decisions that need human input
- Trade-offs where both options are valid
- Changes that might affect other parts of the codebase

---

## Assessment Criteria by Comment Type

### Code Style Comments
```
"Consider renaming X to Y"
"This could be more concise"
```
**Usually PUSH BACK** unless the current name is genuinely confusing.

### Assertion/Test Comments
```
"Combine these assertions"
"Simplify this test"
```
**Often PUSH BACK** — Separate assertions give better failure messages. Don't sacrifice debuggability for brevity.

### Error Handling Comments
```
"Add error handling for X"
"Handle the case where Y is null"
```
**ASSESS carefully** — Is this a real scenario? Don't add defensive code for impossible cases.

### Documentation Comments
```
"Add a docstring"
"Document this behavior"
```
**IMPLEMENT** if the code is genuinely unclear. **PUSH BACK** if the code is self-documenting.

### Security Comments
```
"Validate input X"
"Sanitize before using"
```
**IMPLEMENT** if at a trust boundary. **PUSH BACK** if internal code where input is already validated.

### Performance Comments
```
"This could be optimized by..."
"Consider caching X"
```
**PUSH BACK** unless there's evidence of a real performance problem. Premature optimization is the root of all evil.

---

## Response Templates

### For IMPLEMENT
```
Implementing: [brief description]
Reason: [why this improves the code]
```
Then make the change.

### For PUSH BACK
Draft a response for the PR:
```
Thanks for the suggestion. I'm going to keep the current implementation because:
- [Concrete reason 1]
- [Concrete reason 2]

[Optional: explanation of trade-off considered]
```

### For DISCUSS
Ask the user:
```
Comment suggests: [summary]
Trade-offs:
- Option A: [pros/cons]
- Option B: [pros/cons]
How would you like to proceed?
```

---

## Example Assessment

**Comment**: "These three assertions check for the same constraint. Consider combining them into a single assertion."

**Assessment**:
- Does it fix a bug? No
- Does it improve readability? Marginally
- Does it improve maintainability? No
- Could it make things worse? **YES** — Combined assertion loses specificity. If the test fails, you won't know which pattern was found.

**Decision**: PUSH BACK

**Response**: "Keeping separate assertions for better failure diagnostics. When a test fails, we want to know exactly which forbidden pattern was detected, not just that 'one of three patterns' was found."

---

## After Processing All Comments

Provide a summary:

```
## Review Assessment Summary

**PR**: #194
**Total comments**: 6

| # | Comment | Assessment | Action |
|---|---------|------------|--------|
| 1 | Combine assertions | Low value - loses debug info | PUSH BACK |
| 2 | Add user feedback | Medium value - UX improvement | IMPLEMENT |
| 3 | Rename variable | Nitpick | PUSH BACK |
...

**Implementing**: 2 comments
**Pushing back**: 3 comments
**Discussing**: 1 comment

Shall I proceed with implementing the valuable changes and drafting push-back responses?
```

---

## Common Automated Reviewer Patterns to Watch For

### Copilot Tends To:
- Suggest combining code that's intentionally separate
- Flag "redundancy" that's actually clarity
- Miss project-specific patterns
- Suggest over-abstraction

### Claude (as reviewer) May:
- Be more context-aware but sometimes over-thorough
- Suggest documentation where code is self-documenting
- Sometimes miss that simpler is better
- Focus on high-level patterns while missing low-level bugs
- Provide positive feedback that shouldn't be treated as comprehensive validation

---

## Comparing Copilot vs Claude Reviews

When both reviewers have commented on a PR, generate a comparison summary.

### How to Identify Reviewer Source

```bash
# Get repo info
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')

# Group inline review comments by author
gh api "repos/$REPO/pulls/$PR_NUMBER/comments" | jq '
  group_by(.user.login) |
  map({reviewer: .[0].user.login, count: length, comments: map(.body[:80])})
'

# Group issue comments by author
gh api "repos/$REPO/issues/$PR_NUMBER/comments" | jq '
  group_by(.user.login) |
  map({reviewer: .[0].user.login, count: length, comments: map(.body[:80])})
'
```

### Comparison Summary Template

```
## Reviewer Comparison: PR #194

### Overview
| Metric | Copilot | Claude |
|--------|---------|--------|
| Total comments | 4 | 6 |
| High value | 1 | 3 |
| Low value/nitpicks | 3 | 2 |
| Overlapping concerns | 2 | 2 |

### Agreement (Both flagged)
These issues were caught by both reviewers — higher confidence they matter:
- [ ] Issue X: [brief description]
- [ ] Issue Y: [brief description]

### Copilot Only
Issues only Copilot raised:
- [ ] [description] — Assessment: [IMPLEMENT/PUSH BACK/DISCUSS]

### Claude Only
Issues only Claude raised:
- [ ] [description] — Assessment: [IMPLEMENT/PUSH BACK/DISCUSS]

### Contradictions
Where reviewers disagree or suggest opposite approaches:
- Copilot says: [X]
- Claude says: [Y]
- **Recommendation**: [which to follow and why]

### Complementarity Analysis
- **Copilot strengths this PR**: [e.g., caught syntax issues, import redundancy]
- **Claude strengths this PR**: [e.g., caught logic issues, UX concerns]
- **Blind spots both missed**: [if any obvious issues neither caught]

### Summary
[1-2 sentences on overall review quality and recommended actions]
```

### Interpreting Agreement/Disagreement

| Scenario | Interpretation | Action |
|----------|---------------|--------|
| Both flag same issue | High confidence it matters | Likely IMPLEMENT |
| Only Copilot flags | Often a pattern/style nitpick | Assess carefully, often PUSH BACK |
| Only Claude flags | Often contextual/architectural | Assess carefully, often valuable |
| They contradict | Need human judgment | DISCUSS with user |

### Example Comparison Output

```
## Reviewer Comparison: PR #194

### Overview
| Metric | Copilot | Claude |
|--------|---------|--------|
| Total comments | 6 | 4 |
| High value | 1 | 2 |
| Low value/nitpicks | 4 | 1 |
| Overlapping concerns | 1 | 1 |

### Agreement
- Silent return when no metrics (both caught) → IMPLEMENT

### Copilot Only
- Combine redundant assertions → PUSH BACK (loses debug info)
- Remove "inline polling" from message → PUSH BACK (nitpick)
- Use sys.modules instead of import → IMPLEMENT (valid)
- Simplify test structure → PUSH BACK (over-abstraction)

### Claude Only
- Consider retry logic for flaky API → DISCUSS (scope creep?)
- Add integration test coverage → IMPLEMENT (good catch)
- Type hints on callback → PUSH BACK (internal function)

### Complementarity
- **Copilot**: Good at catching import/syntax patterns
- **Claude**: Better at catching missing functionality and UX issues
- **Together**: Reasonable coverage, but both over-index on style

### Summary
6 of 10 comments are low-value nitpicks. Implement 3 (silent return,
sys.modules, integration test), push back on 6, discuss 1 (retry logic).
```

---

## Key Reminders

1. **Quality over compliance** — A clean review with 0 comments addressed can be better than implementing bad suggestions
2. **Explain push-backs** — Don't just ignore; respond with reasoning
3. **Trust your judgment** — You've read the code; automated reviewers often haven't
4. **Ask when uncertain** — Use DISCUSS for genuinely ambiguous cases
5. **Batch similar decisions** — If pushing back on multiple similar comments, explain once

---

## When Done

After addressing all comments:
1. Commit any implemented changes
2. Push to update the PR
3. Post push-back responses as PR comments (or suggest user does)
4. Advise whether to request re-review
