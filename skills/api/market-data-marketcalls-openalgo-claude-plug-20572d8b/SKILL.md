---
name: market-data
description: Market data retrieval with OpenAlgo - real-time quotes, historical OHLCV, market depth, option chains, WebSocket streaming, and symbol search
---

# OpenAlgo Market Data

Access real-time and historical market data using OpenAlgo's unified Python SDK. Supports REST API for on-demand data and WebSocket for real-time streaming.

## Environment Setup

```python
from openalgo import api

# REST API only
client = api(
    api_key='your_api_key_here',
    host='http://127.0.0.1:5000'
)

# With WebSocket streaming
client = api(
    api_key='your_api_key_here',
    host='http://127.0.0.1:5000',
    ws_url='ws://127.0.0.1:8765',
    verbose=True  # Enable connection logs
)
```

## Quick Start Scripts

### Get Quotes
```bash
python scripts/quotes.py --symbol RELIANCE --exchange NSE
python scripts/quotes.py --symbols RELIANCE,TCS,INFY --exchange NSE
```

### Get Historical Data
```bash
python scripts/history.py --symbol SBIN --exchange NSE --interval 5m --start 2025-01-01 --end 2025-01-15
```

### Get Market Depth
```bash
python scripts/depth.py --symbol SBIN --exchange NSE
```

### Stream Live Data
```bash
python scripts/stream.py --symbols NIFTY,BANKNIFTY --exchange NSE_INDEX --mode ltp
```

---

## REST API Methods

### 1. Single Quote

Get current market quote for a symbol:

```python
response = client.quotes(symbol="RELIANCE", exchange="NSE")
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "open": 1172.0,
    "high": 1196.6,
    "low": 1163.3,
    "ltp": 1187.75,
    "ask": 1188.0,
    "bid": 1187.85,
    "prev_close": 1165.7,
    "volume": 14414545
  }
}
```

### 2. Multiple Quotes

Get quotes for multiple symbols in one call:

```python
response = client.multiquotes(symbols=[
    {"symbol": "RELIANCE", "exchange": "NSE"},
    {"symbol": "TCS", "exchange": "NSE"},
    {"symbol": "INFY", "exchange": "NSE"},
    {"symbol": "NIFTY", "exchange": "NSE_INDEX"}
])
```

**Response:**
```json
{
  "status": "success",
  "results": [
    {
      "symbol": "RELIANCE",
      "exchange": "NSE",
      "data": {
        "open": 1542.3,
        "high": 1571.6,
        "low": 1540.5,
        "ltp": 1569.9,
        "prev_close": 1539.7,
        "ask": 1569.9,
        "bid": 1569.8,
        "oi": 0,
        "volume": 14054299
      }
    },
    ...
  ]
}
```

### 3. Market Depth (Level 2)

Get order book with 5 best bid/ask levels:

```python
response = client.depth(symbol="SBIN", exchange="NSE")
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "open": 760.0,
    "high": 774.0,
    "low": 758.15,
    "ltp": 769.6,
    "ltq": 205,
    "prev_close": 746.9,
    "volume": 9362799,
    "oi": 161265750,
    "totalbuyqty": 591351,
    "totalsellqty": 835701,
    "asks": [
      {"price": 769.6, "quantity": 767},
      {"price": 769.65, "quantity": 115},
      {"price": 769.7, "quantity": 162},
      {"price": 769.75, "quantity": 1121},
      {"price": 769.8, "quantity": 430}
    ],
    "bids": [
      {"price": 769.4, "quantity": 886},
      {"price": 769.35, "quantity": 212},
      {"price": 769.3, "quantity": 351},
      {"price": 769.25, "quantity": 343},
      {"price": 769.2, "quantity": 399}
    ]
  }
}
```

### 4. Historical Data (OHLCV)

Get historical candlestick data:

```python
response = client.history(
    symbol="SBIN",
    exchange="NSE",
    interval="5m",
    start_date="2025-01-01",
    end_date="2025-01-15"
)
```

**Response (Pandas DataFrame):**
```
                            close    high     low    open  volume
timestamp
2025-01-01 09:15:00+05:30  772.50  774.00  763.20  766.50  318625
2025-01-01 09:20:00+05:30  773.20  774.95  772.10  772.45  197189
2025-01-01 09:25:00+05:30  775.15  775.60  772.60  773.20  227544
...
```

**Available Intervals:**
```python
response = client.intervals()
# Returns: {'minutes': ['1m', '3m', '5m', '10m', '15m', '30m'],
#           'hours': ['1h'], 'days': ['D']}
```

### 5. Option Chain

Get complete option chain for an underlying:

```python
chain = client.optionchain(
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    strike_count=10  # ±10 strikes from ATM (optional)
)
```

**Response:**
```json
{
  "status": "success",
  "underlying": "NIFTY",
  "underlying_ltp": 26215.55,
  "expiry_date": "30JAN25",
  "atm_strike": 26200.0,
  "chain": [
    {
      "strike": 26100.0,
      "ce": {
        "symbol": "NIFTY30JAN2526100CE",
        "label": "ITM2",
        "ltp": 490,
        "bid": 490,
        "ask": 491,
        "volume": 1195800,
        "oi": 5000000,
        "lotsize": 75
      },
      "pe": {
        "symbol": "NIFTY30JAN2526100PE",
        "label": "OTM2",
        "ltp": 193,
        "bid": 191.2,
        "ask": 193,
        "volume": 1832700,
        "oi": 4500000,
        "lotsize": 75
      }
    },
    ...
  ]
}
```

### 6. Expiry Dates

Get available expiry dates:

```python
response = client.expiry(
    symbol="NIFTY",
    exchange="NFO",
    instrumenttype="options"  # or "futures"
)
# Returns: ['30-JAN-25', '06-FEB-25', '13-FEB-25', ...]
```

---

## Symbol Search & Discovery

### Search Symbols

```python
response = client.search(query="NIFTY 26000 JAN CE", exchange="NFO")
```

**Response:**
```json
{
  "status": "success",
  "message": "Found 7 matching symbols",
  "data": [
    {
      "symbol": "NIFTY30JAN2526000CE",
      "exchange": "NFO",
      "expiry": "30-JAN-25",
      "strike": 26000,
      "instrumenttype": "CE",
      "lotsize": 75
    },
    ...
  ]
}
```

### Get Symbol Details

```python
response = client.symbol(symbol="NIFTY30JAN25FUT", exchange="NFO")
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "symbol": "NIFTY30JAN25FUT",
    "exchange": "NFO",
    "name": "NIFTY",
    "expiry": "30-JAN-25",
    "instrumenttype": "FUT",
    "lotsize": 75,
    "freeze_qty": 1800,
    "tick_size": 10
  }
}
```

### Get All Instruments

Download complete instrument list for an exchange:

```python
instruments = client.instruments(exchange="NSE")
# Returns Pandas DataFrame with all symbols
```

---

## WebSocket Streaming

### Connection Setup

```python
from openalgo import api
import time

client = api(
    api_key='your_api_key',
    host='http://127.0.0.1:5000',
    ws_url='ws://127.0.0.1:8765',
    verbose=True  # Show connection logs
)

# Connect to WebSocket
client.connect()
```

### Verbose Levels

| Level | Value | Description |
|-------|-------|-------------|
| Silent | `False` or `0` | Errors only (default) |
| Basic | `True` or `1` | Connection, auth, subscription logs |
| Debug | `2` | All market data updates |

### Stream LTP (Last Traded Price)

```python
instruments = [
    {"exchange": "NSE", "symbol": "RELIANCE"},
    {"exchange": "NSE", "symbol": "INFY"},
    {"exchange": "NSE_INDEX", "symbol": "NIFTY"}
]

def on_ltp(data):
    print(f"{data['symbol']}: {data['data']['ltp']}")

client.subscribe_ltp(instruments, on_data_received=on_ltp)

# Run for 60 seconds
time.sleep(60)

# Cleanup
client.unsubscribe_ltp(instruments)
client.disconnect()
```

### Stream Quotes (OHLC + Bid/Ask)

```python
def on_quote(data):
    d = data['data']
    print(f"{data['symbol']}: O={d['open']} H={d['high']} L={d['low']} LTP={d['ltp']}")

client.subscribe_quote(instruments, on_data_received=on_quote)
```

### Stream Market Depth

```python
def on_depth(data):
    d = data['data']
    print(f"{data['symbol']}: Best Bid={d['bids'][0]['price']} Best Ask={d['asks'][0]['price']}")

client.subscribe_depth(instruments, on_data_received=on_depth)
```

### Get Cached Data

Access latest cached data without callback:

```python
# After subscribing
ltp_data = client.get_ltp()
quote_data = client.get_quotes()
depth_data = client.get_depth()

# Access specific symbol
nifty_ltp = ltp_data['ltp']['NSE_INDEX']['NIFTY']['ltp']
```

---

## Market Information

### Trading Holidays

```python
response = client.holidays(year=2025)
```

**Response:**
```json
{
  "data": [
    {
      "date": "2025-01-26",
      "description": "Republic Day",
      "holiday_type": "TRADING_HOLIDAY",
      "closed_exchanges": ["NSE", "BSE", "NFO", "MCX"]
    },
    ...
  ]
}
```

### Exchange Timings

```python
response = client.timings(date="2025-01-15")
```

**Response:**
```json
{
  "data": [
    {"exchange": "NSE", "start_time": 1705293300000, "end_time": 1705315800000},
    {"exchange": "BSE", "start_time": 1705293300000, "end_time": 1705315800000},
    {"exchange": "MCX", "start_time": 1705293000000, "end_time": 1705346700000}
  ]
}
```

---

## Common Patterns

### Build a Watchlist

```python
watchlist = [
    {"symbol": "NIFTY", "exchange": "NSE_INDEX"},
    {"symbol": "BANKNIFTY", "exchange": "NSE_INDEX"},
    {"symbol": "RELIANCE", "exchange": "NSE"},
    {"symbol": "HDFCBANK", "exchange": "NSE"},
    {"symbol": "INFY", "exchange": "NSE"}
]

quotes = client.multiquotes(symbols=watchlist)

for item in quotes.get('results', []):
    data = item.get('data', {})
    change = ((data['ltp'] - data['prev_close']) / data['prev_close']) * 100
    print(f"{item['symbol']}: {data['ltp']} ({change:+.2f}%)")
```

### Fetch Intraday Data

```python
from datetime import date

today = date.today().strftime("%Y-%m-%d")

intraday = client.history(
    symbol="NIFTY",
    exchange="NSE_INDEX",
    interval="1m",
    start_date=today,
    end_date=today
)

print(f"Today's range: High={intraday['high'].max()}, Low={intraday['low'].min()}")
```

### Monitor Option Chain Changes

```python
import time

while True:
    chain = client.optionchain(
        underlying="NIFTY",
        exchange="NSE_INDEX",
        expiry_date="30JAN25",
        strike_count=5
    )

    atm = chain.get('atm_strike')
    print(f"\nNIFTY ATM: {atm}, LTP: {chain.get('underlying_ltp')}")

    for strike in chain.get('chain', []):
        if strike['strike'] == atm:
            ce = strike['ce']
            pe = strike['pe']
            print(f"  CE: {ce['ltp']} (Vol: {ce['volume']})")
            print(f"  PE: {pe['ltp']} (Vol: {pe['volume']})")

    time.sleep(5)
```

---

## Notes

- Use WebSocket for real-time data (lower latency, no rate limits)
- REST API is better for on-demand queries
- Historical data returns Pandas DataFrame for easy analysis
- Option chain includes OI, volume, bid/ask for all strikes
- Use `verbose=2` for debugging WebSocket issues
