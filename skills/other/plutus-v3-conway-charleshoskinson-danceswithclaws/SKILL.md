---
name: plutus-v3-conway
description: "Plutus V3 under Conway: unified context, governance scripts, V2→V3 migration. Conceptual and practical guidance."
allowed-tools:
  - Read
user-invocable: true
---

# plutus-v3-conway

## When to use

- Migrating from Plutus V2 to V3
- Writing governance scripts (voting, proposing)
- Understanding Conway-era script changes

## Operating rules (must follow)

- Confirm target network supports Conway
- Test all governance scripts extensively on testnet
- Don't mix V2 and V3 mental models

## Key V3 changes

### 1. Unified context argument

```
V2: validator(datum, redeemer, context) → Bool
V3: validator(context) → ()  // datum/redeemer inside context
```

### 2. Datum is now optional

- For spending: datum can be Nothing if not needed
- Access via `ScriptContext.scriptInfo`

### 3. New script purposes

```
Spending      - spending UTxOs (existing)
Minting       - minting/burning tokens (existing)
Rewarding     - withdrawing rewards (existing)
Certifying    - stake certificates (existing)
Voting        - governance voting (NEW in V3)
Proposing     - governance proposals (NEW in V3)
```

### 4. Return type changes

- V2: Returns `Bool` (True/False)
- V3: Returns `()` (unit) - failure via error/trace

## V3 interface (Aiken)

### Spending validator

```aiken
validator my_validator {
  spend(
    datum: Option<MyDatum>,
    redeemer: MyRedeemer,
    _own_ref: OutputReference,
    tx: Transaction,
  ) {
    // Return () on success
    // Use expect/fail! for failure
    expect Some(d) = datum
    d.owner == get_signer(tx)
  }
}
```

### Governance validator

```aiken
validator governance {
  vote(
    redeemer: VoteRedeemer,
    voter: Voter,
    tx: Transaction,
  ) {
    // Validate voting logic
    True
  }

  propose(
    redeemer: ProposeRedeemer,
    tx: Transaction,
  ) {
    // Validate proposal logic
    True
  }
}
```

## Migration checklist (V2 → V3)

### 1. Update validator signature

```
// V2
fn spend(datum: Datum, redeemer: Redeemer, ctx: ScriptContext) -> Bool

// V3
fn spend(datum: Option<Datum>, redeemer: Redeemer, own_ref: OutputReference, tx: Transaction) -> ()
```

### 2. Handle optional datum

```aiken
// V3 - datum may be None
spend(datum: Option<Datum>, ...) {
  expect Some(d) = datum  // Fail if None when you need it
  // or
  when datum is {
    Some(d) -> handle_datum(d)
    None -> handle_no_datum()
  }
}
```

### 3. Update return logic

```aiken
// V2 - return Bool
if condition { True } else { False }

// V3 - return () or fail
if condition { () } else { fail @"Condition not met" }
// or use expect
expect condition
```

### 4. Script hash changes

- V3 scripts have different hashes than V2 equivalents
- Recalculate all script addresses
- Update any hardcoded references

## Examples

### Example: Simple V3 spending validator

```aiken
use aiken/collection/list
use cardano/transaction.{Transaction, OutputReference}

type Datum {
  owner: ByteArray,
}

type Redeemer {
  // empty
}

validator simple_lock {
  spend(
    datum: Option<Datum>,
    _redeemer: Redeemer,
    _own_ref: OutputReference,
    tx: Transaction,
  ) {
    expect Some(d) = datum
    list.has(tx.extra_signatories, d.owner)
  }
}
```

### Example: Governance voting script

```aiken
use cardano/transaction.{Transaction}
use cardano/governance.{Voter, ProposalProcedure}

validator dao_governance {
  vote(
    redeemer: Data,
    voter: Voter,
    tx: Transaction,
  ) {
    // Check voter is authorized
    // Check voting rules are followed
    True
  }

  propose(
    redeemer: Data,
    proposal: ProposalProcedure,
    tx: Transaction,
  ) {
    // Check proposer has required stake
    // Check proposal format
    True
  }
}
```

## Conway governance context

### DRep (Delegated Representative)

- Users can delegate voting power to DReps
- Scripts can act as DReps

### Constitutional Committee

- Multi-sig governance for protocol changes
- Scripts can be committee members

### Governance actions

- Parameter changes
- Hard fork initiation
- Treasury withdrawals
- Constitutional changes

## CLI flags for V3

```bash
# Build V3 script with Aiken
aiken build --plutus-version v3

# CLI transaction with V3 script
cardano-cli conway transaction build \
  --tx-in-script-file my_script_v3.plutus \
  ...
```

## Safety / key handling

- Governance scripts are high-stakes—test extensively
- V3 governance affects protocol parameters
- Verify all script hashes after migration
- Use preprod for testing governance flows

## References

- `shared/PRINCIPLES.md`
- [Plutus V3 CIP](https://cips.cardano.org)
- [Conway governance](https://docs.cardano.org)
- `aiken-smart-contracts` (for writing V3 validators)
