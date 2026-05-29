---
name: defi-expert
description: DeFi protocol expert ensuring correct data formats, types, denominations, and API structures. MUST be consulted before writing ANY protocol integration code. Triggers on ANY mention of Aave, Compound, Uniswap, Curve, Balancer, or DeFi terms like liquidation, swap, flash loan, health factor.
---

# DeFi Expert

DeFi protocol expert ensuring correct data formats, types, and denominations.

## When to Use

- Writing ANY protocol integration code (Aave, Compound, Uniswap, Curve, Balancer)
- Working with token amounts and decimals
- Implementing swaps, liquidations, or flash loans
- Debugging DeFi-related precision issues
- Reviewing code that handles token values

## Workflow

### Step 1: Verify Token Decimals

Check decimals for each token (USDC=6, WBTC=8, ETH=18).

### Step 2: Check Denomination

Verify correct unit (wei, ray, wad, bps).

### Step 3: Validate Addresses

Ensure checksummed addresses are used.

---

**CRITICAL: Before writing ANY DeFi code, verify:**
1. Token decimals (USDC=6, not 18!)
2. Denomination (wei, ray, wad, bps)
3. Checksummed addresses

## Denomination Standards

| Unit | Decimals | Usage |
|------|----------|-------|
| wei | 0 | ETH amounts |
| ray | 27 | Aave rates |
| wad | 18 | MakerDAO |
| bps | 4 | Basis points (100 = 1%) |

## Token Decimals

| Token | Decimals |
|-------|----------|
| ETH/WETH | 18 |
| USDC | 6 ⚠️ |
| USDT | 6 ⚠️ |
| DAI | 18 |
| WBTC | 8 ⚠️ |

## Common Errors
```typescript
// ❌ WRONG
const amount = parseEther(value);  // USDC has 6 decimals!
const hf = rawHF / 1e18;  // Aave uses 1e27!

// ✓ CORRECT
const decimals = await token.decimals();
const amount = parseUnits(value, decimals);
const hf = rawHF / 1e27;
```
