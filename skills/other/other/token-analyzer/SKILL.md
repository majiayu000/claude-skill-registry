---
id: token-analyzer
title: Token Analyzer Skill
category: analysis
difficulty: intermediate
triggers:
  - analyze token
  - token review
  - erc20 check
  - fee on transfer
  - rebasing token
  - token integration
related_skills:
  - solidity-scanner/SKILL.md
  - patterns/SKILL.md
  - checklists/SKILL.md
tags:
  - token
  - erc20
  - erc721
  - erc1155
  - integration
last_updated: 2026-02-26
description: >-
  Analyze ERC20/ERC721/ERC1155 token implementations for non-standard
  behavior, fee-on-transfer mechanics, rebasing logic, blacklists,
  pausability, and integration risks. Use when reviewing protocols that
  interact with external tokens or implementing token-related features.
---

# Token Analyzer Skill

## Purpose
Analyze ERC20/ERC721/ERC1155 token implementations for non-standard behavior, fee-on-transfer mechanics, rebasing logic, and integration risks.

## Detection Capabilities
- Fee-on-transfer tokens (deflationary)
- Rebasing tokens (elastic supply)
- Tokens with blacklists/whitelists (USDC, USDT)
- Tokens with pausable transfers
- Tokens with max transaction limits
- Missing return values (USDT-style)
- Tokens with callback hooks (ERC777)
- Tokens returning false instead of reverting
- Approval race conditions
- Double-entry point tokens (tusd-style)
- Tokens with admin mint/burn

## Why This Matters
Over $500M has been lost due to protocol assumptions about "standard" ERC20 behavior. Most tokens deviate from the standard in subtle ways that break DeFi integrations.

## Resources
- [Integration Patterns](resources/integration-patterns.md)
- [Weird Tokens List](resources/weird-tokens-list.md)

## Workflows
- [Token Analysis](workflows/token-analysis.md)

## Prerequisites

Token analysis requires the [Solidity Scanner](../solidity-scanner/SKILL.md) for EVM token implementations. Non-EVM token analysis may require chain-specific scanner skills.

## Validation

To verify token detection capabilities, test against known weird tokens:

```solidity
// Example: Detecting fee-on-transfer behavior
interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

// Detection pattern: balance before/after comparison
uint256 balanceBefore = token.balanceOf(address(this));
token.transferFrom(sender, address(this), amount);
uint256 received = token.balanceOf(address(this)) - balanceBefore;
// If received < amount → fee-on-transfer detected
assert(received == amount); // Will fail for deflationary tokens
```

```python
# Validate token categorization
def test_weird_token_detection():
    categories = ['fee-on-transfer', 'rebasing', 'blacklist', 'pausable', 'missing-return']
    for cat in categories:
        assert token_analyzer.can_detect(cat), f"Missing detection: {cat}"
    print("All token categories verified")
```

```yaml
# Token risk scoring
token: USDT
risks:
  - missing_return_value: true   # Does not return bool
  - blacklist: true              # Admin can freeze addresses
  - pausable: true               # Admin can pause transfers
risk_level: medium
```

## Behavior Guidelines

- Token analysis MUST check all integration points where external tokens are received
- Fee-on-transfer detection is **required** for any DeFi protocol handling arbitrary ERC20s
- Rebasing token checks may optionally be skipped if the protocol explicitly disallows them
- Missing return value handling ALWAYS needs verification (USDT compatibility)
