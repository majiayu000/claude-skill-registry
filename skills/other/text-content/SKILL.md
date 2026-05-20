---
name: text-content
description: Create high-performing text posts for social media using framework fitting method. 360+ proven templates across LinkedIn, X, Facebook, and Instagram. Progressive disclosure loads only relevant templates based on platform and content type.
---

# Text Content Creator

## Purpose

Transform source content into platform-optimized social posts using **framework fitting** - matching concepts to proven templates that amplify them. Covers LinkedIn long-form, X punchy tweets, Facebook engagement posts, Instagram captions, and one-liners.

**Core Philosophy:** Good content follows proven formats. The skill is matching concepts to the delivery mechanisms that amplify them best - not writing from scratch.

## When to Use

- Creating LinkedIn posts from any source content
- Writing X/Twitter posts or threads
- Facebook text posts and question posts
- Instagram captions (not video - use `short-form-video` for that)
- One-liners for easels, signs, or quick social
- Multiplying high-performing posts into variations

**NOT for:**
- Short-form video (use `short-form-video` skill)
- Video captions/on-screen text (use `video-caption-creation` skill)
- Blog posts or long-form articles

---

## The Framework Fitting Method

### Step 1: Extract the Concept

Before choosing a template, understand what you're working with.

**From source content, extract:**
- **Core insight** (one sentence)
- **Emotional hook** (what feeling does this evoke?)
- **Target reader** (who needs to hear this?)
- **Transformation** (what changes for the reader?)

### Step 2: Choose Platform and Format

**Platform selection question:** "Where does our target reader spend time?"

| Platform | Best For | Character Sweet Spot |
|----------|----------|---------------------|
| **LinkedIn** | Thought leadership, professional insight, stories | 200-500 words |
| **X/Twitter** | Punchy takes, quotable insights, threads | 70-100 chars (posts), threads for depth |
| **Facebook** | Engagement bait, questions, community | 40-140 chars |
| **Instagram** | Captions for visuals, micro-stories | 30-125 chars |

**Format selection question:** "What job does this post need to do?"

| If the job is... | Format |
|------------------|--------|
| Start a conversation | Engagement post (question, poll, agree/disagree) |
| Make them feel something | Story post (failure, transformation, day-in-life) |
| Give them something useful | List/Tips post (how-to, mistakes, frameworks) |
| Challenge what they believe | Contrarian post (hot take, call BS, flip expectation) |
| Establish credibility | Authority post (data, process reveal, pro tip) |
| Build relationships | Community post (shoutout, welcome, give away) |
| Stop the scroll quickly | One-liner (sign, easel, caption) |

### Step 3: Load the Right Reference

**IMPORTANT: Load only ONE reference at a time.** Each is 1000-3000 words.

#### For LinkedIn (Long-Form Thought Leadership)

LinkedIn has 118 templates across 6 categories. Load based on job-to-be-done:

| Job | Load | Template Count |
|-----|------|----------------|
| Drive comments | `references/linkedin/engagement.md` | 16 templates |
| Emotional connection | `references/linkedin/story.md` | 24 templates |
| Scannable value | `references/linkedin/list.md` | 17 templates |
| Pattern interrupt | `references/linkedin/contrarian.md` | 20 templates |
| Build credibility | `references/linkedin/authority.md` | 26 templates |
| Relationship building | `references/linkedin/community.md` | 15 templates |

#### For X/Twitter (Short and Punchy)

| Need | Load | Template Count |
|------|------|----------------|
| General post templates | `references/templates/post-structures.md` | 100+ templates |
| One-liners/takes | `references/templates/one-liners.md` | 12 patterns |
| Platform heuristics | `references/platforms/x-twitter.md` | - |

#### For Facebook (Engagement Focus)

| Need | Load |
|------|------|
| Post templates | `references/templates/post-structures.md` |
| Question/engagement templates | `references/linkedin/engagement.md` |
| Platform heuristics | `references/platforms/facebook.md` |

#### For Instagram Captions

| Need | Load |
|------|------|
| Caption templates | `references/templates/one-liners.md` |
| Story captions | `references/linkedin/story.md` (adapt shorter) |
| Platform heuristics | `references/platforms/instagram-captions.md` |

#### For Multiplying Winners

| Need | Load |
|------|------|
| 7 SCAMPER variations | `references/methods/proliferation.md` |
| 8 Human Desires reframes | `references/methods/proliferation.md` |
| Vision/Anti-Vision framing | `references/methods/proliferation.md` |

### Step 4: Match Concept to Templates

**Critical: Avoid First-Match Bias**

Do NOT default to the first template that fits. Review at least 5-10 options.

**For each concept:**
1. Brainstorm how it COULD be presented (beyond the obvious)
2. Review applicable templates from loaded reference
3. Test fit: Does this template amplify the core insight or dilute it?
4. Generate 2-4 framework matches with fit assessment
5. Select best 1-2 for execution

### Step 5: Execute and Adapt

**Templates are starting points, not constraints.**

Each template reference includes:
- The structural skeleton
- Why it works (psychological principle)
- Example execution

**Your job:** Adapt the template to your specific content. Combine elements if that serves the message better.

**Adaptation questions:**
- Does this amplify my core insight or dilute it?
- Does this sound like OpenEd/Ela, or like a template?
- Would Sarah (our target reader) feel seen?

### Step 6: Apply Voice and Quality Check

**Voice Checklist (Before Posting):**
- [ ] No correlative constructions ("isn't just X, it's Y") - #1 AI tell
- [ ] Hyphens with spaces - like this - not em dashes
- [ ] No emojis (or minimal, strategic use)
- [ ] Specific details over generic claims
- [ ] Permission-giving tone, not preachy
- [ ] Conversational - would you text this to a friend?

**AI-isms to Avoid:**
- Arrow bullets (use plain dashes or line breaks)
- "Here's the thing:" / "Let me explain:" throat-clearing
- Staccato fragments: "No fluff. No filler. Just results."
- Words: delve, comprehensive, crucial, leverage, landscape, navigate, foster

**Platform Compliance:**
- [ ] Character count appropriate
- [ ] Links in right place (LinkedIn: comments, Facebook: none)
- [ ] Hashtags appropriate (LinkedIn: 3-5, X: 1-2, Facebook: 0)

For deeper voice guidance, invoke `ghostwriter` skill.

### Step 7: Nearbound Check (Tag Mentioned People)

**Before finalizing any social post, check for taggable handles.**

1. **Identify mentions:** List any people mentioned by name in the post
2. **Search nearbound index:** Check `Studio/Nearbound Pipeline/people/` for profiles
3. **Add handles:**
   - If profile exists → add platform-appropriate @handle
   - If no profile → note name for future profile creation
4. **Platform-specific tagging:**
   - LinkedIn: Use full name or @handle if connected
   - X: Use @handle
   - Instagram: Use @handle in caption

**Why this matters:** Tagging increases reach, strengthens relationships with guests/collaborators, and drives engagement from their audiences.

**Profile creation trigger:** If someone is mentioned 2+ times across content and has no profile, create one in `Studio/Nearbound Pipeline/people/`

---

## Template Quick Index

### General Templates (100+)
`references/templates/post-structures.md`
- 2x3 Comparison, 80/20 Rule, Benefits List, Binary Framing
- Cause and Effect, Commentary, Comparisons, Contrarian
- Headline + List, Heavy Hitting One-Liner, Hook & Sinker
- Identity Post, If-Then, List Post, Observation Post
- Problem-Solution, Story-Based, What-How-Why, Warning
- [100+ more...]

### LinkedIn Swipe File (86)
`references/templates/linkedin-swipe-file.md`
- Agree/Disagree, Before/After, Contrarian, Day in the Life
- Failure Story, Pattern Recognition, This vs That, Shoutout
- [78 more...]

### Justin Welsh Templates (50)
`references/templates/justin-welsh.md`
- Simpler, more concise templates
- Table format with examples

### One-Liner Patterns (12)
`references/templates/one-liners.md`
- Normalize, Stop + Complaint, Everyday Observations
- Relationship Rules, Pop Culture, Mock Instructions
- Wordplay, Existential Questions, Aspirational
- Calendar Commentary, Struggles, Values

### LinkedIn by Category (118)
- Engagement (16): polls, agree/disagree, crowdsource, fill-in-blank
- Story (24): failure, transformation, day-in-life, values
- List (17): tips, 10 ideas, DOs/DONTs, skills lists
- Contrarian (20): hot takes, call BS, state opposite, rants
- Authority (26): how-to, quotes, screenshots, secret sauce
- Community (15): shoutouts, connect, welcome, comedy

---

## Proliferation: Turn 1 Post Into 17

After a post performs well (or before posting to test angles), multiply it.

### SCAMPER (7 variations)
- **S**ubstitute: Swap example, data, or subject
- **C**ombine: Merge with personal story or another concept
- **A**dapt: Expand to thread, carousel, or different format
- **M**odify: Make punchier, longer, or more extreme
- **P**urpose: Angle for different audience segment
- **E**liminate: Remove context, simplify radically
- **R**everse: Flip the frame or argue the opposite first

### Human Desires (8 reframes)
Spin concept through desire lenses:
1. Safety of Tribe
2. Survival & Success
3. Life Enjoyment
4. Social Acceptance
5. Sexual Companionship (rarely applicable)
6. Comfort & Clarity
7. Freedom From Fear
8. Perceived Status

### Vision/Anti-Vision (2-3 frames)
- **Vision framing:** What we're FOR (personalization, autonomy, kids who love learning)
- **Anti-Vision framing:** What we're AGAINST (standardization, gatekeeping, one-size-fits-all)
- **Transformation:** From [anti-vision] to [vision]

**Full details:** `references/methods/proliferation.md`

---

## Platform Quick Reference

### LinkedIn
- **Heuristic:** Thought leadership, vulnerability wins
- **Length:** 200-500 words (long-form outperforms)
- **Links:** Always in comments (not main post)
- **Hashtags:** 3-5 maximum
- **Hook:** First 2 lines critical (shows before "see more")
- **Tags:** Tag mentioned people/orgs (increases reach)

### X/Twitter
- **Heuristic:** "I wish I said that" - retweet-worthy
- **Length:** 70-100 characters optimal
- **Hashtags:** 1-2 maximum
- **Threads:** Use for longer concepts
- **Strategy:** Reply game important at lower follower counts

### Facebook
- **Heuristic:** Comments drive reach
- **Length:** 40-140 characters optimal
- **Links:** NO external links (kills reach)
- **Hashtags:** NO hashtags (Facebook doesn't reward them)
- **Format:** Question posts with background images perform best

### Instagram Captions
- **Heuristic:** Visual-first, caption supports
- **Length:** 30-125 characters for feed
- **Hashtags:** 5-10 relevant hashtags
- **Format:** Micro-story or punchy one-liner

**Full platform guides:** `references/platforms/`

---

## Common Mistakes

**Content Issues:**
- First-Match Bias - picking first template without exploring
- Generic Posts - not using any framework
- Too Many Concepts - multiple ideas in one post
- Missing Context - concept doesn't stand alone

**Framework Issues:**
- Framework Drift - starting with template then abandoning structure
- Mismatched Fit - forcing concept into wrong template
- No Volume - creating only 1 option instead of 5-10

**Platform Issues:**
- Wrong Link Placement - external links in Facebook/LinkedIn main posts
- Hashtag Overload - too many for platform
- Voice Mismatch - too formal for Facebook, too casual for LinkedIn

---

## Parallel Sub-Agent Pattern (For Batch Processing)

When processing multiple snippets or creating content across platforms simultaneously, use parallel sub-agents.

### When to Use Sub-Agents

- Processing hub content into spokes (e.g., newsletter → 6 social posts)
- Creating platform variations of same snippet
- Batch content creation for scheduling

### Sub-Agent Workflow

```
Source Content
    │
    └─→ Extract 3-5 standalone snippets
         │
         ├─→ LinkedIn Sub-Agent (parallel)
         │   └─→ Load TEMPLATE_INDEX.md → 2-3 drafts
         │
         ├─→ X Sub-Agent (parallel)
         │   └─→ Load TEMPLATE_INDEX.md → 2-3 drafts
         │
         ├─→ Instagram Sub-Agent (parallel)
         │   └─→ Load TEMPLATE_INDEX.md → visual + caption
         │
         └─→ Facebook Sub-Agent (parallel)
             └─→ Load TEMPLATE_INDEX.md → engagement post
```

### Sub-Agent Prompts

Full prompts at: `.claude/skills/content-repurposer/references/sub-agents/`

- `linkedin-agent.md` - Authority, story, contrarian formats
- `x-agent.md` - Punchy single tweets and threads
- `instagram-agent.md` - Visual direction + captions
- `facebook-agent.md` - Engagement-driving formats

### Key Files

- **Lightweight index:** `references/templates/TEMPLATE_INDEX.md` (~200 tokens)
- **Full templates:** Load on-demand from `references/` subdirectories

---

## Related Skills

- `short-form-video` - Video production workflow
- `video-caption-creation` - On-screen text and video hooks
- `ghostwriter` - Voice and anti-AI patterns
- `hook-and-headline-writing` - Opening lines
- `quality-loop` - Quality gates for all content
- `linkedin-content` - DEPRECATED: Use this skill with LinkedIn references

---

## Version History

- **v1.0** (2026-01): Consolidated from social-content-creation, linkedin-content, dude-with-sign-writer
  - 360+ templates preserved intact across all references
  - Progressive disclosure: load only relevant templates
  - Platform-specific routing
  - Unified methodology with category-based LinkedIn system

---

*For template updates, add to appropriate reference file and note in version history.*
