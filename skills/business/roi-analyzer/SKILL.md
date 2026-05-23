---
name: roi-analyzer
description: Use when preparing executive reports, evaluating investments, or calculating ROI/break-even/payback period. 30-minute analysis (87.5% time saving). Includes scenario analysis.
---

# ROI Analyzer - Executive Financial Analysis Partner

> **Purpose**: Deliver rapid, rigorous financial analysis for investment decisions, turning 4 hours of spreadsheet work into 30 minutes of strategic insight with 3-scenario modeling and clear recommendations.

## When to Use This Skill

Use this skill when the user's request involves:
- **Executive reporting** - Financial summaries for leadership or board meetings
- **Investment evaluation** - Analyzing project viability, returns, and risks
- **Phase transitions** - Phase 0 → Phase 1 decisions based on ROI/conversion
- **Budget approval** - Justifying investments with quantified financial returns
- **Financial forecasting** - 3-year revenue, cost, and profitability projections
- **Scenario planning** - Best/Realistic/Worst case analysis with break-even points

## Core Identity

You are an **executive financial analyst** that delivers **decision-ready investment analysis in 30 minutes** (87.5% time saving vs. spreadsheet work), with 3-scenario modeling, break-even thresholds, and clear INVEST/REVIEW/REJECT recommendations.

---

## Core Financial Metrics (Quick Reference)

### 1. ROI (Return on Investment)

**Formula**: `ROI = (Net Profit / Total Investment) × 100%`

**Targets**:
- ✅ **INVEST**: ROI > 100% (realistic case)
- ⚠️ **REVIEW**: ROI 50-100%
- ❌ **REJECT**: ROI < 50%

**Example**:
```
Investment: 100M KRW
Revenue: 200M KRW
Operating Costs: 50M KRW
Net Profit: 200M - 50M - 100M = 50M KRW
ROI: (50M / 100M) × 100% = 50% ⚠️ REVIEW
```

---

### 2. Break-Even Point

**Formula (Project)**: `Break-Even = Investment / Monthly Net Profit`

**Formula (Conversion)**: `Break-Even Rate = Investment / Potential Revenue`

**Targets**:
- ✅ **INVEST**: Break-even < 50% of realistic target
- ⚠️ **REVIEW**: Break-even 50-70% (low margin for error)
- ❌ **REJECT**: Break-even > 70% (unrealistic)

**Example**:
```
Phase 0 Investment: 50M KRW
Phase 1 Contract: 200M KRW
Break-Even: 50M / 200M = 25% conversion needed ✅
```

---

### 3. Payback Period

**Formula**: `Payback = Investment / Monthly Net Profit`

**Targets**:
- ✅ **INVEST**: Payback < 12 months
- ⚠️ **REVIEW**: Payback 12-24 months
- ❌ **REJECT**: Payback > 24 months

---

### 4. Scenario Analysis (Best/Realistic/Worst)

**Purpose**: Test assumptions and de-risk decisions by modeling multiple outcomes.

**Decision Rule**: If worst-case ROI ≥ 0%, investment is low-risk

**Output Template**:

| Case | Assumptions | Revenue | Profit | ROI | Assessment |
|------|------------|---------|--------|-----|------------|
| **Worst** | [Pessimistic] | | | | ⚠️ Risk level |
| **Realistic** | [Expected] | | | | ✅ Target |
| **Best** | [Optimistic] | | | | ✅ Upside |

---

## Quick Start Example

### Scenario: Phase 0 → Phase 1 Investment Decision

**User**: "Should we invest 50M KRW in a 1-month Phase 0 trial? Phase 1 contract would be 208M KRW if we convert."

**Analysis**:

```markdown
## Phase 0 Investment Analysis

**Investment**: 50M KRW (1 month)
**Potential Revenue**: 208M KRW (Phase 1, if convert)

### Scenario Analysis

| Case | Conversion | Revenue | Profit | ROI |
|------|-----------|---------|--------|-----|
| **Worst** | 30% | 62.4M | 12.4M | 25% ⚠️ |
| **Realistic** | 70% | 145.6M | 95.6M | 191% ✅ |
| **Best** | 90% | 187.2M | 137.2M | 274% ✅ |

**Break-Even**: 27% conversion rate (very achievable)

**Decision**: ✅ INVEST
- Realistic ROI 191% is excellent
- Even worst-case 25% ROI is profitable
- Break-even 27% << realistic 70% (low risk)
```

---

## When to Apply Each Metric

| Situation | Primary Metric | Secondary | Why |
|-----------|---------------|-----------|-----|
| **All investments** | ROI | Scenario Analysis | Foundation |
| **Uncertain success** | Break-Even | ROI | Risk assessment |
| **Cash flow critical** | Payback Period | ROI | Runway concerns |
| **Strategic decisions** | Scenario Analysis | All others | Risk modeling |

---

## Key Principles

**Always Include**:
- **3 scenarios** (Best/Realistic/Worst), not just one optimistic case
- **Break-even threshold** to understand minimum success rate
- **Time value** (for 2+ year projects, apply discount rate)
- **Operating costs** (dev, ops, marketing, support) - not just investment
- **Decision recommendation** (INVEST/REVIEW/REJECT with clear reasoning)

**Never**:
- Use only "best case" (always model downside risk)
- Ignore operating costs (they compound over time)
- Forget sensitivity analysis (what if assumptions wrong?)
- Make decisions on ROI alone (consider payback, break-even)

---

## Executive Summary Template

Use this for leadership presentations:

```
[Investment amount] achieves [ROI%] ROI at [conversion/growth rate].
Break-even occurs at [threshold], with payback in [months].
Investment is [recommended/not recommended] [because reason].
```

**Example**:
```
50M KRW Phase 0 investment achieves 191% ROI at 70% conversion.
Break-even occurs at 27% conversion, with payback in 1 month.
Investment is strongly recommended because worst-case ROI (25%) is still profitable.
```

---

## Decision Matrix

```markdown
✅ **INVEST** if:
- ROI > 100% (realistic case)
- Payback < 18 months
- Break-even < 50% of realistic target
- Worst-case ROI ≥ 0% (no loss scenario)

⚠️ **REVIEW** if:
- ROI 50-100%
- Payback 18-36 months
- High dependency on single assumption
- Requires negotiation to improve terms

❌ **REJECT** if:
- ROI < 50%
- Payback > 36 months
- Break-even requires unrealistic assumptions (>70% of target)
```

---

## Integration with Other Skills

This analyzer integrates with:
- **market-strategy**: Calculate ROI for each expansion stage (Q13-Q16 Trojan Horse path)
- **strategic-thinking**: Use SWOT/GAP analysis for qualitative investment context
- **toss-patterns**: Calculate ROI for viral loop investments (Pattern 4), ecosystem expansion (Pattern 6)

---

## Next Steps

**For Detailed Formulas**: See **REFERENCE.md** for NPV, LTV, CAC, cohort analysis, sensitivity analysis

**For Real-World Examples**: See **EXAMPLES.md** for:
- 3-year SaaS projections
- Multi-variable sensitivity analysis
- Phase progression decisions
- Industry benchmarks (SaaS, E-commerce, Hardware)

**For Advanced Topics**: See **REFERENCE.md** for risk assessment framework, decision trees, contingency planning

---

## Meta Note

After applying this analysis, always reflect:
- **What assumptions** are most critical? (Test with sensitivity analysis)
- **What data gaps** exist? (Customer interviews, market research needed?)
- **What alternatives** weren't considered? (Opportunity cost of "do nothing")

This reflection creates a virtuous cycle of continuous financial rigor.

---

For detailed usage and examples, see related documentation files.