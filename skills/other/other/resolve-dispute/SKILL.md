---
name: resolve-dispute
user-invocable: false
description: |
  Resolves stuck review findings via a put-up-or-concede exchange. Invoked by the facilitator when a finding survives arbitration without new evidence.
---

A review finding is stuck. Structure its resolution in three steps.

**Step 1 — Frame the dispute.**
Identify and state aloud:
- The disputed finding (one sentence)
- Who holds it
- The facilitator's prior arbitration ruling (one sentence)

**Step 2 — Send the reviewer this message, substituting `[finding]` with the actual finding:**

> Your finding — [finding] — was arbitrated. To keep it open, you must provide ONE of:
> (a) A concrete failure scenario: specific inputs or conditions that produce wrong behavior
> (b) A source citation: file, line number, and what it shows
> (c) A direct counterexample to the arbitration reasoning
>
> One response. No response counts as concession. After that, the facilitator rules and the finding is DECIDED.

**Step 3 — Rule and tag.**

After the reviewer responds:
- Evidence present → the facilitator evaluates it on the merits and rules. Tag the finding DECIDED regardless of outcome.
- No evidence → the facilitator tags DECIDED, asks the reviewer to re-score.
- No response → the facilitator tags DECIDED.

DECIDED findings cannot be re-raised without new substance. This enforces the existing "Don't regurgitate decided points" rule.

**What this skill must not do:**
- Override a finding backed by real evidence
- Auto-resolve — the facilitator still decides after hearing the evidence
- Apply to first-round disagreements — use normal arbitration first
- Suppress legitimate concerns — evidence always reopens the door
