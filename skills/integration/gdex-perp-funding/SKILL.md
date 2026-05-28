---
name: gdex-perp-funding
description: Deposit and withdraw USDC to/from HyperLiquid for perpetual futures trading — constraints, amounts, and managed-custody flow
---

# GDEX: HyperLiquid Funding (Deposit / Withdraw)

Manage USDC deposits and withdrawals between your managed wallet and HyperLiquid perp account.

## When to Use

- Depositing USDC to HyperLiquid before trading perps
- Withdrawing USDC from HyperLiquid back to managed wallet
- Understanding deposit constraints and delivery times

## Prerequisites

- `@gdexsdk/gdex-skill` installed
- Authenticated via managed-custody sign-in — see **gdex-authentication**

## Deposit USDC to HyperLiquid

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

// Amount is human-readable USDC — SDK converts to smallest unit (6 decimals) internally
await skill.perpDeposit({ amount: '10' });   // deposit 10 USDC (minimum)
await skill.perpDeposit({ amount: '100' });  // deposit 100 USDC
```

### Managed-Custody Deposit (Explicit)

```typescript
await skill.perpDeposit({
  amount: '50',
  tokenAddress: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831', // USDC on Arbitrum
  chainId: 42161,     // Arbitrum
  apiKey,
  walletAddress,      // MUST be the CONTROL wallet address (from sign-in), NOT the managed address
  sessionPrivateKey,
});
```

> **CRITICAL:** `walletAddress` must be the **control wallet address** used during sign-in — NOT the managed-custody address returned by `/v1/user`. Passing the managed address causes `400 Unauthorized (code 103)`. See **gdex-authentication** for details.

## Withdraw USDC from HyperLiquid

```typescript
await skill.perpWithdraw({ amount: '5' });   // withdraw 5 USDC
```

### Managed-Custody Withdraw (Explicit)

```typescript
await skill.perpWithdraw({
  amount: '25',
  apiKey,
  walletAddress,
  sessionPrivateKey,
});
```

## Deposit Constraints

| Constraint | Value |
|------------|-------|
| **Chain** | Arbitrum only (chainId `42161`) |
| **Token** | USDC only (`0xaf88d065e77c8cC2239327C5EDb3A432268e5831`) |
| **Min deposit** | 10 USDC |
| **Amount format** | Human-readable (e.g., `'10'` for 10 USDC); SDK converts to 6 decimal smallest unit internally |
| **Fee buffer** | Managed wallet must hold `amount × 1.01` (1% fee) |
| **Delivery time** | ~10 minutes after Arbitrum tx confirms |
| **On-chain amount** | 10 USDC = `10000000` (6 decimals) in the ABI encoding |

## Check USDC Balance on HyperLiquid

```typescript
const balance = await skill.getHlUsdcBalance({ walletAddress: '0xYourAddress' });
console.log('Available USDC:', balance);
```

## ABI Encoding Details

The deposit uses a specific ABI schema with `uint64` for chainId:

| Field | ABI Type | Example |
|-------|----------|---------|
| `chainId` | `uint64` | `42161` |
| `tokenAddress` | `address` | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` |
| `amount` | `uint256` | `10000000` (10 USDC) |
| `nonce` | `string` | Client-generated timestamp + random |

**CRITICAL:** `chainId` is `uint64`, NOT `uint256`. Using `uint256` causes `400 Unauthorized (code 103)`.

Withdraw ABI schema:

| Field | ABI Type | Example |
|-------|----------|---------|
| `amount` | `string` | `'5000000'` (5 USDC in smallest unit) |
| `nonce` | `string` | Client-generated |

## Common Issues

### "Insufficient balance" on deposit
- Managed wallet needs `amount × 1.01` USDC on Arbitrum (1% fee buffer)
- Check managed wallet balance, not HL perp balance

### Deposit doesn't appear on HL
- Normal delivery time is ~10 minutes after Arbitrum tx confirmation
- Use `getHlUsdcBalance()` or `getHlAccountState()` to check

### 400 Unauthorized (code 103)
- **Most common cause:** Passing the managed address as `walletAddress` instead of the control wallet address — see **gdex-authentication**
- Second cause: `uint256` vs `uint64` encoding mismatch for chainId — see **gdex-perp-trading** for full ABI details

## Autonomous Agent Notes (Live-Tested)

1. **Deposit of 10 USDC was E2E verified.** Takes ~10 minutes for USDC to appear on HyperLiquid after Arbitrum tx confirms.
2. **After deposit, check balance with `getHlAccountState()`** — `getGbotUsdcBalance` returns 404.
3. **Amount is human-readable for high-level methods** (`perpDeposit({ amount: '10' })`), but the ABI encoding internally converts to 6-decimal smallest unit (10 USDC = 10000000).
4. **Sign-in must use `chainId: 1`** (EVM) for HL deposit/withdraw operations.
5. **`walletAddress` MUST be control wallet** — passing managed address → 400 Unauthorized (code 103).

## Related Skills

- **gdex-authentication** — Managed-custody auth required for deposits/withdrawals
- **gdex-perp-trading** — Trade perps after funding your HL account
- **gdex-portfolio** — Check overall portfolio including HL positions
