---
name: tax
description: Crypto tax reporting for XPR Network with regional support
---

## Crypto Tax Reporting

You have tools to generate crypto tax reports from on-chain XPR Network activity. Supports **New Zealand** (NZ) and **United States** (US).

### Key Facts

- **NZ tax year:** April 1 – March 31 (e.g. "2025" = Apr 2024 – Mar 2025)
- **US tax year:** January 1 – December 31 (calendar year, e.g. "2024" = Jan 2024 – Dec 2024)
- **NZ has NO capital gains tax** — all crypto gains are taxed as **income** if you're a regular trader
- **US HAS capital gains tax** — short-term (<1 year) taxed as ordinary income, long-term at lower rates. Uses 2024 Single filer federal brackets. Does not include state taxes or NIIT.
- **Cost basis methods:** FIFO (first-in-first-out) or Average Cost
- **All tools are read-only** — they query APIs and calculate, never transact
- **Default region is NZ** — pass `region: "US"` for US tax reports

### Typical Workflow

For a full tax report, the recommended sequence is:

1. `tax_get_balances` — opening balances (start of tax year) and closing balances (end of tax year)
2. `tax_get_dex_trades` — all Metal X DEX trading history for the period
3. `tax_get_transfers` — on-chain transfers, auto-categorized (staking rewards, lending, swaps, NFT sales, etc.)
4. `tax_get_rates` — local currency conversion rates for each token
5. `tax_calculate_gains` — compute taxable gains/losses using FIFO or Average Cost
6. `tax_generate_report` — full report with tax brackets and estimated tax

Or use `tax_generate_report` directly for a one-shot report that orchestrates all steps automatically.

### Data Sources (Mainnet Only)

- **Saltant API** — historical balance snapshots (liquid, staked, lending, yield farm)
- **Metal X API** — DEX trade history in CSV format (only filled trades)
- **Hyperion API** — raw on-chain transfer/action history
- **CoinGecko API** — historical and current crypto prices (set `COINGECKO_API_KEY` in .env for full historical access)

### Transfer Categories

Transfers are auto-categorized by sender/receiver:

| Category | Detection |
|----------|-----------|
| `staking_reward` | from `eosio` or `eosio.vpay` |
| `lending_deposit` | to `lending.loan` |
| `lending_withdrawal` | from `lending.loan` |
| `lending_interest` | from `lending.loan` with interest memo |
| `swap_deposit` | to `proton.swaps` |
| `swap_withdrawal` | from `proton.swaps` |
| `long_stake` | to `longstaking` (XPR long staking) |
| `long_unstake` | from `longstaking` |
| `loan_stake` | to `lock.token` or `yield.farms` (LOAN/SLOAN staking) |
| `loan_unstake` | from `lock.token` or `yield.farms` |
| `dex_deposit` | to `dex` or `metalx` |
| `dex_withdrawal` | from `dex` or `metalx` |
| `nft_sale` | from `atomicmarket` |
| `nft_purchase` | to `atomicmarket` |
| `burn` | to `eosio.null` (token burn = realized loss) |
| `escrow` | to/from `agentescrow` |
| `transfer` | everything else |

### Staking Income Rules

- **Block producer rewards** (`staking_reward`): Full amount is income at time of receipt
- **Long staking** (XPR via `longstaking`): Only the **excess** over the staked amount is income. E.g. stake 100 XPR, unstake 150 XPR → income of 50 XPR
- **LOAN staking** (via `lock.token`/`yield.farms`): Same excess-only rule as long staking
- **Lending interest**: Full amount from `lending.loan` with interest memo is income

### Stablecoin Handling

XUSDC and XMD are pegged to USD — their local currency value uses forex rates (USD/NZD) directly, without CoinGecko. This is more accurate than market-based pricing for stablecoins.

### Rate Sources (Priority Order)

1. **DEX trades** — derives token prices from TOKEN/XMD trade ratios (most accurate, no API limits)
2. **Forward-fill** — gaps between DEX trade dates use nearest prior known rate
3. **CoinGecko** — fallback for dates with no DEX data. Without API key: limited to 365 days. With `COINGECKO_API_KEY`: unlimited history
4. **Forex** — stablecoins use USD→NZD conversion rate

### Delivering the Report

`tax_generate_report` returns a `report_markdown` field — a pre-formatted Markdown document with balance sheets, trading summary, income breakdown, tax brackets, and disclaimer. To deliver it:

1. Upload `report_markdown` via `store_deliverable` with `content_type: "application/pdf"` — this is the primary deliverable
2. Upload `csv_exports.disposals` via `store_deliverable` with `content_type: "text/csv"` — disposals CSV
3. Upload `csv_exports.income` via `store_deliverable` with `content_type: "text/csv"` — income events CSV
4. Call `xpr_deliver_job` with ALL URLs comma-separated (PDF first): `"https://ipfs.io/ipfs/QmPDF...,https://ipfs.io/ipfs/QmDisposals...,https://ipfs.io/ipfs/QmIncome..."`

**IMPORTANT:** You MUST complete ALL steps (upload + deliver) in a single run. Do NOT stop after uploading the PDF — you must also upload the CSVs and call `xpr_deliver_job`. The job is not complete until `xpr_deliver_job` is called.

The frontend displays the primary file (PDF) prominently and lists additional files as download links.

### Known Limitations

- Only **filled DEX trades** are included (not pending orders)
- NFT: only buy/sell supported (not auctions)
- Liquidations on Metal Lending are not supported
- Escrow payments are tracked but not fully categorized
- Historical pricing accuracy depends on DEX trade activity and CoinGecko data availability

### Important Notes

- Always include the **disclaimer** from the report — this is not tax advice
- Suggest users **save CSV exports** for the IRD 7-year record requirement
- The `region` parameter defaults to `"NZ"` on all tools — pass a different region code when other regions are added
- Set `COINGECKO_API_KEY` in .env for best historical pricing (free Demo key removes 365-day limit)
- For tokens not on CoinGecko, the tool derives prices from Metal X DEX trade ratios
