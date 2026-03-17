---
name: design-of-experiments
description: Expert guidance for Design of Experiments (DOE) in Python - interactive goal-driven design selection, classical DOE (factorial, response surface, screening), Bayesian optimization with Gaussian processes, model-driven optimal designs, active learning, and sequential experimentation; includes pyDOE3, pycse, GPyOpt, scikit-optimize, statsmodels
allowed-tools: ["*"]
---

# Design of Experiments (DOE) - Interactive Expert

## Overview

Master experimental design through **interactive, goal-driven guidance** that asks the right questions to recommend the best approach for your situation. This skill covers classical DOE, Bayesian optimization, model-driven designs, and active learning—helping you choose between batch and sequential strategies, screening and optimization, and exploration and exploitation.

**Core value:** Don't start with a method—start with questions. Based on your goals, budget, and constraints, get personalized recommendations for experimental design strategies that maximize information gain per experiment.

## CRITICAL: Start with Questions, Not Methods

**When a user mentions DOE or experimental design, ASK THESE QUESTIONS FIRST:**

### Primary Questions (Ask Before Recommending):

1. **"What is your primary goal?"**
   - **Screening**: Identify which factors matter (many factors → few important)
   - **Optimization**: Find best settings for known factors
   - **Exploration**: Understand the system/build model
   - **Model discrimination**: Choose between competing models
   - **Robustness**: Minimize sensitivity to noise

2. **"Can you run experiments sequentially, or must they be done in a batch?"**
   - **Sequential**: Run one (or few), get results, decide next experiment(s)
   - **Batch**: Must plan all experiments upfront
   - **Hybrid**: Sequential with occasional batches

3. **"How expensive is each experiment?"**
   - **Very expensive**: >$1000 or >1 day per experiment
   - **Moderate**: $100-$1000 or hours per experiment
   - **Cheap**: <$100 or minutes per experiment

4. **"How many factors are you investigating?"**
   - **1-5 factors**: Full factorial, RSM feasible
   - **6-15 factors**: Need screening or fractional designs
   - **>15 factors**: Definitive screening, regularization needed

5. **"Do you have prior knowledge, existing data, or a mechanistic model?"**
   - **Have model**: Use model-driven optimal designs
   - **Have data**: Warm-start Bayesian optimization
   - **No knowledge**: Need exploration, space-filling designs

### Based on Answers, Recommend:

```
Sequential + Expensive + Unknown landscape
    → Bayesian Optimization (GP + Expected Improvement)

Sequential + Have model + Parameter estimation goal
    → Model-driven sequential optimal design

Batch only + Screening goal + Many factors
    → Fractional factorial or Definitive Screening Design

Batch only + Optimization + Few factors
    → Central Composite Design or Box-Behnken

Sequential + Moderate cost + Want model
    → Active learning with Gaussian Process

Batch only + No prior knowledge + Exploration
    → Latin Hypercube Sampling
```

## Quick Decision Tree

```
Can experiments be run sequentially with feedback?
│
├─ YES (Sequential possible)
│   │
│   ├─ Expensive experiments (>$1000 or >1 day each)?
│   │   ├─ YES → Bayesian Optimization
│   │   │        • Expected Improvement for optimization
│   │   │        • Upper Confidence Bound for exploration
│   │   │        • Tools: GPyOpt, scikit-optimize, BoTorch
│   │   │
│   │   └─ NO → Have a model?
│   │       ├─ YES → Model-driven sequential design
│   │       │        • D-optimal for parameter estimation
│   │       │        • Update design as parameters learned
│   │       │
│   │       └─ NO → Active learning
│   │                • GP with uncertainty sampling
│   │                • Tools: modAL, custom GP
│   │
└─ NO (Batch only)
    │
    ├─ What's your goal?
    │   │
    │   ├─ SCREENING (identify important factors)
    │   │   ├─ <20 runs available → Plackett-Burman, Fractional Factorial
    │   │   ├─ 20-50 runs → Definitive Screening Design
    │   │   └─ Tools: pyDOE3, dexpy
    │   │
    │   ├─ OPTIMIZATION (find best settings)
    │   │   ├─ 2-5 factors → Central Composite Design, Box-Behnken
    │   │   ├─ >5 factors → Sequential screening → then optimize
    │   │   ├─ Have model → D-optimal or I-optimal
    │   │   └─ Tools: pyDOE3, pycse, statsmodels
    │   │
    │   ├─ EXPLORATION (understand system)
    │   │   ├─ No prior → Latin Hypercube Sampling
    │   │   ├─ Build surrogate → Space-filling + modeling
    │   │   └─ Tools: pyDOE3, pycse, scipy
    │   │
    │   └─ ROBUSTNESS (minimize variability)
    │       └─ Control + noise factors → Taguchi / Robust Parameter Design
```

## When to Use Each Approach

### Classical DOE (Batch Experiments)

**Use when:**
- Must plan all experiments upfront
- Well-understood system or standard optimization
- Moderate number of factors (<15)
- Experiments are cheap enough for comprehensive coverage

**Best for:**
- Screening many factors (Plackett-Burman, fractional factorial)
- Response surface modeling (CCD, Box-Behnken)
- Standard process optimization
- Teaching/learning DOE concepts

**Tools:** pyDOE3, dexpy, pycse, statsmodels

### Bayesian Optimization (Sequential)

**Use when:**
- Can run experiments one-at-a-time (or small batches)
- Experiments are expensive (time, money, resources)
- Black-box system (no mechanistic model)
- Want to minimize total number of experiments

**Best for:**
- Optimizing expensive processes ($1000+ per run)
- Materials discovery, drug screening
- Hyperparameter tuning for ML models
- Autonomous experimentation / self-driving labs

**Tools:** GPyOpt, scikit-optimize, BoTorch, Ax

### Model-Driven DOE (Optimal Designs)

**Use when:**
- Have mechanistic or empirical model
- Goal is parameter estimation or model discrimination
- Want statistically optimal experiments
- Can update designs based on current parameter estimates

**Best for:**
- Chemical kinetics (rate constant estimation)
- Pharmacokinetics (PK parameter estimation)
- Systems biology (model calibration)
- Comparing competing models

**Tools:** Custom implementation with Fisher Information Matrix, pyoptex

### Active Learning (Sequential Model Building)

**Use when:**
- Want to build accurate surrogate model efficiently
- Can run experiments sequentially
- Need to balance exploration and exploitation
- Moderate experiment cost

**Best for:**
- Adaptive sampling for complex landscapes
- Building GP surrogates for later optimization
- Uncertainty quantification
- Smart data collection

**Tools:** modAL, scikit-learn, GPy

## Quick Reference Table

| Situation | Recommended Approach | Key Tool | Typical # Runs |
|-----------|---------------------|----------|----------------|
| Batch, <5 factors, screening | Full/Fractional Factorial | pyDOE3 | 8-32 |
| Batch, 6-15 factors, screening | Plackett-Burman, DSD | pyDOE3, dexpy | 12-50 |
| Batch, optimization, 2-5 factors | CCD, Box-Behnken | pyDOE3, pycse | 13-50 |
| Batch, exploration, unknown | Latin Hypercube | pyDOE3, pycse | 10×factors |
| **Sequential, expensive, optimize** | **Bayesian Optimization** | **GPyOpt, skopt** | **10-50** |
| Sequential, build model | Active Learning + GP | modAL | 20-100 |
| Have mechanistic model | Model-driven D-optimal | Custom FIM | 10-30 |
| Parameter estimation | D-optimal, A-optimal | pyoptex | Varies |
| Model discrimination | T-optimal, KL-optimal | Custom | 10-20 |
| Multiple objectives | Multi-objective BO | BoTorch | 30-100 |
| Mixture components | Simplex designs | pyDOE3 | 10-30 |

## Quick Start Examples

### Example 1: Classical Response Surface (Batch)

**Situation:** Optimize 3 factors, batch experiments, moderate cost

```python
import pyDOE3 as pyd
import pandas as pd

# Generate Central Composite Design
n_factors = 3
design = pyd.ccdesign(n_factors, center=(0, 4))  # With center points

# Create DataFrame with factor names
factors = ['Temperature', 'Pressure', 'Catalyst']
df = pd.DataFrame(design, columns=factors)

# Scale to actual ranges
ranges = {'Temperature': (300, 400),
          'Pressure': (1, 5),
          'Catalyst': (0.1, 1.0)}

for factor, (low, high) in ranges.items():
    df[factor] = df[factor] * (high - low)/2 + (high + low)/2

print(f"Generated {len(df)} experiments")
print(df.head())

# Export for lab work
df.to_csv('experimental_design.csv', index=False)
```

**Next steps:**
1. Run experiments and collect responses
2. Analyze with statsmodels or pycse
3. Optimize using fitted model

### Example 2: pycse Surface Response

**Situation:** Quick RSM with integrated analysis

```python
from pycse import design_sr, analyze_sr, sr_parity
import numpy as np

# Generate design
bounds = np.array([[300, 400],   # Temperature
                   [1, 5],        # Pressure
                   [0.1, 1.0]])   # Catalyst

design = design_sr(bounds,
                   inputs=['Temperature', 'Pressure', 'Catalyst'],
                   outputs=['Yield'])

print(design)

# After running experiments, add results
design['Yield'] = [78, 82, 75, 88, 91, 85, 79, ...]  # Your data

# Analyze
anova_table = analyze_sr(design)
print(anova_table)

# Parity plot (model fit)
sr_parity(design, show=True)
```

**Advantages:** Integrated workflow, automatic ANOVA, quick visualization

### Example 3: Bayesian Optimization (Sequential)

**Situation:** Expensive experiments, 4 factors, want to minimize total runs

```python
import numpy as np
from skopt import gp_minimize
from skopt.space import Real
from skopt.plots import plot_convergence

# Define parameter space
space = [
    Real(300, 400, name='Temperature'),
    Real(1, 5, name='Pressure'),
    Real(0.1, 1.0, name='Catalyst'),
    Real(10, 60, name='Time')
]

# Your black-box function (returns value to minimize)
def expensive_experiment(params):
    temp, pressure, catalyst, time = params

    # Run actual experiment here
    # For now, simulate
    yield_value = run_experiment(temp, pressure, catalyst, time)

    return -yield_value  # Minimize negative = maximize yield

# Bayesian optimization
result = gp_minimize(
    expensive_experiment,
    space,
    n_calls=30,          # Maximum experiments
    n_random_starts=5,   # Initial random exploration
    acq_func='EI',       # Expected Improvement
    random_state=42
)

print(f"Best parameters: {result.x}")
print(f"Best yield: {-result.fun:.2f}")

# Visualize convergence
plot_convergence(result)
```

**Workflow:**
1. Start with 5 random experiments (exploration)
2. Fit GP surrogate model
3. Suggest next experiment (maximize EI)
4. Run experiment, update model
5. Repeat until convergence

### Example 4: Model-Driven D-Optimal (Parameter Estimation)

**Situation:** Have kinetic model, need to estimate 3 rate constants

```python
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import det

# Your mechanistic model
def model(t, k1, k2, k3):
    """Concentration vs time model"""
    return k1 * (1 - np.exp(-k2 * t)) + k3 * t

# Fisher Information Matrix for given design points
def fisher_information(t_design, k_guess):
    """Calculate FIM for design points t"""
    k1, k2, k3 = k_guess

    # Jacobian (sensitivity matrix)
    J = np.zeros((len(t_design), 3))

    for i, t in enumerate(t_design):
        J[i, 0] = 1 - np.exp(-k2 * t)
        J[i, 1] = k1 * t * np.exp(-k2 * t)
        J[i, 2] = t

    # FIM = J^T * J (assuming constant variance)
    FIM = J.T @ J
    return FIM

# D-optimal criterion: maximize determinant of FIM
def d_optimal_criterion(t_design, k_guess):
    FIM = fisher_information(t_design, k_guess)
    return -np.log(det(FIM))  # Maximize det = minimize -log(det)

# Find optimal design points
k_initial_guess = [1.0, 0.1, 0.05]
n_points = 6

result = minimize(
    lambda t: d_optimal_criterion(t, k_initial_guess),
    x0=np.linspace(0, 100, n_points),
    bounds=[(0, 100)] * n_points,
    method='L-BFGS-B'
)

optimal_times = result.x
print(f"Optimal measurement times: {optimal_times}")

# Run experiments at these times
# After getting data, update k_guess and re-optimize design if sequential
```

**Sequential workflow:**
1. Initial guess for parameters
2. Calculate D-optimal design
3. Run experiments
4. Fit model, update parameter estimates
5. Recalculate optimal design with new estimates
6. Repeat until parameters converge

### Example 5: Active Learning (Build Surrogate)

**Situation:** Want accurate surrogate model, can run sequentially

```python
from modAL.models import ActiveLearner
from modAL.uncertainty import uncertainty_sampling
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

# Initial random sample
X_initial = np.random.uniform([0, 0], [10, 10], size=(5, 2))
y_initial = [expensive_function(x) for x in X_initial]

# Create active learner with GP
regressor = GaussianProcessRegressor(kernel=RBF())
learner = ActiveLearner(
    estimator=regressor,
    query_strategy=uncertainty_sampling,  # Query where uncertain
    X_training=X_initial,
    y_training=y_initial
)

# Active learning loop
n_queries = 20
for i in range(n_queries):
    # Query next experiment (highest uncertainty)
    query_idx, query_instance = learner.query(X_candidate_pool)

    # Run experiment
    y_new = expensive_function(query_instance[0])

    # Update model
    learner.teach(query_instance, y_new)

    print(f"Iteration {i+1}: GP std = {learner.predict(query_instance)[1]:.4f}")

# Final model is in learner.estimator
```

## Workflow: How to Use This Skill

### Step 1: Answer Questions

When starting a DOE project, expect these questions:

1. What's your experimental goal?
2. Can you run sequentially or batch only?
3. How expensive are experiments?
4. How many factors?
5. Do you have a model or prior data?
6. Any constraints on factor combinations?
7. What's your total budget (# experiments)?

### Step 2: Get Recommendation

Based on answers, receive:
- **Recommended approach** with rationale
- **Alternative options** with trade-offs
- **Estimated number of runs** needed
- **Library/tool recommendations**
- **Example code** to get started

### Step 3: Generate Design

Use provided code to:
- Generate design matrix
- Visualize design in factor space
- Check design properties
- Export to CSV for lab work

### Step 4: Run Experiments

Execute experiments according to design:
- Randomize run order (unless sequential)
- Record all results
- Note any deviations or issues

### Step 5: Analyze Results

Analyze data with appropriate methods:
- **Classical**: ANOVA, regression, diagnostics
- **Bayesian**: Update GP, check convergence
- **Model-driven**: Fit model, assess parameters

### Step 6: Make Decisions

Based on analysis:
- **Classical**: Optimize response, validate
- **Bayesian**: Continue or stop? Next experiment?
- **Model-driven**: Parameters converged? Need more data?

## Detailed References

For deep dives into specific topics:

- **references/DESIGN_SELECTION_GUIDE.md** - Complete decision trees with questions
- **references/CLASSICAL_DOE.md** - Factorial, RSM, screening designs
- **references/BAYESIAN_OPTIMIZATION.md** - BO theory, acquisition functions, GP models
- **references/MODEL_DRIVEN_DOE.md** - Optimal designs, Fisher Information
- **references/ACTIVE_LEARNING.md** - Sequential strategies, uncertainty sampling
- **references/ANALYSIS_METHODS.md** - Statistical analysis, ANOVA, diagnostics
- **references/PYCSE_INTEGRATION.md** - Using pycse for RSM workflows

## Common Patterns by Industry

**Chemical Engineering:**
- Reactor optimization → CCD or Bayesian Optimization
- Catalyst screening → Fractional factorial → BO on hits
- Process development → Sequential model-driven DOE

**Materials Science:**
- Composition optimization → Mixture designs or BO
- Property mapping → Latin Hypercube + GP surrogate
- Alloy discovery → High-throughput with active learning

**Pharmaceutical:**
- Formulation → Mixture designs, response surface
- Dose optimization → Bayesian optimization
- PK/PD modeling → Model-driven D-optimal designs

**Manufacturing:**
- Process parameter tuning → CCD or Box-Behnken
- Quality improvement → Taguchi, robust parameter design
- Continuous improvement → Sequential BO

**Machine Learning:**
- Hyperparameter tuning → Bayesian optimization
- Architecture search → BO with discrete/categorical variables
- Neural network training → Adaptive sampling

## Installation

```bash
# Classical DOE
pip install pyDOE3          # Factorial, RSM, LHS
pip install dexpy           # Modern DOE library

# pycse for integrated RSM
pip install pycse

# Bayesian Optimization
pip install scikit-optimize # skopt - easiest to use
pip install GPyOpt          # Comprehensive BO
pip install ax-platform     # Meta's adaptive experimentation
# pip install botorch torch # Advanced BO (requires PyTorch)

# Active Learning
pip install modAL           # Active learning framework

# Gaussian Processes
pip install GPy             # GP models
# scikit-learn has GP built-in

# Analysis
pip install statsmodels     # ANOVA, regression
pip install scipy           # Optimization, statistics
pip install scikit-learn    # ML models, cross-validation

# Visualization
pip install matplotlib seaborn plotly

# Sensitivity Analysis
pip install SALib

# All in one
pip install pyDOE3 dexpy pycse scikit-optimize statsmodels scipy scikit-learn modAL GPy matplotlib seaborn
```

## Best Practices

### 1. Always Start with Questions

**❌ Don't:** "I'll use a Box-Behnken design"
**✅ Do:** "My goal is optimization, I have 3 factors, I can only batch, so Box-Behnken makes sense"

### 2. Match Method to Constraints

- **Budget limited** → Bayesian optimization
- **Time limited** → Batch classical DOE
- **Knowledge limited** → Space-filling exploration
- **Have model** → Model-driven optimal design

### 3. Sequential When Possible

Sequential designs (BO, active learning, model-driven):
- **Adapt** based on results
- **Stop early** if converged
- **Avoid wasted** experiments
- **Total runs** usually fewer than batch

**When batch is better:**
- Parallel equipment available
- Setup cost dominates run cost
- Well-understood system

### 4. Start Simple, Add Complexity

**Initial phase:** Simple screening (fractional factorial, LHS)
**Refinement:** Focus on important factors (RSM, BO)
**Validation:** Confirmation runs

### 5. Validate Assumptions

**Classical DOE assumes:**
- Normal residuals
- Constant variance
- Independent observations
- Linear/quadratic model adequate

**Check diagnostics:** Residual plots, Q-Q plots, lack-of-fit tests

**Bayesian optimization assumes:**
- GP model appropriate
- Kernel choice reasonable
- Enough initial exploration

**Check:** GP posterior uncertainty, kernel hyperparameters

### 6. Use Confirmation Experiments

After finding "optimum":
- Run additional experiments at predicted best settings
- Verify predictions match reality
- Account for prediction uncertainty

## Common Pitfalls

### 1. Using Wrong Design Type

**Problem:** Applying batch RSM to expensive experiments
**Solution:** Ask questions first, consider sequential approaches

### 2. Too Few Initial Points (BO)

**Problem:** GP needs diverse data to model landscape
**Solution:** Start with 5-10 space-filling points (LHS)

### 3. Ignoring Constraints

**Problem:** Design suggests infeasible experiments
**Solution:** Specify constraints upfront, use constrained optimization

### 4. Overfitting Surrogate Models

**Problem:** GP fits noise, poor predictions
**Solution:** Cross-validation, hold-out test sets, regularization

### 5. Not Randomizing Run Order

**Problem:** Systematic effects confounded with factors
**Solution:** Randomize execution order (except sequential designs)

### 6. Stopping Too Early (Sequential)

**Problem:** Declare convergence before truly converged
**Solution:** Use stopping criteria (EI < threshold, GP uncertainty low)

## Cost-Benefit Analysis: Sequential vs Batch

### When Sequential is Worth It:

**Expensive experiments:**
- Batch CCD: 20 runs at $1000 = $20,000
- Sequential BO: 15 runs (converge early) = $15,000
- **Savings: $5,000 + better result**

**Complex landscapes:**
- Batch might miss global optimum
- Sequential adapts to findings
- **Better final result**

### When Batch is Better:

**Cheap experiments:**
- Batch: 30 runs in 1 day (parallel)
- Sequential: 30 runs over 30 days
- **Time savings dominate**

**Setup costs:**
- If setup takes hours, run time minutes
- Batch amortizes setup
- **Sequential overhead too high**

## Response Format

When helping with DOE, Claude should:

1. **Ask questions first** - Don't assume method
2. **Explain recommendation** - Why this approach for their situation
3. **Provide complete code** - Working examples, not pseudocode
4. **Show alternatives** - "BO is best, but if you must batch, try..."
5. **Guide through workflow** - Design → Execute → Analyze → Optimize
6. **Interpret results** - Statistical significance AND practical significance

## Additional Resources

- **pyDOE3 Documentation:** https://pydoe3.readthedocs.io/
- **pycse Examples:** https://kitchingroup.cheme.cmu.edu/pycse/
- **scikit-optimize:** https://scikit-optimize.github.io/
- **GPyOpt:** https://sheffieldml.github.io/GPyOpt/
- **Bayesian Optimization Book:** https://bayesoptbook.com/
- **Design of Experiments (Montgomery):** Classic textbook
- **Statistics for Experimenters (Box, Hunter, Hunter):** Comprehensive reference

## Related Skills

- `python-optimization` - Response optimization after DOE
- `pycse` - Includes regression, ANOVA, confidence intervals for analysis
- `python-multiobjective-optimization` - Multi-response optimization
- `python-plotting` - Visualization of results and diagnostics
