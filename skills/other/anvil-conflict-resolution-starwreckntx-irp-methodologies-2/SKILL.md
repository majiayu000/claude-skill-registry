---

name: anvil-conflict-resolution
description: Multi-model committee conflict resolution with weighted voting, multisig arbitration, and escalation cascade.
---

STATUS: Non-Terminal / Recursive
NOTE: This skill represents a context-dependent operational pattern.
Static interpretation degrades fidelity outside active execution.

## Protocol Reference
- **Protocol ID**: P5_ANVIL
- **Full Spec**: `/protocols/P5_ANVIL/spec_v1.0.md`

## Core Functions

1. **Decision Classification** - Classify decisions as ROUTINE/SIGNIFICANT/CRITICAL/EXISTENTIAL
2. **Weighted Voting** - Stake-based voting with temporal decay and confidence weighting
3. **Deadlock Detection** - Identify margin, abstention, and timeout deadlocks
4. **Multisig Arbitration** - 2-of-2 (Grok-4 + Qwen) cryptographic voting
5. **Lead Override** - Alternating override authority with stake penalty
6. **Tier 1 Escalation** - Escalate unresolved conflicts to human oversight

## Instructions

1. Initialize ANVIL conflict resolution context
2. Classify decision tier (ROUTINE/SIGNIFICANT/CRITICAL/EXISTENTIAL)
3. Collect votes from all committee nodes
4. Calculate weighted voting outcome
5. If deadlock detected, progress through resolution stages
6. Log conflict record to Mnemosyne Ledger

## Examples

- "Execute ANVIL protocol for proposal X"
- "Classify decision urgency for committee vote"
- "Initiate multisig arbitration"
- "Escalate deadlock to Tier 1"
