---
name: outcome-roadmap
description: "Transform an output-focused roadmap (feature list) into an outcome-focused one. Rewrites initiatives as outcome statements reflecting user and business impact. Use when a roadmap lists features instead of results, when making a roadmap more strategic, or when communicating what success looks like vs what will be built."
when_to_use: |
  Apply when:
  - CTO provides a feature list and asks "what should we do next quarter"
  - pm agent receives a roadmap full of features, not outcomes
  - stakeholders need to understand why we're building things, not just what
  - a roadmap review reveals it lists outputs (features) but not outcomes (results)
  Guards — do NOT apply when:
  - The input already states outcomes with metrics
  - This is a single-feature PRD (use /prd instead)
effort: low
allowed-tools: Read, Write
paths:
  - "docs/plans/**"
  - "docs/requirements/**"
---

# Outcome Roadmap — from features to results

Converts a feature-focused roadmap into an outcome-focused one.

**Core principle:** Teams build features, but customers and businesses care about outcomes. An outcome roadmap communicates WHAT CHANGES, not what gets built.

---

## The transformation formula

For every initiative on the roadmap, apply:

```
Enable [customer segment] to [desired customer outcome] so that [business impact]
```

Examples:

| Output (old) | Outcome (new) |
|---|---|
| Q2: Build advanced search filters | Q2: Enable customers to find products 50% faster through intuitive discovery |
| Q2: AI recommendations | Q2: Increase average order value 20% through personalised recommendations |
| Q3: Dashboard redesign | Q3: Help operators monitor all systems with 80% less time spent on dashboards |
| Q3: SSO integration | Q3: Remove auth friction for enterprise admins so we can close 3+ enterprise deals |
| Q4: Mobile app | Q4: Enable users to complete core workflows on mobile so 7-day retention increases from 20% to 35% |

---

## How to apply

### Step 1 — Read the existing roadmap

If the user provides a roadmap file, read it. If they describe it verbally, extract the initiative list.

For each initiative, ask internally:
- What feature / project is planned?
- **Why** are we building it? What changes for customers or the business?
- What metric will improve, and by how much?
- Is there a better, different way to achieve the same outcome?

### Step 2 — Rewrite each initiative as an outcome

For each item in the roadmap:

1. **Identify the output**: What feature or project is planned?
2. **Uncover the outcome**: Why are we building it? Keep asking "So what?" until you reach real customer or business value.
3. **Rewrite**: Use the formula above. Include a metric if possible.

**"So what?" chain example:**
- "We're adding search filters" → So what?
- "Users can narrow results" → So what?
- "Users find what they're looking for faster" → So what?
- "Users convert at higher rates because they find products before abandoning" ✅ That's the outcome.

### Step 3 — Group by strategic theme (optional)

If the roadmap has 5+ items, group related outcomes into themes:
- **Retention** (outcomes that reduce churn)
- **Acquisition** (outcomes that improve conversion)
- **Monetisation** (outcomes that increase revenue per user)
- **Ops efficiency** (outcomes that reduce internal cost/time)

### Step 4 — Output format

```markdown
## Outcome Roadmap — <Product> <Quarter/Year>

### Strategic context
<1–2 sentences on what the team is optimising for this period>

### Q<N> Outcomes

| Initiative | Outcome Statement | Primary Metric | Target |
|------------|------------------|----------------|--------|
| <original feature name> | Enable [segment] to [outcome] so that [business impact] | <metric> | <target> |

### What we're NOT doing this quarter (and why)
- <deprioritised initiative>: <reason — not enough signal / too early / wrong priority>

### Key assumptions
- <assumption this roadmap depends on — if it's wrong, the outcomes change>
```

### Step 5 — Validate

Before presenting, check:
- Every outcome has a measurable component (%, number, ratio, frequency)
- "So what?" has been applied to every item — no pure feature descriptions remain
- At least one "Not doing" item is stated — otherwise scope is unbounded
- Outcomes align with stated OKRs or strategic goals in PROJECT.md

---

## Anti-patterns

❌ **"We will build X"** — that's an output, not an outcome.

❌ **"Improve UX"** — unmeasurable. Rewrite as: "Reduce time to complete checkout from 4min to 90sec".

❌ **Outcome without a metric** — if you can't measure it, you can't know if you achieved it.

❌ **Outcomes that require building a specific solution** — "Enable users to access features via mobile app" locks the solution. Better: "Enable users to complete core workflows on any device".

---

## Integration with pm agent

When the pm agent receives a feature list without a PRD:
1. Check if the list looks like outputs (feature names) or outcomes (result statements)
2. If outputs → apply this skill to transform before decomposing into tasks
3. Pass the outcome statements into the PLAN doc as the "Why" for each task group
