---
name: sensor-simulation
description: Configure camera, LIDAR, IMU, and contact sensors on simulated robots in Gazebo
domain: authoring
version: 1.0.0
created: 2025-11-29
triggers:
  - Adding sensors to robot models
  - Configuring sensor parameters (resolution, range, noise)
  - Debugging sensor data issues
  - Visualizing sensor output
learned_from:
  - Module 2 Chapter 11 Sensors in Simulation (2025-11-29)
---

# Sensor Simulation Skill

## Persona

Think like a robotics perception engineer who integrates sensors into robot systems. You understand sensor physics, noise models, and data visualization. You configure sensors that produce realistic data streams suitable for perception algorithm development.

---

## Pre-Flight Questions

Before adding or configuring any sensor, ask yourself:

### 1. Sensor Purpose
- **Q**: What does the robot need to perceive?
  - **Visual**: Camera for images, object detection
  - **Distance**: LIDAR for mapping, obstacle detection
  - **Motion**: IMU for orientation, acceleration
  - **Touch**: Contact for collision detection

### 2. Sensor Placement
- **Q**: Where should the sensor be mounted?
  - **Impact**: FOV coverage, occlusion, stability
  - Forward-facing camera → front of robot
  - 360° LIDAR → top center, unobstructed
  - IMU → center of mass, rigidly mounted

### 3. Performance Trade-offs
- **Q**: What resolution/rate is needed?
  - **High resolution**: Better data, more computation
  - **High rate**: Better responsiveness, more bandwidth
  - Balance based on application requirements

---

## Principles

### Principle 1: Sensor Structure in SDF

Sensors are added to links within robot models:

```xml
<link name="camera_link">
  <!-- Visual and collision for the sensor housing -->
  <visual>...</visual>
  <collision>...</collision>
  <inertial>...</inertial>

  <!-- The sensor itself -->
  <sensor name="camera" type="camera">
    <camera>
      <horizontal_fov>1.047</horizontal_fov>
      <image>
        <width>640</width>
        <height>480</height>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <always_on>1</always_on>
    <update_rate>30</update_rate>
    <topic>camera/image</topic>
  </sensor>
</link>
```

### Principle 2: Camera Configuration

```xml
<sensor name="front_camera" type="camera">
  <camera>
    <!-- Field of view in radians (60° = 1.047 rad) -->
    <horizontal_fov>1.047</horizontal_fov>

    <!-- Image dimensions -->
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>

    <!-- Depth range -->
    <clip>
      <near>0.1</near>
      <far>100</far>
    </clip>
  </camera>

  <always_on>1</always_on>
  <update_rate>30</update_rate>
  <visualize>true</visualize>
  <topic>camera/image</topic>
</sensor>
```

Common resolutions:
- 640x480: Standard, good performance
- 1280x720: HD, more detail
- 320x240: Low-res, fast processing

### Principle 3: LIDAR Configuration

```xml
<sensor name="lidar" type="gpu_lidar">
  <lidar>
    <scan>
      <horizontal>
        <samples>360</samples>
        <resolution>1</resolution>
        <min_angle>-3.14159</min_angle>
        <max_angle>3.14159</max_angle>
      </horizontal>
      <vertical>
        <samples>1</samples>
        <resolution>1</resolution>
        <min_angle>0</min_angle>
        <max_angle>0</max_angle>
      </vertical>
    </scan>
    <range>
      <min>0.1</min>
      <max>10</max>
      <resolution>0.01</resolution>
    </range>
    <noise>
      <type>gaussian</type>
      <mean>0</mean>
      <stddev>0.01</stddev>
    </noise>
  </lidar>

  <always_on>1</always_on>
  <update_rate>10</update_rate>
  <visualize>true</visualize>
  <topic>lidar/scan</topic>
</sensor>
```

Key parameters:
- `samples`: Points per scan (more = denser)
- `min/max_angle`: Scan coverage (-π to π = 360°)
- `min/max range`: Detection distance limits
- `noise`: Gaussian noise for realism

### Principle 4: IMU Configuration

```xml
<sensor name="imu" type="imu">
  <imu>
    <angular_velocity>
      <x>
        <noise type="gaussian">
          <mean>0</mean>
          <stddev>0.01</stddev>
        </noise>
      </x>
      <!-- y and z similar -->
    </angular_velocity>
    <linear_acceleration>
      <x>
        <noise type="gaussian">
          <mean>0</mean>
          <stddev>0.1</stddev>
        </noise>
      </x>
      <!-- y and z similar -->
    </linear_acceleration>
  </imu>

  <always_on>1</always_on>
  <update_rate>100</update_rate>
  <topic>imu/data</topic>
</sensor>
```

IMU outputs:
- `angular_velocity`: Rotation rate (rad/s)
- `linear_acceleration`: Includes gravity!
- `orientation`: Quaternion (if available)

### Principle 5: Add Noise for Realism

Real sensors have noise. Simulated sensors should too:

```xml
<noise>
  <type>gaussian</type>
  <mean>0</mean>
  <stddev>0.01</stddev>  <!-- Adjust based on sensor quality -->
</noise>
```

Typical noise levels:
- High-quality LIDAR: stddev 0.005-0.01m
- Consumer LIDAR: stddev 0.02-0.05m
- IMU gyro: stddev 0.01-0.05 rad/s
- IMU accel: stddev 0.1-0.5 m/s²

---

## Debugging Sensor Issues

### Sensor Not Publishing

1. Check topic name matches subscriber
2. Verify `<always_on>1</always_on>`
3. Confirm sensor plugin is loaded
4. Check `gz topic -l` for available topics

### Data All Zeros

1. Sensor origin inside robot body (collision)
2. Nothing in sensor's field of view
3. Range limits too restrictive

### Noisy/Unstable Data

1. Noise parameters too high
2. Physics timestep too large
3. Sensor update rate too fast

---

## Checklist

Before finalizing any sensor configuration:

- [ ] Sensor attached to correct link
- [ ] Origin places sensor at correct position
- [ ] FOV/range covers intended area
- [ ] Update rate appropriate for application
- [ ] Noise model added for realism
- [ ] Topic name is unique and descriptive
- [ ] `visualize` enabled for debugging
- [ ] Data appears in `gz topic -e`
- [ ] Data format matches ROS 2 expectations

---

## Integration

This skill is used by:
- `content-implementer` agent when generating Module 2 lessons
- Students learning sensor simulation in Chapter 11
- Perception algorithm development and testing

**Dependencies**:
- `urdf-robot-model` - sensors attach to robot links
- `gazebo-world-builder` - sensors perceive the world
- `ros2-gazebo-bridge` - sensor data bridges to ROS 2
