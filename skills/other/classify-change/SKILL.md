---
name: classify-change
description: Classify a proposed code change as Leaf Node or Core Code to decide how much AI usage and review rigor is appropriate. Use this skill whenever the user asks "is this leaf or core", "what kind of change is this", "should I vibe code this", "can AI write this", "how rigorous should the review be", or before starting any non-trivial change. Also useful as a sub-step inside other workflows (planning, PR prep, code review) when classification matters. Asks 6 diagnostic questions about propagation range, change frequency, tech-debt tolerance, examples, failure cost, and review intensity, then outputs a clear classification with the recommended approach. Trigger even when the user describes a change without explicitly asking for classification — the answer changes how they should proceed.
---

# classify-change

The single most important rule for AI-assisted coding in production: confine the AI's mass output to leaf nodes, where the inevitable bit of tech debt won't propagate through the system. This skill makes the leaf-vs-core call concrete and consistent, so individual judgment doesn't drift across the team.

## When to use

Use whenever the leaf-vs-core distinction matters. Triggers include:

- "Is this leaf or core?"
- "What classification is this change?"
- "Should I vibe code this / can AI write this?"
- "How carefully do I need to review this?"
- Before starting non-trivial work, even when the user didn't ask
- Before or during `plan-feature` or `pr-prepare`, when the leaf/core call should be explicit and consistent with this framework

Skip only for changes that are obviously trivial (typo fixes, etc.).

## The two categories

**Leaf node.** Code that nothing else depends on — feature endpoints, UI components, scripts, reports, one-off migrations. Failure is local. Tech debt here doesn't spread. Safe for high AI involvement, lighter review.

**Core code.** Code many things depend on — auth, payment, data schema, public APIs, shared frameworks, orchestrators. Failure is system-wide. Tech debt here compounds. Requires human leadership and line-by-line review, even if AI assists.

When a change spans both, it counts as **core** (the stricter rule wins).

## The six diagnostic questions

Walk through these in order. Get user input where the answer isn't obvious from the codebase.

### Q1 — Propagation range

> If we change this, what depends on it?

- Few callers (one or two specific places) → leaf-leaning
- Many callers / many modules → core-leaning

### Q2 — Expected change frequency

> Will this part of the codebase keep evolving, or is it close to "done"?

- Likely stable for the foreseeable future → leaf-leaning
- Will keep evolving and needs to stay extensible → core-leaning

### Q3 — Tech-debt tolerance

> If this code becomes a little ugly, will future work suffer?

- A bit of debt is fine, contained → leaf-leaning
- Debt here will block other work → core-leaning

### Q4 — Examples that fit

> Which of these does the change look most like?
>
> - Reports, dashboards, single endpoints, UI components, scripts, one-off jobs → **leaf**
> - Auth, payments, data schema, public APIs, shared utilities, orchestration → **core**

### Q5 — Failure cost

> If this code goes wrong, how far does the failure spread?

- Region of the app, easy rollback → leaf-leaning
- System-wide, affects users / data → core-leaning

### Q6 — Review intensity needed

> Can the change be trusted via interface + tests, or must someone read every line?

- Interface + tests are enough → leaf-leaning
- Line-by-line read required → core-leaning

## Decision logic

After running through the questions:

- **All / mostly leaf-leaning** → classify as **leaf**
- **All / mostly core-leaning** → classify as **core**
- **Mixed / spans both** → classify as **core** (strictest rule wins; consider splitting the change)

## Output format

```markdown
## Classification: [LEAF NODE | CORE CODE]

## Why
- Q1 (propagation): <answer> → <leaf/core>
- Q2 (frequency): <answer> → <leaf/core>
- Q3 (tech debt): <answer> → <leaf/core>
- Q4 (examples): <answer> → <leaf/core>
- Q5 (failure cost): <answer> → <leaf/core>
- Q6 (review intensity): <answer> → <leaf/core>

## Recommended approach

### If LEAF
- Safe for high AI involvement
- 1 reviewer is enough
- Trust the tests + interface; you don't need to read every line
- 3 e2e tests minimum (1 happy + 2 errors)
- Plan still required, but plan.md can be lightweight

### If CORE
- AI may assist, but a human must lead the design and own the review
- 2+ reviewers, including the module owner
- Line-by-line review of the diff
- PR description must mark which files were human-reviewed line-by-line
- If the change is large, split into a human-led core change + a leaf feature change
```

## Edge cases

### "It's a leaf, but it touches core code in passing"

If the change reads core code (imports, calls) but doesn't *modify* core code, it's still leaf. The classification is about which lines change, not which lines exist.

### "It's a script / one-off / migration"

These are leaf even if they read core data — failure is bounded by a single run. But: if the script writes to production data, the *verification* of the script needs to be core-grade (don't trust it from spot-checks alone).

### "The code is in a leaf path but the failure mode is system-wide"

E.g., a script that accidentally writes to every user record. Reclassify based on **failure cost**, not file location. The point of the framework is failure containment.

### "Modeling the boundary will keep moving as models improve"

True. Today's core might be tomorrow's leaf as models become more reliable. Tech leads should re-examine the leaf/core boundary quarterly. But don't move the line based on hope — move it based on track record.

## Common mis-classifications

- **A new endpoint is leaf, even if "the API" is core.** A single new endpoint is local. Modifying the framework that all endpoints use is core.
- **A new UI page is leaf.** Modifying the design system or shared component library is core.
- **A new report is leaf.** Modifying the BI infrastructure / data warehouse schema is core.
- **A bug fix is whatever the file it's in is.** Don't auto-classify bug fixes as low-risk; if the bug is in core, treat the fix as core.

## Stopping condition

End the skill when the user has a clear classification + the recommended approach for it. Carry the classification into `plan-feature` or `pr-prepare` to set the review rigor there — this skill is the canonical owner of the leaf/core definition those workflows should follow.
