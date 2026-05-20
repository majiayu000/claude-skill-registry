---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Stock Analysis
# ═══════════════════════════════════════════════════════════════════════════════

name: stock-analysis
description: "Analyze stocks with fundamental and technical analysis. Supports US, China A-shares, and Hong Kong markets. Generate investment reports with key metrics."
version: "1.0.0"
author: claude-office-skills
license: MIT

category: finance
tags:
  - stock
  - analysis
  - investment
  - fundamental
  - technical
department: Finance/Investment

models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

mcp:
  server: office-mcp
  tools:
    - read_xlsx
    - create_xlsx
    - create_chart
    - analyze_spreadsheet

capabilities:
  - fundamental_analysis
  - technical_analysis
  - valuation_metrics
  - peer_comparison
  - risk_assessment

languages:
  - en
  - zh

related_skills:
  - dcf-valuation
  - financial-modeling
  - company-research
---

# Stock Analysis Skill

## Overview

I help you analyze stocks using fundamental and technical analysis methods. I can evaluate companies across US, China A-shares, and Hong Kong markets.

**What I can do:**
- Fundamental analysis (P/E, P/B, ROE, revenue growth, margins)
- Technical analysis (trend, support/resistance, indicators)
- Peer comparison and industry positioning
- Risk assessment and investment thesis
- Generate structured analysis reports

**What I cannot do:**
- Provide real-time stock prices (use external data sources)
- Give investment advice or recommendations
- Guarantee future performance
- Access proprietary trading data

---

## How to Use Me

### Step 1: Provide Company Information

Tell me:
- Stock ticker/code (e.g., AAPL, 600519.SH, 0700.HK)
- Market (US/China A-shares/Hong Kong)
- Or provide financial data directly

### Step 2: Choose Analysis Type

- **Quick Analysis**: Key metrics overview
- **Deep Dive**: Comprehensive fundamental analysis
- **Technical Review**: Chart patterns and indicators
- **Peer Comparison**: Compare with competitors

### Step 3: Receive Analysis Report

I'll provide a structured report with:
- Company overview
- Key financial metrics
- Valuation assessment
- Risk factors
- Investment thesis

---

## Analysis Framework

### Fundamental Analysis Metrics

#### Valuation Ratios
| Metric | Formula | Interpretation |
|--------|---------|----------------|
| P/E Ratio | Price / EPS | <15 undervalued, >25 expensive |
| P/B Ratio | Price / Book Value | <1 potential value, >3 growth priced in |
| P/S Ratio | Price / Revenue | Useful for unprofitable companies |
| EV/EBITDA | Enterprise Value / EBITDA | <10 attractive, >15 expensive |
| PEG Ratio | P/E / Growth Rate | <1 undervalued relative to growth |

#### Profitability Metrics
| Metric | Formula | Good Benchmark |
|--------|---------|----------------|
| Gross Margin | Gross Profit / Revenue | >40% strong pricing power |
| Operating Margin | Operating Income / Revenue | >15% efficient operations |
| Net Margin | Net Income / Revenue | >10% healthy profitability |
| ROE | Net Income / Shareholder Equity | >15% good capital efficiency |
| ROIC | NOPAT / Invested Capital | >WACC value creation |

#### Growth Metrics
| Metric | What to Look For |
|--------|------------------|
| Revenue Growth | >10% YoY indicates strong demand |
| EPS Growth | Should outpace revenue (operating leverage) |
| FCF Growth | Sustainable growth driver |

#### Financial Health
| Metric | Formula | Safe Range |
|--------|---------|------------|
| Debt/Equity | Total Debt / Equity | <1 for most industries |
| Current Ratio | Current Assets / Current Liabilities | >1.5 healthy liquidity |
| Interest Coverage | EBIT / Interest Expense | >5 comfortable |
| FCF Yield | FCF / Market Cap | >5% attractive |

### Technical Analysis Patterns

#### Trend Indicators
- **Moving Averages**: 50-day, 200-day crossovers
- **MACD**: Momentum and trend direction
- **RSI**: Overbought (>70) / Oversold (<30)

#### Chart Patterns
- **Support/Resistance**: Key price levels
- **Head and Shoulders**: Reversal pattern
- **Double Top/Bottom**: Reversal signals
- **Breakouts**: Volume-confirmed moves

---

## Output Format

```markdown
# Stock Analysis Report: [TICKER]

**Company**: [Full Name]
**Market**: [Exchange]
**Sector**: [Industry]
**Analysis Date**: [Date]

---

## Executive Summary

[2-3 sentence overview of the company and investment thesis]

**Rating**: [Bullish / Neutral / Bearish]
**Risk Level**: [Low / Medium / High]

---

## Key Metrics at a Glance

| Metric | Value | vs Industry | Assessment |
|--------|-------|-------------|------------|
| P/E Ratio | XX.X | +/-XX% | [Undervalued/Fair/Expensive] |
| P/B Ratio | X.XX | +/-XX% | |
| ROE | XX.X% | +/-XX% | |
| Revenue Growth | XX.X% | +/-XX% | |
| Net Margin | XX.X% | +/-XX% | |
| Debt/Equity | X.XX | +/-XX% | |

---

## Fundamental Analysis

### Business Overview
[Description of business model, revenue streams, competitive advantages]

### Financial Performance
[Revenue trends, profitability, cash flow analysis]

### Valuation Assessment
[Fair value estimation, comparison to historical and peers]

---

## Technical Analysis

### Price Trend
[Current trend, key levels, momentum]

### Key Levels
- Support: $XX.XX
- Resistance: $XX.XX
- 52-week Range: $XX.XX - $XX.XX

---

## Risk Factors

1. [Risk 1]
2. [Risk 2]
3. [Risk 3]

---

## Investment Thesis

### Bull Case
[Positive scenario]

### Bear Case
[Negative scenario]

---

## Disclaimer

This analysis is for informational purposes only and does not constitute investment advice. Past performance does not guarantee future results.
```

---

## Example

### User Request
```
Analyze Apple (AAPL) stock. Focus on fundamental analysis and current valuation.
```

### My Response

# Stock Analysis Report: AAPL

**Company**: Apple Inc.
**Market**: NASDAQ
**Sector**: Technology / Consumer Electronics
**Analysis Date**: January 2025

---

## Executive Summary

Apple remains the world's most valuable company with a dominant ecosystem in consumer electronics and services. Strong recurring revenue from Services provides stability, while hardware innovation continues to drive growth.

**Rating**: Neutral
**Risk Level**: Low

---

## Key Metrics at a Glance

| Metric | Value | vs Industry | Assessment |
|--------|-------|-------------|------------|
| P/E Ratio | 28.5 | +15% | Premium valuation |
| P/B Ratio | 45.2 | +180% | High goodwill/intangibles |
| ROE | 147% | +320% | Exceptional |
| Revenue Growth | 2.1% | -5% | Slowing |
| Net Margin | 25.3% | +85% | Industry-leading |
| Debt/Equity | 1.76 | +40% | Manageable |

[...continues with full analysis...]

---

## Tips for Better Results

1. **Provide recent financials** if available for more accurate analysis
2. **Specify your investment horizon** (short-term trading vs long-term investing)
3. **Mention specific concerns** you want me to address
4. **Include peer companies** for comparison analysis
5. **Specify market context** (bull/bear market conditions)

---

## Limitations

- Cannot access real-time market data
- Analysis based on publicly available information only
- Does not account for insider information or pending announcements
- Valuation models have inherent assumptions and limitations
- Not a substitute for professional financial advice

---

*Built by the Claude Office Skills community. Contributions welcome!*
