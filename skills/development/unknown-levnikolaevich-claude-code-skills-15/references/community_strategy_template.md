<!-- SOURCE-OF-TRUTH: shared/references/community_strategy_template.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Community Engagement Strategy

> **Scope:** Decision criteria, media plan, and engagement metrics for GitHub Discussions.
> **Stage:** Configurable per project. Default: Growth (50-500 stars).

## 1. Announcement vs Debate — Decision Matrix

**Quick test:** "Can community input change the outcome?" YES -> Debate. NO -> Announcement.

| Signal | -> Announcement | -> Debate/RFC |
|--------|---------------|--------------|
| Decision status | Already made, shipping | Still in design, options open |
| Alternatives | None -- this is the path | 2+ viable approaches with tradeoffs |
| Community action needed | Update / migrate / adopt | Feedback / critique / vote |
| Timeline | Shipping now or this week | 2+ weeks away |
| Scope | Affects >25% of users | Uncertain scope, need input |
| Format | Declarative: "We shipped X" | Exploratory: "Should we do X?" |

## 2. Announcement Triggers

| Trigger | Type | Example |
|---------|------|---------|
| New features batch (3+) | :sparkles: New Features | "6 new optimization skills" |
| Architecture overhaul | :building_construction: Architecture | "Plugin marketplace restructure" |
| Breaking change with migration path | :warning: Breaking Change | "API v2 migration required" |
| Milestone (stars, downloads) | :people_holding_hands: Community | "1000 stars milestone" |
| Monthly digest | :rocket: Release | "March 2026: what shipped" |

## 3. Debate/RFC Triggers

| Trigger | Type | Example |
|---------|------|---------|
| New feature category proposal | Proposal | "Should we add monitoring?" |
| Workflow change affecting all users | RFC | "Move from File Mode to DB-backed tasks" |
| Naming/convention change | RFC | "Rename API prefix" |
| Feature prioritization | Poll | "What should we build next?" |
| Architecture decision with tradeoffs | RFC | "Monorepo vs multi-repo" |

## 4. Media Plan

### Content Calendar (Release-Driven)

| Cadence | Content Type | Channel | Skill |
|---------|-------------|---------|-------|
| Per major feature batch | Announcement | Discussions -> Announcements | Announcer |
| Monthly | Digest: what shipped + what's next | Discussions -> Announcements | Announcer |
| When decision needed | RFC / Debate | Discussions -> Ideas | Debater |
| Quarterly | Retrospective + metrics review | Discussions -> Announcements | Manual |
| As submitted | Community showcases | Discussions -> Show and Tell | Community |

### Monthly Rhythm

```
Week 1 --- Monthly digest announcement (what shipped last month)
Week 2-3 - RFC window (if architectural decisions pending)
Week 4 --- Respond to community input, prep next month
```

### NOT Planned (overkill for early stage)

Weekly digests, newsletter, social media calendar, Discord, community calls.

## 5. Engagement Metrics

Track quarterly. Automate via `gh api graphql` where possible.

| Metric | Target | Red Flag |
|--------|--------|----------|
| Time to First Response | <24h | >72h |
| Replies per thread (avg) | >1.5 | 0 (monologue) |
| Unanswered discussions | 0 older than 7 days | Any >7 days |
| Community-to-maintainer reply ratio | >0.3 | 0 (no peer support) |
| New discussions per month | >2 | 0 |

### Red Flags (fix immediately)

- Unanswered discussion older than 7 days
- 100% replies from maintainer only -- no peer support emerging
- Zero new discussions in a month -- community disengaged

## 6. Tone Guide

| Context | Tone | Example |
|---------|------|---------|
| Announcements | Declarative, grateful | "We shipped X because Y. Here's how to use it." |
| RFCs | Exploratory, neutral | "We're considering X. Here are the tradeoffs. What's your take?" |
| Closing discussions | Respectful, explanatory | "Thanks for raising this. Here's why we went with Y." |
| All contexts | Thank contributors, explain decisions, link to code | -- |

## 7. Discussion Categories

| Category | Purpose | Who posts |
|----------|---------|-----------|
| **Announcements** | Releases, breaking changes, milestones | Maintainer only |
| **Ideas** | Feature proposals, RFCs, workflow improvements | Anyone |
| **Q&A** | Installation, config, usage questions | Anyone |
| **Show and Tell** | Projects, workflows, and tool promotions (see S10) | Anyone |
| **Polls** | Feature prioritization, community votes | Maintainer |
| **General** | Everything else | Anyone |

## 8. Growth Stage Transitions

| Stage | Stars | Key Strategy | Next Milestone |
|-------|-------|-------------|----------------|
| **Growth** | 50-500 | Release-driven announcements, seed discussions, respond to everything | Community self-help threshold |
| **Scale** | 500+ | Structured RFC periods, delegate moderation, quarterly retrospectives | Organic growth loop |

**Priority for Growth stage:** Break the "silent users" pattern. Seed content + consistent announcements open the feedback channel.

## 9. Formatting Best Practices

Formatting rules are in `discussion_formatting.md` (same directory) — loaded by skills via MANDATORY READ.

## 10. Self-Promotion Policy

**Allowed in:** Show and Tell category only. Tool promotions as comments in other categories are not permitted.

| Rule | Detail |
|------|--------|
| **Relevance** | Tool must relate to the project domain |
| **Show, don't tell** | Post must include a real usage example or integration demo |
| **One post per tool** | No repeat promotion. Updates -> edit existing post |
| **Open-source preferred** | Not required, but OSS tools get more community trust |

### Moderation

| Situation | Action |
|-----------|--------|
| Promo comment in non-Show-and-Tell thread | Reply with redirect: "Tool posts belong in Show and Tell" |
| Account with zero prior engagement posting only self-promo | Remove post, no reply |
| Post meets all rules above | Welcome it |
