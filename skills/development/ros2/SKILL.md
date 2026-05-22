---
name: ros2-development
description: >
  Comprehensive best practices, design patterns, and common pitfalls for ROS2 (Robot Operating System 2)
  development. Use this skill when building ROS2 nodes, packages, launch files, components, or debugging
  ROS2 systems. Trigger whenever the user mentions ROS2, colcon, rclpy, rclcpp, DDS, QoS, lifecycle nodes,
  managed nodes, ROS2 launch, ROS2 parameters, ROS2 actions, nav2, MoveIt2, micro-ROS, or any ROS2-era
  robotics middleware. Also trigger for ROS2 workspace setup, DDS tuning, intra-process communication,
  ROS2 security, or deploying ROS2 in production. Also trigger for colcon build issues, ament_cmake,
  ament_python, CMakeLists.txt for ROS2, package.xml dependencies, rosdep, workspace overlays, custom
  message generation, or ROS2 build troubleshooting. Covers Humble, Iron, Jazzy, and Rolling distributions.
---

# ROS2 Development Skill

## When to Use This Skill
- Building ROS2 packages, nodes, or component containers
- Setting up colcon workspaces, ament_cmake, or ament_python packages
- Writing CMakeLists.txt, package.xml, or setup.py for ROS2
- Defining custom messages, services, or actions
- Writing Python launch files with conditional logic
- Configuring DDS middleware and QoS profiles
- Implementing lifecycle (managed) nodes
- Working with Nav2, MoveIt2, or other ROS2 frameworks
- Debugging DDS discovery, QoS mismatches, or build failures
- Deploying ROS2 to production or embedded systems (micro-ROS)
- Setting up CI/CD for ROS2 packages

## Core Architecture

### 1. Node Design Patterns

**Basic Node (rclpy)**:
```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')

        # 1. Declare parameters with types and descriptions
        self.declare_parameter('rate_hz', 30.0,
            descriptor=ParameterDescriptor(
                description='Processing rate in Hz',
                floating_point_range=[FloatingPointRange(
                    from_value=1.0, to_value=120.0, step=0.0
                )]
            ))
        self.declare_parameter('confidence_threshold', 0.7)
        self.declare_parameter('frame_id', 'camera_link')

        # 2. Read parameters
        rate_hz = self.get_parameter('rate_hz').value
        self.threshold = self.get_parameter('confidence_threshold').value
        self.frame_id = self.get_parameter('frame_id').value

        # 3. Set up QoS profiles
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # 4. Publishers first, then subscribers
        self.det_pub = self.create_publisher(
            DetectionArray, 'detections', reliable_qos)

        self.image_sub = self.create_subscription(
            Image, 'camera/image_raw', self.image_callback, sensor_qos)

        # 5. Timers for periodic work
        self.timer = self.create_timer(1.0 / rate_hz, self.timer_callback)

        # 6. Parameter change callback
        self.add_on_set_parameters_callback(self.param_callback)

        self.get_logger().info(
            f'Perception node started at {rate_hz}Hz, '
            f'threshold={self.threshold}')

    def param_callback(self, params):
        """Handle runtime parameter changes (replaces dynamic_reconfigure)"""
        for param in params:
            if param.name == 'confidence_threshold':
                self.threshold = param.value
                self.get_logger().info(f'Threshold updated to {param.value}')
        return SetParametersResult(successful=True)

    def image_callback(self, msg):
        # Process incoming images
        pass

    def timer_callback(self):
        # Periodic work
        pass

def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Basic Node (rclcpp)**:
```cpp
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <vision_msgs/msg/detection2_d.hpp>
#include <memory>

class PerceptionNode : public rclcpp::Node {
public:
    PerceptionNode() : Node("perception_node") {
        // Declare and get parameters
        this->declare_parameter("rate_hz", 30.0);
        this->declare_parameter("confidence_threshold", 0.7);
        double rate_hz = this->get_parameter("rate_hz").as_double();

        // QoS
        auto sensor_qos = rclcpp::SensorDataQoS();
        auto reliable_qos = rclcpp::QoS(10).reliable();

        // Publishers and subscribers
        det_pub_ = this->create_publisher<vision_msgs::msg::Detection2D>("detections", reliable_qos);
        image_sub_ = this->create_subscription<sensor_msgs::msg::Image>(
            "camera/image_raw", sensor_qos, [this](const std::shared_ptr<const sensor_msgs::msg::Image>& msg){
                this->image_callback(msg);
            });

        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(static_cast<int>(1000.0 / rate_hz)),
            [this](){ this->timer_callback(); });

        RCLCPP_INFO(this->get_logger(), "Perception node started at %.1fHz", rate_hz);
    }

private:
    void image_callback(const std::shared_ptr<const sensor_msgs::msg::Image>& msg) {
        // Use shared_ptr for zero-copy potential
    }
    void timer_callback() {}

    rclcpp::Publisher<vision_msgs::msg::Detection2D>::SharedPtr det_pub_;
    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr image_sub_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<PerceptionNode>());
    rclcpp::shutdown();
    return 0;
}
```

### 2. Lifecycle (Managed) Nodes

Use lifecycle nodes for production systems where you need deterministic startup, shutdown, and error recovery. This is one of ROS2's most important features over ROS1.

**State Machine**: `Unconfigured → Inactive → Active → Finalized`

```python
from rclpy.lifecycle import Node as LifecycleNode, TransitionCallbackReturn

class ManagedPerception(LifecycleNode):
    def __init__(self):
        super().__init__('managed_perception')
        self.get_logger().info('Node created (unconfigured)')

    def on_configure(self, state) -> TransitionCallbackReturn:
        """Load params, allocate memory, set up pubs/subs (but don't activate)"""
        self.declare_parameter('model_path', '')
        model_path = self.get_parameter('model_path').value

        try:
            self.model = load_model(model_path)
            self.det_pub = self.create_lifecycle_publisher(
                DetectionArray, 'detections', 10)
            self.get_logger().info(f'Configured with model: {model_path}')
            return TransitionCallbackReturn.SUCCESS
        except Exception as e:
            self.get_logger().error(f'Configuration failed: {e}')
            return TransitionCallbackReturn.FAILURE

    def on_activate(self, state) -> TransitionCallbackReturn:
        """Start processing — subscriptions go live here"""
        self.image_sub = self.create_subscription(
            Image, 'camera/image_raw', self.image_callback, 1)
        self.get_logger().info('Activated — processing images')
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state) -> TransitionCallbackReturn:
        """Pause processing — safe to reconfigure after this"""
        self.destroy_subscription(self.image_sub)
        self.get_logger().info('Deactivated — stopped processing')
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state) -> TransitionCallbackReturn:
        """Release resources, return to unconfigured"""
        del self.model
        self.get_logger().info('Cleaned up')
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state) -> TransitionCallbackReturn:
        """Final cleanup before destruction"""
        self.get_logger().info('Shutting down')
        return TransitionCallbackReturn.SUCCESS

    def on_error(self, state) -> TransitionCallbackReturn:
        """Handle errors — try to recover or fail gracefully"""
        self.get_logger().error(f'Error in state {state.label}')
        return TransitionCallbackReturn.SUCCESS  # Transition to unconfigured
```

**Orchestrating Lifecycle Nodes** with a launch file:
```python
from launch import LaunchDescription
from launch_ros.actions import LifecycleNode
from launch_ros.event_handlers import OnStateTransition
from launch.actions import EmitEvent, RegisterEventHandler
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition

def generate_launch_description():
    perception = LifecycleNode(
        package='my_pkg', executable='managed_perception',
        name='perception', output='screen',
        parameters=[{'model_path': '/models/yolo.pt'}]
    )

    # Auto-configure on startup
    configure_event = EmitEvent(event=ChangeState(
        lifecycle_node_matcher=lambda node: node == perception,
        transition_id=Transition.TRANSITION_CONFIGURE
    ))

    # Auto-activate after successful configure
    activate_handler = RegisterEventHandler(OnStateTransition(
        target_lifecycle_node=perception,
        goal_state='inactive',
        entities=[EmitEvent(event=ChangeState(
            lifecycle_node_matcher=lambda node: node == perception,
            transition_id=Transition.TRANSITION_ACTIVATE
        ))]
    ))

    return LaunchDescription([
        perception,
        configure_event,
        activate_handler,
    ])
```

### 3. QoS (Quality of Service) — The #1 Source of ROS2 Bugs

QoS mismatches are the most common reason topics silently fail to connect.

**QoS Compatibility Matrix**:
```
Publisher     Subscriber    Compatible?
RELIABLE      RELIABLE      ✅ Yes
RELIABLE      BEST_EFFORT   ✅ Yes
BEST_EFFORT   BEST_EFFORT   ✅ Yes
BEST_EFFORT   RELIABLE      ❌ NO — SILENT FAILURE
```

**Recommended QoS Profiles by Use Case**:
```python
from rclpy.qos import (
    QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy,
    QoSDurabilityPolicy, QoSPresetProfiles
)

# Sensor data (cameras, lidars) — tolerate drops, want latest
SENSOR_QOS = QoSProfile(
    reliability=QoSReliabilityPolicy.BEST_EFFORT,
    history=QoSHistoryPolicy.KEEP_LAST,
    depth=1,
    durability=QoSDurabilityPolicy.VOLATILE
)

# Commands (velocity, joint) — never miss, small buffer
COMMAND_QOS = QoSProfile(
    reliability=QoSReliabilityPolicy.RELIABLE,
    history=QoSHistoryPolicy.KEEP_LAST,
    depth=10,
    durability=QoSDurabilityPolicy.VOLATILE
)

# Map / static data — reliable, and late joiners get it
MAP_QOS = QoSProfile(
    reliability=QoSReliabilityPolicy.RELIABLE,
    history=QoSHistoryPolicy.KEEP_LAST,
    depth=1,
    durability=QoSDurabilityPolicy.TRANSIENT_LOCAL  # Replaces ROS1 latch
)

# Default parameter/state — reliable with some history
STATE_QOS = QoSProfile(
    reliability=QoSReliabilityPolicy.RELIABLE,
    history=QoSHistoryPolicy.KEEP_LAST,
    depth=10
)
```

**Debugging QoS Issues**:
```bash
# Check QoS info for a topic
ros2 topic info /camera/image_raw -v
# Look for "Reliability" and "Durability" fields

# Check for incompatible QoS events
ros2 run rqt_topic rqt_topic  # Shows sub counts and QoS

# If 0 subscribers despite nodes running: QoS MISMATCH
```

### 4. Launch Files (Python-Based)

ROS2 launch files are Python, enabling powerful conditional logic:

```python
import os
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, IncludeLaunchDescription,
    GroupAction, OpaqueFunction, TimerAction
)
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import (
    LaunchConfiguration, PathJoinSubstitution,
    PythonExpression
)
from launch_ros.actions import Node, ComposableNodeContainer, LoadComposableNode
from launch_ros.descriptions import ComposableNode
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    # Arguments
    robot_name_arg = DeclareLaunchArgument('robot_name', default_value='ur5')
    sim_arg = DeclareLaunchArgument('sim', default_value='false')
    use_composition_arg = DeclareLaunchArgument('use_composition', default_value='true')

    robot_name = LaunchConfiguration('robot_name')
    sim = LaunchConfiguration('sim')

    # Load YAML params
    config_file = PathJoinSubstitution([
        FindPackageShare('my_pkg'), 'config', 'robot_params.yaml'
    ])

    # Standard node
    perception_node = Node(
        package='my_pkg',
        executable='perception_node',
        name='perception',
        namespace=robot_name,
        parameters=[config_file, {'use_sim_time': sim}],
        remappings=[
            ('camera/image_raw', 'realsense/color/image_raw'),
            ('detections', 'perception/detections'),
        ],
        output='screen',
        condition=UnlessCondition(LaunchConfiguration('use_composition')),
    )

    # Composable nodes (zero-copy, same process)
    composable_container = ComposableNodeContainer(
        name='perception_container',
        namespace=robot_name,
        package='rclcpp_components',
        executable='component_container_mt',  # Multi-threaded
        composable_node_descriptions=[
            ComposableNode(
                package='my_pkg',
                plugin='my_pkg::PerceptionComponent',
                name='perception',
                parameters=[config_file],
                remappings=[
                    ('camera/image_raw', 'realsense/color/image_raw'),
                ],
            ),
            ComposableNode(
                package='my_pkg',
                plugin='my_pkg::TrackerComponent',
                name='tracker',
            ),
        ],
        condition=IfCondition(LaunchConfiguration('use_composition')),
    )

    # Delayed start for nodes that need others to initialize first
    delayed_planner = TimerAction(
        period=3.0,
        actions=[
            Node(package='my_pkg', executable='planner_node', name='planner')
        ]
    )

    return LaunchDescription([
        robot_name_arg, sim_arg, use_composition_arg,
        perception_node,
        composable_container,
        delayed_planner,
    ])
```

### 5. Components (ROS2's Answer to Nodelets)

```cpp
#include <rclcpp/rclcpp.hpp>
#include <rclcpp_components/register_node_macro.hpp>
#include <sensor_msgs/msg/image.hpp>

namespace my_pkg {

class PerceptionComponent : public rclcpp::Node {
public:
    explicit PerceptionComponent(const rclcpp::NodeOptions& options)
        : Node("perception", options)
    {
        // Use intra-process communication for zero-copy
        auto sub_options = rclcpp::SubscriptionOptions();
        sub_options.use_intra_process_comm =
            rclcpp::IntraProcessSetting::Enable;

        sub_ = this->create_subscription<sensor_msgs::msg::Image>(
            "camera/image_raw",
            rclcpp::SensorDataQoS(),
            [this](sensor_msgs::msg::Image::UniquePtr msg) {
                this->callback(std::move(msg));
            },
            sub_options);
    }

private:
    void callback(sensor_msgs::msg::Image::UniquePtr msg) {
        // UniquePtr = zero-copy when:
        //   - publisher also uses UniquePtr
        //   - both subscriber and publisher use intra-process
        //   - this is the only subscriber
        // msg is moved, not copied
    }

    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_;
};

}  // namespace my_pkg

RCLCPP_COMPONENTS_REGISTER_NODE(my_pkg::PerceptionComponent)
```

### 6. Actions (ROS2 Style)

```python
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from my_interfaces.action import PickPlace

class PickPlaceServer(Node):
    def __init__(self):
        super().__init__('pick_place_server')
        self._action_server = ActionServer(
            self, PickPlace, 'pick_place',
            execute_callback=self.execute_cb,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb,
        )

    def goal_cb(self, goal_request):
        """Decide whether to accept or reject the goal"""
        self.get_logger().info(f'Received goal: {goal_request.target_pose}')
        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):
        """Decide whether to accept cancel requests"""
        self.get_logger().info('Cancel requested')
        return CancelResponse.ACCEPT

    async def execute_cb(self, goal_handle):
        """Execute the action (runs in an executor thread)"""
        feedback_msg = PickPlace.Feedback()

        for i, step in enumerate(self.plan(goal_handle.request)):
            # Check cancellation
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return PickPlace.Result(success=False)

            self.execute_step(step)
            feedback_msg.progress = float(i) / len(self.steps)
            goal_handle.publish_feedback(feedback_msg)

        goal_handle.succeed()
        return PickPlace.Result(success=True)
```

## DDS Configuration

### Choosing a DDS Implementation
```bash
# Set DDS middleware (in ~/.bashrc or launch)
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp    # Recommended for most cases
# export RMW_IMPLEMENTATION=rmw_fastrtps_cpp    # Default, good for multi-machine

# Limit DDS discovery to local machine (reduces network noise)
export ROS_LOCALHOST_ONLY=1

# Use ROS_DOMAIN_ID to isolate robot groups on same network
export ROS_DOMAIN_ID=42  # Range 0-101
```

### CycloneDDS Tuning (cyclonedds.xml)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<CycloneDDS xmlns="https://cdds.io/config">
  <Domain>
    <General>
      <NetworkInterfaceAddress>eth0</NetworkInterfaceAddress>
      <AllowMulticast>false</AllowMulticast>  <!-- Unicast for reliability -->
    </General>
    <Internal>
      <MaxMessageSize>65500</MaxMessageSize>
      <SocketReceiveBufferSize>10MB</SocketReceiveBufferSize>
    </Internal>
    <!-- For large data (images, point clouds) -->
    <Sizing>
      <ReceiveBufferSize>10MB</ReceiveBufferSize>
    </Sizing>
  </Domain>
</CycloneDDS>
```

```bash
export CYCLONEDDS_URI=file:///path/to/cyclonedds.xml
```

## Build System

### Workspace Setup and colcon

```bash
# Create a ROS2 workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Clone packages into src/
cd src
git clone https://github.com/org/my_robot_pkg.git
cd ..

# Install dependencies declared in package.xml files
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src -y

# Build the workspace
source /opt/ros/humble/setup.bash   # Source the ROS2 underlay FIRST
colcon build

# Source the workspace overlay
source install/setup.bash
```

**Essential colcon flags**:
```bash
# Build only specific packages (faster iteration)
colcon build --packages-select my_pkg

# Build a package and all its dependencies
colcon build --packages-up-to my_pkg

# Symlink Python files instead of copying (edit without rebuild)
colcon build --symlink-install

# Parallel jobs (default = nproc, lower if running out of RAM)
colcon build --parallel-workers 4

# Pass CMake args to all packages
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release

# Clean build (remove build/ install/ log/ and rebuild)
rm -rf build/ install/ log/
colcon build

# Build with compiler warnings as errors (CI)
colcon build --cmake-args -DCMAKE_CXX_FLAGS="-Wall -Werror"

# Show build output in real-time (useful for debugging build failures)
colcon build --event-handlers console_direct+
```

### Build Types: ament_cmake vs ament_python

Choose based on your package language:

```
ament_cmake     — C++ packages, mixed C++/Python packages, packages with custom msgs
ament_python    — Pure Python packages (no C++, no custom messages)
```

### package.xml — Declaring Dependencies

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd"
            schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_robot_pkg</name>
  <version>0.1.0</version>
  <description>My robot perception package</description>
  <maintainer email="dev@example.com">Dev Name</maintainer>
  <license>Apache-2.0</license>

  <!-- Build tool — determines build type -->
  <buildtool_depend>ament_cmake</buildtool_depend>
  <!-- For pure Python: <buildtool_depend>ament_python</buildtool_depend> -->

  <!-- Build-time dependencies (headers, CMake modules) -->
  <build_depend>rclcpp</build_depend>
  <build_depend>sensor_msgs</build_depend>
  <build_depend>OpenCV</build_depend>

  <!-- Runtime dependencies -->
  <exec_depend>rclcpp</exec_depend>
  <exec_depend>sensor_msgs</exec_depend>
  <exec_depend>rclpy</exec_depend>

  <!-- Shortcut: depend = build_depend + exec_depend -->
  <depend>rclcpp</depend>
  <depend>sensor_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>tf2_ros</depend>
  <depend>cv_bridge</depend>

  <!-- For custom message generation -->
  <build_depend>rosidl_default_generators</build_depend>
  <exec_depend>rosidl_default_runtime</exec_depend>
  <member_of_group>rosidl_interface_packages</member_of_group>

  <!-- Test dependencies -->
  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_cmake_pytest</test_depend>
  <test_depend>launch_testing_ament_cmake</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

### CMakeLists.txt — ament_cmake Package

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_pkg)

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ── Find dependencies ──────────────────────────────────────────
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(OpenCV REQUIRED)

# ── Custom messages / services / actions ───────────────────────
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Detection.msg"
  "srv/GetPose.srv"
  "action/PickPlace.action"
  DEPENDENCIES geometry_msgs sensor_msgs
)

# ── Standalone executable node ─────────────────────────────────
add_executable(perception_node src/perception_node.cpp)
ament_target_dependencies(perception_node
  rclcpp sensor_msgs cv_bridge OpenCV tf2_ros
)
install(TARGETS perception_node
  DESTINATION lib/${PROJECT_NAME}
)

# ── Component (composable node) ────────────────────────────────
add_library(perception_component SHARED
  src/perception_component.cpp
)
ament_target_dependencies(perception_component
  rclcpp rclcpp_components sensor_msgs cv_bridge OpenCV
)
# Register as a composable node
rclcpp_components_register_node(perception_component
  PLUGIN "my_robot_pkg::PerceptionComponent"
  EXECUTABLE perception_component_node
)
install(TARGETS perception_component
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

# ── Install Python nodes ───────────────────────────────────────
install(PROGRAMS
  scripts/planning_node.py
  DESTINATION lib/${PROJECT_NAME}
)

# ── Install launch, config, rviz, urdf ─────────────────────────
install(DIRECTORY
  launch config rviz urdf
  DESTINATION share/${PROJECT_NAME}
)

# ── Install headers ────────────────────────────────────────────
install(DIRECTORY include/
  DESTINATION include
)

# ── Tests ──────────────────────────────────────────────────────
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()

  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_perception test/test_perception.py)

  find_package(launch_testing_ament_cmake REQUIRED)
  add_launch_test(test/test_integration.py)
endif()

ament_package()
```

### setup.py / setup.cfg — Pure Python Package

```python
# setup.py (for ament_python packages)
from setuptools import find_packages, setup

package_name = 'my_python_pkg'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # Register with ament index
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        # Package manifest
        ('share/' + package_name, ['package.xml']),
        # Launch files
        ('share/' + package_name + '/launch',
            ['launch/robot.launch.py']),
        # Config files
        ('share/' + package_name + '/config',
            ['config/params.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Dev Name',
    maintainer_email='dev@example.com',
    description='My Python robot package',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            # format: 'executable_name = package.module:function'
            'perception_node = my_python_pkg.perception_node:main',
            'planner_node = my_python_pkg.planner_node:main',
        ],
    },
)
```

```cfg
# setup.cfg
[develop]
script_dir=$base/lib/my_python_pkg

[install]
install_scripts=$base/lib/my_python_pkg
```

### Custom Message, Service, and Action Definitions

```
# msg/Detection.msg
std_msgs/Header header
string class_name
float32 confidence
geometry_msgs/Pose pose
float32[4] bbox    # [x_min, y_min, x_max, y_max]
```

```
# srv/GetPose.srv
string object_name
---
bool success
geometry_msgs/PoseStamped pose
string error_message
```

```
# action/PickPlace.action
# Goal
geometry_msgs/Pose target_pose
string object_class
---
# Result
bool success
string error_message
---
# Feedback
float32 progress
string current_phase
```

### Workspace Overlays

```
Underlay (base ROS2)         /opt/ros/humble/
    ↑
Overlay 1 (shared libs)     ~/ros2_ws/install/
    ↑
Overlay 2 (your dev pkg)    ~/dev_ws/install/

Source order matters — LAST sourced overlay wins for duplicate packages.
```

```bash
# Correct source order
source /opt/ros/humble/setup.bash    # Base
source ~/ros2_ws/install/setup.bash  # Shared workspace
source ~/dev_ws/install/setup.bash   # Your development overlay

# NEVER source setup.bash from build/ — always use install/
```

### Build Troubleshooting

```bash
# "Package not found" during build
# → Missing dependency. Check package.xml and run:
rosdep install --from-paths src --ignore-src -y

# "Could not find a package configuration file provided by X"
# → CMake can't find the package. Did you source the underlay?
source /opt/ros/humble/setup.bash

# Build succeeds but node can't be found at runtime
# → Forgot to source the overlay, or entry_points misconfigured
source install/setup.bash
ros2 pkg list | grep my_pkg      # Should appear
ros2 pkg executables my_pkg      # List available executables

# Python changes not reflected after rebuild
# → Use --symlink-install, or clean and rebuild
colcon build --packages-select my_pkg --symlink-install

# "Multiple packages with the same name"
# → Duplicate package in workspace. Check with:
colcon list --packages-select my_pkg

# Build runs out of memory (large C++ packages)
colcon build --parallel-workers 2 --executor sequential

# Custom messages not found by Python nodes
# → Missing rosidl_default_runtime in package.xml exec_depend
# → Or forgot to source install/setup.bash after building msgs
```

## Package Structure (ROS2)

```
my_robot_pkg/
├── CMakeLists.txt              # Or setup.py for pure Python
├── package.xml
├── my_robot_pkg/               # Python module (same name as package)
│   ├── __init__.py
│   ├── perception_node.py
│   └── utils/
│       └── transforms.py
├── src/                        # C++ source
│   └── perception_component.cpp
├── include/my_robot_pkg/       # C++ headers
│   └── perception_component.hpp
├── config/
│   ├── robot_params.yaml
│   └── cyclonedds.xml
├── launch/
│   ├── robot.launch.py
│   └── perception.launch.py
├── msg/
│   └── Detection.msg
├── srv/
│   └── GetPose.srv
├── action/
│   └── PickPlace.action
├── rviz/
│   └── robot.rviz
├── urdf/
│   └── robot.urdf.xacro
└── test/
    ├── test_perception.py      # pytest
    └── test_integration.py     # launch_testing
```

## Debugging Toolkit

```bash
# Topic inspection
ros2 topic list
ros2 topic info /camera/image_raw -v  # Shows QoS details
ros2 topic hz /camera/image_raw
ros2 topic bw /camera/image_raw
ros2 topic echo /joint_states --once

# Node inspection
ros2 node list
ros2 node info /perception

# Parameter management
ros2 param list /perception
ros2 param get /perception confidence_threshold
ros2 param set /perception confidence_threshold 0.8  # Runtime change!

# Lifecycle management
ros2 lifecycle list /managed_perception
ros2 lifecycle set /managed_perception configure
ros2 lifecycle set /managed_perception activate

# Service calls
ros2 service list
ros2 service call /get_pose my_interfaces/srv/GetPose "{}"

# Action monitoring
ros2 action list
ros2 action info /pick_place
ros2 action send_goal /pick_place my_interfaces/action/PickPlace "{target_pose: {x: 1.0}}"

# Bag recording (ROS2 style)
ros2 bag record -a                              # All topics
ros2 bag record /camera/image /tf               # Specific topics
ros2 bag record -s mcap /camera/image           # MCAP format (recommended)
ros2 bag info recording/                        # Inspect
ros2 bag play recording/ --clock                # Playback

# DDS debugging
ros2 doctor                                     # System diagnostics
ros2 daemon stop && ros2 daemon start           # Reset discovery daemon
```

## Production Deployment Checklist

1. **Use lifecycle nodes** for all critical components
2. **Set `ROS_LOCALHOST_ONLY=1`** if not communicating across machines
3. **Pin your DDS implementation** (CycloneDDS recommended)
4. **Configure QoS explicitly** — never rely on defaults for production
5. **Set `ROS_DOMAIN_ID`** to isolate your robot from others on the network
6. **Enable ROS2 security** (SROS2) for authenticated communication
7. **Use composition** for nodes that exchange large data
8. **Record bags in MCAP format** — better tooling, random access, compression
9. **Set up launch-testing** for integration tests
10. **Use `ros2 doctor`** as part of your health check pipeline
