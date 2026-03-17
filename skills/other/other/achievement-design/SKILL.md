---
name: achievement-design
description: Extract achievement entities from narrative text. Use when analyzing trophies, badges, ranks, leaderboards, titles, and progression reward milestones.
---
# achievement-design

Domain skill for Achievement Specialist. Specific extraction rules and expertise.

## Domain Expertise

- **Achievement systems**: Unlockables, milestones, progression rewards
- **Reward structures**: Trophies, badges, titles, ranks
- **Leaderboards**: Competitive rankings, scores, leaderboards
- **Progression milestones**: Meaningful achievement points
- **Player recognition**: Awards for accomplishments

## Entity Types (6 total)

- **achievement** - Achievement unlocks
- **trophy** - Trophy rewards
- **badge** - Badge awards
- **title** - Title unlocks
- **rank** - Player ranks
- **leaderboard** - Leaderboards

## Processing Guidelines

When extracting achievement entities from chapter text:

1. **Identify achievement elements**:
   - Achievement milestones mentioned
   - Trophies or awards referenced
   - Titles or ranks earned
   - Leaderboard mentions
   - Rewards for accomplishments

2. **Extract achievement details**:
   - Achievement name, criteria, reward
   - Trophy type, rarity, significance
   - Title prefix/suffix or special names
   - Rank requirements and benefits
   - Leaderboard categories and scoring

3. **Analyze achievement context**:
   - Achievement difficulty tiers
   - Competitive vs cooperative achievements
   - Solo vs group achievements
   - Hidden achievements vs obvious ones

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Progressive achievements**: Some achievements have multiple tiers
- **Hidden achievements**: Not all achievements are immediately visible
- **Group achievements**: Some require multiple players
- **Seasonal leaderboards**: Rankings may reset periodically
- **Title stacking**: Players may earn multiple titles
