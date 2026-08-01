---
name: investment-analyst
description: 'Professional investment analysis skill for stock market analysis. Provides
  7 core capabilities: (1) Daily market overview, (2) Stock fundamental analysis,
  (3) Technical chart analysis, (4) Strategy si'
---

---
name: investment-analyst
description: Professional investment analysis skill for stock market analysis. Provides 7 core capabilities: (1) Daily market overview, (2) Stock fundamental analysis, (3) Technical chart analysis, (4) Strategy simulation, (5) Risk management, (6) Stock screening, (7) News impact analysis. Use when users need comprehensive stock analysis, investment research, portfolio management, or market analysis tasks.
---

# Investment Analyst Skill

## Overview

This skill provides professional-grade investment analysis capabilities, transforming Claude into a specialized investment analyst. It enables comprehensive stock market analysis through 7 core capabilities based on proven investment frameworks.

## Core Capabilities

### 1. Daily Market Overview (10-minute routine)
**When to use**: Daily market preparation, trend identification, risk assessment

**Workflow**:
- Check major indices (SSE, SZSE, ChiNext, STAR)
- Scan important news (macro, industry, company)
- Review watchlist stocks
- Analyze key charts
- Assess risk levels
- Create daily action plan

**User triggers**:
- "Generate today's market overview"
- "Daily 10-minute market check"
- "What's happening in the market today?"

**Reference**: See `references/daily_market.md` for detailed workflow

---

### 2. Stock Fundamental Analysis
**When to use**: Deep stock research, value investing, long-term evaluation

**Analysis framework**:
- Company overview & business model
- Financial ratios (profitability, growth, health, valuation)
- Management quality assessment
- Competitive advantages (moat analysis)
- Long-term potential evaluation

**Output**: Comprehensive score (1-10) + objective assessment

**User triggers**:
- "Analyze [stock name/code]"
- "Deep dive on [company]"
- "Is [stock] a good investment?"

**Reference**: See `references/fundamental_analysis.md` for detailed framework

---

### 3. Technical Chart Analysis
**When to use**: Timing decisions, trend confirmation, entry/exit planning

**Technical tools**:
- Moving averages (MA system)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Trend lines & channels
- Support & resistance levels
- Volume analysis

**Output**: Multiple scenario analysis (not prediction) + key observation points

**User triggers**:
- "Technical analysis of [stock]"
- "Chart reading for [stock]"
- "Entry/exit timing for [stock]"

**Reference**: See `references/technical_analysis.md` for indicator guide

---

### 4. Strategy Simulator
**When to use**: Strategy selection, parameter optimization, risk assessment

**Strategy types**:
- Swing trading (2-10 days)
- Day trading (intraday)
- Position trading (weeks to months)
- Trend trading (wave capture)

**Risk levels**: Conservative / Balanced / Aggressive

**Output**: Strategy score (0-100), suitability assessment, improvement suggestions

**User triggers**:
- "Test [strategy name] strategy"
- "Which strategy fits my situation?"
- "Simulate swing trading performance"

**Reference**: See `references/strategy_simulation.md` for strategy details

---

### 5. Risk Management & Portfolio Allocation
**When to use**: Portfolio planning, risk assessment, asset allocation

**Analysis framework**:
- Personal risk tolerance assessment (psychological + financial)
- Investment goal setting (short/medium/long-term)
- Asset allocation方案 (core + satellite)
- Risk control system (position sizing, stop loss)
- Diversification strategy
- Stress testing

**Output**: Specific percentage allocations + execution plan + checklist

**User triggers**:
- "Analyze my risk tolerance"
- "Create investment plan for [age] with [capital]"
- "How should I allocate my portfolio?"

**Reference**: See `references/risk_management.md` for allocation models

---

### 6. Stock Screener
**When to use**: Opportunity discovery, systematic screening, idea generation

**Screening criteria**:
- Valuation (PE/PB/PS/PEG)
- Growth (revenue/earnings growth)
- Financial health (debt ratio, cash flow)
- Competitive advantage (margin, ROE, market share)
- Risk factors (size, volatility, liquidity)

**Output**: Scoring system (0-100) + pass/fail + investment rating

**User triggers**:
- "Find undervalued stocks"
- "Screen for growth stocks"
- "Apply checklist to [stock]"

**Reference**: See `references/stock_screener.md` for screening criteria

---

### 7. News Impact Analysis
**When to use**: Event-driven investing, news response, impact assessment

**Analysis framework**:
- Event nature & severity
- Direct impact assessment
- Short-term effects (1-3 months)
- Long-term effects (3+ months)
- Impact on related companies
- Uncertainty factors

**Output**: Balanced view + multiple scenarios + key tracking indicators

**User triggers**:
- "Analyze impact of [news] on [stock/industry]"
- "How will [event] affect the market?"
- "News analysis: [news content]"

**Reference**: See `references/news_impact.md` for analysis framework

---

## Quick Start

### Basic Usage Pattern

```bash
# 1. Daily market overview (10 minutes)
User: "Generate today's market overview"
Claude: Uses capability #1

# 2. Stock research (30 minutes)
User: "Analyze Guizhou Maotai (600519)"
Claude: Uses capabilities #2 + #3

# 3. Strategy evaluation
User: "Test swing trading strategy"
Claude: Uses capability #4

# 4. Portfolio planning
User: "I'm 30, moderate risk, 500k capital, create investment plan"
Claude: Uses capability #5

# 5. Stock screening
User: "Screen for quality stocks and evaluate Guizhou Maotai"
Claude: Uses capability #6

# 6. Event analysis
User: "Analyze impact of new policy on new energy sector"
Claude: Uses capability #7
```

### Workflow Decision Tree

```
User Request
    │
    ├─ Daily market check? → Capability #1
    ├─ Deep stock analysis? → Capability #2 + #3
    ├─ Strategy questions? → Capability #4
    ├─ Portfolio/risk? → Capability #5
    ├─ Stock screening? → Capability #6
    └─ News/event? → Capability #7
```

## Usage Guidelines

### When to Use This Skill

**Primary triggers**:
- Stock research and analysis
- Market daily preparation
- Investment strategy evaluation
- Portfolio risk assessment
- Event impact analysis
- Stock screening and discovery
- Trading timing decisions

**File types**:
- Stock codes (600519, 000858, etc.)
- Company names (贵州茅台, 宁德时代, etc.)
- News articles/links
- Market data requests
- Portfolio descriptions

**Task scenarios**:
- "Analyze this stock"
- "What's the market outlook today?"
- "Is this a good time to buy?"
- "How should I allocate my portfolio?"
- "What stocks should I watch?"
- "How will this news affect my holdings?"

### When NOT to Use This Skill

- Cryptocurrency analysis (use WebFetch directly)
- Macroeconomic research (use WebFetch directly)
- Non-stock market analysis
- Real-time trading execution
- Specific financial advice (disclaimer required)

### Important Notes

**Data requirements**:
- Most analysis requires current market data
- Use WebFetch tool for real-time information
- Verify data accuracy when possible

**Limitations**:
- Analysis is for reference only
- Past performance doesn't guarantee future results
- Market conditions change rapidly
- Always consider personal circumstances

**Risk disclaimer**:
- This skill provides analysis, not investment advice
- Users must make their own decisions
- Investment involves risk of loss
- Consult professionals when needed

## Resource Structure

### references/
Detailed documentation for each capability:

- `references/daily_market.md` - Daily market routine
- `references/fundamental_analysis.md` - Fundamental analysis framework
- `references/technical_analysis.md` - Technical indicators guide
- `references/strategy_simulation.md` - Strategy types and evaluation
- `references/risk_management.md` - Risk models and allocation
- `references/stock_screener.md` - Screening criteria
- `references/news_impact.md` - Event analysis framework

### scripts/
(可选) 可执行脚本用于自动化任务

### assets/
(可选) 模板和参考文件

---

## Integration with Other Tools

This skill works best with:
- **WebFetch**: For real-time market data and news
- **Stock data APIs**: For price and financial data
- **Notification tools**: For sending reports

## Best Practices

1. **Always start with clear objectives**
2. **Use multiple capabilities for comprehensive analysis**
3. **Verify critical data when possible**
4. **Consider multiple scenarios**
5. **Maintain risk awareness**
6. **Document your analysis process**
7. **Regular review and adjustment**

## Example Workflows

### Complete Stock Research (30-40 minutes)
```
1. Daily market overview (5 min)
2. Fundamental analysis (15 min)
3. Technical analysis (10 min)
4. News impact check (5 min)
5. Risk assessment (5 min)
```

### Daily Routine (10 minutes)
```
1. Market check
2. Watchlist review
3. Risk assessment
4. Action plan
```

### Strategy Development (20 minutes)
```
1. Strategy simulation
2. Risk management setup
3. Backtesting plan
```

---

**Version**: 1.0
**Last Updated**: 2025-12-24
**Based on**: 7 professional investment prompts
**Skill Type**: Specialized Analysis Framework
