---
name: policyengine-simulation-mechanics
description: Advanced simulation patterns with policyengine.py - ensure(), output_dataset.data, and map_to_entity()
---

# PolicyEngine Simulation Mechanics

This skill covers advanced patterns for working with policyengine.py simulations, including caching, result access, and entity mapping.

## For Analysts: Core Concepts

When running simulations with policyengine.py (the microsimulation package, not the API client), you work with three key components:

1. **`Simulation.ensure()`** - Smart caching to avoid redundant computation
2. **`simulation.output_dataset.data`** - Accessing calculated results
3. **`map_to_entity()`** - Converting data between entity levels (person ↔ household)

**Note:** This is for microsimulation with policyengine.py, not the policyengine Python API client (which uses `Simulation(situation=...)`).

## Simulation Lifecycle

### The Four Methods

```python
from policyengine.core import Simulation
from policyengine.tax_benefit_models.uk import uk_latest

simulation = Simulation(
    dataset=dataset,
    tax_benefit_model_version=uk_latest,
)

# Method 1: Always run (no caching)
simulation.run()

# Method 2: Run only if needed (recommended)
simulation.ensure()

# Method 3: Save results to disk
simulation.save()

# Method 4: Load results from disk
simulation.load()
```

### When to Use Each

- **`run()`**: Use when you need fresh results or parameters changed
- **`ensure()`**: Use for iterative development (checks cache → disk → run)
- **`save()`**: Use to persist large simulation results
- **`load()`**: Use to resume from previous session

### How ensure() Works

```python
def ensure(self):
    # 1. Check in-memory LRU cache (100 simulations)
    cached = _cache.get(self.id)
    if cached:
        self.output_dataset = cached.output_dataset
        return

    # 2. Try loading from disk
    try:
        self.tax_benefit_model_version.load(self)
    except Exception:
        # 3. Only run if both cache and disk fail
        self.run()
        self.save()

    # 4. Add to cache for next ensure() call
    _cache.add(self.id, self)
```

**Performance impact:**
- First call: Full simulation runtime (seconds to minutes)
- Same session: Instant (in-memory cache)
- New session: Fast (disk load, no recomputation)

### Example: Reusing Baseline Across Reforms

```python
# Run baseline once
baseline = Simulation(dataset=dataset, tax_benefit_model_version=uk_latest)
baseline.ensure()  # First call: runs simulation
baseline.save()    # Persist to disk

# Test multiple reforms
for reform in [reform1, reform2, reform3]:
    baseline.ensure()  # Instant from cache!

    reform_sim = Simulation(
        dataset=dataset,
        tax_benefit_model_version=uk_latest,
        policy=reform
    )
    reform_sim.run()  # Only reform needs to run

    # Compare results...
```

## Accessing Results: output_dataset.data

After running a simulation, all calculated variables are in `simulation.output_dataset.data`.

### Structure (UK Example)

```python
simulation.run()

# Access output container
output = simulation.output_dataset.data

# Entity-level MicroDataFrames
output.person      # Person-level results
output.benunit     # Benefit unit results
output.household   # Household-level results
```

### US Entity Structure

```python
# US has more entities
output.person
output.tax_unit       # Federal tax filing unit
output.spm_unit       # Supplemental Poverty Measure unit
output.family         # Census family definition
output.marital_unit   # Married couple or single
output.household
```

### Available Variables

Each dataframe contains **input variables** + **calculated variables**:

```python
# Person-level (UK)
print(output.person.columns)
# ['person_id', 'person_household_id', 'age', 'employment_income',
#  'income_tax', 'national_insurance', 'net_income', ...]

# Household-level (UK)
print(output.household.columns)
# ['household_id', 'region', 'rent', 'household_net_income',
#  'household_benefits', 'household_tax', ...]

# Benunit-level (UK)
print(output.benunit.columns)
# ['benunit_id', 'universal_credit', 'child_benefit',
#  'working_tax_credit', 'child_tax_credit', ...]
```

### Direct Data Access

```python
# Get specific columns
incomes = output.household[["household_id", "household_net_income"]]

# Filter data
high_earners = output.person[output.person["employment_income"] > 100000]

# Calculate statistics (automatically weighted!)
mean_income = output.household["household_net_income"].mean()
total_tax = output.household["household_tax"].sum()

# Access individual values
first_hh_income = output.household["household_net_income"].iloc[0]
```

### MicroDataFrame Automatic Weighting

All operations respect survey weights automatically:

```python
# These are all weighted calculations
total_population = output.person["person_weight"].sum()
mean_income = output.household["household_net_income"].mean()
poverty_rate = output.household["in_absolute_poverty_bhc"].mean()

# Groupby operations are weighted
by_region = output.household.groupby("region")["household_net_income"].mean()
```

## Entity Mapping with map_to_entity()

Convert data between entity levels (e.g., sum person income to household, or broadcast household rent to persons).

### Method Signature

```python
output.map_to_entity(
    source_entity: str,        # Entity to map from
    target_entity: str,        # Entity to map to
    columns: list[str] = None, # Columns to map (None = all)
    values: np.ndarray = None, # Custom values instead
    how: str = "sum"           # Aggregation method
)
```

### Aggregation Methods

**Person → Group (aggregation):**
- `how="sum"` (default): Sum values within each group
- `how="first"`: Take first value in each group
- `how="mean"`: Average values
- `how="max"`: Maximum value
- `how="min"`: Minimum value

**Group → Person (expansion):**
- `how="project"` (default): Broadcast group value to all members
- `how="divide"`: Split group value equally among members

### Example 1: Sum Person Income to Household

```python
# Sum employment income across all people in each household
household_employment = output.map_to_entity(
    source_entity="person",
    target_entity="household",
    columns=["employment_income"],
    how="sum"
)

# Result is MicroDataFrame at household level
print(household_employment.columns)
# ['household_id', 'employment_income']  # Now household total
```

### Example 2: Broadcast Household Rent to Persons

```python
# Give each person their household's rent value
person_rent = output.map_to_entity(
    source_entity="household",
    target_entity="person",
    columns=["rent"],
    how="project"
)

# Each person now has their household's rent
print(person_rent.columns)
# ['person_id', 'rent']
```

### Example 3: Divide Household Value Per Person

```python
# Split household savings equally among members
person_savings_share = output.map_to_entity(
    source_entity="household",
    target_entity="person",
    columns=["total_savings"],
    how="divide"
)

# If household has £12,000 savings and 3 people, each gets £4,000
```

### Example 4: Map Custom Values

```python
import numpy as np

# Calculate custom person-level values
custom_tax = np.where(
    output.person["employment_income"] > 50000,
    output.person["income_tax"] * 1.1,  # 10% increase for high earners
    output.person["income_tax"]
)

# Aggregate to household level
household_custom_tax = output.map_to_entity(
    source_entity="person",
    target_entity="household",
    values=custom_tax,
    how="sum"
)
```

### Example 5: Multi-Column Mapping

```python
# Map multiple income sources to household level
household_incomes = output.map_to_entity(
    source_entity="person",
    target_entity="household",
    columns=[
        "employment_income",
        "self_employment_income",
        "pension_income",
        "savings_interest_income"
    ],
    how="sum"
)

# Result has all columns at household level
```

### Example 6: Cross-Entity Mapping (Group to Group)

```python
# UK: Map benunit benefits to household level
# (Multiple benunits can exist in one household)
household_uc = output.map_to_entity(
    source_entity="benunit",
    target_entity="household",
    columns=["universal_credit", "child_benefit"],
    how="sum"
)
```

## Automatic Mapping in Aggregate Classes

The `Aggregate` and `ChangeAggregate` classes automatically handle entity mapping when the variable and target entity don't match:

```python
from policyengine.outputs.aggregate import Aggregate, AggregateType

# income_tax is person-level, but we want household-level sum
total_tax = Aggregate(
    simulation=simulation,
    variable="income_tax",  # Person-level
    entity="household",      # Household-level aggregation
    aggregate_type=AggregateType.SUM,
)
total_tax.run()
# Automatically maps income_tax from person to household using sum()
```

## Common Patterns

### Pattern 1: Compare Baseline vs Reform

```python
# Run both simulations
baseline = Simulation(dataset=dataset, tax_benefit_model_version=uk_latest)
baseline.ensure()

reform = Simulation(
    dataset=dataset,
    tax_benefit_model_version=uk_latest,
    policy=reform_policy
)
reform.ensure()

# Get outputs
baseline_out = baseline.output_dataset.data
reform_out = reform.output_dataset.data

# Calculate differences
baseline_income = baseline_out.household["household_net_income"]
reform_income = reform_out.household["household_net_income"]

difference = reform_income - baseline_income

# Count winners/losers (weighted)
winners = (difference > 0).sum()
losers = (difference < 0).sum()
unchanged = (difference == 0).sum()
```

### Pattern 2: Calculate Custom Derived Variable

```python
# Calculate marginal tax rate at person level
person_data = output.person.copy()
person_data["mtr"] = (
    (person_data["income_tax"] + person_data["national_insurance"])
    / person_data["employment_income"].clip(lower=1)
) * 100

# Map to household level (max MTR in household)
household_mtr = output.map_to_entity(
    source_entity="person",
    target_entity="household",
    values=person_data["mtr"].values,
    how="max"
)
```

### Pattern 3: Extract Subset for Analysis

```python
# Get London households with children
london_hh = output.household[output.household["region"] == "LONDON"]

households_with_children = output.person.groupby("person_household_id")["age"].apply(
    lambda ages: (ages < 18).any()
)

# Combine filters
london_ids = set(london_hh["household_id"])
hh_with_kids_ids = set(households_with_children[households_with_children].index)
target_ids = london_ids & hh_with_kids_ids

# Extract subset
subset_hh = output.household[output.household["household_id"].isin(target_ids)]
subset_persons = output.person[output.person["person_household_id"].isin(target_ids)]
```

### Pattern 4: Reuse Baseline Across Multiple Reforms

```python
# Run baseline once
baseline = Simulation(dataset=dataset, tax_benefit_model_version=uk_latest)
baseline.ensure()
baseline.save()

# Test multiple reforms efficiently
reforms = [reform1, reform2, reform3]
results = {}

for reform in reforms:
    baseline.ensure()  # Instant from cache

    reform_sim = Simulation(
        dataset=dataset,
        tax_benefit_model_version=uk_latest,
        policy=reform
    )
    reform_sim.run()

    # Calculate impact
    from policyengine.outputs.change_aggregate import ChangeAggregate, ChangeAggregateType

    revenue = ChangeAggregate(
        baseline_simulation=baseline,
        reform_simulation=reform_sim,
        variable="household_tax",
        aggregate_type=ChangeAggregateType.SUM,
    )
    revenue.run()

    results[reform.name] = revenue.result
```

## Performance Tips

1. **Use `ensure()` for iterative work**: Can save minutes when re-running analyses
2. **Filter before mapping**: Reduces computation on large datasets
3. **Use `Aggregate` classes**: Optimised implementations for common operations
4. **Batch similar calculations**: Run multiple aggregates in sequence
5. **Cache intermediate results**: Store derived calculations

```python
# Good: Filter then map
high_earners = output.person[output.person["employment_income"] > 100000]
high_earner_hh_income = output.map_to_entity(
    source_entity="person",
    target_entity="household",
    values=high_earners["employment_income"].values,
    how="sum"
)

# Less efficient: Map then filter
all_hh_income = output.map_to_entity(
    source_entity="person",
    target_entity="household",
    columns=["employment_income"],
    how="sum"
)
high_earner_hh = all_hh_income[all_hh_income["employment_income"] > 100000]
```

## For Contributors: Implementation

**Current implementation:**

```bash
# Simulation lifecycle
cat policyengine.py/src/policyengine/core/simulation.py

# Entity mapping logic
cat policyengine.py/src/policyengine/core/dataset.py

# Cache implementation
cat policyengine.py/src/policyengine/core/cache.py
```

**Key patterns:**

1. **Simulation caching**: LRU cache with max 100 entries, keyed by UUID
2. **Entity mapping**: Automatic detection of mapping direction (person→group or group→person)
3. **MicroDataFrame**: All entity data uses weighted DataFrames from microdf package

**Related skills:**
- `policyengine-core-skill` - Understanding simulation engine architecture
- `microdf-skill` - Working with weighted DataFrames
- `policyengine-python-client-skill` - Basic simulation usage

## Debugging Tips

### Verify Simulation Ran

```python
assert simulation.output_dataset is not None, "Simulation hasn't run"

# Check for expected variables
expected = ["household_net_income", "household_tax"]
actual = simulation.output_dataset.data.household.columns
assert all(v in actual for v in expected), "Missing variables"
```

### Check Entity Linkages

```python
# Verify person-household mapping is valid
person_hh_ids = set(output.person["person_household_id"])
household_ids = set(output.household["household_id"])
assert person_hh_ids.issubset(household_ids), "Invalid linkage"
```

### Verify Weights

```python
# Check weights sum correctly
total_persons = output.person["person_weight"].sum()
print(f"Weighted population: {total_persons:,.0f}")

# Check for missing weights
assert not output.person["person_weight"].isna().any(), "Missing weights"
```

## Related Documentation

**In policyengine.py repo:**
- `.claude/policyengine-guide.md` - High-level patterns
- `.claude/quick-reference.md` - Syntax cheat sheet
- `.claude/working-with-simulations.md` - Detailed simulation guide
- `examples/` - Full working examples
- `docs/core-concepts.md` - Architecture documentation
