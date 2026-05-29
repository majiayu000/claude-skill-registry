---
name: QuantConnect
description: QuantConnect strategy development with component library (project)
---

# QuantConnect Strategy Development (Component-Based)

Develop modular strategies using reusable components: `./component`

## When to Load This Skill

- Creating new QuantConnect strategy
- Need to add indicators, signals, or risk management
- Troubleshooting QC-specific issues

## Component Library (Progressive Disclosure)

**Use components instead of writing from scratch**. Load only what you need.

### Discovery
```bash
# List all components
./component list

# List by category
./component list indicators
./component list signals
./component list risk_management

# Search by keyword
./component search momentum
./component search stop
```

### Integration
```bash
# View component code
./component show add_rsi

# Get integration guide
./component explain add_rsi
```

**IMPORTANT: Do not read component source files directly. Use --help and explain commands.**

## Available Components

### Indicators (indicators/)
- **add_rsi** - RSI indicator for overbought/oversold
- **add_sma** - Simple Moving Average for trend detection

### Signals (signals/)
- **mean_reversion** - RSI-based mean reversion signals
- **momentum_breakout** - SMA crossover momentum signals

### Risk Management (risk_management/)
- **stop_loss** - Fixed or trailing stop loss

### Sentiment (sentiment/)
- Future: Kalshi prediction market integration

## Strategy Development Workflow

### 1. Plan Strategy
```
1. Choose hypothesis (mean reversion, momentum, etc.)
2. Select components needed:
   - Indicators: RSI, SMA, MACD?
   - Signals: Mean reversion, breakout?
   - Risk: Stop loss, position sizing?
```

### 2. Browse Components
```bash
./component list
./component explain COMPONENT
```

### 3. Build Strategy
```python
from AlgorithmImports import *
from strategy_components.indicators.add_rsi import add_rsi
from strategy_components.signals.mean_reversion import MeanReversionSignal

class MyStrategy(QCAlgorithm):
    def Initialize(self):
        # Add components
        self.rsi = add_rsi(self, symbol="SPY", period=14)
        self.signal = MeanReversionSignal(oversold=30, overbought=70)
        
    def OnData(self, data):
        # Use components
        if self.rsi.IsReady:
            signal = self.signal.get_signal(self.rsi.Current.Value, self.is_long)
            # Execute trades...
```

### 4. Test Strategy
```bash
# Local test first (if possible)
# Then: ./qc_backtest run --strategy strategy.py
```

## Common Patterns

### Mean Reversion
```python
# Components: add_rsi, mean_reversion
self.rsi = add_rsi(self, "SPY", period=14)
self.signal = MeanReversionSignal(oversold=30, overbought=70)
```

### Momentum Breakout
```python
# Components: add_sma, momentum_breakout
self.sma = add_sma(self, "SPY", period=20)
self.signal = MomentumBreakoutSignal(volume_confirmation=True)
```

### With Stop Loss
```python
# Add: stop_loss component
self.stop_loss = StopLossManager(stop_loss_pct=0.05, trailing=False)
# Call: self.stop_loss.set_entry_price(price) after entry
# Check: if self.stop_loss.should_exit(current_price): ...
```

## Beyond MCP Principles

1. **Use component CLI, not source code**
   - `./component list` - browse available
   - `./component explain COMPONENT` - integration guide
   - Don't read .py files directly

2. **Progressive Disclosure**
   - Load only components you need
   - Don't load entire 955-line skill

3. **Modular Architecture**
   - Components are independent
   - Mix and match as needed
   - Reuse across strategies

## Critical QC Errors (Still Important)

### Error 1: SMA NoneType
**Problem**: `self.sma.Current` is None
**Fix**: Check `if self.sma.IsReady` before using

### Error 2: Data Key Missing
**Problem**: `KeyError` on `data[self.symbol]`
**Fix**: Check `if data.ContainsKey(self.symbol)` first

### Error 3: Warmup Issues
**Problem**: Strategy trades during warmup
**Fix**: `if self.IsWarmingUp: return`

## Authoritative Documentation

**When confused about QC API or architecture:**
- QC Docs: https://www.quantconnect.com/docs
- Component README: `SCRIPTS/strategy_components/README.md`

**Do not guess. Use component CLI and QC docs as source of truth.**

---

**Context Savings**: 120 lines (vs 955 lines in old skill) = 87% reduction

**Progressive Disclosure**: Use component CLI to load only what you need

**Trifecta**: CLI works for humans, teams, AND agents

**Beyond MCP Pattern**: Use --help and explain, not source code
