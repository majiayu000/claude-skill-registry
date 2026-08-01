---
name: ros2-testing
description: "Testing: launch_testing, gtest/pytest, rosbag2 C++/Python APIs, ros2trace profiling."
---

# ROS 2 Testing, Rosbag2 & Tracing Instructions (Ubuntu 24.04 LTS & ROS 2 Jazzy)

## 1. Documentation Entry Points

| For | Entry point |
| :--- | :--- |
| Testing tutorials (CLI, gtest, pytest, integration) | `https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Testing/` |
| `launch_testing` / `rosbag2_cpp` / `rosbag2_py` API | `https://docs.ros.org/en/jazzy/p/<package>/` |
| rosbag2 source of truth | `https://github.com/ros2/rosbag2` |

## 2. Running Tests

`colcon test` only prints a summary, so read results with `colcon test-result --all --verbose` — without `--verbose` you cannot see which case failed, and a test that was never registered with the build looks identical to a passing one, so confirm the expected test count rather than the exit code.

## 3. Key Concepts & Code Patterns

### A. Programmatic Rosbag2 Writer (C++)
```cpp
#include <rosbag2_cpp/writer.hpp>
#include <std_msgs/msg/string.hpp>

rosbag2_cpp::Writer writer;
writer.open("my_bag");
writer.create_topic({0, "chatter", "std_msgs/msg/String", "cdr", {}, ""});
writer.write<std_msgs::msg::String>(msg, "chatter", clock.now());
```

### B. Integration Testing (`launch_testing` Python)

In `generate_test_description()`, return a `LaunchDescription` ending in `launch_testing.actions.ReadyToTest()` — everything before it is launch setup, plain `unittest.TestCase` classes run after it against the live processes, and `@launch_testing.post_shutdown_test()` classes run once the processes have exited (where `launch_testing.asserts.assertExitCodes(proc_info)` belongs).

## 4. Symptom -> Root Cause -> Action

| Symptom | Likely root cause | Action |
| :--- | :--- | :--- |
| Node under test never receives the test publisher's messages | QoS mismatch between test fixture and node — same silent DDS failure as production | Match the node's QoS in the fixture; see `ros2-troubleshooting` (`check_qos_compat.py`) |
| Rosbag2 playback in a test produces no callbacks | Bag recorded with `use_sim_time` semantics but the test runs on wall clock, or `/clock` not published during playback | Align `use_sim_time` across the test nodes; play with `--clock` when the bag drives time |
