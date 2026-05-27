---
name: crane-balancer
description: This skill should be used when the user asks about "Balancer V3 integration", "Balancer pool", "weighted pool", "constant product pool", "BPT token", "Balancer vault", "rate provider", or needs to create or interact with Balancer V3 pools using Crane's DFPkg and service libraries.
license: MIT
---

# Crane Balancer V3 Integration

Crane provides comprehensive Balancer V3 integration including pool DFPkgs, vault awareness, authentication, and test infrastructure.

## Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `BalancerV3WeightedPoolDFPkg` | `pool-weighted/BalancerV3WeightedPoolDFPkg.sol` | Deploy weighted pools (80/20, custom weights) |
| `BalancerV3ConstantProductPoolDFPkg` | `pool-constProd/BalancerV3ConstantProductPoolDFPkg.sol` | Deploy 50/50 constant product pools |
| `BalancerV3VaultAwareRepo` | `vault/BalancerV3VaultAwareRepo.sol` | Vault dependency injection |
| `BalancerV3PoolRepo` | `vault/BalancerV3PoolRepo.sol` | Pool metadata storage |
| `BalancerV3WeightedPoolRepo` | `pool-weighted/BalancerV3WeightedPoolRepo.sol` | Weight storage |
| `BalancerV3AuthenticationRepo` | `vault/BalancerV3AuthenticationRepo.sol` | Pool authentication |
| `TestBase_BalancerV3Vault` | `test/bases/TestBase_BalancerV3Vault.sol` | Full vault deployment |
| `ERC4626RateProviderFacetDFPkg` | `rateProviders/ERC4626RateProviderFacetDFPkg.sol` | Rate provider for yield tokens |

## Pool Types

Crane supports two Balancer V3 pool types:

| Type | DFPkg | Use Case |
|------|-------|----------|
| Weighted | `BalancerV3WeightedPoolDFPkg` | Custom weight pools (80/20 ETH/TOKEN) |
| Constant Product | `BalancerV3ConstantProductPoolDFPkg` | 50/50 pools (x*y=k) |

## Quick Start: Deploy Weighted Pool

```solidity
import {IBalancerV3WeightedPoolDFPkg, BalancerV3WeightedPoolDFPkg} from "@crane/contracts/protocols/dexes/balancer/v3/pool-weighted/BalancerV3WeightedPoolDFPkg.sol";
import {TokenConfig, TokenType} from "@balancer-labs/v3-interfaces/contracts/vault/VaultTypes.sol";

contract MyFactory {
    BalancerV3WeightedPoolDFPkg public poolDFPkg;

    function deployPool(
        IERC20 tokenA,
        IERC20 tokenB
    ) external returns (address pool) {
        TokenConfig[] memory tokenConfigs = new TokenConfig[](2);
        tokenConfigs[0] = TokenConfig({
            token: tokenA,
            tokenType: TokenType.STANDARD,
            rateProvider: IRateProvider(address(0)),
            paysYieldFees: false
        });
        tokenConfigs[1] = TokenConfig({
            token: tokenB,
            tokenType: TokenType.STANDARD,
            rateProvider: IRateProvider(address(0)),
            paysYieldFees: false
        });

        uint256[] memory weights = new uint256[](2);
        weights[0] = 80e16;  // 80%
        weights[1] = 20e16;  // 20%

        pool = poolDFPkg.deployPool(
            tokenConfigs,
            weights,
            address(0)  // No hooks
        );
    }
}
```

## Token Configuration

Balancer V3 uses `TokenConfig` for pool tokens:

```solidity
TokenConfig({
    token: IERC20(tokenAddress),
    tokenType: TokenType.STANDARD,      // or TokenType.WITH_RATE
    rateProvider: IRateProvider(address(0)),  // or actual rate provider
    paysYieldFees: false               // true for yield-bearing tokens
})
```

### Token Types

| Type | Use Case | Rate Provider |
|------|----------|---------------|
| `STANDARD` | Regular ERC20 tokens | None required |
| `WITH_RATE` | Yield-bearing tokens (ERC4626) | Required |

## Rate Providers for ERC4626

Deploy rate providers for yield-bearing tokens:

```solidity
import {ERC4626RateProviderFacetDFPkg} from "@crane/contracts/protocols/dexes/balancer/v3/rateProviders/ERC4626RateProviderFacetDFPkg.sol";

// Deploy rate provider for ERC4626 vault
IRateProvider rateProvider = erc4626RateProviderDFPkg.deployRateProvider(IERC4626(vaultAddress));

// Use in token config
TokenConfig({
    token: IERC20(address(vault)),
    tokenType: TokenType.WITH_RATE,
    rateProvider: rateProvider,
    paysYieldFees: true
})
```

## DFPkg Initialization

`BalancerV3WeightedPoolDFPkg` requires initialization:

```solidity
struct PkgInit {
    IFacet balancerV3VaultAwareFacet;
    IFacet betterBalancerV3PoolTokenFacet;
    IFacet defaultPoolInfoFacet;
    IFacet standardSwapFeePercentageBoundsFacet;
    IFacet unbalancedLiquidityInvariantRatioBoundsFacet;
    IFacet balancerV3AuthenticationFacet;
    IFacet balancerV3WeightedPoolFacet;
    IVault balancerV3Vault;
    IDiamondPackageCallBackFactory diamondFactory;
    address poolFeeManager;
}
```

## AwareRepo Pattern

```solidity
import {BalancerV3VaultAwareRepo} from "@crane/contracts/protocols/dexes/balancer/v3/vault/BalancerV3VaultAwareRepo.sol";

// Initialize during deployment
BalancerV3VaultAwareRepo._initialize(vault);

// Access in operations
IVault vault = BalancerV3VaultAwareRepo._balancerV3Vault();
```

## Storage Slots

| Repo | Slot |
|------|------|
| BalancerV3VaultAwareRepo | `"protocols.dexes.balancer.v3.vault.aware"` |
| BalancerV3PoolRepo | `"protocols.dexes.balancer.v3.pool"` |
| BalancerV3WeightedPoolRepo | `"protocols.dexes.balancer.v3.pool.weighted"` |
| BalancerV3AuthenticationRepo | `"protocols.dexes.balancer.v3.authentication"` |

## Testing

```solidity
import {TestBase_BalancerV3Vault} from "@crane/contracts/protocols/dexes/balancer/v3/test/bases/TestBase_BalancerV3Vault.sol";

contract MyTest is TestBase_BalancerV3Vault {
    function setUp() public override {
        super.setUp();
        // vault, router, batchRouter available
        // erc4626RateProviderDFPkg available
    }

    function test_deployPool() public {
        TokenConfig[] memory configs = new TokenConfig[](2);
        configs[0] = standardTokenConfig(dai);
        configs[1] = standardTokenConfig(usdc);

        uint256[] memory weights = new uint256[](2);
        weights[0] = 50e16;
        weights[1] = 50e16;

        // Deploy and test pool
    }
}
```

## File Organization

```
contracts/protocols/dexes/balancer/v3/
├── pool-weighted/
│   ├── BalancerV3WeightedPoolDFPkg.sol
│   ├── BalancerV3WeightedPoolFacet.sol
│   ├── BalancerV3WeightedPoolTarget.sol
│   ├── BalancerV3WeightedPoolRepo.sol
│   └── WeightedTokenConfigUtils.sol
├── pool-constProd/
│   ├── BalancerV3ConstantProductPoolDFPkg.sol
│   ├── BalancerV3ConstantProductPoolFacet.sol
│   └── BalancerV3ConstantProductPoolTarget.sol
├── vault/
│   ├── BalancerV3VaultAwareRepo.sol
│   ├── BalancerV3VaultAwareFacet.sol
│   ├── BalancerV3PoolRepo.sol
│   ├── BalancerV3PoolFacet.sol
│   ├── BalancerV3AuthenticationRepo.sol
│   └── BalancerV3AuthenticationFacet.sol
├── rateProviders/
│   ├── ERC4626RateProviderFacetDFPkg.sol
│   ├── ERC4626RateProviderFacet.sol
│   └── ERC4626RateProviderTarget.sol
├── utils/
│   ├── TokenConfigUtils.sol
│   └── BalancerV38020WeightedPoolMath.sol
└── test/bases/
    ├── TestBase_BalancerV3.sol
    ├── TestBase_BalancerV3Vault.sol
    └── TestBase_BalancerV3_8020WeightedPool.sol
```

## Additional Resources

### Reference Files

- **`references/balancer-services.md`** - Detailed patterns and examples
