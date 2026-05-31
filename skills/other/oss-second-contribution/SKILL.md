---
name: oss-second-contribution
description: |
  Plan and execute your second and third contributions to become a regular contributor.
  Covers relationship building, progressive complexity escalation, and community presence.
  Use when your first PR was merged and you want to keep contributing, when transitioning
  from one-off contributor to regular, or when planning a sustained OSS involvement.
  Not for your first contribution — use the oss-find-issue → oss-contribute chain for that.
---

# Second Contribution

Your first PR got merged. Now what? Most contributors disappear here. This skill covers the transition from "someone who submitted a PR once" to "recognized contributor" — through deliberate relationship building, progressive challenge escalation, and sustained presence.

## Purpose

One merged PR makes you a contributor. Three makes you recognized. Ten makes you trusted. But this isn't about counting PRs — it's about building a relationship with the project and its maintainers. Each contribution should be harder than the last, teach you something new, and demonstrate growing understanding of the project. This skill helps you plan that trajectory instead of randomly picking issues.

## When to Use

- Your first PR was merged and you want to continue contributing
- You want to transition from occasional contributor to regular
- You're planning sustained involvement in a project (e.g., for GSoC, career growth)
- **NOT** for your first contribution — use `oss-find-issue` → `oss-prep-to-contribute` → `oss-contribute`
- **NOT** if your first PR was rejected — reflect on the feedback first

## Prerequisites

- At least one PR merged in the target repo
- Understanding of the repo's contribution workflow (from first contribution)
- `gh` CLI authenticated

## Process

### 1. Reflect on the first contribution

Before planning the next one, learn from the last one.

```bash
# Review your merged PR
gh pr list -R {owner}/{repo} --state merged --author @me --json number,title,mergedAt,reviews,comments

# Read the review comments — what did the maintainer catch?
gh pr view {number} -R {owner}/{repo} --json reviews,comments
```

Answer honestly:
- What went well? What was harder than expected?
- What feedback did the maintainer give? (Review comments reveal what they care about)
- How long did the review take? (Fast review = maintainer trusts the work)
- Did you enjoy working in this codebase? (Sustained contribution requires genuine interest)

### 2. Assess the relationship

Your relationship with the maintainer determines what contributions are appropriate.

```bash
# Check maintainer's responsiveness to your PR
gh pr view {number} -R {owner}/{repo} --json createdAt,mergedAt,reviews --jq '{created: .createdAt, merged: .mergedAt, review_count: (.reviews | length)}'

# Check if they've interacted with you elsewhere
gh api search/issues --method GET -f q="repo:{owner}/{repo} commenter:@me" --jq '.items | length'
```

**Signals the maintainer wants more contributions**:
- Fast review turnaround on your first PR
- "Nice work" or "feel free to tackle more" in PR comments
- They tagged you in related issues
- They approved without extensive revision requests

**Signals to slow down**:
- PR sat for weeks without review
- Extensive revision requests suggesting misalignment
- No acknowledgment beyond the merge
- Repo has very few maintainers (they may be overwhelmed)

### 3. Thinking gate — commitment check

> "Before picking your next issue:
> 1. Why do you want to continue contributing to this repo specifically? (Tech, community, mission, learning?)
> 2. What did your first contribution teach you about the codebase?
> 3. What area of the codebase do you want to understand next?
> 4. What's a realistic cadence? (One PR per week? Per month?)"

Wait for their answer. If they can't articulate why THIS repo, suggest they explore others before committing. Sustained contribution without genuine interest leads to burnout and abandoned PRs.

### 4. Find the next issue with complexity escalation

Your second contribution should be harder than your first — but not dramatically so.

```bash
# Issues in related areas (build on what you know)
gh issue list -R {owner}/{repo} --state open --label "help wanted" \
  --json number,title,labels,authorAssociation,createdAt \
  --jq '.[] | select(.authorAssociation == "MEMBER" or .authorAssociation == "OWNER") | "\(.number)\t\(.title)"'

# Check if maintainer has requested help with anything specific
gh issue list -R {owner}/{repo} --state open --search "help needed" \
  --json number,title,author,authorAssociation | head -10
```

**Complexity escalation ladder**:

| Contribution # | Appropriate Complexity |
|---------------|----------------------|
| 1 (done) | Bug fix, test addition, docs fix |
| 2 | Bug fix in a different module, feature enhancement |
| 3 | Small feature, cross-module change |
| 4-5 | Medium feature, design decision involved |
| 6+ | Significant feature, architectural input |

Pick something that:
- Builds on what you learned (related area, same patterns)
- Is slightly harder (new module, more files, design decisions)
- Has maintainer endorsement (filed by maintainer or labeled for help)

### 5. Build presence beyond code

Code contributions aren't the only way to earn trust. Do 1-2 of these between PRs:

**Review other PRs** (→ `oss-review-prs`):
```bash
# Find PRs you can meaningfully review
gh pr list -R {owner}/{repo} --state open --json number,title,additions,deletions,reviews \
  --jq '.[] | select((.reviews | length) < 2) | "\(.number)\t\(.additions)+\(.deletions)\t\(.title)"'
```

**Answer questions in issues**:
```bash
# Find issues where you can help (in areas you understand)
gh issue list -R {owner}/{repo} --state open --label "question" --json number,title
```

**Join the communication channel**:
- Check CONTRIBUTING.md for Discord, Slack, or mailing list links
- Lurk first, then answer questions in your area of knowledge
- Don't announce yourself — contribute by being helpful

### 6. Track your trajectory

Keep a mental model of your growing understanding.

```bash
# Your contribution history
gh pr list -R {owner}/{repo} --state merged --author @me --json number,title,mergedAt,additions,deletions \
  --jq '.[] | "\(.mergedAt[:10])\t+\(.additions)/-\(.deletions)\t\(.title)"'
```

After each contribution, update your map:
- **Areas I understand**: which modules, patterns, and subsystems?
- **Areas I don't understand**: where are my blind spots?
- **Skills practiced**: what did this contribution exercise?
- **Next challenge**: what's the next level up?

### 7. Set concrete goals

Vague intentions ("I'll contribute more") fail. Set specific targets:

- "I'll submit 1 PR every 2 weeks for the next 2 months"
- "My next PR will touch the {module} I haven't worked in yet"
- "I'll review 2 PRs before submitting my next one"
- "By contribution #5, I'll tackle an issue that requires a design decision"

The goals should escalate in complexity, not just quantity.

## Related Skills

- **Previous step**: ← `oss-post-pr` — after your first PR is merged
- **Trust building**: → `oss-review-prs` — review PRs between contributions
- **Next contribution**: → `oss-find-issue` — find the next issue to work on
- **If exploring new areas**: → `oss-explore-repo` — explore unfamiliar parts of the codebase
- **If new tech encountered**: → `oss-learn-stack` — learn unfamiliar patterns from the repo

## Common Rationalizations

| Shortcut | Why It Fails |
|----------|-------------|
| "I'll just pick another 'good first issue'" | Your second contribution should be harder than your first. Staying at the same level signals you're not growing. Maintainers notice. |
| "I'll contribute to a different repo instead" | Depth beats breadth. Being a regular in one repo builds trust and expertise. Hopping between repos keeps you a perpetual beginner. |
| "I don't need to review PRs, I'll just submit code" | Reviewing PRs builds relationships and teaches you what maintainers care about. Contributors who only submit code miss half the learning. |
| "I'll contribute whenever I feel like it" | Sporadic contributions don't build trust. Maintainers invest in reliable contributors. Set a cadence and stick to it. |
| "My first PR was easy, I'll jump straight to a hard issue" | Two steps up is too far. If your first PR was a typo fix, don't jump to an architectural change. Escalate gradually. |

## Red Flags

- User wants to "contribute more" but can't say why they're interested in this specific repo
- Second issue is the same complexity as the first — no growth trajectory
- User hasn't read the review feedback from their first PR
- User wants to skip community presence and just submit code
- Proposed cadence is unrealistic ("I'll submit a PR every day")

## Verification Checklist

- [ ] First contribution reflected on — lessons learned articulated (step 1)
- [ ] Maintainer relationship assessed — signals read correctly (step 2)
- [ ] User can explain why they want to continue with THIS repo (step 3)
- [ ] Next issue is harder than the first but not overwhelmingly so (step 4)
- [ ] At least one non-code contribution planned (review, answer, community) (step 5)
- [ ] Concrete goals set with specific cadence and complexity targets (step 7)

## Anti-patterns

- **DO NOT** let the user pick another "good first issue" — their second contribution should escalate
- **DO NOT** skip the reflection on the first contribution — the review feedback is a goldmine
- **DO NOT** suggest contributing without genuine interest — burnout helps no one
- **DO NOT** set quantity goals without complexity goals — "10 typo fixes" isn't growth
- **DO NOT** ignore community presence — code-only contributors miss half the value of OSS
