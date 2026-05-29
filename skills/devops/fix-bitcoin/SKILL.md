---
name: fix-bitcoin
description: |
  Run /check-bitcoin, then fix the highest priority Bitcoin issue.
  Creates one fix per invocation. Invoke again for next issue.
  Use /log-bitcoin-issues to create issues without fixing.
---

# /fix-bitcoin

Fix the highest priority Bitcoin issue.

## What This Does

1. Invoke `/check-bitcoin` to audit Bitcoin setup
2. Identify highest priority issue
3. Fix that one issue
4. Verify the fix
5. Report what was done

**This is a fixer.** It fixes one issue at a time. Run again for next issue. Use `/bitcoin` for full lifecycle.

## Process

### 1. Run Primitive

Invoke `/check-bitcoin` skill to get prioritized findings.

### 2. Fix Priority Order

Fix in this order:
1. **P0**: Node not synced, wallet not encrypted
2. **P1**: Missing testnet/mainnet separation
3. **P2**: UTXO consolidation needed
4. **P3**: Advanced features

### 3. Execute Fix

**Node not synced (P0):**
Check sync status:
```bash
bitcoin-cli getblockchaininfo
```
If `headers` > `blocks`, wait or restart:
```bash
bitcoin-cli stop
bitcoind -daemon
```

**Wallet not encrypted (P0):**
Encrypt wallet:
```bash
bitcoin-cli encryptwallet "strong-passphrase"
```
Back up:
```bash
bitcoin-cli backupwallet /path/to/backup.dat
```

**Missing testnet/mainnet separation (P1):**
Split configs:
```ini
# bitcoin.conf
mainnet=1

[test]
testnet=1
walletdir=/var/lib/bitcoin/testnet-wallets
```
Use explicit network flags in tooling:
```bash
bitcoin-cli -testnet getblockchaininfo
```

**UTXO consolidation needed (P2):**
List small UTXOs:
```bash
bitcoin-cli listunspent 1 9999999
```
Create consolidation tx:
```bash
bitcoin-cli createrawtransaction '[{"txid":"...","vout":0}]' '{"bc1q...":0.999}'
```
Sign and send:
```bash
bitcoin-cli signrawtransactionwithwallet <hex>
bitcoin-cli sendrawtransaction <hex>
```

### 4. Verify

After fix:
```bash
bitcoin-cli getblockchaininfo
bitcoin-cli getwalletinfo
```

### 5. Report

```
Fixed: [P0] Wallet not encrypted

Updated: bitcoin.conf
- Added wallet encryption requirement
- Added backup path

Verified: bitcoin-cli getwalletinfo → encrypted

Next highest priority: [P0] Node not synced
Run /fix-bitcoin again to continue.
```

## Branching

Before making changes:
```bash
git checkout -b fix/bitcoin-$(date +%Y%m%d)
```

## Single-Issue Focus

Bitcoin ops are high risk. Fix one thing at a time:
- Test each change thoroughly
- Easy to roll back specific fixes
- Clear audit trail for keys and funds

Run `/fix-bitcoin` repeatedly to work through the backlog.

## Related

- `/check-bitcoin` - The primitive (audit only)
- `/log-bitcoin-issues` - Create issues without fixing
- `/bitcoin` - Full Bitcoin lifecycle
- `/bitcoin-health` - Node diagnostics
