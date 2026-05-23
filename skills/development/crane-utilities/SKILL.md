---
name: crane-utilities
description: This skill should be used when the user asks about "set collections", "AddressSet", "Bytes32Set", "math utilities", "ConstProdUtils", "AMM math", "hash functions", "BetterMath", "pagination", "EIP-712", "cryptography", or needs utility libraries for Crane Diamond development.
license: MIT
---

# Crane Utility Libraries

Crane provides utility libraries for collections, math, cryptography, and common operations.

## Collections (Sets)

Diamond storage-compatible set implementations for unique value collections.

### Available Set Types

| Type | File | Use Case |
|------|------|----------|
| `AddressSet` | `AddressSetRepo.sol` | Unique addresses (operators, whitelist) |
| `Bytes32Set` | `Bytes32SetRepo.sol` | Unique hashes, identifiers |
| `Bytes4Set` | `Bytes4SetRepo.sol` | Function selectors, interface IDs |
| `StringSet` | `StringSetRepo.sol` | Unique strings |
| `UInt256Set` | `UInt256SetRepo.sol` | Unique numeric IDs |

### Set Operations

```solidity
import {AddressSet, AddressSetRepo} from "@crane/contracts/utils/collections/sets/AddressSetRepo.sol";

// In your Repo
struct Storage {
    AddressSet operators;
}

// Operations
AddressSetRepo._add(set, value);        // Add value, idempotent
AddressSetRepo._remove(set, value);     // Remove value, idempotent
AddressSetRepo._contains(set, value);   // Check presence
AddressSetRepo._length(set);            // Get count
AddressSetRepo._index(set, idx);        // Get value at index
AddressSetRepo._indexOf(set, value);    // Get index of value
AddressSetRepo._asArray(set);           // Get all values as array
```

### Pagination

For large sets, use pagination:

```solidity
// Get page of results
(address[] memory page, bool hasMore) = AddressSetRepo._getPage(
    set,
    pageIndex,   // 0-based page number
    pageSize     // Items per page
);
```

## Math Utilities

### ConstProdUtils

Core AMM math for constant product pools (xy=k):

```solidity
import {ConstProdUtils} from "@crane/contracts/utils/math/ConstProdUtils.sol";

using ConstProdUtils for uint256;

// Calculate output for swap
uint256 amountOut = ConstProdUtils._purchaseQuote(
    amountIn,         // Amount being sold
    reserveIn,        // Reserve of input token
    reserveOut,       // Reserve of output token
    feeNumerator      // Fee (e.g., 9970 for 0.3%)
);

// Calculate input needed for desired output
uint256 amountIn = ConstProdUtils._saleQuote(
    amountOut,
    reserveIn,
    reserveOut,
    feeNumerator
);

// Optimal swap amount for balanced deposit
uint256 saleAmt = ConstProdUtils._quoteSaleAmountIn(
    amountIn,
    reserveIn,
    reserveOut,
    feeNumerator
);

// Sort reserves by token address
(uint256 knownReserve, uint256 unknownReserve) = ConstProdUtils._sortReserves(
    knownToken,
    token0,
    reserve0,
    reserve1
);
```

### BetterMath

Extended math operations including 512-bit arithmetic:

```solidity
import {Uint512, BetterMath} from "@crane/contracts/utils/math/BetterMath.sol";

using BetterMath for uint256;
using BetterMath for Uint512;

// Safe operations
uint256 sum = a._add(b);              // Checked addition
uint256 diff = a._sub(b);             // Checked subtraction
uint256 prod = a._mul(b);             // Checked multiplication
uint256 quot = a._div(b);             // Checked division

// 512-bit multiplication (for intermediate precision)
Uint512 memory product = a._mul512(b);
uint256 result = product._div(c);

// Min/max
uint256 smaller = a._min(b);
uint256 larger = a._max(b);

// Percentage calculations
uint256 portion = total._mulDivDown(numerator, denominator);
uint256 portionUp = total._mulDivUp(numerator, denominator);
```

## Cryptography

### EIP-712 (Typed Data Hashing)

```solidity
import {EIP712Repo} from "@crane/contracts/utils/cryptography/EIP712/EIP712Repo.sol";

// Initialize in DFPkg
EIP712Repo._initialize("MyContract", "1");

// Build domain separator
bytes32 domainSeparator = EIP712Repo._domainSeparator();

// Hash typed data
bytes32 digest = keccak256(abi.encodePacked(
    "\x19\x01",
    domainSeparator,
    structHash
));
```

### BetterEfficientHashLib

Optimized hashing:

```solidity
import {BetterEfficientHashLib} from "@crane/contracts/utils/BetterEfficientHashLib.sol";

using BetterEfficientHashLib for bytes;

// Hash bytes efficiently
bytes32 hash = someBytes._hash();

// Hash for CREATE3 salt
bytes32 salt = abi.encode(value)._hash();
```

## String & Bytes Utilities

### BetterStrings

```solidity
import {BetterStrings} from "@crane/contracts/utils/BetterStrings.sol";

using BetterStrings for string;

string memory result = str1._concat(str2);
bool isEmpty = str._isEmpty();
uint256 len = str._length();
```

### BetterBytes

```solidity
import {BetterBytes} from "@crane/contracts/utils/BetterBytes.sol";

using BetterBytes for bytes;

bytes memory slice = data._slice(start, length);
bytes memory concat = data1._concat(data2);
```

### Bytes32 & Bytes4

```solidity
import {Bytes32} from "@crane/contracts/utils/Bytes32.sol";
import {Bytes4} from "@crane/contracts/utils/Bytes4.sol";

using Bytes32 for bytes32;
using Bytes4 for bytes4;

// Convert to hex string
string memory hex32 = someHash._toHexString();
string memory hex4 = someSelector._toHexString();
```

## Address Utilities

```solidity
import {BetterAddress} from "@crane/contracts/utils/BetterAddress.sol";

using BetterAddress for address;

// Check if address is contract
bool isContract = addr._isContract();

// Safe ETH transfer
addr._sendValue(amount);
```

## Constants

Network and protocol constants:

```solidity
import "@crane/contracts/constants/Constants.sol";

// Global constants
uint256 constant WAD = 1e18;
uint256 constant RAY = 1e27;

// Network-specific
import "@crane/contracts/constants/networks/BASE_MAIN.sol";
// Provides addresses for Base mainnet

// Protocol constants
import "@crane/contracts/constants/protocols/utils/permit2/PERMIT2_CONSTANTS.sol";
// Provides Permit2 addresses
```

## File Organization

```
contracts/utils/
├── collections/
│   └── sets/
│       ├── AddressSetRepo.sol
│       ├── Bytes32SetRepo.sol
│       ├── Bytes4SetRepo.sol
│       ├── StringSetRepo.sol
│       └── UInt256SetRepo.sol
├── cryptography/
│   ├── EIP712/
│   │   └── EIP712Repo.sol
│   ├── ERC5267/
│   │   └── ERC5267Facet.sol
│   └── hash/
│       └── *.sol
├── math/
│   ├── BetterMath.sol
│   ├── ConstProdUtils.sol
│   └── [Protocol]Utils.sol
├── BetterAddress.sol
├── BetterBytes.sol
├── BetterEfficientHashLib.sol
├── BetterStrings.sol
├── Bytes32.sol
├── Bytes4.sol
└── UInt256.sol
```

## Additional Resources

### Reference Files

For detailed utility patterns and examples:

- **`references/utility-patterns.md`** - Complete usage patterns and examples
