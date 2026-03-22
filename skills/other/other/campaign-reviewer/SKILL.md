---
name: campaign-reviewer
description: This skill should be used when the user asks "did the changes work", "review what we did on [client]", "how is [action] performing", "review past actions", "what happened after we [did X]", "review Homescape", "check Scout results", or when the campaign-analysis skill detects past executed actions in memory that need evaluation. Also triggers when asked to "measure impact", "compare before and after", or "was [action] effective".
---

# Campaign Reviewer

Review whether past campaign optimizations achieved their expected results by comparing before/after data. Produce a clear verdict and identify what to do next. Works standalone ("review what we did on Homescape") or as a component invoked by the campaign-analysis skill at Step 2.

## When to Use

**Standalone:** User asks about a specific past action's effectiveness. Run the evaluation loop and return a focused verdict with next steps.

**Invoked by another skill:** When past executed actions exist in memory and the calling skill needs to measure outcomes before proceeding with new analysis. Return verdicts that the calling skill can incorporate into its reasoning.

## Evaluation Loop

For each executed action found in memory:

### 1. Identify the Action

Load from memory records:
- What was done? (action type, payload, targets)
- When? (created_at timestamp)
- Why? (experiment title, hypothesis)
- What was the expected impact? (from payload or knowledge.md)

### 2. Check Data Sufficiency

Minimum post-action data windows before drawing conclusions:

| Action type | Minimum window | Reason |
|-------------|---------------|--------|
| Negative keywords | 7 days | Immediate effect, need volume to measure |
| Budget changes | 14 days | CPL needs time to stabilize at new spend level |
| Bid adjustments | 14 days | Auction dynamics need time to settle |
| Ad copy changes | 14-21 days | Statistical significance needs impression volume |
| Landing page changes | 14-21 days | Google reassesses QS over 2-3 weeks |
| Account restructure | 21-30 days | Learning period for Smart Bidding + QS reassessment |

If insufficient time has passed, verdict is **TOO EARLY** — note the review date and do not draw conclusions.

### 3. Compare Before vs After

Build a comparison table for the metrics the action targeted:

```
| Metric        | Before (date) | After (date) | Change    |
|---------------|---------------|--------------|-----------|
| [metric 1]    | [value]       | [value]      | [+/- %]   |
| [metric 2]    | [value]       | [value]      | [+/- %]   |
```

Pull "before" values from knowledge.md entries recorded at the time of the action. Pull "after" from current data.

Check both **direct metrics** (the metric the action targeted) and **indirect effects** (did fixing X break Y?).

### 4. Deliver Verdict

| Verdict | Criteria |
|---------|----------|
| **WORKING** | Target metrics improved in expected direction and magnitude |
| **PARTIALLY WORKING** | Some improvement but less than expected, or improvement in target metric but regression in related metric |
| **NOT WORKING** | No measurable change, or metrics worsened |
| **TOO EARLY** | Insufficient post-action data |

### 5. Investigate Gaps (if not fully WORKING)

When the verdict is PARTIAL or NOT WORKING, investigate why:

- **Did the action take effect?** (Verify negatives are applied, budget actually changed, ads are serving)
- **Did the problem shift?** (New junk replacing blocked junk = match type problem confirmed, not negatives failure)
- **Was the diagnosis wrong?** (Action targeted the wrong root cause)
- **Did external factors interfere?** (Seasonal shift, competitor change, market event)

This investigation may surface new findings that feed back into the calling skill's analysis.

### 6. Recommend Next Steps

Based on the verdict:

- **WORKING** → Record as CONFIRMED in knowledge. Continue monitoring. Consider scaling the approach.
- **PARTIALLY WORKING** → Record partial success. Identify what the remaining gap is. Recommend targeted follow-up.
- **NOT WORKING** → Record as CONTRADICTED. Revise root cause hypothesis. Recommend new investigation.
- **TOO EARLY** → Set a review date. Do not recommend new actions on the same metric until review.

## Output Format

```
### Outcome: [Action name]
- **Action:** [What was done, when]
- **Expected:** [What should have happened]
- **Actual:** [What the data shows]
- **Verdict:** [WORKING | PARTIAL | NOT WORKING | TOO EARLY]
- **Why:** [Explanation — especially important for PARTIAL/NOT WORKING]
- **Next:** [Specific recommendation]
```

## Connecting to Knowledge

Record every verdict in `data/<client_id>/knowledge.md` using the OUTCOME format:

```markdown
- OUTCOME [action date]: "[Action]. Result: [VERDICT]. [Evidence]. [Next steps if any]."
```

For detailed outcome tracking patterns, maturity signals, and the feedback loop framework, load `references/outcome-patterns.md`.

## Additional Resources

### Reference Files

- **`references/outcome-patterns.md`** — Advanced patterns: connecting outcomes to knowledge accumulation, maturity signals (confirmation vs contradiction rates), iterative improvement loops, multi-action attribution
