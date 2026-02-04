---
name: hecras_parse_compute-messages
allowed-tools: [Read, Grep, Glob]
description: |
  Parse HEC-RAS compute output from HDF files to extract execution status,
  diagnostic messages, and performance metrics. Converts raw computation
  messages into structured diagnostics for workflow orchestration.
  Use when checking plan completion status, extracting compute messages,
  diagnosing execution failures, analyzing runtime performance, or
  interpreting HEC-RAS error codes.
  Keywords: compute messages, execution status, plan complete, runtime,
  performance, error diagnostics, HEC-RAS output, simulation results,
  warnings, convergence, instability, time step, iteration.
---

# Parsing HEC-RAS Compute Messages

**Primary Sources (navigate to these for complete details)**:
- **HDF Class Reference**: `ras_commander/hdf/AGENTS.md` - Class hierarchy, decorators
- **HdfResultsPlan Implementation**: `ras_commander/hdf/HdfResultsPlan.py` - Compute message methods
- **Working Example**: `examples/400_1d_hdf_data_extraction.ipynb` - Compute message extraction

This skill provides patterns for extracting and interpreting HEC-RAS computation output. For implementation details, see the primary sources above.

---

## Quick Start

### Check Plan Completion and Extract Messages

```python
from ras_commander import init_ras_project, HdfResultsPlan

# Initialize project
init_ras_project("C:/Projects/MyModel", "6.6")

# Extract compute messages (handles HDF + .txt fallback automatically)
messages = HdfResultsPlan.get_compute_messages("01")

# Check if plan has results (runtime data exists only for completed plans)
runtime = HdfResultsPlan.get_runtime_data("01")
is_complete = runtime is not None

if is_complete:
    print(f"Plan completed in {runtime['Complete Process (hr)'].values[0]:.2f} hours")
else:
    print("Plan has not been executed or did not complete")
```

---

## API Reference

### HdfResultsPlan.get_compute_messages()

**Purpose**: Extract raw computation messages from HDF file

**Signature**:
```python
@staticmethod
@log_call
@standardize_input(file_type='plan_hdf')
def get_compute_messages(hdf_path: Path) -> str
```

**Parameters**:
- `hdf_path`: Plan HDF file path OR plan number string (e.g., "01")

**Returns**: String containing all computation messages, empty string if unavailable

**Fallback Behavior**:
1. First attempts: HDF path `/Results/Summary/Compute Messages (text)`
2. Fallback: `.txt` file via RasControl (for pre-6.x HEC-RAS)

**Example**:
```python
messages = HdfResultsPlan.get_compute_messages("01")
print(len(messages))  # Character count
```

### HdfResultsPlan.get_compute_messages_hdf_only()

**Purpose**: Extract compute messages WITHOUT RasControl/COM fallback

**Use When**: Automated workflows where COM locking is problematic

**Fallback Order**:
1. HDF `/Results/Summary/Compute Messages (text)`
2. `{plan_file}.computeMsgs.txt` (HEC-RAS 6.x+)
3. `{plan_file}.comp_msgs.txt` (HEC-RAS 5.x)

### HdfResultsPlan.get_runtime_data()

**Purpose**: Extract detailed performance metrics for completed plans

**Returns**: DataFrame with columns:
- `Plan Name`, `File Name`
- `Simulation Start Time`, `Simulation End Time`
- `Simulation Duration (s)`, `Simulation Time (hr)`
- `Completing Geometry (hr)`, `Preprocessing Geometry (hr)`
- `Completing Event Conditions (hr)`, `Unsteady Flow Computations (hr)`
- `Complete Process (hr)`
- `Unsteady Flow Speed (hr/hr)`, `Complete Process Speed (hr/hr)`

**Returns None if**: Plan not executed or did not complete

---

## Common Error Patterns

### Critical Errors (Plan Failed)

| Pattern | Meaning | Likely Cause |
|---------|---------|--------------|
| `Unable to open geometry` | Missing/corrupt geometry file | File path error, file locked |
| `Boundary condition not found` | DSS path invalid | Wrong DSS pathname, missing file |
| `ERROR: HDF file cannot be opened` | Output file issue | Permissions, disk full |
| `Unrecoverable error` | Fatal execution error | Model configuration issue |

### Stability Warnings (Plan May Succeed)

| Pattern | Meaning | Action |
|---------|---------|--------|
| `Unsteady flow time step reduction` | Stability issues | May need smaller time step |
| `Exceeded maximum iterations` | Convergence problem | Check Manning's n, geometry |
| `Time step reduced below minimum` | Critical instability | Review problem areas |
| `Solution did not converge` | Numerical issues | Check boundary conditions |

### Informational Messages

| Pattern | Meaning |
|---------|---------|
| `Complete Process` | Plan finished successfully |
| `Writing Results` | Output phase started |
| `Completing Geometry` | Preprocessing successful |
| `Completing Event Conditions` | Boundary setup successful |

---

## Message Parsing Pattern

### Basic Severity Classification

```python
def classify_message_severity(message_line: str) -> str:
    """Classify a compute message line by severity."""
    line_upper = message_line.upper()

    # CRITICAL - plan likely failed
    if any(x in line_upper for x in [
        'UNRECOVERABLE', 'FATAL', 'UNABLE TO OPEN',
        'CANNOT OPEN', 'ERROR:', 'FAILED'
    ]):
        return 'CRITICAL'

    # ERROR - significant issue
    if any(x in line_upper for x in [
        'ERROR', 'NOT FOUND', 'EXCEEDED MAXIMUM'
    ]):
        return 'ERROR'

    # WARNING - potential issue
    if any(x in line_upper for x in [
        'WARNING', 'TIME STEP REDUCTION', 'DID NOT CONVERGE',
        'INSTABILITY', 'REDUCED'
    ]):
        return 'WARNING'

    # INFO - normal operation
    return 'INFO'
```

### Extract Structured Diagnostics

```python
def parse_compute_messages(raw_messages: str) -> dict:
    """Parse raw compute messages into structured format."""
    lines = raw_messages.strip().split('\n')

    result = {
        'critical': [],
        'errors': [],
        'warnings': [],
        'info': [],
        'is_complete': False,
        'total_lines': len(lines)
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue

        severity = classify_message_severity(line)

        if severity == 'CRITICAL':
            result['critical'].append(line)
        elif severity == 'ERROR':
            result['errors'].append(line)
        elif severity == 'WARNING':
            result['warnings'].append(line)
        else:
            result['info'].append(line)

        # Check for completion marker
        if 'COMPLETE PROCESS' in line.upper():
            result['is_complete'] = True

    return result
```

---

## Output Schema for Orchestrators

When reporting compute message analysis, use this structured format:

```markdown
## Compute Messages Analysis

### Execution Status
- **Plan**: {plan_number}
- **HDF File**: {hdf_filename}
- **Completed**: Yes/No
- **Duration**: X.XX hours (if completed)

### Messages by Severity

**CRITICAL ({count})**:
- {critical message 1}
- {critical message 2}

**ERRORS ({count})**:
- {error message 1}

**WARNINGS ({count})**:
- {warning message 1}

**INFO ({count})**: {count} informational messages (omitted for brevity)

### Diagnostics
- {Actionable interpretation}
- {Recommended next steps}

### Performance (if completed)
- Simulation Time: X.X hours
- Compute Time: X.X hours
- Speed Ratio: X.X hr/hr
```

---

## Complete Workflow Example

```python
from ras_commander import init_ras_project, HdfResultsPlan
from pathlib import Path

def analyze_plan_execution(project_path: str, ras_version: str, plan_number: str):
    """Comprehensive compute message analysis for a plan."""

    # Initialize
    init_ras_project(project_path, ras_version)

    # Get compute messages
    messages = HdfResultsPlan.get_compute_messages(plan_number)

    # Get runtime data (None if not complete)
    runtime = HdfResultsPlan.get_runtime_data(plan_number)

    # Parse messages
    parsed = parse_compute_messages(messages)

    # Build report
    report = {
        'plan': plan_number,
        'completed': runtime is not None,
        'critical_count': len(parsed['critical']),
        'error_count': len(parsed['errors']),
        'warning_count': len(parsed['warnings']),
        'info_count': len(parsed['info']),
        'runtime_hours': None,
        'speed_ratio': None
    }

    if runtime is not None:
        report['runtime_hours'] = runtime['Complete Process (hr)'].values[0]
        report['speed_ratio'] = runtime['Complete Process Speed (hr/hr)'].values[0]

    # Print summary
    print(f"Plan {plan_number}: ", end='')
    if report['completed']:
        print(f"COMPLETE in {report['runtime_hours']:.2f}h ({report['speed_ratio']:.1f}x speed)")
    else:
        print("NOT COMPLETE")

    if parsed['critical']:
        print(f"  CRITICAL: {len(parsed['critical'])} issues")
        for msg in parsed['critical'][:3]:  # Show first 3
            print(f"    - {msg[:80]}...")

    if parsed['warnings']:
        print(f"  WARNINGS: {len(parsed['warnings'])} issues")

    return report

# Usage
report = analyze_plan_execution("C:/Projects/Muncie", "6.6", "01")
```

---

## Integration with Results Analyst Agent

When delegating compute message analysis to the Results Analyst Agent:

**Context to Provide**:
1. Plan number and HDF path
2. Expected completion status
3. Any known issues or concerns

**Expected Output**:
1. Structured diagnostics following output schema
2. Severity classification of all messages
3. Actionable recommendations

**Example Delegation**:
```python
Task(
    subagent_type="results-analyst",
    model="sonnet",
    prompt="""
    Analyze compute messages for plan 01.

    Context files:
    - agent_tasks/.agent/STATE.md

    Task: Extract compute messages from examples/Muncie.p01.hdf,
    classify by severity, and provide diagnostics.

    Write findings to: .claude/outputs/results-analyst/compute-analysis.md
    """
)
```

---

## Common Issues

### Empty Messages

**Cause**: Plan not executed yet, or HDF missing Results/Summary group

**Solution**: Check if plan has been executed:
```python
runtime = HdfResultsPlan.get_runtime_data("01")
if runtime is None:
    print("Plan has not been executed - execute with RasCmdr.compute_plan('01')")
```

### COM Locking in Automated Workflows

**Cause**: `get_compute_messages()` may invoke RasControl COM fallback

**Solution**: Use `get_compute_messages_hdf_only()` for automation:
```python
# Safe for parallel/automated workflows
messages = HdfResultsPlan.get_compute_messages_hdf_only("01")
```

### Partial Results

**Cause**: Plan crashed mid-execution

**Symptoms**:
- `get_runtime_data()` returns None
- `get_compute_messages()` shows partial output
- HDF file exists but is incomplete

**Diagnosis**: Check for error patterns at end of messages

---

## Primary Sources

**For complete details, navigate to**:

1. **`ras_commander/hdf/HdfResultsPlan.py`** (lines 717-914)
   - `get_compute_messages()` implementation
   - `get_compute_messages_hdf_only()` implementation
   - HDF path `/Results/Summary/Compute Messages (text)`

2. **`ras_commander/hdf/HdfResultsPlan.py`** (lines 200-305)
   - `get_runtime_data()` implementation
   - Process time extraction
   - Speed calculations

3. **`examples/400_1d_hdf_data_extraction.ipynb`**
   - Working compute message extraction example
   - Output formatting patterns

4. **`ras_commander/hdf/AGENTS.md`**
   - HDF class organization
   - Decorator patterns
   - File type expectations

---

## See Also

- **hecras_extract_results**: Full HDF results extraction patterns
- **hecras_compute_plans**: Plan execution that generates compute messages
- **qa_repair_geometry**: Fixing geometry errors found in messages
