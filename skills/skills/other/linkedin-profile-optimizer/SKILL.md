---
name: linkedin-profile-optimizer
description: Audit and rewrite your LinkedIn profile to attract the right people. Scores each section, rewrites headline and about copy, and includes an AI visibility checklist so you show up in ChatGPT, Perplexity, and Claude search. Use when someone says "optimize my LinkedIn," "LinkedIn profile help," "rewrite my about section," or "how do I show up in AI search."
---

# LinkedIn Profile Optimizer

**Audit your LinkedIn profile and rewrite it to attract the right people — in 15 minutes.**

Most LinkedIn profiles are written for the person who has the profile, not the person who's supposed to find it. This skill fixes that. You'll get a scored audit of every section, three headline rewrites, a full About rewrite in your voice, optimized experience bullets, and an AI visibility checklist — the checklist no other LinkedIn tool includes.

---

## How This Works

You paste your profile. I diagnose what's not working and rewrite it. Every recommendation is specific to what you gave me — no generic advice, no template language.

**What you'll get:**
1. Profile Audit — scored diagnosis with priority order
2. Headline Rewrite — 3 variants with A/B test guidance
3. About Section Rewrite — full rewrite, max 220 words, in your voice
4. Experience Optimization — before/after bullets for your top role(s)
5. AI Visibility Checklist — 8 checks for how well your profile surfaces in AI search

**Time to complete:** 15 minutes if you have your profile handy.

---

## Step 1 — Intake

Ask the user for all of this in a single message:

```
To get started, paste the following in one message:

1. **Current Headline** — exactly as it reads now
2. **Current About section** — the full text (copy from "edit profile")
3. **Top 2–3 Experience entries** — company name, title, and bullet points for each
4. **Featured section** — optional, but helpful if you have one
5. **Who are you trying to attract?** — be specific (e.g., "Series A SaaS founders who need a fractional CMO" not "business owners")
6. **What do you want them to do when they find you?** — one action (book a call, follow you, DM you, apply for a role)
7. **Positioning goal** — which of these: job seeker / client attraction / thought leadership / all three
```

Do not proceed until all seven inputs are provided. If the user is vague on #5 or #6, ask one clarifying question before continuing.

---

## Step 2 — Scan for Buzzwords First

Before scoring, run a buzzword scan. Flag every instance of the following (and any similar) in the user's text:

**Auto-flag list:**
- results-driven, results-oriented
- passionate about, passion for
- dynamic professional
- synergy, synergistic
- leveraging (as noun use)
- comprehensive, robust
- visionary, visionary leader
- thought leader (self-applied)
- seasoned professional
- proven track record
- go-getter
- strategic thinker (unsubstantiated)
- detail-oriented
- team player
- excited to announce, excited to share
- in today's landscape / in this day and age
- game-changing, revolutionary, cutting-edge

Note: "passionate about" is always replaceable with a specific claim. "Results-driven" says nothing. Every flag gets a specific replacement, not just a note.

---

## Step 3 — Output

Deliver all five sections in a single response. Use clear section headers. Keep it dense — no filler, no affirmations, no "great question."

---

### SECTION 1: Profile Audit

Score each of the following sections on a scale of 1–10. After each score, write exactly one sentence of diagnosis — what's working or what's failing.

| Section | Score (/10) | Diagnosis |
|---------|-------------|-----------|
| Headline | — | — |
| About section | — | — |
| Experience (top role) | — | — |
| Featured section | — | — |
| Overall profile fit for stated goal | — | — |

**Total score:** X / 50

**Priority order for fixes:**
List 1–5 in order of highest leverage impact. Format:
```
1. [Section] — [One sentence on why this is the highest priority fix]
2. ...
```

**Scoring guidance:**
- **1–3:** Actively working against the goal (confusing, misleading, or missing entirely)
- **4–6:** Neutral — present but forgettable, won't convert
- **7–8:** Strong — clear and functional, minor sharpening needed
- **9–10:** Exceptional — clear, specific, compelling, and built for the stated audience

Do not give anyone a 9 or 10 unless the copy is genuinely remarkable. Most profiles score between 3–6 on the first pass.

---

### SECTION 2: Headline Rewrite

Write three headline variants. Each one serves a different positioning strategy:

**Variant A — Authority-forward**
Format: `[Role/Title] who [specific outcome they create for their specific audience]`
Example structure: `CFO advisor who helps Series B startups close their first institutional round without losing equity`

**Variant B — Outcome-forward**
Lead with the result, not the role. The person's identity is secondary to what they make happen.
Example structure: `From [problem state] to [outcome state] — [what you do to make it happen]`

**Variant C — Niche-specific**
Own a specific category. Combine audience + method + outcome in a way no one else can claim.
Example structure: `The only [specific descriptor] built for [hyper-specific niche]` or `[Hyper-specific role] for [specific type of company/person]`

After all three variants:

**A/B test recommendation:**
Flag which variant to test first and why. Explain in 2–3 sentences: which goal it supports, who it will and won't attract, and what to watch for in profile views over 30 days.

**Headline constraints:**
- Max 220 characters
- No buzzwords (see scan list above)
- Must contain at least one specific, searchable keyword
- Must make a claim a competitor can't immediately copy

---

### SECTION 3: About Section Rewrite

Write a full rewrite of the About section. Follow this structure exactly:

**Hook (1–2 sentences)**
The first two lines appear before "see more" on mobile. They must stop the right person in their scroll. Lead with a bold, specific claim — not "Hi, I'm [name]." Use Brian Wagner's voice rule: bold contrarian claim or end-result-first.

**Credibility (2–4 sentences)**
Specific, not generic. Not "15 years of experience." Instead: what industries, what companies, what kinds of problems. Ground authority in real patterns, real clients, or real contexts.

**Proof (2–4 sentences)**
Results or patterns — not job titles. Numbers whenever possible. "Helped 3 fintech startups..." beats "experienced in finance." If the user gave you metrics, use them. If they didn't, use the pattern instead and flag that adding a metric here would strengthen the section.

**CTA (1–2 sentences)**
One clear next step. Match it to what the user said they want people to do. Direct, low-friction. Not "feel free to reach out." Instead: "If [specific situation], [specific action] — [how to take it]."

**Constraints:**
- Max 220 words total
- No buzzwords (flag and replace any that appear)
- No first-person opener on the first sentence ("I am" or "I've" — start with the claim, not the person)
- No self-applied adjectives ("passionate," "expert," "seasoned") without proof
- Write like a human, not a LinkedIn template

---

### SECTION 4: Experience Optimization

Rewrite the bullet points for the top 1–2 experience entries the user provided.

**Format for each role:**

```
[Company] | [Title] | [Dates]

BEFORE:
• [Original bullet, verbatim]

AFTER:
• [Rewritten bullet — achievement-first, metric-included, keyword-rich]
```

**Bullet rewrite rules:**
1. **Achievement-first** — Start with the outcome, not the action. "Grew pipeline 40% in 6 months" beats "Responsible for growing pipeline"
2. **Metric-anchored** — Every bullet should have a number, percentage, or scale indicator. If the user didn't provide one, flag it: `[Note: Add a metric here — even a rough one strengthens this significantly]`
3. **Keyword-rich** — Include terms that appear in job postings or searches your target audience would run. Don't keyword-stuff; weave them naturally into the achievement statement
4. **Scannable** — 15 words max per bullet. No paragraphs disguised as bullets
5. **Active verbs only** — "Built," "Grew," "Cut," "Launched," "Closed" — not "Responsible for," "Tasked with," "Helped with"

If the user only gave vague bullets, rewrite what you can and flag where specific data would transform the bullet.

---

### SECTION 5: AI Visibility Checklist

This is the differentiator. Every other LinkedIn optimizer ignores this. AI-powered search engines (ChatGPT, Perplexity, Claude) surface people differently than Google. This checklist tells you how well the profile will surface.

Score each item: ✅ Pass / ⚠️ Needs work / ❌ Missing

Based on what the user shared, assess each check point:

---

**1. Entity Clarity**
Does the profile make it immediately clear who this person is — name, role, and niche — in the first 50 words?
AI models need unambiguous entity data. Profiles that read as "marketing professional" are invisible. Profiles that read as "fractional CMO for Series A SaaS companies" get cited.
→ Pass if: Name + specific role + specific audience appears in headline or opening About lines.

**2. Niche Specificity**
Is there a specific niche claim anywhere on the profile?
AI search rewards specificity because specific claims appear as direct answers to specific queries. "I help B2B companies grow" will never get cited. "I help D2C brands reduce CAC through email list segmentation" might.
→ Pass if: There's at least one hyper-specific claim about audience + method + outcome.

**3. Third-Party Mentions**
Are there any mentions of external validation — media, press, podcasts, publications, companies worked with, or named clients?
AI models cite profiles that have social proof from external sources. "As featured in Forbes" or "former [Company]" creates entity authority.
→ Pass if: At least one external mention exists. Flag if absent — this is a major opportunity.

**4. Content Consistency**
Does the profile's language match what the person posts or publishes?
AI builds entity profiles from multiple data points. If the LinkedIn profile says "growth marketing" but all their posts say "demand gen," the model treats them as two different things.
→ Pass if: Terminology in the profile matches vocabulary used in posts/content the user mentioned.

**5. Direct Answer Language**
Does the About section contain language that directly answers a question someone might type into an AI?
AI search prioritizes copy that reads like an answer. "Brian Wagner helps SaaS founders..." is more citation-ready than "I am a marketer with 15 years of experience."
→ Pass if: At least one sentence reads like the answer to a specific question.

**6. Recency Signals**
Is there current activity on the profile — recent posts, updated experience, recent dates?
AI models deprioritize stale profiles. A profile last updated in 2022 with no recent posts is invisible.
→ Pass if: Experience is current, dates are accurate, and there's evidence of recent activity.

**7. URL / Name Match**
Does the LinkedIn URL match the person's name exactly (or close to it)?
Custom URLs improve discoverability and entity matching. `linkedin.com/in/john-smith-cfo` outperforms `linkedin.com/in/jsmith8734` every time.
→ Pass if: Custom URL is set and matches name + optional role keyword.

**8. Cross-Platform Footprint**
Does the same name + positioning appear on other platforms — website, Twitter/X, Substack, GitHub, podcast appearances?
AI models triangulate identity across platforms. A person who appears as "Jane Doe, fractional CMO" on LinkedIn, their website, and Twitter is treated as a high-authority entity.
→ Pass if: User confirmed they have consistent positioning elsewhere, OR flag this as the #1 off-LinkedIn move to make.

---

**AI Visibility Score:** X / 8

**Top 3 moves to improve AI visibility right now:**
Based on the failed checks, give the three most actionable improvements. Be specific — not "improve your profile" but "add one line to your About section that starts 'Jane Doe helps [specific audience]...'"

---

## Step 4 — Close

After delivering all five sections, end with this exact framing:

```
That's your full LinkedIn optimization package.

What's next?

A) Refine any section — tell me which one and what direction
B) Write 5 LinkedIn posts that match the new positioning (so your content reinforces the profile)
C) Done — you're good to go

Which one?
```

Wait for their response before proceeding.

---

## If They Choose B — LinkedIn Posts

Write 5 LinkedIn posts that reinforce the new positioning. Each post should:

1. Match the voice and positioning established in the About rewrite
2. Target the same audience the user defined in intake
3. Use a different format: (1) personal story, (2) numbered list, (3) contrarian take, (4) client result/pattern, (5) direct CTA post
4. Not mention the LinkedIn profile explicitly — these are standalone posts, not profile promos
5. Follow these rules:
   - Opening line is a hook — bold claim or end-result-first
   - No buzzwords (see scan list)
   - Short paragraphs, lots of whitespace
   - One CTA per post, matching the stated goal
   - Not starting any post with "I" as the first word

---

## Guardrails (Always Active)

**Buzzword zero tolerance:** Any instance of "results-driven," "passionate," "dynamic," "synergy," or similar — flag it explicitly and replace it with something specific. Don't note it in passing; call it out visibly.

**Specificity mandate:** Every recommendation must connect directly to what the user gave you. No advice that could apply to anyone. "Strengthen your headline" is not advice. "Change 'marketing professional' to 'email strategist for 7-figure D2C brands'" is advice.

**Voice integrity:** Write copy that sounds like a human wrote it. If a sentence could appear in a LinkedIn template, rewrite it.

**No fabrication:** If the user gave you no metrics, no external proof, no specific clients — don't invent them. Flag where they'd be helpful and tell the user exactly what to add.

**Honesty in scoring:** Score what they actually gave you, not what you wish they had. A profile that scores 3/10 should be told clearly — with a priority roadmap, not softened with "great foundation."

---

## Compatibility

| Platform | Works? |
|----------|--------|
| Claude Code | ✅ |
| OpenClaw | ✅ |
| Claude.ai | ✅ (paste SKILL.md) |
| ChatGPT | ✅ (paste SKILL.md) |
| GitHub Copilot | ✅ |

---

*Version 1.0.0 — LinkedIn Profile Optimizer*
*Part of the AI Marketing Skills library by Brian Wagner*
*[github.com/BrianRWagner/ai-marketing-skills](https://github.com/BrianRWagner/ai-marketing-skills)*
