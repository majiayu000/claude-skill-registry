---
name: social-media-posts
description: "Create platform-specific social media posts for LinkedIn, Facebook, Instagram, and Reddit. Handles character limits, hashtag strategies, hook placement, and image specs per platform. Works from scratch, from existing content (blog, newsletter, announcement), or as a multi-platform campaign. Produces copy-paste-ready posts. Triggers: 'social media post', 'linkedin post', 'facebook post', 'instagram caption', 'reddit post', 'social posts', 'post to social', 'repurpose for social', 'social media campaign'."
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Social Media Post Generator

Create platform-specific social media posts that respect each platform's conventions, character limits, and audience expectations. Produces copy-paste-ready content.

## Modes

### From Scratch
User provides topic + key points. Generate posts for selected platforms.

### From Content
User provides existing content (blog post, newsletter, announcement, press release). Repurpose into platform-appropriate posts.

### Campaign
Generate a coordinated set of posts across all platforms for a single launch, announcement, or event. Includes posting sequence and timing suggestions.

## Workflow

### 1. Gather Input

| Field | Required | Example |
|-------|----------|---------|
| Topic or source content | Yes | "We just launched a new feature" or path to blog post |
| Target platforms | Yes | LinkedIn, Facebook, Instagram, Reddit |
| Tone | No | Professional, casual, enthusiastic, educational |
| CTA | No | "Try it free", "Read more", "Comment your thoughts" |
| Link to include | No | https://example.com/blog/new-feature |
| Image available? | No | Yes/no — affects post structure |

If the user provides a file path or URL to existing content, read it first and extract the key messages.

### 2. Generate Per-Platform Posts

---

#### LinkedIn

**Audience**: Professionals, B2B, industry peers
**Tone**: Authoritative but approachable, thought-leadership
**Optimal length**: 1,200–1,500 characters (longer posts perform well)

**Structure**:
```
[Hook line — must grab attention before "see more" truncation]
[blank line]
[2-3 short paragraphs with line breaks between]
[blank line]
[CTA or question to drive comments]
[blank line]
[3-5 relevant hashtags]
```

**Rules**:
- Hook must work in first 2 lines (before "…see more" at ~210 chars)
- Use line breaks liberally — wall-of-text kills engagement
- Ask a question at the end to drive comments
- Hashtags: 3-5 max, mix broad (#Marketing) and niche (#CloudflareWorkers)
- Links in comments perform better than in post body (algorithm penalty)
- No emoji overload — 1-2 max, or none for serious topics

**Image specs**: 1200×627px (1.91:1) for link preview, or 1080×1080 (1:1) for standalone

**Example**:
```
We just shipped something we've been building for 6 months.

It started as a "wouldn't it be nice if…" conversation and turned
into our most requested feature. Here's what we learned:

→ Users don't want more features. They want fewer clicks.
→ The prototype we almost killed became the final product.
→ Shipping weekly forced us to cut scope ruthlessly.

The full story is in our latest blog post (link in comments).

What's the hardest product decision you've made this year?

#ProductDevelopment #StartupLife #BuildInPublic
```

---

#### Facebook

**Audience**: Mixed — friends, family, community, local businesses
**Tone**: Conversational, warm, community-focused
**Optimal length**: 80–150 characters for engagement, up to 500 for storytelling

**Structure**:
```
[Opening hook — conversational, relatable]
[1-2 short paragraphs]
[Link (if applicable) — Facebook generates preview cards]
[Engagement prompt — question or poll]
```

**Rules**:
- Link posts: Facebook auto-generates a preview card — don't repeat the headline in your text
- Short posts (under 130 chars) get larger text rendering in feed
- Questions and polls drive highest engagement
- Tag relevant pages when mentioning partners/clients
- Hashtags: 1-3 or none — Facebook hashtags are less effective than other platforms
- Emojis are welcome but don't overdo (2-3 max)

**Image specs**: 1200×630px (1.91:1) for link preview, 1080×1080 (1:1) for photo posts

**Example**:
```
6 months ago we started building something our users kept asking for.
Today it's live. 🚀

We wrote up the full story — the pivots, the almost-killed prototype,
and why "fewer clicks" won over "more features."

[link]

What feature have you shipped that surprised you?
```

---

#### Instagram

**Audience**: Visual-first, younger demographic, lifestyle/brand-focused
**Tone**: Authentic, visual storytelling, personality-forward
**Optimal length**: Key message in first 125 chars (truncation point), full caption up to 2,200

**Structure**:
```
[First line — must work as standalone (before "…more")]
[blank line]
[Story or detail — 2-4 short paragraphs]
[blank line]
[CTA — save, share, comment, link in bio]
.
.
.
[Hashtags — in first comment OR separated by dots]
```

**Rules**:
- First 125 characters must carry the message (everything after is hidden behind "…more")
- No clickable links in captions — direct to "link in bio"
- Hashtags: 20-30 in first comment (not in caption) for discoverability
- Mix hashtag sizes: 5 large (1M+ posts), 10 medium (100K-1M), 10 niche (<100K)
- Emojis are part of the language — use them naturally
- Carousel posts: include a swipe CTA ("Swipe for the full breakdown →")
- Stories: prompt action ("Reply with 🔥 if you relate")

**Image specs**: 1080×1080 (1:1) feed, 1080×1350 (4:5) portrait, 1080×1920 (9:16) stories/reels

**Example**:
```
We shipped our most requested feature today. Here's the story 👇

Six months ago, someone on our team said "wouldn't it be nice
if users could do this in one click instead of five?"

We almost killed the prototype twice. But our users kept asking
for it. So we shipped it.

The biggest lesson? Your users don't want more features.
They want fewer clicks.

Full story → link in bio

💬 What's one feature you wish was simpler in your favourite app?
```

**First comment**:
```
#ProductLaunch #StartupLife #BuildInPublic #TechStartup
#ProductDevelopment #UXDesign #SaaS #FeatureLaunch
[... 20-30 total hashtags]
```

---

#### Reddit

**Audience**: Community-specific, values authenticity, allergic to marketing
**Tone**: Genuine, value-first, conversational, never salesy
**Optimal length**: Title 100-150 chars, body varies by subreddit

**Structure**:
```
Title: [Descriptive, value-focused — NOT clickbait]

Body:
[Context — why this matters to this community]
[The substance — what you learned, built, or discovered]
[Optional: link to more detail]
[Discussion prompt — genuine question]
```

**Rules**:
- **Title is everything** — Reddit lives and dies by titles
- NO self-promotion feel — lead with value, not product
- Each subreddit has different norms — check the rules before posting
- Don't use hashtags (not a Reddit convention)
- Don't use emojis in titles (feels out of place on most subreddits)
- Share the insight, not the product. "Here's what we learned" > "Check out our new feature"
- Cross-posting: adapt tone per subreddit (r/startups vs r/webdev vs r/smallbusiness)

**Subreddit suggestions by topic**:
| Topic | Subreddits |
|-------|-----------|
| Product launch | r/SideProject, r/startups, r/indiehackers |
| Web dev | r/webdev, r/javascript, r/reactjs |
| Design | r/web_design, r/UI_Design |
| Business | r/smallbusiness, r/Entrepreneur |
| Tech | r/programming, r/technology |

**Example**:
```
Title: After 6 months of building, the biggest lesson was
"users want fewer clicks, not more features"

We built a feature our users kept requesting. Halfway through
we almost killed it because the prototype felt clunky.

What saved it: we stopped adding capabilities and started
removing steps. The final version does less than the prototype
but users complete the task in 1 click instead of 5.

Three things I'd tell past-me:
1. Prototype with your heaviest users, not your most vocal ones
2. "Ship weekly" forces you to cut scope — that's a feature
3. The thing users ask for and the thing they need are different

Anyone else had a similar experience where removing features
improved the product?
```

---

### 3. Image Recommendations

For each platform, suggest image requirements:

| Platform | Format | Dimensions | Notes |
|----------|--------|-----------|-------|
| LinkedIn | PNG/JPG | 1200×627 | Text overlay OK, keep key message in centre |
| Facebook | PNG/JPG | 1200×630 | Minimal text (old 20% rule still affects reach) |
| Instagram | PNG/JPG | 1080×1080 | Visual-first — image must work without caption |
| Reddit | PNG/JPG | Varies | Optional — text posts often perform better |

If the `ai-image-generator` skill is available, suggest using it to generate companion images with the right aspect ratios.

### 4. Output Format

Present each post in a clearly labelled block:

```
═══ LINKEDIN ═══
[post content]

═══ FACEBOOK ═══
[post content]

═══ INSTAGRAM (Caption) ═══
[caption content]

═══ INSTAGRAM (First Comment — Hashtags) ═══
[hashtags]

═══ REDDIT (r/subreddit) ═══
Title: [title]
Body: [body]
```

Save to `.jez/artifacts/social-posts-[topic].md` if the user wants to keep them for scheduling.

## Campaign Mode

For launches or announcements, generate a posting sequence:

| Timing | Platform | Post type |
|--------|----------|-----------|
| Day -1 | LinkedIn | Teaser / behind-the-scenes |
| Day 0 (morning) | All platforms | Announcement post |
| Day 0 (afternoon) | Instagram Stories | Quick video/carousel |
| Day +1 | Reddit | Value-focused discussion |
| Day +3 | LinkedIn | Results/learnings follow-up |
| Day +7 | Facebook | Customer reaction / testimonial |

## Quality Rules

1. **Never copy-paste the same text across platforms** — each platform has different conventions
2. **No corporate jargon** — "leverage our synergies" belongs nowhere
3. **Front-load the value** — every platform truncates. The first line must work standalone.
4. **Match the platform culture** — LinkedIn is not Instagram is not Reddit
5. **Include a reason to engage** — question, poll, or genuine discussion prompt
6. **Check character limits** — LinkedIn (3,000), Facebook (63,206), Instagram caption (2,200), Reddit title (300)
7. **Never fake engagement** — no "Drop a 🔥 if you agree" on LinkedIn, no hashtag spam on Reddit
