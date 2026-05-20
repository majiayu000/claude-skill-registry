---
id: attack-chains
title: Attack Chains Skill
category: advanced
difficulty: advanced
triggers:
  - attack chain
  - multi-step exploit
  - exploit sequence
  - chain attack
  - combined vulnerabilities
related_skills:
  - advanced/context-detection/SKILL.md
  - patterns/SKILL.md
  - exploit-forensics/SKILL.md
tags:
  - attack-chains
  - exploits
  - multi-step
  - advanced
last_updated: 2026-02-26
description: >-
  Detect multi-step exploit sequences where individual steps may appear
  benign but combine into critical vulnerabilities. Use when analyzing
  protocols for flash-loan-to-governance chains, oracle manipulation
  sequences, or cross-contract re-entrancy paths inspired by real-world
  exploits like Ronin, Wormhole, and Beanstalk.
---

# Attack Chains Skill

## Purpose
Detect multi-step exploit sequences where individual steps may appear benign but combine into critical vulnerabilities. Real-world exploits rarely use a single vulnerability — they chain multiple issues together.

## Why Attack Chains Matter
- $624M Ronin Bridge: Social engineering → Key compromise → Validator threshold bypass → Fund drain
- $326M Wormhole: Signature verification bypass → Fake VAA → Unauthorized minting
- $182M Beanstalk: Flash loan → Governance vote → Proposal execution → Fund drain
- $130M Cream Finance: Flash loan → Oracle manipulation → Under-collateralized borrow → Drain

## Chain Types
| Chain | Description | File |
|-------|-------------|------|
| Flash Loan | Flash loan enables price/governance manipulation | [flash-loan-chains.md](flash-loan-chains.md) |
| Oracle | Oracle distortion enables economic exploits | [oracle-chains.md](oracle-chains.md) |
| Bridge | Cross-chain verification bypass chains | [bridge-chains.md](bridge-chains.md) |
| Governance | Vote manipulation and proposal hijacking | [governance-chains.md](governance-chains.md) |

## Detection Approach
1. **Identify entry points**: Flash loans, large token transfers, governance proposals
2. **Trace data flow**: Follow manipulated values through the system
3. **Check invariants**: Verify economic invariants hold under manipulation
4. **Simulate chains**: Walk through multi-step sequences mentally or in tests

## Severity
Attack chains are almost always **Critical** or **High** severity because they represent complete exploit paths.

## Prerequisites

Attack chain analysis requires familiarity with individual vulnerability types. The [Patterns](../../patterns/) skill MUST be loaded first. Flash loan chains additionally require understanding of DeFi composability.

## Validation

To verify attack chain detection, test against known exploit reproductions:

```solidity
// Example: Flash loan attack chain detection pattern
// Step 1: Flash loan entry
function attack() external {
    ILendingPool(pool).flashLoan(address(this), token, amount, "");
}
// Step 2: Price manipulation during callback
function executeOperation(address, uint256 amount, uint256 fee, bytes calldata) external {
    // Manipulate oracle price
    IOracle(oracle).update(manipulatedPrice);
    // Step 3: Exploit manipulated state
    IVault(vault).borrow(collateral, inflatedAmount);
    // Step 4: Restore and repay
    IERC20(token).transfer(pool, amount + fee);
}
```

```python
# Validate chain detection coverage
known_chains = ["flash-loan", "oracle", "bridge", "governance"]
for chain in known_chains:
    assert chain_detector.can_detect(chain), f"Missing detection for {chain}"
```

```bash
# Run chain pattern matching tests
python -m pytest tests/attack_chains/ -v
```

## Behavior Guidelines

- Chain analysis MUST consider all entry points (flash loans, large transfers, governance proposals)
- Auditors should optionally model economic profitability of detected chains
- Cross-contract interactions are **required** to be traced through all delegate calls

## References

- [Attack Chains References](references/README.md) - Historical exploit timelines and chain diagrams
