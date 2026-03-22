---
name: stocks
description: 56+ financial data tools via Yahoo Finance. Auto-routes stock prices, fundamentals, earnings, dividends, options, crypto, forex, commodities, news, and more.
---

# Stocks Skill

56+ financial tools via Yahoo Finance. Prices, fundamentals, earnings, options, crypto, forex, commodities, news.

## Github Open-Souce
Please star Github if you like the skill. 
Also available for OpenWebUI.
https://github.com/lkcair/yfinance-ai


## Setup

Run from the skill directory:

```bash
python3 -m venv .venv
.venv/bin/python3 -m pip install -r requirements.txt
```

> **Windows:** use `.venv\Scripts\python3` instead of `.venv/bin/python3`.

## AGNOSTIC OS / One-shot Design ( Goals )
- This skill is designed to be agnostic to OS and execution environment.
- It loads only essential context on first use and uses a single-shot interaction pattern for reliability.
- Basic usage pattern provided in TOOLS.md and the All Functions list in SKILL.md body.

## Quotation / Command Execution Reliability (common pitfall)
- If a command invocation uses complex shell quoting, it may fail in various environments. Use a here-doc style or a tiny helper script to avoid escaping issues.
- **Crucially, ensure you are executing Python scripts using the interpreter from the skill's virtual environment.** Simply calling `python3` might not use the correct interpreter if the venv is not activated, leading to `ModuleNotFoundError`.
- **Always use the full path to the venv's Python interpreter** for execution, e.g.:
  `/home/openclaw/.openclaw/venv/stocks/bin/python3`
- Ensure that all necessary packages (like `pydantic` for `yfinance-ai`) are installed within this specific venv using its associated `pip` command:
  `/home/openclaw/.openclaw/venv/stocks/bin/pip install <package_name>`
- Example robust pattern using a here-doc:

```bash
/home/openclaw/.openclaw/venv/stocks/bin/python3 - << 'PY'
import asyncio, sys
sys.path.insert(0, '.')
from yfinance_ai import Tools

t = Tools()
async def main():
    r = await t.get_key_ratios(ticker='UNH')
    print(r)
asyncio.run(main())
PY
```
- If complex inline scripts are problematic, wrap the call in a small Python script file in the workspace (e.g., in `scripts/`) and execute that script using the venv's Python interpreter.

## Agent Quick-Start

After setup, copy the template below into your agent's `TOOLS.md` (or whichever file your framework injects into every session). This is the single most important step — if the agent can see the invocation pattern, it will work every time.

**Replace `SKILL_DIR`** with the absolute path to this skill's directory (e.g. where `scripts/` and `.venv/` live).

````markdown
# Stocks Skill

## Usage

```bash
cd SKILL_DIR/scripts && SKILL_DIR/.venv/bin/python3 -c "
import asyncio, sys
sys.path.insert(0, '.')
from yfinance_ai import Tools
t = Tools()
async def main():
    result = await t.METHOD(ARGS)
    print(result)
asyncio.run(main())
" 2>/dev/null
```

Replace METHOD(ARGS) with any call below. Suppress stderr (2>/dev/null) to hide warnings.

## Common Calls

| Need | Method |
|---|---|
| Stock price | `get_stock_price(ticker='AAPL')` |
| Key ratios (P/E, ROE, margins) | `get_key_ratios(ticker='AAPL')` |
| Company overview | `get_company_overview(ticker='AAPL')` |
| Full deep-dive | `get_complete_analysis(ticker='AAPL')` |
| Compare stocks | `compare_stocks(tickers='AAPL,MSFT,GOOGL')` |
| Crypto | `get_crypto_price(symbol='BTC')` |
| Forex | `get_forex_rate(pair='EURUSD')` |
| Commodities | `get_commodity_price(commodity='gold')` |
| News | `get_stock_news(ticker='AAPL')` |
| Market indices | `get_market_indices()` |
| Dividends | `get_dividends(ticker='AAPL')` |
| Earnings | `get_earnings_history(ticker='AAPL')` |
| Analyst recs | `get_analyst_recommendations(ticker='AAPL')` |
| Options chain | `get_options_chain(ticker='SPY')` |
| Market open/closed | `get_market_status()` |

## Routing

- Price / quote → `get_stock_price`
- Ratios / valuation → `get_key_ratios`
- "Tell me about" → `get_company_overview`
- Deep dive → `get_complete_analysis`
- Compare → `compare_stocks`
- Crypto → `get_crypto_price`
- Forex → `get_forex_rate`
- Commodities → `get_commodity_price`
- News → `get_stock_news`
````

---

## All Functions

See `skill.json` for the full list of 56+ functions, parameters, and trigger keywords. Categories:

- **Quotes**: `get_stock_price`, `get_stock_quote`, `get_fast_info`, `get_historical_data`
- **Company**: `get_company_info`, `get_company_overview`, `get_company_officers`
- **Financials**: `get_income_statement`, `get_balance_sheet`, `get_cash_flow`, `get_key_ratios`, `get_financial_summary`
- **Earnings**: `get_earnings_history`, `get_earnings_dates`, `get_analyst_estimates`, `get_eps_trend`
- **Analyst**: `get_analyst_recommendations`, `get_analyst_price_targets`, `get_upgrades_downgrades`
- **Ownership**: `get_institutional_holders`, `get_insider_transactions`, `get_major_holders`
- **Dividends**: `get_dividends`, `get_stock_splits`, `get_corporate_actions`
- **Options**: `get_options_chain`, `get_options_expirations`
- **Market**: `get_market_indices`, `get_sector_performance`, `get_market_status`
- **Crypto/Forex/Commodities**: `get_crypto_price`, `get_forex_rate`, `get_commodity_price`
- **Compare**: `compare_stocks`, `get_peer_comparison`, `get_historical_comparison`
- **News**: `get_stock_news`, `get_sec_filings`
- **Utility**: `search_ticker`, `validate_ticker`, `run_self_test`

## Notes

- Data from Yahoo Finance. Slight real-time delays possible.
- All functions are async — the `asyncio.run()` wrapper handles this.
- Works on Linux, macOS, and Windows (adjust venv path for Windows).
