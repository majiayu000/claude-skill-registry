---
name: hydra-head
description: "Hydra Head guidance: setup, keys, peers, lifecycle. Best practices from hydra.family. Use operator skill for execution."
allowed-tools:
  - Read
user-invocable: true
context:
  - "!hydra-node --version 2>&1 | head -3"
---

# hydra-head

> **This is a guidance skill.** Provides best practices and templates. For execution, use `hydra-head-operator`.

## When to use

- Setting up or operating hydra-node
- Understanding Hydra Head lifecycle
- Debugging connectivity or configuration issues

## Operating rules (must follow)

- Confirm network (mainnet/preprod/preview/devnet)
- Use hydra.family docs as source of truth
- Never execute—only provide guidance
- Treat all `.sk` files as secrets

## Key concepts

### Key roles

1. **Cardano keys**: Identify participant on L1, pay tx fees
2. **Hydra keys**: Multi-sign snapshots inside the head

### Lifecycle

```
Init → Commit → Open → [L2 transactions] → Close → Contest → Fanout
```

### Important parameters

- **Contestation period**: Safety window for contesting after Close
- **Deposit period**: Window for recognizing deposits

## Setup guide

### 1. Generate keys

```bash
# Cardano payment keys
cardano-cli conway address key-gen \
  --verification-key-file cardano.vk \
  --signing-key-file cardano.sk

# Hydra keys
hydra-node gen-hydra-key --output-file hydra
# Creates hydra.sk and hydra.vk

chmod 600 *.sk
```

### 2. Exchange keys with peers

Each participant needs:

- Their own `cardano.sk` and `hydra.sk`
- All peers' `cardano.vk` and `hydra.vk`

### 3. Get scripts tx id

```bash
# From hydra-node release notes for your network
# Preview: <scripts-tx-id-preview>
# Preprod: <scripts-tx-id-preprod>
# Mainnet: <scripts-tx-id-mainnet>
```

### 4. Configure hydra-node

```bash
hydra-node run \
  --node-id "alice" \
  --persistence-dir ./hydra-data \
  \
  # Cardano connection (choose one):
  --node-socket /path/to/node.socket \
  --testnet-magic 1 \
  # OR:
  --blockfrost blockfrost.txt \
  \
  # Identity:
  --cardano-signing-key cardano.sk \
  --hydra-signing-key hydra.sk \
  \
  # Peers (repeat for each):
  --cardano-verification-key bob-cardano.vk \
  --hydra-verification-key bob-hydra.vk \
  --peer "bob.example.com:5001" \
  \
  # Protocol:
  --hydra-scripts-tx-id <scripts-tx-id> \
  --contestation-period 120s \
  \
  # API:
  --api-host 0.0.0.0 \
  --api-port 4001 \
  --host 0.0.0.0 \
  --port 5001
```

## Head operations

### Open a head

```bash
# Via hydra-tui
hydra-tui --connect localhost:4001

# Via API
curl -X POST localhost:4001/init
# Then each party commits
curl -X POST localhost:4001/commit \
  -H "Content-Type: application/json" \
  -d '{"utxo": {...}}'
```

### L2 transactions

```bash
# Submit transaction
curl -X POST localhost:4001/submit \
  -H "Content-Type: application/json" \
  -d '{"transaction": "..."}'
```

### Close and fanout

```bash
curl -X POST localhost:4001/close
# Wait for contestation period
curl -X POST localhost:4001/fanout
```

## Examples

### Example: 2-party head on preprod

**User request:** "Set up a 2-party Hydra head on preprod"

**Response:**

```bash
# === Party 1 (Alice) ===

# 1. Create directory
mkdir -p ~/hydra/alice && cd ~/hydra/alice

# 2. Generate keys
cardano-cli conway address key-gen \
  --verification-key-file cardano.vk \
  --signing-key-file cardano.sk

hydra-node gen-hydra-key --output-file hydra
chmod 600 *.sk

# 3. Get preprod scripts tx id from release notes
SCRIPTS_TX_ID="..."

# 4. Exchange keys with Bob (get bob-cardano.vk, bob-hydra.vk)

# 5. Run node
hydra-node run \
  --node-id "alice" \
  --persistence-dir ./data \
  --node-socket $CARDANO_NODE_SOCKET_PATH \
  --testnet-magic 1 \
  --cardano-signing-key cardano.sk \
  --hydra-signing-key hydra.sk \
  --cardano-verification-key bob-cardano.vk \
  --hydra-verification-key bob-hydra.vk \
  --peer "bob-host:5001" \
  --hydra-scripts-tx-id $SCRIPTS_TX_ID \
  --contestation-period 120s \
  --api-port 4001 \
  --port 5001

# === After both nodes running ===

# 6. Init head (either party)
curl -X POST localhost:4001/init

# 7. Commit funds
hydra-tui --connect localhost:4001
# Select UTxO to commit

# 8. Head opens when all commit
```

## Verification checklist

- [ ] All nodes same hydra-node version
- [ ] Scripts tx id matches network
- [ ] cardano-node fully synced and socket ready
- [ ] All peers exchanged correct vkeys
- [ ] PeerConnected messages in logs
- [ ] Network ports open between peers

## Common issues

See `hydra-head-troubleshooter` skill for:

- "No head observed"
- "Head doesn't make progress"
- "Peer out of sync"
- AckSn/PeerConnected issues

## Safety / key handling

- Never share `.sk` files
- Keep separate directories per participant
- Test on devnet/preprod first
- Back up persistence directory

## References

- `shared/PRINCIPLES.md`
- `hydra-head-operator` (for execution)
- `hydra-head-troubleshooter` (for debugging)
- See `reference/sources.md` for doc provenance
