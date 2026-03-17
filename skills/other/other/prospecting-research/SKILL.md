---
name: prospecting-research
description: Conduct deep account and contact research to personalize outreach and identify compelling angles for engagement
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Prospecting Research

> Systematically research target accounts and contacts to craft personalized, relevant outreach that cuts through the noise.

## When to Use This Skill

- Preparing for high-value outbound
- Personalizing enterprise outreach
- Building account intelligence
- Training SDRs on research
- Creating target account profiles

## Methodology Foundation

Based on **Jeb Blount's Fanatical Prospecting** and **TOPO Account-Based Research**, combining:
- Company intelligence gathering
- Contact profiling
- Trigger identification
- Angle development

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures research framework | Time per account |
| Identifies key data points | Outreach approach |
| Suggests personalization angles | Which angle to use |
| Creates research templates | Tool selection |
| Synthesizes findings | Message crafting |

## Instructions

### Step 1: Company Research

**Firmographic Data:**
| Data Point | Source | Why It Matters |
|------------|--------|----------------|
| Company size | LinkedIn, website | ICP fit |
| Revenue | ZoomInfo, news | Budget potential |
| Industry | LinkedIn | Relevance |
| Locations | Website | Territory |
| Tech stack | BuiltWith, job posts | Integration fit |

**Business Context:**
| Data Point | Source | Why It Matters |
|------------|--------|----------------|
| Recent funding | Crunchbase, news | Budget, growth mode |
| Executive changes | LinkedIn, news | New priorities |
| Product launches | Press releases | Initiatives |
| Earnings/reports | SEC, investor calls | Priorities, challenges |
| Partnerships | News | Ecosystem |

### Step 2: Contact Research

**Professional Profile:**
| Data Point | Source | Why It Matters |
|------------|--------|----------------|
| Current role | LinkedIn | Relevance |
| Tenure | LinkedIn | Influence level |
| Career path | LinkedIn | Context |
| Content shared | LinkedIn, Twitter | Interests |
| Mutual connections | LinkedIn | Warm intro |

**Personal Connection Points:**
- Shared alma mater
- Previous company overlap
- Mutual connections
- Content they've created
- Events they've attended

### Step 3: Identify Triggers

**Timing Triggers:**
| Trigger | Implication |
|---------|-------------|
| New in role | Building stack, making changes |
| New company | Bringing solutions from previous |
| Funding | Budget available |
| Hiring | Scaling, needs support |
| Bad earnings | Cost cutting or growth push |

### Step 4: Develop Angles

**Personalization Hierarchy:**
1. **Trigger-based** - Strongest (funding, hire, news)
2. **Content-based** - Strong (their posts, interviews)
3. **Company-based** - Good (industry, challenges)
4. **Mutual connection** - Good (warm intro potential)
5. **Generic** - Weak (avoid)

## Examples

### Example 1: Full Account Research

**Output:**
```
## Account Research: DataFlow Systems

### Company Snapshot

| Attribute | Value | Source |
|-----------|-------|--------|
| Company | DataFlow Systems | |
| Industry | B2B SaaS (Analytics) | LinkedIn |
| Size | 340 employees | LinkedIn |
| Revenue | ~$50M ARR (est.) | ZoomInfo |
| Founded | 2018 | Crunchbase |
| HQ | Austin, TX | Website |
| Funding | $45M Series B (Oct 2024) | Crunchbase |

---

### Technology Stack

| Category | Tool | Source |
|----------|------|--------|
| CRM | Salesforce | BuiltWith, Jobs |
| Marketing | HubSpot | BuiltWith |
| Analytics | Mixpanel | Careers page |
| Data | Snowflake | Job posting |
| [Your Category] | None detected | Research |

**Implication:** Salesforce user = good fit for integration. No tool in our category = greenfield opportunity.

---

### Recent Triggers

| Date | Trigger | Relevance |
|------|---------|-----------|
| Oct 2024 | Series B ($45M) | Budget for tools |
| Nov 2024 | VP Sales hired | New leader = new tools |
| Dec 2024 | 12 SDR positions posted | Scaling outbound |
| Jan 2025 | G2 reviews mention "[pain]" | Known problem |

---

### Business Context

**From LinkedIn:**
- Growing 60% YoY (CEO post)
- Expanding to enterprise segment (VP Sales announcement)
- Recent product launch: AI analytics features

**From News:**
- Named to "Top 50 Startups" list
- Partnership with [Complementary Company]
- CEO spoke at [Industry Conference]

**From Job Posts:**
- Hiring: SDRs (12), AEs (5), RevOps (1)
- Reveals: Scaling sales org significantly
- Tech stack mentioned: Salesforce, Gong, Outreach (competitor!)

---

### Challenges (Inferred)

Based on triggers and context:
1. **Scaling sales team** - Need tools to support
2. **Moving upmarket** - Enterprise processes needed
3. **Rev Ops hire** - Building infrastructure
4. **Competitor in stack** - May be open to alternatives

---

### Target Contacts

| Name | Title | Priority | Angle |
|------|-------|----------|-------|
| Sarah Kim | VP Sales | Primary | New to role (90 days) |
| Mike Chen | RevOps Manager | Secondary | Posted RevOps opening |
| David Park | CEO | Executive | Series B scaling |

---

### Recommended Approach

**Primary Target: Sarah Kim, VP Sales**
- New to role = making changes
- Scaling team = needs tools
- Moving upmarket = needs process

**Angle:** "Congrats on the VP role and Series B! I noticed you're hiring 12 SDRs. Most VP Sales at your stage tell me [challenge] is their biggest issue. Curious if that's true for you?"

**Secondary Path:**
- RevOps Manager Mike Chen (operational angle)
- Mutual connection: [Name] (former colleague)
```

### Example 2: Contact Deep Dive

**Output:**
```
## Contact Research: Sarah Kim, VP Sales

### Profile Summary

| Attribute | Value |
|-----------|-------|
| Name | Sarah Kim |
| Title | VP of Sales |
| Company | DataFlow Systems |
| Location | Austin, TX |
| Tenure | 3 months (started Oct 2024) |
| LinkedIn | linkedin.com/in/sarahkim |

---

### Career Path

| Period | Company | Role | Relevance |
|--------|---------|------|-----------|
| 2024-Present | DataFlow | VP Sales | Target |
| 2021-2024 | ScaleUp Inc | Director Sales | Previous tools? |
| 2018-2021 | BigCorp | Sales Manager | Enterprise exp |
| 2015-2018 | StartupXYZ | AE | SMB background |

**Insight:** Rose through ranks. Enterprise + SMB experience. First VP role = motivated to succeed.

---

### Content Activity

**LinkedIn Posts (Last 90 days):**
- "Excited to join DataFlow!" (Oct)
- Shared article on "Scaling SDR teams"
- Commented on post about sales forecasting
- Posted about team offsite (Dec)

**Themes:** Sales leadership, team building, scaling

**Quote-worthy:** "The hardest part of scaling isn't hiring—it's making sure every rep can sell like your best rep."

---

### Connection Points

| Type | Detail | Approach |
|------|--------|----------|
| Mutual Connection | John Smith (2nd degree) | Ask for intro |
| Content | Scaling article | Reference in outreach |
| Alma Mater | Stanford MBA | Mention if relevant |
| Previous Company | ScaleUp used our competitor | Migration angle |

---

### Professional Interests

Based on activity:
- Sales enablement
- Team scaling
- Forecasting accuracy
- Rep productivity

---

### Personalization Angles

**Angle 1: New VP + Scaling** (Strongest)
```
Hi Sarah,

Congrats on the VP role at DataFlow—and jumping into a Series B scaling mode!

I noticed you shared that article on scaling SDR teams. The quote "making every rep sell like your best rep" really resonated.

That's exactly what [Similar Customer] focused on when they went from 5 to 50 reps.

Curious: what's your #1 challenge as you build out the team?
```

**Angle 2: Content-Based**
```
Hi Sarah,

Loved your take on the hardest part of scaling: "making every rep sell like your best rep."

I work with a lot of VP Sales going through exactly that transition. The common thread? [Insight from our customers].

Worth comparing notes?
```

**Angle 3: Mutual Connection**
```
Hi Sarah,

John Smith mentioned you just took over sales at DataFlow—congrats!

He thought we should connect given your focus on [area].

Would love to hear what's top of mind as you build out the team.
```

---

### Red Flags / Cautions

- Just started (Oct) - may not have full authority yet
- Previous company used competitor - could be loyal
- No public content about specific pain points

---

### Recommended Sequence

**Day 1:** Email (Angle 1 - New VP + Scaling)
**Day 1:** LinkedIn connection (mention scaling article)
**Day 3:** Follow-up email with customer story
**Day 5:** LinkedIn voice note
**Day 7:** Final email with value offer

**Expectation:** 20-30% response rate with this level of personalization
```

## Skill Boundaries

### What This Skill Does Well
- Structuring research process
- Identifying personalization angles
- Finding trigger events
- Synthesizing intelligence

### What This Skill Cannot Do
- Access paid databases
- Verify data accuracy
- Replace genuine relationship building
- Write final message copy

## References

- Jeb Blount's Fanatical Prospecting
- TOPO Account-Based Research
- SalesLoft Personalization Guide
- Outreach.io Research Best Practices

## Related Skills

- `icp-matching` - Qualify before research
- `signal-monitoring` - Trigger identification
- `outbound-sequencer` - Use research in sequences

## Skill Metadata

- **Domain**: SDR Automation
- **Complexity**: Intermediate
- **Mode**: cyborg
- **Time to Value**: 15-30 min per account
- **Prerequisites**: Research tool access
