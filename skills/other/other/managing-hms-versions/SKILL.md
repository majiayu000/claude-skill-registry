---
name: managing-hms-versions
description: |
  Manages HEC-HMS version differences (3.x vs 4.x), handles Python 2/3 compatibility,
  detects HMS installations, and generates version-appropriate Jython scripts. Use when
  working with legacy HMS 3.x projects, upgrading models from 3.x to 4.x, testing across
  multiple HMS versions, or troubleshooting version-specific issues. Handles 32-bit vs
  64-bit architecture differences, memory limits, and script syntax variations.
  Trigger keywords: HMS version, HMS 3.x, HMS 4.x, legacy, upgrade, Python 2 compatible,
  32-bit, 64-bit, version detection, multi-version testing.
---

# Managing HMS Versions

## Quick Start

```python
from hms_commander import HmsJython

# Auto-detect HMS installations
hms_exe = HmsJython.find_hms_executable()
print(f"Found: {hms_exe}")

# Generate version-appropriate script
is_3x = "(x86)" in str(hms_exe)  # 32-bit = HMS 3.x
script = HmsJython.generate_compute_script(
    project_path="project",
    run_name="Run 1",
    python2_compatible=is_3x  # Critical for 3.x!
)

# Execute with detected version
success, stdout, stderr = HmsJython.execute_script(script, hms_exe)
```

## Primary Sources

**Code**: `hms_commander/HmsJython.py` - Version detection and script generation

**Rules**: `.claude/rules/hec-hms/version-support.md` - Complete differences

**Examples**: `examples/01_multi_version_execution.ipynb` - Multi-version workflow

**Task Agent**: `hms_agents/update_3_to_4/` - Automated 3.x → 4.x upgrade

## When to Use This Skill

- Working with legacy HMS 3.x projects
- Upgrading models from 3.x to 4.x
- Testing across multiple HMS versions
- Troubleshooting version-specific script errors
- Setting up multi-version test environments
- Understanding memory and architecture limitations

## Supported Versions

| Version | Support | Architecture | Python | Notes |
|---------|---------|--------------|--------|-------|
| **HMS 4.4.1+** | ✅ Full | 64-bit | Python 3 | Recommended |
| **HMS 3.3-3.5** | ✅ Full | 32-bit | Python 2 | Requires `python2_compatible=True` |
| HMS 4.0-4.3 | ❌ | 64-bit | Python 3 | Legacy classpath not supported |
| HMS 3.0-3.2 | ❓ | 32-bit | Python 2 | Untested |

**See**: `.claude/rules/hec-hms/version-support.md` for complete table

## Critical Differences

### HMS 3.x (32-bit, Python 2)

**Install Path**: `C:\Program Files (x86)\HEC\HEC-HMS\3.x\`
**Max Memory**: ~1.3 GB
**Java**: `java/bin/java.exe`
**Python**: Jython 2.5 (Python 2 syntax)

**Script Generation**:
```python
script = HmsJython.generate_compute_script(
    project_path=path,
    run_name=run,
    python2_compatible=True  # MUST be True for 3.x!
)
```

**Python 2 Syntax**:
```python
print "Computing run"  # No parentheses
```

### HMS 4.x (64-bit, Python 3)

**Install Path**: `C:\Program Files\HEC\HEC-HMS\4.x\`
**Max Memory**: 32+ GB
**Java**: `jre/bin/java.exe`
**Python**: Jython 2.7 (Python 3 syntax)

**Script Generation**:
```python
script = HmsJython.generate_compute_script(
    project_path=path,
    run_name=run
    # python2_compatible=False (default)
)
```

**Python 3 Syntax**:
```python
print(f"Computing {run_name}")  # Parentheses required
```

## Core Capabilities

### 1. Version Detection

```python
# Auto-detect from common install locations
hms_exe = HmsJython.find_hms_executable()

# Check if 3.x or 4.x
if "(x86)" in str(hms_exe):
    print("HMS 3.x detected (32-bit)")
    python2_compatible = True
else:
    print("HMS 4.x detected (64-bit)")
    python2_compatible = False
```

### 2. Version-Appropriate Script Generation

```python
script = HmsJython.generate_compute_script(
    project_path=project_path,
    run_name=run_name,
    python2_compatible=python2_compatible
)
```

HmsJython handles syntax differences automatically.

### 3. Multi-Version Testing

```python
from hms_commander import HmsExamples

# List installed versions
versions = HmsExamples.list_versions()
print(f"Found HMS versions: {versions}")

# Test across all versions
for version in versions:
    HmsExamples.extract_project("tifton", version=version)
    # Run tests for this version
```

**See**: `examples/01_multi_version_execution.ipynb` for complete workflow

### 4. Version Upgrade

**Automated approach** (Recommended):
```python
# Use update_3_to_4 task agent
# See: hms_agents/update_3_to_4/README.md
```

**Manual approach**: Open in HMS 4.x GUI, save (converts file format)

## Common Workflows

### Workflow 1: Legacy 3.x Project

```python
# 1. Detect HMS 3.x
hms_3x_path = r"C:\Program Files (x86)\HEC\HEC-HMS\3.5"

# 2. Generate Python 2 script
script = HmsJython.generate_compute_script(
    project_path=r"C:\Projects\old_project",
    run_name="Run 1",
    python2_compatible=True
)

# 3. Execute
success, stdout, stderr = HmsJython.execute_script(
    script_content=script,
    hms_exe_path=hms_3x_path
)

# 4. Check for Python 2 syntax errors
if "SyntaxError" in stderr:
    print("Forgot python2_compatible=True!")
```

### Workflow 2: Multi-Version Testing

```python
for version in ["3.5", "4.11", "4.13"]:
    # Extract version-specific example
    HmsExamples.extract_project("tifton", version=version)

    # Detect Python 2 vs 3
    python2 = version.startswith("3.")

    # Generate script
    script = HmsJython.generate_compute_script(
        f"tifton_{version}/tifton",
        "1970_simulation",
        python2_compatible=python2
    )

    # Execute
    hms_exe = HmsExamples.get_hms_exe(version)
    success, stdout, stderr = HmsJython.execute_script(script, hms_exe)

    print(f"HMS {version}: {'✅' if success else '❌'}")
```

### Workflow 3: Upgrade 3.x to 4.x

**Use the update_3_to_4 task agent**:
```python
# See: hms_agents/update_3_to_4/AGENT.md
from hms_agents.update_3_to_4 import VersionUpgrader

upgrader = VersionUpgrader(
    project_3x="path/to/hms3x/project",
    project_4x="path/to/hms4x/project"
)

verdict = upgrader.execute()
upgrader.export_modeling_log("UPGRADE_LOG.md")
```

## Troubleshooting

### Issue: Python 2 Syntax Error

**Error**: `SyntaxError: invalid syntax`

**Cause**: Forgot `python2_compatible=True` for HMS 3.x

**Fix**:
```python
script = HmsJython.generate_compute_script(
    project_path=path,
    run_name=run,
    python2_compatible=True  # Add this!
)
```

### Issue: Memory Error (HMS 3.x)

**Error**: `OutOfMemoryError`

**Cause**: HMS 3.x limited to ~1.3 GB (32-bit)

**Fix**: Upgrade to HMS 4.x (64-bit) for large models

### Issue: HMS Not Found

**Error**: `FileNotFoundError: HMS executable not found`

**Fix**:
```python
# Specify path manually
hms_exe = r"C:\Program Files\HEC\HEC-HMS\4.11\HEC-HMS.cmd"
HmsJython.execute_script(script, hms_exe_path=hms_exe)
```

## Reference Files

- `reference/hms-3x-vs-4x.md` - Complete differences table
- `reference/python2-compatibility.md` - Script syntax differences
- `examples/legacy-projects.md` - HMS 3.x workflow examples

## Related Skills

- **executing-hms-runs** - Uses version detection for execution
- **cloning-hms-components** - Clone before upgrading
