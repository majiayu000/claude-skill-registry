---
name: kolmogorov-onsager-hurst
description: "Turbulence scaling theory: K41 energy cascade, Onsager's anomalous dissipation, and Hurst exponent for long-range dependence"
version: 1.0.0
trit: -1
polarity: MINUS
---

# Kolmogorov-Onsager-Hurst Skill

> *"Big whirls have little whirls that feed on their velocity,*
> *and little whirls have lesser whirls and so on to viscosity."*
> — Lewis Fry Richardson (1922)

## Overview

This skill connects three foundational concepts in scaling theory:

| Contributor | Year | Key Insight |
|-------------|------|-------------|
| **Kolmogorov** | 1941 | E(k) ~ k^(-5/3) energy spectrum |
| **Onsager** | 1949 | Anomalous dissipation at Hölder h ≤ 1/3 |
| **Hurst** | 1951 | H exponent measures long-range dependence |

## The K41 Energy Cascade

Kolmogorov's 1941 theory (K41) describes turbulent flow:

```
Energy injection (large scales)
        ↓
    Inertial range: E(k) ~ ε^(2/3) k^(-5/3)
        ↓
Dissipation (viscous scales)

Where:
  k = wavenumber (inverse length scale)
  ε = energy dissipation rate
  E(k) = energy spectrum
```

### The -5/3 Law

```python
import numpy as np

def kolmogorov_spectrum(k, epsilon=1.0, C_K=1.5):
    """
    Kolmogorov energy spectrum E(k) = C_K * ε^(2/3) * k^(-5/3)

    Args:
        k: wavenumber array
        epsilon: energy dissipation rate
        C_K: Kolmogorov constant (~1.5)

    Returns:
        Energy spectrum E(k)
    """
    return C_K * (epsilon ** (2/3)) * (k ** (-5/3))
```

## Onsager's Conjecture (1949)

Lars Onsager conjectured that:

1. **Smooth solutions** (Hölder h > 1/3): Energy is conserved
2. **Rough solutions** (Hölder h ≤ 1/3): Energy can dissipate without viscosity

```
Hölder continuity: |v(x) - v(y)| ≤ C |x - y|^h

h > 1/3  →  Energy conserved (Euler equations)
h = 1/3  →  Critical threshold (K41 prediction)
h < 1/3  →  Anomalous dissipation possible
```

### The 2022-2024 Resolution

Onsager's conjecture was proven in stages:
- **Isett (2018)**: h < 1/3 allows dissipation
- **Buckmaster-De Lellis-Székelyhidi-Vicol (2022-2024)**: Sharp threshold h = 1/3

This work contributed to **Fields Medal** recognition.

## Hurst Exponent

The Hurst exponent H ∈ (0, 1) measures persistence in time series:

```
H = 0.5  →  Random walk (Brownian motion, no memory)
H > 0.5  →  Persistent (trending, positive correlation)
H < 0.5  →  Anti-persistent (mean-reverting, negative correlation)
```

### Connection to Turbulence

For K41 turbulence, velocity increments have **H = 1/3**:

```
Structure function: S_p(r) = <|v(x+r) - v(x)|^p> ~ r^(ζ_p)

K41 prediction: ζ_p = p/3
For p=2: ζ_2 = 2/3

Hurst exponent H = ζ_2 / 2 = 1/3
```

### R/S Analysis (Rescaled Range)

```python
import numpy as np

def hurst_rs(series):
    """
    Estimate Hurst exponent via R/S analysis.

    Returns H where:
      H = 0.5: random walk
      H > 0.5: persistent (trending)
      H < 0.5: anti-persistent (mean-reverting)
    """
    n = len(series)
    if n < 20:
        return 0.5

    max_k = int(np.log2(n)) - 1
    rs_values = []
    ns = []

    for k in range(2, max_k + 1):
        size = n // (2 ** k)
        if size < 4:
            break

        rs_list = []
        for i in range(2 ** k):
            subseries = series[i * size:(i + 1) * size]
            mean = np.mean(subseries)
            cumdev = np.cumsum(subseries - mean)
            R = np.max(cumdev) - np.min(cumdev)
            S = np.std(subseries, ddof=1)
            if S > 0:
                rs_list.append(R / S)

        if rs_list:
            rs_values.append(np.mean(rs_list))
            ns.append(size)

    if len(ns) < 2:
        return 0.5

    # Linear regression in log-log space
    log_n = np.log(ns)
    log_rs = np.log(rs_values)
    slope, _ = np.polyfit(log_n, log_rs, 1)

    return slope

def hurst_dfa(series, order=1):
    """
    Detrended Fluctuation Analysis (DFA) for Hurst estimation.
    More robust than R/S for non-stationary series.
    """
    n = len(series)
    cumsum = np.cumsum(series - np.mean(series))

    scales = []
    flucts = []

    for scale in range(10, n // 4):
        segments = n // scale
        if segments < 1:
            break

        local_trends = []
        for seg in range(segments):
            start = seg * scale
            end = start + scale
            segment = cumsum[start:end]

            # Detrend with polynomial
            x = np.arange(scale)
            coeffs = np.polyfit(x, segment, order)
            trend = np.polyval(coeffs, x)

            local_trends.append(np.sqrt(np.mean((segment - trend) ** 2)))

        scales.append(scale)
        flucts.append(np.mean(local_trends))

    if len(scales) < 2:
        return 0.5

    log_scales = np.log(scales)
    log_flucts = np.log(flucts)
    slope, _ = np.polyfit(log_scales, log_flucts, 1)

    return slope
```

## The Unified Picture

```
┌─────────────────────────────────────────────────────────────────────┐
│                  KOLMOGOROV-ONSAGER-HURST TRIAD                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  KOLMOGOROV (Spectrum)     ONSAGER (Regularity)    HURST (Memory)  │
│  ────────────────────      ─────────────────────   ───────────────  │
│  E(k) ~ k^(-5/3)           Hölder h = 1/3          H = 1/3         │
│                                                                     │
│  Energy cascade            Critical roughness       Persistence     │
│  Inertial range            Dissipation threshold    Structure fn    │
│                                                                     │
│  ────────────────── EQUIVALENCE RELATIONS ──────────────────────   │
│                                                                     │
│  Spectral exponent β = 2H + 1 = 5/3                                │
│  Hölder exponent h = H = 1/3                                        │
│  Fractal dimension D = 2 - H = 5/3                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Relations

```
β = 2H + 1        (spectral exponent ↔ Hurst)
h = H             (Hölder ↔ Hurst for fBm)
D = 2 - H         (fractal dimension ↔ Hurst)

For K41: H = 1/3
  → β = 5/3 ✓ (Kolmogorov spectrum)
  → h = 1/3 ✓ (Onsager threshold)
  → D = 5/3 ✓ (fractal dimension)
```

## Applications

### 1. Financial Time Series

```python
def market_regime(prices):
    """
    Classify market regime by Hurst exponent.
    """
    returns = np.diff(np.log(prices))
    H = hurst_dfa(returns)

    if H > 0.55:
        return "TRENDING", H
    elif H < 0.45:
        return "MEAN_REVERTING", H
    else:
        return "RANDOM_WALK", H
```

### 2. Network Traffic

Long-range dependence in network traffic (Leland et al. 1994):
- Ethernet traffic: H ≈ 0.8-0.9
- TCP flows aggregate to self-similar process
- Impacts queue sizing and congestion

### 3. Biological Systems

- Heartbeat intervals: H ≈ 0.9-1.0 (healthy), H ≈ 0.5 (disease)
- DNA sequences: H varies by region
- Neural spike trains: scaling in avalanches

## GF(3) Integration

```
Trit: -1 (MINUS/Validator)

kolmogorov-onsager-hurst measures and validates scaling properties.
It quantifies rather than generates.

GF(3) Triads:
  kolmogorov-onsager-hurst (-1) ⊗ langevin-dynamics (0) ⊗ fokker-planck-analyzer (+1) = 0 ✓
  kolmogorov-onsager-hurst (-1) ⊗ bifurcation-generator (0) ⊗ lyapunov-function (+1) = 0 ✓
  kolmogorov-onsager-hurst (-1) ⊗ structural-stability (0) ⊗ attractor (+1) = 0 ✓
```

## Cat# Bicomodule Structure

```
Home: Prof (profunctor category)
Poly Op: ⊗ (tensor)
Kan Role: Ran (right Kan extension - measurement/observation)

The Hurst exponent acts as a RIGHT adjoint:
  Ran_H(Turbulence) = Scaling Law

Measuring H from data is computing a limit (right Kan extension).
```

## References

1. Kolmogorov, A.N. (1941). "The local structure of turbulence in incompressible viscous fluid for very large Reynolds numbers."
2. Onsager, L. (1949). "Statistical hydrodynamics." Il Nuovo Cimento.
3. Hurst, H.E. (1951). "Long-term storage capacity of reservoirs." Trans. Am. Soc. Civil Eng.
4. Mandelbrot, B.B. & Van Ness, J.W. (1968). "Fractional Brownian motions, fractional noises and applications."
5. Isett, P. (2018). "A proof of Onsager's conjecture." Annals of Mathematics.
6. Buckmaster, T. et al. (2022-2024). "Wild solutions of the Euler equations."

## Invocation

```
/kolmogorov-onsager-hurst
```

Analyzes time series for scaling properties and regime classification.