---
name: faion-marketing-manager
description: "Marketing Manager role: GTM strategy, landing pages, copywriting, SEO/SEM, content marketing, social media, email campaigns, ads (Google, Meta), analytics, A/B testing, conversion optimization. 72 methodologies."
user-invocable: false
allowed-tools: Read, Write, Edit, Task, WebSearch, AskUserQuestion, TodoWrite, Glob
---

# Marketing Domain Skill

**Communication: User's language. Content: target audience language.**

## Purpose

Orchestrates all marketing activities from go-to-market strategy to growth experiments. Covers GTM planning, landing pages, content marketing, SEO, paid ads, email marketing, social media, and growth hacking.

## Merged From

| Original Skill | Content |
|----------------|---------|
| faion-gtm-manifest | GTM Manifest from research data |
| faion-landing-page | High-converting landing pages |

---

## Agents

| Agent | Purpose | Modes/Skills |
|-------|---------|--------------|
| faion-landing-agent | Landing page orchestrator | analyze, copy, design |
| faion-content-agent | Content marketing, SEO | faion-analytics-skill |
| faion-email-agent | Email marketing campaigns | - |
| faion-social-agent | Social media marketing | - |
| faion-growth-agent | Growth hacking, experiments | faion-analytics-skill |
| faion-ads-agent | Paid advertising | faion-meta-ads-skill, faion-google-ads-skill |

**Landing Agent Mode Mapping:**
| Mode | Replaces | Purpose |
|------|----------|---------|
| analyze | faion-landing-agent (mode: analyze) | Conversion audit, A/B tests |
| copy | faion-landing-agent (mode: copy) | AIDA/PAS copy, headlines |
| design | faion-landing-agent (mode: design) | HTML/Tailwind, mobile-first |

---

## References

Detailed technical context for specialized areas:

| Reference | Content | Lines |
|-----------|---------|-------|
| [seo.md](references/seo.md) | Technical SEO, AEO, Core Web Vitals | ~560 |
| [google-ads.md](references/google-ads.md) | Search, Display, Performance Max | ~1470 |
| [meta-ads.md](references/meta-ads.md) | Facebook, Instagram ads | ~1100 |
| [image-generation.md](references/image-generation.md) | DALL-E, Midjourney, Flux | ~1300 |
| [video-generation.md](references/video-generation.md) | Sora, Runway, Pika | ~860 |
| [audio-production.md](references/audio-production.md) | TTS, voice cloning, podcasts | ~1300 |
| [analytics.md](references/analytics.md) | Mixpanel, PostHog, GA4 | ~1470 |

**Total:** ~8,060 lines of technical reference

---

## Workflows

### Workflow 1: GTM Manifest Creation

```
Read product research → AskUserQuestion (sales model, timeline) → Generate 12 sections → Combine into gtm-manifest-full.md
```

**Prerequisites:** Completed research in `product_docs/`:
- market-research.md
- competitive-analysis.md
- user-personas.md
- pricing-research.md

**Output:**
```
product_docs/gtm-manifest/
├── 01-executive-summary.md
├── 02-market-context.md
├── 03-icp.md
├── 04-value-proposition.md
├── 05-positioning.md
├── 06-messaging-framework.md
├── 07-pricing-packaging.md
├── 08-sales-model.md
├── 09-marketing-channels.md
├── 10-launch-plan.md
├── 11-success-metrics.md
├── 12-risks-mitigations.md
└── gtm-manifest-full.md
```

### Workflow 2: Landing Page Creation

```
Discovery → Copy (AIDA/PAS) → Design → Implementation → Analysis
```

### Workflow 3: Content Marketing

```
Keyword Research → Content Plan → Creation → Optimization → Distribution
```

### Workflow 4: Growth Experiments

```
Hypothesis → Experiment Design → Run → Analyze → Learn → Iterate
```

---

## Methodologies (72)

### GTM Strategy (12)

#### M-MKT-001: Executive Summary

**Problem:** No clear GTM overview for stakeholders.

**Framework:**
```markdown
## Executive Summary

### Vision
[One-sentence vision statement]

### Market Opportunity
- TAM: $X
- SAM: $Y
- SOM: $Z

### Strategy
[3-5 bullet point strategy]

### Timeline
- Month 1-3: [Phase 1]
- Month 4-6: [Phase 2]
```

**Agent:** faion-content-agent

#### M-MKT-002: Market Context Analysis

**Problem:** GTM not grounded in market reality.

**Framework:**
| Section | Content |
|---------|---------|
| TAM/SAM/SOM | Market size with sources |
| Trends | 3-5 relevant market trends |
| Timing | Why now is the right time |
| Regulatory | Compliance considerations |

**Agent:** faion-market-researcher-agent

#### M-MKT-003: ICP Definition

**Problem:** Target customer unclear.

**Framework:**
```markdown
## Ideal Customer Profile

### Demographics
- Industry: [sectors]
- Company Size: [employees/revenue]
- Geography: [regions]

### Psychographics
- Goals: [what they want to achieve]
- Challenges: [pain points]
- Values: [what matters to them]

### Buying Behavior
- Budget: [typical spend]
- Decision Process: [who decides]
- Buying Triggers: [what causes purchase]
```

**Agent:** faion-persona-builder-agent

#### M-MKT-004: Value Proposition Design

**Problem:** Unclear differentiation.

**Framework:**
```markdown
For [target customer]
Who [needs/wants]
Our [product]
Is a [category]
That [key benefit]
Unlike [competitors]
We [unique differentiator]
```

**Agent:** faion-content-agent

#### M-MKT-005: Positioning Statement

**Problem:** Inconsistent positioning.

**Framework:**
| Element | Question |
|---------|----------|
| Target | Who are we for? |
| Category | What category do we compete in? |
| Benefit | What's the main benefit? |
| Proof | Why should they believe us? |

**Agent:** faion-content-agent

#### M-MKT-006: Messaging Framework

**Problem:** Inconsistent messaging across channels.

**Framework:**
```markdown
## Messaging Framework

### Core Message
[One sentence that captures essence]

### Headlines
1. [Primary headline]
2. [Alternative 1]
3. [Alternative 2]

### Tagline
[Short memorable phrase]

### Proof Points
1. [Statistic or fact]
2. [Customer quote]
3. [Feature benefit]

### Objection Handling
| Objection | Response |
|-----------|----------|
| "Too expensive" | [Response] |
| "Too complex" | [Response] |
```

**Agent:** faion-landing-agent (mode: copy)

#### M-MKT-007: Pricing Strategy

**Problem:** Pricing not aligned with value.

**Framework:**
| Model | Best For |
|-------|----------|
| Freemium | User acquisition, PLG |
| Per-seat | Team collaboration tools |
| Usage-based | Variable consumption |
| Tiered | Different customer segments |

**Pricing Checklist:**
- [ ] Competitor price analysis
- [ ] Cost + margin calculation
- [ ] Value-based pricing research
- [ ] Price sensitivity testing

**Agent:** faion-pricing-researcher-agent

#### M-MKT-008: Sales Model Selection

**Problem:** Wrong sales approach for product.

**Framework:**
| Model | ACV | Characteristics |
|-------|-----|-----------------|
| PLG | < $1K | Self-serve, product-led |
| Inside Sales | $1K-$25K | Remote selling |
| Field Sales | > $25K | Enterprise, high-touch |
| Channel | Varies | Partner-led |

**Agent:** faion-growth-agent

#### M-MKT-009: Channel Strategy

**Problem:** Scattered marketing efforts.

**Framework:**
| Channel | Goal | Priority |
|---------|------|----------|
| SEO | Organic traffic | P1 |
| Content | Authority building | P1 |
| Paid Ads | Quick acquisition | P2 |
| Social | Brand awareness | P2 |
| Email | Nurturing | P1 |
| Partnerships | Reach extension | P3 |

**Agent:** faion-growth-agent

#### M-MKT-010: Launch Plan

**Problem:** Uncoordinated launches.

**Framework:**
```markdown
## Launch Plan

### Pre-Launch (4 weeks before)
- [ ] Landing page ready
- [ ] Email list warmed
- [ ] Press contacts prepared
- [ ] Beta users testimonials

### Launch Week
- Day 1: Product Hunt
- Day 2: Press coverage
- Day 3: Social push
- Day 4-5: Influencer content
- Weekend: Community engagement

### Post-Launch
- Week 2: Iterate on feedback
- Week 3-4: Case studies
- Month 2: Expand channels
```

**Agent:** faion-growth-agent

#### M-MKT-011: Success Metrics Definition

**Problem:** No clear success criteria.

**Framework:**
| Metric | Target | Timeframe |
|--------|--------|-----------|
| MRR | $10K | Month 6 |
| Signups | 1000 | Month 3 |
| Activation Rate | 40% | Ongoing |
| Churn | < 5% | Monthly |
| NPS | > 50 | Quarterly |

**Agent:** faion-growth-agent

#### M-MKT-012: Risk Mitigation

**Problem:** Unidentified GTM risks.

**Framework:**
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Low conversion | High | High | A/B test messaging |
| Channel dependency | Medium | High | Diversify channels |
| Competitor response | Medium | Medium | Monitor, differentiate |

**Agent:** faion-growth-agent

### Landing Page (12)

#### M-MKT-013: AIDA Framework

**Problem:** Copy doesn't convert.

**Framework:**
| Stage | Purpose | Elements |
|-------|---------|----------|
| **Attention** | Stop the scroll | Bold headline, striking visual |
| **Interest** | Engage reader | Problem statement, story |
| **Desire** | Create want | Benefits, social proof |
| **Action** | Get conversion | Clear CTA, urgency |

**Agent:** faion-landing-agent (mode: copy)

#### M-MKT-014: PAS Framework

**Problem:** Not addressing pain effectively.

**Framework:**
| Stage | Purpose | Elements |
|-------|---------|----------|
| **Problem** | Identify pain | State the problem clearly |
| **Agitate** | Intensify pain | Show consequences |
| **Solution** | Present answer | Your product as savior |

**Best for:** Aware audience who knows they have a problem.

**Agent:** faion-landing-agent (mode: copy)

#### M-MKT-015: Above the Fold Design

**Problem:** No clear value proposition on landing.

**Framework:**
| Element | Required | Purpose |
|---------|----------|---------|
| Headline | Yes | Main value proposition |
| Subheadline | Yes | Supporting detail |
| Hero image/video | Yes | Visual demonstration |
| CTA button | Yes | Primary conversion |
| Trust badges | Optional | Credibility |

**Agent:** faion-landing-agent (mode: design)

#### M-MKT-016: Social Proof Strategy

**Problem:** No credibility signals.

**Framework:**
| Type | Format |
|------|--------|
| Testimonials | Quote + photo + name + title |
| Logos | "Trusted by X, Y, Z" |
| Numbers | "10,000+ customers" |
| Reviews | Stars + snippets |
| Case studies | Before/after results |

**Agent:** faion-landing-agent (mode: design)

#### M-MKT-017: CTA Optimization

**Problem:** Low click-through rates.

**Framework:**
| Element | Best Practice |
|---------|---------------|
| Copy | Action-oriented, benefit-focused |
| Color | High contrast, stands out |
| Size | Large enough, not overwhelming |
| Position | Above fold + end of sections |
| Urgency | Limited time/quantity when true |

**Good:** "Start Free Trial" / "Get My Report"
**Bad:** "Submit" / "Click Here"

**Agent:** faion-landing-agent (mode: analyze)

#### M-MKT-018: Mobile-First Design

**Problem:** Desktop-only thinking.

**Framework:**
| Element | Mobile Consideration |
|---------|---------------------|
| Typography | Min 16px body text |
| Buttons | Min 44px touch target |
| Forms | Single column, minimal fields |
| Images | Compressed, responsive |
| CTA | Sticky bottom or prominent |

**Agent:** faion-landing-agent (mode: design)

#### M-MKT-019: Form Optimization

**Problem:** Form abandonment.

**Framework:**
| Rule | Implementation |
|------|----------------|
| Minimal fields | Only essential info |
| Progressive disclosure | Multi-step if needed |
| Inline validation | Real-time feedback |
| Clear labels | Above field, not placeholder |
| Smart defaults | Pre-fill when possible |

**Agent:** faion-landing-agent (mode: analyze)

#### M-MKT-020: Page Speed Optimization

**Problem:** Slow load = lost conversions.

**Framework:**
| Target | Threshold |
|--------|-----------|
| LCP | < 2.5s |
| FID | < 100ms |
| CLS | < 0.1 |
| Total load | < 3s |

**Techniques:**
- Image optimization (WebP, lazy loading)
- Minify CSS/JS
- CDN for static assets
- Defer non-critical scripts

**Agent:** faion-landing-agent (mode: design)

#### M-MKT-021: Conversion Rate Benchmarks

**Problem:** No baseline for performance.

**Framework:**
| Industry | Average CR | Good CR | Excellent CR |
|----------|------------|---------|--------------|
| SaaS | 3-5% | 5-10% | 10%+ |
| E-commerce | 1-3% | 3-5% | 5%+ |
| B2B | 2-4% | 4-8% | 8%+ |

**Agent:** faion-landing-agent (mode: analyze)

#### M-MKT-022: A/B Testing Framework

**Problem:** No systematic testing.

**Framework:**
```markdown
## A/B Test Plan

### Hypothesis
Changing [element] from [current] to [new] will increase [metric] by [%]

### Test Setup
- Control: [Current version]
- Variant: [New version]
- Traffic: 50/50
- Duration: 2 weeks minimum

### Success Criteria
- Statistical significance: 95%
- Sample size: [calculated]
- Primary metric: [conversion rate]
```

**Agent:** faion-landing-agent (mode: analyze)

#### M-MKT-023: Heat Map Analysis

**Problem:** Unknown user behavior.

**Framework:**
| Type | Insight |
|------|---------|
| Click map | Where users click |
| Scroll map | How far they scroll |
| Move map | Where attention goes |
| Rage clicks | Frustration points |

**Tools:** Hotjar, FullStory, Microsoft Clarity

**Agent:** faion-landing-agent (mode: analyze)

#### M-MKT-024: Landing Page Checklist

**Problem:** Missing critical elements.

**Framework:**
- [ ] Single clear CTA goal
- [ ] Message match (ad → page)
- [ ] Benefits > features
- [ ] Social proof present
- [ ] Mobile responsive
- [ ] Fast load (< 3s)
- [ ] Contrast CTA button
- [ ] Trust signals
- [ ] Clear headline
- [ ] No navigation distractions

**Agent:** faion-landing-agent (mode: analyze)

### Content Marketing (12)

#### M-MKT-025: Keyword Research

**Problem:** Content not discoverable.

**Framework:**
| Step | Action |
|------|--------|
| Seed keywords | List 10-20 topic areas |
| Expand | Use tools (Ahrefs, SEMrush) |
| Filter | Volume > 100, KD < 50 |
| Categorize | Informational, commercial, transactional |
| Prioritize | Low competition, high intent |

**Agent:** faion-content-agent

#### M-MKT-026: Content Pillar Strategy

**Problem:** Scattered content, no authority.

**Framework:**
```
Pillar Page (broad topic)
├── Cluster 1 (subtopic)
│   ├── Article 1.1
│   ├── Article 1.2
│   └── Article 1.3
├── Cluster 2 (subtopic)
│   ├── Article 2.1
│   └── Article 2.2
└── Cluster 3 (subtopic)
    ├── Article 3.1
    └── Article 3.2

All cluster articles link to pillar page.
```

**Agent:** faion-content-agent

#### M-MKT-027: Content Calendar

**Problem:** Inconsistent publishing.

**Framework:**
| Week | Topic | Format | Channel | Owner |
|------|-------|--------|---------|-------|
| 1 | [Topic A] | Blog | Website | [Name] |
| 1 | [Topic A] | LinkedIn | Social | [Name] |
| 2 | [Topic B] | Video | YouTube | [Name] |

**Agent:** faion-content-agent

#### M-MKT-028: SEO On-Page Optimization

**Problem:** Content not ranking.

**Framework:**
| Element | Best Practice |
|---------|---------------|
| Title tag | Keyword + benefit, < 60 chars |
| Meta description | Compelling, 120-160 chars |
| H1 | Single, contains keyword |
| H2-H6 | Logical hierarchy |
| URL | Short, keyword-rich |
| Images | Alt text, compressed |
| Internal links | 3-5 per article |

**Agent:** faion-content-agent

#### M-MKT-029: Content Repurposing

**Problem:** Content creation too time-consuming.

**Framework:**
```
Blog Post
├── → LinkedIn article
├── → Twitter thread
├── → Newsletter
├── → Infographic
├── → Short video
├── → Podcast episode
└── → Slide deck
```

**Agent:** faion-content-agent

#### M-MKT-030: Link Building Strategy

**Problem:** Low domain authority.

**Framework:**
| Method | Effort | Quality |
|--------|--------|---------|
| Guest posting | High | High |
| HARO | Medium | High |
| Broken link building | Medium | Medium |
| Resource pages | Low | Medium |
| Podcast appearances | Medium | High |

**Agent:** faion-content-agent

#### M-MKT-031: Content Performance Analysis

**Problem:** No content ROI tracking.

**Framework:**
| Metric | Tool | Target |
|--------|------|--------|
| Organic traffic | GA4 | +20% MoM |
| Rankings | SEMrush | Top 10 for keywords |
| Engagement | GA4 | > 3 min avg time |
| Conversions | GA4 | > 2% conversion |
| Backlinks | Ahrefs | +10 per month |

**Agent:** faion-analytics-skill

#### M-MKT-032: Blog Post Template

**Problem:** Inconsistent article structure.

**Framework:**
```markdown
# [Title with keyword]

[Hook: Problem or question]

[Preview: What reader will learn]

## [H2: First main point]
[Content with examples]

## [H2: Second main point]
[Content with examples]

## [H2: Third main point]
[Content with examples]

## Key Takeaways
- [Summary point 1]
- [Summary point 2]
- [Summary point 3]

## Next Steps
[CTA or related content]
```

**Agent:** faion-content-agent

#### M-MKT-033: Long-form Content Structure

**Problem:** Long content lacks readability.

**Framework:**
| Element | Purpose |
|---------|---------|
| Table of contents | Navigation |
| Key takeaways box | Quick summary |
| Subheadings every 300 words | Scanability |
| Bullet lists | Easy reading |
| Images/diagrams | Visual breaks |
| Callout boxes | Important points |
| Expert quotes | Credibility |

**Agent:** faion-content-agent

#### M-MKT-034: Video Content Strategy

**Problem:** No video presence.

**Framework:**
| Type | Length | Platform |
|------|--------|----------|
| Shorts | < 60s | YouTube, TikTok |
| Tutorials | 5-15 min | YouTube |
| Webinars | 30-60 min | YouTube, site |
| Testimonials | 1-2 min | Website, ads |

**Agent:** faion-content-agent

#### M-MKT-035: Podcast Strategy

**Problem:** Missing audio channel.

**Framework:**
| Element | Approach |
|---------|----------|
| Format | Interview, solo, or both |
| Length | 20-45 min optimal |
| Schedule | Weekly consistency |
| Distribution | Apple, Spotify, RSS |
| Repurpose | Clips for social |

**Agent:** faion-content-agent

#### M-MKT-036: Content Governance

**Problem:** Outdated, inconsistent content.

**Framework:**
| Frequency | Action |
|-----------|--------|
| Monthly | Review top 10 pages |
| Quarterly | Content audit |
| Annually | Full refresh |

**Audit criteria:**
- Still accurate?
- Still ranking?
- Can be combined?
- Should be deleted?

**Agent:** faion-content-agent

### Email Marketing (12)

#### M-MKT-037: Welcome Sequence

**Problem:** Poor first impressions.

**Framework:**
| Day | Email | Purpose |
|-----|-------|---------|
| 0 | Welcome | Set expectations |
| 1 | Best content | Deliver value |
| 3 | Story | Build connection |
| 5 | Case study | Show results |
| 7 | Offer | First conversion |

**Agent:** faion-email-agent

#### M-MKT-038: Nurture Sequence

**Problem:** Leads going cold.

**Framework:**
```
Lead enters sequence
├── Week 1: Educational content
├── Week 2: Problem/solution
├── Week 3: Social proof
├── Week 4: Feature highlight
└── Week 5: Offer + urgency
```

**Agent:** faion-email-agent

#### M-MKT-039: Email Copywriting Formula

**Problem:** Low open and click rates.

**Framework:**
| Element | Best Practice |
|---------|---------------|
| Subject | Curiosity, benefit, or urgency |
| Preview text | Complement subject |
| Opening | Personal, hook |
| Body | One idea, scannable |
| CTA | Single, clear action |
| P.S. | Second chance message |

**Agent:** faion-email-agent

#### M-MKT-040: Subject Line Formulas

**Problem:** Emails not opened.

**Framework:**
| Type | Example |
|------|---------|
| Question | "Is your landing page losing you customers?" |
| Number | "5 ways to increase conversions" |
| How-to | "How to write emails that convert" |
| Urgency | "Last chance: 50% off ends tonight" |
| Curiosity | "The #1 mistake 90% of founders make" |

**Agent:** faion-email-agent

#### M-MKT-041: Email Segmentation

**Problem:** One-size-fits-all messaging.

**Framework:**
| Segment | Criteria | Content Type |
|---------|----------|--------------|
| New leads | < 7 days | Educational |
| Engaged | > 3 opens | Product-focused |
| Inactive | No opens 30 days | Re-engagement |
| Customers | Has purchased | Upsell, support |

**Agent:** faion-email-agent

#### M-MKT-042: Email Automation Flows

**Problem:** Manual email work.

**Framework:**
| Trigger | Flow |
|---------|------|
| Signup | Welcome sequence |
| Download | Lead nurture |
| Cart abandon | Recovery sequence |
| Purchase | Onboarding sequence |
| Churn risk | Win-back sequence |

**Agent:** faion-email-agent

#### M-MKT-043: Newsletter Strategy

**Problem:** No consistent communication.

**Framework:**
| Element | Approach |
|---------|----------|
| Frequency | Weekly or bi-weekly |
| Format | Curated + original |
| Value | 80% value, 20% promo |
| Personal | From a person, not brand |
| CTA | One primary action |

**Agent:** faion-email-agent

#### M-MKT-044: Email Deliverability

**Problem:** Emails going to spam.

**Framework:**
| Factor | Action |
|--------|--------|
| Authentication | SPF, DKIM, DMARC |
| Reputation | Monitor sender score |
| Content | Avoid spam triggers |
| List hygiene | Remove bounces, inactive |
| Engagement | Maintain > 20% open rate |

**Agent:** faion-email-agent

#### M-MKT-045: Email A/B Testing

**Problem:** No email optimization.

**Framework:**
| Element | Test Variations |
|---------|-----------------|
| Subject | Length, emoji, personalization |
| Send time | Day, hour |
| CTA | Copy, color, placement |
| Content | Long vs short |
| From name | Person vs brand |

**Agent:** faion-email-agent

#### M-MKT-046: Email Metrics Benchmarks

**Problem:** Unknown email performance.

**Framework:**
| Metric | Average | Good | Excellent |
|--------|---------|------|-----------|
| Open rate | 20% | 25% | 30%+ |
| Click rate | 2% | 4% | 6%+ |
| Unsubscribe | 0.5% | < 0.3% | < 0.1% |
| Bounce | 2% | < 1% | < 0.5% |

**Agent:** faion-email-agent

#### M-MKT-047: Re-engagement Campaigns

**Problem:** Inactive subscribers.

**Framework:**
| Day | Email | Purpose |
|-----|-------|---------|
| 0 | "We miss you" | Reconnect |
| 3 | Best content | Value reminder |
| 7 | Special offer | Incentive |
| 14 | Last chance | Final attempt |
| 21 | Unsubscribe | Clean list |

**Agent:** faion-email-agent

#### M-MKT-048: Transactional Email Optimization

**Problem:** Transactional emails underutilized.

**Framework:**
| Email | Marketing Opportunity |
|-------|----------------------|
| Order confirmation | Cross-sell, referral |
| Shipping notification | Social share CTA |
| Password reset | Feature highlight |
| Invoice | Upgrade offer |

**Agent:** faion-email-agent

### Paid Advertising (12)

#### M-MKT-049: Facebook/Meta Ads Structure

**Problem:** Unorganized ad accounts.

**Framework:**
```
Campaign (Objective)
├── Ad Set 1 (Audience A)
│   ├── Ad 1 (Creative variant)
│   └── Ad 2 (Creative variant)
├── Ad Set 2 (Audience B)
│   ├── Ad 1
│   └── Ad 2
└── Ad Set 3 (Retargeting)
    ├── Ad 1
    └── Ad 2
```

**Agent:** faion-ads-agent

#### M-MKT-050: Google Ads Structure

**Problem:** Messy Google Ads account.

**Framework:**
```
Campaign (Theme/Product)
├── Ad Group 1 (Keyword cluster)
│   ├── Keywords (10-20)
│   └── Ads (3-5 RSAs)
├── Ad Group 2 (Keyword cluster)
│   ├── Keywords
│   └── Ads
└── Ad Group 3 (Keyword cluster)
```

**Agent:** faion-ads-agent

#### M-MKT-051: Audience Targeting Strategy

**Problem:** Wrong audience, wasted spend.

**Framework:**
| Audience Type | Platform | Use Case |
|---------------|----------|----------|
| Interest | Meta | Awareness |
| Lookalike | Meta | Expansion |
| Keyword | Google | Intent |
| Retargeting | Both | Conversion |
| Custom list | Both | Upsell |

**Agent:** faion-ads-agent

#### M-MKT-052: Ad Creative Framework

**Problem:** Low-performing creatives.

**Framework:**
| Element | Requirement |
|---------|-------------|
| Hook | First 3 seconds grab attention |
| Problem | Show pain point |
| Solution | Your product |
| Proof | Testimonial/results |
| CTA | Clear next step |

**Agent:** faion-ads-agent

#### M-MKT-053: Ad Copy Formulas

**Problem:** Boring ad copy.

**Framework:**
| Formula | Structure |
|---------|-----------|
| Before-After-Bridge | Before state → After state → Product is the bridge |
| Problem-Agitate-Solve | Problem → Make it worse → Solution |
| Feature-Advantage-Benefit | What it is → Why it's better → What you get |

**Agent:** faion-ads-agent

#### M-MKT-054: Retargeting Strategy

**Problem:** Losing interested visitors.

**Framework:**
| Audience | Timing | Message |
|----------|--------|---------|
| Page viewers | 1-3 days | Reminder |
| Cart abandoners | 1-7 days | Incentive |
| Past customers | 30+ days | New product |
| Email subscribers | Ongoing | Exclusive offer |

**Agent:** faion-ads-agent

#### M-MKT-055: Ad Budget Allocation

**Problem:** Budget spread too thin.

**Framework:**
| Phase | Allocation |
|-------|------------|
| Testing | 70% testing, 30% proven |
| Scaling | 80% proven, 20% testing |

**Rule of thumb:**
- Min $50/day per ad set for learning
- Kill ads with CPA > 2x target after 1000 impressions
- Scale winners by 20% per day

**Agent:** faion-ads-agent

#### M-MKT-056: Landing Page + Ad Alignment

**Problem:** Message mismatch.

**Framework:**
| Ad Element | Landing Page Match |
|------------|-------------------|
| Headline | Same or similar |
| Offer | Exact match |
| Image | Same or related |
| CTA | Same action |
| Audience | Personalized content |

**Agent:** faion-ads-agent

#### M-MKT-057: ROAS Optimization

**Problem:** Poor return on ad spend.

**Framework:**
| Lever | Action |
|-------|--------|
| Targeting | Narrow to high-intent |
| Creative | Test new hooks |
| Offer | Increase perceived value |
| Landing | Improve conversion rate |
| Timing | Day-parting optimization |

**Target ROAS:**
- E-commerce: 3-5x
- SaaS: Consider LTV (2-3x acceptable)

**Agent:** faion-ads-agent

#### M-MKT-058: Ad Testing Framework

**Problem:** No systematic creative testing.

**Framework:**
| Phase | Test | Duration |
|-------|------|----------|
| 1 | Hooks (first 3s) | 3 days |
| 2 | Body (message) | 3 days |
| 3 | CTA | 3 days |
| 4 | Format (image/video) | 5 days |

**Agent:** faion-ads-agent

#### M-MKT-059: Attribution Modeling

**Problem:** Unknown ad contribution.

**Framework:**
| Model | Use Case |
|-------|----------|
| Last-click | Direct response |
| First-click | Awareness campaigns |
| Linear | Multi-touch journeys |
| Data-driven | Large datasets |

**Agent:** faion-analytics-skill

#### M-MKT-060: Paid Media Reporting

**Problem:** No clear performance view.

**Framework:**
| Metric | Frequency |
|--------|-----------|
| Spend | Daily |
| CPC, CPM | Daily |
| CTR | Daily |
| Conversions | Daily |
| CPA | Weekly |
| ROAS | Weekly |
| LTV:CAC | Monthly |

**Agent:** faion-ads-agent

### Social Media (6)

#### M-MKT-061: Social Media Strategy

**Problem:** Random posting, no strategy.

**Framework:**
| Platform | Goal | Content Type | Frequency |
|----------|------|--------------|-----------|
| LinkedIn | Authority | Insights, stories | 3-5/week |
| Twitter | Engagement | Threads, opinions | 5-7/week |
| Instagram | Brand | Visual, BTS | 3-5/week |
| TikTok | Reach | Entertainment | 5-7/week |

**Agent:** faion-social-agent

#### M-MKT-062: LinkedIn Content Strategy

**Problem:** No LinkedIn presence.

**Framework:**
| Content Type | Frequency | Purpose |
|--------------|-----------|---------|
| Text posts | 3/week | Insights |
| Carousels | 1/week | Education |
| Articles | 1/month | Deep dives |
| Comments | 10/day | Visibility |

**Hook formulas:**
- "I was wrong about [X]"
- "[Number] things I learned from [experience]"
- "Stop [common practice]. Here's why."

**Agent:** faion-social-agent

#### M-MKT-063: Twitter/X Strategy

**Problem:** No Twitter presence.

**Framework:**
| Content Type | Format |
|--------------|--------|
| Threads | 5-10 tweets on one topic |
| Single tweets | Opinions, questions |
| Quote tweets | Add perspective |
| Replies | Build relationships |

**Thread formula:**
1. Hook (problem/promise)
2. Story/context
3. Main points (3-7)
4. Summary
5. CTA

**Agent:** faion-social-agent

#### M-MKT-064: Community Building

**Problem:** No engaged community.

**Framework:**
| Stage | Action |
|-------|--------|
| Attract | Valuable content |
| Engage | Reply to every comment |
| Activate | Ask questions, polls |
| Advocate | Feature members |
| Retain | Exclusive content |

**Agent:** faion-social-agent

#### M-MKT-065: Influencer Partnership

**Problem:** No influencer strategy.

**Framework:**
| Type | Followers | Engagement | Cost |
|------|-----------|------------|------|
| Nano | 1K-10K | 5-10% | $ |
| Micro | 10K-100K | 3-5% | $$ |
| Macro | 100K-1M | 1-3% | $$$ |
| Mega | 1M+ | < 1% | $$$$ |

**Best ROI:** Micro-influencers with high engagement

**Agent:** faion-social-agent

#### M-MKT-066: Social Listening

**Problem:** Missing brand mentions, trends.

**Framework:**
| Monitor | Tool |
|---------|------|
| Brand mentions | Google Alerts, Mention |
| Competitors | SparkToro |
| Industry terms | BuzzSumo |
| Sentiment | Brandwatch |

**Agent:** faion-social-agent

### Growth & Operations (6)

#### M-MKT-067: AARRR Funnel Analysis

**Problem:** Unknown growth leaks.

**Framework:**
| Stage | Metric | Benchmark |
|-------|--------|-----------|
| Acquisition | Visitors | - |
| Activation | Signups | 3-5% of visitors |
| Retention | Return users | 20-40% W1 |
| Revenue | Paid conversion | 2-5% of users |
| Referral | Referral rate | 10-20% |

**Agent:** faion-growth-agent

#### M-MKT-068: Growth Experiment Framework

**Problem:** Random growth efforts.

**Framework:**
```markdown
## Experiment: [Name]

### Hypothesis
If we [change], then [metric] will [increase/decrease] by [%]

### Metrics
- Primary: [conversion rate]
- Secondary: [engagement]

### Design
- Control: [current state]
- Treatment: [change]
- Sample: [users]
- Duration: [2 weeks]

### Results
- [Metric]: X% vs Y%
- Significance: [p-value]
- Decision: [scale/kill/iterate]
```

**Agent:** faion-growth-agent

#### M-MKT-069: Referral Program Design

**Problem:** No organic growth.

**Framework:**
| Element | Best Practice |
|---------|---------------|
| Incentive | Value for both sides |
| Timing | After value moment |
| Friction | One-click sharing |
| Tracking | Unique referral codes |
| Communication | Clear what they get |

**Viral coefficient K = invites * conversion rate**
K > 1 = viral growth

**Agent:** faion-growth-agent

#### M-MKT-070: Customer Lifecycle Marketing

**Problem:** Same messaging for all users.

**Framework:**
| Stage | Goal | Tactics |
|-------|------|---------|
| Prospect | Convert | Ads, content |
| New user | Activate | Onboarding |
| Active user | Retain | Engagement |
| At-risk | Save | Win-back |
| Churned | Recover | Re-engagement |
| Advocate | Amplify | Referral |

**Agent:** faion-growth-agent

#### M-MKT-071: Competitive Intelligence

**Problem:** Unaware of competitor moves.

**Framework:**
| Monitor | Frequency | Tool |
|---------|-----------|------|
| Pricing changes | Monthly | Manual |
| New features | Bi-weekly | Product Hunt |
| Content | Weekly | SparkToro |
| Ads | Weekly | AdLibrary |
| Reviews | Weekly | G2, Capterra |

**Agent:** faion-market-researcher-agent

#### M-MKT-072: Marketing Analytics Stack

**Problem:** No clear data infrastructure.

**Framework:**
| Layer | Tool |
|-------|------|
| Data collection | GA4, Segment |
| Attribution | Triple Whale, Northbeam |
| Visualization | Looker, Metabase |
| Experimentation | Statsig, VWO |
| Customer data | CDP (Segment, RudderStack) |

**Agent:** faion-analytics-skill


> **Note:** Full methodology details available in `methodologies/` folder.

---

## Execution

### GTM Manifest Creation

```python
# Strategy questions
AskUserQuestion(
    questions=[
        {
            "question": "Sales model?",
            "options": [
                {"label": "PLG", "description": "Product-Led Growth"},
                {"label": "Sales-Led", "description": "Enterprise sales"},
                {"label": "Hybrid", "description": "PLG + Sales"}
            ]
        },
        {
            "question": "Launch timeline?",
            "options": [
                {"label": "MVP", "description": "3-6 months"},
                {"label": "Full", "description": "6-12 months"}
            ]
        }
    ]
)

# Generate sections
for section in SECTIONS:
    Task(
        subagent_type="general-purpose",
        prompt=f"""
PROJECT: {project}
SECTION: {section.name}
RESEARCH: {research_data}
OUTPUT: product_docs/gtm-manifest/{section.file}

Write {section.name} section using research data.
"""
    )
```

### Landing Page Creation

```python
# Copywriting
Task(subagent_type="faion-landing-agent (mode: copy)",
     prompt=f"PRODUCT: {p}, AUDIENCE: {a}, FRAMEWORK: AIDA")

# Design
Task(subagent_type="faion-landing-agent (mode: design)",
     prompt=f"COPY: {copy}, STYLE: {modern|minimal|bold}")

# Analysis
Task(subagent_type="faion-landing-agent (mode: analyze)",
     prompt=f"Analyze {url_or_code} for conversion")
```

### Content Marketing

```python
Task(subagent_type="faion-content-agent",
     prompt=f"Create content plan for {topic} targeting {audience}")

Task(subagent_type="faion-content-agent",
     prompt=f"Write blog post: {title}")
```

### Growth Experiments

```python
Task(subagent_type="faion-growth-agent",
     prompt=f"Design experiment to test {hypothesis}")

Task(subagent_type="faion-growth-agent",
     prompt=f"Analyze experiment results: {data}")
```

---

## Technical Skills Used

| Skill | Purpose |
|-------|---------|
| faion-meta-ads-skill | Meta Ads API |
| faion-google-ads-skill | Google Ads API |
| faion-analytics-skill | GA4, Plausible |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-research-domain-skill | Provides market data for marketing |
| faion-product-domain-skill | Provides product positioning |
| faion-seo-skill | SEO optimization |

---

*Domain Skill v1.0 - Marketing*
*72 Methodologies | 8 Agents*
*Merged from: faion-gtm-manifest, faion-landing-page*
