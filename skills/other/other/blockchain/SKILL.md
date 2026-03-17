---
description: "Blockchain and Web3 development with Solidity, Hardhat, Foundry, ethers.js, and smart contract security. Covers Ethereum, Layer 2 solutions, DeFi, NFTs, and decentralized storage. Activates for: blockchain, web3, solidity, smart contract, Ethereum, Hardhat, Foundry, ERC-20, ERC-721, NFT, DeFi, dapp, WalletConnect, IPFS, layer 2, gas optimization, reentrancy, OpenZeppelin."
model: opus
context: fork
---

# Blockchain & Web3 Development

Expert guidance for building production-grade decentralized applications, smart contracts, and Web3 integrations. This skill covers Ethereum ecosystem, alternative chains, security, and frontend integration.

## Ethereum Smart Contract Development

### Solidity Fundamentals

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// @title Secure Vault
/// @notice A vault for depositing and withdrawing ERC-20 tokens
/// @dev Implements reentrancy protection and ownership controls
contract SecureVault is Ownable, ReentrancyGuard {
    mapping(address => mapping(address => uint256)) private balances;
    mapping(address => bool) public allowedTokens;

    event Deposited(address indexed user, address indexed token, uint256 amount);
    event Withdrawn(address indexed user, address indexed token, uint256 amount);
    event TokenAllowed(address indexed token, bool allowed);

    error TokenNotAllowed(address token);
    error InsufficientBalance(uint256 requested, uint256 available);
    error ZeroAmount();

    constructor() Ownable(msg.sender) {}

    /// @notice Deposit tokens into the vault
    /// @param token The ERC-20 token address
    /// @param amount The amount to deposit
    function deposit(address token, uint256 amount) external nonReentrant {
        if (amount == 0) revert ZeroAmount();
        if (!allowedTokens[token]) revert TokenNotAllowed(token);

        // Effects before interactions (CEI pattern)
        balances[msg.sender][token] += amount;

        // Interaction
        bool success = IERC20(token).transferFrom(msg.sender, address(this), amount);
        require(success, "Transfer failed");

        emit Deposited(msg.sender, token, amount);
    }

    /// @notice Withdraw tokens from the vault
    /// @param token The ERC-20 token address
    /// @param amount The amount to withdraw
    function withdraw(address token, uint256 amount) external nonReentrant {
        if (amount == 0) revert ZeroAmount();
        uint256 balance = balances[msg.sender][token];
        if (amount > balance) revert InsufficientBalance(amount, balance);

        // Effects before interactions (CEI pattern)
        balances[msg.sender][token] = balance - amount;

        // Interaction
        bool success = IERC20(token).transfer(msg.sender, amount);
        require(success, "Transfer failed");

        emit Withdrawn(msg.sender, token, amount);
    }

    /// @notice Get balance for a user and token
    function getBalance(address user, address token) external view returns (uint256) {
        return balances[user][token];
    }

    /// @notice Allow or disallow a token for deposits
    function setAllowedToken(address token, bool allowed) external onlyOwner {
        allowedTokens[token] = allowed;
        emit TokenAllowed(token, allowed);
    }
}
```

### ERC Standards Reference

| Standard | Purpose | Key Functions |
|----------|---------|---------------|
| ERC-20 | Fungible tokens | `transfer`, `approve`, `transferFrom`, `balanceOf` |
| ERC-721 | NFTs (unique tokens) | `ownerOf`, `safeTransferFrom`, `tokenURI`, `approve` |
| ERC-1155 | Multi-token (fungible + NFT) | `balanceOf`, `safeTransferFrom`, `safeBatchTransferFrom` |
| ERC-2981 | NFT royalties | `royaltyInfo` |
| ERC-4626 | Tokenized vaults | `deposit`, `withdraw`, `convertToShares`, `convertToAssets` |
| ERC-6551 | Token-bound accounts | NFTs that own assets |

### ERC-721 NFT Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Royalty.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract MyNFT is ERC721, ERC721URIStorage, ERC721Royalty, Ownable {
    uint256 private _nextTokenId;
    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public mintPrice = 0.08 ether;
    string private _baseTokenURI;
    bool public mintingActive = false;

    error MintingNotActive();
    error MaxSupplyReached();
    error InsufficientPayment();
    error MaxPerWalletReached();

    mapping(address => uint256) public mintCount;
    uint256 public constant MAX_PER_WALLET = 5;

    constructor(
        string memory baseURI,
        address royaltyReceiver
    ) ERC721("MyNFT", "MNFT") Ownable(msg.sender) {
        _baseTokenURI = baseURI;
        // 5% royalty
        _setDefaultRoyalty(royaltyReceiver, 500);
    }

    function mint(uint256 quantity) external payable {
        if (!mintingActive) revert MintingNotActive();
        if (_nextTokenId + quantity > MAX_SUPPLY) revert MaxSupplyReached();
        if (msg.value < mintPrice * quantity) revert InsufficientPayment();
        if (mintCount[msg.sender] + quantity > MAX_PER_WALLET) revert MaxPerWalletReached();

        mintCount[msg.sender] += quantity;

        for (uint256 i = 0; i < quantity; i++) {
            uint256 tokenId = _nextTokenId++;
            _safeMint(msg.sender, tokenId);
        }
    }

    function tokenURI(uint256 tokenId)
        public view override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        _requireOwned(tokenId);
        return string(abi.encodePacked(_baseTokenURI, Strings.toString(tokenId), ".json"));
    }

    // Required overrides
    function supportsInterface(bytes4 interfaceId)
        public view override(ERC721, ERC721URIStorage, ERC721Royalty)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    function _update(address to, uint256 tokenId, address auth)
        internal override(ERC721)
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }
}
```

## Development Tools

### Hardhat Setup and Configuration

```typescript
// hardhat.config.ts
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import "@nomicfoundation/hardhat-verify";
import "hardhat-gas-reporter";
import "solidity-coverage";
import * as dotenv from "dotenv";

dotenv.config();

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: { enabled: true, runs: 200 },
      viaIR: true, // Enable IR-based compilation for better optimization
    },
  },
  networks: {
    hardhat: {
      forking: {
        url: process.env.MAINNET_RPC_URL ?? "",
        blockNumber: 19_000_000, // Pin block for deterministic tests
      },
    },
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL ?? "",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
    base: {
      url: "https://mainnet.base.org",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
  },
  etherscan: {
    apiKey: {
      mainnet: process.env.ETHERSCAN_API_KEY ?? "",
      sepolia: process.env.ETHERSCAN_API_KEY ?? "",
      base: process.env.BASESCAN_API_KEY ?? "",
    },
  },
  gasReporter: {
    enabled: process.env.REPORT_GAS === "true",
    currency: "USD",
    coinmarketcap: process.env.COINMARKETCAP_API_KEY,
  },
};

export default config;
```

### Hardhat Testing

```typescript
// test/SecureVault.test.ts
import { loadFixture } from "@nomicfoundation/hardhat-toolbox/network-helpers";
import { expect } from "chai";
import hre from "hardhat";

describe("SecureVault", function () {
  async function deployVaultFixture() {
    const [owner, user1, user2] = await hre.ethers.getSigners();

    // Deploy mock ERC-20 token
    const MockToken = await hre.ethers.getContractFactory("MockERC20");
    const token = await MockToken.deploy("Mock", "MCK", hre.ethers.parseEther("1000000"));

    // Deploy vault
    const Vault = await hre.ethers.getContractFactory("SecureVault");
    const vault = await Vault.deploy();

    // Allow the token
    await vault.setAllowedToken(await token.getAddress(), true);

    // Transfer tokens to user1
    await token.transfer(user1.address, hre.ethers.parseEther("1000"));

    return { vault, token, owner, user1, user2 };
  }

  describe("Deposits", function () {
    it("should accept deposits of allowed tokens", async function () {
      const { vault, token, user1 } = await loadFixture(deployVaultFixture);
      const amount = hre.ethers.parseEther("100");

      await token.connect(user1).approve(await vault.getAddress(), amount);
      await vault.connect(user1).deposit(await token.getAddress(), amount);

      expect(await vault.getBalance(user1.address, await token.getAddress()))
        .to.equal(amount);
    });

    it("should revert on zero amount", async function () {
      const { vault, token, user1 } = await loadFixture(deployVaultFixture);

      await expect(
        vault.connect(user1).deposit(await token.getAddress(), 0)
      ).to.be.revertedWithCustomError(vault, "ZeroAmount");
    });

    it("should revert on disallowed tokens", async function () {
      const { vault, user1 } = await loadFixture(deployVaultFixture);
      const fakeToken = "0x0000000000000000000000000000000000000001";

      await expect(
        vault.connect(user1).deposit(fakeToken, 100)
      ).to.be.revertedWithCustomError(vault, "TokenNotAllowed");
    });

    it("should emit Deposited event", async function () {
      const { vault, token, user1 } = await loadFixture(deployVaultFixture);
      const amount = hre.ethers.parseEther("50");

      await token.connect(user1).approve(await vault.getAddress(), amount);
      await expect(vault.connect(user1).deposit(await token.getAddress(), amount))
        .to.emit(vault, "Deposited")
        .withArgs(user1.address, await token.getAddress(), amount);
    });
  });

  describe("Withdrawals", function () {
    it("should allow withdrawal of deposited tokens", async function () {
      const { vault, token, user1 } = await loadFixture(deployVaultFixture);
      const amount = hre.ethers.parseEther("100");

      await token.connect(user1).approve(await vault.getAddress(), amount);
      await vault.connect(user1).deposit(await token.getAddress(), amount);
      await vault.connect(user1).withdraw(await token.getAddress(), amount);

      expect(await vault.getBalance(user1.address, await token.getAddress()))
        .to.equal(0);
    });

    it("should revert on insufficient balance", async function () {
      const { vault, token, user1 } = await loadFixture(deployVaultFixture);

      await expect(
        vault.connect(user1).withdraw(await token.getAddress(), 100)
      ).to.be.revertedWithCustomError(vault, "InsufficientBalance");
    });
  });
});
```

### Foundry (Forge) Testing

```solidity
// test/SecureVault.t.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "forge-std/Test.sol";
import "../src/SecureVault.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MockERC20 is ERC20 {
    constructor() ERC20("Mock", "MCK") {
        _mint(msg.sender, 1_000_000 ether);
    }
}

contract SecureVaultTest is Test {
    SecureVault vault;
    MockERC20 token;
    address user1 = makeAddr("user1");
    address user2 = makeAddr("user2");

    function setUp() public {
        vault = new SecureVault();
        token = new MockERC20();
        vault.setAllowedToken(address(token), true);

        // Fund user1
        token.transfer(user1, 1000 ether);
    }

    function test_deposit() public {
        vm.startPrank(user1);
        token.approve(address(vault), 100 ether);
        vault.deposit(address(token), 100 ether);
        vm.stopPrank();

        assertEq(vault.getBalance(user1, address(token)), 100 ether);
    }

    function test_revert_depositZeroAmount() public {
        vm.prank(user1);
        vm.expectRevert(SecureVault.ZeroAmount.selector);
        vault.deposit(address(token), 0);
    }

    function testFuzz_deposit(uint256 amount) public {
        amount = bound(amount, 1, 1000 ether);

        vm.startPrank(user1);
        token.approve(address(vault), amount);
        vault.deposit(address(token), amount);
        vm.stopPrank();

        assertEq(vault.getBalance(user1, address(token)), amount);
    }

    // Invariant: total vault balance >= sum of all user balances
    function invariant_solvency() public view {
        uint256 vaultBalance = token.balanceOf(address(vault));
        uint256 user1Balance = vault.getBalance(user1, address(token));
        uint256 user2Balance = vault.getBalance(user2, address(token));
        assertGe(vaultBalance, user1Balance + user2Balance);
    }
}
```

### Deployment Scripts

```typescript
// scripts/deploy.ts (Hardhat)
import hre from "hardhat";

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  // Deploy
  const Vault = await hre.ethers.getContractFactory("SecureVault");
  const vault = await Vault.deploy();
  await vault.waitForDeployment();

  const vaultAddress = await vault.getAddress();
  console.log("SecureVault deployed to:", vaultAddress);

  // Verify on Etherscan (wait for block confirmations first)
  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    console.log("Waiting for block confirmations...");
    await vault.deploymentTransaction()?.wait(5);

    await hre.run("verify:verify", {
      address: vaultAddress,
      constructorArguments: [],
    });
    console.log("Contract verified on Etherscan");
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

```bash
# Foundry deployment
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url $SEPOLIA_RPC_URL \
  --broadcast \
  --verify \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  -vvvv
```

## Smart Contract Security

### Common Vulnerabilities and Mitigations

| Vulnerability | Description | Mitigation |
|---------------|-------------|------------|
| Reentrancy | External call re-enters contract before state update | CEI pattern + `ReentrancyGuard` |
| Integer overflow | Arithmetic wraps around (pre-0.8) | Solidity 0.8+ has built-in checks |
| Front-running | Miners/validators reorder transactions | Commit-reveal schemes, flashbots |
| Access control | Missing authorization checks | OpenZeppelin `Ownable` or `AccessControl` |
| Oracle manipulation | Price oracle returns stale/manipulated data | Chainlink oracles, TWAP |
| Uninitialized proxy | Implementation not initialized after deploy | Use `initializer` modifier |
| Delegatecall injection | Malicious delegatecall target | Restrict delegatecall targets |
| Signature replay | Reusing signed messages across chains/contracts | Include chainId, nonce, contract address |

### Checks-Effects-Interactions (CEI) Pattern

```solidity
// ALWAYS follow this order:
function withdraw(uint256 amount) external {
    // 1. CHECKS - validate inputs and state
    require(balances[msg.sender] >= amount, "Insufficient balance");

    // 2. EFFECTS - update state BEFORE external calls
    balances[msg.sender] -= amount;

    // 3. INTERACTIONS - external calls LAST
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

### Audit Tools

```bash
# Slither - static analysis
pip install slither-analyzer
slither . --config-file slither.config.json

# Mythril - symbolic execution
pip install mythril
myth analyze contracts/SecureVault.sol --solv 0.8.24

# Foundry fuzzing and invariant testing
forge test --fuzz-runs 10000
forge test --match-test invariant
```

## Frontend Integration

### ethers.js v6

```typescript
import { ethers, BrowserProvider, Contract, formatEther, parseEther } from 'ethers';
import VaultABI from './abis/SecureVault.json';

const VAULT_ADDRESS = '0x...';

// Connect wallet
async function connectWallet(): Promise<BrowserProvider> {
  if (!window.ethereum) {
    throw new Error('No wallet detected. Install MetaMask.');
  }

  const provider = new BrowserProvider(window.ethereum);
  await provider.send('eth_requestAccounts', []);
  return provider;
}

// Read from contract (no wallet needed)
async function getBalance(userAddress: string, tokenAddress: string): Promise<string> {
  const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
  const vault = new Contract(VAULT_ADDRESS, VaultABI, provider);
  const balance = await vault.getBalance(userAddress, tokenAddress);
  return formatEther(balance);
}

// Write to contract (wallet required)
async function deposit(tokenAddress: string, amount: string): Promise<void> {
  const provider = await connectWallet();
  const signer = await provider.getSigner();

  // Approve token spending first
  const token = new Contract(tokenAddress, ERC20ABI, signer);
  const tx1 = await token.approve(VAULT_ADDRESS, parseEther(amount));
  await tx1.wait();

  // Deposit
  const vault = new Contract(VAULT_ADDRESS, VaultABI, signer);
  const tx2 = await vault.deposit(tokenAddress, parseEther(amount));
  const receipt = await tx2.wait();

  console.log('Deposited in block:', receipt?.blockNumber);
}

// Listen for events
async function watchDeposits(): Promise<void> {
  const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
  const vault = new Contract(VAULT_ADDRESS, VaultABI, provider);

  vault.on('Deposited', (user, token, amount) => {
    console.log(`${user} deposited ${formatEther(amount)} of ${token}`);
  });
}
```

### viem + wagmi (Modern Alternative)

```typescript
// wagmi config
import { createConfig, http } from 'wagmi';
import { mainnet, sepolia, base } from 'wagmi/chains';
import { injected, walletConnect } from 'wagmi/connectors';

export const config = createConfig({
  chains: [mainnet, sepolia, base],
  connectors: [
    injected(),
    walletConnect({ projectId: process.env.WC_PROJECT_ID! }),
  ],
  transports: {
    [mainnet.id]: http(),
    [sepolia.id]: http(),
    [base.id]: http(),
  },
});

// React hooks with wagmi
import { useAccount, useReadContract, useWriteContract, useWaitForTransactionReceipt } from 'wagmi';
import { parseEther } from 'viem';

function VaultDeposit() {
  const { address } = useAccount();

  const { data: balance } = useReadContract({
    address: VAULT_ADDRESS,
    abi: VaultABI,
    functionName: 'getBalance',
    args: [address!, TOKEN_ADDRESS],
    query: { enabled: !!address },
  });

  const { writeContract, data: hash } = useWriteContract();

  const { isLoading: isConfirming } = useWaitForTransactionReceipt({ hash });

  function handleDeposit() {
    writeContract({
      address: VAULT_ADDRESS,
      abi: VaultABI,
      functionName: 'deposit',
      args: [TOKEN_ADDRESS, parseEther('10')],
    });
  }

  return (
    <div>
      <p>Balance: {balance?.toString()}</p>
      <button onClick={handleDeposit} disabled={isConfirming}>
        {isConfirming ? 'Confirming...' : 'Deposit 10 tokens'}
      </button>
    </div>
  );
}
```

## Gas Optimization Strategies

### Storage Optimization

```solidity
// BAD: Each variable uses a full 32-byte slot
contract Unoptimized {
    uint256 a;    // slot 0
    bool b;       // slot 1 (wastes 31 bytes)
    uint256 c;    // slot 2
    bool d;       // slot 3 (wastes 31 bytes)
}

// GOOD: Pack variables into fewer slots
contract Optimized {
    uint256 a;    // slot 0
    uint256 c;    // slot 1
    bool b;       // slot 2 (packed with d)
    bool d;       // slot 2
}

// Use smaller types when possible
contract PackedStruct {
    struct UserData {
        uint128 balance;     // 16 bytes
        uint64 lastUpdate;   // 8 bytes
        uint32 nonce;        // 4 bytes
        bool active;         // 1 byte
        // Total: 29 bytes, fits in 1 slot
    }
}
```

### Code-Level Optimizations

```solidity
// Use custom errors instead of strings (saves ~50 gas per revert)
error InsufficientBalance(uint256 requested, uint256 available);

// Use unchecked for safe arithmetic (saves ~100 gas per operation)
function sum(uint256[] calldata values) external pure returns (uint256 total) {
    for (uint256 i = 0; i < values.length;) {
        total += values[i];
        unchecked { ++i; } // Safe: i < values.length prevents overflow
    }
}

// Use calldata instead of memory for read-only external function params
function process(bytes calldata data) external pure returns (bytes32) {
    return keccak256(data);
}

// Cache storage reads in memory
function withdrawAll(address[] storage users) internal {
    uint256 length = users.length; // Cache length (1 SLOAD vs N)
    for (uint256 i = 0; i < length;) {
        _withdraw(users[i]);
        unchecked { ++i; }
    }
}
```

## Layer 2 Solutions

| L2 | Type | Best For | Considerations |
|----|------|----------|----------------|
| Optimism (OP Stack) | Optimistic rollup | General dapps, DeFi | 7-day withdrawal, OP_STACK ecosystem |
| Arbitrum | Optimistic rollup | DeFi, complex contracts | 7-day withdrawal, Nitro engine |
| Base | Optimistic rollup (OP Stack) | Consumer apps | Coinbase ecosystem, low fees |
| zkSync Era | ZK rollup | Privacy, instant finality | zkEVM, different gas model |
| Polygon zkEVM | ZK rollup | EVM compatibility | Full EVM equivalence goal |
| Starknet | ZK rollup (STARK) | High-throughput | Cairo language, not EVM |

### Multi-Chain Deployment Pattern

```typescript
// deploy/deploy-multichain.ts
const CHAINS = {
  mainnet: { rpc: process.env.MAINNET_RPC, chainId: 1 },
  base: { rpc: 'https://mainnet.base.org', chainId: 8453 },
  arbitrum: { rpc: 'https://arb1.arbitrum.io/rpc', chainId: 42161 },
  optimism: { rpc: 'https://mainnet.optimism.io', chainId: 10 },
};

async function deployToChain(chainName: string, config: ChainConfig) {
  console.log(`\nDeploying to ${chainName}...`);
  const provider = new ethers.JsonRpcProvider(config.rpc);
  const deployer = new ethers.Wallet(process.env.PRIVATE_KEY!, provider);

  const factory = new ethers.ContractFactory(abi, bytecode, deployer);
  const contract = await factory.deploy();
  await contract.waitForDeployment();

  const address = await contract.getAddress();
  console.log(`${chainName}: ${address}`);

  // Save deployment address
  return { chain: chainName, chainId: config.chainId, address };
}
```

## DeFi Patterns

### Automated Market Maker (AMM) Core Concept

```solidity
// Simplified constant product AMM (x * y = k)
contract SimpleAMM {
    IERC20 public tokenA;
    IERC20 public tokenB;
    uint256 public reserveA;
    uint256 public reserveB;

    uint256 public constant FEE_NUMERATOR = 997;   // 0.3% fee
    uint256 public constant FEE_DENOMINATOR = 1000;

    /// @notice Swap tokenA for tokenB
    function swap(uint256 amountIn, uint256 minAmountOut) external returns (uint256 amountOut) {
        // Apply fee
        uint256 amountInWithFee = amountIn * FEE_NUMERATOR;

        // Constant product formula: (x + dx) * (y - dy) = x * y
        amountOut = (amountInWithFee * reserveB) /
                    (reserveA * FEE_DENOMINATOR + amountInWithFee);

        require(amountOut >= minAmountOut, "Slippage exceeded");

        // Update reserves
        reserveA += amountIn;
        reserveB -= amountOut;

        // Transfer tokens
        tokenA.transferFrom(msg.sender, address(this), amountIn);
        tokenB.transfer(msg.sender, amountOut);
    }
}
```

## NFT Metadata and Storage

### IPFS Metadata Pattern

```typescript
// Upload metadata to IPFS (using Pinata or nft.storage)
import { PinataSDK } from 'pinata';

const pinata = new PinataSDK({
  pinataJwt: process.env.PINATA_JWT!,
});

async function uploadMetadata(tokenId: number, imageFile: File): Promise<string> {
  // 1. Upload image
  const imageUpload = await pinata.upload.file(imageFile);
  const imageURI = `ipfs://${imageUpload.IpfsHash}`;

  // 2. Create and upload metadata JSON
  const metadata = {
    name: `My NFT #${tokenId}`,
    description: 'A unique digital collectible',
    image: imageURI,
    attributes: [
      { trait_type: 'Background', value: 'Blue' },
      { trait_type: 'Rarity', value: 'Rare' },
      { display_type: 'number', trait_type: 'Generation', value: 1 },
    ],
  };

  const metadataUpload = await pinata.upload.json(metadata);
  return `ipfs://${metadataUpload.IpfsHash}`;
}
```

## The Graph (Blockchain Indexing)

```graphql
# subgraph.yaml schema
type Deposit @entity {
  id: Bytes!
  user: Bytes!
  token: Bytes!
  amount: BigInt!
  blockNumber: BigInt!
  blockTimestamp: BigInt!
  transactionHash: Bytes!
}

type User @entity {
  id: Bytes!
  totalDeposited: BigInt!
  depositCount: BigInt!
  deposits: [Deposit!]! @derivedFrom(field: "user")
}
```

```typescript
// subgraph mapping handler
import { Deposited } from '../generated/SecureVault/SecureVault';
import { Deposit, User } from '../generated/schema';
import { BigInt, Bytes } from '@graphprotocol/graph-ts';

export function handleDeposited(event: Deposited): void {
  const deposit = new Deposit(event.transaction.hash.concatI32(event.logIndex.toI32()));
  deposit.user = event.params.user;
  deposit.token = event.params.token;
  deposit.amount = event.params.amount;
  deposit.blockNumber = event.block.number;
  deposit.blockTimestamp = event.block.timestamp;
  deposit.transactionHash = event.transaction.hash;
  deposit.save();

  // Update user aggregate
  let user = User.load(event.params.user);
  if (!user) {
    user = new User(event.params.user);
    user.totalDeposited = BigInt.zero();
    user.depositCount = BigInt.zero();
  }
  user.totalDeposited = user.totalDeposited.plus(event.params.amount);
  user.depositCount = user.depositCount.plus(BigInt.fromI32(1));
  user.save();
}
```

## Alternative Chains

### Solana (Anchor Framework)

```rust
// programs/vault/src/lib.rs
use anchor_lang::prelude::*;

declare_id!("VAULT_PROGRAM_ID");

#[program]
pub mod vault {
    use super::*;

    pub fn deposit(ctx: Context<Deposit>, amount: u64) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
        vault.balance += amount;

        // Transfer SOL
        anchor_lang::system_program::transfer(
            CpiContext::new(
                ctx.accounts.system_program.to_account_info(),
                anchor_lang::system_program::Transfer {
                    from: ctx.accounts.user.to_account_info(),
                    to: ctx.accounts.vault.to_account_info(),
                },
            ),
            amount,
        )?;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Deposit<'info> {
    #[account(mut)]
    pub user: Signer<'info>,
    #[account(mut)]
    pub vault: Account<'info, VaultState>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct VaultState {
    pub authority: Pubkey,
    pub balance: u64,
}
```

## Security Checklist for Smart Contracts

Before deploying any smart contract to mainnet:

- [ ] All functions have proper access control
- [ ] CEI pattern followed for all state-changing functions with external calls
- [ ] ReentrancyGuard on all payable/withdrawal functions
- [ ] Custom errors used instead of require strings
- [ ] Events emitted for all state changes
- [ ] Input validation on all external/public functions
- [ ] Integer arithmetic checked (Solidity 0.8+ or SafeMath)
- [ ] No hardcoded addresses (use constructor parameters or admin setters)
- [ ] Upgradeable proxy properly initialized (if applicable)
- [ ] Slither static analysis passes with no high/medium findings
- [ ] Fuzz testing with 10,000+ runs on critical functions
- [ ] Invariant tests for protocol-level properties
- [ ] Multi-sig or timelock on admin functions for mainnet
- [ ] Emergency pause mechanism implemented
- [ ] Test coverage above 95% on all critical paths
- [ ] Independent audit completed (for contracts holding significant value)
