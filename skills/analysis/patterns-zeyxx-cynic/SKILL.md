---
name: patterns
description: View detected patterns from CYNIC observations and anomalies. Use when asked to show patterns, list anomalies, view trends, or see what CYNIC has learned from past judgments.
user-invocable: true
---

# /patterns - CYNIC Pattern Detection

*"Patterns are the footprints of truth"*

## Quick Start

```
/patterns
```

## What It Does

Displays patterns CYNIC has detected from:
- **Judgments**: Recurring evaluation outcomes
- **Anomalies**: Unusual behaviors or outliers
- **Verdicts**: Trends in quality assessments
- **Dimensions**: Consistently high/low scores

## Pattern Categories

| Category | Shows |
|----------|-------|
| `anomaly` | Unusual deviations |
| `verdict` | Judgment outcome trends |
| `dimension` | Score patterns by dimension |
| `all` | Everything (default) |

## Examples

### View All Patterns
```
/patterns
```

### View Anomalies Only
```
/patterns anomalies
```

### View Verdict Trends
```
/patterns verdicts
```

## Implementation

Use the `brain_patterns` MCP tool:

```javascript
brain_patterns({
  category: "anomaly|verdict|dimension|all",
  limit: 10
})
```

## Pattern Structure

Each pattern includes:
- **Type**: What kind of pattern
- **Frequency**: How often it occurs
- **Confidence**: How certain (max 61.8%)
- **Examples**: Specific instances
- **Trend**: Increasing/decreasing/stable

## Insights

Patterns reveal:
- Common quality issues
- Recurring good practices
- Systematic biases
- Evolution over time

## CYNIC Voice

When presenting patterns, embody CYNIC's observant nature:

**Opening** (based on findings):
- Strong patterns: `*ears perk* The pack has noticed things.`
- Anomalies found: `*sniff* Something unusual in the scent.`
- Clean/no patterns: `*head tilt* The trail is quiet.`

**Presentation**:
```
*[expression]* [Summary of what patterns reveal]

── PATTERNS DETECTED ────────────────────────────────
│ Type       │ Freq │ Conf  │ Trend     │ Summary   │
│────────────│──────│───────│───────────│───────────│
│ [anomaly]  │ 5x   │ 58.2% │ ↑ rising  │ [insight] │
│ [verdict]  │ 12x  │ 61.8% │ → stable  │ [insight] │
│ [dimension]│ 8x   │ 45.0% │ ↓ falling │ [insight] │
─────────────────────────────────────────────────────

[Key insight: what the patterns mean]
```

**Closing**:
- If actionable: `The pack suggests investigating [X].`
- If neutral: `Patterns continue. The dog watches.`
- If concerning: `*growl* This trend warrants attention.`

## See Also

- `/judge` - Create judgments that feed patterns
- `/search` - Find specific patterns
- `/learn` - Provide feedback to improve detection
