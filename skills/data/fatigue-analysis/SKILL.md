---
name: fatigue-analysis
version: 1.0.0
description: Fatigue analysis for offshore structures including S-N curves, rainflow counting, Miner's rule, and DNV standards
author: workspace-hub
category: subject-matter-expert
tags: [fatigue, s-n-curve, rainflow-counting, miners-rule, dnv, mooring-fatigue, structural-fatigue]
platforms: [engineering]
---

# Fatigue Analysis SME Skill

Comprehensive fatigue analysis expertise for offshore structures including mooring lines, risers, and structural components using industry-standard methods and DNV regulations.

## When to Use This Skill

Use fatigue analysis when:
- **Mooring line fatigue** - Calculate fatigue life of mooring components
- **Riser fatigue** - Analyze fatigue damage in flexible and rigid risers
- **Structural fatigue** - Assess fatigue in hull, joints, connections
- **S-N curve analysis** - Apply appropriate fatigue curves
- **Rainflow counting** - Process stress/load time series
- **Miner's rule** - Cumulative damage calculation
- **Fatigue design** - Size components for target life

## Core Knowledge Areas

### 1. S-N Curve Fundamentals

**S-N Curve Equation:**
```
N = a / (Δσ)^m

Where:
- N = Number of cycles to failure
- Δσ = Stress range
- a = S-N curve constant
- m = Slope of S-N curve (typically 3 for steel, 3-5 for welds)
```

**DNV S-N Curves:**
```python
import numpy as np

def get_dnv_sn_curve(
    curve_class: str,
    thickness: float = 25
) -> dict:
    """
    Get DNV S-N curve parameters.

    DNV-RP-C203 S-N curves:
    - B1: High strength welds, machined
    - C: Good quality welds
    - D: Normal welds
    - E: Rough welds
    - F, F1, F3: Poor quality, notches
    - G: Severe notches
    - W1, W2, W3: Seawater with cathodic protection

    Args:
        curve_class: DNV curve classification
        thickness: Plate thickness (mm) for thickness effect

    Returns:
        S-N curve parameters
    """
    # DNV-RP-C203 Table 2-1
    sn_curves = {
        'B1': {'log_a1': 15.117, 'm1': 4.0, 'log_a2': 17.146, 'm2': 5.0},
        'B2': {'log_a1': 14.885, 'm1': 4.0, 'log_a2': 16.856, 'm2': 5.0},
        'C':  {'log_a1': 12.592, 'm1': 3.0, 'log_a2': 16.320, 'm2': 5.0},
        'C1': {'log_a1': 12.449, 'm1': 3.0, 'log_a2': 16.081, 'm2': 5.0},
        'C2': {'log_a1': 12.301, 'm1': 3.0, 'log_a2': 15.835, 'm2': 5.0},
        'D':  {'log_a1': 12.164, 'm1': 3.0, 'log_a2': 15.606, 'm2': 5.0},
        'E':  {'log_a1': 11.972, 'm1': 3.0, 'log_a2': 15.350, 'm2': 5.0},
        'F':  {'log_a1': 11.699, 'm1': 3.0, 'log_a2': 14.832, 'm2': 5.0},
        'F1': {'log_a1': 11.546, 'm1': 3.0, 'log_a2': 14.576, 'm2': 5.0},
        'F3': {'log_a1': 11.398, 'm1': 3.0, 'log_a2': 14.330, 'm2': 5.0},
        'G':  {'log_a1': 11.245, 'm1': 3.0, 'log_a2': 14.080, 'm2': 5.0},
        'W1': {'log_a1': 11.764, 'm1': 3.0, 'log_a2': 15.091, 'm2': 5.0},
        'W2': {'log_a1': 11.533, 'm1': 3.0, 'log_a2': 14.706, 'm2': 5.0},
        'W3': {'log_a1': 11.262, 'm1': 3.0, 'log_a2': 14.183, 'm2': 5.0}
    }

    if curve_class not in sn_curves:
        raise ValueError(f"Unknown S-N curve class: {curve_class}")

    params = sn_curves[curve_class]

    # Convert log_a to a
    a1 = 10 ** params['log_a1']
    a2 = 10 ** params['log_a2']

    # Thickness correction (ref thickness = 25mm)
    if thickness > 25:
        t_factor = (25 / thickness) ** 0.25
        a1 *= t_factor ** params['m1']
        a2 *= t_factor ** params['m2']

    return {
        'class': curve_class,
        'a1': a1,
        'm1': params['m1'],
        'a2': a2,
        'm2': params['m2'],
        'thickness_mm': thickness
    }

# Example: Get F3 curve for mooring chain
sn_f3 = get_dnv_sn_curve('F3', thickness=127)  # 127mm chain

print(f"S-N Curve F3 (Chain):")
print(f"  a1 = {sn_f3['a1']:.2e}, m1 = {sn_f3['m1']}")
print(f"  a2 = {sn_f3['a2']:.2e}, m2 = {sn_f3['m2']}")
```

**Calculate Cycles to Failure:**
```python
def calculate_cycles_to_failure(
    stress_range: float,
    sn_curve: dict
) -> float:
    """
    Calculate cycles to failure for given stress range.

    N = a / (Δσ)^m

    Args:
        stress_range: Stress range (MPa)
        sn_curve: S-N curve parameters from get_dnv_sn_curve()

    Returns:
        Cycles to failure
    """
    # Use first segment if stress range is high
    # Switch to second segment if N > 1e7 (DNV bi-linear curve)

    N1 = sn_curve['a1'] / (stress_range ** sn_curve['m1'])

    if N1 <= 1e7:
        return N1
    else:
        # Use second segment
        N2 = sn_curve['a2'] / (stress_range ** sn_curve['m2'])
        return N2

# Example
stress_range = 50  # MPa
N = calculate_cycles_to_failure(stress_range, sn_f3)

print(f"Stress range: {stress_range} MPa")
print(f"Cycles to failure: {N:.2e}")
print(f"Years at 1 Hz: {N / (365.25 * 24 * 3600):.2f}")
```

### 2. Rainflow Counting

**Rainflow Algorithm:**
```python
def rainflow_counting(
    time_series: np.ndarray,
    bin_width: float = None
) -> tuple[np.ndarray, np.ndarray]:
    """
    Rainflow cycle counting algorithm.

    ASTM E1049-85 standard implementation.

    Args:
        time_series: Stress or load time series
        bin_width: Bin width for histogram (None = auto)

    Returns:
        (ranges, counts) - Stress ranges and cycle counts
    """
    # Simple peak-valley extraction
    peaks_valleys = []
    for i in range(1, len(time_series) - 1):
        if (time_series[i] > time_series[i-1] and time_series[i] > time_series[i+1]) or \
           (time_series[i] < time_series[i-1] and time_series[i] < time_series[i+1]):
            peaks_valleys.append(time_series[i])

    # Rainflow counting
    stack = []
    ranges = []

    for value in peaks_valleys:
        stack.append(value)

        while len(stack) >= 3:
            # Check for cycle
            X = abs(stack[-2] - stack[-3])
            Y = abs(stack[-1] - stack[-2])

            if len(stack) == 3:
                if Y >= X:
                    # Extract cycle
                    ranges.append(X)
                    stack.pop(-2)
                    stack.pop(-2)
                else:
                    break
            else:
                Z = abs(stack[-3] - stack[-4])
                if Y >= X and X >= Z:
                    # Extract cycle
                    ranges.append(X)
                    stack.pop(-2)
                    stack.pop(-2)
                else:
                    break

    # Create histogram
    ranges = np.array(ranges)

    if bin_width is None:
        bin_width = (np.max(ranges) - np.min(ranges)) / 20

    bins = np.arange(0, np.max(ranges) + bin_width, bin_width)
    counts, bin_edges = np.histogram(ranges, bins=bins)

    # Use bin centers
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    return bin_centers, counts

# Example: Mooring tension time series
t = np.linspace(0, 3600, 36000)  # 1 hour
tension = 2000 + 300 * np.sin(2*np.pi*t/10) + 100 * np.sin(2*np.pi*t/3) + 50*np.random.randn(len(t))

ranges, counts = rainflow_counting(tension, bin_width=10)

print(f"Rainflow cycles:")
print(f"  Total cycles: {np.sum(counts)}")
print(f"  Max range: {np.max(ranges):.1f} kN")
```

### 3. Miner's Rule (Cumulative Damage)

**Palmgren-Miner Damage:**
```python
def calculate_fatigue_damage_miners_rule(
    stress_ranges: np.ndarray,
    cycle_counts: np.ndarray,
    sn_curve: dict,
    design_factor: float = 10.0
) -> dict:
    """
    Calculate fatigue damage using Miner's rule.

    D = Σ(n_i / N_i)

    Where:
    - n_i = number of cycles at stress range i
    - N_i = cycles to failure at stress range i

    Args:
        stress_ranges: Array of stress ranges (MPa)
        cycle_counts: Array of cycle counts for each range
        sn_curve: S-N curve parameters
        design_factor: Safety factor (DNV: 10 for mooring)

    Returns:
        Fatigue damage and life prediction
    """
    total_damage = 0.0
    damage_breakdown = []

    for stress_range, n_cycles in zip(stress_ranges, cycle_counts):
        if stress_range > 0:
            # Cycles to failure
            N = calculate_cycles_to_failure(stress_range, sn_curve)

            # Damage contribution
            damage = n_cycles / N

            total_damage += damage

            damage_breakdown.append({
                'stress_range': stress_range,
                'cycles': n_cycles,
                'N_failure': N,
                'damage': damage,
                'damage_percent': 0  # Will be filled later
            })

    # Calculate percentage contributions
    for item in damage_breakdown:
        item['damage_percent'] = (item['damage'] / total_damage * 100) if total_damage > 0 else 0

    # Apply design factor
    total_damage_with_df = total_damage * design_factor

    # Fatigue life
    if total_damage > 0:
        fatigue_life = 1.0 / total_damage  # In units of analysis duration
    else:
        fatigue_life = np.inf

    return {
        'total_damage': total_damage,
        'damage_with_design_factor': total_damage_with_df,
        'fatigue_life': fatigue_life,
        'utilization': total_damage_with_df,
        'passed': total_damage_with_df <= 1.0,
        'breakdown': damage_breakdown
    }

# Example: Calculate fatigue damage
# Assume 1 hour of data, scale to 25 years
hours_per_year = 8760
design_life_years = 25
scale_factor = hours_per_year * design_life_years

# Convert tension ranges to stress (simplified)
stress_ranges = ranges / 100  # kN to MPa (simplified)
cycle_counts_scaled = counts * scale_factor

fatigue_result = calculate_fatigue_damage_miners_rule(
    stress_ranges,
    cycle_counts_scaled,
    sn_f3,
    design_factor=10.0
)

print(f"Fatigue Analysis Results:")
print(f"  Total damage: {fatigue_result['total_damage']:.4f}")
print(f"  With DF=10: {fatigue_result['damage_with_design_factor']:.4f}")
print(f"  Utilization: {fatigue_result['utilization']*100:.1f}%")
print(f"  Passed: {fatigue_result['passed']}")
print(f"  Fatigue life: {fatigue_result['fatigue_life']:.1f} years")
```

### 4. Spectral Fatigue Analysis

**Narrow-Band Spectral Method:**
```python
def spectral_fatigue_narrow_band(
    spectrum: np.ndarray,
    frequencies: np.ndarray,
    sn_curve: dict,
    duration: float,
    design_factor: float = 10.0
) -> dict:
    """
    Calculate fatigue damage using narrow-band spectral method.

    Assumes Rayleigh distribution of stress ranges.

    Args:
        spectrum: Stress response spectrum S(f)
        frequencies: Frequency array (Hz)
        sn_curve: S-N curve parameters
        duration: Duration of analysis (seconds)
        design_factor: Safety factor

    Returns:
        Fatigue damage
    """
    # Spectral moments
    m0 = np.trapz(spectrum, frequencies)
    m2 = np.trapz(spectrum * frequencies**2, frequencies)
    m4 = np.trapz(spectrum * frequencies**4, frequencies)

    # Zero-crossing frequency
    f0 = np.sqrt(m2 / m0)

    # Number of zero crossings in duration
    N0 = f0 * duration

    # Standard deviation of stress
    sigma = np.sqrt(m0)

    # Damage integral for Rayleigh distribution
    # D = N0 * (2*sigma)^m * Γ(1 + m/2) / a

    m = sn_curve['m1']  # Use first slope
    a = sn_curve['a1']

    from scipy.special import gamma

    damage = N0 * (2 * sigma)**m * gamma(1 + m/2) / a

    # Apply design factor
    damage_with_df = damage * design_factor

    # Fatigue life
    if damage > 0:
        fatigue_life = duration / damage
    else:
        fatigue_life = np.inf

    return {
        'total_damage': damage,
        'damage_with_design_factor': damage_with_df,
        'fatigue_life_seconds': fatigue_life,
        'fatigue_life_years': fatigue_life / (365.25 * 24 * 3600),
        'sigma_stress': sigma,
        'zero_crossing_freq': f0
    }

# Example
freq_hz = np.linspace(0.01, 0.5, 500)
S_stress = 100 * freq_hz**(-2)  # Simplified stress spectrum

fatigue_spectral = spectral_fatigue_narrow_band(
    S_stress,
    freq_hz,
    sn_f3,
    duration=3600,  # 1 hour
    design_factor=10.0
)

# Scale to 25 years
fatigue_spectral['damage_25yr'] = fatigue_spectral['total_damage'] * 8760 * 25

print(f"Spectral Fatigue (25 years):")
print(f"  Damage: {fatigue_spectral['damage_25yr']:.4f}")
print(f"  Utilization: {fatigue_spectral['damage_25yr'] * 10:.1f}%")
```

### 5. Mooring Line Fatigue

**Chain Fatigue at Fairlead:**
```python
def mooring_chain_fatigue_analysis(
    tension_time_series: np.ndarray,
    chain_diameter: float,
    chain_grade: str = 'R4',
    design_life_years: float = 25,
    time_step: float = 0.1
) -> dict:
    """
    Complete mooring chain fatigue analysis.

    Args:
        tension_time_series: Tension time series (kN)
        chain_diameter: Chain diameter (mm)
        chain_grade: Chain grade (R3, R4, R5)
        design_life_years: Design life (years)
        time_step: Time step (seconds)

    Returns:
        Fatigue results
    """
    # Chain properties
    grade_factors = {'R3': 0.0219, 'R4': 0.0246, 'R5': 0.0273}
    MBL = grade_factors[chain_grade] * chain_diameter**2  # tonnes

    # Cross-sectional area (nominal)
    d_mm = chain_diameter
    A = np.pi * (d_mm/2)**2  # mm²

    # Convert tension to stress
    stress_time_series = tension_time_series * 1000 / A  # MPa

    # Rainflow counting
    stress_ranges, cycle_counts = rainflow_counting(stress_time_series)

    # Duration of time series
    duration_hours = len(tension_time_series) * time_step / 3600

    # Scale to design life
    hours_total = 8760 * design_life_years
    scale_factor = hours_total / duration_hours

    cycle_counts_scaled = cycle_counts * scale_factor

    # Select S-N curve (DNV: F3 for chain at connector)
    sn_curve = get_dnv_sn_curve('F3', thickness=chain_diameter)

    # Calculate damage
    fatigue_result = calculate_fatigue_damage_miners_rule(
        stress_ranges,
        cycle_counts_scaled,
        sn_curve,
        design_factor=10.0  # DNV-OS-E301
    )

    return {
        'chain_diameter_mm': chain_diameter,
        'chain_grade': chain_grade,
        'MBL_tonnes': MBL,
        'design_life_years': design_life_years,
        'fatigue_damage': fatigue_result['total_damage'],
        'utilization': fatigue_result['utilization'],
        'passed': fatigue_result['passed'],
        'fatigue_life_years': fatigue_result['fatigue_life'],
        'stress_ranges': stress_ranges,
        'cycle_counts': cycle_counts_scaled
    }

# Example
tension = 2000 + 400 * np.sin(2*np.pi*np.arange(36000)/100)  # 1 hour, varied tension

chain_fatigue = mooring_chain_fatigue_analysis(
    tension,
    chain_diameter=127,  # mm
    chain_grade='R4',
    design_life_years=25,
    time_step=0.1
)

print(f"Mooring Chain Fatigue:")
print(f"  Diameter: {chain_fatigue['chain_diameter_mm']} mm {chain_fatigue['chain_grade']}")
print(f"  MBL: {chain_fatigue['MBL_tonnes']:.1f} tonnes")
print(f"  Damage (25 years): {chain_fatigue['fatigue_damage']:.4f}")
print(f"  Utilization: {chain_fatigue['utilization']*100:.1f}%")
print(f"  Status: {'PASS' if chain_fatigue['passed'] else 'FAIL'}")
```

## Complete Examples

### Example 1: Complete Fatigue Assessment

```python
def complete_fatigue_assessment(
    tension_file: str,
    output_dir: str = 'reports/fatigue'
) -> dict:
    """
    Complete fatigue assessment from tension time series.

    Args:
        tension_file: CSV file with tension time series
        output_dir: Output directory

    Returns:
        Fatigue assessment results
    """
    import pandas as pd
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from pathlib import Path

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Load tension data
    df = pd.read_csv(tension_file)
    tension = df['Tension'].values  # kN
    time = df['Time'].values  # seconds

    # Rainflow counting
    ranges, counts = rainflow_counting(tension)

    # Chain properties
    chain_diameter = 127  # mm
    sn_curve = get_dnv_sn_curve('F3', thickness=chain_diameter)

    # Calculate fatigue
    fatigue = mooring_chain_fatigue_analysis(
        tension,
        chain_diameter=chain_diameter,
        design_life_years=25,
        time_step=time[1] - time[0]
    )

    # Create visualizations
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Tension Time Series',
            'Rainflow Histogram',
            'S-N Curve with Load Points',
            'Damage Breakdown'
        )
    )

    # Plot 1: Time series
    fig.add_trace(
        go.Scatter(x=time, y=tension, name='Tension', line=dict(width=1)),
        row=1, col=1
    )

    # Plot 2: Rainflow histogram
    fig.add_trace(
        go.Bar(x=ranges, y=counts, name='Cycle Counts'),
        row=1, col=2
    )

    # Plot 3: S-N curve
    stress_plot = np.logspace(0, 3, 100)
    N_plot = sn_curve['a1'] / stress_plot**sn_curve['m1']

    fig.add_trace(
        go.Scatter(
            x=N_plot, y=stress_plot,
            mode='lines', name='S-N Curve F3',
            line=dict(color='red')
        ),
        row=2, col=1
    )

    # Add load points
    stress_ranges_chain = fatigue['stress_ranges']
    N_values = [calculate_cycles_to_failure(s, sn_curve) for s in stress_ranges_chain]

    fig.add_trace(
        go.Scatter(
            x=N_values, y=stress_ranges_chain,
            mode='markers', name='Load Points',
            marker=dict(size=8)
        ),
        row=2, col=1
    )

    fig.update_xaxes(type='log', title_text='Cycles N', row=2, col=1)
    fig.update_yaxes(type='log', title_text='Stress Range (MPa)', row=2, col=1)

    # Plot 4: Damage breakdown (top contributors)
    breakdown = fatigue_result['breakdown'][:10]  # Top 10
    damage_pct = [item['damage_percent'] for item in breakdown]
    stress_labels = [f"{item['stress_range']:.1f} MPa" for item in breakdown]

    fig.add_trace(
        go.Bar(x=stress_labels, y=damage_pct, name='Damage %'),
        row=2, col=2
    )

    fig.update_layout(height=800, showlegend=True, title_text='Fatigue Assessment Report')
    fig.write_html(output_path / 'fatigue_assessment.html')

    # Export summary
    summary = pd.DataFrame({
        'Parameter': [
            'Chain Diameter (mm)',
            'Chain Grade',
            'MBL (tonnes)',
            'Design Life (years)',
            'Total Damage',
            'Utilization (%)',
            'Fatigue Life (years)',
            'Status'
        ],
        'Value': [
            fatigue['chain_diameter_mm'],
            fatigue['chain_grade'],
            f"{fatigue['MBL_tonnes']:.1f}",
            fatigue['design_life_years'],
            f"{fatigue['fatigue_damage']:.4f}",
            f"{fatigue['utilization']*100:.1f}",
            f"{fatigue['fatigue_life_years']:.1f}",
            'PASS' if fatigue['passed'] else 'FAIL'
        ]
    })

    summary.to_csv(output_path / 'fatigue_summary.csv', index=False)

    print(f"✓ Fatigue assessment complete")
    print(f"  Output: {output_dir}")
    print(f"  Status: {'PASS' if fatigue['passed'] else 'FAIL'}")

    return fatigue
```

## Resources

- **DNV-RP-C203**: Fatigue Design of Offshore Steel Structures
- **DNV-OS-E301**: Position Mooring (Section 7: Fatigue)
- **API RP 2SK**: Design and Analysis of Stationkeeping Systems for Floating Structures
- **ASTM E1049**: Standard Practices for Cycle Counting in Fatigue Analysis
- **BS 7608**: Code of Practice for Fatigue Design and Assessment of Steel Structures

---

**Use this skill for all fatigue analysis in DigitalModel!**
