---
name: campaign-analysis
description: This skill should be used when the user asks to "analyze campaign performance", "check campaigns", "investigate CPL/CVR", "review ad performance", "generate client report", "check ads", "run monthly review", mentions client names (last-minute, nota, Homescape, DMP), or needs campaign optimization insights across Google Ads, Meta, GA4, and Search Console. Also triggers when asked to "write knowledge", "update knowledge", "what do we know about [client]", "check landing page quality", or "check organic search".
---

# Campaign Analysis & Knowledge Accumulation

Analyze campaign performance across Google Ads, Meta, GA4, and Search Console. Build accumulated knowledge over time. Investigate root causes before recommending actions. Track whether past actions worked.

## Two Modes

**Monthly review:** Full flow through all steps — context, data, analysis, investigation, action plan, knowledge.

**Ad-hoc investigation:** Jump to Step 3 with a focused question ("why is CPL high?", "investigate these search terms"). Still must pass through the investigation gate before recommending actions.

## CLI Quick Reference

| Command | Purpose |
|---------|---------|
| `campaign --format json check [id] [--brand X]` | Full data package: KPIs, search terms, QS, IS, GA4, SC |
| `campaign --format json investigate [id] --metric cpl\|cvr\|volume` | Data package with metric focus noted |
| `campaign --format json memory list [id] [--brand X]` | Past experiments, actions, outcomes |
| `campaign google-ads create-negative-list [id] --source X --name X --keyword X` | Create shared negative list |
| `campaign google-ads add-negative [id] --source X --campaign X --search-term X --live` | Single negative keyword |
| `campaign google-ads adjust-budget [id] --source X --campaign X --daily-budget X --live` | Budget change |

Global flags: `--format json`, `--brand <name>`, `--month YYYY-MM`, `--days N`

For full output schema, load `references/output-schema.md`.

## Analysis Workflow

### Step 1: Load History and Context

Before looking at any data, load what is already known:

```bash
campaign --format json check <client_id> --brand <brand>
```

The data package includes `knowledge` (knowledge.md contents), `memory` (past actions), and `context` (client config). Read these FIRST.

**For each prior finding in knowledge.md:**
1. Does the current data confirm or contradict it?
2. Has the situation evolved?

Frame the analysis around these questions — not as a fresh discovery exercise.

### Step 2: Evaluate Past Actions (MANDATORY if actions exist)

If memory contains executed actions, invoke the **campaign-reviewer** skill before proceeding. This is a hard gate — do not skip to new analysis without first measuring what past actions achieved.

The campaign-reviewer evaluates each action: what was done → expected impact → enough data? → current vs expected → verdict (WORKING / PARTIAL / NOT WORKING / TOO EARLY).

Incorporate the verdicts into the analysis:
- **WORKING** actions → validated approach, consider scaling
- **PARTIAL** actions → investigate what's missing, look for problem shifting
- **NOT WORKING** actions → revise root cause hypothesis, do not repeat the same approach
- **TOO EARLY** actions → note review date, do not take additional actions on the same metric

### Step 3: Analyze Current Data

With history and outcomes established, analyze current data. Prioritize:

1. **Findings related to past action outcomes** — If Scout was PARTIAL, what are the new junk clusters?
2. **Prior finding validation** — Do known patterns still hold? (CONFIRMED / CONTRADICTED / EVOLVED)
3. **New discoveries** — What appears in the data that wasn't known before?

For cross-source reasoning patterns (CPL diagnosis, CVR diagnosis, Search Terms + Search Console connections), load `references/cross-source-playbook.md`.

### Step 4: Apply Analytical Judgment

The data package contains raw metrics without pre-filtering. Apply judgment to determine what matters. Key principles:

**Search terms:** Intent > metrics. Cluster by theme. Consider WHY terms matched (match type problem vs missing negatives). Junk ratio > 40% is systemic, not individual bad terms.

**Budget:** Portfolio decision. Only increase budget on efficient (low CPL) AND budget-constrained campaigns. IS lost to rank = QS/bid problem, not budget.

**Quality Score:** Read all 3 components together. Cross-reference with GA4 engagement. QS < 5 on high-spend = urgent.

**Trends:** R-squared < 0.5 = directional only. Check anomaly dates against known events.

For detailed analytical frameworks, benchmarks, and the band-aid vs structural fix matrix, load `references/analytical-principles.md`.

### Step 5: Investigation Gate (MANDATORY)

**STOP. Before recommending any action, investigate root cause for every significant finding.**

This is not optional. Spawn a subagent to investigate independently:

```
Subagent prompt: "Given this data [attach relevant metrics], investigate
why [specific anomaly]. Consider: campaign structure, match type settings,
keyword selection, audience targeting, landing page alignment.
Return: root cause hypothesis with supporting evidence."
```

While the subagent investigates, continue investigating from a different angle. When the subagent returns:

- **If both analyses agree** → proceed to action plan with confirmed root cause
- **If they disagree** → state both hypotheses, identify what data would resolve the disagreement
- **If data is insufficient** → recommend investigation actions (e.g., "audit match types in Google Ads UI"), not optimization actions

**Every recommended action must trace back to a root cause.** Format:

- **Root cause:** [confirmed or hypothesis]
- **Structural fix:** Change that prevents recurrence
- **Immediate action:** Band-aid for symptom relief now

### Step 6: Action Plan

Present findings as a prioritized action plan:

```
### [URGENT|WATCH|OPPORTUNITY] Title
- **Evidence:** Data with source citation
- **Root cause:** From Step 4 (confirmed or hypothesis + what data needed)
- **Structural fix:** Prevents recurrence
- **Immediate action:** Addresses symptom now
- **Expected impact:** Quantified where possible
```

Severity: URGENT (>20% KPI change + confirmed root cause), WATCH (10-20% or unconfirmed), OPPORTUNITY (improvement possible, no regression).

### Step 7: Write Knowledge

Append to `data/<client_id>/knowledge.md`:

```markdown
## YYYY-MM-DD
- CONFIRMED [prior date]: "[Finding] still holds. [Current data]."
- CONTRADICTED [prior date]: "[Finding] no longer holds. [New data]."
- OUTCOME [action date]: "[Action taken]. Result: [WORKING|PARTIAL|NOT WORKING|TOO EARLY]. [Evidence]."
- NEW: "[Finding]. [Evidence from which sources]."
```

Write: cross-source patterns, action outcomes, demand signals, revised understanding.
Do not write: raw data points, one-time observations.

### Step 8: Generate Reports

```bash
campaign brief <client_id>
```

## Additional Resources

### Reference Files

- **`references/cross-source-playbook.md`** — Multi-brand analysis, cross-platform patterns, GA4/SC benchmarks, CPL/CVR/volume investigation reasoning
- **`references/output-schema.md`** — JSON output structure for `campaign check` and `campaign investigate`
- **`references/analytical-principles.md`** — Deep reasoning frameworks: search term intent classification, budget portfolio optimization, root cause investigation, band-aid vs structural fix matrix, outcome tracking patterns
