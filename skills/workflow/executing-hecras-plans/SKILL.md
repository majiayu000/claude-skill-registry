---
name: executing-hecras-plans
description: |
  Executes HEC-RAS plans using RasCmdr.compute_plan(), handles parallel
  execution across multiple plans, manages destination folders, and monitors
  real-time progress with callbacks. Use when running HEC-RAS simulations,
  computing plans, executing models, parallel workflows, setting up
  distributed computation, batch processing, scenario analysis, or monitoring
  execution progress in real-time.
  Triggers: execute, run, compute, HEC-RAS, plan, simulation, parallel, callback, batch, scenario, destination folder, worker, monitoring, progress, real-time.
---

# Executing HEC-RAS Plans

This skill helps you execute HEC-RAS plans using ras-commander. It serves as a navigator to primary sources containing comprehensive documentation and working examples.

## Primary Sources

### 1. Execution Patterns (CLAUDE.md)
**Location**: `C:\GH\ras-commander\ras_commander\CLAUDE.md`

**See sections**:
- **"Plan Execution"** - Core execution methods and parameters
- **"Execution Modes"** - Four modes: single, parallel, sequential, remote
- **"Plan Execution Parameters"** - Complete parameter reference
- **"Common Workflow Pattern"** - Initialize → Execute → Extract

**Key execution modes**:
```python
# Single plan
RasCmdr.compute_plan("01", dest_folder="run1", num_cores=4)

# Parallel local
RasCmdr.compute_parallel(["01", "02", "03"], max_workers=3)

# Sequential test
RasCmdr.compute_test_mode(["01", "02"])
```

### 2. Working Examples (Jupyter Notebooks)

**Core execution notebooks**:
- `examples/110_single_plan_execution.ipynb` - Complete single plan workflow
- `examples/111_executing_plan_sets.ipynb` - Plan sets and batch processing
- `examples/112_sequential_plan_execution.ipynb` - Test mode execution
- `examples/113_parallel_execution.ipynb` - Parallel execution with performance analysis

**Advanced workflows**:
- `examples/500_remote_execution_psexec.ipynb` - Distributed execution
- Real-time monitoring examples (search for `stream_callback` usage)

### 3. Code Documentation (Docstrings)

**Location**: `C:\GH\ras-commander\ras_commander\RasCmdr.py`

**Read docstrings for**:
- `RasCmdr.compute_plan()` - Lines 139-250+ (comprehensive parameter docs)
- `RasCmdr.compute_parallel()` - Parallel execution details
- `RasCmdr.compute_test_mode()` - Sequential debugging mode

**Callback protocol**: `C:\GH\ras-commander\ras_commander\callbacks.py`
- `ExecutionCallback` - Protocol definition
- `ConsoleCallback`, `FileLoggerCallback`, `ProgressBarCallback` - Implementations

## Quick Reference

### Single Plan Execution

**Basic pattern**:
```python
from ras_commander import init_ras_project, RasCmdr

# Initialize
init_ras_project(r"C:\Models\MyProject", "6.6")

# Execute
RasCmdr.compute_plan("01")
```

**With destination folder** (preserves original):
```python
RasCmdr.compute_plan("01", dest_folder="computation_folder")
```

**With monitoring**:
```python
from ras_commander.callbacks import ConsoleCallback

RasCmdr.compute_plan(
    "01",
    stream_callback=ConsoleCallback(verbose=True)
)
```

**Key parameters**:
- `plan_number` - "01", "02", etc. (use strings)
- `dest_folder` - None = in-place, path = separate folder
- `num_cores` - CPU cores to use (None = plan default)
- `clear_geompre` - True after geometry changes
- `verify` - True to check completion
- `skip_existing` - True to resume interrupted runs
- `stream_callback` - Real-time monitoring object

### Parallel Execution

**Execute multiple plans**:
```python
# All plans with 3 workers
RasCmdr.compute_parallel(max_workers=3, num_cores=2)

# Specific plans
RasCmdr.compute_parallel(
    plans_to_run=["01", "02", "03"],
    max_workers=3,
    num_cores=2
)
```

**Worker allocation**:
- `max_workers` - Parallel plan executions
- `num_cores` - Cores per plan
- Total cores used = `max_workers × num_cores`
- Optimal: 2-4 cores per worker, workers ≤ physical cores / num_cores

### Sequential Test Mode

**For debugging**:
```python
# Run plans one at a time in test folder
RasCmdr.compute_test_mode(["01", "02", "03"])
```

**Difference from parallel**:
- ONE plan at a time (not simultaneous)
- Single test folder (not multiple workers)
- Easier to debug issues

## Mode Selection Guide

Use this decision matrix to select the appropriate execution mode:

| Scenario | Recommended Mode | Rationale |
|----------|------------------|-----------|
| Single plan, need full control | `compute_plan()` | Direct control, callback monitoring, parameter tuning |
| Single plan, quick run | `compute_plan()` | Simplest API, minimal overhead |
| Multiple plans, debugging issues | `compute_test_mode()` | Sequential execution, single folder, easier diagnosis |
| Multiple plans, production runs | `compute_parallel()` | Fastest throughput, worker isolation, parallel HDF writes |
| Distributed across machines | `compute_parallel_remote()` | Scale-out to multiple computers |
| HEC-RAS 3.x-5.x legacy | `RasControl` | COM-based automation (see rascontrol documentation) |
| Resume interrupted batch | `compute_parallel(..., skip_existing=True)` | Skips completed plans |
| Scenario comparison study | `compute_parallel()` with dest_folder | Each scenario in separate folder |

**Quick Decision Tree**:
1. **How many plans?** Single → `compute_plan()`, Multiple → continue
2. **Debugging?** Yes → `compute_test_mode()`, No → continue
3. **Multiple machines?** Yes → `compute_parallel_remote()`, No → `compute_parallel()`

**See**: `.claude/rules/hec-ras/execution.md` for complete mode documentation.

## Orchestrator Integration

### Workflow: Inspector → Execute → Analyze

For complex projects, chain execution with inspection and analysis:

```
1. Project Inspector → Understand project structure
2. Mode Selection   → Choose execution approach
3. Execute          → Run plans
4. Results Analyst  → Interpret outputs
```

### Integration with Project Inspector

**Before executing unfamiliar projects**, gather intelligence:

```python
# Step 1: Inspect project (via hecras-project-inspector agent or manual)
# - Get plan count and types
# - Identify dependencies between plans
# - Check geometry complexity (1D vs 2D vs mixed)
# - Review execution recommendations

# Step 2: Based on inspection, select mode
# Example: Inspector finds 5 independent 2D plans
plans = ["01", "02", "03", "04", "05"]
mode = "compute_parallel"  # Independent plans → parallel

# Step 3: Execute with appropriate parameters
RasCmdr.compute_parallel(
    plans_to_run=plans,
    max_workers=3,      # Based on system resources
    num_cores=4,        # 2D models benefit from multiple cores
    verify=True
)

# Step 4: Dispatch to results analysis
# - Extract WSE, velocity, depth from HDF files
# - Generate comparison plots
# - Create summary report
```

### Chaining with Other Skills

**Execution typically follows these upstream skills**:
- `parsing-hecras-geometry` → After geometry modifications
- `reading-dss-boundary-data` → After validating boundary conditions
- `integrating-usgs-gauges` → After setting up gauge-based boundaries

**Execution typically precedes these downstream skills**:
- `extracting-hecras-results` → Parse HDF outputs
- Results visualization → Generate plots and maps
- Validation workflows → Compare to observed data

### Multi-Project Orchestration

For workflows spanning multiple HEC-RAS projects:

```python
from ras_commander import RasPrj, init_ras_project, RasCmdr

# Create separate project contexts
projects = {}
for project_name in ["upstream", "downstream", "tributary"]:
    projects[project_name] = RasPrj()
    init_ras_project(
        f"C:/Models/{project_name}",
        "6.6",
        ras_object=projects[project_name]
    )

# Execute in dependency order
RasCmdr.compute_plan("01", ras_object=projects["upstream"])
RasCmdr.compute_plan("01", ras_object=projects["tributary"])
RasCmdr.compute_plan("01", ras_object=projects["downstream"])
```

**Critical**: Pass `ras_object` when working with multiple projects. See `.claude/rules/python/ras-commander-patterns.md` for context object discipline.

## Common Patterns

### Pattern: Preserve Original Project
```python
# Run in separate folder, leave original untouched
RasCmdr.compute_plan(
    "01",
    dest_folder="results/run_2024_12_11",
    overwrite_dest=True,
    verify=True
)
```

### Pattern: Geometry Modification Workflow
```python
from ras_commander.RasGeo import RasGeo

# Modify geometry
RasGeo.update_mannings_n(geom_file="g01", landcover_map={...})

# Run with forced reprocessing
RasCmdr.compute_plan("01", clear_geompre=True)  # CRITICAL
```

### Pattern: Batch Scenario Processing
```python
scenarios = {
    "baseline": {"plan": "01", "dest": "output/baseline"},
    "mitigation": {"plan": "02", "dest": "output/mitigation"},
}

for name, config in scenarios.items():
    RasCmdr.compute_plan(
        config["plan"],
        dest_folder=config["dest"],
        verify=True
    )
```

### Pattern: Skip Already Completed
```python
# Resume interrupted batch run
for plan in ["01", "02", "03"]:
    RasCmdr.compute_plan(
        plan,
        skip_existing=True,  # Skip if already complete
        verify=True
    )
```

## Real-Time Monitoring

### Console Output
```python
from ras_commander.callbacks import ConsoleCallback

callback = ConsoleCallback(verbose=True)
RasCmdr.compute_plan("01", stream_callback=callback)
```

**Output example**:
```
[Plan 01] Starting execution...
[Plan 01] Geometry Preprocessor Version 6.6
[Plan 01] Computing Plan: 01
[Plan 01] SUCCESS in 45.2s
```

### File Logging
```python
from ras_commander.callbacks import FileLoggerCallback
from pathlib import Path

callback = FileLoggerCallback(output_dir=Path("logs"))
RasCmdr.compute_plan("01", stream_callback=callback)
# Creates: logs/plan_01_execution.log
```

### Progress Bar
```python
from ras_commander.callbacks import ProgressBarCallback

# Requires: pip install tqdm
callback = ProgressBarCallback()
RasCmdr.compute_plan("01", stream_callback=callback)
```

### Custom Callback
```python
from ras_commander.callbacks import ExecutionCallback

class AlertCallback(ExecutionCallback):
    def on_exec_complete(self, plan_number: str, success: bool, duration: float):
        send_email(subject=f"Plan {plan_number} {'SUCCESS' if success else 'FAILED'}")

RasCmdr.compute_plan("01", stream_callback=AlertCallback())
```

**Available callback methods** (all optional):
- `on_prep_start()` - Before geometry preprocessing
- `on_prep_complete()` - After preprocessing
- `on_exec_start()` - HEC-RAS subprocess starts
- `on_exec_message()` - Each .bco file message (real-time)
- `on_exec_complete()` - Execution finishes
- `on_verify_result()` - After verification (if verify=True)

**Thread safety**: Use `SynchronizedCallback` wrapper for parallel execution

## Verification

### Return Value Check
```python
success = RasCmdr.compute_plan("01", verify=True)
if not success:
    print("Execution failed or incomplete")
```

### Parse Compute Messages
```python
from ras_commander.hdf import HdfResultsPlan

messages = HdfResultsPlan.get_compute_messages("01")
if "Complete Process" in messages:
    print("Success!")
```

### Validate Results
```python
wse = HdfResultsPlan.get_wse("01", time_index=-1)
if wse is not None:
    print(f"WSE range: {wse.min():.2f} to {wse.max():.2f} ft")
```

## Performance Optimization

| Setting | Recommendation | When |
|---------|---------------|------|
| `clear_geompre=False` | 2x-10x faster | Geometry unchanged |
| `clear_geompre=True` | Required | After ANY geometry edit |
| `num_cores=2-4` | Best balance | Most models |
| `num_cores=1-2` | Highest efficiency | Resource-limited |

**See**: `.claude/rules/hec-ras/execution.md` for detailed performance guidance.

## Troubleshooting

**Plan doesn't execute** - Check: `init_ras_project()` called? Plan in `ras.plan_df`? HEC-RAS installed? Write permissions?

**HDF not created** - Enable `ConsoleCallback(verbose=True)`, check compute messages, try HEC-RAS GUI manually.

**Debug command**:
```python
from ras_commander import ras
print(f"Project: {ras.project_folder}")
print(f"RAS: {ras.ras_exe_path}")
print(ras.plan_df)
```

---

**Remember**: This skill is a navigator. For detailed documentation, comprehensive examples, and complete API reference, always consult the Primary Sources section above.
