---
name: competitive-intel
description: >
  Research and analyze competitors to find positioning gaps and strategic
  opportunities. Use this skill whenever the user mentions competitors,
  competitive analysis, competitor teardown, market landscape, 'who else does
  this', 'how are we different', or competitor research. Also trigger when the
  user is entering a new market, when positioning feels weak or generic, when
  preparing for a launch, when any downstream skill needs competitors.md but it
  doesn't exist, or when the user asks about differentiation or market gaps.
  Even if the user just names a competitor casually ('what does X do?'), this
  skill likely applies. Three modes: Quick Scan, Deep Teardown, Gap Finder.
---

> **Note:** Examples below use fictional brands (Acme, Lumi, Helm). Replace with your own brand context.

# /competitive-intel -- Know What You're Up Against

You can't differentiate if you don't know what you're differentiating FROM.
Most founders either ignore competitors entirely ("we have no competition") or
obsess over features without understanding messaging.

This skill maps the competitive landscape at the messaging level. Not feature
comparison tables  -  positioning, angles, language, channels, and gaps. The
output feeds directly into positioning-angles and keyword-research to find
white space.

No SaaS tools needed. Systematic web research.

---


## On Activation

1. Check if `brand/` directory exists in the project root.
2. If it does, read available files: `voice-profile.md`, `positioning.md`, `audience.md`, `competitors.md`, `creative-kit.md`, `stack.md`, `learnings.md`.
3. Apply any loaded brand context to enhance research quality  -  use existing audience and positioning data to focus the competitive scan.
4. If `brand/` does not exist, proceed without it  -  this skill works standalone.
5. Read `brand/landscape.md` if it exists  -  check the Claims Blacklist before making ecosystem or competitive claims. If stale (>14 days) or missing, warn that market claims may be outdated.

---

## Iteration Detection

Before starting, check whether `./brand/competitors.md` already exists.

### If competitors.md EXISTS --> Update Mode

Do not start from scratch. Instead:

1. Read the existing competitive intel.
2. Present a summary of current landscape:
   ```
   EXISTING COMPETITIVE INTEL
   Last updated {date} by /competitive-intel

   Competitors analyzed: {N}
   ├── {Competitor 1}    Threat: {level}
   ├── {Competitor 2}    Threat: {level}
   └── {Competitor 3}    Threat: {level}

   Primary gap: {one-line from frontmatter}

   ──────────────────────────────────────────────

   What would you like to do?

   1. Refresh with new web research
   2. Add new competitors
   3. Re-run gap analysis only
   4. Full rebuild from scratch
   ```

3. Process the user's choice:
   - Option 1 --> Re-search existing competitors for updated messaging, pricing, content
   - Option 2 --> Identify new competitors, run teardown, merge into existing file
   - Option 3 --> Use existing teardown data, re-run gap analysis with fresh eyes
   - Option 4 --> Full process from scratch

4. Before overwriting, show what changed and ask for confirmation.

### If competitors.md DOES NOT EXIST --> Full Research Mode

Proceed to the full process below.

---

## The core job

Map who you're competing against, how they position themselves, where they're
strong, where they're weak, and where the gaps are. The output is a strategic
asset that positioning-angles and keyword-research build on.

---

## Mode selection

### Quick Scan (5 minutes)

When you just need to know who the competitors are. Identify 5-8 competitors,
capture their headline positioning, and note obvious gaps. Good for early
exploration.

### Deep Teardown (15-20 minutes)

Full analysis of 3-5 key competitors. Messaging, pricing, channels, content
strategy, SEO footprint. Use when preparing for positioning or launch.

### Gap Finder (10 minutes)

Start from the teardown data and focus exclusively on finding underexploited
territory. Use after a Deep Teardown or when competitors.md already exists.

---

## The competitive research process

### Step 1: Identify competitors

Three categories:

**Direct competitors**  -  solve the same problem for the same audience
- Same product category, same target market
- The ones your customers would name if asked "what else did you consider?"

**Indirect competitors**  -  solve the same problem differently
- Different approach, same outcome
- Includes DIY, hiring a person, using a different category of tool

**Aspirational competitors**  -  where you want to be
- Larger companies in adjacent spaces
- Brands whose positioning or execution you admire
- Not necessarily competitive, but instructive

**How to find them:**
1. Ask the user: "Who do you consider your top 3 competitors?"
2. If Exa available (`exa-search` / `company-research` / Exa MCP): search for "[product category] + [target market]"
3. Search for "[product type] alternatives" and "[product type] vs"
4. Check Product Hunt, G2, Capterra for the product category
5. Look at who ranks for the target keywords

### Step 2: Competitor teardown framework

For each key competitor (3-5), analyze the following (see `references/competitive-frameworks.md` for the full messaging teardown checklist, 2x2 map templates, and gap taxonomy):

**Positioning & Messaging:**
- Homepage headline  -  what's the primary claim?
- Tagline  -  how do they summarize their value?
- Hero copy  -  what transformation do they promise?
- Key differentiator  -  what makes them "the one that [X]"?

**Pricing & Packaging:**
- Pricing model (free, freemium, subscription, one-time)
- Price points and tier names
- What gates the upgrade? (features, usage, support)

**Content & Channels:**
- Blog: topics, frequency, quality, SEO focus
- Social: which platforms, posting frequency, engagement level
- Email: do they have a newsletter? lead magnets?
- Video: YouTube presence, production quality

**SEO Footprint:**
- What keywords do they appear to target?
- Do they have programmatic SEO pages?
- How strong is their content operation?

**Strengths & Weaknesses:**
- What do they do exceptionally well?
- Where are the obvious gaps in their approach?
- What do their users complain about? (check reviews, Reddit, Twitter)

### Step 3: Build the competitive landscape map

```
──────────────────────────────────────────────────

  COMPETITIVE LANDSCAPE

──────────────────────────────────────────────────

  Direct Competitors
  ├── [Competitor 1]
  │   ├── Positioning: "[their headline]"
  │   ├── Strength: [what they do well]
  │   └── Weakness: [where they fall short]
  ├── [Competitor 2]
  │   ├── Positioning: "[their headline]"
  │   ├── Strength: [what they do well]
  │   └── Weakness: [where they fall short]
  └── [Competitor 3]
      ├── Positioning: "[their headline]"
      ├── Strength: [what they do well]
      └── Weakness: [where they fall short]

  Indirect Competitors
  ├── [Alternative 1]  -  [how they solve it differently]
  └── [Alternative 2]  -  [how they solve it differently]

──────────────────────────────────────────────────
```

### Step 4: Find the gaps

This is the payoff. Cross-reference all competitor messaging to find:

**Messaging gaps**  -  what nobody is saying:
- Claims that are true for your product but no competitor makes
- Audiences that nobody specifically targets
- Pain points that nobody directly addresses
- Angles that are conspicuously absent

**Positioning gaps**  -  where nobody lives:
- Map competitors on 2x2 matrices (e.g., simple↔complex × cheap↔expensive)
- Find the quadrant with no competitor
- Identify the "anti-positioning"  -  what would be the opposite of every competitor?

**Channel gaps**  -  where nobody shows up:
- Platforms where the audience exists but competitors don't post
- Content formats nobody uses (video, podcast, interactive tools)
- Communities nobody engages with

**Pricing gaps**  -  where nobody charges:
- Price points between existing tiers
- Packaging models nobody offers (lifetime, usage-based, free tier)

### Step 5: Synthesize differentiation opportunities

Rank the gaps by:
1. **Relevance**  -  does this gap matter to our audience?
2. **Defensibility**  -  can we own this position long-term?
3. **Clarity**  -  can we explain this in one sentence?

Present top 3-5 differentiation opportunities with a starred recommendation.

---

## Output format

Write `./brand/competitors.md` with this structure:

```markdown
---
title: Competitive Intelligence
type: competitive-intel
skill: competitive-intel
date: [ISO date]
competitors_analyzed: [number]
primary_gap: [one-line summary of biggest opportunity]
---

# Competitive Intelligence  -  [Product/Project Name]

## Competitor Teardowns

### [Competitor 1 Name]
- **URL:** [url]
- **Positioning:** "[their headline/tagline]"
- **Pricing:** [model and price points]
- **Strengths:** [what they do well]
- **Weaknesses:** [where they fall short]
- **Content:** [channels and quality]
- **Threat level:** [low/medium/high]

### [Competitor 2 Name]
[Same structure]

---

## Competitive Landscape

### Saturated Claims (everyone says this)
- "[Claim]"
- "[Claim]"

### Partially Claimed (1-2 competitors)
- "[Claim]"  -  used by [Competitor]

### Underexploited Territory
- [Gap 1]
- [Gap 2]
- [Gap 3]

---

## Differentiation Opportunities

1. ★ **[Top opportunity]**  -  [why this is the best gap to own]
2. **[Second opportunity]**  -  [reasoning]
3. **[Third opportunity]**  -  [reasoning]

---

## 2x2 Positioning Map

[Simple/Complex] × [Affordable/Premium]

| | Simple | Complex |
|---|---|---|
| **Premium** | [Competitor] | [Competitor] |
| **Affordable** | ★ **Gap** | [Competitor] |
```

---

## Progressive enhancement levels

| Level | Context Available | Output Quality |
|-------|------------------|---------------|
| L0 | Product name only | Basic competitor list, surface-level analysis |
| L1 | + product description, target market | Focused competitor search, relevant comparisons |
| L2 | + audience.md, voice-profile.md | Audience-aware analysis, positioning-aware gaps |
| L3 | + web research via `exa-search` / `company-research` | Live data, real messaging, verified claims |
| L4 | + existing competitors.md (update) | Evolved intel with trend tracking over time |

---

## Worked Example

**Quick Scan: Verified meal delivery market**

| Competitor | Positioning | Pricing | Strength | Weakness |
|---|---|---|---|---|
| DoorDash | General delivery, verification filter buried | $3-6 delivery + markup | Massive selection | No source verification |
| Sourcify.com | Restaurant directory, no delivery | Free listings | Trusted brand, 20yr history | No ordering, just reviews |
| VerifiedEats | Verified-source-only delivery, 3 cities | $5 delivery + 15% markup | Source-certified restaurants | Tiny coverage area |

**Gap found:** No one owns 'verified-source + affordable delivery + nationwide.' DoorDash has reach but no trust. Sourcify has trust but no delivery. Acme can own the intersection.

---

## What this skill is NOT

- **Not a feature comparison**  -  Feature matrices are commodity analysis. This skill maps messaging, positioning, and strategic gaps  -  the layer that actually drives differentiation decisions.
- **Not market research**  -  This focuses on competitive messaging and positioning. For audience research, use /audience-research. For market sizing and trend analysis, that's a different skill.
- **Not a one-time snapshot**  -  Competitors evolve their messaging. Run this again before major launches, after competitor funding rounds, or when your positioning feels stale.
- **Not a strategy document**  -  The output is intelligence, not a plan. Use /positioning-angles to act on the gaps this skill finds.

---

## Output presentation

### Header

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  COMPETITIVE INTELLIGENCE
  [Product/Project Name]
  Generated [Month Day, Year]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Files Saved

```
  FILES SAVED

  ./brand/competitors.md             ✓
```

### What's Next

```
  WHAT'S NEXT

  Your competitive landscape is mapped with {N}
  competitors analyzed and {N} gaps identified.
  Recommended moves:

  -> /positioning-angles   Exploit the gaps with
                           differentiated angles
                           (~15 min)
  -> /keyword-research     Find content territory
                           competitors miss (~15 min)
  -> /direct-response-copy Write copy that attacks
                           competitor weaknesses
                           (~15 min)

  Or tell me what you're working on and
  I'll route you.
```

---

## Web search fallback

If web search / Exa (`EXA_API_KEY` / MCP) is unavailable:

1. Ask the user for competitor names and URLs directly.
2. If the user provides URLs, attempt to fetch and analyze them.
3. If no URLs available, build the analysis from user knowledge, brand/ files, and general market understanding.
4. Note the limitation clearly: "Competitive analysis is based on provided information and general market knowledge, not live web research. Verify claims before making strategic decisions."
5. Prefix unverified claims with "Estimated:" to signal uncertainty.

---

## Feedback Collection

After delivering the competitive intel:

```
  How did this land?

  a) Great -- using this analysis as-is
  b) Good -- added some competitors I know
  c) Rewrote significantly
  d) Haven't used yet
```

**Processing feedback:**
- **(a) Great:** Log to `./brand/learnings.md` with key gaps found.
- **(b) Good:** Ask which competitors they added. Update competitors.md if they share details.
- **(c) Rewrote:** Ask for the final version. Analyze differences. Offer to update competitors.md.
- **(d) Haven't used:** Note it. Remind next time.

---

## Safety rules

- Never fabricate competitor data  -  positioning decisions built on false competitive intel lead to differentiation claims that collapse on contact with the market. If you can't verify a claim, say so.
- Never present assumptions as facts  -  the user may make pricing, positioning, or launch decisions based on this analysis. Mark unverified information clearly so they know what to double-check.
- Never copy competitor content verbatim beyond short quotes  -  this is analysis, not plagiarism. Short quotes for messaging analysis are fair use; copying blocks of content is not.
- Never write competitive data from one project into another project's brand/  -  competitive landscapes are project-specific. Cross-contamination corrupts strategy.
- Always check `--cwd` context if provided  -  the working directory determines which brand/ to read and write.
- If Exa is unavailable, follow the web search fallback section above - the skill still produces useful output from user knowledge and brand files.
- Focus on messaging and positioning, not feature-by-feature comparisons  -  feature tables are commodity analysis anyone can build. Messaging-level competitive intel is what drives differentiation and is much harder to find elsewhere.
