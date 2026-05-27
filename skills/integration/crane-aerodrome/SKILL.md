---
name: crane-aerodrome
description: This skill should be used when the user asks about "Aerodrome integration", "Aerodrome swap", "Aerodrome liquidity", "volatile pool", "stable pool", "Slipstream", "concentrated liquidity on Aerodrome", or needs to interact with Aerodrome DEX on Base using Crane's service libraries.
license: MIT
---

# Crane Aerodrome Integration

Crane provides comprehensive Aerodrome v1 and Slipstream integration with services, stubs, and test infrastructure.

## Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `AerodromServiceVolatile` | `services/AerodromServiceVolatile.sol` | Volatile pool operations (xy=k) |
| `AerodromServiceStable` | `services/AerodromServiceStable.sol` | Stable pool operations (x^3y+xy^3=k) |
| `AerodromeRouterAwareRepo` | `aware/AerodromeRouterAwareRepo.sol` | Router dependency injection |
| `AerodromePoolMetadataRepo` | `aware/AerodromePoolMetadataRepo.sol` | Pool metadata storage |
| `TestBase_Aerodrome` | `test/bases/TestBase_Aerodrome.sol` | Full protocol deployment |
| `TestBase_Aerodrome_Pools` | `test/bases/TestBase_Aerodrome_Pools.sol` | Pool creation helpers |
| `SlipstreamRewardUtils` | `slipstream/SlipstreamRewardUtils.sol` | CL reward calculations |

## Pool Types

Aerodrome has two pool types with different AMM curves:

| Type | Curve | Use Case | Service |
|------|-------|----------|---------|
| Volatile | xy = k | ETH/USDC, volatile pairs | `AerodromServiceVolatile` |
| Stable | x^3y + xy^3 = k | USDC/USDT, stablecoin pairs | `AerodromServiceStable` |

## Quick Start: Volatile Pool Swap

```solidity
import {AerodromServiceVolatile} from "@crane/contracts/protocols/dexes/aerodrome/v1/services/AerodromServiceVolatile.sol";
import {AerodromeRouterAwareRepo} from "@crane/contracts/protocols/dexes/aerodrome/v1/aware/AerodromeRouterAwareRepo.sol";

contract MyVault {
    function swap(IERC20 tokenIn, IERC20 tokenOut, uint256 amount) external {
        IRouter router = AerodromeRouterAwareRepo._router();
        IPoolFactory factory = router.defaultFactory();
        IPool pool = IPool(factory.getPool(address(tokenIn), address(tokenOut), false));

        AerodromServiceVolatile._swapVolatile(
            AerodromServiceVolatile.SwapVolatileParams({
                router: router,
                factory: factory,
                pool: pool,
                tokenIn: tokenIn,
                tokenOut: tokenOut,
                amountIn: amount,
                recipient: address(this),
                deadline: block.timestamp
            })
        );
    }
}
```

## Service Operations

### Volatile Pool Service

```solidity
// Simple swap
function _swapVolatile(SwapVolatileParams memory params) internal returns (uint256 amountOut);

// Swap and deposit in single transaction
function _swapDepositVolatile(SwapDepositVolatileParams memory params) internal returns (uint256 lpOut);

// Withdraw and swap to single token
function _withdrawSwapVolatile(WithdrawSwapVolatileParams memory params) internal returns (uint256 amountOut);

// Quote optimal swap amount for balanced deposit
function _quoteSwapDepositSaleAmtVolatile(params) internal view returns (uint256 saleAmt);
```

### Stable Pool Service

Same function signatures with `Stable` suffix:

```solidity
function _swapStable(SwapStableParams memory params) internal returns (uint256 amountOut);
function _swapDepositStable(SwapDepositStableParams memory params) internal returns (uint256 lpOut);
```

## Route Building

```solidity
IRouter.Route memory route = IRouter.Route({
    from: address(tokenIn),
    to: address(tokenOut),
    stable: false,  // true for stable pools
    factory: address(factory)
});

IRouter.Route[] memory routes = new IRouter.Route[](1);
routes[0] = route;

router.swapExactTokensForTokens(
    amountIn,
    amountOutMin,
    routes,
    recipient,
    deadline
);
```

## AwareRepo Pattern

```solidity
// Initialize during deployment
AerodromeRouterAwareRepo._initialize(router);

// Access in operations
IRouter router = AerodromeRouterAwareRepo._router();
```

## Testing

```solidity
import {TestBase_Aerodrome_Pools} from "@crane/contracts/protocols/dexes/aerodrome/v1/test/bases/TestBase_Aerodrome_Pools.sol";

contract MyTest is TestBase_Aerodrome_Pools {
    function setUp() public override {
        super.setUp();
        // aerodromeRouter, aerodromeFactory, voter, etc. available
    }

    function test_swap() public {
        // Create pool and test
    }
}
```

## Additional Resources

### Reference Files

- **`references/aerodrome-services.md`** - Detailed service patterns and examples
