---
name: microimpute
description: ML-based variable imputation for survey data - used in policyengine-us-data to fill missing values
---

# MicroImpute

MicroImpute enables ML-based variable imputation through different statistical methods, with comparison and benchmarking capabilities.

## For Users 👥

### What is MicroImpute?

When PolicyEngine calculates population impacts, the underlying survey data has missing information. MicroImpute uses machine learning to fill in those gaps intelligently.

**What imputation does:**
- Fills missing data in surveys
- Uses machine learning to predict missing values
- Maintains statistical relationships
- Improves PolicyEngine accuracy

**Example:**
- Survey asks about income but not capital gains breakdown
- MicroImpute predicts short-term vs long-term capital gains
- Based on patterns from IRS data
- Result: More accurate tax calculations

**You benefit from imputation when:**
- PolicyEngine calculates capital gains tax accurately
- Benefits eligibility uses complete household information
- State-specific calculations have all needed data

## For Analysts 📊

### Installation

```bash
pip install microimpute

# With image export (for plots)
pip install microimpute[images]
```

### What MicroImpute Does

**Imputation problem:**
- Donor dataset has complete information (e.g., IRS tax records)
- Recipient dataset has missing variables (e.g., CPS survey)
- Imputation predicts missing values in recipient using donor patterns

**Methods available:**
- Linear regression
- Random forest
- Quantile forest (preserves full distribution)
- XGBoost
- Hot deck (traditional matching)

### Quick Example

```python
from microimpute import Imputer
import pandas as pd

# Donor data (complete)
donor = pd.DataFrame({
    'income': [50000, 60000, 70000],
    'age': [30, 40, 50],
    'capital_gains': [5000, 8000, 12000]  # Variable to impute
})

# Recipient data (missing capital_gains)
recipient = pd.DataFrame({
    'income': [55000, 65000],
    'age': [35, 45],
    # capital_gains is missing
})

# Impute using quantile forest
imputer = Imputer(method='quantile_forest')
imputer.fit(
    donor=donor,
    donor_target='capital_gains',
    common_vars=['income', 'age']
)

recipient_imputed = imputer.predict(recipient)
# Now recipient has predicted capital_gains
```

### Method Comparison

```python
from microimpute import compare_methods

# Compare different imputation methods
results = compare_methods(
    donor=donor,
    recipient=recipient,
    target_var='capital_gains',
    common_vars=['income', 'age'],
    methods=['linear', 'random_forest', 'quantile_forest']
)

# Shows quantile loss for each method
print(results)
```

### Quantile Loss (Quality Metric)

**Why quantile loss:**
- Measures how well imputation preserves the distribution
- Not just mean accuracy, but full distribution shape
- Lower is better

**Interpretation:**
```python
# Quantile loss around 0.1 = good
# Quantile loss around 0.5 = poor
# Compare across methods to choose best
```

## For Contributors 💻

### Repository

**Location:** PolicyEngine/microimpute

**Clone:**
```bash
git clone https://github.com/PolicyEngine/microimpute
cd microimpute
```

### Current Implementation

**To see structure:**
```bash
tree microimpute/

# Key modules:
ls microimpute/
# - imputer.py - Main Imputer class
# - methods/ - Different imputation methods
# - comparison.py - Method benchmarking
# - utils/ - Utilities
```

**To see specific methods:**
```bash
# Quantile forest implementation
cat microimpute/methods/quantile_forest.py

# Random forest
cat microimpute/methods/random_forest.py

# Linear regression
cat microimpute/methods/linear.py
```

### Dependencies

**Required:**
- numpy, pandas (data handling)
- scikit-learn (ML models)
- quantile-forest (distributional imputation)
- optuna (hyperparameter tuning)
- statsmodels (statistical methods)
- scipy (statistical functions)

**To see all dependencies:**
```bash
cat pyproject.toml
```

### Adding New Imputation Methods

**Pattern:**
```python
# microimpute/methods/my_method.py

class MyMethodImputer:
    def fit(self, X_train, y_train):
        """Train on donor data."""
        # Fit your model
        pass

    def predict(self, X_test):
        """Impute on recipient data."""
        # Return predictions
        pass

    def get_quantile_loss(self, X_val, y_val):
        """Compute validation loss."""
        # Evaluate quality
        pass
```

### Usage in policyengine-us-data

**To see how data pipeline uses microimpute:**
```bash
cd ../policyengine-us-data

# Find usage
grep -r "microimpute" policyengine_us_data/
grep -r "Imputer" policyengine_us_data/
```

**Typical workflow:**
1. Load CPS (has demographics, missing capital gains details)
2. Load IRS PUF (has complete tax data)
3. Use microimpute to predict missing CPS variables from PUF patterns
4. Validate imputation quality
5. Save enhanced dataset

### Testing

**Run tests:**
```bash
make test

# Or
pytest tests/ -v --cov=microimpute
```

**To see test patterns:**
```bash
cat tests/test_imputer.py
cat tests/test_methods.py
```

## Common Patterns

### Pattern 1: Basic Imputation

```python
from microimpute import Imputer

# Create imputer
imputer = Imputer(method='quantile_forest')

# Fit on donor (complete data)
imputer.fit(
    donor=donor_df,
    donor_target='target_variable',
    common_vars=['age', 'income', 'state']
)

# Predict on recipient (missing target_variable)
recipient_imputed = imputer.predict(recipient_df)
```

### Pattern 2: Choosing Best Method

```python
from microimpute import compare_methods

# Test multiple methods
methods = ['linear', 'random_forest', 'quantile_forest', 'xgboost']

results = compare_methods(
    donor=donor,
    recipient=recipient,
    target_var='target',
    common_vars=common_vars,
    methods=methods
)

# Use method with lowest quantile loss
best_method = results.sort_values('quantile_loss').iloc[0]['method']
```

### Pattern 3: Multiple Variable Imputation

```python
# Impute several variables
variables_to_impute = [
    'short_term_capital_gains',
    'long_term_capital_gains',
    'qualified_dividends'
]

for var in variables_to_impute:
    imputer = Imputer(method='quantile_forest')
    imputer.fit(donor=irs_puf, donor_target=var, common_vars=common_vars)
    cps[var] = imputer.predict(cps)
```

## Advanced Features

### Hyperparameter Tuning

**Built-in Optuna integration:**
```python
from microimpute import tune_hyperparameters

# Automatically find best hyperparameters
best_params, study = tune_hyperparameters(
    donor=donor,
    target_var='target',
    common_vars=common_vars,
    method='quantile_forest',
    n_trials=100
)

# Use tuned parameters
imputer = Imputer(method='quantile_forest', **best_params)
```

### Cross-Validation

**Validate imputation quality:**
```python
from sklearn.model_selection import cross_val_score

# Split donor for validation
# Impute on validation set
# Measure accuracy
```

### Visualization

**Plot imputation results:**
```python
import plotly.express as px

# Compare imputed vs actual (on donor validation set)
fig = px.scatter(
    x=actual_values,
    y=imputed_values,
    labels={'x': 'Actual', 'y': 'Imputed'}
)
fig.add_trace(px.line(x=[min, max], y=[min, max]))  # 45-degree line
```

## Statistical Background

**Imputation preserves:**
- Marginal distributions (imputed variable distribution matches donor)
- Conditional relationships (imputation depends on common variables)
- Uncertainty (quantile methods preserve full distribution)

**Trade-offs:**
- **Linear:** Fast, but assumes linear relationships
- **Random forest:** Handles non-linearity, may overfit
- **Quantile forest:** Preserves full distribution, slower
- **XGBoost:** High accuracy, requires tuning

## Integration with PolicyEngine

**Full pipeline (policyengine-us-data):**
```
1. Load CPS survey data
   ↓
2. microimpute: Fill missing variables from IRS PUF
   ↓
3. microcalibrate: Adjust weights to match benchmarks
   ↓
4. Validation: Check against administrative totals
   ↓
5. Package: Distribute enhanced dataset
   ↓
6. PolicyEngine: Use for population simulations
```

## Comparison to Other Methods

**MicroImpute vs traditional imputation:**

**Traditional (mean imputation):**
- Fast but destroys distribution
- All missing values get same value
- Underestimates variance

**MicroImpute (ML methods):**
- Preserves relationships
- Different predictions per record
- Maintains distribution shape

**Quantile forest advantage:**
- Predicts full conditional distribution
- Not just point estimates
- Can sample from predicted distribution

## Performance Tips

**For large datasets:**
```python
# Use random forest (faster than quantile forest)
imputer = Imputer(method='random_forest')

# Or subsample donor
donor_sample = donor.sample(n=10000, random_state=42)
imputer.fit(donor=donor_sample, ...)
```

**For high accuracy:**
```python
# Use quantile forest with tuning
best_params, _ = tune_hyperparameters(...)
imputer = Imputer(method='quantile_forest', **best_params)
```

## Related Skills

- **l0-skill** - Regularization techniques
- **microcalibrate-skill** - Survey calibration (next step after imputation)
- **policyengine-us-data-skill** - Complete data pipeline
- **microdf-skill** - Working with imputed/calibrated data

## Resources

**Repository:** https://github.com/PolicyEngine/microimpute
**PyPI:** https://pypi.org/project/microimpute/
**Documentation:** See README and docstrings in source
