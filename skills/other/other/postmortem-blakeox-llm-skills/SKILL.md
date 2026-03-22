---
name: postmortem
description: Brutally honest incident postmortem. Reconstructs what happened from git, deploys, and logs — not from memory. Questions the process that allowed this to ship, not just the code that broke. No blame, all accountability.
user-invocable: true
argument-hint: "[incident description, PR, or commit]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- "Human error" is not a root cause. Processes exist to catch human error. If they didn't, the process failed.
- The comfortable root cause is the one that doesn't implicate the process. Push past it.
- "We were moving fast" is not an explanation. Moving fast without catching bugs is moving forward and backward at the same time.
- Every incident that surprises you is a monitoring failure on top of a code failure.

## Domain-specific examples

**Root cause — wrong way:**

"The incident was caused by a developer accidentally dropping a column that was still in use. This was an unfortunate oversight. Going forward, we should be more careful with migrations."

**Root cause — right way:**

"The column was dropped in migration `20240301_remove_legacy_fields.rb` (commit `abc1234`, author: Alice, deployed 14:32 UTC). The reporting service still reads this column at `app/queries/revenue_report.rb:67`. Alice didn't know because: (1) there's no cross-service dependency map, (2) the migration had no test that verifies downstream consumers, (3) the PR review (Bob, 14:15 UTC) didn't check for cross-service impact — the review focused on the migrating service only. Root cause: the team has no mechanism to detect cross-service column dependencies. This is the third time a migration has broken a downstream consumer this quarter (see incidents #41, #47). The pattern will repeat until there's automated cross-service schema validation in CI."

## Investigation process

### 1. Reconstruct timeline from evidence
Git history, deploy logs, monitoring. Not from memory. Include the **detection gap** (deploy → detection).

### 2. Five Whys — actually do all five
Don't stop at "the code had a bug." The final Why must implicate a process or system.

### 3. Question the process
For each link: was there a review? Tests? Monitoring? Rollback plan? Time pressure? Who decided to prioritize speed over correctness?

### 4. Challenge the narrative
- "We didn't have time to test" → What was prioritized instead?
- "Edge case" → How many users hit it?
- "Requirements were unclear" → Who was responsible for clarifying?
- "Worked in staging" → What's different about production?

### 5. Evaluate the fix
Root cause or symptom? Would recurrence be prevented? Similar patterns elsewhere?

## Output format

### Incident summary
One paragraph: what, who affected, how long, impact in numbers.

### Timeline
Chronological table: timestamp, event, source. Detection gap prominently displayed.

### Root cause chain
Five Whys with evidence. Final Why implicates process.

### Process failures
What should have caught this: review, test, monitoring, docs, communication gaps. Why each failed.

### Fix assessment
Symptom or root cause? Similar vulnerabilities elsewhere?

### Devil's advocate
Could the team's narrative be right? What context might justify the decisions that led here?

### Action items
Specific, owned, time-bound. What changes, who, by when, how you verify.

### What I didn't investigate / Recurrence risk (1-5, justified)
