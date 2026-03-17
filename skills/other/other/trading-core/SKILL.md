---
name: trading-core
description: Core trading operations with OpenAlgo - place orders, smart orders, basket orders, split orders, and order management across 25+ Indian brokers
---

# OpenAlgo Trading Core

Execute trading operations using OpenAlgo's unified Python SDK. Supports NSE, BSE, NFO, MCX, and currency derivatives with a single API across 25+ brokers.

## Environment Setup

The `OPENALGO_API_KEY` must be set. Get your API key from your OpenAlgo application.

```python
from openalgo import api

client = api(
    api_key='your_api_key_here',
    host='http://127.0.0.1:5000'  # Your OpenAlgo server
)
```

## Quick Start Scripts

### Place Market Order
```bash
python scripts/place_order.py --symbol RELIANCE --exchange NSE --action BUY --quantity 1 --product MIS
```

### Place Smart Order (Position-Aware)
```bash
python scripts/smart_order.py --symbol TATAMOTORS --exchange NSE --action SELL --quantity 5 --position-size 10
```

### Basket Order (Multiple Symbols)
```bash
python scripts/basket_order.py --orders '[{"symbol":"INFY","action":"BUY","quantity":1},{"symbol":"TCS","action":"BUY","quantity":1}]'
```

### Split Order (Large Quantities)
```bash
python scripts/split_order.py --symbol YESBANK --exchange NSE --action SELL --quantity 500 --split-size 100
```

---

## Order Constants

### Exchanges
| Code | Description |
|------|-------------|
| `NSE` | NSE Equity |
| `BSE` | BSE Equity |
| `NFO` | NSE Futures & Options |
| `BFO` | BSE Futures & Options |
| `CDS` | NSE Currency Derivatives |
| `BCD` | BSE Currency Derivatives |
| `MCX` | MCX Commodity |
| `NCDEX` | NCDEX Commodity |
| `NSE_INDEX` | NSE Indices (for quotes only) |
| `BSE_INDEX` | BSE Indices (for quotes only) |

### Product Types
| Code | Description | Use Case |
|------|-------------|----------|
| `CNC` | Cash & Carry | Equity delivery (hold overnight) |
| `NRML` | Normal | F&O positions (hold overnight) |
| `MIS` | Intraday | Auto square-off at market close |

### Price Types
| Code | Description |
|------|-------------|
| `MARKET` | Market Order (immediate execution) |
| `LIMIT` | Limit Order (specify price) |
| `SL` | Stop Loss Limit Order |
| `SL-M` | Stop Loss Market Order |

### Actions
| Code | Description |
|------|-------------|
| `BUY` | Buy order |
| `SELL` | Sell order |

---

## Core API Methods

### 1. Place Order

Place a single order with full control over parameters:

```python
response = client.placeorder(
    strategy="MyStrategy",
    symbol="RELIANCE",
    action="BUY",
    exchange="NSE",
    price_type="MARKET",
    product="MIS",
    quantity=1
)
# Response: {'orderid': '250408000989443', 'status': 'success'}
```

**Limit Order Example:**
```python
response = client.placeorder(
    strategy="MyStrategy",
    symbol="YESBANK",
    action="BUY",
    exchange="NSE",
    price_type="LIMIT",
    product="MIS",
    quantity=1,
    price=16.50,
    trigger_price=0,
    disclosed_quantity=0
)
```

**Stop Loss Order Example:**
```python
response = client.placeorder(
    strategy="MyStrategy",
    symbol="SBIN",
    action="SELL",
    exchange="NSE",
    price_type="SL",
    product="MIS",
    quantity=10,
    price=750,           # Limit price
    trigger_price=752    # Trigger price
)
```

### 2. Smart Order (Position-Aware)

Automatically adjusts order quantity based on current position:

```python
response = client.placesmartorder(
    strategy="SmartBot",
    symbol="TATAMOTORS",
    action="SELL",
    exchange="NSE",
    price_type="MARKET",
    product="MIS",
    quantity=1,
    position_size=5  # Desired final position
)
# If current position is 0, sells 5 to reach -5
# If current position is 3, sells 8 to reach -5
```

**Use Cases:**
- Rebalancing: Set `position_size` to target position
- Reversal: Set `action` opposite to current direction
- Scale-in/out: Adjust `quantity` dynamically

### 3. Basket Order

Execute multiple orders simultaneously:

```python
basket_orders = [
    {
        "symbol": "INFY",
        "exchange": "NSE",
        "action": "BUY",
        "quantity": 1,
        "pricetype": "MARKET",
        "product": "MIS"
    },
    {
        "symbol": "TCS",
        "exchange": "NSE",
        "action": "BUY",
        "quantity": 1,
        "pricetype": "MARKET",
        "product": "MIS"
    },
    {
        "symbol": "WIPRO",
        "exchange": "NSE",
        "action": "BUY",
        "quantity": 1,
        "pricetype": "MARKET",
        "product": "MIS"
    }
]

response = client.basketorder(orders=basket_orders)
# Response includes status for each order
```

### 4. Split Order

Break large orders into smaller chunks to avoid market impact:

```python
response = client.splitorder(
    symbol="YESBANK",
    exchange="NSE",
    action="SELL",
    quantity=500,
    splitsize=100,  # Each order will be max 100
    price_type="MARKET",
    product="MIS"
)
# Creates 5 orders of 100 each
```

**Response:**
```json
{
  "status": "success",
  "split_size": 100,
  "total_quantity": 500,
  "results": [
    {"order_num": 1, "orderid": "123", "quantity": 100, "status": "success"},
    {"order_num": 2, "orderid": "124", "quantity": 100, "status": "success"},
    ...
  ]
}
```

---

## Order Management

### Modify Order

```python
response = client.modifyorder(
    order_id="250408001002736",
    strategy="MyStrategy",
    symbol="YESBANK",
    action="BUY",
    exchange="NSE",
    price_type="LIMIT",
    product="MIS",
    quantity=1,
    price=17.00  # New price
)
```

### Cancel Order

```python
response = client.cancelorder(
    order_id="250408001002736",
    strategy="MyStrategy"
)
```

### Cancel All Orders

```python
response = client.cancelallorder(strategy="MyStrategy")
# Cancels all open and trigger-pending orders
```

### Close All Positions

```python
response = client.closeposition(strategy="MyStrategy")
# Squares off all open positions
```

### Get Order Status

```python
response = client.orderstatus(
    order_id="250408001002736",
    strategy="MyStrategy"
)
# Returns: order_status, average_price, quantity, timestamp
```

### Get Open Position

```python
response = client.openposition(
    strategy="MyStrategy",
    symbol="RELIANCE",
    exchange="NSE",
    product="MIS"
)
# Returns: {'quantity': '10', 'status': 'success'}
```

---

## Symbol Format

OpenAlgo uses standardized symbol formats across all brokers:

### Equity
- `RELIANCE`, `INFY`, `TCS`, `SBIN`

### Futures
- Format: `[SYMBOL][DDMMMYY]FUT`
- Examples: `NIFTY30JAN25FUT`, `BANKNIFTY30JAN25FUT`

### Options
- Format: `[SYMBOL][DDMMMYY][STRIKE][CE/PE]`
- Examples: `NIFTY30JAN2526000CE`, `BANKNIFTY30JAN2555000PE`

---

## Common Patterns

### Intraday Scalping
```python
# Entry
entry = client.placeorder(
    strategy="Scalper",
    symbol="SBIN",
    action="BUY",
    exchange="NSE",
    price_type="MARKET",
    product="MIS",
    quantity=100
)

# Exit with profit target (use limit order)
exit_order = client.placeorder(
    strategy="Scalper",
    symbol="SBIN",
    action="SELL",
    exchange="NSE",
    price_type="LIMIT",
    product="MIS",
    quantity=100,
    price=current_price * 1.005  # 0.5% profit
)
```

### Swing Trading Entry
```python
response = client.placeorder(
    strategy="SwingTrader",
    symbol="TATASTEEL",
    action="BUY",
    exchange="NSE",
    price_type="LIMIT",
    product="CNC",  # Delivery
    quantity=10,
    price=150.00
)
```

### Risk Management - Stop Loss
```python
# Place stop loss immediately after entry
sl_order = client.placeorder(
    strategy="Scalper",
    symbol="SBIN",
    action="SELL",
    exchange="NSE",
    price_type="SL-M",
    product="MIS",
    quantity=100,
    trigger_price=entry_price * 0.995  # 0.5% stop loss
)
```

---

## Error Handling

```python
response = client.placeorder(...)

if response.get('status') == 'success':
    print(f"Order placed: {response['orderid']}")
else:
    print(f"Error: {response.get('message', 'Unknown error')}")
```

## Notes

- Always verify `OPENALGO_API_KEY` is set before trading
- Use `MIS` for intraday, `CNC`/`NRML` for positional trades
- Test with small quantities first
- Use Analyzer mode for paper trading: `client.analyzertoggle(mode=True)`
