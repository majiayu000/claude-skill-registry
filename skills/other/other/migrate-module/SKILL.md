---
name: migrate-module
description: Migrate Python modules from SDR_stochastic research code to vrp-toolkit architecture. Use when migrating files from the old codebase structure to the new three-layer architecture (Problem/Algorithm/Data layers), refactoring paper-specific code into generic implementations, or converting research notebooks into educational tutorials.
---

# Migrate Module

Automate the migration of research code modules from the SDR_stochastic project into the reusable vrp-toolkit architecture.

## Migration Resources

**For complete migration guide, see:**
- **[MIGRATION_GUIDE.md](references/MIGRATION_GUIDE.md)** - Comprehensive technical guide
  - Source code locations
  - Complete file mapping (9 files)
  - Migration phases (Phase 1-3)
  - Refactoring guidelines and patterns
  - Common issues and solutions

**Quick references:**
- [migration_map.md](references/migration_map.md) - File mappings only
- [architecture.md](references/architecture.md) - Three-layer architecture

## Migration Workflow

### Step 1: Identify and Plan

1. **Determine the module to migrate**
   - Check [migration_map.md](references/migration_map.md) for file mappings
   - Identify source file in `/SDR_stochastic/new version/`
   - Note the destination path and refactoring requirements

2. **Read and analyze the source code**
   - Read the entire source file
   - Identify dependencies and imports
   - Note any paper-specific hardcoded values
   - Understand the module's purpose and interface

### Step 2: Refactor for Generalization

1. **Extract hardcoded values**
   - Identify magic numbers, file paths, dataset names
   - Convert to function parameters or config objects
   - Common patterns: battery capacity, time windows, location names

   Example transformation:
   ```python
   # Before
   def solve():
       capacity = 100  # Hardcoded

   # After
   def solve(capacity: float = 100):
   ```

2. **Decouple architecture layers**
   - Separate problem definitions from algorithms
   - Extract algorithm-specific code to appropriate layer
   - Follow interfaces in [architecture.md](references/architecture.md)

3. **Generalize data structures**
   - Replace paper-specific types with generic abstractions
   - Ensure compatibility with `Instance`, `Solution`, `Solver` interfaces

### Step 3: Implement in New Location

1. **Create or update the destination file**
   - Place code in the correct layer (Problem/Algorithm/Data)
   - Follow vrp-toolkit directory structure
   - Use appropriate naming conventions (see architecture guide)

2. **Add documentation**
   - Add docstrings to public functions/classes
   - Use Google or NumPy docstring style
   - Include parameters, return values, and examples

   ```python
   def solve_pdptw(instance: PDPTWInstance, config: ALNSConfig) -> Solution:
       """Solve PDPTW using ALNS algorithm.

       Args:
           instance: Problem instance to solve
           config: Algorithm configuration parameters

       Returns:
           Solution object containing routes and objective value
       """
   ```

3. **Update imports**
   - Change import paths to new package structure
   - Use relative imports within vrp_toolkit
   - Update any external dependencies

### Step 4: Create Test Case

Create a simple test to verify functionality:

```python
def test_basic_functionality():
    """Basic smoke test for migrated module"""
    # Create minimal instance
    instance = create_test_instance()

    # Run migrated function
    result = migrated_function(instance)

    # Verify basic properties
    assert result is not None
    assert result.is_feasible()
```

### Step 5: Verify Migration

1. **Check imports resolve correctly**
   - Try importing the new module
   - Verify no circular dependencies

2. **Run the test case**
   - Ensure basic functionality works
   - Compare behavior with original code if needed

3. **Verify architectural compliance**
   - Check layer separation (no Problem code in Algorithm layer, etc.)
   - Ensure following the Solver/Instance/Solution interfaces

## Special Cases

### Migrating Jupyter Notebooks
When migrating `.ipynb` files to tutorials:

1. **Clean up for educational clarity**
   - Add markdown explanations between code cells
   - Remove debugging/experimental code
   - Structure: Problem → Setup → Solve → Visualize → Interpret

2. **Ensure reproducibility**
   - Keep examples runnable in <30 seconds
   - Use small test instances
   - Include all necessary imports

3. **Follow tutorial naming convention**
   - Format: `0X_descriptive_name.ipynb`
   - Update README with tutorial description

### Merging Multiple Files
When multiple source files map to one destination (e.g., `order_info.py` + `demands.py` → `generators.py`):

1. Identify common functionality
2. Create unified interface
3. Preserve all unique features from each source
4. Organize as separate classes or functions within the same module

## Key References

- **File mappings:** See [migration_map.md](references/migration_map.md)
- **Architecture patterns:** See [architecture.md](references/architecture.md)
- **Project guidelines:** See `CLAUDE.md` in project root

## Design Principles

- ✅ Minimal viable clarity over perfection
- ✅ Generalize from specific to reusable
- ✅ Decouple layers cleanly
- ❌ No over-engineering before 2+ use cases
- ❌ No documentation before code works
