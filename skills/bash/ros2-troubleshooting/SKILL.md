---
name: ros2-troubleshooting
description: "Troubleshooting: REP 103/105 ground-truth checks, TF/IMU/LiDAR misalignment, use_sim_time, lifecycle states, executor deadlocks, DDS domain conflicts."
---

# ROS 2 Troubleshooting & Physical Ground-Truth Verification Guide (Ubuntu 24.04 LTS & ROS 2 Jazzy)

## 1. Core Principles & Anti-Hallucination Protocol
- **Physical Ground-Truth Over Logic Assumptions**: Never claim a robot or sensor direction is correct based solely on code math. Always verify coordinate frame conventions (REP 103 body axes, REP 105 frame relations), physical sensor mounting orientations, and TF transformation trees.
- **REP 103 Body Coordinate Conventions**:
  - `+X`: Always points **Forward** (Linear velocity `cmd_vel.linear.x > 0` MUST move the robot body forward).
  - `+Y`: Always points **Left**.
  - `+Z`: Always points **Up**.
  - `+Yaw`: Counter-clockwise rotation (turning left).

## 1a. Runnable Ground-Truth Checks

These ship **next to this SKILL.md in `scripts/`** — resolve the path from this
skill's own directory, not the user's CWD (plugin install:
`${CLAUDE_PLUGIN_ROOT}/skills/ros2-troubleshooting/scripts/`). Source ROS 2
first. Exit code 0 = PASS, 1 = FAIL, 2 = no data.

**Invoke them with `python3` and a real path. They are plain scripts, not a ROS 2
package** — there is no package to `ros2 run`, and inventing one (`ros2 run
ros2_troubleshooting_helpers …`) is a known failure mode. Tell the user the exact
command you ran, e.g.:

```bash
source /opt/ros/jazzy/setup.bash
python3 ~/.claude/skills/ros2-troubleshooting/scripts/check_qos_compat.py --topic /scan
```

Run these before manual diagnosis — they turn the physical checks below into pass/fail facts:
- `check_imu_gravity.py [--topic /imu/data]` — robot at rest: gravity must be ~+9.81 on +Z (REP 103). Catches flipped/rotated IMU mounts.
- `check_odom_direction.py [--topic /odom]` — push the robot forward ~1 m; odometry displacement must be positive along heading. Catches inverted motors/encoders/TF.
- `check_tf_tree.py --sensors laser_frame,imu_link` — verifies `map->odom->base_link` resolves and prints each sensor mount as RPY degrees to compare against the physical mounting. It **always** prints a `VERIFY PHYSICALLY` advisory for a ~180 deg roll or yaw, including when that mounting is intentional — the advisory is a prompt to compare against the hardware, not a verdict that the TF is wrong. Do not tell the user a correct transform will pass without flagging.
- `check_qos_compat.py --topic /scan` — checks every publisher/subscriber pair on a topic for DDS QoS incompatibility. Catches the silent "topic publishes at 30 Hz but my subscriber receives nothing" case (BEST_EFFORT pub vs RELIABLE sub, VOLATILE pub vs TRANSIENT_LOCAL sub).

## 2. Physical Sensor & Motion Misalignment Diagnosis

### A. Inverted Sensor & Motion Symptom Checklist
- **Symptom 1: Robot moves backward when commanded forward (`cmd_vel.linear.x > 0`)**:
  - *Root Cause A*: Motor wiring / PWM sign inverted in hardware interface or diff drive controller.
  - *Root Cause B*: Wheel encoder direction reversed.
  - *Root Cause C*: Robot base TF frame `base_link` rotated 180 degrees (`yaw = 3.14159`) relative to world/odom frame.
  - *Action*: Inspect motor controller parameters `wheel_radius` / `left_wheel_radius_multiplier` / joint command signs. Verify body-frame displacement along forward heading while physically pushing robot forward.

- **Symptom 2: Nav2 costmap is upside down or obstacle points spawn behind the robot**:
  - *Root Cause*: LiDAR TF offset (`base_link` -> `laser_frame`) has an inverted roll/pitch/yaw (e.g. `roll = 3.14159` or `yaw = 3.14159`) because sensor was mounted upside-down or backwards.
  - *Action*: Run `ros2 run tf2_ros tf2_echo base_link laser_frame` and verify quaternions/RPY match physical mounting.

- **Symptom 3: EKF Odometry (`robot_localization`) diverges or spins wildly**:
  - *Root Cause A*: IMU `angular_velocity.z` sign is opposite to wheel odometry yaw rate during turns.
  - *Root Cause B*: Gravity vector in stationary IMU is on `+X` or `+Y` axis instead of `+Z` (~9.81 m/s²).
  - *Action*: Verify stationary IMU message `ros2 topic echo /imu/data`. `linear_acceleration.z` must be ~`+9.81` m/s² when resting flat.

## 3. Real-World System Failure Cases & Fixes

### A. Simulation & Clock Synchronization (`use_sim_time`)
- **Symptom**: TF lookup fails with `Lookup would require extrapolation into the past/future`, or Nav2 action goals freeze.
- **Root Cause**: `use_sim_time` is set to `true` on Gazebo/bag playback, but individual nodes run with wall time (`use_sim_time: false`).
- **Fix**: Ensure every node in simulation/bag playback sets `use_sim_time: true`:
  ```python
  Node(package='my_pkg', executable='my_node', parameters=[{'use_sim_time': True}])
  ```

### B. Nav2 Lifecycle Node State Transitions
- **Symptom**: Nav2 servers respond to CLI topic echo, but action goals return `Goal rejected` or time out.
- **Root Cause**: Lifecycle nodes (`controller_server`, `planner_server`, `amcl`) are stuck in `unconfigured` or `inactive` state.
- **Fix**: Check lifecycle states: `ros2 lifecycle get /controller_server`. Manually transition or configure `nav2_lifecycle_manager` to manage all lifecycle nodes.

### C. Executor Deadlocks & Async Callback Freezes
- **Symptom**: Calling `spin_until_future_complete` or `wait_for_service` inside a callback hangs the entire node.
- **Root Cause**: A single-threaded executor cannot process service responses while executing a blocking callback on the same thread.
- **Fix**: Use `MultiThreadedExecutor` and assign separate `ReentrantCallbackGroup` to async service clients / action calls.

### D. URDF Self-Collision & MoveIt 2 Freeze
- **Symptom**: MoveIt 2 motion planner immediately fails with `No valid path found` or `State in collision`.
- **Root Cause**: Collision geometries in URDF overlap (e.g. gripper colliding with wrist link) or SRDF Allowed Collision Matrix (ACM) is missing.
- **Fix**: Regenerate SRDF ACM using MoveIt Setup Assistant to disable collision checking for adjacent fixed joints.

### E. DDS Multicast & Domain ID Interference (`ROS_DOMAIN_ID`)
- **Symptom**: Unrelated robots or PCs on the same Wi-Fi receive duplicate topics or experience high packet loss.
- **Root Cause**: Default `ROS_DOMAIN_ID=0` shared across local network.
- **Fix**: Set a unique `export ROS_DOMAIN_ID=N` (0-101 safe on Linux; higher IDs may collide with OS ephemeral ports) per developer/robot.

## 4. Step-by-Step Diagnostic Decision Tree

```
[Issue Reported]
   │
   ├── Clock / TF Extrapolation Error?
   │     └── Verify `use_sim_time: true` on ALL nodes when running Gazebo or Rosbag
   │
   ├── Nav2 Action Goal Rejected?
   │     └── Run `ros2 lifecycle get /controller_server` (Must be `active`)
   │
   ├── Robot moves in wrong direction / TF inverted?
   │     ├── Step 1: Push robot forward 1 meter by hand  `ros2 topic echo /odom` (twist.twist.linear.x must be positive; position displacement along body heading must be positive)
   │     ├── Step 2: Turn robot left by hand  `ros2 topic echo /imu/data` (angular_velocity.z must be positive)
   │     └── Step 3: Check Static TF  `ros2 run tf2_ros tf2_echo base_link laser_frame`
   │
   └── Node freezes on async call / service?
         └── Replace single-threaded blocking spin with `MultiThreadedExecutor` & `ReentrantCallbackGroup`
```

## 5. Common Anti-Patterns & Prevention Rules

| Anti-Pattern | Correct Pattern / Fix |
| :--- | :--- |
| Changing sign in application logic to fix inverted motor | Fix motor direction in `ros2_control` config or hardware interface, NOT in application code |
| Hardcoding frame names without leading `/` inconsistencies | Standardize frame IDs (`map`, `odom`, `base_link`, `laser_frame`) without leading slashes |
| Mismatch between publisher (`BestEffort`) & subscriber (`Reliable`) | Explicitly set `rclcpp::SensorDataQoS()` on sensor subscribers |
| Blocking `spin_until_future_complete` inside a callback | Use `MultiThreadedExecutor` or async done callbacks |

## 6. Official References
- **REP 103 Standard Units & Coordinate Conventions**: `https://www.ros.org/reps/rep-0103.html`
- **REP 105 Coordinate Frames**: `https://www.ros.org/reps/rep-0105.html`
- **ROS 2 TF2 Concepts**: `https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Tf2.html`
