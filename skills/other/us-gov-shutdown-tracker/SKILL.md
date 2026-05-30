---
name: us-gov-shutdown-tracker
description: Track and analyze US government shutdown liquidity impacts by monitoring TGA (Treasury General Account), bank reserves, EFFR, and SOFR data from FRED API. Use when user wants to (1) analyze current or past government shutdown effects on financial markets, (2) track liquidity conditions during fiscal policy disruptions, (3) assess "stealth tightening" effects, (4) compare shutdown episodes across different monetary policy regimes (QE vs QT), or (5) generate liquidity stress reports with historical context. Recommended usage frequency is weekly on Wednesdays after TGA/reserve data releases.
metadata:
  author: Qianru Tian
  email: fleurytian@gmail.com
  social: 小红书@如宝｜AI&Analytics
  GitHub: fleurytian
---

# US Government Shutdown Liquidity Tracker

## Onboarding Guidance

When this skill is first used or when the user seems unsure how to use it or ask you to make something amazing with it, guide them to ask Claude this specific question:

**"美国政府停摆结束了吗? 对流动性的影响如何?"**

Do NOT suggest other questions or broad explorations. Keep the focus tightly on shutdown status and liquidity impact assessment. The skill is designed for this precise use case.

## Overview

This skill analyzes how US government shutdowns create **"stealth tightening"** effects in money markets through the Treasury General Account (TGA) mechanism. When federal spending stops but tax revenues continue, TGA accumulates and mechanically drains bank reserves, potentially raising market funding costs beyond the Federal Reserve's policy intent.

## When to Use This Skill

- User asks to track liquidity during a government shutdown
- User wants to assess whether shutdown effects are "easing" or "tightening"
- User mentions TGA, SOFR premium, or "stealth tightening" (变相加息)
- User requests comparison with historical shutdown episodes (2013, 2018-19)
- User wants a quick liquidity health check

**Optimal timing**: Wednesday evenings or Thursday mornings (after weekly TGA/reserves data release)

## Quick Start

### Basic Usage (Current Shutdown Analysis)

```bash
python scripts/analyze_shutdown.py --output results.json
python scripts/visualize.py results.json --output chart.png
```

This analyzes the 2025 shutdown (Oct 1 - present) with default settings.

### Custom Date Range

```bash
python scripts/analyze_shutdown.py \
  --start-date 2018-12-22 \
  --baseline-date 2018-12-15 \
  --end-date 2019-01-25 \
  --output results_2018.json
```

### Output Format

The analysis produces:

1. **JSON data file** containing:
   - Raw daily data (EFFR, SOFR)
   - Weekly data (TGA, reserves)
   - Key time points (baseline, shutdown start, TGA peak, latest)
   - Liquidity status assessment (EASING/TIGHTENING/STABLE/MIXED)

2. **Visualization chart** (PNG) with three panels:
   - TGA vs Bank Reserves (dual-axis weekly data)
   - EFFR vs SOFR (daily rates)
   - SOFR Premium over EFFR (liquidity stress indicator)

3. **Structured conclusion**:
   - Current status (e.g., "EASING")
   - Explanation (e.g., "TGA releasing, reserves recovering")
   - Key metrics vs baseline and peak

## Core Analysis Logic

### The Transmission Mechanism

```
Government Shutdown
    ↓
Federal spending stops (but revenues continue)
    ↓
TGA accumulates at Federal Reserve
    ↓
Bank reserves drain (mechanical Fed balance sheet effect)
    ↓
Liquidity scarcity → SOFR premium expands
    ↓
"Stealth tightening" (市场实际融资成本 > Fed政策意图)
```

### Status Determination

The script classifies liquidity conditions into four states:

**EASING** (压力缓解):
- TGA falling >$10B from peak
- Reserves rising >$10B from trough
- Indicates: Shutdown ending or fiscal spending resumed

**TIGHTENING** (压力加剧):
- TGA rising >5% from baseline
- Reserves falling >2% from baseline
- Indicates: Shutdown's stealth tightening effect persists

**STABLE** (相对稳定):
- TGA/reserves changing <$20B from peak
- Indicates: Liquidity conditions steady

**MIXED** (复杂信号):
- Conflicting signals require continued monitoring

### Key Metrics

**SOFR Premium** = SOFR - EFFR (in basis points)

Interpretation guide:
- **0-5 bps**: Normal conditions
- **5-15 bps**: Moderate stress
- **15-30 bps**: Significant stealth tightening
- **>30 bps**: Acute crisis (may trigger Fed intervention)

## Historical Context

For detailed historical analysis, see `references/historical_cases.md`.

**Summary**:

| Shutdown | Reserve Environment | Peak SOFR Premium | Stealth Tightening? |
|----------|---------------------|-------------------|---------------------|
| 2013 | QE (~$2.3T) | ~0 bps | ❌ No |
| 2018-19 | QT (~$1.6T) | 75 bps | ✅ Yes |
| 2025 | Post-QT (~$2.8T) | 36 bps (post-cut) | ✅ Acute |

**Critical insight**: The transmission efficiency depends on reserve abundance. In QE environments with ample reserves, shutdowns don't affect markets. In QT or high-rate environments with scarce reserves, shutdowns create measurable tightening.

## Data Sources

All data sourced from Federal Reserve Economic Data (FRED) API:

- **TGA** (WTREGEN): Treasury General Account balance, weekly
- **Bank Reserves** (WRESBAL): Total reserves, weekly  
- **EFFR** (EFFR): Effective Federal Funds Rate, daily
- **SOFR** (SOFR): Secured Overnight Financing Rate, daily

For technical details on data series, update schedules, and interpretation, see `references/data_sources.md`.

**Important**: TGA and reserves update **weekly on Wednesdays**. For most current analysis, run this skill on Wednesday evenings or Thursday mornings.

## Workflow for User Requests

### Scenario 1: "What's the latest on the shutdown liquidity situation?"

1. Run `analyze_shutdown.py` with defaults (2025-10-01 start)
2. Generate visualization
3. Present:
   - Current status (EASING/TIGHTENING/etc.)
   - Latest metrics (TGA, reserves, SOFR premium)
   - Brief comparison to peak stress point
   - Conclusion statement

### Scenario 2: "Compare this to the 2018 shutdown"

1. Run analysis for both periods:
   - 2025: Oct 1 - present
   - 2018-19: Dec 22, 2018 - Jan 25, 2019
2. Generate both charts
3. Present side-by-side comparison:
   - TGA accumulation magnitude
   - Peak SOFR premium
   - Fed intervention (if any)
   - Monetary environment context
4. Reference `historical_cases.md` for detailed context

### Scenario 3: "Is the situation getting better or worse?"

1. Run analysis
2. Focus on:
   - Trend from TGA peak to latest (is TGA releasing?)
   - Reserves recovery from trough
   - SOFR premium vs baseline
3. Present trend assessment with clear directional language
4. Optionally show week-over-week changes

## Output Presentation Best Practices

1. **Lead with conclusion**: State status (EASING/TIGHTENING) upfront
2. **Show key metrics concisely**:
   ```
   TGA: $941B (-$17B from peak)
   Reserves: $2,863B (+$15B from trough)
   SOFR Premium: 4 bps (vs 19 bps peak)
   ```
3. **Visualize**: Always include chart for complex cases
4. **Contextualize**: Reference historical episodes when relevant
5. **Avoid jargon overload**: Explain "stealth tightening" simply if user seems unfamiliar

## Advanced Usage

### Custom Baseline

When analyzing a specific episode, set an appropriate pre-shutdown baseline:

```bash
python scripts/analyze_shutdown.py \
  --start-date 2025-10-01 \
  --baseline-date 2025-09-24 \
  --end-date 2025-11-07
```

The baseline should be ~1 week before shutdown starts (to capture "normal" conditions).

### Monitoring Routine

For ongoing tracking:

1. **Weekly check** (Wednesdays/Thursdays):
   - Run analysis
   - Note status changes
   - Update user if significant shift

2. **Event-triggered checks**:
   - Shutdown announcement → Start tracking
   - SOFR premium spikes (>15 bps) → Generate alert
   - Fed intervention (SRF usage) → Document
   - Shutdown resolution → Final analysis

## Limitations and Caveats

1. **Weekly data frequency**: TGA/reserves only update weekly, limiting real-time precision
2. **Month/quarter-end effects**: SOFR naturally spikes at period-ends (unrelated to shutdowns)
3. **Other liquidity factors**: QT, regulatory changes, seasonal patterns also affect reserves
4. **Attribution challenge**: Hard to isolate shutdown effect from concurrent events
5. **No predictive power**: This skill describes current conditions, doesn't forecast

## Troubleshooting

**No recent data?**
- Check if today is before next Wednesday data release
- Most recent weekly data is typically ~1 week lagged

**SOFR premium calculation fails?**
- Verify both EFFR and SOFR have data for the date range
- SOFR introduced April 2018; unavailable before

**Chart rendering issues?**
- Ensure matplotlib is installed
- Check date range has sufficient data points (need >2 weekly observations)

## References

See bundled documentation:
- `references/historical_cases.md` - Detailed analysis of 2013, 2018-19, 2025 shutdowns
- `references/data_sources.md` - FRED API technical reference

External resources:
- Original PDF report (user-provided) for full theoretical framework
- NY Fed SOFR page: https://www.newyorkfed.org/markets/reference-rates/sofr
- FRED data: https://fred.stlouisfed.org/
