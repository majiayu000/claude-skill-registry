---
name: crane-uniswap
description: This skill should be used when the user asks about "Uniswap integration", "Uniswap V2 swap", "Uniswap V2 liquidity", "UniswapV2Service", "Uniswap V3", "Uniswap V4", "concentrated liquidity", or needs to interact with Uniswap DEX using Crane's service libraries.
license: MIT
---

# Crane Uniswap Integration

Crane provides Uniswap V2, V3, and V4 integration with services, stubs, libraries, and test infrastructure.

## Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `UniswapV2Service` | `v2/services/UniswapV2Service.sol` | V2 swap, deposit, withdraw operations |
| `UniswapV2RouterAwareRepo` | `v2/aware/UniswapV2RouterAwareRepo.sol` | Router dependency injection |
| `UniswapV2FactoryAwareRepo` | `v2/aware/UniswapV2FactoryAwareRepo.sol` | Factory dependency injection |
| `TestBase_UniswapV2` | `v2/test/bases/TestBase_UniswapV2.sol` | Full protocol deployment |
| `TestBase_UniswapV2_Pools` | `v2/test/bases/TestBase_UniswapV2_Pools.sol` | Pool creation helpers |
| `UniswapV3Factory` | `v3/UniswapV3Factory.sol` | V3 factory stub |
| `UniswapV3Pool` | `v3/UniswapV3Pool.sol` | V3 pool implementation |
| `UniswapV4Utils` | `v4/utils/UniswapV4Utils.sol` | V4 utility functions |
| `UniswapV4Quoter` | `v4/utils/UniswapV4Quoter.sol` | V4 quote calculations |

## Uniswap V2 (Standard 0.3% Fee)

Unlike Camelot's directional fees, Uniswap V2 uses a fixed 0.3% fee:

```solidity
// UniswapV2Service always uses 300 (0.3%) for fee calculations
feePercent = 300;
```

## Quick Start: Execute V2 Swap

```solidity
import {UniswapV2Service} from "@crane/contracts/protocols/dexes/uniswap/v2/services/UniswapV2Service.sol";
import {IUniswapV2Router} from "@crane/contracts/interfaces/protocols/dexes/uniswap/v2/IUniswapV2Router.sol";
import {IUniswapV2Pair} from "@crane/contracts/interfaces/protocols/dexes/uniswap/v2/IUniswapV2Pair.sol";

contract UniswapSwapper {
    IUniswapV2Router public router;

    function swap(
        IUniswapV2Pair pool,
        IERC20 tokenIn,
        IERC20 tokenOut,
        uint256 amountIn
    ) external returns (uint256 amountOut) {
        tokenIn.transferFrom(msg.sender, address(this), amountIn);

        amountOut = UniswapV2Service._swap(
            router,
            pool,
            amountIn,
            tokenIn,
            tokenOut
        );
    }
}
```

## V2 Service Operations

### Deposit (Add Liquidity)

```solidity
function _deposit(
    IUniswapV2Router router,
    IERC20 tokenA,
    IERC20 tokenB,
    uint256 amountADesired,
    uint256 amountBDesired
) internal returns (uint256 liquidity);
```

### Withdraw (Remove Liquidity)

```solidity
function _withdrawDirect(
    IUniswapV2Pair pool,
    uint256 amt
) internal returns (uint256 amount0, uint256 amount1);
```

### Swap

```solidity
// Swap with pool auto-detection
function _swap(
    IUniswapV2Router router,
    IUniswapV2Pair pool,
    uint256 amountIn,
    IERC20 tokenIn,
    IERC20 tokenOut
) internal returns (uint256 amountOut);

// Swap exact tokens for tokens
function _swapExactTokensForTokens(
    IUniswapV2Router router,
    IERC20 tokenIn,
    uint256 amountIn,
    IERC20 tokenOut,
    uint256 minAmountOut,
    address recipient
) internal returns (uint256 amountOut);

// Swap tokens for exact tokens
function _swapTokensForExactTokens(
    IUniswapV2Router router,
    IERC20 tokenIn,
    uint256 amountInMax,
    IERC20 tokenOut,
    uint256 amountOut,
    address recipient
) internal returns (uint256 amountIn);
```

### Swap and Deposit (Zap In)

```solidity
function _swapDeposit(
    IUniswapV2Router router,
    IUniswapV2Pair pool,
    IERC20 tokenIn,
    uint256 saleAmt,
    IERC20 opToken
) internal returns (uint256 lpAmount);
```

### Withdraw and Swap (Zap Out)

```solidity
function _withdrawSwapDirect(
    IUniswapV2Pair pool,
    IUniswapV2Router router,
    uint256 amt,
    IERC20 tokenOut,
    IERC20 opToken
) internal returns (uint256 amountOut);
```

## Reserve Sorting

```solidity
(
    uint256 knownReserve,
    uint256 opposingReserve,
    uint256 feePercent,
    uint256 unknownFee
) = UniswapV2Service._sortReserves(pool, knownToken);
```

## Testing V2

```solidity
import {TestBase_UniswapV2} from "@crane/contracts/protocols/dexes/uniswap/v2/test/bases/TestBase_UniswapV2.sol";

contract MyTest is TestBase_UniswapV2 {
    function setUp() public override {
        super.setUp();
        // uniswapV2Factory and uniswapV2Router available
    }

    function test_swap() public {
        address pair = uniswapV2Factory.createPair(
            address(tokenA),
            address(tokenB)
        );

        // Add liquidity
        UniswapV2Service._deposit(
            uniswapV2Router,
            tokenA,
            tokenB,
            1000e18,
            1000e18
        );

        // Execute swap
        uint256 amountOut = UniswapV2Service._swap(
            uniswapV2Router,
            IUniswapV2Pair(pair),
            100e18,
            tokenA,
            tokenB
        );
    }
}
```

## Uniswap V3 (Concentrated Liquidity)

Crane includes V3 pool and factory stubs with math libraries:

```
contracts/protocols/dexes/uniswap/v3/
├── UniswapV3Factory.sol
├── UniswapV3Pool.sol
├── UniswapV3PoolDeployer.sol
├── NoDelegateCall.sol
├── interfaces/
│   ├── IUniswapV3Factory.sol
│   ├── IUniswapV3Pool.sol
│   └── pool/
│       ├── IUniswapV3PoolActions.sol
│       └── ...
└── libraries/
    ├── TickMath.sol
    ├── SqrtPriceMath.sol
    ├── SwapMath.sol
    ├── FullMath.sol
    └── ...
```

## Uniswap V4 (Hooks)

Crane includes V4 utilities and quoter:

```solidity
import {UniswapV4Utils} from "@crane/contracts/protocols/dexes/uniswap/v4/utils/UniswapV4Utils.sol";
import {UniswapV4Quoter} from "@crane/contracts/protocols/dexes/uniswap/v4/utils/UniswapV4Quoter.sol";

// Quote a swap
UniswapV4Quoter.quoteSwap(poolKey, amountIn, zeroForOne);

// Quote a zap (single-token deposit)
UniswapV4ZapQuoter.quoteZap(poolKey, amountIn, token);
```

## File Organization

```
contracts/protocols/dexes/uniswap/
├── v2/
│   ├── services/
│   │   └── UniswapV2Service.sol
│   ├── aware/
│   │   ├── UniswapV2RouterAwareRepo.sol
│   │   └── UniswapV2FactoryAwareRepo.sol
│   ├── stubs/
│   │   ├── UniV2Factory.sol
│   │   ├── UniV2Pair.sol
│   │   ├── UniV2Router02.sol
│   │   └── deps/libs/
│   │       ├── Math.sol
│   │       ├── UniswapV2Library.sol
│   │       └── ...
│   └── test/bases/
│       ├── TestBase_UniswapV2.sol
│       └── TestBase_UniswapV2_Pools.sol
├── v3/
│   ├── UniswapV3Factory.sol
│   ├── UniswapV3Pool.sol
│   ├── interfaces/
│   │   └── ...
│   ├── libraries/
│   │   ├── TickMath.sol
│   │   ├── SqrtPriceMath.sol
│   │   └── ...
│   └── test/bases/
│       └── TestBase_UniswapV3.sol
└── v4/
    ├── interfaces/
    │   ├── IHooks.sol
    │   └── IPoolManager.sol
    ├── libraries/
    │   └── ...
    ├── types/
    │   ├── Currency.sol
    │   ├── PoolId.sol
    │   └── PoolKey.sol
    └── utils/
        ├── UniswapV4Utils.sol
        ├── UniswapV4Quoter.sol
        └── UniswapV4ZapQuoter.sol
```

## Storage Slots (AwareRepos)

| Repo | Slot |
|------|------|
| UniswapV2RouterAwareRepo | `"protocols.dexes.uniswap.v2.router.aware"` |
| UniswapV2FactoryAwareRepo | `"protocols.dexes.uniswap.v2.factory.aware"` |

## Additional Resources

### Reference Files

- **`references/uniswap-services.md`** - Detailed patterns and examples
