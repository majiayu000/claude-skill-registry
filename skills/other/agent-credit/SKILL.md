---
name: agent-credit
description: Borrow from Aave via credit delegation. Agent self-funds by borrowing against delegator collateral. Supports borrow, repay, health checks. Works on Aave V2/V3.
---

# Aave Credit Delegation

Borrow funds from Aave using delegated credit. Your main wallet supplies collateral and delegates borrowing power to the agent's wallet. The agent can then autonomously borrow tokens when needed — the debt accrues against the delegator's position.

> **Protocol:** Works on **Aave V3** and **Aave V2** — the function signatures for credit delegation (`borrow`, `repay`, `approveDelegation`, `borrowAllowance`) are identical across both versions. Just swap in the V2 LendingPool and ProtocolDataProvider addresses. The only cosmetic difference: V3 returns collateral/debt in USD (8 decimals), V2 in ETH (18 decimals). The health factor safety check works correctly on both.

## Compatible With

- **[OpenClaw](https://openclaw.ai/)** — Install as a skill, the agent borrows autonomously
- **[Claude Code](https://www.npmjs.com/package/@anthropic-ai/claude-code)** — Run scripts directly from a Claude Code session
- **Any agent framework** — Plain bash + Foundry's `cast`, works anywhere with a shell

Combines with **[Bankr](https://bankr.bot/)** skills for borrow-then-swap flows: borrow USDC via delegation, then use Bankr to swap, bridge, or deploy it.

## How Credit Delegation Works

Credit delegation in Aave V3 separates two things: **borrowing power** and **delegation approval**.

**Borrowing power is holistic.** It comes from your entire collateral position across all assets. If you deposit $10k worth of ETH at 80% LTV, you have $8k of borrowing power — period. That borrowing power isn't locked to any specific asset.

**Delegation approval is isolated per debt token.** You control *which* assets the agent can borrow and *how much* of each by calling `approveDelegation()` on individual VariableDebtTokens. Each asset has its own debt token contract, and each approval is independent.

This means you can, for example:
- Deposit ETH as collateral (gives you broad borrowing power)
- Approve the agent to borrow up to 500 USDC (via the USDC VariableDebtToken)
- Approve the agent to borrow up to 0.1 WETH (via the WETH VariableDebtToken)
- Leave cbETH unapproved (agent cannot borrow it at all)

The agent can only borrow assets you've explicitly approved, up to the amounts you've set — but the *capacity* to borrow comes from your total collateral, not from any single deposit.

```
Your Collateral (holistic)              Delegation Approvals (isolated)
┌─────────────────────────┐             ┌──────────────────────────────┐
│  $5k ETH                │             │  USDC DebtToken → agent: 500 │
│  $3k USDC               │  ───LTV───▶ │  WETH DebtToken → agent: 0.1 │
│  $2k cbETH              │   = $8k     │  cbETH DebtToken → agent: 0  │
│  Total: $10k @ 80% LTV  │  capacity   └──────────────────────────────┘
└─────────────────────────┘
```

## Flow

```
Delegator (your wallet)                 Agent Wallet (delegatee)
    │                                        │
    │  1. supply collateral to Aave          │
    │  2. approveDelegation(agent, amount)   │
    │        on the VariableDebtToken        │
    │                                        │
    │            ┌─── 3. borrow(asset,       │
    │            │       amount, onBehalfOf   │
    │            │       = delegator)         │
    │            │                            │
    │     [debt on YOUR position]    [tokens in agent wallet]
    │            │                            │
    │            └─── 4. repay(asset,         │
    │                    amount, onBehalfOf   │
    │                    = delegator)         │
```

## Quick Start

### Prerequisites

1. **Foundry** must be installed (`cast` CLI):
   ```bash
   curl -L https://foundry.paradigm.xyz | bash && foundryup
   ```

2. **Delegator setup** (done ONCE by the user, NOT the agent):
   - Supply collateral to Aave V3 (via app.aave.com or contract)
   - Call `approveDelegation(agentAddress, maxAmount)` on the **VariableDebtToken** of the asset you want the agent to borrow
   - The VariableDebtToken address can be found via: `cast call $DATA_PROVIDER "getReserveTokensAddresses(address)(address,address,address)" $ASSET --rpc-url $RPC`

3. **Configure the skill**:
   ```bash
   mkdir -p ~/.openclaw/skills/aave-delegation
   cat > ~/.openclaw/skills/aave-delegation/config.json << 'EOF'
   {
     "chain": "base",
     "rpcUrl": "https://mainnet.base.org",
     "agentPrivateKey": "0xYOUR_AGENT_PRIVATE_KEY",
     "delegatorAddress": "0xYOUR_MAIN_WALLET",
     "poolAddress": "0xA238Dd80C259a72e81d7e4664a9801593F98d1c5",
     "dataProviderAddress": "0x2d8A3C5677189723C4cB8873CfC9C8976FDF38Ac",
     "assets": {
       "USDC": {
         "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
         "decimals": 6
       },
       "WETH": {
         "address": "0x4200000000000000000000000000000000000006",
         "decimals": 18
       }
     },
     "safety": {
       "minHealthFactor": "1.5",
       "maxBorrowPerTx": "1000",
       "maxBorrowPerTxUnit": "USDC"
     }
   }
   EOF
   ```

4. **Verify setup**:
   ```bash
   scripts/aave-setup.sh
   ```

## Core Usage

### Check Status (allowance, health, debt)

```bash
# Full status report
scripts/aave-status.sh

# Check specific asset delegation
scripts/aave-status.sh USDC

# Just health factor
scripts/aave-status.sh --health-only
```

### Borrow via Delegation

```bash
# Borrow 100 USDC
scripts/aave-borrow.sh USDC 100

# Borrow 0.5 WETH
scripts/aave-borrow.sh WETH 0.5
```

The borrow script automatically:
1. Checks delegation allowance (sufficient?)
2. Checks delegator health factor (safe to borrow?)
3. Executes the borrow
4. Reports the result

### Repay Debt

```bash
# Repay 100 USDC
scripts/aave-repay.sh USDC 100

# Repay all USDC debt
scripts/aave-repay.sh USDC max
```

The repay script automatically:
1. Approves the Pool to spend the token (if needed)
2. Executes the repay
3. Reports remaining debt

## Safety System

**Every borrow operation runs these checks BEFORE executing:**

1. **Delegation allowance** — Is the remaining allowance >= requested amount?
2. **Health factor** — Is the delegator's health factor > `minHealthFactor` (default 1.5) AFTER this borrow?
3. **Per-tx cap** — Is the amount <= `maxBorrowPerTx`?
4. **Confirmation** — Logs the full operation details before sending

If ANY check fails, the borrow is **aborted** with a clear error message.

⚠️ **The agent must NEVER bypass safety checks.** If the user asks the agent to borrow and the health factor is too low, the agent should refuse and explain why.

## Capabilities

### Read Operations (no gas needed)

- **Check delegation allowance** — How much can the agent still borrow?
- **Check health factor** — Is the delegator's position safe?
- **Check outstanding debt** — How much does the delegator owe on each asset?
- **Check available liquidity** — Is there enough in the Aave pool to borrow?
- **Resolve debt token addresses** — Look up VariableDebtToken for any asset

### Write Operations (needs gas in agent wallet)

- **Borrow** — Draw funds from Aave against delegated credit
- **Repay** — Return borrowed funds to reduce delegator's debt
- **Approve** — Approve Pool to spend tokens for repayment

## Supported Chains

| Chain     | Pool Address                                 | Gas Cost  |
|-----------|----------------------------------------------|-----------|
| Base      | `0xA238Dd80C259a72e81d7e4664a9801593F98d1c5` | Very Low  |
| Ethereum  | `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2` | High      |
| Polygon   | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` | Very Low  |
| Arbitrum  | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` | Low       |

See [deployments.md](deployments.md) for full address list including debt tokens.

## Common Patterns

### Agent Self-Funding for Gas

```bash
# Check if we have enough gas
BALANCE=$(cast balance $AGENT_ADDRESS --rpc-url $RPC)
if [ "$BALANCE" -lt "1000000000000000" ]; then  # < 0.001 ETH
  # Borrow a small amount of WETH for gas
  aave-borrow.sh WETH 0.005
fi
```

### Borrow + Swap via Bankr

```bash
# Borrow USDC from delegated credit
aave-borrow.sh USDC 100
# Swap to ETH using Bankr
bankr.sh "Swap 100 USDC for ETH on Base"
```

### Periodic DCA

```bash
# Agent borrows USDC weekly and swaps to ETH
aave-borrow.sh USDC 100
bankr.sh "Swap 100 USDC for ETH on Base"
```

### Safety-First Portfolio Rebalance

```bash
# Always check health first
aave-status.sh
# Only borrow if healthy
aave-borrow.sh USDC 500
```

## Configuration Reference

### config.json Fields

| Field                    | Required | Description                                   |
|--------------------------|----------|-----------------------------------------------|
| `chain`                  | Yes      | Chain name (base, ethereum, polygon, arbitrum) |
| `rpcUrl`                 | Yes      | JSON-RPC endpoint URL                         |
| `agentPrivateKey`        | Yes      | Agent wallet private key (0x-prefixed)        |
| `delegatorAddress`       | Yes      | User's main wallet that delegated credit      |
| `poolAddress`            | Yes      | Aave V3 Pool contract address                 |
| `dataProviderAddress`    | Yes      | Aave V3 PoolDataProvider address              |
| `assets`                 | Yes      | Map of symbol → {address, decimals}           |
| `safety.minHealthFactor` | No       | Min HF after borrow (default: 1.5)            |
| `safety.maxBorrowPerTx`  | No       | Max borrow per transaction (default: 1000)    |
| `safety.maxBorrowPerTxUnit` | No    | Unit for maxBorrowPerTx (default: USDC)       |

### Environment Variables (override config)

| Variable                    | Overrides              |
|-----------------------------|------------------------|
| `AAVE_RPC_URL`              | `rpcUrl`               |
| `AAVE_AGENT_PRIVATE_KEY`    | `agentPrivateKey`      |
| `AAVE_DELEGATOR_ADDRESS`    | `delegatorAddress`     |
| `AAVE_POOL_ADDRESS`         | `poolAddress`          |
| `AAVE_MIN_HEALTH_FACTOR`    | `safety.minHealthFactor` |

## Error Handling

| Error                        | Cause                                     | Fix                                              |
|------------------------------|-------------------------------------------|--------------------------------------------------|
| `INSUFFICIENT_ALLOWANCE`     | Delegation amount exceeded                | Delegator must call `approveDelegation()` again   |
| `HEALTH_FACTOR_TOO_LOW`      | Borrow would risk liquidation             | Reduce amount or add collateral                   |
| `AMOUNT_EXCEEDS_CAP`         | Per-tx safety cap hit                     | Reduce amount or update config                    |
| `INSUFFICIENT_LIQUIDITY`     | Not enough in Aave pool                   | Try smaller amount or different asset             |
| `INSUFFICIENT_GAS`           | Agent wallet has no native token          | Send gas to agent wallet                          |
| `EMODE_MISMATCH`             | Asset incompatible with delegator's eMode | Borrow an asset in the same eMode category        |

## Security

See [safety.md](safety.md) for the full threat model and emergency procedures.

**Critical rules:**
1. **The delegator's private key must NEVER be in this repo, config, or scripts** — this is the agent's workspace. The delegator manages their side via the Aave UI or a block explorer.
2. **Never commit config.json to version control** — it contains the agent's private key
3. **Never set `minHealthFactor` below 1.2** — liquidation happens at 1.0
4. **Always cap delegation amounts** — never approve `type(uint256).max`
5. **Monitor delegator health** — set up alerts if HF drops below 2.0
6. **Agent must refuse** to borrow if safety checks fail, even if instructed to

## Resources

- **Aave V3 Docs**: https://docs.aave.com/developers
- **Credit Delegation Guide**: https://docs.aave.com/developers/guides/credit-delegation
- **Aave Address Book**: https://github.com/bgd-labs/aave-address-book
- **Foundry Book**: https://book.getfoundry.sh/
- **DebtToken Reference**: https://docs.aave.com/developers/tokens/debttoken
