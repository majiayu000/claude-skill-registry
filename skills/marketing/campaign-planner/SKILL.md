---
name: campaign-planner
description: 'Use when the user asks to "plan an influencer campaign", "build a campaign blueprint", or "launch a product with creators"; produces campaign objectives, platform and influencer-tier strategy, content requirements, a phased timeline, budget allocation, and KPI targets. Not for writing individual creator briefs — use brief-generator.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use when planning a new influencer campaign, launching a product with influencer support, building seasonal or tentpole activations, designing always-on creator programs, restructuring an underperforming campaign, or preparing a campaign plan to present to stakeholders. Activate when the user gives a brand, budget, audience, or timeframe and wants the full strategy-to-execution blueprint before briefs or outreach begin."
argument-hint: "<brand or product> [budget] [platform] [timeframe]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Plan
---

# Campaign Planner

This skill helps you design comprehensive influencer marketing campaigns from strategy to execution plan. It creates actionable blueprints that align business objectives with creative execution.

## Quick Start

Shortest invocation:

```
Create an influencer campaign plan for [product launch]
```

Common scenario:

```
Plan an influencer campaign for [brand] with [budget] targeting [audience] during [timeframe]
```

## Skill Contract

- **Reads**: brand and product details, target audience, campaign type, budget, timeline, and any constraints supplied by the user. If `memory-management` is active, prior audience profiles and past-campaign benchmarks load from the hot cache.
- **Writes**: a campaign plan document saved to `memory/influencer/campaign-planner/YYYY-MM-DD-<topic>.md`.
- **Promotes**: durable facts (campaign name, primary objective, total budget, go-live date, KPI targets) to `memory/hot-cache.md`.
- **Done when**:
  - Objectives are SMART and have explicit success and failure definitions.
  - Influencer mix, content deliverables, timeline, budget, and KPIs are each specified with numbers, not placeholders.
  - The plan names the next step (brief generation) and any open approvals.
- **Primary next skill**: [brief-generator](../../plan/brief-generator/SKILL.md)

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family is Tier 1: every skill works with no live integrations. Provide the brand, audience, budget, and timeline directly and the plan builds from your inputs.

Optional connectors that strengthen the plan when available:

- `~~influencer database` — size the influencer mix and validate tier follower ranges.
- `~~social platform analytics` — set platform-specific reach and engagement benchmarks.
- `~~CRM` — align conversion targets and attribution with existing pipeline data.
- `~~analytics` — pull past-campaign actuals for realistic KPI and budget-efficiency targets.

See [CONNECTORS.md](../../CONNECTORS.md) for the free/keyless data recipe per category. Without any connector, ask the user for the missing inputs and proceed.

## Instructions

When a user requests campaign planning:

1. **Gather Campaign Requirements**

   ```markdown
   ### Campaign Brief Input
   
   **Brand Information**:
   - Brand: [name]
   - Product/Service: [description]
   - Value Proposition: [key benefits]
   - Target Audience: [demographics, psychographics]
   
   **Campaign Context**:
   - Campaign Type: [launch/awareness/seasonal/always-on]
   - Reason for Campaign: [why now]
   - Timeline: [start-end dates]
   - Budget: [total budget or range]
   
   **Constraints**:
   - Must include: [requirements]
   - Must avoid: [restrictions]
   - Approvals needed: [stakeholders]
   ```

2. **Define Campaign Objectives**

   ```markdown
   ## Campaign Objectives
   
   ### Campaign Name: [Name]
   
   ### Primary Objective
   
   **Goal**: [Specific objective]
   **Metric**: [How it will be measured]
   **Target**: [Specific number/percentage]
   
   ### Secondary Objectives
   
   | Objective | Metric | Target |
   |-----------|--------|--------|
   | [Objective 1] | [metric] | [target] |
   | [Objective 2] | [metric] | [target] |
   | [Objective 3] | [metric] | [target] |
   
   ### SMART Goal Check
   
   - ✅ **S**pecific: [how it's specific]
   - ✅ **M**easurable: [how it's measured]
   - ✅ **A**chievable: [why it's realistic]
   - ✅ **R**elevant: [business alignment]
   - ✅ **T**ime-bound: [timeline]
   
   ### Success Definition
   
   **This campaign is successful if**:
   - [Success criteria 1]
   - [Success criteria 2]
   - [Success criteria 3]
   
   **This campaign fails if**:
   - [Failure indicator 1]
   - [Failure indicator 2]
   ```

3. **Develop Campaign Strategy**

   ```markdown
   ## Campaign Strategy
   
   ### Strategic Approach
   
   **Big Idea**: [One-line campaign concept]
   
   **Strategy Statement**:
   We will [action] to [audience] by [method] resulting in [outcome].
   
   ### Target Audience
   
   **Primary Audience**:
   - Demographics: [details]
   - Psychographics: [values, interests, lifestyle]
   - Pain points: [challenges we address]
   - Media behavior: [where they consume content]
   
   **Secondary Audience** (if applicable):
   - [Description]
   
   ### Key Messages
   
   **Primary Message**:
   > "[Core message]"
   
   **Supporting Messages**:
   1. [Message 1]
   2. [Message 2]
   3. [Message 3]
   
   **Proof Points**:
   - [Evidence/claim 1]
   - [Evidence/claim 2]
   
   ### Campaign Pillars
   
   | Pillar | Focus | Content Angle |
   |--------|-------|---------------|
   | [Pillar 1] | [focus area] | [content approach] |
   | [Pillar 2] | [focus area] | [content approach] |
   | [Pillar 3] | [focus area] | [content approach] |
   
   ### Platform Strategy
   
   | Platform | Role | Content Focus | % Budget |
   |----------|------|---------------|----------|
   | [Platform 1] | Primary | [focus] | [%] |
   | [Platform 2] | Secondary | [focus] | [%] |
   | [Platform 3] | Supporting | [focus] | [%] |
   
   ### Competitive Differentiation
   
   **What makes this campaign different**:
   - [Differentiator 1]
   - [Differentiator 2]
   ```

4. **Define Influencer Criteria**

   ```markdown
   ## Influencer Strategy
   
   ### Influencer Mix
   
   | Tier | Follower Range | Quantity | Role | Budget % |
   |------|----------------|----------|------|----------|
   | Macro | 100K-1M | [#] | [role] | [%] |
   | Micro | 10K-100K | [#] | [role] | [%] |
   | Nano | <10K | [#] | [role] | [%] |
   
   ### Selection Criteria
   
   **Must-Have Requirements**:
   
   | Criterion | Requirement | Priority |
   |-----------|-------------|----------|
   | Niche | [category] | Required |
   | Platform | [platforms] | Required |
   | Engagement Rate | >[%] | Required |
   | Audience Demographics | [specs] | Required |
   | Brand Safety | [criteria] | Required |
   | Content Quality | [standard] | Required |
   
   **Preferred Criteria**:
   
   | Criterion | Preference | Weight |
   |-----------|------------|--------|
   | [Criterion 1] | [preference] | [weight] |
   | [Criterion 2] | [preference] | [weight] |
   
   **Exclusions**:
   - No current competitor partnerships
   - No controversial content history
   - [Other exclusions]
   
   ### Ideal Influencer Profile
   
   **Profile: "[Persona Name]"**
   
   - Age: [range]
   - Platform focus: [primary platform]
   - Content style: [description]
   - Audience: [description]
   - Posting frequency: [frequency]
   - Brand partnership style: [authentic/polished/etc.]
   - Example influencers: @[handle1], @[handle2]
   
   ### Relationship Type
   
   | Type | Description | Quantity | Terms |
   |------|-------------|----------|-------|
   | [Type 1] | [description] | [#] | [terms] |
   | [Type 2] | [description] | [#] | [terms] |
   ```

5. **Plan Content Requirements**

   ```markdown
   ## Content Plan
   
   ### Content Deliverables
   
   | Deliverable | Platform | Format | Quantity/Influencer | Total |
   |-------------|----------|--------|---------------------|-------|
   | [Type 1] | [platform] | [format] | [#] | [#] |
   | [Type 2] | [platform] | [format] | [#] | [#] |
   | [Type 3] | [platform] | [format] | [#] | [#] |
   
   **Total Content Pieces**: [#]
   
   ### Content Guidelines
   
   **Required Elements**:
   - [ ] Brand mention
   - [ ] Product feature/demo
   - [ ] Call-to-action: [specific CTA]
   - [ ] Disclosure (#ad, #sponsored, etc.)
   - [ ] Hashtags: [required hashtags]
   - [ ] Link/Swipe-up: [URL]
   - [ ] Promo code: [code]
   
   **Creative Direction**:
   - Tone: [description]
   - Visual style: [description]
   - Do's: [what to include]
   - Don'ts: [what to avoid]
   
   **Creative Freedom Level**: [High/Medium/Low]
   - [Explanation of boundaries]
   
   ### Content Themes
   
   | Theme | Description | % of Content | Example |
   |-------|-------------|--------------|---------|
   | [Theme 1] | [description] | [%] | [example] |
   | [Theme 2] | [description] | [%] | [example] |
   
   ### Approval Process
   
   | Stage | Reviewer | Timeline | Notes |
   |-------|----------|----------|-------|
   | Script/Concept | [who] | [days] before | [notes] |
   | Draft Content | [who] | [days] before | [notes] |
   | Final Approval | [who] | [days] before | [notes] |
   ```

6. **Create Campaign Timeline**

   ```markdown
   ## Campaign Timeline
   
   ### Key Dates
   
   | Milestone | Date | Owner |
   |-----------|------|-------|
   | Campaign Kick-off | [date] | [owner] |
   | Influencer Selection Complete | [date] | [owner] |
   | Outreach Complete | [date] | [owner] |
   | Contracts Signed | [date] | [owner] |
   | Product Shipment | [date] | [owner] |
   | Brief Delivery | [date] | [owner] |
   | Content Due | [date] | [owner] |
   | Content Review/Approval | [date] | [owner] |
   | Content Goes Live | [date] | [owner] |
   | Campaign Ends | [date] | [owner] |
   | Final Report Due | [date] | [owner] |
   
   ### Detailed Timeline
   
   **Phase 1: Pre-Campaign (Weeks 1-2)**
   
   | Week | Task | Owner | Deliverable |
   |------|------|-------|-------------|
   | 1 | Finalize strategy | [owner] | Strategy doc |
   | 1 | Influencer identification | [owner] | Shortlist |
   | 2 | Influencer outreach | [owner] | Confirmed partners |
   | 2 | Contract negotiation | [owner] | Signed contracts |
   
   **Phase 2: Production (Weeks 3-4)**
   
   | Week | Task | Owner | Deliverable |
   |------|------|-------|-------------|
   | 3 | Brief distribution | [owner] | Briefs sent |
   | 3 | Product shipment | [owner] | Products delivered |
   | 4 | Content creation | Influencers | Draft content |
   | 4 | Content review | [owner] | Approved content |
   
   **Phase 3: Activation (Weeks 5-6)**
   
   | Week | Task | Owner | Deliverable |
   |------|------|-------|-------------|
   | 5 | Content goes live | Influencers | Live posts |
   | 5-6 | Community management | [owner] | Engagement |
   | 5-6 | Real-time optimization | [owner] | Adjustments |
   
   **Phase 4: Post-Campaign (Week 7+)**
   
   | Week | Task | Owner | Deliverable |
   |------|------|-------|-------------|
   | 7 | Data collection | [owner] | Raw data |
   | 7 | Performance analysis | [owner] | Analysis |
   | 8 | Final report | [owner] | Campaign report |
   
   ### Gantt View
   
   ```
   Week:        1    2    3    4    5    6    7    8
   Strategy     ████
   Selection    ████ ████
   Contracts         ████ ████
   Briefing               ████
   Production              ████ ████
   Live                         ████ ████
   Analysis                               ████ ████
   ```
   ```

7. **Allocate Budget**

   ```markdown
   ## Budget Allocation
   
   ### Total Budget: $[X]
   
   ### Budget Breakdown by Category
   
   | Category | Amount | % of Total | Notes |
   |----------|--------|------------|-------|
   | Influencer Fees | $[X] | [%] | [notes] |
   | Product/Gifting | $[X] | [%] | [notes] |
   | Content Production | $[X] | [%] | [notes] |
   | Paid Amplification | $[X] | [%] | [notes] |
   | Agency/Tools | $[X] | [%] | [notes] |
   | Contingency | $[X] | [%] | 10% buffer |
   | **Total** | **$[X]** | **100%** | |
   
   ### Budget by Influencer Tier
   
   | Tier | # Influencers | Cost Each | Total | % |
   |------|---------------|-----------|-------|---|
   | Macro | [#] | $[X] | $[X] | [%] |
   | Micro | [#] | $[X] | $[X] | [%] |
   | Nano | [#] | $[X] | $[X] | [%] |
   
   ### Budget by Platform
   
   | Platform | Budget | % | Rationale |
   |----------|--------|---|-----------|
   | [Platform 1] | $[X] | [%] | [reason] |
   | [Platform 2] | $[X] | [%] | [reason] |
   
   ### Cost Efficiency Targets
   
   | Metric | Target | Calculation |
   |--------|--------|-------------|
   | CPM | $[X] | Budget ÷ (Est. Impressions/1000) |
   | CPE | $[X] | Budget ÷ Est. Engagements |
   | Cost per Content | $[X] | Budget ÷ Content Pieces |
   ```

8. **Establish Success Metrics**

   ```markdown
   ## Success Metrics & KPIs
   
   ### Primary KPIs
   
   | KPI | Target | Benchmark | Measurement |
   |-----|--------|-----------|-------------|
   | [KPI 1] | [target] | [industry avg] | [how measured] |
   | [KPI 2] | [target] | [industry avg] | [how measured] |
   | [KPI 3] | [target] | [industry avg] | [how measured] |
   
   ### Secondary Metrics
   
   | Metric | Target | Notes |
   |--------|--------|-------|
   | Total Reach | [X] | |
   | Total Impressions | [X] | |
   | Engagement Rate | [%] | |
   | Video Views | [X] | |
   | Link Clicks | [X] | |
   | Promo Code Uses | [X] | |
   | EMV Generated | $[X] | |
   
   ### Conversion Metrics (if applicable)
   
   | Metric | Target | Attribution |
   |--------|--------|-------------|
   | Website Visits | [X] | UTM tracking |
   | Conversions | [X] | Promo codes + pixels |
   | Revenue | $[X] | Attribution model |
   | ROAS | [X]:1 | Revenue ÷ Spend |
   
   ### Benchmarks
   
   | Metric | Our Target | Industry Avg | Past Campaign |
   |--------|------------|--------------|---------------|
   | [metric] | [target] | [avg] | [past] |
   
   ### Reporting Cadence
   
   | Report | Frequency | Contents | Audience |
   |--------|-----------|----------|----------|
   | Daily Tracker | Daily | Live metrics | Team |
   | Weekly Update | Weekly | Performance summary | Stakeholders |
   | Final Report | Post-campaign | Full analysis | Leadership |
   ```

9. **Compile Campaign Plan Document**

   ```markdown
   # Campaign Plan: [Campaign Name]
   
   ## Executive Summary
   
   **Campaign**: [Name]
   **Brand**: [Brand]
   **Timeline**: [Dates]
   **Budget**: $[X]
   **Goal**: [Primary objective in one sentence]
   
   **The Plan in Brief**:
   [2-3 sentence summary of the campaign approach]
   
   ---
   
   [Full sections as detailed above]
   
   ---
   
   ## Appendix
   
   ### A. Influencer Shortlist
   [Link to influencer discovery results]
   
   ### B. Brief Template
   [Link to brief-generator output]
   
   ### C. Content Examples
   [Reference content examples]
   
   ### D. Approval Workflows
   [Detailed approval process]
   
   ### E. Risk Mitigation
   
   | Risk | Likelihood | Impact | Mitigation |
   |------|------------|--------|------------|
   | [Risk 1] | [H/M/L] | [H/M/L] | [action] |
   | [Risk 2] | [H/M/L] | [H/M/L] | [action] |
   
   ---
   
   **Document Version**: 1.0
   **Last Updated**: [date]
   **Owner**: [name]
   **Approvals**: [required approvals]
   ```

## Example

**User**: "Create a campaign plan for a new sustainable sneaker launch targeting Gen Z on TikTok and Instagram with a $50K budget"

**Output**: [Complete campaign plan with sustainability messaging strategy, micro-influencer heavy approach, UGC-focused content, launch timeline, and conversion tracking via promo codes]

## Tips for Success

1. **Start with clear objectives** - Everything else flows from goals
2. **Know your audience deeply** - Use audience-analyzer insights
3. **Balance reach and engagement** - Mix influencer tiers strategically
4. **Build in flexibility** - Plans need room to adapt
5. **Set realistic targets** - Use benchmarks from past campaigns

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and handoff schema.
- [state-model.md](../../references/state-model.md) — memory tiers and save-path conventions.
- [CONNECTORS.md](../../CONNECTORS.md) — free/keyless data recipes per connector category.
- [audience-analyzer](../../insight/audience-analyzer/SKILL.md) — define the target audience this plan serves.
- [brief-generator](../../plan/brief-generator/SKILL.md) — turn the plan into per-influencer briefs.
- [budget-optimizer](../../plan/budget-optimizer/SKILL.md) — refine the budget allocation.
- [influencer-discovery](../../map/influencer-discovery/SKILL.md) — find influencers matching the criteria.

## Next Best Skill

- **Primary**: [brief-generator](../../plan/brief-generator/SKILL.md) — convert the approved plan into concrete influencer briefs.
- **Alternate**: [budget-optimizer](../../plan/budget-optimizer/SKILL.md) — pressure-test and optimize the budget split before locking the plan.
- **Alternate**: [influencer-discovery](../../map/influencer-discovery/SKILL.md) — build the shortlist against the selection criteria defined here.

Termination note: keep a visited-set of skills invoked this session. If the primary next skill has already run this session, stop and report the chain complete rather than re-invoking. Do not chain deeper than 3 hops from the originating request.
