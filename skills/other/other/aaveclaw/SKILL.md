---
name: aaveclaw
description: Aave V3 lending protocol on Base Sepolia testnet. Deposit WETH collateral, borrow USDC, repay loans, withdraw collateral, check health factor, and mint test tokens via faucet. Use when users want to interact with Aave lending, check their lending position health, or get testnet tokens.
---

# aaveclaw - Aave V3 Lending on Base Sepolia

Interact with Aave V3 lending protocol on Base Sepolia testnet. Manages the full lending lifecycle using the wallet from `~/.x402-config.json`.

## Setup

Run `setup.sh` on first use to install dependencies (ethers v6):

```
bash scripts/setup.sh
```

## Commands

### Check Health Factor

Check the current lending position. Safe to run anytime, read-only.

```
bash scripts/health.sh [address]
```

If no address is provided, uses the configured wallet address.

### Mint Test Tokens (Faucet)

Get testnet WETH or USDC from the Aave faucet. Run this first if the wallet has no tokens.

```
bash scripts/faucet.sh weth 1       # Mint 1 WETH
bash scripts/faucet.sh usdc 1000    # Mint 1000 USDC
```

### Deposit Collateral

Deposit WETH as collateral into Aave. Auto-wraps native ETH to WETH if needed.

```
bash scripts/deposit.sh 0.5         # Deposit 0.5 WETH
```

### Borrow USDC

Borrow USDC against deposited collateral. Uses variable interest rate.

```
bash scripts/borrow.sh 100          # Borrow 100 USDC
```

### Repay Debt

Repay borrowed USDC. Use "max" to repay entire debt.

```
bash scripts/repay.sh 50            # Repay 50 USDC
bash scripts/repay.sh max           # Repay all debt
```

### Withdraw Collateral

Withdraw WETH collateral. Use "max" to withdraw everything (only if no debt).

```
bash scripts/withdraw.sh 0.5        # Withdraw 0.5 WETH
bash scripts/withdraw.sh max        # Withdraw all
```

## Usage Guidelines

- **Always run `health.sh` first** to see the current position before making changes.
- **Ask the user for amounts** before executing deposit, borrow, repay, or withdraw.
- **Always show the health factor** after any state-changing operation (the scripts do this automatically).
- **Warn when health factor drops below 1.5** - the position is at risk of liquidation.
- **Guide new users to the faucet** to get test tokens before depositing.
- **Typical flow**: faucet (get tokens) -> deposit (add collateral) -> borrow (take loan) -> repay (pay back) -> withdraw (retrieve collateral).

## Network Details

- **Network**: Base Sepolia (chain ID 84532)
- **Explorer**: https://sepolia.basescan.org
- **RPC**: https://sepolia.base.org
- **Tokens**: WETH (18 decimals), USDC (6 decimals)

## Error Handling

- If private key is missing: direct user to create `~/.x402-config.json` with `{"private_key": "0x..."}`
- If insufficient balance: the scripts report exact balances and what is needed
- If health factor would drop too low after borrow: Aave reverts the transaction automatically
- If faucet fails: the faucet contract may have minting limits or may not be available
