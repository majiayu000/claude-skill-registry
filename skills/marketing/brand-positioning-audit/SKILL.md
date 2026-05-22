---
name: brand-positioning-audit
version: "2.0.0"
price: "$9"
author: "@BrianRWagner"
platform: claude-code
slug: "brw-brand-positioning-audit"
description: "Diagnose brand positioning with a 6-dimension scorecard, identify the root failure, and receive specific rewrite-level fixes — including headline, subheadline, and CTA rewrites ready to use."
---

> **Optimized for Claude Code, Cursor, GitHub Copilot, and any AI that accepts markdown instructions.**
> Paste this SKILL.md into your AI's context or project instructions and run it immediately.

---

# Brand Positioning Audit

Most brands don't have a messaging problem. They have a positioning problem — and bad messaging is the symptom.

"We help teams work better together" is not a positioning. Neither is "The leading platform for [category]." These sound like something, but they say nothing. They don't tell your ICP why you're the obvious choice. They don't separate you from the 47 competitors saying the same thing.

This audit diagnoses your positioning across 6 dimensions. Finds the root failure. Gives you specific rewrite-level fixes — not direction, actual copy you can use.

---

## Mode

Detect from context or ask: *"Quick diagnosis, full audit, or full audit with rewrites?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | Root failure identified + top 2 fixes | Fast gut-check, pre-meeting clarity |
| `standard` | 6-dimension scorecard + root cause + specific rewrite-level fixes | Full positioning overhaul |
| `deep` | Full audit + headline/subheadline/CTA rewrites + competitive separation analysis | GTM launch, rebrand, investor pitch |

**Default: `standard`** — use `quick` for fast direction. Use `deep` when you need ready-to-use copy alongside the diagnosis.

---

## Context Loading Gates

**The AI must confirm all gates before running any analysis.**

```
GATE CHECK — Required Before Starting
======================================
[ ] Brand URL provided (minimum required)
[ ] OR current messaging pasted directly (if no website)
[ ] ICP defined — optional but significantly improves diagnosis
[ ] Top competitors identified — optional but improves competitive separation scoring
[ ] Stated frustration with current positioning — optional, helps focus the audit

If URL is unavailable: ask user to paste homepage copy and about page copy.
Do not audit vague descriptions. Need actual messaging to analyze.
```

---

## Phase 1: Context Intake

Ask for all inputs in a single message:

```
To run your brand positioning audit, give me:

1. Brand URL (homepage + about page if possible)
2. Current tagline or hero headline (if you know it)
3. Who you sell to — be specific. "B2B founders" is better than "businesses."
4. Your top 2-3 competitors (optional)
5. What specifically frustrates you about your current positioning? (optional — helps focus the audit)
```

If this is a re-audit: load prior audit scores and show deltas per dimension.

---

## Phase 2: Analysis — Research + Scoring

**Fetch the brand's website and capture:**
- Exact hero headline and subheadline (verbatim)
- About page positioning language (verbatim)
- Any stated ICP or "who it's for" language
- How they describe differentiation
- What proof they include (testimonials, case studies, data)
- Primary CTA copy

**Score each of the 6 dimensions on a 1-10 scale:**

---

### Dimension 1: ICP Clarity (1-10)

Is it clear exactly who this is for?

**A 10:** The ICP is specific enough that someone could name 5 real people who fit.
**A 5:** General category stated but no specificity (e.g., "for marketers" — which marketers? doing what? at what stage?)
**A 1:** No indication of who this is for. Anyone could be the customer.

**Evidence:** Quote the exact copy that does or doesn't define ICP clearly.

---

### Dimension 2: Value Clarity (1-10)

Is the primary value proposition stated in concrete, outcome terms?

**A 10:** Specific outcome stated with a mechanism. "Cut your response time in half by routing support tickets automatically."
**A 5:** Category stated but benefit is vague. "Streamline your workflow."
**A 1:** No clear value stated. "The better way to work."

**Evidence:** Quote the exact copy that does or doesn't articulate value.

---

### Dimension 3: Differentiation (1-10)

Does anything about this positioning make it impossible to swap with a competitor?

**A 10:** The position is specific enough that a competitor would need to fundamentally change their business to claim it.
**A 5:** There's a differentiation angle but it's not owned — any competitor could claim it too with minor messaging changes.
**A 1:** No differentiation. Interchangeable with every competitor.

**Evidence:** Quote the differentiation copy (or note its absence). Test: could a competitor say this exact thing?

---

### Dimension 4: Proof Credibility (1-10)

Does the positioning feel earned, or asserted?

**A 10:** Specific numbers, named clients, before/after results, recognized validators.
**A 5:** Some proof exists but it's vague or generic (e.g., "thousands of happy customers").
**A 1:** Pure assertion. Nothing to validate the claim.

**Evidence:** List what proof elements are present and rate their specificity.

---

### Dimension 5: Message-Market Fit (1-10)

Does the language match how the ICP actually talks about this problem?

**A 10:** The copy uses the exact phrases, pain points, and framing the ICP uses in their own words — not how the company wants to describe itself.
**A 5:** Close, but there's noticeable inside-out language (features, capabilities, platform) rather than outside-in language (outcomes, pain, situation).
**A 1:** The language is entirely internal. Sounds like how the founders talk about the product, not how customers talk about their problem.

**Evidence:** Quote 2-3 phrases that feel "inside-out" vs. how the ICP would actually phrase the problem.

---

### Dimension 6: Competitive Separation (1-10)

Is there a clear reason to choose this over alternatives?

**A 10:** The positioning creates a specific comparison frame that makes competitors' alternatives look like wrong choices for the right buyer.
**A 5:** Better/faster/cheaper than competitors — but doesn't explain why the comparison is one-sided.
**A 1:** No competitive framing at all. Assumes the buyer has no alternatives.

**Evidence:** Quote competitive separation language (or note absence). Name the closest competitor — could they make the same claim?

---

## Phase 3: Generate — Full Audit Output

### Root Failure Identification

After scoring all 6 dimensions, identify the single root failure. Don't list all problems — find the one that's causing the others.

**Root failure types:**
- **Clarity failure** — Can't tell what this is or who it's for. Everything else is downstream of not knowing the fundamental answer.
- **Audience failure** — ICP is too broad or wrong. All the messaging is aimed at no one in particular.
- **Differentiation failure** — The position is real but not owned. Competitors say the same thing.
- **Proof failure** — Claims aren't earned. Positioning requires proof that doesn't exist yet.
- **Language failure** — Positioning insight is right but expressed in inside-out language. Rewrites will fix it.

State: "The root failure is: [type] — [one sentence on why]"

---

### Audit Output Format

```markdown
# Brand Positioning Audit — [Brand Name]
*Audited: [Date] | Version 2.0*

## Scorecard

| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| ICP Clarity | [X] | [one-line summary] |
| Value Clarity | [X] | [one-line summary] |
| Differentiation | [X] | [one-line summary] |
| Proof Credibility | [X] | [one-line summary] |
| Message-Market Fit | [X] | [one-line summary] |
| Competitive Separation | [X] | [one-line summary] |
| **Overall** | **[avg]** | |

## Root Diagnosis

Root failure: **[type]**

[2-3 sentences on what's actually broken and why fixing the other dimensions won't matter until this is resolved]

## Evidence (verbatim from site)

Current hero: "[verbatim headline]"
Current sub: "[verbatim subheadline]"

What's missing: [specific element — ICP? outcome? proof? differentiation?]

## Priority Fixes

**Fix 1 (address root failure first):**
[Specific action — e.g., "Narrow the ICP from 'marketers' to 'solo consultant-founders doing their own marketing'"]
Why: [one sentence]

**Fix 2:**
[Specific action]
Why: [one sentence]

**Fix 3:**
[Specific action]
Why: [one sentence]

## Rewrite Pack

Three specific rewrites you can use now. No direction — actual copy.

**Option A — Benefit-forward:**
Headline: [rewrite]
Subheadline: [rewrite]
CTA: [rewrite]

**Option B — ICP-specific:**
Headline: [rewrite — leads with who it's for]
Subheadline: [rewrite]
CTA: [rewrite]

**Option C — Differentiation-led:**
Headline: [rewrite — leads with the owned position]
Subheadline: [rewrite]
CTA: [rewrite]

## Strategic Risks if Unchanged

1. [What happens if the root failure isn't fixed — specific consequence]
2. [Second risk]
3. [Third risk — may be competitive: "A competitor who positions against this exact gap will take your category"]
```

---

## Phase 4: Self-Critique

After generating the audit, run this mandatory review:

```
SELF-CRITIQUE — Audit Quality Check
=====================================
Scorecard accuracy (1-10): ___
- Are scores based on actual evidence from the site, not gut feel?
- Did I quote verbatim copy to justify each score?

Root failure specificity (1-10): ___
- Is the root failure one concrete thing, or a list of problems dressed up as one?
- If someone asked "what should I fix FIRST?" — is the answer obvious?

Rewrite quality (1-10): ___
- Are the three rewrites genuinely different positioning approaches?
- Or are they slight variations of the same idea?
- Would any of these headlines stop a cold prospect in the right direction?

Risks specificity (1-10): ___
- Are the strategic risks specific to this brand's situation?
- Or could they apply to any brand with a positioning problem?

If any score < 7: revise that section.
Improvements: [specific]

Overall: [one sentence — is this audit decision-quality?]
```

---

## Phase 5: Final Output + Iteration Menu

Present the refined audit. Then close with:

```
That's your brand positioning audit for [Brand].
Overall score: [X]/10 | Root failure: [type]

What's next?

A) Rewrite mode — I'll generate 3 more headline options for the strongest positioning angle
B) Competitor benchmark mode — I'll audit one competitor using the same scorecard and show where you have an advantage
C) Decision mode — You're choosing between two positioning directions; I'll evaluate each against the scorecard
D) Done — take the rewrites and implement

Reply with a letter or describe where you want to go.
```

**If A — Rewrite Mode:**
Identify the highest-potential positioning angle from the audit. Generate 5 additional variations optimized for that angle. For each: note what it prioritizes (clarity / differentiation / ICP specificity / proof) and the context it's best suited for (homepage hero / sales deck / LinkedIn bio / cold outreach).

**If B — Competitor Benchmark:**
Run the same 6-dimension scorecard on the named competitor. Present side-by-side:
| Dimension | [Brand] | [Competitor] | Advantage |
|-----------|---------|--------------|-----------|
| ICP Clarity | X | X | [who wins] |
| ...etc |

Conclude: "Your clearest competitive advantage is [dimension]. The rewrite should exploit this."

**If C — Decision Mode:**
Score each positioning direction candidate against the 6 dimensions. Recommend one. Explain why the other is weaker — specifically, which dimension it fails on and why that matters for their ICP.

---

*Brand Positioning Audit v2.0.0 — Part of the AI Marketing Skills library by Brian Wagner (@BrianRWagner)*
*Works with: Claude Code, Cursor, GitHub Copilot, VS Code Copilot, ChatGPT, Claude.ai*
