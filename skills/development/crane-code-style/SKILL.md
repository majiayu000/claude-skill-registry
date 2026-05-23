---
name: crane-code-style
description: This skill should be used when the user asks about "code style", "naming convention", "imports", "section headers", "slot naming", "viaIR", "stack too deep", "formatting", or needs guidance on Crane's code conventions and style requirements.
license: MIT
---

# Crane Code Style Guide

Crane follows strict code conventions for consistency and maintainability. This skill covers section headers, imports, naming, and critical compilation rules.

## Section Headers

Use 78-character wide comment blocks for major sections:

```solidity
/* -------------------------------------------------------------------------- */
/*                             Section Name                                   */
/* -------------------------------------------------------------------------- */
```

Shorter form for subsections:

```solidity
/* ------ Feature Name ------ */
```

## Import Organization

Group imports by source, with import aliases:

```solidity
// External libraries
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@solady/utils/SafeERC20.sol";

// Crane interfaces
import {IFacet} from "@crane/contracts/interfaces/IFacet.sol";
import {IOperable} from "@crane/contracts/access/operable/interfaces/IOperable.sol";

// Crane contracts
import {OperableRepo} from "@crane/contracts/access/operable/OperableRepo.sol";
import {OperableTarget} from "@crane/contracts/access/operable/OperableTarget.sol";

// Test utilities (in test files)
import {Test} from "forge-std/Test.sol";
import {Vm, VM_ADDRESS} from "forge-std/Vm.sol";
```

### Import Aliases

Defined in `foundry.toml` and `remappings.txt`:

| Alias | Path |
|-------|------|
| `@crane/` | Crane framework contracts |
| `@solady/` | Solady library |
| `@openzeppelin/` | OpenZeppelin contracts |
| `forge-std/` | Foundry test utilities |

## Function Organization

Order functions by visibility:

1. Constructor
2. Receive
3. Fallback
4. External
5. Public
6. Internal
7. Private

## Naming Conventions

| Pattern | Usage | Example |
|---------|-------|---------|
| `_layout()` | Storage access | `_layout()`, `_layout(bytes32 slot_)` |
| `_initialize()` | Storage setup | `_initialize(address owner_)` |
| `_functionName()` | Internal Repo functions | `_isOperator()`, `_setOperator()` |
| `_onlyXxx()` | Guard functions in Repos | `_onlyOwner()`, `_onlyOperator()` |
| `onlyXxx` | Modifiers | `onlyOwner`, `onlyOperator` |
| `layout` | Storage parameter name | `Storage storage layout` |
| `param_` | Function parameters | `owner_`, `slot_`, `name_` |

### Parameter Trailing Underscore

All function parameters end with underscore to avoid shadowing:

```solidity
function transfer(address to_, uint256 amount_) external {
    // to_ and amount_ don't shadow state variables
}
```

## Storage Slot Naming

Use hierarchical dot-notation for storage slot names:

| Category | Pattern | Example |
|----------|---------|---------|
| Crane core | `crane.{domain}.{feature}` | `"crane.access.operable"` |
| Protocol integrations | `protocols.{category}.{protocol}.{version}.{feature}` | `"protocols.dexes.balancer.v3.vault.aware"` |
| EIP implementations | `eip.erc.{number}` | `"eip.erc.8023"` |

```solidity
bytes32 internal constant STORAGE_SLOT = keccak256(abi.encode("crane.access.operable"));
```

## Critical: No viaIR Compilation

**NEVER enable `via_ir` or `viaIR` in foundry.toml.**

IR compilation is forbidden because:
- Dramatically slower compilation (10-100x slower)
- Excessive memory usage
- Breaks parallel agent workflows
- Not necessary when code is properly structured

### Resolving Stack Too Deep Errors

When encountering "stack too deep" errors, **refactor using structs**:

```solidity
// WRONG - too many local variables
function badFunction(
    address tokenA,
    address tokenB,
    uint256 amountA,
    uint256 amountB,
    address recipient,
    uint256 deadline
) external {
    uint256 reserveA = pair.reserveA();
    uint256 reserveB = pair.reserveB();
    uint256 totalSupply = pair.totalSupply();
    // ... stack too deep!
}

// CORRECT - group into structs
struct DepositParams {
    address tokenA;
    address tokenB;
    uint256 amountA;
    uint256 amountB;
    address recipient;
    uint256 deadline;
}

struct PoolState {
    uint256 reserveA;
    uint256 reserveB;
    uint256 totalSupply;
}

function goodFunction(DepositParams memory params) external {
    PoolState memory state = PoolState({
        reserveA: pair.reserveA(),
        reserveB: pair.reserveB(),
        totalSupply: pair.totalSupply()
    });
    // Struct members don't consume stack slots
}
```

### Stack Too Deep Solutions

1. **Group parameters into structs**: Bundle related function parameters
2. **Group intermediate state**: Use `State` or `Context` structs
3. **Use `memory` for computation**: Struct fields don't consume stack
4. **Extract helper functions**: Split complex functions
5. **Use block scoping**: Limit variable lifetimes with `{ ... }`

## Configuration

Standard Crane configuration:

- **Solidity**: 0.8.30
- **Optimizer runs**: 1 (for contract size limits)
- **EVM version**: Prague
- **via_ir**: false (ALWAYS)

## Additional Resources

### Reference Files

- **`references/complete-style-guide.md`** - Full style guide with more examples

### Key Files

- `/contracts/StyleGuide.sol` - Reference template
- `/foundry.toml` - Build configuration
- `/remappings.txt` - Import aliases
