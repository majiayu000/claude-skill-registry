---
name: growth-at-scale
description: |
  Full growth stack for products that have found traction.
  MCP servers, unified APIs, ads, newsletters, referrals.

  DO NOT USE until /dashboard shows consistent traction signal.
  This is Phase 2 - after finding product-market fit.
argument-hint: "[product-with-traction]"
---

# /growth-at-scale

Scale what's working. Only use after finding traction.

## Prerequisites

Before using this skill:
1. `/dashboard` shows consistent traffic growth (3+ weeks)
2. You know what's driving traffic (source analysis done)
3. Conversion is happening (users signing up/paying)
4. You're ready to invest time in growth infrastructure

If these aren't true, go back to experimentation with `/announce`, `/post`, `/seo-baseline`.

## What This Does

Activates the full growth stack:
1. **Unified social posting** - Multi-platform automation
2. **Paid ads** - Google, Meta, Twitter campaigns
3. **Newsletter** - Capture and nurture leads
4. **Referral program** - User-driven growth
5. **Advanced analytics** - Funnels, cohorts, attribution

## Full Stack Overview

### Layer 1: MCP Servers (API Automation)

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "google-ads": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-google-ads"]
    },
    "meta-ads": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-meta-ads"]
    },
    "social-media": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-social-media"]
    },
    "hubspot": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-hubspot"]
    }
  }
}
```

### Layer 2: Unified Social API

**Recommendation: Late (getlate.dev)**
- Single API to 13+ platforms
- Developer-friendly
- Free tier generous

Alternative: Buffer API

### Layer 3: Newsletter

**Recommendation: Buttondown**
- API-first
- Simple
- Great for developers

Alternative: ConvertKit/Kit

### Layer 4: Referral Program

**Recommendation: Dub Partners**
- Also handles link tracking
- Modern API
- Good free tier

Alternative: GrowSurf, Rewardful

### Layer 5: Advanced Analytics

**Stack:**
- PostHog - Product analytics, funnels, traffic (via pageviews)
- Stripe - Revenue
- Sentry - Errors

**NOT in our stack:** Vercel Analytics (no API/CLI/MCP - unusable)

## Skills to Build (When Needed)

### `/social` - Unified Posting

```bash
/social post "content" --platforms twitter,linkedin,threads
/social schedule "content" --at "2pm tomorrow"
/social analytics --last 7d
```

### `/ads` - Campaign Management

```bash
/ads status                    # All campaigns
/ads create google --budget 50 # New campaign
/ads pause meta campaign-123   # Pause campaign
/ads report --last 30d         # Performance report
```

### `/newsletter` - Email Campaigns

```bash
/newsletter draft "subject"    # Create draft
/newsletter send draft-123     # Send to subscribers
/newsletter stats              # Open/click rates
```

### `/referral` - Referral Program

```bash
/referral setup               # Configure program
/referral stats               # Referral metrics
/referral payout              # Process payouts
```

### `/double-down` - Orchestrator

```bash
/double-down product-name

# Triggers full workflow:
# 1. Analyze traffic sources
# 2. Identify top converting channels
# 3. Suggest content to amplify
# 4. Set up newsletter capture
# 5. Consider ads for winning channels
# 6. Set up referral program
```

## Research: What's Available

### Ad Platform APIs

| Platform | API | MCP Server | Browser Fallback |
|----------|-----|------------|------------------|
| Google Ads | REST | Exists | Yes |
| Meta Ads | Marketing API | Exists | Yes |
| Twitter/X Ads | v2 API | Partial | Yes |
| LinkedIn Ads | REST | No | Yes |
| Reddit Ads | REST | No | Yes |
| TikTok Ads | REST | No | Yes |

### Social Media APIs

| Platform | API | Notes |
|----------|-----|-------|
| Twitter/X | v2 API | Rate limited |
| LinkedIn | Marketing API | Requires approval |
| Instagram | Graph API | Via Meta |
| YouTube | Data API | For channel management |
| Threads | Via Instagram | Limited |

### Unified Social APIs

| Service | Platforms | Free Tier |
|---------|-----------|-----------|
| Late | 13+ | Generous |
| Buffer | 6+ | Limited |
| Hootsuite | 8+ | No |

### Newsletter APIs

| Service | API Quality | Developer Experience |
|---------|-------------|---------------------|
| Buttondown | Excellent | Best |
| ConvertKit | Good | Good |
| Mailchimp | Good | Complex |
| Substack | None | Manual only |

### Referral/Affiliate APIs

| Service | Type | Notes |
|---------|------|-------|
| GrowSurf | Referral | Good API |
| Dub Partners | Referral + Links | Modern |
| Rewardful | Affiliate | Stripe integration |
| Trackdesk | Affiliate | Full featured |

## Browser Automation Workflows

For platforms without APIs:

```typescript
// Substack posting
mcp__claude-in-chrome__navigate to substack
mcp__claude-in-chrome__find "new post button"
mcp__claude-in-chrome__form_input with content
mcp__claude-in-chrome__computer click publish

// Product Hunt launch
mcp__claude-in-chrome__navigate to producthunt/posts/new
// Fill in form fields
// Schedule launch
```

## When to Activate

Only activate growth-at-scale components when:

| Signal | Threshold | Action |
|--------|-----------|--------|
| Traffic growth | >50% WoW for 3 weeks | Consider ads |
| Conversion happening | >1% signup rate | Add newsletter capture |
| Users asking to share | Any | Add referral program |
| Organic social working | Engagement >5% | Automate posting |

## Anti-Patterns

**Don't:**
- Set up newsletter before you have traffic
- Run ads without knowing what converts
- Automate posting before establishing voice
- Add referral program without users

**Do:**
- Build on what's already working
- One channel at a time
- Measure everything
- Cut what doesn't work fast

## Related Skills

- `/dashboard` - See traction first
- `/announce` - Manual launch posts
- `/post` - Manual social posts
- `/brand-builder` - Establish voice before automating
