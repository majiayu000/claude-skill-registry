---
name: market-intel
description: Track markets, trends, and opportunities
user_invocable: true
---

# Market Intel Skill

## Purpose
Monitor and analyze:
- Cryptocurrency markets
- Tech stocks
- Industry trends
- Emerging opportunities

## Invocation
```
/market-intel [focus] [options]
```

### Arguments
- `focus`: crypto, stocks, trends, or all
- `--asset [symbol]`: Specific asset to check
- `--summary`: Quick overview
- `--deep`: Detailed analysis

### Examples
```
/market-intel crypto               # Crypto market overview
/market-intel stocks --asset NVDA  # Check specific stock
/market-intel trends               # What's emerging
/market-intel all --summary        # Quick full briefing
```

## Coverage Areas

### Crypto Markets
| Asset | Priority | Notes |
|-------|----------|-------|
| BTC | High | Store of value narrative |
| ETH | High | Ecosystem activity |
| SOL | Medium | Alt L1 benchmark |
| Others | Low | As relevant |

### Tech Stocks
| Asset | Priority | Notes |
|-------|----------|-------|
| NVDA | High | AI bellwether |
| MSFT | High | Enterprise AI |
| GOOG | High | AI + search |
| META | Medium | Social + AI |
| AAPL | Medium | Consumer tech |

### Trends to Track
- AI developments
- Regulatory changes
- M&A activity
- Funding rounds
- Product launches

## Data Sources

### Price Data
- CoinGecko (crypto)
- Yahoo Finance (stocks)
- TradingView (charts)

### News & Analysis
- Bloomberg
- Reuters
- Crypto-specific outlets
- X/Twitter sentiment

### On-Chain (Crypto)
- Glassnode metrics
- Whale activity
- DeFi TVL

## Workflow

1. **Gather**: Pull latest data
2. **Analyze**: Identify significant moves
3. **Context**: What's driving changes
4. **Opportunities**: What's actionable
5. **Report**: Summarize findings

## Output Format

```markdown
## Market Intel - [DATE]

### Summary
[One paragraph overview]

### Crypto
- BTC: $XX,XXX (X% 24h)
- ETH: $X,XXX (X% 24h)
- Notable: [Significant event]

### Stocks
- NVDA: $XXX (X% day)
- Notable moves: [What's moving]

### Trends
- [Emerging trend 1]
- [Emerging trend 2]

### Opportunities
- [Potential opportunity]

### Risk Factors
- [What to watch]
```

## Posting Integration

Can generate market commentary posts:
- Quick takes on moves
- Analysis threads
- Trend observations

Uses `personality/analyst.md` for voice.

## Disclaimers

Always include when sharing:
- "Not financial advice"
- "DYOR"
- "May have positions"

## Update Frequency

- Price checks: On demand
- Full analysis: Daily
- Trend review: Weekly
