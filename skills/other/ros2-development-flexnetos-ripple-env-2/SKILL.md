---
name: ros2-development
description: ROS2 Humble development skills for building, testing, and running robotics packages
icon: 🤖
category: robotics
tools:
  - colcon
  - ros2
  - rosdep
  - rviz2
  - gazebo
---

# ROS2 Development Skills

## Overview

This skill provides expertise in ROS2 Humble development using the RoboStack/Pixi environment.

## Prerequisites

- Active development shell (`nom develop` or `direnv allow`)
- Pixi packages installed (`pixi install`)

## Build Commands

### Quick Build
```bash
cb                                    # colcon build --symlink-install
cbs                                   # colcon build (standard)
colcon build --symlink-install        # Full command
```

### Selective Build
```bash
colcon build --packages-select <pkg>  # Build specific package
colcon build --packages-up-to <pkg>   # Build package and dependencies
```

## Test Commands

### Run Tests
```bash
ct                                    # colcon test
colcon test                           # Full command
colcon test --packages-select <pkg>   # Test specific package
```

### View Results
```bash
ctr                                   # colcon test-result --verbose
colcon test-result --verbose          # Full command
```

## ROS2 CLI

### Nodes and Topics
```bash
ros2 node list                        # List running nodes
ros2 topic list                       # List available topics
ros2 topic echo /topic_name           # Subscribe to topic
ros2 topic info /topic_name           # Topic information
ros2 topic hz /topic_name             # Message frequency
```

### Services and Actions
```bash
ros2 service list                     # List services
ros2 service call /srv type '{data}' # Call service
ros2 action list                      # List actions
ros2 action send_goal /action type   # Send action goal
```

### Parameters
```bash
ros2 param list                       # List parameters
ros2 param get /node param_name       # Get parameter
ros2 param set /node param_name val   # Set parameter
```

### Launch
```bash
ros2 launch <package> <launch.py>     # Launch file
ros2 run <package> <executable>       # Run single node
```

## Package Management

### Add ROS2 Packages
```bash
pixi add ros-humble-<package-name>    # Add from RoboStack
pixi search ros-humble-*              # Search available packages
```

### Common Packages
- `ros-humble-desktop` - Full desktop installation
- `ros-humble-rviz2` - Visualization tool
- `ros-humble-gazebo-ros-pkgs` - Gazebo simulation
- `ros-humble-nav2-bringup` - Navigation stack
- `ros-humble-moveit` - Motion planning

## Environment

### Check Environment
```bash
ros2-env                              # Show ROS2 environment variables
printenv | grep ROS                   # All ROS-related variables
```

### Workspace Setup
```bash
source install/setup.bash             # Source workspace (after build)
```

## Best Practices

1. **Always use symlink install** for development (`--symlink-install`)
2. **Clean build** when changing CMakeLists: `rm -rf build install log`
3. **Check dependencies** before building: `rosdep check --from-paths src`
4. **Use colcon mixins** for common build configurations

## Troubleshooting

### Build Failures
- Check `log/latest_build/<pkg>/` for detailed errors
- Ensure all dependencies are installed via pixi
- Verify Python path with `which python`

### Runtime Issues
- Source workspace: `source install/setup.bash`
- Check node status: `ros2 node list`
- Verify topic publishing: `ros2 topic echo /topic`

## Related Skills

- [DevOps](../devops/SKILL.md) - CI/CD for ROS2 packages
- [Nix Environment](../nix-environment/SKILL.md) - Environment management
