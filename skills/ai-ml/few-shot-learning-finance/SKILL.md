---
name: few-shot-learning-finance
description: Use when implementing models that learn from minimal data or need to adapt to new market regimes rapidly. Covers episodic learning, context sets, support and query sequences, zero-shot vs few-shot learning, meta-learning for finance, transfer learning across assets and regimes, and quick adaptation to market changes.
---

# Few-Shot Learning for Finance

## Purpose

Guide for implementing few-shot learning techniques in financial trading strategies, enabling models to quickly adapt to new market regimes or trade previously unseen assets with minimal data.

## When to Use

Activate this skill when:
- Implementing models that adapt to regime changes quickly
- Trading new or low-liquidity assets with limited history
- Building strategies that transfer knowledge across assets
- Dealing with non-stationary markets or structural breaks
- Implementing meta-learning for trading strategies
- Creating context-based prediction systems

## Core Concepts

### 1. Few-Shot vs Zero-Shot Learning

**Few-Shot Learning:**
- Model has seen the target asset during training
- Can use historical data from same asset (in context set)
- Training set and test set overlap: `I_train ∩ I_test = I`
- Example: Adapting to new regime of S&P 500 after COVID-19

**Zero-Shot Learning:**
- Model has NEVER seen the target asset during training
- Must transfer knowledge from different assets entirely
- Training set and test set disjoint: `I_train ∩ I_test = ∅`
- Example: Trading a new cryptocurrency using patterns learned from equities

```python
# Few-shot setting
train_assets = ['SPY', 'GLD', 'TLT']  # 30 assets
test_assets = ['SPY', 'GLD', 'TLT']   # Same 30 assets, different time period

# Zero-shot setting
train_assets = ['SPY', 'GLD', 'TLT']  # 30 assets for training
test_assets = ['BTC', 'ETH', 'SOL']   # 20 different assets for testing
```

### 2. Episodic Learning

Train models the same way they'll be used at test time:

**Traditional Training:**
```python
# Standard mini-batch training - all assets mixed together
for epoch in epochs:
    for batch in shuffle(all_data):
        loss = model(batch)
        optimizer.step()
```

**Episodic Training:**
```python
# Episode-based training - mimics test-time usage
for episode in episodes:
    # Sample target sequence (what we want to predict)
    target_asset, target_time = sample_target()

    # Sample context set C (what we condition on)
    context_set = sample_contexts(
        assets=train_assets,
        exclude=(target_asset, target_time),  # Ensure causality
        size=C  # Number of context sequences
    )

    # Make prediction using context
    prediction = model(target=target, context=context_set)

    loss = criterion(prediction, true_value)
    optimizer.step()
```

**Key Principles:**
- Each episode = one prediction task
- Context set must be causal (occurred before target)
- Model learns to transfer patterns from context to target
- Trains on k-shot tasks to perform well on k-shot evaluation

### 3. Context Set Construction

Context set `C` contains sequences from other assets/regimes that inform the prediction.

**Properties:**
- **Size**: Typically 10-30 sequences
- **Causality**: All context must occur before target time
- **Diversity**: Include different assets and market conditions
- **Quality**: CPD segmentation improves performance 11.3% vs random

**Construction Methods:**

1. **Random**: Sample random sequences before target_time
2. **Time-equivalent**: Same time window as target, different assets
3. **CPD-segmented**: Use change-point detection for clean regime segments

See [IMPLEMENTATION.md](IMPLEMENTATION.md#context-set-construction) for code examples.

### 4. Meta-Learning Architecture

**How It Works:**

1. **Encode context sequences** → Learn patterns from similar situations
2. **Encode target sequence** → Understand current market state
3. **Cross-attention** → Target queries context for relevant patterns
4. **Combine representations** → Integrate transferred knowledge
5. **Predict position** → Generate trading signal

**Key Insight:** Cross-attention automatically identifies which context sequences are most similar to the target, weighting them higher in the final prediction.

See [IMPLEMENTATION.md](IMPLEMENTATION.md#meta-learning-architecture) for implementation.

### 5. Transfer Learning Scenarios

**1. Same Asset, Different Regime (Few-Shot)**
- Target: SPY in 2020 (COVID crash)
- Context: SPY in 2008 (financial crisis), SPY in 2018 (correction)
- Transfer: Crisis response patterns

**2. Different Assets, Similar Dynamics (Zero-Shot)**
- Target: New cryptocurrency (BTC)
- Context: Gold, Silver, Crude Oil (commodities)
- Transfer: Trending behavior, volatility patterns

**3. Cross-Asset Momentum Spillover**
- Target: European equities (CAC40)
- Context: US equities (SPY), Asian equities (Nikkei)
- Transfer: Leading indicators, correlation structures

### 6. Training Objectives

**Joint Loss Function:**
```python
L_joint = α * L_MLE + L_Sharpe

where:
- L_MLE: Maximum likelihood (forecasting accuracy)
- L_Sharpe: Negative Sharpe ratio (trading performance)
- α: Balance parameter (1.0 for Gaussian, 5.0 for quantile)
```

**Why Joint Training?**
- Pure forecasting doesn't optimize for trading
- Pure Sharpe can overfit to training period
- Joint training balances both objectives

See [IMPLEMENTATION.md](IMPLEMENTATION.md#training-objectives) for implementation.

## Evaluation Protocols

### Expanding Window Backtest

**Process:**
1. Train on 1990-1995 data
2. Test on 1995-2000
3. Expand training to 1990-2000
4. Test on 2000-2005
5. Continue expanding...

**Critical**: Context sets must only use data from training period (no look-ahead).

See [IMPLEMENTATION.md](IMPLEMENTATION.md#expanding-window-backtest) for code.

### Zero-Shot Evaluation

**Setup:**
- Train on 30 assets (traditional futures)
- Test on 20 completely different assets (cryptocurrencies)
- Context from training assets only
- Validates true transfer learning capability

See [IMPLEMENTATION.md](IMPLEMENTATION.md#zero-shot-evaluation) for implementation.

## Performance Insights from X-Trend Paper

### Few-Shot Results (2018-2023)

- **Baseline** (no context): Sharpe = 2.27
- **X-Trend** (with context): Sharpe = 2.70 (+18.9%)
- **X-Trend** (CPD context): Sharpe = 2.70 (+18.9%)
- **vs TSMOM**: Sharpe = 0.23 (10× improvement)

### Zero-Shot Results (2018-2023)

- **Baseline**: Sharpe = -0.11 (loss-making!)
- **X-Trend-G** (Gaussian): Sharpe = 0.47 (profitable)
- **TSMOM**: Sharpe = -0.26
- **5× Sharpe improvement** vs baseline

### COVID-19 Recovery

- **Baseline**: 254 days to recover from drawdown
- **X-Trend**: 162 days (2× faster recovery)

## Best Practices

### DO:

✅ **Use episodic training** - train how you test
✅ **Ensure causality** - context must precede target
✅ **Sample diverse contexts** - different assets, regimes, conditions
✅ **Use change-point detection** - improves Sharpe by 11%+
✅ **Test zero-shot performance** - validates true transfer learning
✅ **Joint optimization** - balance forecasting and trading objectives

### DON'T:

❌ **Don't leak future information** into context set
❌ **Don't use same (asset, time) in context and target**
❌ **Don't assume transferability** without testing
❌ **Don't skip few-shot evaluation** even for zero-shot models
❌ **Don't ignore context set size** - typically 10-30 is optimal

## Common Pitfalls

### Pitfall 1: Data Leakage
```python
# WRONG - context from future!
context = sample_sequences(all_time_periods)

# CORRECT - context only from past
context = sample_sequences(before=target_time)
```

### Pitfall 2: Overfitting to Context Construction
```python
# WRONG - optimization on test set
best_cpd_threshold = optimize_on_test_set()

# CORRECT - validate on held-out data
best_cpd_threshold = cross_validate_on_train_set()
```

### Pitfall 3: Ignoring Asset Heterogeneity
```python
# WRONG - assume all assets behave identically
encoding = lstm(features)

# CORRECT - use entity embeddings
encoding = lstm(features) + asset_embedding[asset_id]
```

See [IMPLEMENTATION.md](IMPLEMENTATION.md#common-pitfalls) for more examples.

## Implementation Checklist

When implementing few-shot learning:

- [ ] Define few-shot vs zero-shot split (asset overlap)
- [ ] Implement episodic training loop
- [ ] Create context sampling function (ensure causality)
- [ ] Add cross-attention mechanism for context integration
- [ ] Implement joint loss (forecasting + trading)
- [ ] Set context size (10-30 sequences)
- [ ] Add CPD-based context construction (optional, +11% Sharpe)
- [ ] Implement expanding window backtest
- [ ] Test zero-shot performance separately
- [ ] Monitor attention weights for interpretability
- [ ] Validate no future information leaks

## Key Takeaways

1. **Few-shot ≠ Small Model** - Models can be large, but they adapt with minimal examples
2. **Context Quality Matters** - CPD segmentation beats random sampling
3. **Zero-shot Tests Transfer** - If it works on unseen assets, transfer is real
4. **Episodic Training Required** - Don't mix all data; train in episodes
5. **Joint Objectives Help** - Forecasting + trading better than either alone

## Related Skills

- `financial-time-series` - Momentum factors, returns, portfolio construction
- `change-point-detection` - GP-CPD for regime segmentation
- `x-trend-architecture` - Cross-attention mechanisms

## Reference Files

- [IMPLEMENTATION.md](IMPLEMENTATION.md) - Context construction methods, meta-learning architecture, evaluation protocols, common pitfalls

## References

- Matching Networks for One Shot Learning (Vinyals et al. 2016)
- Model-Agnostic Meta-Learning (Finn et al. 2017)
- Neural Processes (Garnelo et al. 2018)
- X-Trend: Few-Shot Learning Patterns (Wood et al. 2024)

---

**Last Updated**: Based on X-Trend paper (March 2024)
**Skill Type**: Domain Knowledge
**Line Count**: ~310 (under 500-line rule ✅)
