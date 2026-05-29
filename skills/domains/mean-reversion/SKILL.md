---
name: scarface-mean-reversion
description: Trade mean reversion setups in the style of Scarface Trades, the mean reversion specialist known for mathematical precision and statistical edge. Emphasizes standard deviation bands, RSI extremes, and calculated entries with defined risk. Use when trading overextended moves, fading extremes, or building systematic reversion strategies.
---

# Scarface Trades Mean Reversion Style Guide

## Overview

Scarface Trades is a trader known for mastering mean reversion—the principle that prices tend to return to their average over time. When a stock deviates significantly from its mean, probability favors a snap-back. His approach is purely mathematical: standard deviations, RSI extremes, and statistical probabilities define every trade.

## Core Philosophy

> "Price always returns to the mean. The only question is when and how far it overshoots."

> "Two standard deviations is where the math gets interesting. Three is where money is made."

> "I don't predict direction. I bet on reversion to the mean with defined risk."

Mean reversion isn't about being right—it's about probability. When price extends 2-3 standard deviations from its mean, the statistical odds of reversion increase dramatically. Scarface trades these probabilities with strict math and risk management.

## Design Principles

1. **Standard Deviation is King**: Price at 2σ has ~95% historical reversion probability.

2. **RSI Confirms Extremes**: Oversold (<30) or overbought (>70) adds confluence.

3. **Define Risk First**: Know your stop before calculating position size.

4. **Scale In, Scale Out**: Enter in thirds at 2σ, 2.5σ, 3σ; exit in thirds at mean.

5. **Time Frame Alignment**: Higher timeframe mean = stronger magnet.

## The Math

### Standard Deviation Bands

```
Mean (μ) = SMA(price, period)
Standard Deviation (σ) = STDEV(price, period)

Upper Band 1σ = μ + (1 × σ)
Upper Band 2σ = μ + (2 × σ)
Upper Band 3σ = μ + (3 × σ)

Lower Band 1σ = μ - (1 × σ)
Lower Band 2σ = μ - (2 × σ)
Lower Band 3σ = μ - (3 × σ)
```

**Statistical Probabilities (Normal Distribution):**
- Price within 1σ: 68.2% of the time
- Price within 2σ: 95.4% of the time
- Price within 3σ: 99.7% of the time

**Reversion Edge:**
- At 2σ: ~95% chance price returns to within 1σ
- At 3σ: ~99% chance price returns to within 2σ

### RSI Calculation

```
RS = Average Gain (n periods) / Average Loss (n periods)
RSI = 100 - (100 / (1 + RS))

Oversold: RSI < 30
Overbought: RSI > 70
Extreme Oversold: RSI < 20
Extreme Overbought: RSI > 80
```

### Position Sizing Formula

```
Risk Amount = Account × Risk Percentage (typically 1-2%)
Position Size = Risk Amount / (Entry Price - Stop Price)

Example:
  Account: $100,000
  Risk: 1% = $1,000
  Entry: $50.00
  Stop: $52.00 (2σ + buffer)
  
  Position Size = $1,000 / $2.00 = 500 shares
```

## When Trading Mean Reversion

### Always

- Calculate standard deviation bands before entering
- Confirm with RSI or other momentum oscillator
- Set stops beyond the extreme (3σ + ATR buffer)
- Scale into positions at multiple deviation levels
- Take partial profits at the mean
- Use limit orders, not market orders

### Never

- Fight a trend without deviation from mean
- Enter at 1σ (not enough edge)
- Hold through earnings or major catalysts
- Average down without predefined levels
- Ignore volume (climactic volume = exhaustion)
- Risk more than 2% per trade

### Prefer

- Stocks with history of mean-reverting behavior
- High RSI divergence with price
- End-of-day setups (overnight reversion)
- Liquid names with tight spreads
- Multiple timeframe confluence
- Scaling in/out over single entry/exit

## Code Patterns

### Mean Reversion Scanner

```python
class MeanReversionScanner:
    """
    Scarface-style mean reversion setup identification.
    Pure math: standard deviations and RSI extremes.
    """
    
    def __init__(self, lookback_period: int = 20):
        self.period = lookback_period
    
    def calculate_bands(self, prices: pd.Series) -> dict:
        """
        Calculate mean and standard deviation bands.
        """
        mean = prices.rolling(self.period).mean()
        std = prices.rolling(self.period).std()
        
        return {
            'mean': mean,
            'std': std,
            'upper_1sd': mean + std,
            'upper_2sd': mean + (2 * std),
            'upper_3sd': mean + (3 * std),
            'lower_1sd': mean - std,
            'lower_2sd': mean - (2 * std),
            'lower_3sd': mean - (3 * std),
        }
    
    def calculate_z_score(self, price: float, mean: float, std: float) -> float:
        """
        How many standard deviations from the mean?
        """
        return (price - mean) / std
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Relative Strength Index calculation.
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def scan_for_setups(self, 
                        symbols: List[str], 
                        data: Dict[str, pd.DataFrame]) -> List[Setup]:
        """
        Scan universe for mean reversion setups.
        """
        setups = []
        
        for symbol in symbols:
            df = data[symbol]
            prices = df['close']
            
            bands = self.calculate_bands(prices)
            rsi = self.calculate_rsi(prices)
            
            current_price = prices.iloc[-1]
            current_mean = bands['mean'].iloc[-1]
            current_std = bands['std'].iloc[-1]
            current_rsi = rsi.iloc[-1]
            
            z_score = self.calculate_z_score(current_price, current_mean, current_std)
            
            # Long setup: price at -2σ or below with RSI < 30
            if z_score <= -2 and current_rsi < 30:
                setups.append(Setup(
                    symbol=symbol,
                    direction='LONG',
                    z_score=z_score,
                    rsi=current_rsi,
                    entry_price=current_price,
                    mean_target=current_mean,
                    stop_price=bands['lower_3sd'].iloc[-1] - self.atr_buffer(df),
                    edge_probability=self.get_reversion_probability(z_score)
                ))
            
            # Short setup: price at +2σ or above with RSI > 70
            elif z_score >= 2 and current_rsi > 70:
                setups.append(Setup(
                    symbol=symbol,
                    direction='SHORT',
                    z_score=z_score,
                    rsi=current_rsi,
                    entry_price=current_price,
                    mean_target=current_mean,
                    stop_price=bands['upper_3sd'].iloc[-1] + self.atr_buffer(df),
                    edge_probability=self.get_reversion_probability(z_score)
                ))
        
        return sorted(setups, key=lambda x: abs(x.z_score), reverse=True)
    
    def get_reversion_probability(self, z_score: float) -> float:
        """
        Statistical probability of reversion based on z-score.
        """
        from scipy import stats
        # Probability of returning to within 1σ
        return stats.norm.cdf(1) - stats.norm.cdf(z_score) if z_score < 0 else \
               stats.norm.cdf(z_score) - stats.norm.cdf(1)
    
    def atr_buffer(self, df: pd.DataFrame, period: int = 14) -> float:
        """
        ATR-based buffer for stop placement.
        """
        high = df['high']
        low = df['low']
        close = df['close']
        
        tr = pd.concat([
            high - low,
            abs(high - close.shift(1)),
            abs(low - close.shift(1))
        ], axis=1).max(axis=1)
        
        return tr.rolling(period).mean().iloc[-1]
```

### Position Manager with Scaling

```python
class MeanReversionPositionManager:
    """
    Manage scaled entries and exits for mean reversion trades.
    """
    
    def __init__(self, 
                 account_size: float,
                 risk_per_trade: float = 0.01):  # 1%
        self.account = account_size
        self.risk_pct = risk_per_trade
    
    def calculate_scaled_entries(self, setup: Setup) -> List[Entry]:
        """
        Scale into position at 2σ, 2.5σ, 3σ levels.
        Scarface method: thirds at each level.
        """
        direction = 1 if setup.direction == 'LONG' else -1
        mean = setup.mean_target
        std = (setup.entry_price - mean) / setup.z_score * direction
        
        total_risk = self.account * self.risk_pct
        risk_per_level = total_risk / 3
        
        entries = []
        
        levels = [
            ('2.0σ', 2.0, 0.33),
            ('2.5σ', 2.5, 0.33),
            ('3.0σ', 3.0, 0.34),
        ]
        
        for label, sigma, allocation in levels:
            entry_price = mean + (direction * -1 * sigma * std)
            stop_distance = abs(setup.stop_price - entry_price)
            
            shares = int((risk_per_level * allocation * 3) / stop_distance)
            
            entries.append(Entry(
                level=label,
                price=entry_price,
                shares=shares,
                allocation_pct=allocation
            ))
        
        return entries
    
    def calculate_scaled_exits(self, 
                                setup: Setup,
                                avg_entry: float,
                                total_shares: int) -> List[Exit]:
        """
        Scale out at mean, -1σ (for longs), and breakeven.
        """
        direction = 1 if setup.direction == 'LONG' else -1
        mean = setup.mean_target
        std = abs(setup.entry_price - mean) / abs(setup.z_score)
        
        exits = [
            Exit(
                level='Mean (μ)',
                price=mean,
                shares=int(total_shares * 0.50),
                reason='Primary target: reversion to mean'
            ),
            Exit(
                level='1σ toward entry',
                price=mean + (direction * -0.5 * std),
                shares=int(total_shares * 0.25),
                reason='Partial: halfway to mean'
            ),
            Exit(
                level='Runner',
                price=mean + (direction * std),  # 1σ past mean
                shares=int(total_shares * 0.25),
                reason='Runner: extended reversion'
            ),
        ]
        
        return exits
    
    def calculate_risk_reward(self, setup: Setup, entries: List[Entry]) -> dict:
        """
        Calculate overall risk/reward for scaled position.
        """
        total_shares = sum(e.shares for e in entries)
        avg_entry = sum(e.price * e.shares for e in entries) / total_shares
        
        risk = abs(avg_entry - setup.stop_price) * total_shares
        reward = abs(setup.mean_target - avg_entry) * total_shares
        
        return {
            'avg_entry': avg_entry,
            'total_shares': total_shares,
            'total_risk_dollars': risk,
            'target_reward_dollars': reward,
            'risk_reward_ratio': reward / risk,
            'required_win_rate': 1 / (1 + reward/risk)
        }
```

### Backtesting Mean Reversion

```python
class MeanReversionBacktest:
    """
    Backtest mean reversion strategy with realistic assumptions.
    """
    
    def __init__(self, 
                 entry_z_threshold: float = 2.0,
                 exit_z_threshold: float = 0.0,  # Mean
                 stop_z_threshold: float = 3.5,
                 lookback: int = 20):
        self.entry_z = entry_z_threshold
        self.exit_z = exit_z_threshold
        self.stop_z = stop_z_threshold
        self.lookback = lookback
    
    def run_backtest(self, 
                     prices: pd.Series,
                     start_date: str,
                     end_date: str) -> BacktestResult:
        """
        Run backtest on historical data.
        """
        prices = prices.loc[start_date:end_date]
        
        mean = prices.rolling(self.lookback).mean()
        std = prices.rolling(self.lookback).std()
        z_score = (prices - mean) / std
        
        trades = []
        position = None
        
        for i in range(self.lookback, len(prices)):
            current_z = z_score.iloc[i]
            current_price = prices.iloc[i]
            
            if position is None:
                # Check for entry
                if current_z <= -self.entry_z:
                    position = Trade(
                        direction='LONG',
                        entry_price=current_price,
                        entry_date=prices.index[i],
                        entry_z=current_z,
                        stop_price=mean.iloc[i] - (self.stop_z * std.iloc[i])
                    )
                elif current_z >= self.entry_z:
                    position = Trade(
                        direction='SHORT',
                        entry_price=current_price,
                        entry_date=prices.index[i],
                        entry_z=current_z,
                        stop_price=mean.iloc[i] + (self.stop_z * std.iloc[i])
                    )
            else:
                # Check for exit
                exit_signal = False
                exit_reason = None
                
                if position.direction == 'LONG':
                    if current_z >= self.exit_z:
                        exit_signal = True
                        exit_reason = 'TARGET'
                    elif current_price <= position.stop_price:
                        exit_signal = True
                        exit_reason = 'STOP'
                else:  # SHORT
                    if current_z <= self.exit_z:
                        exit_signal = True
                        exit_reason = 'TARGET'
                    elif current_price >= position.stop_price:
                        exit_signal = True
                        exit_reason = 'STOP'
                
                if exit_signal:
                    position.exit_price = current_price
                    position.exit_date = prices.index[i]
                    position.exit_reason = exit_reason
                    position.pnl_pct = self.calculate_pnl(position)
                    trades.append(position)
                    position = None
        
        return self.analyze_trades(trades)
    
    def calculate_pnl(self, trade: Trade) -> float:
        """Calculate percentage P&L for a trade."""
        if trade.direction == 'LONG':
            return (trade.exit_price - trade.entry_price) / trade.entry_price
        else:
            return (trade.entry_price - trade.exit_price) / trade.entry_price
    
    def analyze_trades(self, trades: List[Trade]) -> BacktestResult:
        """Compute strategy statistics."""
        if not trades:
            return BacktestResult(total_trades=0)
        
        pnls = [t.pnl_pct for t in trades]
        winners = [t for t in trades if t.pnl_pct > 0]
        losers = [t for t in trades if t.pnl_pct <= 0]
        
        return BacktestResult(
            total_trades=len(trades),
            win_rate=len(winners) / len(trades),
            avg_win=np.mean([t.pnl_pct for t in winners]) if winners else 0,
            avg_loss=np.mean([t.pnl_pct for t in losers]) if losers else 0,
            profit_factor=abs(sum(t.pnl_pct for t in winners) / 
                            sum(t.pnl_pct for t in losers)) if losers else float('inf'),
            total_return=np.prod([1 + p for p in pnls]) - 1,
            max_drawdown=self.calculate_max_drawdown(pnls),
            sharpe_ratio=np.mean(pnls) / np.std(pnls) * np.sqrt(252) if np.std(pnls) > 0 else 0,
            avg_holding_period=np.mean([(t.exit_date - t.entry_date).days for t in trades])
        )
```

## Mental Model

Scarface approaches mean reversion by asking:

1. **How extended is it?** Z-score tells you standard deviations from mean
2. **Is momentum confirming?** RSI extremes add confluence
3. **What's my risk?** Stop at 3σ + ATR buffer
4. **What's the probability?** >2σ has 95%+ reversion probability
5. **How do I scale?** Enter in thirds, exit in thirds

## The Setup Checklist

```
□ Price at 2σ or beyond from 20-period mean
□ RSI < 30 (long) or RSI > 70 (short)
□ No earnings within 5 days
□ Sufficient liquidity (>1M avg volume)
□ Stop calculated (3σ + 1 ATR buffer)
□ Position sized to 1% account risk
□ Scaling levels defined (2σ, 2.5σ, 3σ)
□ Exit targets defined (mean, runner)
```

## Signature Scarface Moves

- Standard deviation bands (2σ, 3σ entries)
- RSI confirmation at extremes
- Scaling in at multiple sigma levels
- Taking profits at the mean
- ATR-based stop buffers
- Mathematical position sizing
- Z-score quantification of setups
- Probability-based edge calculation
