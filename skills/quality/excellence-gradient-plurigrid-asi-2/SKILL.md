---
name: excellence-gradient
description: "Measure quality. Descend toward excellence. No binary gates—only vectors."
trit: -1
polarity: MINUS
---

# Excellence Gradient

**Trit**: -1 (VALIDATOR - measures, constrains, reduces toward optimum)

## Core Principle

Quality is not a gate—it's a gradient. Binary pass/fail obscures the path to excellence. Measure everything. Descend continuously toward the minimum of the loss function: distance from ideal.

## The Airlock Principle

**The airlock should not eat the air.**

Validation exists to protect value, not consume it. If your quality gates:
- Take longer than the work they validate → **broken**
- Block more than they enable → **broken**  
- Cost more than the bugs they catch → **broken**
- Kill momentum instead of channeling it → **broken**

```
Cost(validation) << Value(protected)
Time(gate) << Time(work)
Friction(process) < Momentum(team)

airlock_efficiency = value_protected / momentum_consumed
# Target: efficiency > 10x
# If < 1x: gate eats more than it saves → remove or automate
```

The airlock is a *membrane*, not a wall. It regulates flow, doesn't stop it.

## Quality Lineage

| Pioneer | Contribution | Key Metric |
|---------|-------------|------------|
| **Deming** | 14 Points, PDCA | Variation reduction |
| **Juran** | Pareto principle, Quality Trilogy | Cost of poor quality |
| **Ohno** | Toyota Production System | Lead time, waste (muda) |
| **Shingo** | Poka-yoke, SMED | Defects approaching zero |
| **Crosby** | Zero defects, Quality is free | Price of non-conformance |

## Excellence Temperature (τ)

Distance from optimal. Lower is better. τ = 0 is perfection.

```python
def excellence_temperature(metrics: dict) -> float:
    """
    τ ∈ [0, ∞) where τ → 0 as quality → perfect
    Analogous to simulated annealing: high τ = chaos, low τ = crystallized excellence
    """
    weights = {
        'coverage': 0.20,      # Test coverage
        'latency': 0.15,       # P99 response time
        'satisfaction': 0.25,  # User NPS/CSAT
        'debt_ratio': 0.20,    # Technical debt / LOC
        'defect_rate': 0.20,   # Defects per KLOC
    }
    
    # Normalize each to [0,1] where 0 = optimal
    τ = sum(weights[k] * distance_from_optimal(k, v) 
            for k, v in metrics.items())
    return τ
```

## Measurable Excellence Criteria

### 1. Code Quality Metrics

| Metric | Formula | Target | Critical |
|--------|---------|--------|----------|
| **Coverage** | `tested_lines / total_lines` | ≥ 0.80 | < 0.60 |
| **Complexity** | Cyclomatic per function | ≤ 10 | > 20 |
| **Duplication** | `dup_lines / total_lines` | ≤ 0.03 | > 0.10 |
| **Debt Ratio** | `remediation_time / dev_time` | ≤ 0.05 | > 0.20 |
| **Doc Coverage** | `documented / public_symbols` | ≥ 0.90 | < 0.50 |

### 2. Performance Metrics

| Metric | Formula | Target | Critical |
|--------|---------|--------|----------|
| **P50 Latency** | 50th percentile | ≤ 100ms | > 500ms |
| **P99 Latency** | 99th percentile | ≤ 500ms | > 2000ms |
| **Error Rate** | `errors / requests` | ≤ 0.001 | > 0.01 |
| **Availability** | Uptime % | ≥ 99.9% | < 99.0% |
| **Throughput** | RPS at P99 SLO | ≥ baseline×1.2 | < baseline |

### 3. User Satisfaction Metrics

| Metric | Formula | Target | Critical |
|--------|---------|--------|----------|
| **NPS** | promoters - detractors | ≥ 50 | < 0 |
| **CSAT** | satisfied / respondents | ≥ 0.85 | < 0.70 |
| **Task Success** | completed / attempted | ≥ 0.95 | < 0.80 |
| **Time to Value** | signup → first value | ≤ 5min | > 30min |
| **Churn** | lost / total per period | ≤ 0.02/mo | > 0.10/mo |

### 4. Technical Debt Indicators

| Metric | Formula | Target | Critical |
|--------|---------|--------|----------|
| **TODO Count** | grep -r TODO | ≤ 10 | > 100 |
| **Dependency Age** | avg months since update | ≤ 6 | > 24 |
| **Security Vulns** | CVE count (high/critical) | 0 | > 0 |
| **Dead Code** | unreachable / total | ≤ 0.01 | > 0.05 |
| **Build Time** | CI pipeline duration | ≤ 10min | > 30min |

## Gradient Descent Protocol

```python
def descend_toward_excellence(current_state: Metrics) -> Action:
    """
    Not binary pass/fail. Continuous improvement via gradient.
    """
    τ = excellence_temperature(current_state)
    gradient = compute_gradient(current_state)
    
    # Priority = steepest descent direction
    worst_metric = max(gradient.items(), key=lambda x: x[1])
    
    return Action(
        focus=worst_metric[0],
        expected_τ_reduction=worst_metric[1],
        effort_estimate=effort_model(worst_metric[0])
    )

def compute_gradient(state: Metrics) -> dict:
    """
    ∂τ/∂metric for each metric
    Higher gradient = faster improvement opportunity
    """
    return {
        metric: partial_derivative(excellence_temperature, metric, state)
        for metric in state.keys()
    }
```

## Anti-Patterns Detection

### Code Anti-Patterns

```python
ANTI_PATTERNS = {
    'god_class': lambda c: c.methods > 20 or c.lines > 500,
    'feature_envy': lambda m: external_calls(m) > internal_calls(m) * 2,
    'shotgun_surgery': lambda f: len(dependents(f)) > 10,
    'primitive_obsession': lambda c: primitive_params(c) > 5,
    'speculative_generality': lambda c: unused_abstractions(c) > 0,
    'dead_code': lambda f: call_count(f) == 0 and not exported(f),
    'copy_paste': lambda b: similar_blocks(b) > 2,
}

def detect_anti_patterns(codebase) -> list[Violation]:
    violations = []
    for name, detector in ANTI_PATTERNS.items():
        for entity in codebase.entities():
            if detector(entity):
                violations.append(Violation(
                    pattern=name,
                    location=entity.location,
                    severity=PATTERN_SEVERITY[name],
                    fix_effort=PATTERN_EFFORT[name]
                ))
    return sorted(violations, key=lambda v: v.severity, reverse=True)
```

### Process Anti-Patterns

| Anti-Pattern | Detection Signal | Response |
|-------------|-----------------|----------|
| **Heroics** | 1 person on all critical paths | Distribute knowledge |
| **Scope Creep** | Requirements grow > 20%/sprint | Freeze and ship |
| **Gold Plating** | Features beyond spec | Ship MVP, iterate |
| **Analysis Paralysis** | > 2 weeks without shipping | Timebox decisions |
| **Bikeshedding** | > 30min on trivial choices | Executive decision |
| **NIH Syndrome** | Rewriting solved problems | Adopt proven solutions |

## GF(3) Triads

```
# Excellence Gradient Bundle (VALIDATOR ⊗ COORDINATOR ⊗ GENERATOR = 0)
excellence-gradient (-1) ⊗ chromatic-walk (0) ⊗ refuse-mediocrity (+1) = 0 ✓  [Quality Pursuit]
excellence-gradient (-1) ⊗ unworld (0) ⊗ refuse-mediocrity (+1) = 0 ✓  [Standard Derivation]
excellence-gradient (-1) ⊗ kinetic-block (0) ⊗ refuse-mediocrity (+1) = 0 ✓  [Momentum Measure]
excellence-gradient (-1) ⊗ implicit-coordination (0) ⊗ refuse-mediocrity (+1) = 0 ✓  [Parallel Quality]
excellence-gradient (-1) ⊗ topos-catcolab (0) ⊗ refuse-mediocrity (+1) = 0 ✓  [Collaborative Excellence]

# With other generators
excellence-gradient (-1) ⊗ acsets (0) ⊗ gay-mcp (+1) = 0 ✓  [Metric Coloring]
excellence-gradient (-1) ⊗ open-games (0) ⊗ agent-o-rama (+1) = 0 ✓  [Quality Games]
excellence-gradient (-1) ⊗ cognitive-surrogate (0) ⊗ koopman-generator (+1) = 0 ✓  [Learning Dynamics]
```

## Commands

```bash
# Compute current excellence temperature
just excellence-τ

# Run full quality audit
just quality-audit

# Detect anti-patterns
just anti-patterns

# Gradient descent: suggest next improvement
just descend

# Compare τ over time
just τ-history --days 30
```

## Implementation

```bash
#!/usr/bin/env bash
# excellence-gradient.sh

compute_excellence_temperature() {
    coverage=$(just coverage-report | grep -oP '\d+\.\d+')
    latency_p99=$(just latency-p99)
    debt_ratio=$(just tech-debt-ratio)
    defect_rate=$(just defect-rate)
    
    # Weighted sum (lower = better)
    τ=$(python3 -c "
weights = [0.25, 0.20, 0.30, 0.25]
metrics = [$((100 - coverage))/100, $latency_p99/2000, $debt_ratio, $defect_rate]
print(sum(w*m for w,m in zip(weights, metrics)))
")
    echo "τ = $τ"
}
```

## The Validator Role (-1)

This skill is MINUS because it **constrains and measures**:
- Measures distance from excellence
- Detects deviations (anti-patterns)
- Provides gradient direction (what to fix next)
- Validates improvements (τ decreased?)

Without measurement, "excellence" is just opinion. With measurement, it's navigation.

## Deming's 14 Points (Selected)

1. **Constancy of purpose** → Track τ daily
2. **Cease dependence on inspection** → Build quality in
3. **Drive out fear** → Measure to improve, not punish
4. **Break down barriers** → Shared metrics, shared goals
5. **Eliminate slogans** → Replace with measurable targets

## The Equation

```
Excellence = lim(t→∞) descent(τ₀, gradient, t)

Where:
- τ₀ = starting temperature
- gradient = ∇τ (direction of steepest improvement)
- t = iterations of PDCA
```

## One Rule

**If you can't measure it, you can't improve it. If τ isn't decreasing, you're not improving.**
