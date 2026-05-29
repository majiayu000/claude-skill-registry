---
name: hecras_compute_rascontrol
description: |
  Executes HEC-RAS plans using RasControl class via HECRASController COM interface
  for legacy HEC-RAS versions (3.x-5.x). Handles COM lifecycle management, session
  tracking, orphan cleanup, steady/unsteady result extraction, and watchdog
  protection for Jupyter notebooks. Use when automating legacy HEC-RAS, extracting
  results from older versions, comparing across HEC-RAS versions, or needing
  COM-based automation that RasCmdr cannot provide.
  Triggers: RasControl, HECRASController, COM, legacy, HEC-RAS 4, HEC-RAS 5,
  win32com, steady results, unsteady results, version comparison, COM interface,
  legacy automation, 3.x, 4.x, 5.x, orphan cleanup, watchdog, session tracking.
---

# Executing HEC-RAS Plans via RasControl (COM Interface)

This skill helps you automate HEC-RAS versions 3.x-5.x using the RasControl class, which wraps the HECRASController COM interface with ras-commander conventions.

## Primary Sources

### 1. RasControl Implementation
**Location**: `ras_commander/RasControl.py`

**Key sections**:
- Lines 438-527: `RasControl` class with version mapping and output variable codes
- Lines 543-742: COM lifecycle management (`_com_open_close()`)
- Lines 746-884: `run_plan()` with smart skip and watchdog protection
- Lines 936-1177: `get_steady_results()` - extract steady state profiles
- Lines 1179-1458: `get_unsteady_results()` - extract time series with Max WS
- Lines 1647-1909: Process management API (orphan cleanup)

### 2. Working Examples (Jupyter Notebooks)
- `examples/120_automating_ras_with_win32com.ipynb` - Low-level win32com exploration
- `examples/121_legacy_hecrascontroller_and_rascontrol.ipynb` - Complete RasControl workflows

### 3. Related Documentation
- `.claude/rules/hec-ras/execution.md` - Execution mode comparison
- `ras_commander/CLAUDE.md` - Library context and module organization

## When to Use RasControl vs RasCmdr

| Scenario | Use RasControl | Use RasCmdr |
|----------|---------------|-------------|
| HEC-RAS 3.x-5.x | Yes | No |
| HEC-RAS 6.x+ | No (use COM only if needed) | Yes (preferred) |
| Need GUI interaction | Yes (COM opens GUI) | No (headless) |
| Version comparison | Yes | Yes |
| Production workflows | Limited | Preferred |
| Parallel execution | No (single-threaded) | Yes |

## Quick Reference

### Basic Workflow

```python
from ras_commander import init_ras_project, RasControl

# Initialize project with version
init_ras_project(project_path, "5.0.6")  # Or "506", "4.1", "41", etc.

# Run plan (checks if current, skips if up-to-date)
success, msgs = RasControl.run_plan("02")

# Force recomputation
success, msgs = RasControl.run_plan("02", force_recompute=True)

# Extract steady state results
df_steady = RasControl.get_steady_results("02")

# Extract unsteady time series (includes Max WS row)
df_unsteady = RasControl.get_unsteady_results("01")
```

### Version Format Support

RasControl accepts flexible version formats:

```python
# All equivalent - HEC-RAS 4.1
init_ras_project(path, "4.1")
init_ras_project(path, "41")

# All equivalent - HEC-RAS 5.0.6
init_ras_project(path, "5.0.6")
init_ras_project(path, "506")

# All equivalent - HEC-RAS 6.6
init_ras_project(path, "6.6")
init_ras_project(path, "66")
```

**Supported versions**: 3.0-3.1.3, 4.0-4.1, 5.0-5.0.7, 6.0-6.7

### Separating Max WS from Time Series

```python
# Max WS contains computational maximums (critical for design!)
df_maxws = df_unsteady[df_unsteady['time_string'] == 'Max WS']
df_timeseries = df_unsteady[df_unsteady['datetime'].notna()]

# Plot time series with Max WS reference line
import matplotlib.pyplot as plt
xs_data = df_timeseries[df_timeseries['node_id'] == '10000']
plt.plot(xs_data['datetime'], xs_data['wsel'])
plt.axhline(df_maxws[df_maxws['node_id'] == '10000']['wsel'].iloc[0],
            color='r', linestyle='--', label='Max WS')
```

## COM Lifecycle Management

### Critical Pattern: Open-Operate-Close

RasControl handles COM lifecycle automatically via `_com_open_close()`:

```python
# Internal pattern (you don't call this directly)
# 1. Create COM object: win32com.client.Dispatch("RAS66.HECRASController")
# 2. Open project: com_rc.Project_Open(project_path)
# 3. Create session lock for crash recovery
# 4. Execute operation
# 5. Close HEC-RAS: com_rc.QuitRas()
# 6. Clean up session tracking
```

**Why this matters**:
- COM objects MUST be released properly
- Orphaned ras.exe processes consume resources
- Session tracking enables recovery after crashes

### Session Tracking Infrastructure

RasControl tracks all active COM sessions:

```python
# List tracked processes
df = RasControl.list_processes()
print(df)  # Shows PID, tracked status, project, age

# List all ras.exe (including untracked)
df_all = RasControl.list_processes(show_all=True)
```

### Orphan Detection and Cleanup

After crashes or Jupyter kernel restarts:

```python
# Scan for orphaned processes
orphans = RasControl.scan_orphans()
if orphans:
    print(f"Found {len(orphans)} orphaned processes")

# Interactive cleanup (prompts for confirmation)
RasControl.cleanup_orphans()

# Automatic cleanup (no prompts)
count = RasControl.cleanup_orphans(interactive=False)

# Dry run (see what would be cleaned)
RasControl.cleanup_orphans(dry_run=True)

# Nuclear option - kill ALL ras.exe (requires "YES" confirmation)
RasControl.force_cleanup_all()
```

### Watchdog Protection

For long-running operations in Jupyter:

```python
# With watchdog (default) - survives kernel restarts
success, msgs = RasControl.run_plan("01", use_watchdog=True, max_runtime=3600)

# Without watchdog (not recommended in Jupyter)
success, msgs = RasControl.run_plan("01", use_watchdog=False)
```

**Watchdog features**:
- Independent Python process monitors parent
- Terminates ras.exe if Python crashes
- Enforces max_runtime timeout
- Responds to manual lock file deletion

## Result Extraction

### Steady State Results

```python
df = RasControl.get_steady_results("02")

# DataFrame columns:
# - river, reach, node_id (location)
# - profile (profile name)
# - wsel (water surface elevation)
# - velocity, flow, froude, energy, max_depth, min_ch_el
```

### Unsteady Results with Datetime

```python
df = RasControl.get_unsteady_results("01")

# DataFrame columns:
# - river, reach, node_id (location)
# - time_index (1 = Max WS, 2+ = timesteps)
# - time_string ("Max WS" or "18FEB1999 0000")
# - datetime (datetime64[ns], NaT for Max WS)
# - wsel, velocity, flow, froude, energy, max_depth, min_ch_el
```

### Computation Messages

```python
# Read computation messages (tries .txt then HDF)
msgs = RasControl.get_comp_msgs("01")
print(msgs)
```

## Common Patterns

### Pattern: Version Comparison

```python
from ras_commander import RasPlan

versions = [("5.0.6", "506"), ("6.3.1", "631"), ("6.6", "66")]
results = {}

for version_name, version_code in versions:
    # Clone plan for this version
    new_plan = RasPlan.clone_plan("01", new_shortid=f"v{version_code}")

    # Run with this version
    init_ras_project(project_path, version_name)
    RasControl.run_plan(new_plan, force_recompute=True)

    # Extract results
    results[version_name] = RasControl.get_unsteady_results(new_plan)

# Compare across versions
for version, df in results.items():
    max_wse = df[df['time_string'] == 'Max WS']['wsel'].max()
    print(f"v{version}: Max WSE = {max_wse:.2f} ft")
```

### Pattern: Error Recovery

```python
try:
    success, msgs = RasControl.run_plan("01")
except Exception as e:
    print(f"COM error: {e}")

    # Clean up any orphaned processes
    RasControl.cleanup_orphans(interactive=False)

    # Read computation messages for diagnosis
    comp_msgs = RasControl.get_comp_msgs("01")
    print(f"Computation messages:\n{comp_msgs}")
```

### Pattern: Extract Before Running

```python
# Check if results are current before running
success, msgs = RasControl.run_plan("01")

if "Results are current" in msgs[0]:
    print("Skipped - results already up-to-date")
else:
    print("Plan executed")

# Extract results (works whether run or skipped)
df = RasControl.get_unsteady_results("01")
```

## Troubleshooting

### COM Object Not Found

```python
# Error: "COM object not found" or "Class not registered"

# Verify HEC-RAS COM registration
import win32com.client
try:
    rc = win32com.client.Dispatch("RAS66.HECRASController")
    print("COM registered correctly")
except Exception as e:
    print(f"COM issue: {e}")
    print("Solution: Reinstall HEC-RAS or run as Administrator")
```

### HEC-RAS Freezes or Hangs

```python
# Check for orphaned processes
RasControl.list_processes(show_all=True)

# Clean up orphans
RasControl.cleanup_orphans()

# If still stuck, nuclear option (kills ALL ras.exe)
RasControl.force_cleanup_all()
```

### Results Extraction Fails

```python
# If get_steady_results() or get_unsteady_results() fails:

# 1. Check if plan was executed
success, msgs = RasControl.run_plan("01", force_recompute=True)

# 2. Check computation messages
comp_msgs = RasControl.get_comp_msgs("01")
print(comp_msgs)

# 3. Look for "error" or "warning" in messages
if "error" in comp_msgs.lower():
    print("Computation had errors - fix model issues")
```

### Version Mismatch

```python
# Error: Version 'X.Y' not supported

# Check supported versions
print(RasControl.VERSION_MAP.keys())

# Use normalized format
init_ras_project(path, "5.0.6")  # Not "5.06" or "5.6"
```

## Performance Considerations

### COM is Single-Threaded

- RasControl cannot run plans in parallel
- Each operation opens/closes HEC-RAS GUI
- For parallel execution, use RasCmdr with HEC-RAS 6.x+

### GUI Overhead

- COM interface opens HEC-RAS GUI (requires active desktop)
- Slower than RasCmdr subprocess execution
- Consider RDP session for headless servers

### Memory Usage

- Large unsteady simulations may consume significant RAM
- Use `max_times` parameter to limit extraction:
  ```python
  df = RasControl.get_unsteady_results("01", max_times=20)
  ```

## Migration Path: RasControl to RasCmdr

When upgrading to HEC-RAS 6.x+:

```python
# Legacy (RasControl - HEC-RAS 5.x)
init_ras_project(path, "5.0.6")
RasControl.run_plan("01")
df = RasControl.get_steady_results("01")

# Modern (RasCmdr - HEC-RAS 6.x)
from ras_commander import RasCmdr
from ras_commander.hdf import HdfResultsPlan

init_ras_project(path, "6.6")
RasCmdr.compute_plan("01")
hdf = HdfResultsPlan(ras.plan_df.loc[0, 'HDF_Results_Path'])
wse = hdf.get_steady_wse()
```

## Where to Learn More

### Primary Sources
- **RasControl.py** - Complete API with docstrings
- **examples/121_legacy_hecrascontroller_and_rascontrol.ipynb** - Full workflow examples

### Related Skills
- **hecras_compute_plans** - Modern RasCmdr execution (HEC-RAS 6.x+)
- **hecras_extract_results** - HDF-based result extraction

### Related Rules
- `.claude/rules/hec-ras/execution.md` - Execution mode comparison
- `.claude/rules/python/static-classes.md` - Static class pattern

---

**Remember**: RasControl is for legacy HEC-RAS (3.x-5.x). For HEC-RAS 6.x+, prefer RasCmdr and HDF-based methods for better performance and reliability.
