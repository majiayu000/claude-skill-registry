---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Crypto Report
# ═══════════════════════════════════════════════════════════════════════════════

name: crypto-report
description: "Analyze cryptocurrency projects with tokenomics, on-chain metrics, and market analysis. Generate comprehensive crypto research reports."
version: "1.0.0"
author: claude-office-skills
license: MIT

category: finance
tags:
  - crypto
  - blockchain
  - tokenomics
  - defi
  - research
department: Finance/Crypto

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
  - tokenomics_analysis
  - on_chain_metrics
  - protocol_research
  - market_analysis
  - risk_assessment

languages:
  - en
  - zh

related_skills:
  - stock-analysis
  - company-research
  - investment-memo
---

# Crypto Report Skill

## Overview

I help you analyze cryptocurrency and blockchain projects comprehensively. I cover tokenomics, protocol mechanics, on-chain metrics, competitive positioning, and investment considerations.

**What I can do:**
- Tokenomics analysis (supply, distribution, vesting)
- Protocol/technology assessment
- On-chain metrics interpretation
- Market and competitive analysis
- Risk factor identification
- Investment thesis development

**What I cannot do:**
- Access real-time prices or on-chain data
- Predict price movements
- Provide investment advice
- Audit smart contracts

---

## How to Use Me

### Step 1: Specify the Project

Tell me:
- Token/project name and ticker
- Blockchain network
- Project category (L1, L2, DeFi, NFT, etc.)
- Any specific metrics you have

### Step 2: Choose Analysis Scope

- **Quick Overview**: Token summary and key metrics
- **Deep Dive**: Comprehensive protocol analysis
- **Tokenomics Focus**: Supply and distribution analysis
- **Technical Review**: Protocol mechanics and security

### Step 3: Provide Context (Optional)

- On-chain data (TVL, transactions, users)
- Token holder distribution
- Recent developments or news

---

## Analysis Framework

### Project Categories

| Category | Examples | Key Metrics |
|----------|----------|-------------|
| Layer 1 | ETH, SOL, AVAX | TPS, TVL, Developer Activity |
| Layer 2 | ARB, OP, MATIC | TVL, Transactions, Fee Savings |
| DeFi | UNI, AAVE, MKR | TVL, Volume, Revenue |
| Infrastructure | LINK, GRT, FIL | Usage, Integrations, Revenue |
| Gaming/NFT | AXS, SAND, IMX | Users, Transactions, Volume |
| Stablecoins | USDC, DAI, FRAX | Market Cap, Peg Stability |

### Tokenomics Analysis

#### Supply Metrics
```
Max Supply: Total tokens that will ever exist
Total Supply: Tokens minted to date
Circulating Supply: Tokens available in market
Inflation Rate: Annual supply increase
```

#### Distribution Assessment
| Holder Type | Typical Range | Concern Level |
|-------------|---------------|---------------|
| Team | 10-20% | >25% concerning |
| Investors | 15-25% | >30% concerning |
| Treasury | 10-20% | Depends on governance |
| Community | 40-60% | Higher is better |
| Ecosystem | 10-20% | For incentives |

#### Vesting Analysis
- Cliff periods
- Linear vs milestone vesting
- Unlock schedule impact

### On-Chain Metrics

| Metric | Description | What It Tells You |
|--------|-------------|-------------------|
| TVL | Total Value Locked | Protocol adoption |
| Active Users | Daily/Monthly active wallets | Real usage |
| Transaction Count | On-chain transactions | Activity level |
| Gas Fees | Transaction costs | Demand for blockspace |
| Developer Commits | GitHub activity | Development momentum |
| Token Velocity | Turnover rate | Holding behavior |

### Valuation Approaches

#### Relative Valuation
- Market Cap / TVL
- FDV / Revenue (annualized)
- P/S Ratio (Protocol Revenue)
- Comparison to peers

#### Token Value Accrual
- Fee distribution
- Buyback and burn
- Staking rewards
- Governance rights

---

## Output Format

```markdown
# Crypto Research Report: [Token Name] ([TICKER])

**Network**: [Blockchain]
**Category**: [L1/L2/DeFi/etc.]
**Research Date**: [Date]
**Price at Analysis**: $[X.XX]

---

## Executive Summary

[2-3 sentence overview of the project and investment thesis]

**Rating**: [Bullish / Neutral / Bearish]
**Risk Level**: [Low / Medium / High / Very High]

---

## Key Metrics at a Glance

| Metric | Value | Notes |
|--------|-------|-------|
| Price | $[X.XX] | |
| Market Cap | $[X]M/B | |
| FDV | $[X]M/B | |
| Circulating Supply | [X]M | [X]% of max |
| Max Supply | [X]M | |
| TVL | $[X]M/B | |
| 24h Volume | $[X]M | |
| Rank | #[X] | By market cap |

---

## 1. Project Overview

### What It Does
[Clear explanation of what the project does]

### Problem & Solution
**Problem**: [What problem does it solve?]
**Solution**: [How does the protocol address it?]

### Technology Stack
- Blockchain: [Network]
- Consensus: [Mechanism]
- Smart Contracts: [Language/Platform]
- Key Innovations: [Technical differentiators]

### Team
| Name | Role | Background |
|------|------|------------|
| | Founder | |
| | CTO | |

**Team Assessment**: [Anonymous? Doxxed? Track record?]

### Roadmap
| Phase | Timeline | Milestones |
|-------|----------|------------|
| Completed | | |
| Current | | |
| Upcoming | | |

---

## 2. Tokenomics

### Token Utility
- [ ] Governance voting
- [ ] Fee payments
- [ ] Staking rewards
- [ ] Collateral
- [ ] Access/Membership
- [ ] [Other utility]

### Supply Dynamics
```
Max Supply:         [X] tokens
Total Supply:       [X] tokens ([X]% of max)
Circulating Supply: [X] tokens ([X]% of total)
Inflation Rate:     [X]% annually
```

### Distribution
| Allocation | % | Tokens | Vesting |
|------------|---|--------|---------|
| Team | | | |
| Investors | | | |
| Treasury | | | |
| Community | | | |
| Ecosystem | | | |

### Vesting Schedule
[Chart or description of unlock schedule]

**Upcoming Unlocks**:
| Date | Amount | % of Circ | Impact |
|------|--------|-----------|--------|
| | | | |

### Value Accrual
[How does the token capture value?]
- Fee mechanism: [Description]
- Burn mechanism: [Description]
- Staking: [APY and lock-up]

---

## 3. On-Chain Analysis

### Activity Metrics
| Metric | Current | 30d Trend | 90d Trend |
|--------|---------|-----------|-----------|
| Daily Active Users | | | |
| Daily Transactions | | | |
| TVL | | | |
| Protocol Revenue | | | |

### Holder Analysis
| Category | Count | % Supply |
|----------|-------|----------|
| Top 10 Holders | | |
| Top 100 Holders | | |
| Exchange Holdings | | |
| Staked Tokens | | |

### Network Health
- Decentralization: [Assessment]
- Security: [Audit status, incidents]
- Uptime: [Historical performance]

---

## 4. Market Analysis

### Competitive Landscape
| Competitor | Market Cap | TVL | Key Differentiator |
|------------|-----------|-----|---------------------|
| [Comp 1] | | | |
| [Comp 2] | | | |
| [Comp 3] | | | |

### Market Position
[Where does this project fit in the ecosystem?]

### Adoption Metrics
- Integrations: [Number and quality]
- Partnerships: [Key partners]
- Developer Ecosystem: [Activity level]

---

## 5. Valuation

### Relative Valuation
| Metric | [TOKEN] | Peer Avg | Assessment |
|--------|---------|----------|------------|
| MC/TVL | | | |
| FDV/Revenue | | | |
| MC/Users | | | |

### Bull Case Valuation
[Assumptions and target price]

### Bear Case Valuation
[Assumptions and target price]

---

## 6. Risk Analysis

### Key Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Smart Contract Risk | | | Audits: [Status] |
| Regulatory Risk | | | |
| Competition | | | |
| Team Risk | | | |
| Tokenomics Risk | | | |
| Market Risk | | | |

### Red Flags
- [ ] Anonymous team
- [ ] Unaudited contracts
- [ ] High team allocation
- [ ] No real utility
- [ ] Concentrated holdings
- [ ] [Other flags]

---

## 7. Investment Thesis

### Bull Case
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

### Bear Case
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

### Catalysts
| Catalyst | Timeline | Impact |
|----------|----------|--------|
| | | |

---

## Conclusion

### Summary
[Overall assessment in 2-3 sentences]

### Rating
**[Bullish / Neutral / Bearish]** with **[High/Medium/Low]** conviction

### Key Watchpoints
1. [What to monitor]
2. [What to monitor]
3. [What to monitor]

---

## Disclaimer

This report is for informational purposes only and does not constitute financial advice. Cryptocurrency investments are highly speculative and risky. Do your own research (DYOR) before making any investment decisions.

---

## Sources
- [Official documentation]
- [Block explorer]
- [Analytics platforms]
```

---

## Tips for Better Results

1. **Provide on-chain data** if you have access (TVL, users, etc.)
2. **Specify your investment horizon** (trading vs long-term holding)
3. **Mention specific concerns** you want addressed
4. **Include recent news** that might be relevant
5. **Ask for comparisons** with specific competitors

---

## Limitations

- Cannot access real-time prices or on-chain data
- Cannot audit smart contracts
- Analysis based on publicly available information
- Crypto markets are highly volatile and unpredictable
- Not financial or investment advice

---

*Built by the Claude Office Skills community. Contributions welcome!*
