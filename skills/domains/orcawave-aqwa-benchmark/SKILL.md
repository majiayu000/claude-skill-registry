---
name: orcawave-aqwa-benchmark
description: Cross-validation specialist for comparing OrcaWave and AQWA diffraction
  analysis results. Provides statistical comparison, peak value validation, and automated
  benchmark reporting for hydrodynamic coefficient verification.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- AQWA OrcaWave comparison
- diffraction benchmark
- RAO validation
- hydrodynamic coefficient comparison
- cross-tool validation
- panel method benchmark
- added mass comparison
- damping comparison
---

# OrcaWave-AQWA Benchmark Skill

Specialized expertise for cross-validating OrcaWave and AQWA diffraction analysis results with statistical comparison frameworks.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  numpy: '>=1.24.0'
  pandas: '>=2.0.0'
  plotly: '>=5.15.0'
  scipy: '>=1.11.0'
compatibility:
  tested_python:
  - '3.10'
  - '3.11'
  - '3.12'
  - '3.13'
  os:
  - Windows
  - Linux
  - macOS
```

## When to Use

- Validating OrcaWave results against AQWA benchmarks
- Comparing RAO amplitudes and phases between tools
- Verifying added mass and damping matrices
- Running automated benchmark test suites
- Generating comparison reports for quality assurance
- Establishing confidence in diffraction analysis results
- Identifying discrepancies between panel method implementations

## Validation Criteria

### Standard Tolerances

| Metric | Tolerance | Scope |
|--------|-----------|-------|
| Peak RAO Deviation | 5% | Significant values (>=10% of peak) |
| Phase Deviation | 5 degrees | At significant RAO values |
| Added Mass | 5% | Diagonal terms |
| Damping | 10% | Frequency-dependent |
| Mean Drift | 10% | All headings |

### Significance Threshold

Only values >= 10% of peak magnitude are considered for validation. This focuses comparison on physically meaningful responses rather than numerical noise in low-response regions.

## Python API

### Basic Comparison

```python
from digitalmodel.modules.diffraction.comparison_framework import (
    DiffractionComparator,
    PeakRAOComparator
)
from digitalmodel.modules.diffraction.aqwa_converter import AQWAConverter
from digitalmodel.modules.diffraction.orcawave_converter import OrcaWaveConverter

# Load AQWA results
aqwa_converter = AQWAConverter()
aqwa_results = aqwa_converter.convert_to_unified_schema(
    lis_file="aqwa_results/vessel.LIS",
    output_format="dict"
)

# Load OrcaWave results
orcawave_converter = OrcaWaveConverter(vessel_object)
orcawave_results = orcawave_converter.convert()

# Create comparator
comparator = DiffractionComparator(
    reference=aqwa_results,
    test=orcawave_results,
    reference_name="AQWA",
    test_name="OrcaWave"
)

# Run full comparison
results = comparator.compare_all()

# Print summary
print(f"Overall agreement: {results['overall_agreement']:.1%}")
print(f"RAO correlation: {results['rao_correlation']:.3f}")
print(f"Max deviation: {results['max_deviation']:.1%}")
```

### Peak-Focused Validation

```python
from digitalmodel.modules.diffraction.comparison_framework import PeakRAOComparator

# Peak-focused comparison (recommended for validation)
peak_comparator = PeakRAOComparator(
    aqwa_results=aqwa_results,
    orcawave_results=orcawave_results,
    peak_threshold=0.10,  # 10% of peak magnitude
    tolerance=0.05  # 5% tolerance
)

# Compare peak values
peak_results = peak_comparator.compare_peaks()

# Check if validation passed
if peak_results['validation_passed']:
    print("VALIDATION PASSED")
    print(f"  Points within tolerance: {peak_results['points_within_tolerance']:.1%}")
else:
    print("VALIDATION FAILED")
    print(f"  Deviations found: {len(peak_results['deviations'])}")

# Generate detailed report
peak_comparator.generate_peak_report_html(
    peak_results,
    output_file="reports/benchmark_validation.html"
)
```

### Matrix Comparison

```python
from digitalmodel.modules.diffraction.comparison_framework import MatrixComparator

# Compare added mass matrices
matrix_comp = MatrixComparator()

# Compare at specific frequency
freq = 0.1  # rad/s
am_comparison = matrix_comp.compare_added_mass(
    aqwa_matrix=aqwa_results['added_mass'][freq],
    orcawave_matrix=orcawave_results['added_mass'][freq],
    tolerance=0.05
)

print(f"Added mass agreement at {freq} rad/s:")
for dof, deviation in am_comparison['diagonal_deviations'].items():
    status = "OK" if deviation < 0.05 else "FAIL"
    print(f"  {dof}: {deviation:.1%} [{status}]")

# Compare damping matrices
damp_comparison = matrix_comp.compare_damping(
    aqwa_matrix=aqwa_results['damping'][freq],
    orcawave_matrix=orcawave_results['damping'][freq],
    tolerance=0.10
)
```

### Statistical Analysis

```python
from digitalmodel.modules.diffraction.comparison_framework import StatisticalAnalyzer

# Initialize analyzer
analyzer = StatisticalAnalyzer()

# Compute correlation metrics
correlation = analyzer.compute_correlation(
    aqwa_raos=aqwa_results['raos'],
    orcawave_raos=orcawave_results['raos']
)

print(f"Pearson R: {correlation['pearson_r']:.4f}")
print(f"R-squared: {correlation['r_squared']:.4f}")
print(f"RMSE: {correlation['rmse']:.4f}")
print(f"Max error: {correlation['max_error']:.4f}")

# Compute per-DOF statistics
dof_stats = analyzer.compute_dof_statistics(
    aqwa_raos=aqwa_results['raos'],
    orcawave_raos=orcawave_results['raos']
)

for dof, stats in dof_stats.items():
    print(f"{dof}: R²={stats['r_squared']:.3f}, RMSE={stats['rmse']:.4f}")
```

## Configuration Examples

### Benchmark Suite Configuration

```yaml
# configs/benchmark_suite.yml

benchmark:
  name: "FPSO Diffraction Validation"
  description: "OrcaWave vs AQWA comparison for FPSO vessel"

  reference:
    tool: "AQWA"
    version: "2024.R1"
    files:
      lis_file: "aqwa_results/fpso.LIS"
      dat_file: "aqwa_results/fpso.dat"

  test:
    tool: "OrcaWave"
    version: "11.4"
    files:
      owr_file: "orcawave_results/fpso.owr"

  comparison:
    tolerances:
      rao_amplitude: 0.05  # 5%
      rao_phase: 5.0  # degrees
      added_mass: 0.05
      damping: 0.10
      mean_drift: 0.10

    significance:
      peak_threshold: 0.10  # 10% of peak

    dofs:
      - Surge
      - Sway
      - Heave
      - Roll
      - Pitch
      - Yaw

    headings: [0, 30, 60, 90, 120, 150, 180]

  output:
    directory: "reports/benchmark/"
    formats: ["html", "json", "csv"]
    include_plots: true
```

### Automated Validation Script

```yaml
# configs/validation_criteria.yml

validation:
  pass_criteria:
    # At least 90% of significant points within tolerance
    min_points_within_tolerance: 0.90

    # Maximum allowed deviation for any single point
    max_single_deviation: 0.15

    # Minimum correlation coefficient
    min_correlation: 0.95

  report_levels:
    - level: "summary"
      include: ["overall_status", "key_metrics"]
    - level: "detailed"
      include: ["per_dof_analysis", "frequency_breakdown"]
    - level: "diagnostic"
      include: ["all_deviations", "raw_data"]
```

## CLI Usage

```bash
# Run full benchmark comparison
python -m digitalmodel.modules.diffraction.benchmark compare \
    --aqwa aqwa_results/vessel.LIS \
    --orcawave orcawave_results/vessel.owr \
    --output reports/comparison.html

# Peak-focused validation
python -m digitalmodel.modules.diffraction.benchmark validate \
    --aqwa aqwa_results/vessel.LIS \
    --orcawave orcawave_results/vessel.owr \
    --tolerance 0.05 \
    --peak-threshold 0.10

# Generate comparison plots
python -m digitalmodel.modules.diffraction.benchmark plot \
    --aqwa aqwa_results/vessel.LIS \
    --orcawave orcawave_results/vessel.owr \
    --output plots/ \
    --format html

# Export comparison data
python -m digitalmodel.modules.diffraction.benchmark export \
    --aqwa aqwa_results/vessel.LIS \
    --orcawave orcawave_results/vessel.owr \
    --format csv \
    --output comparison_data.csv
```

## Report Generation

### HTML Report Structure

```python
from digitalmodel.modules.diffraction.comparison_framework import BenchmarkReporter

# Initialize reporter
reporter = BenchmarkReporter()

# Generate comprehensive report
reporter.generate_html_report(
    comparison_results=results,
    output_file="reports/benchmark_report.html",
    sections=[
        "executive_summary",
        "rao_comparison_plots",
        "matrix_comparison",
        "statistical_analysis",
        "deviation_table",
        "recommendations"
    ]
)
```

### Report Sections

1. **Executive Summary**: Pass/fail status, key metrics
2. **RAO Comparison Plots**: Interactive Plotly charts per DOF
3. **Matrix Comparison**: Added mass/damping heat maps
4. **Statistical Analysis**: Correlation, RMSE, R-squared
5. **Deviation Table**: All points exceeding tolerance
6. **Recommendations**: Suggested actions for discrepancies

## Benchmark Test Cases

### Standard Test Suite

```python
from digitalmodel.modules.diffraction.benchmark import BenchmarkSuite

# Initialize test suite
suite = BenchmarkSuite()

# Add test cases
suite.add_test_case(
    name="heave_resonance",
    description="Heave RAO at resonance frequency",
    frequency_range=(0.3, 0.5),
    dofs=["Heave"],
    tolerance=0.05
)

suite.add_test_case(
    name="roll_resonance",
    description="Roll RAO at natural period",
    frequency_range=(0.1, 0.2),
    dofs=["Roll"],
    tolerance=0.05
)

suite.add_test_case(
    name="beam_seas",
    description="Beam sea response (90 degrees)",
    headings=[90],
    dofs=["Sway", "Roll"],
    tolerance=0.05
)

# Run test suite
results = suite.run(
    aqwa_results=aqwa_data,
    orcawave_results=orcawave_data
)

# Generate test report
suite.generate_report(results, "reports/test_suite_results.html")
```

## Troubleshooting Discrepancies

### Common Causes of Deviation

| Issue | Typical Deviation | Solution |
|-------|-------------------|----------|
| Mesh differences | 5-15% | Use similar panel counts |
| Coordinate systems | Phase shift | Verify origin/orientation |
| Frequency resolution | Variable | Interpolate to common frequencies |
| Irregular frequency removal | 10-20% at specific freqs | Check lid method settings |
| Viscous damping | Roll/pitch deviation | Ensure consistent settings |

### Diagnostic Workflow

```python
from digitalmodel.modules.diffraction.comparison_framework import DiagnosticAnalyzer

# Initialize diagnostic analyzer
diagnostic = DiagnosticAnalyzer()

# Run diagnostics
issues = diagnostic.identify_issues(
    aqwa_results=aqwa_data,
    orcawave_results=orcawave_data,
    comparison_results=results
)

# Print identified issues
for issue in issues:
    print(f"Issue: {issue['type']}")
    print(f"  Severity: {issue['severity']}")
    print(f"  DOFs affected: {issue['dofs']}")
    print(f"  Recommendation: {issue['recommendation']}")
```

## Integration with CI/CD

### Automated Validation in Pipeline

```yaml
# .github/workflows/diffraction-validation.yml

name: Diffraction Benchmark Validation

on:
  push:
    paths:
      - 'orcawave_results/**'
      - 'aqwa_results/**'

jobs:
  validate:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run benchmark validation
        run: |
          python -m digitalmodel.modules.diffraction.benchmark validate \
            --aqwa aqwa_results/vessel.LIS \
            --orcawave orcawave_results/vessel.owr \
            --tolerance 0.05 \
            --fail-on-deviation

      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: benchmark-report
          path: reports/benchmark_validation.html
```

## Best Practices

1. **Consistent Setup**: Use identical environmental conditions (depth, density)
2. **Matching Frequencies**: Interpolate to common frequency discretization
3. **Coordinate Alignment**: Verify origin and axis conventions match
4. **Peak Focus**: Validate significant values, not numerical noise
5. **Document Differences**: Record known differences between tools
6. **Version Control**: Track software versions for reproducibility
7. **Regular Validation**: Re-run benchmarks after software updates

## Related Skills

- [orcawave-analysis](../orcawave-analysis/SKILL.md) - OrcaWave analysis execution
- [aqwa-analysis](../aqwa-analysis/SKILL.md) - AQWA analysis execution
- [hydrodynamics](../hydrodynamics/SKILL.md) - Coefficient management

## References

- Comparison Framework: `src/digitalmodel/modules/diffraction/comparison_framework.py`
- Benchmark Data: `docs/modules/orcawave/L01_aqwa_benchmark/`
- AQWA Converter: `src/digitalmodel/modules/diffraction/aqwa_converter.py`
- OrcaWave Converter: `src/digitalmodel/modules/diffraction/orcawave_converter.py`

---

**Version History**

- **1.0.0** (2026-01-17): Initial release with comparison framework, peak validation, and statistical analysis
