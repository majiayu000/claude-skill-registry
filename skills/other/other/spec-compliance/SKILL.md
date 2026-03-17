---
id: spec-compliance
title: Spec Compliance Skill
category: methodology
difficulty: intermediate
triggers:
  - ERC compliance
  - EIP check
  - standard compliance
  - token standard
  - ERC-20 compliance
  - ERC-721 compliance
related_skills:
  - solidity-scanner/SKILL.md
  - token-analyzer/SKILL.md
tags:
  - erc
  - eip
  - compliance
  - standards
last_updated: 2026-02-26
description: >-
  Verify smart contract implementations comply with EIP/ERC standards
  and protocol specifications. Use when checking ERC-20, ERC-721,
  ERC-1155, ERC-4626, or EIP-712 compliance, or when identifying
  non-standard token behavior that causes integration failures.
---

# Spec Compliance Skill

Verify smart contract implementations comply with EIP/ERC standards and protocol specifications. Non-compliant implementations cause integration failures, fund losses, and security vulnerabilities.

---

## Why Compliance Matters

| Impact of Non-Compliance | Example |
|--------------------------|----------|
| Integration failure | DEXs can't list non-standard ERC20 (missing `decimals()`) |
| Silent fund loss | ERC721 `safeTransferFrom` not calling `onERC721Received` = NFTs lost |
| Security vulnerability | EIP-712 without `chainId` = cross-chain signature replay |
| Accounting errors | ERC4626 wrong rounding direction = vault inflation attack |
| Ecosystem rejection | Bridges, wallets, indexers refuse non-standard tokens |

---

## Supported Standards

### Token Standards

| Standard | Type | Key Functions | Common Issues |
|----------|------|---------------|---------------|
| ERC-20 | Fungible token | `transfer`, `approve`, `transferFrom` | Missing return values, approve race |
| ERC-721 | Non-fungible token | `safeTransferFrom`, `approve`, `ownerOf` | Missing receiver callback |
| ERC-1155 | Multi-token | `safeTransferFrom`, `safeBatchTransferFrom` | Batch operation atomicity |
| ERC-4626 | Tokenized vault | `deposit`, `withdraw`, `convertToShares` | Rounding direction, first depositor attack |
| ERC-2612 | Permit (gasless approve) | `permit`, `nonces`, `DOMAIN_SEPARATOR` | Signature replay, frontrunning |

### Infrastructure Standards

| Standard | Type | Security Focus |
|----------|------|----------------|
| EIP-712 | Typed data signing | Domain separator, chain ID |
| EIP-1967 | Proxy storage slots | Standard slot locations |
| EIP-2535 | Diamond standard | Selector collision, storage isolation |
| EIP-4337 | Account abstraction | UserOp validation, paymaster trust |
| EIP-1153 | Transient storage | TSTORE/TLOAD lifecycle |
| EIP-2981 | Royalty info | Not enforceable (informational only) |

---

## Compliance Verification Approach

### 1. Interface Completeness

Does the contract implement ALL required functions with correct signatures?

```solidity
// ERC-20 REQUIRED interface (IERC20)
function totalSupply() external view returns (uint256);
function balanceOf(address account) external view returns (uint256);
function transfer(address to, uint256 amount) external returns (bool);
function allowance(address owner, address spender) external view returns (uint256);
function approve(address spender, uint256 amount) external returns (bool);
function transferFrom(address from, address to, uint256 amount) external returns (bool);

// ERC-20 REQUIRED events
event Transfer(address indexed from, address indexed to, uint256 value);
event Approval(address indexed owner, address indexed spender, uint256 value);

// OPTIONAL but expected by most integrations
function name() external view returns (string memory);
function symbol() external view returns (string memory);
function decimals() external view returns (uint8);
```

### 2. Behavioral Compliance

Does each function behave as specified? (Not just exist with the right signature)

### 3. Edge Case Handling

Does the implementation handle boundary conditions specified in the standard?

---

## Resources
- [ERC Standards](resources/erc-standards.md)
- [EIP Security](resources/eip-security.md)

## Workflows
- [Compliance Audit](workflows/compliance-audit.md)
