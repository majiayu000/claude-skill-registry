---
name: wallet-cli
description: How to run watch, keygen, and sign wallet CLI commands. Use when executing wallet commands or testing wallet functionality.
---

# Wallet CLI Usage

Guide for running the three wallet types: watch, keygen, and sign.

## Prerequisites

- Wallets must be built: `make build`
- Configuration files must exist in `config/wallet/`
- For BTC/BCH: Bitcoin Core node running (for watch wallet)
- For ETH: Ethereum node running (for watch wallet)

## Required Flags

All wallet commands require the `--config` flag:

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--config` | `-c` | **Yes** | Path to configuration file |
| `--coin` | | No | Coin type: `btc`, `bch`, `eth`, `xrp`, `hyt` (default: `btc`) |
| `--account-config` | | No | Path to account config for multisig |
| `--wallet` | `-w` | No | Bitcoin Core wallet name (BTC/BCH only) |

## Configuration Files

```
config/wallet/
├── btc/
│   ├── watch.yaml      # Watch wallet config
│   ├── keygen.yaml     # Keygen wallet config
│   ├── sign1.yaml      # Sign wallet config (auth1)
│   └── sign2.yaml      # Sign wallet config (auth2)
├── bch/
│   └── ...             # Same structure as btc/
├── eth/
│   └── ...
├── xrp/
│   └── ...
└── account/
    ├── account.yaml       # Single-sig account config
    ├── account_2of3.yaml  # 2-of-3 multisig config
    └── account_3of3.yaml  # 3-of-3 multisig config
```

## Watch Wallet

Online wallet for creating unsigned transactions and sending signed transactions.

### Common Commands

```bash
# Create deposit transaction
watch --config config/wallet/btc/watch.yaml --coin btc create deposit

# Create payment transaction
watch --config config/wallet/btc/watch.yaml --coin btc create payment

# Send signed transaction
watch --config config/wallet/btc/watch.yaml --coin btc send --file data/tx/btc/payment_signed.psbt

# Import addresses
watch --config config/wallet/btc/watch.yaml --coin btc import address --file data/address/btc/addresses.csv

# Import descriptors (BTC only)
watch --config config/wallet/btc/watch.yaml --coin btc import descriptor --file data/descriptor/btc/descriptors.json

# Monitor transactions
watch --config config/wallet/btc/watch.yaml --coin btc monitor senttx --account deposit

# API commands
watch --config config/wallet/btc/watch.yaml --coin btc api balance --account payment
watch --config config/wallet/btc/watch.yaml --coin btc api listunspent --account payment
```

## Keygen Wallet

Offline cold wallet for key generation and first signature.

### Common Commands

```bash
# Create seed
keygen --config config/wallet/btc/keygen.yaml --coin btc create seed

# Generate HD keys
keygen --config config/wallet/btc/keygen.yaml --coin btc create hdkey --account client --keynum 10

# Export addresses
keygen --config config/wallet/btc/keygen.yaml --coin btc export address --account client

# Export descriptors (BTC only)
keygen --config config/wallet/btc/keygen.yaml --coin btc descriptor export --account payment --output data/descriptor/btc/payment.json

# Import private keys to Bitcoin Core
keygen --config config/wallet/btc/keygen.yaml --coin btc import privkey --account client

# Sign transaction (first signature)
keygen --config config/wallet/btc/keygen.yaml --coin btc sign signature --file data/tx/btc/payment_unsigned.psbt

# Create multisig addresses (with account config)
keygen --config config/wallet/btc/keygen.yaml --account-config config/wallet/account/account_2of3.yaml --coin btc create multisig --account payment
```

## Sign Wallet

Offline cold wallet for additional signatures on multisig transactions.

**Note**: Sign wallet only supports `btc` and `bch` coins.

### Common Commands

```bash
# Create seed
sign1 --config config/wallet/btc/sign1.yaml --coin btc create seed

# Generate HD key for auth account
sign1 --config config/wallet/btc/sign1.yaml --coin btc create hdkey

# Export full public key
sign1 --config config/wallet/btc/sign1.yaml --coin btc export fullpubkey

# Import private key
sign1 --config config/wallet/btc/sign1.yaml --coin btc import privkey

# Sign transaction (second/additional signature)
sign1 --config config/wallet/btc/sign1.yaml --coin btc sign signature --file data/tx/btc/payment_unsigned_1.psbt
```

## Multi-Coin Examples

### Ethereum

```bash
# Watch wallet
watch --config config/wallet/eth/watch.yaml --coin eth create deposit
watch --config config/wallet/eth/watch.yaml --coin eth api syncing

# Keygen wallet
keygen --config config/wallet/eth/keygen.yaml --coin eth create seed
keygen --config config/wallet/eth/keygen.yaml --coin eth create hdkey --account client --keynum 10
```

### Ripple (XRP)

```bash
# Watch wallet
watch --config config/wallet/xrp/watch.yaml --coin xrp create deposit

# Keygen wallet
keygen --config config/wallet/xrp/keygen.yaml --coin xrp create seed
keygen --config config/wallet/xrp/keygen.yaml --coin xrp create hdkey --account client --keynum 10
```

## E2E Script Usage

E2E scripts set config paths as variables and use `-c` short flag:

```bash
# From scripts/operation/btc/e2e/*.sh
BTC_CONFIG_WATCH="${PROJECT_ROOT}/config/wallet/btc/watch.yaml"
BTC_CONFIG_KEYGEN="${PROJECT_ROOT}/config/wallet/btc/keygen.yaml"

watch -c "${BTC_CONFIG_WATCH}" --coin btc create payment
keygen -c "${BTC_CONFIG_KEYGEN}" --coin btc sign signature --file tx.psbt
```

## Troubleshooting

### Error: "--config flag is required"

All wallet commands now require explicit config path:

```bash
# Wrong (old way with env vars - no longer works)
export BTC_WATCH_WALLET_CONF=./config/wallet/btc/watch.yaml
watch create deposit

# Correct (new way)
watch --config ./config/wallet/btc/watch.yaml --coin btc create deposit
```

### Error: "coin args is invalid"

Ensure `--coin` flag has valid value:

- Watch/Keygen: `btc`, `bch`, `eth`, `xrp`, `hyt`
- Sign: `btc`, `bch` only

## Related

- `docs/commands.md` - Full command reference
- `docs/crypto/btc/psbt/user-guide.md` - PSBT workflow
- `docs/crypto/btc/taproot/user-guide.md` - Taproot usage
