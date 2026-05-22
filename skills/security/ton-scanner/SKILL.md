---
id: TON-SCANNER
title: TON Smart Contract Security Scanner
category: chain-specific
difficulty: advanced
triggers:
  - ton smart contract audit
  - func security
  - tact security
  - ton vulnerability
  - message chain analysis
related_skills:
  - ton-scanner/resources/ton-patterns.md
  - ton-scanner/workflows/ton-audit.md
tags:
  - ton
  - func
  - tact
  - actor-model
  - security
last_updated: 2026-02-24
description: >-
  Use when the user wants to audit TON smart contracts for security
  vulnerabilities, scan FunC or Tact contracts for message chain replay, bounce
  handling, or gas issues, review TON DeFi protocols for actor-model concurrency
  flaws, or analyze asynchronous message passing security.
---

# TON Scanner Skill

## Purpose

Analyze TON (The Open Network) smart contracts written in FunC or Tact for security vulnerabilities. TON's actor-model architecture, asynchronous message passing, and TVM (TON Virtual Machine) create a fundamentally different security model from EVM-based chains.

## TON Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         TON Network                             │
│                                                                 │
│  ┌──────────────┐    async messages     ┌──────────────┐        │
│  │  Contract A   │ ──────────────────► │  Contract B   │        │
│  │  (Shard 1)    │ ◄────────────────── │  (Shard 2)    │        │
│  │               │    bounce/reply      │               │        │
│  │  FunC / Tact  │                      │  FunC / Tact  │        │
│  └──────┬───────┘                      └──────┬───────┘        │
│         │                                      │                │
│         ▼                                      ▼                │
│  ┌──────────────┐                      ┌──────────────┐        │
│  │    Storage    │                      │    Storage    │        │
│  │  (Cells/BoC)  │                      │  (Cells/BoC)  │        │
│  │  pays rent    │                      │  pays rent    │        │
│  └──────────────┘                      └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

### Key Differences from EVM

| Aspect | EVM (Solidity) | TON (FunC/Tact) |
|---|---|---|
| Execution Model | Synchronous, atomic | Asynchronous, actor-based messages |
| Cross-Contract Calls | Atomic within transaction | Non-atomic, separate transactions |
| Storage Cost | One-time gas | Ongoing rent (storage fees) |
| Data Structure | Key-value mapping | Cell trees (max 1023 bits, 4 refs) |
| Reentrancy | Within same transaction | Not possible (async messages) |
| Failure Handling | Revert entire tx | Bounce messages, partial failure |
| Languages | Solidity, Vyper | FunC (low-level), Tact (high-level) |
| Address Format | 20-byte, single chain | Workchain ID + 256-bit hash |

### Languages

| Language | Level | Usage | Security Characteristics |
|---|---|---|---|
| **FunC** | Low-level | Core contracts, jettons, NFTs | Direct TVM access, manual cell serialization, easy to misuse |
| **Tact** | High-level | Modern contracts | Type-safe, auto-serialization, safer defaults but newer |
| **Fift** | Assembly-level | Deployment scripts | Direct TVM opcodes, used for contract deployment |

## Detection Capabilities

### Critical Vulnerabilities
- **Message chain gas exhaustion**: Multi-hop messages run out of gas before completing all operations
- **Missing bounce handling**: Bounced messages not processed → permanent fund loss
- **Unbounded storage growth**: Attacker-controlled data storage drains contract balance via rent
- **Missing replay protection**: Same message processed multiple times

### High Vulnerabilities
- **Carry-value attacks**: Incoming message value used to fund outgoing messages without accounting
- **Cell overflow/underflow**: Exceeding 1023-bit or 4-reference cell limits during serialization
- **Workchain ID confusion**: Not validating workchain in address leads to cross-chain issues
- **Incorrect message mode flags**: Wrong send mode causes unintended gas forwarding or balance drain

### Medium Vulnerabilities
- **Storage fee drain**: Contract balance slowly depleted by rent payments on stored data
- **Sharded message ordering**: Assuming message order across shards causes race conditions
- **Tick-tock contract abuse**: Automatic execution contracts with expensive operations
- **Missing `accept_message()` in external handlers**: External messages silently dropped without gas acceptance

## Real-World TON Incidents

| Incident | Vulnerability | Impact |
|---|---|---|
| Early Jetton implementations | Missing bounce handling | Token loss on failed transfers |
| DNS auction contracts | Gas exhaustion in multi-message chains | Auctions stuck irrecoverably |
| Various NFT marketplaces | Replay attacks (no seqno) | Duplicate sales/purchases |
| Storage-based attacks | Unbounded storage growth | Contract balance drained by rent |

## Resources
- [TON Patterns](resources/ton-patterns.md) — Full vulnerability patterns with FunC/Tact code
- [TON Audit Workflow](workflows/ton-audit.md) — Step-by-step audit methodology

## Related Scanners
- [Solidity Scanner](../solidity-scanner/) — EVM comparison for cross-chain auditors
- [Solana Scanner](../solana-scanner/) — Another non-EVM async model for comparison

## Error Code Reference

Common TON/FunC error codes encountered during audits. TON uses numeric exit codes in `throw()` / `throw_if()` / `throw_unless()` statements.

### Standard TVM Exit Codes

| Exit Code | Name | Meaning |
|----------|------|----------|
| `0` | Success | Normal successful execution |
| `2` | `Stack underflow` | Too few arguments on the stack — FunC function signature mismatch |
| `3` | `Stack overflow` | Stack exceeded limits |
| `4` | `Integer overflow` | Integer does not fit into 257-bit signed range |
| `5` | `Integer out of range` | Value outside expected range for operation |
| `6` | `Invalid opcode` | Unknown TVM instruction — possible code corruption |
| `7` | `Type check error` | Wrong type on stack — e.g., expected cell, got integer |
| `8` | `Cell overflow` | Cell data exceeds 1023 bits or 4 references |
| `9` | `Cell underflow` | Attempted to read more data than cell contains |
| `10` | `Dictionary error` | Invalid dictionary (hashmap) operation |
| `11` | `Unknown error` | General "most common" error |
| `13` | `Out of gas` | Computation exceeded gas limit |
| `-14` | `Out of gas (credit)` | Gas credit depleted before `accept_message()` |

### Common Application Exit Codes (Convention)

| Exit Code Range | Convention | Meaning |
|----------------|-----------|----------|
| `30-39` | Auth errors | Unauthorized sender (`throw_unless(33, ...)`) |
| `40-49` | State errors | Invalid contract state for operation |
| `50-59` | Balance errors | Insufficient balance for operation |
| `60-69` | Validation errors | Invalid input parameters |
| `100-199` | Jetton Standard | Jetton (token) specific errors |
| `200-299` | NFT Standard | NFT specific errors |
| `300-399` | DEX errors | Liquidity pool / AMM errors |
| `400+` | Application-specific | Custom application logic errors |

### Jetton Standard Error Codes

| Exit Code | Meaning |
|----------|----------|
| `73` | Insufficient jetton balance for transfer |
| `74` | Not enough TON for gas fees attached to transfer |
| `75` | Invalid sender — not the jetton wallet owner |
| `76` | Discovery: unknown jetton wallet |

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| Bounce handler vulnerabilities missed | Scanner doesn't analyze `bounced<>` message handlers | Audit all `recv_internal` branches that handle bounced messages — check for state rollback correctness |
| Message chain replay not detected | Scanner analyzes single messages, not chains | Trace full message chains: initial message → internal messages → bounces; check seqno/query_id uniqueness |
| Gas estimation issues not flagged | Scanner doesn't model TON gas economics | Flag messages without `accept_message()` or with insufficient gas forwarding via `msg_value` |
| Actor model concurrency bugs missed | Scanner uses synchronous mental model | Map all async message flows; check for time-of-check/time-of-use between separate messages |
| FunC vs Tact pattern mismatch | Scanner patterns written for FunC, code is in Tact | Verify Tact's auto-generated FunC output; Tact handles some safety checks automatically |
| Storage fee drain not caught | Scanner doesn't model TON storage costs | Check that contracts handle `storage_fee` deductions; verify minimum balance maintenance |
