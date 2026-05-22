---
name: content-repurposer
description: Specialized framework fitting for multi-platform content distribution. Takes any source content and transforms it into platform-optimized posts with correct voice, context, and tagging. Use when repurposing newsletters, podcasts, articles, or archive content into social posts.
---

# Content Repurposer

Transform source content into platform-optimized posts using framework fitting.

**Core job:** Take content from any source → understand context → extract snippets → match to templates → optimize for each platform.

---

## Context Awareness (Critical)

### Brand Context

**OpenEd is a company, not an individual.**

| Aspect | Implication |
|--------|-------------|
| Voice | Brand account, not personal ("we" not "I") |
| Authority | 125,000+ families, 9 states, tuition-free resources |
| Tone | Helpful expert, not salesy. Permission-giving, not preachy. |
| Identity | Pro-child, not anti-school. Mix and match philosophy. |

**Always load:** `opened-identity` for full brand context.

### Source Context

The source determines voice and framing:

| Source | Voice | Framing | Tagging |
|--------|-------|---------|---------|
| **Podcast guest** | Third person | Make THEM look good | Tag guest on all platforms |
| **Newsletter** | First person plural | "We found..." "Our team..." | Tag mentioned sources |
| **Archive article** | Authority | Fresh angle, current relevance | Tag original author if external |
| **Staff insight** | First person plural | Share the discovery | Internal attribution |

**Podcast guest example:**
```
❌ "I learned so much from Ken Danford..."
✅ "Ken Danford (@northstarteens) explains why..."
✅ "@kendanford's insight on self-directed learning..."
```

---

## The Framework Fitting Process

### Step 1: Identify Source Type

```
What am I repurposing?
├─ Podcast episode → Load guest context, prepare @handles
├─ Newsletter → Extract TTT segments (Thought/Trend/Tool)
├─ Article → Extract key insights, stats, quotes
├─ Archive content → Find fresh angle, check current relevance
└─ Raw insight → Match to template directly
```

### Step 2: Extract Snippets by Type

From any source, identify standalone pieces:

| Snippet Type | What to Extract | Best Templates |
|--------------|-----------------|----------------|
| **hot_take** | Opinion that stands alone | Contrarian, Paradox Hook, Call BS |
| **stat** | Data point + interpretation | Authority, Commentary, Data Story |
| **how_to** | Actionable advice | List, Thread, Tips, Carousel |
| **quote** | Memorable line from source | Quote + Commentary |
| **story** | Transformation arc | Story, Day-in-Life |

### Step 3: Check Nearbound

Before drafting, check for taggable people:

```
1. Identify all names mentioned
2. Search: Studio/Nearbound Pipeline/people/
3. If found → Get @handle for target platform
4. If not found → Note for future profile creation
```

**Priority tags:** Podcast guests, quoted experts, tool/curriculum founders.

### Step 4: Route to Platforms

| Snippet | LinkedIn | X | Instagram | Facebook |
|---------|----------|---|-----------|----------|
| hot_take | Contrarian | Paradox Hook | Quote card | Agree/Disagree |
| stat | Authority | Commentary | Carousel | Question |
| how_to | List | Thread | Carousel | Fill-blank |
| quote | Quote + Hot Take | Commentary | Quote card | Validation |
| story | Transformation | Thread | Carousel | Story post |

### Step 5: Apply Platform Constraints

| Platform | Length | Hashtags | Links | Tone |
|----------|--------|----------|-------|------|
| **LinkedIn** | 200-500 words | 3-5 | OK in body | Professional authority |
| **X** | 70-100 chars | 0-2 | In reply | Punchy, scroll-stopping |
| **Instagram** | 30-150 chars | 5-10 | Bio only | Casual, visual-first |
| **Facebook** | 10-40 words | 0 | Comments only | Conversational, questions |
| **TikTok** | 50-150 chars | 3-5 | Bio only | Casual, trend-aware |

---

## Template Quick Reference

**Load full templates from:** `.claude/skills/text-content/references/`

### LinkedIn (6 categories)
- `linkedin/engagement.md` - Polls, Agree/Disagree (16 templates)
- `linkedin/story.md` - Transformations, Values (24 templates)
- `linkedin/list.md` - Tips, Frameworks (17 templates)
- `linkedin/contrarian.md` - Hot takes, Rants (20 templates)
- `linkedin/authority.md` - Quotes, How-to (26 templates)
- `linkedin/community.md` - Shoutouts, Introductions (15 templates)

### X/Twitter
- `templates/post-structures.md` - 100+ formats
- `templates/one-liners.md` - 12 punchy patterns

### Instagram/Facebook
- `platforms/instagram-captions.md`
- `platforms/facebook.md`

---

## Output Format

For each platform, produce:

```markdown
## [Platform] Post

**Template:** [Template name used]
**Source:** [What this came from]

---

[The actual post content]

---

**Tags:** @handle1 @handle2
**Hashtags:** #tag1 #tag2 (platform-appropriate count)
**Visual direction:** [If needed - quote card, carousel, etc.]
```

---

## Dimension Handling (Visual Assets)

When source includes a 16:9 infographic or thumbnail:

```
Original (16:9 - article thumbnail)
    │
    ├─→ Instagram Feed (4:5)
    │   Prompt: "Adapt this infographic to 4:5 portrait,
    │            prioritize [key element], crop or extend background"
    │
    ├─→ Instagram/Facebook Square (1:1)
    │   Prompt: "Center the key message, square crop"
    │
    └─→ Stories/Reels Cover (9:16)
        Prompt: "Vertical adaptation, text readable on mobile"
```

**Use:** `nano-banana-image-generator` with re-input of original image.

---

## Voice Constraints (Always Apply)

**From `ai-tells` - HARD BLOCKS:**

❌ No correlative constructions:
- "X isn't just Y - it's Z"
- "It's not about X, it's about Y"

❌ No forbidden words:
- delve, comprehensive, crucial, leverage, landscape, navigate, foster, facilitate, realm, paradigm, embark, journey, tapestry, myriad, multifaceted, seamless, cutting-edge

❌ No setup phrases:
- "The best part?", "What if I told you", "Here's the thing", "Let's be honest"

❌ No staccato patterns:
- "No fluff. No filler. Just results."

**Dash usage:** Hyphens with spaces - like this. Never em dashes.

---

## Batch Processing Mode

When repurposing multiple pieces (e.g., full newsletter → social):

```
1. Read entire source
2. Extract ALL snippets (usually 3-5 per newsletter)
3. For each snippet:
   ├─ Identify type (hot_take, stat, how_to, quote, story)
   ├─ Check nearbound for tags
   └─ Generate 2-3 platform drafts
4. Output organized by platform:
   ├─ LinkedIn (2-3 posts)
   ├─ X (2-3 posts)
   ├─ Instagram (1-2 posts + visual direction)
   └─ Facebook (1-2 posts)
```

**Expected output:** 6-9 total posts per newsletter/article.

---

## When to Use This Skill

**Use content-repurposer when:**
- Newsletter is complete → need social posts
- Podcast is published → need clip promotions
- Article is live → need distribution posts
- Archive content identified → need fresh framing
- Any content needs multi-platform adaptation

**Don't use for:**
- Original content creation (use specific content skills)
- Video production (use video-caption-creation)
- Newsletter writing (use opened-daily-newsletter-writer)

---

## Related Skills

- `text-content` - Full template library (this skill routes TO those templates)
- `newsletter-to-social` - Automated newsletter → social (uses this methodology)
- `opened-identity` - Brand voice (always load)
- `ai-tells` - Hard blocks (always apply)
- `nano-banana-image-generator` - Visual adaptations

---

## Example: Podcast Guest Repurposing

**Source:** Podcast with Ken Danford about self-directed learning

**Step 1:** Identify source type → Podcast guest

**Step 2:** Extract snippets:
- hot_take: "The best thing a school can do is get out of the way"
- stat: "75% of North Star teens go to college - without transcripts"
- story: Ken quit teaching to prove schools are optional

**Step 3:** Check nearbound → Ken Danford profile exists, @kendanford on X

**Step 4:** Draft posts:

**LinkedIn (Authority):**
```
Ken Danford spent 10 years as a public school teacher.

Then he quit to prove schools are optional.

His self-directed learning center, North Star, has helped hundreds of teens:
- No grades
- No transcripts
- 75% college attendance rate

The secret? "Get out of the way and let them lead."

Full conversation on the OpenEd podcast: [link]

#SelfDirectedLearning #AlternativeEducation #Homeschooling
```

**X:**
```
"The best thing a school can do is get out of the way."

@kendanford quit teaching to prove it. 75% of his students go to college - without transcripts.

[link to episode]
```

**Instagram (Quote card direction):**
```
Visual: Quote card with Ken's face + "Get out of the way and let them lead."
Caption: When a 10-year teacher quits to prove schools are optional... and it works. Link in bio.

#homeschool #selfdirectedlearning #alternativeeducation #unschooling #parentingtips
```

---

*Framework fitting is the core technique. This skill specializes in it.*
