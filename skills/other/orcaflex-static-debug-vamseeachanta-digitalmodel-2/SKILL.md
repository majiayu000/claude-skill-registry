---
name: orcaflex-static-debug
description: Troubleshoot and resolve OrcaFlex static analysis convergence issues.
  Diagnose common problems including line connectivity, tensions, environmental conditions,
  and numerical instabilities.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- static convergence
- static analysis failed
- convergence issues
- static not converging
- OrcaFlex statics
- model not converging
- catenary convergence
- unstable statics
---
# OrcaFlex Static Debug Skill

Diagnose and resolve OrcaFlex static analysis convergence issues with systematic troubleshooting approaches.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-modeling: '>=2.0.0,<3.0.0'
orcaflex_version: '>=11.0'
compatibility:
  tested_python:
  - '3.10'
  - '3.11'
  - '3.12'
  - '3.13'
  os:
  - Windows
  - Linux
  - macOS
```

## Changelog

### [1.0.0] - 2026-01-17

**Added:**
- Initial release with comprehensive debugging approaches
- Common error patterns and solutions
- Diagnostic code examples
- Step-by-step troubleshooting guide

## When to Use

- OrcaFlex static analysis fails to converge
- Model returns "Statics not converged" error
- Static results show unrealistic values
- Troubleshooting new model configurations
- Debugging catenary line issues
- Investigating vessel connection problems
- Resolving numerical instabilities

## Common Error Messages

| Error | Likely Cause | Section |
|-------|--------------|---------|
| "Statics failed to converge" | Multiple possible | Full diagnosis |
| "Line catenary diverged" | Line configuration | Lines section |
| "Singular stiffness matrix" | Disconnected components | Connectivity |
| "Buoy/vessel not in equilibrium" | Forces not balanced | Equilibrium |
| "Line end not at seabed" | Anchor configuration | Anchors |
| "Excessive damping required" | Numerical instability | Damping |

## Diagnostic Workflow

```
[Static Analysis Failed]
         ↓
[1. Check Error Message]
         ↓
[2. Validate Model Structure]
    ├── Connectivity
    ├── Object positions
    └── Line configurations
         ↓
[3. Check Initial Conditions]
    ├── Tensions
    ├── Lengths
    └── Positions
         ↓
[4. Review Environment]
    ├── Water depth
    ├── Current
    └── Waves (should be off for statics)
         ↓
[5. Adjust Solver Settings]
    ├── Damping
    ├── Tolerance
    └── Iteration limits
         ↓
[6. Incremental Testing]
    ├── Simplify model
    ├── Add components one by one
    └── Identify failing element
```

## Diagnostic Code

### Basic Static Diagnosis

```python
import OrcFxAPI
from pathlib import Path

def diagnose_static_failure(model_path: str) -> dict:
    """
    Diagnose why static analysis might be failing.

    Args:
        model_path: Path to OrcaFlex model file

    Returns:
        Dictionary with diagnostic results
    """
    diagnostics = {
        "model_loaded": False,
        "issues": [],
        "warnings": [],
        "recommendations": []
    }

    try:
        model = OrcFxAPI.Model()
        model.LoadData(model_path)
        diagnostics["model_loaded"] = True
    except Exception as e:
        diagnostics["issues"].append(f"Failed to load model: {e}")
        return diagnostics

    # Check environment settings
    general = model.general

    # Wave should be off or very small for statics
    if hasattr(general, 'WaveType'):
        if general.WaveType != "None":
            diagnostics["warnings"].append(
                f"Wave type is '{general.WaveType}' - consider 'None' for statics"
            )

    # Check objects
    for obj in model.objects:
        obj_type = obj.typeName
        obj_name = obj.name

        # Check lines
        if obj_type == "Line":
            check_line(obj, diagnostics)

        # Check vessels
        elif obj_type == "Vessel":
            check_vessel(obj, diagnostics)

        # Check buoys
        elif obj_type in ["6D Buoy", "3D Buoy"]:
            check_buoy(obj, diagnostics)

    # Generate recommendations
    generate_recommendations(diagnostics)

    return diagnostics


def check_line(line, diagnostics: dict):
    """Check line configuration for common issues."""
    name = line.name

    # Check length
    try:
        total_length = sum(line.Length)
        if total_length <= 0:
            diagnostics["issues"].append(
                f"Line '{name}': Total length is {total_length}m (must be > 0)"
            )
    except:
        diagnostics["issues"].append(
            f"Line '{name}': Cannot read length - check Sections"
        )

    # Check connections
    try:
        end_a = line.EndAConnection
        end_b = line.EndBConnection

        if end_a == "Free" and end_b == "Free":
            diagnostics["issues"].append(
                f"Line '{name}': Both ends are Free - must have at least one connection"
            )
    except:
        pass

    # Check line type
    try:
        line_type = line.LineType
        if line_type is None or line_type == "":
            diagnostics["issues"].append(
                f"Line '{name}': No LineType assigned"
            )
    except:
        pass


def check_vessel(vessel, diagnostics: dict):
    """Check vessel configuration."""
    name = vessel.name

    # Check if vessel data is loaded
    try:
        displacement = vessel.Displacement
        if displacement <= 0:
            diagnostics["warnings"].append(
                f"Vessel '{name}': Displacement is {displacement} (check units)"
            )
    except:
        diagnostics["warnings"].append(
            f"Vessel '{name}': Cannot read displacement"
        )


def check_buoy(buoy, diagnostics: dict):
    """Check buoy configuration."""
    name = buoy.name

    # Check position
    try:
        z = buoy.InitialZ
        # Check if buoy is at reasonable depth
        if z > 100:  # Suspiciously high
            diagnostics["warnings"].append(
                f"Buoy '{name}': InitialZ = {z}m - check if this is intended"
            )
    except:
        pass


def generate_recommendations(diagnostics: dict):
    """Generate recommendations based on findings."""
    if diagnostics["issues"]:
        diagnostics["recommendations"].append(
            "Fix all issues before attempting static analysis"
        )

    if len(diagnostics["warnings"]) > 3:
        diagnostics["recommendations"].append(
            "Multiple warnings - consider simplifying model first"
        )

    if not diagnostics["issues"] and not diagnostics["warnings"]:
        diagnostics["recommendations"].append(
            "Model structure looks OK - try adjusting solver settings"
        )
```

### Incremental Static Testing

```python
def test_static_incrementally(model_path: str) -> dict:
    """
    Test static analysis by progressively enabling components.

    Returns which component causes failure.
    """
    model = OrcFxAPI.Model()
    model.LoadData(model_path)

    results = {"tests": [], "failing_component": None}

    # Get all lines
    lines = [obj for obj in model.objects if obj.typeName == "Line"]

    # Disable all lines
    for line in lines:
        line.IncludedInStatics = "No"

    # Test with no lines
    try:
        model.CalculateStatics()
        results["tests"].append({"component": "Base model (no lines)", "passed": True})
    except Exception as e:
        results["tests"].append({"component": "Base model", "passed": False, "error": str(e)})
        results["failing_component"] = "Base model"
        return results

    # Enable lines one by one
    for line in lines:
        line.IncludedInStatics = "Yes"

        try:
            model.CalculateStatics()
            results["tests"].append({"component": f"Line: {line.name}", "passed": True})
        except Exception as e:
            results["tests"].append({
                "component": f"Line: {line.name}",
                "passed": False,
                "error": str(e)
            })
            results["failing_component"] = line.name

            # Disable this line and continue
            line.IncludedInStatics = "No"

    return results
```

### Solver Settings Adjustment

```python
def adjust_solver_for_convergence(model) -> bool:
    """
    Progressively adjust solver settings to achieve convergence.

    Returns True if convergence achieved.
    """
    # Settings to try
    damping_values = [10, 20, 50, 100, 200]
    tolerance_values = [1e-5, 1e-4, 1e-3, 1e-2]

    for damping in damping_values:
        for tolerance in tolerance_values:
            try:
                # Apply settings
                model.general.StaticsDamping = damping
                model.general.StaticsTolerance = tolerance

                # Try statics
                model.CalculateStatics()
                print(f"Converged with Damping={damping}, Tolerance={tolerance}")
                return True

            except OrcFxAPI.OrcaFlexError:
                continue

    print("Failed to converge with any settings combination")
    return False
```

## Common Issues and Solutions

### 1. Line Catenary Diverged

**Symptoms:**
- Error mentions "catenary" or "line diverged"
- Specific line name in error message

**Causes:**
- Line too short for connection points
- Incorrect end positions
- Incompatible line type properties

**Solutions:**

```python
# Check line geometry
line = model["Failing_Line"]

# Get end positions
end_a_x, end_a_y, end_a_z = line.EndAX, line.EndAY, line.EndAZ
end_b_x, end_b_y, end_b_z = line.EndBX, line.EndBY, line.EndBZ

# Calculate required length (straight line minimum)
import math
min_length = math.sqrt(
    (end_b_x - end_a_x)**2 +
    (end_b_y - end_a_y)**2 +
    (end_b_z - end_a_z)**2
)

total_length = sum(line.Length)
print(f"Minimum length required: {min_length:.1f}m")
print(f"Total line length: {total_length:.1f}m")

if total_length < min_length * 1.1:
    print("Line is too short! Increase length by at least 10%")
```

### 2. Vessel Not in Equilibrium

**Symptoms:**
- "Vessel not in equilibrium"
- Large forces/moments on vessel

**Causes:**
- Mooring forces don't balance
- Incorrect initial position
- Missing or misconfigured lines

**Solutions:**

```yaml
# Option 1: Let OrcaFlex find equilibrium position
vessel:
  IncludedInStatics: "Included"
  CalculatedPosition: "Yes"  # Let OrcaFlex calculate position

# Option 2: Fix vessel position
vessel:
  IncludedInStatics: "Included"
  InitialX: 0.0
  InitialY: 0.0
  InitialZ: 0.0  # At draft
```

### 3. Anchor Not at Seabed

**Symptoms:**
- "End not at seabed"
- Anchor position mismatch

**Solutions:**

```python
# Ensure anchor is at seabed
water_depth = model.environment.WaterDepth

for line in lines:
    if line.EndAConnection == "Anchored":
        # Set anchor at seabed
        line.EndAZ = -water_depth

    if line.EndBConnection == "Anchored":
        line.EndBZ = -water_depth
```

### 4. Buoy/Structure Instability

**Symptoms:**
- 6D Buoy convergence failure
- Unrealistic rotations

**Solutions:**

```yaml
# Add constraints during statics
6DBuoy:
  Name: "CALM_Buoy"
  # Fix orientation during statics
  Constraint1: "Fixed"    # Fix X rotation
  Constraint2: "Fixed"    # Fix Y rotation
  Constraint3: "Free"     # Allow Z rotation (yaw)
```

### 5. Zero-Tension Lines

**Symptoms:**
- Singular stiffness matrix
- Lines with zero or negative tension

**Solutions:**

```python
# Check initial tensions
for line in lines:
    try:
        # Estimate initial tension from catenary
        weight_in_water = line.MassPerUnitLength * 9.81 * (1 - 1025/7850)
        length = sum(line.Length)

        # Very rough tension estimate
        estimated_tension = weight_in_water * length / 2

        if estimated_tension < 100:  # Very low tension
            print(f"Warning: {line.name} may have low tension")
            print("Consider:")
            print("  - Increasing line length")
            print("  - Adjusting end positions")
            print("  - Adding buoyancy")
    except:
        pass
```

## Solver Settings Reference

### Damping Settings

| StaticsDamping | Use Case |
|----------------|----------|
| 1-10 | Well-behaved models |
| 10-50 | Typical offshore models |
| 50-100 | Challenging convergence |
| 100-500 | Severe instabilities |

### Tolerance Settings

| Tolerance | Accuracy | Use Case |
|-----------|----------|----------|
| 1e-6 | Very high | Final production runs |
| 1e-5 | High | Standard analysis |
| 1e-4 | Medium | Initial testing |
| 1e-3 | Low | Debug convergence |

### Iteration Limits

```yaml
general:
  MaxStaticsIterations: 200      # Default is usually 100
  StaticsMinDamping: 0.01
  StaticsMaxDamping: 100
```

## Debug Checklist

### Quick Checks

- [ ] Water depth is correct
- [ ] All lines have valid line types
- [ ] End connections are properly defined
- [ ] Vessel/buoy initial positions are reasonable
- [ ] No objects at exactly the same position
- [ ] Waves are disabled for pure statics

### Line Checks

- [ ] Line lengths exceed minimum span
- [ ] Segment lengths are appropriate
- [ ] Line type properties are valid (EA, mass, diameter)
- [ ] End connections reference existing objects
- [ ] Anchor depths match water depth

### Vessel/Buoy Checks

- [ ] Displacement and draft are correct
- [ ] COG position is realistic
- [ ] RAO data is loaded (if applicable)
- [ ] Connection points are valid

### Environment Checks

- [ ] Current profile is reasonable
- [ ] Water depth matches model
- [ ] Seabed elevation is correct

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations
- [orcaflex-line-wizard](../orcaflex-line-wizard/SKILL.md) - Configure line properties
- [orcaflex-mooring-iteration](../orcaflex-mooring-iteration/SKILL.md) - Optimize tensions
- [catenary-riser](../catenary-riser/SKILL.md) - Catenary analysis

## References

- OrcaFlex Theory: Static Analysis
- OrcaFlex Help: Troubleshooting
- Orcina Support: Common Statics Issues
