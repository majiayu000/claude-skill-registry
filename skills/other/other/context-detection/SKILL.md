---
id: context-detection
title: Context Detection Skill
category: advanced
difficulty: intermediate
triggers:
  - detect protocol
  - identify protocol type
  - auto detect
  - context detection
  - protocol classification
related_skills:
  - advanced/protocol-templates/SKILL.md
  - checklists/SKILL.md
  - patterns/SKILL.md
tags:
  - detection
  - automation
  - protocol-classification
last_updated: 2026-02-26
description: >-
  Automatically identify the type of protocol being audited to load
  appropriate checklists, templates, and vulnerability patterns without
  manual configuration. Use when starting any new audit to classify the
  protocol (DeFi lending, AMM, bridge, governance, etc.) and surface
  the most relevant checks.
---

# Context Detection Skill

## Purpose
Automatically identify the type of protocol being audited to load appropriate checklists, templates, and vulnerability patterns without manual configuration.

## Detection Signals

### DeFi Lending Protocol
```
Signals:
- Functions: deposit, withdraw, borrow, repay, liquidate
- State: collateralFactor, borrowRate, totalBorrows, totalReserves
- Imports: InterestRateModel, PriceOracle
- Patterns: health factor calculations, LTV ratios
→ Load: lending-template, defi-lending-checklist, oracle-chains
```

### DEX / AMM
```
Signals:
- Functions: swap, addLiquidity, removeLiquidity, getAmountOut
- State: reserve0, reserve1, totalLiquidity, fee
- Imports: IUniswapV2Pair, IUniswapV3Pool
- Patterns: constant product (x*y=k), concentrated liquidity, tick math
→ Load: amm-dex-template, dex-amm-checklist, flash-loan-chains
```

### Bridge
```
Signals:
- Functions: sendMessage, receiveMessage, relayMessage, verifyProof
- State: nonce, messageHash, guardians, threshold
- Imports: MessageVerifier, CrossChainMessenger
- Patterns: lock-mint-burn-unlock, validator signatures
→ Load: bridge-template, bridge-checklist, bridge-chains
```

### Governance
```
Signals:
- Functions: propose, vote, execute, queue, cancel
- State: proposals, votingPower, quorum, timelock
- Imports: GovernorAlpha, GovernorBravo, TimelockController
- Patterns: proposal lifecycle, voting snapshots, delegation
→ Load: governance-checklist, governance-chains
```

### Staking
```
Signals:
- Functions: stake, unstake, claim, getReward
- State: rewardRate, rewardPerToken, totalStaked
- Imports: StakingRewards, MasterChef
- Patterns: reward accumulation per share, lock periods
→ Load: staking-template, staking-checklist
```

### NFT / Gaming
```
Signals:
- Functions: mint, burn, tokenURI, onERC721Received
- State: tokenId, baseURI, maxSupply, royaltyInfo
- Imports: ERC721, ERC1155, VRF
- Patterns: merkle proof minting, reveal mechanics, randomness
→ Load: nft-marketplace-template, nft-gaming-checklist
```

### Vault / Yield
```
Signals:
- Functions: deposit, withdraw, harvest, compound
- State: totalAssets, totalShares, strategy
- Imports: ERC4626, Strategy
- Patterns: share/asset conversion, yield strategies
→ Load: defi-patterns, staking-checklist
```

## Detection Algorithm
1. Scan all contract interfaces (function signatures)
2. Scan import statements
3. Scan state variable names
4. Match against known protocol type signatures
5. Return ranked list of protocol types with confidence scores
6. Load templates for highest-confidence match

## Multiple Protocol Types
Many protocols combine multiple types (e.g., lending + staking + governance). When multiple types detected:
1. Load ALL matching templates
2. Prioritize by detection confidence
3. Add cross-module interaction checks
4. Apply comprehensive checklist as baseline

## Prerequisites

Context detection requires access to contract source code or verified ABI. The detection algorithm MUST have function signature databases loaded.

## Validation

To verify detection accuracy, test against known protocol types:

```python
# Validate detection signals
def test_lending_detection():
    signals = detect_protocol("contracts/LendingPool.sol")
    assert signals['type'] == 'lending'
    assert signals['confidence'] > 0.85
    print(f"Detection verified: {signals['type']} ({signals['confidence']:.2f})")
```

```yaml
# Expected detection outcome for Uniswap V2 Pair
input: UniswapV2Pair.sol
expected:
  type: amm-dex
  confidence: 0.95
  signals: [swap, addLiquidity, reserve0, reserve1]
  templates: [amm-dex-template, dex-amm-checklist]
```

```bash
# Run detection test suite
python -m pytest tests/context_detection/ -v
```

## Behavior Guidelines

- Detection MUST run before loading any protocol-specific templates
- Protocols with confidence below 0.5 should use the comprehensive checklist as fallback
- Multi-type protocols ALWAYS load all matching templates
- Manual override is optionally available when automated detection is uncertain

## References

- [Context Detection References](references/README.md) - Function signature databases and classification trees
