---
name: "ros2-custom-interfaces"
description: "Generate ROS 2 custom message (.msg) and service (.srv) interface definitions for educational content. This skill should be used when creating lessons that teach interface design, writing exercises involving custom data types, or generating worked examples for robotics communication protocols."
version: "1.0.0"
status: "active"
---

# ROS 2 Custom Interfaces Skill

**Purpose**: Generate accurate, educational ROS 2 custom message and service interface definitions following official ROS 2 Humble patterns for the Physical AI textbook.

## When to Use

- Creating lessons in Chapter 5 (Communication Mastery - Lesson 3)
- Writing interface design exercises
- Generating worked examples for custom robot data types
- Teaching .msg and .srv file format and build process

## Live Documentation Access

**CRITICAL**: Before generating any code, fetch current ROS 2 documentation using Context7 MCP:

```
Tool: mcp__context7__resolve-library-id
libraryName: "ros2 custom interfaces"

Then:
Tool: mcp__context7__get-library-docs
context7CompatibleLibraryID: [resolved ID]
topic: "custom msg srv interfaces"
```

This ensures interface patterns match current ROS 2 Humble conventions.

## Interface Definition Patterns

### Custom Message (.msg) Pattern

```
# File: msg/RobotStatus.msg
# Custom message for robot status reporting

# Header with timestamp
builtin_interfaces/Time stamp

# Robot identification
string robot_name
int32 robot_id

# Status information
bool is_active
float64 battery_level      # 0.0 to 100.0
float64[] joint_positions  # Array of joint angles in radians

# Nested message (from geometry_msgs)
geometry_msgs/Pose current_pose
```

### Custom Service (.srv) Pattern

```
# File: srv/MoveRobot.srv
# Custom service for robot movement commands

# Request
string target_frame
geometry_msgs/Point target_position
float64 speed_factor  # 0.0 to 1.0
---
# Response
bool success
string message
float64 time_to_reach  # Estimated seconds
```

## Package Structure for Interfaces

```
my_robot_interfaces/
├── CMakeLists.txt
├── package.xml
├── msg/
│   ├── RobotStatus.msg
│   └── SensorData.msg
└── srv/
    ├── MoveRobot.srv
    └── GetStatus.srv
```

### CMakeLists.txt (Essential Parts)

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_interfaces)

find_package(ament_cmake REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotStatus.msg"
  "msg/SensorData.msg"
  "srv/MoveRobot.srv"
  "srv/GetStatus.srv"
  DEPENDENCIES builtin_interfaces geometry_msgs
)

ament_package()
```

### package.xml (Essential Parts)

```xml
<?xml version="1.0"?>
<package format="3">
  <name>my_robot_interfaces</name>
  <version>0.1.0</version>
  <description>Custom interfaces for robot communication</description>
  <maintainer email="you@example.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>rosidl_default_generators</buildtool_depend>

  <depend>builtin_interfaces</depend>
  <depend>geometry_msgs</depend>

  <member_of_group>rosidl_interface_packages</member_of_group>
</package>
```

## Built-in Types Reference

### Primitive Types
| Type | Description | Python Equivalent |
|------|-------------|-------------------|
| bool | Boolean | bool |
| byte | 8-bit unsigned | int |
| char | 8-bit char | str (single char) |
| float32 | 32-bit float | float |
| float64 | 64-bit float | float |
| int8/16/32/64 | Signed integers | int |
| uint8/16/32/64 | Unsigned integers | int |
| string | UTF-8 string | str |

### Array Types
| Syntax | Description |
|--------|-------------|
| `float64[]` | Unbounded array |
| `float64[3]` | Fixed-size array (3 elements) |
| `float64[<=10]` | Bounded array (max 10) |

### Common Standard Message Types
- `std_msgs/String`, `std_msgs/Int32`, `std_msgs/Bool`
- `geometry_msgs/Point`, `geometry_msgs/Pose`, `geometry_msgs/Twist`
- `sensor_msgs/Image`, `sensor_msgs/LaserScan`, `sensor_msgs/JointState`
- `builtin_interfaces/Time`, `builtin_interfaces/Duration`

## Educational Requirements

### Layer 1 (Manual Foundation)
- Explain why custom interfaces needed (type safety, documentation)
- Walk through .msg/.srv file format
- Demonstrate build process with colcon

### Layer 2 (AI Collaboration)
- Design interface from natural language requirements
- Iterate on interface design with AI feedback
- Generate boilerplate package structure (Three Roles INVISIBLE)

### Layer 3 (Intelligence Design)
- Interface versioning strategies
- Designing for extensibility
- Standard vs custom interface decision framework

## Hardware Tier Compatibility

**Note**: Interface packages require compilation with colcon.

- **Tier 1**: Cloud ROS 2 workspace with colcon build
- **Tier 2+**: Local ROS 2 Humble installation

Build commands:
```bash
cd ~/ros2_ws
colcon build --packages-select my_robot_interfaces
source install/setup.bash
```

## Common Mistakes to Prevent

1. **Missing DEPENDENCIES**: Always list dependent packages in CMakeLists.txt
2. **Wrong member_of_group**: Must include `rosidl_interface_packages`
3. **Type mismatches**: Python uses float for float32/float64, int for all integers
4. **Forgetting to source**: Must source install/setup.bash after build

## Interface Design Decision Framework

**Create Custom Message When:**
- Standard messages don't capture your data structure
- You need semantic meaning (RobotStatus vs generic struct)
- Multiple nodes will use the same data format
- Type checking prevents bugs

**Use Standard Messages When:**
- Data fits existing types (Point, Pose, Twist)
- Interoperability with existing tools needed
- Rapid prototyping (avoid build cycle)

## Integration with Other Skills

- **ros2-publisher-subscriber**: Using custom messages in pub/sub
- **ros2-service-pattern**: Using custom services
- **ros2-launch-system**: Building interface packages in workspace

## Authoritative Source

All patterns verified against: https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html
