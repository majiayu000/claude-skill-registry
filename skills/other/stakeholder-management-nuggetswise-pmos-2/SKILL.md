---
name: stakeholder-management
description: Use when planning an initiative - maps stakeholders, tracks alignment, and plans communication strategy.
---

# Stakeholder Management

## Overview

Maps stakeholders using power/interest grid, tracks their alignment and concerns, and creates a communication plan. Prevents initiatives from failing due to stakeholder misalignment.

## When to Use

- Starting a new initiative or major feature
- Charter approved, need to build support
- Sensing resistance to a proposal
- Before major product decisions
- Quarterly stakeholder review

## Core Pattern

**Step 1: Identify Stakeholders**

For the initiative in question, list all stakeholders who:
- Have decision authority (can approve/block)
- Control resources (budget, engineering, design)
- Are impacted (their team's work changes)
- Have expertise needed (domain knowledge, technical input)
- Represent customers/users

Ask user: "Which initiative is this for?" and "Who are the key stakeholders?"

If user unsure, suggest checking:
- Charter owners and approvers
- Engineering/design leads
- Product leadership
- Customer-facing teams (sales, CS, support)
- Cross-functional partners (legal, compliance, ops)

**Step 2: Power/Interest Grid Analysis**

For each stakeholder, assess:
- **Power:** High (can approve/block) or Low (influence only)
- **Interest:** High (cares deeply) or Low (peripheral concern)
- **Current Stance:** Support / Neutral / Oppose / Unknown
- **Why they care:** What's their stake in this?

Place in grid:
- **High Power, High Interest:** Manage closely (key players)
- **High Power, Low Interest:** Keep satisfied (need approval but not engaged)
- **Low Power, High Interest:** Keep informed (champions, advocates)
- **Low Power, Low Interest:** Monitor (minimal effort)

**Step 3: Alignment Tracking**

For each stakeholder, document:
- **Concerns:** What worries them about this initiative?
- **What they need:** Info, decision, resources, reassurance?
- **Last contact:** When did we last engage?
- **Next action:** Specific next step to move them toward support

**Step 4: Communication Plan**

For each stakeholder, define:
- **Cadence:** Weekly, biweekly, monthly, or ad-hoc?
- **Format:** 1:1 meeting, email update, dashboard, demo?
- **Key messages:** Top 3 things they need to hear

**Step 5: Generate Output**

Write to `outputs/stakeholders/stakeholder-map-[initiative]-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: stakeholder-management
initiative: [Initiative name]
sources:
  - outputs/roadmap/Q1-2026-charters.md (modified: YYYY-MM-DD)
  - (stakeholder list provided by user)
downstream:
  - outputs/delivery/prds/[initiative].md
---

# Stakeholder Map: [Initiative]

## Initiative Context
**What:** [1-sentence description of initiative]
**Why:** [Why this matters to the business]
**Timeline:** [Expected completion]

## Power/Interest Grid

### Manage Closely (High Power, High Interest)
| Stakeholder | Role | Current Stance | Why They Care | Strategy |
|-------------|------|----------------|---------------|----------|
| [Name] | [Title] | Support/Neutral/Oppose | [Their stake] | [Engagement approach] |

### Keep Satisfied (High Power, Low Interest)
| Stakeholder | Role | Current Stance | Why They Care | Strategy |
|-------------|------|----------------|---------------|----------|
| [Name] | [Title] | Support/Neutral/Oppose | [Their stake] | [Engagement approach] |

### Keep Informed (Low Power, High Interest)
| Stakeholder | Role | Current Stance | Why They Care | Strategy |
|-------------|------|----------------|---------------|----------|
| [Name] | [Title] | Support/Neutral/Oppose | [Their stake] | [Engagement approach] |

### Monitor (Low Power, Low Interest)
| Stakeholder | Role | Current Stance | Why They Care | Strategy |
|-------------|------|----------------|---------------|----------|
| [Name] | [Title] | Support/Neutral/Oppose | [Their stake] | [Engagement approach] |

## Alignment Tracking

| Stakeholder | Concerns | What They Need | Last Contact | Next Action | Owner |
|-------------|----------|----------------|--------------|-------------|-------|
| [Name] | [Key concerns] | [Info/decision/support] | YYYY-MM-DD or "Not yet" | [Specific next step] | [PM/other] |

## Relationship Management

| Stakeholder | Cadence | Channel | Relationship | Last Contact | Next Action |
|-------------|---------|---------|--------------|--------------|-------------|
| [Name] | Weekly/Biweekly/Monthly | 1:1/Slack/Staff meeting | Good/Neutral/Strained | YYYY-MM-DD | [Action] |

## Blockers Analysis

| Stakeholder | What They're Blocking | Root Cause | Unblock Strategy | Owner | Target Date |
|-------------|----------------------|------------|------------------|-------|-------------|
| [Name] | [Issue] | [Why] | [Action] | [PM] | [Date] |

## How to Win Each Stakeholder

| Stakeholder | Their Win Condition | What They Fear | Winning Message | Proof They Need |
|-------------|--------------------|--------------------|-----------------|-----------------|
| [Name] | [What success looks like to them] | [Their worry] | [Key message] | [Evidence that moves them] |

## Communication Plan

| Stakeholder | Cadence | Format | Key Messages | Next Touchpoint |
|-------------|---------|--------|--------------|-----------------|
| [Name] | Weekly/Biweekly/Monthly/Ad-hoc | 1:1/Email/Dashboard/Demo | [Top 3 messages] | YYYY-MM-DD |

## Risks & Mitigation

| Stakeholder | Risk | Impact if Opposed | Mitigation Plan |
|-------------|------|-------------------|-----------------|
| [Name] | [What could go wrong] | High/Med/Low | [How to prevent/address] |

## Approval Chain

**Required approvals:**
1. [Stakeholder] - [What they approve] - Status: Pending/Approved/Blocked
2. [Stakeholder] - [What they approve] - Status: Pending/Approved/Blocked

**Timeline:**
- [Milestone] by [Date]
- [Milestone] by [Date]

## Unknowns / Open Questions

- [What stakeholder info is missing?]
- [Whose support level is unclear?]
- [What concerns need investigation?]

## Sources Used
- [file paths or "Stakeholder list provided by user"]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [Stakeholder has high power] | Evidence/Assumption | [org chart or "Assumed from role"] |
| [Stakeholder opposes] | Evidence/Assumption | [meeting notes or "Assumed from past feedback"] |
| [Approval needed by X date] | Evidence | [charter:line or project timeline] |
```

**Step 6: Copy to History & Update Tracker**

- Copy to `history/stakeholder-management/stakeholder-map-[initiative]-YYYY-MM-DD.md`
- Update `nexa/state.json` and append to `outputs/audit/auto-run-log.md`

## Quick Reference

### Engagement Strategies by Quadrant

| Quadrant | Strategy | Tactics |
|----------|----------|---------|
| **High Power, High Interest** | Manage closely | Weekly 1:1s, early involvement in decisions, solicit input |
| **High Power, Low Interest** | Keep satisfied | Monthly updates, ensure no surprises, make their job easy |
| **Low Power, High Interest** | Keep informed | Regular comms, leverage as champions, gather feedback |
| **Low Power, Low Interest** | Monitor | Occasional updates, minimal effort unless they escalate |

### Common Concerns by Role

| Role | Typical Concerns | How to Address |
|------|------------------|----------------|
| **Engineering Lead** | Scope creep, tech debt, timeline | Clear requirements, technical trade-off discussions |
| **Design Lead** | User research, design debt, quality | User evidence, design review cadence |
| **Product Leadership** | Business impact, resource allocation | Metrics, ROI, strategic alignment |
| **Sales/CS** | Customer impact, training, positioning | Customer evidence, enablement plan |
| **Legal/Compliance** | Risk, liability, regulatory | Early involvement, clear documentation |

## Common Mistakes

- **Missing stakeholders:** Only mapping leadership → Include IC influencers, cross-functional partners
- **Assuming support:** "They'll be fine" → Explicitly confirm stance
- **No follow-up:** Just mapping once → Track alignment changes over time
- **Vague next actions:** "Talk to them" → Specific action with deadline
- **Ignoring opposition:** Hoping it goes away → Address concerns proactively

## Verification Checklist

- [ ] All key stakeholders identified
- [ ] Power/interest assessed for each
- [ ] Current stance documented (not assumed)
- [ ] Concerns captured for each stakeholder
- [ ] Next actions specific and dated
- [ ] Communication plan defined
- [ ] Approval chain mapped
- [ ] Risks identified
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Stakeholder is key decision maker] | Evidence/Assumption | [org chart or "Role-based assessment"] |
| [Stakeholder has X concern] | Evidence | [meeting notes, email, or "Stated in conversation"] |
| [Need approval by X] | Evidence | [charter timeline or project plan] |
