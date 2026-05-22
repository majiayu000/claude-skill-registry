---
id: COSMOS-SCAN
title: Cosmos / CosmWasm Security Scanner
category: chain-scanner
trigger: "Audit Cosmos|CosmWasm|IBC"
last_updated: 2026-02-24
description: >-
  Use when the user wants to audit Cosmos SDK modules or CosmWasm smart
  contracts, scan IBC protocol interactions for relay, channel, or packet
  vulnerabilities, review Cosmos Go modules for state machine exploits, or
  analyze cross-chain message handling in the Cosmos ecosystem.
---

# Cosmos / CosmWasm Security Scanner

Security scanner for Cosmos SDK modules (Go), CosmWasm smart contracts (Rust/WASM), and Inter-Blockchain Communication (IBC) protocol interactions.

---

## Language & Runtime

| Attribute | Value |
|-----------|-------|
| Chain | Cosmos Hub, Osmosis, Juno, Neutron, Injective, Sei, + 60 app-chains |
| Smart Contract Language | Rust (compiled to WASM) |
| SDK Language | Go (custom Cosmos SDK modules) |
| VM | CosmWasm (WASM-based) |
| Token Standard | CW20 (fungible), CW721 (NFT), CW1155 (multi-token) |
| Key Framework | `cosmwasm-std`, Cosmos SDK |
| Storage Model | Key-value store (binary prefixed maps) |
| Gas Model | Gas consumed per operation, configurable per chain |

---

## Detection Capabilities

| Category | Detection | Severity |
|----------|-----------|----------|
| **Authorization** | Missing `info.sender` check on Execute handlers | Critical |
| **Authorization** | Keeper function callable without proper auth (SDK modules) | Critical |
| **Authorization** | AuthZ overly broad grants enabling privilege escalation | High |
| **IBC** | Packet source/destination validation missing | Critical |
| **IBC** | Channel ordering assumption violation | High |
| **IBC** | Timeout and acknowledgement handling errors | High |
| **State** | Unbounded `range()` iteration (gas DoS) | High |
| **State** | Iterator invalidation during mutation | High |
| **State** | Storage key collision in multi-contract systems | Medium |
| **Cross-Contract** | SubMessage reply handler not checking `msg_id` | High |
| **Cross-Contract** | Bank send reentrancy via SubMessage reply | Medium |
| **Math** | `Uint128`/`Uint256` overflow (panics in debug, wraps in release) | High |
| **Math** | `Decimal256` precision loss in rate calculations | Medium |
| **Governance** | Parameter manipulation via governance proposal | Medium |
| **Governance** | Admin key not removable (centralization) | Medium |
| **BlockHooks** | BeginBlocker/EndBlocker gas consumption DoS (SDK modules) | High |
| **Migration** | `migrate()` entry point without access control | Critical |

---

## Architecture Model: CosmWasm Contracts

```
┌────────────────────────────────────────────────┐
│  CosmWasm Contract Entry Points               │
├────────────┬───────────┬───────────┬───────────┤
│ instantiate │ execute    │ query      │ migrate    │
│ (once)      │ (state)    │ (read)     │ (upgrade)  │
└────────────┴───────────┴───────────┴───────────┘
        │                                      │
   State (Items, Maps, SnapshotMaps)    SubMessages
        │                                      │
   Storage (KV Store)               Reply Handler
```

### Entry Point Security Model

| Entry Point | `info.sender` | State Access | Security Focus |
|-------------|---------------|--------------|----------------|
| `instantiate` | Contract deployer | Write | Set admin, validate config |
| `execute` | Transaction signer | Write | **Primary attack surface** |
| `query` | Not available | Read-only | Gas DoS, expensive computation |
| `migrate` | Contract admin | Write | **Must check authorization** |
| `reply` | Contract itself | Write | SubMessage result handling |
| `sudo` | Chain governance | Write | Privileged chain operations |

---

## Notable Cosmos/CosmWasm Vulnerabilities

| Incident | Chain | Issue | Impact |
|----------|-------|-------|--------|
| Osmosis LP bug (2022) | Osmosis | Rounding error in LP share calculation | $5M at risk (white-hat) |
| Juno whale governance (2022) | Juno | Governance used to confiscate tokens | Governance centralization debate |
| Terra UST depeg (2022) | Terra | Algorithmic stablecoin design flaw | ~$40B market value lost |
| Wormhole bridge (2022) | Multi | Guardian signature verification bypass | $320M stolen |
| CW20 unlimited mint | Various | Missing admin check on mint execute | Token inflation |
| IBC race condition | Various | Packet ordering assumption violated | Token duplication |

---

## Key Vulnerability Patterns

### 1. Missing `info.sender` Check

```rust
// VULNERABLE: Anyone can call
pub fn execute_withdraw(
    deps: DepsMut,
    _info: MessageInfo,  // sender not checked!
    amount: Uint128,
) -> Result<Response, ContractError> {
    // Withdraws funds without checking who's requesting
    let msg = BankMsg::Send {
        to_address: "attacker".to_string(),
        amount: vec![Coin { denom: "uatom".to_string(), amount }],
    };
    Ok(Response::new().add_message(msg))
}

// SAFE: Validates caller
pub fn execute_withdraw(
    deps: DepsMut,
    info: MessageInfo,
    amount: Uint128,
) -> Result<Response, ContractError> {
    let config = CONFIG.load(deps.storage)?;
    if info.sender != config.admin {
        return Err(ContractError::Unauthorized {});
    }
    // Proceed with withdrawal...
}
```

### 2. Unbounded State Iteration

```rust
// VULNERABLE: Iterates ALL entries — gas DoS as state grows
pub fn query_all_balances(deps: Deps) -> StdResult<Vec<(Addr, Uint128)>> {
    let result: Vec<_> = BALANCES
        .range(deps.storage, None, None, Order::Ascending)
        .collect::<StdResult<Vec<_>>>()?;  // Unbounded!
    Ok(result)
}

// SAFE: Paginated with limit
pub fn query_balances(
    deps: Deps,
    start_after: Option<Addr>,
    limit: Option<u32>,
) -> StdResult<Vec<(Addr, Uint128)>> {
    let limit = limit.unwrap_or(30).min(100); // Cap at 100
    let start = start_after.map(Bound::exclusive);
    let result: Vec<_> = BALANCES
        .range(deps.storage, start, None, Order::Ascending)
        .take(limit as usize)
        .collect::<StdResult<Vec<_>>>()?;
    Ok(result)
}
```

### 3. SubMessage Reply Handler Bug

```rust
// VULNERABLE: Reply handler doesn't check which SubMessage triggered it
#[entry_point]
pub fn reply(deps: DepsMut, _env: Env, msg: Reply) -> Result<Response, ContractError> {
    // Assumes all replies are from the token transfer SubMessage
    // But could be from any SubMessage!
    handle_transfer_reply(deps, msg)
}

// SAFE: Checks reply ID
const TRANSFER_REPLY_ID: u64 = 1;
const MINT_REPLY_ID: u64 = 2;

#[entry_point]
pub fn reply(deps: DepsMut, _env: Env, msg: Reply) -> Result<Response, ContractError> {
    match msg.id {
        TRANSFER_REPLY_ID => handle_transfer_reply(deps, msg),
        MINT_REPLY_ID => handle_mint_reply(deps, msg),
        _ => Err(ContractError::UnknownReplyId { id: msg.id }),
    }
}
```

---

## Resources
- [CosmWasm Patterns](resources/cosmwasm-patterns.md)
- [IBC Security](resources/ibc-security.md)

## Workflows
- [CosmWasm Audit](workflows/cosmwasm-audit.md)

## Error Code Reference

Common Cosmos SDK, CosmWasm, and IBC error codes encountered during audits.

### CosmWasm Standard Errors

| Error Type | Error Name | Meaning |
|-----------|-----------|----------|
| `StdError::NotFound` | `NotFound { kind }` | Queried item not found in storage |
| `StdError::InvalidBase64` | `InvalidBase64 { msg }` | Invalid base64 encoding in message |
| `StdError::InvalidUtf8` | `InvalidUtf8 { msg }` | Invalid UTF-8 in string conversion |
| `StdError::Overflow` | `Overflow { source }` | Arithmetic overflow in `Uint128`/`Uint256` operations |
| `StdError::DivideByZero` | `DivideByZero { source }` | Division by zero in math operation |
| `StdError::ConversionOverflow` | `ConversionOverflow { source }` | Type conversion exceeds target range |
| `StdError::GenericErr` | `GenericErr { msg }` | Catch-all error — check `msg` for specifics |

### Cosmos SDK Module Errors

| Module | Codespace | Error Code | Meaning |
|--------|----------|-----------|----------|
| `bank` | `bank` | `5` | Insufficient funds for send |
| `bank` | `bank` | `8` | Send disabled for denom |
| `staking` | `staking` | `5` | Validator not found |
| `staking` | `staking` | `7` | Delegation not found |
| `staking` | `staking` | `12` | Insufficient shares for undelegation |
| `auth` | `auth` | `4` | Insufficient fee |
| `auth` | `auth` | `9` | Signature verification failed |
| `gov` | `gov` | `3` | Unknown proposal |
| `gov` | `gov` | `5` | Inactive proposal — voting period ended |

### IBC Protocol Errors

| Module | Error Code | Meaning |
|--------|-----------|----------|
| `channel` | `5` | Channel not found |
| `channel` | `11` | Packet already received — replay protection |
| `channel` | `17` | Packet timeout — message expired |
| `connection` | `5` | Connection not found |
| `transfer` | `3` | Invalid denomination trace |
| `transfer` | `6` | Receive disabled on this channel |
| `client` | `6` | Client state not found |
| `client` | `9` | Consensus state not found |

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| IBC message handling vulnerabilities missed | Scanner only checks contract logic, not IBC layer | Load `resources/ibc-security.md` and audit `ibc_packet_receive` / `ibc_packet_ack` handlers |
| CosmWasm reply handler issues not detected | Scanner doesn't follow submessage flow | Trace all `SubMsg` with `ReplyOn::Success`/`ReplyOn::Error` and match reply IDs |
| State machine exploit not flagged | Scanner checks individual messages, not sequences | Analyze multi-message transaction flows for state inconsistencies |
| Missing sudo handler audit | Scanner focuses on execute/query only | Check `sudo()` entry point — often used for privileged chain-level operations |
| Gas griefing not detected | Scanner doesn't model gas costs | Flag unbounded loops/iterations in `execute` and `query` handlers |
| Cross-contract call risks missed | Scanner doesn't trace inter-contract calls | Map all `WasmMsg::Execute` and `WasmQuery::Smart` calls to external contracts |
