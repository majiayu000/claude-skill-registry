---
name: readme-writer
description: Guidelines for writing module READMEs that explain how a module works to developers who need to use it or understand its internals. Use when documenting a module, package, or subsystem.
---

# Module README Writing Guide

## File Placement

Place the README in the same folder as the module it explains, not at the package root.

```
# Good: README next to the module it documents
sequencer-client/src/sequencer/README.md
archiver/src/archiver/l1/README.md

# Also good: Package-level README for small packages
slasher/README.md
```

Use package-level READMEs when the package is small or you want to explain the package as a whole.

## Structure

### 1. Overview

Start with 2-4 sentences explaining what the module does and where it fits in the system.

```markdown
# L1 Transaction Utils

This module handles sending L1 txs, including simulating txs, choosing gas prices,
estimating gas limits, monitoring sent txs, speeding them up, and cancelling them.
Each instance of `L1TxUtils` is stateful, corresponds to a given publisher EOA,
and tracks its in-flight txs.
```

### 2. Usage Context

Explain when and how this module is used. Who calls it? Under what conditions?

```markdown
## Usage

The slasher is integrated into the Aztec node and activates when:
1. The node is configured as a validator
2. The validator is selected as proposer for a slot
3. Slashable offenses have been detected
```

### 3. Code Examples

For utility-like modules, include a code snippet showing typical usage:

```typescript
const versionManager = new version.VersionManager(DB_VERSION, rollupAddress, {
  dataDir: '/path/to/data',
  serviceName: 'my-database',
});

await versionManager.checkVersionAndHandle(
  async () => await initializeFreshDatabase(),
  async (oldVersion, newVersion) => await migrate(oldVersion, newVersion),
);
```

### 4. Core Concepts

Define domain-specific terms and objects (blocks, checkpoints, slots, proposals, offenses, etc.). Explain relationships between them.

```markdown
### Slot vs Block vs Checkpoint

- **Slot**: A fixed time window (e.g., 72 seconds) during which a proposer can build blocks
- **Block**: A single batch of transactions, executed and validated
- **Checkpoint**: The collection of all blocks built in a slot, attested by validators
```

### 5. Main API

List main methods without exhaustive parameter/return documentation. Focus on what each does:

```markdown
## API

- `sendTransaction`: Sends an L1 tx and returns the tx hash. Consumes a nonce.
- `monitorTransaction`: Monitors a sent tx and speeds up or cancels it.
- `sendAndMonitorTransaction`: Combines sending and monitoring in a single call.
```

### 6. State Lifecycle

Use tables to document object states and transitions:

```markdown
| From | To | Condition | Effect |
|-|-|-|-|
| `idle` | `sent` | `send_tx` | A new tx is sent and nonce is consumed |
| `sent` | `speed-up` | `stall_time exceeded` | Tx replaced with higher gas |
| `sent` | `mined` | `get_nonce(latest) > tx_nonce` | Tx confirmed |
```

### 7. Timing and Sequence

Use ASCII diagrams or tables for temporal flows:

```markdown
T=0s    Slot begins
T=0-2s  SYNCHRONIZING, PROPOSER_CHECK
T=2s    Start building Block 1
T=10s   Block 1 deadline, start Block 2
...
T=72s   Slot ends
```

For parallel operations, use multi-column timelines:

```markdown
Time | Proposer              | Validators
-----|----------------------|------------------
10s  | Finish Block 1       | (idle)
12s  |                      | Receive Block 1
18s  | Finish Block 2       | Re-executing Block 1
```

### 8. Dependencies

Explain what other modules this connects to:

```markdown
## Integration Flow

1. **Offense Detection**: Watchers emit `WANT_TO_SLASH_EVENT` when they detect violations
2. **Offense Collection**: SlashOffensesCollector stores offenses in SlasherOffensesStore
3. **Action Execution**: SequencerPublisher executes actions on L1
```

### 9. Error Handling

Dedicate a section to unhappy paths and how deviations are handled:

```markdown
## Handling Timing Variations

### Slow Initialization

If initialization completes at 3s instead of 2s:
- Block 1 has 1s less time (7s instead of 8s)
- Sub-slot deadlines remain fixed
- Still enough time to build, just with fewer transactions
```

### 10. Configuration

Document configuration options with their purpose and constraints:

```markdown
## Configuration

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `slotDuration` | 72s | Total time for checkpoint |
| `blockDuration` | 8s | Duration of each sub-slot |
```

Include considerations for how values relate to each other:

```markdown
The `slashingOffsetInRounds` needs to be strictly greater than the proof
submission window to be able to slash for epoch prunes or data withholding.
```

### 11. Security

Include when the module has security implications:

```markdown
## Vetoing

The slashing system includes a veto mechanism that allows designated vetoers
to block slash payloads during the execution delay period. This provides a
safety valve for incorrectly proposed slashes.
```

## Writing Style

### Explain Rationale

Don't just document what happens—explain why:

```markdown
# Bad
The last sub-slot is reserved for validator re-execution.

# Good
The last sub-slot is reserved for validator re-execution. Validators execute
blocks sequentially with a ~2s propagation delay. For the last block, there's
no next block to build while validators re-execute, so we must wait for them
to finish before collecting attestations.
```

### Avoid Subjective Qualifiers

```markdown
# Bad
This is a key aspect of the design with critical security implications.

# Good
This provides a safety valve for incorrectly proposed slashes.
```

### Be Succinct

```markdown
# Bad
It is important to note that the configuration values must satisfy certain
constraints which will be explained in detail in the following section.

# Good
These values must satisfy certain constraints (explained below).
```

### Include Only Relevant Sections

Not every module needs every section. Skip sections that don't apply:
- Small utilities don't need architecture sections
- Stateless modules don't need lifecycle tables
- Internal modules don't need usage examples
- Not everything has security implications

Ask yourself: "Does this section help someone understand or use this module?" If not, skip it.
