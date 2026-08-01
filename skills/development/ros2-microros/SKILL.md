---
name: ros2-microros
description: "micro-ROS: agent, rclc client API, micro_ros_setup, custom transports, static memory."
---

# micro-ROS Instructions (Ubuntu 24.04 LTS & ROS 2 Jazzy)

## 1. Architecture

micro-ROS connects constrained MCUs (STM32, ESP32, FreeRTOS, Zephyr) to the ROS 2 DDS graph via `micro_ros_agent` + the `rclc` client library over Micro XRCE-DDS. Static memory pools (`rmw_microxrcedds`) give zero steady-state heap allocation when `RMW_UXRCE_ALLOW_DYNAMIC_ALLOCATIONS=OFF`.

## 2. Documentation Entry Points

| For | Entry point |
| :--- | :--- |
| Tutorials, supported boards, transports | `https://micro.ros.org/` |
| Firmware build system (`micro_ros_setup`) | `https://github.com/micro-ROS/micro_ros_setup` |
| `rclc` executor / node API source | `https://github.com/ros2/rclc` |

## 3. Key Concepts & Patterns

### A. Embedded Client Node Setup (`rclc` in C)
```c
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>

int main(void) {
  rcl_allocator_t allocator = rcl_get_default_allocator();
  rclc_support_t support = {0};
  rcl_node_t node = {0};
  rcl_publisher_t pub = {0};

  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "mcu_node", "", &support);
  rclc_publisher_init_default(&pub, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32), "chatter");

  // Clean up
  rcl_publisher_fini(&pub, &node);
  rcl_node_fini(&node);
  rclc_support_fini(&support);
  return 0;
}
```

### B. Micro-ROS Agent Execution
```bash
# Serial Transport (e.g. UART to USB)
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -b 115200

# UDP Transport
ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888
```

## 4. Symptom -> Root Cause -> Action

| Symptom | Likely root cause | Action |
| :--- | :--- | :--- |
| MCU node vanishes from graph after MCU reset, agent still running | XRCE session not re-created; firmware assumes a one-time init | Add a reconnect state machine: `rmw_uros_ping_agent()` periodically, re-init entities on failure |
| `rclc_support_init` returns error on the MCU | Transport not reachable (wrong serial dev/baud, UDP port/IP) | Run the agent with `-v6` verbose and watch for session establishment; verify transport config in firmware |
| Publisher works but subscriber callback never fires | Executor never spun, or `rclc_executor_init` handle count smaller than the number of subscriptions/timers | Spin the executor in the main loop; count every subscription+timer+service in `num_handles` |
| Hard fault / crash when publishing string or sequence messages | Message memory not allocated — rclc doesn't auto-allocate unbounded fields | Allocate with `micro_ros_utilities_create_message_memory` or assign static buffers before publishing |
| Large messages never arrive | Payload exceeds XRCE-DDS stream/MTU buffer configured in the firmware | Increase the transport MTU/stream buffer in the colcon.meta / transport config, or shrink the message |
| Best-effort topics flood then stall on serial | Serial bandwidth saturated: publish rate x message size exceeds baud rate | Lower publish rate, raise baud rate, or switch to UDP transport |
