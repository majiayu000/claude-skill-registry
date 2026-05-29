---
name: robot-bringup
description: >
  Patterns and best practices for bringing up a complete ROS2-based robotics system on a robot's
  onboard computer, including systemd services, launch file composition, ordered startup, and
  production monitoring. Use this skill when configuring a robot to start ROS2 nodes on boot,
  writing systemd unit files for ROS2 launch, composing layered launch files for full robot stacks,
  setting up watchdog monitoring, configuring udev rules for deterministic device naming, or
  debugging boot-time race conditions. Trigger whenever the user mentions robot bringup, robot
  startup, systemd for ROS2, ROS2 on boot, launch file composition, robot boot sequence, udev
  rules for cameras or serial ports, watchdog for robot systems, automatic restart for ROS2 nodes,
  network configuration for multi-machine ROS2, log rotation for robots, graceful shutdown of
  robot stacks, or SSH-based remote debugging of robots. Also trigger for environment setup in
  systemd (sourcing workspaces), ordered startup with health checks, deterministic device naming,
  or any discussion of running ROS2 systems as long-running production services. Covers systemd
  on Ubuntu 22.04/24.04 with ROS2 Humble, Iron, and Jazzy.
---

# Robot Bringup Skill

## When to Use This Skill

- Configuring a robot to automatically start its full ROS2 stack on boot via systemd
- Writing systemd unit files that correctly source ROS2 workspaces and set DDS environment
- Composing layered launch files (hardware, drivers, perception, application) into a single bringup
- Setting up ordered startup with health checks to avoid race conditions between dependent nodes
- Writing udev rules for deterministic device naming of cameras, LiDARs, and serial devices
- Configuring CycloneDDS or FastDDS for multi-machine ROS2 discovery across robot and base station
- Implementing watchdog and heartbeat monitoring for production robot systems
- Setting up log rotation and structured logging for long-running robot deployments
- Writing graceful shutdown handlers that bring actuators to a safe state before exit
- Debugging boot-time failures, service ordering issues, or device enumeration races

## The Robot Bringup Stack

A production robot bringup follows a layered startup sequence from hardware initialization through application-level nodes. Each layer depends on the one below it.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                            │
│  Navigation, manipulation, mission planning, HRI                    │
├─────────────────────────────────────────────────────────────────────┤
│                        PERCEPTION LAYER                             │
│  Object detection, SLAM, point cloud filtering, sensor fusion       │
├─────────────────────────────────────────────────────────────────────┤
│                         DRIVER LAYER                                │
│  Camera drivers, LiDAR drivers, motor controllers, IMU              │
├─────────────────────────────────────────────────────────────────────┤
│                        HARDWARE LAYER                               │
│  udev rules, device enumeration, USB reset, firmware check          │
├─────────────────────────────────────────────────────────────────────┤
│                      ROS2 ENVIRONMENT                               │
│  Source workspace, set RMW, ROS_DOMAIN_ID, DDS config               │
├─────────────────────────────────────────────────────────────────────┤
│                    SYSTEMD TARGETS & SERVICES                       │
│  network-online.target → robot-hw.target → robot-bringup.target     │
├─────────────────────────────────────────────────────────────────────┤
│                      LINUX BOOT (systemd)                           │
│  BIOS/UEFI → GRUB → kernel → systemd init                          │
├─────────────────────────────────────────────────────────────────────┤
│                         HARDWARE BOOT                               │
│  Power supply, onboard computer, peripherals                        │
└─────────────────────────────────────────────────────────────────────┘
```

## systemd Service Units for ROS2

### Basic ROS2 Service Unit

Place service files in `/etc/systemd/system/`. This template starts a ROS2 launch file as a long-running service with watchdog support.

```ini
# /etc/systemd/system/robot-bringup.service
[Unit]
Description=Robot ROS2 Bringup Stack
Documentation=https://github.com/my-org/my-robot
After=network-online.target robot-hw.target
Wants=network-online.target
Requires=robot-hw.target

[Service]
Type=notify
User=robot
Group=robot
WorkingDirectory=/home/robot

# Load ROS2 environment variables from a dedicated env file
EnvironmentFile=/etc/robot/ros2.env

# Pre-start check: verify critical devices exist
ExecStartPre=/usr/local/bin/robot-device-check.sh

# Start the ROS2 launch file via bash so we can source the workspace
ExecStart=/bin/bash -c '\
  source /opt/ros/${ROS_DISTRO}/setup.bash && \
  source /home/robot/ros2_ws/install/setup.bash && \
  exec ros2 launch my_robot_bringup bringup.launch.py'

# Graceful shutdown: send SIGINT first (Ctrl+C equivalent for ROS2)
ExecStop=/bin/kill -INT $MAINPID
TimeoutStopSec=30

# Restart on failure, but not on clean exit
Restart=on-failure
RestartSec=5

# systemd watchdog: service must call sd_notify(WATCHDOG=1) within this interval
WatchdogSec=30

# Process management
KillMode=mixed
KillSignal=SIGINT
FinalKillSignal=SIGKILL
TimeoutStartSec=60

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=robot-bringup

[Install]
WantedBy=multi-user.target
```

### Environment Setup in systemd

Store environment variables in a dedicated file rather than sourcing .bashrc (which is not loaded by systemd).

```bash
# /etc/robot/ros2.env
# ROS2 distribution
ROS_DISTRO=humble

# DDS middleware selection
RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Domain isolation: unique per robot to avoid cross-talk
ROS_DOMAIN_ID=42

# CycloneDDS configuration file path
CYCLONEDDS_URI=file:///etc/robot/cyclonedds.xml

# Disable localhost-only mode for multi-machine setups
ROS_LOCALHOST_ONLY=0

# Logging configuration
ROS_LOG_DIR=/var/log/ros2
RCUTILS_LOGGING_USE_STDOUT=0
RCUTILS_COLORIZED_OUTPUT=0

# Robot-specific configuration
ROBOT_NAME=my_robot_01
ROBOT_CONFIG_DIR=/etc/robot/config
```

### Dependencies Between Services

Split the robot stack into multiple systemd services with explicit ordering. This allows independent restart of layers and clearer failure isolation.

```ini
# /etc/systemd/system/robot-drivers.service
[Unit]
Description=Robot Hardware Drivers (cameras, LiDAR, IMU, motors)
After=network-online.target robot-hw.target
Wants=network-online.target
Requires=robot-hw.target

[Service]
Type=notify
User=robot
EnvironmentFile=/etc/robot/ros2.env
ExecStart=/bin/bash -c '\
  source /opt/ros/${ROS_DISTRO}/setup.bash && \
  source /home/robot/ros2_ws/install/setup.bash && \
  exec ros2 launch my_robot_bringup drivers.launch.py'
Restart=on-failure
RestartSec=5
WatchdogSec=30
KillMode=mixed
KillSignal=SIGINT
TimeoutStopSec=20
StandardOutput=journal
SyslogIdentifier=robot-drivers

[Install]
WantedBy=robot-bringup.target
```

```ini
# /etc/systemd/system/robot-perception.service
[Unit]
Description=Robot Perception Stack (SLAM, detection, sensor fusion)
After=robot-drivers.service
Requires=robot-drivers.service
PartOf=robot-drivers.service

[Service]
Type=notify
User=robot
EnvironmentFile=/etc/robot/ros2.env
ExecStart=/bin/bash -c '\
  source /opt/ros/${ROS_DISTRO}/setup.bash && \
  source /home/robot/ros2_ws/install/setup.bash && \
  exec ros2 launch my_robot_bringup perception.launch.py'
Restart=on-failure
RestartSec=5
WatchdogSec=30
KillMode=mixed
KillSignal=SIGINT
TimeoutStopSec=20
StandardOutput=journal
SyslogIdentifier=robot-perception

[Install]
WantedBy=robot-bringup.target
```

```ini
# /etc/systemd/system/robot-application.service
[Unit]
Description=Robot Application Layer (navigation, planning, HRI)
After=robot-perception.service
Requires=robot-perception.service
PartOf=robot-perception.service

[Service]
Type=notify
User=robot
EnvironmentFile=/etc/robot/ros2.env
ExecStart=/bin/bash -c '\
  source /opt/ros/${ROS_DISTRO}/setup.bash && \
  source /home/robot/ros2_ws/install/setup.bash && \
  exec ros2 launch my_robot_bringup application.launch.py'
Restart=on-failure
RestartSec=10
WatchdogSec=30
KillMode=mixed
KillSignal=SIGINT
TimeoutStopSec=20
StandardOutput=journal
SyslogIdentifier=robot-application

[Install]
WantedBy=robot-bringup.target
```

### Restart Policies and Failure Recovery

Configure rate limiting to prevent restart loops when a service is fundamentally broken (e.g., missing device, configuration error).

```ini
# Add to the [Service] section of any robot service
Restart=on-failure
RestartSec=5

# Allow at most 5 restart attempts within 120 seconds
StartLimitIntervalSec=120
StartLimitBurst=5

# Ramp up restart delay to avoid thrashing
# RestartSec can also be set dynamically via drop-in overrides:
#   RestartSec=5   (first few retries, fast recovery)
#   After StartLimitBurst is hit, the unit enters failed state
#   Use systemctl reset-failed robot-drivers.service to retry

# On final failure, trigger an alert
OnFailure=robot-alert@%n.service
```

### Resource Limits and cgroups

Constrain resource usage to prevent a runaway node from starving the rest of the system.

```ini
# Add to the [Service] section
# Limit memory to 2 GB (hard kill at 2.5 GB)
MemoryMax=2G
MemoryHigh=1800M

# Limit CPU to 300% (3 cores on a multi-core system)
CPUQuota=300%

# Set real-time scheduling priority for time-critical drivers
# Requires the user to have rtprio permissions in /etc/security/limits.d/
Nice=-5
IOSchedulingClass=realtime
IOSchedulingPriority=0

# Restrict filesystem access
ProtectHome=read-only
ProtectSystem=strict
ReadWritePaths=/var/log/ros2 /tmp
PrivateTmp=true
```

## Launch File Composition and Layering

### Launch Layer Architecture

Organize launch files into layers that mirror the systemd service architecture. Each layer is an independent launch file that can be tested in isolation.

```
bringup.launch.py  (top-level: composes all layers)
├── hardware.launch.py     (udev checks, device readiness)
├── drivers.launch.py      (camera, LiDAR, IMU, motor drivers)
│   ├── camera.launch.py
│   ├── lidar.launch.py
│   └── motors.launch.py
├── perception.launch.py   (SLAM, detection, fusion)
│   ├── slam.launch.py
│   └── detection.launch.py
└── application.launch.py  (navigation, planning, HRI)
    ├── navigation.launch.py
    └── mission.launch.py
```

### Hardware Layer Launch

```python
# my_robot_bringup/launch/hardware.launch.py
from launch import LaunchDescription
from launch.actions import LogInfo, ExecuteProcess, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, EnvironmentVariable

def generate_launch_description():
    # Declare arguments for hardware configuration
    robot_name = LaunchConfiguration('robot_name',
        default=EnvironmentVariable('ROBOT_NAME', default_value='default_robot'))

    # Check that critical devices are present
    check_camera = ExecuteProcess(
        cmd=['test', '-e', '/dev/robot/camera_front'],
        name='check_camera_front',
        output='screen',
    )

    check_lidar = ExecuteProcess(
        cmd=['test', '-e', '/dev/robot/lidar'],
        name='check_lidar',
        output='screen',
    )

    check_imu = ExecuteProcess(
        cmd=['test', '-e', '/dev/robot/imu'],
        name='check_imu',
        output='screen',
    )

    log_ready = TimerAction(
        period=2.0,
        actions=[LogInfo(msg='Hardware checks passed, devices ready')],
    )

    return LaunchDescription([
        check_camera,
        check_lidar,
        check_imu,
        log_ready,
    ])
```

### Driver Layer Launch

```python
# my_robot_bringup/launch/drivers.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, SetRemap
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    use_sim = LaunchConfiguration('use_sim', default='false')
    camera_config = LaunchConfiguration('camera_config', default='default')

    # Camera driver
    camera_node = Node(
        package='usb_cam',
        executable='usb_cam_node_exe',
        name='camera_front',
        parameters=[PathJoinSubstitution([
            FindPackageShare('my_robot_bringup'), 'config', 'camera_front.yaml'
        ])],
        remappings=[('/image_raw', '/camera/front/image_raw')],
    )

    # LiDAR driver
    lidar_node = Node(
        package='sllidar_ros2',
        executable='sllidar_node',
        name='lidar',
        parameters=[{
            'serial_port': '/dev/robot/lidar',
            'serial_baudrate': 460800,
            'frame_id': 'lidar_link',
            'angle_compensate': True,
        }],
    )

    # IMU driver
    imu_node = Node(
        package='imu_driver',
        executable='imu_node',
        name='imu',
        parameters=[{
            'port': '/dev/robot/imu',
            'frame_id': 'imu_link',
            'publish_rate': 100.0,
        }],
    )

    # Motor controller driver
    motor_node = Node(
        package='motor_driver',
        executable='motor_controller_node',
        name='motor_controller',
        parameters=[PathJoinSubstitution([
            FindPackageShare('my_robot_bringup'), 'config', 'motors.yaml'
        ])],
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim', default_value='false'),
        DeclareLaunchArgument('camera_config', default_value='default'),
        camera_node,
        lidar_node,
        imu_node,
        motor_node,
    ])
```

### Perception Layer Launch

```python
# my_robot_bringup/launch/perception.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, ComposableNodeContainer, LoadComposableNode
from launch_ros.descriptions import ComposableNode
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    enable_slam = LaunchConfiguration('enable_slam', default='true')
    enable_detection = LaunchConfiguration('enable_detection', default='true')

    # Use a composable node container for zero-copy perception pipeline
    perception_container = ComposableNodeContainer(
        name='perception_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container_mt',
        composable_node_descriptions=[
            ComposableNode(
                package='image_proc',
                plugin='image_proc::RectifyNode',
                name='rectify',
                remappings=[('image', '/camera/front/image_raw')],
            ),
            ComposableNode(
                package='my_detection',
                plugin='my_detection::DetectorNode',
                name='detector',
                parameters=[PathJoinSubstitution([
                    FindPackageShare('my_robot_bringup'), 'config', 'detector.yaml'
                ])],
            ),
        ],
        condition=IfCondition(enable_detection),
    )

    # SLAM node
    slam_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam',
        parameters=[PathJoinSubstitution([
            FindPackageShare('my_robot_bringup'), 'config', 'slam.yaml'
        ])],
        condition=IfCondition(enable_slam),
    )

    return LaunchDescription([
        DeclareLaunchArgument('enable_slam', default_value='true'),
        DeclareLaunchArgument('enable_detection', default_value='true'),
        perception_container,
        slam_node,
    ])
```

### Application Layer Launch

```python
# my_robot_bringup/launch/application.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    nav_params = LaunchConfiguration('nav_params', default=PathJoinSubstitution([
        FindPackageShare('my_robot_bringup'), 'config', 'nav2_params.yaml'
    ]))

    # Include Nav2 bringup
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([
            FindPackageShare('nav2_bringup'), 'launch', 'bringup_launch.py'
        ])),
        launch_arguments={
            'params_file': nav_params,
            'use_sim_time': LaunchConfiguration('use_sim', default='false'),
        }.items(),
    )

    # Mission planner
    mission_node = Node(
        package='my_mission',
        executable='mission_planner',
        name='mission_planner',
        parameters=[PathJoinSubstitution([
            FindPackageShare('my_robot_bringup'), 'config', 'mission.yaml'
        ])],
    )

    return LaunchDescription([
        DeclareLaunchArgument('nav_params', default_value=''),
        DeclareLaunchArgument('use_sim', default_value='false'),
        nav2_bringup,
        mission_node,
    ])
```

### Top-Level Bringup Launch

This launch file composes all layers into a single entry point, with conditional arguments for simulation vs. real hardware and robot variant selection.

```python
# my_robot_bringup/launch/bringup.launch.py
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, IncludeLaunchDescription,
    GroupAction, LogInfo, TimerAction,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration, PathJoinSubstitution, PythonExpression,
)
from launch_ros.actions import PushRosNamespace, SetParameter
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_share = FindPackageShare('my_robot_bringup')
    use_sim = LaunchConfiguration('use_sim')
    robot_variant = LaunchConfiguration('robot_variant')
    enable_perception = LaunchConfiguration('enable_perception')
    enable_navigation = LaunchConfiguration('enable_navigation')

    # Hardware layer (skip in simulation)
    hardware_launch = GroupAction(
        actions=[
            LogInfo(msg='Starting hardware layer...'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([pkg_share, 'launch', 'hardware.launch.py'])
                ),
            ),
        ],
        condition=UnlessCondition(use_sim),
    )

    # Driver layer
    drivers_launch = GroupAction(
        actions=[
            LogInfo(msg='Starting driver layer...'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([pkg_share, 'launch', 'drivers.launch.py'])
                ),
                launch_arguments={'use_sim': use_sim}.items(),
            ),
        ],
    )

    # Perception layer (conditional)
    perception_launch = GroupAction(
        actions=[
            LogInfo(msg='Starting perception layer...'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([pkg_share, 'launch', 'perception.launch.py'])
                ),
            ),
        ],
        condition=IfCondition(enable_perception),
    )

    # Application layer (conditional)
    application_launch = GroupAction(
        actions=[
            LogInfo(msg='Starting application layer...'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([pkg_share, 'launch', 'application.launch.py'])
                ),
                launch_arguments={'use_sim': use_sim}.items(),
            ),
        ],
        condition=IfCondition(enable_navigation),
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim', default_value='false',
            description='Use simulation instead of real hardware'),
        DeclareLaunchArgument('robot_variant', default_value='standard',
            description='Robot variant: standard, heavy_payload, outdoor'),
        DeclareLaunchArgument('enable_perception', default_value='true',
            description='Enable perception stack'),
        DeclareLaunchArgument('enable_navigation', default_value='true',
            description='Enable navigation and application stack'),

        # Set use_sim_time globally
        SetParameter(name='use_sim_time', value=use_sim),

        LogInfo(msg=['Bringing up robot variant: ', robot_variant]),

        hardware_launch,
        drivers_launch,
        perception_launch,
        application_launch,
    ])
```

### Conditional Loading (Sim vs Real, Robot Variants)

Use `IfCondition`, `UnlessCondition`, and `PythonExpression` to swap configurations based on runtime arguments.

```python
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import PythonExpression, LaunchConfiguration

robot_variant = LaunchConfiguration('robot_variant')

# Load a variant-specific config file
variant_config = PathJoinSubstitution([
    FindPackageShare('my_robot_bringup'), 'config', 'variants',
    PythonExpression(["'", robot_variant, "' + '.yaml'"]),
])

# Conditional node: only load the arm driver for heavy_payload variant
arm_driver = Node(
    package='arm_driver',
    executable='arm_controller_node',
    name='arm_controller',
    condition=IfCondition(
        PythonExpression(["'", robot_variant, "' == 'heavy_payload'"])
    ),
)
```

## Ordered Startup with Health Checks

### Startup Dependency Graph

Nodes must start in a specific order to avoid subscribing to topics that do not yet exist or calling services before they are available.

```
                    ┌──────────────┐
                    │  motors.srv  │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ camera   │ │  lidar   │ │   imu    │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             ▼            ▼            ▼
        ┌──────────────────────────────────┐
        │        perception / SLAM         │
        └──────────────┬───────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │      navigation / planning       │
        └──────────────────────────────────┘
```

### Health Check Scripts

Use health check scripts in `ExecStartPre` to block service startup until dependencies are ready.

```bash
#!/bin/bash
# /usr/local/bin/robot-device-check.sh
# Verifies that all required hardware devices are present before starting drivers.
# Exit code 0 = all devices found, non-zero = missing device.

set -euo pipefail

REQUIRED_DEVICES=(
    "/dev/robot/camera_front"
    "/dev/robot/lidar"
    "/dev/robot/imu"
    "/dev/robot/motor_controller"
)

TIMEOUT=30
POLL_INTERVAL=1
elapsed=0

for device in "${REQUIRED_DEVICES[@]}"; do
    elapsed=0
    while [ ! -e "$device" ]; do
        if [ "$elapsed" -ge "$TIMEOUT" ]; then
            echo "ERROR: Device $device not found after ${TIMEOUT}s" >&2
            exit 1
        fi
        echo "Waiting for $device... (${elapsed}s/${TIMEOUT}s)"
        sleep "$POLL_INTERVAL"
        elapsed=$((elapsed + POLL_INTERVAL))
    done
    echo "Found device: $device"
done

echo "All required devices are present."
exit 0
```

```bash
#!/bin/bash
# /usr/local/bin/wait-for-ros2-nodes.sh
# Blocks until specified ROS2 nodes are active.
# Usage: wait-for-ros2-nodes.sh node_name1 node_name2 ...

set -euo pipefail

source /opt/ros/${ROS_DISTRO}/setup.bash
source /home/robot/ros2_ws/install/setup.bash

TIMEOUT=60
POLL_INTERVAL=2

for node_name in "$@"; do
    elapsed=0
    while ! ros2 node list 2>/dev/null | grep -q "$node_name"; do
        if [ "$elapsed" -ge "$TIMEOUT" ]; then
            echo "ERROR: Node $node_name not found after ${TIMEOUT}s" >&2
            exit 1
        fi
        echo "Waiting for node $node_name... (${elapsed}s/${TIMEOUT}s)"
        sleep "$POLL_INTERVAL"
        elapsed=$((elapsed + POLL_INTERVAL))
    done
    echo "Node active: $node_name"
done

echo "All required nodes are active."
exit 0
```

### Wait-for-Topic Pattern

A reusable Python utility to block until a topic is being published, useful for ordered startup in launch files.

```python
#!/usr/bin/env python3
# wait_for_topic.py
# Usage: python3 wait_for_topic.py /scan sensor_msgs/msg/LaserScan --timeout 30

import argparse
import sys
import time
import importlib

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data


class TopicWaiter(Node):
    def __init__(self, topic_name, msg_type_str, timeout):
        super().__init__('topic_waiter')
        self.received = False
        self.timeout = timeout
        self.start_time = time.time()

        # Dynamically import the message type
        module_name, class_name = msg_type_str.rsplit('/', 1)
        module_name = module_name.replace('/', '.')
        module = importlib.import_module(module_name)
        msg_type = getattr(module, class_name)

        self.sub = self.create_subscription(
            msg_type, topic_name, self._callback, qos_profile_sensor_data)
        self.timer = self.create_timer(1.0, self._check_timeout)
        self.get_logger().info(f'Waiting for topic {topic_name}...')

    def _callback(self, msg):
        self.get_logger().info('Topic is active, message received.')
        self.received = True

    def _check_timeout(self):
        if self.received:
            raise SystemExit(0)
        elapsed = time.time() - self.start_time
        if elapsed > self.timeout:
            self.get_logger().error(f'Timeout after {self.timeout}s')
            raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('topic', help='Topic name to wait for')
    parser.add_argument('msg_type', help='Message type (e.g., sensor_msgs/msg/LaserScan)')
    parser.add_argument('--timeout', type=float, default=30.0)
    args = parser.parse_args()

    rclpy.init()
    node = TopicWaiter(args.topic, args.msg_type, args.timeout)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
```

### Lifecycle Node Orchestration for Ordered Startup

Use lifecycle (managed) nodes to enforce startup ordering. A lifecycle manager configures and activates nodes in sequence, ensuring each node completes its configuration before the next one starts.

```python
# lifecycle_manager.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Lifecycle manager controls the startup/shutdown order
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager',
        output='screen',
        parameters=[{
            # Nodes are transitioned in order: configure, then activate
            'node_names': [
                'motor_controller',
                'camera_driver',
                'lidar_driver',
                'slam',
                'navigation',
            ],
            'autostart': True,
            # Timeout for each node transition
            'bond_timeout': 10.0,
            # Check period for node bonds
            'bond_respawn_max_duration': 2.0,
        }],
    )

    return LaunchDescription([
        lifecycle_manager,
    ])
```

## udev Rules for Deterministic Device Naming

### Writing udev Rules for Cameras

USB cameras can enumerate in any order on boot, causing `/dev/video0` to be unpredictable. Use udev rules to assign stable symlinks based on device attributes.

```bash
# /etc/udev/rules.d/99-robot-cameras.rules
# Assign stable device names based on USB port path (physical location).
# Find attributes with: udevadm info --name=/dev/video0 --attribute-walk

# Front camera: USB hub port 1, interface 0 (video capture)
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", \
  KERNELS=="1-1.2:1.0", ATTR{index}=="0", \
  SYMLINK+="robot/camera_front", MODE="0666", GROUP="video"

# Rear camera: USB hub port 2, interface 0 (video capture)
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", \
  KERNELS=="1-1.3:1.0", ATTR{index}=="0", \
  SYMLINK+="robot/camera_rear", MODE="0666", GROUP="video"

# Depth camera (RealSense): by serial number
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b3a", \
  ATTRS{serial}=="123456789", ATTR{index}=="0", \
  SYMLINK+="robot/camera_depth", MODE="0666", GROUP="video"
```

### Writing udev Rules for Serial Devices

Serial devices (IMU, motor controller, GPS) also need stable names since `/dev/ttyUSB*` numbering is non-deterministic.

```bash
# /etc/udev/rules.d/99-robot-serial.rules
# IMU on FTDI serial adapter (identified by serial number)
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", \
  ATTRS{serial}=="AB0CDEFG", \
  SYMLINK+="robot/imu", MODE="0666", GROUP="dialout"

# Motor controller on USB port path
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", \
  KERNELS=="1-1.4:1.0", \
  SYMLINK+="robot/motor_controller", MODE="0666", GROUP="dialout"

# GPS receiver
SUBSYSTEM=="tty", ATTRS{idVendor}=="1546", ATTRS{idProduct}=="01a7", \
  SYMLINK+="robot/gps", MODE="0666", GROUP="dialout"

# LiDAR (CP2102 adapter)
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", \
  ATTRS{serial}=="0001", \
  SYMLINK+="robot/lidar", MODE="0666", GROUP="dialout"
```

### Reloading and Testing

```bash
# Reload udev rules without rebooting
sudo udevadm control --reload-rules
sudo udevadm trigger

# Test a rule against a specific device
sudo udevadm test $(udevadm info --query=path --name=/dev/ttyUSB0)

# View all attributes for a device (use to find idVendor, serial, etc.)
udevadm info --name=/dev/ttyUSB0 --attribute-walk

# Monitor udev events in real time (plug/unplug devices to see events)
udevadm monitor --subsystem-match=tty --property
```

## Network Configuration for Multi-Machine ROS2

### Static IP Configuration

Assign a static IP to the robot's wired interface using netplan (Ubuntu 22.04+).

```yaml
# /etc/netplan/01-robot-network.yaml
network:
  version: 2
  ethernets:
    eth0:
      addresses:
        - 10.0.0.10/24
      routes:
        - to: default
          via: 10.0.0.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
  wifis:
    wlan0:
      dhcp4: true
      access-points:
        "RobotNetwork":
          password: "securepassword"
```

```bash
# Apply netplan configuration
sudo netplan apply
```

### DDS Discovery Across Machines

CycloneDDS requires explicit peer configuration for multi-machine setups since multicast may not work across network segments.

```xml
<!-- /etc/robot/cyclonedds.xml -->
<CycloneDDS>
  <Domain>
    <General>
      <Interfaces>
        <NetworkInterface name="eth0" priority="default" multicast="false"/>
      </Interfaces>
      <AllowMulticast>false</AllowMulticast>
    </General>
    <Discovery>
      <ParticipantIndex>auto</ParticipantIndex>
      <Peers>
        <!-- Robot onboard computer -->
        <Peer address="10.0.0.10"/>
        <!-- Base station / operator workstation -->
        <Peer address="10.0.0.20"/>
        <!-- Second robot (if applicable) -->
        <Peer address="10.0.0.11"/>
      </Peers>
      <MaxAutoParticipantIndex>30</MaxAutoParticipantIndex>
    </Discovery>
    <Internal>
      <SocketReceiveBufferSize min="10MB"/>
    </Internal>
  </Domain>
</CycloneDDS>
```

### Firewall Rules

DDS uses a range of UDP ports for discovery and data exchange. Open these ports on both the robot and the base station.

```bash
#!/bin/bash
# /usr/local/bin/robot-firewall-setup.sh
# Open firewall ports for CycloneDDS discovery and data exchange.

# DDS discovery (SPDP) uses UDP port 7400 + (250 * domain_id) + participant_id
# For domain_id=42: base port = 7400 + 250*42 = 17900
DOMAIN_ID=42
BASE_PORT=$((7400 + 250 * DOMAIN_ID))

# Allow discovery (SPDP) multicast/unicast
sudo ufw allow proto udp from 10.0.0.0/24 to any port $BASE_PORT:$((BASE_PORT + 100))

# Allow data exchange (SEDP) user traffic ports
DATA_PORT=$((BASE_PORT + 1))
sudo ufw allow proto udp from 10.0.0.0/24 to any port $DATA_PORT:$((DATA_PORT + 200))

# Allow all traffic on the robot subnet (simpler alternative)
# sudo ufw allow from 10.0.0.0/24

sudo ufw reload
echo "Firewall configured for ROS2 DDS on domain $DOMAIN_ID"
```

### ROS_DOMAIN_ID and ROS_LOCALHOST_ONLY

```bash
# Isolate robots on the same network by domain ID (0-232)
export ROS_DOMAIN_ID=42

# Lock DDS traffic to localhost only (useful for single-machine development)
export ROS_LOCALHOST_ONLY=1

# For multi-machine setups, ensure ROS_LOCALHOST_ONLY is 0 on all machines
export ROS_LOCALHOST_ONLY=0

# Verify DDS discovery across machines
ros2 daemon stop && ros2 daemon start
ros2 topic list  # Should see topics from both machines
```

## Watchdog and Heartbeat Monitoring

### systemd Watchdog Integration

When `WatchdogSec` is set in the service unit, the process must periodically notify systemd that it is alive. If the notification is missed, systemd restarts the service.

```python
#!/usr/bin/env python3
# watchdog_node.py
# A ROS2 node that integrates with systemd watchdog via sd_notify.

import os
import socket
import time

import rclpy
from rclpy.node import Node
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus


class WatchdogNode(Node):
    """Notifies systemd that the ROS2 process is alive."""

    def __init__(self):
        super().__init__('watchdog_node')

        # Read the watchdog interval from systemd environment
        watchdog_usec = os.environ.get('WATCHDOG_USEC')
        if watchdog_usec:
            # Notify at half the watchdog interval for safety margin
            interval_sec = int(watchdog_usec) / 1_000_000 / 2.0
        else:
            interval_sec = 10.0
            self.get_logger().warn('WATCHDOG_USEC not set, using 10s interval')

        # Connect to systemd notification socket
        self.notify_socket = os.environ.get('NOTIFY_SOCKET')

        # Signal that startup is complete
        self._sd_notify('READY=1')
        self.get_logger().info(
            f'Watchdog node started, notify interval: {interval_sec:.1f}s')

        # Periodically send watchdog keepalive
        self.create_timer(interval_sec, self._watchdog_tick)

        # Subscribe to system diagnostics to detect failures
        self.diag_sub = self.create_subscription(
            DiagnosticArray, '/diagnostics', self._diag_callback, 10)
        self.system_healthy = True

    def _watchdog_tick(self):
        """Send watchdog keepalive to systemd if system is healthy."""
        if self.system_healthy:
            self._sd_notify('WATCHDOG=1')
        else:
            self.get_logger().error(
                'System unhealthy, withholding watchdog notification')

    def _diag_callback(self, msg):
        """Monitor diagnostics for critical errors."""
        for status in msg.status:
            if status.level == DiagnosticStatus.ERROR:
                self.get_logger().error(f'Critical error: {status.name}: {status.message}')
                self.system_healthy = False
                return
        self.system_healthy = True

    def _sd_notify(self, state):
        """Send notification to systemd."""
        if not self.notify_socket:
            return
        addr = self.notify_socket
        if addr[0] == '@':
            addr = '\0' + addr[1:]
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        try:
            sock.connect(addr)
            sock.sendall(state.encode())
        finally:
            sock.close()


def main():
    rclpy.init()
    node = WatchdogNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### ROS2-Level Heartbeat Monitor Node

A monitor node that subscribes to heartbeat topics from critical subsystems and publishes overall system health. If a heartbeat is missed, it triggers a safe stop.

```python
#!/usr/bin/env python3
# heartbeat_monitor.py
# Monitors heartbeats from critical nodes and triggers safe stop if any go silent.

import time

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from std_msgs.msg import Bool, String
from geometry_msgs.msg import Twist
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue


class HeartbeatMonitor(Node):
    def __init__(self):
        super().__init__('heartbeat_monitor')

        # Declare parameters for monitored nodes and timeout
        self.declare_parameter('monitored_nodes', [
            'motor_controller', 'camera_driver', 'lidar_driver', 'slam'
        ])
        self.declare_parameter('heartbeat_timeout_sec', 5.0)
        self.declare_parameter('check_period_sec', 1.0)

        self.monitored_nodes = self.get_parameter('monitored_nodes').value
        self.timeout = self.get_parameter('heartbeat_timeout_sec').value
        check_period = self.get_parameter('check_period_sec').value

        # Track last heartbeat time for each monitored node
        self.last_heartbeat = {name: time.time() for name in self.monitored_nodes}

        # Subscribe to each node's heartbeat topic
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            depth=1,
        )
        for node_name in self.monitored_nodes:
            self.create_subscription(
                Bool, f'/{node_name}/heartbeat',
                lambda msg, n=node_name: self._heartbeat_callback(n, msg),
                reliable_qos,
            )

        # Publishers
        self.health_pub = self.create_publisher(
            DiagnosticArray, '/system_health', 10)
        self.estop_pub = self.create_publisher(
            Bool, '/emergency_stop', reliable_qos)
        self.cmd_vel_pub = self.create_publisher(
            Twist, '/cmd_vel', 10)

        # Periodic health check
        self.create_timer(check_period, self._check_health)
        self.get_logger().info(
            f'Monitoring heartbeats for: {self.monitored_nodes}')

    def _heartbeat_callback(self, node_name, msg):
        """Record heartbeat reception time."""
        self.last_heartbeat[node_name] = time.time()

    def _check_health(self):
        """Check all heartbeats and publish diagnostics."""
        now = time.time()
        diag_array = DiagnosticArray()
        diag_array.header.stamp = self.get_clock().now().to_msg()
        all_healthy = True

        for node_name in self.monitored_nodes:
            elapsed = now - self.last_heartbeat[node_name]
            status = DiagnosticStatus()
            status.name = f'heartbeat/{node_name}'

            if elapsed < self.timeout:
                status.level = DiagnosticStatus.OK
                status.message = f'Alive ({elapsed:.1f}s ago)'
            else:
                status.level = DiagnosticStatus.ERROR
                status.message = f'TIMEOUT ({elapsed:.1f}s since last heartbeat)'
                all_healthy = False
                self.get_logger().error(
                    f'Heartbeat timeout for {node_name}: {elapsed:.1f}s')

            status.values = [
                KeyValue(key='elapsed_sec', value=f'{elapsed:.2f}'),
                KeyValue(key='timeout_sec', value=f'{self.timeout:.2f}'),
            ]
            diag_array.status.append(status)

        self.health_pub.publish(diag_array)

        if not all_healthy:
            self._trigger_safe_stop()

    def _trigger_safe_stop(self):
        """Send zero velocity and emergency stop signal."""
        self.get_logger().warn('Triggering safe stop due to heartbeat failure')
        # Publish zero velocity
        self.cmd_vel_pub.publish(Twist())
        # Publish emergency stop
        estop_msg = Bool()
        estop_msg.data = True
        self.estop_pub.publish(estop_msg)


def main():
    rclpy.init()
    node = HeartbeatMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Hardware Watchdog Integration

Many robot onboard computers have a hardware watchdog timer (e.g., Intel TCO, iTCO_wdt). If the software fails to pet the watchdog, the hardware performs a hard reboot.

```bash
# Enable the hardware watchdog in systemd
# /etc/systemd/system.conf
# RuntimeWatchdogSec=30
# RebootWatchdogSec=10min
# ShutdownWatchdogSec=10min

# Or configure per-service in the unit file:
# WatchdogSec=30 triggers systemd to restart the service
# The hardware watchdog (configured via RuntimeWatchdogSec) reboots
# the entire machine if systemd itself becomes unresponsive.

# Verify hardware watchdog is active
sudo cat /sys/class/watchdog/watchdog0/state
# Should output: active

# Check watchdog timeout
sudo cat /sys/class/watchdog/watchdog0/timeout
```

## Logging and Log Rotation

### ROS2 Log Configuration

```bash
# Set log level via environment
export RCUTILS_LOGGING_USE_STDOUT=0          # Log to stderr (captured by journald)
export RCUTILS_COLORIZED_OUTPUT=0            # Disable color codes in log files
export RCUTILS_CONSOLE_OUTPUT_FORMAT="[{severity}] [{time}] [{name}]: {message}"

# Set log level at runtime
ros2 run my_pkg my_node --ros-args --log-level debug
ros2 run my_pkg my_node --ros-args --log-level my_node:=debug

# Set log level via parameter (Humble+)
ros2 param set /my_node use_sim_time false
ros2 service call /my_node/set_logger_level rcl_interfaces/srv/SetLoggerLevel \
  "{logger_name: 'my_node', level: 10}"
```

### journald Configuration for ROS2 Services

```ini
# /etc/systemd/journald.conf.d/robot.conf
[Journal]
# Persist logs across reboots
Storage=persistent

# Limit total journal size to 1 GB
SystemMaxUse=1G

# Limit per-file size to 100 MB
SystemMaxFileSize=100M

# Keep logs for 30 days
MaxRetentionSec=30day

# Rate limit: allow bursts during startup
RateLimitIntervalSec=10s
RateLimitBurst=10000

# Forward to syslog for remote logging
ForwardToSyslog=yes
```

```bash
# View logs for a specific robot service
journalctl -u robot-drivers.service -f

# View logs since last boot
journalctl -u robot-bringup.service -b

# View logs with priority filtering (error and above)
journalctl -u robot-bringup.service -p err

# Export logs for analysis
journalctl -u robot-bringup.service --since "2024-01-01" --output=json > logs.json
```

### logrotate for ROS2 Log Files

ROS2 writes log files to `~/.ros/log/` by default, or to `$ROS_LOG_DIR`. These grow unbounded without rotation.

```ini
# /etc/logrotate.d/ros2
/var/log/ros2/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 robot robot
    maxsize 100M
    dateext
    dateformat -%Y%m%d
    postrotate
        # Notify ROS2 nodes to reopen log files (if using file logging)
        systemctl kill --signal=HUP robot-bringup.service 2>/dev/null || true
    endscript
}

/home/robot/.ros/log/**/*.log {
    daily
    rotate 3
    compress
    missingok
    notifempty
    maxsize 50M
}
```

### Structured Logging for Production

```python
import json
import logging
from rclpy.node import Node


class StructuredLogger:
    """Wraps ROS2 logger with structured JSON output for production monitoring."""

    def __init__(self, node: Node):
        self.node = node
        self.logger = node.get_logger()

    def log_event(self, event_type: str, level: str = 'info', **kwargs):
        """Log a structured event with key-value metadata."""
        entry = {
            'event': event_type,
            'node': self.node.get_name(),
            'namespace': self.node.get_namespace(),
            'stamp': self.node.get_clock().now().nanoseconds,
            **kwargs,
        }
        message = json.dumps(entry)
        getattr(self.logger, level)(message)


# Usage in a node:
# self.slog = StructuredLogger(self)
# self.slog.log_event('detection', count=5, latency_ms=12.3)
# self.slog.log_event('motor_fault', level='error', motor_id=2, code=0x0A)
```

## Graceful Shutdown Sequences

### Signal Handling in ROS2 Nodes

ROS2 nodes should handle `SIGINT` and `SIGTERM` to bring actuators to a safe state before exiting.

```python
#!/usr/bin/env python3
# safe_shutdown_node.py
# Demonstrates graceful shutdown with safe state transitions.

import signal
import sys

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool


class SafeShutdownNode(Node):
    def __init__(self):
        super().__init__('safe_shutdown_node')

        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.brake_pub = self.create_publisher(Bool, '/brakes/engage', 10)

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._shutdown_handler)
        signal.signal(signal.SIGINT, self._shutdown_handler)

        self.get_logger().info('Node started with graceful shutdown handler')

    def _shutdown_handler(self, signum, frame):
        """Handle shutdown signals by commanding safe state."""
        sig_name = signal.Signals(signum).name
        self.get_logger().warn(f'Received {sig_name}, initiating safe shutdown...')

        # Step 1: Command zero velocity immediately
        zero_twist = Twist()  # All fields default to 0.0
        for _ in range(5):
            self.cmd_vel_pub.publish(zero_twist)

        # Step 2: Engage brakes
        brake_msg = Bool()
        brake_msg.data = True
        self.brake_pub.publish(brake_msg)

        # Step 3: Wait briefly for commands to be received
        self.get_logger().info('Safe state commanded, shutting down...')

        # Step 4: Clean exit
        self.destroy_node()
        rclpy.shutdown()
        sys.exit(0)


def main():
    rclpy.init()
    node = SafeShutdownNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Ordered Shutdown via systemd Dependencies

The `PartOf` and `Before` directives ensure that application-level services are stopped before drivers, preventing the situation where a navigation node sends velocity commands after the motor driver has exited.

```ini
# /etc/systemd/system/robot-application.service
[Unit]
# ...
PartOf=robot-perception.service
Before=robot-perception.service

# When robot-perception stops, robot-application is stopped FIRST
# (Before= reverses the stop order relative to start order)

[Service]
# Use SIGINT for ROS2's signal handler, then SIGTERM, then SIGKILL
KillSignal=SIGINT
TimeoutStopSec=15
FinalKillSignal=SIGTERM
SendSIGKILL=yes
```

### Safe State on Shutdown

```python
# Use rclpy context shutdown callback for cleanup
import rclpy
from rclpy.node import Node


class ActuatorNode(Node):
    def __init__(self):
        super().__init__('actuator_node')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        # Register a callback that runs during rclpy.shutdown()
        context = self.context
        context.on_shutdown(self._on_shutdown)

    def _on_shutdown(self):
        """Called automatically during rclpy.shutdown()."""
        self.get_logger().info('Shutdown callback: commanding zero velocity')
        self.cmd_pub.publish(Twist())
```

## Remote Monitoring and Debugging

### SSH Tunneling for ROS2 Topics

Forward DDS traffic over SSH when direct network connectivity is not available (e.g., robot is on a cellular connection).

```bash
#!/bin/bash
# ssh-ros2-tunnel.sh
# Creates an SSH tunnel for ROS2 DDS traffic between local machine and robot.
# Usage: ./ssh-ros2-tunnel.sh robot@10.0.0.10

set -euo pipefail

ROBOT_HOST="${1:?Usage: $0 robot@host}"
DOMAIN_ID="${ROS_DOMAIN_ID:-0}"
BASE_PORT=$((7400 + 250 * DOMAIN_ID))

echo "Setting up SSH tunnel for ROS2 domain $DOMAIN_ID (ports $BASE_PORT-$((BASE_PORT + 200)))"

# Forward DDS discovery and data ports
ssh -N \
  -L ${BASE_PORT}:localhost:${BASE_PORT} \
  -L $((BASE_PORT + 1)):localhost:$((BASE_PORT + 1)) \
  -L $((BASE_PORT + 10)):localhost:$((BASE_PORT + 10)) \
  -L $((BASE_PORT + 11)):localhost:$((BASE_PORT + 11)) \
  "$ROBOT_HOST" &

SSH_PID=$!
echo "SSH tunnel PID: $SSH_PID"

# Set environment for local ROS2 to use localhost-only discovery
export ROS_LOCALHOST_ONLY=1
echo "Run: export ROS_LOCALHOST_ONLY=1"
echo "Then use ros2 topic list, ros2 topic echo, etc."
echo "Press Ctrl+C to close tunnel."

wait $SSH_PID
```

### Remote journalctl and Service Management

```bash
# View live robot logs remotely
ssh robot@10.0.0.10 'journalctl -u robot-bringup.service -f'

# Check service status
ssh robot@10.0.0.10 'systemctl status robot-drivers.service robot-perception.service'

# Restart a single layer without rebooting
ssh robot@10.0.0.10 'sudo systemctl restart robot-perception.service'

# View boot-time service ordering
ssh robot@10.0.0.10 'systemd-analyze blame | head -20'

# Check for failed services
ssh robot@10.0.0.10 'systemctl --failed'

# Stream structured logs as JSON
ssh robot@10.0.0.10 'journalctl -u robot-bringup.service -o json --follow'
```

### Deploying Updates via SSH

```bash
#!/bin/bash
# deploy-to-robot.sh
# Build locally, copy to robot, and restart services.
# Usage: ./deploy-to-robot.sh robot@10.0.0.10

set -euo pipefail

ROBOT_HOST="${1:?Usage: $0 robot@host}"
WORKSPACE="/home/robot/ros2_ws"

echo "=== Building workspace locally ==="
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release --packages-select my_robot_bringup

echo "=== Syncing to robot ==="
rsync -avz --delete \
  --exclude='build/' --exclude='log/' \
  src/ "${ROBOT_HOST}:${WORKSPACE}/src/"

echo "=== Building on robot ==="
ssh "$ROBOT_HOST" "cd ${WORKSPACE} && \
  source /opt/ros/\${ROS_DISTRO}/setup.bash && \
  colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release"

echo "=== Restarting robot services ==="
ssh "$ROBOT_HOST" 'sudo systemctl restart robot-bringup.target'

echo "=== Checking service status ==="
ssh "$ROBOT_HOST" 'sleep 3 && systemctl status robot-bringup.target --no-pager'

echo "Deploy complete."
```

## Robot Bringup Anti-Patterns

### 1. Sourcing setup.bash in .bashrc for systemd

**Problem:** systemd services do not load `~/.bashrc` or `~/.profile`. Environment variables set there are invisible to the service, causing ROS2 commands to fail with "command not found" or missing package errors.

```bash
# BAD: Relying on .bashrc for systemd services
# ~/.bashrc
source /opt/ros/humble/setup.bash  # systemd will never see this

# GOOD: Use EnvironmentFile in the service unit and source explicitly in ExecStart
# /etc/robot/ros2.env
ROS_DISTRO=humble
RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# In the service unit:
# EnvironmentFile=/etc/robot/ros2.env
# ExecStart=/bin/bash -c 'source /opt/ros/${ROS_DISTRO}/setup.bash && ...'
```

### 2. No Startup Ordering

**Problem:** Starting all ROS2 nodes simultaneously causes race conditions. A navigation node may attempt to call a service that has not yet been advertised by the driver, leading to intermittent startup failures.

**Fix:** Use `After=` and `Requires=` in systemd units, or use a lifecycle manager to enforce ordered transitions:

```ini
# BAD: All services start in parallel with no ordering
[Unit]
Description=Robot Navigation
# No After= or Requires= directives

# GOOD: Explicit dependency chain
[Unit]
Description=Robot Navigation
After=robot-perception.service
Requires=robot-perception.service
```

### 3. Using Restart=always Without Rate Limiting

**Problem:** A service that crashes on startup (e.g., missing config file, hardware disconnected) will restart in a tight loop, consuming CPU and flooding the journal.

**Fix:** Use `StartLimitIntervalSec` and `StartLimitBurst` to cap restart attempts:

```ini
# BAD: Infinite restart loop
[Service]
Restart=always
RestartSec=1

# GOOD: Rate-limited restarts with failure notification
[Service]
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=120
StartLimitBurst=5
```

### 4. Relying on network.target Instead of network-online.target

**Problem:** `network.target` is reached as soon as the network configuration starts, not when connectivity is actually established. DDS discovery fails because the network interface does not have an IP address yet.

**Fix:** Use `network-online.target` and ensure `systemd-networkd-wait-online.service` or `NetworkManager-wait-online.service` is enabled:

```ini
# BAD: network.target does not guarantee connectivity
[Unit]
After=network.target

# GOOD: Wait for actual network connectivity
[Unit]
After=network-online.target
Wants=network-online.target
```

### 5. No Log Rotation

**Problem:** ROS2 log files in `~/.ros/log/` and journal entries grow without limit, eventually filling the disk on an embedded system with limited storage.

**Fix:** Configure logrotate for ROS2 log files and set journald size limits:

```bash
# BAD: No log management
# Logs in ~/.ros/log/ grow forever, disk fills up after weeks of operation

# GOOD: logrotate config + journald limits
# /etc/logrotate.d/ros2 (see Logging section above)
# /etc/systemd/journald.conf: SystemMaxUse=1G
```

### 6. Hardcoded Device Paths (/dev/ttyUSB0)

**Problem:** `/dev/ttyUSB0` can be assigned to any USB serial device depending on enumeration order. After a reboot, the IMU might become `/dev/ttyUSB1` and the motor controller `/dev/ttyUSB0`, reversing the mapping.

**Fix:** Use udev rules to create stable symlinks:

```yaml
# BAD: Hardcoded device path in ROS2 params
serial_port: "/dev/ttyUSB0"  # Which device is this? It changes on reboot!

# GOOD: Stable symlink via udev rule
serial_port: "/dev/robot/imu"  # Always points to the correct device
```

### 7. Running the Entire Stack as Root

**Problem:** Running ROS2 as root is a security risk and can cause permission issues with `rosbag2`, log files, and parameter persistence. A bug in a ROS2 node could damage the operating system.

**Fix:** Create a dedicated `robot` user and grant only the necessary device permissions via udev `GROUP` and `MODE` rules:

```bash
# BAD: Running as root
# ExecStart=/bin/bash -c 'source /opt/ros/humble/setup.bash && ros2 launch ...'
# (runs as root because no User= is specified)

# GOOD: Dedicated user with minimal privileges
# Create robot user
sudo useradd -r -m -s /bin/bash robot
sudo usermod -aG dialout,video,plugdev robot

# In the service unit:
# User=robot
# Group=robot

# udev rules grant device access to the robot user's groups:
# MODE="0666", GROUP="dialout"
```

### 8. No Graceful Shutdown Handler

**Problem:** When systemd sends `SIGTERM` or `SIGINT` to stop a ROS2 node, the node exits immediately without commanding zero velocity or engaging brakes. The robot may coast or continue moving with the last commanded velocity.

**Fix:** Register signal handlers or use rclpy's shutdown callback to command a safe state:

```python
# BAD: No shutdown handling, node just exits
def main():
    rclpy.init()
    node = MotorControlNode()
    rclpy.spin(node)
    # Robot is still moving with last commanded velocity!

# GOOD: Shutdown handler commands safe state
def main():
    rclpy.init()
    node = MotorControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.command_zero_velocity()
        node.engage_brakes()
        node.destroy_node()
        rclpy.shutdown()
```

## Robot Bringup Checklist

1. **udev rules written and tested** for all USB devices (cameras, LiDARs, serial adapters) with stable symlinks under `/dev/robot/`
2. **systemd service units created** for each layer (drivers, perception, application) with correct `After=`/`Requires=` ordering
3. **ROS2 environment file** (`/etc/robot/ros2.env`) configured with `ROS_DISTRO`, `RMW_IMPLEMENTATION`, `ROS_DOMAIN_ID`, and `CYCLONEDDS_URI`
4. **CycloneDDS or FastDDS XML** configured with explicit peer list for multi-machine discovery
5. **Launch files layered and composable** with conditional arguments for sim/real and robot variants
6. **Health check scripts** written for `ExecStartPre` to verify device presence before starting drivers
7. **Watchdog integration** configured: `WatchdogSec` in service units and `sd_notify(WATCHDOG=1)` in the ROS2 process
8. **Heartbeat monitor node** deployed to detect node failures and trigger safe stop
9. **Graceful shutdown handlers** registered in all actuator nodes (zero velocity, engage brakes on `SIGINT`/`SIGTERM`)
10. **Log rotation configured** via logrotate for `$ROS_LOG_DIR` and journald `SystemMaxUse` limits
11. **Restart policies rate-limited** with `StartLimitIntervalSec` and `StartLimitBurst` to prevent restart loops
12. **Resource limits set** via `MemoryMax`, `CPUQuota` to prevent runaway nodes from starving the system
13. **Network and firewall configured** with static IPs, DDS port rules, and `ROS_LOCALHOST_ONLY` set correctly
14. **Full boot test performed** from power-off to autonomous operation, verifying service ordering and recovery from simulated failures
