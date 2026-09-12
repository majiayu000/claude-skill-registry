---
name: newsletter
description: |
  Design, write, and grow editorial newsletters with consistent voice and format. Creates newsletter strategy, templates, and growth playbook. Use when someone wants to start a newsletter, improve an existing one, grow subscribers, write a newsletter issue, plan newsletter content, or set up on Substack, Beehiiv, Ghost, or ConvertKit. Triggers on 'newsletter', 'editorial', 'weekly email', 'subscriber growth', 'newsletter template', 'email digest', 'Substack', 'Beehiiv', 'newsletter strategy', 'newsletter issue', 'recurring email', or 'email content'. Even if they just say 'I want to email my audience regularly' or 'start a weekly email', this is the skill. Covers curated, editorial, and hybrid formats with referral programs, platform guidance, and engagement metrics.
category: distribution
tier: nice-to-have
reads:
  - brand/voice-profile.md
  - brand/audience.md
writes:
  - marketing/newsletter/strategy.md
  - marketing/newsletter/template.md
  - marketing/newsletter/issues/{date}-{slug}.md
depends-on:
  - brand-voice
triggers:
  - newsletter
  - write a newsletter
  - weekly update
  - curated email
  - editorial email
  - subscriber growth
  - newsletter strategy
  - email digest
allowed-tools: []
---

# Newsletter System

You design and write editorial newsletters that people actually look forward to receiving. Not corporate updates nobody reads — opinionated, valuable, personality-driven emails that build an audience over time.

## On Activation

1. Read `brand/voice-profile.md` — newsletters live or die by voice consistency
2. Read `brand/audience.md` — understand what they care about, how sophisticated they are
3. If starting fresh, ask: What's the newsletter about? Who's it for? What format appeals to you?
4. Check `marketing/newsletter/` for existing strategy and past issues

---

## Brand Integration

- **voice-profile.md** → Newsletters live or die by voice consistency. If voice is warm/conversational, use 'I' perspective with personal anecdotes. If authoritative/editorial, use curated insights with expert framing. The voice must feel like a person writing, not a company broadcasting.
- **audience.md** → Content selection and depth matches audience sophistication. Technical audience gets deep dives. General audience gets accessible summaries with links to learn more.

---

## Step 1: Define the Newsletter

### Newsletter Types

| Type | Description | Best For | Example |
|------|-------------|----------|---------|
| **Curated** | Best links + your commentary | Industry watchers, busy professionals | The Hustle, TLDR |
| **Editorial** | Original essays/insights | Thought leaders, opinionated founders | Stratechery, Lenny's Newsletter |
| **Hybrid** | Mix of original + curated | Most founders and creators | Morning Brew, Dense Discovery |
| **Product update** | What's new in your product | SaaS companies with active users | Linear, Notion changelogs |
| **Educational** | Teaches one skill per issue | Course creators, consultants | James Clear, Marketing Examples |

### Strategy Doc

Before writing a single issue, establish:

```yaml
---
name: "Newsletter Name"
tagline: "One-line value prop (what they get + how often)"
type: curated | editorial | hybrid | product | educational
frequency: weekly | biweekly | daily
send_day: Tuesday
send_time: "9:00 AM ET"
target_audience: "Who specifically reads this"
core_topic: "The single topic area"
voice: "How it sounds (reference voice-profile.md)"
success_metric: "Open rate > 40%, click rate > 5%"
---
```

---

## Step 2: Build the Template

Every newsletter needs a repeatable structure readers come to expect.

### Template Structure

```markdown
# [Newsletter Name] — Issue #[N]

## [Catchy issue title or theme]

### Intro (2-3 sentences)
[Personal hook — what happened this week, what's on your mind, why this issue matters]

---

### Section 1: [Main Value Block]
[The core content — original insight, deep dive, or primary curation]

### Section 2: [Secondary Value]
[Supporting content, related links, or complementary angle]

### Section 3: [Quick Hits / Links]
- **[Link title]** — One-line commentary on why it matters
- **[Link title]** — One-line commentary
- **[Link title]** — One-line commentary

---

### [Recurring Section Name]
[Something predictable readers look forward to: tool of the week, quote, stat, hot take]

---

### CTA
[One primary ask: share, reply, check out product, visit link]

---

[Sign-off in your voice]
[Name]

[Footer: unsubscribe, share link, social links]
```

### Format-Specific Templates

**Curated Newsletter:**
- 5-7 links with 2-3 sentence commentary each
- Group by theme or rank by importance
- Your opinion is the value — don't just summarize

**Editorial Newsletter:**
- One main essay (500-1,000 words)
- Strong opening hook
- Clear argument or insight
- End with a question or call to reply

**Hybrid Newsletter:**
- One short original piece (300-500 words)
- 3-5 curated links with commentary
- One recurring section (tool, quote, tip)

---

## Step 3: Write an Issue

### The Writing Process

1. **Choose the theme**: One core topic per issue. No scatter.
2. **Write the hook**: First 2 sentences determine if they read or archive. Make it personal, specific, or surprising.
3. **Deliver the value**: The thing they subscribed for. Don't bury it.
4. **Keep sections scannable**: Bold key phrases. Short paragraphs. Clear headers.
5. **Close with energy**: A question, a challenge, a forward-looking tease.

### Issue Output Format

```yaml
---
issue_number: 42
title: "Issue title"
subject: "Email subject line"
preview: "Preview text"
theme: "Core topic"
send_date: 2026-03-12
word_count: 850
status: draft
---
```

### Writing Rules

- **Personality first**: Readers subscribe for your take, not the news itself
- **One idea per section**: Don't cram. Each section has one job.
- **Scannable**: Someone skimming should get 60% of the value. Bold key points.
- **Consistent length**: Set an expectation and keep it. Plus or minus 20% variance max.
- **Predictable structure**: Readers should know where to find what they want.
- **End with a question**: The reply is the highest-engagement action. Invite it.

### AI Tells to Avoid in Newsletters

Newsletters live or die on voice. Generic AI voice is fatal — readers unsubscribe from "content," they stay for a person.

**Words to ban:** delve, comprehensive, robust, utilize, landscape, navigate, foster, empower, elevate, streamline, crucial, leverage
**Phrases to ban:** "In today's fast-paced world," "It's worth noting that," "Let's dive in," "Without further ado," "In conclusion"
**Structural tells:** Every section same length. No personal anecdotes. No opinions without hedging. Perfect grammar everywhere (real newsletters have personality quirks). No contractions.
**The test:** Read it aloud. If it sounds like a press release or a textbook, rewrite it. It should sound like a smart friend talking over coffee.

---

## Step 4: Frequency Recommendations

| Frequency | Pros | Cons | Best For |
|-----------|------|------|----------|
| Daily | Habit-forming, high engagement | Burnout risk, high content demand | News, curation-heavy |
| Weekly | Sustainable, high quality per issue | Slower growth | Most creators and businesses |
| Biweekly | Low pressure, high quality | Harder to build habit | In-depth analysis, B2B |
| Monthly | Maximum quality | Easy to forget about | Reports, roundups |

**Default recommendation**: Weekly. It's the sweet spot between staying top-of-mind and maintaining quality.

---

## Step 5: Growth Assets (Agent-Actionable)

For each newsletter, generate these growth assets:

### Signup Page Copy
Write a dedicated newsletter signup page with:
- Headline: What they get + how often ("Weekly insights for founders building in public")
- 3 bullet points: Specific value per issue
- Social proof: Subscriber count, notable readers, or open rate stats
- Single email field + subscribe button
- "No spam. Unsubscribe anytime."

### Welcome Email
Write the welcome email that triggers on signup:
- Deliver on the promise (what to expect, when)
- Ask for a reply ("What are you working on?") — boosts deliverability
- Set the relationship tone from day one

### Referral Copy
Write referral program copy with tiered rewards:
- **1 referral**: Bonus content (exclusive post, template, etc.)
- **3 referrals**: Free resource or community access
- **10 referrals**: Product discount or 1:1 consultation
- Include the share CTA copy and referral email template

### Cross-Promotion Outreach Template
Write a cross-promo pitch email for newsletters of similar size:
- Introduce your newsletter (subscriber count, niche, open rate)
- Propose mutual recommendation
- Keep it short, genuine, no-strings

### Social Teaser Copy
For each issue, generate 1-2 social posts that share a highlight and link to the archive/signup:
- Pull the most surprising or valuable line from the issue
- End with "Subscribe for more like this: [link]"

### Growth Channel Reference

| Channel | Tactic | Expected Conversion |
|---------|--------|-------------------|
| Website | Homepage signup bar, exit intent popup, blog post CTAs | 1-3% of visitors |
| Social | Pin newsletter link in bio, share issue highlights | 0.5-2% of followers |
| Cross-promo | Newsletter swaps with similar-size newsletters | 50-200 subs per swap |
| Lead magnet | Free resource into newsletter opt-in | 20-40% of landing page visitors |
| Referral | Give subscribers a referral link + incentive | 10-20% of new subs |
| Content | SEO articles with newsletter CTA | Compounding over time |

---

## Step 6: Engagement Metrics

| Metric | Good | Great | Action If Low |
|--------|------|-------|---------------|
| Open rate | 30-40% | 40-50%+ | Better subjects, clean list, check deliverability |
| Click rate | 2-4% | 5-8%+ | Better CTAs, more relevant links, clearer value |
| Reply rate | 1-2% | 3-5%+ | Ask better questions, be more personal |
| Unsubscribe | <0.5% | <0.2% | Check frequency, relevance, expectations |
| Growth rate | 5-10%/mo | 10-20%/mo | Add acquisition channels, improve lead magnets |

---

---

## Worked Example

**Newsletter: "The Build Log" — Weekly hybrid newsletter for indie hackers**

**Subject Line Variants:**
1. "The feature that almost killed our conversion rate" (recommended)
2. "Build Log #12: when metrics lie"
3. "What I learned from a $0 week"

**Preview Text:** Plus 3 tools I switched to this month

**Issue:**

```
# The Build Log — Issue #12

## The feature that almost killed our conversion rate

Last week I shipped a "smart onboarding" flow. Took 3 days to build. Looked beautiful.

Conversion dropped 23%.

Turns out, users don't want smart. They want fast. The old flow was 2 steps. The new one was 5. Each step was better — but 5 steps is 5 chances to leave.

I reverted Thursday morning. Conversion recovered by Friday.

**The lesson:** Complexity is a tax. Every step you add needs to earn 10x what it costs in drop-off.

---

### 3 things worth your time

**[Why most MVPs are too big](link)** — This thread nails it. Your MVP should embarrass you, not impress your friends.

**[Indie Hackers revenue dashboard](link)** — New feature lets you see revenue benchmarks by category. I spent 30 minutes comparing and it was worth every second.

**[PostHog's session replay](link)** — Free tier is generous. Watching real users navigate your app is humbling and instructive.

---

### Tool I switched to

**Plausible Analytics** — Replaced Google Analytics. Lighter, privacy-friendly, and I actually look at the dashboard now because it's not overwhelming.

---

What's the last feature you shipped that backfired? Hit reply — I read everything.

— James
```

---

## Output Structure

```
marketing/newsletter/
├── strategy.md                    # Newsletter definition and strategy
├── template.md                    # Repeatable issue template
├── growth-plan.md                 # Acquisition and referral strategy
└── issues/
    ├── 2026-03-12-issue-title.md  # Individual issues
    └── ...
```

**Integration**: Issues output in plain text format compatible with `gws` CLI for sending.

See [references/archetype-templates.md](references/archetype-templates.md) for the detailed output presentation format (visual summary with subject line variants, send recommendations, files saved, and what's next sections).

---

## References

- [newsletter-examples.md](references/newsletter-examples.md): Detailed breakdowns of 7 top newsletters (Lenny, Morning Brew, Ben's Bites, Sahil Bloom, Greg Isenberg, The Hustle, Rundown AI) with voice markers and sample structures
- [archetype-templates.md](references/archetype-templates.md): 6 format templates, platform guidance (Beehiiv, Substack, Kit, Ghost), growth strategies, monetization frameworks, and output presentation format

---

## Related Skills

- **brand-voice**: Establish voice before writing
- **content-atomizer**: Break newsletter issues into social posts
- **email-sequences**: Automated sequences (welcome, etc.) complement the newsletter
- **lead-magnet**: Create opt-in resources that feed the newsletter list
- **seo-content**: Blog content that drives newsletter signups
