---
name: aave-bsc
description: Interact with Aave V3 lending protocol on BNB Smart Chain (BSC).
metadata: { "cryptoclaw": { "emoji": "🏦" } }
---

# AAVE V3 BSC SKILL

This skill allows CryptoClaw to interact with the Aave V3 protocol on the BNB Smart Chain (BSC).

## Protocol Addresses (BSC)

- **Pool Proxy:** `0x6807dc923806fE8Fd134338EABCA509979a7e0cB`
- **Pool Addresses Provider:** `0xff75B6da14FfbbfD355Daf7a2731456b3562Ba6D`
- **Protocol Data Provider:** `0xc90Df74A7c16245c5F5C5870327Ceb38Fe5d5328`

## Common Functions

### getUserAccountData

Query the user's current account state (collateral, debt, health factor).

- **Contract:** Pool Proxy (`0x6807dc923806fE8Fd134338EABCA509979a7e0cB`)
- **ABI Snippet:** `[{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserAccountData","outputs":[{"internalType":"uint256","name":"totalCollateralBase","type":"uint256"},{"internalType":"uint256","name":"totalDebtBase","type":"uint256"},{"internalType":"uint256","name":"availableBorrowsBase","type":"uint256"},{"internalType":"uint256","name":"currentLiquidationThreshold","type":"uint256"},{"internalType":"uint256","name":"ltv","type":"uint256"},{"internalType":"uint256","name":"healthFactor","type":"uint256"}],"stateMutability":"view","type":"function"}]`

### supply

Supply an asset as collateral.

- **Contract:** Pool Proxy (`0x6807dc923806fE8Fd134338EABCA509979a7e0cB`)
- **ABI Snippet:** `[{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"onBehalfOf","type":"address"},{"internalType":"uint16","name":"referralCode","type":"uint16"}],"name":"supply","outputs":[],"stateMutability":"nonpayable","type":"function"}]`
- **Note:** Requires `approve` on the asset contract first.

### withdraw

Withdraw supplied collateral.

- **Contract:** Pool Proxy (`0x6807dc923806fE8Fd134338EABCA509979a7e0cB`)
- **ABI Snippet:** `[{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"to","type":"address"}],"name":"withdraw","outputs":[{"internalType":"uint256","name":"amountWithdrawn","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]`

### borrow

Borrow an asset against collateral.

- **Contract:** Pool Proxy (`0x6807dc923806fE8Fd134338EABCA509979a7e0cB`)
- **ABI Snippet:** `[{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"interestRateMode","type":"uint256"},{"internalType":"uint16","name":"referralCode","type":"uint16"},{"internalType":"address","name":"onBehalfOf","type":"address"}],"name":"borrow","outputs":[],"stateMutability":"nonpayable","type":"function"}]`
- **InterestRateMode:** 2 (Variable) is standard.

## Asset Addresses (BSC Underlying)

- **WBNB:** `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c`
- **USDT:** `0x55d398326f99059fF775485246999027B3197955`
- **USDC:** `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d`
- **BTCB:** `0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c`
- **ETH:** `0x2170Ed0880ac9A755fd29B2688956BD959F933F8`

## Usage Instructions

1. Check user account data before suggesting borrow/withdraw.
2. Always calculate gas estimates before write operations.
3. For supply, ensure token approval is granted.
