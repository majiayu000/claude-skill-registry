---
name: options-trading
description: Options trading with OpenAlgo - single leg orders, multi-leg strategies (Iron Condor, Straddle, Strangle, Spreads), options chain analysis, and Greeks calculation
---

# OpenAlgo Options Trading

Execute options trading strategies using OpenAlgo's unified Python SDK. Supports index options (NIFTY, BANKNIFTY, FINNIFTY), stock options, and complex multi-leg strategies.

## Environment Setup

```python
from openalgo import api

client = api(
    api_key='your_api_key_here',
    host='http://127.0.0.1:5000'
)
```

## Quick Start Scripts

### Single Leg Options Order
```bash
python scripts/options_order.py --underlying NIFTY --expiry 30JAN25 --offset ATM --option-type CE --action BUY --quantity 75
```

### Iron Condor Strategy
```bash
python scripts/iron_condor.py --underlying NIFTY --expiry 30JAN25 --quantity 75
```

### Straddle Strategy
```bash
python scripts/straddle.py --underlying BANKNIFTY --expiry 30JAN25 --action BUY --quantity 30
```

---

## Options Symbol Format

OpenAlgo uses standardized symbol formats:

| Type | Format | Example |
|------|--------|---------|
| Index Options | `[INDEX][DDMMMYY][STRIKE][CE/PE]` | `NIFTY30JAN2526000CE` |
| Stock Options | `[SYMBOL][DDMMMYY][STRIKE][CE/PE]` | `RELIANCE30JAN251400CE` |
| Index Futures | `[INDEX][DDMMMYY]FUT` | `NIFTY30JAN25FUT` |

## Offset System

OpenAlgo uses an intuitive offset system to select strikes relative to ATM:

| Offset | Meaning | Example (NIFTY ATM=26000) |
|--------|---------|---------------------------|
| `ATM` | At The Money | 26000 |
| `ITM1` | 1 strike In The Money | CE: 25950, PE: 26050 |
| `ITM2` | 2 strikes In The Money | CE: 25900, PE: 26100 |
| `OTM1` | 1 strike Out of The Money | CE: 26050, PE: 25950 |
| `OTM2` | 2 strikes Out of The Money | CE: 26100, PE: 25900 |
| `OTM5` | 5 strikes Out of The Money | CE: 26250, PE: 25750 |

---

## Core API Methods

### 1. Single Leg Options Order

Place ATM, ITM, or OTM options orders:

```python
# ATM Call Option
response = client.optionsorder(
    strategy="OptionsBot",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    offset="ATM",
    option_type="CE",
    action="BUY",
    quantity=75,
    pricetype="MARKET",
    product="NRML",
    splitsize=0  # 0 = no splitting
)
```

**Response:**
```json
{
  "exchange": "NFO",
  "offset": "ATM",
  "option_type": "CE",
  "orderid": "25013000000001",
  "status": "success",
  "symbol": "NIFTY30JAN2526000CE",
  "underlying": "NIFTY30JAN25FUT",
  "underlying_ltp": 26015.50
}
```

**ITM Put Option:**
```python
response = client.optionsorder(
    strategy="OptionsBot",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    offset="ITM3",  # 3 strikes ITM
    option_type="PE",
    action="BUY",
    quantity=75,
    pricetype="MARKET",
    product="NRML"
)
```

**OTM Call Option:**
```python
response = client.optionsorder(
    strategy="OptionsBot",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    offset="OTM5",  # 5 strikes OTM
    option_type="CE",
    action="SELL",
    quantity=75,
    pricetype="MARKET",
    product="NRML"
)
```

### 2. Multi-Leg Options Order

Execute complex strategies with multiple legs in a single call:

#### Iron Condor (4 legs)
```python
response = client.optionsmultiorder(
    strategy="Iron Condor",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    legs=[
        {"offset": "OTM6", "option_type": "CE", "action": "BUY", "quantity": 75},
        {"offset": "OTM6", "option_type": "PE", "action": "BUY", "quantity": 75},
        {"offset": "OTM4", "option_type": "CE", "action": "SELL", "quantity": 75},
        {"offset": "OTM4", "option_type": "PE", "action": "SELL", "quantity": 75}
    ]
)
```

**Response:**
```json
{
  "status": "success",
  "underlying": "NIFTY",
  "underlying_ltp": 26050.45,
  "results": [
    {"leg": 1, "action": "BUY", "offset": "OTM6", "option_type": "CE", "symbol": "NIFTY30JAN2526350CE", "orderid": "123", "status": "success"},
    {"leg": 2, "action": "BUY", "offset": "OTM6", "option_type": "PE", "symbol": "NIFTY30JAN2525750PE", "orderid": "124", "status": "success"},
    {"leg": 3, "action": "SELL", "offset": "OTM4", "option_type": "CE", "symbol": "NIFTY30JAN2526250CE", "orderid": "125", "status": "success"},
    {"leg": 4, "action": "SELL", "offset": "OTM4", "option_type": "PE", "symbol": "NIFTY30JAN2525850PE", "orderid": "126", "status": "success"}
  ]
}
```

#### Bull Call Spread (2 legs)
```python
response = client.optionsmultiorder(
    strategy="Bull Call Spread",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    legs=[
        {"offset": "ATM", "option_type": "CE", "action": "BUY", "quantity": 75},
        {"offset": "OTM2", "option_type": "CE", "action": "SELL", "quantity": 75}
    ]
)
```

#### Bear Put Spread (2 legs)
```python
response = client.optionsmultiorder(
    strategy="Bear Put Spread",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    legs=[
        {"offset": "ATM", "option_type": "PE", "action": "BUY", "quantity": 75},
        {"offset": "OTM2", "option_type": "PE", "action": "SELL", "quantity": 75}
    ]
)
```

#### Straddle (2 legs)
```python
response = client.optionsmultiorder(
    strategy="Long Straddle",
    underlying="BANKNIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    legs=[
        {"offset": "ATM", "option_type": "CE", "action": "BUY", "quantity": 30},
        {"offset": "ATM", "option_type": "PE", "action": "BUY", "quantity": 30}
    ]
)
```

#### Strangle (2 legs)
```python
response = client.optionsmultiorder(
    strategy="Short Strangle",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    legs=[
        {"offset": "OTM3", "option_type": "CE", "action": "SELL", "quantity": 75},
        {"offset": "OTM3", "option_type": "PE", "action": "SELL", "quantity": 75}
    ]
)
```

#### Diagonal Spread (Different Expiries)
```python
response = client.optionsmultiorder(
    strategy="Diagonal Spread",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    legs=[
        {"offset": "ITM2", "option_type": "CE", "action": "BUY", "quantity": 75, "expiry_date": "27FEB25"},
        {"offset": "OTM2", "option_type": "CE", "action": "SELL", "quantity": 75, "expiry_date": "30JAN25"}
    ]
)
```

#### Calendar Spread (Same Strike, Different Expiries)
```python
response = client.optionsmultiorder(
    strategy="Calendar Spread",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    legs=[
        {"offset": "ATM", "option_type": "CE", "action": "BUY", "quantity": 75, "expiry_date": "27FEB25"},
        {"offset": "ATM", "option_type": "CE", "action": "SELL", "quantity": 75, "expiry_date": "30JAN25"}
    ]
)
```

---

## Options Analysis

### Get Option Symbol
Find the exact symbol for a given strike:

```python
response = client.optionsymbol(
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    offset="ATM",
    option_type="CE"
)
# Response: {'symbol': 'NIFTY30JAN2526000CE', 'exchange': 'NFO', 'lotsize': 75, ...}
```

### Get Option Chain
Retrieve the full option chain for analysis:

```python
chain = client.optionchain(
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    strike_count=10  # ±10 strikes from ATM
)
```

**Response includes for each strike:**
```json
{
  "strike": 26000.0,
  "ce": {
    "symbol": "NIFTY30JAN2526000CE",
    "label": "ATM",
    "ltp": 250.50,
    "bid": 250.00,
    "ask": 251.00,
    "volume": 1500000,
    "oi": 5000000,
    "lotsize": 75
  },
  "pe": {
    "symbol": "NIFTY30JAN2526000PE",
    "label": "ATM",
    "ltp": 245.00,
    "bid": 244.50,
    "ask": 245.50,
    "volume": 1200000,
    "oi": 4500000,
    "lotsize": 75
  }
}
```

### Calculate Option Greeks
Get Delta, Gamma, Theta, Vega, Rho for any option:

```python
greeks = client.optiongreeks(
    symbol="NIFTY30JAN2526000CE",
    exchange="NFO",
    interest_rate=0.00,
    underlying_symbol="NIFTY",
    underlying_exchange="NSE_INDEX"
)
```

**Response:**
```json
{
  "status": "success",
  "symbol": "NIFTY30JAN2526000CE",
  "option_type": "CE",
  "strike": 26000.0,
  "spot_price": 25966.05,
  "option_price": 250,
  "days_to_expiry": 28.5,
  "implied_volatility": 15.6,
  "greeks": {
    "delta": 0.4967,
    "gamma": 0.000352,
    "theta": -7.919,
    "vega": 28.9489,
    "rho": 9.733994
  }
}
```

### Calculate Synthetic Future Price

```python
synthetic = client.syntheticfuture(
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25"
)
# Response: {'synthetic_future_price': 26050.05, 'atm_strike': 26000.0, ...}
```

### Get Expiry Dates

```python
expiries = client.expiry(
    symbol="NIFTY",
    exchange="NFO",
    instrumenttype="options"
)
# Returns list of expiry dates: ['30-JAN-25', '06-FEB-25', '13-FEB-25', ...]
```

---

## Common Index Details

| Index | Exchange | Lot Size | Strike Gap |
|-------|----------|----------|------------|
| NIFTY | NSE_INDEX | 75 | 50 |
| BANKNIFTY | NSE_INDEX | 30 | 100 |
| FINNIFTY | NSE_INDEX | 65 | 50 |
| MIDCPNIFTY | NSE_INDEX | 50 | 25 |
| SENSEX | BSE_INDEX | 20 | 100 |
| BANKEX | BSE_INDEX | 30 | 100 |

---

## Strategy Patterns

### Weekly Options Selling (Theta Decay)
```python
# Short Strangle - Sell OTM options to collect premium
response = client.optionsmultiorder(
    strategy="Weekly Strangle",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",  # Weekly expiry
    legs=[
        {"offset": "OTM5", "option_type": "CE", "action": "SELL", "quantity": 75},
        {"offset": "OTM5", "option_type": "PE", "action": "SELL", "quantity": 75}
    ]
)
```

### Directional Play with Protection
```python
# Bull Call Spread - Limited risk bullish bet
response = client.optionsmultiorder(
    strategy="Bullish Spread",
    underlying="BANKNIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    legs=[
        {"offset": "ATM", "option_type": "CE", "action": "BUY", "quantity": 30},
        {"offset": "OTM3", "option_type": "CE", "action": "SELL", "quantity": 30}
    ]
)
```

### Event Day Volatility Play
```python
# Long Straddle before results/events
response = client.optionsmultiorder(
    strategy="Event Straddle",
    underlying="RELIANCE",
    exchange="NSE",
    expiry_date="30JAN25",
    legs=[
        {"offset": "ATM", "option_type": "CE", "action": "BUY", "quantity": 250},
        {"offset": "ATM", "option_type": "PE", "action": "BUY", "quantity": 250}
    ]
)
```

### Butterfly Spread (Low Capital)
```python
response = client.optionsmultiorder(
    strategy="Long Butterfly",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="30JAN25",
    legs=[
        {"offset": "ITM2", "option_type": "CE", "action": "BUY", "quantity": 75},
        {"offset": "ATM", "option_type": "CE", "action": "SELL", "quantity": 150},
        {"offset": "OTM2", "option_type": "CE", "action": "BUY", "quantity": 75}
    ]
)
```

---

## Margin Calculation

Calculate required margin before placing orders:

```python
margin = client.margin(positions=[
    {
        "symbol": "NIFTY30JAN2526000CE",
        "exchange": "NFO",
        "action": "SELL",
        "product": "NRML",
        "pricetype": "MARKET",
        "quantity": "75"
    },
    {
        "symbol": "NIFTY30JAN2525000CE",
        "exchange": "NFO",
        "action": "BUY",
        "product": "NRML",
        "pricetype": "MARKET",
        "quantity": "75"
    }
])

print(f"Total Margin Required: {margin['data']['total_margin_required']}")
print(f"SPAN Margin: {margin['data']['span_margin']}")
print(f"Exposure Margin: {margin['data']['exposure_margin']}")
```

---

## Notes

- Always check available margin before placing option sell orders
- Use `splitsize` parameter for large orders to avoid freeze quantity limits
- Weekly options expire on Thursday, monthly on last Thursday
- NIFTY lot size is 75, BANKNIFTY is 30
- Use Analyzer mode for paper trading: `client.analyzertoggle(mode=True)`
