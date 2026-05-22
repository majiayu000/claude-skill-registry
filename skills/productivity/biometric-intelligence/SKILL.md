---
name: biometric-intelligence
description: Uses Oura ring data to make energy-aware decisions about scheduling, task prioritization, and recovery recommendations. Understands HRV, sleep quality, readiness scores, and their implications for productivity.
---

# Biometric Intelligence Skill

This skill enables energy-aware decision making using Oura ring biometric data.

## Key Metrics from Oura

### Readiness Score (0-100)
- **85+**: Peak performance day - tackle hard problems
- **70-84**: Normal productivity - regular work
- **60-69**: Low energy - focus on maintenance tasks
- **<60**: Recovery needed - minimal cognitive load

### Sleep Score (0-100)
- **85+**: Well-rested - complex tasks OK
- **70-84**: Adequate - normal work capacity
- **<70**: Sleep debt - prioritize rest, avoid decisions

### HRV (Heart Rate Variability)
- **Above baseline**: Good recovery, stress tolerance high
- **Below baseline**: Accumulated stress, need recovery
- **Trending down**: Approaching burnout, reduce load

### Activity Balance
- **Met goal**: Good energy expenditure
- **Under goal**: May have excess energy, physical activity helps
- **Way over**: Rest needed, avoid stacking stress

## Energy-Aware Scheduling Principles

### High Readiness Days (85+)
- Schedule deep work sessions
- Tackle creative or complex problems
- Make important decisions
- Push on challenging goals
- Social/networking activities

### Medium Readiness Days (70-84)
- Regular task execution
- Meetings and collaboration
- Administrative work
- Learning and skill building
- Moderate exercise

### Low Readiness Days (<70)
- Quick wins and easy tasks
- Reading and passive learning
- Planning (not executing)
- Gentle movement only
- Social media/content consumption

## Hunter Brain + Biometrics Patterns

### When HRV is Low
- Resistance will be HIGH
- Don't fight it - log and redirect
- Use body doubling or external accountability
- Break tasks into 10-minute chunks

### When Sleep Score is Low
- Dopamine regulation is impaired
- Hyperfocus risk (on wrong things)
- Set hard time boundaries
- Avoid starting new projects

### Recovery Recommendations

Based on Oura data, recommend:

1. **Physical**: Light walk, stretching, nap
2. **Mental**: No new decisions, routine tasks only
3. **Social**: Low-stakes interactions
4. **Work**: Clear backlog, inbox zero, easy wins

## API Integration

The Oura data is available at:
```
GET /api/oura/daily
```

Response structure:
```json
{
  "readiness": 78,
  "sleep_score": 82,
  "hrv_balance": "above_baseline",
  "activity_score": 65,
  "recommendation": "Normal productivity day"
}
```

## Using This Skill

When a user asks about scheduling or prioritization:

1. Check current Oura data
2. Match task difficulty to energy level
3. Suggest appropriate activities
4. Warn about low-energy pitfalls
5. Recommend recovery if needed

Example response:
```
Based on your Oura data:
- Readiness: 72 (normal)
- Sleep: 68 (slightly low)
- HRV: below baseline

Recommendation: This is a "maintenance day" not a "breakthrough day."
Focus on:
✓ Clearing email backlog
✓ Quick task completions
✓ Light planning
✗ Avoid: Complex coding, important decisions, new initiatives

Consider a 20-min walk to boost HRV before afternoon work.
```
