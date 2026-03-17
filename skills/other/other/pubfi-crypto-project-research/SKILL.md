---
name: pubfi-crypto-project-research
description: Generate professional, evidence-backed research reports for crypto projects.
---

# Crypto Project Research (Professional)

> **Goal**: Produce a decision-grade, evidence-backed research report for a crypto project.
>
> **Non-negotiable**: No mock, simulated, guessed, or placeholder numbers in the final report.

## Inputs

- `project_name` (required): e.g., "Aave", "Uniswap", "EigenLayer"
- `special_requirements` (optional): free-text constraints such as
  - analysis focus (e.g., “security-first”, “tokenomics deep dive”)
  - scope (chains / products / time range)
  - competitor set to include/exclude
  - output preferences (language, length, investor vs developer angle)

All other identifiers (CoinGecko id, DefiLlama slug), project type, and module selection must be inferred automatically.

### Example Inputs

- `Aave`
- `Uniswap | focus: fee switch + governance risks; competitors: Sushi, Curve; output: Chinese`

## Rules (Data Integrity)

- **Every key metric must have a source link** (API URL, dashboard link, or official doc) in the **Sources** section.
- Use **UTC** timestamps. Include **Data Retrieved At** (ISO 8601) for each external API pull.
- Prefer primary/official sources first; use third-party aggregators (CoinGecko/DefiLlama) as the default for market + DeFi fundamentals.
- When there is conflicting data across sources:
  - Present both values with sources
  - Explain plausible reasons (methodology differences)
  - Avoid “picking” one silently

---

## Framework

Your report must always include these dimensions (in this order):

1. **Project Overview**
2. **Market & Positioning**
3. **Product & Business Model**
4. **Security & Risk**
5. **On-chain & Fundamental Metrics**
6. **Recent Updates**

---

## Modules (Optional, Configurable)

Pick modules based on inferred project type and the user’s `special_requirements`.

### Module List

- `Tokenomics & Supply`: supply, emissions, utility, sinks/sources
- `Unlocks & Distribution`: vesting/unlock schedule, concentration, insiders
- `Governance`: DAO structure, voting power, proposals cadence
- `Architecture & Dependencies`: core components, key dependencies, upgradeability
- `Liquidity & Market Structure`: exchange liquidity, depth, slippage, CEX/DEX split
- `Regulatory/Compliance`: jurisdiction, KYC/AML exposure, enforcement risks
- `Ecosystem & Integrations`: partners, composability, distribution channels
- `Stablecoin Mechanics` (if stablecoin): peg design, collateral, liquidation, reflexivity
- `Bridge Risk` (if bridge): trust assumptions, validation set, historical incidents
- `Derivatives Risk` (if derivatives): oracle design, liquidation engine, insurance fund
- `RWA Risk` (if RWA): custodians, legal structure, off-chain settlement

### Default Module Selection by Type

- `defi`: Tokenomics & Supply, Governance, Architecture & Dependencies, Liquidity & Market Structure
- `l1/l2`: Architecture & Dependencies, Ecosystem & Integrations, Tokenomics & Supply
- `stablecoin`: Stablecoin Mechanics, Tokenomics & Supply (if applicable), Regulatory/Compliance
- `bridge`: Bridge Risk, Architecture & Dependencies
- `derivatives`: Derivatives Risk, Architecture & Dependencies, Liquidity & Market Structure
- `restaking`: Architecture & Dependencies, Security & Risk, Tokenomics & Supply
- `cefi`: Regulatory/Compliance, Business Model, Proof-of-Reserves (if available)
- `meme/nft/gamefi`: Liquidity & Market Structure, Tokenomics & Supply, Community

---

## Data Sources Strategy (Reliable First)

### Priority Order

1. **Official / Primary**
   - Project docs, blog, governance forum, GitHub, audits, official dashboards
2. **Battle-tested Aggregators (Preferred Defaults)**
   - **CoinGecko** (prices, market cap, supply, exchange data)
   - **DefiLlama** (TVL, fees, revenue, protocol overview)
3. **Specialized (Use when needed; cite clearly)**
   - Etherscan / Basescan / Arbiscan (contracts, admin, proxy, holders)
   - Dune / Flipside dashboards (methodology-dependent)
   - Token unlock providers (only if they publish sources/methodology)

### CoinGecko API (Market Data)

Base URL: `https://api.coingecko.com/api/v3`

Recommended endpoints (use real calls, record retrieval time):

- Resolve ID (if needed):
  - `GET /coins/list`
- Project snapshot:
  - `GET /coins/{id}`
- Simple price:
  - `GET /simple/price?ids={id}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true`
- Historical chart (optional, for context):
  - `GET /coins/{id}/market_chart?vs_currency=usd&days=30`

Must extract (if available):
- Price (USD), 24h change, 24h volume
- Market cap, FDV
- Circulating supply, total/max supply
- Top exchanges / liquidity indicators (if provided)

### DefiLlama API (Fundamentals)

Base URL: `https://api.llama.fi`

Recommended endpoints (use real calls, record retrieval time):

- Resolve protocol slug (if needed):
  - `GET /protocols`
- Protocol overview (TVL + chains + basic info):
  - `GET /protocol/{slug}`
- Fees (and Revenue if provided as a breakdown label):
  - `GET /summary/fees/{slug}`

- Unlocks / Emissions (optional; use when you need transparent token emission schedules):
  - `GET /api/emissions`
  - `GET /api/emission/{protocol}`

Notes:
- DefiLlama’s `GET /summary/fees/{protocol}` endpoint is the canonical free endpoint for fees.
- Some protocols include a label breakdown (e.g. `Revenue`, `SupplySideRevenue`, etc.) inside the response (fields like `totalDataChartBreakdown`). If the response does **not** provide a revenue label/breakdown, then **Revenue must be `N/A`** (do not infer it).

Must extract (when available):
- TVL (current + 7d/30d trend if provided)
- TVL by chain
- Fees (24h/7d/30d as available) and Revenue (only if explicitly present in the response breakdown, with timeframe definitions)

### Source Link Requirements

For the final report, include:
- API URLs used (CoinGecko + DefiLlama)
- Official docs link
- Audit report links (if any)
- Contract explorer links for critical contracts (if applicable)

---

## Execution Workflow

### Step 0: Identify Project + IDs

Infer identifiers automatically:

- Determine CoinGecko `id`:
  - Prefer an exact match for `project_name`
  - Else use CoinGecko `GET /coins/list` to map `project_name` → `id`
- Determine DefiLlama protocol `slug`:
  - Prefer an exact match for `project_name`
  - Else use DefiLlama `GET /protocols` to map `project_name` → `slug`

Infer `project_type` from:
- DefiLlama category/tags/chains (when available)
- CoinGecko categories/tags (when available)
- Official docs (when needed)

Then select modules:
- Start from the default module set for the inferred type
- Apply `special_requirements` (add/remove modules, competitors, and depth)

If ID/slug cannot be confidently matched:
- Do not guess
- Ask for clarification (preferred) OR proceed with partial report and mark missing sections as `N/A`

### Step 1: Pull Data (Real-Time)

- Pull CoinGecko snapshot + simple price
- Pull DefiLlama protocol overview + fees/revenue (if exists)
- Pull official sources (docs/blog/GitHub/audits)

Record:
- `Data Retrieved At (UTC)` per source

### Step 2: Normalize & Validate

- Normalize currencies to **USD**
- Note units (TVL in USD, fees in USD)
- Ensure timeframe consistency (24h vs 7d vs 30d)
- If a metric seems anomalous:
  - cross-check with at least one secondary source
  - explain discrepancy in the report

### Step 3: Write Report (Professional Format)

Follow the output structure below exactly.

---

## Output Format (Professional Report)

The final answer must be a **single Markdown report** with the following structure.

### 1) Title

`# {Project Name} Research Report`

Include:
- `Report Date (UTC): YYYY-MM-DD`

### 2) TL;DR

- **Conclusion**: 3–6 bullets, action-oriented
- **Risk Lights**:
  - `Security`: Green/Yellow/Red
  - `Tokenomics/Unlocks`: Green/Yellow/Red
  - `Market/Liquidity`: Green/Yellow/Red
  - `Governance/Admin`: Green/Yellow/Red
  - `Regulatory` (if relevant): Green/Yellow/Red

### 3) One-liner

`{Project} is ... (one sentence, plain language, non-marketing)`

### 4) Key Data Panel

A table with **only real data** (or `N/A`). Each row must be traceable to sources.

| Metric | Value | As of (UTC) | Source |
|---|---:|---|---|
| Price (USD) |  |  |  |
| Market Cap |  |  |  |
| FDV |  |  |  |
| 24h Volume |  |  |  |
| Circulating / Total / Max Supply |  |  |  |
| TVL (USD) |  |  |  |
| TVL by Chain |  |  |  |
| Fees (7d / 30d) |  |  |  |
| Revenue (7d / 30d) |  |  |  |
| Audits |  |  |  |
| Admin / Upgradeability |  |  |  |
| Key Contracts |  |  |  |
| Major Unlocks (next 30/90d) |  |  |  |

Rules for `Major Unlocks`:
- Only fill this row if you have an explicit unlock/emission schedule source (e.g., DefiLlama emissions endpoints, an unlock provider with methodology, or official vesting docs).

### 5) Deep Dive

Use the fixed framework sections:

#### A. Project Overview
- What it does, who it serves
- Key components

#### B. Market & Positioning
- Target users and category
- Moat and differentiation
- Go-to-market distribution

#### C. Product & Business Model
- Value creation and value capture
- Fee model and who earns what
- Sustainability considerations

#### D. Security & Risk
- Smart contract risk, audits, known incidents
- Admin keys / multisig / timelock
- Oracle, bridge, third-party dependency risks

#### E. On-chain & Fundamental Metrics
- TVL / fees / revenue interpretation
- Growth vs cyclicality
- Quality of TVL (sticky vs mercenary), if evidence exists

#### F. Recent Updates
- Last 30–90 days: releases, governance, partnerships, security events

### 6) Competitive Comparison

- Choose 2–5 close competitors
- Provide a table with comparable metrics (TVL, fees, rev, valuation, key risks)
- Include sources for each competitor metric (can be the same aggregators)

### 7) Risk Checklist

A bulleted checklist. Each item must be evidence-backed.

Examples of categories (don’t include items without evidence):
- Upgradeable contracts with weak controls
- Highly concentrated token supply
- Large unlocks near-term
- Reliance on a single oracle/bridge/custodian
- Unclear revenue model / incentives only

### 8) Community

- Where the community lives (X/Discord/Forum)
- Quality signals: governance participation, developer activity (with links)

### 10) Sources

- Group by type:
  - Official docs
  - CoinGecko API URLs used
  - DefiLlama API URLs used
  - Audits
  - Explorers
  - Dashboards

---

## Quality Bar

- Writing must be factual, non-hype, and decision-oriented.
- No generic filler. Every claim should be tied to evidence or clearly labeled as an open question.
- Use consistent units and timestamps.
