---
name: URDF Validator & Fixer
description: Pre-import validation and auto-fix for URDF files targeting Isaac Sim / USD
---

# URDF Validator & Fixer

Validate and fix URDF files before importing into Isaac Sim. Catches USD naming violations, duplicate materials, unbounded joint limits, missing inertial properties, and broken mesh references — problems that otherwise cause silent import failures.

## Workflow

Follow this sequence for best results:

### Phase 1: Inspect
Get a structural overview of the robot model.

```
urdf_inspect(file_path="/path/to/robot.urdf")
```

Review: link/joint counts, kinematic tree, mass distribution, mesh files.

### Phase 2: Validate
Check for all known issues.

```
urdf_validate(file_path="/path/to/robot.urdf")
```

Review: issues by severity (error > warning > info) and category.

### Phase 3: Fix
Auto-fix what can be fixed.

```
urdf_fix(
    file_path="/path/to/robot.urdf",
    output_path="/path/to/robot_fixed.urdf"
)
```

The original file is **never modified**. Check `name_mapping` in the result — if links or joints were renamed, downstream code (controllers, configs) needs updating too.

### Phase 4: Re-validate
Confirm fixes resolved the issues.

```
urdf_validate(file_path="/path/to/robot_fixed.urdf")
```

Expect zero errors for fixed categories. Remaining warnings (e.g., missing collision geometry, package:// URIs) may need manual attention.

## Tool Reference

### `urdf_validate`
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_path` | str | None | Path to URDF file |
| `urdf_string` | str | None | URDF XML as string |
| `categories` | list[str] | all | Filter: `usd_naming`, `materials`, `joint_limits`, `inertial`, `collision`, `mesh_references` |
| `min_severity` | str | "info" | Minimum: `error`, `warning`, `info` |

### `urdf_fix`
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_path` | str | None | Path to URDF file |
| `urdf_string` | str | None | URDF XML as string |
| `output_path` | str | auto | Output file path (default: `*_fixed.urdf`) |
| `fix_categories` | list[str] | all | `usd_naming`, `materials`, `joint_limits`, `inertial` |
| `default_mass` | float | 0.1 | Default mass (kg) for missing inertial |
| `default_inertia` | float | 0.001 | Default diagonal inertia value |
| `max_joint_position` | float | 2π | Replace ±inf position limits |
| `max_joint_velocity` | float | π | Default velocity limit (rad/s) |
| `max_joint_effort` | float | 100.0 | Default effort limit (Nm) |

### `urdf_inspect`
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_path` | str | None | Path to URDF file |
| `urdf_string` | str | None | URDF XML as string |

## Validation Categories

| Category | What it checks | Auto-fixable? |
|----------|---------------|---------------|
| `usd_naming` | Hyphens, dots, spaces, leading digits in link/joint/material names | Yes — renames + updates all references |
| `materials` | Duplicate definitions with different RGBA, missing textures, JPEG warnings | Yes — deduplicates by appending suffix |
| `joint_limits` | Infinite limits, missing effort/velocity, missing `<limit>` element | Yes — clamps to configurable defaults |
| `inertial` | Missing `<inertial>`, zero/negative mass, zero inertia tensor | Yes — adds configurable defaults |
| `collision` | Visual geometry without corresponding collision geometry | No — requires manual modeling |
| `mesh_references` | Nonexistent mesh files, `package://` URIs | No — mesh files must exist on disk |

## Isaac Sim Tips

- **USD naming is critical**: Isaac Sim converts URDF names to USD prim paths. Hyphens, dots, and spaces cause silent failures or mangled paths.
- **Inertial is required**: Links without `<inertial>` may be silently skipped or cause physics instability.
- **Joint limits matter**: Infinite limits can cause solver divergence. Isaac Sim may clamp them internally but the behavior is undefined.
- **`package://` URIs won't resolve**: Isaac Sim doesn't have ROS package resolution. Convert to relative or absolute paths.
- **Fixed joints get merged**: By default Isaac Sim merges fixed joints. If you need them separate, set `merge_fixed_joints = False` in import config.

## Common Pitfalls

1. **Renaming breaks downstream code**: After USD naming fixes, joint names change. Update your controller configs, ROS topics, and any code referencing joint names by checking the `name_mapping` output.
2. **Default inertial values are placeholders**: The auto-fix adds small default values to prevent crashes. Replace them with actual CAD-derived values for accurate simulation.
3. **Collision geometry affects performance**: Missing collision geometry means no contact detection for that link. Add simplified collision meshes for physics-critical links.
4. **Mesh paths are relative to URDF location**: When moving a fixed URDF to a different directory, mesh references may break. Keep the URDF and mesh directories together.

## End-to-End Verification

After fixing, verify the import works in Isaac Sim:

```bash
/path/to/isaacsim/python.sh scripts/verify_urdf_isaac_sim.py \
    --original /path/to/robot.urdf \
    --fixed /path/to/robot_fixed.urdf
```

This script imports both URDFs headless, checks prim paths, joints, articulation, and runs physics steps to verify stability.
