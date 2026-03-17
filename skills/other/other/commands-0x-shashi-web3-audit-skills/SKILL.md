---
id: commands
title: Commands Skill
category: interface
difficulty: beginner
triggers:
  - /audit
  - /scan
  - /checklist
  - /report
  - /severity
  - /patterns
  - /chain-guide
  - /fix-review
  - /variant
  - /exploit
related_skills:
  - solidity-scanner/SKILL.md
  - checklists/SKILL.md
  - report-writer/SKILL.md
  - severity/SKILL.md
  - patterns/SKILL.md
  - chain-guides/SKILL.md
  - fix-review/SKILL.md
  - variant-analysis/SKILL.md
tags:
  - commands
  - interface
  - workflow
last_updated: 2026-02-26
description: >-
  Structured command patterns for invoking audit capabilities through
  slash commands. Use when triggering /audit, /scan, /checklist, /report,
  /severity, /patterns, or other slash commands that map to underlying
  skills and load the correct context for each workflow.
---

# Commands Skill

## Purpose

Provides structured command patterns for invoking audit capabilities through the plugin. Each command maps to one or more underlying skills, loads the correct context, and executes the appropriate workflow.

## Command Reference

### `/audit <contract|directory>`

**Purpose**: Run a full comprehensive security audit.

| Parameter | Required | Example | Description |
|---|---|---|---|
| `<target>` | Yes | `Vault.sol`, `src/` | Contract file or directory to audit |
| `--chain` | No | `ethereum`, `arbitrum` | Target chain (default: ethereum) |
| `--type` | No | `defi`, `nft`, `bridge` | Protocol type for checklist selection |
| `--depth` | No | `quick`, `comprehensive` | Audit depth (default: comprehensive) |

**Skills invoked**: `solidity-scanner` → `methodology/comprehensive-audit` → `checklists` → `report-writer`

**Example**:
```
/audit src/Vault.sol --chain arbitrum --type defi
```

**Output**: Full audit report with findings grouped by severity, root cause analysis, PoC code, and fix recommendations.

---

### `/scan <contract>`

**Purpose**: Fast 15–20 minute vulnerability scan for triage or contest warm-up.

| Parameter | Required | Example | Description |
|---|---|---|---|
| `<target>` | Yes | `Token.sol` | Contract file to scan |
| `--focus` | No | `reentrancy`, `access` | Narrow scan to specific area |

**Skills invoked**: `solidity-scanner/workflows/quick-scan` → `severity/SKILL.md`

**Example**:
```
/scan src/LendingPool.sol --focus reentrancy
```

**Output**: Prioritized list of potential vulnerabilities with severity estimates and quick-fix suggestions.

---

### `/checklist <protocol-type>`

**Purpose**: Load a protocol-specific security checklist.

| Parameter | Required | Example | Description |
|---|---|---|---|
| `<type>` | Yes | `erc20`, `erc4626`, `amm`, `lending`, `bridge` | Protocol or token standard |
| `--format` | No | `markdown`, `interactive` | Output format |

**Available checklists**:

| Type | Description | Items |
|---|---|---|
| `erc20` | ERC-20 token compliance + security | Transfer, approval, supply checks |
| `erc721` | NFT contract security | Minting, ownership, royalty checks |
| `erc4626` | Tokenized vault security | Share math, first depositor, inflation |
| `amm` | Automated market maker | Slippage, oracle, MEV, pool manipulation |
| `lending` | Lending protocol | Liquidation, interest, collateral, oracle |
| `bridge` | Cross-chain bridge | Message verification, replay, finality |
| `governance` | DAO governance | Flash loan voting, quorum, timelock |
| `staking` | Staking contracts | Reward calculation, withdrawal, unbonding |
| `proxy` | Upgradeable contracts | Storage layout, initialization, access |

**Skills invoked**: `checklists/` → protocol-specific checklist file

**Example**:
```
/checklist erc4626
```

---

### `/report`

**Purpose**: Generate formatted audit report from collected findings.

| Parameter | Required | Example | Description |
|---|---|---|---|
| `--format` | No | `markdown`, `pdf`, `json` | Report format (default: markdown) |
| `--template` | No | `standard`, `contest`, `client` | Report template |
| `--include-gas` | No | flag | Include gas optimization findings |

**Skills invoked**: `report-writer/SKILL.md`

**Output structure**:
```
1. Executive Summary
2. Scope and Methodology
3. Findings (Critical → High → Medium → Low → Informational)
4. Each finding: Title, Severity, Description, Impact, PoC, Recommendation
5. Appendix: Tool outputs, gas analysis
```

**Example**:
```
/report --format markdown --template contest
```

---

### `/severity <finding-description>`

**Purpose**: Classify a finding's severity using structured criteria.

| Parameter | Required | Example | Description |
|---|---|---|---|
| `<description>` | Yes | "unchecked return value in withdraw" | Brief description of the finding |
| `--context` | No | "vault holds 10M USDC" | Additional context for severity |

**Skills invoked**: `severity/SKILL.md` → `scoring/SKILL.md`

**Assessment criteria applied**:
1. **Impact**: What can go wrong? (fund loss, DoS, governance)
2. **Likelihood**: How likely is exploitation? (attacker cost, prerequisites)
3. **Scope**: Who is affected? (single user, all users, protocol)
4. **Existing mitigations**: Any guards already in place?

**Example**:
```
/severity "reentrancy in withdraw() allows drain" --context "vault holds 10M USDC"
```

**Output**: Severity rating (Critical/High/Medium/Low) with detailed justification and comparable historical findings.

---

### `/patterns <category>`

**Purpose**: Browse the vulnerability pattern catalog for a specific category.

| Parameter | Required | Example | Description |
|---|---|---|---|
| `<category>` | Yes | `reentrancy`, `oracle`, `access`, `token`, `math` | Pattern category |
| `--chain` | No | `solana`, `move` | Chain-specific patterns |

**Available categories**:

| Category | Patterns Covered |
|---|---|
| `reentrancy` | Single, cross-function, cross-contract, read-only, ERC777, ERC721 |
| `oracle` | Spot price, stale price, reserve-based, circular dependency, decimal mismatch |
| `access` | Missing modifier, unprotected init, wrong role, delegatecall bypass |
| `token` | Fee-on-transfer, rebasing, non-standard decimals, approve race, blacklist |
| `math` | Rounding, first depositor, precision loss, overflow, fee calculation |
| `mev` | Sandwich, missing deadline, missing slippage, permit front-running |
| `signature` | Replay, malleable, missing nonce, missing chainId, ecrecover zero |
| `proxy` | Storage collision, uninitialized impl, UUPS missing guard, selector clash |
| `dos` | Unbounded loop, external call revert, griefing, self-destruct force-send |

**Skills invoked**: `patterns/SKILL.md` → `variant-analysis/resources/variant-patterns.md`

**Example**:
```
/patterns reentrancy
```

---

### `/chain-guide <chain>`

**Purpose**: Load chain-specific security considerations and audit context.

| Parameter | Required | Example | Description |
|---|---|---|---|
| `<chain>` | Yes | `ethereum`, `solana`, `move`, `cosmos` | Target chain |
| `--focus` | No | `gas`, `consensus`, `bridges` | Specific area within chain |

**Supported chains**:

| Chain | Scanner | Key Differences |
|---|---|---|
| Ethereum / EVM | `solidity-scanner/` | Baseline — reentrancy, MEV, gas |
| Solana | `solana-scanner/` | Account model, PDA, CPI, no reentrancy guard |
| Move (Aptos/Sui) | `move-scanner/` | Resource model, abilities, module publish |
| Cairo (Starknet) | `cairo-scanner/` | Felt252, storage proofs, Sierra |
| CosmWasm | `cosmos-scanner/` | IBC, message handling, gas metering |
| Fuel (Sway) | `fuel-scanner/` | UTXO, predicates, scripts |
| TON (FunC/Tact) | `ton-scanner/` | Actor model, async messages, bouncing |
| Aztec (Noir) | `aztec-scanner/` | Privacy, encrypted state, kernel proofs |

**Skills invoked**: `chain-guides/` → chain-specific scanner `SKILL.md`

**Example**:
```
/chain-guide solana --focus accounts
```

---

### `/fix-review <finding-id>`

**Purpose**: Review a proposed fix to verify it correctly addresses the vulnerability.

| Parameter | Required | Example | Description |
|---|---|---|---|
| `<finding>` | Yes | `H-01`, `reentrancy in withdraw` | Finding ID or description |
| `--diff` | No | `fix-branch..main` | Git diff to review |

**Skills invoked**: `fix-review/SKILL.md` → `variant-analysis/SKILL.md`

**Checks performed**:
1. Root cause addressed (not just symptom)
2. No new vulnerabilities introduced
3. All variant instances also fixed
4. Edge cases covered
5. Tests added for the vulnerability
6. No regressions to existing functionality

**Example**:
```
/fix-review H-01 --diff fix/reentrancy..main
```

---

### `/variant <bug-description>`

**Purpose**: Run variant analysis from a known bug to find all related instances.

| Parameter | Required | Example | Description |
|---|---|---|---|
| `<description>` | Yes | "reentrancy in withdraw()" | Bug description to hunt variants for |
| `--scope` | No | `all`, `contract`, `module` | Search scope (default: all) |

**Skills invoked**: `variant-analysis/SKILL.md` → `variant-analysis/workflows/variant-hunt.md`

**Example**:
```
/variant "unchecked return value in transfer" --scope all
```

---

### `/exploit <protocol-name>`

**Purpose**: Load historical exploit forensics for a protocol or exploit category.

| Parameter | Required | Example | Description |
|---|---|---|---|
| `<name>` | Yes | `euler`, `curve`, `reentrancy` | Protocol name or exploit category |

**Skills invoked**: `exploit-forensics/` → specific case study file

**Example**:
```
/exploit euler
```

---

## Command Chaining

Commands can be logically chained for complex workflows:

```
/scan Vault.sol                          → Find initial vulnerabilities
/variant "reentrancy in withdraw()"      → Find all variants
/severity "reentrancy across 3 functions" → Classify aggregate severity
/report --template contest               → Generate contest submission
```

## Error Handling

| Error | Response |
|---|---|
| Unknown command | Suggest closest matching command |
| Missing required parameter | Prompt with parameter description and example |
| Unsupported chain | List all supported chains |
| No findings found | Report clean result with confidence level and areas covered |
| File not found | Prompt for correct path with workspace file listing |

## Resources
- [Implementation Guide](resources/implementation-guide.md)
