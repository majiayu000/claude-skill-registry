---
name: bch-development
description: Bitcoin Cash (BCH) API implementation rules. Critical pattern for embedding Bitcoin struct and overriding BCH-specific methods. Use when working on BCH-related code in internal/infrastructure/api/btc/bch/.
---

# BCH (Bitcoin Cash) Development Rules

## 🚨 CRITICAL: Override Pattern for BCH-Specific Logic

**This is a non-negotiable architectural rule.** BCH implementation uses struct embedding with method override pattern.

### Architecture Overview

```go
// internal/infrastructure/api/btc/bch/bitcoin_cash.go
type BitcoinCash struct {
    apibtcimpl.Bitcoin  // Embeds BTC implementation
}
```

**Key Principle:** `BitcoinCash` embeds `Bitcoin`, inheriting all BTC methods by default.

## Rules

### ✅ DO: Override on BCH Side

When BCH requires different logic from BTC:

1. **Create a new file** in `internal/infrastructure/api/btc/bch/`
2. **Implement the method** with the same name on `BitcoinCash`
3. **This "overrides"** the embedded `Bitcoin` method

### ❌ DON'T: Modify BTC Side for BCH

- **NEVER** modify `internal/infrastructure/api/btc/btc/` for BCH-specific requirements
- **NEVER** add BCH conditionals in BTC code
- **NEVER** add BCH-specific types or logic to the BTC package

## Why This Pattern?

| Reason | Explanation |
|--------|-------------|
| **Separation of Concerns** | BTC code remains pure and focused |
| **Maintainability** | BCH changes don't affect BTC |
| **Clarity** | BCH differences are explicit in BCH directory |
| **Safety** | BTC modifications can't accidentally break BCH |

## Implementation Examples

### Example 1: GetAddressInfo Override

BCH has a different response structure for `getaddressinfo` RPC:

```go
// internal/infrastructure/api/btc/bch/address.go
// BCH-specific response type
type GetAddressInfoResult struct {
    Address      string `json:"address"`
    ScriptPubKey string `json:"scriptPubKey"`
    Label        string `json:"label,omitempty"`  // BCH uses Label (singular)
    Labels       []struct {                       // BCH has different Labels structure
        Name    string `json:"name"`
        Purpose string `json:"purpose"`
    } `json:"labels"`
    // ... other BCH-specific fields
}

// Override GetAddressInfo for BCH
func (b *BitcoinCash) GetAddressInfo(addr string) (*dtobtc.AddressInfo, error) {
    // BCH-specific implementation
    // ...
}
```

### Example 2: GetAccount Override

BCH requires different logic for getting account info:

```go
// internal/infrastructure/api/btc/bch/account.go
func (b *BitcoinCash) GetAccount(addr string) (string, error) {
    // BCH calls GetAddressInfo (which is also overridden)
    res, err := b.GetAddressInfo(addr)
    if err != nil {
        return "", fmt.Errorf("fail to call btc.GetAddressInfo() in bch: %w", err)
    }
    // BCH-specific label extraction
    if len(res.Labels) == 0 {
        return "", nil
    }
    return res.Labels[0], nil
}
```

### Example 3: Chain Parameters Override

BCH has different network magic numbers:

```go
// internal/infrastructure/api/btc/bch/bitcoin_cash.go
const (
    MainnetMagic wire.BitcoinNet = 0xe8f3e1e3  // BCH-specific
    TestnetMagic wire.BitcoinNet = 0xf4f3e5f4  // BCH-specific
    Regtestmagic wire.BitcoinNet = 0xfabfb5da  // BCH-specific
)

func (b *BitcoinCash) initChainParams() {
    // Override chain parameters for BCH
}
```

## BCH vs BTC: Feature Differences

| Feature | BTC | BCH |
|---------|-----|-----|
| SegWit | ✅ Supported | ❌ Not supported |
| Taproot | ✅ Supported | ❌ Not supported |
| Address Format | Legacy, SegWit, Taproot | Legacy, CashAddr |
| Network Magic | BTC values | BCH-specific values |

## Directory Structure

```
internal/infrastructure/api/btc/
├── btc/                      # BTC implementation (DO NOT modify for BCH)
│   ├── bitcoin.go            # Bitcoin struct and methods
│   ├── account.go
│   ├── address.go
│   └── ...
├── bch/                      # BCH overrides (ADD new files here)
│   ├── bitcoin_cash.go       # BitcoinCash struct (embeds Bitcoin)
│   ├── account.go            # Override: GetAccount
│   ├── address.go            # Override: GetAddressInfo
│   └── ...
└── connection.go             # Shared connection logic
```

## Checklist for BCH Changes

When implementing BCH-specific logic:

- [ ] File created in `internal/infrastructure/api/btc/bch/` (NOT in `btc/`)
- [ ] Method has same signature as the BTC method being overridden
- [ ] No changes made to `internal/infrastructure/api/btc/btc/`
- [ ] BCH-specific types defined in BCH package (if needed)
- [ ] Error messages include "bch" for traceability

## Common Mistakes

### ❌ WRONG: Adding BCH Logic to BTC

```go
// internal/infrastructure/api/btc/btc/account.go
func (b *Bitcoin) GetAccount(addr string) (string, error) {
    if b.coinTypeCode == domainCoin.BCH {  // DON'T DO THIS!
        // BCH-specific logic
    }
    // BTC logic
}
```

### ✅ CORRECT: Override in BCH Package

```go
// internal/infrastructure/api/btc/bch/account.go
func (b *BitcoinCash) GetAccount(addr string) (string, error) {
    // BCH-specific logic here
}
```

## Technical Note: How Go Embedding Works

When `BitcoinCash` embeds `Bitcoin`:

1. All `Bitcoin` methods are "promoted" to `BitcoinCash`
2. If `BitcoinCash` defines a method with the same name, it takes precedence
3. The embedded `Bitcoin` methods can still be called via `b.Bitcoin.MethodName()`

```go
// Call overridden method (uses BitcoinCash.GetAddressInfo)
info, _ := bch.GetAddressInfo(addr)

// Call embedded method directly (uses Bitcoin.GetAddressInfo)
info, _ := bch.Bitcoin.GetAddressInfo(addr)
```

## Related Files

| File | Purpose |
|------|---------|
| `internal/infrastructure/api/btc/bch/bitcoin_cash.go` | BitcoinCash struct definition |
| `internal/infrastructure/api/btc/btc/bitcoin.go` | Bitcoin struct (embedded by BCH) |
| `internal/application/ports/btc/interface.go` | Bitcoiner interface |

## Related Documentation

- [BCH Technical Docs](../../../docs/crypto/bch/)
- [BTC Technical Docs](../../../docs/crypto/btc/)
