---
name: trading-expert
version: 1.0.0
description: Expert-level algorithmic trading, market systems, quantitative analysis, and trading platforms
category: domains
tags: [trading, algorithmic-trading, quant, markets, finance, hft]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(python:*)
---

# Trading Expert

Expert guidance for algorithmic trading systems, quantitative analysis, market data processing, and trading platform development.

## Core Concepts

### Trading Systems
- Algorithmic trading strategies
- High-frequency trading (HFT)
- Market making
- Arbitrage strategies
- Portfolio optimization
- Risk management

### Market Data
- Order book processing
- Tick data analysis
- Market microstructure
- Real-time data feeds
- Historical data analysis

### Execution
- Order routing
- Smart order routing (SOR)
- Execution algorithms (TWAP, VWAP)
- Slippage minimization
- Transaction cost analysis

## Trading Strategy Implementation

```python
import pandas as pd
import numpy as np
from typing import Optional

class TradingStrategy:
    def __init__(self, symbol: str, capital: float = 100000):
        self.symbol = symbol
        self.capital = capital
        self.position = 0
        self.cash = capital
        self.trades = []

    def moving_average_crossover(self, data: pd.DataFrame,
                                  short_window: int = 50,
                                  long_window: int = 200) -> pd.Series:
        """Simple Moving Average Crossover Strategy"""
        data['SMA_short'] = data['close'].rolling(window=short_window).mean()
        data['SMA_long'] = data['close'].rolling(window=long_window).mean()

        # Generate signals
        data['signal'] = 0
        data.loc[data['SMA_short'] > data['SMA_long'], 'signal'] = 1
        data.loc[data['SMA_short'] < data['SMA_long'], 'signal'] = -1

        return data['signal']

    def mean_reversion(self, data: pd.DataFrame,
                       window: int = 20,
                       num_std: float = 2.0) -> pd.Series:
        """Mean Reversion Strategy using Bollinger Bands"""
        data['MA'] = data['close'].rolling(window=window).mean()
        data['STD'] = data['close'].rolling(window=window).std()
        data['upper_band'] = data['MA'] + (data['STD'] * num_std)
        data['lower_band'] = data['MA'] - (data['STD'] * num_std)

        # Generate signals
        data['signal'] = 0
        data.loc[data['close'] < data['lower_band'], 'signal'] = 1  # Buy
        data.loc[data['close'] > data['upper_band'], 'signal'] = -1  # Sell

        return data['signal']

    def momentum_strategy(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Momentum Strategy using RSI"""
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))

        # Generate signals
        data['signal'] = 0
        data.loc[data['RSI'] < 30, 'signal'] = 1  # Oversold - Buy
        data.loc[data['RSI'] > 70, 'signal'] = -1  # Overbought - Sell

        return data['signal']

class Backtester:
    def __init__(self, initial_capital: float = 100000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0
        self.trades = []

    def run(self, data: pd.DataFrame, signals: pd.Series) -> dict:
        """Run backtest on historical data"""
        portfolio_value = []

        for i in range(len(data)):
            if signals.iloc[i] == 1 and self.position == 0:  # Buy signal
                shares = self.capital // data['close'].iloc[i]
                cost = shares * data['close'].iloc[i]
                self.capital -= cost
                self.position = shares
                self.trades.append({
                    'type': 'BUY',
                    'price': data['close'].iloc[i],
                    'shares': shares,
                    'date': data.index[i]
                })

            elif signals.iloc[i] == -1 and self.position > 0:  # Sell signal
                proceeds = self.position * data['close'].iloc[i]
                self.capital += proceeds
                self.trades.append({
                    'type': 'SELL',
                    'price': data['close'].iloc[i],
                    'shares': self.position,
                    'date': data.index[i]
                })
                self.position = 0

            # Calculate portfolio value
            current_value = self.capital + (self.position * data['close'].iloc[i])
            portfolio_value.append(current_value)

        return self.calculate_metrics(portfolio_value, data)

    def calculate_metrics(self, portfolio_value: list, data: pd.DataFrame) -> dict:
        """Calculate performance metrics"""
        returns = pd.Series(portfolio_value).pct_change()

        total_return = (portfolio_value[-1] - self.initial_capital) / self.initial_capital
        sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252)
        max_drawdown = self.calculate_max_drawdown(portfolio_value)

        return {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_trades': len(self.trades),
            'final_value': portfolio_value[-1]
        }

    def calculate_max_drawdown(self, portfolio_value: list) -> float:
        """Calculate maximum drawdown"""
        peak = portfolio_value[0]
        max_dd = 0

        for value in portfolio_value:
            if value > peak:
                peak = value
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd

        return max_dd
```

## Order Execution

```python
from enum import Enum
from decimal import Decimal
from datetime import datetime

class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"

class Order:
    def __init__(self, symbol: str, side: OrderSide, order_type: OrderType,
                 quantity: int, price: Optional[Decimal] = None):
        self.id = self.generate_order_id()
        self.symbol = symbol
        self.side = side
        self.type = order_type
        self.quantity = quantity
        self.price = price
        self.filled_quantity = 0
        self.status = "NEW"
        self.created_at = datetime.now()

    def generate_order_id(self) -> str:
        import uuid
        return str(uuid.uuid4())

class OrderManager:
    def __init__(self):
        self.orders = {}
        self.positions = {}

    def place_order(self, order: Order) -> str:
        """Place new order"""
        self.orders[order.id] = order

        # Route to exchange/broker
        self.route_order(order)

        return order.id

    def cancel_order(self, order_id: str) -> bool:
        """Cancel existing order"""
        if order_id in self.orders:
            order = self.orders[order_id]
            if order.status in ["NEW", "PARTIALLY_FILLED"]:
                order.status = "CANCELLED"
                return True
        return False

    def route_order(self, order: Order):
        """Smart order routing"""
        # Check for best execution venue
        venues = self.get_venue_quotes(order.symbol)
        best_venue = self.select_best_venue(venues, order)

        # Send order to venue
        self.send_to_venue(order, best_venue)
```

## Risk Management

```python
class RiskManager:
    def __init__(self, max_position_size: float = 0.1,
                 max_portfolio_risk: float = 0.02,
                 stop_loss_pct: float = 0.05):
        self.max_position_size = max_position_size
        self.max_portfolio_risk = max_portfolio_risk
        self.stop_loss_pct = stop_loss_pct

    def calculate_position_size(self, capital: float, price: float,
                                volatility: float) -> int:
        """Calculate optimal position size using Kelly Criterion"""
        max_position_value = capital * self.max_position_size
        shares = int(max_position_value / price)

        # Adjust for volatility
        risk_adjusted_shares = int(shares * (1 - volatility))

        return max(0, risk_adjusted_shares)

    def check_risk_limits(self, portfolio: dict) -> bool:
        """Check if portfolio is within risk limits"""
        total_value = portfolio['cash'] + sum(p['value'] for p in portfolio['positions'])
        total_risk = sum(p['risk'] for p in portfolio['positions'])

        if total_risk / total_value > self.max_portfolio_risk:
            return False

        return True

    def calculate_var(self, returns: pd.Series, confidence: float = 0.95) -> float:
        """Calculate Value at Risk"""
        return returns.quantile(1 - confidence)
```

## Market Data Processing

```python
class MarketDataProcessor:
    def __init__(self):
        self.order_book = {'bids': [], 'asks': []}

    def process_tick(self, tick: dict):
        """Process real-time tick data"""
        if tick['type'] == 'trade':
            self.process_trade(tick)
        elif tick['type'] == 'quote':
            self.update_order_book(tick)

    def update_order_book(self, quote: dict):
        """Update order book with new quote"""
        if quote['side'] == 'bid':
            self.order_book['bids'] = sorted(
                self.order_book['bids'] + [(quote['price'], quote['size'])],
                key=lambda x: x[0],
                reverse=True
            )[:100]  # Keep top 100
        else:
            self.order_book['asks'] = sorted(
                self.order_book['asks'] + [(quote['price'], quote['size'])],
                key=lambda x: x[0]
            )[:100]

    def calculate_vwap(self, trades: list) -> float:
        """Calculate Volume Weighted Average Price"""
        total_volume = sum(t['volume'] for t in trades)
        vwap = sum(t['price'] * t['volume'] for t in trades) / total_volume
        return vwap

    def calculate_spread(self) -> float:
        """Calculate bid-ask spread"""
        if self.order_book['bids'] and self.order_book['asks']:
            best_bid = self.order_book['bids'][0][0]
            best_ask = self.order_book['asks'][0][0]
            return best_ask - best_bid
        return 0
```

## Best Practices

- Always backtest strategies on historical data
- Implement proper risk management
- Monitor execution quality (slippage, fill rates)
- Use limit orders to control execution price
- Implement circuit breakers for risk control
- Log all trades and orders for audit
- Test in paper trading before live deployment
- Monitor latency in real-time systems
- Implement failover mechanisms
- Regular strategy performance review

## Anti-Patterns

❌ No backtesting before live trading
❌ Ignoring transaction costs
❌ Over-optimization (curve fitting)
❌ No risk management
❌ Trading without stop losses
❌ Ignoring market microstructure
❌ No position sizing strategy

## Resources

- QuantConnect: https://www.quantconnect.com/
- Zipline: https://www.zipline.io/
- Backtrader: https://www.backtrader.com/
- Interactive Brokers API: https://interactivebrokers.github.io/
