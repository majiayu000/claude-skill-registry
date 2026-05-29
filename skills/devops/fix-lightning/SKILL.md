---
name: fix-lightning
description: |
  Run /check-lightning, then fix the highest priority Lightning issue.
  Creates one fix per invocation. Invoke again for next issue.
  Use /log-lightning-issues to create issues without fixing.
---

# /fix-lightning

Fix the highest priority Lightning issue.

## What This Does

1. Invoke `/check-lightning` to audit Lightning health
2. Identify highest priority issue
3. Fix that one issue
4. Verify the fix
5. Report what was done

**This is a fixer.** It fixes one issue at a time. Run again for next issue. Use `/lightning` for full lifecycle.

## Process

### 1. Run Primitive

Invoke `/check-lightning` skill to get prioritized findings.

### 2. Fix Priority Order

Fix in this order:
1. **P0**: Node not synced, watchtower not configured
2. **P1**: Peer connectivity issues
3. **P2**: Low inbound liquidity, channel rebalancing needed
4. **P3**: Advanced routing/fees

### 3. Execute Fix

**Node not synced (P0):**
Confirm chain sync:
```bash
lncli getinfo
bitcoin-cli getblockchaininfo
```

If `synced_to_chain=false`, restart LND after backend is healthy:
```bash
sudo systemctl restart lnd
```

**Watchtower not configured (P0):**
Enable watchtower client and add a tower:
```bash
# lnd.conf
wtclient.active=1

lncli wtclient add --tower_addr=host:9911
```

**Peer connectivity issues (P1):**
Reconnect to peer:
```bash
lncli listpeers
lncli disconnect <pubkey>
lncli connect <pubkey>@host:port
```

**Low inbound liquidity (P2):**
Open a channel with pushed sats to create inbound:
```bash
lncli openchannel --node_key=<pubkey> --local_amt=1000000 --push_amt=200000
```

**Channel rebalancing needed (P2):**
Move balance from outgoing-heavy to incoming-heavy channel:
```bash
lncli listchannels
lncli rebalancechannel --from_chan_id=<from> --to_chan_id=<to> --amount=50000
```

### 4. Verify

After fix:
```bash
lncli getinfo
lncli listchannels
lncli listpeers
```

### 5. Report

```
Fixed: [P0] Node not synced

Updated: lnd service
- Restarted after chain backend healthy
- Confirmed synced_to_chain=true

Verified: lncli getinfo → synced_to_chain=true

Next highest priority: [P0] Watchtower not configured
Run /fix-lightning again to continue.
```

## Branching

Before making changes:
```bash
git checkout -b fix/lightning-$(date +%Y%m%d)
```

## Single-Issue Focus

Lightning is sensitive. Fix one thing at a time:
- Test each change thoroughly
- Easy to rollback specific fixes
- Clear audit trail for ops

Run `/fix-lightning` repeatedly to work through the backlog.

## Related

- `/check-lightning` - The primitive (audit only)
- `/log-lightning-issues` - Create issues without fixing
- `/lightning` - Full Lightning lifecycle
