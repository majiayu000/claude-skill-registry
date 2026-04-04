---
name: product-appeal-analyzer
description: Evaluate product desirability, market positioning, and emotional resonance—the complement to friction analysis. Assess whether users will WANT a product (not just use it), identity fit, trust signals, and value proposition clarity. Activate on "will they like it", "market positioning", "appeal analysis", "product desirability", "value proposition", "why would someone choose this", "landing page review", "conversion optimization", "messaging strategy". NOT for UX friction analysis (use ux-friction-analyzer), visual design implementation (use web-design-expert), or A/B test setup (use frontend-developer).
allowed-tools: Read,Write,Edit,WebFetch
category: Research & Analysis
tags:
  - product-strategy
  - marketing
  - positioning
  - value-proposition
  - conversion
  - user-research
pairs-with:
  - skill: ux-friction-analyzer
    reason: Appeal asks "do they want it?" Friction asks "can they use it?" Use both.
  - skill: competitive-cartographer
    reason: Position against alternatives with strategic mapping
  - skill: web-design-expert
    reason: Implement visual identity recommendations
---

# Product Appeal Analyzer

Evaluate whether users will *want* a product—not just use it. The complement to friction analysis.

**Core insight**: Users don't choose the best product—they choose the product that feels most like it was made for them.

## When to Use

✅ **Use for:**
- Evaluating landing pages, product pages, app store listings
- Positioning a product against alternatives
- Crafting messaging, tone, visual identity direction
- Assessing emotional resonance with target personas
- Pre-launch "will this convert?" analysis

❌ **NOT for:**
- UX friction audits (→ use ux-friction-analyzer)
- Visual design execution (→ use web-design-expert)
- A/B test implementation (→ use frontend-developer)
- Market size estimation or financial forecasting
- Feature comparison matrices

---

## The Desirability Triangle

**All three must be present.** Missing any one kills conversion:

```
                    IDENTITY FIT
                    "This is for people like me"
                         /\
                        /  \
                       /    \
                      /  ★   \
                     / DESIRE \
                    /          \
                   /______________\
        PROBLEM               TRUST
        URGENCY               SIGNALS
   "I need this now"     "This will actually work"
```

| Missing Element | User Reaction |
|-----------------|---------------|
| Identity Fit | "Seems useful, but not for me" |
| Problem Urgency | "Cool, maybe someday" |
| Trust Signals | "Looks sketchy / too good to be true" |

**Decision tree**: When analyzing, score each vertex 1-10. If any is &lt;5, that's your priority fix.

---

## Quick Analysis: The 5-Second Test

Within 5 seconds of landing, a visitor should know:

1. **What is this?** (Category recognition)
2. **Who is it for?** (Identity signal)
3. **What's the core promise?** (Value proposition)
4. **What do I do next?** (Clear CTA)

**How to run it:**
- Show landing page to someone unfamiliar for exactly 5 seconds
- Hide it, then ask: "What was that? Who's it for? What would you do there?"
- Record verbatim—don't coach or clarify

**Scoring:**

| Result | Score | Action |
|--------|-------|--------|
| All 4 clear in &lt;3 sec | 9-10 | Ship it |
| All 4 clear in 3-5 sec | 7-8 | Minor polish |
| 3 of 4 clear | 5-6 | Fix the gap |
| 2 or fewer clear | 2-4 | Significant rework |
| Confusing/unclear | 0-1 | Start over |

---

## Analysis Process

### Step 1: Identify Target Personas

For each persona, document:
- **Who**: One-sentence description
- **Problem**: What's broken + how it feels
- **Current workaround**: What they do today (and why it sucks)
- **Identity**: How they see themselves, who they want to become

### Step 2: Score the Desirability Triangle

For each persona:

```
PERSONA: [Name]

IDENTITY FIT                    [/10]
  Visual identity match         [/10]  "Does this look like my kind of tool?"
  Language resonance            [/10]  "Do they speak my language?"
  Implied user match            [/10]  "Are people like me shown?"

PROBLEM URGENCY                 [/10]
  Pain point acknowledged       [/10]  "They understand my problem"
  Emotional resonance           [/10]  "They get how frustrating it is"
  Solution clarity              [/10]  "I see how this fixes it"

TRUST SIGNALS                   [/10]
  Professional execution        [/10]  "This looks legitimate"
  Social proof                  [/10]  "Others like me use it"
  Risk reduction                [/10]  "What if it doesn't work?"

OVERALL APPEAL SCORE:           [/90]
```

### Step 3: Map Objections

| Objection | Type | How Addressed? |
|-----------|------|----------------|
| "Is this legit?" | Trust | [Answer] |
| "I've tried things before" | Skepticism | [Answer] |
| "Too expensive" | Value | [Answer] |
| "Too complicated" | Effort | [Answer] |
| "Not for people like me" | Identity | [Answer] |
| "What if it doesn't work?" | Risk | [Answer] |
| "I'll do it later" | Urgency | [Answer] |

### Step 4: Generate Recommendations

Use priority formula: `Impact = (Users Affected × Severity) / Fix Difficulty`

Categorize into:
- **Immediate** (ship this week)
- **Medium-term** (this sprint)
- **Long-term** (roadmap)

---

## Common Anti-Patterns

### Feature Soup Headline

**Novice thinking**: "List all capabilities to show value"

**Reality**: Visitors scan for 2-3 seconds. Feature lists feel generic.

**What to use instead**:
| Bad | Good |
|-----|------|
| "AI-Powered Recovery Planning Tool with Analytics" | "Know exactly what to do next in your recovery" |
| "Comprehensive Legal Document Platform" | "Find out in 2 minutes if your record can be expunged" |

**Detection**: Headline contains 3+ nouns or buzzwords like "AI-powered", "comprehensive", "platform"

### Screenshot Hero

**Novice thinking**: "Show the product interface so people know what they're getting"

**Reality**: Strangers don't understand your UI. They care about outcomes.

**What to use instead**:
- Person experiencing the benefit
- The outcome/result they'll get
- Abstract visualization of the transformation

**Detection**: Hero image is a product screenshot with no context

### Trust Ladder Violation

**Novice thinking**: "Get their email immediately, then convert them"

**Reality**: Trust builds in stages. Asking for too much too early kills conversion.

**The Trust Ladder** (each rung requires more trust):
1. Land on page → Professional design, no broken elements
2. Click/explore → Clear navigation, fast load
3. Spend &gt;2 min → Demonstrated value, clear progress
4. Enter info → Why you need it explained, no dark patterns
5. Create account → Privacy visible, minimal fields, clear benefit
6. Pay money → Guarantee, testimonials, recognizable processor

**Detection**: Asking for account creation before demonstrating value

### Identity Mismatch

**Novice thinking**: "Broad appeal = more users"

**Reality**: When everyone is the target, no one feels targeted.

**What to use instead**:
| Signal Type | How It Works |
|-------------|--------------|
| Visual identity | Dark mode = "power user"; Soft pastels = "wellness" |
| Language/tone | "Crush your goals" vs "Find your balance" |
| Social proof | Company logos vs individual testimonials |
| Complexity | Minimal = simplicity-seeker; Feature-rich = power user |

**Detection**: Homepage tries to appeal to 3+ different personas

---

## Self-Contained Tools

### Analysis Workflow

1. **Read** the landing page content and structure
2. **WebFetch** the target URL to analyze live content
3. **Write** analysis results to a markdown file
4. **Edit** recommendations into actionable copy changes

### Appeal Scorer Script

Run: `python scripts/appeal_scorer.py <url>`

Produces structured JSON output with scores and recommendations.

### Reference Files (See for deep dives)

| File | When to Use |
|------|-------------|
| `references/scoring-templates.md` | Full scoring matrices and templates |
| `references/trust-ladder.md` | Deep dive on trust building stages |
| `references/identity-signals.md` | Visual/verbal identity signal catalog |
| `references/objection-catalog.md` | Common objections by product type |

---

## Output Format

When running this skill, produce:

1. **Executive Summary** - 3 bullet key findings
2. **Desirability Triangle Scores** - Per persona
3. **5-Second Test Assessment** - What's clear, what's not
4. **Top 3 Objections** - And how to address them
5. **Priority Recommendations** - Immediate / Medium / Long-term

---

## Integration with ux-friction-analyzer

**Appeal + Friction = Complete picture**

| This Skill Answers | ux-friction-analyzer Answers |
|--------------------|------------------------------|
| "Do they want it?" | "Can they use it?" |
| Will they choose this over alternatives? | Can they complete the task? |
| Does it feel made for them? | Does the flow make sense? |
| Is the promise compelling? | Is the experience smooth? |

**Run both**: High appeal + high friction = frustrated users. Low friction + low appeal = abandoned product.

---

**Philosophy**: A product with low friction but low appeal gets abandoned. A product with high appeal but high friction gets frustrated users. You need both.
