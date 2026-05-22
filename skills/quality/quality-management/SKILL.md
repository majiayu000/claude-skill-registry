---
name: quality-management
description: When the user wants to improve product quality, implement quality control systems, reduce defects, or analyze quality data. Also use when the user mentions "SPC," "statistical process control," "Six Sigma," "DMAIC," "control charts," "process capability," "Cp," "Cpk," "quality control," "defect reduction," "inspection," "acceptance sampling," or "quality assurance." For lean improvements, see lean-manufacturing. For process optimization, see process-optimization.
---

# Quality Management

You are an expert in quality management and statistical process control. Your goal is to help organizations improve product quality, reduce defects, implement robust quality systems, and drive continuous quality improvement through data-driven methods.

## Initial Assessment

Before implementing quality improvements, understand:

1. **Quality Issues**
   - What quality problems exist? (defects, returns, complaints)
   - Current defect rates or quality levels?
   - Cost of poor quality (COPQ)?
   - Customer quality requirements?

2. **Process Context**
   - Manufacturing process type?
   - Key quality characteristics to control?
   - Current inspection and testing methods?
   - Process stability and capability?

3. **Quality System Maturity**
   - Existing quality management system? (ISO 9001, etc.)
   - Quality tools and methods in use?
   - Data collection and analysis capabilities?
   - Quality culture and mindset?

4. **Improvement Goals**
   - Target defect levels (ppm, sigma level)?
   - Priority quality characteristics?
   - Timeline and resources?
   - Regulatory or certification requirements?

---

## Quality Management Framework

### Quality Philosophy Evolution

**1. Inspection (Traditional)**
- Inspect quality into product
- Sort good from bad
- Reactive approach
- High cost, limited effectiveness

**2. Quality Control (SPC Era)**
- Monitor and control processes
- Statistical methods
- Prevent defects
- Continuous monitoring

**3. Quality Assurance (System Approach)**
- Build quality into processes
- Prevention focus
- System design and standards
- ISO 9001, quality systems

**4. Total Quality Management (TQM)**
- Organization-wide quality focus
- Customer-centric
- Continuous improvement culture
- Everyone responsible for quality

**5. Six Sigma (Data-Driven)**
- Statistical rigor
- DMAIC/DMADV methodology
- 3.4 defects per million target
- Project-based improvement

### Cost of Quality Framework

**Prevention Costs:**
- Quality planning and design
- Process control systems
- Training
- Preventive maintenance

**Appraisal Costs:**
- Inspection and testing
- Quality audits
- Measurement equipment
- Lab testing

**Internal Failure Costs:**
- Scrap and rework
- Re-inspection
- Downtime from quality issues
- Yield loss

**External Failure Costs:**
- Returns and recalls
- Warranty claims
- Customer complaints
- Lost sales and reputation

**Rule of 10:** Cost increases 10x at each stage (prevention → internal → external)

---

## Statistical Process Control (SPC)

### Control Charts

Control charts monitor process stability over time and detect special cause variation.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

class ControlCharts:
    """
    Statistical Process Control charts
    X-bar & R charts, p-charts, c-charts, etc.
    """

    def __init__(self, data, subgroup_size=5):
        """
        Parameters:
        - data: array of measurements or DataFrame
        - subgroup_size: sample size per subgroup
        """
        self.data = np.array(data)
        self.subgroup_size = subgroup_size
        self.n_subgroups = len(data) // subgroup_size

    def xbar_r_chart(self):
        """
        X-bar and R (Range) control chart for variables data

        Returns control limits and data for plotting
        """

        # Reshape into subgroups
        subgroups = self.data[:self.n_subgroups * self.subgroup_size].reshape(
            self.n_subgroups, self.subgroup_size
        )

        # Calculate subgroup means and ranges
        xbar = subgroups.mean(axis=1)
        R = subgroups.max(axis=1) - subgroups.min(axis=1)

        # Overall mean and average range
        xbar_mean = xbar.mean()
        R_mean = R.mean()

        # Control chart constants (for n=5, A2=0.577, D3=0, D4=2.114)
        # For other sample sizes, use full table
        constants = {
            2: {'A2': 1.880, 'D3': 0, 'D4': 3.267},
            3: {'A2': 1.023, 'D3': 0, 'D4': 2.574},
            4: {'A2': 0.729, 'D3': 0, 'D4': 2.282},
            5: {'A2': 0.577, 'D3': 0, 'D4': 2.114},
            6: {'A2': 0.483, 'D3': 0, 'D4': 2.004},
            7: {'A2': 0.419, 'D3': 0.076, 'D4': 1.924},
            8: {'A2': 0.373, 'D3': 0.136, 'D4': 1.864},
            9: {'A2': 0.337, 'D3': 0.184, 'D4': 1.816},
            10: {'A2': 0.308, 'D3': 0.223, 'D4': 1.777}
        }

        n = self.subgroup_size
        A2 = constants.get(n, constants[5])['A2']
        D3 = constants.get(n, constants[5])['D3']
        D4 = constants.get(n, constants[5])['D4']

        # X-bar chart limits
        xbar_ucl = xbar_mean + A2 * R_mean
        xbar_lcl = xbar_mean - A2 * R_mean

        # R chart limits
        r_ucl = D4 * R_mean
        r_lcl = D3 * R_mean

        # Detect out-of-control points
        xbar_ooc = (xbar > xbar_ucl) | (xbar < xbar_lcl)
        r_ooc = (R > r_ucl) | (R < r_lcl)

        return {
            'xbar': xbar,
            'xbar_mean': xbar_mean,
            'xbar_ucl': xbar_ucl,
            'xbar_lcl': xbar_lcl,
            'xbar_out_of_control': xbar_ooc,
            'R': R,
            'R_mean': R_mean,
            'R_ucl': r_ucl,
            'R_lcl': r_lcl,
            'R_out_of_control': r_ooc,
            'in_control': not (xbar_ooc.any() or r_ooc.any())
        }

    def p_chart(self, defects, sample_sizes):
        """
        p-chart for proportion defective (attribute data)

        Parameters:
        - defects: array of number of defectives per sample
        - sample_sizes: array of sample sizes (can be variable)
        """

        defects = np.array(defects)
        sample_sizes = np.array(sample_sizes)

        # Proportion defective per sample
        p = defects / sample_sizes

        # Average proportion defective
        p_bar = defects.sum() / sample_sizes.sum()

        # Control limits (3-sigma)
        # For variable sample size, calculate limits for each point
        if len(set(sample_sizes)) == 1:
            # Constant sample size
            n = sample_sizes[0]
            ucl = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / n)
            lcl = max(0, p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / n))

            ucl = np.full_like(p, ucl)
            lcl = np.full_like(p, lcl)
        else:
            # Variable sample size
            ucl = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / sample_sizes)
            lcl = np.maximum(0, p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / sample_sizes))

        # Out of control points
        ooc = (p > ucl) | (p < lcl)

        return {
            'p': p,
            'p_bar': p_bar,
            'ucl': ucl,
            'lcl': lcl,
            'out_of_control': ooc,
            'in_control': not ooc.any()
        }

    def c_chart(self, defects_per_unit):
        """
        c-chart for count of defects per unit

        Parameters:
        - defects_per_unit: array of defect counts per unit
        """

        c = np.array(defects_per_unit)

        # Average defects per unit
        c_bar = c.mean()

        # Control limits (based on Poisson distribution)
        ucl = c_bar + 3 * np.sqrt(c_bar)
        lcl = max(0, c_bar - 3 * np.sqrt(c_bar))

        # Out of control
        ooc = (c > ucl) | (c < lcl)

        return {
            'c': c,
            'c_bar': c_bar,
            'ucl': ucl,
            'lcl': lcl,
            'out_of_control': ooc,
            'in_control': not ooc.any()
        }

    def plot_xbar_r_chart(self, results):
        """Plot X-bar and R control charts"""

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        # X-bar chart
        x = range(1, len(results['xbar']) + 1)

        ax1.plot(x, results['xbar'], 'bo-', label='Subgroup Mean')
        ax1.axhline(results['xbar_mean'], color='green', linestyle='-', linewidth=2, label='Center Line')
        ax1.axhline(results['xbar_ucl'], color='red', linestyle='--', linewidth=2, label='UCL')
        ax1.axhline(results['xbar_lcl'], color='red', linestyle='--', linewidth=2, label='LCL')

        # Mark out-of-control points
        ooc_indices = np.where(results['xbar_out_of_control'])[0]
        if len(ooc_indices) > 0:
            ax1.plot(ooc_indices + 1, results['xbar'][ooc_indices], 'rx', markersize=12, markeredgewidth=3)

        ax1.set_xlabel('Subgroup Number')
        ax1.set_ylabel('Subgroup Mean')
        ax1.set_title('X-bar Control Chart')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # R chart
        ax2.plot(x, results['R'], 'bo-', label='Subgroup Range')
        ax2.axhline(results['R_mean'], color='green', linestyle='-', linewidth=2, label='Center Line')
        ax2.axhline(results['R_ucl'], color='red', linestyle='--', linewidth=2, label='UCL')
        ax2.axhline(results['R_lcl'], color='red', linestyle='--', linewidth=2, label='LCL')

        # Mark out-of-control points
        ooc_indices = np.where(results['R_out_of_control'])[0]
        if len(ooc_indices) > 0:
            ax2.plot(ooc_indices + 1, results['R'][ooc_indices], 'rx', markersize=12, markeredgewidth=3)

        ax2.set_xlabel('Subgroup Number')
        ax2.set_ylabel('Subgroup Range')
        ax2.set_title('R Control Chart')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

# Example usage - Variable data (measurements)
np.random.seed(42)
# Simulate process data (mean=100, std=2)
data = np.random.normal(100, 2, 100)

spc = ControlCharts(data, subgroup_size=5)
results = spc.xbar_r_chart()

print("X-bar Chart:")
print(f"  Center Line (X-bar-bar): {results['xbar_mean']:.2f}")
print(f"  UCL: {results['xbar_ucl']:.2f}")
print(f"  LCL: {results['xbar_lcl']:.2f}")
print(f"  Process in control: {results['in_control']}")

print("\nR Chart:")
print(f"  Center Line (R-bar): {results['R_mean']:.2f}")
print(f"  UCL: {results['R_ucl']:.2f}")
print(f"  LCL: {results['R_lcl']:.2f}")

# Plot
fig = spc.plot_xbar_r_chart(results)
plt.show()

# Example - Attribute data (p-chart)
defects = np.array([5, 8, 3, 6, 12, 4, 7, 5, 9, 6])
sample_sizes = np.array([100] * 10)

p_chart_results = spc.p_chart(defects, sample_sizes)
print(f"\np-chart:")
print(f"  Average proportion defective: {p_chart_results['p_bar']:.4f} ({p_chart_results['p_bar']*100:.2f}%)")
print(f"  UCL: {p_chart_results['ucl'][0]:.4f}")
print(f"  LCL: {p_chart_results['lcl'][0]:.4f}")
print(f"  Process in control: {p_chart_results['in_control']}")
```

### Process Capability Analysis

```python
class ProcessCapability:
    """
    Process capability analysis (Cp, Cpk, Pp, Ppk)
    Measures how well process meets specifications
    """

    def __init__(self, data, lsl, usl, target=None):
        """
        Parameters:
        - data: array of process measurements
        - lsl: lower specification limit
        - usl: upper specification limit
        - target: target value (optional, default is midpoint)
        """
        self.data = np.array(data)
        self.lsl = lsl
        self.usl = usl
        self.target = target if target is not None else (lsl + usl) / 2

    def calculate_capability(self):
        """Calculate process capability indices"""

        # Process statistics
        mean = self.data.mean()
        std = self.data.std(ddof=1)  # Sample standard deviation

        # Within-subgroup variation (short-term capability)
        # For simplicity, using overall std; ideally use R-bar/d2 method
        sigma_within = std

        # Specification width
        spec_width = self.usl - self.lsl

        # Cp: Potential capability (assumes process centered)
        # Cp = (USL - LSL) / (6 * sigma)
        cp = spec_width / (6 * sigma_within)

        # Cpk: Actual capability (accounts for centering)
        # Cpk = min[(USL - mean)/(3*sigma), (mean - LSL)/(3*sigma)]
        cpu = (self.usl - mean) / (3 * sigma_within)
        cpl = (mean - self.lsl) / (3 * sigma_within)
        cpk = min(cpu, cpl)

        # Pp and Ppk (overall/long-term capability, using total variation)
        sigma_total = std  # Overall standard deviation
        pp = spec_width / (6 * sigma_total)
        ppu = (self.usl - mean) / (3 * sigma_total)
        ppl = (mean - self.lsl) / (3 * sigma_total)
        ppk = min(ppu, ppl)

        # Estimated defect rates (ppm)
        # Using normal distribution
        z_usl = (self.usl - mean) / std
        z_lsl = (self.lsl - mean) / std

        defects_above_usl = (1 - stats.norm.cdf(z_usl)) * 1e6
        defects_below_lsl = stats.norm.cdf(z_lsl) * 1e6
        total_defects_ppm = defects_above_usl + defects_below_lsl

        # Sigma level (for Six Sigma)
        # Z_min = min(|z_usl|, |z_lsl|)
        z_min = min(abs(z_usl), abs(z_lsl))
        sigma_level = z_min

        return {
            'mean': mean,
            'std_dev': std,
            'lsl': self.lsl,
            'usl': self.usl,
            'target': self.target,
            'cp': cp,
            'cpk': cpk,
            'pp': pp,
            'ppk': ppk,
            'defects_ppm': total_defects_ppm,
            'sigma_level': sigma_level,
            'interpretation': self._interpret_cpk(cpk)
        }

    def _interpret_cpk(self, cpk):
        """Interpret Cpk value"""
        if cpk >= 2.0:
            return 'Excellent (Six Sigma class)'
        elif cpk >= 1.67:
            return 'Very Good (5 Sigma class)'
        elif cpk >= 1.33:
            return 'Adequate (4 Sigma class)'
        elif cpk >= 1.0:
            return 'Marginal (3 Sigma class)'
        else:
            return 'Poor (process not capable)'

    def plot_capability(self, capability_results):
        """Plot process capability histogram with spec limits"""

        fig, ax = plt.subplots(figsize=(10, 6))

        # Histogram
        ax.hist(self.data, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black')

        # Fitted normal curve
        mean = capability_results['mean']
        std = capability_results['std_dev']
        x = np.linspace(self.data.min(), self.data.max(), 100)
        ax.plot(x, stats.norm.pdf(x, mean, std), 'b-', linewidth=2, label='Normal Fit')

        # Specification limits
        ax.axvline(self.lsl, color='red', linestyle='--', linewidth=2, label=f'LSL = {self.lsl}')
        ax.axvline(self.usl, color='red', linestyle='--', linewidth=2, label=f'USL = {self.usl}')
        ax.axvline(self.target, color='green', linestyle=':', linewidth=2, label=f'Target = {self.target}')
        ax.axvline(mean, color='blue', linestyle='-', linewidth=2, label=f'Mean = {mean:.2f}')

        # Annotations
        textstr = f'Cp = {capability_results["cp"]:.2f}\n'
        textstr += f'Cpk = {capability_results["cpk"]:.2f}\n'
        textstr += f'Defects = {capability_results["defects_ppm"]:.0f} ppm\n'
        textstr += f'Sigma Level = {capability_results["sigma_level"]:.2f}'

        ax.text(0.02, 0.98, textstr, transform=ax.transAxes,
                fontsize=11, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        ax.set_xlabel('Measurement')
        ax.set_ylabel('Density')
        ax.set_title('Process Capability Analysis')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

# Example usage
np.random.seed(42)
# Simulate process data
data = np.random.normal(50, 2, 200)

# Specification limits
lsl = 42
usl = 58
target = 50

pc = ProcessCapability(data, lsl, usl, target)
capability = pc.calculate_capability()

print("Process Capability Analysis:")
print(f"  Process Mean: {capability['mean']:.2f}")
print(f"  Process Std Dev: {capability['std_dev']:.2f}")
print(f"  Cp: {capability['cp']:.2f}")
print(f"  Cpk: {capability['cpk']:.2f}")
print(f"  Interpretation: {capability['interpretation']}")
print(f"  Estimated Defects: {capability['defects_ppm']:.0f} ppm")
print(f"  Sigma Level: {capability['sigma_level']:.2f} sigma")

# Plot
fig = pc.plot_capability(capability)
plt.show()
```

---

## Six Sigma Methodology

### DMAIC Framework

**Define:**
- Project charter and scope
- Voice of Customer (VOC)
- Critical-to-Quality (CTQ) characteristics
- Project goals and metrics

**Measure:**
- Baseline performance measurement
- Data collection plan
- Measurement System Analysis (MSA)
- Process capability baseline

**Analyze:**
- Root cause analysis
- Statistical analysis
- Hypothesis testing
- Identify key input variables (X's)

**Improve:**
- Generate solutions
- Pilot improvements
- Design of Experiments (DOE)
- Implement changes

**Control:**
- Control plan
- SPC charts
- Standard operating procedures
- Sustainability plan

### DMAIC Implementation

```python
class SixSigmaProject:
    """
    Six Sigma DMAIC project tracking and analysis
    """

    def __init__(self, project_name, ctq_characteristic, baseline_data):
        """
        Parameters:
        - project_name: project identifier
        - ctq_characteristic: critical-to-quality metric
        - baseline_data: baseline measurements
        """
        self.project_name = project_name
        self.ctq = ctq_characteristic
        self.baseline_data = np.array(baseline_data)
        self.improved_data = None

    def define_phase(self, problem_statement, goal, scope):
        """Define phase outputs"""
        self.problem = problem_statement
        self.goal = goal
        self.scope = scope

        return {
            'project': self.project_name,
            'problem': problem_statement,
            'goal': goal,
            'scope': scope,
            'ctq': self.ctq
        }

    def measure_phase(self):
        """Measure baseline performance"""

        baseline_mean = self.baseline_data.mean()
        baseline_std = self.baseline_data.std(ddof=1)
        baseline_median = np.median(self.baseline_data)

        # Calculate defects (assuming spec limits provided)
        # For this example, assume values > target+3*std are defects
        target = baseline_mean
        defects = np.sum(self.baseline_data > target + 3*baseline_std)
        defect_rate = defects / len(self.baseline_data)
        dpmo = defect_rate * 1e6  # Defects per million opportunities

        return {
            'baseline_mean': baseline_mean,
            'baseline_std': baseline_std,
            'baseline_median': baseline_median,
            'sample_size': len(self.baseline_data),
            'defect_rate': defect_rate,
            'dpmo': dpmo
        }

    def analyze_phase(self, potential_causes):
        """
        Analyze phase - identify root causes

        potential_causes: list of potential X variables with data
        Example: [{'name': 'Temperature', 'data': [...]}, ...]
        """

        # Correlation analysis with CTQ (Y variable)
        correlations = []

        for cause in potential_causes:
            # Calculate correlation
            corr, p_value = stats.pearsonr(cause['data'], self.baseline_data[:len(cause['data'])])

            correlations.append({
                'cause': cause['name'],
                'correlation': corr,
                'p_value': p_value,
                'significant': p_value < 0.05
            })

        # Sort by absolute correlation
        correlations = sorted(correlations, key=lambda x: abs(x['correlation']), reverse=True)

        return pd.DataFrame(correlations)

    def improve_phase(self, improved_data):
        """
        Improve phase - measure improvements

        improved_data: measurements after improvement
        """
        self.improved_data = np.array(improved_data)

        # Calculate improvement
        baseline_mean = self.baseline_data.mean()
        improved_mean = self.improved_data.mean()

        baseline_std = self.baseline_data.std(ddof=1)
        improved_std = self.improved_data.std(ddof=1)

        # Improvement metrics
        mean_improvement = ((baseline_mean - improved_mean) / baseline_mean) * 100
        std_reduction = ((baseline_std - improved_std) / baseline_std) * 100

        # Statistical test (t-test to verify improvement is significant)
        t_stat, p_value = stats.ttest_ind(self.baseline_data, self.improved_data)

        return {
            'baseline_mean': baseline_mean,
            'improved_mean': improved_mean,
            'mean_improvement_pct': mean_improvement,
            'baseline_std': baseline_std,
            'improved_std': improved_std,
            'std_reduction_pct': std_reduction,
            't_statistic': t_stat,
            'p_value': p_value,
            'improvement_significant': p_value < 0.05
        }

    def control_phase(self, control_plan):
        """
        Control phase - sustain improvements

        control_plan: dict with control methods
        """
        return {
            'control_plan': control_plan,
            'spc_charts': 'X-bar and R charts implemented',
            'reaction_plan': 'Out-of-control procedures documented',
            'training': 'Operators trained on new process'
        }

    def project_summary(self):
        """Generate project summary report"""

        if self.improved_data is None:
            return "Improvement data not yet available"

        measure_results = self.measure_phase()
        improve_results = self.improve_phase(self.improved_data)

        summary = f"""
Six Sigma Project Summary: {self.project_name}

Define:
  Problem: {self.problem}
  Goal: {self.goal}
  CTQ: {self.ctq}

Measure (Baseline):
  Mean: {measure_results['baseline_mean']:.2f}
  Std Dev: {measure_results['baseline_std']:.2f}
  DPMO: {measure_results['dpmo']:.0f}

Improve (Results):
  Improved Mean: {improve_results['improved_mean']:.2f}
  Mean Improvement: {improve_results['mean_improvement_pct']:.1f}%
  Std Dev Reduction: {improve_results['std_reduction_pct']:.1f}%
  Statistical Significance: {'Yes' if improve_results['improvement_significant'] else 'No'} (p={improve_results['p_value']:.4f})

Control:
  SPC monitoring in place
  Control plan documented
  Training completed
        """

        return summary

# Example usage
np.random.seed(42)
baseline = np.random.normal(100, 15, 100)  # High variation
improved = np.random.normal(95, 8, 100)    # Lower mean, lower variation

project = SixSigmaProject(
    project_name="Reduce Cycle Time Variation",
    ctq_characteristic="Cycle Time (seconds)",
    baseline_data=baseline
)

# Define
define_output = project.define_phase(
    problem_statement="High cycle time variation causing quality issues",
    goal="Reduce cycle time variation by 50% and lower mean by 5%",
    scope="Assembly line station #3"
)

# Measure
measure_output = project.measure_phase()
print("Measure Phase:")
print(f"  Baseline Mean: {measure_output['baseline_mean']:.2f}")
print(f"  Baseline Std: {measure_output['baseline_std']:.2f}")
print(f"  DPMO: {measure_output['dpmo']:.0f}")

# Analyze (example with mock data)
causes = [
    {'name': 'Temperature', 'data': np.random.normal(70, 5, 100)},
    {'name': 'Operator Experience', 'data': np.random.normal(5, 2, 100)},
    {'name': 'Material Hardness', 'data': np.random.normal(50, 3, 100)}
]

analyze_output = project.analyze_phase(causes)
print("\nAnalyze Phase - Correlations:")
print(analyze_output)

# Improve
improve_output = project.improve_phase(improved)
print("\nImprove Phase:")
print(f"  Mean Improvement: {improve_output['mean_improvement_pct']:.1f}%")
print(f"  Std Reduction: {improve_output['std_reduction_pct']:.1f}%")
print(f"  Significant: {improve_output['improvement_significant']}")

# Project summary
print("\n" + project.project_summary())
```

### Design of Experiments (DOE)

```python
from itertools import product

class DesignOfExperiments:
    """
    Factorial Design of Experiments
    Test multiple factors simultaneously
    """

    def __init__(self, factors):
        """
        factors: dict {factor_name: [low_level, high_level]}

        Example:
        {
            'Temperature': [150, 200],
            'Pressure': [30, 50],
            'Time': [10, 15]
        }
        """
        self.factors = factors
        self.factor_names = list(factors.keys())
        self.n_factors = len(factors)

    def full_factorial_design(self):
        """
        Create full factorial design (2^k experiments)
        All combinations of factor levels
        """

        # Create all combinations
        levels = [self.factors[f] for f in self.factor_names]
        combinations = list(product(*levels))

        # Create design matrix
        design = pd.DataFrame(combinations, columns=self.factor_names)

        # Add run order (randomize)
        design['run_order'] = np.random.permutation(len(design))
        design = design.sort_values('run_order').reset_index(drop=True)

        return design

    def analyze_results(self, design, responses):
        """
        Analyze DOE results - calculate main effects and interactions

        Parameters:
        - design: design matrix from full_factorial_design()
        - responses: array of measured responses for each run
        """

        design = design.copy()
        design['response'] = responses

        # Calculate main effects
        main_effects = {}

        for factor in self.factor_names:
            low_level = self.factors[factor][0]
            high_level = self.factors[factor][1]

            low_avg = design[design[factor] == low_level]['response'].mean()
            high_avg = design[design[factor] == high_level]['response'].mean()

            effect = high_avg - low_avg

            main_effects[factor] = {
                'low_avg': low_avg,
                'high_avg': high_avg,
                'effect': effect
            }

        # Calculate two-way interactions
        interactions = {}

        for i, factor1 in enumerate(self.factor_names):
            for factor2 in self.factor_names[i+1:]:
                # Four combinations
                ll = design[
                    (design[factor1] == self.factors[factor1][0]) &
                    (design[factor2] == self.factors[factor2][0])
                ]['response'].mean()

                lh = design[
                    (design[factor1] == self.factors[factor1][0]) &
                    (design[factor2] == self.factors[factor2][1])
                ]['response'].mean()

                hl = design[
                    (design[factor1] == self.factors[factor1][1]) &
                    (design[factor2] == self.factors[factor2][0])
                ]['response'].mean()

                hh = design[
                    (design[factor1] == self.factors[factor1][1]) &
                    (design[factor2] == self.factors[factor2][1])
                ]['response'].mean()

                # Interaction effect
                interaction_effect = ((hh - hl) - (lh - ll)) / 2

                interactions[f'{factor1}*{factor2}'] = {
                    'effect': interaction_effect
                }

        return {
            'main_effects': main_effects,
            'interactions': interactions,
            'design_with_results': design
        }

    def plot_main_effects(self, analysis_results):
        """Plot main effects"""

        main_effects = analysis_results['main_effects']

        n = len(main_effects)
        fig, axes = plt.subplots(1, n, figsize=(5*n, 4))

        if n == 1:
            axes = [axes]

        for i, (factor, effects) in enumerate(main_effects.items()):
            ax = axes[i]

            levels = self.factors[factor]
            avgs = [effects['low_avg'], effects['high_avg']]

            ax.plot(levels, avgs, 'bo-', linewidth=2, markersize=10)
            ax.set_xlabel(factor, fontsize=12, fontweight='bold')
            ax.set_ylabel('Average Response', fontsize=12)
            ax.set_title(f'{factor} Main Effect\n(Effect = {effects["effect"]:.2f})', fontsize=12)
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

# Example usage
factors = {
    'Temperature': [150, 200],
    'Pressure': [30, 50],
    'Time': [10, 15]
}

doe = DesignOfExperiments(factors)

# Create design
design = doe.full_factorial_design()
print("Factorial Design:")
print(design)

# Simulate responses (in reality, these would be measured)
# Assume Temperature has large positive effect, Pressure small negative, Time minimal
np.random.seed(42)
responses = []
for _, row in design.iterrows():
    # Simulate response based on factor levels
    response = 50  # baseline
    response += 0.2 * (row['Temperature'] - 175)  # Temperature effect
    response -= 0.1 * (row['Pressure'] - 40)      # Pressure effect
    response += 0.05 * (row['Time'] - 12.5)       # Time effect
    response += np.random.normal(0, 2)            # Random error

    responses.append(response)

# Analyze
analysis = doe.analyze_results(design, responses)

print("\nMain Effects:")
for factor, effects in analysis['main_effects'].items():
    print(f"  {factor}: {effects['effect']:.2f}")

print("\nInteractions:")
for interaction, effects in analysis['interactions'].items():
    print(f"  {interaction}: {effects['effect']:.2f}")

# Plot
fig = doe.plot_main_effects(analysis)
plt.show()
```

---

## Quality Tools (Seven QC Tools)

### Pareto Analysis

```python
class ParetoAnalysis:
    """
    Pareto chart - identify vital few from trivial many
    80/20 rule
    """

    def __init__(self, categories, frequencies):
        """
        Parameters:
        - categories: list of defect/problem categories
        - frequencies: list of occurrence counts
        """
        self.df = pd.DataFrame({
            'category': categories,
            'frequency': frequencies
        })

        # Sort by frequency descending
        self.df = self.df.sort_values('frequency', ascending=False).reset_index(drop=True)

        # Calculate cumulative percentage
        total = self.df['frequency'].sum()
        self.df['percentage'] = (self.df['frequency'] / total) * 100
        self.df['cumulative_pct'] = self.df['percentage'].cumsum()

    def plot_pareto(self):
        """Create Pareto chart"""

        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Bar chart
        x = range(len(self.df))
        ax1.bar(x, self.df['frequency'], color='skyblue', edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Category', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(self.df['category'], rotation=45, ha='right')

        # Cumulative line
        ax2 = ax1.twinx()
        ax2.plot(x, self.df['cumulative_pct'], 'ro-', linewidth=2, markersize=8)
        ax2.set_ylabel('Cumulative %', fontsize=12, fontweight='bold')
        ax2.set_ylim([0, 105])
        ax2.axhline(80, color='green', linestyle='--', linewidth=2, label='80%')
        ax2.legend(loc='center right')

        # Title
        plt.title('Pareto Chart - Defect Analysis', fontsize=14, fontweight='bold')

        plt.tight_layout()
        return fig

    def identify_vital_few(self, threshold=80):
        """Identify categories contributing to threshold % of problems"""

        vital_few = self.df[self.df['cumulative_pct'] <= threshold]

        return {
            'vital_few_categories': vital_few['category'].tolist(),
            'vital_few_count': len(vital_few),
            'total_categories': len(self.df),
            'vital_few_contribution_pct': vital_few['percentage'].sum()
        }

# Example usage
categories = ['Scratches', 'Dents', 'Color Mismatch', 'Dimension Out of Spec',
              'Missing Parts', 'Contamination', 'Assembly Error', 'Other']
frequencies = [145, 98, 67, 52, 28, 21, 15, 8]

pareto = ParetoAnalysis(categories, frequencies)

print("Pareto Analysis:")
print(pareto.df)

vital = pareto.identify_vital_few(threshold=80)
print(f"\nVital Few: {vital['vital_few_categories']}")
print(f"  {vital['vital_few_count']} out of {vital['total_categories']} categories")
print(f"  Contributing to {vital['vital_few_contribution_pct']:.1f}% of problems")

fig = pareto.plot_pareto()
plt.show()
```

### Fishbone (Ishikawa) Diagram

```python
class FishboneDiagram:
    """
    Fishbone (Ishikawa) diagram for root cause analysis
    6M categories: Man, Machine, Material, Method, Measurement, Mother Nature (Environment)
    """

    def __init__(self, problem_statement):
        self.problem = problem_statement
        self.causes = {
            'Man': [],
            'Machine': [],
            'Material': [],
            'Method': [],
            'Measurement': [],
            'Environment': []
        }

    def add_cause(self, category, cause):
        """Add potential cause to category"""
        if category in self.causes:
            self.causes[category].append(cause)
        else:
            raise ValueError(f"Category must be one of: {list(self.causes.keys())}")

    def display(self):
        """Display fishbone diagram in text format"""

        print(f"\nFishbone Diagram: {self.problem}")
        print("=" * 60)

        for category, causes in self.causes.items():
            print(f"\n{category}:")
            for cause in causes:
                print(f"  - {cause}")

    def prioritize_causes(self, voting_scores):
        """
        Prioritize causes using team voting

        voting_scores: dict {cause: score}
        """

        all_causes = []
        for category, causes in self.causes.items():
            for cause in causes:
                score = voting_scores.get(cause, 0)
                all_causes.append({
                    'category': category,
                    'cause': cause,
                    'score': score
                })

        df = pd.DataFrame(all_causes)
        df = df.sort_values('score', ascending=False)

        return df

# Example usage
fishbone = FishboneDiagram("High Defect Rate in Assembly")

# Add causes
fishbone.add_cause('Man', 'Inadequate training')
fishbone.add_cause('Man', 'Operator fatigue')
fishbone.add_cause('Machine', 'Equipment calibration drift')
fishbone.add_cause('Machine', 'Worn tooling')
fishbone.add_cause('Material', 'Supplier quality variation')
fishbone.add_cause('Material', 'Incoming inspection gaps')
fishbone.add_cause('Method', 'Unclear work instructions')
fishbone.add_cause('Method', 'Inconsistent process sequence')
fishbone.add_cause('Measurement', 'Gage repeatability issues')
fishbone.add_cause('Environment', 'Temperature fluctuations')

fishbone.display()

# Prioritize (team voting scores)
scores = {
    'Worn tooling': 9,
    'Supplier quality variation': 8,
    'Inadequate training': 7,
    'Equipment calibration drift': 6,
    'Unclear work instructions': 5,
    'Operator fatigue': 4,
    'Inconsistent process sequence': 4,
    'Gage repeatability issues': 3,
    'Incoming inspection gaps': 3,
    'Temperature fluctuations': 2
}

prioritized = fishbone.prioritize_causes(scores)
print("\n\nPrioritized Causes:")
print(prioritized)
```

---

## Acceptance Sampling

```python
class AcceptanceSampling:
    """
    Acceptance sampling plans
    Single and double sampling
    """

    def __init__(self, lot_size, aql=1.0, ltpd=5.0):
        """
        Parameters:
        - lot_size: size of production lot
        - aql: Acceptable Quality Level (% defects)
        - ltpd: Lot Tolerance Percent Defective
        """
        self.lot_size = lot_size
        self.aql = aql / 100  # Convert to proportion
        self.ltpd = ltpd / 100

    def single_sampling_plan(self, sample_size, acceptance_number):
        """
        Single sampling plan: n, c
        - n: sample size
        - c: acceptance number (max defects to accept lot)

        Returns OC curve data
        """

        # Operating Characteristic (OC) curve
        # Probability of acceptance for different defect levels
        p_defects = np.linspace(0, 0.15, 50)  # Defect rates from 0% to 15%
        p_accept = []

        for p in p_defects:
            # Binomial probability: P(d <= c | n, p)
            prob = sum([stats.binom.pmf(d, sample_size, p)
                       for d in range(acceptance_number + 1)])
            p_accept.append(prob)

        return {
            'sample_size': sample_size,
            'acceptance_number': acceptance_number,
            'p_defects': p_defects,
            'p_accept': p_accept
        }

    def plot_oc_curve(self, sampling_plan):
        """Plot Operating Characteristic curve"""

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(sampling_plan['p_defects'] * 100,
               np.array(sampling_plan['p_accept']) * 100,
               'b-', linewidth=2)

        # Mark AQL and LTPD
        ax.axvline(self.aql * 100, color='green', linestyle='--', label=f'AQL = {self.aql*100:.1f}%')
        ax.axvline(self.ltpd * 100, color='red', linestyle='--', label=f'LTPD = {self.ltpd*100:.1f}%')

        ax.set_xlabel('Lot Defect Rate (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Probability of Acceptance (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'OC Curve - Sampling Plan (n={sampling_plan["sample_size"]}, c={sampling_plan["acceptance_number"]})',
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

        plt.tight_layout()
        return fig

    def evaluate_plan(self, sample, acceptance_number):
        """
        Evaluate sample and make accept/reject decision

        Parameters:
        - sample: array of inspected units (1=defect, 0=good)
        - acceptance_number: max defects to accept

        Returns decision and defect count
        """

        defects = np.sum(sample)
        decision = 'ACCEPT' if defects <= acceptance_number else 'REJECT'

        return {
            'sample_size': len(sample),
            'defects_found': defects,
            'acceptance_number': acceptance_number,
            'decision': decision,
            'defect_rate_pct': (defects / len(sample)) * 100
        }

# Example usage
acceptance = AcceptanceSampling(lot_size=1000, aql=1.0, ltpd=5.0)

# Define sampling plan
plan = acceptance.single_sampling_plan(sample_size=80, acceptance_number=2)

print("Sampling Plan:")
print(f"  Sample Size: {plan['sample_size']}")
print(f"  Acceptance Number: {plan['acceptance_number']}")

# Plot OC curve
fig = acceptance.plot_oc_curve(plan)
plt.show()

# Evaluate a sample (simulate inspection)
np.random.seed(42)
sample = np.random.binomial(1, 0.02, 80)  # 2% defect rate in sample

result = acceptance.evaluate_plan(sample, acceptance_number=2)
print(f"\nInspection Result:")
print(f"  Defects Found: {result['defects_found']}")
print(f"  Defect Rate: {result['defect_rate_pct']:.2f}%")
print(f"  Decision: {result['decision']}")
```

---

## Tools & Libraries

### Python Libraries

**Statistical Analysis:**
- `scipy.stats`: Statistical tests and distributions
- `statsmodels`: Advanced statistical modeling
- `numpy`, `pandas`: Data manipulation
- `matplotlib`, `seaborn`, `plotly`: Visualization

**Quality-Specific:**
- `pyqt-fit`: Quality tools and SPC
- `quality`: Quality control functions (if available)

**Six Sigma & DOE:**
- `pyDOE2`: Design of experiments
- `scikit-learn`: Machine learning for quality prediction

### Commercial Quality Software

**Statistical Quality Control:**
- **Minitab**: Industry-standard statistical software
- **JMP**: SAS statistical discovery software
- **Statgraphics**: Statistical analysis and DOE
- **SigmaXL**: Excel-based Six Sigma tools

**Quality Management Systems:**
- **SAP QM**: Quality management module
- **Oracle Quality**: Quality management cloud
- **Intelex**: EQMS (Enterprise Quality Management System)
- **MasterControl**: Quality and compliance management
- **ETQ Reliance**: Quality management software

**SPC Software:**
- **InfinityQS**: Real-time SPC
- **QEQA 3DM**: SPC and quality analysis
- **SPC for Excel**: Excel-based SPC tools
- **WinSPC**: Statistical process control software

---

## Common Challenges & Solutions

### Challenge: Lack of Data

**Problem:**
- Insufficient historical data
- Poor data collection systems
- Missing or incomplete records

**Solutions:**
- Start collecting data immediately (even manual)
- Implement automated data capture (sensors, MES)
- Use check sheets and simple recording methods
- Pilot data collection in one area first
- Use existing data creatively (maintenance logs, customer complaints)

### Challenge: Special vs. Common Cause Confusion

**Problem:**
- Overreacting to common cause variation
- Ignoring special causes
- Tampering with stable processes

**Solutions:**
- Implement control charts to distinguish
- Train team on variation types
- Establish reaction plans for out-of-control signals
- Use statistical tests (rules for out-of-control)
- Avoid knee-jerk reactions to single data points

### Challenge: Low Process Capability

**Problem:**
- Cpk < 1.0
- High defect rates
- Process can't meet specifications

**Solutions:**
- Reduce variation (improve phase of DMAIC)
- Center the process on target
- Review specifications (are they realistic?)
- Improve measurement system
- Consider process redesign or new equipment
- Implement 100% inspection temporarily

### Challenge: Measurement System Issues

**Problem:**
- Gage R&R indicates poor measurement system
- Operator-to-operator variation
- Equipment calibration problems

**Solutions:**
- Conduct Measurement System Analysis (MSA)
- Calibrate equipment regularly
- Standardize measurement procedures
- Train operators on measurement technique
- Automate measurements where possible
- Use Gage R&R studies to quantify and improve

### Challenge: Resistance to Quality Methods

**Problem:**
- "We don't have time for statistics"
- Seen as academic or theoretical
- Quality viewed as QC department's job only

**Solutions:**
- Show quick wins and tangible benefits
- Use simple tools first (Pareto, fishbone)
- Involve operators in data collection
- Celebrate quality improvements
- Leadership reinforcement
- Tie quality to business metrics (cost, customer satisfaction)

---

## Output Format

### Quality Analysis Report

**Executive Summary:**
- Current quality level and defect rates
- Key quality issues identified
- Root causes determined
- Improvement recommendations and expected impact

**Process Capability Analysis:**

| Characteristic | LSL | USL | Mean | Std Dev | Cp | Cpk | DPMO | Assessment |
|----------------|-----|-----|------|---------|----|----|------|------------|
| Dimension A | 10.0 | 12.0 | 11.1 | 0.15 | 2.22 | 1.98 | 45 | Excellent |
| Weight | 48.0 | 52.0 | 50.5 | 1.2 | 0.56 | 0.42 | 145,000 | Poor |
| Surface Finish | 2.0 | 5.0 | 3.2 | 0.8 | 1.25 | 0.83 | 42,500 | Marginal |

**Control Chart Status:**
- **Process A**: In control, stable performance
- **Process B**: Out of control - special cause detected on 2/15
- **Process C**: In control but poor capability (Cpk=0.85)

**Pareto Analysis - Top Defects:**
1. Surface scratches (35% of defects)
2. Dimension out of spec (28%)
3. Color mismatch (18%)
4. Other (19%)

**Root Cause Analysis:**
- Primary: Worn tooling causing dimension issues
- Secondary: Operator training gaps for surface handling
- Tertiary: Incoming material variation

**Recommendations:**

**Priority 1 (Immediate):**
- Replace worn tooling on Line 2
- Implement 100% inspection for Weight characteristic
- Launch Six Sigma project on Weight process

**Priority 2 (30 days):**
- Operator training on surface handling techniques
- Implement X-bar/R charts on all critical dimensions
- Supplier quality improvement program

**Priority 3 (90 days):**
- DOE to optimize Process B parameters
- Automated measurement system for Weight
- Preventive maintenance schedule for tooling

**Expected Benefits:**
- Defect reduction: 60-70%
- Cost of quality reduction: $500K annually
- Customer complaints reduction: 50%
- Scrap/rework savings: $200K annually

---

## Questions to Ask

If you need more context:
1. What quality problems or defects are occurring?
2. What are the current defect rates or quality metrics?
3. Are there specifications or quality standards to meet?
4. What is the manufacturing process and key quality characteristics?
5. What quality data is available?
6. Are there customer complaints or field failures?
7. What is the cost of poor quality?
8. Is there a quality management system in place?

---

## Related Skills

- **lean-manufacturing**: For waste elimination and continuous improvement
- **process-optimization**: For process improvement and efficiency
- **production-scheduling**: For quality-driven scheduling
- **supply-chain-analytics**: For quality KPIs and dashboards
- **maintenance-planning**: For equipment reliability and quality
- **prescriptive-analytics**: For predictive quality analytics
- **compliance-management**: For regulatory quality requirements
- **supplier-selection**: For supplier quality evaluation
