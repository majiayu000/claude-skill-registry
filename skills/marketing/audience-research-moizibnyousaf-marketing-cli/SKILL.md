---
name: audience-research
description: >
  Build detailed buyer personas and audience profiles from research. Use this
  skill whenever the user mentions audience, buyer persona, ideal customer,
  target market, ICP, watering holes, 'who am I selling to', customer research,
  or audience profile. Also use when content feels unfocused or generic (that's
  an audience problem), when conversion is low because messaging doesn't
  resonate, when starting any new project (audience should be first), or when
  any downstream skill needs audience.md but it doesn't exist yet. Even if the
  user doesn't explicitly ask for audience research, trigger this if they're
  writing copy or building a landing page without a clear audience defined.
  Three approaches: Quick Profile, Persona Build, Community Mining.
---

> **Note:** Examples below use fictional brands (Acme, Lumi, Helm). Replace with your own brand context.

# /audience-research -- Know Who You're Talking To

Every marketing skill gets better when you know your audience. Generic copy
happens when you write for "everyone." Specific copy that converts happens
when you write for a real person with real problems.

This skill builds that audience profile. It's the foundation  -  8 of 11 content
skills read `audience.md` to shape their output. Running this first makes
everything downstream sharper.

No SaaS tools needed. Systematic research plus web search.

---


## On Activation

1. Check if `brand/` directory exists in the project root.
2. If it does, read available files: `voice-profile.md`, `positioning.md`, `audience.md`, `competitors.md`, `creative-kit.md`, `stack.md`, `learnings.md`.
3. Apply any loaded brand context to enhance output quality  -  skip questions the user has already answered.
4. If `brand/` does not exist, proceed without it  -  this skill works standalone.

---

## Iteration Detection

Before starting, check whether `./brand/audience.md` already exists.

### If audience.md EXISTS --> Update Mode

Do not start from scratch. Instead:

1. Read the existing audience profile.
2. Present a summary of current personas:
   ```
   EXISTING AUDIENCE PROFILE
   Last updated {date} by /audience-research

   Personas:
   ├── {Persona 1 name}    {one-liner}
   ├── {Persona 2 name}    {one-liner}
   └── Primary: {primary persona name}

   Watering holes: {N} mapped

   ──────────────────────────────────────────────

   What would you like to do?

   1. Refine existing personas with fresh research
   2. Add a new persona segment
   3. Deep-dive into watering holes
   4. Full rebuild from scratch
   ```

3. Process the user's choice:
   - Option 1 --> Re-run research for existing personas, update with new data
   - Option 2 --> Identify the new segment, build persona, merge into existing file
   - Option 3 --> Focus on community mining for existing personas
   - Option 4 --> Full process from scratch

4. Before overwriting, show what changed and ask for confirmation.

### If audience.md DOES NOT EXIST --> Full Research Mode

Proceed to the full process below.

---

## The core job

Build a complete picture of who buys this product, why they buy it, where they
hang out, and what language they use. The output is structured enough for other
skills to parse but human enough to be useful for strategy.

---

## Approach selection

Choose based on what's available:

### Quick Profile (L0  -  zero context)

When no brand files exist and minimal information is provided. Ask 5 key questions:

1. **What does your product do?** (one sentence)
2. **Who currently uses it?** (or who do you want to use it?)
3. **What problem does it solve?** (the pain before, the relief after)
4. **What alternatives exist?** (what would they do without you?)
5. **What's the price point?** (free, $10/mo, $500/mo, enterprise?)

From these 5 answers, generate a working persona. It won't be perfect but it
gives every downstream skill something to work with.

### Persona Build (L1-L2  -  some context)

When you have basic product info or existing brand files. Systematic persona
construction using demographics, psychographics, and jobs-to-be-done.

### Community Mining (L3-L4  -  full research)

When `exa-search` / Exa MCP or web search is available. Deep research into where the audience
lives online, what language they use, what they complain about, and what they
aspire to.

---

## The audience research process

### Step 1: Identify the transformation

Same as positioning  -  start with the outcome, not the product.

- What does the customer's life look like BEFORE? (the pain state)
- What does it look like AFTER? (the desired state)
- What's the gap between those two states?

The gap defines who your audience is: people stuck in the BEFORE state who want
the AFTER state but haven't found a good way to get there.

### Step 2: Build buyer personas

For each distinct audience segment (usually 1-3), build:

**Demographics** (who they are):
- Role/title, company size, industry
- Age range, income level, location
- Technical sophistication

**Psychographics** (how they think):
- Goals and aspirations
- Fears and frustrations
- Values and beliefs about this category
- How they make decisions (data-driven, social proof, gut feel)

**Jobs-to-be-done** (why they hire your product  -  see `references/jtbd-framework.md` for the full framework, Forces of Progress, and job mapping template):
- Functional job: What task are they trying to accomplish?
- Emotional job: How do they want to feel?
- Social job: How do they want to be perceived?

**Language patterns** (how they talk):
- Words they use to describe their problem
- Jargon level (none, industry-standard, expert)
- Tone they respond to (casual, professional, irreverent)

### Step 3: Find watering holes

Where does this audience already gather? This is where you'll distribute content.

**Search process** (use `exa-search` / Exa MCP when available):
1. Search for "[problem/topic] + reddit/forum/community"
2. Search for "[job title/role] + newsletter/podcast/blog"
3. Search for "[competitor name] + reviews/alternatives"
4. Look at who engages with competitor content on social platforms

**Map the landscape:**

```
──────────────────────────────────────────────────

  AUDIENCE WATERING HOLES

──────────────────────────────────────────────────

  Online Communities
  ├── r/[subreddit]  -  [activity level, relevance]
  ├── [Forum/Discord]  -  [activity level, relevance]
  └── [Facebook Group]  -  [activity level, relevance]

  Content They Consume
  ├── [Newsletter]  -  [subscriber count if known]
  ├── [Podcast]  -  [relevance]
  └── [Blog/Publication]  -  [relevance]

  Social Platforms
  ├── [Platform]  -  [how they use it]
  └── [Platform]  -  [how they use it]

  Events & Conferences
  └── [Event]  -  [relevance]

──────────────────────────────────────────────────
```

### Step 4: Map pain points and objections

For each persona, identify:

**Pain points** (what hurts today):
- What triggers the search for a solution?
- What's the cost of NOT solving this? (time, money, stress)
- What have they tried before that didn't work?

**Objections** (what stops them from buying):
- Price objections: "Is it worth the money?"
- Trust objections: "Will this actually work for me?"
- Effort objections: "Is this going to be hard to implement?"
- Timing objections: "Is now the right time?"
- Alternative objections: "Can I just do this myself?"

### Step 5: Identify language mines

Search for actual quotes from the audience  -  Reddit posts, review sites, forum
threads, social media. These are gold for copywriting.

Look for:
- How they describe their problem (use their exact words)
- Emotional language they use (frustrated, overwhelmed, stuck)
- Aspirational language (wish I could, dream of, finally)
- Comparison language (better than, unlike, switch from)

---

## Output format

Write `./brand/audience.md` with this structure. The `## Archetypes` block at the top is the structured contract consumed by Studio's archetype-pulse-cards and any future skill that needs a card-shaped persona summary. The fuller persona blocks below it carry the long-form context.

```markdown
---
title: Audience Profile
type: audience-research
skill: audience-research
date: [ISO date]
personas: [number]
primary_persona: [name]
archetypes: [number]
---

# Audience Profile  -  [Product/Project Name]

## Archetypes

Card-shaped summary of every persona. One archetype per persona. Required fields per archetype: `name`, `one_liner`, `demographic`, `top_pain`, `top_desire`, `watering_hole`, `language_quote`. Do not skip fields. If you do not have evidence for one, write "not measured" rather than fabricating.

### Archetype: [Name]

- **one_liner:** [Who they are and what they want, one sentence]
- **demographic:** [Role, company size, technical level  -  single line]
- **top_pain:** [The single biggest pain in their words]
- **top_desire:** [The single biggest goal in their words]
- **watering_hole:** [Primary community / channel where they live]
- **language_quote:** [One actual quote or representative phrase, in quotes]

### Archetype: [Name 2]

[Same six fields. Repeat for each persona.]

---

## Primary Persona: [Name]

**One-liner:** [Who they are and what they want in one sentence]

### Demographics
- **Role:** [title/role]
- **Company:** [size/type]
- **Technical level:** [low/medium/high]

### Psychographics
- **Goals:** [what they want]
- **Fears:** [what keeps them up at night]
- **Values:** [what they believe about this category]

### Jobs-to-be-Done
- **Functional:** [task they need done]
- **Emotional:** [how they want to feel]
- **Social:** [how they want to be perceived]

### Pain Points
1. [Pain point with emotional context]
2. [Pain point with emotional context]
3. [Pain point with emotional context]

### Objections
1. [Objection] → [How to address it]
2. [Objection] → [How to address it]

### Language Mines
> "[Actual quote or representative language]"
> "[Actual quote or representative language]"

---

## Watering Holes

[Community map from Step 3]

---

## Secondary Persona: [Name] (if applicable)

[Same structure, abbreviated]
```

---

## Progressive enhancement levels

| Level | Context Available | Output Quality |
|-------|------------------|---------------|
| L0 | Nothing  -  5 questions only | Working persona, generic watering holes |
| L1 | Product info + basic brand files | Targeted persona, category-specific insights |
| L2 | + competitor data from competitors.md | Differentiated personas, competitive gaps |
| L3 | + web research via `exa-search` | Real quotes, verified watering holes, data-backed |
| L4 | + existing audience.md (refinement) | Evolved personas with historical learning |

---

## Worked Example

**Project:** Acme (verified meal delivery app)

**Persona: Sarah, the Busy Parent**
- Age: 32, lives in suburbs, works part-time
- Pain: 'I spend 30 minutes every night figuring out what's organic on DoorDash'
- Goal: Feed her family verified-source food without the mental load
- Watering holes: health-conscious parent Facebook groups, verified-source food Instagram, neighborhood Slack
- Language mine: 'I just want to order without checking every single ingredient'
- Buying trigger: Sees a friend post about it in her WhatsApp group

**Persona: Ahmed, the College Student**
- Age: 20, lives on campus, limited budget
- Pain: 'The only verified-source option near me is one overpriced restaurant'
- Goal: Affordable verified-source food delivered to his dorm
- Watering holes: r/EatCheapAndHealthy, campus food subreddit, TikTok
- Language mine: 'Why is verified-source food always 2x the price?'

---

## What this skill is NOT

- **Not persona fiction**  -  Every claim must come from research, user input, or web data. Never invent demographics or psychographics to fill gaps.
- **Not audience.md only**  -  This skill writes the file, but the real output is strategic understanding of who buys and why.
- **Not market research**  -  This focuses on buyer personas and watering holes. For competitive landscape, use /competitive-intel. For market sizing and trends, that's a different analysis.
- **Not a one-time exercise**  -  Personas evolve. Run this again when conversion drops, when expanding to new segments, or when feedback contradicts existing personas.

---

## What's Next

After writing audience.md, present:

```
  WHAT'S NEXT

  Your audience profile is set. Every downstream
  skill will use these personas. Recommended moves:

  -> /positioning-angles   Find the angle that
                           resonates with this
                           audience (~15 min)
  -> /competitive-intel    Map competitors your
                           audience is comparing
                           you against (~10 min)
  -> /keyword-research     Find what this audience
                           searches for (~15 min)

  Or tell me what you're working on and
  I'll route you.
```

---

## Feedback Collection

After delivering the audience profile:

```
  How did this land?

  a) Great -- using these personas as-is
  b) Good -- tweaked some details
  c) Rewrote significantly
  d) Haven't used yet
```

**Processing feedback:**
- **(a) Great:** Log to `./brand/learnings.md` with persona names and context.
- **(b) Good:** Ask what changed. Log the adjustment to learnings.md.
- **(c) Rewrote:** Ask for the final version. Analyze differences. Offer to update audience.md with their version.
- **(d) Haven't used:** Note it. Remind next time.

---

## Safety rules

- Never fabricate quotes  -  downstream skills use language mines as real customer voice in copy. Fabricated quotes produce inauthentic messaging that erodes trust. Mark web-sourced language as "representative" if paraphrased.
- Never assume demographics without evidence  -  persona decisions drive targeting, pricing, and channel strategy. Wrong demographics cascade into wrong marketing. Ask or research.
- Never write audience data from one project into another project's brand/  -  audience profiles are project-specific. Cross-contamination means one project's strategy infects another.
- Always check `--cwd` context if provided  -  the working directory determines which brand/ to read and write.
- If Exa is unavailable, skip web research steps and note the limitation - the skill still produces useful output at L0-L2, just without verified watering holes and real quotes.
