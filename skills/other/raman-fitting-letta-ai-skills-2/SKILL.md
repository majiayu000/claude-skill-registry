---
name: raman-fitting
description: This skill provides guidance for fitting peaks in Raman spectroscopy data, particularly for materials like graphene. Use this skill when tasks involve Raman spectrum analysis, peak fitting (G peak, 2D peak, D peak), or spectroscopic curve fitting using Lorentzian, Gaussian, or Voigt functions.
---

# Raman Spectrum Peak Fitting

## Overview

This skill provides procedural knowledge for fitting peaks in Raman spectroscopy data. Raman spectroscopy is commonly used to characterize materials like graphene, carbon nanotubes, and other crystalline structures. Proper peak fitting requires understanding both the physics of Raman scattering and robust numerical fitting techniques.

## Critical First Step: Data Exploration

Before any fitting attempts, perform comprehensive data exploration to avoid fundamental misinterpretations:

### 1. Verify Data Format
- Examine file structure carefully (delimiters, column separators, row numbering)
- Check for locale-specific number formats (e.g., `47183,554644` may use comma as decimal separator)
- Identify whether columns represent wavenumber, wavelength, or require conversion
- Look for header rows or metadata that may affect parsing

### 2. Assess Data Range and Quality
- Determine the wavenumber range covered by the dataset
- Check if expected peak positions fall within the data range
- Identify noise levels and baseline characteristics
- Plot the entire spectrum before attempting any fits

### 3. Compare Against Expected Values
For graphene Raman spectra, typical peak positions are:
- **D peak**: ~1350 cm⁻¹ (disorder-induced)
- **G peak**: ~1580 cm⁻¹ (in-plane vibration)
- **2D peak**: ~2700 cm⁻¹ (second-order)

If data range excludes expected peak positions, document this limitation before proceeding.

## Peak Fitting Workflow

### Step 1: Background Subtraction
- Apply baseline correction before fitting peaks
- Common methods: linear baseline, polynomial fit, or asymmetric least squares
- Document the baseline method used

### Step 2: Select Appropriate Peak Function
Choose based on physical broadening mechanisms:

| Function | Use Case |
|----------|----------|
| **Lorentzian** | Natural linewidth broadening, homogeneous systems |
| **Gaussian** | Instrumental broadening, inhomogeneous systems |
| **Voigt** | Combination of both effects (most physically realistic) |
| **Pseudo-Voigt** | Computationally simpler approximation to Voigt |

### Step 3: Define Fitting Region
- Select regions containing individual peaks
- Avoid arbitrary region changes without documented justification
- Consider overlapping peaks that may require multi-peak fitting

### Step 4: Set Physical Constraints
Apply parameter bounds based on physical knowledge:
- Peak positions: within ±50 cm⁻¹ of expected values
- Linewidths (FWHM): typically 10-100 cm⁻¹ for Raman peaks
- Intensities: positive values only

### Step 5: Execute Fit and Validate

## Fit Quality Validation

### Metrics to Check
1. **R² value**: Should be > 0.9 for acceptable fits; < 0.5 indicates fit failure
2. **Residual analysis**: Look for systematic deviations, not random scatter
3. **Parameter bounds**: Parameters hitting bounds indicates fit problems
4. **Physical plausibility**: Compare fitted values against literature

### Warning Signs of Fit Failure
- Parameters exactly at constraint boundaries
- R² < 0.5
- Fitted peak position differs > 50 cm⁻¹ from expected
- Fitted linewidth unreasonably narrow (< 5 cm⁻¹) or broad (> 200 cm⁻¹)
- Negative intensity values

### Response to Poor Fits
When fits fail, systematically explore alternatives:
1. Try different peak functions (Gaussian, Voigt instead of Lorentzian)
2. Consider multiple overlapping peaks
3. Improve background subtraction
4. Adjust fitting region
5. Check for data quality issues in that spectral region

Do NOT accept poor fits as "the best possible" without exhausting alternatives.

## Code Design Principles

### Write Modular, Reusable Code
Instead of creating multiple scripts with duplicated code:

```python
# Define once and reuse
def lorentzian(x, amplitude, center, gamma):
    """Lorentzian peak function."""
    return amplitude * gamma**2 / ((x - center)**2 + gamma**2)

def fit_peak(wavenumber, intensity, region, peak_func, initial_guess, bounds):
    """Generic peak fitting with validation."""
    mask = (wavenumber >= region[0]) & (wavenumber <= region[1])
    x_fit, y_fit = wavenumber[mask], intensity[mask]

    popt, pcov = curve_fit(peak_func, x_fit, y_fit, p0=initial_guess, bounds=bounds)

    # Validate fit
    y_pred = peak_func(x_fit, *popt)
    r_squared = 1 - np.sum((y_fit - y_pred)**2) / np.sum((y_fit - np.mean(y_fit))**2)

    return popt, pcov, r_squared
```

### Include Sanity Checks
```python
def validate_graphene_peak(peak_name, position, expected, tolerance=50):
    """Check if fitted position is physically reasonable."""
    if abs(position - expected) > tolerance:
        print(f"WARNING: {peak_name} at {position:.1f} cm⁻¹ differs from expected {expected} cm⁻¹")
        return False
    return True
```

## Common Pitfalls

1. **Incomplete Data Exploration**: Jumping to fitting without understanding data format and range
2. **Accepting Poor Fits**: Reporting R² < 0.5 as valid results
3. **Ignoring Physical Constraints**: Not checking if results match known material properties
4. **Code Duplication**: Creating multiple scripts instead of parameterized functions
5. **Arbitrary Region Selection**: Changing fitting regions without justification
6. **Missing Baseline Correction**: Fitting raw data without background subtraction
7. **Single Function Assumption**: Not trying alternative peak shapes when fits fail

## Output Requirements

When reporting Raman fitting results, include:
1. Data format and any preprocessing applied
2. Fitting function and justification
3. Fitted parameters with uncertainties
4. R² or other goodness-of-fit metric
5. Comparison to expected literature values
6. Any limitations or caveats (e.g., data range issues)

## References

For detailed information on Raman spectroscopy fitting approaches, consult `references/raman_fitting_guide.md`.
