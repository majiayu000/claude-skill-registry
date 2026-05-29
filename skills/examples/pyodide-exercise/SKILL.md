---
name: "pyodide-exercise"
description: "Create browser-based Python exercises using Pyodide. Use for interactive coding without local setup."
version: "0.1.0"
status: "placeholder"
---

# Pyodide Exercise Skill

**Purpose**: Create interactive Python exercises that run in the browser using Pyodide.

## When to Use

- Creating hands-on coding exercises
- Building Tier 1 alternatives for GPU-required content
- Making robotics concepts accessible without hardware

## Capabilities

| Feature | Support |
|---------|---------|
| Python 3.11 | Full |
| NumPy | Yes |
| Matplotlib | Yes (inline) |
| Custom modules | Via micropip |
| MockROS | Custom bridge |

## Exercise Structure

```
<PythonRunner>
  - Initial code (editable)
  - Test cases (hidden or visible)
  - Expected output
  - Hints (progressive)
</PythonRunner>
```

## Output

- PythonRunner component with exercise
- Pre-loaded imports
- Test validation logic
- Success/failure feedback

## Integration

- Used by lesson-generator for interactive exercises
- Works with MockROSBridge for ROS simulation
- Integrated with RobotViewer for visualization

---

**Status**: Placeholder - To be implemented for interactive lab component (Phase 6).
