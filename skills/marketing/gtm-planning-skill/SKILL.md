---
document_name: "gtm-planning.skill.md"
location: ".claude/skills/gtm-planning.skill.md"
codebook_id: "CB-SKILL-GTM-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for go-to-market planning"
skill_metadata:
  category: "marketing"
  complexity: "advanced"
  estimated_time: "varies"
  prerequisites:
    - "Positioning complete"
    - "Messaging framework"
category: "skills"
status: "active"
tags:
  - "skill"
  - "marketing"
  - "gtm"
  - "launch"
ai_parser_instructions: |
  This skill defines procedures for GTM planning.
  Used by Product Marketing Manager agent.
---

# GTM Planning Skill

=== PURPOSE ===

Procedures for go-to-market strategy and launch planning.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(pmm) @ref(CB-AGENT-PMM-001) | Primary skill for GTM |

=== PROCEDURE: GTM Strategy ===

**Components:**
1. Target market definition
2. Value proposition
3. Pricing strategy
4. Distribution channels
5. Launch timeline
6. Success metrics

=== PROCEDURE: Launch Tiers ===

**Tier Definitions:**
| Tier | Scope | Activities |
|------|-------|------------|
| Tier 1 | Major release | Full campaign, PR, events |
| Tier 2 | Significant feature | Blog, email, social |
| Tier 3 | Minor feature | Changelog, documentation |
| Tier 4 | Bug fix/patch | Release notes only |

**Tier Selection Criteria:**
- Market impact
- Revenue potential
- Competitive response
- Customer demand
- Strategic importance

=== PROCEDURE: Launch Checklist ===

**Pre-Launch (T-30 days):**
- [ ] Positioning finalized
- [ ] Messaging approved
- [ ] Pricing confirmed
- [ ] Launch tier determined
- [ ] Assets list created

**Pre-Launch (T-14 days):**
- [ ] Landing page ready
- [ ] Documentation complete
- [ ] Demo/video ready
- [ ] Email templates drafted
- [ ] Social content planned

**Pre-Launch (T-7 days):**
- [ ] Sales enablement complete
- [ ] Support briefed
- [ ] Press release ready
- [ ] Blog post drafted
- [ ] Final QA of materials

**Launch Day:**
- [ ] Feature deployed
- [ ] Documentation live
- [ ] Landing page live
- [ ] Email sent
- [ ] Social posts published
- [ ] Monitoring in place

**Post-Launch (T+7 days):**
- [ ] Metrics reviewed
- [ ] Customer feedback gathered
- [ ] Issues addressed
- [ ] Retro completed

=== PROCEDURE: GTM Document ===

**Location:** `devdocs/marketing/gtm-plan.md`

**Structure:**
```markdown
# Go-to-Market Plan: [Feature/Product]

## Overview
- Feature: [name]
- Launch Date: [date]
- Launch Tier: [1-4]
- Owner: @pmm

## Target Audience
[Who this is for]

## Key Messages
[From messaging framework]

## Launch Activities

### Marketing
- [ ] Blog post
- [ ] Email campaign
- [ ] Social media
- [ ] Landing page

### Sales
- [ ] Sales deck updated
- [ ] Battlecard created
- [ ] Demo script ready

### Support
- [ ] Documentation
- [ ] FAQ
- [ ] Training

## Timeline
| Date | Activity | Owner | Status |
|------|----------|-------|--------|
| T-14 | Assets ready | PMM | Pending |
| T-7 | Final review | All | Pending |
| T-0 | Launch | DevOps | Pending |

## Success Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Signups | X | Analytics |
| Activation | Y% | Product |
| Revenue | $Z | Finance |

## Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [Impact] | [Plan] |
```

=== PROCEDURE: Channel Strategy ===

**Channel Mix:**
```markdown
## Distribution Channels

### Owned
- Website
- Blog
- Email list
- Documentation

### Earned
- PR/Press
- Reviews
- Word of mouth
- Community

### Paid (if applicable)
- Ads
- Sponsorships
- Events
```

**Channel Prioritization:**
| Channel | Reach | Cost | Effort | Priority |
|---------|-------|------|--------|----------|
| Blog | Medium | Low | Low | High |
| Email | High | Low | Medium | High |
| Social | Medium | Low | Medium | Medium |
| PR | High | Medium | High | For Tier 1 |

=== PROCEDURE: Metrics Framework ===

**Funnel Metrics:**
```
Awareness → Visits → Signups → Activation → Revenue
    |          |        |          |           |
  Impressions  Unique   Conv.     Active     MRR/ARR
              visitors  rate      users
```

**Launch KPIs:**
| Phase | Metric | Definition |
|-------|--------|------------|
| Awareness | Reach | Unique impressions |
| Interest | Traffic | Website visits |
| Consideration | Signups | New accounts |
| Decision | Activation | First value achieved |
| Advocacy | NPS | Net promoter score |

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(positioning) | Strategy foundation |
| @skill(messaging) | Content creation |
