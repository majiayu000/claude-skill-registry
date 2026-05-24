---
name: policyengine-core
description: PolicyEngine Core simulation engine - the foundation powering all PolicyEngine calculations
---

# PolicyEngine Core

PolicyEngine Core is the microsimulation engine that powers all PolicyEngine calculations. It's a fork of OpenFisca-Core adapted for PolicyEngine's needs.

## For Users 👥

### What is Core?

When you use policyengine.org to calculate taxes or benefits, PolicyEngine Core is the "calculator" running behind the scenes.

**Core provides:**
- The simulation engine that processes tax rules
- Variable and parameter management
- Entity relationships (person → family → household)
- Period handling (2024, 2025, etc.)

You don't interact with Core directly - you use it through:
- **Web app:** policyengine.org
- **Python packages:** policyengine-us, policyengine-uk
- **API:** api.policyengine.org

### Why Core Matters

Core ensures:
- ✅ **Accuracy** - Calculations follow official rules exactly
- ✅ **Consistency** - Same rules applied everywhere
- ✅ **Transparency** - All rules traceable to legislation
- ✅ **Performance** - Vectorized calculations for speed

## For Analysts 📊

### Understanding Core Concepts

When writing PolicyEngine code, you'll encounter Core concepts:

**Variables:**
- Represent quantities (income_tax, ctc, snap, etc.)
- Defined for specific entities (person, household, tax_unit)
- Calculated from formulas or set directly

**Parameters:**
- Policy rules that change over time (tax rates, benefit amounts)
- Organized hierarchically (gov.irs.credits.ctc.amount.base_amount)
- Stored in YAML files

**Entities:**
- Person: Individual
- Family: Family unit
- Tax unit: Tax filing unit
- Household: Physical household
- Marital unit: Marital status grouping
- SPM unit: Supplemental Poverty Measure unit

**Periods:**
- Year: 2024, 2025, etc.
- Month: 2024-01, 2024-02, etc.
- Specific dates: 2024-06-15

### Core in Action

```python
from policyengine_us import Simulation

# When you create a simulation
sim = Simulation(situation=household)

# Core manages:
# - Entity relationships
# - Variable dependencies
# - Parameter lookups
# - Period conversions

# When you calculate
result = sim.calculate("income_tax", 2024)

# Core:
# 1. Checks if already calculated
# 2. Identifies dependencies (income → AGI → taxable income → tax)
# 3. Calculates dependencies first
# 4. Applies formulas
# 5. Returns result
```

### Core vs Country Packages

**Core (policyengine-core):**
- Generic simulation engine
- No specific tax/benefit rules
- Variable and parameter infrastructure

**Country packages (policyengine-us, etc.):**
- Built on Core
- Contain specific tax/benefit rules
- Define variables and parameters for that country

**Relationship:**
```
policyengine-core (engine)
    ↓ powers
policyengine-us (US rules)
    ↓ used by
policyengine-api (REST API)
    ↓ serves
policyengine-app (web interface)
```

## For Contributors 💻

### Repository

**Location:** PolicyEngine/policyengine-core
**Origin:** Fork of OpenFisca-Core

**Clone:**
```bash
git clone https://github.com/PolicyEngine/policyengine-core
```

### Current Architecture

**To see current structure:**
```bash
tree policyengine_core/

# Key directories:
# - variables/ - Variable class and infrastructure
# - parameters/ - Parameter class and infrastructure
# - entities/ - Entity definitions
# - simulations/ - Simulation class
# - periods/ - Period handling
# - reforms/ - Reform application
```

**To understand a specific component:**
```bash
# Variable system
cat policyengine_core/variables/variable.py

# Parameter system
cat policyengine_core/parameters/parameter.py

# Simulation engine
cat policyengine_core/simulations/simulation.py

# Entity system
cat policyengine_core/entities/entity.py
```

### Key Classes

**Variable:**
```python
# To see Variable class implementation
cat policyengine_core/variables/variable.py

# Variables in country packages inherit from this:
from policyengine_core.variables import Variable

class income_tax(Variable):
    value_type = float
    entity = Person
    label = "Income tax"
    definition_period = YEAR

    def formula(person, period, parameters):
        # Vectorized formula
        return calculate_tax(...)
```

**Simulation:**
```python
# To see Simulation class implementation
cat policyengine_core/simulations/simulation.py

# Manages calculation graph and caching
sim = Simulation(situation=situation)
sim.calculate("variable", period)
```

**Parameters:**
```python
# To see Parameter handling
cat policyengine_core/parameters/parameter_node.py

# Access in formulas:
parameters(period).gov.irs.credits.ctc.amount.base_amount
```

### Vectorization (Critical!)

Core requires vectorized operations - no if-elif-else with arrays:

**❌ Wrong (scalar logic):**
```python
if age < 18:
    eligible = True
else:
    eligible = False
```

**✅ Correct (vectorized):**
```python
eligible = age < 18  # NumPy boolean array
```

**Why:** Core processes many households simultaneously for performance.

**To see vectorization examples:**
```bash
# Search for where() usage (vectorized if-then-else)
grep -r "np.where" policyengine_core/

# Find select() usage (vectorized case statements)
grep -r "select" policyengine_core/
```

### Formula Dependencies

Core automatically resolves variable dependencies:

```python
class taxable_income(Variable):
    def formula(person, period, parameters):
        # Core automatically calculates these first:
        agi = person("adjusted_gross_income", period)
        deduction = person("standard_deduction", period)
        return agi - deduction

class income_tax(Variable):
    def formula(person, period, parameters):
        # Core knows to calculate taxable_income first
        taxable = person("taxable_income", period)
        return apply_brackets(taxable, ...)
```

**To see dependency resolution:**
```bash
# Find trace functionality
grep -r "trace" policyengine_core/simulations/

# Enable in your code:
simulation.trace = True
simulation.calculate("income_tax", 2024)
```

### Period Handling

**To see period implementation:**
```bash
cat policyengine_core/periods/period.py

# Period types:
# - YEAR: 2024
# - MONTH: 2024-01
# - ETERNITY: permanent values
```

**Usage in variables:**
```python
# Annual variable
definition_period = YEAR  # Called with 2024

# Monthly variable
definition_period = MONTH  # Called with "2024-01"

# Convert periods
yearly_value = person("monthly_income", period.this_year) * 12
```

### Testing Core Changes

**To run Core tests:**
```bash
cd policyengine-core
make test

# Specific test
pytest tests/core/test_variables.py -v
```

**To test in country package:**
```bash
# Changes to Core affect all country packages
cd policyengine-us
pip install -e ../policyengine-core  # Local development install
make test
```

### Key Differences from OpenFisca

PolicyEngine Core differs from OpenFisca-Core:

**To see PolicyEngine changes:**
```bash
# Compare to OpenFisca
# Core fork diverged to add:
# - Enhanced performance
# - Better error messages
# - PolicyEngine-specific features

# See commit history for PolicyEngine changes
git log --oneline
```

## Core Development Workflow

### Making Changes to Core

1. **Clone repo:**
   ```bash
   git clone https://github.com/PolicyEngine/policyengine-core
   ```

2. **Install for development:**
   ```bash
   make install
   ```

3. **Make changes** to variable.py, simulation.py, etc.

4. **Test locally:**
   ```bash
   make test
   ```

5. **Test in country package:**
   ```bash
   cd ../policyengine-us
   pip install -e ../policyengine-core
   make test
   ```

6. **Format and commit:**
   ```bash
   make format
   git commit -m "Description"
   ```

### Understanding Impact

Changes to Core affect:
- ✅ All country packages (US, UK, Canada, IL, NG)
- ✅ The API
- ✅ The web app
- ✅ All analysis tools

**Critical:** Always test in multiple country packages before merging.

## Common Core Patterns

### Pattern 1: Adding a New Variable Type

**Current variable types:**
```bash
# See supported types
grep "value_type" policyengine_core/variables/variable.py
```

**Types:** int, float, bool, str, Enum, date

### Pattern 2: Custom Formulas

**Formula signature:**
```python
def formula(entity, period, parameters):
    # entity: Person, TaxUnit, Household, etc.
    # period: 2024, "2024-01", etc.
    # parameters: Parameter tree for period
    return calculated_value
```

**To see formula examples:**
```bash
# Search country packages for formulas
grep -A 10 "def formula" ../policyengine-us/policyengine_us/variables/ | head -50
```

### Pattern 3: Parameter Access

**Accessing parameters in formulas:**
```python
# Navigate parameter tree
param = parameters(period).gov.irs.credits.ctc.amount.base_amount

# Parameters automatically valid for period
# No need to check dates manually
```

**To see parameter structure:**
```bash
# Example from country package
tree ../policyengine-us/policyengine_us/parameters/gov/
```

## Advanced Topics

### Formula Caching

Core caches calculations automatically:
```python
# First call calculates
tax1 = sim.calculate("income_tax", 2024)

# Second call returns cached value
tax2 = sim.calculate("income_tax", 2024)  # Instant
```

### Performance Optimization: Batching Parameter Lookups

When parameter lookups happen inside loops, batch them beforehand to avoid repeated function call overhead:

**❌ Inefficient (repeated lookups):**
```python
# Inside uprate_parameters or similar functions
for instant in instants:
    value = uprating_parameter(instant)  # Repeated function calls
    # ... use value
```

**✅ Efficient (batched lookups):**
```python
# Pre-compute all values before the loop
value_cache = {
    instant: uprating_parameter(instant)
    for instant in instants
}

# Use cached values in loop
for instant in instants:
    value = value_cache[instant]  # Fast dictionary lookup
    # ... use value
```

**Why it matters:**
- Parameter lookups involve instant/period conversions and tree traversal
- In large parameter sets (like policyengine-us), this can cause millions of redundant calls
- Example: `uprate_parameters` reduced from 15s to 13.8s (8% improvement) by batching lookups

**When to batch:**
- Parameter lookups inside loops
- Multiple lookups of the same value at different points in code
- Any repeated `parameters(period).path.to.value` calls

**To find optimization opportunities:**
```bash
# Profile import time
python -m cProfile -o profile.stats -c "from policyengine_us.system import system"

# Search for parameter lookup hotspots
grep -r "parameters(period)" policyengine_core/parameters/
```

### Neutralizing Variables

```python
# Set variable to zero in reform
reform = {
    "income_tax": {
        "2024-01-01.2100-12-31": 0
    }
}
```

### Adding Variables

Country packages add variables by inheriting from Core's Variable class.

**See policyengine-us-skill for variable creation patterns.**

## Resources

**Repository:** https://github.com/PolicyEngine/policyengine-core

**Documentation:**
- Core API docs (see README in repo)
- OpenFisca docs (original): https://openfisca.org/doc/

**Related skills:**
- **policyengine-us-skill** - Using Core through country packages
- **policyengine-standards-skill** - Code quality standards

## Troubleshooting

### Common Issues

**Variable not found:**
```python
# Error: Variable 'income_tax' not found
# Solution: Variable is defined in country package, not Core
# Use policyengine-us, not policyengine-core directly
```

**Scalar vs array operations:**
```python
# Error: truth value of array is ambiguous
# Solution: Use np.where() instead of if-else
# See vectorization section above
```

**Period mismatch:**
```python
# Error: Cannot compute variable_name for period 2024-01
# Solution: Check definition_period matches request
# YEAR variables need YEAR periods (2024, not "2024-01")
```

**To debug:**
```python
# Enable tracing
sim.trace = True
sim.calculate("variable", period)
# See calculation dependency tree
```

## Contributing to Core

**Before contributing:**
1. Read Core README
2. Understand OpenFisca architecture
3. Test changes in multiple country packages
4. Follow policyengine-standards-skill

**Development standards:**
- Python 3.10-3.13
- Black formatting (79-char)
- Comprehensive tests
- No breaking changes without discussion
