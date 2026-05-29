---
name: market-regime
cluster: financial
description: "Analyzes financial market regimes to identify trends, volatility, and shifts in asset classes."
tags: ["finance","market-regime","volatility-analysis"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "market regime financial analysis trends volatility"
---

# market-regime

## Purpose
This skill analyzes financial market regimes to detect trends, volatility, and shifts in asset classes like stocks, bonds, or cryptocurrencies. It processes historical data to classify regimes (e.g., bull, bear, sideways) and provides actionable insights for trading or risk management.

## When to Use
Use this skill when you need to evaluate market conditions for decision-making, such as before executing trades, assessing portfolio risk, or building predictive models. Apply it in volatile markets, during economic events, or for backtesting strategies. Avoid if you lack historical data access, as it requires at least 1 year of price data.

## Key Capabilities
- Identifies market regimes using statistical methods like moving averages and Bollinger Bands.
- Analyzes volatility with metrics such as standard deviation or VIX equivalents.
- Detects trend shifts by comparing short-term vs. long-term indicators.
- Supports multiple asset classes via APIs or data feeds (e.g., Yahoo Finance, Alpha Vantage).
- Outputs regime classifications, volatility scores, and regime duration forecasts.

## Usage Patterns
Invoke this skill via CLI for quick analysis or integrate it into Python scripts for automated workflows. Always provide asset symbols and time periods. For CLI, use synchronous calls; for API, handle asynchronous responses. Configure with a JSON file for custom parameters, e.g., set thresholds for volatility detection.

To run a basic analysis:
1. Set environment variable for authentication: `export OPENCLAW_API_KEY=your_api_key_here`.
2. Pass data sources via flags or config files.
3. Chain with other skills, like economic-indicators, for combined insights.

## Common Commands/API
Use the OpenClaw CLI or REST API for interactions. Authentication requires the `$OPENCLAW_API_KEY` environment variable.

- **CLI Command**: `openclaw market-regime analyze --asset AAPL --period 90d --metric volatility`
  - Flags: `--asset` (required, e.g., stock symbol), `--period` (e.g., "30d" for 30 days), `--metric` (e.g., "volatility" or "trend").
  - Output: JSON with regime type, volatility score, and key metrics.

- **API Endpoint**: POST to `https://api.openclaw.ai/v1/market-regime/analyze`
  - Request body: JSON like `{"asset": "BTC-USD", "period": "1y", "metrics": ["volatility", "trends"]}`
  - Response: 200 OK with JSON payload, e.g., `{"regime": "bull", "volatility": 0.15}`.
  - Headers: Include `Authorization: Bearer $OPENCLAW_API_KEY`.

Code snippet for Python integration:
```python
import requests
api_key = os.environ.get('OPENCLAW_API_KEY')
response = requests.post('https://api.openclaw.ai/v1/market-regime/analyze', 
                         headers={'Authorization': f'Bearer {api_key}'}, 
                         json={'asset': 'GOOGL', 'period': '180d'})
print(response.json()['regime'])  # Outputs e.g., 'bear'
```

Config format: Use a YAML file for advanced settings, e.g.,
```yaml
asset: SPY
period: 365d
metrics:
  - volatility
  - trends
thresholds:
  volatility_high: 0.2
```

## Integration Notes
Integrate with other OpenClaw skills by piping outputs or using shared data models. For example, combine with trading-strategies skill for automated alerts. Ensure data consistency by using standard formats like OHLCV (Open, High, Low, Close, Volume). If using external data, map it to the skill's expected schema (e.g., CSV with columns: date, open, high, low, close). Test integrations in a sandbox environment first. For web apps, use webhooks to receive regime updates.

## Error Handling
Handle errors by checking HTTP status codes or CLI exit codes. Common errors:
- 401 Unauthorized: Verify `$OPENCLAW_API_KEY` is set and valid.
- 400 Bad Request: Ensure JSON payload is correctly formatted (e.g., valid asset symbol).
- 429 Too Many Requests: Implement retry logic with exponential backoff.

In code, use try-except blocks:
```python
try:
    response = requests.post(...)  # As above
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"Error: {err.response.status_code} - {err.response.text}")
    # Retry or log the error
```

If data fetch fails (e.g., invalid period), the skill returns a specific error code; parse the response for details like "ERR_INVALID_PERIOD".

## Concrete Usage Examples
1. **Example 1: Analyze Stock Volatility**
   - Task: Check if Apple (AAPL) is in a high-volatility regime over the last 60 days.
   - Command: `openclaw market-regime analyze --asset AAPL --period 60d --metric volatility`
   - Expected Output: JSON like `{"regime": "high_volatility", "score": 0.25}`. Use this to trigger a sell alert in a trading bot.

2. **Example 2: Identify Crypto Trends**
   - Task: Detect trend shifts for Bitcoin (BTC-USD) over the past year.
   - API Call: POST to `/v1/market-regime/analyze` with body `{"asset": "BTC-USD", "period": "1y", "metrics": ["trends"]}`
   - Code Snippet:
     ```python
     response = requests.post(..., json={'asset': 'BTC-USD', 'period': '1y', 'metrics': ['trends']})
     trends = response.json()['trends']  # e.g., ['upward_shift_at_2023-06-01']
     ```
   - Use the output to update a dashboard or adjust investment allocations.

## Graph Relationships
- Related to: economic-indicators (depends on for macro data), trading-strategies (provides input for strategy decisions).
- Clusters with: financial (core cluster for this skill).
- Tags overlap: finance, volatility-analysis (shared with risk-assessment skills).
