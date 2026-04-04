---
name: visualization
description: Data visualization with OpenAlgo - candlestick charts, options payoff diagrams, P&L dashboards, and real-time Streamlit dashboards
---

# OpenAlgo Visualization

Create trading charts, dashboards, and visualizations using OpenAlgo data. Build interactive Streamlit dashboards for real-time monitoring.

## Environment Setup

```python
from openalgo import api
import pandas as pd
import plotly.graph_objects as go

client = api(
    api_key='your_api_key_here',
    host='http://127.0.0.1:5000'
)
```

## Quick Start Scripts

### Candlestick Chart
```bash
python scripts/candlestick.py --symbol SBIN --exchange NSE --interval 5m --days 5
```

### Options Payoff Diagram
```bash
python scripts/payoff.py --strategy "iron_condor" --underlying NIFTY --expiry 30JAN25
```

### P&L Dashboard
```bash
streamlit run scripts/pnl_dashboard.py
```

---

## Candlestick Charts

### Basic Candlestick with Plotly

```python
from openalgo import api
import plotly.graph_objects as go

client = api(api_key='your_key', host='http://127.0.0.1:5000')

# Fetch historical data
df = client.history(
    symbol="SBIN",
    exchange="NSE",
    interval="5m",
    start_date="2025-01-01",
    end_date="2025-01-10"
)

# Create candlestick chart
fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='SBIN'
)])

fig.update_layout(
    title='SBIN 5-Minute Chart',
    yaxis_title='Price',
    xaxis_title='Time',
    xaxis_rangeslider_visible=False
)

fig.show()
```

### Candlestick with Volume

```python
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.03,
                    row_heights=[0.7, 0.3])

# Candlestick
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='Price'
), row=1, col=1)

# Volume bars
colors = ['green' if c >= o else 'red' for c, o in zip(df['close'], df['open'])]
fig.add_trace(go.Bar(
    x=df.index,
    y=df['volume'],
    marker_color=colors,
    name='Volume'
), row=2, col=1)

fig.update_layout(
    title='SBIN Chart with Volume',
    xaxis_rangeslider_visible=False
)

fig.show()
```

### Moving Averages

```python
# Calculate MAs
df['SMA_20'] = df['close'].rolling(window=20).mean()
df['SMA_50'] = df['close'].rolling(window=50).mean()
df['EMA_9'] = df['close'].ewm(span=9, adjust=False).mean()

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['open'], high=df['high'],
    low=df['low'], close=df['close'],
    name='Price'
))

fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50', line=dict(color='orange')))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA_9'], name='EMA 9', line=dict(color='purple')))

fig.show()
```

---

## Options Payoff Diagrams

### Long Call Payoff

```python
import numpy as np
import plotly.graph_objects as go

def long_call_payoff(spot_range, strike, premium):
    """Calculate long call payoff."""
    return np.maximum(spot_range - strike, 0) - premium

# Parameters
strike = 26000
premium = 250
spot_range = np.arange(25000, 27000, 50)

payoff = long_call_payoff(spot_range, strike, premium)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=spot_range,
    y=payoff,
    mode='lines',
    name='Long Call',
    line=dict(color='green', width=2)
))

fig.add_hline(y=0, line_dash="dash", line_color="gray")
fig.add_vline(x=strike, line_dash="dash", line_color="blue", annotation_text="Strike")

fig.update_layout(
    title=f'Long Call Payoff (Strike: {strike}, Premium: {premium})',
    xaxis_title='Spot Price',
    yaxis_title='Profit/Loss'
)

fig.show()
```

### Iron Condor Payoff

```python
def iron_condor_payoff(spot_range, pe_buy, pe_sell, ce_sell, ce_buy,
                       pe_buy_prem, pe_sell_prem, ce_sell_prem, ce_buy_prem):
    """Calculate Iron Condor payoff."""
    # Long PE (far OTM)
    long_pe = np.maximum(pe_buy - spot_range, 0) - pe_buy_prem
    # Short PE (near OTM)
    short_pe = pe_sell_prem - np.maximum(pe_sell - spot_range, 0)
    # Short CE (near OTM)
    short_ce = ce_sell_prem - np.maximum(spot_range - ce_sell, 0)
    # Long CE (far OTM)
    long_ce = np.maximum(spot_range - ce_buy, 0) - ce_buy_prem

    return long_pe + short_pe + short_ce + long_ce

# Iron Condor parameters
spot_range = np.arange(25000, 27000, 25)
pe_buy, pe_sell = 25500, 25750    # Put strikes
ce_sell, ce_buy = 26250, 26500    # Call strikes
pe_buy_prem, pe_sell_prem = 50, 100
ce_sell_prem, ce_buy_prem = 100, 50

payoff = iron_condor_payoff(
    spot_range, pe_buy, pe_sell, ce_sell, ce_buy,
    pe_buy_prem, pe_sell_prem, ce_sell_prem, ce_buy_prem
)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=spot_range, y=payoff,
    mode='lines', name='Iron Condor',
    fill='tozeroy',
    line=dict(color='purple', width=2)
))

fig.add_hline(y=0, line_dash="dash")
fig.update_layout(
    title='Iron Condor Payoff Diagram',
    xaxis_title='Spot Price at Expiry',
    yaxis_title='Profit/Loss'
)

fig.show()
```

### Straddle Payoff

```python
def straddle_payoff(spot_range, strike, call_prem, put_prem, position='long'):
    """Calculate straddle payoff."""
    call_payoff = np.maximum(spot_range - strike, 0) - call_prem
    put_payoff = np.maximum(strike - spot_range, 0) - put_prem

    if position == 'long':
        return call_payoff + put_payoff
    else:  # short
        return -(call_payoff + put_payoff)

spot_range = np.arange(25000, 27000, 25)
strike = 26000
call_prem, put_prem = 250, 245

long_payoff = straddle_payoff(spot_range, strike, call_prem, put_prem, 'long')
short_payoff = straddle_payoff(spot_range, strike, call_prem, put_prem, 'short')

fig = go.Figure()
fig.add_trace(go.Scatter(x=spot_range, y=long_payoff, name='Long Straddle', line=dict(color='green')))
fig.add_trace(go.Scatter(x=spot_range, y=short_payoff, name='Short Straddle', line=dict(color='red')))
fig.add_hline(y=0, line_dash="dash")

fig.update_layout(
    title='Straddle Payoff Comparison',
    xaxis_title='Spot Price',
    yaxis_title='Profit/Loss'
)

fig.show()
```

---

## Real-time Streamlit Dashboard

### Basic Dashboard Template

```python
# streamlit_dashboard.py
import streamlit as st
from openalgo import api
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="OpenAlgo Dashboard", layout="wide")

# Initialize client
@st.cache_resource
def get_client():
    return api(
        api_key=st.secrets.get("OPENALGO_API_KEY", "your_key"),
        host=st.secrets.get("OPENALGO_HOST", "http://127.0.0.1:5000")
    )

client = get_client()

# Sidebar
st.sidebar.title("OpenAlgo Dashboard")
symbols = st.sidebar.text_input("Symbols (comma-separated)", "NIFTY,BANKNIFTY,RELIANCE")
exchange = st.sidebar.selectbox("Exchange", ["NSE", "NSE_INDEX", "NFO", "MCX"])
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 60, 5)

# Main content
st.title("Real-time Market Dashboard")

# Watchlist
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Watchlist")

    symbol_list = [{"symbol": s.strip(), "exchange": exchange} for s in symbols.split(",")]

    placeholder = st.empty()

    while True:
        quotes = client.multiquotes(symbols=symbol_list)

        if quotes.get('status') == 'success':
            data = []
            for item in quotes.get('results', []):
                d = item.get('data', {})
                change = d['ltp'] - d['prev_close'] if d.get('prev_close') else 0
                change_pct = (change / d['prev_close'] * 100) if d.get('prev_close') else 0

                data.append({
                    'Symbol': item['symbol'],
                    'LTP': d.get('ltp', 0),
                    'Change': change,
                    'Change%': change_pct,
                    'Volume': d.get('volume', 0)
                })

            df = pd.DataFrame(data)

            # Style the dataframe
            def color_change(val):
                color = 'green' if val > 0 else 'red' if val < 0 else 'black'
                return f'color: {color}'

            styled_df = df.style.applymap(color_change, subset=['Change', 'Change%'])
            placeholder.dataframe(styled_df, use_container_width=True)

        time.sleep(refresh_rate)

with col2:
    st.subheader("Quick Stats")
    st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
```

### P&L Dashboard

```python
# pnl_dashboard.py
import streamlit as st
from openalgo import api
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="P&L Dashboard", layout="wide")

@st.cache_resource
def get_client():
    return api(api_key="your_key", host="http://127.0.0.1:5000")

client = get_client()

st.title("Portfolio P&L Dashboard")

# Fetch positions
positions = client.positionbook()
holdings = client.holdings()
funds = client.funds()

col1, col2, col3 = st.columns(3)

# Funds summary
if funds.get('status') == 'success':
    fund_data = funds.get('data', {})
    col1.metric("Available Cash", f"₹{float(fund_data.get('availablecash', 0)):,.2f}")
    col2.metric("M2M Realized", f"₹{float(fund_data.get('m2mrealized', 0)):,.2f}")
    col3.metric("M2M Unrealized", f"₹{float(fund_data.get('m2munrealized', 0)):,.2f}")

# Positions
st.subheader("Open Positions")
if positions.get('status') == 'success':
    pos_data = positions.get('data', [])
    if pos_data:
        df = pd.DataFrame(pos_data)
        df['pnl'] = pd.to_numeric(df['pnl'], errors='coerce')

        # P&L chart
        fig = px.bar(df, x='symbol', y='pnl', color='pnl',
                     color_continuous_scale=['red', 'green'],
                     title='Position-wise P&L')
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df, use_container_width=True)
    else:
        st.info("No open positions")

# Holdings
st.subheader("Holdings")
if holdings.get('status') == 'success':
    hold_data = holdings.get('data', {}).get('holdings', [])
    if hold_data:
        df = pd.DataFrame(hold_data)
        st.dataframe(df, use_container_width=True)

        # Holdings pie chart
        fig = px.pie(df, values='quantity', names='symbol', title='Holdings Distribution')
        st.plotly_chart(fig, use_container_width=True)
```

---

## Chart Patterns

### Support/Resistance Lines

```python
import numpy as np
from scipy.signal import argrelextrema

def find_support_resistance(df, order=5):
    """Find support and resistance levels."""
    highs = df['high'].values
    lows = df['low'].values

    # Find local maxima and minima
    resistance_idx = argrelextrema(highs, np.greater, order=order)[0]
    support_idx = argrelextrema(lows, np.less, order=order)[0]

    resistance_levels = highs[resistance_idx]
    support_levels = lows[support_idx]

    return support_levels, resistance_levels

support, resistance = find_support_resistance(df)

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['open'], high=df['high'],
                              low=df['low'], close=df['close']))

for level in support[-3:]:  # Last 3 support levels
    fig.add_hline(y=level, line_dash="dash", line_color="green",
                  annotation_text=f"Support: {level:.2f}")

for level in resistance[-3:]:  # Last 3 resistance levels
    fig.add_hline(y=level, line_dash="dash", line_color="red",
                  annotation_text=f"Resistance: {level:.2f}")

fig.show()
```

---

## Notes

- Use Plotly for interactive charts
- Streamlit for quick dashboards
- Matplotlib for static charts
- Consider caching data to reduce API calls
- WebSocket streaming for real-time updates in dashboards
