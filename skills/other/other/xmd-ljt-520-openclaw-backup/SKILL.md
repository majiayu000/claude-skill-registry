---
name: xmd
description: Metal Dollar (XMD) stablecoin — mint, redeem, supply analytics, collateral reserves, oracle prices
---

## Metal Dollar (XMD)

You have tools to interact with XMD, XPR Network's native stablecoin. XMD is a multi-collateral stablecoin pegged to $1 USD, minted and redeemed through the `xmd.treasury` contract.

### How XMD Works

- **Mint:** Send a supported stablecoin (e.g. XUSDC) to `xmd.treasury` with memo `mint` → receive equivalent XMD at oracle price
- **Redeem:** Send XMD to `xmd.treasury` with memo `redeem,SYMBOL` (e.g. `redeem,XUSDC`) → receive equivalent stablecoin back
- **1:1 peg:** Oracle-priced at $1, backed by stablecoin reserves in the treasury
- **Zero fees:** Currently 0% mint and redemption fees on all collateral types

### Supported Collateral

| Token | Contract | Oracle Feed | Max Treasury % | Status |
|-------|----------|-------------|----------------|--------|
| XUSDC | xtokens | USDC/USD | 60% | Mint + Redeem |
| XPAX | xtokens | PAX/USD | 15% | Mint + Redeem |
| XPYUSD | xtokens | PYUSD/USD | 15% | Mint + Redeem |
| MPD | mpd.token | MPD/USD | 2% | Mint + Redeem |

### Contracts

- `xmd.token` — XMD token contract (precision 6, issuer = xmd.treasury)
- `xmd.treasury` — Mint/redeem logic, collateral management, oracle integration
- `oracles` — On-chain price feeds from multiple providers

### Read-Only Tools (safe, no signing)

- `xmd_get_config` — treasury config: paused state, fee account, minimum oracle price threshold
- `xmd_list_collateral` — all supported collateral tokens with fees, limits, oracle prices, mint/redeem volumes
- `xmd_get_supply` — XMD total circulating supply
- `xmd_get_balance` — check any account's XMD balance
- `xmd_get_treasury_reserves` — current stablecoin reserves backing XMD, with USD valuations and collateralization ratio
- `xmd_get_oracle_price` — current oracle price for any collateral token (with individual provider data)

### Write Tools (require `confirmed: true`)

- `xmd_mint` — mint XMD by depositing a supported stablecoin
- `xmd_redeem` — redeem XMD for a supported stablecoin

### Safety Rules

- Oracle price must be >= 0.995 (`minOraclePrice`) for mint/redeem to proceed
- Each collateral has a `maxTreasuryPercent` cap — if the treasury already holds too much of one stablecoin, minting with it is blocked
- Check `isMintEnabled` / `isRedeemEnabled` before attempting operations
- The treasury can be paused by admins (`isPaused`) — check config first
- XMD has precision 6 — all amounts use 6 decimal places (e.g. `1.000000 XMD`)
