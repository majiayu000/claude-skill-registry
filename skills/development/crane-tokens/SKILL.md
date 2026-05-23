---
name: crane-tokens
description: This skill should be used when the user asks to "deploy an ERC20 token", "create a token", "implement ERC20", "add permit to token", "mint/burn functionality", "ERC4626 vault", "tokenized vault", "ERC721 NFT", or needs guidance on token standards implementation with Crane's Diamond Factory Packages.
license: MIT
---

# Crane Token Components

Crane provides pre-built Diamond Factory Packages (DFPkg) for deploying ERC20, ERC20Permit, and ERC4626 tokens as Diamond proxies.

## Token Package Selection

| Need | Package | Features |
|------|---------|----------|
| Basic ERC20 | `ERC20DFPkg` | Transfer, approve, metadata |
| ERC20 + Permit | `ERC20PermitDFPkg` | + EIP-2612 gasless approvals |
| Full-featured token | `ERC20PermitMintBurnLockedOwnableDFPkg` | + Mint/burn with owner control |

## Quick Start: Deploy ERC20 with Permit

```solidity
import {ERC20PermitDFPkg, IERC20PermitDFPkg} from "@crane/contracts/tokens/ERC20/ERC20PermitDFPkg.sol";
import {IERC20} from "@crane/contracts/interfaces/IERC20.sol";

// 1. Deploy facets (typically done once via FactoryService)
IFacet erc20Facet = factory.deployFacet(type(ERC20Facet).creationCode, salt);
IFacet erc5267Facet = factory.deployFacet(type(ERC5267Facet).creationCode, salt);
IFacet erc2612Facet = factory.deployFacet(type(ERC2612Facet).creationCode, salt);

// 2. Deploy package with facet references
ERC20PermitDFPkg pkg = new ERC20PermitDFPkg(IERC20PermitDFPkg.PkgInit({
    erc20Facet: erc20Facet,
    erc5267Facet: erc5267Facet,
    erc2612Facet: erc2612Facet
}));

// 3. Deploy token instance via Diamond factory
IERC20 token = IERC20(diamondFactory.deploy(
    pkg,
    abi.encode(IERC20PermitDFPkg.PkgArgs({
        name: "My Token",
        symbol: "MTK",
        decimals: 18,
        totalSupply: 1_000_000e18,
        recipient: msg.sender,
        optionalSalt: bytes32(0)
    }))
));
```

## Available Packages

### ERC20DFPkg

Basic ERC20 token with metadata.

**PkgInit** (constructor):
```solidity
struct PkgInit {
    IFacet erc20Facet;
}
```

**PkgArgs** (deployment):
```solidity
struct PkgArgs {
    string name;
    string symbol;
    uint8 decimals;      // Defaults to 18 if 0
    uint256 totalSupply; // Initial mint amount
    address recipient;   // Required if totalSupply > 0
    bytes32 optionalSalt;
}
```

**Interfaces**: `IERC20`, `IERC20Metadata`

### ERC20PermitDFPkg

ERC20 with EIP-2612 permit (gasless approvals).

**PkgInit**:
```solidity
struct PkgInit {
    IFacet erc20Facet;
    IFacet erc5267Facet;   // EIP-5267 domain separator
    IFacet erc2612Facet;   // EIP-2612 permit
}
```

**PkgArgs**: Same as ERC20DFPkg

**Interfaces**: `IERC20`, `IERC20Metadata`, `IERC20Permit`, `IERC5267`

### ERC20PermitMintBurnLockedOwnableDFPkg

Full-featured token with owner-controlled mint/burn and time-locked ownership transfer.

**PkgInit**:
```solidity
struct PkgInit {
    IFacet erc20Facet;
    IFacet erc5267Facet;
    IFacet erc2612Facet;
    IFacet erc20MintBurnOwnableFacet;
    IDiamondPackageCallBackFactory diamondFactory;
}
```

**PkgArgs**:
```solidity
struct PkgArgs {
    string name;
    string symbol;
    uint8 decimals;
    address owner;        // Initial owner (mint/burn access)
    bytes32 optionalSalt;
}
```

**Interfaces**: `IERC20`, `IERC20Metadata`, `IERC20Permit`, `IERC5267`, `IERC20MintBurn`

**Convenience deploy function**:
```solidity
function deployToken(
    string memory name,
    string memory symbol,
    uint8 decimals,
    address owner,
    bytes32 optionalSalt
) external returns (address tokenAddress);
```

## Token Component Files

| File | Purpose |
|------|---------|
| `ERC20Repo.sol` | Diamond storage for balances, allowances, metadata |
| `ERC20Target.sol` | Business logic (transfer, approve, etc.) |
| `ERC20Facet.sol` | Diamond facet exposing IERC20 + IFacet |
| `ERC20PermitTarget.sol` | Permit extension logic |
| `ERC20PermitFacet.sol` | Diamond facet for permit |
| `ERC20MintBurnOwnableFacet.sol` | Mint/burn with onlyOwner modifier |

## Storage Pattern

Tokens use standard Crane Repo pattern:

```solidity
library ERC20Repo {
    bytes32 internal constant STORAGE_SLOT = keccak256("eip.erc.20");

    struct Storage {
        string name;
        string symbol;
        uint8 decimals;
        uint256 totalSupply;
        mapping(address => uint256) balanceOf;
        mapping(address => mapping(address => uint256)) allowance;
    }

    function _initialize(string memory name_, string memory symbol_, uint8 decimals_) internal;
    function _mint(address to_, uint256 amount_) internal;
    function _burn(address from_, uint256 amount_) internal;
    function _transfer(address from_, address to_, uint256 amount_) internal;
}
```

## Testing Tokens

Use the provided TestBase contracts:

```solidity
import {TestBase_ERC20} from "@crane/contracts/tokens/ERC20/TestBase_ERC20.sol";
import {TestBase_ERC20Permit} from "@crane/contracts/tokens/ERC20/TestBase_ERC20Permit.sol";

contract MyToken_Test is TestBase_ERC20Permit {
    function _deployToken() internal override returns (IERC20Permit) {
        // Deploy your token instance
    }
}
```

## Additional Resources

### Reference Files

For detailed implementation patterns and examples:

- **`references/token-packages.md`** - Complete package comparison and deployment patterns
