---
name: alpaca-api
cluster: financial
description: "Interact with Alpaca\'s API for stock trading and market data retrieval."
tags: ["finance","api","stock-trading","alpaca"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "alpaca api finance trading stocks market data"
---

# alpaca-api

## Purpose
This skill allows the AI to interact with Alpaca's API for executing stock trades, retrieving market data, and managing accounts, using HTTP requests to Alpaca's endpoints.

## When to Use
Use this skill for tasks involving real-time financial data, such as fetching stock prices, placing buy/sell orders, or checking account balances in a trading bot or financial analysis workflow. Avoid it for non-financial tasks or when real-time data isn't needed.

## Key Capabilities
- Fetch market data via GET requests to endpoints like /v2/stocks/{symbol}/quotes for real-time quotes.
- Place orders using POST /v2/orders with JSON payloads for buy/sell actions.
- Retrieve account details via GET /v2/account, including cash balance and positions.
- Support for paper trading mode by setting the API base URL to https://paper-api.alpaca.markets.
- Handle WebSocket connections for live market updates, e.g., subscribing to trades on wss://stream.data.alpaca.markets/v2.

## Usage Patterns
Always initialize requests with authentication headers using $ALPACA_API_KEY and $ALPACA_SECRET_KEY as environment variables. For example, set headers like {'APCA-API-KEY-ID': os.environ['ALPACA_API_KEY'], 'APCA-API-SECRET-KEY': os.environ['ALPACA_SECRET_KEY']}. Use GET for data retrieval and POST for actions like trading. Rate limit requests to avoid API throttling (Alpaca's limit is 200 requests per minute per IP). Test in paper trading mode first by switching the base URL.

## Common Commands/API
- GET /v2/stocks/{symbol}/bars: Fetch historical bars; include query params like ?timeframe=1Min&limit=100. Example: requests.get('https://api.alpaca.markets/v2/stocks/AAPL/bars?timeframe=1Day', headers=auth_headers).
- POST /v2/orders: Place an order; send JSON body like {"symbol": "AAPL", "qty": 10, "side": "buy", "type": "market", "time_in_force": "day"}. Code snippet:
  ```
  import requests
  response = requests.post('https://api.alpaca.markets/v2/orders', json=order_data, headers=auth_headers)
  print(response.json())
  ```
- GET /v2/account: Get account info; no body needed. Use with auth headers.
- DELETE /v2/orders/{order_id}: Cancel an order; include the order ID in the URL path.
- WebSocket for real-time: Connect to wss://stream.data.alpaca.markets/v2 and send {"action": "authenticate", "key": $ALPACA_API_KEY, "secret": $ALPACA_SECRET_KEY}.

## Integration Notes
Store API keys in environment variables like export ALPACA_API_KEY='your_key' and export ALPACA_SECRET_KEY='your_secret'. Use a library like requests in Python for HTTP interactions. For production, handle base URL differences: use https://api.alpaca.markets for live and https://paper-api.alpaca.markets for testing. Integrate with other skills by piping data, e.g., fetch data from this skill and pass to a 'data-analysis' skill. Config format: Use a .env file with ALPACA_API_KEY=xxx and ALPACA_SECRET_KEY=yyy, then load with python-dotenv.

## Error Handling
Check HTTP status codes: 401 for auth errors (retry after verifying $ALPACA_API_KEY), 429 for rate limits (wait and retry with exponential backoff), 404 for invalid endpoints (log and abort). Parse JSON responses for Alpaca-specific errors, e.g., if "code" == "invalid_symbol", suggest checking the stock symbol. Implement try-except blocks around requests, like:
```
try:
    response = requests.get(url, headers=auth_headers)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"Error: {err.response.status_code} - {err.response.text}")
```
Log all errors with timestamps and retry transient errors up to 3 times.

## Concrete Usage Examples
1. Fetch real-time quote for AAPL: Use GET /v2/stocks/AAPL/quote with auth headers, then extract price from the response JSON. Code: requests.get('https://api.alpaca.markets/v2/stocks/AAPL/quote', headers=auth_headers).json()['ask_price'].
2. Place a market buy order for 5 shares of TSLA: Send POST /v2/orders with body {"symbol": "TSLA", "qty": 5, "side": "buy", "type": "market"}. Verify with GET /v2/orders to check status.

## Graph Relationships
- Related to cluster: financial (e.g., connects with other financial tools like 'stock-analysis').
- Tagged with: finance, api, stock-trading, alpaca (links to skills in api cluster for broader integrations).
