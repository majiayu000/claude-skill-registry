---
id: static-analysis
title: Static Analysis Skill
category: methodology
difficulty: intermediate
triggers:
  - static analysis
  - slither
  - mythril
  - aderyn
  - semgrep
  - automated scan
related_skills:
  - solidity-scanner/SKILL.md
  - methodology/SKILL.md
tags:
  - static-analysis
  - slither
  - mythril
  - tooling
last_updated: 2026-02-26
description: >-
  Integrate automated static analysis tools (Slither, Mythril, Aderyn,
  Semgrep) into the audit workflow to catch known vulnerability patterns
  before manual review. Use when starting an audit to establish a coverage
  baseline, or when configuring static analysis tooling for a project.
---

# Static Analysis Skill

Integrate automated static analysis tools into the audit workflow to catch low-hanging vulnerabilities before manual review. Static analysis should be the FIRST step after compilation — it surfaces issues that automated tools excel at finding, freeing manual review time for complex logic and economic vulnerabilities.

---

## Why Static Analysis First?

| Benefit | Details |
|---------|--------|
| Coverage baseline | Ensures known vulnerability patterns are checked across ALL functions |
| Prioritization | Findings direct manual reviewer to highest-risk areas |
| Speed | Minutes vs hours/days for manual review |
| Consistency | Never misses a pattern it knows about (humans do) |
| Documentation | Generates structured output for audit reports |

---

## Detection Capabilities

### What Static Analysis Catches Well

| Category | Examples |
|----------|----------|
| Reentrancy | All variants: ETH, ERC-20, cross-function, read-only |
| Unchecked calls | Missing return value checks on `transfer`, `send`, low-level `call` |
| Access control | Unprotected `selfdestruct`, missing modifiers, `tx.origin` auth |
| State issues | Uninitialized storage, shadowed variables, redundant state |
| Dangerous patterns | Controlled `delegatecall`, hardcoded gas, `block.timestamp` dependency |
| Code quality | Floating pragma, unused variables, dead code, naming conventions |
| Standard compliance | ERC-20 / ERC-721 interface compliance |
| Compiler issues | Use of deprecated patterns, assembly without memory safety |

### What Static Analysis Misses

| Category | Why |
|----------|-----|
| Business logic | Tools don't understand protocol semantics |
| Economic attacks | Flash loan manipulation, oracle gaming |
| Cross-contract interactions | Limited to single-contract analysis (mostly) |
| Governance attacks | Vote manipulation, proposal hijacking |
| MEV / sandwich | Requires mempool context |
| Timing attacks | Cross-block state dependencies |
| Complex math errors | Rounding, precision loss in multi-step calculations |

---

## Tool Comparison

| Tool | Language | Approach | Speed | False Positives | Best For |
|------|----------|----------|-------|----------------|----------|
| **Slither** | Python | AST + data flow | Fast (seconds) | Low-Medium | Broad vulnerability detection, code quality |
| **Mythril** | Python | Symbolic execution + SMT | Slow (minutes-hours) | Low | Deep state reachability, proving exploitability |
| **Aderyn** | Rust | AST analysis | Very fast | Low | Quick scans, CI/CD integration |
| **Semgrep** | Python | Pattern matching | Fast | Depends on rules | Custom rules, org-specific patterns |
| **Foundry invariant tests** | Solidity | Fuzzing | Medium | Very low | Invariant verification |
| **Echidna** | Haskell | Property-based fuzzing | Slow | Very low | Finding edge cases in complex state |
| **Medusa** | Go | Parallel fuzzing | Medium | Very low | Faster alternative to Echidna |

### Recommended Workflow

```
1. Slither (always — fast, broad coverage)
     │
2. Aderyn (always — fast, complementary detectors)
     │
3. Semgrep with custom rules (if org has rules)
     │
4. Mythril (selectively — on high-risk functions only)
     │
5. Echidna/Medusa (if invariant tests needed)
```

---

## Slither Quick Reference

### Installation

```bash
pip install slither-analyzer
# Requires solc installed (managed by solc-select)
pip install solc-select
solc-select install 0.8.20
solc-select use 0.8.20
```

### Common Commands

```bash
# Full scan
slither .

# Filter out dependencies
slither . --filter-paths "node_modules|lib|test"

# Specific detectors
slither . --detect reentrancy-eth,arbitrary-send-eth,controlled-delegatecall

# JSON output
slither . --json output.json

# Code analysis printers
slither . --print contract-summary
slither . --print function-summary
slither . --print inheritance-graph
slither . --print call-graph
slither . --print variable-order  # Storage layout
```

---

## Aderyn Quick Reference

### Installation

```bash
cargo install aderyn
# Or via npm
npm install -g aderyn
```

### Usage

```bash
# Full scan
aderyn .

# Specific scope
aderyn . --src src/

# Markdown output
aderyn . --output report.md
```

### Key Detectors

| Detector | Description |
|----------|-----------|
| `centralization-risk` | Functions callable by single address |
| `unsafe-erc20-functions` | Direct `transfer`/`approve` without Safe wrapper |
| `push-0` | `PUSH0` opcode incompatible with older EVM versions |
| `solmate-safe-transfer-lib` | Solmate SafeTransferLib doesn't check contract existence |
| `unprotected-init` | Missing initializer guard |

---

## Semgrep Quick Reference

```bash
# Install
pip install semgrep

# Run with Solidity rules
semgrep --config "p/solidity" .

# Custom rule example
semgrep --config custom-rules/ .
```

### Custom Rule Example

```yaml
rules:
  - id: unchecked-low-level-call
    patterns:
      - pattern: |
          (bool $SUCCESS, ) = $ADDR.call{...}(...);
      - pattern-not-inside: |
          require($SUCCESS, ...);
    message: "Low-level call return value not checked"
    severity: ERROR
    languages: [solidity]
```

---

## Resources
- [Slither Guide](resources/slither-guide.md) — Full configuration, detectors, triage

## Workflows
- [Static Analysis Workflow](workflows/static-analysis.md) — Step-by-step process
