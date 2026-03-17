---
id: protocol-templates
title: Protocol Templates Skill
category: advanced
difficulty: intermediate
triggers:
  - protocol template
  - audit template
  - amm template
  - lending template
  - bridge template
  - governance template
related_skills:
  - advanced/context-detection/SKILL.md
  - checklists/SKILL.md
  - patterns/SKILL.md
tags:
  - templates
  - protocol-specific
  - checklists
  - advanced
last_updated: 2026-02-26
description: >-
  Structured, protocol-type-specific audit templates enumerating the exact
  checks, invariants, and attack vectors relevant to each protocol category.
  Use when auditing AMM/DEX, lending, bridge, governance, or vault protocols
  to load targeted checklists based on context detection results.
---

# Protocol Templates Skill

## Purpose
Provide structured, protocol-type-specific audit templates that enumerate the exact checks, invariants, and attack vectors relevant to each protocol category. These templates are loaded based on context detection.

## Available Templates

| Template | Protocol Type | Key Focus Areas |
|----------|--------------|-----------------|
| [AMM/DEX](amm-dex-template.md) | Uniswap, Curve, Balancer-style | Price manipulation, LP attacks, MEV |
| [Bridge](bridge-template.md) | Cross-chain bridges | Message verification, replay, accounting |
| [Lending](lending-template.md) | Aave, Compound-style | Oracle, liquidation, interest rates |
| [NFT Marketplace](nft-marketplace-template.md) | OpenSea, Blur-style | Order validation, royalties, signatures |
| [Staking](staking-template.md) | Lido, RocketPool-style | Reward distribution, withdrawal, delegation |

## Template Structure
Each template follows a consistent format:
1. **Protocol Overview**: What the protocol does
2. **Architecture Checklist**: Structural checks
3. **Invariants**: Mathematical properties that must hold
4. **Attack Vectors**: Known exploits for this protocol type
5. **Critical Functions**: Functions requiring deepest review
6. **Integration Risks**: External dependency risks
7. **Economic Considerations**: Game theory and incentive analysis

## Usage
1. Context detection identifies protocol type
2. Appropriate template is loaded
3. Auditor follows template checklist systematically
4. Findings tagged with template category for standardized reporting

## Prerequisites

Protocol templates require [Context Detection](../context-detection/SKILL.md) for automatic loading. Manual template selection is also supported.

## Validation

To verify template coverage, validate against known protocol types:

```python
# Validate template completeness
required_sections = ["Overview", "Architecture Checklist", "Invariants", "Attack Vectors", "Critical Functions"]
for template in templates:
    for section in required_sections:
        assert section in template.sections, f"{template.name} missing {section}"
```

```yaml
# Example template loading configuration
detected_type: amm-dex
confidence: 0.92
loaded_templates:
  - amm-dex-template.md
  - defi-patterns.md
checklist: dex-amm-checklist
```

```bash
# Test template file integrity
for f in *-template.md; do echo "Validating $f"; head -5 "$f"; done
```

## Behavior Guidelines

- Template loading is **required** when context detection confidence exceeds 0.8
- Auditors MUST verify that all invariants in the template are tested
- Custom template sections may optionally be added for novel protocol designs

## References

- [Protocol Templates References](references/README.md) - Template customization guides and architecture patterns
