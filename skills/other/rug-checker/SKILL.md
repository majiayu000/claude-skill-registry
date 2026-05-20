---
name: rug-checker
description: >
  Solana token rug-pull risk analysis. 10-point on-chain check with visual report.
  Zero API keys. Read-only. Not financial advice.
version: 0.1.4
author: Anvil AI
tags: [security, crypto, solana, defi, rug-pull, discord, discord-v2]
permissions:
  - network
---

# Rug Checker — Agent Skill Definition

## Skill Metadata

| Field | Value |
|-------|-------|
| **Slug** | `rug-checker` |
| **Version** | `0.1.3` |
| **Author** | Anvil AI |
| **Category** | DeFi / Security |
| **Chain** | Solana |
| **Risk Level** | Read-only (no wallet interactions) |

## Activation Triggers

Activate this skill when the user's message matches any of these patterns:

| Pattern | Example |
|---------|---------|
| Rug check / rug pull check | "Do a rug check on BONK" |
| Token safety | "Is this token safe?" |
| Scam check | "Is this a scam?" |
| Token risk analysis | "What's the risk on this token?" |
| Honeypot check | "Is this a honeypot?" |
| Token audit | "Audit this token" |
| LP locked | "Is the LP locked on this?" |
| Mint authority | "Can they mint more tokens?" |
| Token lookup + Solana address | "What is DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263?" |

> **Note:** If the user asks "Should I buy [token]?", redirect: *"I can't advise on whether to buy — but I can check the on-chain risk factors for you."* Then run the analysis.

**Address detection:** If the user provides a base58 string of 32-44 characters, treat it as a Solana token address. If they provide a name/symbol, resolve it first.

## Agent Workflow

### Step 1: Extract the Token

Parse the user's message for either:
- A Solana address (base58, 32-44 chars matching `[1-9A-HJ-NP-Za-km-z]{32,44}`)
- A token name or symbol (e.g., "BONK", "bonk", "Wheelchair Fish")

If unclear, ask: *"Which token would you like me to check? Give me the contract address or token name."*

### Step 2: Resolve the Token

```bash
bash scripts/detect-token.sh <address_or_name>
```

**Output varies by input type:**

**If given a Solana address:** JSON with `found: true/false`, `address`, `name`, `symbol`, market data.

**If given a name/symbol:** JSON with `ambiguous: true` and a `candidates` array containing up to 5 matches with address, name, symbol, liquidity, and age. **If detect-token returns candidates, you MUST present them to the user and ask which one they mean. NEVER auto-pick a candidate.** Checking the wrong token is worse than not checking at all.

Example candidate response:
```json
{
  "query": "bonk",
  "ambiguous": true,
  "candidates": [
    {"address": "DezXAZ8z...", "name": "Bonk", "symbol": "BONK", "liquidity_usd": 5000000, "age": "400d"},
    {"address": "56Lc5...", "name": "BonkFork", "symbol": "BONK", "liquidity_usd": 12000, "age": "3d"}
  ]
}
```

Present candidates as a numbered list:
> I found multiple tokens matching "bonk". Which one did you mean?
> 1. **BONK** (Bonk) — `DezXAZ8z...` — $5.0M liquidity, 400d old
> 2. **BONK** (BonkFork) — `56Lc5...` — $12K liquidity, 3d old

Then re-run with the confirmed mint address.

If `found: false` (and not `ambiguous`), tell the user the token couldn't be found and ask them to double-check the address.

### Step 3: Run Risk Analysis

```bash
bash scripts/analyze-risk.sh <token_address>
```

**Output:** JSON with 10 risk checks, composite score (0-100), tier (SAFE/CAUTION/WARNING/DANGER/CRITICAL).

### Step 4: Generate Report

```bash
bash scripts/analyze-risk.sh <address> | bash scripts/format-report.sh
```

Or pipe the saved JSON:

```bash
bash scripts/format-report.sh < analysis.json
```

**Output:** Formatted Markdown report card with visual risk bars, market overview, and links.

### Step 5: Present to User

Display the formatted report. Add brief commentary based on the tier:

| Tier | Commentary Template |
|------|-------------------|
| 🟢 SAFE (0-15) | "Low on-chain risk indicators detected. Note: this only covers on-chain factors — team, legal, and market risks are not assessed." |
| 🟡 CAUTION (16-35) | "Some yellow flags here. Not necessarily a scam, but proceed with caution and do your own research." |
| 🟠 WARNING (36-55) | "Several risk factors detected. Be careful with this one." |
| 🔴 DANGER (56-75) | "Significant red flags. This has multiple indicators of a potential rug pull." |
| ⛔ CRITICAL (76-100) | "Extreme risk. This token has critical safety issues. Strongly avoid." |

**Always end with the disclaimer** (it's built into format-report.sh). **Never use language that implies a buy/sell recommendation** (e.g., "looks solid", "good investment", "safe bet").

### Discord v2 Delivery Mode (OpenClaw v2026.2.14+)

When running in a Discord channel:

- Send a compact first message with: token, tier, score, and top 3 risk drivers.
- Keep the first message under ~1200 characters; avoid rendering the full long report first.
- If Discord components are available, include quick actions:
  - `Show Full Risk Breakdown`
  - `Show Data Sources`
  - `Re-Run Check`
- If components are unavailable, provide the same options as a numbered list.
- For long reports, send in short chunks (<=15 lines) to avoid noisy channel spam.

## Error Handling

| Error | Cause | Agent Response |
|-------|-------|---------------|
| Exit code 2 from detect-token | Token not found | "I couldn't find that token. Please check the address — it should be a Solana SPL token mint address (32-44 base58 characters)." |
| Exit code 1 from detect-token | API failure | "I'm having trouble reaching the token APIs right now. Try again in a minute." |
| `composite_score: -1` | All data sources failed | "All three data sources are down right now. I can't safely analyze this token without data." |
| `rugcheck` unavailable | Rugcheck API down | Analysis proceeds with DexScreener + Solana RPC (degraded but functional). Note this in your response. |
| `found: true` but name "Unknown" | Token exists on-chain but has no DEX listings | "This token exists on Solana but doesn't appear to be listed on any DEX. It may be too new or a non-tradeable token." |

## Data Sources

| Source | What It Provides | Required? |
|--------|-----------------|-----------|
| Rugcheck.xyz | Mint/freeze authority, top holders, LP locks, risk flags, insider detection, verification status | Primary (most checks degrade without it) |
| DexScreener | Price, volume, liquidity, FDV, market cap, token age, name resolution | Secondary (market context) |
| Solana RPC | On-chain mint/freeze authority verification | Tertiary (fallback verification) |

## Risk Checks (10 points)

| # | Check | Weight | What It Detects |
|---|-------|--------|----------------|
| 1 | Mint Authority | 2.0 | Can creator mint unlimited tokens? |
| 2 | Freeze Authority | 1.5 | Can creator freeze holder wallets? |
| 3 | Holder Concentration | 1.5 | Are tokens concentrated in few wallets? |
| 4 | LP Lock Status | 2.0 | Can liquidity be pulled? (classic rug) |
| 5 | Token Age | 1.0 | How old is the token? |
| 6 | Liquidity Depth | 1.0 | Is there enough liquidity to trade? |
| 7 | Rugcheck Flags | 1.0 | Rugcheck.xyz automated risk flags |
| 8 | Insider Activity | 1.5 | Coordinated wallet networks detected? |
| 9 | Transfer Fee | 1.0 | Hidden tax on transfers? |
| 10 | Verification | 0.5 | Listed on Jupiter? |

## Safety

### ⚠️ NOT Financial Advice — This Is Non-Negotiable

This skill provides **informational risk signals only**. The agent MUST NOT:
- Recommend buying or selling any token — ever
- Use language implying a token is a "good buy", "looks solid", or is "safe to invest in"
- Frame analysis results as investment validation
- Guarantee any token is safe or unsafe
- Replace professional financial advice
- Account for off-chain risks (team, legal, regulatory, market sentiment)

A low risk score means **low on-chain risk indicators were detected** — it does NOT mean the token is a good investment or free from risk.

### 🔒 Read-Only

This skill:
- **Never** interacts with any wallet
- **Never** signs or submits any transaction
- **Never** requests private keys or seed phrases
- **Never** sends tokens or funds
- Only reads publicly available on-chain data and public API endpoints

### 🛡️ No API Keys

All data sources are free, public APIs. No API keys are stored or transmitted.

## Example Prompts

```
"Rug check DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
"Is BONK safe?"
"Check this token for me: 5smiafTeV4ATT6naUWTwzcsvix4VU9nQ7ReyzKiqpump"
"Is this a rug pull? [address]"
"Analyze the risk on this Solana token"
"Do a safety check on $WIF"
```

## Dependencies

- `bash` 4+
- `curl`
- `jq`
- `bc` (for floating-point comparisons)
- Internet access to: `api.rugcheck.xyz`, `api.dexscreener.com`, `api.mainnet-beta.solana.com`
