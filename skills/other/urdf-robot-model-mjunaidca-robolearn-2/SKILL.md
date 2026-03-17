---
name: urdf-robot-model
description: Create robot models using URDF with proper links, joints, visual geometry, collision shapes, and physical properties
domain: authoring
version: 1.0.0
created: 2025-11-29
triggers:
  - Creating new robot URDF files
  - Adding physical properties to robot models
  - Debugging URDF parsing errors
  - Converting robot designs to URDF format
learned_from:
  - Module 2 Chapter 9 Robot Description (2025-11-29)
---

# URDF Robot Model Skill

## Persona

Think like a robotics mechanical engineer who designs robot models for simulation. You understand the relationship between visual appearance, collision geometry, and physical dynamics. You create URDFs that load without errors, simulate realistically, and are maintainable through xacro modularity.

---

## Pre-Flight Questions

Before creating or modifying any URDF, ask yourself:

### 1. Robot Structure
- **Q**: What is the kinematic chain of this robot?
  - **Impact**: Determines link hierarchy and joint connections
  - Base link → intermediate links → end effectors

- **Q**: What joint types are needed?
  - **fixed**: No motion (sensor mounts, rigid connections)
  - **revolute**: Rotation with limits (arms, hinges)
  - **continuous**: Unlimited rotation (wheels, propellers)
  - **prismatic**: Linear motion (lifts, slides)

### 2. Physical Realism
- **Q**: Does every link have mass and inertia?
  - **Without**: Robot floats, behaves unrealistically
  - **With**: Proper gravity response, stable physics

- **Q**: Are collision shapes simpler than visual shapes?
  - **Visual**: Detailed mesh for appearance
  - **Collision**: Simplified primitives for performance

### 3. Coordinate Frames
- **Q**: Is the origin at the correct location?
  - Links: Origin typically at joint attachment point
  - Joints: Origin at rotation/translation axis

- **Q**: Are all rotations in radians (not degrees)?

---

## Principles

### Principle 1: Every Link Needs Three Elements

```xml
<link name="base_link">
  <!-- Visual: What you see -->
  <visual>
    <geometry><box size="0.3 0.2 0.1"/></geometry>
    <material name="blue"/>
  </visual>

  <!-- Collision: What physics uses -->
  <collision>
    <geometry><box size="0.3 0.2 0.1"/></geometry>
  </collision>

  <!-- Inertial: How it responds to forces -->
  <inertial>
    <mass value="5.0"/>
    <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.02" iyz="0" izz="0.03"/>
  </inertial>
</link>
```

Missing any element causes problems:
- No visual → invisible robot
- No collision → passes through objects
- No inertial → unstable physics

### Principle 2: Joint Axis and Origin Matter

```xml
<joint name="wheel_joint" type="continuous">
  <parent link="base_link"/>
  <child link="wheel_link"/>
  <!-- Origin: Where child attaches relative to parent -->
  <origin xyz="0 0.15 0" rpy="1.5708 0 0"/>
  <!-- Axis: Direction of rotation/translation -->
  <axis xyz="0 0 1"/>
</joint>
```

Common mistakes:
- Wrong axis → wheel rotates incorrectly
- Wrong origin → parts don't align
- Missing rpy → incorrect orientation

### Principle 3: Use Standard Inertia Formulas

**Box** (dimensions a, b, c; mass m):
```
ixx = m/12 * (b² + c²)
iyy = m/12 * (a² + c²)
izz = m/12 * (a² + b²)
```

**Cylinder** (radius r, length h; mass m):
```
ixx = iyy = m/12 * (3r² + h²)
izz = m/2 * r²
```

**Sphere** (radius r; mass m):
```
ixx = iyy = izz = 2/5 * m * r²
```

### Principle 4: Validate Before Simulating

```bash
# Check URDF syntax
check_urdf robot.urdf

# Visualize in RViz
ros2 launch urdf_tutorial display.launch.py model:=robot.urdf

# Expected output for valid URDF:
# robot name is: my_robot
# ---------- Successfully Coverage [6] link(s)  ----------
```

---

## Common Patterns

### Differential Drive Robot

```xml
<?xml version="1.0"?>
<robot name="diff_drive">
  <!-- Base -->
  <link name="base_link">
    <visual><geometry><box size="0.3 0.2 0.1"/></geometry></visual>
    <collision><geometry><box size="0.3 0.2 0.1"/></geometry></collision>
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.02" ixy="0" ixz="0" iyy="0.03" iyz="0" izz="0.04"/>
    </inertial>
  </link>

  <!-- Left Wheel -->
  <link name="left_wheel">
    <visual><geometry><cylinder radius="0.05" length="0.02"/></geometry></visual>
    <collision><geometry><cylinder radius="0.05" length="0.02"/></geometry></collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.0003" ixy="0" ixz="0" iyy="0.0003" iyz="0" izz="0.0006"/>
    </inertial>
  </link>

  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0 0.11 -0.03" rpy="-1.5708 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

  <!-- Right Wheel (similar, opposite y) -->
  <!-- Caster (sphere, fixed joint) -->
</robot>
```

### Sensor Mount

```xml
<link name="camera_link">
  <visual><geometry><box size="0.02 0.04 0.02"/></geometry></visual>
  <collision><geometry><box size="0.02 0.04 0.02"/></geometry></collision>
  <inertial>
    <mass value="0.1"/>
    <inertia ixx="0.00001" ixy="0" ixz="0" iyy="0.00001" iyz="0" izz="0.00001"/>
  </inertial>
</link>

<joint name="camera_joint" type="fixed">
  <parent link="base_link"/>
  <child link="camera_link"/>
  <origin xyz="0.15 0 0.05" rpy="0 0 0"/>
</joint>
```

---

## Checklist

Before finalizing any URDF:

- [ ] Every link has visual, collision, and inertial
- [ ] All joints have correct type (fixed/revolute/continuous/prismatic)
- [ ] Joint origins place child links correctly
- [ ] Joint axes point in correct direction
- [ ] Inertia values are positive and reasonable
- [ ] `check_urdf` passes without errors
- [ ] Robot visualizes correctly in RViz
- [ ] Physics simulation is stable in Gazebo

---

## Integration

This skill is used by:
- `content-implementer` agent when generating Module 2 lessons
- Students learning robot modeling in Chapter 9
- Future robotics courses requiring robot descriptions

**Dependencies**:
- `gazebo-world-builder` - for placing robots in worlds
- `sensor-simulation` - for adding sensors to robots
- `ros2-gazebo-bridge` - for controlling robots from ROS 2
