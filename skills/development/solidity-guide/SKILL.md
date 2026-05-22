---
name: solidity-guide
description: |
  Solidity/Ethereum guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Solidity files (.sol), or when the user mentions Solidity/Ethereum/smart contracts.
  Provides gas optimization patterns, reentrancy prevention, upgradeable contract guidelines,
  and testing standards specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: solidity
  extensions: ".sol"
---

# Solidity Guide

> Applies to: Solidity 0.8.20+, Ethereum, EVM-compatible chains, DeFi, NFTs

## Core Principles

1. **Security First**: Every function is a potential attack surface. Assume adversarial callers.
2. **Gas Efficiency**: On-chain computation is expensive. Optimize storage access and minimize state changes.
3. **Explicit Over Implicit**: Use explicit visibility, explicit types, and named return values.
4. **Immutability by Default**: Prefer `immutable` and `constant` for values that do not change after deployment.
5. **Standards Compliance**: Use OpenZeppelin for ERC standards. Do not roll your own token logic.

## Guardrails

### Compiler Version

- ALWAYS specify pragma version range: `pragma solidity ^0.8.20;`
- Do NOT use floating pragmas in production (e.g., `>=0.8.0`). Pin to a minor range.
- Enable the optimizer with at least 200 runs for production deployments.

### Security

- NEVER use `tx.origin` for authorization. Use `msg.sender`.
- NEVER use `selfdestruct` in new contracts (deprecated in Dencun).
- ALWAYS use `ReentrancyGuard` from OpenZeppelin for functions that make external calls.
- ALWAYS validate external inputs: check zero addresses, bounds, and array lengths.
- Use `SafeERC20` for token transfers (handles non-standard return values).
- Emit events for every state-changing operation (required for off-chain indexing).

### Gas Optimization

- Pack storage variables: group `uint128`, `uint64`, `bool` into single 256-bit slots.
- Use `calldata` instead of `memory` for read-only external function parameters.
- Use custom errors instead of `require` strings (saves ~50 bytes per error site).
- Cache storage reads in local variables when accessed more than once.
- Use `unchecked` blocks for arithmetic that provably cannot overflow.
- Prefer `mapping` over `array` for large datasets (O(1) vs O(n) lookups).

### Access Control

- Use OpenZeppelin `AccessControl` or `Ownable2Step` (not plain `Ownable`).
- Separate admin roles: deployer, upgrader, pauser, minter. No single god key.
- Consider a timelock for sensitive admin operations (`TimelockController`).

### Upgradability

- Use UUPS proxy pattern (preferred) or Transparent proxy when upgradability is required.
- NEVER change storage layout ordering in upgraded implementations.
- Use `@openzeppelin/contracts-upgradeable` with `initializer` instead of constructors.
- ALWAYS include a storage gap: `uint256[50] private __gap;`
- Disable initializers in the constructor: `_disableInitializers();`

## Key Patterns

### Checks-Effects-Interactions (CEI)

Prevents reentrancy by ordering operations: validate, update state, then call externally.

```solidity
function withdraw(uint256 amount) external nonReentrant {
    // 1. CHECKS
    if (amount == 0) revert ZeroAmount();
    if (balances[msg.sender] < amount) revert InsufficientBalance();

    // 2. EFFECTS: update state BEFORE external calls
    balances[msg.sender] -= amount;

    // 3. INTERACTIONS: external calls last
    (bool success, ) = msg.sender.call{value: amount}("");
    if (!success) revert TransferFailed();

    emit Withdrawn(msg.sender, amount);
}
```

### Pull Over Push

Let users withdraw funds instead of pushing payments to them.

```solidity
mapping(address => uint256) public pendingWithdrawals;

function claimPayment() external nonReentrant {
    uint256 amount = pendingWithdrawals[msg.sender];
    if (amount == 0) revert NothingToClaim();
    pendingWithdrawals[msg.sender] = 0;

    (bool success, ) = msg.sender.call{value: amount}("");
    if (!success) revert TransferFailed();
    emit PaymentClaimed(msg.sender, amount);
}
```

### Guard Checks with Custom Errors

Custom errors are cheaper than `require` strings and support typed parameters.

```solidity
error Unauthorized(address caller);
error InsufficientBalance(uint256 requested, uint256 available);
error ZeroAddress();

function transfer(address to, uint256 amount) external {
    if (to == address(0)) revert ZeroAddress();
    if (balances[msg.sender] < amount) {
        revert InsufficientBalance(amount, balances[msg.sender]);
    }
    balances[msg.sender] -= amount;
    balances[to] += amount;
    emit Transfer(msg.sender, to, amount);
}
```

### UUPS Proxy Pattern

```solidity
import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import {OwnableUpgradeable} from "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract MyProtocol is UUPSUpgradeable, OwnableUpgradeable {
    uint256 public protocolFee;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() { _disableInitializers(); }

    function initialize(address owner, uint256 fee) external initializer {
        __Ownable_init(owner);
        __UUPSUpgradeable_init();
        protocolFee = fee;
    }

    function _authorizeUpgrade(address) internal override onlyOwner {}

    uint256[49] private __gap;
}
```

## Security Checklist

- **Reentrancy**: Apply `nonReentrant` to external-call functions. Follow CEI even with the guard. Watch for cross-function reentrancy on shared state.
- **Integer Safety**: Solidity 0.8+ has overflow checks. Use `unchecked` only when provably safe.
- **Front-Running**: Use commit-reveal for auctions/voting. Add deadline params to swaps. Use `block.timestamp`, not `block.number`.
- **Access Control**: Never rely on `tx.origin`. Use `Pausable` for emergency stops.

## Testing

### Foundry (forge) -- Recommended

```solidity
// test/Vault.t.sol
pragma solidity ^0.8.20;

import {Test} from "forge-std/Test.sol";
import {Vault} from "../src/Vault.sol";

contract VaultTest is Test {
    Vault public vault;
    address public alice = makeAddr("alice");

    function setUp() public {
        vault = new Vault();
        vm.deal(alice, 10 ether);
    }

    function test_deposit_updates_balance() public {
        vm.prank(alice);
        vault.deposit{value: 1 ether}();
        assertEq(vault.balances(alice), 1 ether);
    }

    function test_withdraw_reverts_on_insufficient_balance() public {
        vm.prank(alice);
        vm.expectRevert(Vault.InsufficientBalance.selector);
        vault.withdraw(1 ether);
    }

    // Fuzz testing: forge generates random inputs automatically
    function testFuzz_deposit_and_withdraw(uint96 amount) public {
        vm.assume(amount > 0 && amount <= 10 ether);
        vm.startPrank(alice);
        vault.deposit{value: amount}();
        vault.withdraw(amount);
        vm.stopPrank();
        assertEq(vault.balances(alice), 0);
    }
}
```

### Hardhat (alternative)

Use `npx hardhat test` with Chai matchers and `ethers.js` for JS/TS projects.

## Tooling

```bash
forge build && forge test         # Compile and test (Foundry)
forge test -vvvv                  # Verbose with stack traces
forge test --fuzz-runs 10000      # Extended fuzz testing
forge coverage                    # Coverage report
forge fmt                         # Format Solidity files
forge snapshot                    # Gas snapshot for benchmarking
slither .                         # Static analysis (Slither)
myth analyze src/Contract.sol     # Symbolic execution (Mythril)
npx hardhat compile && npx hardhat test  # Hardhat alternative
```

### Pre-Deployment Checklist

- [ ] `forge test` passes, Slither reports zero high/medium findings
- [ ] Gas snapshot compared (`forge snapshot --diff`)
- [ ] Storage layout verified for upgradeable contracts
- [ ] Deploy script tested on fork: `forge script --fork-url $RPC_URL`
- [ ] Admin keys secured (multisig, timelock)

## References

- [references/patterns.md](references/patterns.md) -- ERC20, proxy upgrades, gas optimization examples

## External References

- [Solidity Docs](https://docs.soliditylang.org/) | [OpenZeppelin](https://docs.openzeppelin.com/contracts/) | [Foundry Book](https://book.getfoundry.sh/)
- [Solidity by Example](https://solidity-by-example.org/) | [EIP Standards](https://eips.ethereum.org/)
- [Smart Contract Security (Consensys)](https://consensys.github.io/smart-contract-best-practices/) | [Slither](https://github.com/crytic/slither)
