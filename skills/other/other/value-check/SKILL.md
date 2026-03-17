---
name: value-check
description: Evaluate whether a feature or product idea delivers discoverable value to end users
user-invocable: true
disable-model-invocation: true
---

# Value Check

Evaluate a feature, product direction, or the overall product against four dimensions of user value. Adapted from the Value Realization framework.

**When to use:** Before building a new feature, evaluating PMF, planning marketing, prioritizing the roadmap, or when asking "will users actually want this?"

## Input

The user will describe one of:
- A specific feature idea (e.g., "automated rent tracking via bank feeds")
- A product direction (e.g., "pivot toward property managers")
- The overall product (e.g., "evaluate BrickTrack's current PMF")
- A comparison (e.g., "should we build X or Y next?")

## Product Context

BrickTrack is a property investment portfolio tracker for Australian landlords. Core value proposition: replace messy spreadsheets with an organized dashboard for tracking properties, rent, expenses, loans, depreciation, and tax-time reporting.

- **Target users:** Australian property investors (1-5 properties, self-managed or with property manager)
- **Competitors:** spreadsheets (primary), PropertyMe (property managers), TaxTank (tax-focused), Sharesight (shares, not property)
- **Stage:** Pre-launch, building toward MVP
- **Pricing:** Freemium (1 property free, paid for multi-property)

## Four-Dimension Analysis

For each dimension, assess with a status indicator and explain reasoning.

### 1. Value Clarity (Can users articulate why they'd use this?)

Ask: "If a landlord told their friend about this, what would they say?"

| Status | Meaning |
|--------|---------|
| GREEN | Users can explain the value in one sentence without jargon |
| YELLOW | Users understand it but struggle to explain it simply |
| RED | Users don't know what problem this solves |

**Method:** Write the one-sentence pitch a user would give. If you can't write it clearly, the value isn't clear.

### 2. Value Timeline (When does the user get value?)

| Pattern | Example | Risk |
|---------|---------|------|
| Immediate | "I added my property and instantly see my equity position" | Low — users get hooked fast |
| Delayed | "After 12 months of data, I can see my portfolio performance" | High — users churn before value arrives |
| Hybrid | "I see my properties now, and over time get deeper insights" | Medium — needs clear short-term hooks |

**Method:** Identify the first moment of value. If it's more than 1 session away, flag it and propose a short-term hook.

### 3. Value Perception (Can users see/feel their progress?)

Ask: "Is the value visible in the UI, or is it invisible backend work?"

| Status | Meaning |
|--------|---------|
| GREEN | Users see a dashboard, chart, number, or status that makes value tangible |
| YELLOW | Value exists but requires the user to interpret or find it |
| RED | Value is invisible — happens in the background with no feedback |

**Method:** Describe what the user *sees* that proves this feature is working for them. If you can't point to a specific UI element, the value is invisible.

### 4. Value Discovery (Do users already know they want this?)

| Pattern | Implication |
|---------|-------------|
| Known need | "I need to track my rental income" — easy to market, users search for it |
| Latent need | "I didn't know I needed depreciation tracking until I saw how much tax I was missing" — requires education |
| Created need | "I never thought about benchmarking my yield against suburbs" — risky, may not resonate |

**Method:** Identify which type. For latent/created needs, propose the "aha moment" — the specific interaction that makes the user realize they need this.

## Output Format

```
## Value Check: [Feature/Product]

### Summary
| Dimension | Status | One-Line Assessment |
|-----------|--------|-------------------|
| Clarity   | [G/Y/R] | ... |
| Timeline  | [G/Y/R] | ... |
| Perception| [G/Y/R] | ... |
| Discovery | [G/Y/R] | ... |

### Overall Verdict
[GO / RETHINK / STOP]
- GO: 3-4 green — build it
- RETHINK: 2+ yellow — refine the value proposition before building
- STOP: Any red — fundamental value gap, solve before investing effort

### Detailed Analysis
[One paragraph per dimension with reasoning]

### Recommendations
[2-3 specific, actionable next steps]

### Comparable Products
[1-2 examples of products that solved similar value problems, with what we can learn]
```

## Tips

- **Features != Value.** "We added bank feed integration" is a feature. "You never have to manually enter a transaction again" is value.
- **Test the pitch.** If you can't explain the value to a non-technical landlord in one sentence, it's not clear enough.
- **Invisible value = no value** to users. Always make the outcome visible in the UI.
- **When comparing features:** Run value-check on each independently, then compare the verdicts side by side.
