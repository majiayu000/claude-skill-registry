---
name: mfe-emergence
description: "Complex systems and emergent behavior — chaos theory, fractals, neural networks, cellular automata, and computability. Analyzes dynamical systems for chaos via Lyapunov exponents, classifies bifurcations, measures fractal dimension, and models emergent phenomena. Use when analyzing chaotic systems, computing Lyapunov exponents, classifying bifurcations, measuring fractal dimension, modeling neural networks, or studying emergent behavior from simple rules."
user-invocable: false
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "chaos"
          - "complexity"
          - "nonlinear"
          - "attractor"
          - "fractal"
          - "network"
          - "learning"
          - "neural"
          - "emergent"
          - "self-organizing"
        contexts:
          - "mathematical problem solving"
          - "math reasoning"
---

# Emergence

Part IX: Growing — Chapters 28, 29, 30, 31 — Plane Position: (0.5, 0) radius 0.4 — 36 Primitives

## Workflow

1. **Identify the dynamical system** — determine whether it is discrete (logistic map, cellular automaton) or continuous (ODE system)
2. **Compute the Lyapunov exponent** to classify behavior: λ > 0 indicates chaos, λ < 0 indicates convergence to periodic orbit
3. **Analyze bifurcations** by varying parameters — classify as saddle-node, pitchfork, Hopf, or period-doubling
4. **Measure fractal dimension** for strange attractors using d = log(N)/log(1/r) for self-similar structures
5. **Estimate prediction horizon** using t_predict ≈ (1/λ) × ln(Δ/δ₀) to quantify how far ahead the system remains predictable

## Key Concepts

**Neural Network** (definition): An artificial neural network is a computational graph: y = f_L(W_L * f_{L-1}(... f_1(W_1 * x + b_1) ...+ b_L)), where W_i are weight matrices, b_i are bias vectors, and f_i are nonlinear activation functions. A perceptron is the single-layer case: y = sigma(w^T x + b).
  - Approximating complex input-output mappings from data
  - Pattern recognition in images, text, and audio
  - Building flexible function approximators for regression and classification

**Logistic Map** (definition): The logistic map is the discrete dynamical system x_{n+1} = r * x_n * (1 - x_n), where x_n in [0,1] and r in [0,4]. It exhibits period doubling, bifurcations, and chaos as r increases, serving as the canonical example of deterministic chaos.
  - Modeling population dynamics with carrying capacity
  - Demonstrating how simple rules produce complex behavior
  - Studying the onset of chaos through parameter variation

**Turing Machine** (definition): A Turing machine is a mathematical model of computation consisting of: an infinite tape divided into cells, a head that reads/writes symbols and moves left/right, a finite set of states Q, and a transition function delta: Q x Gamma -> Q x Gamma x {L,R}. It defines the boundary of computability.
  - Defining the fundamental limits of what can be computed
  - Providing a precise model for algorithm analysis
  - Establishing the theoretical foundation of computer science

**Bifurcation Theory** (definition): A bifurcation occurs when a small change in a parameter causes a qualitative change in the system's behavior. Types include: saddle-node (creation/annihilation of fixed points), pitchfork (symmetry breaking), Hopf (birth of limit cycle), and period-doubling (orbit stability change).
  - Identifying critical parameter values where system behavior changes qualitatively
  - Classifying transitions between stable and unstable regimes
  - Designing systems that avoid or exploit bifurcation behavior

**Fractal Dimension** (definition): The Hausdorff dimension d_H of a set S is the critical value where the Hausdorff measure transitions from infinity to zero: d_H = inf{d : H^d(S) = 0}. For self-similar fractals with N copies scaled by factor r, d = log(N)/log(1/r). Fractals have non-integer dimension.
  - Measuring the complexity and space-filling properties of irregular shapes
  - Characterizing natural structures like coastlines, trees, and blood vessels
  - Quantifying the roughness or irregularity of a geometric object

**Self-Similarity** (definition): A set S is self-similar if it can be decomposed into parts that are scaled copies of the whole: S = union_{i=1}^N f_i(S), where each f_i is a contraction mapping (similitude) with scaling ratio r_i < 1. Exact self-similarity holds for mathematical fractals; statistical self-similarity holds for natural fractals.
  - Identifying fractal structure in natural and artificial patterns
  - Generating complex geometry from simple recursive rules
  - Modeling phenomena that look similar at different scales

**Church-Turing Thesis** (axiom): The Church-Turing thesis states that any function which is effectively computable (by an algorithm, in the intuitive sense) is computable by a Turing machine. This is a thesis, not a theorem -- it cannot be formally proved, but all known computational models have been shown equivalent to Turing machines.
  - Defining the boundary between computable and non-computable problems
  - Justifying the use of any convenient computational model for proving results
  - Understanding why programming languages are all fundamentally equivalent in power

**Lyapunov Exponent** (definition): The maximal Lyapunov exponent lambda measures the average exponential rate of divergence of nearby trajectories: lambda = lim_{n->inf} (1/n) sum_{i=0}^{n-1} ln|f'(x_i)|. For the logistic map, lambda > 0 indicates chaos; lambda < 0 indicates convergence to a periodic orbit.
  - Quantifying the degree of chaos in a dynamical system
  - Predicting the time horizon for reliable forecasting
  - Distinguishing deterministic chaos from random noise

**Sensitive Dependence on Initial Conditions** (definition): A dynamical system exhibits sensitive dependence on initial conditions if there exists delta > 0 such that for any x and any epsilon > 0, there exists y with |x-y| < epsilon and n > 0 such that |f^n(x) - f^n(y)| > delta. Informally: arbitrarily close initial states eventually diverge by a macroscopic amount.
  - Understanding fundamental limits of predictability in chaotic systems
  - Quantifying the butterfly effect in weather and climate
  - Distinguishing deterministic chaos from stochastic randomness

**Cellular Automaton** (definition): A cellular automaton is a discrete dynamical system on a regular grid where each cell has a finite state updated simultaneously according to a local rule depending on neighboring cells. Wolfram's Rule 110 is proven Turing-complete. Conway's Game of Life uses a 2D grid with birth/survival rules B3/S23.
  - Modeling emergent behavior from simple local interaction rules
  - Studying computational universality in minimal systems
  - Simulating physical and biological systems on discrete lattices

## Composition Patterns

- Logistic Map + emergence-lyapunov-exponent -> Classification of chaotic vs periodic regimes by sign of Lyapunov exponent (sequential)
- Lyapunov Exponent + change-ode -> Stability classification of continuous dynamical systems (sequential)
- Feigenbaum Constants + emergence-logistic-map -> Universal prediction of chaos onset from period-doubling parameters (sequential)
- Strange Attractor + emergence-fractal-dimension -> Quantitative characterization of attractor geometry (parallel)
- Bifurcation Theory + structure-eigenvalue -> Complete classification of local bifurcations via eigenvalue crossing patterns (sequential)
- Sensitive Dependence on Initial Conditions + emergence-lyapunov-exponent -> Prediction horizon: t_predict ~ (1/lambda) * ln(Delta/delta_0) (sequential)
- Ergodic Theory + mapping-probability-axioms -> Statistical mechanics from dynamical systems: thermodynamic ensembles justified by ergodicity (parallel)
- Fractal Dimension + emergence-strange-attractor -> Quantitative characterization of chaotic attractor complexity (parallel)
- Self-Similarity + emergence-fractal-dimension -> Dimension calculation from similarity ratios: d = log(N)/log(1/r) for N copies at scale r (sequential)
- L-System + emergence-fractal-dimension -> Fractal plants with measurable dimension from L-system rules (sequential)

## Cross-Domain Links

- **change**: Compatible domain for composition and cross-referencing
- **mapping**: Compatible domain for composition and cross-referencing
- **unification**: Compatible domain for composition and cross-referencing
- **synthesis**: Compatible domain for composition and cross-referencing

## Activation Patterns

- chaos
- complexity
- nonlinear
- attractor
- fractal
- network
- learning
- neural
- emergent
- self-organizing
