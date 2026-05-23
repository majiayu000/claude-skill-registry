---
name: aqr-factor-investing
description: Build investment systems in the style of AQR Capital Management, the quantitative investment firm pioneering factor investing. Emphasizes academic rigor, transparent methodology, and systematic factor exposure. Use when building factor models, conducting asset pricing research, or designing systematic portfolios.
---

# AQR Capital Management Style Guide

## Overview

AQR (Applied Quantitative Research), founded by Cliff Asness and other academics from Goldman Sachs, is a quantitative investment firm managing ~$100B. Known for bringing academic factor research to practical investing, they emphasize transparency, rigorous methodology, and the democratization of quantitative techniques.

## Core Philosophy

> "The best ideas in finance come from rigorous academic research, not from Wall Street intuition."

> "Factors work because of risk, behavior, or structure—understand which before you invest."

> "If you can't explain it simply, you don't understand it well enough."

AQR believes that systematic factors (value, momentum, quality, etc.) represent persistent sources of returns that can be harvested through disciplined implementation. They emphasize understanding *why* strategies work, not just *that* they work.

## Design Principles

1. **Academic Foundation**: Start with peer-reviewed research.

2. **Factor Discipline**: Stick to factors with economic rationale.

3. **Transparency**: Publish methodology, admit mistakes.

4. **Diversification**: Across factors, geographies, and asset classes.

5. **Implementation Matters**: Transaction costs can kill paper returns.

## When Building Factor Strategies

### Always

- Ground strategies in academic research
- Understand the economic rationale (risk, behavioral, structural)
- Test across multiple time periods and geographies
- Account for realistic transaction costs
- Combine multiple factors for diversification
- Construct factors to be investment-grade (liquidity, capacity)

### Never

- Chase factors discovered through data mining
- Ignore the implementation gap (paper vs. real returns)
- Assume factor premia are stable over time
- Concentrate in single factors or markets
- Forget about factor crowding
- Trade more than necessary

### Prefer

- Composite factors over single metrics
- Long-short over long-only for pure factor exposure
- Equal-risk weighting over equal-dollar weighting
- Gradual rebalancing over discrete trading
- Transaction cost-aware optimization
- Factor timing skepticism

## Code Patterns

### Factor Construction

```python
class FactorBuilder:
    """
    AQR-style factor construction: robust, diversified, investment-grade.
    """
    
    def __init__(self, data_provider):
        self.data = data_provider
    
    def build_value_factor(self, 
                           universe: List[str],
                           date: date) -> pd.Series:
        """
        Value factor: composite of multiple value metrics.
        AQR uses book/price, earnings/price, forecast earnings/price, etc.
        """
        metrics = {}
        
        # Book to Price (classic Fama-French)
        metrics['book_to_price'] = self.data.get_fundamentals(
            universe, 'book_value', date
        ) / self.data.get_prices(universe, date)
        
        # Earnings to Price
        metrics['earnings_to_price'] = self.data.get_fundamentals(
            universe, 'trailing_earnings', date
        ) / self.data.get_prices(universe, date)
        
        # Forward Earnings to Price (analyst estimates)
        metrics['forward_ep'] = self.data.get_fundamentals(
            universe, 'forward_earnings', date
        ) / self.data.get_prices(universe, date)
        
        # Cash Flow to Price
        metrics['cf_to_price'] = self.data.get_fundamentals(
            universe, 'operating_cf', date
        ) / self.data.get_prices(universe, date)
        
        # Composite: z-score and average
        composite = pd.DataFrame(metrics)
        z_scores = composite.apply(lambda x: self.winsorize_and_zscore(x), axis=0)
        
        return z_scores.mean(axis=1)
    
    def build_momentum_factor(self,
                               universe: List[str],
                               date: date) -> pd.Series:
        """
        Momentum: 12-month return, skipping most recent month.
        Classic Jegadeesh-Titman with AQR refinements.
        """
        # 12-1 momentum (skip last month to avoid reversal)
        prices = self.data.get_price_history(universe, date, lookback_months=13)
        
        # Return from t-12 to t-1
        momentum_12_1 = prices.iloc[-22] / prices.iloc[0] - 1  # Skip last month
        
        # AQR enhancement: also consider intermediate momentum
        momentum_6_1 = prices.iloc[-22] / prices.iloc[-132] - 1
        
        # Industry-adjusted (avoid sector bets)
        industries = self.data.get_industries(universe)
        mom_adj = momentum_12_1.groupby(industries).transform(
            lambda x: x - x.mean()
        )
        
        return self.winsorize_and_zscore(mom_adj)
    
    def build_quality_factor(self,
                              universe: List[str],
                              date: date) -> pd.Series:
        """
        Quality: profitability, stability, and financial health.
        Based on AQR's "Quality Minus Junk" research.
        """
        profitability = self.calculate_profitability(universe, date)
        growth = self.calculate_growth_stability(universe, date)
        safety = self.calculate_safety(universe, date)
        payout = self.calculate_payout(universe, date)
        
        # Composite quality score
        quality = pd.DataFrame({
            'profitability': self.winsorize_and_zscore(profitability),
            'growth': self.winsorize_and_zscore(growth),
            'safety': self.winsorize_and_zscore(safety),
            'payout': self.winsorize_and_zscore(payout)
        })
        
        return quality.mean(axis=1)
    
    def calculate_profitability(self, universe, date):
        """Gross profits / assets, ROE, ROA, etc."""
        gp = self.data.get_fundamentals(universe, 'gross_profit', date)
        assets = self.data.get_fundamentals(universe, 'total_assets', date)
        return gp / assets
    
    def calculate_safety(self, universe, date):
        """Low leverage, low volatility, low beta."""
        leverage = self.data.get_fundamentals(universe, 'debt_to_equity', date)
        volatility = self.data.get_volatility(universe, date, lookback_days=252)
        
        # Invert so higher is better
        return -(leverage.rank() + volatility.rank()) / 2
    
    def winsorize_and_zscore(self, series: pd.Series, clip_std: float = 3.0):
        """Winsorize outliers and standardize."""
        z = (series - series.mean()) / series.std()
        z = z.clip(-clip_std, clip_std)
        return (z - z.mean()) / z.std()
```

### Multi-Factor Portfolio Construction

```python
class FactorPortfolio:
    """
    AQR's portfolio construction: factor exposure with risk management.
    """
    
    def __init__(self, factors: Dict[str, FactorBuilder], 
                 risk_model: RiskModel,
                 transaction_cost_model: TCostModel):
        self.factors = factors
        self.risk = risk_model
        self.tcost = transaction_cost_model
    
    def construct_portfolio(self,
                            universe: List[str],
                            date: date,
                            factor_weights: Dict[str, float],
                            risk_target: float = 0.10) -> pd.Series:
        """
        Build a portfolio with target factor exposures.
        """
        # Calculate factor scores
        factor_scores = {}
        for name, builder in self.factors.items():
            factor_scores[name] = builder.build(universe, date)
        
        # Combine factors with weights
        combined_score = sum(
            factor_scores[name] * weight 
            for name, weight in factor_weights.items()
        )
        
        # Convert scores to weights (long-short)
        raw_weights = self.scores_to_weights(combined_score)
        
        # Scale to target risk
        portfolio_vol = self.risk.estimate_volatility(raw_weights)
        scaled_weights = raw_weights * (risk_target / portfolio_vol)
        
        return scaled_weights
    
    def scores_to_weights(self, scores: pd.Series) -> pd.Series:
        """
        Convert z-scores to portfolio weights.
        AQR approach: proportional to score, with constraints.
        """
        # Long top tercile, short bottom tercile
        n = len(scores)
        tercile = n // 3
        
        sorted_idx = scores.sort_values().index
        
        weights = pd.Series(0.0, index=scores.index)
        weights[sorted_idx[:tercile]] = -1.0 / tercile  # Short bottom
        weights[sorted_idx[-tercile:]] = 1.0 / tercile   # Long top
        
        return weights
    
    def calculate_turnover_cost(self,
                                 current: pd.Series,
                                 target: pd.Series,
                                 date: date) -> float:
        """
        Estimate transaction costs from rebalancing.
        """
        trades = (target - current).abs()
        costs = self.tcost.estimate(trades, date)
        return costs.sum()
    
    def optimize_with_turnover(self,
                                current: pd.Series,
                                target: pd.Series,
                                max_turnover_cost: float) -> pd.Series:
        """
        Trade toward target, but respect turnover budget.
        """
        trades = target - current
        
        # If unconstrained cost is acceptable, trade fully
        full_cost = self.calculate_turnover_cost(current, target, date)
        if full_cost <= max_turnover_cost:
            return target
        
        # Otherwise, trade partially (proportionally)
        trade_fraction = max_turnover_cost / full_cost
        return current + trades * trade_fraction
```

### Factor Attribution and Reporting

```python
class FactorAttribution:
    """
    AQR-style transparent performance attribution.
    Understand exactly where returns came from.
    """
    
    def __init__(self, factor_returns: pd.DataFrame):
        self.factor_returns = factor_returns
    
    def attribute_returns(self,
                          portfolio_returns: pd.Series,
                          factor_exposures: pd.DataFrame) -> AttributionResult:
        """
        Decompose portfolio returns into factor contributions.
        
        R_p = Σ(β_i * F_i) + α + ε
        """
        # Align data
        common_dates = portfolio_returns.index.intersection(
            self.factor_returns.index
        )
        
        port_ret = portfolio_returns.loc[common_dates]
        fact_ret = self.factor_returns.loc[common_dates]
        exposures = factor_exposures.loc[common_dates]
        
        # Calculate factor contributions
        contributions = {}
        total_factor_return = 0
        
        for factor in fact_ret.columns:
            factor_contribution = (exposures[factor] * fact_ret[factor]).sum()
            contributions[factor] = {
                'avg_exposure': exposures[factor].mean(),
                'factor_return': fact_ret[factor].sum(),
                'contribution': factor_contribution,
                'contribution_pct': factor_contribution / port_ret.sum() * 100
            }
            total_factor_return += factor_contribution
        
        # Alpha is unexplained return
        alpha = port_ret.sum() - total_factor_return
        
        return AttributionResult(
            total_return=port_ret.sum(),
            factor_contributions=contributions,
            alpha=alpha,
            r_squared=self.calculate_r_squared(port_ret, fact_ret, exposures)
        )
    
    def factor_performance_report(self,
                                   start_date: date,
                                   end_date: date) -> pd.DataFrame:
        """
        Generate factor performance summary.
        AQR publishes these regularly for transparency.
        """
        returns = self.factor_returns.loc[start_date:end_date]
        
        report = pd.DataFrame({
            'Total Return': returns.sum(),
            'Annualized Return': returns.mean() * 252,
            'Volatility': returns.std() * np.sqrt(252),
            'Sharpe Ratio': returns.mean() / returns.std() * np.sqrt(252),
            'Max Drawdown': self.calculate_max_drawdown(returns),
            'Hit Rate': (returns > 0).mean()
        })
        
        return report
```

### Backtesting with Realistic Frictions

```python
class RealisticBacktest:
    """
    AQR emphasizes the gap between paper and real returns.
    Model all frictions realistically.
    """
    
    def __init__(self, 
                 tcost_model: TransactionCostModel,
                 borrow_cost_model: BorrowCostModel,
                 market_impact_model: MarketImpactModel):
        self.tcost = tcost_model
        self.borrow = borrow_cost_model
        self.impact = market_impact_model
    
    def run_backtest(self,
                     strategy: Strategy,
                     start_date: date,
                     end_date: date,
                     initial_capital: float = 1e8) -> BacktestResult:
        """
        Backtest with realistic transaction costs and frictions.
        """
        capital = initial_capital
        positions = pd.Series(dtype=float)
        
        results = []
        
        for date in trading_days(start_date, end_date):
            # Generate target portfolio
            target = strategy.generate_positions(date, capital)
            
            # Calculate trading costs
            trades = target - positions
            
            trading_cost = self.tcost.estimate(trades, date)
            market_impact = self.impact.estimate(trades, date)
            
            # Borrow costs for short positions
            short_positions = positions[positions < 0]
            borrow_cost = self.borrow.estimate(short_positions, date)
            
            # Execute trades (adjust for costs)
            capital -= trading_cost + market_impact
            positions = target
            
            # Calculate return
            price_returns = self.get_returns(positions.index, date)
            gross_pnl = (positions * price_returns).sum()
            
            net_pnl = gross_pnl - trading_cost - market_impact - borrow_cost
            capital += net_pnl
            
            results.append({
                'date': date,
                'gross_pnl': gross_pnl,
                'trading_cost': trading_cost,
                'market_impact': market_impact,
                'borrow_cost': borrow_cost,
                'net_pnl': net_pnl,
                'capital': capital,
                'turnover': trades.abs().sum() / capital
            })
        
        return self.analyze_results(pd.DataFrame(results))
    
    def analyze_results(self, results: pd.DataFrame) -> BacktestResult:
        """Compute performance metrics with cost breakdown."""
        gross_returns = results['gross_pnl'] / results['capital'].shift(1)
        net_returns = results['net_pnl'] / results['capital'].shift(1)
        
        return BacktestResult(
            gross_sharpe=gross_returns.mean() / gross_returns.std() * np.sqrt(252),
            net_sharpe=net_returns.mean() / net_returns.std() * np.sqrt(252),
            implementation_drag=(gross_returns.sum() - net_returns.sum()) / len(results) * 252,
            avg_turnover=results['turnover'].mean(),
            total_trading_costs=results['trading_cost'].sum(),
            total_impact_costs=results['market_impact'].sum(),
            total_borrow_costs=results['borrow_cost'].sum()
        )
```

## Mental Model

AQR approaches factor investing by asking:

1. **Is there academic evidence?** Peer-reviewed research, not marketing
2. **What's the economic story?** Risk premium, behavioral bias, or structural?
3. **Does it survive transaction costs?** Paper returns ≠ real returns
4. **Is it crowded?** Factor popularity erodes returns
5. **Can we implement at scale?** Liquidity and capacity constraints

## Signature AQR Moves

- Composite factors over single metrics
- Academic-quality research process
- Transparent methodology
- Realistic transaction cost modeling
- Multi-asset class diversification
- Factor timing skepticism
- Long-short for pure factor exposure
- Published factor returns for benchmarking
