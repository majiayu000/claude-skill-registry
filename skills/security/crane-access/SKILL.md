---
name: crane-access
description: This skill should be used when the user asks about "access control", "onlyOwner", "onlyOperator", "ownership transfer", "MultiStepOwnable", "ERC8023", "operable pattern", "function-level permissions", "reentrancy protection", "reentrancy lock", or needs to restrict function access in Crane Diamond contracts.
license: MIT
---

# Crane Access Control Components

Crane provides three access control patterns for Diamond proxies: MultiStepOwnable (ERC-8023), Operable, and ReentrancyLock.

## Component Selection

| Need | Component | Purpose |
|------|-----------|---------|
| Ownership with time-lock | MultiStepOwnable | Two-step ownership transfer with buffer period |
| Delegated permissions | Operable | Global and function-level operator authorization |
| Reentrancy protection | ReentrancyLock | Transient storage lock for cross-function reentrancy |

## Quick Start: Add Access Control

```solidity
// Import modifiers
import {MultiStepOwnableModifiers} from "@crane/contracts/access/ERC8023/MultiStepOwnableModifiers.sol";
import {OperableModifiers} from "@crane/contracts/access/operable/OperableModifiers.sol";
import {ReentrancyLockModifiers} from "@crane/contracts/access/reentrancy/ReentrancyLockModifiers.sol";

// Use in your Target contract
contract MyTarget is MultiStepOwnableModifiers, OperableModifiers, ReentrancyLockModifiers {
    function adminOnly() external onlyOwner {
        // Only owner can call
    }

    function operatorOnly() external onlyOperator {
        // Global operators or function-specific operators
    }

    function ownerOrOperator() external onlyOwnerOrOperator {
        // Either owner or operator can call
    }

    function noReentrant() external nonReentrant {
        // Protected from reentrancy
    }
}
```

## MultiStepOwnable (ERC-8023)

Time-locked two-step ownership transfer with buffer period.

### Storage

```solidity
struct Storage {
    address owner;
    address pendingOwner;
    bool pendingOwnerConfirmed;
    uint256 ownershipBufferPeriod;  // e.g., 1 days
    uint256 bufferPeriodEnd;
}
```

### Ownership Transfer Flow

1. **Initiate**: Owner calls `initiateOwnershipTransfer(newOwner)`
2. **Wait**: Buffer period must elapse
3. **Confirm**: Owner calls `confirmOwnershipTransfer(newOwner)`
4. **Accept**: New owner calls `acceptOwnershipTransfer()`

```solidity
// Step 1: Current owner initiates
MultiStepOwnableRepo._initiateOwnershipTransfer(newOwner);

// Step 2: Wait for buffer period (e.g., 1 day)

// Step 3: Current owner confirms
MultiStepOwnableRepo._confirmOwnershipTransfer(newOwner);

// Step 4: New owner accepts
MultiStepOwnableRepo._acceptOwnershipTransfer();

// Owner can cancel anytime before acceptance
MultiStepOwnableRepo._cancelPendingOwnershipTransfer();
```

### Guard Functions

```solidity
// Revert if msg.sender is not owner
MultiStepOwnableRepo._onlyOwner();

// Revert if msg.sender is not pending owner
MultiStepOwnableRepo._onlyPendingOwner();
```

### Modifiers

```solidity
modifier onlyOwner() {
    MultiStepOwnableRepo._onlyOwner();
    _;
}
```

### Initialization

```solidity
// In DFPkg.initAccount()
MultiStepOwnableRepo._initialize(
    initialOwner,    // First owner
    1 days           // Buffer period for transfers
);
```

## Operable Pattern

Delegated authorization for global and function-level permissions.

### Storage

```solidity
struct Storage {
    mapping(address => bool) isOperator;  // Global operators
    mapping(bytes4 func => mapping(address => bool)) isOperatorFor;  // Function-level
}
```

### Authorization Levels

1. **Global Operator**: Can call any function protected by `onlyOperator`
2. **Function Operator**: Can only call specific functions

### Setting Permissions (Owner Only)

```solidity
// Grant/revoke global operator status
OperableRepo._setOperatorStatus(operatorAddress, true);   // Grant
OperableRepo._setOperatorStatus(operatorAddress, false);  // Revoke

// Grant/revoke function-level operator
OperableRepo._setFunctionOperatorStatus(
    IMyContract.someFunction.selector,  // Function selector
    operatorAddress,                     // Operator
    true                                 // Approval
);
```

### Checking Permissions

```solidity
// Check global operator
bool isGlobal = OperableRepo._isOperator(account);

// Check function operator
bool isForFunc = OperableRepo._isFunctionOperator(
    IMyContract.someFunction.selector,
    account
);
```

### Guard Functions

```solidity
// Revert if not global OR function operator for msg.sig
OperableRepo._onlyOperator();

// Revert if not owner AND not operator
OperableRepo._onlyOwnerOrOperator();
```

### Modifiers

```solidity
// Only global or function-level operators
modifier onlyOperator() {
    OperableRepo._onlyOperator();
    _;
}

// Owner OR any operator
modifier onlyOwnerOrOperator() {
    OperableRepo._onlyOwnerOrOperator();
    _;
}
```

## ReentrancyLock

Transient storage-based reentrancy protection (EIP-1153).

### Usage

```solidity
modifier nonReentrant() {
    ReentrancyLockRepo._onlyUnlocked();
    ReentrancyLockRepo._lock();
    _;
    ReentrancyLockRepo._unlock();
}
```

### Functions

```solidity
// Lock the reentrancy guard
ReentrancyLockRepo._lock();

// Unlock the reentrancy guard
ReentrancyLockRepo._unlock();

// Check if locked
bool locked = ReentrancyLockRepo._isLocked();

// Revert if locked (guard function)
ReentrancyLockRepo._onlyUnlocked();
```

### Benefits

- Uses transient storage (cleared after transaction)
- Gas efficient compared to storage-based guards
- Protects against cross-function reentrancy

## Component Files

| Component | Files |
|-----------|-------|
| MultiStepOwnable | `MultiStepOwnableRepo.sol`, `MultiStepOwnableModifiers.sol`, `MultiStepOwnableTarget.sol`, `MultiStepOwnableFacet.sol` |
| Operable | `OperableRepo.sol`, `OperableModifiers.sol`, `OperableTarget.sol`, `OperableFacet.sol` |
| ReentrancyLock | `ReentrancyLockRepo.sol`, `ReentrancyLockModifiers.sol`, `ReentrancyLockTarget.sol`, `ReentrancyLockFacet.sol` |

## AccessFacetFactoryService

Deploy access control facets:

```solidity
import {AccessFacetFactoryService} from "@crane/contracts/access/AccessFacetFactoryService.sol";

// Deploy MultiStepOwnable facet
IFacet ownerFacet = AccessFacetFactoryService.deployMultiStepOwnableFacet(create3Factory);

// Deploy Operable facet
IFacet operableFacet = AccessFacetFactoryService.deployOperableFacet(create3Factory);

// Deploy ReentrancyLock facet
IFacet reentrancyFacet = AccessFacetFactoryService.deployReentrancyLockFacet(create3Factory);
```

## Additional Resources

### Reference Files

For detailed patterns and examples:

- **`references/access-patterns.md`** - Complete access control integration patterns
