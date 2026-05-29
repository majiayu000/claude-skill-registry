---
name: crane-natspec
description: This skill should be used when the user asks about "natspec", "documentation", "include-tag", "selector", "cast", "@custom:signature", "@custom:selector", "@custom:topiczero", "@custom:interfaceid", "AsciiDoc", or needs guidance on documenting Crane contracts with NatSpec and AsciiDoc include-tags.
license: MIT
---

# Crane NatSpec & Documentation Standards

Crane uses NatSpec combined with AsciiDoc include-tags for accurate, extractable documentation.

## AsciiDoc Include-Tags

Wrap documented symbols with include-tags for documentation extraction:

```solidity
// tag::MySymbol[]
/// @notice Description of the symbol
function myFunction() external { ... }
// end::MySymbol[]
```

### Tag Format Rules

- Tag markers must match exactly (no extra spaces inside `[]`)
- Tag name should match the symbol being documented
- Use PascalCase for tag names matching type names
- Use camelCase for function tag names

### Example Usage

```solidity
// tag::transfer[]
/// @notice Transfers tokens to a recipient
/// @param to_ The recipient address
/// @param amount_ The amount to transfer
/// @return success True if transfer succeeded
/// @custom:signature transfer(address,uint256)
/// @custom:selector 0xa9059cbb
function transfer(address to_, uint256 amount_) external returns (bool success);
// end::transfer[]
```

## Custom NatSpec Tags

### Functions

| Tag | Purpose | Example |
|-----|---------|---------|
| `@custom:signature` | Canonical signature string | `transfer(address,uint256)` |
| `@custom:selector` | bytes4 selector | `0xa9059cbb` |

```solidity
/// @notice Transfers tokens
/// @custom:signature transfer(address,uint256)
/// @custom:selector 0xa9059cbb
function transfer(address to_, uint256 amount_) external returns (bool);
```

### Errors

| Tag | Purpose | Example |
|-----|---------|---------|
| `@custom:signature` | Canonical error signature | `NotOwner(address)` |
| `@custom:selector` | bytes4 selector | `0x30cd7471` |

```solidity
/// @notice Thrown when caller is not the owner
/// @custom:signature NotOwner(address)
/// @custom:selector 0x30cd7471
error NotOwner(address caller);
```

### Events

| Tag | Purpose | Example |
|-----|---------|---------|
| `@custom:signature` | Canonical event signature | `Transfer(address,address,uint256)` |
| `@custom:topiczero` | bytes32 topic0 hash | `0xddf252ad...` |

```solidity
/// @notice Emitted on token transfer
/// @custom:signature Transfer(address,address,uint256)
/// @custom:topiczero 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
event Transfer(address indexed from, address indexed to, uint256 amount);
```

**Note**: Events use `@custom:topiczero` (bytes32), not `@custom:selector` (bytes4).

### ERC-165 Interfaces

| Tag | Purpose | Example |
|-----|---------|---------|
| `@custom:interfaceid` | bytes4 interface ID | `0x01ffc9a7` |

```solidity
/// @title IERC165
/// @custom:interfaceid 0x01ffc9a7
interface IERC165 {
    function supportsInterface(bytes4 interfaceId) external view returns (bool);
}
```

## Computing Values with `cast`

Use Foundry's `cast` to compute selectors and hashes:

### Function Selector (bytes4)

```bash
cast sig "transfer(address,uint256)"
# Output: 0xa9059cbb
```

### Error Selector (bytes4)

```bash
cast sig "NotOwner(address)"
# Output: 0x30cd7471
```

### Event Topic0 (bytes32)

```bash
cast keccak "Transfer(address,address,uint256)"
# Output: 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
```

### Interface ID (bytes4)

For interface IDs, prefer computing in Solidity:

```solidity
bytes4 interfaceId = type(IMyInterface).interfaceId;
```

Or compute manually by XOR-ing all function selectors:

```bash
# Get each selector
cast sig "func1(uint256)"  # 0x12345678
cast sig "func2(address)"  # 0x87654321

# XOR them in Solidity or manually
bytes4 interfaceId = 0x12345678 ^ 0x87654321;
```

## Complete Documentation Example

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

// tag::IMyToken[]
/// @title IMyToken
/// @notice Interface for MyToken
/// @custom:interfaceid 0x36372b07
interface IMyToken {

    // tag::Transfer[]
    /// @notice Emitted when tokens are transferred
    /// @param from The sender address
    /// @param to The recipient address
    /// @param amount The amount transferred
    /// @custom:signature Transfer(address,address,uint256)
    /// @custom:topiczero 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
    event Transfer(address indexed from, address indexed to, uint256 amount);
    // end::Transfer[]

    // tag::InsufficientBalance[]
    /// @notice Thrown when transfer amount exceeds balance
    /// @param account The account with insufficient balance
    /// @param balance The current balance
    /// @param required The required amount
    /// @custom:signature InsufficientBalance(address,uint256,uint256)
    /// @custom:selector 0xcf479181
    error InsufficientBalance(address account, uint256 balance, uint256 required);
    // end::InsufficientBalance[]

    // tag::transfer[]
    /// @notice Transfers tokens to a recipient
    /// @param to_ The recipient address
    /// @param amount_ The amount to transfer
    /// @return success True if the transfer succeeded
    /// @custom:signature transfer(address,uint256)
    /// @custom:selector 0xa9059cbb
    function transfer(address to_, uint256 amount_) external returns (bool success);
    // end::transfer[]

    // tag::balanceOf[]
    /// @notice Returns the token balance of an account
    /// @param account_ The account to query
    /// @return balance The token balance
    /// @custom:signature balanceOf(address)
    /// @custom:selector 0x70a08231
    function balanceOf(address account_) external view returns (uint256 balance);
    // end::balanceOf[]
}
// end::IMyToken[]
```

## Validation Checklist

For each documented symbol, verify:

- [ ] Include-tags wrap the symbol correctly
- [ ] Tag names match symbol names
- [ ] `@custom:signature` matches actual signature exactly
- [ ] `@custom:selector` computed correctly (functions/errors)
- [ ] `@custom:topiczero` computed correctly (events)
- [ ] `@custom:interfaceid` computed correctly (interfaces)
- [ ] NatSpec params match function parameters

## Additional Resources

### Reference Files

- **`references/natspec-examples.md`** - More complete examples

### Quick Reference

| Symbol Type | Selector Tag | Hash Type |
|-------------|--------------|-----------|
| Function | `@custom:selector` | bytes4 |
| Error | `@custom:selector` | bytes4 |
| Event | `@custom:topiczero` | bytes32 |
| Interface | `@custom:interfaceid` | bytes4 (XOR of selectors) |
