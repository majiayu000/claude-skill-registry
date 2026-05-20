---
name: integrate-playground
description: Systematic workflow and API reference for integrating Streamlit playground with vrp-toolkit modules. Use when developing playground features, connecting UI to vrp-toolkit APIs, or encountering API signature mismatches. Provides interface mapping table, contract test integration, and troubleshooting guide to avoid token-intensive source code exploration.
---

# Integrate Playground with VRP-Toolkit

Token-efficient workflow for connecting Streamlit playground UI to vrp-toolkit backend APIs.

## Core Problem

Developing playground features requires knowing exact API signatures of vrp-toolkit modules. Without reference documentation, this requires repeatedly reading source code (consuming thousands of tokens per integration) and leads to API mismatch errors.

## Solution

This skill provides:
1. **Interface Mapping Table** - Playground needs → vrp-toolkit APIs
2. **API Quick Reference** - Exact signatures with usage examples
3. **Contract Test Integration** - Automated verification of interfaces
4. **Common Error Patterns** - Troubleshooting guide

## Workflow

### Step 1: Check Interface Mapping

**Before writing any integration code:**

1. Open [interface_mapping.md](references/interface_mapping.md)
2. Find the workflow you're implementing (e.g., "Generate synthetic map")
3. Note the exact API signature
4. Check for common mistakes marked with ⚠️

**Example:**
```markdown
Need: Generate synthetic map
API: RealMap(n_r: int, n_c: int, dist_function: Callable, dist_params: Dict)
Common mistake: ❌ Don't use num_customers, use n_c
```

### Step 2: Verify with Contract Test (Optional)

**If uncertain about API behavior:**

1. Check if contract test exists in `contracts/` directory
2. Run the test: `pytest contracts/test_<feature>.py -v`
3. Read test code to see usage examples
4. Test validates: parameters accepted, attributes available, reproducibility

**Example:**
```bash
pytest contracts/test_realmap_api.py -v
# See test_realmap_initialization() for usage example
```

### Step 3: Write Integration Code

**Follow the mapping table exactly:**

```python
# ✅ Correct: Use exact signature from mapping table
np.random.seed(seed)  # For reproducibility
real_map = RealMap(
    n_r=num_restaurants,
    n_c=num_customers,
    dist_function=np.random.uniform,
    dist_params={'low': 0, 'high': 100}
)

# ❌ Wrong: Assumed API
real_map = RealMap(
    num_customers=num_customers,
    num_restaurants=num_restaurants,
    area_size=100,
    seed=seed
)
```

**Data access pattern:**
- Most generators create data in `__init__`, not via `.generate()` method
- Access via attributes: `.demand_table`, `.order_table`, `.time_matrix`
- See [interface_mapping.md](references/interface_mapping.md) for each API's pattern

### Step 4: Add Error Handling

**Common error patterns:**

```python
try:
    instance = PDPTWInstance(
        order_table=order_table,
        distance_matrix=real_map.distance_matrix,
        time_matrix=order_gen.time_matrix,
        robot_speed=1.0
    )
except TypeError as e:
    st.error(f"API mismatch: {e}")
    st.info("Check interface_mapping.md for correct parameters")
```

### Step 5: Add Contract Test (For New Integrations)

**When adding new playground feature:**

1. Create test in `contracts/test_<feature>.py`
2. Test should verify:
   - API signature matches mapping table
   - Reproducibility (same seed → same result)
   - Feasibility (results meet constraints)
   - Objective values are consistent

3. Add test reference to [interface_mapping.md](references/interface_mapping.md)

**Template:**
```python
# contracts/test_new_feature.py
def test_api_signature():
    """Verifies API matches interface_mapping.md"""
    # Test exact parameters...

def test_reproducibility():
    """Same seed produces same result"""
    np.random.seed(42)
    result1 = generate_feature()

    np.random.seed(42)
    result2 = generate_feature()

    assert result1 == result2
```

## Quick Reference Files

### For Complete API Details
See [api_signatures.md](references/api_signatures.md) for:
- Full parameter lists with types
- Return types and attributes
- Usage examples
- Import statements

### For Contract Testing
See [contract_tests.md](references/contract_tests.md) for:
- How to write contract tests
- Test organization patterns
- Running and maintaining tests
- Linking tests to mapping table

### For Troubleshooting
See [troubleshooting.md](references/troubleshooting.md) for:
- Common error messages and fixes
- Module caching issues (need to restart Streamlit)
- Attribute vs method access patterns
- Missing parameter errors

## Anti-Patterns to Avoid

❌ **Don't assume API signatures**
- Always check mapping table first
- Don't guess parameter names

❌ **Don't repeatedly read source code**
- Use this skill's mapping table (< 1000 tokens)
- Avoid re-reading vrp-toolkit source (several thousand tokens each time)

❌ **Don't call non-existent methods**
- Check if it's an attribute or method
- Most generators use attributes: `.demand_table`, not `.generate()`

❌ **Don't skip contract tests for complex integrations**
- Tests catch issues early
- Tests document expected behavior
- Tests prevent regressions

## Maintenance

**When vrp-toolkit API changes:**
1. Update [interface_mapping.md](references/interface_mapping.md)
2. Update affected contract tests in `contracts/`
3. Run tests to verify: `pytest contracts/ -v`
4. Update playground code
5. Update [troubleshooting.md](references/troubleshooting.md) if new error patterns emerge

**When adding new playground features:**
1. Add API to [interface_mapping.md](references/interface_mapping.md)
2. Add detailed signature to [api_signatures.md](references/api_signatures.md)
3. Create contract test in `contracts/`
4. Reference test in mapping table

## Token Efficiency

**Without this skill:**
- Read RealMap source: ~1500 tokens
- Read DemandGenerator source: ~1200 tokens
- Read OrderGenerator source: ~1800 tokens
- Read PDPTWInstance source: ~2000 tokens
- **Total: ~6500 tokens per integration**

**With this skill:**
- Read interface_mapping.md: ~800 tokens
- **Total: ~800 tokens per integration**

**Savings: ~5700 tokens (87% reduction)**
