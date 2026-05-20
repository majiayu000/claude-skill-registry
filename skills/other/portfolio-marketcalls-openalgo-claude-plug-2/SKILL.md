---
name: portfolio
description: Portfolio management with OpenAlgo - funds, positions, holdings, order book, trade book, margin calculator, and account management
---

# OpenAlgo Portfolio Management

Manage your trading portfolio using OpenAlgo's unified Python SDK. Access funds, positions, holdings, orders, trades, and margin information.

## Environment Setup

```python
from openalgo import api

client = api(
    api_key='your_api_key_here',
    host='http://127.0.0.1:5000'
)
```

## Quick Start Scripts

### Portfolio Summary
```bash
python scripts/portfolio.py --summary
```

### View Positions
```bash
python scripts/portfolio.py --positions
```

### View Holdings
```bash
python scripts/portfolio.py --holdings
```

### Calculate Margin
```bash
python scripts/margin.py --symbol NIFTY30JAN2526000CE --exchange NFO --action SELL --quantity 75
```

---

## Core API Methods

### 1. Funds

Get account balance and margin information:

```python
response = client.funds()
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "availablecash": "320.66",
    "collateral": "0.00",
    "m2mrealized": "3.27",
    "m2munrealized": "-7.88",
    "utiliseddebits": "679.34"
  }
}
```

**Fields Explained:**
- `availablecash`: Cash available for new trades
- `collateral`: Pledged collateral value
- `m2mrealized`: Realized Mark-to-Market P&L
- `m2munrealized`: Unrealized Mark-to-Market P&L
- `utiliseddebits`: Margin utilized for open positions

### 2. Position Book

Get all open positions:

```python
response = client.positionbook()
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "symbol": "RELIANCE",
      "exchange": "NSE",
      "product": "MIS",
      "quantity": "10",
      "average_price": "1180.50",
      "ltp": "1189.90",
      "pnl": "94.00"
    },
    {
      "symbol": "SBIN",
      "exchange": "NSE",
      "product": "MIS",
      "quantity": "-5",
      "average_price": "770.20",
      "ltp": "769.80",
      "pnl": "2.00"
    }
  ]
}
```

**Notes:**
- Positive quantity = Long position
- Negative quantity = Short position
- P&L is calculated as (LTP - Avg Price) * Quantity

### 3. Holdings

Get delivery holdings (CNC):

```python
response = client.holdings()
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "holdings": [
      {
        "symbol": "RELIANCE",
        "exchange": "NSE",
        "product": "CNC",
        "quantity": 10,
        "pnl": -149.0,
        "pnlpercent": -11.1
      },
      {
        "symbol": "TATASTEEL",
        "exchange": "NSE",
        "product": "CNC",
        "quantity": 5,
        "pnl": -15.0,
        "pnlpercent": -10.41
      }
    ],
    "statistics": {
      "totalholdingvalue": 17680.0,
      "totalinvvalue": 20010.0,
      "totalprofitandloss": -2330.0,
      "totalpnlpercentage": -11.65
    }
  }
}
```

### 4. Order Book

Get all orders for the day:

```python
response = client.orderbook()
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "orders": [
      {
        "action": "BUY",
        "symbol": "RELIANCE",
        "exchange": "NSE",
        "orderid": "250408000989443",
        "product": "MIS",
        "quantity": "1",
        "price": 1186.0,
        "pricetype": "MARKET",
        "order_status": "complete",
        "trigger_price": 0.0,
        "timestamp": "08-Apr-2025 13:58:03"
      },
      {
        "action": "BUY",
        "symbol": "YESBANK",
        "exchange": "NSE",
        "orderid": "250408001002736",
        "product": "MIS",
        "quantity": "1",
        "price": 16.5,
        "pricetype": "LIMIT",
        "order_status": "open",
        "trigger_price": 0.0,
        "timestamp": "08-Apr-2025 14:13:45"
      }
    ],
    "statistics": {
      "total_buy_orders": 2.0,
      "total_sell_orders": 0.0,
      "total_completed_orders": 1.0,
      "total_open_orders": 1.0,
      "total_rejected_orders": 0.0
    }
  }
}
```

**Order Statuses:**
- `complete`: Order executed
- `open`: Order pending
- `cancelled`: Order cancelled
- `rejected`: Order rejected
- `trigger_pending`: SL/SL-M waiting for trigger

### 5. Trade Book

Get all executed trades:

```python
response = client.tradebook()
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "action": "BUY",
      "symbol": "RELIANCE",
      "exchange": "NSE",
      "orderid": "250408000989443",
      "product": "MIS",
      "quantity": 1,
      "average_price": 1180.1,
      "timestamp": "13:58:03",
      "trade_value": 1180.1
    }
  ]
}
```

### 6. Order Status

Get status of a specific order:

```python
response = client.orderstatus(
    order_id="250408000989443",
    strategy="MyStrategy"
)
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "action": "BUY",
    "average_price": 1180.1,
    "exchange": "NSE",
    "order_status": "complete",
    "orderid": "250408000989443",
    "price": 0,
    "pricetype": "MARKET",
    "product": "MIS",
    "quantity": "1",
    "symbol": "RELIANCE",
    "timestamp": "08-Apr-2025 13:58:03",
    "trigger_price": 0
  }
}
```

### 7. Open Position

Get position for a specific symbol:

```python
response = client.openposition(
    strategy="MyStrategy",
    symbol="RELIANCE",
    exchange="NSE",
    product="MIS"
)
```

**Response:**
```json
{
  "status": "success",
  "quantity": "10"
}
```

---

## Margin Calculator

### Single Position Margin

```python
response = client.margin(positions=[
    {
        "symbol": "NIFTY30JAN2526000CE",
        "exchange": "NFO",
        "action": "SELL",
        "product": "NRML",
        "pricetype": "MARKET",
        "quantity": "75"
    }
])
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_margin_required": 125000.00,
    "span_margin": 95000.00,
    "exposure_margin": 30000.00
  }
}
```

### Multi-Leg Margin (Spread Benefit)

```python
response = client.margin(positions=[
    {
        "symbol": "NIFTY30JAN2526000CE",
        "exchange": "NFO",
        "action": "BUY",
        "product": "NRML",
        "pricetype": "MARKET",
        "quantity": "75"
    },
    {
        "symbol": "NIFTY30JAN2526500CE",
        "exchange": "NFO",
        "action": "SELL",
        "product": "NRML",
        "pricetype": "MARKET",
        "quantity": "75"
    }
])
# Spread margin will be lower than naked option margin
```

---

## Account Actions

### Close All Positions

Square off all open positions:

```python
response = client.closeposition(strategy="MyStrategy")
```

**Response:**
```json
{
  "status": "success",
  "message": "All Open Positions Squared Off"
}
```

### Cancel All Orders

Cancel all pending orders:

```python
response = client.cancelallorder(strategy="MyStrategy")
```

**Response:**
```json
{
  "status": "success",
  "message": "Canceled 5 orders. Failed to cancel 0 orders.",
  "canceled_orders": ["250408001042620", "250408001042667"],
  "failed_cancellations": []
}
```

---

## Analyzer Mode

Test strategies without real execution:

### Check Analyzer Status

```python
response = client.analyzerstatus()
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "analyze_mode": true,
    "mode": "analyze",
    "total_logs": 25
  }
}
```

### Toggle Analyzer Mode

```python
# Enable paper trading
response = client.analyzertoggle(mode=True)

# Disable paper trading (live mode)
response = client.analyzertoggle(mode=False)
```

---

## Telegram Alerts

Send trading notifications:

```python
response = client.telegram(
    username="your_openalgo_username",
    message="NIFTY crossed 26000! Entry triggered."
)
```

**Response:**
```json
{
  "status": "success",
  "message": "Notification sent successfully"
}
```

---

## Common Patterns

### Daily P&L Summary

```python
def get_daily_pnl():
    """Calculate total daily P&L from positions."""
    positions = client.positionbook()

    if positions.get('status') != 'success':
        return None

    total_pnl = 0
    for pos in positions.get('data', []):
        total_pnl += float(pos.get('pnl', 0))

    return total_pnl

pnl = get_daily_pnl()
print(f"Today's P&L: ₹{pnl:,.2f}")
```

### Check Available Margin

```python
def check_margin_available():
    """Check if sufficient margin is available."""
    funds = client.funds()

    if funds.get('status') != 'success':
        return 0

    return float(funds['data'].get('availablecash', 0))

available = check_margin_available()
print(f"Available Margin: ₹{available:,.2f}")
```

### Risk Management - Position Limits

```python
def check_position_limit(symbol, exchange, product, max_quantity):
    """Check if position is within limits."""
    position = client.openposition(
        strategy="RiskManager",
        symbol=symbol,
        exchange=exchange,
        product=product
    )

    if position.get('status') != 'success':
        return True  # Allow if can't check

    current_qty = abs(int(position.get('quantity', 0)))

    if current_qty >= max_quantity:
        print(f"Position limit reached for {symbol}: {current_qty}/{max_quantity}")
        return False

    return True

# Usage
if check_position_limit("NIFTY30JAN25FUT", "NFO", "NRML", 500):
    # Place order
    pass
```

### End of Day Square Off

```python
from datetime import datetime

def eod_squareoff():
    """Square off all MIS positions before market close."""
    now = datetime.now()

    # Check if it's near market close (3:15 PM)
    if now.hour == 15 and now.minute >= 10:
        response = client.closeposition(strategy="EOD_Squareoff")
        print(f"EOD Square off: {response}")
        return response

    return None
```

### Portfolio Snapshot

```python
def portfolio_snapshot():
    """Get complete portfolio snapshot."""
    funds = client.funds()
    positions = client.positionbook()
    holdings = client.holdings()
    orders = client.orderbook()

    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'funds': funds.get('data', {}),
        'positions': positions.get('data', []),
        'holdings': holdings.get('data', {}),
        'orders': orders.get('data', {})
    }

    return snapshot

snapshot = portfolio_snapshot()
print(f"Available: ₹{snapshot['funds'].get('availablecash', 0)}")
print(f"Open Positions: {len(snapshot['positions'])}")
print(f"Holdings: {len(snapshot['holdings'].get('holdings', []))}")
```

---

## Market Information

### Trading Holidays

```python
response = client.holidays(year=2025)

for holiday in response.get('data', []):
    print(f"{holiday['date']}: {holiday['description']}")
```

### Exchange Timings

```python
response = client.timings(date="2025-01-15")

for timing in response.get('data', []):
    exchange = timing['exchange']
    start = datetime.fromtimestamp(timing['start_time'] / 1000)
    end = datetime.fromtimestamp(timing['end_time'] / 1000)
    print(f"{exchange}: {start.strftime('%H:%M')} - {end.strftime('%H:%M')}")
```

---

## Notes

- Always check funds before placing large orders
- Use Analyzer mode for testing strategies
- Monitor positions regularly for risk management
- Set up Telegram alerts for important events
- Position book updates in real-time during market hours
- Holdings update T+1 after delivery trades
