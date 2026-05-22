---
name: crane-deployment
description: This skill should be used when the user asks about "create3", "deploy", "diamond factory", "package", "deterministic deployment", "cross-chain", "DiamondPackageCallBackFactory", "FactoryService", or needs guidance on deploying Diamond proxies and facets using Crane's factory system.
license: MIT
---

# Crane Deployment Patterns

Crane uses a two-factory system for deterministic cross-chain deployments of Diamond proxies.

## Factory Hierarchy

```
Create3Factory                    # Deploys facets, packages, and any contract
    └── DiamondPackageCallBackFactory   # Deploys Diamond proxy instances from packages
```

## Deployment Flow

### Step 1: Initialize Factories

In test `setUp()` or deployment scripts:

```solidity
(ICreate3Factory factory, IDiamondPackageCallBackFactory diamondFactory) =
    InitDevService.initEnv(address(this));
```

### Step 2: Deploy Facets

Use Create3Factory to deploy facets with deterministic addresses:

```solidity
IFacet erc20Facet = factory.deployFacet(
    type(ERC20Facet).creationCode,
    abi.encode(type(ERC20Facet).name)._hash()  // Salt from name hash
);
```

### Step 3: Deploy Package

Deploy package with facet references in constructor:

```solidity
IERC20DFPkg erc20Pkg = IERC20DFPkg(address(
    factory.deployPackageWithArgs(
        type(ERC20DFPkg).creationCode,
        abi.encode(IERC20DFPkg.PkgInit({ erc20Facet: erc20Facet })),  // Constructor args
        abi.encode(type(ERC20DFPkg).name)._hash()  // Salt
    )
));
```

### Step 4: Deploy Diamond Proxy Instances

```solidity
// Option A: Via package's deploy() helper
IERC20 token = erc20Pkg.deploy(diamondFactory, "Token", "TKN", 18, 1000e18, recipient, bytes32(0));

// Option B: Via factory directly
address proxy = diamondFactory.deploy(pkg, abi.encode(pkgArgs));
```

## Key Components

| Component | Purpose |
|-----------|---------|
| `Create3Factory` | Deploys any contract with deterministic addresses via CREATE3 |
| `DiamondPackageCallBackFactory` | Deploys Diamond proxies, calls `initAccount()` via delegatecall |
| `IDiamondFactoryPackage` | Interface for packages - bundles facets + initialization logic |
| `InitDevService` | Library to bootstrap the factory system in tests |

## Create3Factory Methods

### `deployFacet()`

Deploy a facet (no constructor args):

```solidity
IFacet facet = factory.deployFacet(
    type(MyFacet).creationCode,
    salt
);
```

### `deployPackageWithArgs()`

Deploy a package with constructor arguments:

```solidity
IDiamondFactoryPackage pkg = IDiamondFactoryPackage(address(
    factory.deployPackageWithArgs(
        type(MyPkg).creationCode,
        abi.encode(IMyPkg.PkgInit({ ... })),  // Constructor args
        salt
    )
));
```

### `deploy()`

Deploy any contract:

```solidity
address deployed = factory.deploy(
    creationCode,
    salt
);
```

## Salt Calculation

Always derive salt from type name for deterministic addresses:

```solidity
using BetterEfficientHashLib for bytes;

bytes32 salt = abi.encode(type(MyContract).name)._hash();
```

This ensures:
- Same address across all EVM chains
- Predictable deployment addresses
- No salt collision between different contracts

## DiamondPackageCallBackFactory Flow

1. User calls `factory.deploy(pkg, pkgArgs)`
2. Factory calculates deterministic address via `pkg.calcSalt(pkgArgs)`
3. Factory deploys `MinimalDiamondCallBackProxy` via CREATE2
4. Proxy calls back to factory's `initAccount()`
5. Factory delegatecalls `pkg.initAccount()` to initialize storage
6. Factory calls `pkg.postDeploy()` for any post-deployment hooks

## FactoryService Pattern

Group related deployments in FactoryService libraries:

```solidity
library MyFeatureFactoryService {
    using BetterEfficientHashLib for bytes;
    Vm constant vm = Vm(VM_ADDRESS);

    function deployMyFacet(ICreate3Factory factory) internal returns (IFacet) {
        IFacet facet = factory.deployFacet(
            type(MyFacet).creationCode,
            abi.encode(type(MyFacet).name)._hash()
        );
        vm.label(address(facet), type(MyFacet).name);  // Always label!
        return facet;
    }
}
```

See `references/factory-service-examples.md` for complete examples.

## Test Setup Pattern

```solidity
contract MyTest is CraneTest {
    IFacet myFacet;
    IMyDFPkg myPkg;

    function setUp() public override {
        super.setUp();  // Initializes factories

        // Deploy facet
        myFacet = create3Factory.deployFacet(
            type(MyFacet).creationCode,
            abi.encode(type(MyFacet).name)._hash()
        );
        vm.label(address(myFacet), "MyFacet");

        // Deploy package
        myPkg = IMyDFPkg(address(
            create3Factory.deployPackageWithArgs(
                type(MyDFPkg).creationCode,
                abi.encode(IMyDFPkg.PkgInit({ myFacet: myFacet })),
                abi.encode(type(MyDFPkg).name)._hash()
            )
        ));
        vm.label(address(myPkg), "MyDFPkg");
    }
}
```

## Additional Resources

### Reference Files

- **`references/factory-service-examples.md`** - Complete FactoryService examples
- **`references/deployment-scripts.md`** - Production deployment script patterns

### Key Files

- `/contracts/factories/create3/Create3Factory.sol` - CREATE3 factory
- `/contracts/factories/diamondPkg/DiamondPackageCallBackFactory.sol` - Diamond factory
- `/contracts/InitDevService.sol` - Factory initialization
- `/contracts/interfaces/IDiamondFactoryPackage.sol` - Package interface with flow diagram
