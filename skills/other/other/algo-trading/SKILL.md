---
name: algo-trading
cluster: financial
description: "Implements algorithmic trading strategies using quantitative models and financial APIs for automated trading."
tags: ["algo-trading","finance","quantitative"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "algorithmic trading finance quantitative strategies stocks analysis"
---

# algo-trading

## Purpose
This skill automates algorithmic trading by integrating quantitative models with financial APIs to execute buy/sell orders based on predefined strategies. It processes market data, runs backtests, and handles live trading to minimize human intervention in financial markets.

## When to Use
Use this skill for high-frequency trading, portfolio optimization, or strategy backtesting in volatile markets. Apply it when you need to automate trades based on indicators like moving averages or RSI, especially for stocks, forex, or crypto, to reduce emotional decisions and improve efficiency.

## Key Capabilities
- Fetch real-time or historical data from APIs like Alpha Vantage or Yahoo Finance using endpoints such as `/query?function=TIME_SERIES_DAILY`.
- Implement strategies like moving average crossover or mean reversion with built-in functions, e.g., `strategy.run('MA_Crossover', params)`.
- Backtest models on historical data with metrics like Sharpe ratio, using commands like `backtest --data CSV_FILE --strategy STRATEGY_NAME`.
- Execute trades via broker APIs, supporting integration with Alpaca (e.g., POST /v2/orders) or Robinhood, with risk controls like stop-loss.
- Handle data analysis with libraries like NumPy for calculations, e.g., computing RSI in 2 lines: `rsi = talib.RSI(close, timeperiod=14); signals = np.where(rsi > 70, 'sell', 'buy')`.

## Usage Patterns
To use this skill, first set environment variables for authentication, e.g., export ALPHA_VANTAGE_API_KEY=$SERVICE_API_KEY. Initialize the skill in your code with `import openclaw; oc = openclaw.Skill('algo-trading')`. For CLI, run `openclaw algo-trading init --config config.json` to load a strategy file. In scripts, call strategies like `oc.execute_strategy('MA_Crossover', symbols=['AAPL'], timeframe='1d')`. Always wrap calls in try-except blocks for error resilience. For live trading, enable with a flag: `oc.run_live('--broker alpaca --key $ALPACA_KEY')`.

## Common Commands/API
- CLI Command: `openclaw algo-trading run --strategy MA_Crossover --symbols AAPL,GOOG --timeframe 1h` to execute a strategy on specified stocks.
- API Endpoint: GET https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&apikey=$SERVICE_API_KEY for fetching intraday data.
- Code Snippet:  
  ```python
  import openclaw
  oc = openclaw.Skill('algo-trading')
  data = oc.fetch_data('AAPL', '1d')  # Fetches daily data
  signals = oc.analyze_strategy('MA_Crossover', data)
  ```
- Config Format: Use JSON for strategies, e.g., {"strategy": "MA_Crossover", "params": {"short_window": 50, "long_window": 200}, "symbols": ["AAPL"]}. Load via `openclaw algo-trading load-config path/to/config.json`.
- Another Command: `openclaw algo-trading backtest --file historical.csv --strategy RSI_Overbought --iterations 100` to run simulations.
- API Call Example: POST https://api.alpaca.markets/v2/orders with body {"symbol": "AAPL", "qty": 10, "side": "buy", "type": "market"} for placing orders, authenticated via $ALPACA_KEY header.

## Integration Notes
Integrate by adding the skill to your OpenClaw agent via `openclaw add-skill algo-trading`. For external APIs, set auth in env vars like export BROKER_API_KEY=$SERVICE_API_KEY and use in code: `oc.set_auth('alpaca', os.environ['BROKER_API_KEY'])`. Ensure data pipelines match, e.g., parse API responses into Pandas DataFrames for analysis. For webhooks, configure callbacks like `oc.register_webhook('/triggers', lambda event: oc.execute_strategy('event_strategy'))`. Test integrations in a sandbox environment first, using flags like `--sandbox true` to simulate trades without real execution.

## Error Handling
Always check for API errors by wrapping calls in try-except, e.g.:  
```python
try:
    response = oc.fetch_data('AAPL', '1d')
except APIError as e:
    print(f"API Error: {e.code} - {e.message}")  # Handles 429 for rate limits
```
Handle common issues like rate limits by implementing retries: use `oc.retry_on_error(call_func, max_retries=3)`. For invalid configs, validate with `openclaw algo-trading validate-config config.json`, which returns errors like "Missing param: short_window". Log all errors with timestamps for auditing, e.g., via `oc.log_error('Trade failed: insufficient funds')`. If authentication fails, prompt for env var checks, e.g., ensure $SERVICE_API_KEY is set.

## Concrete Usage Examples
1. **Backtesting a Moving Average Strategy**: Load historical data and run a backtest. Command: `openclaw algo-trading backtest --file aapl_historical.csv --strategy MA_Crossover`. In code:  
   ```python
   oc = openclaw.Skill('algo-trading')
   data = oc.load_data('aapl_historical.csv')
   results = oc.backtest_strategy('MA_Crossover', data)
   print(results['sharpe_ratio'])  # Outputs e.g., 1.2
   ```
   This analyzes past performance to refine the strategy before live use.

2. **Executing a Live Trade on RSI Signal**: Fetch real-time data, generate signals, and place an order. Command: `openclaw algo-trading run --strategy RSI_Overbought --symbols TSLA --broker alpaca`. In code:  
   ```python
   oc = openclaw.Skill('algo-trading')
   rsi_data = oc.fetch_data('TSLA', '1m')
   signal = oc.analyze_strategy('RSI_Overbought', rsi_data)
   if signal == 'sell':
       oc.execute_trade('TSLA', 'sell', 5)  # Sells 5 shares
   ```
   This automates selling when RSI exceeds 70, using live API calls.

## Graph Relationships
- Depends on: financial-data-fetcher (for market data retrieval)
- Related to: risk-analysis (for evaluating trade risks)
- Conflicts with: manual-trading (due to automation focus)
- Enhances: portfolio-management (by adding automated strategies)
