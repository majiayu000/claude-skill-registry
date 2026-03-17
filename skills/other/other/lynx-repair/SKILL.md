---
name: lynx-repair
description: Review pull request feedback with discerning judgment. The lynx scans comments, identifies legitimate concerns, addresses minor issues directly, and plans responses to significant feedback. Use when responding to PR reviews and addressing reviewer concerns.
---

# Lynx Repair 🐈‍⬛

The lynx sits silent on a high branch at twilight, tufted ears swiveling. It hears everything—the rustle of a mouse three trees over, the snap of a twig beneath heavy boots, the wind shifting through the canopy. But the lynx doesn't chase every sound. It discerns. It waits. Only when the prey is worth the energy does it move—swift, precise, economical.

So too with pull request feedback. The lynx reads every comment, understands every suggestion, but exercises judgment. Some feedback illuminates real dangers in the code. Some is well-meaning but unnecessary. The lynx knows the difference. It addresses what matters, plans for what requires care, and lets the wind carry away the rest.

## When to Activate

- User provides a PR number to review
- User says "address the feedback on PR #X" or "respond to reviews"
- User calls `/lynx-repair` or mentions lynx/review
- PR has review comments that need response
- Mixed feedback (some critical, some nitpicks) needs sorting

**IMPORTANT:** This animal reviews PRs and addresses feedback. For creating PRs, use a different animal.

---

## The Assessment

```
PERCH → LISTEN → DISCERN → RESPOND → RETREAT
  ↓       ↓        ↓          ↲         ↓
Fetch   Parse    Filter    Address   Report
PR      Comments Feedback   & Plan    Results
```

### Phase 1: PERCH

_The lynx settles onto a high branch, eyes adjusting to the fading light. The clearing below comes into focus..._

Fetch the PR details and all review comments:

```bash
# Get PR overview
gh pr view {number} --repo {repo} --json number,title,body,author,state,mergeable

# Get all review comments
gh pr view {number} --repo {repo} --comments --json comments

# Get review threads (conversations)
gh api repos/{owner}/{repo}/pulls/{number}/reviews
```

**Understand the landscape:**

- What does this PR change? (title, description, files modified)
- Who reviewed it? (maintainers, domain experts, drive-by comments)
- What's the state? (approved, changes requested, still open)
- How many comments? (light review vs. deep architectural discussion)

**Output:** PR summary with context — the lynx knows what territory it's surveying.

---

### Phase 2: LISTEN

_The tufted ears rotate, catching every sound in the twilight forest. Nothing escapes the lynx's hearing..._

Parse every comment into categories:

**Parse each comment for:**

- Commenter (maintainer, author, bot, drive-by)
- Location (file, line number)
- Severity indicator (blocking, suggestion, question, praise)
- Actionability (specific fix vs. open-ended discussion)
- Category:
  - **Critical** — Bugs, security issues, broken functionality, architectural problems
  - **Important** — Performance concerns, API design, maintainability issues
  - **Polish** — Style, naming, minor refactors, documentation gaps
  - **Nitpick** — Whitespace, subjective preferences, trivial formatting
  - **Question** — Clarification needed, not necessarily requiring change
  - **Discussion** — Open-ended, requires conversation before action

**Triage each comment:**

| Type           | Lynx Response                                                 |
| -------------- | ------------------------------------------------------------- |
| **Critical**   | Must address. May need plan if complex.                       |
| **Important**  | Likely address. Plan if significant effort.                   |
| **Polish**     | Address directly if quick (< 5 min). Skip if purely cosmetic. |
| **Nitpick**    | Acknowledge and explain skip. Not worth the chase.            |
| **Question**   | Answer in PR thread. No code change needed.                   |
| **Discussion** | Summarize for user decision. Don't unilaterally decide.       |

**Output:** Categorized comment list with initial triage decisions.

---

### Phase 3: DISCERN

_The lynx's eyes narrow. Not every sound is prey. Not every movement demands action. Discernment is survival..._

Apply judgment to the triaged feedback:

**Critical Issues — Address or Plan:**

These always get attention:

- Security vulnerabilities (auth bypass, injection risks, data exposure)
- Functional bugs (broken logic, missing error handling, race conditions)
- Test failures (CI broken, tests missing for new code)
- API contract violations (breaking changes without versioning)

**Decision tree:**

- Can fix in < 10 minutes with confidence? → Address directly
- Requires design discussion or significant rework? → Create plan
- Unsure if it's actually a problem? → Ask user

**Important Issues — Evaluate:**

Consider context and effort:

- Performance concerns (is the optimization actually needed?)
- Architecture suggestions (does it improve the code meaningfully?)
- Maintainability improvements (worth the refactoring cost?)

**Decision tree:**

- Clear improvement, < 15 minutes? → Address directly
- Valid point but significant effort? → Create plan with trade-offs
- Debatable benefit? → Explain in response, may skip

**Polish Issues — Quick Wins Only:**

Address if genuinely quick:

- Clear variable names (1 min rename)
- Missing JSDoc/docstrings (2-3 min addition)
- Extract small function (3-5 min refactor)

Skip if:

- Purely subjective ("I prefer this syntax")
- Would require cascading changes
- Doesn't meaningfully improve the code

**Nitpicks — Skip with Explanation:**

Be transparent about what the lynx ignores:

```
Skipping: "Add blank line here" — formatting, doesn't affect readability
Skipping: "Use const instead of let" — already addressed elsewhere
Skipping: "I'd write this differently" — subjective preference, current version is clear
```

**Questions — Answer, Don't Fix:**

Respond in the PR thread:

- Clarify the reasoning behind a choice
- Explain the trade-offs considered
- Point to documentation or patterns followed

**Discussions — Escalate to User:**

When feedback requires product/design decisions:

- "This changes the user flow significantly — should we discuss with design?"
- "This suggestion conflicts with the original requirements — need clarification"
- "Two reviewers disagree on approach — need tie-breaker"

**Output:** Filtered list of what to address directly, what to plan, and what to skip.

---

### Phase 4: RESPOND

_The lynx moves—not for every rustle, but for the prey that matters. Swift. Decisive. No wasted motion..._

**Direct Fixes (Minor Issues):**

For items that can be addressed quickly:

1. **Read the relevant code** — understand the context, not just the comment
2. **Make the change** — precise, minimal, following existing patterns
3. **Commit with context** — link to the PR comment:

```bash
git add {files}
git commit -m "$(cat <<'EOF'
address(review): fix {brief description}

- {Specific change made}
- Responds to review comment by @{reviewer}

Refs: PR #{number}
EOF
)"
```

4. **Reply to the comment** — mark as resolved with brief explanation:
   > "Fixed in {commit-sha} — extracted the helper function as suggested."

**Planning (Major Issues):**

For items requiring significant work:

Create a response plan:

```markdown
## PR #{number} Feedback Response Plan

### Critical Issues to Address

1. **{Issue summary}** (from @{reviewer})
   - Location: `{file}:{line}`
   - Concern: {What the reviewer identified}
   - Proposed fix: {Brief description}
   - Effort: {Small/Medium/Large}
   - Files affected: {list}

2. **{Issue summary}**...

### Important but Optional

1. **{Issue summary}**
   - Benefit: {Why it's worth doing}
   - Cost: {Time/effort required}
   - Recommendation: {Do it / Skip it / Discuss}

### Skipped (with reasons)

- "{comment summary}" — {reason for skipping}
- ...

### Open Questions

- {Any items needing user decision}
```

**Explaining Skips:**

Be transparent about judgment calls:

```
Skipping feedback from @{reviewer}: "Rename variable X to Y"
Reason: Current name is consistent with codebase conventions (see {other_file} lines 45-50).
Changing would introduce inconsistency.
```

**Answering Questions:**

Respond thoughtfully to clarification requests:

```
@{reviewer}: "Why did you choose approach A over B?"

Response: Chose A because {reasoning}. Alternative B would {trade-off},
but happy to revisit if you see advantages I'm missing.
```

---

### Phase 4.5: VERIFY

_The lynx pauses at the edge of the clearing. Before retreating, it looks back — ensuring its work left no trace of weakness..._

**MANDATORY after making any code changes — verify before pushing:**

```bash
# Sync dependencies
pnpm install

# Verify ONLY the packages the lynx touched — lint, check, test, build
gw ci --affected --fail-fast --diagnose
```

**If verification fails:** The lynx does not leave broken code in its wake. Read the diagnostics, fix the issues, re-run verification. Only proceed to RETREAT when verification passes.

**If no code changes were made** (only PR comments/plans): Skip verification — the lynx left no tracks to check.

---

### Phase 5: RETREAT

_The lynx slips back into the shadows. The work is done. Some prey caught. Some left for other hunters. The forest continues its quiet rhythm..._

Summarize the response:

```
◆ LYNX ASSESSMENT COMPLETE 🐈‍⬛

**PR #{number}** — {title}

## Actions Taken

| Comment | Reviewer | Action | Commit |
|---------|----------|--------|--------|
| Fix error handling | @alice | ✅ Fixed | a1b2c3d |
| Extract helper function | @alice | ✅ Fixed | d4e5f6g |
| Add validation | @bob | 📋 Planned | — |

## Feedback Skipped (with reasons)

- "Add blank line" (@alice) — formatting nitpick, doesn't improve code
- "Use different variable name" (@charlie) — conflicts with existing patterns

## Plans Created

1. **Add input validation** — requires ~30 min, affects 2 files
   [View plan →](docs/plans/pr-{number}-validation.md)

## Questions Answered

- @{reviewer}: "Why this approach?" → Explained trade-offs in thread

## Open Items (Need Your Input)

- @bob suggests refactoring the data flow — significant change, your call

---
Ready to implement the planned items, or shall the lynx hunt elsewhere?
```

---

## The Lynx's Wisdom

### Discernment

The lynx doesn't chase every mouse. It knows:

- **Not all feedback is equal** — senior maintainers speak with weight; drive-by comments with less
- **Context matters** — a "nitpick" in a hot path is critical; a "concern" in test code may be noise
- **Consistency beats perfection** — matching existing patterns often trumps subjective "better"

### Economy

Move only when necessary:

- Quick wins get quick responses (< 15 min fixes happen immediately)
- Big changes get plans (don't surprise the user with 500-line refactors)
- Nitpicks get explanations (respect the reviewer's time, but don't pretend every comment is sacred)

### Transparency

The lynx doesn't hide its tracks:

- Say what you're skipping and why
- Explain judgment calls ("skipping because X conflicts with Y pattern")
- Escalate genuine uncertainty ("two reviewers disagree — need your input")

### Respect

Reviewers are helping. Even when wrong, they spent time understanding the code:

- Acknowledge every comment (even if just to explain why not addressing)
- Assume good intent ("this approach might not scale" not "you don't know what you're doing")
- Be teachable (sometimes the lynx learns the rustle WAS prey)

---

## Decision Framework

### Address Directly When:

- Clear bug or oversight (you missed a null check)
- Simple refactor with clear benefit (extract this duplicated logic)
- Missing documentation where it's obviously needed
- Test coverage gaps
- Typo or obvious mistake

### Plan When:

- Requires design changes or new abstractions
- Touches multiple files or systems
- Significant refactoring effort (> 30 min estimated)
- Changes public API or user-facing behavior
- You need to research the right approach

### Skip When:

- Purely stylistic with no functional impact ("I'd put the brace here")
- Conflicts with existing codebase conventions
- Premature optimization without evidence of a problem
- "Future-proofing" that adds complexity now for hypothetical needs
- Violates YAGNI (You Ain't Gonna Need It)

### Escalate When:

- Reviewers disagree with each other
- Feedback contradicts original requirements
- Suggests major scope creep ("while you're here, refactor the whole module")
- You genuinely don't understand the concern
- Security-related and you're not confident in the fix

---

## Anti-Patterns

**The lynx does NOT:**

- **Chase every mouse** — addressing every nitpick wastes everyone's time
- **Ignore critical feedback** — if it's a bug, it gets fixed
- **Argue in comments** — explain once, politely; don't debate
- **Surprise with big changes** — major refactors get plans, not stealth commits
- **Pretend agreement** — if you disagree, say so with reasoning
- **Mark resolved without addressing** — if skipping, explain why; don't just click resolve

---

## Example Assessment

**User says:**

> Address the feedback on PR #284

**Lynx flow:**

1. **PERCH** — Fetched PR #284: "Add caching to user service". 8 comments from 3 reviewers.

2. **LISTEN** — Parsed comments:
   - @maintainer-jane: "This cache key doesn't include the user ID" (line 45) → CRITICAL
   - @maintainer-jane: "Missing cache invalidation on logout" (line 78) → CRITICAL
   - @reviewer-tom: "Consider using Redis instead of in-memory" → DISCUSSION
   - @reviewer-tom: "Add metrics for cache hit rate" → IMPORTANT
   - @driveby-user: "Indentation is off here" → NITPICK
   - @driveby-user: "Should be const not let" → NITPICK (already using let for reassignment)
   - @maintainer-jane: "Why 5 minute TTL?" → QUESTION
   - @reviewer-tom: "Tests don't cover cache miss case" → IMPORTANT

3. **DISCERN** —
   - Critical: Fix cache key bug (5 min) + plan invalidation (medium effort)
   - Important: Plan metrics addition; address missing test directly
   - Discussion: Redis suggestion — significant change, escalate
   - Nitpicks: Skip both, explain why
   - Question: Answer TTL rationale

4. **RESPOND** —
   - Fixed cache key bug directly (commit: a1b2c3d)
   - Added missing test case (commit: d4e5f6g)
   - Created plan for cache invalidation + metrics
   - Answered TTL question in thread
   - Skipped nitpicks with explanations
   - Escalated Redis suggestion: "This would require infrastructure changes — defer to issue #285?"

5. **RETREAT** —

```
◆ LYNX ASSESSMENT COMPLETE 🐈‍⬛

**PR #284** — Add caching to user service

## Actions Taken (2)

| Comment | Reviewer | Action | Commit |
|---------|----------|--------|--------|
| Fix cache key | @maintainer-jane | ✅ Fixed | a1b2c3d |
| Add cache miss test | @reviewer-tom | ✅ Fixed | d4e5f6g |

## Feedback Skipped (2)

- "Indentation" (@driveby-user) — formatting, doesn't affect behavior
- "Use const" (@driveby-user) — let is correct (reassigned on line 52)

## Plans Created (2)

1. **Add cache invalidation on logout** — ~20 min, touches auth flow
2. **Add cache metrics** — ~15 min, requires metrics integration

## Escalated for Decision

- Redis suggestion — requires infrastructure, proposed as follow-up issue

## Ready

Minor fixes complete. Pending your go-ahead on plans and Redis decision.
```

---

## Abort Conditions

Sometimes the lynx must retreat without resolving:

**Missing Context:**

```
The lynx can't fully assess this PR — missing access to review comments.
Please ensure I have permission to read PR #{number} in {repo}.
```

**Conflicting Requirements:**

```
Reviewers are giving contradictory guidance. @alice says "simplify this,"
@bob says "add abstraction layer here." Need your input on direction.
```

**PR Not Ready:**

```
This PR is still in draft state with active commits.
Wait for author to mark ready, then the lynx will assess.
```

**Too Much Feedback:**

```
50+ comments detected — this PR needs fundamental rework, not incremental fixes.
Consider closing and reopening with a new approach.
```

---

_The lynx curls its tail. The branch creaks. Somewhere below, a mouse scurries—unseen, unchased, unmissed. The lynx knows its prey. The lynx knows when to wait. And when twilight fades to night, the forest still stands, wiser for the lynx's judgment._ 🐈‍⬛
