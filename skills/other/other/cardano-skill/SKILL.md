---
name: aiken-smart-contract
description: >
  Write, test, and debug Aiken smart contracts for Cardano.
  Use when writing validators, minting policies, or any on-chain Plutus code.
  Triggers on: Aiken, validator, smart contract, Cardano on-chain, Plutus,
  minting policy, spend validator, datum, redeemer, plutus.json, blueprint.
  Covers language syntax, validator patterns, property-based testing,
  security best practices, stdlib usage, and off-chain MeshJS integration.
user-invocable: true
---

# Aiken Smart Contract Development

You are an expert Aiken smart contract developer for Cardano. Aiken is a pure
functional language that compiles to UPLC (Untyped Plutus Lambda Calculus)
targeting Plutus V3.

## Core Principles

1. **Validators are predicates** — they return Bool. True = authorize, False = reject.
2. **No side effects** — pure functional, no mutation, no loops (use recursion).
3. **Local reasoning only** — eUTxO model means each validator sees only its own context.
4. **Test everything** — Aiken's test runner uses the real CEK machine. Tests are production-accurate.
5. **Security first** — understand double satisfaction, datum hijacking, and other eUTxO-specific attacks.

## Decision Tree

When asked to write a smart contract:

1. **Identify the validator purpose**: spend, mint, withdraw, publish, vote, propose
2. **Design the datum and redeemer types** before writing logic
3. **Write the validator** using the correct handler signature
4. **Write tests immediately** — unit tests first, then property-based
5. **Review for security** — check the security patterns in [security.md](reference/security.md)
6. **Build and verify** — `aiken build` must succeed, `aiken check` must pass
7. **Write off-chain integration** — build transactions with MeshJS, test on preview testnet (see [offchain.md](reference/offchain.md))

When asked to audit or review a smart contract:

1. **Follow the auditing methodology** in [auditing.md](reference/auditing.md)
2. **Phase 1:** Understand types, state model, actors, and trust boundaries
3. **Phase 2:** Systematic vulnerability scan against all 11 security categories
4. **Phase 3:** Parameterized validator analysis (if applicable)
5. **Phase 4:** Multi-validator interaction review (if applicable)
6. **Phase 5:** Test coverage assessment — identify missing tests
7. **Report findings** with severity, location, exploitation path, and fix

## Handler Signatures (Aiken v1.1+)

```aiken
// Spending validator — most common
validator my_validator {
  spend(
    datum: Option<MyDatum>,    // Always Option — may be missing
    redeemer: MyRedeemer,
    output_reference: OutputReference,
    transaction: Transaction,
  ) {
    todo
  }
}

// Minting policy
validator my_policy {
  mint(
    redeemer: MyRedeemer,
    policy_id: PolicyId,
    transaction: Transaction,
  ) {
    todo
  }
}

// Withdrawal validator
validator my_withdrawal {
  withdraw(
    redeemer: MyRedeemer,
    credential: Credential,
    transaction: Transaction,
  ) {
    todo
  }
}

// Certificate publishing
validator my_cert {
  publish(
    redeemer: MyRedeemer,
    certificate: Certificate,
    transaction: Transaction,
  ) {
    todo
  }
}

// Governance voting
validator my_vote {
  vote(
    redeemer: MyRedeemer,
    voter: Voter,
    transaction: Transaction,
  ) {
    todo
  }
}

// Governance proposal
validator my_proposal {
  propose(
    redeemer: MyRedeemer,
    proposal_procedure: ProposalProcedure,
    transaction: Transaction,
  ) {
    todo
  }
}

// Fallback for unhandled purposes
validator my_fallback {
  else(script_context: ScriptContext) {
    todo
  }
}
```

## Multi-Purpose Validators

A single validator can handle multiple purposes (same script hash):

```aiken
validator token_lock {
  mint(redeemer: MintAction, policy_id: PolicyId, tx: Transaction) {
    // Minting logic
    todo
  }

  spend(datum: Option<LockDatum>, redeemer: SpendAction, _oref: OutputReference, tx: Transaction) {
    // Spending logic — require token burn
    todo
  }
}
```

## Parameterized Validators

Validators can take compile-time parameters:

```aiken
validator my_validator(owner: VerificationKeyHash, deadline: POSIXTime) {
  spend(_datum: Option<Data>, _redeemer: Data, _oref: OutputReference, tx: Transaction) {
    let must_be_signed = list.has(tx.extra_signatories, owner)
    let must_be_after_deadline =
      interval.is_entirely_after(tx.validity_range, deadline)
    must_be_signed && must_be_after_deadline
  }
}
```

Parameters are applied when building the script address from the blueprint.

## Key Language Idioms

```aiken
// Pattern matching (exhaustive)
when redeemer is {
  Lock -> handle_lock(datum, tx)
  Unlock -> handle_unlock(datum, tx)
}

// expect — unsafe downcast, fails if wrong
expect Some(datum) = datum_opt
expect InlineDatum(raw) = output.datum
expect typed_datum: MyDatum = raw

// Pipe operator — chain operations
tx.outputs
  |> list.filter(fn(o) { o.address == script_address })
  |> list.any(fn(o) { check_output(o) })

// Trace for debugging (removed in production with --trace-level silent)
trace @"checking signature"
let signed = list.has(tx.extra_signatories, owner)
// ? operator — postfix, traces expression name if False
list.has(tx.extra_signatories, owner)?
// Produces trace: "list.has(tx.extra_signatories, owner) ? False"
// NOTE: ? is postfix only (expr?), not infix (expr ? "msg")
```

## Common Validation Patterns

```aiken
// Check transaction signed by key
list.has(tx.extra_signatories, owner_pkh)

// Check time (must be after deadline)
interval.is_entirely_after(tx.validity_range, deadline)

// Check time (must be before deadline)
interval.is_entirely_before(tx.validity_range, deadline)

// Find own input
expect Some(own_input) = transaction.find_input(tx.inputs, oref)

// Find outputs to a script address
transaction.find_script_outputs(tx.outputs, script_hash)

// Check NFT exists in value
assets.quantity_of(value, policy_id, asset_name) == 1

// Merge values
assets.merge(value_a, value_b)

// Check lovelace amount
assets.lovelace_of(output.value) >= min_amount
```

## Testing

Always write tests alongside validators. See [testing.md](reference/testing.md) for full details.

```aiken
// Unit test
test must_be_signed() {
  let tx = Transaction {
    ..transaction.placeholder,
    extra_signatories: [mock_signer],
  }
  my_validator.spend(Some(datum), redeemer, mock_oref, tx)
}

// Expected failure
test must_fail_without_signature() fail {
  my_validator.spend(Some(datum), redeemer, mock_oref, transaction.placeholder)
}

// Parameterized validator — pass params first, then handler args
// validator gift_card(utxo_ref: OutputReference, token_name: ByteArray) { mint(...) }
// Call as: gift_card.mint(utxo_ref, token_name, redeemer, policy_id, tx)

// Property-based test
test prop_any_signer_works(signer via fuzz.bytearray_fixed(28)) {
  let datum = MyDatum { owner: signer }
  let tx = Transaction {
    ..transaction.placeholder,
    extra_signatories: [signer],
  }
  my_validator.spend(Some(datum), Unlock, mock_oref, tx)
}
```

## CLI Workflow

```bash
aiken new my-project          # Scaffold new project
aiken build                   # Compile, generate plutus.json
aiken check                   # Typecheck + run all tests
aiken check -m "test_name"    # Run specific test
aiken fmt                     # Format code
aiken docs                    # Generate documentation
aiken blueprint address       # Generate script address from blueprint
```

## Reference Material

For detailed information, consult:

- [Language reference](reference/language.md) — types, syntax, modules, encoding
- [Validator patterns](reference/validators.md) — common validator architectures
- [Testing guide](reference/testing.md) — unit, property-based, scenario testing
- [Security patterns](reference/security.md) — eUTxO attack vectors and mitigations (11 categories)
- [Auditing methodology](reference/auditing.md) — structured audit process, severity classification, CIP-52 compliance
- [Standard library](reference/stdlib.md) — key modules and functions
- [Design patterns](reference/patterns.md) — withdraw-zero trick, UTxO indexers, upgrade/migration, etc.
- [Gotchas](reference/gotchas.md) — compiler pitfalls, type system surprises, testing patterns
- [Off-chain integration](reference/offchain.md) — MeshJS transaction building, datum encoding, integration testing
- [CIP-113 Programmable Tokens](reference/cip113.md) — multi-validator architecture, registry, transfer flows, E2E testing

## Examples

Working examples with full test suites (all compiler-validated):

**Phase 1 — Core Patterns:**
- [Hello World](examples/hello-world.md) — simplest spend validator
- [Vesting](examples/vesting.md) — time-locked spending with dual authorization
- [Gift Card](examples/gift-card.md) — mint+spend dual handler with one-shot NFT

**Phase 2 — Security & Design Patterns:**
- [Multi-Sig](examples/multi-sig.md) — M-of-N threshold signatures
- [State Machine](examples/state-machine.md) — continuing output pattern with state transitions
- [NFT Vault](examples/nft-vault.md) — datum hijacking prevention with NFT authentication

**Phase 3 — Advanced Optimization Patterns:**
- [Withdraw Zero](examples/withdraw-zero.md) — batch validation via withdrawal delegation
- [UTxO Indexer](examples/utxo-indexer.md) — O(1) input-output linking with redeemer indices
- [Tagged Output](examples/tagged-output.md) — double satisfaction prevention with crypto hashing
- [Validity Range](examples/validity-range.md) — interval normalisation for time-based validation
- [TVMP](examples/tvmp.md) — transaction-level validation via minting policy receipt tokens
- [Pool Restriction](examples/pool-restriction.md) — certificate-based delegation control with pool whitelist
- [Oracle Feed](examples/oracle-feed.md) — reference input authentication with NFT verification

**Phase 4 — Governance:**
- [Governance Vote](examples/governance-vote.md) — SPO voting authorization via `vote` handler
- [Governance Publish](examples/governance-publish.md) — DRep registration control via `publish` handler
- [Governance Propose](examples/governance-propose.md) — treasury withdrawal guardrails via `propose` handler

**Phase 5 — DeFi & Inheritance:**
- [Escrow](examples/escrow.md) — time-locked two-party exchange with refund/cancel
- [Dead Man's Switch](examples/dead-mans-switch.md) — proof-of-life inheritance with periodic check-in
- [Multi-Beneficiary](examples/multi-beneficiary.md) — percentage-based fund splitting for multiple heirs

**Phase 6 — Marketplace & DAO:**
- [Marketplace](examples/marketplace.md) — NFT listing/buying/cancelling with payment verification
- [DAO Vote](examples/dao-vote.md) — token-weighted governance voting with lock-until-deadline

**Phase 7 — Novel Patterns:**
- [Notary](examples/notary.md) — proof-of-existence document notarization (no Cardano equivalent exists)

## Production References

Open-source Aiken contracts for studying production-scale implementations.
These go beyond teaching patterns into real-world architecture:

**DEX Contracts (Audited, Production):**
- [Minswap DEX V2](https://github.com/minswap/minswap-dex-v2) — Constant product AMM with batching architecture. Order validators, pool validators, batcher flow. Shows how withdraw-zero trick scales to production DEX throughput.
- [Minswap Stableswap](https://github.com/minswap/minswap-stableswap) — Stableswap curve implementation in Aiken. Advanced math with the `rational` module.
- [SundaeSwap V3](https://github.com/SundaeSwap-finance/sundae-contracts) — DEX rewritten from Plutus to Aiken. Uses withdraw-zero (`stake.ak`) for order batching. Good example of `validators/` and `lib/` project structure at scale.

**Lending & DeFi (Audited, Production):**
- [Lenfi Smart Contracts](https://github.com/lenfiLabs/lenfi-smart-contracts) — Pooled lending protocol in Aiken. Oracle validator, pool management, liquidation. Audited by Anastasia Labs + TxPipe. Open source.
- [fallen-icarus P2P DeFi](https://github.com/fallen-icarus) — Full suite: [cardano-loans](https://github.com/fallen-icarus/cardano-loans) (P2P lending with credit histories, compound interest), [cardano-options](https://github.com/fallen-icarus/cardano-options) (options contracts), [cardano-swaps](https://github.com/fallen-icarus/cardano-swaps) (order-book DEX with atomic swaps). Aiken branches active.

**NFT & Marketplace:**
- [Nebula](https://github.com/spacebudz/nebula) (SpaceBudz) — NFT marketplace contract with bid/offer UTxO model, chain indexer, event listener. Production Aiken.

**DAO & Governance:**
- [Logical Mechanism](https://github.com/logical-mechanism) — "Distributed Representation" semi-liquid mint-lock-stake DAO. Also [Assist](https://github.com/logical-mechanism/Assist) library of specialized Aiken functions.

**Reusable Libraries:**
- [Anastasia Labs Design Patterns](https://github.com/Anastasia-Labs/aiken-design-patterns) — Importable library (`aiken add anastasia-labs/aiken-design-patterns --version v1.1.0`). Modules: merkelized validator, multi UTxO indexer, tx level minter, linked list (ordered/unordered), stake validator, parameter validation. Conway+ extensions planned.
- [SundaeSwap aicone](https://github.com/SundaeSwap-finance/aicone) — Reusable Aiken utility libraries.

**SDK Integration:**
- [MeshJS Contracts](https://github.com/MeshJS/mesh/tree/main/packages/mesh-contract/src) — Aiken contracts (escrow, marketplace, swap, vesting) with full TypeScript SDK integration. Shows the on-chain → off-chain bridge.

**Learning Resources:**
- [Awesome Aiken](https://github.com/aiken-lang/awesome-aiken) — Curated list of Aiken libraries, dApps, tutorials.
- [Aiken Official Docs](https://aiken-lang.org/fundamentals/getting-started) — Language fundamentals and common design patterns.
- [Cardano CTF](https://github.com/vacuumlabs/cardano-ctf) — 25 challenges teaching real exploit patterns against Plutus/Aiken validators.
