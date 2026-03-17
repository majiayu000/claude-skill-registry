---
name: personal-finance-skill
description: >
  Personal finance management skill providing 75 tools across 7 extensions
  for bank account aggregation (Plaid), brokerage trading (Alpaca), portfolio
  monitoring (IBKR), tax optimization, market intelligence (Finnhub, SEC EDGAR,
  FRED, BLS, Alpha Vantage), social sentiment (StockTwits, X/Twitter, Quiver),
  and financial analysis. Supports scheduled scans, anomaly detection, net worth
  tracking, tax-loss harvesting, and approval-gated execution of financial actions.
license: MIT
metadata:
  author: contributors
  version: "2.0.0"
  tools: "75"
  extensions: "finance-core, plaid-connect, alpaca-trading, ibkr-portfolio, tax-engine, market-intel, social-sentiment"
---

# Personal Finance Skill

A comprehensive personal finance management skill with 75 tools across 7 extensions for banking, investing, tax, market intelligence, social sentiment, and financial analysis workflows.

## When to Use

Activate this skill when a user asks for:

- **Account aggregation** — connecting bank accounts, viewing balances, syncing transactions
- **Net worth / cash flow** — computing totals, tracking spending, savings rate analysis
- **Portfolio monitoring** — positions, allocation, performance, drift detection
- **Trading** — placing/canceling orders, market data, asset lookup (Alpaca)
- **Tax optimization** — estimated liability, TLH candidates, wash sale checks, quarterly payments
- **Tax document processing** — parsing W-2, 1099-B/DIV/INT, K-1, Form 1040, Schedules A-E/SE, Form 8949, Form 6251 (AMT), state returns
- **Market intelligence** — company news, SEC filings, analyst recommendations, economic data (FRED, BLS), news sentiment
- **Social sentiment** — StockTwits sentiment, X/Twitter cashtag analysis, trending symbols, congressional trading
- **Recurring expense tracking** — subscriptions, bills, income streams
- **Anomaly detection** — unusual transactions, balance drops, duplicate charges
- **Financial briefings** — weekly/monthly summaries with action items
- **Scheduled finance workflows** — cron-based scans, alerts, reports

## Architecture Overview

Seven extensions organized in three layers:

```
Intelligence Layer
  tax-engine (23 tools) — parsing (15), liability, TLH, wash sales, lots,
    Schedule D computation, state tax, AMT
  market-intel (10 tools) — news, fundamentals, SEC filings, economic data
  social-sentiment (6 tools) — StockTwits, X/Twitter, congressional trades

Data Source Adapters
  plaid-connect (8)   alpaca-trading (10)   ibkr-portfolio (9)

Foundation Layer
  finance-core (9 tools) — canonical models, storage, normalization,
    policy checks, anomaly detection, briefs
```

**Data flow**: Adapters fetch provider data → finance-core normalizes and stores → intelligence layer analyzes → policy engine gates actions.

## Tool Catalog

### finance-core — 9 tools

| Tool | Description | Risk |
|------|-------------|------|
| `finance_upsert_snapshot` | Store normalized financial data snapshot (idempotent) | LOW |
| `finance_get_state` | Get current financial state (accounts, positions, etc.) | READ |
| `finance_get_transactions` | Query transactions with filters and pagination | READ |
| `finance_get_net_worth` | Calculate net worth breakdown by category/account | READ |
| `finance_detect_anomalies` | Scan for unusual transactions, balance drops, fee spikes | READ |
| `finance_cash_flow_summary` | Income vs expenses by category with savings rate | READ |
| `finance_subscription_tracker` | Identify recurring charges and subscription patterns | READ |
| `finance_generate_brief` | Create structured financial summary with action items | READ |
| `finance_policy_check` | Validate proposed action against policy rules | READ |

> Full schemas: [references/ext-finance-core.md](references/ext-finance-core.md)

### plaid-connect — 8 tools

| Tool | Description | Risk |
|------|-------------|------|
| `plaid_create_link_token` | Initialize Plaid Link for account connection | LOW |
| `plaid_exchange_token` | Exchange public token for permanent access | MED |
| `plaid_get_accounts` | List connected accounts with balances | READ |
| `plaid_get_transactions` | Fetch transactions via cursor-based sync | READ |
| `plaid_get_investments` | Fetch holdings, securities, investment transactions | READ |
| `plaid_get_liabilities` | Fetch credit, student loan, and mortgage data | READ |
| `plaid_get_recurring` | Identify recurring inflow/outflow streams | READ |
| `plaid_webhook_handler` | Process incoming Plaid webhook events | LOW |

> Full schemas: [references/ext-plaid-connect.md](references/ext-plaid-connect.md)

### alpaca-trading — 10 tools

| Tool | Description | Risk |
|------|-------------|------|
| `alpaca_get_account` | Get account balances, buying power, status | READ |
| `alpaca_list_positions` | List all open positions | READ |
| `alpaca_get_position` | Get single position by symbol | READ |
| `alpaca_list_orders` | List orders with status/date filters | READ |
| `alpaca_create_order` | Submit buy/sell order with safety checks | **HIGH** |
| `alpaca_cancel_order` | Cancel a pending order | MED |
| `alpaca_portfolio_history` | Historical equity and P/L over time | READ |
| `alpaca_get_assets` | Search tradable assets by class/exchange | READ |
| `alpaca_market_data` | Get snapshots, bars, or quotes for symbols | READ |
| `alpaca_clock` | Check if market is open, next open/close | READ |

> Full schemas: [references/ext-alpaca-trading.md](references/ext-alpaca-trading.md)

### ibkr-portfolio — 9 tools

| Tool | Description | Risk |
|------|-------------|------|
| `ibkr_auth_status` | Check gateway authentication status | READ |
| `ibkr_tickle` | Keep gateway session alive (~1 min interval) | LOW |
| `ibkr_list_accounts` | List accounts (must call first) | READ |
| `ibkr_get_positions` | Get positions for an account (paginated) | READ |
| `ibkr_portfolio_allocation` | Allocation by asset class, sector, group | READ |
| `ibkr_portfolio_performance` | NAV time series and returns | READ |
| `ibkr_search_contracts` | Search contracts by symbol/name/type | READ |
| `ibkr_market_snapshot` | Real-time market data for contracts | READ |
| `ibkr_get_orders` | Get current live orders | READ |

> Full schemas: [references/ext-ibkr-portfolio.md](references/ext-ibkr-portfolio.md)

### tax-engine — 23 tools

| Tool | Description | Risk |
|------|-------------|------|
| `tax_parse_1099b` | Parse 1099-B (proceeds, cost basis, wash sales) | READ |
| `tax_parse_1099div` | Parse 1099-DIV (dividends, capital gains) | READ |
| `tax_parse_1099int` | Parse 1099-INT (interest, bond premiums) | READ |
| `tax_parse_w2` | Parse W-2 (wages, withholding, SS/Medicare) | READ |
| `tax_parse_k1` | Parse Schedule K-1 (partnership pass-through) | READ |
| `tax_parse_1040` | Parse Form 1040 (main federal return) | READ |
| `tax_parse_schedule_a` | Parse Schedule A (itemized deductions, SALT cap) | READ |
| `tax_parse_schedule_b` | Parse Schedule B (interest/dividend payors) | READ |
| `tax_parse_schedule_c` | Parse Schedule C (self-employment income) | READ |
| `tax_parse_schedule_d` | Parse Schedule D (capital gains netting) | READ |
| `tax_parse_schedule_e` | Parse Schedule E (rental/royalty/partnership) | READ |
| `tax_parse_schedule_se` | Parse Schedule SE (self-employment tax) | READ |
| `tax_parse_form_8949` | Parse Form 8949 (sales and dispositions) | READ |
| `tax_parse_state_return` | Parse state return (CA 540, NY IT-201, etc.) | READ |
| `tax_parse_form_6251` | Parse Form 6251 (AMT) | READ |
| `tax_estimate_liability` | Calculate federal/state tax with brackets | READ |
| `tax_find_tlh_candidates` | Identify tax-loss harvesting opportunities | READ |
| `tax_check_wash_sales` | Validate wash sale rule compliance (61-day window) | READ |
| `tax_lot_selection` | Compare FIFO/LIFO/specific ID for a proposed sale | READ |
| `tax_quarterly_estimate` | Quarterly estimated payments with safe harbor | READ |
| `tax_compute_schedule_d` | Compute Schedule D netting with loss carryover | READ |
| `tax_compute_state_tax` | Compute state tax for CA/NY/NJ/IL/PA/MA/TX/FL | READ |
| `tax_compute_amt` | Compute Alternative Minimum Tax (Form 6251) | READ |

> Full schemas: [references/ext-tax-engine.md](references/ext-tax-engine.md)

### market-intel — 10 tools

| Tool | Description | Risk |
|------|-------------|------|
| `intel_company_news` | Get recent news articles for a company (Finnhub) | READ |
| `intel_market_news` | Get general market news by category (Finnhub) | READ |
| `intel_stock_fundamentals` | Get reported financial statements (Finnhub) | READ |
| `intel_analyst_recommendations` | Get analyst buy/hold/sell consensus (Finnhub) | READ |
| `intel_sec_filings` | List SEC filings for a company by ticker (EDGAR) | READ |
| `intel_sec_search` | Full-text search across SEC filings (EDGAR) | READ |
| `intel_fred_series` | Fetch economic time series (GDP, CPI, rates) (FRED) | READ |
| `intel_fred_search` | Search for FRED series by keyword | READ |
| `intel_bls_data` | Fetch labor/price statistics time series (BLS) | READ |
| `intel_news_sentiment` | Get news with AI-scored sentiment (Alpha Vantage) | READ |

> Full schemas: [references/ext-market-intel.md](references/ext-market-intel.md)

### social-sentiment — 6 tools

| Tool | Description | Risk |
|------|-------------|------|
| `social_stocktwits_sentiment` | Get bull/bear sentiment for a stock (StockTwits) | READ |
| `social_stocktwits_trending` | Get currently trending symbols (StockTwits) | READ |
| `social_x_search` | Search recent tweets by keyword (X/Twitter) | READ |
| `social_x_user_timeline` | Get recent tweets from a user (X/Twitter) | READ |
| `social_x_cashtag` | Search cashtag with keyword sentiment scoring (X) | READ |
| `social_quiver_congress` | Get congressional stock trading disclosures (Quiver) | READ |

> Full schemas: [references/ext-social-sentiment.md](references/ext-social-sentiment.md)

## Key Workflows

### 1. Onboarding — Connect Accounts

```
plaid_create_link_token(products: ["transactions", "investments", "liabilities"])
  → User completes Plaid Link
  → plaid_exchange_token(publicToken)
  → plaid_get_accounts → finance_upsert_snapshot(source: "plaid")
  → plaid_get_transactions → finance_upsert_snapshot
  → plaid_get_investments → finance_upsert_snapshot
  → finance_get_net_worth → present baseline to user
```

### 2. Daily Scan — Anomaly Detection

```
plaid_get_transactions(cursor) → finance_upsert_snapshot
alpaca_list_positions → finance_upsert_snapshot(source: "alpaca")
ibkr_auth_status → ibkr_get_positions → finance_upsert_snapshot(source: "ibkr")
  → finance_detect_anomalies(lookbackDays: 7)
  → Alert on medium/high severity findings
```

### 3. Tax-Loss Harvesting

```
finance_get_state(include: ["positions"])
  → tax_find_tlh_candidates(positions, marginalRate)
  → tax_check_wash_sales(proposedSales, recentPurchases)
  → tax_lot_selection(symbol, qty, lots)
  → finance_policy_check(actionType: "tax_move")
  → [If approved] alpaca_create_order(side: "sell", ...)
```

### 4. Quarterly Tax Review

```
tax_parse_w2 + tax_parse_1099b + tax_parse_1099div + tax_parse_1099int
  → tax_estimate_liability(filingStatus, income)
  → tax_quarterly_estimate(projectedIncome, priorYearTax, paymentsMade)
  → finance_generate_brief(period: "quarterly")
```

### 5. Portfolio Monitoring

```
alpaca_list_positions + ibkr_get_positions
  → finance_upsert_snapshot (both sources)
  → ibkr_portfolio_allocation (check drift)
  → alpaca_portfolio_history (performance trend)
  → finance_detect_anomalies
  → finance_generate_brief(period: "weekly")
```

### 6. Company Research — Market Intelligence

```
intel_company_news(symbol: "AAPL", limit: 10)
  → intel_analyst_recommendations(symbol: "AAPL")
  → intel_stock_fundamentals(symbol: "AAPL", freq: "quarterly")
  → intel_sec_filings(symbol: "AAPL", formType: "10-K")
  → intel_news_sentiment(tickers: "AAPL")
  → social_stocktwits_sentiment(symbol: "AAPL")
  → social_x_cashtag(symbol: "AAPL")
```

### 7. Economic Overview

```
intel_fred_series(seriesId: "GDP")
  → intel_fred_series(seriesId: "CPIAUCSL")
  → intel_fred_series(seriesId: "UNRATE")
  → intel_bls_data(seriesIds: ["CES0000000001"])
  → intel_fred_series(seriesId: "DFF")
```

### 8. Full Tax Return Processing

```
tax_parse_1040(rawData) → tax_parse_schedule_a(rawData)
  → tax_parse_schedule_b(rawData) → tax_parse_schedule_c(rawData)
  → tax_parse_schedule_d(rawData) → tax_parse_schedule_e(rawData)
  → tax_parse_form_8949(rawData) → tax_parse_schedule_se(rawData)
  → tax_compute_schedule_d(gains, losses, carryovers)
  → tax_compute_state_tax(stateCode, taxableIncome, filingStatus)
  → tax_compute_amt(taxableIncome, adjustments, regularTax)
  → tax_parse_state_return(rawData)
```

### 9. Congressional Trading Signals

```
social_quiver_congress(daysBack: 30)
  → Filter for large purchases
  → intel_company_news(symbol: <top_ticker>)
  → alpaca_market_data(symbols: <top_ticker>)
  → social_stocktwits_sentiment(symbol: <top_ticker>)
```

## Configuration

### Environment Variables

| Variable | Extension | Description |
|----------|-----------|-------------|
| `PLAID_CLIENT_ID` | plaid-connect | Plaid API client ID |
| `PLAID_SECRET` | plaid-connect | Plaid API secret key |
| `PLAID_ENV` | plaid-connect | sandbox / development / production |
| `ALPACA_API_KEY` | alpaca-trading | Alpaca API key |
| `ALPACA_API_SECRET` | alpaca-trading | Alpaca API secret |
| `ALPACA_ENV` | alpaca-trading | paper / live |
| `IBKR_BASE_URL` | ibkr-portfolio | Client Portal Gateway URL |
| `FINNHUB_API_KEY` | market-intel | Finnhub API key (finnhub.io) |
| `FRED_API_KEY` | market-intel | FRED API key (fred.stlouisfed.org) |
| `BLS_API_KEY` | market-intel | BLS registration key (v2) |
| `ALPHA_VANTAGE_API_KEY` | market-intel | Alpha Vantage API key |
| `X_API_BEARER_TOKEN` | social-sentiment | X/Twitter OAuth 2.0 Bearer Token |
| `QUIVER_API_KEY` | social-sentiment | Quiver Quantitative API key |

### Extension Config

Each extension has an `openclaw.plugin.json` with a `configSchema`. Key settings:

- **finance-core**: `storageDir`, `anomalyThresholds`, `policyRulesPath`
- **plaid-connect**: `plaidEnv`, `webhookUrl`, `clientName`, `countryCodes`
- **alpaca-trading**: `env` (paper/live), `maxOrderQty`, `maxOrderNotional`
- **ibkr-portfolio**: `baseUrl`, `defaultAccountId`
- **tax-engine**: `defaultFilingStatus`, `defaultState`, `defaultTaxYear`
- **market-intel**: `finnhubApiKeyEnv`, `fredApiKeyEnv`, `blsApiKeyEnv`, `alphaVantageApiKeyEnv`, `secEdgarUserAgent`
- **social-sentiment**: `xApiBearerTokenEnv`, `quiverApiKeyEnv`

## Cron Examples

### Weekly Financial Brief
```bash
openclaw cron add \
  --name "Finance Weekly Brief" \
  --cron "0 8 * * 1" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Run personal-finance-skill weekly workflow: sync all providers, compute net worth delta, top spend changes, upcoming bills, tax posture, and portfolio drift. Send concise brief with action queue."
```

### Daily Anomaly Scan
```bash
openclaw cron add \
  --name "Finance Daily Anomaly" \
  --cron "15 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Sync latest transactions, run finance_detect_anomalies. Alert on medium/high/critical findings only."
```

### Quarterly Tax Check
```bash
openclaw cron add \
  --name "Quarterly Tax Review" \
  --cron "0 9 1 1,4,6,9 *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Run quarterly tax review: estimate liability, check withholding gap, find TLH opportunities, assess quarterly payment risk."
```

### Portfolio Drift Monitor
```bash
openclaw cron add \
  --name "Portfolio Drift Monitor" \
  --cron "*/30 13-21 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --message "Check portfolio allocation vs target bands. Alert if drift exceeds threshold for 2 consecutive scans."
```

## Non-Negotiable Guardrails

These rules apply to all AI agents using this skill:

1. **Always run `finance_policy_check` before any side-effecting action** (trades, transfers, tax moves).
2. **Never bypass approval requirements.** If policy requires user or advisor approval, halt and request it.
3. **Numeric outputs must come from deterministic calculators.** Never use LLM arithmetic for tax amounts, P/L, or net worth — always use the tool.
4. **Recommendations must include assumptions and data freshness.** Every financial recommendation states what data it used and when that data was last updated.
5. **Never expose raw access tokens or API keys** in tool outputs or conversation.
6. **Never auto-execute in live trading** without explicit user confirmation, even if policy rules allow it.
7. **All investment-related outputs must include disclaimer**: "This is informational only, not financial advice. Consult a qualified advisor before making financial decisions."
8. **If data is stale, say so.** Report data freshness before advising.

## Reference Index

Detailed documentation is available in the `references/` directory:

| File | Contents |
|------|----------|
| [references/ext-finance-core.md](references/ext-finance-core.md) | 9 tools, storage layer, normalization functions |
| [references/ext-plaid-connect.md](references/ext-plaid-connect.md) | 8 tools, Plaid Link flow, webhook handling |
| [references/ext-alpaca-trading.md](references/ext-alpaca-trading.md) | 10 tools, order lifecycle, safety limits |
| [references/ext-ibkr-portfolio.md](references/ext-ibkr-portfolio.md) | 9 tools, session management, market data fields |
| [references/ext-tax-engine.md](references/ext-tax-engine.md) | 23 tools, 15 parsers + 8 calculators/strategy, form field mappings |
| [references/ext-market-intel.md](references/ext-market-intel.md) | 10 tools, Finnhub/SEC EDGAR/FRED/BLS/Alpha Vantage |
| [references/ext-social-sentiment.md](references/ext-social-sentiment.md) | 6 tools, StockTwits/X/Twitter/Quiver Quantitative |
| [references/data-models-and-schemas.md](references/data-models-and-schemas.md) | Canonical types, enums, entity schemas |
| [references/risk-and-policy-guardrails.md](references/risk-and-policy-guardrails.md) | Policy engine, approval tiers, hard rules |
| [references/api-plaid.md](references/api-plaid.md) | Full Plaid API reference |
| [references/api-alpaca-trading.md](references/api-alpaca-trading.md) | Full Alpaca API reference |
| [references/api-ibkr-client-portal.md](references/api-ibkr-client-portal.md) | IBKR Client Portal Web API reference |
| [references/api-openclaw-framework.md](references/api-openclaw-framework.md) | OpenClaw architecture reference |
| [references/api-openclaw-extension-patterns.md](references/api-openclaw-extension-patterns.md) | How to build OpenClaw extensions |
| [references/api-irs-tax-forms.md](references/api-irs-tax-forms.md) | IRS tax form schemas and rules |
