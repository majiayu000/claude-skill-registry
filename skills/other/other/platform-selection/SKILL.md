---
date: 2026-02-07
created: 2026-02-07
name: platform-selection
version: 1.0.0
description: "When the user wants to choose a community platform, compare community tools, or migrate between platforms. Also use when the user mentions 'Discord,' 'Slack,' 'Circle,' 'forum,' 'community platform,' 'where to host,' 'platform comparison,' 'migrate community,' or 'which platform.' For setting up the chosen platform, see community-ops."
tags:
  - platform-selection
  - skill
---

# Platform Selection

You are an expert in community platforms and tooling. Your goal is to help users choose the right platform for their community's specific needs, avoiding the trap of picking what's popular instead of what fits.

## Before Starting

**Check for community context first:**
If `.claude/community-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Community Profile
- Community type (professional, creator, product, learning, interest-based)
- Expected size in 12 months
- Primary engagement style (async discussion, real-time chat, events, content)

### 2. Member Needs
- Technical comfort level of members
- Where do they already spend time online?
- Do they need mobile access?
- Privacy/anonymity requirements

### 3. Business Requirements
- Budget for platform costs
- Integration needs (CRM, payment, product)
- Analytics and reporting needs
- Content ownership and data portability concerns

---

## Platform Market Data

| Platform | Estimated Community Users | Pricing (2024) | Best Audience |
|----------|-------------------------|-----------------|---------------|
| Discord | 200M+ monthly active users | Free (Nitro $9.99/mo optional) | Tech, gaming, creator, Gen Z/Millennial |
| Slack | 35M+ DAU (workspace model) | Free (limited) / $7.25+/user/mo Pro | Professional, B2B, enterprise |
| Circle | 10K+ communities hosted | $49-399/mo | Creators, courses, paid communities |
| Discourse | 30K+ forums | Free (self-hosted) / $50-300/mo cloud | OSS, technical, knowledge-heavy |
| Mighty Networks | 5K+ communities | $41-360/mo | Creator economy, coaching |
| Skool | Growing (new entrant) | $99/mo flat | Info-product creators |

**Named platform choices:** Midjourney chose Discord (16M+ members). Y Combinator uses a custom forum. Notion uses a mix of Discord (general) + ambassador community. Figma uses a custom community platform. Lenny's Newsletter uses Circle. Indie Hackers uses a custom Ember.js forum. Stripe uses GitHub Discussions + Discord.

---

## Platform Categories

### Real-Time Chat Platforms

**Discord**

Best for: Gaming, creator, developer, and tech communities. Any audience comfortable with chat-heavy interfaces.

| Strength | Limitation |
|----------|-----------|
| Free for all features | Overwhelming for non-tech audiences |
| Excellent voice/video | Content gets buried in chat scroll |
| Rich bot ecosystem | No native long-form content |
| Granular roles and permissions | No built-in email or CRM |
| Server discovery for growth | Professional audiences may resist |

**Ideal when:** Your audience is tech-savvy, values real-time interaction, you want voice channels, and you're budget-constrained.

**Slack**

Best for: Professional, B2B, and workplace-adjacent communities.

| Strength | Limitation |
|----------|-----------|
| Familiar to professionals | Free tier limitations (90-day history) |
| Clean, focused interface | Expensive at scale ($7.25+/user/mo for Pro) |
| Strong integrations | No native events or courses |
| Threaded conversations | Limited discovery/growth features |
| Slack Connect for partnerships | Channel sprawl problem |

**Ideal when:** Your members already use Slack for work, community is under 500 active members, or you're building a B2B professional network.

### Community-First Platforms

**Circle**

Best for: Creator communities, course-based communities, paid memberships.

| Strength | Limitation |
|----------|-----------|
| Built for community (spaces, events, courses) | Starts at $49/mo |
| Clean, modern interface | Smaller integration ecosystem |
| Native live streams and events | Less real-time than chat platforms |
| Membership and payment built in | Limited customization |
| Headless option for embedding | |

**Ideal when:** You're monetizing the community, offering courses, or need a polished member-facing experience.

**Mighty Networks**

Best for: Creator and coaching communities with course content.

| Strength | Limitation |
|----------|-----------|
| All-in-one (community + courses + events) | Higher price point |
| Native mobile app | Less flexible than modular tools |
| Activity feed format | Limited integrations |
| Built-in payments | Smaller ecosystem |

**Ideal when:** You want one platform for community, courses, and events without stitching tools together.

**Bettermode (formerly Tribe)**

Best for: Product communities and customer communities with a forum feel.

| Strength | Limitation |
|----------|-----------|
| Embeddable in your product | Requires more setup |
| SEO-friendly (public content) | Less real-time engagement |
| Customizable with APIs | Smaller user base |
| Gamification built in | |

**Ideal when:** You want a community embedded in your product or need SEO-friendly public discussions.

### Forum Platforms

**Discourse**

Best for: Open source, technical, and knowledge-base communities.

| Strength | Limitation |
|----------|-----------|
| Excellent for long-form discussion | Requires hosting (or paid cloud) |
| SEO-friendly by default | Higher learning curve |
| Trust level system | Not great for real-time chat |
| Open source, self-hostable | Setup requires technical skill |
| Plugin ecosystem | |

**Ideal when:** You want searchable, persistent knowledge. Long-form discussion matters more than real-time chat. Open source/self-hosting is important.

**GitHub Discussions**

Best for: Developer and open source communities.

| Strength | Limitation |
|----------|-----------|
| Native to developer workflow | Only for tech/developer audiences |
| Integrated with code repos | Limited engagement features |
| Free | No events, no real-time chat |
| Searchable and linkable | No community management tools |

**Ideal when:** Your community is centered around a codebase and your members already live in GitHub.

### Emerging and Niche

**Geneva** — Group chat redesigned. Good for social/lifestyle communities.
**Luma** — Events-first community. Good for communities built around gatherings.
**Skool** — Gamified community + courses. Popular with info-product creators.
**Forem** — Open source platform (powers dev.to). Good for content-driven communities.

---

## Decision Framework

### Step 1: Eliminate by Deal-Breakers

Check these hard requirements first:

| Requirement | Eliminates |
|-------------|-----------|
| Must be free | Circle, Mighty, Slack Pro |
| Must support 10K+ members cheaply | Slack |
| Need native courses/content | Discord, Slack, Discourse |
| Need SEO (public content) | Discord, Slack |
| Members are non-technical | Discord, Discourse self-hosted |
| Need product embedding | Most except Bettermode, Circle headless |
| Need self-hosting/data ownership | Most SaaS platforms |

### Step 2: Match to Engagement Style

| Primary Engagement | Best Platforms |
|-------------------|---------------|
| Real-time chat and voice | Discord, Slack |
| Async discussion and knowledge | Discourse, Bettermode, Circle |
| Courses and learning | Circle, Mighty, Skool |
| Events and meetups | Luma, Circle, Discord |
| Content and publishing | Forem, Bettermode, Discourse |

### Step 3: Score Remaining Options

Rate each remaining platform 1-5 on:

| Criteria | Weight | Platform A | Platform B |
|----------|--------|-----------|-----------|
| Member experience | 25% | | |
| Engagement features | 20% | | |
| Admin/moderation tools | 15% | | |
| Growth/discovery | 15% | | |
| Integrations | 10% | | |
| Cost at scale | 10% | | |
| Data portability | 5% | | |

---

## Platform Migration

If moving an existing community:

### Pre-Migration
1. **Announce early** — give 4-6 weeks notice minimum
2. **Explain why** — be honest about what's better about the new platform
3. **Run parallel** — keep old platform open during transition
4. **Migrate content** — move the most valuable discussions and resources
5. **Recruit ambassadors** — get power users to try the new platform first

### Migration Checklist
- [ ] New platform set up and tested
- [ ] Key content migrated or archived
- [ ] Redirect/link from old platform to new
- [ ] Ambassador group active on new platform
- [ ] Announcement sent via all channels
- [ ] Old platform set to read-only (not deleted)
- [ ] 30-day overlap period planned

### Common Migration Mistakes
- Deleting the old platform immediately
- Not migrating valuable content
- Expecting 100% of members to move (expect 40-60%)
- Choosing the new platform without member input

---

## Task-Specific Questions

1. What's your community type and expected size in 12 months?
2. Is real-time chat or async discussion more important?
3. What's your monthly budget for platform costs?
4. How technical are your members?
5. Do you need the community to be public (SEO) or private?
6. What tools does it need to integrate with?

---

## Related Skills

- **community-strategy**: For overall strategy before choosing a platform
- **community-ops**: For setting up and configuring the chosen platform
- **community-launch**: For launching on the new platform
- **community-metrics**: For analytics capabilities per platform
