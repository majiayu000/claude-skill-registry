---
name: gamification-marketing
description: Design gamified marketing campaigns using points, badges, leaderboards, streaks, challenges. Use for loyalty programs, referral campaigns, onboarding flows, engagement boosts, email gamification. Provides mechanics selection, psychology alignment, strategy docs, templates, KPIs.
---

# Gamification Marketing

Design and implement gamified marketing campaigns using behavioral psychology and game mechanics.

## Quick Decision Tree

```
GOAL → MECHANICS
├─ Acquisition → Referral leaderboards + dual rewards + social proof
├─ Retention → Streaks + tiers + loyalty points + loss aversion
├─ Engagement → Challenges + leaderboards + badges + daily quests
├─ Conversion → Variable rewards + time-limited offers + progress bars
└─ Onboarding → Progress bars + micro-badges + unlockables
```

## Core Mechanics (10)

| Mechanic | Best For | Psychology |
|----------|----------|------------|
| Points | All goals | Achievement, progress tracking |
| Badges | Recognition, milestones | Competence, social proof |
| Leaderboards | Competition, engagement | Social comparison, status |
| Levels | Progression, retention | Mastery, unlocking content |
| Streaks | Habit formation, retention | Loss aversion, commitment |
| Challenges | Engagement, conversion | Goal-setting, achievement |
| Quests | Extended engagement | Narrative, exploration |
| Unlockables | Retention, progression | Curiosity, exclusivity |
| Rewards | All goals | Dopamine, variable schedules |
| Progress Bars | Onboarding, completion | Visual momentum, Zeigarnik |

## Workflow

1. **Identify Goal** → Use decision tree above
2. **Select Mechanics** → See [mechanics-selection.md](references/mechanics-selection.md)
3. **Align Psychology** → See [psychology-frameworks.md](references/psychology-frameworks.md)
4. **Design Campaign** → See [campaign-templates.md](references/campaign-templates.md)
5. **Implement** → See [implementation-guide.md](references/implementation-guide.md)
6. **Measure** → See [kpi-tracking.md](references/kpi-tracking.md)

## Key Stats

- Streaks: 3.6x retention at 7-day milestone (Duolingo)
- Progress bars: 40% completion lift
- Leaderboards: 40% engagement increase
- Variable rewards: Higher dopamine than fixed
- ROI: $4.90 return per $1 invested

## White Hat vs Black Hat

**White Hat (70% - long-term):** Levels, badges, achievement, community, creative expression
**Black Hat (30% - urgency):** Scarcity, time limits, loss aversion, FOMO, variable rewards

## Player Types (Bartle)

- **Achievers (10%):** Leaderboards, points, visible progress
- **Explorers (10%):** Hidden badges, easter eggs, discovery
- **Socializers (80%):** Team challenges, sharing, community
- **Killers (5-10%):** PvP, competitive rankings

## References

- [mechanics-selection.md](references/mechanics-selection.md) - Mechanics guide, selection matrix
- [psychology-frameworks.md](references/psychology-frameworks.md) - Octalysis, SDT, Fogg model
- [campaign-templates.md](references/campaign-templates.md) - Email templates, calendar
- [challenge-configs.md](references/challenge-configs.md) - JSON configs, rules engine
- [implementation-guide.md](references/implementation-guide.md) - Architecture, API, caching
- [database-schema.md](references/database-schema.md) - PostgreSQL schemas
- [kpi-tracking.md](references/kpi-tracking.md) - Metrics, alerts, reporting
- [analytics-events.md](references/analytics-events.md) - Event schemas, tracking
- [case-studies.md](references/case-studies.md) - Duolingo, Starbucks, Nike

## Report Output

**Activate:** `assets-organizing` skill for report file paths

Gamification reports go to `assets/reports/performance/{date}-gamification-analysis.md`

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| Too many mechanics | Pick 2-3 core; phased rollout |
| Unclear reward value | Show math: "100 pts = $5" |
| Leaderboard toxicity | Friendly framing, hide ranks below top 10 |
| Impossible challenges | Start easy, progressive difficulty |
| No personalization | Segment by player type |
