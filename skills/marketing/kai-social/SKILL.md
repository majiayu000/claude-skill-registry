---
name: kai-social
description: Plan and batch-produce social media content across platforms (Instagram, X/Twitter, TikTok, LinkedIn, YouTube). Generates a week or month of posts with platform-specific formatting, hashtags, hooks, and posting schedule. Use when "social media posts", "social calendar", "plan social content", "Instagram posts", "tweets", "LinkedIn posts", "TikTok ideas", "social media strategy", "batch social", or any request to systematically produce social media content.
---

Plan and batch-produce social media content across platforms with platform-specific optimization.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Social Discovery

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Brand/product** — what are we posting about?
2. **Platforms** — which ones? (Instagram, X, TikTok, LinkedIn, YouTube)
3. **Time horizon** — 1 week or 1 month?
4. **Posting cadence** — how often per platform?
5. **Content pillars** — what themes/topics? (educational, behind-the-scenes, product, social proof, culture)
6. **Tone** — professional, casual, bold, irreverent?
7. **Existing content** — any blog posts, videos, or assets to repurpose?

## Phase 2: Social Calendar

Load these before planning:
- `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\social-media-strategy.md`
- Platform-specific channels as needed:
  - `E:\Dev2\kai-cmo-harness-work\knowledge\channels\instagram.md`
  - `E:\Dev2\kai-cmo-harness-work\knowledge\channels\x-twitter.md`
  - `E:\Dev2\kai-cmo-harness-work\knowledge\channels\tiktok-algorithm.md`
  - `E:\Dev2\kai-cmo-harness-work\knowledge\channels\youtube.md`
  - `E:\Dev2\kai-cmo-harness-work\knowledge\channels\linkedin-articles.md`

Generate `workspace/social/_calendar.md`:

| Day | Platform | Pillar | Format | Hook | Status |
|-----|----------|--------|--------|------|--------|
| Mon | LinkedIn | Educational | Text post | Insight/contrarian take | Draft |
| Mon | X | Product | Thread | Problem → solution | Draft |
| Tue | Instagram | Social proof | Carousel | Customer result | Draft |
| Tue | TikTok | Educational | Short video script | Hook question | Draft |
| ... | ... | ... | ... | ... | ... |

### Content Pillar Mix

Recommend a balanced mix:
- **40% Value/Educational** — teach something useful
- **25% Social Proof** — results, testimonials, case studies
- **20% Product** — features, demos, tutorials
- **15% Culture/BTS** — team, process, behind-the-scenes

### Approval Gate

Present calendar before producing posts.

## Phase 3: Batch Production

### Platform-Specific Formats

**LinkedIn:**
- Hook line (pattern interrupt or bold claim)
- 3-5 short paragraphs
- Line breaks between every thought
- CTA at the end
- 1200-1500 chars optimal

**X/Twitter:**
- Single tweets: max 280 chars, front-load the hook
- Threads: 3-7 tweets, each standalone valuable, numbered
- End thread with CTA or summary

**Instagram:**
- Captions: hook in first line (before "...more"), 150-300 words
- Carousel: 5-10 slides, one idea per slide, bold text
- Reels: script format (hook in first 3 seconds)

**TikTok:**
- Hook in first 2 seconds (question, bold claim, or visual pattern interrupt)
- 15-60 second script
- Trending format adaptation
- CTA as last frame

**YouTube:**
- Shorts: 30-60 second script, hook-first
- Community posts: poll or discussion question

### Per-Post Output

```markdown
# [Platform] — [Day] — [Pillar]

**Format:** [text/carousel/thread/video script]
**Hook:** [first line or first 3 seconds]

## Copy
[Full post text]

## Hashtags (if applicable)
[platform-appropriate hashtags]

## Visual Direction (if applicable)
[Brief description of image/carousel/video]

## Posting Notes
- Best time: [time]
- Cross-post to: [other platforms, if adapted]
```

### Quality Gates (per post)

1. **Hook in first line** (no warm-up, no preamble)
2. **Zero banned words**
3. **Zero AI slop**
4. **Platform character limits** respected
5. **Single CTA** (or no CTA for pure value posts)
6. **Not generic** — could only come from THIS brand

## Phase 4: Output

```
workspace/social/
├── _calendar.md
├── linkedin/
│   ├── mon-educational.md
│   ├── wed-social-proof.md
│   └── ...
├── x-twitter/
│   └── ...
├── instagram/
│   └── ...
├── tiktok/
│   └── ...
└── _quality-report.md
```
