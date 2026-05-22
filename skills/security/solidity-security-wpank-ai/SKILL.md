---
name: solidity-security
model: standard
category: devops
description: Smart contract security patterns, vulnerability prevention, gas optimization, and audit preparation for Solidity development. Use when writing, auditing, or hardening smart contracts against reentrancy, overflow, access control, oracle manipulation, and front-running attacks.
version: 1.0.0
tags: [solidity, security, smart-contracts, blockchain, defi, audit]
---

# Solidity Security

Smart contract security patterns, vulnerability prevention, and secure development practices for Solidity.

## When to Use

- Writing or reviewing smart contracts
- Auditing contracts for vulnerabilities
- Implementing DeFi protocols
- Preventing reentrancy, overflow, and access control issues
- Optimizing gas while maintaining security
- Preparing contracts for professional audits


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install solidity-security
```


---

## Critical Vulnerabilities

### 1. Reentrancy

Attacker calls back into your contract before state is updated.

| Variant | Description | Fix |
|---------|-------------|-----|
| Single-function | Re-enters the same function mid-execution | CEI pattern + `ReentrancyGuard` |
| Cross-function | Re-enters a different function sharing state | `nonReentrant` on all state-mutating functions |
| Cross-contract | Re-enters through an intermediary contract | Treat every external call as re-entry vector |
| Read-only | View functions return stale state mid-operation | Guard on externally-consumed view functions |

**Vulnerable:**

```solidity
function withdraw() public {
    uint256 amount = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] = 0;  // Too late!
}
```

**Secure (Checks-Effects-Interactions + Guard):**

```solidity
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureBank is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function withdraw() public nonReentrant {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Insufficient balance");

        balances[msg.sender] = 0;  // EFFECT before INTERACTION

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

### 2. Integer Overflow/Underflow

**Pre-0.8.0 vulnerability** — arithmetic silently wraps around.

```solidity
// Solidity 0.8+ has built-in overflow/underflow checks
contract SecureToken {
    mapping(address => uint256) public balances;

    function transfer(address to, uint256 amount) public {
        // Automatically reverts on overflow/underflow
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

> For Solidity < 0.8.0, use `SafeMath` from OpenZeppelin. Be especially cautious with multiplication before comparison — the BEC Token exploit used `cnt * _value` overflow to mint infinite tokens.

### 3. Access Control

| Pattern | Use Case |
|---------|----------|
| `Ownable` / `Ownable2Step` | Single-admin contracts |
| `AccessControl` with roles | Multi-role systems |
| Multisig + `TimelockController` | DeFi protocol admin |

```solidity
import "@openzeppelin/contracts/access/Ownable.sol";

contract SecureContract is Ownable {
    function withdraw(uint256 amount) public onlyOwner {
        payable(owner()).transfer(amount);
    }
}
```

**Critical rules:**
- Every `external`/`public` state-changing function needs access control
- Never use `tx.origin` for authentication — use `msg.sender`
- Use two-step ownership transfer (`Ownable2Step`) to prevent accidental transfers
- No single key should control enough power to drain the protocol

### 4. Front-Running

Attackers observe pending transactions in the mempool and submit their own first.

**Mitigation — Commit-Reveal:**

```solidity
contract SecureDEX {
    mapping(bytes32 => bool) public usedCommitments;

    function commitTrade(bytes32 commitment) public {
        usedCommitments[commitment] = true;
    }

    function revealTrade(
        uint256 amount, uint256 minOutput, bytes32 secret
    ) public {
        bytes32 commitment = keccak256(
            abi.encodePacked(msg.sender, amount, minOutput, secret)
        );
        require(usedCommitments[commitment], "Invalid commitment");
        // Perform swap
    }
}
```

### 5. Oracle Manipulation

| Bad | Good |
|-----|------|
| AMM spot price (flash-loan manipulable) | Chainlink or TWAP oracle |
| No freshness check on oracle data | Validate `updatedAt`, `answeredInRound`, price > 0 |
| Single oracle with no fallback | Primary + fallback oracle with circuit breaker |

```solidity
(uint80 roundId, int256 price, , uint256 updatedAt, uint80 answeredInRound) =
    priceFeed.latestRoundData();
require(price > 0, "Invalid price");
require(updatedAt > 0, "Round not complete");
require(answeredInRound >= roundId, "Stale round");
require(block.timestamp - updatedAt <= MAX_STALENESS, "Price too old");
```

### 6. Signature Replay

Signatures without nonce, chain ID, or contract binding can be replayed.

**Use EIP-712 typed data:**

```solidity
import "@openzeppelin/contracts/utils/cryptography/EIP712.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract SecureRelay is EIP712 {
    mapping(address => uint256) public nonces;

    bytes32 private constant ACTION_TYPEHASH = keccak256(
        "ExecuteAction(address to,uint256 amount,uint256 nonce,uint256 deadline)"
    );

    constructor() EIP712("SecureRelay", "1") {}

    function executeAction(
        address to, uint256 amount, uint256 deadline,
        bytes calldata signature
    ) external {
        require(block.timestamp <= deadline, "Signature expired");
        uint256 currentNonce = nonces[msg.sender]++;
        bytes32 structHash = keccak256(
            abi.encode(ACTION_TYPEHASH, to, amount, currentNonce, deadline)
        );
        bytes32 hash = _hashTypedDataV4(structHash);
        require(ECDSA.recover(hash, signature) == msg.sender, "Invalid sig");
        payable(to).transfer(amount);
    }
}
```

---

## Security Patterns

### Checks-Effects-Interactions (CEI)

The foundational pattern — validate, update state, then interact externally.

```solidity
function withdraw(uint256 amount) public {
    require(amount <= balances[msg.sender], "Insufficient");  // CHECK
    balances[msg.sender] -= amount;                           // EFFECT
    (bool success, ) = msg.sender.call{value: amount}("");    // INTERACTION
    require(success, "Transfer failed");
}
```

### Pull Over Push

Let users withdraw funds instead of pushing payments to them. Prevents one failed transfer from blocking all others.

```solidity
contract SecurePayment {
    mapping(address => uint256) public pendingWithdrawals;

    function recordPayment(address recipient, uint256 amount) internal {
        pendingWithdrawals[recipient] += amount;
    }

    function withdraw() public {
        uint256 amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "Nothing to withdraw");
        pendingWithdrawals[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}
```

### Emergency Stop (Circuit Breaker)

```solidity
import "@openzeppelin/contracts/security/Pausable.sol";

contract EmergencyStop is Pausable, Ownable {
    function criticalFunction() public whenNotPaused { /* ... */ }
    function emergencyStop() public onlyOwner { _pause(); }
    function resume() public onlyOwner { _unpause(); }
}
```

---

## Gas Optimization

| Technique | Why |
|-----------|-----|
| Use `uint256` over smaller types | Smaller types still use 256-bit slot + extra conversion gas |
| Pack storage variables | Multiple small vars in one 32-byte slot |
| Use `calldata` over `memory` for args | Avoids copying data to memory |
| Emit events instead of storing | Events are cheaper than storage for read-only data |

**Storage packing example:**

```solidity
// 3 variables in 1 slot (gas efficient)
contract PackedStorage {
    uint128 public a;  // Slot 0
    uint64 public b;   // Slot 0
    uint64 public c;   // Slot 0
    uint256 public d;  // Slot 1
}
```

---

## Proxy & Upgrade Safety

| Rule | Why |
|------|-----|
| Use EIP-1967 storage slots | Prevents storage collision between proxy and implementation |
| Call `_disableInitializers()` in constructor | Prevents attacker from initializing the implementation contract |
| Use `uint256[50] __gap` in base contracts | Reserves storage slots for future upgrades |
| Test upgrades on fork before mainnet | Catches storage layout incompatibilities |

---

## Audit Preparation Checklist

| Category | Critical Items |
|----------|---------------|
| Reentrancy | CEI pattern followed, `ReentrancyGuard` on external-calling functions |
| Access Control | All privileged functions protected, no `tx.origin`, initializers guarded |
| External Calls | Return values checked, no `delegatecall` to untrusted addresses |
| Token Handling | `SafeERC20` used, fee-on-transfer handled, ERC-777 hooks considered |
| Math | Solidity 0.8+, `unchecked` blocks audited, multiply-before-divide |
| Oracles | No spot price, freshness validated, fallback configured |
| Upgrades | EIP-1967 slots, storage gaps, no re-initialization |
| Gas/DoS | Bounded loops, pull payments, no single-user blocking |
| Documentation | NatSpec on public/external functions, events for state changes |
| Testing | 95%+ coverage on critical paths, fuzz testing, invariant testing |

---

## Security Analysis Tools

| Tool | Purpose |
|------|---------|
| Slither | Static analysis — reentrancy, access control, unchecked calls |
| Mythril | Symbolic execution — overflow, reachability |
| Echidna | Property-based fuzz testing |
| Foundry | Fuzz testing, invariant testing, fork testing |
| Securify | Automated security scanning |

---

## References

- [Vulnerability Patterns](references/vulnerability-patterns.md) — 17 vulnerability categories with vulnerable/secure code pairs
- [Audit Checklist](references/audit-checklist.md) — Pre-deployment checklist organized by category with CRITICAL flagging
- [Exploit Examples](references/exploit-examples.md) — 8 real-world exploit breakdowns with attack flow analysis

---

## NEVER Do

| Anti-Pattern | Why It Kills |
|-------------|-------------|
| External call before state update | Reentrancy — The DAO lost $60M this way |
| `tx.origin` for auth | Phishing through intermediary contracts |
| AMM spot price as oracle | Flash loans make single-block manipulation trivial |
| Unchecked `delegatecall` to user address | Attacker overwrites your contract storage |
| Floating pragma (`^0.8.0`) | Pin exact version for reproducible builds |
| Unbounded loops over storage arrays | Block gas limit DoS — contract becomes unusable |
| `selfdestruct` in shared libraries | Parity froze $150M permanently this way |
| Signatures without nonce + chain ID | Replay attacks across chains and transactions |
| Push payments in loops | One failed transfer blocks all subsequent ones |
| `unchecked` blocks without proof of safety | Re-enables the overflow bugs Solidity 0.8 fixed |
