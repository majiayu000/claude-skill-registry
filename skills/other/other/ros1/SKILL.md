---
name: ros1-development
description: >
  Best practices, design patterns, and common pitfalls for ROS1 (Robot Operating System 1) development.
  Use this skill when building ROS1 nodes, packages, launch files, or debugging ROS1 systems. Trigger
  whenever the user mentions ROS1, catkin, rospy, roscpp, roslaunch, roscore, rostopic, tf, actionlib,
  message types, services, or any ROS1-era robotics middleware. Also trigger for migrating ROS1 code
  to ROS2, maintaining legacy ROS1 systems, or building ROS1-ROS2 bridges. Covers catkin workspaces,
  nodelets, dynamic reconfigure, pluginlib, and the full ROS1 ecosystem.
---

# ROS1 Development Skill

## When to Use This Skill
- Building or maintaining ROS1 packages and nodes
- Writing launch files, message types, or services
- Debugging ROS1 communication (topics, services, actions)
- Configuring catkin workspaces and build systems
- Working with tf/tf2 transforms, URDF, or robot models
- Using actionlib for long-running tasks
- Optimizing nodelets for zero-copy transport
- Planning ROS1 → ROS2 migration

## Core Architecture Principles

### 1. Node Design

**Single Responsibility Nodes**: Each node should do ONE thing well. Resist the temptation to build monolithic "do-everything" nodes.

```python
# BAD: Monolithic node
class RobotNode:
    def __init__(self):
        self.sub_camera = rospy.Subscriber('/camera/image', Image, self.camera_cb)
        self.sub_lidar = rospy.Subscriber('/lidar/points', PointCloud2, self.lidar_cb)
        self.pub_cmd = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.pub_map = rospy.Publisher('/map', OccupancyGrid, queue_size=1)
        # This node does perception, planning, AND control

# GOOD: Decomposed nodes
class PerceptionNode:    # Fuses sensor data → publishes /obstacles
class PlannerNode:       # Subscribes /obstacles → publishes /path
class ControllerNode:    # Subscribes /path → publishes /cmd_vel
```

**Node Initialization Pattern**:
```python
#!/usr/bin/env python
import rospy
from std_msgs.msg import String

class MyNode:
    def __init__(self):
        rospy.init_node('my_node', anonymous=False)

        # 1. Load parameters FIRST
        self.rate = rospy.get_param('~rate', 10.0)
        self.frame_id = rospy.get_param('~frame_id', 'base_link')

        # 2. Set up publishers BEFORE subscribers
        #    (prevents callbacks firing before publisher is ready)
        self.pub = rospy.Publisher('~output', String, queue_size=10)

        # 3. Set up subscribers LAST
        self.sub = rospy.Subscriber('~input', String, self.callback)

        rospy.loginfo(f"[{rospy.get_name()}] Initialized with rate={self.rate}")

    def callback(self, msg):
        # Process and republish
        result = String(data=msg.data.upper())
        self.pub.publish(result)

    def run(self):
        rate = rospy.Rate(self.rate)
        while not rospy.is_shutdown():
            # Periodic work here
            rate.sleep()

if __name__ == '__main__':
    try:
        node = MyNode()
        node.run()
    except rospy.ROSInterruptException:
        pass
```

### 2. Topic Design

**Naming Conventions**:
```
/robot_name/sensor_type/data_type

# Examples:
/ur5/joint_states              # Robot joint states
/realsense/color/image_raw     # Camera color image
/realsense/depth/points        # Depth point cloud
/mobile_base/cmd_vel           # Velocity commands
/gripper/command               # Gripper commands
```

**Queue Sizes Matter**:
```python
# For sensor data (high frequency, OK to drop old messages):
rospy.Subscriber('/camera/image', Image, self.cb, queue_size=1)

# For commands (don't want to miss any):
rospy.Publisher('/cmd_vel', Twist, queue_size=10)

# For large data (point clouds, images) - use small queues to prevent memory bloat:
rospy.Subscriber('/lidar/points', PointCloud2, self.cb, queue_size=1)

# NEVER use queue_size=0 (infinite) for high-frequency topics
# This WILL cause memory leaks under load
```

**Latched Topics** for data that changes infrequently:
```python
# Robot description, static maps, calibration data
pub = rospy.Publisher('/robot_description', String, queue_size=1, latch=True)
```

### 3. Launch File Best Practices

```xml
<launch>
  <!-- ALWAYS use args for configurability -->
  <arg name="robot_name" default="ur5"/>
  <arg name="sim" default="false"/>
  <arg name="debug" default="false"/>

  <!-- Group by subsystem with namespaces -->
  <group ns="$(arg robot_name)">

    <!-- Conditional loading based on sim vs real -->
    <group if="$(arg sim)">
      <include file="$(find my_pkg)/launch/sim_drivers.launch"/>
    </group>
    <group unless="$(arg sim)">
      <include file="$(find my_pkg)/launch/real_drivers.launch"/>
    </group>

    <!-- Node with proper remapping -->
    <node pkg="my_pkg" type="perception_node.py" name="perception"
          output="screen" respawn="true" respawn_delay="5">
      <param name="rate" value="30.0"/>
      <param name="frame_id" value="$(arg robot_name)_base_link"/>
      <remap from="~input_image" to="/$(arg robot_name)/camera/image_raw"/>
      <remap from="~output_detections" to="detections"/>
      <!-- Load a YAML param file -->
      <rosparam file="$(find my_pkg)/config/perception.yaml" command="load"/>
    </node>

  </group>

  <!-- Debug tools (conditionally loaded) -->
  <group if="$(arg debug)">
    <node pkg="rviz" type="rviz" name="rviz"
          args="-d $(find my_pkg)/rviz/debug.rviz"/>
    <node pkg="rqt_graph" type="rqt_graph" name="rqt_graph"/>
  </group>
</launch>
```

### 4. TF Transform Tree

**Rules**:
- Every frame has EXACTLY one parent (tree, not graph)
- Static transforms use `static_transform_publisher`
- Dynamic transforms publish at consistent rates
- ALWAYS set timestamps correctly

```python
import tf2_ros

# Publishing transforms
br = tf2_ros.TransformBroadcaster()
t = TransformStamped()
t.header.stamp = rospy.Time.now()  # CRITICAL: Use current time
t.header.frame_id = "odom"
t.child_frame_id = "base_link"
t.transform.translation.x = x
t.transform.translation.y = y
t.transform.rotation = quaternion_from_euler(0, 0, theta)
br.sendTransform(t)

# Listening for transforms (with timeout and exception handling)
tf_buffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tf_buffer)

try:
    trans = tf_buffer.lookup_transform(
        'map', 'base_link',
        rospy.Time(0),          # Get latest available
        rospy.Duration(1.0)     # Wait up to 1 second
    )
except (tf2_ros.LookupException,
        tf2_ros.ConnectivityException,
        tf2_ros.ExtrapolationException) as e:
    rospy.logwarn(f"TF lookup failed: {e}")
```

### 5. Actionlib for Long-Running Tasks

```python
import actionlib
from my_msgs.msg import PickPlaceAction, PickPlaceGoal, PickPlaceResult

# Server
class PickPlaceServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer(
            'pick_place',
            PickPlaceAction,
            execute_cb=self.execute,
            auto_start=False  # ALWAYS set auto_start=False
        )
        self.server.start()

    def execute(self, goal):
        feedback = PickPlaceFeedback()

        # Check for preemption INSIDE your loop
        for step in self.plan_steps(goal):
            if self.server.is_preempt_requested():
                self.server.set_preempted()
                return
            self.execute_step(step)
            feedback.progress = step.progress
            self.server.publish_feedback(feedback)

        result = PickPlaceResult(success=True)
        self.server.set_succeeded(result)
```

## Common Pitfalls & Failure Modes

### Time Synchronization
```python
# BAD: Comparing timestamps from different clocks
if camera_msg.header.stamp == lidar_msg.header.stamp:  # Almost never true

# GOOD: Use message_filters for approximate time sync
import message_filters
sub_cam = message_filters.Subscriber('/camera/image', Image)
sub_lidar = message_filters.Subscriber('/lidar/points', PointCloud2)
sync = message_filters.ApproximateTimeSynchronizer(
    [sub_cam, sub_lidar], queue_size=10, slop=0.05  # 50ms tolerance
)
sync.registerCallback(self.synced_callback)
```

### Callback Threading
```python
# ROS1 uses a single-threaded spinner by default.
# Long-running callbacks BLOCK all other callbacks.

# BAD:
def callback(self, msg):
    result = self.expensive_computation(msg)  # Blocks for 2 seconds!
    self.pub.publish(result)

# GOOD: Use a MultiThreadedSpinner or process in a separate thread
rospy.init_node('my_node')
# ... setup ...
spinner = rospy.MultiThreadedSpinner(num_threads=4)
spinner.spin()

# Or use a processing thread:
import threading, queue
class MyNode:
    def __init__(self):
        self.work_queue = queue.Queue(maxsize=1)
        self.worker = threading.Thread(target=self._process_loop, daemon=True)
        self.worker.start()

    def callback(self, msg):
        try:
            self.work_queue.put_nowait(msg)  # Non-blocking
        except queue.Full:
            pass  # Drop old data

    def _process_loop(self):
        while not rospy.is_shutdown():
            msg = self.work_queue.get()
            result = self.expensive_computation(msg)
            self.pub.publish(result)
```

### Parameter Server Anti-Patterns
```python
# BAD: Hardcoded values
self.threshold = 0.5

# BAD: Global params without namespace
self.threshold = rospy.get_param('threshold', 0.5)  # Collides across nodes

# GOOD: Private params with defaults
self.threshold = rospy.get_param('~threshold', 0.5)

# GOOD: Dynamic reconfigure for runtime tuning
from dynamic_reconfigure.server import Server
from my_pkg.cfg import MyNodeConfig
self.dyn_server = Server(MyNodeConfig, self.dyn_callback)
```

## Nodelets for Zero-Copy Transport

When nodes exchange large data (images, point clouds) within the same process, nodelets eliminate serialization overhead:

```cpp
// my_nodelet.h
#include <nodelet/nodelet.h>
#include <pluginlib/class_list_macros.h>

class MyNodelet : public nodelet::Nodelet {
  virtual void onInit() {
    ros::NodeHandle& nh = getNodeHandle();
    ros::NodeHandle& pnh = getPrivateNodeHandle();
    // Use shared_ptr for zero-copy: pass pointers, not copies
    pub_ = nh.advertise<sensor_msgs::Image>("output", 1);
    sub_ = nh.subscribe("input", 1, &MyNodelet::callback, this);
  }
};
PLUGINLIB_EXPORT_CLASS(MyNodelet, nodelet::Nodelet)
```

## Package Structure

```
my_robot_pkg/
├── CMakeLists.txt
├── package.xml
├── setup.py                    # For Python packages
├── config/
│   ├── robot_params.yaml       # Default parameters
│   └── dynamic_reconfigure/    # .cfg files
├── launch/
│   ├── robot.launch            # Top-level launcher
│   ├── drivers.launch          # Hardware drivers
│   └── perception.launch       # Perception pipeline
├── msg/                        # Custom message definitions
│   └── Detection.msg
├── srv/                        # Service definitions
│   └── GetPose.srv
├── action/                     # Action definitions
│   └── PickPlace.action
├── src/                        # C++ source
│   └── my_node.cpp
├── scripts/                    # Python nodes (executable)
│   └── perception_node.py
├── include/my_robot_pkg/       # C++ headers
│   └── my_node.h
├── rviz/                       # RViz configs
│   └── debug.rviz
├── urdf/                       # Robot model
│   └── robot.urdf.xacro
└── test/                       # Unit and integration tests
    ├── test_perception.py
    └── test_perception.test    # rostest launch file
```

## Debugging Toolkit

```bash
# Essential diagnostic commands
rostopic list                     # See all active topics
rostopic hz /camera/image_raw     # Check publish rate
rostopic bw /lidar/points         # Check bandwidth
rostopic echo /joint_states -n 1  # Inspect one message

rosnode list                      # Active nodes
rosnode info /perception          # Connections and subscriptions

roswtf                            # Automated diagnostics

rqt_graph                         # Visual node/topic graph
rqt_console                       # Log viewer with filtering

# TF debugging
rosrun tf tf_monitor              # Monitor TF tree health
rosrun tf view_frames             # Generate TF tree PDF
rosrun tf tf_echo map base_link   # Print transform continuously

# Bag file operations
rosbag record -a                  # Record everything (careful with disk!)
rosbag record /camera/image /tf   # Record specific topics
rosbag info recording.bag         # Inspect bag contents
rosbag play recording.bag --clock # Playback with simulated time
```

## ROS1 → ROS2 Migration Checklist

When planning a migration, note these key differences:
- `rospy` → `rclpy`, `roscpp` → `rclcpp`
- `catkin_make` → `colcon build`
- `roslaunch` XML → ROS2 Python launch files
- Global parameter server → Per-node parameters
- `rospy.Rate` → `node.create_timer()`
- Single `roscore` → DDS discovery (no central master)
- `message_filters` works in both, but API differs
- Custom messages: same `.msg` format, different build system
- Nodelets → ROS2 Components (intra-process communication)
- `dynamic_reconfigure` → ROS2 parameters with callbacks

Start migration from leaf nodes (sensors, actuators) and work inward.
Use the `ros1_bridge` package to run both stacks simultaneously during transition.
