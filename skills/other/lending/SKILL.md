---
name: lending
description: LOAN Protocol lending and borrowing on XPR Network (lending.loan contract)
---

## LOAN Protocol (Metal X Lending)

You have tools to interact with the LOAN Protocol on XPR Network — a Compound-style pooled lending protocol at `lending.loan`. Users supply assets to earn interest and borrow against their collateral.

**IMPORTANT: LOAN Protocol is mainnet only.** There is no testnet deployment. All lending tools operate on mainnet.

### Key Concepts

- **L-Tokens** — share tokens (LBTC, LUSDC, LXPR, etc.) representing a user's share in the lending pool. When you supply XBTC, you receive LBTC. L-tokens auto-compound interest.
- **Collateral Factor** — max borrow percentage of collateral value (e.g. 70% = can borrow up to $70 per $100 deposited). Borrowing close to this limit risks immediate liquidation.
- **Utilization Rate** — ratio of borrowed to total assets. High utilization = higher borrow rates. Each market targets an optimal utilization (kink point).
- **Variable Rate** — borrow rate that fluctuates with utilization. All borrowers in a market pay the same variable rate.
- **Liquidation** — when a user's borrow exceeds their collateral factor threshold, liquidators can repay the debt and seize discounted collateral. Liquidation incentive is currently 10%.
- **LOAN Token** — governance/reward token. Suppliers and borrowers earn LOAN rewards proportional to their position.

### Available Markets

14 active markets including: XUSDC, XBTC, XETH, XPR, XMT, XDOGE, XLTC, XXRP, XSOL, XXLM, XADA, XHBAR, XUSDT, XMD.

### Read-Only Tools (safe, no signing)

- `loan_list_markets` — list all lending markets with utilization, reserves, interest models, and collateral factors
- `loan_get_market` — get detailed info for a specific market by L-token symbol (e.g. "LBTC")
- `loan_get_user_positions` — get a user's supply (L-token shares) and borrow positions across all markets
- `loan_get_user_rewards` — get a user's unclaimed LOAN rewards per market
- `loan_get_config` — get global lending config (oracle, close factor, liquidation incentive)
- `loan_get_market_apy` — get historical deposit/borrow APY including LOAN rewards (7d, 30d, 90d) from Metal X API
- `loan_get_market_tvl` — get historical TVL (total value locked) in USD with utilization ratio (7d, 30d, 90d)

### Write Tools (require `confirmed: true`)

All write operations require explicit confirmation. For supply and repay, the tool builds a token transfer to `lending.loan`. For borrow/redeem/withdraw, it calls the lending contract directly.

- `loan_enter_markets` — enter markets to enable lending/borrowing (must do this first)
- `loan_exit_markets` — exit markets (only if no outstanding positions)
- `loan_supply` — supply underlying tokens to earn interest (transfers to lending.loan with "mint" memo)
- `loan_borrow` — borrow underlying tokens against deposited collateral
- `loan_repay` — repay variable or stable borrows (transfers to lending.loan with "repay" memo)
- `loan_redeem` — redeem L-tokens for underlying tokens (burns deposited shares)
- `loan_withdraw_collateral` — withdraw L-tokens from collateral (reduces borrowing capacity)
- `loan_claim_rewards` — claim accrued LOAN token rewards

### Typical User Flow

1. **Enter markets** — `loan_enter_markets` with the market symbols you want to use
2. **Supply** — `loan_supply` underlying tokens (e.g. 1.0 XBTC) → auto-mints LBTC and deposits as collateral
3. **Borrow** — `loan_borrow` against collateral (e.g. borrow 500 XUSDC using LBTC collateral)
4. **Repay** — `loan_repay` when ready to pay back the loan
5. **Redeem** — `loan_redeem` to withdraw your original tokens + earned interest
6. **Claim** — `loan_claim_rewards` to claim any LOAN token rewards

### Safety Rules

- NEVER borrow close to the collateral factor limit — users will be liquidated
- Always recommend borrowing at most 50-60% of the collateral factor to leave a safety buffer
- Check utilization before redeeming — high utilization means less cash available for withdrawals
- Supply and repay use token transfers (to lending.loan with memo); borrow/redeem/withdraw use direct contract actions
- All write tools require `confirmed: true` — present the details first and ask for confirmation
