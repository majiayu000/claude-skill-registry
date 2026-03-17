---
name: orcaflex-code-check
description: Verify OrcaFlex model results against industry standards (DNV, API, ISO).
  Perform capacity checks, safety factor verification, and compliance reporting for
  offshore structures.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- code check
- standards compliance
- DNV check
- API check
- ISO check
- safety factor
- capacity check
- design verification
---
# OrcaFlex Code Check Skill

Verify OrcaFlex model results against industry standards (DNV, API, ISO) with automated capacity checks and compliance reporting.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-modeling: '>=2.0.0,<3.0.0'
  structural-analysis: '>=1.0.0,<2.0.0'
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
- Initial release with standards compliance checking
- Mooring line capacity verification
- Safety factor calculation
- Multi-standard support (DNV, API, ISO)

## When to Use

- Verify mooring line tensions against MBL limits
- Check riser stress against allowable
- Validate safety factors per design codes
- Generate compliance reports for certification
- Design verification before fabrication
- Audit existing designs against current standards

## Supported Standards

### Mooring Systems

| Standard | Application | Key Checks |
|----------|-------------|------------|
| **API RP 2SK** | Stationkeeping | Safety factors, line capacity |
| **DNV-OS-E301** | Position mooring | Tension limits, fatigue |
| **ISO 19901-7** | Mooring systems | Capacity, redundancy |

### Risers

| Standard | Application | Key Checks |
|----------|-------------|------------|
| **API RP 2RD** | Riser design | Stress, fatigue |
| **DNV-OS-F201** | Dynamic risers | Stress, VIV |
| **API STD 2RD** | Design of risers | Combined loading |

### Pipelines

| Standard | Application | Key Checks |
|----------|-------------|------------|
| **DNV-OS-F101** | Submarine pipelines | Wall thickness, buckling |
| **API RP 1111** | Pipeline design | Pressure containment |

## Configuration

### Mooring Code Check

```yaml
# configs/mooring_code_check.yml

code_check:
  standard: "API_RP_2SK"
  edition: "2015"

  mooring:
    lines:
      - name: "Leg_1"
        line_type: "Chain_R4_84mm"
        mbl: 8500.0  # kN - Minimum Breaking Load
      - name: "Leg_2"
        line_type: "Chain_R4_84mm"
        mbl: 8500.0

    safety_factors:
      intact:
        static: 1.67    # API RP 2SK Table 2
        dynamic: 1.82
      damaged:
        static: 1.25
        dynamic: 1.43

    load_conditions:
      - name: "100-year intact"
        condition: "intact"
        load_type: "dynamic"
      - name: "100-year damaged"
        condition: "damaged"
        load_type: "dynamic"

  output:
    report_path: "reports/code_check/"
    format: "html"
```

### Riser Code Check

```yaml
# configs/riser_code_check.yml

code_check:
  standard: "DNV_OS_F201"
  edition: "2021"

  riser:
    name: "SCR"
    material:
      grade: "X65"
      smys: 448.0   # MPa
      smts: 531.0   # MPa
      young_modulus: 207000.0  # MPa

    geometry:
      od: 0.2731    # m
      wt: 0.0159    # m (wall thickness)

    design_factors:
      gamma_SC: 1.04   # Safety class factor
      gamma_m: 1.15    # Material factor
      gamma_F: 1.10    # Load factor
      alpha_U: 1.00    # Material strength factor

    checks:
      - "hoop_stress"
      - "longitudinal_stress"
      - "equivalent_stress"
      - "collapse"
      - "propagation_buckling"

  output:
    report_path: "reports/riser_code_check/"
```

## Python API

### Mooring Safety Factor Check

```python
from digitalmodel.structural.structural_analysis.capacity import CapacityChecker

def check_mooring_safety_factors(
    max_tensions: dict,
    mbl_values: dict,
    standard: str = "API_RP_2SK"
) -> dict:
    """
    Check mooring line tensions against MBL limits.

    Args:
        max_tensions: Dict of {line_name: max_tension_kN}
        mbl_values: Dict of {line_name: mbl_kN}
        standard: Design standard to use

    Returns:
        Dict with check results
    """
    # Safety factors per API RP 2SK (2015)
    if standard == "API_RP_2SK":
        safety_factors = {
            "intact_dynamic": 1.82,
            "intact_static": 1.67,
            "damaged_dynamic": 1.43,
            "damaged_static": 1.25
        }
    elif standard == "DNV_OS_E301":
        safety_factors = {
            "intact_dynamic": 2.20,
            "damaged_dynamic": 1.50
        }
    else:
        raise ValueError(f"Unknown standard: {standard}")

    results = {}

    for line_name, max_tension in max_tensions.items():
        mbl = mbl_values.get(line_name)
        if mbl is None:
            continue

        # Calculate utilization
        line_results = {
            "max_tension_kN": max_tension,
            "mbl_kN": mbl,
            "checks": {}
        }

        for condition, sf_required in safety_factors.items():
            allowable = mbl / sf_required
            utilization = max_tension / allowable
            passes = utilization <= 1.0
            actual_sf = mbl / max_tension

            line_results["checks"][condition] = {
                "allowable_kN": allowable,
                "utilization": utilization,
                "actual_sf": actual_sf,
                "required_sf": sf_required,
                "passes": passes
            }

        results[line_name] = line_results

    return results

# Example usage
max_tensions = {
    "Leg_1": 2450.5,
    "Leg_2": 2380.2,
    "Leg_3": 2320.1,
    "Leg_4": 2290.8
}

mbl_values = {
    "Leg_1": 8500.0,
    "Leg_2": 8500.0,
    "Leg_3": 8500.0,
    "Leg_4": 8500.0
}

results = check_mooring_safety_factors(max_tensions, mbl_values)

for line, data in results.items():
    intact_check = data["checks"]["intact_dynamic"]
    print(f"{line}: Utilization = {intact_check['utilization']:.2%}, "
          f"SF = {intact_check['actual_sf']:.2f} "
          f"({'PASS' if intact_check['passes'] else 'FAIL'})")
```

### Riser Stress Check

```python
from digitalmodel.structural.structural_analysis.capacity import CapacityChecker
import math

def check_riser_stress(
    max_tension: float,
    max_bend_moment: float,
    internal_pressure: float,
    external_pressure: float,
    od: float,
    wt: float,
    smys: float,
    standard: str = "DNV_OS_F201"
) -> dict:
    """
    Check riser stress against allowable per design code.

    Args:
        max_tension: Maximum tension (kN)
        max_bend_moment: Maximum bending moment (kN.m)
        internal_pressure: Internal pressure (MPa)
        external_pressure: External pressure (MPa)
        od: Outer diameter (m)
        wt: Wall thickness (m)
        smys: Specified minimum yield strength (MPa)
        standard: Design standard

    Returns:
        Dict with stress check results
    """
    id_ = od - 2 * wt
    area = math.pi / 4 * (od**2 - id_**2)
    i_moment = math.pi / 64 * (od**4 - id_**4)

    # Axial stress
    sigma_a = max_tension * 1000 / area / 1e6  # MPa

    # Bending stress
    sigma_b = max_bend_moment * 1000 * (od / 2) / i_moment / 1e6  # MPa

    # Hoop stress (thin wall approximation)
    delta_p = internal_pressure - external_pressure
    sigma_h = delta_p * (od - wt) / (2 * wt)  # MPa

    # Von Mises equivalent stress
    sigma_e = math.sqrt(
        sigma_a**2 + sigma_b**2 + sigma_h**2
        - sigma_a * sigma_h - sigma_b * sigma_h - sigma_a * sigma_b
        + 3 * 0  # Shear assumed zero
    )

    # Allowable stress per DNV-OS-F201
    if standard == "DNV_OS_F201":
        gamma_SC = 1.04  # Normal safety class
        gamma_m = 1.15
        alpha_U = 1.00

        sigma_allowable = smys * alpha_U / (gamma_SC * gamma_m)
    else:
        # API approach
        sigma_allowable = smys * 0.67  # 2/3 SMYS

    utilization = sigma_e / sigma_allowable

    return {
        "axial_stress_MPa": sigma_a,
        "bending_stress_MPa": sigma_b,
        "hoop_stress_MPa": sigma_h,
        "von_mises_stress_MPa": sigma_e,
        "allowable_stress_MPa": sigma_allowable,
        "utilization": utilization,
        "passes": utilization <= 1.0,
        "standard": standard
    }

# Example usage
result = check_riser_stress(
    max_tension=1500.0,      # kN
    max_bend_moment=250.0,   # kN.m
    internal_pressure=25.0,  # MPa
    external_pressure=15.0,  # MPa
    od=0.2731,               # m
    wt=0.0159,               # m
    smys=448.0               # MPa (X65)
)

print(f"Von Mises Stress: {result['von_mises_stress_MPa']:.1f} MPa")
print(f"Allowable: {result['allowable_stress_MPa']:.1f} MPa")
print(f"Utilization: {result['utilization']:.2%}")
print(f"Status: {'PASS' if result['passes'] else 'FAIL'}")
```

### Standards Lookup

```python
from digitalmodel.infrastructure.common.standards_lookup import StandardsLookup

# Initialize lookup
lookup = StandardsLookup()

# Search for relevant standards
results = lookup.search("mooring design")

for standard in results:
    print(f"{standard['name']}: {standard['path']}")

# Get specific standard
api_2sk = lookup.get("API_RP_2SK_2015")
print(f"Standard: {api_2sk['title']}")
print(f"Location: {api_2sk['path']}")
```

### Generate Compliance Report

```python
def generate_compliance_report(
    check_results: dict,
    output_path: str,
    project_info: dict
) -> str:
    """Generate HTML compliance report."""

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Code Compliance Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #333; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            .pass {{ color: green; font-weight: bold; }}
            .fail {{ color: red; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Code Compliance Report</h1>
        <h2>Project: {project_info.get('name', 'N/A')}</h2>
        <p>Standard: {check_results.get('standard', 'N/A')}</p>
        <p>Date: {check_results.get('date', 'N/A')}</p>

        <h3>Summary</h3>
        <table>
            <tr>
                <th>Component</th>
                <th>Max Load</th>
                <th>Allowable</th>
                <th>Utilization</th>
                <th>Status</th>
            </tr>
    """

    for component, data in check_results.get("components", {}).items():
        status_class = "pass" if data["passes"] else "fail"
        status_text = "PASS" if data["passes"] else "FAIL"

        html_content += f"""
            <tr>
                <td>{component}</td>
                <td>{data['max_load']:.1f}</td>
                <td>{data['allowable']:.1f}</td>
                <td>{data['utilization']:.1%}</td>
                <td class="{status_class}">{status_text}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    with open(output_path, "w") as f:
        f.write(html_content)

    return output_path
```

## Safety Factors Reference

### API RP 2SK (2015)

| Condition | Analysis | Safety Factor |
|-----------|----------|---------------|
| Intact | Quasi-static | 1.67 |
| Intact | Dynamic | 1.82 |
| Damaged | Quasi-static | 1.25 |
| Damaged | Dynamic | 1.43 |

### DNV-OS-E301

| Condition | Consequence Class 1 | Consequence Class 2 |
|-----------|---------------------|---------------------|
| ULS Intact | 2.20 | 2.50 |
| ULS Damaged | 1.50 | 1.65 |
| ALS | 1.00 | 1.10 |

### ISO 19901-7

| Condition | Category 1 | Category 2 |
|-----------|------------|------------|
| Intact | 1.67 | 2.00 |
| Damaged | 1.25 | 1.50 |

## Best Practices

### Before Code Check

1. **Verify simulation completed** - Ensure full 3-hour run
2. **Check load cases** - Cover all design conditions
3. **Validate inputs** - Correct MBL, geometry, material
4. **Document assumptions** - Record safety class, consequence class

### During Check

1. **Use correct standard** - Match project requirements
2. **Apply correct factors** - Consider condition (intact/damaged)
3. **Check all components** - Lines, connections, anchors
4. **Consider fatigue** - Not just ultimate capacity

### Reporting

1. **Clear presentation** - Pass/fail for each check
2. **Utilization ratios** - Show margin
3. **Reference standard** - Cite clause numbers
4. **Recommendations** - Action items for failures

## Error Handling

```python
try:
    results = check_mooring_safety_factors(tensions, mbl_values, "API_RP_2SK")
except ValueError as e:
    print(f"Unknown standard: {e}")
    print("Supported standards: API_RP_2SK, DNV_OS_E301, ISO_19901_7")

except KeyError as e:
    print(f"Missing data: {e}")
    print("Ensure all lines have MBL values defined")
```

## Related Skills

- [orcaflex-post-processing](../orcaflex-post-processing/SKILL.md) - Extract results
- [orcaflex-extreme-analysis](../orcaflex-extreme-analysis/SKILL.md) - Find design loads
- [structural-analysis](../structural-analysis/SKILL.md) - Structural capacity checks
- [fatigue-analysis](../fatigue-analysis/SKILL.md) - Fatigue code checks

## References

- API RP 2SK: Design and Analysis of Stationkeeping Systems
- DNV-OS-E301: Position Mooring
- DNV-OS-F201: Dynamic Risers
- ISO 19901-7: Stationkeeping Systems for Floating Offshore Structures
- Source: `src/digitalmodel/infrastructure/common/standards_lookup.py`
- Source: `src/digitalmodel/modules/structural_analysis/capacity.py`
