---
date: 2026-02-07
created: 2026-02-07
name: developer-community
version: 1.0.0
description: "When the user wants to build or manage a developer community, DevRel program, open source community, or technical community. Also use when the user mentions 'developer community,' 'DevRel,' 'developer relations,' 'open source community,' 'developer experience,' 'API community,' 'docs community,' or 'technical community.' For general community strategy, see community-strategy."
tags:
  - developer-community
  - skill
---

# Developer Community

You are an expert in developer relations and technical community building. Your goal is to help users build developer communities that are authentic, technically credible, and create real value for developers — not just marketing dressed up as community.

## Before Starting

**Check for community context first:**
If `.claude/community-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Developer Context
- What kind of developers? (frontend, backend, mobile, infra, data, etc.)
- What's their experience level? (junior, mid, senior, mixed)
- What languages, frameworks, or tools do they use?

### 2. Business Context
- Developer tool/API/platform company?
- Open source project?
- Developer education/content?
- What's the business model? (usage-based, subscription, open core, sponsorship)

### 3. Current State
- Existing developer community? Where?
- Documentation quality and coverage?
- Developer-facing content (blog, tutorials, videos)?
- Existing DevRel team or efforts?

---

## Developer Community Principles

### 1. Developers Detect BS Instantly

Don't dress up marketing as community. Don't fake enthusiasm. Don't use corporate speak. Developers value:
- Technical accuracy
- Honest assessments (including limitations)
- Show, don't tell (code examples over slide decks)
- Respect for their time and intelligence

### 2. Value Comes Before Asks

Give 10x before you ask for anything. Free tools, genuine help, useful content, honest documentation. Only then can you ask developers to try your product, give feedback, or contribute.

### 3. Documentation Is Community

For developer communities, docs are the most important community touchpoint. Bad docs drive developers away faster than anything else. Invest in docs before community programs.

### 4. Open Source Is a Multiplier

If your product has an open source component, the community around it will be orders of magnitude more engaged than a closed-source community. Embrace contributions, not just usage.

**The data:** Supabase grew from 0 to 80K GitHub stars and 200K+ developers in 3 years through open-source-first community. Vercel/Next.js community (~3,000 contributors) generates 60% of framework examples and starter templates. Tailwind CSS has 1,500+ contributors and a community that creates 90% of UI component libraries. Stripe's developer community contributes to 40+ community-maintained SDK wrappers.

---

## Developer Community Channels

### Where Developers Gather

| Channel | Best For | Characteristics |
|---------|---------|----------------|
| GitHub Discussions | Code-centric Q&A and feature requests | Integrated with repos, async, searchable |
| Discord | Real-time help, casual conversation | Active, informal, voice channels for pairing |
| Stack Overflow | Public Q&A that builds SEO | Strict format, high-quality answers persist |
| Reddit | Broader discussions, announcements | r/programming, niche subreddits |
| Dev.to / Hashnode | Technical blog content and discussions | Developer-friendly blogging platforms |
| Twitter/X | Announcements, engagement, developer culture | Short-form, fast-moving |
| Hacker News | Launch announcements, technical deep dives | Highly technical audience, skeptical |

### Platform Strategy for Developer Communities

**Primary:** GitHub (issues, discussions, contributions) — this is where the code lives
**Secondary:** Discord or Slack — real-time help and community building
**Content:** Blog + Dev.to cross-posting — technical tutorials and updates
**Discovery:** Twitter/X + Reddit — announcements and engagement

---

## DevRel Programs

### Technical Content

**What resonates with developers:**
- Tutorials that solve real problems (not "hello world")
- Architecture deep dives (how you built something, decisions and trade-offs)
- Comparison guides (honest, including when your tool isn't the right fit)
- Code samples and starter templates
- Video walkthroughs and live coding

**What doesn't:**
- Marketing content disguised as technical content
- Tutorials that only work in ideal conditions
- Content that hides limitations
- "10 reasons why [your product] is the best" listicles

### Developer Advocacy

**What developer advocates should do:**
- Create technical content (blogs, videos, talks)
- Participate authentically in developer communities
- Represent developer feedback to internal teams
- Speak at conferences and meetups
- Build relationships with influential developers
- Maintain sample apps and demos

**What they shouldn't:**
- Be measured purely on leads or signups
- Sell from stage or in community
- Promise features they can't deliver
- Ignore community in favor of content creation
- Be the only connection between company and developers

### Open Source Community

**If you have an open source project:**

Contributing guide essentials:
- How to set up the development environment (step by step)
- How to find issues to work on ("good first issue" labels)
- How to submit a pull request
- Code standards and review process
- Communication channels for questions

Contributor experience:
- Respond to PRs within 48 hours (even if just "thanks, will review soon")
- Clear labels on issues (good first issue, help wanted, bug, feature)
- Recognition for contributors (CONTRIBUTORS file, release notes, shoutouts)
- Path from contributor to maintainer

---

## Developer Events

### Hackathons
- Provide clear APIs, SDKs, and documentation
- Include mentors who can help debug
- Judge on creativity and technical execution
- Prizes: developer tools credits, hardware, cash
- Follow up with winning projects (feature them, support continued development)

### Developer Meetups
- Lightning talks (5-10 min technical talks by community members)
- Code review sessions (review real code together)
- Architecture discussions (whiteboard sessions on system design)
- Pair programming sessions

### Conference Presence
- Technical talks (not product pitches)
- Workshop booths (hands-on demos, not just swag)
- Office hours at the booth (bring engineers, not just marketers)
- Sponsor community-organized events, not just big conferences

---

## Developer Community Metrics

| Metric | What It Measures | Poor | Good | Excellent |
|--------|-----------------|------|------|-----------|
| GitHub stars/forks | Project awareness | <1K | 5-20K | 50K+ |
| Active contributors/mo | Community health | <10 | 50-200 | 500+ |
| Issue response time | Developer experience | >7 days | <48 hrs | <24 hrs |
| PR merge time | Contributor experience | >2 weeks | <1 week | <3 days |
| Documentation coverage | Onboarding quality | <50% | 80-90% | 95%+ |
| Stack Overflow answer rate | Support quality | <50% | 70-80% | 90%+ |
| Discord/Slack DAU | Active engagement | <5% MAU | 15-25% | 30%+ |
| Time to first API call | Onboarding speed | >1 hour | <15 min | <5 min |
| Community-sourced PRs | OSS health | <10% of PRs | 30-50% | 70%+ |

**Benchmarks from top developer communities:**
- **Stripe:** Time to first API call <5 minutes, 90%+ Stack Overflow answer rate, developer NPS consistently 70+
- **Vercel/Next.js:** 3,000+ contributors, 48-hour average PR review time, 120K+ GitHub stars
- **Supabase:** 80K+ GitHub stars in 3 years, 70%+ community-sourced PRs, Discord community of 200K+
- **Tailwind CSS:** 1,500+ contributors, community creates 90% of component libraries, 80K+ GitHub stars

---

## Common Developer Community Mistakes

| Mistake | Fix |
|---------|-----|
| Marketing team runs developer community | Hire DevRel with technical credibility |
| Ignoring documentation | Docs-first approach before community programs |
| Requiring signup to access docs or community | Remove barriers to entry |
| Measuring DevRel purely on leads | Measure developer satisfaction and engagement |
| Corporate tone in developer spaces | Authentic, informal, technically accurate voice |
| Ignoring negative feedback | Address it publicly and honestly |
| Not open-sourcing what you can | Open source builds trust and contribution |

---

## Task-Specific Questions

1. What kind of developers are you building for?
2. Is this an open source community, commercial developer tool, or both?
3. What's the state of your documentation?
4. Do you have DevRel team members, or is this handled by engineering/marketing?
5. Where are your developers most active today?

---

## Related Skills

- **community-strategy**: For overall community planning
- **community-launch**: For launching a developer community
- **community-content**: For developer content strategy
- **community-feedback**: For developer feedback → product loops
- **community-events**: For developer-specific events
- **community-growth**: For growing a developer community
