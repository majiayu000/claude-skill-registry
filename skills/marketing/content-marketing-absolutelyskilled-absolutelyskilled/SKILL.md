---
name: content-marketing
version: 0.1.0
description: >
  Use this skill when creating content strategy, writing SEO-optimized blog posts,
  planning content calendars, or repurposing content across channels. Triggers on
  blog strategy, content calendar, SEO content, content repurposing, editorial
  workflow, content pillars, topic clusters, and any task requiring content
  marketing planning or execution.
category: marketing
tags: [content-marketing, blog, seo-content, editorial, content-strategy]
recommended_skills: [copywriting, content-seo, email-marketing, social-media-strategy]
platforms:
  - claude-code
  - gemini-cli
  - openai-codex
license: MIT
maintainers:
  - github: maddhruv
---

When this skill is activated, always start your first response with the 🧢 emoji.

# Content Marketing

Content marketing is the practice of creating and distributing valuable, relevant
content to attract, engage, and convert a defined audience - rather than interrupting
them with ads. Done well, it compounds over time: a single pillar page drives
organic traffic for years, a repurposed webinar becomes ten assets, and a consistent
editorial calendar builds brand authority that paid media cannot buy.

This skill covers content strategy, SEO-driven editorial planning, pillar-cluster
architecture, cross-channel repurposing, and performance measurement - giving an
agent the judgment to plan, write, and distribute content the way a seasoned content
strategist would.

---

## When to use this skill

Trigger this skill when the user:
- Wants to build or audit a content strategy for a product, brand, or niche
- Needs to create or redesign a content calendar (weekly, monthly, quarterly)
- Asks for help writing, structuring, or optimizing an SEO blog post
- Wants to design a pillar page and topic-cluster architecture
- Needs a playbook for repurposing one piece of content across channels
- Asks how to set up an editorial workflow (briefing, drafting, review, publish)
- Wants to define or track content marketing KPIs and attribution

Do NOT trigger this skill for:
- Paid advertising copy or media buying (ad copy is a different discipline)
- Technical SEO implementation - crawl budgets, structured data, site speed (use `technical-seo-engineering`)

---

## Key principles

1. **Audience first** - Every content decision starts with the reader. Who are they,
   what question are they asking, and what do they need to do after reading? Content
   that serves the audience earns trust; content that serves the brand earns nothing.

2. **Pillar-cluster model** - Organize content around broad pillar pages that cover
   a topic comprehensively, supported by cluster articles that go deep on subtopics.
   Internal links between them signal topical authority to search engines and guide
   readers through a logical journey.

3. **Consistency beats virality** - One viral post does not build an audience.
   Publishing two quality pieces per week for a year compounds into a moat. Establish
   a cadence you can sustain, then optimize for quality within that constraint.

4. **Repurpose everything** - Every long-form piece contains a dozen shorter assets.
   A 2,000-word blog post becomes a LinkedIn thread, a tweet storm, a short-form
   video script, an email newsletter section, and three social graphics. Maximize
   the return on every research hour invested.

5. **Measure and iterate** - Content marketing ROI is real but lagging. Measure
   organic traffic, keyword rankings, scroll depth, email signups, and pipeline
   influenced. Use data to double down on what works and prune what does not.

---

## Core concepts

### Content funnel - TOFU / MOFU / BOFU

Match content type to where the reader sits in their decision journey:

| Stage | Name | Intent | Examples |
|---|---|---|---|
| TOFU | Top of Funnel | Awareness - broad problem discovery | How-to guides, listicles, explainer posts, trend reports |
| MOFU | Middle of Funnel | Consideration - evaluating solutions | Comparison posts, case studies, webinars, whitepapers |
| BOFU | Bottom of Funnel | Decision - ready to buy or sign up | Pricing pages, demos, customer stories, ROI calculators |

A healthy content program publishes across all three stages. Over-indexing on TOFU
drives traffic but no pipeline; over-indexing on BOFU limits reach.

### Pillar pages and topic clusters

A **pillar page** is a long-form (2,000-5,000 word) comprehensive guide on a broad
topic (e.g., "The Complete Guide to Email Marketing"). It links out to **cluster
articles** - focused posts on subtopics (e.g., "How to Write a Subject Line That
Gets Opened", "Email List Segmentation Strategies"). Each cluster article links back
to the pillar.

Benefits: topical authority, improved crawlability, longer time-on-site, and a
natural internal linking structure that distributes page rank.

### Content types and formats

| Type | Best for | Typical length |
|---|---|---|
| Blog post / article | SEO, thought leadership, TOFU | 1,000-3,000 words |
| Pillar page | Topical authority, TOFU/MOFU | 3,000-6,000 words |
| Case study | Social proof, MOFU/BOFU | 800-1,500 words |
| Whitepaper / report | Lead gen, MOFU | 2,000-8,000 words |
| Email newsletter | Retention, nurture | 300-800 words |
| Social content | Distribution, reach | Platform-native |
| Video / podcast | Awareness, trust | Format-dependent |

### Distribution channels

Content does not distribute itself. Plan distribution at the time of creation:

- **Owned** - Blog, email list, social profiles, community (highest ROI, builds assets)
- **Earned** - Backlinks, press mentions, shares, guest posts (high credibility)
- **Paid** - Sponsored posts, content amplification (speed, reach on demand)

Owned channels compound; paid channels stop working the moment you stop paying.

---

## Common tasks

### Build a content strategy

Use this framework to define or audit a content strategy:

1. **Define the audience** - Job title, company size, key pain points, content they
   already consume. Build 1-3 audience personas maximum.
2. **Audit existing content** - Inventory all published pieces: URL, topic, funnel
   stage, monthly traffic, ranking keywords, backlinks. Identify gaps and
   cannibalization.
3. **Choose 3-5 content pillars** - Broad themes that sit at the intersection of
   your audience's needs and your product's expertise (e.g., "Developer Productivity",
   "API Design", "Engineering Culture").
4. **Map content to funnel** - For each pillar, plan TOFU, MOFU, and BOFU content.
5. **Set goals and KPIs** - Organic sessions, leads from content, keyword rankings
   for target terms, email subscribers, backlinks earned.
6. **Define publishing cadence** - Sustainable frequency comes first. Start with
   two posts per week before aiming for daily.

### Create a content calendar

A content calendar prevents gaps, enables planning, and aligns stakeholders. Minimum
required fields per entry:

| Field | Description |
|---|---|
| Title / working title | Clear enough for a writer to start from |
| Target keyword | Primary keyword the piece will rank for |
| Funnel stage | TOFU / MOFU / BOFU |
| Content pillar | Which strategic theme this belongs to |
| Format | Blog post, case study, video, etc. |
| Target persona | Who is this written for |
| Publish date | Committed date, not aspirational |
| Owner | Writer responsible for the draft |
| Status | Idea / Brief / In progress / Review / Scheduled / Published |

Recommended cadence: plan 6-8 weeks ahead, review and adjust monthly.

### Write an SEO-optimized blog post

Follow this structure for every long-form blog post:

1. **Keyword research first** - Identify a primary keyword (target: 500-5,000 monthly
   searches, low-to-medium difficulty). Find 5-10 semantically related secondary
   keywords to weave in naturally.
2. **SERP analysis** - Read the top 5 ranking pages. Note: content format, headings
   used, questions answered, length. Your post must cover everything they cover and
   add unique value (original data, deeper examples, better structure).
3. **Outline with H2/H3 structure** - Mirror the mental model of someone searching
   the keyword. Lead with "what" before "how". Use questions as headings when the
   keyword is question-form.
4. **Write the introduction** - Hook (relatable problem or surprising stat), bridge
   (why this matters), thesis (what the post covers). Under 150 words.
5. **Body** - Use the inverted pyramid: most important information first in each
   section. Short paragraphs (3-5 lines max). Use bullet lists for scannable points.
   Include code examples, screenshots, or data where relevant.
6. **Conclusion** - Summarize the 3 key takeaways. Include a clear CTA (subscribe,
   download, start a trial).
7. **On-page SEO** - Primary keyword in title (near the front), first 100 words,
   one H2, meta description (under 160 chars). Alt text on all images. Internal
   links to 2-4 related posts.

### Design a pillar-cluster content model

Steps to build a pillar-cluster architecture for a topic area:

1. **Choose the pillar topic** - Broad enough to support 10+ subtopics, specific
   enough to be relevant to your product (e.g., "Content Marketing for SaaS").
2. **Research subtopics** - Use keyword tools to find related queries. Group them
   into 8-15 cluster themes.
3. **Audit existing content** - Map existing posts to cluster slots. Identify gaps.
4. **Write or update the pillar page** - Comprehensive coverage of the main topic.
   Dedicate a section to each cluster theme with a paragraph of context and a link
   to the cluster article.
5. **Write or update cluster articles** - Each cluster article goes deep on one
   subtopic. Every cluster article links back to the pillar page.
6. **Build internal links** - Each cluster article also links to 2-3 sibling cluster
   articles where relevant.

### Repurpose content across channels - playbook

For every long-form piece, extract the following derivative assets:

| Source asset | Derivative | Channel |
|---|---|---|
| Blog post | Key insight thread (5-8 posts) | X / Twitter, LinkedIn |
| Blog post | Short-form video script (60-90 sec) | YouTube Shorts, Instagram Reels, TikTok |
| Blog post | Email newsletter section | Email list |
| Blog post | Infographic (stats + process) | Pinterest, LinkedIn, blog embeds |
| Webinar / podcast | Audiogram clips | Social, YouTube |
| Webinar / podcast | Transcript cleaned into blog post | Blog, SEO |
| Data report | Press release + stat soundbites | PR, social |

Repurposing rule: change the format, not just the words. A blog post copy-pasted to
LinkedIn is not repurposing - a thread that distills the 5 key insights is.

### Set up an editorial workflow

A minimal but complete editorial workflow prevents quality regressions at scale:

1. **Brief** - Writer receives: target keyword, audience persona, funnel stage,
   target length, outline skeleton, internal links to include, deadline.
2. **Draft** - Writer submits first draft in the CMS or shared doc. Draft includes
   meta title, meta description, slug, and at least one internal link suggestion.
3. **Editorial review** - Editor checks: accuracy, structure, voice, SEO (keyword
   placement, headings, meta), and CTA clarity. Single round of feedback.
4. **Revisions** - Writer addresses all feedback. Marks items resolved.
5. **Final QA** - Check images have alt text, all links work, CMS fields are
   complete (category, tags, author, featured image).
6. **Schedule / publish** - Publish or schedule. Add to distribution queue.
7. **Promotion** - Post to social, include in next email newsletter, notify internal
   stakeholders.

### Measure content performance - KPIs and attribution

Track these metrics per content piece and in aggregate:

| KPI | Tool | What it tells you |
|---|---|---|
| Organic sessions | Google Analytics / Search Console | SEO reach |
| Keyword ranking position | Ahrefs / Semrush | Search visibility |
| Scroll depth / time on page | GA4 / Hotjar | Engagement quality |
| Email signups from content | GA4 goals / HubSpot | Lead gen efficiency |
| Backlinks earned | Ahrefs | Authority building |
| Content-influenced pipeline | CRM (HubSpot, Salesforce) | Revenue impact |
| Social shares / engagement | Native analytics | Distribution reach |

Attribution model recommendation: use first-touch for awareness KPIs (which content
introduced leads to your brand) and multi-touch for pipeline KPIs (which content
appeared in the journey of closed deals).

---

## Anti-patterns / common mistakes

| Mistake | Why it's wrong | What to do instead |
|---|---|---|
| Publishing for publishing's sake | Thin, low-effort content dilutes topical authority and earns no backlinks or shares | Set a quality bar: every piece must be the best resource on the web for its target keyword |
| Ignoring distribution | Great content with zero promotion reaches no one | Plan distribution before writing; dedicate as much time to promotion as to creation |
| Targeting only high-volume keywords | High-volume terms have high competition; new domains cannot rank for them | Target long-tail keywords (low volume, high intent) first; build authority before pursuing head terms |
| Skipping the content audit | Creating new content while duplicating or cannibalizing existing posts | Audit quarterly; consolidate thin posts, update outdated ones, redirect cannibalized URLs |
| No content-to-product connection | Content that never mentions your product cannot generate pipeline | Include a relevant product CTA in every MOFU/BOFU piece; link TOFU content to problem-aware landing pages |
| Measuring only vanity metrics | Pageviews and social likes do not pay salaries | Track email signups, demo requests, and pipeline influenced alongside traffic |

---

## Gotchas

1. **Content calendar without deadlines is fiction** - A calendar with "aspirational" publish dates is not a calendar. Dates must be committed and tied to an owner. Without a hard publish date, work expands to fill all available time and cadence collapses.

2. **Repurposing means format change, not copy-paste** - Copying a blog post into LinkedIn as-is is not repurposing - it performs poorly and signals low effort. Format must change: a 2,000-word post becomes a 7-post thread that distills the key insights, not a wall of text.

3. **Pillar pages without cluster links don't work** - A pillar page with no internal links to spoke articles is just a long article. The SEO benefit comes from the bidirectional link structure. Build the cluster first, then wire the links.

4. **Targeting high-volume keywords too early** - New domains cannot rank for head terms (10K+ monthly searches) regardless of content quality. Begin with long-tail, low-competition keywords (<1K searches/month) to build domain authority before competing for volume.

5. **Publishing without a distribution plan reaches no one** - Great content without promotion earns zero traffic. Treat distribution as a production step, not an afterthought. Plan social, email, and outreach before writing begins.

---

## References

For detailed templates and structures, read the relevant file from `references/`:

- `references/content-templates.md` - Blog post, case study, and whitepaper templates

Only load a references file if the current task requires detailed templates or
structural scaffolding.

---

## Companion check

> On first activation of this skill in a conversation: check which companion skills are installed by running `ls ~/.claude/skills/ ~/.agent/skills/ ~/.agents/skills/ .claude/skills/ .agent/skills/ .agents/skills/ 2>/dev/null`. Compare the results against the `recommended_skills` field in this file's frontmatter. For any that are missing, mention them once and offer to install:
> ```
> npx skills add AbsolutelySkilled/AbsolutelySkilled --skill <name>
> ```
> Skip entirely if `recommended_skills` is empty or all companions are already installed.
