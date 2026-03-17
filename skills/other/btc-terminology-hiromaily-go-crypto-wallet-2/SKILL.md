---
name: btc-terminology
description: Critical Bitcoin terminology rules to prevent confusion between bech32m (encoding) and taproot (address type). Use when working on BTC-related code, config files, or shell scripts.
---

# BTC Terminology Rules

## 🚨 CRITICAL: Bech32m vs Taproot

**This is a common source of bugs.** Do NOT confuse these terms:

| Term | What It Is | Where Used |
|------|------------|------------|
| **bech32m** | Encoding format (HOW address is serialized) | Bitcoin Core RPC, shell scripts |
| **taproot** | Address type (WHAT the address represents) | Config files, domain model |

**Key Rule:** `bech32m` ≠ `taproot` — They are related but NOT interchangeable.

## Quick Reference Table

| Context | Correct Term | Example |
|---------|--------------|---------|
| Config YAML/TOML files | `taproot` | `address_type: "taproot"` |
| Environment variables | `taproot` | `WALLET_ADDRESS_TYPE="taproot"` |
| Bitcoin Core CLI/RPC | `bech32m` | `bitcoin-cli getnewaddress "" bech32m` |
| Shell scripts (receiver addresses) | `bech32m` | `getnewaddress "" bech32m` |
| Go domain code (`internal/domain/address/`) | `taproot` | `AddrTypeTaproot` |
| Go Bitcoin Core interface (`internal/domain/bitcoin/`) | `bech32m` | `AddressTypeTaproot = "bech32m"` |

## Common Mistakes

### ❌ WRONG

```yaml
# Config file - DON'T use bech32m
address_type: "bech32m"  # WRONG!
```

```bash
# Shell script - DON'T use taproot for Bitcoin Core RPC
bitcoin-cli getnewaddress "" taproot  # WRONG!
```

### ✅ CORRECT

```yaml
# Config file - Use taproot
address_type: "taproot"  # CORRECT!
```

```bash
# Shell script - Use bech32m for Bitcoin Core RPC
bitcoin-cli getnewaddress "" bech32m  # CORRECT!
```

## Technical Background

### Why Two Different Terms?

1. **Taproot** (BIP341) = SegWit version 1 address type (P2TR - Pay-to-Taproot)
2. **Bech32m** (BIP350) = Encoding format that fixes checksum issues in original Bech32

All Taproot addresses are encoded using bech32m, but:

- User-facing config uses "taproot" (what you want)
- Bitcoin Core RPC uses "bech32m" (how it's encoded)

### Address Format Comparison

| Encoding | SegWit Version | Address Type | Prefix | Config Value |
|----------|----------------|--------------|--------|--------------|
| Base58 | N/A | P2PKH | `1...` | `legacy` |
| Base58 | N/A | P2SH | `3...` | `p2sh-segwit` |
| Bech32 | v0 | P2WPKH | `bc1q...` | `bech32` |
| **Bech32m** | **v1** | **P2TR** | **`bc1p...`** | **`taproot`** |

## Codebase Mapping

The project has two different type definitions:

```go
// internal/domain/bitcoin/address_type.go
// For Bitcoin Core RPC communication
AddressTypeTaproot AddressType = "bech32m"  // Bitcoin Core uses "bech32m"

// internal/domain/address/types.go
// For user-facing configuration
AddrTypeTaproot AddrType = "taproot"  // User sees "taproot"
```

Conversion between these is handled by mapper functions:

```go
// internal/infrastructure/api/btc/btc/mapper.go
// FromAddressType: "bech32m" (Bitcoin Core) → "taproot" (user-facing)
// ToAddressType:   "taproot" (user-facing) → "bech32m" (Bitcoin Core)
```

## Verification Checklist

When working with Taproot/Bech32m code:

- [ ] Config files (YAML/TOML) use `address_type: "taproot"`
- [ ] Environment variables use `WALLET_ADDRESS_TYPE="taproot"`
- [ ] Bitcoin Core RPC calls in shell scripts use `bech32m`
- [ ] Shell scripts generating receiver addresses use `bech32m`
- [ ] Go code uses correct type for the layer:
  - Domain/config layer: `AddrTypeTaproot` (value: `"taproot"`)
  - Bitcoin Core interface: `AddressTypeTaproot` (value: `"bech32m"`)

## Related Files

| File | Purpose |
|------|---------|
| `internal/domain/address/types.go` | User-facing `AddrType` definitions |
| `internal/domain/bitcoin/address_type.go` | Bitcoin Core `AddressType` definitions |
| `internal/infrastructure/api/btc/btc/mapper.go` | Type conversion functions |
| `docs/crypto/btc/taproot/user-guide.md` | Taproot user guide |

## Related Documentation

- [BIP350](https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki) - Bech32m specification
- [BIP341](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) - Taproot specification
- [BIP86](https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki) - Taproot key derivation (m/86'/...)
