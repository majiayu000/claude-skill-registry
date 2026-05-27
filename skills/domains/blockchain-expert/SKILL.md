---
name: blockchain-expert
version: 1.0.0
description: Expert-level blockchain, Web3, smart contracts, DeFi, and cryptocurrency development
category: domains
tags: [blockchain, web3, smart-contracts, defi, ethereum, solidity]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Blockchain Expert

Expert guidance for blockchain development, smart contracts, Web3 applications, DeFi protocols, and cryptocurrency systems.

## Core Concepts

### Blockchain Fundamentals
- Distributed ledger technology
- Consensus mechanisms (PoW, PoS, PoA)
- Cryptographic hashing
- Public/private key cryptography
- Transaction validation
- Block structure and chain

### Smart Contracts
- Solidity programming
- Gas optimization
- Security patterns
- Upgradeable contracts
- Testing and auditing
- Contract interactions

### Web3 & DeFi
- Decentralized applications (dApps)
- DeFi protocols (AMM, lending, staking)
- NFTs and token standards
- Layer 2 solutions
- Cross-chain bridges
- Wallet integration

## Smart Contract Development

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SimpleToken is ERC20, Ownable, ReentrancyGuard {
    uint256 public constant MAX_SUPPLY = 1000000 * 10**18;

    mapping(address => bool) public minters;

    event MinterAdded(address indexed minter);
    event MinterRemoved(address indexed minter);

    modifier onlyMinter() {
        require(minters[msg.sender], "Not a minter");
        _;
    }

    constructor() ERC20("SimpleToken", "SMPL") {
        minters[msg.sender] = true;
    }

    function mint(address to, uint256 amount) external onlyMinter {
        require(totalSupply() + amount <= MAX_SUPPLY, "Max supply exceeded");
        _mint(to, amount);
    }

    function burn(uint256 amount) external {
        _burn(msg.sender, amount);
    }

    function addMinter(address minter) external onlyOwner {
        minters[minter] = true;
        emit MinterAdded(minter);
    }

    function removeMinter(address minter) external onlyOwner {
        minters[minter] = false;
        emit MinterRemoved(minter);
    }
}

// Staking Contract
contract StakingPool is ReentrancyGuard {
    IERC20 public stakingToken;
    IERC20 public rewardToken;

    uint256 public rewardRate = 100; // Reward tokens per second
    uint256 public lastUpdateTime;
    uint256 public rewardPerTokenStored;

    mapping(address => uint256) public userRewardPerTokenPaid;
    mapping(address => uint256) public rewards;
    mapping(address => uint256) public balances;

    uint256 private _totalSupply;

    constructor(address _stakingToken, address _rewardToken) {
        stakingToken = IERC20(_stakingToken);
        rewardToken = IERC20(_rewardToken);
    }

    function rewardPerToken() public view returns (uint256) {
        if (_totalSupply == 0) {
            return rewardPerTokenStored;
        }
        return rewardPerTokenStored +
               (((block.timestamp - lastUpdateTime) * rewardRate * 1e18) / _totalSupply);
    }

    function earned(address account) public view returns (uint256) {
        return ((balances[account] *
                (rewardPerToken() - userRewardPerTokenPaid[account])) / 1e18) +
               rewards[account];
    }

    modifier updateReward(address account) {
        rewardPerTokenStored = rewardPerToken();
        lastUpdateTime = block.timestamp;
        if (account != address(0)) {
            rewards[account] = earned(account);
            userRewardPerTokenPaid[account] = rewardPerTokenStored;
        }
        _;
    }

    function stake(uint256 amount) external nonReentrant updateReward(msg.sender) {
        require(amount > 0, "Cannot stake 0");
        _totalSupply += amount;
        balances[msg.sender] += amount;
        stakingToken.transferFrom(msg.sender, address(this), amount);
    }

    function withdraw(uint256 amount) external nonReentrant updateReward(msg.sender) {
        require(amount > 0, "Cannot withdraw 0");
        _totalSupply -= amount;
        balances[msg.sender] -= amount;
        stakingToken.transfer(msg.sender, amount);
    }

    function getReward() external nonReentrant updateReward(msg.sender) {
        uint256 reward = rewards[msg.sender];
        if (reward > 0) {
            rewards[msg.sender] = 0;
            rewardToken.transfer(msg.sender, reward);
        }
    }
}
```

## DeFi: AMM Implementation

```solidity
// Simple Automated Market Maker (like Uniswap)
contract SimpleAMM is ReentrancyGuard {
    IERC20 public token0;
    IERC20 public token1;

    uint256 public reserve0;
    uint256 public reserve1;

    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event Swap(address indexed user, address tokenIn, uint256 amountIn, uint256 amountOut);
    event AddLiquidity(address indexed user, uint256 amount0, uint256 amount1);
    event RemoveLiquidity(address indexed user, uint256 amount0, uint256 amount1);

    constructor(address _token0, address _token1) {
        token0 = IERC20(_token0);
        token1 = IERC20(_token1);
    }

    function addLiquidity(uint256 amount0, uint256 amount1)
        external
        nonReentrant
        returns (uint256 shares)
    {
        token0.transferFrom(msg.sender, address(this), amount0);
        token1.transferFrom(msg.sender, address(this), amount1);

        if (totalSupply == 0) {
            shares = sqrt(amount0 * amount1);
        } else {
            shares = min(
                (amount0 * totalSupply) / reserve0,
                (amount1 * totalSupply) / reserve1
            );
        }

        require(shares > 0, "Shares = 0");

        _mint(msg.sender, shares);
        _update(
            token0.balanceOf(address(this)),
            token1.balanceOf(address(this))
        );

        emit AddLiquidity(msg.sender, amount0, amount1);
    }

    function removeLiquidity(uint256 shares)
        external
        nonReentrant
        returns (uint256 amount0, uint256 amount1)
    {
        uint256 balance0 = token0.balanceOf(address(this));
        uint256 balance1 = token1.balanceOf(address(this));

        amount0 = (shares * balance0) / totalSupply;
        amount1 = (shares * balance1) / totalSupply;

        require(amount0 > 0 && amount1 > 0, "Amount = 0");

        _burn(msg.sender, shares);
        _update(balance0 - amount0, balance1 - amount1);

        token0.transfer(msg.sender, amount0);
        token1.transfer(msg.sender, amount1);

        emit RemoveLiquidity(msg.sender, amount0, amount1);
    }

    function swap(address tokenIn, uint256 amountIn)
        external
        nonReentrant
        returns (uint256 amountOut)
    {
        require(tokenIn == address(token0) || tokenIn == address(token1), "Invalid token");

        bool isToken0 = tokenIn == address(token0);

        (IERC20 tokenIn_, IERC20 tokenOut, uint256 reserveIn, uint256 reserveOut) =
            isToken0
                ? (token0, token1, reserve0, reserve1)
                : (token1, token0, reserve1, reserve0);

        tokenIn_.transferFrom(msg.sender, address(this), amountIn);

        // 0.3% fee
        uint256 amountInWithFee = (amountIn * 997) / 1000;

        // x * y = k formula
        amountOut = (reserveOut * amountInWithFee) / (reserveIn + amountInWithFee);

        tokenOut.transfer(msg.sender, amountOut);

        _update(
            token0.balanceOf(address(this)),
            token1.balanceOf(address(this))
        );

        emit Swap(msg.sender, tokenIn, amountIn, amountOut);
    }

    function _mint(address to, uint256 amount) private {
        balanceOf[to] += amount;
        totalSupply += amount;
    }

    function _burn(address from, uint256 amount) private {
        balanceOf[from] -= amount;
        totalSupply -= amount;
    }

    function _update(uint256 _reserve0, uint256 _reserve1) private {
        reserve0 = _reserve0;
        reserve1 = _reserve1;
    }

    function sqrt(uint256 y) private pure returns (uint256 z) {
        if (y > 3) {
            z = y;
            uint256 x = y / 2 + 1;
            while (x < z) {
                z = x;
                x = (y / x + x) / 2;
            }
        } else if (y != 0) {
            z = 1;
        }
    }

    function min(uint256 x, uint256 y) private pure returns (uint256) {
        return x <= y ? x : y;
    }
}
```

## Web3 Integration

```typescript
import { ethers } from 'ethers';
import { Contract, Provider, Signer } from 'ethers';

class Web3Client {
    private provider: Provider;
    private signer?: Signer;

    constructor(rpcUrl: string) {
        this.provider = new ethers.JsonRpcProvider(rpcUrl);
    }

    async connectWallet(): Promise<string> {
        // Connect to MetaMask
        if (typeof window.ethereum !== 'undefined') {
            const provider = new ethers.BrowserProvider(window.ethereum);
            await provider.send("eth_requestAccounts", []);
            this.signer = await provider.getSigner();
            return await this.signer.getAddress();
        }
        throw new Error('No wallet found');
    }

    async getBalance(address: string): Promise<string> {
        const balance = await this.provider.getBalance(address);
        return ethers.formatEther(balance);
    }

    async sendTransaction(to: string, amount: string): Promise<string> {
        if (!this.signer) throw new Error('Wallet not connected');

        const tx = await this.signer.sendTransaction({
            to,
            value: ethers.parseEther(amount)
        });

        const receipt = await tx.wait();
        return receipt?.hash || '';
    }

    getContract(address: string, abi: any[]): Contract {
        return new ethers.Contract(
            address,
            abi,
            this.signer || this.provider
        );
    }

    async callContract(
        contractAddress: string,
        abi: any[],
        method: string,
        args: any[]
    ): Promise<any> {
        const contract = this.getContract(contractAddress, abi);
        return await contract[method](...args);
    }

    async estimateGas(
        contractAddress: string,
        abi: any[],
        method: string,
        args: any[]
    ): Promise<bigint> {
        const contract = this.getContract(contractAddress, abi);
        return await contract[method].estimateGas(...args);
    }
}
```

## Best Practices

### Smart Contract Security
- Use OpenZeppelin contracts for standards
- Implement reentrancy guards
- Check for integer overflow/underflow (use Solidity 0.8+)
- Validate all inputs
- Use pull over push for payments
- Implement circuit breakers for emergencies
- Comprehensive testing and auditing

### Gas Optimization
- Use `uint256` over smaller types
- Pack storage variables
- Use `calldata` for function parameters
- Minimize storage operations
- Use events for data that doesn't need on-chain storage
- Batch operations when possible

### Development
- Use Hardhat/Foundry for development
- Write comprehensive tests
- Use test networks before mainnet
- Implement upgrade patterns carefully
- Monitor contract events
- Document all functions

## Anti-Patterns

❌ No reentrancy protection
❌ Unchecked external calls
❌ Using `tx.origin` for authorization
❌ Floating pragma versions
❌ No access control
❌ Storing sensitive data on-chain
❌ No gas limit considerations

## Resources

- Ethereum: https://ethereum.org/en/developers/
- Solidity: https://docs.soliditylang.org/
- OpenZeppelin: https://www.openzeppelin.com/
- Hardhat: https://hardhat.org/
- Ethers.js: https://docs.ethers.org/
