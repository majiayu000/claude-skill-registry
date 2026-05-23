---
name: crane-architecture
description: This skill should be used when the user asks about "facet", "target", "repo", "diamond pattern", "storage slot", "guard function", "DFPkg", "AwareRepo", "Service pattern", "Modifiers", "ERC2535", or needs guidance on Crane's core architectural patterns for building modular, upgradeable smart contracts.
license: MIT
---

# Crane Architecture Patterns

Crane is a Diamond-first (ERC2535) Solidity development framework for building modular, upgradeable smart contracts. This skill provides guidance on the core architectural patterns.

## Core Pattern: Facet-Target-Repo

Every feature in Crane follows a three-tier architecture:

| Layer | File Pattern | Purpose |
|-------|--------------|---------|
| **Repo** | `*Repo.sol` | Storage library with assembly-based slot binding. Defines `Storage` struct and dual `_layout()` functions. No state variables. |
| **Target** | `*Target.sol` | Implementation contract with business logic. Uses Repo for storage access. Inherits interfaces. |
| **Facet** | `*Facet.sol` | Diamond facet. Extends Target and implements `IFacet` for metadata (name, interfaces, selectors). |

### When to Create Each Layer

- **Repo**: Always create first. Contains all storage and internal helper functions.
- **Target**: Create when business logic needs to be shared or tested independently.
- **Facet**: Create when exposing functionality through the Diamond proxy.

## Storage Slot Pattern

All Repos use the Diamond storage pattern with dual function overloads:

```solidity
library ExampleRepo {
    bytes32 internal constant STORAGE_SLOT = keccak256(abi.encode("crane.feature.name"));

    struct Storage {
        mapping(address => bool) isOperator;
    }

    // Parameterized version - allows custom slot
    function _layout(bytes32 slot) internal pure returns (Storage storage layout) {
        assembly { layout.slot := slot }
    }

    // Default version - uses STORAGE_SLOT
    function _layout() internal pure returns (Storage storage) {
        return _layout(STORAGE_SLOT);
    }
}
```

### Dual Function Overload Pattern

Every Repo function has TWO overloads:

```solidity
// 1. Parameterized: takes Storage as first param
function _isOperator(Storage storage layout, address query) internal view returns (bool) {
    return layout.isOperator[query];
}

// 2. Default: calls parameterized with _layout()
function _isOperator(address query) internal view returns (bool) {
    return _isOperator(_layout(), query);
}
```

This enables:
- Default usage with standard storage slot
- Custom slot usage for multi-instance patterns
- Composability between Repos

## Guard Functions Pattern

Repos contain `_onlyXxx()` guard functions with access control logic. Modifiers are thin wrappers:

```solidity
// In Repo - contains the actual check logic
function _onlyOperator(Storage storage layout) internal view {
    if (!_isOperator(layout, msg.sender) && !_isFunctionOperator(layout, msg.sig, msg.sender)) {
        revert IOperable.NotOperator(msg.sender);
    }
}

function _onlyOperator() internal view {
    _onlyOperator(_layout());
}

// In Modifiers contract - thin delegation wrapper
modifier onlyOperator() {
    OperableRepo._onlyOperator();
    _;
}
```

## Additional Patterns

### Modifiers Contract (`*Modifiers.sol`)

Abstract contracts with reusable modifiers delegating to Repo guards:

```solidity
abstract contract OperableModifiers {
    modifier onlyOperator() {
        OperableRepo._onlyOperator();
        _;
    }
}
```

### Service Library (`*Service.sol`)

Stateless libraries for complex business logic. Use structs to avoid stack-too-deep:

```solidity
library CamelotV2Service {
    struct SwapParams {
        ICamelotV2Router router;
        uint256 amountIn;
        IERC20 tokenIn;
    }

    function _swap(SwapParams memory params) internal { ... }
}
```

### AwareRepo (`*AwareRepo.sol`)

Dependency injection for external contract references:

```solidity
library BalancerV3VaultAwareRepo {
    bytes32 internal constant STORAGE_SLOT = keccak256("protocols.dexes.balancer.v3.vault.aware");

    struct Storage {
        IVault balancerV3Vault;
    }

    function _initialize(IVault vault) internal { _layout().balancerV3Vault = vault; }
    function _balancerV3Vault() internal view returns (IVault) { return _layout().balancerV3Vault; }
}
```

### Diamond Factory Package (`*DFPkg.sol`)

Bundles facets into deployable packages. See `references/dfpkg-pattern.md` for complete details.

## IFacet Interface

All facets implement `IFacet`:

```solidity
function facetName() external view returns (string memory name);
function facetInterfaces() external view returns (bytes4[] memory interfaces);
function facetFuncs() external view returns (bytes4[] memory funcs);
function facetMetadata() external view returns (string memory name, bytes4[] memory interfaces, bytes4[] memory functions);
```

## Storage Slot Naming Convention

Use hierarchical dot-notation:

| Pattern | Example |
|---------|---------|
| Crane core | `"crane.access.operable"` |
| Protocol integrations | `"protocols.dexes.balancer.v3.vault.aware"` |
| EIP implementations | `"eip.erc.8023"` |

## Key Reference Files

For complete implementations, examine these files in the Crane codebase:

- `contracts/access/operable/` - Complete Facet-Target-Repo example
- `contracts/introspection/ERC2535/ERC2535Repo.sol` - Diamond storage management
- `contracts/access/ERC8023/` - Two-step ownership (EIP-8023)
- `contracts/protocols/dexes/camelot/v2/services/CamelotV2Service.sol` - Service pattern

## Additional Resources

### Reference Files

For detailed patterns and complete examples:
- **`references/dfpkg-pattern.md`** - Diamond Factory Package pattern in depth
- **`references/factory-service.md`** - FactoryService pattern for deployment

### Quick Decision Guide

| Need | Pattern |
|------|---------|
| Storage for a feature | Create `*Repo.sol` |
| Business logic | Create `*Target.sol` or `*Service.sol` |
| Diamond-exposed functions | Create `*Facet.sol` |
| External contract reference | Create `*AwareRepo.sol` |
| Reusable access control | Create `*Modifiers.sol` |
| Deployable package | Create `*DFPkg.sol` |
