---
name: calhacks-agenticrobot
description: This guide sets up MERLIN to control XLeRobot in ManiSkill simulation
  for sim2real validation.
---

# ManiSkill + XLeRobot Setup Guide

This guide sets up MERLIN to control XLeRobot in ManiSkill simulation for sim2real validation.

## Quick Setup (15 minutes)

### 1. Create ManiSkill Environment

```bash
# Create separate conda env for ManiSkill
conda create -y -n merlin-sim python=3.11
conda activate merlin-sim

# Install ManiSkill and dependencies
pip install mani-skill pygame rerun-sdk

# Download ReplicaCAD scene dataset
python -m mani_skill.utils.download_asset "ReplicaCAD"
```

### 2. Install XLeRobot Files in ManiSkill

1. **Download XLeRobot simulation files:**
   - Clone: `https://github.com/xle-robots/xle-robot`
   - Navigate to: `sim/maniskill/` folder

2. **Copy to ManiSkill package:**
   ```bash
   # Find your ManiSkill installation
   MANI_PATH=$(python -c "import mani_skill; print(mani_skill.__path__[0])")

   # Copy XLeRobot files
   cp -r xle-robot/sim/maniskill/agents/xlerobot/ $MANI_PATH/agents/robots/
   cp -r xle-robot/sim/maniskill/assets/xlerobot/ $MANI_PATH/assets/robots/
   cp -r xle-robot/sim/maniskill/envs/scenes/* $MANI_PATH/envs/scenes/
   ```

3. **Register XLeRobot in ManiSkill:**
   ```bash
   # Edit: $MANI_PATH/agents/robots/__init__.py
   # Add: from .xlerobot import *
   ```

### 3. Test ManiSkill Standalone

```bash
# Test ManiSkill works with XLeRobot
python -m mani_skill.examples.demo_ctrl_action \
  -e "ReplicaCAD_SceneManipulation-v1" \
  -r "xlerobot_single" \
  --render-mode="human" \
  --shader="default" \
  -c "pd_joint_delta_pos"
```

**Expected:** XLeRobot appears in 3D scene, can accept keyboard commands.

### 4. Run MERLIN with ManiSkill

```bash
# Activate MERLIN environment (with ManiSkill installed)
conda activate merlin-sim

# Set PYTHONPATH to MERLIN
export PYTHONPATH=/path/to/calhacks:$PYTHONPATH

# Run agent mission in ManiSkill
python examples/test_maniskill.py
```

**Expected:**
- ManiSkill environment loads
- Agent executes pick-and-place in sim
- Results printed to console

### 5. Full Integration Test

```bash
# Run MERLIN with ManiSkill backend
python main.py --backend maniskill --agent simple --mission "Pick and place demo"
```

**Expected Output:**
```json
{
  "ok": true,
  "backend": "maniskill",
  "agent": "SimpleAgent",
  "mission": "Pick and place demo",
  "result": "Mission complete:\nInitial status: battery=95.0%\nNavigated to object at [...]\n..."
}
```

## Architecture

```
┌─────────────────────────────────────┐
│        SimpleAgent                  │
│   (hardcoded pick-and-place)        │
└──────────────┬──────────────────────┘
               │ agent.run_mission()
               ▼
┌──────────────────────────────────────┐
│     MCP Server (5 tools)             │
│  navigate_to, grasp, release, etc    │
└──────────────┬──────────────────────┘
               │ execute_tool()
               ▼
┌──────────────────────────────────────┐
│    StateMachine (60 Hz loop)         │
│  IDLE → NAVIGATING → MANIPULATING    │
└──────────────┬──────────────────────┘
               │ state-specific logic
               ▼
┌──────────────────────────────────────┐
│  ManiSkillController                 │
│  (XLeRobot in ReplicaCAD scene)      │
└──────────────┬──────────────────────┘
               │ gymnasium API
               ▼
    XLeRobot Robot (Physics Sim)
     - 7 DOF arm
     - gripper
     - sensors
```

## Next Steps

### Immediate (sim validation)
1. Run `test_maniskill.py` and verify agent controls robot
2. Modify mission prompts to test different behaviors
3. Add custom control policies in `_build_action()` method

### Before Real Hardware
1. Record trajectories from successful sim missions
2. Test transfer learning (sim → real)
3. Validate gripper force/torque limits
4. Test emergency stop procedures

### Real Hardware (XLE Robot)
1. Create `XLEController` backend (rest API or ROS2)
2. Test low-level commands match sim
3. Validate sensor readings
4. Deploy trained agents

## Troubleshooting

### ManiSkill import error
```
Error: cannot import mani_skill.envs
Solution: pip install --upgrade mani-skill
```

### XLeRobot files not found
```
Error: Robot xlerobot_single not registered
Solution: Verify XLeRobot files copied to ManiSkill package
         Check /agents/robots/__init__.py has xlerobot import
```

### Slow simulation
```
Solution 1: Use --shader="default" (faster than ray-tracing)
Solution 2: Reduce render resolution or use headless mode
Solution 3: Upgrade GPU drivers
```

### Observation extraction failing
```
Solution: Print env.observation_space to see observation keys
         Modify _extract_pose() in maniskill.py to match actual keys
```

## Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Sim step latency | 10-50ms | Depends on render mode |
| Physics accuracy | High | Calibrated for XLeRobot |
| Gripper simulation | Binary (open/close) | Realistic forces in production |
| Camera simulation | Yes | Can capture RGB/depth for vision |

## Files Modified

- `merlin/hardware/maniskill.py` - ManiSkillController (new)
- `merlin/hardware/__init__.py` - Factory support (updated)
- `examples/test_maniskill.py` - Integration test (new)
- `SETUP_MANISKILL.md` - This guide (new)

## Resources

- [XLeRobot Documentation](https://xle-robots.github.io)
- [ManiSkill Documentation](https://mani-skill.org)
- [ManiSkill XLeRobot Setup](https://github.com/xle-robots/xle-robot/tree/main/sim/maniskill)
- [MERLIN Architecture](./subsystem_plans/05_SYSTEM_ARCHITECTURE.md)

---

**Ready to validate your robot missions in simulation before real hardware! 🚀**
