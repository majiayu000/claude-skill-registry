---
name: distribution-engine
description: "Construisez un système de distribution complet (posting, DM delivery, retargeting, tracking) qui transforme vos hooks en pipeline prévisible, basé sur la méthodologie A4 du Marketing Swarm de Lasse Flagstad. Use when: **Lancer une machine de contenu LinkedIn/X** - Cadence, review flow, posting engine; **Automatiser les DMs après engagement** - Trigger → message → tag → booking; **Installer le retargeting** - Email + Meta/IG pour ne jamais perdre un lead; **Créer un dashboard simple** - Les 6 ..."
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Distribution Engine

> Construisez un système de distribution complet (posting, DM delivery, retargeting, tracking) qui transforme vos hooks en pipeline prévisible, basé sur la méthodologie A4 du Marketing Swarm de Lasse Flagstad.

## When to Use This Skill

- **Lancer une machine de contenu LinkedIn/X** - Cadence, review flow, posting engine
- **Automatiser les DMs après engagement** - Trigger → message → tag → booking
- **Installer le retargeting** - Email + Meta/IG pour ne jamais perdre un lead
- **Créer un dashboard simple** - Les 6 métriques qui comptent vraiment
- **Connecter hooks → pipeline** - Du commentaire au call booké

## Methodology Foundation

**Source**: Lasse Flagstad - A4 Distribution Engineer (Marketing Swarm, 2025)

**Core Principle**: "La distribution n'est pas un add-on. C'est le système nerveux de votre marketing. Sans wiring propre, même les meilleurs hooks meurent dans le vide."

**Why This Matters**: La plupart des créateurs produisent du contenu sans système de capture. Le Distribution Engine connecte chaque point de contact (post, comment, DM, email, ad) en un flux mesurable et optimisable.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Structure le posting engine** - Qui poste, où, à quelle cadence, avec quel review flow
2. **Configure le DM delivery** - Triggers automatiques, messages, tags, routing
3. **Installe le retargeting** - Email 3-touch + Meta pixel pour les non-convertis
4. **Crée l'Event Map + UTMs** - Tracking créatif qui raconte une histoire
5. **Définit le Mini Dashboard** - Les 6 métriques quotidiennes essentielles

## How to Use

### Créer un système de distribution from scratch
```
Je lance du contenu sur LinkedIn mais je n'ai aucun système de capture. Aide-moi à construire mon distribution engine.
```

### Optimiser un système existant qui fuit
```
J'ai des posts qui performent mais je perds les leads entre le comment et le booking. Audite mon flow avec le skill distribution-engine.
```

### Installer le tracking et le dashboard
```
Je veux savoir exactement combien de leads passent de post → DM → call → close. Configure mon tracking.
```

## Instructions

### Step 1: Audit des outils existants

```
## Inventory Check

**Email/CRM:**
[ ] ESP: _____________ (ConvertKit, Mailchimp, Brevo, etc.)
[ ] CRM: _____________ (HubSpot, Pipedrive, Notion, etc.)

**Automation:**
[ ] DM Tool: _____________ (Phantombuster, Dripify, manuel)
[ ] Calendar: _____________ (Calendly, Cal.com, HubSpot)

**Tracking:**
[ ] Analytics: _____________ (GA4, Plausible, Fathom)
[ ] Meta Pixel: [ ] Installé [ ] Non
[ ] LinkedIn Insight Tag: [ ] Installé [ ] Non

**Content:**
[ ] Posting queue: _____________ (Buffer, Hypefury, manuel)
[ ] Link shortener: _____________ (Short.io, Bitly, none)

**Access this week:**
[ ] ESP [ ] Calendar [ ] DM tool [ ] Analytics [ ] Ad Manager
```

**Why each matters:**
- ESP → Nurture automation + deliverability
- CRM → Lead tracking + handoff to sales
- DM Tool → Speed of response après engagement
- Pixels → Retargeting des visiteurs non-convertis
- Calendar → Friction-free booking

---

### Step 2: Posting Engine Design

```
## Posting Engine v1

**Who posts:**
[ ] Founder only (personal brand)
[ ] Founder + team member (amplification)
[ ] Team via queue (scaled content)

**Platform priority:**
1. _____________ (primary - usually LinkedIn)
2. _____________ (secondary - X, newsletter, etc.)

**Cadence:**
- Primary: ___ posts/week
- Secondary: ___ posts/week
- Stories/ephemeral: ___ /week

**Review flow:**
[ ] Draft → Self-review → Post
[ ] Draft → Peer review → Schedule
[ ] AI draft → Human edit → Schedule

**Best slots (test these):**
- LinkedIn: Tue-Thu 7-9am, 12pm, 5-6pm local ICP time
- X: Varies by audience, test 4 slots

**Content mix (per 4 posts):**
- 1 Comment-magnet (engagement driver)
- 1 Proof/case study (credibility)
- 1 POV/insight (thought leadership)
- 1 Soft CTA (booking/lead magnet)
```

---

### Step 3: DM Delivery System

```
## DM Delivery Map

**Trigger → Message → Action**

1. **Comment with keyword** (e.g., "MAP", "GUIDE", "YES")
   → Auto-DM: "[Asset] + starter question"
   → Tag: lead_commented
   → Action: Add to nurture sequence

2. **Profile visit** (if tool allows)
   → Manual or auto DM: "Saw you checked us out..."
   → Tag: profile_visitor

3. **Post engagement** (like/repost without comment)
   → Soft DM after 24h: "Thanks for engaging..."
   → Tag: warm_lead

**DM Templates (3 tones):**

**Friendly:**
"Hey [name]! Saw your comment — here's the [asset] as promised.
Quick Q: What's your biggest challenge with [topic] right now?"

**Direct:**
"[Asset] link: [URL]
One question: Are you actively trying to fix [problem] or just researching?"

**Curious:**
"Sent! Curious — what made you comment on that post specifically?"

**Rules:**
- Respond within 2h during business hours
- Max 2 follow-ups if no reply
- Always end with a question (keeps thread alive)
- Tag everything for segmentation
```

---

### Step 4: Retargeting Setup

```
## Retargeting v1 (Never Lose a Lead)

**Layer 1: Email (3-touch minimum)**
- Touch 1: Value delivery (lead magnet, insight)
- Touch 2: Proof/case (social proof, numbers)
- Touch 3: Soft invite (booking, VSL)

**Layer 2: Meta/IG Retargeting**
- Audience: Website visitors 7-30 days
- Exclude: Already booked / customers
- Creative: 3 variants (proof, POV, invite)
- Budget: $5-20/day to start

**Layer 3: LinkedIn (optional)**
- Insight Tag on key pages (VSL, booking)
- Matched audience from email list
- Thought leader ads (boost organic posts)

**Pixel placement:**
- Homepage: awareness
- VSL/Sales page: intent
- Booking page: high intent
- Thank you page: conversion (exclude from retargeting)
```

---

### Step 5: Event Map + UTMs

```
## Event Naming (Creative, Not Generic)

**Standard events → Story-driven names:**
- page_view → entered_universe
- scroll_50 → reading_deep
- video_play → watching_proof
- cta_click → raised_hand
- form_start → committing
- form_complete → opted_in
- book_click → booking_intent
- booked_call → pipeline_added
- showed_up → serious_buyer
- closed_won → customer_born

**UTM Structure:**
```
?utm_source=[platform]
&utm_medium=[content_type]
&utm_campaign=[campaign_name]
&utm_content=[specific_post_id]
```

**Examples:**
- LinkedIn comment-magnet post:
  `?utm_source=linkedin&utm_medium=post&utm_campaign=lead_magnet_jan&utm_content=hook_v1`

- Email nurture touch 2:
  `?utm_source=email&utm_medium=nurture&utm_campaign=evergreen&utm_content=proof_email`

- Meta retargeting ad:
  `?utm_source=meta&utm_medium=retargeting&utm_campaign=vsl_push&utm_content=testimonial_ad`
```

---

### Step 6: Mini Dashboard (6 Metrics)

```
## Daily Dashboard

| Metric | Source | Target | Red Flag |
|--------|--------|--------|----------|
| **Impressions** | LinkedIn/X analytics | Trending up | -30% WoW |
| **Engagement Rate** | (likes+comments)/impressions | >3% | <1.5% |
| **DMs Sent** | DM tool or manual count | X/day | 0 for 2+ days |
| **Leads Captured** | CRM/ESP | X/week | <50% of target |
| **Calls Booked** | Calendar | X/week | <30% of leads |
| **Show Rate** | Calendar + CRM | >75% | <60% |

**Weekly Review Questions:**
1. Which post drove most DMs this week?
2. What's the comment → DM → book conversion?
3. Which retargeting creative is winning?
4. Where's the biggest drop-off in the funnel?

**Monthly Actions:**
- Prune dead automations
- Refresh retargeting audiences
- Test 1 unconventional distribution play
```

## Examples

### Example 1: Solopreneur LinkedIn → Coaching Calls

**Setup:**
- Posting: 4x/week (Tue, Wed, Thu, Sat)
- DM: Manual with templates, keyword "GUIDE"
- Retargeting: Email only (no ad budget)
- Tracking: UTMs + Calendly analytics

**Flow:**
```
Post with hook + "Comment GUIDE"
    ↓
DM with lead magnet + question
    ↓
Reply qualifies → Send booking link
    ↓
Email reminder (T-24h, T-2h)
    ↓
Call → Close or nurture
```

**Results tracked:**
- Comments/post: 15-30
- DM response rate: 60%
- DM → Book: 20%
- Show rate: 80%

---

### Example 2: Agency Multi-Channel

**Setup:**
- Posting: Founder (LinkedIn) + Team (X, newsletter)
- DM: Phantombuster auto-DM on keyword
- Retargeting: Meta pixel + email sequence
- Tracking: GA4 + HubSpot CRM

**Flow:**
```
LinkedIn post (founder) + X thread (team)
    ↓
Auto-DM on comment keyword
    ↓
Lead magnet delivery + CRM tag
    ↓
Email nurture (5-touch evergreen)
    ↓
Meta retargeting (VSL viewers)
    ↓
Booking page → Call → Close
```

**Dashboard:**
- Weekly impressions: 50k+
- Leads/week: 20-40
- Calls booked: 8-12
- Close rate: 25%

## Checklists

### Pre-Launch Checklist

```
## Before First Post

**Tracking:**
[ ] UTM structure defined
[ ] Analytics installed (GA4 or alternative)
[ ] Key events configured
[ ] Pixels placed (Meta, LinkedIn if using)

**Capture:**
[ ] DM templates written (3 tones)
[ ] Keyword chosen for comment-magnet
[ ] Lead magnet ready to send
[ ] CRM/ESP tags created

**Flow:**
[ ] Posting schedule set
[ ] Review process defined
[ ] First week of content drafted
[ ] Retargeting audiences created (even if not running yet)

**Dashboard:**
[ ] 6 metrics identified
[ ] Tracking source for each
[ ] Weekly review time blocked
```

### Weekly Health Check

```
## Distribution Health (5 min)

[ ] All links working?
[ ] DM tool connected?
[ ] New leads tagged correctly?
[ ] Retargeting audiences updating?
[ ] Any automation errors?

## Performance (10 min)

[ ] Best post this week?
[ ] Worst post this week?
[ ] DM → Book conversion?
[ ] Show rate?
[ ] One thing to test next week?
```

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| Posts get views, no comments | Hook not comment-worthy | Add explicit CTA ("Comment X if...") |
| Comments but no DMs sent | Automation broken or too slow | Check tool, reduce delay |
| DMs sent, no replies | Message too salesy | Lead with value, end with question |
| Leads but no bookings | Friction in booking flow | Simplify, add calendar link in DM |
| Bookings but no-shows | Weak reminders | Add SMS, value reminder in email |
| Retargeting not working | Pixel not firing | Use Meta Pixel Helper to debug |

## Creative Distribution Plays

**Beyond standard posting:**

1. **Comment-first strategy** - Comment on ICP posts before posting yourself
2. **Partner post swaps** - Cross-promote with complementary creators
3. **Dark posts in communities** - Share in private groups, not just feed
4. **Podcast guesting → content** - Repurpose appearances as posts
5. **Event-triggered outreach** - DM people who engage with competitors
6. **Newsletter sponsorships** - Reach audiences without building them

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

### Source
- Lasse Flagstad - A4 Distribution Engineer (Marketing Swarm)
- `sources/swarms/lasse-marketing-swarm.md` (if saved)

### Tools
- [Phantombuster](https://phantombuster.com) - LinkedIn automation
- [Hypefury](https://hypefury.com) - X/LinkedIn scheduling
- [Cal.com](https://cal.com) - Open source Calendly alternative
- [Plausible](https://plausible.io) - Privacy-friendly analytics

## Related Skills

- `headline-formulas/` - Craft the hooks that feed this engine
- `nurture-sequences/` - What happens after lead capture
- `email-writing/` - Craft the emails in your sequences
- `landing-page-copy/` - Optimize the pages leads land on

---

*Skill version: 1.0*
*Last updated: 2026-01-28*
*Source: Lasse Flagstad Marketing Swarm*
