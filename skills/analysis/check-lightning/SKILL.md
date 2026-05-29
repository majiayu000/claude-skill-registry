---
name: check-lightning
description: |
  Audit Lightning Network integration. Checks node health, channel balances,
  peer connectivity, invoice handling, and routing. Use when: reviewing
  Lightning setup, diagnosing payment failures, or capacity planning.
  Keywords: lightning, lnd, cln, channels, invoices, bolt11.
---

# /check-lightning

Audit Lightning integration. Output findings as structured report.

## What This Does

1. Check node sync status
2. Check channel balances (inbound/outbound)
3. Audit peer connectivity
4. Verify invoice generation
5. Review payment routing success rate
6. Check watchtower configuration
7. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-lightning-issues` to create GitHub issues or `/fix-lightning` to fix.

## Process

### 1. Node Sync Status (lncli getinfo)

```bash
# LND: node info + sync status
lncli --network=testnet getinfo

# CLN alternative
lightning-cli getinfo
```

### 2. Channel Balance (inbound/outbound liquidity)

```bash
# Channel balances + local/remote liquidity
lncli --network=testnet channelbalance
lncli --network=testnet listchannels

# On-chain wallet balance
lncli --network=testnet walletbalance

# CLN alternative
lightning-cli listfunds
lightning-cli listchannels
```

### 3. Peer Connectivity

```bash
# Peers connected?
lncli --network=testnet listpeers

# CLN alternative
lightning-cli listpeers
```

### 4. Invoice Generation

```bash
# Create test invoice (bolt11)
lncli --network=testnet addinvoice --amt 1000 --memo "healthcheck"

# List invoices
lncli --network=testnet listinvoices --max_invoices 5

# CLN alternative
lightning-cli invoice 1000 "healthcheck" "healthcheck"
lightning-cli listinvoices
```

### 5. Payment Routing Success Rate

```bash
# Forwarding history (route success)
lncli --network=testnet fwdinghistory --max_events 50

# Recent payments
lncli --network=testnet listpayments --max_payments 20

# CLN alternative
lightning-cli listforwards
lightning-cli listpays
```

### 6. Watchtower Configuration

```bash
# Watchtower info (LND)
lncli --network=testnet tower info 2>/dev/null || echo "No tower info (watchtower off?)"
lncli --network=testnet listtowers 2>/dev/null | head -5

# CLN alternative
lightning-cli listwatchtowers 2>/dev/null | head -5
```

### 7. Deep Audit

Spawn `lightning-auditor` agent for comprehensive review:
- Channel policy sanity (fees, cltv deltas)
- Route liquidity vs payment sizes
- Invoice expiry + preimage handling
- Peer reliability and channel age
- Backup + recovery posture

## Output Format

```markdown
## Lightning Audit

### P0: Critical (Payment Failures)
- Node not synced - Cannot route or pay
- No inbound liquidity - Invoices cannot be paid
- Watchtower disabled on public node

### P1: Essential (Must Fix)
- Peers disconnected or flapping
- High failure rate in forwarding history
- Invoice generation failing (bolt11 invalid)

### P2: Important (Should Fix)
- Low outbound liquidity - Payments often fail
- Fee policy too high for routes
- No channel backups verified
- No monitoring for stuck HTLCs

### P3: Nice to Have
- Optimize channel mix for inbound capacity
- Add more diverse peers
- Track success rate over time

## Current Status
- Sync: Unknown
- Liquidity: Unknown
- Peers: Unknown
- Invoices: Unknown
- Routing: Unknown
- Watchtower: Unknown

## Summary
- P0: 2 | P1: 3 | P2: 4 | P3: 3
- Recommendation: Fix sync + inbound liquidity before routing work
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| Node not synced | P0 |
| No inbound liquidity | P0 |
| Watchtower off on public node | P0 |
| Peer instability | P1 |
| Routing failures | P1 |
| Invoice generation broken | P1 |
| Low outbound liquidity | P2 |
| Fee policy too high | P2 |
| Missing channel backups | P2 |
| Optimization work | P3 |

## Related

- `/log-lightning-issues` - Create GitHub issues from findings
- `/fix-lightning` - Fix Lightning issues
- `/lightning` - Full Lightning lifecycle management
- `/check-bitcoin` - Bitcoin on-chain audit
- `/check-btcpay` - BTCPay Server audit
- `/check-payments` - Multi-provider payment audit
