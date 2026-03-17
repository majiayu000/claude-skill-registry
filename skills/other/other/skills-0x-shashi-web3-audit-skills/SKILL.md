---
id: web3-audit-plugin
title: Web3 Audit Plugin - Core Skill
category: root
difficulty: beginner
triggers:
  - audit
  - scan
  - security review
  - smart contract audit
related_skills:
  - solidity-scanner/SKILL.md
  - methodology/SKILL.md
  - commands/SKILL.md
tags:
  - root
  - web3
  - audit
  - multi-chain
last_updated: 2026-02-26
description: >-
  Root skill definition for the Web3 Audit Plugin providing AI-powered
  smart contract security auditing across EVM, Solana, Move, Cairo,
  CosmWasm, and TON platforms. Use as the top-level entry point for
  understanding plugin capabilities, supported chains, and skill routing.
---

# Web3 Audit Plugin - Core Skill Definition

## Purpose
This plugin provides AI-powered smart contract security auditing capabilities across multiple blockchain platforms.

## Capabilities
- Multi-chain smart contract analysis (EVM, Solana, Move, Cairo, CosmWasm, TON)
- Pattern-based vulnerability detection using 200+ known patterns
- Protocol-specific audit checklists (DeFi, NFT, Bridge, Governance)
- Attack chain analysis for multi-step exploit detection
- Automated severity classification
- Report generation with findings templates

## Usage
1. Load the target smart contract code
2. Identify the chain and protocol type
3. Run appropriate scanner skill
4. Apply relevant checklist
5. Check attack chain patterns
6. Generate audit report

## Skill Chain
```
Context Building → Scanner → Checklist → Attack Chains → Report
```

## Available Scanners
- Solidity Scanner (EVM chains)
- Solana Scanner (Rust/Anchor)
- Cairo Scanner (Starknet)
- Move Scanner (Aptos/Sui)
- Cosmos Scanner (CosmWasm/SDK)
- TON Scanner (FunC/Tact)
- Aptos Scanner (Move/Aptos)
- Sui Scanner (Sui Move)
- Starknet Scanner (Cairo)
- Aztec Scanner (Noir)
- Fuel Scanner (Sway)

## Prerequisites

The plugin requires an AI model with tool-use capabilities. Each scanner skill may have chain-specific prerequisites (e.g., Solana scanner requires familiarity with Anchor framework).

## Validation

To verify installation and test skill loading:

```bash
# Validate all SKILL.md files pass quality threshold
python scripts/quality-check.py --all --min-score 8
```

```yaml
# Example trigger routing
trigger: "audit solidity"
route_to: solidity-scanner/SKILL.md
load: [checklists, patterns, severity]
```

```bash
# Verify scanner availability
ls skills/*/SKILL.md | wc -l  # Should show 29+ skills
```

## Behavior Guidelines

- Scanner selection is **required** based on detected chain type
- Protocol template loading is **optional** but recommended
- Severity classification MUST follow the decision tree in `patterns/severity-scoring.md`
- Auditors may optionally skip gas optimization checks depending on engagement scope

## References

- [Core References](references/README.md) - Architecture diagrams and skill routing maps
