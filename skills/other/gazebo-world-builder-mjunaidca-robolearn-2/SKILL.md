---
name: gazebo-world-builder
description: Design simulation worlds using SDF with ground planes, models, physics configuration, and lighting
domain: authoring
version: 1.0.0
created: 2025-11-29
triggers:
  - Creating new Gazebo world files
  - Adding models from Gazebo Fuel
  - Configuring physics parameters
  - Debugging physics instability
learned_from:
  - Module 2 Chapter 10 Building Simulation Worlds (2025-11-29)
---

# Gazebo World Builder Skill

## Persona

Think like a simulation environment designer who creates realistic testing grounds for robots. You understand physics engines, lighting, and model placement. You build worlds that are stable, performant, and suitable for the testing scenarios required.

---

## Pre-Flight Questions

Before creating or modifying any SDF world, ask yourself:

### 1. Environment Purpose
- **Q**: What is this world testing?
  - **Impact**: Determines obstacles, terrain, lighting needs
  - Navigation → obstacles, open spaces
  - Manipulation → tables, objects to grasp
  - Outdoor → terrain, weather effects

### 2. Physics Requirements
- **Q**: What physics engine should be used?
  - **DART**: Default, good balance of speed/accuracy
  - **ODE**: Older, widely compatible
  - **Bullet**: Good for many contacts

- **Q**: What step size is appropriate?
  - **0.001s**: High accuracy, slower
  - **0.004s**: Default, good balance
  - **0.01s**: Fast but less accurate

### 3. Model Sources
- **Q**: Are models from Gazebo Fuel or custom?
  - **Fuel**: Use `https://fuel.gazebosim.org/...` URIs
  - **Custom**: Define inline or reference local files

---

## Principles

### Principle 1: Every World Needs Core Elements

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="my_world">
    <!-- Physics configuration -->
    <physics type="dart">
      <max_step_size>0.004</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <!-- Lighting -->
    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <!-- Ground plane -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
        </collision>
        <visual name="visual">
          <geometry><plane><normal>0 0 1</normal><size>100 100</size></plane></geometry>
        </visual>
      </link>
    </model>
  </world>
</sdf>
```

### Principle 2: Use Gazebo Fuel for Standard Models

```xml
<!-- Include model from Fuel -->
<include>
  <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Table</uri>
  <name>table_1</name>
  <pose>2 0 0 0 0 0</pose>
</include>

<!-- Multiple instances with different names -->
<include>
  <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Cardboard Box</uri>
  <name>box_1</name>
  <pose>2.5 0.3 0.8 0 0 0</pose>
</include>
```

Popular Fuel models:
- `OpenRobotics/models/Table`
- `OpenRobotics/models/Cardboard Box`
- `OpenRobotics/models/Coke Can`
- `OpenRobotics/models/Construction Cone`

### Principle 3: Configure Physics for Stability

```xml
<physics type="dart">
  <!-- Step size: smaller = more accurate but slower -->
  <max_step_size>0.004</max_step_size>

  <!-- Real-time factor: 1.0 = real-time, less than 1.0 = slower -->
  <real_time_factor>1.0</real_time_factor>

  <!-- Gravity vector (m/s²) -->
  <gravity>0 0 -9.81</gravity>
</physics>
```

For unstable simulations:
1. Reduce step size (0.004 → 0.001)
2. Increase solver iterations
3. Check collision geometry (too complex?)
4. Verify inertia values (too small?)

### Principle 4: Surface Properties for Realism

```xml
<surface>
  <friction>
    <ode>
      <mu>0.8</mu>      <!-- Static friction -->
      <mu2>0.6</mu2>    <!-- Dynamic friction -->
    </ode>
  </friction>
  <contact>
    <ode>
      <kp>1e6</kp>      <!-- Contact stiffness -->
      <kd>100</kd>      <!-- Contact damping -->
    </ode>
  </contact>
</surface>
```

Typical values:
- Rubber on concrete: mu=0.8-1.0
- Metal on metal: mu=0.3-0.5
- Ice: mu=0.05-0.1

---

## Common Patterns

### Indoor Room

```xml
<world name="indoor_room">
  <!-- Physics, lighting, ground (as above) -->

  <!-- Walls -->
  <model name="wall_north">
    <static>true</static>
    <pose>0 5 1 0 0 0</pose>
    <link name="link">
      <collision name="collision">
        <geometry><box><size>10 0.2 2</size></box></geometry>
      </collision>
      <visual name="visual">
        <geometry><box><size>10 0.2 2</size></box></geometry>
      </visual>
    </link>
  </model>

  <!-- Furniture from Fuel -->
  <include>
    <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Table</uri>
    <pose>2 2 0 0 0 0</pose>
  </include>
</world>
```

### Obstacle Course

```xml
<world name="obstacle_course">
  <!-- Base elements -->

  <!-- Scattered obstacles -->
  <include>
    <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Construction Cone</uri>
    <name>cone_1</name>
    <pose>3 1 0 0 0 0</pose>
  </include>
  <include>
    <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Construction Cone</uri>
    <name>cone_2</name>
    <pose>5 -2 0 0 0 0</pose>
  </include>

  <!-- Goal marker -->
  <model name="goal">
    <static>true</static>
    <pose>10 0 0.1 0 0 0</pose>
    <link name="link">
      <visual name="visual">
        <geometry><cylinder><radius>0.5</radius><length>0.2</length></cylinder></geometry>
        <material><ambient>0 1 0 1</ambient></material>
      </visual>
    </link>
  </model>
</world>
```

---

## Checklist

Before finalizing any SDF world:

- [ ] Physics engine and step size configured
- [ ] Lighting provides adequate visibility
- [ ] Ground plane present and stable
- [ ] All model URIs are valid (Fuel or local)
- [ ] Model names are unique
- [ ] Poses place models at correct locations
- [ ] Static models marked `<static>true</static>`
- [ ] World loads in Gazebo without errors
- [ ] Physics simulation is stable (no explosions)

---

## Integration

This skill is used by:
- `content-implementer` agent when generating Module 2 lessons
- Students learning world building in Chapter 10
- Capstone projects requiring custom environments

**Dependencies**:
- `urdf-robot-model` - for robots to place in worlds
- `sensor-simulation` - for testing sensors in environments
- `ros2-gazebo-bridge` - for controlling simulations
