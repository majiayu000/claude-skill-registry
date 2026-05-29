---
name: bifurcation
description: Hopf bifurcation detection for dynamical system state transitions with GF(3) phase portraits
version: 1.0.0
---


# Bifurcation

**Detects and navigates bifurcation points in dynamical systems where qualitative behavior changes.**

**Trit**: 0 (ERGODIC - Coordinator between stable states)
**Color**: #9966FF (Purple - neutral zone bridging warm/cold)

---

## Core Concepts

### Bifurcation Types

| Type | Description | GF(3) Mapping |
|------|-------------|---------------|
| **Saddle-Node** | Two equilibria collide and annihilate | PLUS ↔ MINUS collision |
| **Hopf** | Equilibrium → limit cycle | ERGODIC spawns oscillation |
| **Pitchfork** | Symmetry-breaking | One ERGODIC → two ±PLUS/MINUS |
| **Transcritical** | Exchange of stability | PLUS ↔ MINUS swap roles |
| **Period-Doubling** | Route to chaos | Trit cascade: 0 → 1 → -1 → 0... |

---

## Hopf Bifurcation Detection

```python
import numpy as np
from scipy.linalg import eig

def detect_hopf(jacobian_fn, params, param_name, param_range):
    """
    Detect Hopf bifurcation by finding where eigenvalues cross imaginary axis.

    At Hopf bifurcation:
    - Pair of complex conjugate eigenvalues
    - Real part crosses zero
    - Imaginary part nonzero (oscillation frequency)
    """
    bifurcation_points = []

    for p in param_range:
        params[param_name] = p
        J = jacobian_fn(params)
        eigenvalues = eig(J)[0]

        # Find complex conjugate pairs
        for ev in eigenvalues:
            if np.abs(np.imag(ev)) > 1e-6:  # Has imaginary part
                if np.abs(np.real(ev)) < 1e-4:  # Real part near zero
                    bifurcation_points.append({
                        'param': p,
                        'eigenvalue': ev,
                        'frequency': np.abs(np.imag(ev)),
                        'type': 'hopf'
                    })

    return bifurcation_points
```

---

## GF(3) Phase Portrait

```python
def gf3_phase_portrait(system_fn, x_range, y_range, trit_classifier):
    """
    Generate phase portrait with GF(3) coloring.

    Each region colored by dominant behavior:
    - PLUS (+1): Expanding/generating (warm hues)
    - ERGODIC (0): Neutral/cycling (neutral hues)
    - MINUS (-1): Contracting/validating (cold hues)
    """
    X, Y = np.meshgrid(x_range, y_range)
    U, V = system_fn(X, Y)

    # Classify each point by local behavior
    trits = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            trits[i,j] = trit_classifier(U[i,j], V[i,j])

    # Color map: -1 → blue, 0 → green, +1 → red
    colors = {-1: '#0066FF', 0: '#00FF66', 1: '#FF6600'}

    return X, Y, U, V, trits, colors
```

---

## Bifurcation Diagram Generator

```clojure
#!/usr/bin/env bb
(require '[babashka.process :as p])

(defn logistic-map [r x]
  (* r x (- 1 x)))

(defn iterate-map [f x0 n-transient n-samples]
  "Iterate map, discard transient, collect samples"
  (let [trajectory (iterate (partial f) x0)
        post-transient (drop n-transient trajectory)]
    (take n-samples post-transient)))

(defn bifurcation-diagram [r-range x0 n-transient n-samples]
  "Generate bifurcation diagram data"
  (for [r r-range]
    {:r r
     :attractors (distinct
                   (iterate-map #(logistic-map r %) x0 n-transient n-samples))
     :period (count (distinct
                      (iterate-map #(logistic-map r %) x0 n-transient n-samples)))}))

;; Detect period-doubling cascade (route to chaos)
(defn period-doubling-points [diagram]
  "Find r values where period doubles"
  (loop [prev nil
         points []
         remaining diagram]
    (if (empty? remaining)
      points
      (let [curr (first remaining)
            period (:period curr)]
        (if (and prev (= (* 2 (:period prev)) period))
          (recur curr (conj points (:r curr)) (rest remaining))
          (recur curr points (rest remaining)))))))
```

---

## State Transition Detection

```python
class BifurcationMonitor:
    """
    Monitor system for bifurcation events in real-time.
    """

    def __init__(self, state_dim, history_len=100):
        self.state_dim = state_dim
        self.history = []
        self.history_len = history_len
        self.current_regime = 'unknown'

    def update(self, state, params):
        self.history.append({'state': state, 'params': params})
        if len(self.history) > self.history_len:
            self.history.pop(0)

        # Detect regime changes
        new_regime = self._classify_regime()
        if new_regime != self.current_regime:
            self._on_bifurcation(self.current_regime, new_regime)
            self.current_regime = new_regime

    def _classify_regime(self):
        """Classify current dynamical regime"""
        if len(self.history) < 10:
            return 'transient'

        states = np.array([h['state'] for h in self.history[-50:]])
        variance = np.var(states, axis=0)

        if np.all(variance < 1e-6):
            return 'fixed_point'  # MINUS: stable
        elif self._is_periodic(states):
            return 'limit_cycle'  # ERGODIC: oscillating
        else:
            return 'chaotic'  # PLUS: generating complexity

    def _is_periodic(self, states, tol=1e-3):
        """Check if trajectory is periodic"""
        # Simple periodicity check via autocorrelation
        for period in range(2, len(states)//2):
            if np.allclose(states[:-period], states[period:], atol=tol):
                return True
        return False

    def _on_bifurcation(self, old_regime, new_regime):
        """Handle bifurcation event"""
        trit_map = {
            'fixed_point': -1,  # MINUS: stable attractor
            'limit_cycle': 0,   # ERGODIC: periodic orbit
            'chaotic': 1        # PLUS: strange attractor
        }

        old_trit = trit_map.get(old_regime, 0)
        new_trit = trit_map.get(new_regime, 0)

        print(f"BIFURCATION: {old_regime} ({old_trit}) → {new_regime} ({new_trit})")
        print(f"GF(3) delta: {new_trit - old_trit}")
```

---

## Triadic Bifurcation Analysis

When analyzing bifurcations, deploy three parallel agents:

```
PLUS (+1) Agent: Explore parameter space forward (increase control parameter)
ERGODIC (0) Agent: Monitor current state, detect oscillations
MINUS (-1) Agent: Analyze stability, compute Lyapunov exponents

Conservation: +1 + 0 + (-1) = 0 ✓
```

---

## Integration with ruler-maximal

```clojure
;; In ruler-maximal session initialization
(defn check-skill-bifurcation [skill-state]
  "Detect if skill loading pattern is approaching bifurcation"
  (let [usage-variance (variance (vals (:usage-counts skill-state)))
        load-frequency (/ (count (:loaded-skills skill-state))
                          (:session-duration skill-state))]
    (cond
      (< usage-variance 0.1) :fixed-point   ;; Stable usage pattern
      (periodic? (:load-history skill-state)) :limit-cycle  ;; Cyclic loading
      :else :exploring)))  ;; Still exploring skill space
```

---

## Commands

```bash
# Analyze system for bifurcations
bb -e '(bifurcation/analyze system params)'

# Generate bifurcation diagram
bb scripts/bifurcation_diagram.bb --param r --range "2.5:4.0:0.001"

# Monitor real-time state transitions
bb scripts/bifurcation_monitor.bb --system lorenz
```

---

## References

- Strogatz, "Nonlinear Dynamics and Chaos" (2015)
- Kuznetsov, "Elements of Applied Bifurcation Theory" (2004)
- Guckenheimer & Holmes, "Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields"

---

## Related Skills

- `dynamical-systems` (0): General dynamical systems theory
- `chaos-theory` (+1): Strange attractors, sensitivity to initial conditions
- `stability-analysis` (-1): Lyapunov exponents, basin boundaries
- `ruler-maximal` (0): Uses bifurcation for skill state transitions
- `gay-mcp` (0): GF(3) color mapping for phase portraits