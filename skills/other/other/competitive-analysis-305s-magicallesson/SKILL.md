---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Competitive Analysis
# ═══════════════════════════════════════════════════════════════════════════════

name: competitive-analysis
description: "Analyze competitors systematically. Compare products, features, pricing, positioning, and market strategies. Generate comprehensive competitive intelligence reports."
version: "1.0.0"
author: claude-office-skills
license: MIT

category: research
tags:
  - competitive
  - analysis
  - market
  - strategy
  - benchmarking
department: Strategy/Marketing

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
  - competitor_profiling
  - feature_comparison
  - pricing_analysis
  - positioning_mapping
  - swot_analysis

languages:
  - en
  - zh

related_skills:
  - company-research
  - deep-research
  - proposal-writer
---

# Competitive Analysis Skill

## Overview

I help you systematically analyze competitors to inform strategic decisions. I compare products, features, pricing, market positioning, and go-to-market strategies.

**What I can do:**
- Build competitor profiles
- Create feature comparison matrices
- Analyze pricing strategies
- Map market positioning
- Identify competitive advantages
- Generate strategic recommendations

**What I cannot do:**
- Access competitor internal data
- Provide real-time pricing updates
- Monitor competitor activity continuously
- Access proprietary market research

---

## How to Use Me

### Step 1: Define the Scope

Tell me:
- Your company/product (for context)
- Competitors to analyze (or ask me to identify them)
- Industry/market segment
- Geographic scope
- Specific aspects to focus on

### Step 2: Choose Analysis Type

- **Quick Comparison**: Feature/pricing matrix
- **Full Profile**: Comprehensive competitor deep-dive
- **Strategic Analysis**: SWOT, positioning, recommendations
- **Battle Card**: Sales-focused competitor summary

### Step 3: Specify Output

- Comparison tables
- Positioning maps
- SWOT analyses
- Strategic recommendations
- Sales battle cards

---

## Analysis Frameworks

### Porter's Competitor Analysis

```
┌─────────────────────────────────────────────────────────────┐
│                  Competitor Analysis                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Future Goals         2. Current Strategy                │
│     - What drives            - How they compete             │
│       the competitor?        - What are they doing?         │
│                                                              │
│  3. Assumptions          4. Capabilities                    │
│     - About themselves       - Strengths                    │
│     - About the industry     - Weaknesses                   │
│                                                              │
│             ↓ Combined = Competitor Response Profile ↓       │
│                                                              │
│  - What will competitor do?                                  │
│  - Where is competitor vulnerable?                           │
│  - What will provoke the greatest retaliation?              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Competitive Positioning Matrix

```
                    Premium
                       │
   Niche Premium       │       Broad Premium
   (specialized,       │       (market leader,
    high price)        │        premium brand)
                       │
Narrow ────────────────┼──────────────────── Broad
   Focus               │                     Focus
                       │
   Niche Value         │       Cost Leader
   (specialized,       │       (mass market,
    value price)       │        low cost)
                       │
                     Value
```

### Feature Comparison Matrix

| Feature | You | Comp A | Comp B | Comp C | Importance |
|---------|-----|--------|--------|--------|------------|
| Feature 1 | ✅ | ✅ | ❌ | ⚠️ | High |
| Feature 2 | ✅ | ❌ | ✅ | ✅ | Medium |
| Feature 3 | ❌ | ✅ | ✅ | ❌ | Low |

Legend: ✅ Strong | ⚠️ Partial | ❌ Absent

---

## Output Format

```markdown
# Competitive Analysis Report: [Market/Product]

**Analysis Date**: [Date]
**Prepared for**: [Company/Team]
**Competitors Analyzed**: [Number]

---

## Executive Summary

[3-4 sentences summarizing key competitive findings and strategic implications]

**Key Takeaways**:
1. [Takeaway 1]
2. [Takeaway 2]
3. [Takeaway 3]

---

## Market Overview

### Market Definition
[Define the market being analyzed]

### Market Size & Growth
| Metric | Value | Source |
|--------|-------|--------|
| Market Size | $[X]B | |
| Growth Rate | [X]% CAGR | |
| Key Trends | | |

### Competitive Landscape Overview
[Description of competitive dynamics]

---

## Competitor Profiles

### Competitor 1: [Name]

#### Company Overview
| Attribute | Details |
|-----------|---------|
| Founded | |
| Headquarters | |
| Employees | |
| Funding/Revenue | |
| Target Market | |

#### Product/Service Overview
[Description of main offerings]

#### Strengths
- [Strength 1]
- [Strength 2]
- [Strength 3]

#### Weaknesses
- [Weakness 1]
- [Weakness 2]
- [Weakness 3]

#### Strategy
[How they compete, go-to-market approach]

---

### Competitor 2: [Name]
[Same structure...]

---

### Competitor 3: [Name]
[Same structure...]

---

## Feature Comparison

| Feature/Capability | [You] | [Comp 1] | [Comp 2] | [Comp 3] |
|-------------------|-------|----------|----------|----------|
| [Feature 1] | | | | |
| [Feature 2] | | | | |
| [Feature 3] | | | | |
| [Feature 4] | | | | |
| [Feature 5] | | | | |

### Feature Analysis
[Key observations from feature comparison]

---

## Pricing Comparison

| Tier/Plan | [You] | [Comp 1] | [Comp 2] | [Comp 3] |
|-----------|-------|----------|----------|----------|
| Entry/Free | | | | |
| Mid-tier | | | | |
| Enterprise | | | | |

### Pricing Insights
[Key observations about pricing strategies]

---

## Positioning Map

[Description of how competitors are positioned]

```
                 High Price
                     │
    [Comp A]         │         [Your Company]
                     │
Low ─────────────────┼───────────────────── High
Innovation           │                      Innovation
                     │
    [Comp C]         │         [Comp B]
                     │
                 Low Price
```

---

## SWOT Summary

### Your Competitive Position

| Strengths | Weaknesses |
|-----------|------------|
| | |

| Opportunities | Threats |
|---------------|---------|
| | |

---

## Competitive Advantages

### Your Advantages Over Competitors
1. **vs [Comp 1]**: [Advantage]
2. **vs [Comp 2]**: [Advantage]
3. **vs [Comp 3]**: [Advantage]

### Areas Where Competitors Excel
1. **[Comp 1]**: [Their advantage]
2. **[Comp 2]**: [Their advantage]
3. **[Comp 3]**: [Their advantage]

---

## Strategic Recommendations

### Immediate Actions
1. [Action 1]
2. [Action 2]
3. [Action 3]

### Medium-term Strategy
1. [Strategy 1]
2. [Strategy 2]

### Competitive Responses to Watch
1. [Potential competitor move]
2. [Potential competitor move]

---

## Battle Cards

### vs [Competitor 1]

**When They Come Up**: [Typical scenarios]

**Their Pitch**: [How they position against you]

**Our Response**: [Counter-positioning]

**Key Differentiators**:
- We have / They don't: [Feature]
- They have / We don't: [Feature]

**Win Themes**: [What helps us win]

**Objection Handling**:
- "[Objection 1]" → [Response]
- "[Objection 2]" → [Response]

---

## Appendix

### Data Sources
- Company websites
- Product documentation
- News and press releases
- Industry reports
- Review sites

### Methodology
[How the analysis was conducted]

---

*Competitive intelligence is time-sensitive. Verify key data points before strategic decisions.*
```

---

## Tips for Better Results

1. **Provide your company context** for relevant comparison
2. **Name specific competitors** or describe the criteria to identify them
3. **Specify focus areas** (features, pricing, positioning, etc.)
4. **Share any known information** about competitors
5. **Indicate the purpose** (strategic planning, sales enablement, etc.)
6. **Request battle cards** for sales teams

---

## Limitations

- Cannot access competitors' internal data
- Cannot provide real-time information
- Analysis based on publicly available information
- Cannot monitor competitor activity continuously
- May not reflect most recent changes

---

*Built by the Claude Office Skills community. Contributions welcome!*
