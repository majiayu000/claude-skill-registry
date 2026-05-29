---
name: ros2-gazebo-bridge
description: Configure ros_gz_bridge to connect Gazebo topics with ROS 2 for closed-loop control
domain: authoring
version: 1.0.0
created: 2025-11-29
triggers:
  - Connecting Gazebo simulation to ROS 2
  - Configuring topic bridges
  - Spawning robots from ROS 2 launch files
  - Debugging bridge issues
learned_from:
  - Module 2 Chapter 12 ROS 2 + Gazebo Integration (2025-11-29)
---

# ROS 2 Gazebo Bridge Skill

## Persona

Think like a robotics systems integrator who connects simulation to control systems. You understand message type mappings, topic naming conventions, and launch file orchestration. You create reliable bridges that enable seamless ROS 2 control of simulated robots.

---

## Pre-Flight Questions

Before configuring any bridge, ask yourself:

### 1. Data Flow Direction
- **Q**: Which direction does data flow?
  - **ROS_TO_GZ**: Commands from ROS 2 to simulation (cmd_vel)
  - **GZ_TO_ROS**: Sensor data from simulation to ROS 2 (images, scans)
  - **BIDIRECTIONAL**: Both directions (rare, use sparingly)

### 2. Message Type Compatibility
- **Q**: Do ROS 2 and Gazebo message types match?
  - **Impact**: Incompatible types cause silent failures
  - Always verify mapping exists in ros_gz_bridge

### 3. Topic Naming
- **Q**: Are topic names consistent across systems?
  - **Convention**: Use same name for both sides when possible
  - **Namespace**: Use robot namespace for multi-robot

---

## Principles

### Principle 1: Bridge Syntax

Command-line format:
```
/TOPIC@ROS_MSG@GZ_MSG
```

Direction modifiers:
```
/TOPIC@ROS_MSG@GZ_MSG      # Bidirectional (default)
/TOPIC@ROS_MSG[gz.msgs.X   # GZ to ROS only
/TOPIC@ROS_MSG]gz.msgs.X   # ROS to GZ only
```

### Principle 2: Common Message Mappings

| ROS 2 Type | Gazebo Type | Use Case |
|------------|-------------|----------|
| `geometry_msgs/msg/Twist` | `gz.msgs.Twist` | Velocity commands |
| `sensor_msgs/msg/Image` | `gz.msgs.Image` | Camera images |
| `sensor_msgs/msg/LaserScan` | `gz.msgs.LaserScan` | 2D LIDAR |
| `sensor_msgs/msg/PointCloud2` | `gz.msgs.PointCloudPacked` | 3D LIDAR |
| `sensor_msgs/msg/Imu` | `gz.msgs.IMU` | IMU data |
| `std_msgs/msg/Float64` | `gz.msgs.Double` | Scalar values |
| `geometry_msgs/msg/Pose` | `gz.msgs.Pose` | Position/orientation |

### Principle 3: Command-Line Usage

```bash
# Single topic bridge
ros2 run ros_gz_bridge parameter_bridge \
  /cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist

# Multiple topics
ros2 run ros_gz_bridge parameter_bridge \
  /cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist \
  /camera/image@sensor_msgs/msg/Image[gz.msgs.Image \
  /lidar/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan
```

### Principle 4: YAML Configuration

For complex setups, use YAML:

```yaml
# bridge_config.yaml
- ros_topic_name: "/cmd_vel"
  gz_topic_name: "/cmd_vel"
  ros_type_name: "geometry_msgs/msg/Twist"
  gz_type_name: "gz.msgs.Twist"
  direction: ROS_TO_GZ

- ros_topic_name: "/camera/image"
  gz_topic_name: "/camera/image"
  ros_type_name: "sensor_msgs/msg/Image"
  gz_type_name: "gz.msgs.Image"
  direction: GZ_TO_ROS

- ros_topic_name: "/lidar/scan"
  gz_topic_name: "/lidar/scan"
  ros_type_name: "sensor_msgs/msg/LaserScan"
  gz_type_name: "gz.msgs.LaserScan"
  direction: GZ_TO_ROS
```

Launch with:
```bash
ros2 run ros_gz_bridge parameter_bridge --ros-args -p config_file:=bridge_config.yaml
```

### Principle 5: Launch File Integration

```python
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        # Start Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                'gz_sim.launch.py'
            ]),
            launch_arguments={'world': 'my_world.sdf'}.items(),
        ),

        # Spawn robot
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-topic', '/robot_description',
                '-name', 'my_robot',
                '-x', '0', '-y', '0', '-z', '0.1'
            ],
        ),

        # Bridge topics
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                '/camera/image@sensor_msgs/msg/Image[gz.msgs.Image',
            ],
        ),

        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
        ),
    ])
```

---

## Debugging Bridge Issues

### Topic Not Bridging

1. Verify topic names match exactly (case-sensitive)
2. Check message type spelling
3. Confirm Gazebo is publishing: `gz topic -e -t /topic`
4. Confirm ROS 2 sees it: `ros2 topic list`

### Data Not Flowing

1. Direction wrong (ROS_TO_GZ vs GZ_TO_ROS)
2. Message types incompatible
3. Gazebo world not running
4. Bridge process crashed

### Message Type Mismatch

```bash
# Check ROS 2 message type
ros2 interface show sensor_msgs/msg/Image

# Check Gazebo message type
gz msg --info gz.msgs.Image
```

---

## Common Patterns

### Differential Drive Control

```yaml
# Velocity command (ROS → Gazebo)
- ros_topic_name: "/cmd_vel"
  gz_topic_name: "/model/my_robot/cmd_vel"
  ros_type_name: "geometry_msgs/msg/Twist"
  gz_type_name: "gz.msgs.Twist"
  direction: ROS_TO_GZ

# Odometry (Gazebo → ROS)
- ros_topic_name: "/odom"
  gz_topic_name: "/model/my_robot/odometry"
  ros_type_name: "nav_msgs/msg/Odometry"
  gz_type_name: "gz.msgs.Odometry"
  direction: GZ_TO_ROS
```

### Full Sensor Suite

```yaml
# Camera
- ros_topic_name: "/camera/image_raw"
  gz_topic_name: "/camera/image"
  ros_type_name: "sensor_msgs/msg/Image"
  gz_type_name: "gz.msgs.Image"
  direction: GZ_TO_ROS

# LIDAR
- ros_topic_name: "/scan"
  gz_topic_name: "/lidar/scan"
  ros_type_name: "sensor_msgs/msg/LaserScan"
  gz_type_name: "gz.msgs.LaserScan"
  direction: GZ_TO_ROS

# IMU
- ros_topic_name: "/imu/data"
  gz_topic_name: "/imu"
  ros_type_name: "sensor_msgs/msg/Imu"
  gz_type_name: "gz.msgs.IMU"
  direction: GZ_TO_ROS
```

---

## Checklist

Before finalizing any bridge configuration:

- [ ] All topic names verified (exact match)
- [ ] Message type mappings confirmed
- [ ] Direction correct for each topic
- [ ] YAML syntax valid (if using config file)
- [ ] Gazebo topics publishing (`gz topic -l`)
- [ ] ROS 2 topics visible (`ros2 topic list`)
- [ ] Data flowing (`ros2 topic echo`)
- [ ] Launch file orchestrates correctly
- [ ] Multi-robot namespacing (if needed)

---

## Integration

This skill is used by:
- `content-implementer` agent when generating Module 2 lessons
- Students learning ROS 2-Gazebo integration in Chapter 12
- All simulation-based robotics development

**Dependencies**:
- `urdf-robot-model` - robots to spawn and control
- `gazebo-world-builder` - worlds to simulate in
- `sensor-simulation` - sensor data to bridge
