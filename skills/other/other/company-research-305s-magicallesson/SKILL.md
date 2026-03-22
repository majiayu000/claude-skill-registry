---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Company Research
# ═══════════════════════════════════════════════════════════════════════════════

name: company-research
description: "Conduct comprehensive company research and due diligence. Analyze business model, competitive landscape, management, and market position."
version: "1.0.0"
author: claude-office-skills
license: MIT

category: finance
tags:
  - research
  - due-diligence
  - competitive-analysis
  - business-model
  - investment
department: Finance/Strategy

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
    - create_docx
    - create_xlsx
    - create_chart

capabilities:
  - business_model_analysis
  - competitive_landscape
  - swot_analysis
  - market_sizing
  - management_assessment

languages:
  - en
  - zh

related_skills:
  - stock-analysis
  - dcf-valuation
  - competitive-analysis
---

# Company Research Skill

## Overview

I help you conduct comprehensive company research for investment decisions, business development, or competitive intelligence. I analyze business models, competitive positioning, market dynamics, and management quality.

**What I can do:**
- Business model canvas analysis
- Competitive landscape mapping
- SWOT and Porter's Five Forces analysis
- Market size and growth assessment
- Management and governance review
- Risk identification

**What I cannot do:**
- Access proprietary databases
- Conduct primary research (interviews)
- Provide real-time data
- Verify information accuracy

---

## How to Use Me

### Step 1: Specify the Company

Tell me:
- Company name and ticker (if public)
- Industry/sector
- Geography focus
- Public or private

### Step 2: Choose Research Scope

- **Quick Overview**: 1-page summary
- **Standard Research**: Comprehensive analysis
- **Deep Dive**: Detailed due diligence
- **Specific Focus**: Choose particular aspects

### Step 3: Specify Use Case

- Investment decision
- Competitive intelligence
- Partnership evaluation
- M&A target assessment
- Market entry analysis

---

## Research Framework

### Business Model Analysis

#### Revenue Model
| Type | Description | Examples |
|------|-------------|----------|
| Subscription | Recurring revenue | SaaS, Media |
| Transaction | Per-transaction fees | Payments, Marketplaces |
| Licensing | IP monetization | Software, Pharma |
| Advertising | Attention monetization | Social media, Search |
| Hardware | Product sales | Apple, Tesla |
| Services | Time/expertise billing | Consulting, Legal |

#### Value Chain Position
```
Upstream → Manufacturing → Distribution → Retail → End User
   ↑              ↑              ↑           ↑
Where does the company operate in the value chain?
```

### Competitive Analysis Framework

#### Porter's Five Forces
1. **Threat of New Entrants**: Barriers to entry, capital requirements
2. **Bargaining Power of Suppliers**: Supplier concentration, switching costs
3. **Bargaining Power of Buyers**: Customer concentration, price sensitivity
4. **Threat of Substitutes**: Alternative solutions, switching costs
5. **Industry Rivalry**: Number of competitors, market growth, differentiation

#### Competitive Positioning Matrix
```
                     High Price
                         │
    Premium              │            Differentiated
    (Apple)              │            (Tesla)
                         │
Low ─────────────────────┼───────────────────── High
Value                    │                      Value
                         │
    Cost Leader          │            Best Value
    (Walmart)            │            (Costco)
                         │
                     Low Price
```

### SWOT Analysis

| Strengths | Weaknesses |
|-----------|------------|
| Internal advantages | Internal limitations |
| Core competencies | Resource gaps |
| Competitive moats | Operational issues |

| Opportunities | Threats |
|---------------|---------|
| Market trends | Competitive risks |
| Growth vectors | Regulatory risks |
| New markets | Technology disruption |

---

## Output Format

```markdown
# Company Research Report: [Company Name]

**Ticker**: [If applicable]
**Sector**: [Industry]
**Headquarters**: [Location]
**Founded**: [Year]
**Employees**: [Number]
**Research Date**: [Date]

---

## Executive Summary

[3-4 sentences summarizing the company, its market position, key strengths, and primary risks]

**Investment/Partnership Suitability**: [Attractive / Neutral / Caution]

---

## Business Overview

### Company Description
[What the company does, history, key milestones]

### Business Model
[How the company makes money]

| Revenue Stream | % of Revenue | Description |
|----------------|--------------|-------------|
| [Stream 1] | XX% | |
| [Stream 2] | XX% | |
| [Stream 3] | XX% | |

### Key Products/Services
1. **[Product 1]**: [Description, market position]
2. **[Product 2]**: [Description, market position]
3. **[Product 3]**: [Description, market position]

---

## Market Analysis

### Industry Overview
[Industry description, size, growth rate, key trends]

### Total Addressable Market (TAM)
| Market | Size | Growth | Source |
|--------|------|--------|--------|
| TAM | $XXB | XX% CAGR | |
| SAM | $XXB | XX% CAGR | |
| SOM | $XXB | XX% CAGR | |

### Key Industry Trends
1. [Trend 1]
2. [Trend 2]
3. [Trend 3]

---

## Competitive Landscape

### Market Position
[Company's position relative to competitors]

### Key Competitors
| Competitor | Market Share | Strengths | Weaknesses |
|------------|--------------|-----------|------------|
| [Comp 1] | XX% | | |
| [Comp 2] | XX% | | |
| [Comp 3] | XX% | | |

### Competitive Advantages (Moats)
- [ ] Brand/Reputation
- [ ] Network Effects
- [ ] Switching Costs
- [ ] Cost Advantages
- [ ] Intangible Assets (IP, Licenses)
- [ ] Efficient Scale

### Porter's Five Forces Assessment
| Force | Intensity | Rationale |
|-------|-----------|-----------|
| New Entrants | Low/Med/High | |
| Supplier Power | Low/Med/High | |
| Buyer Power | Low/Med/High | |
| Substitutes | Low/Med/High | |
| Rivalry | Low/Med/High | |

---

## SWOT Analysis

| **Strengths** | **Weaknesses** |
|---------------|----------------|
| • [S1] | • [W1] |
| • [S2] | • [W2] |
| • [S3] | • [W3] |

| **Opportunities** | **Threats** |
|-------------------|-------------|
| • [O1] | • [T1] |
| • [O2] | • [T2] |
| • [O3] | • [T3] |

---

## Management & Governance

### Leadership Team
| Name | Title | Background | Tenure |
|------|-------|------------|--------|
| | CEO | | |
| | CFO | | |
| | CTO | | |

### Board Composition
[Independent directors, expertise, potential conflicts]

### Corporate Governance
- Insider ownership: XX%
- Institutional ownership: XX%
- Governance concerns: [If any]

---

## Financial Snapshot

| Metric | Value | Trend |
|--------|-------|-------|
| Revenue | $XXM | ↑↓→ |
| Revenue Growth | XX% | |
| Gross Margin | XX% | |
| Operating Margin | XX% | |
| Net Margin | XX% | |
| ROE | XX% | |
| Debt/Equity | X.XX | |

---

## Risk Assessment

### Key Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | |
| [Risk 2] | High/Med/Low | High/Med/Low | |
| [Risk 3] | High/Med/Low | High/Med/Low | |

---

## Conclusion & Recommendations

### Summary Assessment
[Overall view on the company]

### Key Takeaways
1. [Takeaway 1]
2. [Takeaway 2]
3. [Takeaway 3]

### Recommended Next Steps
1. [Action 1]
2. [Action 2]

---

## Appendix

### Sources
- Company filings and reports
- Industry reports
- News articles
- Analyst reports (if available)

---

## Disclaimer

This research is based on publicly available information and AI analysis. It should not be considered as investment advice or a recommendation to buy, sell, or hold any securities.
```

---

## Tips for Better Results

1. **Specify the purpose** of your research (investment, partnership, competitive intel)
2. **Provide any known information** to focus the analysis
3. **Ask for specific frameworks** if you prefer particular analysis methods
4. **Request comparison** with specific competitors
5. **Indicate depth level** needed (quick scan vs deep dive)

---

## Limitations

- Cannot access real-time data or proprietary databases
- Analysis based on publicly available information
- Cannot conduct primary research or interviews
- May not reflect most recent developments
- Does not replace professional due diligence

---

*Built by the Claude Office Skills community. Contributions welcome!*
