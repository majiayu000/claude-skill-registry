---
name: Content Strategy
model: reasoning
description: >
  Plan content aligned with user personas and journey stages. Use when asked to
  "plan content," "create content strategy," "build editorial calendar," "map
  content to personas," "audit existing content," or when aligning
  marketing/docs content with user journeys defined in persona docs.
version: 1.0.0
tags: [marketing, content, strategy, editorial]
---

# Content Strategy

Plan and organize content that serves specific user personas at each stage of their journey. Content strategy bridges the gap between knowing who your users are (personas) and delivering the right message at the right time.

## Purpose

Every piece of content should answer three questions:

1. **Who is this for?** — Which persona are we addressing?
2. **Where are they?** — What stage of their journey are they in?
3. **What do they need?** — What information moves them forward?

Content without persona alignment is noise. Strategy turns noise into signal.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install content-strategy
```


---

## Content Mapping

Map each journey stage to content goals and types. This is the backbone of your strategy.

| Stage | Goal | User Mindset | Content Types |
|-------|------|-------------|---------------|
| Awareness | Attract | "I have a problem" | Blog posts, social media, infographics, short videos, podcasts |
| Consideration | Educate | "I'm evaluating solutions" | Whitepapers, case studies, webinars, comparison guides, deep-dive articles |
| Decision | Convert | "I'm ready to choose" | Product demos, free trials, testimonials, pricing pages, ROI calculators |
| Retention | Delight | "I need to get more value" | Tutorials, newsletters, community forums, release notes, tips & tricks |
| Advocacy | Amplify | "I want to share this" | User stories, referral programs, speaking opportunities, co-branded content |

### How to Use This Map

1. Identify which personas you are targeting
2. Determine which stage they are currently in
3. Select content types from that stage's row
4. Create content that addresses their specific mindset
5. Include a clear path to the next stage

---

## Content Audit Template

Before creating new content, audit what you already have.

| URL | Title | Type | Target Persona | Journey Stage | Monthly Traffic | Quality Score (1-5) | Action Needed |
|-----|-------|------|----------------|---------------|-----------------|---------------------|---------------|
| /blog/intro | Getting Started | Blog | New Developer | Awareness | 2,400 | 4 | Update examples |
| /docs/api | API Reference | Docs | Senior Dev | Retention | 8,100 | 3 | Restructure |
| /pricing | Plans | Page | Decision Maker | Decision | 1,200 | 2 | Rewrite with social proof |

**Action categories:** Keep, Update, Consolidate, Rewrite, Archive, Delete

After auditing, you'll see gaps — stages or personas with no content. Prioritize filling those gaps.

---

## Editorial Calendar Template

Plan content on a rolling 4-week cycle with persona alignment.

### Weekly View

| Day | Content Piece | Persona | Stage | Channel | Status |
|-----|--------------|---------|-------|---------|--------|
| Mon | Blog: "5 Signs You Need X" | Startup Founder | Awareness | Blog, LinkedIn | Draft |
| Tue | Social: Key stat from whitepaper | Tech Lead | Consideration | Twitter, LinkedIn | Scheduled |
| Wed | Tutorial: Advanced config | Power User | Retention | Docs, YouTube | In Review |
| Thu | Case study: Company Y | Decision Maker | Decision | Blog, Email | Published |
| Fri | Newsletter digest | All | Retention | Email | Template |

### Monthly Planning Checklist

- Review previous month's content performance
- Identify top-performing content and why it worked
- Check persona coverage — did every persona get at least one piece?
- Check stage coverage — are any journey stages neglected?
- Align with product roadmap — upcoming launches, features, events
- Set 3-5 content goals with measurable targets
- Assign owners and deadlines for each piece
- Schedule distribution across channels

---

## Content Types Guide

| Content Type | Effort | Impact | Best Stage | Shelf Life |
|-------------|--------|--------|------------|------------|
| Blog post (short) | Low | Medium | Awareness | 6-12 months |
| Blog post (long-form) | Medium | High | Awareness/Consideration | 12-24 months |
| Social media post | Low | Low | Awareness | 1-3 days |
| Whitepaper | High | High | Consideration | 12-24 months |
| Case study | Medium | High | Decision | 12+ months |
| Webinar | High | High | Consideration | 6 months (live) |
| Comparison guide | Medium | High | Consideration | 6 months |
| Tutorial | Medium | High | Retention | Until product changes |
| Newsletter | Low | Medium | Retention | 1 week |
| User story | Medium | High | Advocacy | 12+ months |
| Documentation | High | High | Retention | Ongoing |
| Interactive tool | High | High | Decision | Until product changes |

---

## SEO Integration

Align keyword strategy with personas and search intent.

| Keyword Cluster | Search Intent | Persona | Journey Stage | Content Format |
|----------------|---------------|---------|---------------|----------------|
| "what is [concept]" | Informational | Beginner | Awareness | Blog, glossary |
| "how to [task]" | Informational | Practitioner | Awareness/Retention | Tutorial, guide |
| "[product] vs [competitor]" | Commercial | Evaluator | Consideration | Comparison guide |
| "[product] pricing" | Transactional | Decision Maker | Decision | Pricing page |
| "[product] tutorial" | Informational | Current User | Retention | Tutorial, docs |

### Search Intent Alignment

- **Informational** → Awareness and Retention content. Educate, don't sell.
- **Navigational** → Retention content. Make it easy to find what they need.
- **Commercial** → Consideration content. Compare honestly, show proof.
- **Transactional** → Decision content. Remove friction, provide clarity.

---

## Content Quality Checklist

Run every piece of content through this before publishing.

### Accuracy & Value
- Claims are factual and supported by data or sources
- Information is current and not outdated
- Content provides actionable takeaways
- Examples are realistic and relevant to the target persona

### Persona Alignment
- Target persona is identified and content speaks to their needs
- Tone matches what this persona expects
- Pain points or goals addressed are real for this persona
- Content meets the user where they are in their journey

### Call to Action
- One clear primary CTA aligned with the journey stage
- CTA is a natural next step, not a jarring sales pitch
- Awareness → "Learn more" / Consideration → "See demo" / Decision → "Start free trial"

### SEO
- Primary keyword in title, first paragraph, and one header
- Meta description written and compelling (under 160 characters)
- Internal links connect to related content at adjacent journey stages

---

## Content Repurposing

Maximize every piece of content by repurposing across formats and channels.

```
Long-form blog post (source)
├── 3-5 social media posts (pull key stats, quotes, tips)
├── Newsletter section (summarize with link)
├── Infographic (visualize data or framework)
├── Short video / reel (explain one key point)
├── Slide deck (for webinar or presentation)
└── Documentation snippet (if technical)
```

### Repurposing Rules

1. Start with your highest-effort content — repurpose down, not up
2. Adapt, don't copy-paste — each format has its own conventions
3. Link back to the source — drive traffic to the comprehensive piece
4. Spread over time — don't publish all repurposed pieces on the same day
5. Track which repurposed formats perform best — double down on those

---

## Measurement

| Content Type | Primary KPI | Target Benchmark |
|-------------|-------------|-----------------|
| Blog post | Organic pageviews | 500+ views/month |
| Whitepaper | Downloads (leads) | 5%+ conversion |
| Case study | Page views → demo requests | 3%+ to demo |
| Webinar | Registrations | 40%+ attendance |
| Tutorial | Completion rate | 70%+ completion |
| Newsletter | Open rate | 25%+ open rate |
| Social media | Engagement rate | 2%+ engagement |
| Pricing page | Conversion rate | 3%+ conversion |

Review metrics monthly. Content that underperforms for 3+ months should be audited and either improved or archived.

---

## NEVER Do

1. **Never create content without a target persona** — "everyone" is not a persona
2. **Never publish without a clear CTA** — every piece moves the reader somewhere
3. **Never ignore analytics** — gut feelings are not a content strategy
4. **Never sacrifice quality for volume** — one great piece beats five mediocre ones
5. **Never write for search engines first** — write for humans, optimize for search
6. **Never let content rot** — schedule quarterly audits, archive what's stale
7. **Never skip the editorial calendar** — ad hoc publishing leads to gaps and inconsistency

---

## Related Skills

- **copywriting**: For writing the actual copy within content pieces
- **social-content**: For platform-specific social media content
- **marketing-psychology**: For understanding what drives content engagement
- **page-cro**: For optimizing conversion on content-driven pages
