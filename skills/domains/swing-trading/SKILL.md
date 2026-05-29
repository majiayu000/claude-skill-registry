---
name: minervini-swing-trading
description: Trade swing setups in the style of Mark Minervini, 3x US Investing Champion with 220%+ annual returns. Emphasizes SEPA methodology, trend templates, volatility contraction patterns (VCP), and strict risk management. Use when swing trading momentum stocks, identifying breakout setups, or building systematic trend-following strategies.
---

# Mark Minervini Swing Trading Style Guide

## Overview

Mark Minervini is a 3-time US Investing Champion who turned $100,000 into over $30 million. His SEPA (Specific Entry Point Analysis) methodology combines trend analysis, volatility contraction patterns, and strict risk management into a repeatable system. He emphasizes buying leading stocks at specific low-risk entry points within confirmed uptrends.

## Core Philosophy

> "The goal is not to buy low and sell high. It's to buy high and sell higher."

> "Risk management is not about avoiding losses—it's about keeping losses small so you can stay in the game."

> "I don't buy stocks that are going up. I buy stocks that are going up the right way."

Minervini believes that most of the money in the stock market is made in the middle of a move, not at the bottom. By waiting for stocks to prove themselves in a Stage 2 uptrend, you trade with the trend while managing risk through precise entries.

## Design Principles

1. **Trend First**: Only buy stocks in a confirmed Stage 2 uptrend.

2. **Specific Entry Points**: Enter at low-risk pivot points, not randomly.

3. **Volatility Contraction**: Tightening price action precedes explosive moves.

4. **Cut Losses Quickly**: 7-8% maximum loss, often tighter.

5. **Let Winners Run**: Sell strength, not weakness.

## The Trend Template (8 Criteria)

A stock MUST pass ALL 8 criteria before consideration:

```
1. Current price > 150-day MA
2. Current price > 200-day MA
3. 150-day MA > 200-day MA
4. 200-day MA trending up for at least 1 month (ideally 4-5 months)
5. 50-day MA > 150-day MA AND 50-day MA > 200-day MA
6. Current price > 50-day MA
7. Current price at least 25% above 52-week low
8. Current price within 25% of 52-week high (ideally within 15%)
```

**Stage Analysis:**
- **Stage 1**: Basing/accumulation (avoid)
- **Stage 2**: Advancing/uptrend (BUY ZONE)
- **Stage 3**: Topping/distribution (avoid)
- **Stage 4**: Declining/downtrend (avoid)

## Volatility Contraction Pattern (VCP)

The VCP is Minervini's signature setup:

```
VCP Structure:
                    
Price    T1
  |      /\
  |     /  \   T2
  |    /    \ /\   T3
  |   /      X  \ /\    Pivot
  |  /       |   X  \  /----→ BREAKOUT
  | /        |   |   \/
  |/         |   |    
  Base       C1  C2   C3 (contractions tighten)

T = Thrust (price expansion)
C = Contraction (price tightening)
```

**VCP Characteristics:**
- Minimum 2 contractions, ideally 3-4
- Each contraction is SHALLOWER than the previous
- Contractions: 1st: 20-35%, 2nd: 10-20%, 3rd: 5-15%, 4th: 3-8%
- Volume DECREASES during contractions (supply drying up)
- Volume INCREASES on breakout (demand returning)

## When Swing Trading

### Always

- Confirm stock passes ALL 8 trend template criteria
- Wait for a proper VCP or constructive base
- Enter on breakout above pivot with volume surge (50%+ above average)
- Set stop at 7-8% maximum (tighter if possible based on structure)
- Have a sell plan BEFORE you enter
- Trade liquid stocks (avg volume > 400K)

### Never

- Buy a stock in Stage 1, 3, or 4
- Chase extended stocks (>10% above pivot)
- Average down on a losing position
- Hold through an 8%+ loss
- Buy on light volume breakouts
- Ignore relative strength vs market

### Prefer

- Stocks with RS Rating > 85 (top 15% performers)
- EPS growth > 25% recent quarters
- Tight consolidations (VCP) over wide-and-loose bases
- Breakouts from IPO bases or first Stage 2 breakouts
- Industry group strength (top 20% of groups)
- Institutional accumulation (up weeks on volume)

## Code Patterns

### Trend Template Scanner

```python
class TrendTemplateScanner:
    """
    Minervini Trend Template: all 8 criteria must pass.
    This is the first filter—non-negotiable.
    """
    
    def check_trend_template(self, 
                              df: pd.DataFrame,
                              min_200ma_uptrend_days: int = 22) -> TrendTemplateResult:
        """
        Check if stock passes all 8 trend template criteria.
        """
        close = df['close']
        
        # Calculate moving averages
        ma_50 = close.rolling(50).mean()
        ma_150 = close.rolling(150).mean()
        ma_200 = close.rolling(200).mean()
        
        current_price = close.iloc[-1]
        current_50ma = ma_50.iloc[-1]
        current_150ma = ma_150.iloc[-1]
        current_200ma = ma_200.iloc[-1]
        
        # 52-week high/low
        high_52w = close.rolling(252).max().iloc[-1]
        low_52w = close.rolling(252).min().iloc[-1]
        
        # Check 200-day MA trend
        ma_200_month_ago = ma_200.iloc[-min_200ma_uptrend_days]
        ma_200_trending_up = current_200ma > ma_200_month_ago
        
        criteria = {
            '1_price_above_150ma': current_price > current_150ma,
            '2_price_above_200ma': current_price > current_200ma,
            '3_150ma_above_200ma': current_150ma > current_200ma,
            '4_200ma_trending_up': ma_200_trending_up,
            '5_50ma_above_150_and_200': (current_50ma > current_150ma) and (current_50ma > current_200ma),
            '6_price_above_50ma': current_price > current_50ma,
            '7_price_25pct_above_52w_low': current_price >= low_52w * 1.25,
            '8_price_within_25pct_of_52w_high': current_price >= high_52w * 0.75,
        }
        
        all_pass = all(criteria.values())
        
        return TrendTemplateResult(
            passes=all_pass,
            criteria=criteria,
            stage=self.determine_stage(df, criteria),
            price=current_price,
            ma_50=current_50ma,
            ma_150=current_150ma,
            ma_200=current_200ma,
            pct_from_52w_high=(current_price - high_52w) / high_52w * 100,
            pct_from_52w_low=(current_price - low_52w) / low_52w * 100
        )
    
    def determine_stage(self, df: pd.DataFrame, criteria: dict) -> int:
        """
        Determine Weinstein Stage (1-4).
        """
        if all(criteria.values()):
            return 2  # Stage 2 uptrend
        
        close = df['close']
        ma_200 = close.rolling(200).mean()
        
        # Stage 4: Price below declining 200 MA
        if close.iloc[-1] < ma_200.iloc[-1] and ma_200.iloc[-1] < ma_200.iloc[-22]:
            return 4
        
        # Stage 3: Price near/below flattening 200 MA
        if close.iloc[-1] < ma_200.iloc[-1] * 1.05:
            return 3
        
        # Stage 1: Basing
        return 1
    
    def scan_universe(self, 
                      symbols: List[str], 
                      data: Dict[str, pd.DataFrame]) -> List[TrendTemplateResult]:
        """
        Scan universe for stocks passing trend template.
        """
        results = []
        
        for symbol in symbols:
            df = data[symbol]
            if len(df) < 200:  # Need enough history
                continue
            
            result = self.check_trend_template(df)
            result.symbol = symbol
            
            if result.passes:
                results.append(result)
        
        # Sort by proximity to 52-week high (tighter = better)
        return sorted(results, key=lambda x: x.pct_from_52w_high, reverse=True)
```

### VCP Pattern Detector

```python
class VCPDetector:
    """
    Volatility Contraction Pattern detection.
    The tighter the contractions, the more explosive the breakout.
    """
    
    def __init__(self, 
                 min_contractions: int = 2,
                 max_first_contraction: float = 0.35,
                 contraction_ratio: float = 0.6):
        self.min_contractions = min_contractions
        self.max_first_contraction = max_first_contraction
        self.contraction_ratio = contraction_ratio  # Each contraction should be this % of previous
    
    def detect_vcp(self, df: pd.DataFrame) -> VCPResult:
        """
        Detect VCP pattern in price data.
        """
        close = df['close']
        high = df['high']
        low = df['low']
        volume = df['volume']
        
        # Find recent high (potential left side of base)
        lookback = 60  # ~3 months
        recent_high_idx = high.iloc[-lookback:].idxmax()
        recent_high = high.loc[recent_high_idx]
        
        # Find contractions from that high
        contractions = self.find_contractions(df, recent_high_idx)
        
        if len(contractions) < self.min_contractions:
            return VCPResult(valid=False, reason="Insufficient contractions")
        
        # Validate contraction depths are decreasing
        if not self.validate_contraction_depths(contractions):
            return VCPResult(valid=False, reason="Contractions not tightening")
        
        # Check volume pattern (should decrease during base)
        if not self.validate_volume_pattern(df, recent_high_idx):
            return VCPResult(valid=False, reason="Volume not contracting")
        
        # Calculate pivot point
        pivot = self.calculate_pivot(df, contractions)
        
        # Calculate tightness score (lower is better)
        tightness = contractions[-1]['depth']
        
        return VCPResult(
            valid=True,
            contractions=contractions,
            pivot_price=pivot,
            tightness_pct=tightness * 100,
            base_length_days=(df.index[-1] - df.index[recent_high_idx]).days,
            volume_dry_up=self.calculate_volume_dryup(df, recent_high_idx)
        )
    
    def find_contractions(self, 
                          df: pd.DataFrame, 
                          start_idx) -> List[dict]:
        """
        Find swing high/low contractions from start point.
        """
        high = df['high']
        low = df['low']
        
        contractions = []
        current_high = high.loc[start_idx]
        
        # Walk forward finding contractions
        subset = df.loc[start_idx:]
        
        i = 0
        while i < len(subset) - 5:
            # Find next swing low
            window = subset.iloc[i:i+10]
            swing_low_idx = window['low'].idxmin()
            swing_low = window['low'].loc[swing_low_idx]
            
            # Find next swing high after that
            remaining = subset.loc[swing_low_idx:]
            if len(remaining) < 5:
                break
            
            next_window = remaining.iloc[:10]
            swing_high_idx = next_window['high'].idxmax()
            swing_high = next_window['high'].loc[swing_high_idx]
            
            depth = (current_high - swing_low) / current_high
            
            contractions.append({
                'high': current_high,
                'low': swing_low,
                'depth': depth,
                'high_date': start_idx if len(contractions) == 0 else swing_high_idx,
                'low_date': swing_low_idx
            })
            
            current_high = swing_high
            i = subset.index.get_loc(swing_high_idx) - subset.index.get_loc(subset.index[0])
            i += 1
        
        return contractions
    
    def validate_contraction_depths(self, contractions: List[dict]) -> bool:
        """
        Each contraction should be shallower than the previous.
        """
        for i in range(1, len(contractions)):
            if contractions[i]['depth'] >= contractions[i-1]['depth'] * 1.1:  # Allow 10% tolerance
                return False
        return True
    
    def validate_volume_pattern(self, df: pd.DataFrame, start_idx) -> bool:
        """
        Volume should decrease during the base formation.
        """
        volume = df['volume']
        subset = volume.loc[start_idx:]
        
        if len(subset) < 20:
            return False
        
        first_half_avg = subset.iloc[:len(subset)//2].mean()
        second_half_avg = subset.iloc[len(subset)//2:].mean()
        
        return second_half_avg < first_half_avg * 0.9  # Volume should be lower
    
    def calculate_pivot(self, df: pd.DataFrame, contractions: List[dict]) -> float:
        """
        Pivot is the high of the last contraction.
        """
        if not contractions:
            return df['high'].iloc[-20:].max()
        
        return contractions[-1]['high']
    
    def calculate_volume_dryup(self, df: pd.DataFrame, start_idx) -> float:
        """
        How much has volume dried up during the base?
        """
        volume = df['volume']
        avg_volume_before = volume.loc[:start_idx].iloc[-20:].mean()
        recent_volume = volume.iloc[-5:].mean()
        
        return (avg_volume_before - recent_volume) / avg_volume_before
```

### Entry and Risk Management

```python
class MinerviniTradeManager:
    """
    Entry, position sizing, and risk management per Minervini rules.
    """
    
    def __init__(self, 
                 account_size: float,
                 max_risk_per_trade: float = 0.01,  # 1%
                 max_position_pct: float = 0.25):    # 25% max single position
        self.account = account_size
        self.risk_per_trade = max_risk_per_trade
        self.max_position = max_position_pct
    
    def calculate_entry(self, 
                        vcp: VCPResult, 
                        current_price: float) -> EntryPlan:
        """
        Calculate entry point and buy zone.
        """
        pivot = vcp.pivot_price
        
        # Buy zone: pivot to 5% above pivot
        buy_zone_low = pivot
        buy_zone_high = pivot * 1.05
        
        # Is current price in buy zone?
        in_buy_zone = buy_zone_low <= current_price <= buy_zone_high
        
        # Extended if >5% above pivot
        extended = current_price > buy_zone_high
        
        return EntryPlan(
            pivot_price=pivot,
            buy_zone=(buy_zone_low, buy_zone_high),
            current_price=current_price,
            in_buy_zone=in_buy_zone,
            extended=extended,
            pct_above_pivot=(current_price - pivot) / pivot * 100
        )
    
    def calculate_stop(self, 
                       entry_price: float, 
                       vcp: VCPResult,
                       max_stop_pct: float = 0.08) -> StopPlan:
        """
        Calculate stop loss based on chart structure.
        Minervini: max 7-8%, but tighter if structure allows.
        """
        # Option 1: Below the last contraction low
        structure_stop = vcp.contractions[-1]['low'] * 0.99  # 1% below
        structure_stop_pct = (entry_price - structure_stop) / entry_price
        
        # Option 2: Fixed percentage
        fixed_stop = entry_price * (1 - max_stop_pct)
        
        # Use tighter of the two
        if structure_stop_pct <= max_stop_pct:
            stop_price = structure_stop
            stop_type = 'STRUCTURE'
        else:
            stop_price = fixed_stop
            stop_type = 'FIXED_PCT'
        
        return StopPlan(
            stop_price=stop_price,
            stop_pct=(entry_price - stop_price) / entry_price * 100,
            stop_type=stop_type,
            structure_stop=structure_stop,
            fixed_stop=fixed_stop
        )
    
    def calculate_position_size(self, 
                                 entry_price: float, 
                                 stop_price: float) -> PositionSize:
        """
        Position sizing based on risk.
        """
        risk_amount = self.account * self.risk_per_trade
        risk_per_share = entry_price - stop_price
        
        # Shares based on risk
        shares_by_risk = int(risk_amount / risk_per_share)
        
        # Max position check
        max_shares = int(self.account * self.max_position / entry_price)
        
        final_shares = min(shares_by_risk, max_shares)
        
        return PositionSize(
            shares=final_shares,
            position_value=final_shares * entry_price,
            position_pct=final_shares * entry_price / self.account * 100,
            risk_dollars=final_shares * risk_per_share,
            risk_pct=final_shares * risk_per_share / self.account * 100,
            limited_by='RISK' if shares_by_risk < max_shares else 'MAX_POSITION'
        )
    
    def create_trade_plan(self, 
                          symbol: str,
                          df: pd.DataFrame,
                          vcp: VCPResult) -> TradePlan:
        """
        Complete trade plan with entry, stop, and targets.
        """
        current_price = df['close'].iloc[-1]
        
        entry = self.calculate_entry(vcp, current_price)
        stop = self.calculate_stop(entry.pivot_price, vcp)
        position = self.calculate_position_size(entry.pivot_price, stop.stop_price)
        
        # Profit targets
        risk = entry.pivot_price - stop.stop_price
        target_1 = entry.pivot_price + (risk * 2)   # 2:1
        target_2 = entry.pivot_price + (risk * 3)   # 3:1
        target_3 = entry.pivot_price * 1.20         # 20% move
        
        return TradePlan(
            symbol=symbol,
            entry=entry,
            stop=stop,
            position=position,
            targets={
                '2R': target_1,
                '3R': target_2,
                '20%': target_3
            },
            risk_reward_ratio=2.0,  # Minimum acceptable
            breakout_volume_required=df['volume'].rolling(50).mean().iloc[-1] * 1.5
        )
```

### Sell Rules

```python
class MinerviniSellRules:
    """
    Minervini's selling discipline: protect gains, cut losses.
    """
    
    def check_sell_signals(self, 
                           trade: ActiveTrade,
                           df: pd.DataFrame) -> List[SellSignal]:
        """
        Check all sell rules and return triggered signals.
        """
        signals = []
        current_price = df['close'].iloc[-1]
        
        # 1. STOP LOSS (mandatory)
        if current_price <= trade.stop_price:
            signals.append(SellSignal(
                type='STOP_LOSS',
                priority=1,
                action='SELL_ALL',
                reason=f'Price {current_price:.2f} hit stop {trade.stop_price:.2f}'
            ))
        
        # 2. Climax top (sell into strength)
        if self.detect_climax_top(df, trade):
            signals.append(SellSignal(
                type='CLIMAX_TOP',
                priority=2,
                action='SELL_HALF',
                reason='Climactic price/volume action'
            ))
        
        # 3. Break of 50-day MA after extended run
        if self.check_50ma_break(df, trade):
            signals.append(SellSignal(
                type='50MA_BREAK',
                priority=3,
                action='SELL_HALF',
                reason='Closed below 50-day MA after extended move'
            ))
        
        # 4. Lower low after lower high (trend change)
        if self.detect_lower_low(df):
            signals.append(SellSignal(
                type='TREND_CHANGE',
                priority=2,
                action='SELL_ALL',
                reason='Lower high followed by lower low'
            ))
        
        # 5. Holding period too long without progress
        if self.check_stalled_trade(trade, current_price):
            signals.append(SellSignal(
                type='TIME_STOP',
                priority=4,
                action='REVIEW',
                reason='Position stalled for 3+ weeks'
            ))
        
        return sorted(signals, key=lambda x: x.priority)
    
    def detect_climax_top(self, df: pd.DataFrame, trade: ActiveTrade) -> bool:
        """
        Climax top: largest single-day gain on highest volume.
        Often signals exhaustion.
        """
        close = df['close']
        volume = df['volume']
        
        # Recent daily returns
        daily_return = close.pct_change().iloc[-1]
        avg_return = close.pct_change().iloc[-50:].mean()
        
        # Volume comparison
        current_volume = volume.iloc[-1]
        avg_volume = volume.rolling(50).mean().iloc[-1]
        
        # Climax: big up day (>2x average return) on huge volume (>2x average)
        is_climax = (daily_return > avg_return * 3) and (current_volume > avg_volume * 2)
        
        # Only matters if we're already up significantly
        current_gain = (close.iloc[-1] - trade.entry_price) / trade.entry_price
        
        return is_climax and current_gain > 0.20
    
    def check_50ma_break(self, df: pd.DataFrame, trade: ActiveTrade) -> bool:
        """
        Close below 50 MA after being extended above it.
        """
        close = df['close']
        ma_50 = close.rolling(50).mean()
        
        current_price = close.iloc[-1]
        current_50ma = ma_50.iloc[-1]
        
        # Was extended above 50 MA?
        max_extension = ((close.iloc[-20:] - ma_50.iloc[-20:]) / ma_50.iloc[-20:]).max()
        
        return current_price < current_50ma and max_extension > 0.10
    
    def detect_lower_low(self, df: pd.DataFrame) -> bool:
        """
        Lower high followed by lower low = potential trend change.
        """
        high = df['high']
        low = df['low']
        
        # Find recent swing points
        recent_high_1 = high.iloc[-20:-10].max()
        recent_high_2 = high.iloc[-10:].max()
        recent_low_1 = low.iloc[-20:-10].min()
        recent_low_2 = low.iloc[-10:].min()
        
        lower_high = recent_high_2 < recent_high_1
        lower_low = recent_low_2 < recent_low_1
        
        return lower_high and lower_low
    
    def check_stalled_trade(self, 
                            trade: ActiveTrade, 
                            current_price: float,
                            max_stall_days: int = 15) -> bool:
        """
        Position going nowhere for too long.
        """
        days_held = (datetime.now() - trade.entry_date).days
        gain_pct = (current_price - trade.entry_price) / trade.entry_price
        
        # Stalled: held >15 days with <5% gain
        return days_held > max_stall_days and gain_pct < 0.05
```

## Mental Model

Minervini approaches swing trading by asking:

1. **Is it Stage 2?** If not, skip it entirely
2. **Is there a proper base?** VCP or constructive pattern
3. **Where's the pivot?** Specific entry point with defined risk
4. **What's my risk?** Stop before entry, always
5. **Am I early or late?** Only buy in the buy zone, never extended

## The Trade Checklist

```
□ Stock passes ALL 8 trend template criteria
□ VCP or proper base pattern identified
□ Volume declining during base (supply dried up)
□ Pivot point clearly defined
□ Entry within 5% of pivot (not extended)
□ Stop loss set (max 7-8%, tighter if possible)
□ Position sized to 1% account risk
□ Volume surge on breakout (50%+ above average)
□ RS Rating > 80 (top performers)
□ EPS growth positive and accelerating
```

## Signature Minervini Moves

- Trend Template (8 criteria filter)
- Volatility Contraction Pattern (VCP)
- Stage 2 only (never Stage 1, 3, or 4)
- Buy at pivot, not before
- 7-8% maximum stop loss
- Sell into strength (climax tops)
- Position sizing by risk
- Volume confirmation on breakout
