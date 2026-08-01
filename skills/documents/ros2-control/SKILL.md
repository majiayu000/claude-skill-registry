---
name: ros2-control
description: "ros2_control: controller manager, hardware interfaces, URDF ros2_control tags, controller spawners."
---

# ros2_control Development Instructions (Ubuntu 24.04 LTS & ROS 2 Jazzy)

## 1. Architecture

`ros2_control` decouples hardware drivers (`hardware_interface::SystemInterface`, `ActuatorInterface`, `SensorInterface`) from controller logic (`diff_drive_controller`, `joint_trajectory_controller`). Interface names are exactly `position`, `velocity`, `effort` — verify which ones your controller requires before writing the URDF.

## 2. Documentation Entry Points

| For | Entry point |
| :--- | :--- |
| Everything (Jazzy docs root — architecture, getting started, demos) | `https://control.ros.org/jazzy/index.html` |
| Per-controller parameter reference | `https://control.ros.org/jazzy/doc/ros2_controllers/doc/controllers_index.html` |

## 3. Wiring

The URDF `<ros2_control name="..." type="system">` block declares one
`<hardware><plugin>` and, per joint, the `<command_interface>` the controller
will write and the `<state_interface>` entries it reads back.

Controllers are started by the `spawner` executable from the `controller_manager`
package, passed `--controller-manager` with the actual namespace. `joint_state_broadcaster`
is **not** started automatically and must be spawned before the others, or
`/joint_states` stays silent and the robot model renders gray in RViz.

## 4. Symptom -> Root Cause -> Action

| Symptom | Likely root cause | Action |
| :--- | :--- | :--- |
| `diff_drive_controller` active, `/cmd_vel` published, nothing moves | In Jazzy `diff_drive_controller` subscribes to **`geometry_msgs/msg/TwistStamped` only** — a plain `Twist` publisher never matches, silently. There is **no `use_stamped_vel` parameter** in Jazzy; do not invent one | Publish `TwistStamped`, or put a `twist_stamper` between your `Twist` source and the controller. Confirm the subscribed type with `ros2 topic info /cmd_vel -v` |
| Spawner times out waiting for `/controller_manager` | controller_manager not running, wrong namespace, or `use_sim_time` mismatch delaying clock | Check `ros2 node list` for controller_manager; pass `--controller-manager` with the actual namespace |
| Controller activation fails with resource/interface conflict | Two controllers claim the same `command_interface` | `ros2 control list_hardware_interfaces` — check which interfaces are claimed; deactivate the conflicting controller |
| Controller loads then fails to configure | Params YAML not passed to controller_manager, or controller type string wrong | Verify params file reaches the `ros2_control_node`/`gz_ros2_control` node; check `type:` matches installed plugin (`ros2 control list_controller_types`) |
| Hardware activates but robot doesn't move on commands | Command interface names in URDF `<ros2_control>` don't match what the controller expects (`velocity` vs `position`), or hardware `write()` not implemented | Compare `ros2 control list_hardware_interfaces` vs controller's required interfaces |
| Odometry from `diff_drive_controller` drifts vs real distance | `wheel_radius` / `wheel_separation` don't match the physical chassis | Measure the real chassis; verify with `check_odom_direction.py` (bundled in `ros2-troubleshooting`) after fixing |
| Robot drives backward on forward command, logs look fine | Wheel joint axis flipped in URDF, or motor polarity inverted in hardware interface | Fix sign at the hardware interface or joint axis — never patch it in application code |

## 5. Calibration Baselines (`diff_drive_controller`)
Real hardware never matches CAD — tire deformation under load makes the effective wheel radius and separation differ from the measured chassis, so measure, then correct with the built-in multipliers rather than fudging the geometry:
1. **`wheel_radius`**: drive a measured straight line (e.g. 2.0 m by tape). Reported/actual ratio -> correct via `left_wheel_radius_multiplier` / `right_wheel_radius_multiplier` (baseline 1.0).
2. **`wheel_separation`**: rotate the robot exactly 5 full turns in place; error in reported yaw -> correct via `wheel_separation_multiplier` (baseline 1.0). Separation has no effect on straight-line driving, so fix the radius first or it contaminates this test.
3. Re-verify after every tire/load change with `check_odom_direction.py` (bundled in `ros2-troubleshooting`); straight-line drift to one side usually means the two radius multipliers need to differ slightly.
