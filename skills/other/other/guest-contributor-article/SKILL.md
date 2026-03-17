---
name: guest-contributor-article
description: End-to-end workflow for ghostwriting SEO articles in a guest contributor's voice. Covers source gathering, voice analysis, anti-hallucination sourcing, drafting, and quality gates. Use when writing an article under someone else's byline for the OpenEd blog.
---

# Guest Contributor Article

Ghostwrite an SEO article in a guest contributor's authentic voice. We do 80% of the work, they get the byline and a plug for their platform.

**Core principle:** Every claim, recommendation, and story in the article must trace to something the contributor actually said or published. If you can't source it, flag it or cut it.

---

## When to Use This Skill

- Writing an article for the OpenEd blog under a guest contributor's byline
- The contributor has agreed (or is being pitched) to lend their name
- You have access to their source material (blog, podcast, articles, talks)

**Prerequisite skills loaded automatically:**
- `ghostwriter` - AI pattern detection, voice transformation
- `quality-loop` - 5-judge quality gates

---

## The Anti-Hallucination Rule

This is the #1 risk in ghostwriting. The LLM will confidently fabricate:
- Book titles the contributor never recommended
- URLs that don't exist (Bookshop.org, Amazon links)
- Quotes they never said
- Statistics they never cited
- Programs or organizations they never mentioned

**The fix:** Every section of the outline must cite its source BEFORE drafting begins. If a claim has no source, it gets one of three treatments:

1. **[VERIFIED]** - Traced to a specific blog post, article, podcast, or talk
2. **[INFERRED]** - Reasonable inference from their body of work (flag for contributor review)
3. **[PLACEHOLDER]** - Marked with `[NOTE FOR CONTRIBUTOR]` in the draft

Never invent links. If you want to link a book title, use only:
- Links the contributor uses on their own site
- OpenEd internal links you've verified exist
- Leave the title unlinked if no verified URL exists

---

## Phase 1: Contributor Brief

Create `README.md` in the contributor's folder.

```
Guest Contributors/[contributor-name]/
├── README.md              # This brief
├── sources/               # Their actual content
│   ├── articles/          # Blog posts, written pieces
│   ├── podcasts/          # Transcripts
│   └── youtube-transcripts/
├── seo-research/          # Content briefs from /seo-research
├── drafts/                # Article versions
└── images/                # Thumbnails, infographics
```

**README.md must include:**

| Section | What Goes Here |
|---------|---------------|
| Relationship context | How we know them, warmth level, last contact |
| Why they fit | Their expertise area, audience overlap with OpenEd |
| Source material inventory | Checklist of content to gather (blog, podcast, YouTube, social) |
| Expertise areas | Their topic domains |
| Potential angles | 3-5 article ideas before SEO research |
| Draft strategy | Voice approach, what to plug, how to differentiate |
| Next actions | Checklist with status |

---

## Phase 2: Source Gathering

Collect 3-5 pieces of their actual content. Read them. This is not optional.

**Priority order:**
1. OpenEd podcast appearance (if they were a guest)
2. Their blog / newsletter (primary voice source)
3. Other podcast appearances or talks
4. Social media posts (LinkedIn, X)
5. Books or courses (note key chapters/sections)

**What to extract from each source:**
- Direct quotes worth preserving
- Personal stories and anecdotes (with source citation)
- Frameworks or terminology they invented (these are their fingerprints)
- Data points or statistics they cite
- Specific recommendations (books, tools, programs) - note the EXACT source where they recommended each one
- Tone markers: sentence length, humor style, how they use "I", capitalization habits, rhetorical patterns

Save source material to `sources/` folder with clear attribution.

---

## Phase 3: SEO Topic Selection

Run `/seo-research` with their expertise area.

**Criteria:**
- Volume: 500+/month (flexible for niche topics with high CPC)
- Competition: < 0.5
- Their expertise genuinely maps to the keyword
- OpenEd doesn't already own this keyword
- SERP gap: no practitioner/personal voice content ranking

**Output:** Content brief saved to `seo-research/` folder.

---

## Phase 4: Voice Analysis

Study their writing and document patterns in the README under "Voice Notes for Drafting."

**Document these specifically:**

| Pattern | Example from Janssen | Example from Mason |
|---------|---------------------|-------------------|
| Sentence rhythm | Short declaratives, dashes for asides | Longer paragraphs, systems-level then personal |
| Signature phrases | "I LOVE" (caps), "I promise we'll get there" | Bloomer/Doomer/Gloomer/Zoomer framework |
| How they use "I" | Frequently, personal anecdotes | Rarely, except for personal anecdotes |
| How they cite data | Specific numbers ("between 2,000 and 5,000 books") | One or two stats per section, always contextualized |
| Humor | Self-deprecating, permission-giving | Dry, intellectual |
| What they DON'T do | Preach, lecture, use jargon | Oversell, ignore tradeoffs |
| Typical headers | Descriptive, conversational | Descriptive, not clever |
| How they close | Permission-giving ("even Dog Man, even for seven minutes") | Forward-looking, optimistic but not naive |

---

## Phase 5: Source-Mapped Outline

Create the article outline with every section mapped to its source. This is the anti-hallucination gate.

**Format:**

```markdown
## [H2 Title] (~word count)

**What goes here:** [Description]
**Sources:**
- Personal story about X → from [blog post URL] / [podcast timestamp]
- Statistic about Y → from [their article title, date]
- Book recommendations → from [specific blog post where they listed these]

**Voice note:** [How this section should sound based on voice analysis]
```

**Before drafting, verify:**
- [ ] Every personal story traces to something they've told publicly
- [ ] Every recommendation traces to their content (not your knowledge)
- [ ] Every statistic traces to something they've cited
- [ ] Sections where you're inferring are marked [INFERRED]
- [ ] The OpenEd plug feels natural, not grafted on

---

## Phase 6: Draft

### Structure Template

```markdown
---
title: "[Title]"
author: [Contributor Name]
byline: "[One-sentence bio with company and credentials]"
status: draft-v1
primary_keyword: [keyword]
secondary_keywords: [list]
slug: [url-slug]
date: [YYYY-MM-DD]
sources: "[list of source material used]"
---

# [Title]

*[Contributor Name] is [credentials]. They [what they're known for].
[Link to their platform]. [Link to their OpenEd podcast appearance if applicable].*

[Article body]
```

### Drafting Rules

1. **Write in their voice, not OpenEd's.** Use their sentence patterns, their frameworks, their humor. The ghostwriter skill's "Charlie's Signature Moves" do NOT apply here - those are for Charlie's voice.

2. **Italicized intro paragraph.** Before the article body, one paragraph introducing who they are with links to their platform and OpenEd podcast appearance. This goes below the byline in the frontmatter.

3. **OpenEd internal links.** Weave in 3+ internal links to existing OpenEd content. These should feel like helpful references, not promotions.

4. **Contributor platform plug.** Include naturally - usually through their personal story leading into what they built. Don't make it an ad. The Janssen piece does this well: her daughter's reading struggle story naturally leads to why she started Savvy Learning.

5. **[NOTE FOR CONTRIBUTOR] placeholders.** When you want a personal anecdote but aren't sure they have one, or when you're inferring rather than sourcing, mark it clearly. Example: `[NOTE FOR JANSSEN: Do you have a specific student/family story that illustrates this?]`

6. **No invented links.** Do not create URLs. If you want to link book titles, either use the contributor's own links from their site or leave titles unlinked.

7. **Word count.** Target the SERP-recommended range from the content brief, typically 1,500-2,500 words.

---

## Phase 7: Source Verification Report

Before sending to the contributor or publishing, create a verification table. Append to the draft file or save separately.

```markdown
## Source Verification

| Claim / Recommendation | Source | Status |
|------------------------|--------|--------|
| "tested at 12th-grade reading level in kindergarten" | OpenEd podcast Dec 2025, 14:32 | VERIFIED |
| Dog Man recommendation | everyday-reading.com/books-like-dog-man | VERIFIED |
| The Wild Robot recommendation | everyday-reading.com/books-for-reluctant-readers | VERIFIED |
| "between 2,000 and 5,000 books" | 3 in 30 podcast, episode X | VERIFIED |
| All Thirteen feedback claim | [could not find specific post] | INFERRED |
```

**Rules:**
- Every book/tool/program recommendation must trace to the contributor's content
- Every personal story must trace to a public telling
- Every statistic must trace to a cited source
- INFERRED items get flagged for contributor review

---

## Phase 8: Quality Gate

Run through `quality-loop` with one modification:

**Modified Judge 2 (Accuracy Checker):** In addition to standard accuracy checks, verify:
- [ ] All claims trace to the contributor's published content (not general knowledge)
- [ ] No hallucinated URLs
- [ ] No book/program recommendations the contributor hasn't made
- [ ] Contributor's bio details are accurate
- [ ] OpenEd internal links are valid (not 404s)

**Modified Judge 3 (OpenEd Voice):** The article should NOT sound like OpenEd's usual voice. It should sound like the contributor. Judge for:
- [ ] Voice matches contributor's documented patterns
- [ ] OpenEd strategic narrative woven in subtly (not imposed)
- [ ] The plug for their platform is natural

All other judges run as standard.

---

## Phase 9: Delivery & Collaboration

**If pitching (they haven't agreed yet):**
- Send draft with pitch email (use `Outreach Templates/Guest_Article_Pitch_Template.md`)
- Frame as "we did the heavy lifting, you polish and approve"

**If agreed (they said yes):**
- Send draft for review
- Note what's sourced vs. what needs their input
- Invite them to add personal anecdotes at placeholder spots
- Make their edits, run quality loop again

**Publication:**
- Publish on OpenEd blog via `webflow-publish` with full byline
- Create social assets via `newsletter-to-social`
- Send contributor share-ready posts with @handles

---

## Skill Chain

| Phase | Skill |
|-------|-------|
| SEO research | `seo-research` |
| Source transcripts | `youtube-downloader` / `twitter-scraper` |
| Voice + AI patterns | `ghostwriter` |
| Quality gates | `quality-loop` |
| Title options | `article-titles` |
| Thumbnail | `nano-banana-image-generator` |
| Publish | `webflow-publish` |
| Social spokes | `newsletter-to-social` |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Inventing book/product links | Never create URLs. Link only from verified sources or leave unlinked |
| Writing in Charlie/OpenEd voice | Write in the CONTRIBUTOR's voice. Study their patterns first |
| Recommending things they never recommended | Every recommendation must trace to their content |
| Making up quotes | Only use quotes from transcripts/articles. Mark inferred quotes as [INFERRED] |
| Over-plugging OpenEd | 3+ internal links is fine, but the article should serve the reader, not the brand |
| Stacking AI tells | Load `ghostwriter` and run forbidden patterns check. "Actually" max 1-2 uses |
| Same structure every time | Vary the approach (narrative vs. listicle vs. how-to). Track what you've done |

---

*Created: 2026-02-05. Based on the Janssen Bradshaw and Mason Pashia contributor packages.*
