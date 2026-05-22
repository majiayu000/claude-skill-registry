---
name: Crane Testing
description: This skill should be used when the user asks about "testbase", "behavior library", "invariant test", "handler", "fuzz test", "test pattern", "Behavior_", "TestBase_", or needs guidance on Crane's testing infrastructure for writing comprehensive smart contract tests.
version: 0.1.0
---

# Crane Testing Patterns

Crane uses structured testing patterns with TestBase contracts, Behavior libraries, and Handler contracts for comprehensive coverage.

## Test Directory Structure

Test infrastructure lives in `contracts/`, test specs live in `test/`:

```
contracts/                              # Test infrastructure WITH the code
├── access/ERC8023/
│   ├── MultiStepOwnableRepo.sol
│   ├── MultiStepOwnableFacet.sol
│   └── TestBase_IMultiStepOwnable.sol  # TestBase next to implementation
├── introspection/ERC165/
│   ├── ERC165Facet.sol
│   ├── TestBase_IERC165.sol            # Behavior testing
│   └── Behavior_IERC165.sol            # Validation library
└── test/
    ├── stubs/                          # Example implementations
    ├── comparators/                    # Assertion helpers
    └── behaviors/                      # Shared behavior utilities

test/foundry/spec/                      # Actual test specs mirror contracts/
├── access/ERC8023/
│   └── MultiStepOwnable.t.sol
└── introspection/ERC165/
    └── ERC165Facet.t.sol
```

## TestBase Pattern

Two types of TestBase contracts exist:

### Protocol Setup TestBase

Sets up protocol infrastructure with inheritance chains:

```solidity
abstract contract TestBase_CamelotV2 is TestBase_Weth9 {
    ICamelotFactory internal camelotV2Factory;
    ICamelotV2Router internal camelotV2Router;

    function setUp() public virtual override {
        TestBase_Weth9.setUp();  // Call parent setUp
        if (address(camelotV2Factory) == address(0)) {
            camelotV2Factory = new CamelotFactory(feeToSetter);
        }
        if (address(camelotV2Router) == address(0)) {
            camelotV2Router = new CamelotRouter(address(camelotV2Factory), address(weth));
        }
    }
}
```

### Behavior TestBase

Defines expected behavior via virtual functions:

```solidity
abstract contract TestBase_IFacet is Test {
    IFacet internal testFacet;

    function setUp() public virtual {
        testFacet = facetTestInstance();
    }

    // Virtual functions - inheritors return expected values
    function facetTestInstance() public virtual returns (IFacet);
    function controlFacetInterfaces() public view virtual returns (bytes4[] memory);
    function controlFacetFuncs() public view virtual returns (bytes4[] memory);

    // Test functions validate actual vs expected
    function test_IFacet_FacetInterfaces() public {
        assertTrue(Behavior_IFacet.areValid_IFacet_facetInterfaces(
            testFacet, controlFacetInterfaces(), testFacet.facetInterfaces()
        ));
    }
}
```

## Behavior Libraries (`Behavior_*.sol`)

Libraries encapsulating validation logic for interface compliance. Named `Behavior_I{Interface}`:

```solidity
library Behavior_IERC165 {
    // expect_* - Store expected values in ComparatorRepo
    function expect_IERC165_supportsInterface(IERC165 subject, bytes4[] memory expectedInterfaces_) public {
        Bytes4SetComparatorRepo._recExpectedBytes4(
            address(subject), IERC165.supportsInterface.selector, expectedInterfaces_
        );
    }

    // isValid_* - Compare expected vs actual directly
    function isValid_IERC165_supportsInterfaces(IERC165 subject, bool expected, bool actual)
        public view returns (bool valid)
    {
        valid = expected == actual;
        if (!valid) {
            console.logBehaviorError(...);
        }
    }

    // hasValid_* - Validate against stored expectations
    function hasValid_IERC165_supportsInterface(IERC165 subject) public view returns (bool isValid_) {
        for (uint256 i = 0; i < expectedCount; i++) {
            bytes4 interfaceId = _expected_IERC165_supportsInterface(subject)._index(i);
            isValid_ = isValid_ && subject.supportsInterface(interfaceId);
        }
    }
}
```

### Behavior Function Types

| Pattern | Purpose | Example |
|---------|---------|---------|
| `expect_*` | Store expected values | `expect_IERC165_supportsInterface(subject, interfaces)` |
| `isValid_*` / `areValid_*` | Compare expected vs actual directly | `isValid_IERC165_supportsInterfaces(subject, true, actual)` |
| `hasValid_*` | Validate against stored expectations | `hasValid_IERC165_supportsInterface(subject)` |

## Handler Pattern (Invariant Testing)

For fuzz/invariant testing, use a Handler + TestBase pattern:

### Handler Contract

Wraps Subject Under Test (SUT), exposes fuzzable operations, tracks expected state:

```solidity
contract ERC20TargetStubHandler is Test {
    IERC20 public sut;
    mapping(bytes32 => uint256) internal _expectedAllowance;

    function transfer(uint256 ownerSeed, uint256 toSeed, uint256 amount) external {
        address owner = addrFromSeed(ownerSeed);  // Normalize fuzz input
        address to = addrFromSeed(toSeed);

        uint256 bal = sut.balanceOf(owner);
        vm.prank(owner);

        if (amount > bal) {
            vm.expectRevert(...);  // Declare expected revert
            sut.transfer(to, amount);
            return;
        }

        vm.expectEmit(true, true, false, true);  // Declare expected event
        emit IERC20.Transfer(owner, to, amount);
        sut.transfer(to, amount);
    }
}
```

### Invariant TestBase

Declares invariants and virtual deployment functions:

```solidity
abstract contract TestBase_ERC20 is Test {
    ERC20TargetStubHandler public handler;

    function _deployToken(ERC20TargetStubHandler handler_) internal virtual returns (IERC20);

    function setUp() public virtual {
        handler = new ERC20TargetStubHandler();
        IERC20 token = _deployToken(handler);
        handler.attachToken(token);

        targetContract(address(handler));
        targetSelector(FuzzSelector({
            addr: address(handler),
            selectors: [handler.transfer.selector, handler.approve.selector]
        }));
    }

    function invariant_totalSupply_equals_sumBalances() public view {
        address[] memory addrs = handler.asAddresses();
        uint256 sum = 0;
        for (uint256 i = 0; i < addrs.length; i++) {
            sum += handler.balanceOf(addrs[i]);
        }
        assertEq(sum, handler.totalSupply());
    }
}
```

## TestBase Inheritance Chain

```
CraneTest                          # Factory setup (create3Factory, diamondFactory)
    └── TestBase_Weth9             # WETH deployment
        └── TestBase_CamelotV2     # Camelot factory + router
            └── TestBase_CamelotV2_Pools  # Pool creation helpers
                └── YourTest.t.sol  # Actual test contract
```

## Key Conventions

- Handler normalizes fuzz inputs: `addrFromSeed(seed)` maps to small address set
- Handler tracks expected state: `_expectedAllowance`, `_seen`, etc.
- Invariant functions named `invariant_*` for Foundry discovery
- Use `vm.expectRevert` / `vm.expectEmit` to declare expected behavior
- TestBase declares virtual `_deploy*` functions for SUT injection

## Additional Resources

### Reference Files

- **`references/behavior-library.md`** - Complete Behavior library guide
- **`references/handler-pattern.md`** - Invariant testing with Handlers

### Key Files

- `/contracts/test/CraneTest.sol` - Base with factory infrastructure
- `/contracts/introspection/ERC165/Behavior_IERC165.sol` - Behavior example
- `/contracts/tokens/ERC20/TestBase_ERC20.sol` - Invariant testing example
- `/contracts/test/comparators/Bytes4SetComparator.sol` - Set comparison
