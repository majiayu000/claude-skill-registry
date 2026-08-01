---
name: ros2-core
description: "ROS 2 Jazzy core: rclcpp/rclpy, TF2 transforms, odometry/EKF fusion, node parameters, launch, QoS."
---

# ROS 2 Jazzy (Ubuntu 24.04 LTS) Core Development Instructions

## 1. Documentation Entry Points

Navigate within these rather than guessing deep URLs.

| For | Entry point |
| :--- | :--- |
| Jazzy concepts, tutorials, how-to guides | `https://docs.ros.org/en/jazzy/` |
| `rclcpp` C++ API index | `https://docs.ros.org/en/jazzy/p/rclcpp/` |
| `rclpy` Python API index | `https://docs.ros.org/en/jazzy/p/rclpy/` |
| Robot bringup: TF tree, odometry, EKF fusion | `https://docs.nav2.org/setup_guides/index.html` |

## 2. Symbols to Verify There (never write these from memory)

- **TF2** — `tf2_ros::TransformBroadcaster`, `tf2_ros::StaticTransformBroadcaster`, `tf2_ros::Buffer`, `tf2_ros::TransformListener`, `canTransform()`, `lookupTransform()`, `tf2::TimePointZero`, `tf2::ExtrapolationException`; message `geometry_msgs/msg/TransformStamped`. Frame conventions are REP 105 (`map` -> `odom` -> `base_link` -> `base_footprint` -> sensor frames) — see `ros2-troubleshooting`.
- **QoS** — `rclcpp::SensorDataQoS()` / `rclpy.qos.qos_profile_sensor_data` on sensor topics; inspect real endpoint QoS with `ros2 topic info <topic> -v`. The depth-only default (`create_subscription(..., 10)`) is RELIABLE + **VOLATILE** — not TRANSIENT_LOCAL; check the enum rather than asserting it.
- **Packaging & build wiring** — see `ros2-package`.

## 3. Local System Inspection & Interfaces (Ground Truth)
- **Message Definition Inspection**: `ros2 interface show <interface_name>` (e.g. `ros2 interface show nav_msgs/msg/Odometry` or `geometry_msgs/msg/TransformStamped`).
- **Package Installed Assets**: `ros2 pkg prefix <package_name>`
- **Live Topics / Params**: `ros2 topic list -t`, `ros2 param list <node_name>`.

## 4. Symptom -> Root Cause -> Action

| Symptom | Likely root cause | Action |
| :--- | :--- | :--- |
| Topic listed in `ros2 topic list` but subscriber receives nothing | Incompatible QoS: BestEffort publisher vs Reliable subscriber, or volatile pub vs transient_local sub | `check_qos_compat.py --topic <topic>` (bundled in `ros2-troubleshooting`) checks every pub/sub pair, or read `ros2 topic info <topic> -v`; align them (`SensorDataQoS` for sensors) |
| Nodes on two machines can't see each other | Different `ROS_DOMAIN_ID`/RMW implementations, or multicast blocked on the network | Match `ROS_DOMAIN_ID` and `RMW_IMPLEMENTATION`; test discovery with `ros2 multicast receive/send` |
| Timers/subscriptions starve while one callback runs | Single-threaded executor blocked by a long or blocking callback | `MultiThreadedExecutor` + `ReentrantCallbackGroup` for blocking work; never sleep in callbacks |
| Reported minimum range is absurdly small (or `nan` propagates) | `ranges` filtered for `inf` only; readings below `range_min` or above `range_max` and `nan` were kept | Keep a reading only if `math.isfinite(r) and msg.range_min <= r <= msg.range_max` — the message docs say values outside those bounds must be discarded |
| Node exits with `rcl_shutdown already called` / `ExternalShutdownException` on Ctrl-C or SIGTERM | `rclpy.shutdown()` called after the context is already down, or `spin()` interrupted without handling it | Catch `KeyboardInterrupt` **and** `rclpy.executors.ExternalShutdownException` around `spin()`, and guard teardown with `if rclpy.ok(): rclpy.shutdown()` |

## 5. Strict Coding Rules
1. Always match topic subscriber QoS to publisher QoS (e.g. `SensorDataQoS` for high-rate LiDAR/IMU/Odom topics).
2. Never trust a sensor array without bounds-checking it. For `LaserScan`, a value is usable only when finite **and** within `[range_min, range_max]`; filtering `inf` alone still lets `nan` and out-of-range readings through and produces a confidently wrong answer.
3. Make shutdown clean: wrap `spin()` so `KeyboardInterrupt` and `ExternalShutdownException` are caught, and only call `rclpy.shutdown()` when `rclpy.ok()`.
