---
name: renaissance-statistical-arbitrage
description: Build trading systems in the style of Renaissance Technologies, the most successful quantitative hedge fund in history. Emphasizes statistical arbitrage, signal processing, and rigorous scientific methodology. Use when developing alpha research, signal extraction, or systematic trading strategies.
---

# Renaissance Technologies Style Guide

## Overview

Renaissance Technologies, founded by mathematician Jim Simons, operates the Medallion Fund—the most successful hedge fund in history with ~66% annual returns before fees over 30+ years. The firm hires mathematicians, physicists, and computer scientists (not finance people) and applies rigorous scientific methods to market data.

## Core Philosophy

> "We don't hire people from business schools. We hire people from the hard sciences."

> "Patterns in data are ephemeral. If something works, it's probably going to stop working."

> "We're not in the business of predicting. We're in the business of finding patterns that repeat slightly more often than they should."

Renaissance believes markets are not perfectly efficient but nearly so. Profits come from finding tiny, statistically significant edges and exploiting them at massive scale with rigorous risk management.

## Design Principles

1. **Scientific Method**: Form hypotheses, test rigorously, reject most ideas.

2. **Signal, Not Prediction**: Find patterns that repeat more often than chance; don't predict the future.

3. **Decay Awareness**: Every signal degrades over time. Continuous research is survival.

4. **Statistical Significance**: If it's not statistically significant, it doesn't exist.

5. **Ensemble Everything**: Combine thousands of weak signals into robust strategies.

## When Building Trading Systems

### Always

- Demand statistical significance (p < 0.01 minimum, ideally much lower)
- Account for multiple hypothesis testing (Bonferroni, FDR correction)
- Test on out-of-sample data with proper temporal separation
- Model transaction costs, slippage, and market impact
- Assume every signal will decay—build infrastructure for continuous research
- Combine signals orthogonally (uncorrelated sources of alpha)

### Never

- Trust a backtest without out-of-sample validation
- Ignore survivorship bias, lookahead bias, or selection bias
- Assume past correlations will persist
- Over-optimize on historical data (curve fitting)
- Trade on intuition or narrative
- Assume a signal will last forever

### Prefer

- Hidden Markov models for regime detection
- Spectral analysis for cyclical patterns
- Non-linear methods for complex relationships
- Ensemble methods over single models
- Short holding periods (faster signal decay detection)
- Statistical tests over visual inspection

## Code Patterns

### Rigorous Backtesting Framework

```python
class RenaissanceBacktester:
    """
    Renaissance-style backtesting: paranoid about biases.
    """
    
    def __init__(self, strategy, universe):
        self.strategy = strategy
        self.universe = universe
        self.results = []
    
    def run(self, start_date, end_date, 
            train_window_days=252, 
            test_window_days=63,
            embargo_days=5):
        """
        Walk-forward validation with embargo period.
        Never let training data leak into test period.
        """
        current = start_date
        
        while current + timedelta(days=train_window_days + test_window_days) <= end_date:
            train_end = current + timedelta(days=train_window_days)
            
            # EMBARGO: gap between train and test to prevent leakage
            test_start = train_end + timedelta(days=embargo_days)
            test_end = test_start + timedelta(days=test_window_days)
            
            # Train on historical data
            train_data = self.get_point_in_time_data(current, train_end)
            self.strategy.fit(train_data)
            
            # Test on future data (strategy cannot see this during training)
            test_data = self.get_point_in_time_data(test_start, test_end)
            returns = self.strategy.execute(test_data)
            
            self.results.append({
                'train_period': (current, train_end),
                'test_period': (test_start, test_end),
                'returns': returns,
                'sharpe': self.calculate_sharpe(returns)
            })
            
            current = test_end
        
        return self.analyze_results()
    
    def get_point_in_time_data(self, start, end):
        """
        CRITICAL: Return data as it existed at each point in time.
        No future information, no restated financials, no survivorship bias.
        """
        return self.universe.get_pit_snapshot(start, end)
    
    def analyze_results(self):
        """Statistical analysis of walk-forward results."""
        returns = [r['returns'] for r in self.results]
        
        # t-test: is mean return significantly different from zero?
        t_stat, p_value = stats.ttest_1samp(returns, 0)
        
        return {
            'mean_return': np.mean(returns),
            'sharpe_ratio': np.mean(returns) / np.std(returns) * np.sqrt(252),
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.01,
            'n_periods': len(self.results)
        }
```

### Signal Combination with Decay Tracking

```python
class SignalEnsemble:
    """
    Renaissance insight: combine many weak signals.
    Track decay and retire dying signals.
    """
    
    def __init__(self, decay_halflife_days=30):
        self.signals = {}  # signal_id -> SignalModel
        self.performance = {}  # signal_id -> rolling performance
        self.decay_halflife = decay_halflife_days
    
    def add_signal(self, signal_id, model, weight=1.0):
        self.signals[signal_id] = {
            'model': model,
            'weight': weight,
            'created_at': datetime.now(),
            'alive': True
        }
        self.performance[signal_id] = RollingStats(window=252)
    
    def generate_combined_signal(self, features):
        """
        Weighted combination of orthogonal signals.
        Signals with decayed performance get lower weights.
        """
        predictions = {}
        weights = {}
        
        for signal_id, signal in self.signals.items():
            if not signal['alive']:
                continue
            
            pred = signal['model'].predict(features)
            
            # Weight by original weight × recent performance
            perf = self.performance[signal_id]
            decay_weight = self.calculate_decay_weight(perf)
            
            predictions[signal_id] = pred
            weights[signal_id] = signal['weight'] * decay_weight
        
        # Normalize weights
        total_weight = sum(weights.values())
        if total_weight == 0:
            return 0.0
        
        combined = sum(
            predictions[sid] * weights[sid] / total_weight
            for sid in predictions
        )
        
        return combined
    
    def update_performance(self, signal_id, realized_return, predicted_direction):
        """Track whether signal correctly predicted direction."""
        correct = (realized_return > 0) == (predicted_direction > 0)
        self.performance[signal_id].add(1.0 if correct else 0.0)
        
        # Kill signals that have decayed below threshold
        if self.performance[signal_id].mean() < 0.51:  # Barely better than random
            self.signals[signal_id]['alive'] = False
    
    def calculate_decay_weight(self, perf):
        """Exponential decay based on recent hit rate."""
        hit_rate = perf.mean()
        # Scale: 50% hit rate = 0 weight, 55% = 0.5, 60% = 1.0
        return max(0, (hit_rate - 0.50) * 10)
```

### Hidden Markov Model for Regime Detection

```python
class MarketRegimeHMM:
    """
    Renaissance-style regime detection using Hidden Markov Models.
    Markets exhibit different statistical properties in different regimes.
    """
    
    def __init__(self, n_regimes=3):
        self.n_regimes = n_regimes
        self.model = None
        self.regime_stats = {}
    
    def fit(self, returns, volume, volatility):
        """
        Fit HMM to market observables.
        Discover latent regimes from price/volume/volatility patterns.
        """
        # Stack observables into feature matrix
        observations = np.column_stack([
            returns,
            np.log(volume + 1),
            volatility
        ])
        
        self.model = hmm.GaussianHMM(
            n_components=self.n_regimes,
            covariance_type='full',
            n_iter=1000
        )
        self.model.fit(observations)
        
        # Decode to get most likely regime sequence
        regimes = self.model.predict(observations)
        
        # Characterize each regime
        for regime in range(self.n_regimes):
            mask = regimes == regime
            self.regime_stats[regime] = {
                'mean_return': returns[mask].mean(),
                'volatility': returns[mask].std(),
                'frequency': mask.mean(),
                'mean_duration': self.calculate_duration(regimes, regime)
            }
        
        return self
    
    def current_regime(self, recent_observations):
        """Infer current regime from recent data."""
        probs = self.model.predict_proba(recent_observations)
        return np.argmax(probs[-1])
    
    def regime_adjusted_signal(self, base_signal, current_regime):
        """Adjust signal strength based on regime."""
        regime = self.regime_stats[current_regime]
        
        # Scale signal inversely with volatility
        # (same signal in high-vol regime should have smaller position)
        vol_adjustment = 0.15 / regime['volatility']  # Target 15% vol
        
        return base_signal * vol_adjustment
```

### Multiple Hypothesis Testing Correction

```python
class AlphaResearch:
    """
    Renaissance approach: test thousands of hypotheses,
    but correct for multiple testing to avoid false discoveries.
    """
    
    def __init__(self, significance_level=0.01):
        self.alpha = significance_level
        self.tested_hypotheses = []
    
    def test_signal(self, signal_name, returns, predictions):
        """Test if a signal has predictive power."""
        # Information Coefficient: correlation of prediction with outcome
        ic = stats.spearmanr(predictions, returns)
        
        # t-test for significance
        n = len(returns)
        t_stat = ic.correlation * np.sqrt(n - 2) / np.sqrt(1 - ic.correlation**2)
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))
        
        self.tested_hypotheses.append({
            'signal': signal_name,
            'ic': ic.correlation,
            't_stat': t_stat,
            'p_value': p_value
        })
        
        return p_value
    
    def get_significant_signals(self, method='fdr'):
        """
        After testing many signals, apply multiple testing correction.
        """
        p_values = [h['p_value'] for h in self.tested_hypotheses]
        
        if method == 'bonferroni':
            # Most conservative: divide alpha by number of tests
            adjusted_alpha = self.alpha / len(p_values)
            significant = [
                h for h in self.tested_hypotheses 
                if h['p_value'] < adjusted_alpha
            ]
        
        elif method == 'fdr':
            # Benjamini-Hochberg: control false discovery rate
            sorted_hypotheses = sorted(self.tested_hypotheses, key=lambda x: x['p_value'])
            significant = []
            
            for i, h in enumerate(sorted_hypotheses):
                # BH threshold: (rank / n_tests) * alpha
                threshold = ((i + 1) / len(p_values)) * self.alpha
                if h['p_value'] <= threshold:
                    significant.append(h)
                else:
                    break  # All remaining will also fail
        
        return significant
```

## Mental Model

Renaissance approaches trading by asking:

1. **Is there a pattern?** Statistical test, not eyeballing
2. **Is it significant?** After multiple testing correction?
3. **Is it robust?** Out-of-sample, different time periods, different instruments?
4. **Will it persist?** What's the economic rationale for why this shouldn't be arbitraged away?
5. **How will it decay?** What's the monitoring plan?

## Signature Renaissance Moves

- Hire scientists, not traders
- Thousands of small signals, not a few big ones
- Paranoid about data snooping and overfitting
- Hidden Markov models for regime detection
- Signal decay tracking and retirement
- Rigorous walk-forward validation
- Multiple hypothesis testing correction
- Point-in-time data to prevent lookahead bias
