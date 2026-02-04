---
name: product-roadmap
version: "1.1.0"
category: business
description: "Product Roadmap Skill"
last_updated: 2026-02-03
---

# Product Roadmap Skill

> Version: 1.0.0
> Category: Product
> Triggers: Planning work, checking priorities, roadmap questions

## Quick Reference

### Current Capabilities (Phase 0 Complete)

- ✅ 77 AI agent definitions across 23 categories
- ✅ 106+ automation scripts
- ✅ 88+ documentation files
- ✅ Full CLI tooling (workspace, repository_sync)
- ✅ O&G Knowledge System with RAG
- ✅ Claude Flow MCP integration
- ✅ Compliance propagation framework

### Strategic Focus Areas

1. Foundation strengthening (configuration, testing)
2. Enhanced automation and parallel operations
3. Monitoring dashboards and visibility
4. Cross-repository intelligence
5. Team collaboration features
6. Advanced CI/CD orchestration

## Phase Overview

| Phase | Focus | Timeline |
|-------|-------|----------|
| **1** | Foundation Strengthening | Weeks 1-3 |
| **2** | Enhanced Automation | Weeks 4-7 |
| **3** | Monitoring & Dashboards | Weeks 8-11 |
| **4** | Cross-Repository Intelligence | Weeks 12-16 |
| **5** | Team Collaboration | Weeks 17-20 |
| **6** | Advanced CI/CD | Weeks 21-26 |

## Phase 1: Foundation (Critical)

**Goal:** All repos configured, 80%+ test coverage, zero broken integrations

### Must Complete
- [ ] Configure all 25 repository URLs in `config/repos.conf`
- [ ] Verify all 5 MCP servers operational
- [ ] Finalize `config/sync-items.json` settings
- [ ] Establish cross-repository test framework
- [ ] Populate `docs/api/` directory

## Phase 2: Enhanced Automation

**Goal:** 50% reduction in manual sync time

### Must Complete
- [ ] Smart conflict resolution with auto-merge
- [ ] Enhanced parallel operations (10-repo)
- [ ] Automated dependency updates across repos
- [ ] Branch strategy templates

## Phase 3: Monitoring Dashboards

**Goal:** Real-time dashboard operational, 90% issue auto-detection

### Must Complete
- [ ] Real-time web dashboard (Plotly visualizations)
- [ ] Health score metrics per repository
- [ ] Alerting system (build failure, stale branches)
- [ ] Activity timeline visualization

## Effort Scale

| Code | Duration | Examples |
|------|----------|----------|
| **XS** | 1 day | Config change, single script update |
| **S** | 2-3 days | New utility script, docs update |
| **M** | 1 week | New feature module, integration |
| **L** | 2 weeks | Major feature, cross-repo changes |
| **XL** | 3+ weeks | System-wide changes, new subsystems |

## Domain-Specific Initiatives

### Energy & O&G
- O&G Knowledge System enhancement
- BSEE data integration
- Lower Tertiary analysis automation

### Marine Engineering
- Marine analysis standardization
- Engineering verification system

### Web & Applications
- Full-stack templates (Rails 8 + React)
- Component library sync

## Success Metrics

### Phase 1
- All 25 repositories configured
- 80% baseline test coverage
- Zero broken MCP integrations

### Phase 2
- 50% reduction in manual sync time
- 80% auto-resolution of common conflicts

### Phase 3
- Dashboard operational with real-time data
- 90% issue auto-detection rate

## Repository Count

- **Total:** 25+ repositories
- **Work:** 15 repositories
- **Personal:** 11 repositories

## Full Reference

See: @.agent-os/product/roadmap.md

## Product Roadmap Frameworks

### Now / Next / Later
The simplest and often most effective roadmap format:

- **Now** (current sprint/month): Committed work. High confidence in scope and timeline. These are the things the team is actively building.
- **Next** (next 1-3 months): Planned work. Good confidence in what, less confidence in exactly when. Scoped and prioritized but not yet started.
- **Later** (3-6+ months): Directional. These are strategic bets and opportunities we intend to pursue, but scope and timing are flexible.

When to use: Most teams, most of the time. Especially good for communicating externally or to leadership because it avoids false precision on dates.

### Quarterly Themes
Organize the roadmap around 2-3 themes per quarter:

- Each theme represents a strategic area of investment
- Under each theme, list the specific initiatives planned
- Themes should map to company or team OKRs
- This format makes it easy to explain WHY you are building what you are building

When to use: When you need to show strategic alignment. Good for planning meetings and executive communication.

### OKR-Aligned Roadmap
Map roadmap items directly to Objectives and Key Results:

- Start with the team's OKRs for the period
- Under each Key Result, list the initiatives that will move that metric
- Include the expected impact of each initiative on the Key Result
- This creates clear accountability between what you build and what you measure

When to use: Organizations that run on OKRs.

### Timeline / Gantt View
Calendar-based view with items on a timeline:

- Shows start dates, end dates, and durations
- Visualizes parallelism and sequencing
- Good for identifying resource conflicts
- Shows dependencies between items

When to use: Execution planning with engineering. NOT good for communicating externally (creates false precision expectations).

## Prioritization Frameworks

### RICE Score
Score each initiative on four dimensions, then calculate RICE = (Reach x Impact x Confidence) / Effort

- **Reach**: How many users/customers will this affect in a given time period?
- **Impact**: How much will this move the needle for each person reached? Score: 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal.
- **Confidence**: How confident are we in the estimates? 100% = high, 80% = medium, 50% = low.
- **Effort**: How many person-months of work?

### MoSCoW
- **Must have**: Non-negotiable commitments.
- **Should have**: Important and expected, but delivery is viable without them.
- **Could have**: Desirable but clearly lower priority.
- **Won't have**: Explicitly out of scope for this period.

### ICE Score
Simpler than RICE. Score each item 1-10 on Impact, Confidence, and Ease.

ICE Score = Impact x Confidence x Ease

### Value vs Effort Matrix
- **High value, Low effort** (Quick wins): Do these first.
- **High value, High effort** (Big bets): Plan these carefully.
- **Low value, Low effort** (Fill-ins): Do these when you have spare capacity.
- **Low value, High effort** (Money pits): Do not do these.

## Dependency Mapping

### Identifying Dependencies
- **Technical dependencies**: Feature B requires infrastructure work from Feature A
- **Team dependencies**: Feature requires work from another team
- **External dependencies**: Waiting on a vendor, partner, or third-party integration
- **Knowledge dependencies**: Need research or investigation results before starting
- **Sequential dependencies**: Must ship Feature A before starting Feature B

### Managing Dependencies
- List all dependencies explicitly in the roadmap
- Assign an owner to each dependency
- Set a "need by" date
- Build buffer around dependencies -- they are the highest-risk items
- Flag dependencies that cross team boundaries early
- Have a contingency plan: what do you do if the dependency slips?

## Capacity Planning

### Allocating Capacity
A healthy allocation for most product teams:

- **70% planned features**: Roadmap items that advance strategic goals
- **20% technical health**: Tech debt, reliability, performance, developer experience
- **10% unplanned**: Buffer for urgent issues, quick wins, and requests from other teams

### Capacity vs Ambition
- If roadmap commitments exceed capacity, something must give
- Do not solve capacity problems by pretending people can do more -- solve by cutting scope
- When adding to the roadmap, always ask: "What comes off?"

## Communicating Roadmap Changes

### How to Communicate Changes
1. **Acknowledge the change**: Be direct about what is changing and why
2. **Explain the reason**: What new information drove this decision?
3. **Show the tradeoff**: What was deprioritized to make room?
4. **Show the new plan**: Updated roadmap with the changes reflected
5. **Acknowledge impact**: Who is affected and how?

### Avoiding Roadmap Whiplash
- Do not change the roadmap for every piece of new information
- Batch roadmap updates at natural cadences (monthly, quarterly)
- Distinguish between "roadmap change" (strategic reprioritization) and "scope adjustment" (normal execution refinement)
- Track how often the roadmap changes

## Sources

- Original: workspace-hub product roadmap
- Enriched: [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (2026-02-03)

---

*Use this when planning work, checking priorities, or understanding product direction.*
