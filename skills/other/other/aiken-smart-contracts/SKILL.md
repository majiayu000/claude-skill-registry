---
name: aiken-smart-contracts
description: "Aiken workflows: validators, building, blueprints, .plutus generation. Safe guidance for smart contract development."
allowed-tools:
  - Bash(aiken:*)
  - Bash(cardano-cli:*)
  - Read
  - Write
context:
  - "!aiken --version 2>&1 | head -3"
  - "!aiken --help 2>&1 | head -20"
---

# aiken-smart-contracts

## When to use

- Writing or auditing Aiken validators
- Building and testing smart contracts
- Generating .plutus artifacts for CLI/MeshJS

## Operating rules (must follow)

- Confirm Aiken version before generating code
- Verify script hashes after every rebuild
- Test on preprod/preview before mainnet
- Treat datum/redeemer schemas as versioned APIs

## Workflow

### 1. Initialize project

```bash
aiken new my-project
cd my-project
```

### 2. Project structure

```
my-project/
├── aiken.toml           # Project config
├── lib/                 # Reusable modules
├── validators/          # Validator entry points
│   └── my_validator.ak
└── plutus.json          # Generated blueprint
```

### 3. Write validator

```aiken
// validators/my_validator.ak
use aiken/transaction.{ScriptContext}

validator {
  fn spend(datum: Data, redeemer: Data, ctx: ScriptContext) -> Bool {
    // Your validation logic
    True
  }
}
```

### 4. Build and test

```bash
# Build all validators
aiken build

# Run tests
aiken check

# Format code
aiken fmt
```

### 5. Generate artifacts

```bash
# Blueprint is auto-generated at plutus.json
# Extract .plutus for cardano-cli:
aiken blueprint convert > my_validator.plutus

# Get script hash
cardano-cli conway transaction policyid \
  --script-file my_validator.plutus
```

### 6. Derive script address

```bash
cardano-cli conway address build \
  --payment-script-file my_validator.plutus \
  --testnet-magic 1 \
  --out-file script.addr
```

## Examples

### Example: Simple spending validator

**User request:** "Create a validator that only allows spending by a specific pubkey"

**Response:**

```aiken
// validators/pubkey_lock.ak
use aiken/hash.{Blake2b_224, Hash}
use aiken/transaction.{ScriptContext, Spend}
use aiken/transaction/credential.{VerificationKey}

type Datum {
  owner: Hash<Blake2b_224, VerificationKey>
}

type Redeemer {
  // Could be unit if no redeemer data needed
}

validator {
  fn spend(datum: Datum, _redeemer: Redeemer, ctx: ScriptContext) -> Bool {
    let ScriptContext { transaction, purpose } = ctx
    expect Spend(_) = purpose

    // Check if owner signed the transaction
    list.has(transaction.extra_signatories, datum.owner)
  }
}
```

```bash
# Build
aiken build

# Test
aiken check

# Generate .plutus
aiken blueprint convert > pubkey_lock.plutus
```

### Example: Parameterized validator

**User request:** "Create a time-locked validator"

**Response:**

```aiken
// validators/time_lock.ak
use aiken/interval.{Finite, Interval, IntervalBound}
use aiken/transaction.{ScriptContext, ValidityRange}

type Datum {
  lock_until: Int  // POSIX time in milliseconds
}

validator {
  fn spend(datum: Datum, _redeemer: Data, ctx: ScriptContext) -> Bool {
    let valid_range: ValidityRange = ctx.transaction.validity_range

    // Check if current time is past lock_until
    when valid_range.lower_bound.bound_type is {
      Finite(tx_earliest_time) -> tx_earliest_time > datum.lock_until
      _ -> False
    }
  }
}
```

## V3 considerations (Conway)

- Single unified context argument
- Datum may be optional for some patterns
- Governance script purposes available
- Use `aiken build --plutus-version v3` if targeting V3

## Safety / key handling

- Datum/redeemer are on-chain visible—no secrets
- Version your datum schemas (breaking changes break funds)
- Verify script hash matches after any rebuild
- Always test with small amounts first

## References

- `shared/PRINCIPLES.md`
- [Aiken documentation](https://aiken-lang.org)
- `cardano-cli-plutus-scripts` (for deployment)
