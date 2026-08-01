---
name: ros2-dev
description: "Nav2 & SLAM: AMCL, costmaps, MPPI/DWB/Smac plugins, behavior trees, SLAM Toolbox, RTAB-Map, Isaac ROS VSLAM, docking."
---

# Nav2 & SLAM Development (Ubuntu 24.04 LTS & ROS 2 Jazzy)

## 1. Establish first (Nav2-specific; the general gates are in `CLAUDE.md`)

Nav2 config is only correct relative to a specific robot. Ask if unstated:

- **Footprint / inscribed radius** — `inflation_radius` and every "won't fit through the door" complaint depend on it. A default copied from a tutorial robot is the most common root cause of bad navigation.
- **Drive type** — diff / omni / ackermann. Sets `motion_model` and rules out planners (car-like needs `SmacPlannerHybrid`).
- **Where does `map -> odom` come from** — AMCL, SLAM Toolbox, or RTAB-Map? Exactly one may publish it. Two is a silent conflict.
- **Modifying an existing `nav2_params.yaml` or starting fresh?** Modify in place when one exists; a wholesale replacement silently drops the robot-specific values already tuned into it.

## 2. The loop

1. **Read the shipped defaults first** — `/opt/ros/$ROS_DISTRO/share/nav2_bringup/params/nav2_params.yaml`. This is the baseline for every value you write; never emit a parameter you haven't seen there or in the docs.
2. **Verify odometry and TF physically before touching Nav2 params.** Bad odom cannot be fixed by tuning — `check_odom_direction.py`, `check_tf_tree.py --sensors laser_frame` (bundled in `ros2-troubleshooting`).
3. **Write the config**, changing one thing at a time from the baseline.
4. **Prove it**: all lifecycle servers `active` (`ros2 lifecycle get /controller_server`), a goal is accepted, and the robot actually moves. "The YAML looks right" is not done.

## 3. Plugin strings are fully namespaced

The single most common startup-killing error is dropping the package prefix:

```yaml
plugin: "nav2_mppi_controller::MPPIController"   # correct
plugin: "mppi_controller::MPPIController"        # server loads nothing, Nav2 dies at startup
```

Confirm the string against the shipped defaults file before writing it.

## 4. Symptom -> Root Cause -> Action

| Symptom | Likely root cause | Action |
| :--- | :--- | :--- |
| Action goals return `Goal rejected` / freeze while topics look fine | Lifecycle servers stuck `unconfigured`/`inactive` | `ros2 lifecycle get /controller_server` etc.; check `nav2_lifecycle_manager` `node_names` covers all servers |
| `Timed out waiting for transform` / extrapolation errors | `use_sim_time` inconsistent across nodes, or `map->odom` publisher missing | Verify every node's `use_sim_time`; confirm exactly ONE of AMCL/SLAM publishes `map->odom` |
| Costmap empty even though `/map` is published | QoS mismatch: map_server publishes `transient_local`, subscriber uses volatile durability | Set subscriber durability to `transient_local`; check `ros2 topic info /map -v` |
| Obstacles appear but never clear from costmap | `raytrace_max_range` <= `obstacle_max_range` in obstacle layer | Set raytrace range slightly larger than obstacle range |
| "No valid trajectory" / robot refuses to move near obstacles | Inflation too large for footprint, or velocity limits effectively zero | Compare `inflation_radius` + `footprint` vs corridor width; check `min_vel_x`/`max_vel_x` actually nonzero |
| AMCL pose diverges while driving | Odometry noise params unrealistic, or initial pose never set | Set initial pose; sanity-check odom quality first (`check_odom_direction.py`), then tune `alpha1-4` |
| MPPI oscillates / prefers reversing | Critic weights: `PreferForwardCritic` too weak vs `PathAlignCritic` | Raise `PreferForwardCritic.cost_weight`; verify against the shipped defaults as baseline |
| Path planned through walls | Static layer not enabled in global costmap, or wrong `map_topic` | Check global costmap `plugins` list includes static layer and its `map_topic` |
| Controller server won't load a plugin at startup | Plugin string missing its package namespace (see §3) | Copy the exact string from the shipped defaults |

## 5. Reference (load only when you need it)

- **`references/symbols.md`** — doc entry points, plugin/critic/planner/BT node names, costmap layers, SLAM packages. Read this before naming anything.
- **`references/tuning.md`** — AMCL, costmap, MPPI and slam_toolbox baselines with tune-in-this-direction guidance. Read this when the robot moves but behaves badly.

## 6. Strict Rules
1. Never mix obsolete ROS 1 `move_base` or ROS 2 Foxy parameter names.
2. Exactly one node publishes `map -> odom`. Verify which before adding another localization source.
3. Never tune Nav2 solely in simulation — sim uses ideal kinematics; re-verify on hardware.
