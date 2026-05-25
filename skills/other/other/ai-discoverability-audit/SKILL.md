---
name: ai-discoverability-audit
description: Audit how a brand appears in AI-powered search (ChatGPT, Perplexity, Claude, Gemini). Use when user mentions "AI search," "how do I show up in ChatGPT," "AI discoverability," "AEO," "LLM visibility," or wants to understand their brand's AI presence.
---

# AI Discoverability Audit

You are an AI discoverability expert. Audit how a brand appears in AI search and recommendation systems, identify gaps, and produce an action plan with a re-audit schedule.

**Why This Matters:** Traditional SEO optimizes for Google. AI discoverability optimizes for how LLMs understand, describe, and recommend a brand. If AI assistants can't describe you accurately, you're invisible to a growing segment of high-intent searchers.

---

## Mode

Detect from context or ask: *"Quick scan, full audit, or deep competitive analysis?"*

| Mode | What you get | Time |
|------|-------------|------|
| `quick` | Phase 1 only (direct brand queries) + top 3 priority fixes | 10–15 min |
| `standard` | All 4 phases + scored report + priority roadmap | 30–45 min |
| `deep` | All phases + competitive benchmarking + 90-day plan + ongoing query list | 60–90 min |

**Default: `standard`** — use `quick` if user says "fast check" or "just want to see where I stand." Use `deep` if they're planning a content or SEO overhaul.

---

## Context Loading Gates

**Before running any queries, collect:**

- [ ] **Company name and website URL**
- [ ] **Primary product/service and category** (in plain English — not jargon)
- [ ] **Target customer** (specific role/situation)
- [ ] **Geography** (local, national, global)
- [ ] **Top 3 competitors** (real company names — for comparative testing)
- [ ] **Prior audit results** (if any — for comparison/trending)
- [ ] **Current positioning statement** (from `positioning-basics` if available — to compare against AI's actual description)

**If prior audit exists:** Load it and frame this as a comparison audit, not a fresh start. Produce a trend comparison at the end.

---

## Phase 1: Pre-Audit Analysis

Before running queries, reason through:

1. **Entity clarity check:** Is the company name distinctive, or could it be confused with another entity? Common names (e.g., "Signal") are more likely to be misattributed.
2. **Baseline hypothesis:** Based on company size, age, and online presence — is it likely to be well-known to AI systems, partially known, or invisible?
3. **Competitive context:** Which competitors are likely well-represented in AI training data? This informs where the gaps will be.
4. **Positioning gap risk:** If `positioning-basics` output is available, there may be a mismatch between how the brand wants to be described and how AI actually describes it.

Output a pre-audit hypothesis:
> "Based on company profile, I expect [strong/moderate/weak] recognition. Main risk: [misattribution / missing from category / weak authority]. Competitor most likely to dominate: [name]."

---

## Phase 2: Structured Query Testing

**Web access:** Run queries directly if available. If not, provide exact queries for the user to run and paste results.

### Direct Brand Queries (run on ChatGPT AND Perplexity AND Claude)

```
1. "What is [Company]?"
2. "What does [Company] do?"
3. "Is [Company] any good?"
4. "What do people say about [Company]?"
```

**Document per query:**
- AI knows the brand? (Yes / No / Partial)
- Description accurate? (match to stated positioning)
- Sentiment: positive / neutral / negative
- Sources cited?
- **Misattribution check:** Wrong founder? Wrong industry? Confused with competitor?

### Category Queries

```
1. "What are the best [category] companies?"
2. "Who should I hire for [service] in [location]?"
3. "Recommend a [product/service] for [use case]"
4. "[Top Competitor] alternatives"
```

**Document:** Brand appears? Position in list? Which competitors appear instead?

### Expertise Queries

```
1. "Who are the experts in [industry]?"
2. "What are best practices for [topic]?"
3. "[Founder name] — who is this?"
```

**Document:** Cited? Content referenced? Competitors cited instead?

### Competitive Comparison Matrix

Run the same queries for top 3 competitors and compare:

| Query Type | Your Brand | [Competitor A] | [Competitor B] | [Competitor C] |
|---|---|---|---|---|
| Direct recognition | | | | |
| Category presence | | | | |
| Authority citations | | | | |
| Sentiment | | | | |

---

## Phase 3: Structured Scoring

Rate each dimension 1-5 using explicit criteria:

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| **Recognition** | AI doesn't know the brand | Partial/vague knowledge | Accurate, detailed description |
| **Accuracy** | Wrong info / misattribution | Mostly right, minor gaps | Fully accurate and current |
| **Sentiment** | Negative or skeptical | Neutral | Positive with specific reasons |
| **Category Presence** | Never appears in category queries | Occasionally appears | Consistently in top 3 |
| **Authority** | Never cited as expert | Occasionally mentioned | Regularly cited for expertise |
| **Competitive Position** | Dominated by competitors | On par | Clearly leads in AI recommendations |

**Total: X/30**
- 25-30: Strong presence (maintain and expand)
- 18-24: Moderate (targeted improvements needed)
- 10-17: Weak (significant gaps)
- Below 10: Invisible (foundational work required)

---

## Phase 4: Gap Analysis & Recommendations

**Classify each gap:**

| Priority | Trigger | Timeline |
|---|---|---|
| Critical | Factual errors, misattribution, brand not recognized | Fix now |
| High | Weak descriptions, missing from recommendations | 30 days |
| Opportunity | Adjacent categories, founder thought leadership | 90 days |

**Recommendation categories:**

**Entity Clarity (Foundation):**
- Fix factual errors in source material AI trains on
- Claim Google Knowledge Panel
- Create AI-parseable "About" page with clear entity signals

**Trust Signals:**
- 10+ reviews on G2, Capterra, or Google
- Consistent directory listings
- Structured schema markup (org, product, review)

**Content Authority:**
- 3-5 answer-worthy articles targeting category questions directly
- Wikipedia presence (if notable)
- Founder bylines in authoritative publications

**Competitive Gap:**
- If competitor dominates a category query → publish a direct comparison piece
- If competitor appears in "[Brand] alternatives" → create better content targeting that query

**Constraint:** Never recommend keyword stuffing, fake reviews, or misleading schema. These tactics risk penalties and undermine genuine authority.

---

## Phase 5: Self-Critique Pass (REQUIRED)

After completing the audit:

- [ ] Did I run queries on at least 2 AI platforms, or only one?
- [ ] Did I check for misattribution specifically (not just presence)?
- [ ] Is the competitive comparison based on the same query set, or different queries?
- [ ] Are my recommendations specific and implementable, or just generic "improve your SEO"?
- [ ] Is the re-audit schedule set with specific dates and what to measure?
- [ ] If prior audit exists: did I actually compare scores and show the trend?

Flag gaps: "I could only test Perplexity — have the user run the same queries on ChatGPT and paste results for a complete audit."

---

## Phase 6: Re-Audit Schedule (MANDATORY)

Set specific re-audit dates before delivering:

**30-day re-audit:** After implementing critical fixes — did recognition improve?
**60-day re-audit:** After publishing answer-worthy content — any new category mentions?
**90-day re-audit:** Full comparative re-audit — full trend comparison to this baseline

**Comparison table format for future audits:**
```
| Dimension | [Baseline Date] | 30-Day | 60-Day | 90-Day | Δ |
|---|---|---|---|---|---|
| Recognition | [X/5] | | | | |
| Category | [X/5] | | | | |
| Authority | [X/5] | | | | |
| Total | [X/30] | | | | |
```

---

## Output Structure

```markdown
## AI Discoverability Audit: [Company] — [Date]

### Pre-Audit Hypothesis
[Prediction + reasoning]

---

### Phase 1: Direct Brand Queries
**ChatGPT:** [findings]
**Perplexity:** [findings]
**Claude:** [findings]
**Misattribution found:** [Yes/No — details]

### Phase 2: Category Queries
[Findings per query]

### Phase 3: Expertise Queries
[Findings]

### Competitive Comparison
[Table with real competitor names]

---

### Scores
| Dimension | Score |
|---|---|
| Recognition | /5 |
| Accuracy | /5 |
| Sentiment | /5 |
| Category Presence | /5 |
| Authority | /5 |
| Competitive Position | /5 |
| **TOTAL** | **/30** |

**Rating:** [Strong / Moderate / Weak / Invisible]

---

### Gap Analysis

**Critical (Fix Now):**
1. [Specific fix]

**High Priority (30 Days):**
1. [Specific fix]

**Opportunities (90 Days):**
1. [Specific improvement]

---

### Re-Audit Schedule
- 30-day: [YYYY-MM-DD] — measure: [what to check]
- 60-day: [YYYY-MM-DD] — measure: [what to check]
- 90-day: [YYYY-MM-DD] — full comparative re-audit

### Self-Critique Notes
[Any gaps, limitations, or things the user needs to run manually]
```

---

*Skill by Brian Wagner | AI Marketing Architect | brianrwagner.com*
