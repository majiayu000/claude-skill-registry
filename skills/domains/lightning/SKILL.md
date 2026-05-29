---
name: lightning
description: |
  Complete Lightning Network lifecycle. Audits channels, routing, invoices.
  Plans capacity, executes rebalancing, verifies payments. Every run does all.

  Auto-invoke when: files contain lightning/lnd/bolt11/invoice, imports
  lightning packages, references LND_* env vars, channel handlers modified.
argument-hint: "[focus area, e.g. 'channels' or 'liquidity']"
---

# /lightning

World-class Lightning lifecycle. Audit, plan, execute, verify—every time.

## What This Does

Examines your Lightning setup, finds all gaps, fixes them, and verifies payments
end-to-end. No partial modes. Every run does the full cycle.

## Branching

Assumes you start on `master`/`main`. Before making code changes:

```bash
git checkout -b fix/lightning-$(date +%Y%m%d)
```

Config-only changes (node config, env vars, services) don't require a branch.
Code changes do.

## Process

### 0. Environment Check

**Confirm network and connectivity first.** Before any Lightning ops:

```bash
lncli --network=testnet getinfo | jq '.chains, .synced_to_chain'
lncli getinfo | jq '.uris, .identity_pubkey'
```

Check:
- Testnet vs mainnet is intentional
- Node is synced to chain
- Peers reachable (no stale URIs)

### 1. Audit

**Spawn the auditor.** Use the `lightning-auditor` subagent for deep analysis.
It examines:
- Channel health (active, disabled, policy asymmetry)
- Liquidity (local/remote balance skew, inbound capacity)
- Routing performance (failures, fee policy, CLTV)
- Invoice hygiene (expiry, amountless, memo policy)
- Security (macaroon use, no secrets logged)
- Ops (backup status, watchtower, autopilot settings)

**Run automated checks:**
```bash
lightning-auditor --full
```

### 2. Plan

From audit findings, build a remediation plan. Don't just list issues—plan
the fixes.

For each finding:
- **Config issues** → Fix directly (lnd.conf, systemd, env vars)
- **Channel issues** → Plan closure/reopen or rebalancing
- **Code issues** → Delegate to Codex with clear specs

Prioritize:
1. **P0** — Funds at risk, node offline, broken payments
2. **P1** — Liquidity dead ends, routing failures
3. **P2** — Suboptimal fees, imbalance, missing UX
4. **P3** — Nice-to-haves, metrics polish

### 3. Execute

**Fix everything.** Don't stop at a report.

**Config fixes (do directly):**
```bash
# Example: update env vars or config
rg -n "LND_|lnd.conf" .
```

**Channel management:**
- Close dead channels, reopen with better peers
- Adjust fees and CLTV to match route goals
- Rebalance to restore inbound/outbound capacity

**Rebalancing:**
```bash
lncli --network=testnet listchannels | jq '.channels[] | {chan_id, local_balance, remote_balance}'
```

### 4. Verify

**Prove it works.** Not "looks right"—actually works.

**Connectivity + sync:**
```bash
lncli --network=testnet getinfo | jq '.synced_to_chain'
```

**Invoice create + pay (use a second node):**
```bash
lncli --network=testnet addinvoice --amt 1000 --memo "smoke"
lncli --network=testnet payinvoice <bolt11>
```

**Channel balance verification:**
```bash
lncli --network=testnet listchannels | jq '.channels[] | {chan_id, local_balance, remote_balance}'
```

If any verification fails, go back and fix it. Don't declare done until all
checks pass.

## Channel Management

Guidance:
- Prefer few high-quality peers over many weak ones
- Avoid long-lived channels with dead liquidity
- Keep inbound capacity for receiving use cases
- Keep outbound capacity for paying and routing
- Use fee policy to shape traffic, not to chase micro-yield

## Liquidity Planning

Plan capacity by purpose:
- **Send-first**: higher local balance
- **Receive-first**: higher remote balance
- **Routing**: balanced channels, diverse peers

Targets:
- Maintain 20-40% inbound on critical channels
- Avoid >80% one-sided imbalance
- Rebalance before outbound drops below 10%

## Default Stack

Assumes LND + Bitcoin Core + systemd + Docker (optional). Adapts to other
stacks—concepts are the same, only tooling differs.

## What You Get

When complete:
- Healthy channels with stable peers
- Planned liquidity with clear inbound/outbound targets
- Verified invoice creation and payment flow
- Rebalancing executed where needed
- Routing policy aligned with goals
- Configuration sane and documented
