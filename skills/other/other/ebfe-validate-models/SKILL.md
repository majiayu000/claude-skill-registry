---
name: ebfe_validate_models
model: sonnet
description: |
  Validate organized eBFE/BLE model using ras-commander dataframes.

  Uses init_ras_project() then checks plan_df, boundary_df, rasmap_df to verify:
  - All plan files exist
  - All DSS files exist with relative paths
  - All terrain files exist with relative paths
  - All HDF results accessible
  - No absolute paths (would cause GUI popups)

  Use after organizing eBFE model to verify it's actually runnable.
  Generates validation report and script for user re-verification.
---

# eBFE Model Validator Skill

## Purpose

Validate organized eBFE models using ras-commander's built-in dataframe validation capabilities.

**Why This Matters**: Not enough to just organize files - must verify the HEC-RAS project is actually runnable using ras-commander's own validation.

## Validation Using ras-commander Dataframes

### Step 1: Initialize Project

```python
from ras_commander import init_ras_project
from pathlib import Path

# Initialize organized model
ras = init_ras_project(organized_ras_folder, version)

# If this succeeds, basic project structure is valid
# Now check dataframes for path validity
```

### Step 2: Validate plan_df

**Check all plan file references**:

```python
print("Validating Plans (plan_df)...")

for idx, row in ras.plan_df.iterrows():
    plan_number = row['plan_number']

    checks = {}

    # Check plan file exists
    plan_file = Path(row['plan_file'])
    checks['plan_file_exists'] = plan_file.exists()

    # Check geometry file exists
    if 'geom_file' in row and pd.notna(row['geom_file']):
        geom_file = Path(row['geom_file'])
        checks['geom_file_exists'] = geom_file.exists()

    # Check flow file exists
    if 'flow_file' in row and pd.notna(row['flow_file']):
        flow_file = Path(row['flow_file'])
        checks['flow_file_exists'] = flow_file.exists()

    # Check HDF file exists (pre-run results)
    if 'hdf_path' in row and pd.notna(row['hdf_path']):
        hdf_file = Path(row['hdf_path'])
        checks['hdf_exists'] = hdf_file.exists()
        if hdf_file.exists():
            print(f"  ✓ Plan {plan_number}: Pre-run results found")

    # Check for absolute paths (CRITICAL)
    checks['no_absolute_paths'] = not plan_file.is_absolute()

    if all(v for k, v in checks.items() if v is not None):
        print(f"  ✓ Plan {plan_number}: All checks passed")
    else:
        failed = [k for k, v in checks.items() if v is False]
        print(f"  ✗ Plan {plan_number}: Failed checks: {failed}")
```

### Step 3: Validate boundary_df (DSS Files)

**Check all DSS boundary condition references**:

```python
print("\nValidating Boundary Conditions (boundary_df)...")

if hasattr(ras, 'boundary_df') and ras.boundary_df is not None:
    for idx, row in ras.boundary_df.iterrows():
        if 'dss_file' in row and pd.notna(row['dss_file']):
            dss_path = Path(row['dss_file'])

            # CRITICAL: Check if absolute (causes GUI popup)
            if dss_path.is_absolute():
                print(f"  ✗ FAIL: Absolute DSS path: {dss_path}")
                print(f"    Will cause 'DSS path needs correction' GUI popup")
                print(f"    AUTOMATION BLOCKER - must fix")
                continue

            # Check if file exists
            if dss_path.exists():
                print(f"  ✓ PASS: DSS found: {dss_path}")
            else:
                # Try relative to project
                dss_resolved = ras.prj_file.parent / dss_path
                if dss_resolved.exists():
                    print(f"  ✓ PASS: DSS found (relative): {dss_path}")

                    # Validate DSS pathname contents
                    from ras_commander.dss import RasDss
                    catalog = RasDss.get_catalog(dss_resolved)
                    print(f"    Contains {len(catalog)} pathname(s)")

                    # Validate pathnames
                    for pathname in catalog['pathname']:
                        result = RasDss.check_pathname(dss_resolved, pathname)
                        if not result.is_valid:
                            print(f"    ⚠️ Invalid pathname: {pathname}")
                else:
                    print(f"  ✗ FAIL: DSS not found: {dss_path}")
                    print(f"    Model will not run")
```

### Step 4: Validate rasmap_df (Terrain Files)

**Check terrain file references**:

```python
print("\nValidating Terrain (rasmap_df)...")

if hasattr(ras, 'rasmap_df') and ras.rasmap_df is not None:
    for idx, row in ras.rasmap_df.iterrows():
        if 'terrain_file' in row and pd.notna(row['terrain_file']):
            terrain_path = Path(row['terrain_file'])

            # CRITICAL: Check if absolute
            if terrain_path.is_absolute():
                print(f"  ✗ FAIL: Absolute terrain path: {terrain_path}")
                print(f"    Will cause errors in RAS Mapper")
                continue

            # Check if file exists
            if terrain_path.exists():
                print(f"  ✓ PASS: Terrain found: {terrain_path}")

                # Validate using RasMap
                from ras_commander import RasMap
                is_valid = RasMap.is_valid_layer(terrain_path, layer_type='terrain')
                if is_valid:
                    print(f"    ✓ Terrain layer valid")
                else:
                    print(f"    ⚠️ Terrain layer validation failed")
            else:
                # Try relative to project
                terrain_resolved = ras.prj_file.parent / terrain_path
                if terrain_resolved.exists():
                    print(f"  ✓ PASS: Terrain found (relative): {terrain_path}")
                else:
                    print(f"  ✗ FAIL: Terrain not found: {terrain_path}")
                    print(f"    Model will not run")

                    # Search for terrain file
                    terrain_name = terrain_path.name
                    found = list(ras.prj_file.parent.glob(f'**/{terrain_name}'))
                    if found:
                        print(f"    Found at: {found[0]}")
                        print(f"    .rasmap needs correction to: {found[0].relative_to(ras.prj_file.parent)}")
```

### Step 5: Validation Summary

```python
print("\n" + "="*80)
print("Validation Summary")
print("="*80)

summary = {
    'plans_checked': len(ras.plan_df),
    'plans_valid': plans_valid_count,
    'dss_checked': dss_count,
    'dss_valid': dss_valid_count,
    'terrain_checked': terrain_count,
    'terrain_valid': terrain_valid_count,
    'absolute_paths_found': absolute_path_count,
    'all_checks_passed': all_checks_passed
}

print(f"\nPlans: {summary['plans_valid']}/{summary['plans_checked']} valid")
print(f"DSS Files: {summary['dss_valid']}/{summary['dss_checked']} valid")
print(f"Terrain Files: {summary['terrain_valid']}/{summary['terrain_checked']} valid")
print(f"Absolute paths: {summary['absolute_paths_found']}")

if summary['all_checks_passed']:
    print("\n✓ MODEL IS FULLY VALIDATED AND RUNNABLE")
    print("  - All paths are relative")
    print("  - All files exist")
    print("  - Ready for HEC-RAS")
    print("  - Ready for automation (no GUI popups)")
else:
    print("\n✗ MODEL HAS ISSUES")
    print("  See validation details above")
    print("  May need additional path corrections")

return summary
```

## Output Format

### Validation Report (agent/validation_report.md)

```markdown
# eBFE Model Validation Report

**Model**: {StudyArea} ({HUC8})
**Pattern**: {Pattern}
**Validated**: {Date}

## Validation Using ras-commander Dataframes

### Plan Validation (plan_df)
- Plans checked: X
- Plans valid: X
- HDF files found: X (pre-run results)
- Issues: {list any issues}

### Boundary Condition Validation (boundary_df)
- DSS files checked: X
- DSS files valid: X
- Absolute paths: X (FAIL if > 0)
- DSS pathnames validated: X,XXX
- Issues: {list any issues}

### Terrain Validation (rasmap_df)
- Terrain files checked: X
- Terrain files valid: X
- Absolute paths: X (FAIL if > 0)
- Issues: {list any issues}

## Overall Status

{✓ PASS or ✗ FAIL}

{If PASS}: Model is fully validated and runnable
{If FAIL}: See issues above, additional path corrections needed
```

### Validation Script (validate_{model}_{huc8}.py)

**Agent generates standalone script** for user to re-run validation

## See Also

- **eBFE Agent**: `.claude/agents/ebfe-organizer/SUBAGENT.md` - Complete agent
- **Path Validation**: `.claude/rules/validation/validation-patterns.md`
- **DSS Validation**: `.claude/rules/hec-ras/dss-files.md`
- **Critical Fixes**: `feature_dev_notes/eBFE_Integration/CRITICAL_FIXES.md`
