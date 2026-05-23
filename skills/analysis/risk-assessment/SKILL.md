---
name: risk-assessment
version: "1.0.0"
category: engineering
description: "Risk Assessment Skill"
---

# Risk Assessment Skill

```yaml
name: risk-assessment
version: 1.0.0
category: sme
tags: [risk, probabilistic, monte-carlo, reliability, uncertainty, sensitivity-analysis, marine-safety]
created: 2026-01-06
updated: 2026-01-06
author: Claude
description: |
  Expert risk assessment and probabilistic analysis for marine and offshore
  operations. Includes Monte Carlo simulations, reliability calculations,
  uncertainty quantification, and decision-making under risk.
```

## When to Use This Skill

Use this skill when you need to:
- Perform Monte Carlo simulations for uncertainty quantification
- Calculate system reliability and failure probabilities
- Conduct sensitivity analysis to identify critical parameters
- Create risk matrices for hazard assessment
- Perform probabilistic design and analysis
- Quantify uncertainties in marine operations
- Make decisions under uncertainty with risk metrics
- Validate designs against reliability targets

## Core Knowledge Areas

### 1. Monte Carlo Simulation

Basic Monte Carlo framework:

```python
import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple, Optional
import pandas as pd

@dataclass
class RandomVariable:
    """Statistical distribution for a random variable."""
    name: str
    distribution: str  # 'normal', 'lognormal', 'uniform', 'weibull', etc.
    parameters: dict  # Distribution-specific parameters

    def sample(self, size: int = 1) -> np.ndarray:
        """
        Generate random samples from distribution.

        Args:
            size: Number of samples

        Returns:
            Array of random samples

        Example:
            >>> rv = RandomVariable(
            ...     name='wave_height',
            ...     distribution='weibull',
            ...     parameters={'c': 2.0, 'scale': 3.5}
            ... )
            >>> samples = rv.sample(1000)
        """
        if self.distribution == 'normal':
            return np.random.normal(
                loc=self.parameters['mean'],
                scale=self.parameters['std'],
                size=size
            )
        elif self.distribution == 'lognormal':
            return np.random.lognormal(
                mean=self.parameters['mean'],
                sigma=self.parameters['std'],
                size=size
            )
        elif self.distribution == 'uniform':
            return np.random.uniform(
                low=self.parameters['min'],
                high=self.parameters['max'],
                size=size
            )
        elif self.distribution == 'weibull':
            return stats.weibull_min.rvs(
                c=self.parameters['c'],
                scale=self.parameters['scale'],
                size=size
            )
        elif self.distribution == 'exponential':
            return np.random.exponential(
                scale=self.parameters['scale'],
                size=size
            )
        else:
            raise ValueError(f"Unknown distribution: {self.distribution}")

def monte_carlo_simulation(
    model: Callable,
    random_variables: List[RandomVariable],
    n_samples: int = 10000,
    seed: Optional[int] = None
) -> Dict[str, np.ndarray]:
    """
    Perform Monte Carlo simulation.

    Args:
        model: Function that takes random variable samples and returns result
        random_variables: List of RandomVariable objects
        n_samples: Number of Monte Carlo samples
        seed: Random seed for reproducibility

    Returns:
        Dictionary with input samples and output results

    Example:
        >>> def mooring_tension_model(wave_height, current_speed):
        ...     # Simplified mooring tension model
        ...     return 1000 + 150 * wave_height + 50 * current_speed
        >>>
        >>> rv_wave = RandomVariable(
        ...     'wave_height',
        ...     'weibull',
        ...     {'c': 2.0, 'scale': 3.5}
        ... )
        >>> rv_current = RandomVariable(
        ...     'current_speed',
        ...     'normal',
        ...     {'mean': 1.0, 'std': 0.3}
        ... )
        >>>
        >>> results = monte_carlo_simulation(
        ...     model=lambda samples: mooring_tension_model(
        ...         samples['wave_height'],
        ...         samples['current_speed']
        ...     ),
        ...     random_variables=[rv_wave, rv_current],
        ...     n_samples=10000
        ... )
    """
    if seed is not None:
        np.random.seed(seed)

    # Generate samples for all random variables
    samples = {}
    for rv in random_variables:
        samples[rv.name] = rv.sample(n_samples)

    # Run model for all samples
    outputs = model(samples)

    # Combine inputs and outputs
    results = {**samples, 'output': outputs}

    return results

def calculate_statistics(
    data: np.ndarray,
    percentiles: List[float] = [5, 50, 95]
) -> dict:
    """
    Calculate statistical parameters from Monte Carlo results.

    Args:
        data: Array of simulation results
        percentiles: Percentile values to calculate

    Returns:
        Dictionary with statistics

    Example:
        >>> stats = calculate_statistics(results['output'])
        >>> print(f"Mean: {stats['mean']:.1f}")
        >>> print(f"Std: {stats['std']:.1f}")
        >>> print(f"95th percentile: {stats['p95']:.1f}")
    """
    stats_dict = {
        'mean': np.mean(data),
        'std': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        'median': np.median(data),
        'cv': np.std(data) / np.mean(data)  # Coefficient of variation
    }

    # Add percentiles
    for p in percentiles:
        stats_dict[f'p{p}'] = np.percentile(data, p)

    return stats_dict
```

### 2. Reliability Analysis

Calculate reliability and failure probability:

```python
def calculate_reliability(
    response_data: np.ndarray,
    limit_state: float,
    mode: str = 'less_than'
) -> dict:
    """
    Calculate reliability from Monte Carlo results.

    Args:
        response_data: Array of response values
        limit_state: Limit state threshold
        mode: 'less_than' or 'greater_than'

    Returns:
        Dictionary with reliability metrics

    Example:
        >>> # Mooring tension should be < 8000 kN
        >>> reliability = calculate_reliability(
        ...     response_data=results['output'],
        ...     limit_state=8000,
        ...     mode='less_than'
        ... )
        >>> print(f"Reliability: {reliability['reliability']:.4f}")
        >>> print(f"Probability of failure: {reliability['pf']:.6f}")
    """
    n_samples = len(response_data)

    if mode == 'less_than':
        # Failure when response >= limit_state
        failures = response_data >= limit_state
    elif mode == 'greater_than':
        # Failure when response <= limit_state
        failures = response_data <= limit_state
    else:
        raise ValueError(f"Unknown mode: {mode}")

    n_failures = np.sum(failures)
    pf = n_failures / n_samples  # Probability of failure
    reliability = 1 - pf

    # Reliability index (beta)
    # β = -Φ^(-1)(Pf) where Φ is standard normal CDF
    if pf > 0 and pf < 1:
        beta = -stats.norm.ppf(pf)
    elif pf == 0:
        beta = np.inf
    else:  # pf == 1
        beta = -np.inf

    return {
        'n_samples': n_samples,
        'n_failures': n_failures,
        'pf': pf,
        'reliability': reliability,
        'beta': beta,
        'target_met': reliability >= 0.9999  # Example: 4-9's reliability
    }

def system_reliability_series(
    component_reliabilities: List[float]
) -> float:
    """
    Calculate system reliability for series system.

    Series system: All components must work for system to work.

    Args:
        component_reliabilities: List of component reliabilities

    Returns:
        System reliability

    Example:
        >>> # 3 mooring lines in series (all must hold)
        >>> R_sys = system_reliability_series([0.999, 0.9995, 0.998])
        >>> print(f"System reliability: {R_sys:.6f}")
    """
    # R_sys = Π R_i (product of all component reliabilities)
    R_sys = np.prod(component_reliabilities)
    return R_sys

def system_reliability_parallel(
    component_reliabilities: List[float]
) -> float:
    """
    Calculate system reliability for parallel system.

    Parallel system: At least one component must work for system to work.

    Args:
        component_reliabilities: List of component reliabilities

    Returns:
        System reliability

    Example:
        >>> # 3 redundant mooring lines (only 1 needs to hold)
        >>> R_sys = system_reliability_parallel([0.95, 0.95, 0.95])
        >>> print(f"System reliability: {R_sys:.6f}")
    """
    # R_sys = 1 - Π(1 - R_i) (1 minus product of all failures)
    pf_components = [1 - R for R in component_reliabilities]
    pf_sys = np.prod(pf_components)
    R_sys = 1 - pf_sys
    return R_sys

def calculate_form_reliability(
    mean: np.ndarray,
    cov_matrix: np.ndarray,
    limit_state_gradient: np.ndarray
) -> dict:
    """
    First Order Reliability Method (FORM) for reliability analysis.

    Args:
        mean: Mean values of random variables
        cov_matrix: Covariance matrix
        limit_state_gradient: Gradient of limit state function at mean point

    Returns:
        Dictionary with FORM results

    Example:
        >>> # 2 random variables: Hs, Tp
        >>> mean = np.array([5.0, 10.0])
        >>> cov = np.array([[1.0, 0.5], [0.5, 2.0]])
        >>> gradient = np.array([150.0, 50.0])  # ∂g/∂Hs, ∂g/∂Tp
        >>> form_result = calculate_form_reliability(mean, cov, gradient)
        >>> print(f"Reliability index β: {form_result['beta']:.3f}")
    """
    # Reliability index: β = μ / sqrt(∇g^T Σ ∇g)
    # where μ is mean, Σ is covariance, ∇g is gradient

    numerator = np.dot(gradient, mean)
    denominator = np.sqrt(
        np.dot(gradient, np.dot(cov_matrix, gradient))
    )

    beta = numerator / denominator

    # Probability of failure from β
    pf = stats.norm.cdf(-beta)

    return {
        'beta': beta,
        'pf': pf,
        'reliability': 1 - pf
    }
```

### 3. Sensitivity Analysis

Identify critical parameters:

```python
def sensitivity_analysis_correlation(
    inputs: Dict[str, np.ndarray],
    output: np.ndarray
) -> pd.DataFrame:
    """
    Sensitivity analysis using correlation coefficients.

    Args:
        inputs: Dictionary of input variable samples
        output: Output variable samples

    Returns:
        DataFrame with correlation coefficients sorted by absolute value

    Example:
        >>> sensitivity = sensitivity_analysis_correlation(
        ...     inputs={
        ...         'wave_height': results['wave_height'],
        ...         'current_speed': results['current_speed'],
        ...         'wind_speed': results['wind_speed']
        ...     },
        ...     output=results['output']
        ... )
        >>> print(sensitivity)
    """
    correlations = {}

    for var_name, var_samples in inputs.items():
        # Pearson correlation coefficient
        corr = np.corrcoef(var_samples, output)[0, 1]
        correlations[var_name] = corr

    # Create DataFrame
    df = pd.DataFrame.from_dict(
        correlations,
        orient='index',
        columns=['correlation']
    )

    # Add absolute value and rank
    df['abs_correlation'] = df['correlation'].abs()
    df = df.sort_values('abs_correlation', ascending=False)
    df['rank'] = range(1, len(df) + 1)

    return df

def sensitivity_analysis_variance(
    inputs: Dict[str, np.ndarray],
    output: np.ndarray,
    n_partitions: int = 10
) -> pd.DataFrame:
    """
    Variance-based sensitivity analysis (Sobol indices approximation).

    Args:
        inputs: Dictionary of input variable samples
        output: Output variable samples
        n_partitions: Number of partitions for conditional variance

    Returns:
        DataFrame with sensitivity indices

    Example:
        >>> sensitivity = sensitivity_analysis_variance(
        ...     inputs=results,
        ...     output=results['output']
        ... )
    """
    total_variance = np.var(output)

    sensitivity_indices = {}

    for var_name, var_samples in inputs.items():
        if var_name == 'output':
            continue

        # Partition variable range
        percentiles = np.linspace(0, 100, n_partitions + 1)
        bins = np.percentile(var_samples, percentiles)

        # Calculate conditional variance
        conditional_means = []
        for i in range(n_partitions):
            mask = (var_samples >= bins[i]) & (var_samples < bins[i + 1])
            if np.sum(mask) > 0:
                conditional_means.append(np.mean(output[mask]))

        # Variance of conditional means
        variance_of_means = np.var(conditional_means)

        # First-order sensitivity index (approximation)
        S1 = variance_of_means / total_variance if total_variance > 0 else 0

        sensitivity_indices[var_name] = {
            'first_order': S1
        }

    # Create DataFrame
    df = pd.DataFrame.from_dict(sensitivity_indices, orient='index')
    df = df.sort_values('first_order', ascending=False)
    df['rank'] = range(1, len(df) + 1)

    return df

def tornado_plot_data(
    base_value: float,
    variables: Dict[str, dict],
    model: Callable
) -> pd.DataFrame:
    """
    Generate data for tornado diagram (one-at-a-time sensitivity).

    Args:
        base_value: Base case output value
        variables: Dict with variable names and {'low', 'high', 'nominal'} values
        model: Model function

    Returns:
        DataFrame with tornado plot data

    Example:
        >>> variables = {
        ...     'wave_height': {'low': 3.0, 'nominal': 5.0, 'high': 8.0},
        ...     'current_speed': {'low': 0.5, 'nominal': 1.0, 'high': 1.5}
        ... }
        >>> tornado_data = tornado_plot_data(
        ...     base_value=5000,
        ...     variables=variables,
        ...     model=mooring_model
        ... )
    """
    results = []

    for var_name, var_values in variables.items():
        # Calculate output at low and high values
        # (keeping other variables at nominal)

        inputs_low = {k: v['nominal'] for k, v in variables.items()}
        inputs_low[var_name] = var_values['low']
        output_low = model(inputs_low)

        inputs_high = {k: v['nominal'] for k, v in variables.items()}
        inputs_high[var_name] = var_values['high']
        output_high = model(inputs_high)

        # Calculate swing
        swing = abs(output_high - output_low)

        results.append({
            'variable': var_name,
            'output_low': output_low,
            'output_high': output_high,
            'swing': swing,
            'low_value': var_values['low'],
            'high_value': var_values['high']
        })

    df = pd.DataFrame(results)
    df = df.sort_values('swing', ascending=False)
    df['rank'] = range(1, len(df) + 1)

    return df
```

### 4. Risk Matrices and Hazard Assessment

```python
from enum import Enum

class Severity(Enum):
    """Consequence severity levels."""
    NEGLIGIBLE = 1
    MINOR = 2
    MODERATE = 3
    MAJOR = 4
    CATASTROPHIC = 5

class Likelihood(Enum):
    """Event likelihood levels."""
    RARE = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    ALMOST_CERTAIN = 5

class RiskLevel(Enum):
    """Risk level categories."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4

@dataclass
class Hazard:
    """Hazard definition."""
    id: str
    description: str
    severity: Severity
    likelihood: Likelihood
    existing_controls: List[str]
    residual_risk: Optional[RiskLevel] = None

def calculate_risk_level(
    severity: Severity,
    likelihood: Likelihood
) -> RiskLevel:
    """
    Calculate risk level from severity and likelihood.

    Uses 5x5 risk matrix.

    Args:
        severity: Consequence severity
        likelihood: Event likelihood

    Returns:
        Risk level

    Example:
        >>> risk = calculate_risk_level(
        ...     Severity.MAJOR,
        ...     Likelihood.POSSIBLE
        ... )
        >>> print(risk)  # RiskLevel.HIGH
    """
    # 5x5 risk matrix
    # Rows: Likelihood (1-5)
    # Columns: Severity (1-5)
    risk_matrix = np.array([
        [1, 1, 2, 2, 3],  # Rare
        [1, 2, 2, 3, 3],  # Unlikely
        [2, 2, 3, 3, 4],  # Possible
        [2, 3, 3, 4, 4],  # Likely
        [3, 3, 4, 4, 4]   # Almost Certain
    ])

    risk_value = risk_matrix[likelihood.value - 1, severity.value - 1]

    # Map to RiskLevel
    if risk_value == 1:
        return RiskLevel.LOW
    elif risk_value == 2:
        return RiskLevel.MEDIUM
    elif risk_value == 3:
        return RiskLevel.HIGH
    else:  # risk_value == 4
        return RiskLevel.VERY_HIGH

def assess_hazards(
    hazards: List[Hazard]
) -> pd.DataFrame:
    """
    Assess list of hazards and calculate risk levels.

    Args:
        hazards: List of Hazard objects

    Returns:
        DataFrame with hazard assessment

    Example:
        >>> hazards = [
        ...     Hazard(
        ...         id='H001',
        ...         description='Mooring line failure',
        ...         severity=Severity.MAJOR,
        ...         likelihood=Likelihood.UNLIKELY,
        ...         existing_controls=['Regular inspection', 'Design factor 2.5']
        ...     ),
        ...     Hazard(
        ...         id='H002',
        ...         description='Vessel collision',
        ...         severity=Severity.CATASTROPHIC,
        ...         likelihood=Likelihood.RARE,
        ...         existing_controls=['AIS', 'Exclusion zone', 'Radar']
        ...     )
        ... ]
        >>> assessment = assess_hazards(hazards)
    """
    results = []

    for hazard in hazards:
        risk_level = calculate_risk_level(hazard.severity, hazard.likelihood)

        results.append({
            'hazard_id': hazard.id,
            'description': hazard.description,
            'severity': hazard.severity.name,
            'likelihood': hazard.likelihood.name,
            'risk_level': risk_level.name,
            'controls': '; '.join(hazard.existing_controls)
        })

    df = pd.DataFrame(results)

    # Sort by risk level (descending)
    risk_order = {
        'VERY_HIGH': 4,
        'HIGH': 3,
        'MEDIUM': 2,
        'LOW': 1
    }
    df['risk_value'] = df['risk_level'].map(risk_order)
    df = df.sort_values('risk_value', ascending=False)
    df = df.drop('risk_value', axis=1)

    return df
```

### 5. Extreme Value Analysis

```python
from scipy.stats import genextreme

def fit_extreme_value_distribution(
    data: np.ndarray,
    method: str = 'gev'
) -> dict:
    """
    Fit extreme value distribution to data.

    Args:
        data: Array of extreme values (e.g., annual maxima)
        method: 'gev' (Generalized Extreme Value) or 'gumbel'

    Returns:
        Dictionary with fitted parameters and statistics

    Example:
        >>> # Annual maximum wave heights
        >>> annual_max_Hs = np.array([8.5, 9.2, 7.8, 10.1, 8.9, ...])
        >>> fit = fit_extreme_value_distribution(annual_max_Hs, 'gev')
        >>> print(f"Shape: {fit['shape']:.3f}")
        >>> print(f"Location: {fit['location']:.2f}")
        >>> print(f"Scale: {fit['scale']:.2f}")
    """
    if method == 'gev':
        # Fit GEV distribution
        shape, location, scale = genextreme.fit(data)

        # Calculate return values
        return_periods = [10, 50, 100, 1000, 10000]  # years
        return_values = {}

        for T in return_periods:
            # Return level for return period T
            p = 1 - 1/T
            x_T = genextreme.ppf(p, shape, loc=location, scale=scale)
            return_values[f'{T}yr'] = x_T

        return {
            'shape': shape,
            'location': location,
            'scale': scale,
            'return_values': return_values
        }

    elif method == 'gumbel':
        # Gumbel is special case of GEV with shape=0
        location, scale = stats.gumbel_r.fit(data)

        return_periods = [10, 50, 100, 1000, 10000]
        return_values = {}

        for T in return_periods:
            p = 1 - 1/T
            x_T = stats.gumbel_r.ppf(p, loc=location, scale=scale)
            return_values[f'{T}yr'] = x_T

        return {
            'shape': 0.0,  # Gumbel has shape = 0
            'location': location,
            'scale': scale,
            'return_values': return_values
        }

    else:
        raise ValueError(f"Unknown method: {method}")
```

## Complete Examples

### Example 1: Complete Mooring System Risk Assessment

```python
import numpy as np
from pathlib import Path

def complete_mooring_risk_assessment(
    design_parameters: dict,
    environmental_parameters: dict,
    n_simulations: int = 10000
) -> dict:
    """
    Complete probabilistic risk assessment for mooring system.

    Example:
        >>> design = {
        ...     'n_lines': 8,
        ...     'line_capacity': 10000,  # kN
        ...     'safety_factor': 2.5
        ... }
        >>> environment = {
        ...     'wave_height': {'distribution': 'weibull', 'c': 2.0, 'scale': 3.5},
        ...     'wave_period': {'distribution': 'normal', 'mean': 10.0, 'std': 2.0},
        ...     'current_speed': {'distribution': 'normal', 'mean': 1.0, 'std': 0.3}
        ... }
        >>> results = complete_mooring_risk_assessment(
        ...     design,
        ...     environment,
        ...     n_simulations=10000
        ... )
    """
    print("="*70)
    print("MOORING SYSTEM RISK ASSESSMENT")
    print("="*70)

    # Step 1: Define random variables
    print("\n[Step 1/6] Defining random variables...")

    random_vars = []
    for var_name, var_params in environment_parameters.items():
        rv = RandomVariable(
            name=var_name,
            distribution=var_params['distribution'],
            parameters={k: v for k, v in var_params.items() if k != 'distribution'}
        )
        random_vars.append(rv)
        print(f"  {var_name}: {var_params['distribution']}")

    # Step 2: Define mooring tension model
    print("\n[Step 2/6] Defining mooring tension model...")

    def mooring_tension_model(samples):
        """Simplified mooring tension model."""
        Hs = samples['wave_height']
        Tp = samples['wave_period']
        V_c = samples['current_speed']

        # Simplified empirical model
        tension = (
            1000 +  # Pretension
            200 * Hs +  # Wave contribution
            50 * Hs**2 / Tp +  # Dynamic amplification
            100 * V_c  # Current drag
        )

        return tension

    # Step 3: Run Monte Carlo simulation
    print(f"\n[Step 3/6] Running Monte Carlo simulation ({n_simulations} samples)...")

    mc_results = monte_carlo_simulation(
        model=mooring_tension_model,
        random_variables=random_vars,
        n_samples=n_simulations,
        seed=42
    )

    # Calculate statistics
    stats = calculate_statistics(mc_results['output'])

    print(f"  Mean tension: {stats['mean']:.1f} kN")
    print(f"  Std deviation: {stats['std']:.1f} kN")
    print(f"  95th percentile: {stats['p95']:.1f} kN")
    print(f"  Max: {stats['max']:.1f} kN")

    # Step 4: Reliability analysis
    print("\n[Step 4/6] Performing reliability analysis...")

    # Design limit (capacity / safety factor)
    design_limit = design_parameters['line_capacity'] / design_parameters['safety_factor']

    reliability_result = calculate_reliability(
        response_data=mc_results['output'],
        limit_state=design_limit,
        mode='less_than'
    )

    print(f"  Design limit: {design_limit:.1f} kN")
    print(f"  Probability of failure: {reliability_result['pf']:.6f}")
    print(f"  Reliability: {reliability_result['reliability']:.6f}")
    print(f"  Reliability index β: {reliability_result['beta']:.3f}")

    # Step 5: Sensitivity analysis
    print("\n[Step 5/6] Performing sensitivity analysis...")

    sensitivity = sensitivity_analysis_correlation(
        inputs={k: v for k, v in mc_results.items() if k != 'output'},
        output=mc_results['output']
    )

    print(f"\nSensitivity ranking:")
    for idx, row in sensitivity.iterrows():
        print(f"  {idx}: correlation = {row['correlation']:.3f}")

    # Step 6: System reliability
    print("\n[Step 6/6] Calculating system reliability...")

    # Assume independent mooring lines
    component_reliability = reliability_result['reliability']

    # Series system (all lines must hold for 100% intact)
    R_all_intact = system_reliability_series(
        [component_reliability] * design_parameters['n_lines']
    )

    # Parallel redundancy (system fails if all lines fail)
    R_total_failure = 1 - (1 - component_reliability)**design_parameters['n_lines']

    print(f"  Single line reliability: {component_reliability:.6f}")
    print(f"  All lines intact: {R_all_intact:.6f}")
    print(f"  Avoid total failure: {R_total_failure:.10f}")

    # Summary
    summary = {
        'statistics': stats,
        'reliability': reliability_result,
        'sensitivity': sensitivity,
        'system_reliability': {
            'all_intact': R_all_intact,
            'total_failure_avoidance': R_total_failure
        }
    }

    print("\n" + "="*70)
    print("ASSESSMENT COMPLETE")
    print("="*70)

    return summary

# Run assessment
design_parameters = {
    'n_lines': 8,
    'line_capacity': 10000,
    'safety_factor': 2.5
}

environmental_parameters = {
    'wave_height': {'distribution': 'weibull', 'c': 2.0, 'scale': 3.5},
    'wave_period': {'distribution': 'normal', 'mean': 10.0, 'std': 2.0},
    'current_speed': {'distribution': 'normal', 'mean': 1.0, 'std': 0.3}
}

risk_assessment = complete_mooring_risk_assessment(
    design_parameters,
    environmental_parameters,
    n_simulations=10000
)
```

## Best Practices

### 1. Sample Size Selection

```python
def determine_sample_size(
    target_pf: float,
    confidence_level: float = 0.95
) -> int:
    """
    Determine required sample size for target failure probability.

    Rule of thumb: N ≈ 10/Pf for reasonable confidence

    Args:
        target_pf: Target probability of failure
        confidence_level: Confidence level

    Returns:
        Recommended sample size

    Example:
        >>> n = determine_sample_size(target_pf=1e-4, confidence_level=0.95)
        >>> print(f"Recommended samples: {n}")
    """
    # Basic rule: need at least 10 failures
    # So N * Pf ≥ 10
    # N ≥ 10 / Pf

    n_basic = int(10 / target_pf)

    # For higher confidence, increase further
    if confidence_level >= 0.99:
        n_recommended = n_basic * 5
    elif confidence_level >= 0.95:
        n_recommended = n_basic * 3
    else:
        n_recommended = n_basic * 2

    return max(n_recommended, 1000)  # Minimum 1000 samples
```

### 2. Convergence Checking

```python
def check_monte_carlo_convergence(
    data: np.ndarray,
    window_size: int = 1000
) -> dict:
    """
    Check if Monte Carlo simulation has converged.

    Args:
        data: Simulation output data
        window_size: Window size for moving average

    Returns:
        Dictionary with convergence metrics
    """
    n = len(data)

    # Calculate cumulative mean
    cumulative_mean = np.cumsum(data) / np.arange(1, n + 1)

    # Calculate moving coefficient of variation
    if n > window_size:
        moving_std = np.std(data[-window_size:])
        moving_mean = np.mean(data[-window_size:])
        cov = moving_std / moving_mean if moving_mean != 0 else 0
    else:
        cov = np.std(data) / np.mean(data) if np.mean(data) != 0 else 0

    # Convergence criterion: COV < 5%
    converged = cov < 0.05

    return {
        'converged': converged,
        'cov': cov,
        'final_mean': cumulative_mean[-1],
        'samples_used': n
    }
```

## Resources

### Textbooks

- Ang, A.H-S., Tang, W.H. (2007). *Probability Concepts in Engineering*
- Melchers, R.E., Beck, A.T. (2018). *Structural Reliability Analysis and Prediction*
- DNV (2021). *DNVGL-RP-C205: Environmental Conditions and Environmental Loads*

### Standards

- **DNV-RP-C205**: Environmental conditions and environmental loads
- **DNV-RP-C206**: Fatigue methodology of offshore ships
- **ISO 2394**: General principles on reliability for structures
- **API RP 2A**: Planning, designing and constructing fixed offshore platforms

### Software

- **@RISK**: Monte Carlo simulation add-in for Excel
- **Crystal Ball**: Oracle's risk analysis software
- **OpenTURNS**: Open source library for uncertainty quantification
- **scipy.stats**: Python statistical distributions

---

**Use this skill for:** Expert probabilistic risk assessment and reliability analysis for marine and offshore systems with comprehensive uncertainty quantification.
