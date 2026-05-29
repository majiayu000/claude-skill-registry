---
name: "ros2-launch-system"
description: "Generate ROS 2 Python launch files and multi-node system configurations for educational content. This skill should be used when creating lessons that teach launch file syntax, writing exercises involving multi-node startup, parameter configuration, or generating worked examples for robot system deployment."
version: "1.0.0"
status: "active"
---

# ROS 2 Launch System Skill

**Purpose**: Generate accurate, educational ROS 2 Python launch files and multi-node configurations following official ROS 2 Humble patterns for the Physical AI textbook.

## When to Use

- Creating lessons in Chapter 6 (Building Robot Systems)
- Writing multi-node deployment exercises
- Generating worked examples for system startup
- Teaching parameter configuration and node composition
- Chapter 7 capstone project integration

## Live Documentation Access

**CRITICAL**: Before generating any code, fetch current ROS 2 documentation using Context7 MCP:

```
Tool: mcp__context7__resolve-library-id
libraryName: "ros2 launch"

Then:
Tool: mcp__context7__get-library-docs
context7CompatibleLibraryID: [resolved ID]
topic: "launch file python"
```

This ensures launch patterns match current ROS 2 Humble API.

## Launch File Patterns

### Basic Launch File (Canonical)

```python
# File: launch/robot_system.launch.py

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_robot_pkg',
            executable='publisher_node',
            name='sensor_publisher',
            output='screen',
        ),
        Node(
            package='my_robot_pkg',
            executable='subscriber_node',
            name='data_processor',
            output='screen',
        ),
    ])
```

### Launch File with Parameters

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_robot_pkg',
            executable='configurable_node',
            name='robot_controller',
            output='screen',
            parameters=[{
                'robot_name': 'my_robot',
                'update_rate': 10.0,
                'max_speed': 1.5,
                'enabled_sensors': ['lidar', 'camera', 'imu'],
            }],
        ),
    ])
```

### Launch File with Parameter File (YAML)

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('my_robot_pkg'),
        'config',
        'robot_params.yaml'
    )

    return LaunchDescription([
        Node(
            package='my_robot_pkg',
            executable='robot_node',
            name='robot_controller',
            output='screen',
            parameters=[config],
        ),
    ])
```

### Parameter File (YAML)

```yaml
# File: config/robot_params.yaml
robot_controller:
  ros__parameters:
    robot_name: "physical_ai_bot"
    update_rate: 20.0
    max_linear_speed: 2.0
    max_angular_speed: 1.57
    sensors:
      lidar:
        enabled: true
        topic: "/scan"
      camera:
        enabled: true
        topic: "/image_raw"
```

### Launch File with Arguments

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='default_robot',
        description='Name of the robot'
    )

    sim_mode_arg = DeclareLaunchArgument(
        'sim_mode',
        default_value='true',
        description='Run in simulation mode'
    )

    return LaunchDescription([
        robot_name_arg,
        sim_mode_arg,
        Node(
            package='my_robot_pkg',
            executable='robot_node',
            name='robot_controller',
            output='screen',
            parameters=[{
                'robot_name': LaunchConfiguration('robot_name'),
                'simulation': LaunchConfiguration('sim_mode'),
            }],
        ),
    ])
```

## Package Structure for Launch Files

```
my_robot_pkg/
├── my_robot_pkg/
│   ├── __init__.py
│   ├── publisher_node.py
│   └── subscriber_node.py
├── launch/
│   ├── robot_system.launch.py
│   └── debug_system.launch.py
├── config/
│   ├── robot_params.yaml
│   └── debug_params.yaml
├── package.xml
├── setup.py
└── setup.cfg
```

### setup.py (Essential Parts for Launch)

```python
from setuptools import setup
import os
from glob import glob

package_name = 'my_robot_pkg'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
        # Include config files
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'publisher_node = my_robot_pkg.publisher_node:main',
            'subscriber_node = my_robot_pkg.subscriber_node:main',
        ],
    },
)
```

## Debugging Multi-Node Systems

### Using ros2doctor

```bash
# Check system health
ros2 doctor

# Verbose output
ros2 doctor --report
```

### Using rqt_graph

```bash
# Visualize node graph
ros2 run rqt_graph rqt_graph
```

### Logging Levels

```python
# In node code
self.get_logger().debug('Detailed debug info')
self.get_logger().info('Normal operation')
self.get_logger().warn('Warning condition')
self.get_logger().error('Error occurred')
self.get_logger().fatal('Fatal error')
```

```bash
# Set log level at runtime
ros2 run my_pkg my_node --ros-args --log-level debug
```

## Educational Requirements

### Layer 1 (Manual Foundation)
- Explain launch file structure and purpose
- Walk through LaunchDescription components
- Demonstrate parameter passing patterns

### Layer 2 (AI Collaboration)
- Generate launch files from system requirements
- Debug multi-node communication issues with AI
- Optimize node configuration (Three Roles INVISIBLE)

### Layer 3 (Intelligence Design)
- System architecture patterns
- Configuration management strategies
- Reusable launch file components

### Layer 4 (Spec-Driven)
- Design system from specification
- Multi-node integration testing
- Capstone project orchestration

## Hardware Tier Compatibility

All launch files MUST work on:
- **Tier 1**: Cloud ROS 2 (TheConstruct) with turtlesim
- **Tier 2+**: Local ROS 2 Humble with physical robots

Launch commands:
```bash
# Build and source
cd ~/ros2_ws
colcon build --packages-select my_robot_pkg
source install/setup.bash

# Launch
ros2 launch my_robot_pkg robot_system.launch.py

# Launch with arguments
ros2 launch my_robot_pkg robot_system.launch.py robot_name:=my_bot sim_mode:=false
```

## Common Mistakes to Prevent

1. **Missing data_files in setup.py**: Launch files won't be installed
2. **Wrong path in get_package_share_directory**: Package name must match
3. **Forgetting to rebuild**: Changes require `colcon build`
4. **Parameter type mismatches**: YAML types must match node expectations

## Integration with Other Skills

- **ros2-publisher-subscriber**: Nodes to launch
- **ros2-service-pattern**: Service nodes in system
- **ros2-custom-interfaces**: Interface packages as dependencies
- **lesson-generator**: For full lesson structure

## Authoritative Source

All patterns verified against:
- https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Creating-Launch-Files.html
- https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html
