---
id: variant-analysis
title: Variant Analysis Skill
category: methodology
difficulty: advanced
triggers:
  - variant analysis
  - find all instances
  - same bug pattern
  - root cause search
  - bug class
related_skills:
  - variant-analysis/workflows/variant-hunt.md
  - variant-analysis/resources/variant-patterns.md
  - cyfrin-findings/SKILL.md
  - patterns/SKILL.md
tags:
  - variant-analysis
  - methodology
  - patterns
  - root-cause
last_updated: 2026-02-26
description: >-
  Systematically hunt for every variant of a discovered vulnerability
  across the entire codebase. Use when a bug is found and all instances
  of the same root cause pattern must be identified, or when performing
  variant analysis during competitive audits on Code4rena or Sherlock.
---

# Variant Analysis Skill

## Purpose

When you find one vulnerability, systematically hunt for **every variant** of the same root cause across the entire codebase. Variant analysis is the difference between finding 1 bug and finding 5–15 bugs from a single discovery. Elite auditors use this skill to multiply their finding count and provide comprehensive coverage.

## Why Variant Analysis Matters

| Situation | Without Variant Analysis | With Variant Analysis |
|---|---|---|
| Found unchecked return in `withdraw()` | Report 1 finding | Search all external calls → find 4 more instances → 5 findings |
| Found missing access control on `setFee()` | Report 1 finding | Check all admin functions → find `setPause()`, `setOracle()` unprotected → 3 findings |
| Found reentrancy in `claim()` | Report 1 finding | Check all state-changing functions with external calls → find `liquidate()` also vulnerable → 2 findings |
| Found rounding error in `deposit()` | Report 1 finding | Check all division operations → find `withdraw()`, `getExchangeRate()` → 3 findings |

**Real-world data**: Analysis of Code4rena and Sherlock contest results shows that top auditors consistently find 2–5x more instances of a bug class than median auditors, primarily through systematic variant analysis.

## Core Concept

```
Found Bug → Abstract to Pattern → Search Entire Codebase → Validate Each Match → Report All Variants
```

### The Abstraction Ladder

Moving from a specific bug to a general pattern:

```
Level 0 (Specific):    "withdraw() doesn't check IERC20.transfer return value"
Level 1 (Function):    "unchecked return value on token transfer"
Level 2 (Category):    "unchecked external call return value"
Level 3 (Root Cause):  "missing validation of external interaction result"
Level 4 (Universal):   "missing input/output validation"
```

**Optimal search level**: Level 2–3. Too specific (Level 0–1) misses variants. Too broad (Level 4) produces too many false positives.

## Variant Dimensions

A single root cause can manifest across multiple dimensions:

### 1. Same Function, Different Contracts

```
Found: Missing slippage check in PoolA.swap()
Search: All contracts with swap() functions
Result: PoolB.swap(), PoolC.swap() also missing slippage check
```

### 2. Same Root Cause, Different Functions

```
Found: Reentrancy in withdraw()
Search: All functions that make external calls before state updates
Result: claim(), liquidate(), flashLoan() also have CEI violations
```

### 3. Same Pattern, Different Manifestation

```
Found: Oracle price can be manipulated via flash loan
Search: All places where spot prices are used for critical calculations
Result: Liquidation threshold uses spot price too → same attack vector
```

### 4. Cross-Contract Variants

```
Found: Access control missing on Module A's admin function
Search: ALL modules in the protocol for admin functions
Result: Module B and Module C have same missing guard
```

### 5. Cross-Protocol Variants

```
Found: ERC4626 first-depositor attack in Vault A
Search: Historical data for same pattern in other protocols
Result: 28+ findings in Solodit database with same root cause
```

## Root Cause Taxonomy

| Root Cause Category | Common Variants | Search Strategy |
|---|---|---|
| **Missing validation** | Unchecked return, missing bounds, no zero-check | Grep all external interactions |
| **Incorrect ordering** | CEI violation, pre-state read, TOCTOU | Trace state reads vs external calls |
| **Access control gap** | Missing modifier, wrong role, unprotected init | Grep all public/external functions |
| **Arithmetic error** | Wrong rounding, precision loss, overflow | Grep all division/multiplication |
| **State inconsistency** | Stale cache, cross-function read, reentrancy | Map state dependencies |
| **Integration mismatch** | Fee-on-transfer, non-standard ERC20, decimals | List all token interactions |
| **Oracle dependency** | Stale price, spot manipulation, decimal mismatch | Find all price reads |
| **Timing dependency** | Block timestamp, deadline, frontrunning | Grep all time-based logic |

## Process Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  1. FIND    │────►│ 2. ABSTRACT │────►│  3. SEARCH  │
│  Initial    │     │  Root cause  │     │  Grep / AST │
│  Bug        │     │  pattern     │     │  Full cbase │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
┌─────────────┐     ┌─────────────┐     ┌──────▼──────┐
│  6. REPORT  │◄────│ 5. EXPAND   │◄────│ 4. VALIDATE │
│  All grouped│     │  Related     │     │  Each match │
│  by root    │     │  patterns    │     │  exploitable│
└─────────────┘     └─────────────┘     └─────────────┘
```

1. **Find**: Discover initial vulnerability during audit
2. **Abstract**: Reduce to root cause pattern at Level 2–3
3. **Search**: Grep/regex/AST search entire codebase for the pattern
4. **Validate**: Confirm each match is actually reachable and exploitable
5. **Expand**: Check related patterns (same root cause, different manifestation)
6. **Report**: Group all variants under single root cause with per-instance severity

## Variant Sources

| Source | Use Case | Example |
|---|---|---|
| Current audit findings | Found 1, find all | Reentrancy in one function → check all |
| Cyfrin/Solodit database | Historical pattern matching | "This oracle pattern has 145+ findings" |
| DeFiHackLabs | Real exploit reproduction | "Euler hack used same reentrancy variant" |
| Code4rena / Sherlock reports | Cross-protocol patterns | "Compound fork X had this — check Y" |
| Known Solidity compiler bugs | Version-specific issues | "Solidity <0.8.15 has ABI encoder bug" |
| OpenZeppelin advisories | Dependency vulnerabilities | "OZ v4.7.3 has governance vulnerability" |

## Resources
- [Variant Patterns](resources/variant-patterns.md) — Catalog of 12 major variant pattern classes with search strategies
- [Variant Hunt Workflow](workflows/variant-hunt.md) — Step-by-step methodology for executing a variant hunt

## Integration with Other Skills

| Skill | Integration |
|---|---|
| `cyfrin-findings/` | Query historical findings for the same root cause pattern |
| `patterns/` | Cross-reference with vulnerability pattern catalog |
| `anti-patterns/` | Anti-pattern signatures can seed variant searches |
| `exploit-forensics/` | Real-world exploits reveal pattern classes to hunt for |
| `static-analysis/` | Automate variant detection with custom Slither detectors |
| `checklists/` | Each variant class maps to checklist items |
