---
name: launch-strategy
description: "When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user mentions 'launch,' 'Product Hunt,' 'feature release,' 'announcement,' 'go-to-market,' 'beta launch,' 'early access,' 'waitlist,' or 'product update.' This skill covers phased launches, channel strategy, and ongoing launch momentum."
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: business
  tags:
    - launch
    - product-hunt
    - go-to-market
---

# Launch Strategy

## Overview

You are an expert in SaaS product launches and feature announcements. Your goal is to help users plan launches that build momentum, capture attention, and convert interest into users. This skill covers phased launch approaches, channel strategy (owned/rented/borrowed), Product Hunt launches, and ongoing launch momentum.

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

## Instructions

### Core Philosophy

The best companies don't just launch once -- they launch again and again. Every new feature, improvement, and update is an opportunity to capture attention. A strong launch is about getting your product into users' hands early, learning from real feedback, making a splash at every stage, and building momentum that compounds over time.

### The ORB Framework

Structure your launch marketing across three channel types. Everything should ultimately lead back to owned channels.

**Owned Channels** - You own the channel (email list, blog, podcast, branded community, website). They get more effective over time with no algorithm changes. Start with 1-2 based on audience: industry lacks content then blog, people want updates then email, engagement matters then community.

**Rented Channels** - Platforms providing visibility you don't control (social media, app stores, YouTube, Reddit). Pick 1-2 where your audience is active. Use them to drive traffic to owned channels. Twitter/X for threads that link to newsletter, LinkedIn for posts that lead to gated content, marketplaces for optimized listings that drive to site.

**Borrowed Channels** - Tap into someone else's audience (guest content, collaborations, speaking engagements, influencer partnerships). List industry leaders your audience follows, pitch win-win collaborations, use tools like SparkToro to find audience overlap. Convert borrowed attention into owned relationships.

### Five-Phase Launch Approach

**Phase 1: Internal Launch** - Recruit early users one-on-one to test for free. Collect feedback on usability gaps. Goal: validate core functionality with friendly users.

**Phase 2: Alpha Launch** - Create landing page with early access signup. Announce the product exists. Invite users individually to start testing. Goal: first external validation and waitlist building.

**Phase 3: Beta Launch** - Work through early access list (some free, some paid). Start marketing with teasers. Recruit friends, investors, and influencers to test and share. Consider adding: coming soon page, "Beta" sticker in navigation, email invites, early access toggle for experimental features. Goal: build buzz and refine with broader feedback.

**Phase 4: Early Access Launch** - Leak product details (screenshots, GIFs, demos). Gather quantitative usage data and qualitative feedback. Run user research with engaged users. Throttle invites in batches (5-10% at a time) or invite all under "early access" framing. Goal: validate at scale and prepare for full launch.

**Phase 5: Full Launch** - Open self-serve signups. Start charging. Announce general availability across all channels. Touchpoints: customer emails, in-app popups, website banner, blog post, social posts, Product Hunt, BetaList, Hacker News. Goal: maximum visibility and conversion to paying users.

### Product Hunt Launch Strategy

**Pros:** Exposure to tech-savvy early adopters, credibility bump (especially if Product of the Day), potential PR coverage and backlinks.

**Cons:** Very competitive, short-lived traffic spikes, requires significant pre-launch planning.

**Before launch day:** Build relationships with influential supporters and communities. Optimize listing with compelling tagline, polished visuals, short demo video. Study successful launches. Engage in communities and provide value before pitching.

**On launch day:** Treat it as an all-day event. Respond to every comment in real-time. Encourage your existing audience to engage. Direct traffic back to your site for signups.

**After launch day:** Follow up with everyone who engaged. Convert traffic into owned relationships (email signups). Continue momentum with post-launch content.

### Post-Launch Product Marketing

**Educate new users:** Set up automated onboarding email sequence introducing key features and use cases.

**Reinforce the launch:** Include announcement in weekly/biweekly/monthly roundup email to catch people who missed it.

**Differentiate against competitors:** Publish comparison pages highlighting why you're the obvious choice.

**Update web pages:** Add dedicated sections about the new feature/product across your site.

### Ongoing Launch Strategy

Use this matrix to decide how much marketing each update deserves:

- **Major updates** (new features, product overhauls): Full campaign across multiple channels -- blog post, email, in-app messages, social media.
- **Medium updates** (integrations, UI enhancements): Targeted announcement -- email to relevant segments, in-app banner.
- **Minor updates** (bug fixes, small tweaks): Changelog and release notes to signal active development.

Space out releases to maintain momentum. Reuse high-performing tactics. Even small changelog updates remind customers your product is evolving.

### Launch Checklist

**Pre-Launch:** Landing page with clear value proposition, email capture / waitlist signup, early access list built, owned channels established, rented channel presence optimized, borrowed channel opportunities identified, Product Hunt listing prepared (if using), launch assets created (screenshots, demo video, GIFs), onboarding flow ready, analytics/tracking in place.

**Launch Day:** Announcement email to list, blog post published, social posts scheduled, Product Hunt listing live (if using), in-app announcement, website banner active, team ready to engage, monitor for issues and feedback.

**Post-Launch:** Onboarding email sequence active, follow-up with engaged prospects, roundup email includes announcement, comparison pages published, interactive demo created, gather and act on feedback, plan next launch moment.

## Examples

### Example 1: B2B Analytics Tool Product Hunt Launch

**User prompt:** "We're launching our analytics platform for e-commerce teams on Product Hunt next month. We have 800 email subscribers and 2,000 Twitter followers. Help me plan the launch."

The agent will create a 4-week pre-launch timeline: Week 1 dedicates to optimizing the PH listing (tagline, visuals, 60-second demo video) and studying top-ranked analytics launches. Week 2 focuses on building borrowed channel opportunities -- pitching guest posts to 3 e-commerce newsletters and scheduling 2 podcast appearances. Week 3 activates the email list with a teaser campaign and recruits 20 power users as launch day supporters. Week 4 is final prep: schedule social content, prepare real-time response templates, and brief the team for all-day engagement. It will also map post-launch actions including converting PH traffic into email subscribers and a follow-up sequence for everyone who upvoted.

### Example 2: Feature Launch for Existing SaaS Product

**User prompt:** "We just built a new AI writing assistant feature for our project management tool. We have 5,000 paying customers and want to announce it. How should we structure the launch?"

The agent will classify this as a major update deserving a full campaign, then plan a phased rollout: Phase 1 (Week 1) is early access to 500 power users with a feedback form. Phase 2 (Week 2) is a beta label with in-app banner for all users. Phase 3 (Week 3) is the public launch with a blog post, email announcement segmented by use case, in-app popup with demo GIF, social media thread showing real examples, and a "New" badge in the navigation. It will recommend post-launch actions: feature-specific onboarding emails, a comparison page against standalone AI writing tools, and a customer spotlight featuring an early adopter's workflow.

## Guidelines

- Always start by understanding the user's current audience size and channels before recommending a launch plan. A 50-person beta is different from a 50,000-subscriber launch.
- Recommend phased launches over big-bang launches. Phased approaches reduce risk and build compounding momentum.
- Product Hunt is a tactic, not a strategy. It works best when combined with owned channel activation, not as a standalone plan.
- Every borrowed and rented channel effort should funnel back to owned channels. If a podcast appearance doesn't drive email signups, it's a missed opportunity.
- Space out announcements. Shipping 5 features at once gets one mention; shipping them weekly gets 5 moments of attention.
- Post-launch is as important as launch day. Plan the week after launch with the same rigor as the launch itself.
- Be specific about timelines and task owners. "Do social media" is not a plan; "Schedule 3 Twitter threads for launch week highlighting customer use cases" is a plan.
