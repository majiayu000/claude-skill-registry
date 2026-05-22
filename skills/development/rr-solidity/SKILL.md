---
name: rr-solidity
description: Comprehensive Solidity smart contract development skill using Foundry framework. Use for writing, testing, deploying, and auditing Solidity contracts with security-first practices. Also triggers when working with .sol files, Foundry project files (foundry.toml), test files (.t.sol), or smart contract deployment scripts. Example triggers: "Write smart contract", "Create Solidity test", "Deploy contract", "Audit smart contract", "Fix security vulnerability", "Write Foundry test", "Set up Foundry project"
---

# Solidity Development with Foundry

## Overview

Comprehensive skill for professional Solidity smart contract development using the Foundry framework. Provides security-first development practices, testing patterns, static analysis integration (Slither, solhint), and deployment workflows for EVM-compatible blockchains.

## When to Use This Skill

Automatically activate when:
- Working with `.sol` (Solidity) files
- User mentions smart contracts, blockchain, Web3, DeFi, or Ethereum
- Foundry project detected (`foundry.toml` present)
- User requests contract deployment, testing, or security auditing
- Working with forge, cast, or anvil commands
- Implementing ERC standards (ERC20, ERC721, ERC1155, etc.)


## Development Workflow

### 1. Write Secure Contracts

Follow security-first patterns from `references/solidity-security.md`:

**Always implement:**
- Checks-Effects-Interactions (CEI) pattern
- Access control (Ownable, AccessControl)
- Input validation
- Emergency pause mechanisms
- Pull over push for payments
- Custom errors for gas efficiency

**Example contract structure:**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {Pausable} from "@openzeppelin/contracts/security/Pausable.sol";

contract MyContract is Ownable, Pausable {
    /*//////////////////////////////////////////////////////////////
                                 ERRORS
    //////////////////////////////////////////////////////////////*/

    error InvalidInput();
    error InsufficientBalance();

    /*//////////////////////////////////////////////////////////////
                                 EVENTS
    //////////////////////////////////////////////////////////////*/

    event ActionCompleted(address indexed user, uint256 amount);

    /*//////////////////////////////////////////////////////////////
                            STATE VARIABLES
    //////////////////////////////////////////////////////////////*/

    mapping(address => uint256) public balances;

    /*//////////////////////////////////////////////////////////////
                              CONSTRUCTOR
    //////////////////////////////////////////////////////////////*/

    constructor() Ownable(msg.sender) {}

    /*//////////////////////////////////////////////////////////////
                           EXTERNAL FUNCTIONS
    //////////////////////////////////////////////////////////////*/

    function deposit() external payable whenNotPaused {
        if (msg.value == 0) revert InvalidInput();
        balances[msg.sender] += msg.value;
        emit ActionCompleted(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external whenNotPaused {
        // CEI Pattern: Checks
        if (amount == 0) revert InvalidInput();
        if (balances[msg.sender] < amount) revert InsufficientBalance();

        // Effects
        balances[msg.sender] -= amount;

        // Interactions
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        emit ActionCompleted(msg.sender, amount);
    }
}
```

### 2. Write Comprehensive Tests

Follow testing patterns from `references/foundry-testing.md`:

**Test structure:**

```solidity
import {Test, console} from "forge-std/Test.sol";
import {MyContract} from "../src/MyContract.sol";

contract MyContractTest is Test {
    MyContract public myContract;

    address constant OWNER = address(1);
    address constant USER = address(2);

    function setUp() public {
        vm.prank(OWNER);
        myContract = new MyContract();
    }

    // Unit tests
    function test_Deposit() public { }

    // Edge cases
    function test_RevertWhen_ZeroDeposit() public { }

    // Fuzz tests
    function testFuzz_Deposit(uint256 amount) public { }

    // Invariant tests
    function invariant_TotalBalanceMatchesContract() public { }
}
```

**Run tests:**

```bash
forge test              # Run all tests
forge test -vvv         # Verbose output
forge test --gas-report # Include gas costs
forge coverage          # Coverage report
```

### 3. Security Analysis

**Run comprehensive security checks:**

```bash
# Static analysis with Slither
slither . --exclude-optimization --exclude-informational

# Linting with solhint
solhint 'src/**/*.sol' 'test/**/*.sol'

# Or use the automated script
bash scripts/check_security.sh
```

**Pre-deployment checklist** (from `references/solidity-security.md`):
- [ ] Reentrancy protection implemented
- [ ] Access controls on privileged functions
- [ ] Input validation on all external functions
- [ ] Emergency pause mechanism
- [ ] External calls follow CEI pattern
- [ ] Events emitted for state changes
- [ ] Gas optimizations applied
- [ ] Test coverage >90%
- [ ] Slither analysis passed
- [ ] solhint checks passed
- [ ] Professional audit for mainnet

### 4. Build and Deploy

**Build contracts:**

```bash
forge build --optimize --optimizer-runs 200
```

**Deploy using script:**

```solidity
// script/Deploy.s.sol
import {Script} from "forge-std/Script.sol";
import {MyContract} from "../src/MyContract.sol";

contract DeployScript is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        MyContract myContract = new MyContract();
        console.log("Deployed at:", address(myContract));

        vm.stopBroadcast();
    }
}
```

**Execute deployment:**

```bash
# Load environment variables
source .env

# Simulate deployment
forge script script/Deploy.s.sol --rpc-url $SEPOLIA_RPC_URL

# Deploy to testnet
forge script script/Deploy.s.sol \
    --rpc-url $SEPOLIA_RPC_URL \
    --broadcast \
    --verify

# Deploy to mainnet (after audits!)
forge script script/Deploy.s.sol \
    --rpc-url $MAINNET_RPC_URL \
    --broadcast \
    --verify
```

## Advanced Testing Patterns

### Mainnet Forking

Test against real deployed contracts:

```solidity
contract ForkTest is Test {
    IERC20 constant USDC = IERC20(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);

    function setUp() public {
        vm.createSelectFork("mainnet", 18_000_000);
    }

    function test_InteractWithRealProtocol() public {
        // Test with actual mainnet state
    }
}
```

```bash
forge test --fork-url $MAINNET_RPC_URL
```

### Invariant Testing

Test properties that must always hold:

```solidity
function invariant_SumOfBalancesEqualsTotalSupply() public {
    assertEq(token.totalSupply(), handler.sumOfBalances());
}
```

### Fuzz Testing

Test with randomized inputs:

```solidity
function testFuzz_Transfer(address to, uint256 amount) public {
    vm.assume(to != address(0));
    amount = bound(amount, 1, 1000 ether);
    // Test with random inputs
}
```

## Gas Optimization

Key strategies from `references/solidity-security.md`:

1. **Storage packing** - Group uint8/uint16/etc in single slots
2. **uint256 for counters** - Native EVM word size
3. **calldata over memory** - For function parameters
4. **Events over storage** - Log data instead of storing
5. **Custom errors** - More gas-efficient than strings
6. **Immutable/constant** - For unchanging values

## Contract Verification

```bash
# Verify on Etherscan
forge verify-contract $CONTRACT_ADDRESS \
    src/MyContract.sol:MyContract \
    --chain-id 1 \
    --etherscan-api-key $ETHERSCAN_KEY

# With constructor args
forge verify-contract $CONTRACT_ADDRESS \
    src/MyContract.sol:MyContract \
    --chain-id 1 \
    --etherscan-api-key $ETHERSCAN_KEY \
    --constructor-args $(cast abi-encode "constructor(uint256)" 100)
```

## Common Commands Reference

Quick reference from `references/foundry-commands.md`:

**Development:**
```bash
forge build                    # Compile contracts
forge test                     # Run tests
forge test -vvv                # Verbose test output
forge coverage                 # Coverage report
forge fmt                      # Format code
forge clean                    # Clean artifacts
```

**Testing:**
```bash
forge test --match-test test_Transfer    # Run specific test
forge test --match-contract MyTest       # Run specific contract
forge test --gas-report                  # Show gas usage
forge test --fork-url $RPC_URL          # Fork testing
forge snapshot                           # Gas snapshot
```

**Deployment:**
```bash
forge script script/Deploy.s.sol --broadcast
forge create src/MyContract.sol:MyContract --rpc-url $RPC_URL
forge verify-contract $ADDRESS src/MyContract.sol:MyContract
```

**Debugging:**
```bash
forge test --debug test_MyTest           # Interactive debugger
cast run $TX_HASH --debug                # Debug transaction
cast run $TX_HASH --trace                # Trace transaction
```

**Local node:**
```bash
anvil                                    # Start local node
anvil --fork-url $MAINNET_RPC_URL       # Fork mainnet locally
```

## Security Tools Integration

### Slither

Static analyzer with 99+ vulnerability detectors:

```bash
slither .                                # Full analysis
slither . --exclude-optimization         # Skip optimizations
slither . --exclude-informational        # Critical issues only
slither . --checklist                    # Generate checklist
```

### solhint

Linter configured via `assets/solhint.config.json`:

```bash
solhint 'src/**/*.sol'                   # Lint source
solhint 'test/**/*.sol'                  # Lint tests
solhint --fix 'src/**/*.sol'             # Auto-fix issues
```

## Resources


### references/
- `solidity-security.md` - Comprehensive security patterns, vulnerabilities, and mitigation strategies
- `foundry-testing.md` - Testing patterns including fuzzing, invariants, fork testing, and mocking
- `foundry-commands.md` - Complete command reference for forge, cast, and anvil

## Best Practices Summary

1. **Security First**: Always implement CEI pattern, access controls, and input validation
2. **Test Coverage**: Aim for >90% coverage with unit, fuzz, and invariant tests
3. **Static Analysis**: Run Slither and solhint before every deployment
4. **Gas Optimization**: Apply after security, never at the expense of safety
5. **Documentation**: Use NatSpec comments for all public/external functions
6. **Audit**: Professional audit required for mainnet deployment
7. **Verification**: Verify all contracts on Etherscan post-deployment
8. **Emergency**: Include pause mechanisms for critical contracts

## Common Patterns to Reference

When implementing specific functionality, reference these sections:

- **ERC20 tokens** - Use OpenZeppelin's implementation
- **Access control** - `references/solidity-security.md` (AccessControl, Ownable)
- **Upgradeable contracts** - OpenZeppelin's proxy patterns
- **Reentrancy protection** - `references/solidity-security.md` (CEI pattern)
- **Testing external protocols** - `references/foundry-testing.md` (fork testing)
- **Gas optimization** - `references/solidity-security.md` (optimization strategies)
- **Randomness** - Use Chainlink VRF, never block.timestamp alone
- **Oracles** - Use Chainlink price feeds for production

## Workflow Example

Complete workflow for adding a new feature:

1. **Write contract** following security patterns
2. **Write tests** with >90% coverage
3. **Run tests**: `forge test -vvv`
4. **Check coverage**: `forge coverage`
5. **Run Slither**: `slither .`
6. **Run solhint**: `solhint 'src/**/*.sol'`
7. **Format code**: `forge fmt`
8. **Build**: `forge build`
9. **Deploy to testnet**: `forge script script/Deploy.s.sol --broadcast`
10. **Verify**: `forge verify-contract ...`
11. **Get audit** (for mainnet)
12. **Deploy to mainnet** after audit approval
