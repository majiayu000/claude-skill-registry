---
id: solidity-scanner
title: Solidity Scanner Skill
category: scanner
difficulty: intermediate
triggers:
  - solidity audit
  - smart contract security
  - EVM vulnerability
  - solidity scan
  - ethereum audit
related_skills:
  - methodology/SKILL.md
  - severity/SKILL.md
  - checklists/SKILL.md
  - patterns/SKILL.md
  - variant-analysis/SKILL.md
  - static-analysis/SKILL.md
  - exploit-forensics/SKILL.md
tags:
  - solidity
  - evm
  - scanner
  - security
last_updated: 2026-02-24
description: >-
  Use when the user wants to audit Solidity smart contracts for security
  vulnerabilities, scan EVM-compatible contracts for reentrancy, oracle
  manipulation, access-control, or flash-loan issues, review DeFi protocols on
  Ethereum, Arbitrum, Optimism, Base, Polygon, or BSC, or generate security
  audit reports for smart contract deployments.
---

# Solidity Scanner Skill

## Purpose

Analyze Solidity smart contracts for security vulnerabilities across all EVM-compatible chains. This is the primary scanner for the most widely-deployed smart contract language, covering DeFi, NFTs, governance, bridges, and all Ethereum-ecosystem protocols.

## Supported Chains

| Chain | EVM Compatibility | Key Differences |
|---|---|---|
| Ethereum | Full | Baseline — all patterns apply |
| Arbitrum | Full | L2 sequencer risk, `block.number` returns L1 block, gas pricing differs |
| Optimism / Base | Full | L2 sequencer risk, `TIMESTAMP` from L1, cross-domain messaging |
| Polygon | Full | Different gas token (MATIC), PoS consensus, reorg risk higher |
| BSC | Full | Lower gas costs enable different attack economics |
| Avalanche | Full | Subnet awareness, different finality model |
| Scroll | Full | zkEVM — some precompile differences |
| Linea | Full | zkEVM — some opcode cost differences |
| zkSync Era | Partial | Different address derivation, no `SELFDESTRUCT`, custom deployment model |
| Blast | Full | Native yield — `WETH.balance()` increases, rebasing assumptions |

### Chain-Specific Audit Considerations

When auditing for a specific chain, check these additional concerns:

```
Arbitrum/Optimism:
  ├── Sequencer downtime → oracle stale price risk
  ├── L1-to-L2 message delay → bridge timing attacks
  └── block.number semantics differ from L1

zkSync Era:
  ├── msg.value behaves differently in system contracts
  ├── Contract deployment uses CREATE2-like hash, not CREATE
  ├── Some opcodes unavailable or priced differently
  └── Native account abstraction changes tx.origin semantics

Blast:
  ├── ETH and USDB are rebasing tokens by default
  ├── Protocol must explicitly configure yield mode
  └── balanceOf(address) can change between transactions without transfers
```

## Detection Capabilities

### Critical / High Severity

| Category | Specific Patterns | Detection Method |
|---|---|---|
| **Reentrancy** | Classic single-function, cross-function, cross-contract, read-only, ERC777 callback, ERC721 callback | State write after external call analysis |
| **Access control** | Missing modifiers, `tx.origin` auth, unprotected `initialize()`, unprotected `selfdestruct`, privilege escalation | Public/external function modifier scan |
| **Unsafe external calls** | Unchecked `transfer()` return, unchecked low-level call, unchecked `approve()`, USDT non-standard behavior | Return value tracking |
| **Oracle manipulation** | Uniswap V2/V3 spot price, missing Chainlink staleness check, reserve-based pricing, circular pricing | Oracle usage pattern matching |
| **Flash loan vectors** | Balance-based pricing, single-tx manipulation, donation attacks | Balance-as-input detection |
| **Proxy vulnerabilities** | Uninitialized impl, storage collision, missing `_disableInitializers()`, UUPS auth bypass | Proxy pattern recognition |

### Medium Severity

| Category | Specific Patterns | Detection Method |
|---|---|---|
| **Integer issues** | Unsafe downcast, truncation on assignment, rounding errors in share math, first depositor inflation | `SafeCast` absence, division analysis |
| **Token handling** | Fee-on-transfer incompatibility, rebasing token assumption, non-standard decimals, approve race condition | Token interaction pattern scan |
| **MEV exposure** | Missing deadline, missing slippage protection, sandwich vulnerability, permit front-running | Swap/router call analysis |
| **Centralization** | Untimelocked admin powers, excessive owner privileges, upgradeable without governance | Admin function audit |
| **Signature issues** | Missing nonce, missing chainId, missing deadline, ecrecover zero-address, malleable signatures | Signature verification scan |
| **DoS vectors** | Unbounded loops, external call revert in batch, force-sent ETH breaking balance checks | Loop and batch analysis |

### Low / Informational

| Category | Specific Patterns |
|---|---|
| **Gas optimization** | Storage vs memory, redundant SLOADs, unchecked math for bounded loops, calldata vs memory |
| **Code quality** | Missing events, missing NatSpec, unused variables, floating pragma, unlocked compiler |
| **Best practices** | `block.timestamp` dependency, missing zero-address checks, magic numbers, missing error messages |

## Compiler Version Awareness

| Solidity Version | Key Security Considerations |
|---|---|
| < 0.8.0 | No built-in overflow protection — check for SafeMath usage |
| 0.8.0–0.8.12 | Built-in overflow but `unchecked` blocks bypass it — audit all `unchecked` usage |
| 0.8.13–0.8.14 | ABI encoder bug with nested arrays (fixed in 0.8.15) |
| 0.8.15–0.8.19 | Optimizer bug with `Yul` code (fixed in 0.8.20) |
| 0.8.20+ | Default EVM target = Shanghai (`PUSH0`) — may not deploy on all L2s |
| 0.8.24+ | Transient storage (`TSTORE`/`TLOAD`) available — new reentrancy guard patterns |
| 0.8.26+ | Custom storage layouts, event errors in interfaces |

## Workflows

| Workflow | Duration | Best For | Link |
|---|---|---|---|
| Quick Scan | 15–20 min | Triage, contest warm-up, initial assessment | [quick-scan.md](workflows/quick-scan.md) |
| Comprehensive Audit | 3–5 days | Protocol launch, client engagement, major upgrade | [comprehensive-audit.md](workflows/comprehensive-audit.md) |
| Competitive Audit | 8–16 hours | Code4rena, Sherlock, CodeHawks contests | [competitive-audit.md](workflows/competitive-audit.md) |

## Resources

| Resource | Purpose | Link |
|---|---|---|
| Vulnerability Patterns | Complete pattern catalog with code examples | [vulnerability-patterns.md](resources/vulnerability-patterns.md) |
| Severity Guide | Classification criteria with decision tree | [severity-guide.md](resources/severity-guide.md) |
| Tool Configs | Slither, Aderyn, Mythril, Semgrep setup | [tool-configs.md](resources/tool-configs.md) |
| False Positives | Common FPs with reasoning for each | [false-positives.md](resources/false-positives.md) |
| Foundry Security | 10 vulnerability categories with Foundry PoC tests | [foundry-security.md](resources/foundry-security.md) |
| Foundry Testing | Fuzz, invariant, fork, differential testing guide | [foundry-testing.md](resources/foundry-testing.md) |
| Foundry Cheatcodes | 150+ cheatcodes reference for security auditors | [foundry-cheatcodes.md](resources/foundry-cheatcodes.md) |
| Gas & Security | Gas optimization patterns with security trade-offs | [gas-security.md](resources/gas-security.md) |
| Foundry CI/CD | GitHub Actions for automated security testing | [foundry-ci-cd.md](resources/foundry-ci-cd.md) |

## Standard Audit Procedure

```
1. Load Solidity contract(s) and note compiler version
2. Map inheritance tree and external dependencies
3. Identify protocol type (DeFi, NFT, governance, bridge, etc.)
4. Select workflow based on engagement type
5. Run static analysis tools (Slither → Aderyn → Mythril)
6. Execute manual review per methodology
7. Classify each finding with severity guide
8. Run variant analysis on confirmed findings
9. Generate structured report
```

## Integration with Other Skills

| Skill | How Solidity Scanner Uses It |
|---|---|
| `methodology/` | Provides the audit methodology framework (phases, timing, approach) |
| `severity/` | Classifies each finding into Critical/High/Medium/Low |
| `scoring/` | Scores overall protocol security posture |
| `checklists/` | Protocol-specific security checklists (ERC-20, vault, AMM, etc.) |
| `patterns/` | Vulnerability pattern database for cross-reference |
| `variant-analysis/` | When one bug is found, hunt for all variants |
| `static-analysis/` | Tool configuration and integration |
| `exploit-forensics/` | Real-world exploit case studies for pattern awareness |
| `fix-review/` | Verify proposed fixes after initial audit |
| `differential-review/` | Compare upgraded contract versions |
| `chain-guides/` | Chain-specific considerations when target != Ethereum mainnet |

## Error Code Reference

Common Solidity/EVM error selectors and revert reasons encountered during audits. Use a selector decoder like [openchain.xyz](https://openchain.xyz/signatures) or [4byte.directory](https://www.4byte.directory/) to identify unknown selectors.

### OpenZeppelin Standard Errors

| Error Selector | Error Signature | Meaning |
|----------------|----------------|----------|
| `0xe450d38c` | `ERC20InsufficientBalance(address,uint256,uint256)` | Token balance too low for transfer |
| `0xfb8f41b2` | `ERC20InsufficientAllowance(address,uint256,uint256)` | Allowance too low for transferFrom |
| `0x118cdaa7` | `OwnableUnauthorizedAccount(address)` | Caller is not the owner |
| `0x1e4fbdf7` | `OwnableInvalidOwner(address)` | Invalid owner address (e.g., zero address) |
| `0xe602df05` | `ERC20InvalidApprover(address)` | Invalid address for approve |
| `0x94280d62` | `ERC20InvalidReceiver(address)` | Invalid receiver (zero address) |
| `0xd93c0665` | `EnforcedPause()` | Contract is paused |
| `0x8dfc202b` | `ExpectedPause()` | Contract is NOT paused (expected to be) |
| `0xa9fbf51f` | `AccessControlUnauthorizedAccount(address,bytes32)` | Missing role for access control |
| `0xd92e233d` | `ZeroAddress()` | Zero address provided where not allowed |

### ERC Standard Errors

| Error Selector | Error Signature | Meaning |
|----------------|----------------|----------|
| `0x7e273289` | `ERC721NonexistentToken(uint256)` | Token ID does not exist |
| `0x177e802f` | `ERC721InsufficientApproval(address,uint256)` | Not approved for token operation |
| `0x64283d7b` | `ERC721IncorrectOwner(address,uint256,address)` | Token not owned by expected address |
| `0xf0dd15fd` | `ERC4626ExceededMaxDeposit(address,uint256,uint256)` | Deposit exceeds vault max |
| `0x936941fc` | `ERC4626ExceededMaxRedeem(address,uint256,uint256)` | Redeem exceeds vault max |

### Common Revert Reasons (String)

| Revert String | Typical Source | Audit Significance |
|--------------|---------------|--------------------|
| `"ReentrancyGuard: reentrant call"` | OpenZeppelin ReentrancyGuard | Guard is active — check if all entry points are protected |
| `"Initializable: contract is already initialized"` | OZ proxy initializer | Re-initialization attempt — check `_disableInitializers()` |
| `"Address: low-level call failed"` | OZ Address library | External call failure — check error handling |
| `"SafeERC20: low-level call failed"` | OZ SafeERC20 | Token transfer failure — may indicate non-standard token |
| `"Pausable: paused"` / `"Pausable: not paused"` | OZ Pausable | Pause state mismatch — check centralization risk |
| `"ECDSA: invalid signature"` | OZ ECDSA | Signature verification failed — check for malleable sigs |
| `"ERC20: transfer amount exceeds balance"` | OZ ERC20 (pre-custom-errors) | Insufficient balance — older OZ version indicator |

### Proxy-Related Errors

| Error Selector | Error Signature | Meaning |
|----------------|----------------|----------|
| `0xb398979f` | `ERC1967InvalidImplementation(address)` | Invalid implementation address for proxy |
| `0x4c9c8ce3` | `ERC1967InvalidAdmin(address)` | Invalid admin address for transparent proxy |
| `0x7e2732890` | `ERC1967NonPayable()` | Proxy received ETH when not expected |
| `0xf92ee8a9` | `InvalidInitialization()` | OZ v5 Initializable — already initialized |
| `0xd7e6bcf8` | `NotInitializing()` | OZ v5 Initializable — not in initializing state |

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| Scanner loads generic patterns instead of Solidity-specific | Trigger phrases not matching the Solidity scanner | Verify `triggers` field in frontmatter matches user query; check TRIGGERS.md mapping |
| False positives on `unchecked` blocks | Scanner flags all unchecked math as unsafe | Check Solidity version — 0.8.x+ has built-in overflow; `unchecked` in bounded loops is safe |
| Missed reentrancy in cross-contract calls | Scanner only checks single-function reentrancy | Enable cross-contract analysis mode; load `patterns/` for read-only reentrancy patterns |
| Oracle manipulation not detected | Protocol uses custom oracle not matching known patterns | Manually check any `balanceOf()` or reserve-based pricing; add custom oracle pattern |
| L2-specific issues not flagged | Chain-specific guide not loaded | Load the appropriate `chain-guides/` file for the target L2 before scanning |
| Proxy storage collision missed | Scanner doesn't map storage layouts across proxy/impl | Use `differential-review/` skill to compare storage layouts; check for `_gap` variables |
| Too many low-severity findings | Scanning in paranoid mode | Switch to "Standard" scan profile; filter informational findings for final report |
