---
name: crane-camelot
description: This skill should be used when the user asks about "Camelot integration", "Camelot swap", "Camelot liquidity", "Camelot V2", "fee-on-transfer tokens", "asymmetric fees", "directional fees", or needs to interact with Camelot DEX on Arbitrum using Crane's service library.
license: MIT
---

# Crane Camelot V2 Integration

Crane provides Camelot V2 integration with service library, stubs, and test infrastructure. Camelot differs from standard Uniswap V2 forks by supporting asymmetric (directional) fees.

## Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `CamelotV2Service` | `services/CamelotV2Service.sol` | Swap, deposit, withdraw operations |
| `CamelotV2RouterAwareRepo` | `CamelotV2RouterAwareRepo.sol` | Router dependency injection |
| `CamelotV2FactoryAwareRepo` | `CamelotV2FactoryAwareRepo.sol` | Factory dependency injection |
| `TestBase_CamelotV2` | `test/bases/TestBase_CamelotV2.sol` | Full protocol deployment |

## Key Difference: Asymmetric Fees

Camelot pools have **directional fees** - different fees for each swap direction:

```solidity
// Camelot's getReserves returns fees for each direction
(uint112 reserve0, uint112 reserve1, uint16 token0feePercent, uint16 token1FeePercent) = pool.getReserves();

// token0feePercent: Fee when swapping token0 -> token1
// token1FeePercent: Fee when swapping token1 -> token0
```

## Quick Start: Execute Swap

```solidity
import {CamelotV2Service} from "@crane/contracts/protocols/dexes/camelot/v2/services/CamelotV2Service.sol";
import {ICamelotV2Router} from "@crane/contracts/interfaces/protocols/dexes/camelot/v2/ICamelotV2Router.sol";
import {ICamelotPair} from "@crane/contracts/interfaces/protocols/dexes/camelot/v2/ICamelotPair.sol";

contract CamelotSwapper {
    ICamelotV2Router public router;

    function swap(
        ICamelotPair pool,
        IERC20 tokenIn,
        IERC20 tokenOut,
        uint256 amountIn
    ) external returns (uint256 amountOut) {
        tokenIn.transferFrom(msg.sender, address(this), amountIn);

        amountOut = CamelotV2Service._swap(
            router,
            pool,
            amountIn,
            tokenIn,
            tokenOut,
            address(0)  // referrer (optional)
        );
    }
}
```

## Service Operations

### Deposit (Add Liquidity)

```solidity
function _deposit(
    ICamelotV2Router router,
    IERC20 tokenA,
    IERC20 tokenB,
    uint256 amountADesired,
    uint256 amountBDesired
) internal returns (uint256 liquidity);
```

### Withdraw (Remove Liquidity)

```solidity
// Direct withdrawal (no router)
function _withdrawDirect(
    ICamelotPair pool,
    uint256 amt
) internal returns (uint256 amount0, uint256 amount1);
```

### Swap

```solidity
// Swap with pool auto-detection
function _swap(
    ICamelotV2Router router,
    ICamelotPair pool,
    uint256 amountIn,
    IERC20 tokenIn,
    IERC20 tokenOut,
    address referrer
) internal returns (uint256 amountOut);

// Swap with explicit reserves and fees
function _swap(
    ICamelotV2Router router,
    uint256 amountIn,
    IERC20 tokenIn,
    uint256 reserveIn,
    uint256 feePercent,
    IERC20 tokenOut,
    uint256 reserveOut,
    address referrer
) internal returns (uint256 amountOut);
```

### Swap and Deposit (Zap In)

```solidity
function _swapDeposit(
    ICamelotV2Router router,
    ICamelotPair pool,
    IERC20 tokenIn,
    uint256 saleAmt,
    IERC20 opToken,
    address referrer
) internal returns (uint256 lpAmount);
```

### Withdraw and Swap (Zap Out)

```solidity
function _withdrawSwapDirect(
    ICamelotPair pool,
    ICamelotV2Router router,
    uint256 amt,
    IERC20 tokenOut,
    IERC20 opToken,
    address referrer
) internal returns (uint256 amountOut);
```

## Reserve Sorting

Get reserves sorted by known token:

```solidity
(
    uint256 knownReserve,
    uint256 opposingReserve,
    uint256 knownFeePercent,
    uint256 opposingFeePercent
) = CamelotV2Service._sortReserves(pool, knownToken);
```

## Testing

```solidity
import {TestBase_CamelotV2} from "@crane/contracts/protocols/dexes/camelot/v2/test/bases/TestBase_CamelotV2.sol";

contract MyTest is TestBase_CamelotV2 {
    function setUp() public override {
        super.setUp();
        // camelotV2Factory and camelotV2Router available
    }

    function test_swap() public {
        // Create pair
        address pair = camelotV2Factory.createPair(
            address(tokenA),
            address(tokenB)
        );

        // Add liquidity
        CamelotV2Service._deposit(
            camelotV2Router,
            tokenA,
            tokenB,
            1000e18,
            1000e18
        );

        // Execute swap
        uint256 amountOut = CamelotV2Service._swap(
            camelotV2Router,
            ICamelotPair(pair),
            100e18,
            tokenA,
            tokenB,
            address(0)
        );
    }
}
```

## Fee-on-Transfer Token Support

Camelot uses `swapExactTokensForTokensSupportingFeeOnTransferTokens` to support deflationary tokens:

```solidity
router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
    amountIn,
    amountOutMin,
    path,
    to,
    referrer,
    deadline
);
```

## File Organization

```
contracts/protocols/dexes/camelot/v2/
├── services/
│   └── CamelotV2Service.sol
├── CamelotV2RouterAwareRepo.sol
├── CamelotV2FactoryAwareRepo.sol
├── stubs/
│   ├── CamelotFactory.sol
│   ├── CamelotRouter.sol
│   ├── CamelotPair.sol
│   └── libraries/
│       ├── Math.sol
│       ├── SafeMath.sol
│       └── UniswapV2Library.sol
└── test/bases/
    └── TestBase_CamelotV2.sol
```

## Additional Resources

### Reference Files

- **`references/camelot-services.md`** - Detailed patterns and examples
