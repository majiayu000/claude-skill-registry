---
name: erc4337-privacy-wallet
description: Privacy-preserving ERC-4337 wallet development for vehicle identity and sensitive data protection. Use when implementing ERC-4337 account abstraction wallets that handle sensitive information (vehicle license plates, biometric data, personal IDs) requiring on-chain privacy. Triggers on requests like "implement ERC-4337 wallet for vehicle", "create privacy-protected account abstraction", "build wallet with vehicle number privacy", "develop ERC-4337 with ZK proof integration", or any smart contract wallet development requiring commitment schemes, deterministic address generation, and sensitive data protection.
---

# ERC-4337 Privacy-Protected Wallet

## Overview

This skill provides comprehensive support for developing ERC-4337 compliant Account Abstraction wallets with privacy-preserving features, specifically designed for vehicle identity and other sensitive data use cases. It combines smart contract templates, testing frameworks, privacy validation tools, and security best practices to enable the secure implementation of wallets that protect user privacy while maintaining on-chain functionality.

**Key Capabilities:**
- Privacy-protected smart contract templates (PrivacyProtectedAccount, AccountFactory, VehicleRegistry)
- Commitment scheme implementation for sensitive data (vehicle plates, personal info)
- Deterministic address generation using CREATE2
- Comprehensive test suites with privacy verification
- Automated privacy validation tooling
- Security and compliance checklists

## When to Use This Skill

Invoke this skill when you encounter requests involving:

- **Vehicle Identity Wallets**: "Create a wallet from vehicle license plate information"
- **ERC-4337 Implementation**: "Implement account abstraction for privacy-protected accounts"
- **Sensitive Data Protection**: "Build wallet that hides user's personal identification"
- **Deterministic Address Generation**: "Generate predictable wallet addresses from private data"
- **ZK Proof Integration**: "Add zero-knowledge proof verification to ERC-4337 wallet"
- **Privacy Auditing**: "Validate that my smart contract doesn't leak sensitive information"

## Quick Start Guide

### 1. Understand the Requirements

Ask the user these key questions:
- What sensitive data needs protection? (vehicle plate, biometric, etc.)
- Is deterministic address generation required?
- Are ZK proofs needed, or is commitment hashing sufficient?
- What is the target blockchain/testnet?

### 2. Set Up the Project

```bash
# Copy contract templates
cp -r assets/contracts/* ./contracts/

# Install dependencies
cd contracts
npm install

# Compile contracts
npm run compile
```

### 3. Customize for Your Use Case

**For vehicle-based wallets:**
```solidity
// Off-chain: Compute vehicle commitment
const plateNumber = "ABC-1234";
const userSalt = ethers.id("user-secret-entropy");
const commitment = ethers.keccak256(
    ethers.solidityPacked(["string", "bytes32"], [plateNumber, userSalt])
);

// Deploy account with commitment
const account = await factory.createAccount(
    ownerAddress,
    commitment,
    12345  // deployment salt
);
```

**For biometric/other sensitive data:**
```solidity
// Replace plateNumber with your sensitive data
const biometricHash = computeHash(biometricData);
const commitment = ethers.keccak256(
    ethers.solidityPacked(["bytes32", "bytes32"], [biometricHash, userSalt])
);
```

### 4. Run Privacy Validation

```bash
# Validate that contracts don't leak sensitive data
python scripts/validate_privacy.py contracts/PrivacyProtectedAccount.sol
```

### 5. Run Tests

```bash
# Run comprehensive test suite
npm test

# Run specific test file
npx hardhat test tests/PrivacyProtectedAccount.test.ts
```

## Core Components

### 1. PrivacyProtectedAccount

The main account contract that implements ERC-4337's `IAccount` interface with privacy features.

**Key Features:**
- Stores only commitment (hash) of sensitive data, never raw values
- Deterministic address generation via CREATE2
- ERC-4337 compliant UserOperation validation
- Owner-based access control
- Batch transaction execution

**Usage:**
```solidity
// Deploy via factory
const account = await factory.createAccount(owner, vehicleCommitment, salt);

// Verify ownership without revealing data
const isValid = await account.verifyVehicleOwnership(plateNumber, userSalt);

// Execute transaction
await account.execute(targetAddress, value, calldata);
```

**Privacy Guarantee:**
- Vehicle commitment is stored as `bytes32` hash
- Raw plate number never touches blockchain
- Verification is view-only (off-chain safe)

### 2. AccountFactory

Factory contract for deploying PrivacyProtectedAccount instances with deterministic addresses.

**Key Features:**
- CREATE2-based deterministic deployment
- Counterfactual address computation
- Batch account creation
- Cross-chain address consistency

**Usage:**
```solidity
// Compute address before deployment
const predictedAddress = await factory.getAddress(owner, commitment, salt);

// Deploy account
const account = await factory.createAccount(owner, commitment, salt);

// Address matches prediction
assert(accountAddress === predictedAddress);
```

**Use Cases:**
- Receive funds before account creation
- Consistent addresses across multiple chains
- Privacy-preserving wallet generation

### 3. VehicleRegistry

Optional registry contract for managing vehicle-to-wallet mappings with privacy.

**Key Features:**
- Maps commitments to wallet addresses
- Authorized verifier system
- Selective disclosure support
- Batch registration

**Usage:**
```solidity
// Register vehicle with commitment only
await registry.registerVehicle(commitment, walletAddress, metadataHash);

// Verify registration (authorized only)
const isRegistered = await registry.verifyVehicleRegistration(commitment);

// Update commitment (ownership transfer)
await registry.updateVehicleCommitment(oldCommitment, newCommitment);
```

## Implementation Workflow

### Step 1: Define Privacy Model

Determine what needs privacy protection:

**Example - Vehicle Wallet:**
```
Sensitive: License plate number
Public: Wallet address, transaction history
Commitment: keccak256(plateNumber + salt)
```

**Example - Biometric Wallet:**
```
Sensitive: Fingerprint hash
Public: Wallet address
Commitment: keccak256(fingerprintHash + salt)
```

### Step 2: Generate Commitment Off-Chain

**CRITICAL: Never pass raw sensitive data to blockchain functions.**

```javascript
// Frontend/Backend - OFF-CHAIN computation
import { ethers } from 'ethers';

function generateCommitment(sensitiveData, userSecret) {
    // Generate cryptographically secure salt
    const salt = ethers.keccak256(
        ethers.solidityPacked(
            ['string', 'uint256', 'address'],
            [userSecret, Date.now(), userAddress]
        )
    );

    // Compute commitment
    const commitment = ethers.keccak256(
        ethers.solidityPacked(['string', 'bytes32'], [sensitiveData, salt])
    );

    return { commitment, salt };
}

// Usage
const { commitment, salt } = generateCommitment(licensePlate, userSecret);
// Store salt securely off-chain!
// Send only commitment to blockchain
```

### Step 3: Deploy Account

```javascript
// Connect to factory
const factory = await ethers.getContractAt('AccountFactory', factoryAddress);

// Optional: Predict address first
const predictedAddress = await factory.getAddress(
    ownerAddress,
    commitment,
    deploymentSalt
);
console.log('Account will be deployed at:', predictedAddress);

// Deploy account
const tx = await factory.createAccount(ownerAddress, commitment, deploymentSalt);
await tx.wait();

console.log('Account deployed at:', predictedAddress);
```

### Step 4: Create and Submit UserOperation

```javascript
import { ethers } from 'ethers';

// Build UserOperation
const userOp = {
    sender: accountAddress,
    nonce: await account.getNonce(),
    initCode: '0x',  // Empty if account exists
    callData: account.interface.encodeFunctionData('execute', [
        targetAddress,
        value,
        data
    ]),
    accountGasLimits: ethers.solidityPacked(
        ['uint128', 'uint128'],
        [verificationGasLimit, callGasLimit]
    ),
    preVerificationGas,
    gasFees: ethers.solidityPacked(
        ['uint128', 'uint128'],
        [maxPriorityFeePerGas, maxFeePerGas]
    ),
    paymasterAndData: '0x',  // Or paymaster address + data
    signature: '0x'  // Will be filled after signing
};

// Sign UserOperation
const userOpHash = await account.getUserOpHash(userOp);
const signature = await owner.signMessage(ethers.getBytes(userOpHash));
userOp.signature = signature;

// Submit to bundler
await bundler.sendUserOperation(userOp);
```

### Step 5: Verify Privacy Protection

```bash
# Run automated privacy validation
python scripts/validate_privacy.py contracts/YourContract.sol

# Expected output:
# ✅ PRIVACY VALIDATION PASSED
# No privacy violations detected.
```

## Privacy Patterns

### Pattern 1: Basic Commitment

```solidity
// Off-chain
const commitment = keccak256(abi.encodePacked(sensitiveData, salt));

// On-chain
bytes32 public dataCommitment;

function initialize(bytes32 _commitment) external {
    dataCommitment = _commitment;
}

function verify(string memory data, bytes32 salt) external view returns (bool) {
    return keccak256(abi.encodePacked(data, salt)) == dataCommitment;
}
```

### Pattern 2: Multi-Attribute Commitment

```solidity
// For vehicles with multiple attributes
struct VehicleData {
    string plateNumber;
    string model;
    uint256 year;
}

// Off-chain
const commitment = keccak256(abi.encode(
    vehicleData.plateNumber,
    vehicleData.model,
    vehicleData.year,
    salt
));
```

### Pattern 3: ZK Proof Integration

For advanced privacy (see `references/privacy-patterns.md` for full examples):

```solidity
// Verify ZK proof instead of revealing data
function _validateSignature(
    PackedUserOperation calldata userOp,
    bytes32 userOpHash
) internal override returns (uint256) {
    (bytes memory proof, bytes memory publicInputs) =
        abi.decode(userOp.signature, (bytes, bytes));

    require(zkVerifier.verify(proof, publicInputs), "Invalid proof");
    return SIG_VALIDATION_SUCCESS;
}
```

## Testing Strategy

### Privacy Tests

```typescript
describe("Privacy Protection", () => {
    it("should not store raw sensitive data", async () => {
        // Verify storage doesn't contain plate number
        for (let i = 0; i < 20; i++) {
            const storage = await ethers.provider.getStorage(account.address, i);
            expect(storage).to.not.include(ethers.hexlify(ethers.toUtf8Bytes(plateNumber)));
        }
    });

    it("should verify with correct preimage", async () => {
        const isValid = await account.verifyVehicleOwnership(plateNumber, salt);
        expect(isValid).to.be.true;
    });

    it("should reject wrong preimage", async () => {
        const isValid = await account.verifyVehicleOwnership("WRONG-PLATE", salt);
        expect(isValid).to.be.false;
    });
});
```

### ERC-4337 Tests

```typescript
describe("UserOperation Validation", () => {
    it("should validate correct signature", async () => {
        const userOp = buildUserOp({ sender: account.address });
        const userOpHash = await entryPoint.getUserOpHash(userOp);
        userOp.signature = await owner.signMessage(ethers.getBytes(userOpHash));

        await expect(entryPoint.handleOps([userOp], bundler.address))
            .to.not.be.reverted;
    });
});
```

## Security Checklist

Before deploying to mainnet, verify:

- [ ] Run privacy validation: `python scripts/validate_privacy.py`
- [ ] All tests passing: `npm test`
- [ ] No raw sensitive data in storage or events
- [ ] Commitment generation uses strong salt (≥256 bits entropy)
- [ ] Verification functions are `view` or `pure`
- [ ] Access control properly implemented
- [ ] EntryPoint address is correct
- [ ] Contracts verified on Etherscan
- [ ] Professional security audit completed

See `references/security-checklist.md` for complete checklist.

## Common Pitfalls

### ❌ Storing Raw Sensitive Data

```solidity
// NEVER DO THIS
contract BadExample {
    string public licensePlate;  // Publicly visible!
}
```

### ✅ Correct Approach

```solidity
// DO THIS
contract GoodExample {
    bytes32 public vehicleCommitment;  // Only hash stored
}
```

### ❌ Weak Salt Generation

```solidity
// WEAK - predictable
bytes32 salt = bytes32(block.timestamp);
```

### ✅ Strong Salt

```solidity
// STRONG - unique per user with high entropy
bytes32 salt = keccak256(abi.encodePacked(
    userSecret,
    block.timestamp,
    block.prevrandao,
    msg.sender
));
```

### ❌ Exposing Data in Events

```solidity
// NEVER DO THIS
event VehicleRegistered(string plateNumber);
```

### ✅ Events with Commitments

```solidity
// DO THIS
event VehicleRegistered(bytes32 indexed commitment);
```

## Advanced Topics

### ZK-SNARK Integration

For zero-knowledge proof integration, see `references/privacy-patterns.md` section on ZK proofs.

**High-level flow:**
1. Generate ZK circuit for vehicle ownership
2. Prove knowledge of plate number without revealing it
3. Verify proof on-chain in `_validateSignature()`

### Cross-Chain Deployment

```bash
# Deploy to multiple networks with same addresses
npx hardhat run scripts/deploy.ts --network sepolia
npx hardhat run scripts/deploy.ts --network polygonAmoy

# Addresses match due to CREATE2 determinism
```

### Gasless Transactions with Paymaster

```javascript
// Add paymaster to UserOperation
userOp.paymasterAndData = ethers.solidityPacked(
    ['address', 'bytes'],
    [paymasterAddress, paymasterData]
);

// User doesn't pay gas - paymaster sponsors it
```

## Resources

### Bundled Resources

- **`assets/contracts/`**: Production-ready contract templates
  - `PrivacyProtectedAccount.sol` - Main account contract
  - `AccountFactory.sol` - Deterministic factory
  - `VehicleRegistry.sol` - Optional registry
  - `package.json`, `hardhat.config.ts` - Project setup

- **`assets/tests/`**: Comprehensive test suites
  - Privacy protection tests
  - ERC-4337 compliance tests
  - Gas optimization tests

- **`scripts/validate_privacy.py`**: Automated privacy validation tool
  - Scans for sensitive data leaks
  - Validates commitment patterns
  - Checks event safety

- **`references/`**: In-depth documentation
  - `erc4337-architecture.md` - ERC-4337 deep dive
  - `privacy-patterns.md` - Privacy implementation patterns
  - `security-checklist.md` - Comprehensive security guide

### External Resources

- [ERC-4337 Specification](https://eips.ethereum.org/EIPS/eip-4337)
- [Account Abstraction Docs](https://docs.erc4337.io/)
- [MynaWallet Reference](https://github.com/MynaWallet/monorepo)
- [Toyota MON](https://www.toyota-blockchain-lab.org/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)

## Support and Troubleshooting

### Common Issues

**Issue: Gas estimation fails**
```
Solution: Ensure account has sufficient deposit in EntryPoint
await account.addDeposit({ value: ethers.parseEther("0.1") });
```

**Issue: Signature validation fails**
```
Solution: Check that userOpHash is computed correctly
const userOpHash = await entryPoint.getUserOpHash(userOp);
```

**Issue: Privacy validation fails**
```
Solution: Review reported violations and fix
- Remove string storage for sensitive data
- Make verification functions view/pure
- Use commitments instead of raw data
```

### Getting Help

1. Check `references/` for detailed documentation
2. Review test files for usage examples
3. Run privacy validation for security issues
4. Consult ERC-4337 documentation for protocol questions

## 参考文献
- [ETHGlobalTokyo上位チーム勝手に解説 Myna](https://zenn.dev/kozayupapa/scraps/782815787c5c33)
- [a42inc/ETHGlobalTokyo2023](https://github.com/a42inc/ETHGlobalTokyo2023)
- [マイナンバーカードの公開鍵からSmartAccountのアドレスを一意に導出する方法 Study](https://zenn.dev/kozayupapa/articles/b0025b213ed39f)
- [マイナンバーカードで署名をするところを動かしてみよう:ERC-4337 (AccountAbstraction)](https://zenn.dev/kozayupapa/articles/3347b360712b12)
- [MynaWallet/monorepo](https://github.com/MynaWallet/monorepo)
- [【Account Abstraction】UserOperation周りの具体的な実装について](https://zenn.dev/pokena/articles/84e243cf91a2cf)
- [マイナウォレットメモ](https://zenn.dev/pokena/scraps/c8d8189a1c6cb9)
