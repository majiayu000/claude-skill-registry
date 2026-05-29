---
name: bitcoin
description: |
  Complete Bitcoin payment lifecycle. Audits current state, fixes all issues,
  and verifies payment flows work end-to-end. Every run does all of this.

  Auto-invoke when: files contain bitcoin/btc/utxo/satoshi, imports bitcoin
  packages, references BITCOIN_* or BTC_* env vars, wallet handlers modified.
argument-hint: "[focus area, e.g. 'wallet' or 'testnet config']"
---

# /bitcoin

World-class Bitcoin lifecycle. Audit, fix, verify—every time.

## What This Does

Examines your Bitcoin integration, finds every gap, fixes them, and verifies the full payment flow end-to-end. No partial modes. Every run does the full cycle.

## Branching

Assumes you start on `master`/`main`. Before making code changes:

```bash
git checkout -b fix/bitcoin-$(date +%Y%m%d)
```

Configuration-only changes (env vars, node settings) don't require a branch. Code changes do.

## Process

### 0. Environment Check

**Detect network mismatch first.** Before any Bitcoin operations:
- Confirm daemon, CLI, and app all use the same network (mainnet/testnet/signet/regtest).
- Confirm RPC credentials, wallet name, and cookie auth align.
- Confirm wallet is loaded and indexers (txindex, blockfilterindex) match app needs.

If mismatched, resources or transactions won't be visible to your app.

### 1. Audit

**Spawn the auditor.** Use the `bitcoin-auditor` subagent for deep parallel analysis. It checks:
- Configuration (env vars, node profiles, network parity)
- Wallet health (balance, UTXO set, watch-only status)
- Transaction creation (fee rate, RBF, change output)
- Confirmation tracking (mempool, block height, reorg handling)
- Security (no hardcoded seeds, RPC locked down, no secrets in logs)
- Operational safety (dust rules, min confirmations, double-spend handling)

**Run automated checks.** Use your project tooling or scripts if present.

### 2. Plan

From audit findings, build a complete remediation plan. Categorize each item:
- **P0** — Loss of funds or broken payment flow
- **P1** — Security risk or correctness bug
- **P2** — Reliability, observability, or UX gap
- **P3** — Cleanup or optimization

### 3. Execute

**Fix everything.** Don't stop at a report.

**Configuration fixes (do directly):**
```bash
# Example: update RPC env vars
export BITCOIN_RPC_URL="http://127.0.0.1:18332"
export BITCOIN_RPC_USER="bitcoin"
export BITCOIN_RPC_PASS="..."
```

**Code fixes (delegate to Codex):**
```bash
codex exec --full-auto "Fix [specific issue]. \
File: [path]. Problem: [what's wrong]. \
Solution: [what it should do]. \
Reference: [pattern file]. \
Verify: pnpm typecheck && pnpm test" \
--output-last-message /tmp/codex-fix.md 2>/dev/null
```

Then validate: `git diff --stat && pnpm typecheck`

### 4. Verify

**Prove it works.** Not "looks right"—actually works.

**Chain sync verification:**
```bash
bitcoin-cli -testnet getblockchaininfo | jq '.blocks, .headers'
```

**Address generation and validation:**
```bash
ADDR="$(bitcoin-cli -testnet getnewaddress)"
bitcoin-cli -testnet validateaddress "$ADDR"
```

**Test transaction creation and verification:**
1. Fund a testnet address (faucet or controlled wallet).
2. Create and sign a transaction.
3. Broadcast it and verify it is in mempool.
4. Confirm it in a block and verify confirmations increment.

**End-to-end payment flow:**
1. Create a payment request in the app.
2. Pay from a testnet wallet.
3. Verify webhook/poller records txid and amount.
4. Verify confirmation thresholds update state.

If any verification fails, go back and fix it. Don't declare done until everything passes.

## Default Stack

Assumes Node.js + TypeScript + Bitcoin Core (bitcoind/bitcoin-cli) + Docker. Adapts to other stacks—concepts stay the same.

## What You Get

When complete:
- Working Bitcoin payment flow (testnet tx succeeds, state updates)
- Wallet management with sane UTXO and change handling
- Confirmation tracking with reorg-safe logic
- Fee policy and RBF behavior aligned with product goals
- All configuration in place (dev and prod)
- Deep verification passing

User can:
- Generate valid addresses
- Create and broadcast a test transaction
- See confirmations update state
- Validate end-to-end payment lifecycle
