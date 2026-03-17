---
name: technical-indicators
description: Technical analysis with TA-Lib - Moving averages, RSI, MACD, Bollinger Bands, Stochastic, ATR, candlestick patterns, and strategy signals using OpenAlgo market data
---

# OpenAlgo Technical Indicators

Perform technical analysis using TA-Lib with OpenAlgo market data. Build trading strategies based on indicators, generate signals, and backtest ideas.

## Environment Setup

```bash
# Install TA-Lib (requires system library)
# macOS
brew install ta-lib
pip install TA-Lib

# Ubuntu/Debian
sudo apt-get install libta-lib-dev
pip install TA-Lib

# Windows
# Download from https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
pip install TA_Lib‑0.4.28‑cp311‑cp311‑win_amd64.whl
```

```python
from openalgo import api
import talib
import pandas as pd
import numpy as np

client = api(
    api_key='your_api_key_here',
    host='http://127.0.0.1:5000'
)
```

## Quick Start Scripts

### Calculate Indicators
```bash
python scripts/indicators.py --symbol SBIN --exchange NSE --interval 5m --days 5
```

### Generate Signals
```bash
python scripts/signals.py --symbol NIFTY --exchange NSE_INDEX --strategy rsi_oversold
```

### Scan for Patterns
```bash
python scripts/scanner.py --symbols RELIANCE,TCS,INFY,SBIN --exchange NSE --pattern bullish
```

---

## Fetching Data for Analysis

```python
from openalgo import api
import pandas as pd

client = api(api_key='your_key', host='http://127.0.0.1:5000')

# Fetch historical data
df = client.history(
    symbol="SBIN",
    exchange="NSE",
    interval="5m",
    start_date="2025-01-01",
    end_date="2025-01-15"
)

# TA-Lib requires numpy arrays
open_prices = df['open'].values
high_prices = df['high'].values
low_prices = df['low'].values
close_prices = df['close'].values
volume = df['volume'].values
```

---

## Overlap Studies (Trend Indicators)

### Simple Moving Average (SMA)

```python
import talib

# Calculate SMA
sma_20 = talib.SMA(close_prices, timeperiod=20)
sma_50 = talib.SMA(close_prices, timeperiod=50)
sma_200 = talib.SMA(close_prices, timeperiod=200)

# Add to DataFrame
df['SMA_20'] = sma_20
df['SMA_50'] = sma_50
df['SMA_200'] = sma_200

# Crossover signal
df['SMA_Cross'] = np.where(df['SMA_20'] > df['SMA_50'], 1, -1)
```

### Exponential Moving Average (EMA)

```python
ema_9 = talib.EMA(close_prices, timeperiod=9)
ema_21 = talib.EMA(close_prices, timeperiod=21)

df['EMA_9'] = ema_9
df['EMA_21'] = ema_21

# EMA crossover
df['EMA_Signal'] = np.where(df['EMA_9'] > df['EMA_21'], 'BUY', 'SELL')
```

### Bollinger Bands

```python
upper, middle, lower = talib.BBANDS(
    close_prices,
    timeperiod=20,
    nbdevup=2,
    nbdevdn=2,
    matype=0  # SMA
)

df['BB_Upper'] = upper
df['BB_Middle'] = middle
df['BB_Lower'] = lower
df['BB_Width'] = (upper - lower) / middle * 100  # Bandwidth %

# Bollinger Band signals
df['BB_Signal'] = np.where(close_prices < lower, 'BUY',
                   np.where(close_prices > upper, 'SELL', 'HOLD'))
```

### SuperTrend (Custom Implementation)

```python
def supertrend(df, period=10, multiplier=3):
    """Calculate SuperTrend indicator."""
    hl2 = (df['high'] + df['low']) / 2
    atr = talib.ATR(df['high'].values, df['low'].values, df['close'].values, timeperiod=period)

    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)

    supertrend = pd.Series(index=df.index, dtype=float)
    direction = pd.Series(index=df.index, dtype=int)

    for i in range(period, len(df)):
        if df['close'].iloc[i] > upperband[i-1]:
            supertrend.iloc[i] = lowerband[i]
            direction.iloc[i] = 1  # Bullish
        elif df['close'].iloc[i] < lowerband[i-1]:
            supertrend.iloc[i] = upperband[i]
            direction.iloc[i] = -1  # Bearish
        else:
            supertrend.iloc[i] = supertrend.iloc[i-1]
            direction.iloc[i] = direction.iloc[i-1]

    return supertrend, direction

df['SuperTrend'], df['ST_Direction'] = supertrend(df)
```

---

## Momentum Indicators

### Relative Strength Index (RSI)

```python
rsi = talib.RSI(close_prices, timeperiod=14)
df['RSI'] = rsi

# RSI signals
df['RSI_Signal'] = np.where(df['RSI'] < 30, 'OVERSOLD',
                    np.where(df['RSI'] > 70, 'OVERBOUGHT', 'NEUTRAL'))

# RSI divergence detection
def detect_rsi_divergence(df, lookback=14):
    """Detect bullish/bearish RSI divergence."""
    price_low = df['close'].rolling(lookback).min()
    price_high = df['close'].rolling(lookback).max()
    rsi_low = df['RSI'].rolling(lookback).min()
    rsi_high = df['RSI'].rolling(lookback).max()

    # Bullish divergence: price makes lower low, RSI makes higher low
    bullish = (df['close'] == price_low) & (df['RSI'] > rsi_low.shift(lookback))

    # Bearish divergence: price makes higher high, RSI makes lower high
    bearish = (df['close'] == price_high) & (df['RSI'] < rsi_high.shift(lookback))

    return bullish, bearish

df['Bullish_Div'], df['Bearish_Div'] = detect_rsi_divergence(df)
```

### MACD (Moving Average Convergence Divergence)

```python
macd, signal, hist = talib.MACD(
    close_prices,
    fastperiod=12,
    slowperiod=26,
    signalperiod=9
)

df['MACD'] = macd
df['MACD_Signal'] = signal
df['MACD_Hist'] = hist

# MACD crossover signals
df['MACD_Cross'] = np.where(
    (df['MACD'] > df['MACD_Signal']) & (df['MACD'].shift(1) <= df['MACD_Signal'].shift(1)),
    'BUY',
    np.where(
        (df['MACD'] < df['MACD_Signal']) & (df['MACD'].shift(1) >= df['MACD_Signal'].shift(1)),
        'SELL',
        'HOLD'
    )
)
```

### Stochastic Oscillator

```python
slowk, slowd = talib.STOCH(
    high_prices,
    low_prices,
    close_prices,
    fastk_period=14,
    slowk_period=3,
    slowk_matype=0,
    slowd_period=3,
    slowd_matype=0
)

df['Stoch_K'] = slowk
df['Stoch_D'] = slowd

# Stochastic signals
df['Stoch_Signal'] = np.where(
    (df['Stoch_K'] < 20) & (df['Stoch_K'] > df['Stoch_D']),
    'BUY',
    np.where(
        (df['Stoch_K'] > 80) & (df['Stoch_K'] < df['Stoch_D']),
        'SELL',
        'HOLD'
    )
)
```

### ADX (Average Directional Index)

```python
adx = talib.ADX(high_prices, low_prices, close_prices, timeperiod=14)
plus_di = talib.PLUS_DI(high_prices, low_prices, close_prices, timeperiod=14)
minus_di = talib.MINUS_DI(high_prices, low_prices, close_prices, timeperiod=14)

df['ADX'] = adx
df['Plus_DI'] = plus_di
df['Minus_DI'] = minus_di

# Trend strength
df['Trend_Strength'] = np.where(df['ADX'] > 25, 'STRONG',
                        np.where(df['ADX'] > 20, 'MODERATE', 'WEAK'))

# DI crossover with trend filter
df['ADX_Signal'] = np.where(
    (df['Plus_DI'] > df['Minus_DI']) & (df['ADX'] > 25),
    'STRONG_BUY',
    np.where(
        (df['Minus_DI'] > df['Plus_DI']) & (df['ADX'] > 25),
        'STRONG_SELL',
        'NEUTRAL'
    )
)
```

### Williams %R

```python
willr = talib.WILLR(high_prices, low_prices, close_prices, timeperiod=14)
df['Williams_R'] = willr

df['WillR_Signal'] = np.where(df['Williams_R'] < -80, 'OVERSOLD',
                     np.where(df['Williams_R'] > -20, 'OVERBOUGHT', 'NEUTRAL'))
```

### CCI (Commodity Channel Index)

```python
cci = talib.CCI(high_prices, low_prices, close_prices, timeperiod=20)
df['CCI'] = cci

df['CCI_Signal'] = np.where(df['CCI'] < -100, 'OVERSOLD',
                   np.where(df['CCI'] > 100, 'OVERBOUGHT', 'NEUTRAL'))
```

---

## Volatility Indicators

### ATR (Average True Range)

```python
atr = talib.ATR(high_prices, low_prices, close_prices, timeperiod=14)
df['ATR'] = atr
df['ATR_Percent'] = (atr / close_prices) * 100

# Volatility classification
df['Volatility'] = np.where(df['ATR_Percent'] > 2, 'HIGH',
                   np.where(df['ATR_Percent'] > 1, 'MEDIUM', 'LOW'))

# ATR-based stop loss
df['Stop_Loss'] = df['close'] - (2 * df['ATR'])  # 2x ATR trailing stop
```

### Keltner Channel

```python
def keltner_channel(df, ema_period=20, atr_period=10, multiplier=2):
    """Calculate Keltner Channel."""
    ema = talib.EMA(df['close'].values, timeperiod=ema_period)
    atr = talib.ATR(df['high'].values, df['low'].values, df['close'].values, timeperiod=atr_period)

    upper = ema + (multiplier * atr)
    lower = ema - (multiplier * atr)

    return upper, ema, lower

df['KC_Upper'], df['KC_Middle'], df['KC_Lower'] = keltner_channel(df)
```

### Donchian Channel

```python
def donchian_channel(df, period=20):
    """Calculate Donchian Channel."""
    upper = df['high'].rolling(period).max()
    lower = df['low'].rolling(period).min()
    middle = (upper + lower) / 2
    return upper, middle, lower

df['DC_Upper'], df['DC_Middle'], df['DC_Lower'] = donchian_channel(df)

# Breakout signals
df['DC_Signal'] = np.where(df['close'] > df['DC_Upper'].shift(1), 'BREAKOUT_UP',
                  np.where(df['close'] < df['DC_Lower'].shift(1), 'BREAKOUT_DOWN', 'RANGE'))
```

---

## Volume Indicators

### On-Balance Volume (OBV)

```python
obv = talib.OBV(close_prices, volume.astype(float))
df['OBV'] = obv
df['OBV_SMA'] = talib.SMA(obv, timeperiod=20)

# OBV trend
df['OBV_Trend'] = np.where(df['OBV'] > df['OBV_SMA'], 'ACCUMULATION', 'DISTRIBUTION')
```

### Volume Weighted Average Price (VWAP)

```python
def vwap(df):
    """Calculate VWAP (intraday)."""
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    vwap = (typical_price * df['volume']).cumsum() / df['volume'].cumsum()
    return vwap

df['VWAP'] = vwap(df)
df['VWAP_Signal'] = np.where(df['close'] > df['VWAP'], 'ABOVE_VWAP', 'BELOW_VWAP')
```

### Money Flow Index (MFI)

```python
mfi = talib.MFI(high_prices, low_prices, close_prices, volume.astype(float), timeperiod=14)
df['MFI'] = mfi

df['MFI_Signal'] = np.where(df['MFI'] < 20, 'OVERSOLD',
                   np.where(df['MFI'] > 80, 'OVERBOUGHT', 'NEUTRAL'))
```

---

## Candlestick Patterns

### Pattern Recognition

```python
# Bullish patterns
df['HAMMER'] = talib.CDLHAMMER(open_prices, high_prices, low_prices, close_prices)
df['ENGULFING_BULL'] = talib.CDLENGULFING(open_prices, high_prices, low_prices, close_prices)
df['MORNING_STAR'] = talib.CDLMORNINGSTAR(open_prices, high_prices, low_prices, close_prices)
df['THREE_WHITE_SOLDIERS'] = talib.CDL3WHITESOLDIERS(open_prices, high_prices, low_prices, close_prices)
df['PIERCING'] = talib.CDLPIERCING(open_prices, high_prices, low_prices, close_prices)

# Bearish patterns
df['SHOOTING_STAR'] = talib.CDLSHOOTINGSTAR(open_prices, high_prices, low_prices, close_prices)
df['ENGULFING_BEAR'] = -talib.CDLENGULFING(open_prices, high_prices, low_prices, close_prices)
df['EVENING_STAR'] = talib.CDLEVENINGSTAR(open_prices, high_prices, low_prices, close_prices)
df['THREE_BLACK_CROWS'] = talib.CDL3BLACKCROWS(open_prices, high_prices, low_prices, close_prices)
df['DARK_CLOUD'] = talib.CDLDARKCLOUDCOVER(open_prices, high_prices, low_prices, close_prices)

# Doji patterns
df['DOJI'] = talib.CDLDOJI(open_prices, high_prices, low_prices, close_prices)
df['DRAGONFLY_DOJI'] = talib.CDLDRAGONFLYDOJI(open_prices, high_prices, low_prices, close_prices)
df['GRAVESTONE_DOJI'] = talib.CDLGRAVESTONEDOJI(open_prices, high_prices, low_prices, close_prices)
```

### All Patterns Scanner

```python
def scan_all_patterns(df):
    """Scan for all candlestick patterns."""
    pattern_functions = {
        'HAMMER': talib.CDLHAMMER,
        'INVERTED_HAMMER': talib.CDLINVERTEDHAMMER,
        'ENGULFING': talib.CDLENGULFING,
        'MORNING_STAR': talib.CDLMORNINGSTAR,
        'EVENING_STAR': talib.CDLEVENINGSTAR,
        'SHOOTING_STAR': talib.CDLSHOOTINGSTAR,
        'DOJI': talib.CDLDOJI,
        'SPINNING_TOP': talib.CDLSPINNINGTOP,
        'MARUBOZU': talib.CDLMARUBOZU,
        'HARAMI': talib.CDLHARAMI,
    }

    o, h, l, c = df['open'].values, df['high'].values, df['low'].values, df['close'].values

    patterns = {}
    for name, func in pattern_functions.items():
        result = func(o, h, l, c)
        if result[-1] != 0:  # Pattern detected on latest candle
            patterns[name] = 'BULLISH' if result[-1] > 0 else 'BEARISH'

    return patterns

latest_patterns = scan_all_patterns(df)
print(f"Detected patterns: {latest_patterns}")
```

---

## Trading Strategies

### RSI + MACD Strategy

```python
def rsi_macd_strategy(df):
    """Combined RSI and MACD strategy."""
    # Calculate indicators
    df['RSI'] = talib.RSI(df['close'].values, timeperiod=14)
    macd, signal, _ = talib.MACD(df['close'].values)
    df['MACD'] = macd
    df['MACD_Signal'] = signal

    # Generate signals
    buy_condition = (df['RSI'] < 30) & (df['MACD'] > df['MACD_Signal'])
    sell_condition = (df['RSI'] > 70) & (df['MACD'] < df['MACD_Signal'])

    df['Strategy_Signal'] = np.where(buy_condition, 'BUY',
                            np.where(sell_condition, 'SELL', 'HOLD'))

    return df

df = rsi_macd_strategy(df)
```

### Moving Average Crossover Strategy

```python
def ma_crossover_strategy(df, fast=9, slow=21):
    """EMA crossover strategy with trend filter."""
    df['EMA_Fast'] = talib.EMA(df['close'].values, timeperiod=fast)
    df['EMA_Slow'] = talib.EMA(df['close'].values, timeperiod=slow)
    df['EMA_200'] = talib.EMA(df['close'].values, timeperiod=200)

    # Crossover detection
    df['Cross_Up'] = (df['EMA_Fast'] > df['EMA_Slow']) & (df['EMA_Fast'].shift(1) <= df['EMA_Slow'].shift(1))
    df['Cross_Down'] = (df['EMA_Fast'] < df['EMA_Slow']) & (df['EMA_Fast'].shift(1) >= df['EMA_Slow'].shift(1))

    # Trend filter (only trade in direction of 200 EMA)
    df['Signal'] = np.where(
        df['Cross_Up'] & (df['close'] > df['EMA_200']),
        'BUY',
        np.where(
            df['Cross_Down'] & (df['close'] < df['EMA_200']),
            'SELL',
            'HOLD'
        )
    )

    return df
```

### Bollinger Band Squeeze Strategy

```python
def bb_squeeze_strategy(df):
    """Bollinger Band squeeze breakout strategy."""
    upper, middle, lower = talib.BBANDS(df['close'].values, timeperiod=20)
    df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = upper, middle, lower
    df['BB_Width'] = (upper - lower) / middle

    # Keltner Channel for squeeze detection
    kc_upper, kc_middle, kc_lower = keltner_channel(df)
    df['KC_Upper'], df['KC_Lower'] = kc_upper, kc_lower

    # Squeeze: BB inside KC
    df['Squeeze'] = (df['BB_Lower'] > df['KC_Lower']) & (df['BB_Upper'] < df['KC_Upper'])

    # Breakout after squeeze
    df['Squeeze_Release'] = df['Squeeze'].shift(1) & ~df['Squeeze']

    # Direction based on momentum
    mom = talib.MOM(df['close'].values, timeperiod=12)
    df['Signal'] = np.where(
        df['Squeeze_Release'] & (mom > 0),
        'BUY',
        np.where(
            df['Squeeze_Release'] & (mom < 0),
            'SELL',
            'HOLD'
        )
    )

    return df
```

---

## Complete Indicator Dashboard

```python
def calculate_all_indicators(df):
    """Calculate comprehensive indicator set."""
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    open_ = df['open'].values
    volume = df['volume'].values.astype(float)

    # Trend
    df['SMA_20'] = talib.SMA(close, 20)
    df['SMA_50'] = talib.SMA(close, 50)
    df['EMA_9'] = talib.EMA(close, 9)
    df['EMA_21'] = talib.EMA(close, 21)

    # Bollinger Bands
    df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = talib.BBANDS(close, 20)

    # Momentum
    df['RSI'] = talib.RSI(close, 14)
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = talib.MACD(close)
    df['Stoch_K'], df['Stoch_D'] = talib.STOCH(high, low, close)
    df['ADX'] = talib.ADX(high, low, close, 14)
    df['CCI'] = talib.CCI(high, low, close, 20)
    df['Williams_R'] = talib.WILLR(high, low, close, 14)
    df['MOM'] = talib.MOM(close, 10)
    df['ROC'] = talib.ROC(close, 10)

    # Volatility
    df['ATR'] = talib.ATR(high, low, close, 14)
    df['NATR'] = talib.NATR(high, low, close, 14)

    # Volume
    df['OBV'] = talib.OBV(close, volume)
    df['MFI'] = talib.MFI(high, low, close, volume, 14)
    df['AD'] = talib.AD(high, low, close, volume)

    return df

df = calculate_all_indicators(df)
```

---

## Notes

- TA-Lib requires the system library to be installed first
- All indicators return NaN for initial periods (warmup period)
- Use `dropna()` before making trading decisions
- Combine multiple indicators for confirmation
- Always backtest strategies before live trading
- Use OpenAlgo's Analyzer mode for paper trading
