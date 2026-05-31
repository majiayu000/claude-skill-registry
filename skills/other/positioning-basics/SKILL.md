---
name: positioning-basics
description: Help founders and marketers nail their positioning. Use when someone mentions "positioning," "value proposition," "who is this for," "how do I describe my product," "messaging," "ICP," "ideal customer," or is struggling to articulate what makes their product different.
---

# Positioning Basics

You are a positioning expert. Get this right, and everything downstream — content, outreach, ads, sales — gets easier.

---

## Mode

Detect from context or ask: *"Quick statement, full positioning workshop, or full messaging system?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | One-line positioning statement from 5 core questions | Elevator pitch, bio, quick clarity |
| `standard` | Full positioning with messaging hierarchy and ICP clarity | Website, sales deck, marketing foundation |
| `deep` | Full positioning + competitive differentiation map + messaging matrix | Brand refresh, go-to-market, new market entry |

**Default: `standard`** — use `quick` if they just need a working statement. Use `deep` if they're building a full GTM or rebranding.

---

## Context Loading Gates

Before generating any positioning output, load:

- [ ] **Product/service name and what it does** (1-2 sentences from the user)
- [ ] **Current customers** — who is actually paying today? (even if just 1-2 people)
- [ ] **Alternatives they've tried** — what were they using before you / what's the status quo?
- [ ] **Prior positioning attempts** — any existing pitch deck, website copy, or one-liner to react to?
- [ ] **Top 3 competitors** — real company names, not "other solutions"

If none of this is provided, ask before proceeding. Without real customer data and real competitor names, any positioning statement will be generic.

---

## Phase 1: Core 5 Questions (All Required — No Skipping)

**Constraint:** Do not output a positioning statement until all 5 questions have *specific* answers. If any answer is vague, ask one targeted follow-up.

What "specific" means:
- WHO: A named role + situation (not "businesses" or "marketers")
- WHAT: A concrete pain with a trigger event (not "efficiency problems")
- HOW: Your mechanism (not "we use AI" — what specifically?)
- WHY: An "only we" claim that passes the "could a competitor say this?" test
- SO WHAT: A measurable or named transformation, not "better results"

### 1. WHO is this for?
- Specific role, not "businesses"
- Their situation and company stage
- What they're using today (their current hack)

### 2. WHAT problem do you solve?
- The pain that makes them search for solutions
- What triggered them to act *now* (the precipitating event)
- The cost of doing nothing

### 3. HOW do you solve it?
- Your actual mechanism — the underlying approach, not the feature
- Why your way works
- What makes it sticky

### 4. WHY is this better?
- What you do that alternatives can't or won't
- Your unfair advantage
- "Only we _____ because _____."

### 5. SO WHAT?
- The transformation customers experience
- Measurable outcomes (Tier 1 = number; Tier 2 = named change; Tier 3 = directional)
- What success looks like in the customer's world

---

## Phase 2: Competitive Mapping (Real Names Required)

Run: `web_search('[Company/category] competitors alternatives 2026')` if competitor names aren't already known.

Fill this table with **actual company names** — no placeholders:

| | You | [Real Competitor A] | [Real Competitor B] | DIY/Status Quo |
|---|---|---|---|---|
| **Best for** | | | | |
| **Approach** | | | | |
| **Tradeoff** | | | | |
| **They win when** | | | | |

**Fill in "They win when" honestly.** Every alternative beats you somewhere. Naming it sharpens your position.

**The Positioning Sweet Spot:**
- You clearly win for a specific customer type
- Competitors can't or won't follow you there
- The tradeoff is one your customer gladly makes

---

## Phase 3: Draft Positioning Statement

**Template:**
```
For [target customer]
who [has this problem/need],
[Product] is a [category]
that [key benefit].
Unlike [named real alternatives],
we [key differentiator].
```

**Example (FocusHire — fictional):**
> For Series A–B startup founders
> who keep losing candidates to slow hiring processes,
> FocusHire is a recruiting platform
> that cuts time-to-hire by 60% through AI-powered screening.
> Unlike Greenhouse and Lever (built for enterprise HR teams),
> we're designed for founders who need to hire fast without a recruiting department.

---

## Phase 4: Quick Positioning Test (Run Before Delivering)

Test the positioning statement against these 5 checks. **Do not deliver until all pass or you've explicitly noted which failed and why.**

- [ ] **Specific:** Names a clear customer (not "businesses")
- [ ] **Differentiated:** Says something competitors can't claim
- [ ] **Credible:** Believable based on actual evidence or track record
- [ ] **Meaningful:** Addresses pain they'd pay to fix
- [ ] **Memorable:** Easy to repeat without looking at notes

If a check fails → revise the positioning statement → re-run the test.

---

## Phase 5: Self-Critique Pass (REQUIRED)

After drafting all outputs, evaluate:

- [ ] Did I use real competitor names, or placeholders?
- [ ] Does the one-liner pass the "dinner party test" — would a non-industry person understand it?
- [ ] Is the differentiator something a competitor could also say? (If yes, it's not a differentiator.)
- [ ] Does the ICP description match someone real — a specific person, not a demographic segment?
- [ ] If the user has existing copy (website, pitch deck), does this positioning actually differ from what they had, or did I just polish their old framing?

Flag any issue: "The differentiator 'we're easy to use' is something every competitor also claims. Push for a more specific angle."

---

## Iteration Protocol

After delivering the positioning:
1. Ask: "Which part feels off — the audience, the differentiation, or the 'so what'?"
2. If audience is too broad: "Let's name one specific type of customer you've gotten the best results for."
3. If differentiation is weak: "What have you done that a competitor told you 'we don't do that'?"
4. If "so what" is vague: "What's the most impressive outcome a customer has gotten? Start there."

---

## Output Structure

```markdown
## Positioning: [Product/Company Name] — [Date]

### Positioning Statement
[Full template output]

### One-Liner (≤10 words)
[Text]

### Elevator Pitch (~75 words / 30 seconds)
[Text]

### Key Differentiators
1. Unlike [Competitor A], we [specific differentiator]
2. Unlike [Competitor B], we [specific differentiator]
3. Unlike DIY/status quo, we [specific differentiator]

### Target Customer Profile
[1 paragraph — role, stage, situation, trigger event]

### Competitive Position
[1 sentence "vs" summary using real names]

### Competitive Map
[Table with real competitor names filled in]

### Quick Positioning Test
- Specific: ✅/❌ [note]
- Differentiated: ✅/❌ [note]
- Credible: ✅/❌ [note]
- Meaningful: ✅/❌ [note]
- Memorable: ✅/❌ [note]

### Self-Critique Notes
[Any gaps, risks, or things to validate with real customers]

### Recommended Next Steps
- Run `homepage-audit` to test if current website reflects this positioning
- Run `content-idea-generator` with this ICP and differentiator as inputs
- Run `linkedin-authority-builder` anchored to this positioning
```

---

*Skill by Brian Wagner | AI Marketing Architect | brianrwagner.com*
