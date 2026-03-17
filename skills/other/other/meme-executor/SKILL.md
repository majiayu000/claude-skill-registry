---
name: meme-executor
description: |
  Solana memecoin trade execution and simulation. Use when you already have a TradePlan (token, side, size, SL/TP, slippage, risk mode) from meme-trader / flow-tracker / degen-savant and want to either simulate or send a swap through a Solana wallet.
tools: Read(pattern:.claude/skills/meme-executor/**), TodoWrite
---

# Meme Executor - Solana Trade Execution Layer

Solana-focused execution skill that turns high‑level trade plans into concrete orders.

## Current Status: Phase 1 (Safe Mode)

| Component | Status | Risk Level |
|-----------|--------|------------|
| `execute-trade.ts` | DRY RUN only | None |
| `auto-trader.ts` | DRY RUN only | None |
| `jupiter-client.ts` | Quote-only | None |
| `wallet-manager.ts` | Read-only | None |
| `position-tracker.ts` | Local tracking | None |

**No real transactions are sent in Phase 1.**

## When to Use

- You already have a **TradePlan** from other agents/skills:
  - `meme-trader` (signals + sizing)
  - `flow-tracker` (liquidity + position sizing)
  - `degen-savant` (narrative / conviction)
  - `contract-surgeon` (rug/safety cleared)
- You want to:
  - Simulate trades and log PnL without sending real transactions
  - Eventually route real orders via a configured Solana wallet + DEX router

## Core Responsibilities

- Parse a structured trade plan (token, side, size %, target size, SL/TP, slippage).
- Apply simple risk checks (max position %, max concurrent positions hooks).
- **DRY‑RUN by default** – log what would be traded and why.
- Provide clear TODO hooks for wiring:
  - Jupiter swap routing
  - Wallet private key / signer configuration
  - Trade log storage (JSONL or database)

## TradePlan Interface

The executor expects a JSON payload matching this shape:

```ts
export interface TradePlan {
  tokenAddress: string;
  symbol?: string;
  chain: 'solana';
  side: 'buy' | 'sell';
  // either percentage of portfolio or absolute amount in SOL
  sizing: {
    mode: 'percent' | 'absolute';
    value: number; // e.g. 2 = 2% or 0.5 = 0.5 SOL
  };
  riskMode: 'degen' | 'moderate' | 'conservative';
  entryLimitPrice?: number; // optional, for limit-style behavior
  maxSlippageBps: number; // e.g. 1000 = 10%
  stopLossPrice?: number;
  takeProfit1?: number;
  takeProfit2?: number;
  notes?: string; // free-form rationale from upstream agents
  dryRun?: boolean; // default true; set false only once wired to real wallet
}
```

## Usage (Simulation First)

From the repo root, a typical simulated execution call will look like:

```bash
npx tsx .claude/skills/meme-executor/scripts/execute-trade.ts \
  --plan-file /path/to/trade-plan.json
```

Where `trade-plan.json` contains a single `TradePlan` object.

## Output Formats

- **Simulation Log (default)** – human-friendly summary:
  - What would be bought/sold
  - Position size and notional exposure
  - SL/TP levels and implied RR
  - Any risk rule violations
- **JSON Log (--json)** – machine-friendly output for chaining into other tools.

## New Phase 1 Components

### Jupiter Client (Quote-Only)

Get swap quotes without executing:

```bash
# Get a quote for swapping SOL to a token
npx tsx .claude/skills/meme-executor/scripts/jupiter-client.ts \
  --quote --input SOL --output <TOKEN_MINT> --amount 0.1

# JSON output
npx tsx .claude/skills/meme-executor/scripts/jupiter-client.ts \
  --quote --input SOL --output BONK --amount 0.5 --json
```

### Wallet Manager (Read-Only)

Check wallet balances without signing:

```bash
# Check balance of any wallet
npx tsx .claude/skills/meme-executor/scripts/wallet-manager.ts \
  --balance --address <WALLET_ADDRESS>

# Use devnet
npx tsx .claude/skills/meme-executor/scripts/wallet-manager.ts \
  --balance --address <WALLET_ADDRESS> --devnet
```

### Position Tracker

Track open positions locally:

```bash
# Add a position (after buy)
npx tsx .claude/skills/meme-executor/scripts/position-tracker.ts \
  --add --token <MINT> --symbol MEME --entry-price 0.001 --amount 1000 \
  --sl 0.0007 --tp 0.002

# List positions
npx tsx .claude/skills/meme-executor/scripts/position-tracker.ts --list

# Check stop-loss/take-profit triggers
npx tsx .claude/skills/meme-executor/scripts/position-tracker.ts \
  --check --prices '{"<MINT>": 0.0015}'

# Close a position
npx tsx .claude/skills/meme-executor/scripts/position-tracker.ts \
  --close --token <MINT> --exit-price 0.002
```

## Phase Roadmap

| Phase | Components | Risk |
|-------|------------|------|
| **1 (Current)** | Quote, balance, tracking | None |
| **2** | Devnet swap execution | Low (fake SOL) |
| **3** | Mainnet paper trading | None (simulated) |
| **4** | Mainnet live (small size) | High |

## Data Quality Validation Layer

<data_validation>
**Pre-Execution Data Requirements:**
All trades (even simulated) require validated data to ensure backtesting fidelity.

```typescript
interface ExecutionDataQuality {
  price_quality: {
    score: number;           // Min 90 for execution
    sources_count: number;   // Min 2
    max_deviation: number;   // Max 5% between sources
    freshness_ms: number;    // Max 30000 (30s)
  };
  liquidity_check: {
    available: number;       // Must support trade size
    slippage_estimate: number;
    depth_ratio: number;     // Our size / available liquidity
  };
  risk_clearance: {
    rug_score: number;       // From meme-trader
    position_approved: boolean; // From risk-portfolio-manager
    kill_switch_status: 'active' | 'paused' | 'halted';
  };
}

interface ValidationResult {
  approved: boolean;
  quality_score: number;
  warnings: string[];
  blockers: string[];
}
```

**Validation Pipeline:**
```
Trade Plan → Price Validation → Liquidity Check → Risk Clearance → Execute/Reject
                 ↓                    ↓                 ↓
            Min 2 sources      Size < 5% pool    No kill switch
            Max 5% deviation   Slippage < limit   Position approved
            Max 30s stale      Depth sufficient   Rug score < 7
```

**Validation Output (included in dry-run):**
```
DATA VALIDATION REPORT
═════════════════════════════════════

PRICE DATA: PASSED (94/100)
├─ Sources: 3/3 (dexscreener, birdeye, jupiter)
├─ Prices: $0.00042 | $0.000418 | $0.000421
├─ Deviation: 0.48% (< 5% threshold)
├─ Freshness: 8 seconds ago
└─ Status: VALID

LIQUIDITY CHECK: PASSED
├─ Available Liquidity: $127,000
├─ Trade Size: $500 (0.39% of pool)
├─ Estimated Slippage: 0.8%
├─ Depth Ratio: HEALTHY
└─ Status: SUFFICIENT

RISK CLEARANCE: PASSED
├─ Rug Score: 4/10 (acceptable)
├─ Position Sizing: APPROVED (2.3% of portfolio)
├─ Kill Switch: ACTIVE
├─ Daily Loss Buffer: $1,260 remaining
└─ Status: CLEARED

OVERALL: APPROVED FOR EXECUTION
Quality Score: 92/100
Warnings: None
Blockers: None
```

**Rejection Scenarios:**
| Condition | Action | Message |
|-----------|--------|---------|
| Price quality < 90 | REJECT | "Insufficient price data quality" |
| Single source only | WARN | "Low confidence - single source" |
| Price deviation > 5% | REJECT | "Price disagreement - investigate" |
| Stale data > 60s | REJECT | "Data too old for execution" |
| Size > 5% of pool | WARN | "High slippage expected" |
| Rug score > 7 | REJECT | "Token failed safety check" |
| Kill switch halted | REJECT | "Trading halted - risk limit" |
</data_validation>

## Real-Time Data Integration

<real_time_data>
**Data Sources for Execution:**
```typescript
const executionDataSources = {
  price: {
    primary: 'jupiter',      // Most accurate for Solana swaps
    fallback: ['dexscreener', 'birdeye'],
    refresh_interval: 5000,  // 5 seconds
    max_age: 30000,          // 30 seconds
  },
  liquidity: {
    primary: 'jupiter',      // Direct pool data
    fallback: ['raydium-api', 'dexscreener'],
    refresh_interval: 10000,
  },
  execution: {
    rpc: 'helius',
    backup_rpc: 'triton',
    commitment: 'confirmed',
  },
};
```

**Pre-Execution Price Fetch:**
```bash
# Fetch validated price before execution
npx tsx .claude/skills/meme-executor/scripts/pre-execution-check.ts \
  --token <MINT> \
  --size 500 \
  --validate-liquidity \
  --output json
```
</real_time_data>

## Safety & TODOs

- This skill **MUST remain DRY‑RUN ONLY** until:
  - A secure wallet management pattern is agreed
  - Jupiter / router integration is properly tested on devnet
  - Data validation pipeline is production-tested
- When enabling live trading:
  - Add explicit `--live` flag and environment guardrails
  - Require confirmation in higher‑level orchestration agents
  - Implement daily loss limits via risk-portfolio-manager
  - Add kill switch command integration
  - Require minimum data quality score of 90/100
  - Log all executions for audit and backtesting validation


