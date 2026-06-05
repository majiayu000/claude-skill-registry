---
name: kai-repurpose
description: Take one pillar content piece and produce 15-25 derivative assets across platforms — social posts, email, LinkedIn article, video scripts, newsletter section, infographic brief, and more. The ultimate content multiplier. Use when "repurpose this", "turn this into", "make social posts from this blog", "content repurposing", "1 to many", "atomize this content", "extract posts from", or any request to derive multiple pieces from one source.
---

Take 1 pillar → produce 15-25 channel-specific assets. The content multiplier.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Pillar Input

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Source content** — paste it, link it, or point to the file
2. **Platforms** — which channels should get derivative content?
3. **Priority** — what matters most? (social reach, email engagement, SEO, video views)

Load: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\content-repurposing.md`

## Phase 2: Extraction Map

Read the pillar content and extract:
- **Key insights** (3-5 standalone ideas)
- **Data points** (stats, numbers, results)
- **Quotable lines** (bold claims, memorable phrases)
- **Steps/frameworks** (any process or list)
- **Stories/examples** (anecdotes, case studies)
- **Contrarian takes** (anything that challenges conventional wisdom)

Generate `workspace/repurposed/_extraction-map.md`:

| Extract | Type | Best Channel | Format |
|---------|------|-------------|--------|
| "Stat about X" | Data point | X, LinkedIn | Single post |
| "3-step framework" | Process | Instagram carousel, LinkedIn | Carousel / text post |
| "Contrarian claim" | Take | X thread, TikTok | Thread / video script |
| ... | ... | ... | ... |

### Quote Mining Pass

When the source is a transcript, podcast, webinar, interview, or long article, run a quote mining pass before derivative production.

Create `workspace/repurposed/_quote-bank.md` with:
- **Source location**: file path, URL, episode name, transcript timestamp, or paragraph locator
- **Quote or paraphrase**: mark direct quotes clearly; keep direct quotes short
- **Use case**: hook, proof, objection, story, CTA, email subject, clip candidate
- **Risk note**: unsupported claim, private detail, medical/legal/financial claim, or needs approval
- **Attribution requirement**: guest name, customer approval, anonymous/internal, or source citation

Rules:
- Preserve exact source locations so every derivative can be traced back.
- Do not invent quotes, credentials, or expert authority.
- Treat quote mining as source extraction, not rewriting. Rewrite only in derivative files.
- Draft as a dry run first; publishing or scheduling requires explicit approval.

## Phase 3: Derivative Production

From one pillar, produce:

### Standard Derivative Set (adapt based on platforms)

| # | Asset | Platform | Format |
|---|-------|----------|--------|
| 1 | LinkedIn text post (insight #1) | LinkedIn | 1200 chars |
| 2 | LinkedIn text post (insight #2) | LinkedIn | 1200 chars |
| 3 | LinkedIn carousel (framework) | LinkedIn | 8-10 slides outline |
| 4 | X/Twitter thread (full argument) | X | 5-7 tweets |
| 5 | X/Twitter single tweet (data point #1) | X | 280 chars |
| 6 | X/Twitter single tweet (data point #2) | X | 280 chars |
| 7 | X/Twitter single tweet (contrarian take) | X | 280 chars |
| 8 | Instagram carousel (key takeaways) | Instagram | 5-7 slides outline |
| 9 | Instagram caption (story/example) | Instagram | 150-300 words |
| 10 | TikTok video script (hook + insight) | TikTok | 30-60 seconds |
| 11 | TikTok video script (contrarian take) | TikTok | 15-30 seconds |
| 12 | Email newsletter section | Email | 100-200 words |
| 13 | Email standalone (value-add) | Email | 300-500 words |
| 14 | LinkedIn article (expanded angle) | LinkedIn | 700-1000 words |
| 15 | YouTube Shorts script | YouTube | 30-60 seconds |
| 16-25 | Additional platform-specific variants | Various | Various |

### Rules

- Each derivative must stand alone (no "as I wrote in my blog post...")
- Adapt tone to platform (LinkedIn = professional, X = punchy, TikTok = conversational)
- Different hook for each piece (even when based on the same insight)
- Every piece gets quality gate check: zero banned words, zero AI slop, platform limits
- Credit the pillar only if the platform norms expect it

## Phase 4: Output

```
workspace/repurposed/
├── _extraction-map.md
├── _source-pillar.md          # Copy of original for reference
├── linkedin/
│   ├── post-insight-1.md
│   ├── post-insight-2.md
│   ├── carousel-framework.md
│   └── article-expanded.md
├── x-twitter/
│   ├── thread-full.md
│   ├── tweet-stat-1.md
│   ├── tweet-stat-2.md
│   └── tweet-contrarian.md
├── instagram/
│   ├── carousel-takeaways.md
│   └── caption-story.md
├── tiktok/
│   ├── script-insight.md
│   └── script-contrarian.md
├── email/
│   ├── newsletter-section.md
│   └── standalone-email.md
├── youtube/
│   └── shorts-script.md
└── _quality-report.md
```

## Phase 5: Publishing Schedule

Generate a suggested posting schedule — stagger derivatives over 1-2 weeks so they don't cannibalize each other. Lead with the highest-reach platform, follow with niche channels.
