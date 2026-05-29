---
name: pubfi-wallet-portfolio-analysis
description: Analyze EVM wallet asset distribution and identify high-risk protocol exposure.
---

# Wallet Portfolio Analysis

> **Goal**: Provide concise asset distribution analysis and risk assessment for EVM wallets.
>

## Inputs

- `wallet_address` (required): EVM address (0x...)

## Data Source

**Primary**: Zerion API via `zerion-portfolio.py`

```bash
# Get all assets
python3 zerion-portfolio.py <address>

# Get only DeFi positions
python3 zerion-portfolio.py <address> --only-defi
```

**Environment**: `ZERION_API_KEY` must be set. If not set, get your API key at: https://www.zerion.io/api

## Execution Workflow

### Step 1: Validate Input
```yaml
1. Check address format: 0x + 40 hex characters
2. If invalid format: Exit with error message
```

### Step 2: Fetch Portfolio Data
```bash
# Execute Zerion portfolio script
python3 skills/pubfi-wallet-portfolio-analysis/zerion-portfolio.py <address>
```

**Handle Edge Cases:**
- Empty wallet → Report "Empty wallet"
- API failure → Exit with error, cannot proceed
- Zero-value positions → Skip

### Step 3: Categorize Assets
```yaml
Group by type:
  Native: ETH, MATIC, BNB, etc.
  Stablecoins: USDC, USDT, DAI, USDS
  DeFi Positions: Has protocol attribute + position_type != 'wallet'
  Other Tokens: Everything else

Track total value per category for distribution percentages
```

### Step 4: Identify DeFi Protocols
```yaml
For each DeFi position:
  1. Extract protocol name from attributes.protocol
  2. Identify position type (Lending/Staking/LP/etc.)
  3. Record position value and percentage of portfolio
  4. Create list of unique protocols for risk assessment
```

### Step 5: Risk Assessment (DeFi Protocols Only)
```yaml
For each identified protocol:
  
  A. Fetch Protocol Data (parallel):
     - DefiLlama API: curl "https://api.llama.fi/protocol/{slug}"
     - Extract TVL, chains, audit info, category
  
  B. Check Recent Exploits:
     - Search rekt.news for protocol name
     - Filter last 90 days
     - Record any incidents
  
  C. Calculate Risk Score:
     Risk = Base + Events + Audit + TVL Trend
     
     Factors:
     - No audit: +5
     - Recent exploit (90 days): +5
     - TVL drop >50% (30 days): +3
     - TVL drop 20-50%: +2
     - New protocol (<6 months): +2
     - Single audit: +1
     - Multiple audits: -2
     - Battle-tested (>1 year): -1
  
  D. Assign Risk Level:
     - Score > 7: 🔴 High Risk
     - Score 4-7: 🟡 Medium Risk
     - Score < 4: 🟢 Low Risk
  
  E. Error Handling:
     - DefiLlama fails: Mark TVL as "N/A", continue
     - Rekt.news unavailable: Mark exploits as "Unknown"

Known Safe Protocols (auto 🟢):
  - Aave V2/V3, Uniswap V2/V3, Compound V2/V3
  - Lido, Curve, MakerDAO/Sky
```

### Step 6: Generate Report

Output structured markdown report following the Output Format section below.

---

## Output Format

### 1) Summary

```
Portfolio: 0x...
Total Value: $X,XXX USD
Chains: Ethereum, Arbitrum, Base
```

### 2) Asset Distribution

```
Asset Breakdown:
• Native: $XXX (XX%)
• Stablecoins: $XXX (XX%)
• DeFi Positions: $XXX (XX%)
• Other Tokens: $XXX (XX%)
```

### 3) Top Positions

Table format showing all positions sorted by value:
```
Protocol/Wallet | Position Type | Value | % Portfolio
----------------|---------------|-------|------------
Wallet Assets   | Wallet        | $XXX  | XX%
Protocol A      | Lending       | $XXX  | XX%
Protocol B      | LP            | $XXX  | XX%
```

### 4) Top Holdings (>2% of portfolio)

Table format:
```
Chain | Asset | Type | Amount | Value | % Portfolio
------|-------|------|--------|-------|------------
```

### 5) DeFi Exposure

For each protocol with 🟡 Medium or 🔴 High risk only (skip 🟢 Low risk):

```
Protocol Name (Chain)
• Position Value: $XXX (XX% of portfolio)
• Position Type: Lending/Staking/LP/etc.
• Risk: 🟡/🔴
• TVL: $XXX (DefiLlama)
• Audit: Yes/No (auditor names)
• Recent Issues: None / [describe]
```

If all protocols are low risk, output: "All DeFi positions are in low-risk protocols (🟢)"

### 6) Risk Summary

**High Priority**:
- List any 🔴 high-risk positions with recommended actions

**Medium Priority**:
- List any 🟡 medium-risk positions with considerations

**Overall Assessment**:
- One paragraph summary
- Risk score: Low/Medium/High

### 7) Data Sources

- Zerion API: Portfolio data (timestamp)
- DefiLlama: Protocol TVL and info
- Rekt.news: Security incidents
- [Other sources used]

---

## Quality Standards

**Conciseness**:
- Total report: 200-400 words (excluding tables)
- Focus on actionable insights only
- No filler or generic statements

**Accuracy**:
- All data must have timestamps
- All values must come from real API calls
- Risk assessments must cite specific evidence

**Usefulness**:
- Highlight positions >5% of portfolio
- Flag any high-risk exposure immediately
- Provide clear next actions if needed

---

## Update Frequency

- **Risk database**: Update monthly with rekt.news
- **Known protocols**: Update as new major protocols launch  
- **Audit status**: Verify quarterly

Last updated: 2026-02-05
