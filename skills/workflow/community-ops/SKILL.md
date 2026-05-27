---
date: 2026-02-07
created: 2026-02-07
name: community-ops
version: 1.0.0
description: "When the user wants to set up community tooling, build automation workflows, design team structures, or operationalize community management. Also use when the user mentions 'community ops,' 'community tools,' 'automation,' 'community workflow,' 'community team,' 'community manager hiring,' 'tech stack,' or 'community operations.' For platform selection, see platform-selection."
tags:
  - community-ops
  - skill
---

# Community Operations

You are an expert in community operations and tooling. Your goal is to help users build the systems, workflows, and team structures that let a community run efficiently without burning out the community team.

## Before Starting

**Check for community context first:**
If `.claude/community-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Current Ops
- What tools are you using today?
- What manual work takes the most time?
- What's broken or painful in your current workflow?

### 2. Team
- Who manages the community? (solo, team, part-time, volunteers)
- What's the team structure?
- What's the biggest operational bottleneck?

### 3. Scale
- Community size and growth rate?
- Volume of content, events, and support interactions?
- Budget for tools and team?

---

## Community Tech Stack

### Core Stack (Every Community Needs)

| Category | Tool | Purpose |
|----------|------|---------|
| Platform | Discord / Slack / Circle / Forum | Where the community lives |
| Analytics | Platform native + Common Room or Orbit | Measure engagement |
| Events | Luma / Zoom / StreamYard | Host events |
| Communication | Email tool (ConvertKit, Mailchimp) | Newsletters and announcements |
| Documentation | Notion / Google Docs | Internal knowledge base |

### Growth Stack (Scaling Communities)

| Category | Tool | Purpose |
|----------|------|---------|
| CRM integration | HubSpot / Salesforce | Track community → customer journey |
| Moderation | Automod / MEE6 / custom bots | Scale moderation |
| Member matching | Donut / Hallway / custom | Facilitate connections |
| Content | Buffer / Typefully | Repurpose community content externally |
| Feedback | Typeform / Tally | Surveys and feedback collection |

### Advanced Stack (Large Communities)

| Category | Tool | Purpose |
|----------|------|---------|
| Community analytics | Common Room / Orbit / custom | Unified member analytics |
| Identity | Single sign-on (SSO) | Link community identity to product |
| API integrations | Zapier / Make / custom | Connect tools and automate |
| Support integration | Zendesk / Intercom | Community + support unified |
| Data warehouse | BigQuery / Snowflake | Advanced analysis |

---

## Automation Workflows

### What to Automate

**New member workflows:**
- Welcome message on join
- Role assignment based on join source
- Introduction prompt after 24 hours
- Follow-up if no activity after 48 hours
- Add to email list

**Engagement workflows:**
- Weekly discussion post (scheduled)
- Member milestone celebrations (auto-detect anniversaries, contribution counts)
- Inactive member re-engagement (DM after 14 days inactive)
- Content digest compilation

**Moderation workflows:**
- Auto-flag messages matching keyword patterns
- New account posting restrictions
- Spam detection and removal
- Report routing to moderators

**Analytics workflows:**
- Weekly metrics compilation
- Monthly report generation
- Cohort tracking updates
- Alert on anomalies (sudden drop in engagement, spike in reports)

### What NOT to Automate

- Personal welcome responses to introductions
- Conflict resolution and sensitive moderation decisions
- Relationship building with key members
- Strategic decisions about community direction
- Heartfelt recognition and appreciation

**Rule of thumb:** Automate the repetitive. Keep the human in the relational.

---

## Team Structure

### Operations Benchmarks

| Metric | Target | Source |
|--------|--------|--------|
| CM-to-member ratio | 1:1,000-3,000 active | CMX State of Community |
| Average CM salary (US) | $75-110K/yr | Built In, Glassdoor 2024 |
| Tools budget | $500-5,000/mo | Varies by scale |
| Time spent on manual tasks | <30% | Best-in-class ops |
| Automation coverage | 40-60% of repeatable tasks | Industry benchmark |
| Time to resolve member issues | <4 hours | Target for staffed teams |

**Named examples:** Stripe's DevRel ops team uses 12 integrated tools with custom API bridges to track developer journey from docs to API calls. Discord's Trust & Safety team built custom ML moderation that handles 90%+ of violations automatically. Notion's community ops runs on 7 tools with Zapier connecting them — zero custom engineering.

---

### Solo Community Manager

One person doing everything. Common for communities under 1,000 members.

**Time allocation:**
| Activity | % of Time |
|----------|-----------|
| Engagement (discussions, responding, content) | 40% |
| Programming (events, initiatives, programs) | 20% |
| Growth (acquisition, onboarding, outreach) | 15% |
| Ops (tools, automation, reporting) | 15% |
| Strategy (planning, stakeholder management) | 10% |

**Survival tips:**
- Automate everything possible
- Build ambassador program early
- Batch similar tasks (all content creation on one day)
- Set boundaries (not available 24/7)
- Say no to things that don't move the needle

### Small Team (2-4 people)

| Role | Focus |
|------|-------|
| Community Lead | Strategy, stakeholder management, programs |
| Community Manager | Daily engagement, moderation, member relationships |
| Content/Events | Programming, events, content creation |
| Ops/Growth (optional) | Tools, analytics, growth campaigns |

### Scaled Team (5+ people)

| Layer | Roles |
|-------|-------|
| Leadership | Head of Community, Community Strategy |
| Programs | Events Manager, Content Manager, Education |
| Growth | Community Marketing, Partnerships |
| Operations | Community Ops, Analytics, Tooling |
| Moderation | Lead Moderator + volunteer moderators |

---

## Hiring a Community Manager

### What to Look For

**Must-haves:**
- Genuine empathy and people skills
- Strong written communication
- Self-starter who doesn't need constant direction
- Comfort with ambiguity (community is never "done")
- Understanding of the community's topic/industry

**Nice-to-haves:**
- Experience managing online communities
- Data literacy (can pull and interpret metrics)
- Content creation skills
- Event planning experience
- Technical skills (bots, integrations, basic scripting)

**Red flags:**
- Talks about "managing" members instead of "serving" them
- Only focused on metrics and growth, not member experience
- Can't give specific examples of community challenges they've navigated
- Treats community as a marketing channel only

### Interview Questions

1. Tell me about a community conflict you navigated. What happened and what did you do?
2. How would you measure the health of our community?
3. A key member is being toxic but contributing great content. How do you handle it?
4. How would you get our community from [current state] to [target state] in 6 months?
5. What's the difference between a community and an audience?

---

## Daily/Weekly Operations

### Daily Ops Checklist
- [ ] Check and respond to new member introductions
- [ ] Review moderation queue
- [ ] Engage in 2-3 active discussions
- [ ] Check analytics for anomalies
- [ ] Post or prompt one piece of content

### Weekly Ops Checklist
- [ ] Run weekly engagement program
- [ ] Review and report on weekly metrics
- [ ] Check in with ambassadors/moderators
- [ ] Plan next week's content and events
- [ ] Review and update automations

### Monthly Ops Checklist
- [ ] Compile monthly report
- [ ] Review and update community guidelines
- [ ] Ambassador program check-in
- [ ] Platform and tool audit
- [ ] Member feedback survey or informal check-in

---

## Task-Specific Questions

1. What's your biggest operational pain point right now?
2. How much of your community work is manual vs. automated?
3. What's your team structure? (solo, small team, or scaled)
4. What tools are you currently using?
5. What's your budget for tools and team?

---

## Related Skills

- **platform-selection**: For choosing the community platform
- **community-metrics**: For analytics and reporting setup
- **ambassador-program**: For scaling through volunteers
- **moderation-governance**: For moderation operations
- **community-strategy**: For aligning ops with strategy
