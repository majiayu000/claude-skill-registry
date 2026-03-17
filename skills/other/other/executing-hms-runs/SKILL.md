---
name: executing-hms-runs
description: |
  Executes HEC-HMS simulations using HmsCmdr.compute_run(), handles parallel
  execution across multiple runs, and manages Jython script generation. Use when
  running HMS simulations, executing runs, computing models, or setting up parallel
  computation workflows. Handles HMS 3.x and 4.x version differences, Python 2/3
  compatibility, destination folder management, and multi-run coordination.
  Trigger keywords: run simulation, execute HMS, compute run, parallel execution,
  batch runs, Jython script, HMS 3.x, HMS 4.x, Python 2 compatible.
---

# Executing HEC-HMS Runs

## Quick Start

```python
from hms_commander import init_hms_project, HmsCmdr

# Initialize project
init_hms_project(r"C:\Projects\watershed")

# Execute single run
HmsCmdr.compute_run("Run 1")

# Execute multiple runs in parallel
HmsCmdr.compute_parallel(["Run 1", "Run 2", "Run 3"], max_workers=2)
```

## Primary Sources

**Code (Authoritative API)**:
- `hms_commander/HmsCmdr.py` - Execution engine with complete docstrings
- `hms_commander/HmsJython.py` - Script generation and version detection

**Examples (Working Demonstrations)**:
- `examples/01_multi_version_execution.ipynb` - Complete workflow
- `examples/04_hms_workflow.ipynb` - End-to-end simulation

**Rules (Patterns & Decisions)**:
- `.claude/rules/hec-hms/execution.md` - Execution patterns
- `.claude/rules/hec-hms/version-support.md` - HMS 3.x vs 4.x differences

## When to Use This Skill

**Trigger Scenarios**:
- User says "run HMS simulation"
- User says "execute this model"
- User says "compute all runs in parallel"
- User mentions "Jython script"
- Working with HMS 3.x (requires Python 2 compatibility)
- Need to execute batch simulations
- Setting up automated workflows

## Core Capabilities

### 1. Single Run Execution

**Pattern**: Initialize → Compute → Verify

See `reference/compute_run.md` for complete API details.

**Key Decision**: When to use `compute_run()` vs `compute_test_mode()`
- Use `compute_run()` for actual simulation
- Use `compute_test_mode()` to validate setup without running

### 2. Parallel Execution

**Pattern**: Batch runs across multiple workers

See `reference/parallel.md` for parallel execution strategies.

**Key Decision**: How many workers?
- Default: 2 workers (safe for most systems)
- CPU-bound: Use `os.cpu_count() - 1`
- Memory-constrained: Use 1 worker (sequential)
- Large models: Consider memory per run × workers

### 3. Jython Script Generation

**Pattern**: Generate version-appropriate script → Execute via HMS

See `reference/jython.md` for script generation details.

**Critical Decision**: HMS 3.x vs 4.x
- HMS 3.x: MUST use `python2_compatible=True`
- HMS 4.x: Use default (Python 3 syntax)
- Auto-detection: Check install path contains "(x86)" = 3.x

## HMS Version Awareness

**This skill handles BOTH HMS 3.x and 4.x**:

| Aspect | HMS 3.x | HMS 4.x |
|--------|---------|---------|
| Architecture | 32-bit | 64-bit |
| Python Syntax | Python 2 (`print "x"`) | Python 3 (`print("x")`) |
| Script Flag | `python2_compatible=True` | Default |
| Max Memory | ~1.3 GB | 32+ GB |
| Install Path | `Program Files (x86)` | `Program Files` |

**See**: `.claude/rules/hec-hms/version-support.md` for complete differences

## Common Workflows

### Workflow 1: Basic Execution

```python
from hms_commander import init_hms_project, HmsCmdr

init_hms_project(r"C:\Projects\watershed")
HmsCmdr.compute_run("Run 1")
```

**See**: `examples/basic-run.md` for complete walkthrough

### Workflow 2: Batch Execution (Sequential)

```python
runs = ["Baseline", "Alternative_1", "Alternative_2"]
HmsCmdr.compute_batch(runs)
```

**See**: `examples/batch-runs.md` for batch strategies

### Workflow 3: Parallel Execution

```python
runs = ["Run_1", "Run_2", "Run_3", "Run_4"]
HmsCmdr.compute_parallel(runs, max_workers=2)
```

**See**: `reference/parallel.md` for worker allocation

### Workflow 4: Legacy HMS 3.x Project

```python
from hms_commander import HmsJython

# Generate Python 2 compatible script
script = HmsJython.generate_compute_script(
    project_path=r"C:\Projects\old_project",
    run_name="Run 1",
    python2_compatible=True  # CRITICAL for HMS 3.x!
)

# Execute with HMS 3.x
success, stdout, stderr = HmsJython.execute_script(
    script_content=script,
    hms_exe_path=r"C:\Program Files (x86)\HEC\HEC-HMS\3.5"
)
```

**See**: `.claude/rules/hec-hms/version-support.md` for legacy workflows

## Troubleshooting

**Common Issues**:

1. **HMS Not Found**: See `reference/jython.md#finding-hms`
2. **Memory Errors**: See `reference/jython.md#memory-allocation`
3. **Python 2 Syntax Errors**: See `.claude/rules/hec-hms/version-support.md`
4. **Parallel Execution Hangs**: See `reference/parallel.md#debugging`

## Integration Points

**Before Execution**:
- Use `HmsBasin` to modify parameters (see `parsing-basin-models` skill)
- Use `HmsMet` to update precipitation (see `updating-met-models` skill)
- Use `HmsControl` to set time window (see `.claude/rules/hec-hms/control-files.md`)

**After Execution**:
- Use `HmsDss` to extract results (see `extracting-dss-results` skill)
- Use `HmsResults` for analysis (see `.claude/rules/hec-hms/dss-operations.md`)

## Reference Files

**Detailed API Documentation** (load on-demand):
- `reference/compute_run.md` - HmsCmdr.compute_run() complete API
- `reference/parallel.md` - Parallel execution strategies
- `reference/jython.md` - Script generation and execution
- `reference/troubleshooting.md` - Common issues and solutions

**Complete Examples** (working code):
- `examples/basic-run.md` - Simple single run
- `examples/batch-runs.md` - Sequential batch execution
- `examples/parallel-runs.md` - Parallel execution with worker allocation
- `examples/legacy-3x.md` - HMS 3.x compatibility

## Testing This Skill

Use real HMS projects for testing:

```python
from hms_commander import HmsExamples

# Extract example project
HmsExamples.extract_project("tifton")

# Test execution
init_hms_project("tifton/tifton")
HmsCmdr.compute_run("1970_simulation")
```

**See**: `.claude/rules/testing/tdd-approach.md` for testing philosophy

## Key Patterns (Not in Primary Sources)

### Pattern 1: Destination Folder Management

HMS creates output in the project folder. For organized results:

```python
# Results go to project_folder/results/RUN_<run_name>.results
# DSS file location specified in .run file
```

**Decision**: HMS writes to project folder, not a separate destination folder like RAS.

### Pattern 2: Version Auto-Detection

```python
from pathlib import Path

hms_path = Path(r"C:\Program Files (x86)\HEC\HEC-HMS\3.5")
is_3x = "(x86)" in str(hms_path)  # 32-bit = HMS 3.x
python2_compatible = is_3x
```

**Decision**: Use install path pattern for version detection, not HMS version file.

### Pattern 3: Error Handling

```python
try:
    HmsCmdr.compute_run("Run 1")
except Exception as e:
    # Check HMS log file for details
    log_file = hms.project_folder / f"RUN_Run 1.log"
    if log_file.exists():
        print(log_file.read_text())
    raise
```

**Decision**: HMS errors appear in log files, check those for diagnostics.

## Related Skills

- **parsing-basin-models** - Modify parameters before execution
- **updating-met-models** - Update precipitation before execution
- **extracting-dss-results** - Process outputs after execution
- **cloning-hms-components** - Create QAQC comparison runs
- **managing-hms-versions** - Multi-version testing workflows

---

**Navigation**: This skill points to primary sources. For complete API details, read the code docstrings in `hms_commander/HmsCmdr.py` and `hms_commander/HmsJython.py`.
