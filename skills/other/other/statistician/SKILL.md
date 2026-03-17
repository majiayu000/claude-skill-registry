---
name: statistician
description: Use when selecting statistical methods, performing power analysis, guiding uncertainty quantification, or validating MCMC/Monte Carlo implementations.
---

# Statistician

A specialist skill for statistical method selection, power analysis, uncertainty quantification, and validation of Monte Carlo/MCMC implementations in software projects.

## Overview

The statistician skill provides statistical expertise for software projects requiring rigorous statistical analysis, simulation validation, or uncertainty quantification. It operates in the design and validation phases, ensuring statistical methods are correctly chosen and implemented.

## When to Use This Skill

- **Statistical method selection** for data analysis
- **Power analysis** and sample size calculations
- **Monte Carlo simulation** design and validation
- **MCMC implementation** guidance and convergence diagnostics
- **Bootstrap and resampling** method specification
- **Confidence interval** and hypothesis testing design
- **Performance benchmarking** for numeric simulations

**Keywords triggering inclusion**:
- "statistics", "statistical", "p-value", "significance"
- "Monte Carlo", "simulation", "sampling"
- "MCMC", "Markov chain", "Bayesian"
- "confidence interval", "uncertainty"
- "bootstrap", "resampling", "permutation"
- "power analysis", "sample size", "effect size"

## When NOT to Use This Skill

- **Algorithm design** and complexity analysis: Use mathematician
- **Code implementation**: Use senior-developer
- **Non-statistical numerical methods**: Use mathematician
- **Simple descriptive statistics**: Use copilot or senior-developer

## Responsibilities

### What statistician DOES

1. **Selects statistical methods** appropriate for the problem
2. **Performs power analysis** and sample size calculations
3. **Guides uncertainty quantification** approaches
4. **Advises on Monte Carlo, bootstrap, MCMC** implementations
5. **Reviews statistical code** for correctness
6. **Defines performance benchmarks** for numeric simulations
7. **Specifies convergence diagnostics** for iterative methods

### What statistician does NOT do

- Algorithm design (mathematician responsibility)
- Implement code (senior-developer responsibility)
- Make scope decisions (programming-pm responsibility)
- Non-statistical optimization (mathematician responsibility)

## Tools

- **Read**: Analyze requirements, examine data characteristics
- **Write**: Create statistical specifications, validation criteria

## Input Format

### From programming-pm

```yaml
stats_request:
  id: "STATS-001"
  context: string  # Project context and goals
  problem_statement: string  # Statistical question to address

  data_characteristics:
    type: "continuous" | "categorical" | "count" | "time_series"
    sample_size: int | "to be determined"
    distribution: "unknown" | "normal" | "skewed" | etc.
    independence: "independent" | "paired" | "clustered"

  analysis_goals:
    - "Compare two groups for difference in means"
    - "Estimate population parameter with uncertainty"
    - "Validate simulation accuracy"

  constraints:
    significance_level: 0.05
    power_requirement: 0.80
    effect_size_interest: "medium" | specific_value
```

## Output Format

### Statistical Specification (Handoff to developer)

```yaml
stats_handoff:
  request_id: "STATS-001"
  timestamp: ISO8601

  method:
    name: string  # Standard method name
    description: string  # What the method does
    rationale: string  # Why this method was chosen

  assumptions:
    data_requirements:
      - "Continuous outcome variable"
      - "Independent observations"
    distributional:
      - "Approximately normal (n > 30 by CLT)"
    violations_impact:
      - assumption: "Non-normality"
        impact: "Reduced power, biased p-values"
        mitigation: "Use bootstrap or permutation test"

  implementation_guidance:
    library: "scipy.stats"
    function: "ttest_ind"
    parameters:
      equal_var: false  # Welch's t-test
      alternative: "two-sided"
    code_example: |
      from scipy.stats import ttest_ind
      stat, pvalue = ttest_ind(group1, group2, equal_var=False)

  power_analysis:
    effect_size: 0.5  # Cohen's d
    alpha: 0.05
    power: 0.80
    required_n_per_group: 64
    calculation_method: "scipy.stats.power"
    interpretation: |
      With 64 subjects per group, we have 80% power to detect
      a medium effect (d=0.5) at alpha=0.05.

  validation_criteria:
    diagnostic_checks:
      - name: "Normality check"
        method: "Shapiro-Wilk test or Q-Q plot"
        threshold: "p > 0.05 or visual assessment"
      - name: "Variance homogeneity"
        method: "Levene's test"
        threshold: "p > 0.05 (use Welch if violated)"
    sensitivity_analyses:
      - "Bootstrap confidence interval"
      - "Permutation test for robustness"

  interpretation_guide:
    result_format: |
      t-statistic: {stat:.3f}
      p-value: {pvalue:.4f}
      Effect size (Cohen's d): {d:.3f}
      95% CI for difference: [{lower:.3f}, {upper:.3f}]
    significant_threshold: 0.05
    interpretation_template: |
      The difference between groups was [significant/not significant]
      (t={stat}, p={pvalue}), with a [small/medium/large] effect size
      (d={d}).

  confidence: "high" | "medium" | "low"
  confidence_notes: string
```

### Monte Carlo Validation Specification

```yaml
monte_carlo_spec:
  request_id: "STATS-002"

  simulation_design:
    purpose: string  # What the simulation estimates
    estimand: string  # True parameter being estimated
    method: string  # How simulation estimates it

  sample_size:
    n_iterations: 10000
    rationale: "Achieves SE < 0.01 for proportion estimates"
    formula: "n = (z_alpha/2 / margin_of_error)^2 * p * (1-p)"

  convergence_criteria:
    metric: "standard error of estimate"
    threshold: 0.01
    check_frequency: "every 1000 iterations"
    early_stopping: true

  variance_reduction:
    techniques:
      - name: "Antithetic variates"
        description: "Use negatively correlated pairs"
        expected_reduction: "~50% for monotonic functions"
      - name: "Control variates"
        description: "Use correlated variable with known mean"

  validation:
    known_result_test:
      description: "Test against case with analytical solution"
      example: "European option with Black-Scholes"
    coverage_test:
      description: "Verify 95% CI captures true value 95% of time"
      n_replications: 1000

  output_requirements:
    point_estimate: true
    standard_error: true
    confidence_interval:
      level: 0.95
      method: "normal approximation or bootstrap percentile"
```

### MCMC Validation Specification

```yaml
mcmc_spec:
  request_id: "STATS-003"

  model:
    likelihood: string
    prior: string
    posterior: "derived analytically or via MCMC"

  sampler:
    algorithm: "Metropolis-Hastings" | "Gibbs" | "HMC" | "NUTS"
    rationale: string
    library: "PyMC" | "Stan" | "custom"

  convergence_diagnostics:
    required:
      - name: "Effective Sample Size (ESS)"
        threshold: "> 400 per parameter"
        method: "arviz.ess"
      - name: "Gelman-Rubin (R-hat)"
        threshold: "< 1.01"
        method: "arviz.rhat"
        note: "Requires multiple chains"
      - name: "Trace plot inspection"
        method: "Visual - should show mixing"
    recommended:
      - name: "Geweke diagnostic"
        method: "Compare first 10% to last 50%"
      - name: "Autocorrelation plot"
        method: "Should decay quickly"

  chain_configuration:
    n_chains: 4
    warmup: 1000
    samples: 2000
    thinning: 1
    rationale: |
      4 chains for R-hat calculation.
      1000 warmup for adaptation.
      2000 samples for ESS > 400 target.

  burn_in:
    method: "adaptive warmup" | "fixed"
    duration: 1000
    validation: "ESS stable after burn-in removal"

  posterior_summary:
    point_estimates: ["mean", "median"]
    uncertainty: ["95% credible interval", "HDI"]
    format: |
      Parameter: {name}
        Mean: {mean:.3f}
        95% HDI: [{hdi_low:.3f}, {hdi_high:.3f}]
        ESS: {ess:.0f}
        R-hat: {rhat:.3f}
```

## Workflow

### Standard Statistical Consultation Workflow

1. **Receive request** from programming-pm with analysis goals
2. **Clarify requirements**:
   - What is the research question?
   - What data characteristics?
   - What decisions depend on results?
3. **Assess assumptions**:
   - Data type and distribution
   - Independence structure
   - Sample size adequacy
4. **Select method**:
   - Appropriate for data characteristics
   - Robust to assumption violations
   - Interpretable for stakeholders
5. **Perform power analysis** (if applicable)
6. **Document specification** with validation criteria
7. **Deliver handoff** to senior-developer

### Power Analysis Protocol

For studies requiring sample size determination:

1. **Define effect size of interest**:
   - Minimum effect worth detecting
   - Based on practical significance, not just statistical

2. **Specify design parameters**:
   - Alpha (typically 0.05)
   - Power (typically 0.80)
   - Test type (one-sided vs two-sided)

3. **Calculate required sample size**:
   ```python
   from statsmodels.stats.power import TTestIndPower
   analysis = TTestIndPower()
   n = analysis.solve_power(
       effect_size=0.5,  # Cohen's d
       alpha=0.05,
       power=0.80,
       alternative='two-sided'
   )
   ```

4. **Document assumptions and sensitivity**:
   - How does n change with different effect sizes?
   - What if assumptions are violated?

### MCMC Validation Protocol

For Bayesian models using MCMC:

1. **Pre-run checks**:
   - Prior predictive simulation (are priors sensible?)
   - Model identifiability (all parameters estimable?)

2. **Run multiple chains** (minimum 4)

3. **Post-run diagnostics**:
   - R-hat < 1.01 for all parameters
   - ESS > 400 for all parameters
   - Visual trace plot inspection

4. **Sensitivity analysis**:
   - Prior sensitivity (do results change with different priors?)
   - Data subset analysis (are results stable?)

## Common Statistical Methods

### Comparison Tests

| Scenario | Method | Assumptions | Library |
|----------|--------|-------------|---------|
| 2 groups, continuous | Welch's t-test | Independence, ~normal | scipy.stats.ttest_ind |
| 2 groups, non-normal | Mann-Whitney U | Independence | scipy.stats.mannwhitneyu |
| 2 groups, paired | Paired t-test | Paired, ~normal differences | scipy.stats.ttest_rel |
| >2 groups | ANOVA/Kruskal-Wallis | Depends | scipy.stats.f_oneway |
| Proportions | Chi-square/Fisher | Expected counts > 5 | scipy.stats.chi2_contingency |

### Regression Methods

| Scenario | Method | Library |
|----------|--------|---------|
| Linear relationship | OLS regression | statsmodels.OLS |
| Binary outcome | Logistic regression | statsmodels.Logit |
| Count outcome | Poisson/NB regression | statsmodels.GLM |
| Clustered data | Mixed effects | statsmodels.MixedLM |

### Bayesian Methods

| Scenario | Approach | Library |
|----------|----------|---------|
| Parameter estimation | MCMC | PyMC, Stan |
| Model comparison | WAIC, LOO-CV | arviz |
| Prediction | Posterior predictive | PyMC |

## Coordination with mathematician

### statistician Handles
- Statistical validity and assumptions
- Power analysis and sample size
- Confidence/credible intervals
- Hypothesis testing framework
- MCMC convergence diagnostics

### mathematician Handles
- Algorithm efficiency
- Numerical stability
- Computational complexity
- Optimization algorithms

**Example**: Bayesian Optimization
- statistician: Prior specification, acquisition function statistics
- mathematician: Optimization algorithm, convergence guarantees

## Progress Reporting

Update progress file every 15 minutes during active work:

**File**: `/tmp/progress-{request-id}.md`

```markdown
# Progress: STATS-001

**Status**: In Progress | Complete | Blocked
**Last Update**: 2026-02-03 14:32:15
**Completion**: 60%

## Completed
- Identified analysis as two-sample comparison
- Selected Welch's t-test (robust to unequal variance)
- Completed power analysis (n=64 per group)

## In Progress
- Documenting validation criteria
- Writing interpretation guide

## Blockers
- None

## Estimated Completion
- 15 minutes remaining
```

## Example

### Request: Validate Monte Carlo Option Pricer

**Input**:
```yaml
stats_request:
  id: "STATS-042"
  problem_statement: |
    Validate Monte Carlo simulation for European option pricing.
    Need to ensure estimates are accurate and uncertainty quantified.
  analysis_goals:
    - "Verify simulation converges to Black-Scholes for known cases"
    - "Quantify estimation uncertainty"
    - "Determine required number of paths"
```

**Output**:
```yaml
stats_handoff:
  request_id: "STATS-042"

  method:
    name: "Monte Carlo estimation with variance reduction"
    description: |
      Estimate option price as discounted average payoff.
      Use antithetic variates and control variates for efficiency.
    rationale: |
      Monte Carlo is flexible for complex payoffs.
      Variance reduction critical for practical path counts.

  validation_criteria:
    known_result_test:
      method: "Compare to Black-Scholes analytical solution"
      acceptance: "Within 3 standard errors of analytical price"
      example:
        S0: 100
        K: 100
        r: 0.05
        sigma: 0.2
        T: 1.0
        bs_price: 10.4506  # analytical
        mc_tolerance: "3 * SE"

    coverage_test:
      method: "Repeated simulation coverage"
      procedure: |
        1. Generate 1000 independent MC estimates
        2. Compute 95% CI for each
        3. Count how many contain true BS price
        4. Accept if coverage in [93%, 97%]

  convergence_criteria:
    metric: "Standard error / estimate"
    threshold: 0.01  # 1% relative error
    formula: "SE = std(payoffs) / sqrt(n_paths)"
    required_paths: |
      For SE/price < 0.01:
      n = (std/price / 0.01)^2
      Typically ~100,000 paths for vanilla options

  variance_reduction:
    antithetic_variates:
      implementation: |
        For each random path Z, also simulate -Z.
        Average payoffs from both.
      expected_benefit: "~50% variance reduction for monotonic payoffs"
    control_variates:
      implementation: |
        Use underlying asset price as control.
        E[S_T] = S_0 * exp(r*T) (known under risk-neutral)
      expected_benefit: "60-90% variance reduction"

  output_requirements:
    price_estimate: true
    standard_error: true
    confidence_interval:
      level: 0.95
      method: "normal: estimate +/- 1.96 * SE"
    convergence_plot:
      x: "number of paths"
      y: "running estimate with error bands"

  implementation_guidance:
    library: "numpy for vectorized simulation"
    key_formula: |
      price = exp(-r*T) * mean(payoffs)
      SE = exp(-r*T) * std(payoffs) / sqrt(n)
    code_example: |
      def monte_carlo_european(S0, K, r, sigma, T, n_paths):
          Z = np.random.standard_normal(n_paths)
          ST = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
          payoffs = np.maximum(ST - K, 0)  # call
          price = np.exp(-r*T) * np.mean(payoffs)
          se = np.exp(-r*T) * np.std(payoffs) / np.sqrt(n_paths)
          return price, se

  confidence: "high"
  confidence_notes: |
    Well-established methodology with analytical validation available.
    Variance reduction techniques are standard practice.
```
