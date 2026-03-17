---
name: crypto-ta-analyzer
description: Technical analysis with 29+ indicators (BB, Ichimoku, RSI, MACD). Generates 7-tier trading signals with divergence detection, volume confirmation, and squeeze alerts for crypto and stocks.
---

# Crypto & Stock Technical Analysis

Multi-indicator technical analysis system that generates high-confidence trading signals by combining 29+ proven algorithms. Features divergence detection, Bollinger Band squeeze alerts, volume confirmation, and a 7-tier signal system. Ideal for cryptocurrency and stock market analysis.

## Core Workflow

### 1. Data Acquisition

Fetch historical price data from any supported source:

**CoinGecko (via MCP tools):**
```
Use coingecko_get_historical_chart tool with:
- coin_id: Target cryptocurrency (e.g., 'bitcoin', 'ethereum')
- days: Time range ('7', '30', '90', '365', 'max')
- vs_currency: Base currency (default 'usd')
```

**Other Supported Sources:**
- Exchange APIs (Binance, Coinbase, etc.) - OHLCV format
- Yahoo Finance - Stock data
- Any price-only data - Automatic OHLC approximation

**Minimum Requirements**:
- At least 100 data points for reliable analysis (50 minimum)
- Price data required, volume recommended
- Recent data preferred for active trading signals

### 2. Convert Data to OHLCV Format

The generic data converter auto-detects and normalizes any supported format:

```python
from scripts.data_converter import normalize_ohlcv, validate_data_quality

# Auto-detect format and convert
ohlcv_df, metadata = normalize_ohlcv(raw_data, source="auto")

# Check conversion quality
print(f"Format detected: {metadata['detected_format']}")
print(f"Rows: {metadata['original_rows']} -> {metadata['final_rows']}")
print(f"Warnings: {metadata['warnings']}")

# Validate data quality
quality_report = validate_data_quality(ohlcv_df)
```

**Backward compatible** with old CoinGecko converter:
```python
from scripts.data_converter import prepare_analysis_data
ohlcv_df = prepare_analysis_data(coingecko_json_data)
```

### 3. Run Technical Analysis

Execute the analyzer with prepared data:

```python
from scripts.ta_analyzer import TechnicalAnalyzer
import json

# Initialize analyzer with OHLCV data
analyzer = TechnicalAnalyzer(ohlcv_df)

# Run comprehensive analysis
results = analyzer.analyze_all()

# Display results
print(json.dumps(results, indent=2))
```

### 4. Interpret Results

Analysis returns comprehensive data including new features:
```json
{
  "scoreTotal": 8.5,
  "tradeSignal": "STRONG_UPTREND",
  "tradeSignal7Tier": "STRONG_BUY",
  "tradeTrigger": true,
  "currentPrice": 45234.56,
  "priceChange24h": 3.45,
  "confidence": 0.75,
  "normalizedScore": 0.42,
  "volumeConfirmation": 0.85,
  "squeezeDetected": false,
  "divergences": {
    "RSI": "NONE",
    "MACD": "NONE",
    "OBV": "NONE"
  },
  "individualScores": {
    "RSI": 1.0,
    "MACD": 1.0,
    "BB": 0.75,
    "OBV": 0.8,
    "ICHIMOKU": 1.0,
    ...
  },
  "individualSignals": {
    "RSI": "BUY",
    "MACD": "BUY",
    "BB": "BUY",
    ...
  },
  "regime": {
    "regime": "TRENDING",
    "adx": 32.5,
    "dmiDirection": "UP"
  },
  "warnings": []
}
```

**7-Tier Signal System** (NEW):
- **STRONG_BUY**: High confidence bullish (normalized >= 0.5, confidence >= 0.7)
- **BUY**: Moderate confidence bullish (normalized >= 0.35, confidence >= 0.5)
- **WEAK_BUY**: Low confidence bullish (normalized >= 0.2)
- **NEUTRAL**: No clear direction
- **WEAK_SELL**: Low confidence bearish (normalized <= -0.2)
- **SELL**: Moderate confidence bearish (normalized <= -0.35, confidence >= 0.5)
- **STRONG_SELL**: High confidence bearish (normalized <= -0.5, confidence >= 0.7)

**Legacy Signal Interpretation** (backward compatible):
- **scoreTotal >= 7.0**: STRONG_UPTREND - High confidence bullish signal
- **scoreTotal 3.0-6.9**: NEUTRAL - Mixed signals, wait for clarity
- **scoreTotal < 3.0**: DOWNTREND - Bearish signal, avoid longs

**Divergence Types**:
- **BULLISH_DIV**: Price lower low + indicator higher low = potential reversal up
- **BEARISH_DIV**: Price higher high + indicator lower high = potential reversal down
- **HIDDEN_BULLISH**: Trend continuation signal in uptrend
- **HIDDEN_BEARISH**: Trend continuation signal in downtrend
- **NONE**: No divergence detected

## Available Indicators (29)

### Core Indicators (10) - Weight: 1.0
- **RSI** (Relative Strength Index) - Momentum oscillator with divergence detection
- **MACD** (Moving Average Convergence Divergence) - Trend-following momentum with divergence
- **BB** (Bollinger Bands) - NEW: Volatility bands with squeeze detection
- **OBV** (On-Balance Volume) - NEW: Volume-price divergence indicator
- **ICHIMOKU** (Ichimoku Cloud) - NEW: Multi-component trend system (crypto-optimized 10/30/60)
- **EMA** (Exponential Moving Average) - Short/long crossover
- **SMA** (Simple Moving Average) - Short/long crossover
- **MFI** (Money Flow Index) - Volume-weighted RSI
- **KDJ** (Stochastic with J line) - Overbought/oversold with momentum
- **SAR** (Parabolic SAR) - Trend reversal detection

### Strong Indicators (5) - Weight: 0.75
- **DEMA** (Double Exponential MA) - Reduced lag moving average
- **MESA** (MESA Adaptive MA) - Ehlers Hilbert Transform based
- **CCI** (Commodity Channel Index) - Cyclical trend identification
- **AROON** - Trend timing indicator
- **APO** (Absolute Price Oscillator) - Trend strength

### Supporting Indicators (14) - Weight: 0.5
- **ADX** (Average Directional Index) - Trend strength
- **DMI** (Directional Movement Index) - Trend direction
- **CMO** (Chande Momentum Oscillator) - Modified RSI
- **KAMA** (Kaufman Adaptive MA) - Volatility-adjusted MA
- **MOMI** (Momentum) - Rate of price change
- **PPO** (Percentage Price Oscillator) - Normalized MACD
- **ROC** (Rate of Change) - Percentage momentum
- **TRIMA** (Triangular MA) - Smoothed moving average
- **TRIX** (Triple Exponential MA) - Smoothed momentum
- **T3** (Tillson T3) - Low-lag smooth MA
- **WMA** (Weighted MA) - Linearly weighted
- **VWAP** (Volume Weighted Average Price) - NEW: Institutional reference
- **ATR_SIGNAL** (ATR Volatility Signal) - NEW: Volatility-based signals
- **CAD** (CMO with Regime-Aware Mean Reversion) - Adaptive momentum

See [references/indicators.md](references/indicators.md) for detailed indicator explanations.

## Usage Patterns

### Quick Analysis
For rapid assessment of a single cryptocurrency:

```
1. Call coingecko_get_historical_chart for target coin (7-30 days)
2. Convert data using coingecko_converter
3. Run ta_analyzer.analyze_all()
4. Present scoreTotal and tradeSignal to user
```

### Comparative Analysis
To compare multiple cryptocurrencies:

```
1. Call coingecko_compare_coins for target coins
2. For each coin:
   - Fetch historical chart data
   - Run technical analysis
   - Store results
3. Create comparison table with scores and signals
4. Identify strongest/weakest performers
```

### Deep Dive Analysis
For comprehensive assessment with context:

```
1. Fetch multiple timeframes (7d, 30d, 90d)
2. Run analysis on each timeframe
3. Check for signal agreement across timeframes
4. Review individual indicator signals for divergences
5. Cross-reference with market data (market cap, volume, dominance)
6. Provide detailed report with confidence levels
```

### Trend Monitoring
For ongoing market surveillance:

```
1. Fetch current data for watchlist
2. Run analysis on all coins
3. Filter for STRONG_UPTREND signals (score >= 7)
4. Rank by score descending
5. Present top opportunities with context
```

## Best Practices

### Data Quality
- **Always validate** data quality before analysis using validate_data_quality()
- Ensure minimum 100 data points (preferably 200+)
- Check for missing values or data gaps
- Use appropriate timeframe for user's trading strategy

### Interpretation Guidelines
- **Never rely on single indicator** - the power is in consensus
- **Consider market context** - indicators behave differently in trending vs ranging markets
- **Watch for divergences** - when price contradicts indicators, reversal may be coming
- **Volume confirms price** - MFI provides crucial validation
- **Multiple timeframes** - confirm signals across different periods

### Common Patterns

**High Conviction Bullish** (STRONG_BUY):
- 7-tier signal: STRONG_BUY or BUY
- Confidence >= 0.7
- RSI between 30-70 (not overbought)
- MACD bullish crossover
- Price above Ichimoku cloud
- OBV confirms with no bearish divergence
- Volume confirmation >= 0.7
- ADX > 25 (strong trend)

**Breakout Setup**:
- Bollinger Band squeeze detected (squeezeDetected: true)
- ADX rising from < 20
- Volume starting to increase
- Watch for band expansion

**Trend Exhaustion Warning**:
- Score > 7 BUT RSI > 80 or MFI > 90
- Bearish divergence on RSI, MACD, or OBV
- Price above Bollinger upper band (%B > 1.0)
- Potential reversal or pullback incoming

**Divergence-Based Reversal**:
- Bearish divergence: Prepare for potential top
- Bullish divergence: Watch for potential bottom
- OBV divergence is most reliable (volume precedes price)

**False Breakout**:
- Strong price move BUT ADX < 20
- Low volume (volumeConfirmation < 0.5)
- OBV not confirming price move
- Likely whipsaw or temporary spike

**Ichimoku Confirmation**:
- Price above cloud + Tenkan above Kijun = Strong bullish
- Price below cloud + Tenkan below Kijun = Strong bearish
- Price inside cloud = No-trade zone, wait for clarity

## Limitations

### CoinGecko Data Considerations
- CoinGecko provides price points, not true OHLC bars
- Converter approximates OHLC from adjacent prices
- Works well for trend analysis, less precise for intraday patterns

### Indicator Nature
- Most indicators are **lagging** - calculated from past data
- Can generate **whipsaws** in choppy, sideways markets
- **Overfitting risk** - too many indicators can cause analysis paralysis
- Market regime changes require adaptation

### Recommended Use Cases
✅ **Great for**: Trend identification, medium-term signals, portfolio screening  
✅ **Good for**: Entry/exit timing, risk assessment, comparative analysis  
⚠️ **Limited for**: High-frequency trading, precise intraday timing, ranging markets  
❌ **Avoid for**: News-driven moves, low-liquidity coins, extreme volatility events

## Advanced Techniques

### Custom Scoring Weights
Modify indicator weights based on market conditions:
- **Trending markets**: Increase weight of MACD, EMA, ADX
- **Ranging markets**: Increase weight of RSI, CCI, Stochastic
- **High volatility**: Increase weight of SAR, KAMA (adaptive indicators)

### Multi-Timeframe Confirmation
Analyze same coin across multiple timeframes:
```
- 7 days (short-term trend)
- 30 days (medium-term trend)  
- 90 days (long-term trend)
```

Strongest signals occur when all timeframes agree.

### Sector Analysis
Analyze multiple coins in same sector to identify:
- Sector-wide trends vs individual coin movements
- Relative strength leaders
- Laggard coins with catch-up potential

## Troubleshooting

### Issue: Score stuck at 0 or very low
**Cause**: Insufficient data or flat price action  
**Solution**: Fetch longer historical period or check data quality

### Issue: Conflicting signals across indicators
**Cause**: Market in transition or ranging  
**Solution**: Score will be neutral - wait for clearer direction

### Issue: High score but bearish user intuition
**Cause**: Indicators lag price, or news-driven move  
**Solution**: Cross-reference with market context, recent news, volume

### Issue: Analysis fails with NaN values
**Cause**: Insufficient data for indicator calculation  
**Solution**: Fetch minimum 100 data points, preferably 200+

## Integration with CoinGecko MCP

This skill is designed to work seamlessly with CoinGecko MCP tools:

**Primary Tools Used**:
- `coingecko_get_historical_chart` - Main data source
- `coingecko_get_price` - Quick current price checks
- `coingecko_compare_coins` - Multi-coin analysis
- `coingecko_get_market_data` - Context and validation

**Workflow Integration**:
1. User asks about a cryptocurrency
2. Use CoinGecko tools to fetch data
3. Convert to OHLCV format
4. Run technical analysis
5. Present results with context from market data

## Example Outputs

### Simple Analysis Response
```
Bitcoin Technical Analysis (7-day period)

📊 7-Tier Signal: STRONG_BUY
🎯 Confidence: 78%
💰 Current Price: $45,234.56 (+3.45% 24h)
📈 Volume Confirmation: 85%

Key Indicators:
✅ RSI: BUY (38.2 - healthy level, no divergence)
✅ MACD: BUY (bullish crossover, no divergence)
✅ Bollinger: BUY (price near upper band, no squeeze)
✅ OBV: BUY (volume confirms trend, no divergence)
✅ Ichimoku: BUY (price above cloud)
✅ Volume: ACCUMULATION (MFI bullish)

Warnings: None

Recommendation: Strong buy signal with volume confirmation.
No divergences or overbought conditions detected.
```

### Comparative Analysis Response
```
Top 5 Cryptocurrencies by Technical Score (30-day analysis)

1. Solana (SOL): 9.0 - STRONG_UPTREND
   - All momentum indicators bullish
   - Strong volume confirmation
   
2. Ethereum (ETH): 7.5 - STRONG_UPTREND
   - Trending higher, minor overbought warning
   
3. Bitcoin (BTC): 5.0 - NEUTRAL
   - Consolidating after recent move
   
4. Cardano (ADA): 2.5 - DOWNTREND
   - Multiple bearish signals
   
5. XRP: 1.0 - DOWNTREND
   - Weak momentum and volume
```

## Related Resources

- **Indicator Details**: See [references/indicators.md](references/indicators.md)
- **Core Analysis Engine**: [scripts/ta_analyzer.py](scripts/ta_analyzer.py)
- **Data Converter**: [scripts/coingecko_converter.py](scripts/coingecko_converter.py)
