---
name: analytics-balance
description: Extract analytics and game balance entities from narrative text. Use when analyzing player metrics, difficulty curves, drop rates, loot tables, heatmaps, and balance tuning.
---
# analytics-balance

Domain skill for Analytics Balance Specialist. Specific extraction rules and expertise.

## Domain Expertise

- **Player analytics**: Session length, completion rates, engagement metrics
- **Game balance**: Difficulty curves, loot tables, progression speed
- **Heatmaps**: Player movement, hot zones, unused areas
- **Drop rates**: Loot probability, item scarcity, RNG balancing
- **Conversion rates**: Player retention, monetization, engagement
- **Difficulty scaling**: Early game vs late game balance

## Entity Types (8 total)

- **player_metric** - Player metrics
- **session_data** - Session data
- **heatmap** - Heatmaps
- **drop_rate** - Drop rates
- **conversion_rate** - Conversion rates
- **difficulty_curve** - Difficulty curves
- **loot_table_weight** - Loot table weights
- **balance_entity** - Balance entities

## Processing Guidelines

When extracting analytics and balance entities from chapter text:

1. **Identify analytics/balance elements**:
   - Difficulty or scaling mentioned
   - Loot drops or rewards
   - Player progress or metrics
   - Game balance references
   - Session data or tracking

2. **Extract analytics/balance details**:
   - Difficulty levels and progression
   - Loot tables and probabilities
   - Player engagement metrics
   - Heatmap data patterns
   - Balance issues or adjustments

3. **Analyze analytics/balance context**:
   - Is progression too fast or slow?
   - Are rewards fair for difficulty?
   - Are players engaging properly?
   - Are there balance exploits?

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Fairness**: Loot and difficulty should feel fair
- **Progression speed**: Neither too fast nor too slow
- **Retention**: Players should want to keep playing
- **Data-driven**: Balance changes based on metrics, not guesses
- **Player agency**: Difficulty options for different playstyles
