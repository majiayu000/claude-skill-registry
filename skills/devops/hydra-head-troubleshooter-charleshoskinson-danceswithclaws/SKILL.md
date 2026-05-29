---
name: hydra-head-troubleshooter
description: "Hydra troubleshooting: decision tree for common issues. Maps symptoms to fixes with verification steps."
allowed-tools:
  - Read
user-invocable: true
context:
  - "!hydra-node --version 2>&1 | head -3"
---

# hydra-head-troubleshooter

## When to use

- Hydra Head doesn't start or no head observed
- Head exists but doesn't make progress
- Peers out of sync or disconnected
- Log messages: PeerConnected, AckSn, LogicOutcome errors

## Operating rules (must follow)

- Confirm network and hydra-node version first
- Request logs from ALL participants for same time window
- Never request key contents (file paths OK)
- Output: (1) Root cause (2) Fix steps (3) Verification

## Quick diagnostic commands

```bash
# Check hydra-node version
hydra-node --version

# Check API health
curl -s localhost:4001/health

# Check peers
curl -s localhost:4001/peers

# Check head status
curl -s localhost:4001/status

# Check metrics (if enabled)
curl -s localhost:6001/metrics | grep hydra
```

## Decision tree

### A) "No head is observed from the chain"

**Symptoms:**

- Head never appears in logs
- No Init/Commit/Open progression
- Client shows no head state

**Check 1: Cardano connection**

```bash
# Verify cardano-node is ready
cardano-cli query tip --testnet-magic 1
# Should show current slot, not error

# Check socket exists
ls -la $CARDANO_NODE_SOCKET_PATH
```

**Fix:** Wait for cardano-node sync, verify socket path and network magic

**Check 2: Scripts tx id**

```bash
# Verify you're using correct scripts tx id for network
# Get from hydra-node release notes

# In hydra-node logs, look for:
grep -i "script" hydra-node.log | head -20
```

**Fix:** Use correct `--hydra-scripts-tx-id` for your network

**Check 3: Key mismatch**

```bash
# Verify cardano.sk matches what peers have as your vkey
cardano-cli key verification-key \
  --signing-key-file cardano.sk \
  --verification-key-file check.vkey

# Compare check.vkey with what you distributed
```

**Fix:** Re-exchange verification keys with all peers

---

### B) "Head does not make progress"

**Symptoms:**

- Head exists but stuck at Init or Commit
- Snapshots not confirmed
- Commands hang or timeout

**Check 1: Peer connectivity**

```bash
# In logs, look for PeerConnected
grep "PeerConnected" hydra-node.log

# Check metrics
curl -s localhost:6001/metrics | grep peers_connected
```

**Fix:** Verify `--peer host:port` is correct and ports are reachable

**Check 2: Hydra key mismatch**

```bash
# Look for AckSn issues
grep -E "AckSn|LogicOutcome" hydra-node.log

# Verify hydra keys match
hydra-node verify-keys \
  --hydra-signing-key hydra.sk \
  --hydra-verification-key peer-hydra.vk
```

**Fix:** Re-exchange hydra verification keys

**Check 3: Version mismatch**

```bash
# All nodes must run compatible versions
hydra-node --version
# Compare across all participants
```

**Fix:** Align hydra-node versions

---

### C) "Head stuck: peer out of sync"

**Symptoms:**

- One node accepts txs, others reject
- Snapshots stop being signed
- Ledger state diverged

**Cause:** Different ledger views due to config drift or missed txs

**Fix: Snapshot side-loading**

```bash
# 1. Get latest snapshot from healthy node
curl -s http://healthy-node:4001/snapshot > snapshot.json

# 2. Post to out-of-sync node
curl -X POST http://out-of-sync-node:4001/snapshot \
  -H "Content-Type: application/json" \
  -d @snapshot.json
```

**Verify:** Snapshots resume, all parties sign again

---

### D) Mirror nodes / HA issues

**Symptoms:**

- `SnapshotAlreadySigned` in logs
- etcd quorum issues

**Reality:**

- `SnapshotAlreadySigned` is transient and harmless with mirrors
- Keep mirror count < floor(n/2) for quorum stability

**Fix:** Reduce mirror count or accept transient warnings

---

## Log patterns to grep

| Pattern             | Meaning                              |
| ------------------- | ------------------------------------ |
| `PeerConnected`     | Peer connected successfully          |
| `PeerDisconnected`  | Peer lost connection                 |
| `AckSn`             | Snapshot acknowledgment              |
| `LogicOutcome`      | Head logic result (check for errors) |
| `SnapshotConfirmed` | Snapshot finalized                   |
| `HeadIsOpen`        | Head successfully opened             |
| `HeadIsClosed`      | Head closed, contestation started    |

## Verification checklist

After any fix:

- [ ] All nodes same hydra-node version
- [ ] Scripts tx id correct for network
- [ ] cardano-node ready (query tip works)
- [ ] PeerConnected for all peers
- [ ] AckSn messages flowing
- [ ] No LogicOutcome errors

## Examples

### Example: Diagnose stuck head

**User request:** "My Hydra head won't open—stuck at commit"

**Response:**

```bash
# 1. Check all peers connected
grep "PeerConnected" hydra-node.log | tail -10
# Should see PeerConnected for each peer

# 2. If missing peers, check network
nc -zv peer-host 5001
# Should show "Connection succeeded"

# 3. Check all parties committed
curl -s localhost:4001/status | jq .
# Look for parties and their commit status

# 4. Check for key issues
grep -E "InvalidSignature|WrongParty" hydra-node.log

# Common fix: restart with correct peer addresses
# Verify --peer host:port matches actual peer locations
```

## References

- `hydra-head` (operational guidance)
- `hydra-head-operator` (execution)
- `reference/sources.md` (doc provenance)
- [hydra.family troubleshooting](https://hydra.family/head-protocol/docs/how-to/operating-hydra)
