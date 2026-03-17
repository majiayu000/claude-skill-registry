---
name: docker-ros2-development
description: >
  Best practices for Docker-based ROS2 development including multi-stage Dockerfiles, docker-compose
  for multi-container robotic systems, DDS discovery across containers, GPU passthrough for perception,
  and dev-vs-deploy container patterns. Use this skill when containerizing ROS2 workspaces, setting up
  docker-compose for robot software stacks, debugging DDS communication between containers, configuring
  NVIDIA Container Toolkit for GPU workloads, forwarding X11/Wayland for rviz2 and GUI tools, or
  managing USB device passthrough for cameras and serial devices. Trigger whenever the user mentions
  Docker with ROS2, docker-compose for robots, Dockerfile for colcon workspaces, container networking
  for DDS, GPU containers for perception, devcontainer for ROS2, multi-stage builds for ROS2, or
  deploying ROS2 in containers. Also trigger for CI/CD with Docker-based ROS2 builds, CycloneDDS
  or FastDDS configuration in containers, shared memory in Docker, or X11 forwarding for rviz2.
  Covers Humble, Iron, Jazzy, and Rolling distributions across Ubuntu 22.04 and 24.04 base images.
---

# Docker-Based ROS2 Development Skill

## When to Use This Skill

- Writing Dockerfiles for ROS2 workspaces with colcon builds
- Setting up docker-compose for multi-container robotic systems
- Debugging DDS discovery failures between containers (CycloneDDS, FastDDS)
- Configuring GPU passthrough with NVIDIA Container Toolkit for perception nodes
- Forwarding X11 or Wayland displays for rviz2 and rqt tools
- Managing USB device passthrough for cameras, LiDARs, and serial devices
- Building CI/CD pipelines with Docker-based ROS2 builds and test runners
- Creating devcontainer configurations for VS Code with ROS2 extensions
- Optimizing Docker layer caching for colcon workspace builds
- Designing dev-vs-deploy container strategies with multi-stage builds

## ROS2 Docker Image Hierarchy

Official OSRF images follow a layered hierarchy. Always choose the smallest base that satisfies dependencies.

```
┌──────────────────────────────────────────────────────────────────┐
│  ros:<distro>-desktop-full  (~3.5 GB)                            │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  ros:<distro>-desktop     (~2.8 GB)                        │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │  ros:<distro>-perception (~2.2 GB)                    │  │  │
│  │  │  ┌────────────────────────────────────────────────┐   │  │  │
│  │  │  │  ros:<distro>-ros-base  (~1.1 GB)              │   │  │  │
│  │  │  │  ┌──────────────────────────────────────────┐  │   │  │  │
│  │  │  │  │  ros:<distro>-ros-core (~700 MB)         │  │   │  │  │
│  │  │  │  └──────────────────────────────────────────┘  │   │  │  │
│  │  │  └────────────────────────────────────────────────┘   │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

| Image Tag               | Base OS        | Size    | Contents                                    | Use Case                            |
|--------------------------|----------------|---------|---------------------------------------------|-------------------------------------|
| `ros:humble-ros-core`    | Ubuntu 22.04   | ~700 MB | rclcpp, rclpy, rosout, launch               | Minimal runtime for single nodes    |
| `ros:humble-ros-base`    | Ubuntu 22.04   | ~1.1 GB | ros-core + common_interfaces, rosbag2       | Most production deployments         |
| `ros:humble-perception`  | Ubuntu 22.04   | ~2.2 GB | ros-base + image_transport, cv_bridge, PCL  | Camera/lidar perception pipelines   |
| `ros:humble-desktop`     | Ubuntu 22.04   | ~2.8 GB | perception + rviz2, rqt, demos              | Development with GUI tools          |
| `ros:jazzy-ros-core`     | Ubuntu 24.04   | ~750 MB | rclcpp, rclpy, rosout, launch               | Minimal runtime (Jazzy/Noble)       |
| `ros:jazzy-ros-base`     | Ubuntu 24.04   | ~1.2 GB | ros-core + common_interfaces, rosbag2       | Production deployments (Jazzy)      |

## Multi-Stage Dockerfiles for ROS2

### Dev Stage

The development stage includes build tools, debuggers, and editor support for interactive use.

```dockerfile
FROM ros:humble-desktop AS dev
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake gdb python3-pip \
    python3-colcon-common-extensions python3-rosdep \
    ros-humble-ament-lint-auto ros-humble-ament-cmake-pytest \
    ccache \
    && rm -rf /var/lib/apt/lists/*
ENV CCACHE_DIR=/ccache
ENV CC="ccache gcc"
ENV CXX="ccache g++"
```

### Build Stage

Copies only `src/` and `package.xml` files to maximize cache hits during dependency resolution.

```dockerfile
FROM ros:humble-ros-base AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions python3-rosdep \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /ros2_ws
# Copy package manifests first for dependency caching
COPY src/my_pkg/package.xml src/my_pkg/package.xml
RUN . /opt/ros/humble/setup.sh && apt-get update && \
    rosdep install --from-paths src --ignore-src -r -y && \
    rm -rf /var/lib/apt/lists/*
# Source changes invalidate only this layer and below
COPY src/ src/
RUN . /opt/ros/humble/setup.sh && \
    colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release \
      --event-handlers console_direct+
```

### Runtime Stage

Contains only the built install space and runtime dependencies. No compilers, no source code.

```dockerfile
FROM ros:humble-ros-core AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-yaml ros-humble-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /ros2_ws/install /ros2_ws/install
RUN groupadd -r rosuser && useradd -r -g rosuser -m rosuser
USER rosuser
COPY ros_entrypoint.sh /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["ros2", "launch", "my_pkg", "bringup.launch.py"]
```

### Full Multi-Stage Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
# Usage:
#   docker build --target dev -t my_robot:dev .
#   docker build --target runtime -t my_robot:latest .
ARG ROS_DISTRO=humble
ARG BASE_IMAGE=ros:${ROS_DISTRO}-ros-base

# Stage 1: Dependency base — install apt and rosdep deps
FROM ${BASE_IMAGE} AS deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions python3-rosdep \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /ros2_ws
# Copy only package.xml files for rosdep resolution (maximizes cache reuse)
COPY src/my_robot_bringup/package.xml src/my_robot_bringup/package.xml
COPY src/my_robot_perception/package.xml src/my_robot_perception/package.xml
COPY src/my_robot_msgs/package.xml src/my_robot_msgs/package.xml
COPY src/my_robot_navigation/package.xml src/my_robot_navigation/package.xml
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
    apt-get update && \
    rosdep install --from-paths src --ignore-src -r -y && \
    rm -rf /var/lib/apt/lists/*

# Stage 2: Development — full dev environment
FROM deps AS dev
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gdb valgrind ccache python3-pip python3-pytest \
    ros-${ROS_DISTRO}-ament-lint-auto \
    ros-${ROS_DISTRO}-launch-testing-ament-cmake \
    ros-${ROS_DISTRO}-rviz2 ros-${ROS_DISTRO}-rqt-graph \
    && rm -rf /var/lib/apt/lists/*
ENV CCACHE_DIR=/ccache CC="ccache gcc" CXX="ccache g++"
COPY src/ src/
COPY ros_entrypoint.sh /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]

# Stage 3: Build — compile workspace
FROM deps AS build
COPY src/ src/
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
    colcon build \
      --cmake-args -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF \
      --event-handlers console_direct+ \
      --parallel-workers $(nproc)

# Stage 4: Runtime — minimal production image
FROM ros:${ROS_DISTRO}-ros-core AS runtime
ARG ROS_DISTRO=humble
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-yaml ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /ros2_ws/install /ros2_ws/install
RUN groupadd -r rosuser && useradd -r -g rosuser -m -s /bin/bash rosuser
USER rosuser
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
COPY ros_entrypoint.sh /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["ros2", "launch", "my_robot_bringup", "robot.launch.py"]
```

The entrypoint script both dev and runtime stages use:

```bash
#!/bin/bash
set -e
source /opt/ros/${ROS_DISTRO}/setup.bash
if [ -f /ros2_ws/install/setup.bash ]; then
    source /ros2_ws/install/setup.bash
fi
exec "$@"
```

## Docker Compose for Multi-Container ROS2 Systems

### Basic Multi-Container Setup

Each ROS2 subsystem runs in its own container with process isolation, independent scaling, and per-service resource limits.

```yaml
# docker-compose.yml
version: "3.8"

x-ros-common: &ros-common
  environment:
    - ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-0}
    - RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
    - CYCLONEDDS_URI=file:///cyclonedds.xml
  volumes:
    - ./config/cyclonedds.xml:/cyclonedds.xml:ro
    - /dev/shm:/dev/shm
  network_mode: host
  restart: unless-stopped

services:
  rosbridge:
    <<: *ros-common
    image: my_robot:latest
    command: ros2 launch rosbridge_server rosbridge_websocket_launch.xml port:=9090

  perception:
    <<: *ros-common
    image: my_robot_perception:latest
    command: ros2 launch my_robot_perception perception.launch.py
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    devices:
      - /dev/video0:/dev/video0            # USB camera passthrough

  navigation:
    <<: *ros-common
    image: my_robot_navigation:latest
    command: >
      ros2 launch my_robot_navigation navigation.launch.py
        use_sim_time:=false map:=/maps/warehouse.yaml
    volumes:
      - ./maps:/maps:ro

  driver:
    <<: *ros-common
    image: my_robot_driver:latest
    command: ros2 launch my_robot_driver driver.launch.py
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0          # Serial motor controller
      - /dev/ttyACM0:/dev/ttyACM0          # IMU over USB-serial
    group_add:
      - dialout
```

### Service Dependencies with Health Checks

```yaml
services:
  driver:
    <<: *ros-common
    image: my_robot_driver:latest
    healthcheck:
      test: ["CMD", "bash", "-c",
             "source /opt/ros/humble/setup.bash && ros2 topic list | grep -q /joint_states"]
      interval: 5s
      timeout: 10s
      retries: 5
      start_period: 15s

  navigation:
    <<: *ros-common
    image: my_robot_navigation:latest
    depends_on:
      driver:
        condition: service_healthy         # Wait for driver topics

  perception:
    <<: *ros-common
    image: my_robot_perception:latest
    depends_on:
      driver:
        condition: service_healthy         # Camera driver must be ready
```

### Profiles for Dev vs Deploy

```yaml
services:
  driver:
    <<: *ros-common
    image: my_robot_driver:latest
    command: ros2 launch my_robot_driver driver.launch.py

  rviz:
    <<: *ros-common
    profiles: ["dev"]
    image: my_robot:dev
    command: ros2 run rviz2 rviz2 -d /rviz/config.rviz
    environment:
      - DISPLAY=${DISPLAY}
      - QT_X11_NO_MITSHM=1
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix:rw

  rosbag_record:
    <<: *ros-common
    profiles: ["dev"]
    image: my_robot:dev
    command: ros2 bag record -a --storage sqlite3 --max-bag-duration 300 -o /bags/session
    volumes:
      - ./bags:/bags

  watchdog:
    <<: *ros-common
    profiles: ["deploy"]
    image: my_robot:latest
    command: ros2 launch my_robot_bringup watchdog.launch.py
    restart: always
```

```bash
docker compose --profile dev up          # Dev tools (rviz, rosbag)
docker compose --profile deploy up -d    # Production (watchdog, no GUI)
```

## DDS Discovery Across Containers

### CycloneDDS XML Config for Unicast Across Containers

When containers use bridge networking (no multicast), configure explicit unicast peer lists.

```xml
<!-- cyclonedds.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<CycloneDDS xmlns="https://cdds.io/config">
  <Domain>
    <General>
      <Interfaces>
        <NetworkInterface autodetermine="true" priority="default"/>
      </Interfaces>
      <AllowMulticast>false</AllowMulticast>
    </General>
    <Discovery>
      <!-- Peer list uses docker-compose service names as hostnames -->
      <Peers>
        <Peer address="perception"/>
        <Peer address="navigation"/>
        <Peer address="driver"/>
        <Peer address="rosbridge"/>
      </Peers>
      <ParticipantIndex>auto</ParticipantIndex>
      <MaxAutoParticipantIndex>120</MaxAutoParticipantIndex>
    </Discovery>
    <Internal>
      <SocketReceiveBufferSize min="10MB"/>
    </Internal>
  </Domain>
</CycloneDDS>
```

### FastDDS XML Config

```xml
<!-- fastdds.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<dds xmlns="http://www.eprosima.com/XMLSchemas/fastRTPS_Profiles">
  <profiles>
    <participant profile_name="docker_participant" is_default_profile="true">
      <rtps>
        <builtin>
          <discovery_config>
            <discoveryProtocol>SIMPLE</discoveryProtocol>
            <leaseDuration><sec>10</sec></leaseDuration>
          </discovery_config>
          <initialPeersList>
            <locator>
              <udpv4><address>perception</address><port>7412</port></udpv4>
            </locator>
            <locator>
              <udpv4><address>navigation</address><port>7412</port></udpv4>
            </locator>
            <locator>
              <udpv4><address>driver</address><port>7412</port></udpv4>
            </locator>
          </initialPeersList>
        </builtin>
      </rtps>
    </participant>
  </profiles>
</dds>
```

Mount and activate in compose:

```yaml
# CycloneDDS
environment:
  - RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
  - CYCLONEDDS_URI=file:///cyclonedds.xml
volumes:
  - ./config/cyclonedds.xml:/cyclonedds.xml:ro

# FastDDS
environment:
  - RMW_IMPLEMENTATION=rmw_fastrtps_cpp
  - FASTRTPS_DEFAULT_PROFILES_FILE=/fastdds.xml
volumes:
  - ./config/fastdds.xml:/fastdds.xml:ro
```

### Shared Memory Transport in Docker

DDS shared memory (zero-copy) requires `/dev/shm` sharing between containers. This provides highest throughput for large messages (images, point clouds).

```yaml
services:
  perception:
    shm_size: "512m"                    # Default 64 MB is too small for image topics
    volumes:
      - /dev/shm:/dev/shm              # Share host shm for inter-container zero-copy
```

```xml
<!-- Enable shared memory in CycloneDDS -->
<CycloneDDS xmlns="https://cdds.io/config">
  <Domain>
    <SharedMemory>
      <Enable>true</Enable>
    </SharedMemory>
  </Domain>
</CycloneDDS>
```

Constraints: all communicating containers must share `/dev/shm` or use `ipc: host`. Use `--ipc=shareable` on one container and `--ipc=container:<name>` on others for scoped sharing.

## Networking Modes and ROS2 Implications

### Host Networking

```yaml
services:
  my_node:
    network_mode: host      # Shares host network namespace; DDS multicast works natively
```

### Bridge Networking (Default)

```yaml
services:
  my_node:
    networks: [ros_net]
networks:
  ros_net:
    driver: bridge          # DDS multicast blocked; requires unicast peer config
```

### Macvlan Networking

```yaml
networks:
  ros_macvlan:
    driver: macvlan
    driver_opts:
      parent: eth0
    ipam:
      config:
        - subnet: 192.168.1.0/24
          gateway: 192.168.1.1
services:
  my_node:
    networks:
      ros_macvlan:
        ipv4_address: 192.168.1.50   # Real LAN IP; DDS multicast works natively
```

### Decision Table

| Factor              | Host             | Bridge                  | Macvlan               |
|---------------------|------------------|-------------------------|-----------------------|
| DDS discovery       | Works natively   | Needs unicast peers     | Works natively        |
| Network isolation   | None             | Full isolation          | LAN-level isolation   |
| Port conflicts      | Yes (host ports) | No (mapped ports)       | No (unique IPs)       |
| Performance         | Native           | Slight overhead         | Near-native           |
| Multi-host support  | No               | With overlay networks   | Yes (same LAN)        |
| When to use         | Dev, single host | CI/CD, multi-tenant     | Multi-robot on LAN    |

## GPU Passthrough for Perception

### NVIDIA Container Toolkit Setup

```bash
# Install NVIDIA Container Toolkit on the host
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### Compose Config with deploy.resources

```yaml
services:
  perception:
    image: my_robot_perception:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1                    # Number of GPUs (or "all")
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility,video
    shm_size: "1g"                        # Large shm for GPU<->CPU transfers
```

For Dockerfiles that need CUDA, start from NVIDIA base and install ROS2 on top:

```dockerfile
FROM nvidia/cuda:12.2.0-cudnn8-runtime-ubuntu22.04 AS perception-base
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg2 lsb-release \
    && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
       -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) \
       signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
       http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
       > /etc/apt/sources.list.d/ros2.list \
    && apt-get update && apt-get install -y --no-install-recommends \
       ros-humble-ros-base ros-humble-cv-bridge ros-humble-image-transport \
    && rm -rf /var/lib/apt/lists/*
```

### Verification

```bash
docker compose exec perception bash -c '
  nvidia-smi
  python3 -c "import torch; print(f\"CUDA available: {torch.cuda.is_available()}\")"
'
```

## Display Forwarding

### X11 Forwarding

```yaml
services:
  rviz:
    image: my_robot:dev
    command: ros2 run rviz2 rviz2
    environment:
      - DISPLAY=${DISPLAY:-:0}                   # Forward host display
      - QT_X11_NO_MITSHM=1                       # Disable MIT-SHM (crashes in Docker)
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix:rw          # X11 socket
      - ${HOME}/.Xauthority:/root/.Xauthority:ro  # Auth cookie
    network_mode: host
```

```bash
# Allow local Docker containers to access the X server
xhost +local:docker
# More secure variant:
xhost +SI:localuser:$(whoami)
```

### Wayland Forwarding

```yaml
services:
  rviz:
    image: my_robot:dev
    command: ros2 run rviz2 rviz2
    environment:
      - WAYLAND_DISPLAY=${WAYLAND_DISPLAY:-wayland-0}
      - XDG_RUNTIME_DIR=/run/user/1000
      - QT_QPA_PLATFORM=wayland
    volumes:
      - ${XDG_RUNTIME_DIR}/${WAYLAND_DISPLAY}:/run/user/1000/${WAYLAND_DISPLAY}:rw
```

### Headless Rendering

For CI/CD or remote machines without a physical display:

```bash
# Run rviz2 headless with Xvfb for screenshot capture or testing
docker run --rm my_robot:dev bash -c '
  apt-get update && apt-get install -y xvfb mesa-utils &&
  Xvfb :99 -screen 0 1920x1080x24 &
  export DISPLAY=:99
  source /opt/ros/humble/setup.bash
  ros2 run rviz2 rviz2 -d /config/test.rviz --screenshot /output/frame.png
'
```

## Volume Mounts and Workspace Overlays

### Source Mounts for Dev

Mount only `src/` during development. Let colcon write `build/`, `install/`, and `log/` inside named volumes to avoid bind mount performance issues.

```yaml
# BAD: mounting entire workspace — build artifacts on bind mount are slow
# volumes:
#   - ./my_ros2_ws:/ros2_ws

# GOOD: mount only source, use named volumes for build artifacts
services:
  dev:
    image: my_robot:dev
    volumes:
      - ./src:/ros2_ws/src:rw                     # Source code (bind mount)
      - build_vol:/ros2_ws/build                   # Build artifacts (named volume)
      - install_vol:/ros2_ws/install               # Install space (named volume)
      - log_vol:/ros2_ws/log                       # Log output (named volume)
    working_dir: /ros2_ws

volumes:
  build_vol:
  install_vol:
  log_vol:
```

### ccache Caching

Persist ccache across container rebuilds for faster C++ compilation:

```yaml
services:
  dev:
    volumes:
      - ccache_vol:/ccache
    environment:
      - CCACHE_DIR=/ccache
      - CCACHE_MAXSIZE=2G
      - CC=ccache gcc
      - CXX=ccache g++
volumes:
  ccache_vol:
```

### ROS Workspace Overlay in Docker

Keep upstream packages cached and only rebuild custom packages:

```dockerfile
# Stage 1: upstream dependencies (rarely changes)
FROM ros:humble-ros-base AS upstream
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-nav2-bringup ros-humble-slam-toolbox \
    ros-humble-robot-localization \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: custom packages overlay on top
FROM upstream AS workspace
WORKDIR /ros2_ws
COPY src/ src/
RUN . /opt/ros/humble/setup.sh && colcon build --symlink-install
# install/setup.bash automatically sources /opt/ros/humble as underlay
```

## USB Device Passthrough

### Cameras and Serial Devices

```yaml
services:
  camera_driver:
    image: my_robot_driver:latest
    devices:
      - /dev/video0:/dev/video0        # USB camera (V4L2)
      - /dev/video1:/dev/video1
    group_add:
      - video                          # Access /dev/videoN without root

  motor_driver:
    image: my_robot_driver:latest
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0      # USB-serial motor controller
      - /dev/ttyACM0:/dev/ttyACM0      # Arduino/Teensy
    group_add:
      - dialout                        # Access serial ports without root
```

### Udev Rules Inside Containers

Create stable device symlinks on the host so container paths remain consistent regardless of USB enumeration order.

```bash
# /etc/udev/rules.d/99-robot-devices.rules (host-side)
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="robot/motor_controller"
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="robot/lidar"
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="0825", SYMLINK+="robot/camera"
```

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

```yaml
services:
  driver:
    devices:
      - /dev/robot/motor_controller:/dev/ttyMOTOR   # Stable symlink
      - /dev/robot/lidar:/dev/ttyLIDAR
      - /dev/robot/camera:/dev/video0
```

### Dynamic Device Attachment

For devices plugged in after the container starts:

```yaml
services:
  driver:
    # Option 1: privileged (use only when necessary)
    privileged: true
    volumes:
      - /dev:/dev

    # Option 2: cgroup device rules (more secure)
    # device_cgroup_rules:
    #   - 'c 188:* rmw'                  # USB-serial (major 188)
    #   - 'c 81:* rmw'                   # Video devices (major 81)
```

## Dev Container Configuration

```json
// .devcontainer/devcontainer.json
{
  "name": "ROS2 Humble Dev",
  "build": {
    "dockerfile": "../Dockerfile",
    "target": "dev",
    "args": { "ROS_DISTRO": "humble" }
  },
  "runArgs": [
    "--network=host", "--ipc=host", "--pid=host",
    "--privileged", "--gpus", "all",
    "-e", "DISPLAY=${localEnv:DISPLAY}",
    "-e", "QT_X11_NO_MITSHM=1",
    "-v", "/tmp/.X11-unix:/tmp/.X11-unix:rw",
    "-v", "/dev:/dev"
  ],
  "workspaceMount": "source=${localWorkspaceFolder},target=/ros2_ws/src,type=bind",
  "workspaceFolder": "/ros2_ws",
  "mounts": [
    "source=ros2-build-vol,target=/ros2_ws/build,type=volume",
    "source=ros2-install-vol,target=/ros2_ws/install,type=volume",
    "source=ros2-log-vol,target=/ros2_ws/log,type=volume",
    "source=ros2-ccache-vol,target=/ccache,type=volume"
  ],
  "containerEnv": {
    "ROS_DISTRO": "humble",
    "RMW_IMPLEMENTATION": "rmw_cyclonedds_cpp",
    "CCACHE_DIR": "/ccache",
    "RCUTILS_COLORIZED_OUTPUT": "1"
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-iot.vscode-ros",
        "ms-vscode.cpptools",
        "ms-python.python",
        "ms-vscode.cmake-tools",
        "smilerobotics.urdf",
        "redhat.vscode-xml",
        "redhat.vscode-yaml"
      ],
      "settings": {
        "ros.distro": "humble",
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "C_Cpp.default.compileCommands": "/ros2_ws/build/compile_commands.json",
        "cmake.configureOnOpen": false
      }
    }
  },
  "postCreateCommand": "sudo apt-get update && rosdep update && rosdep install --from-paths src --ignore-src -r -y",
  "remoteUser": "rosuser"
}
```

## CI/CD with Docker

### GitHub Actions Workflow

```yaml
# .github/workflows/ros2-docker-ci.yml
name: ROS2 Docker CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-test:
    runs-on: ubuntu-22.04
    strategy:
      fail-fast: false
      matrix:
        ros_distro: [humble, jazzy]
        include:
          - ros_distro: humble
            ubuntu: "22.04"
          - ros_distro: jazzy
            ubuntu: "24.04"
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ matrix.ros_distro }}-${{ hashFiles('src/**/package.xml') }}
          restore-keys: ${{ runner.os }}-buildx-${{ matrix.ros_distro }}-

      - name: Build and test
        run: |
          docker build --target dev \
            --build-arg ROS_DISTRO=${{ matrix.ros_distro }} \
            -t test-image:${{ matrix.ros_distro }} .
          docker run --rm test-image:${{ matrix.ros_distro }} bash -c '
            source /opt/ros/${{ matrix.ros_distro }}/setup.bash &&
            cd /ros2_ws &&
            colcon build --cmake-args -DBUILD_TESTING=ON &&
            colcon test --event-handlers console_direct+ &&
            colcon test-result --verbose'

      - name: Push runtime image
        if: github.ref == 'refs/heads/main'
        uses: docker/build-push-action@v5
        with:
          context: .
          target: runtime
          build-args: ROS_DISTRO=${{ matrix.ros_distro }}
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ matrix.ros_distro }}-latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ matrix.ros_distro }}-${{ github.sha }}
          push: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache-new,mode=max

      - name: Rotate cache
        run: rm -rf /tmp/.buildx-cache && mv /tmp/.buildx-cache-new /tmp/.buildx-cache
```

### Layer Caching

Order Dockerfile instructions from least-frequently-changed to most-frequently-changed:

```
1. Base image         (ros:humble-ros-base)     — changes on distro upgrade
2. System apt packages                           — changes on new dependency
3. rosdep install     (from package.xml)         — changes on new ROS dep
4. COPY src/ src/                                — changes on every code edit
5. colcon build                                  — rebuilds on source change
```

### Build Matrix Across Distros

```yaml
strategy:
  matrix:
    ros_distro: [humble, iron, jazzy, rolling]
    rmw: [rmw_cyclonedds_cpp, rmw_fastrtps_cpp]
    exclude:
      - ros_distro: iron           # Iron EOL — skip
        rmw: rmw_fastrtps_cpp
```

## Docker ROS2 Anti-Patterns

### 1. Running Everything in One Container

**Problem:** Putting perception, navigation, planning, and drivers in a single container defeats the purpose of containerization. A crash in one subsystem takes down everything.

**Fix:** Split into one service per subsystem. Use docker-compose to orchestrate.

```yaml
# BAD: monolithic container
services:
  robot:
    image: my_robot:latest
    command: ros2 launch my_robot everything.launch.py

# GOOD: one container per subsystem
services:
  perception:
    image: my_robot_perception:latest
    command: ros2 launch my_robot_perception perception.launch.py
  navigation:
    image: my_robot_navigation:latest
    command: ros2 launch my_robot_navigation navigation.launch.py
  driver:
    image: my_robot_driver:latest
    command: ros2 launch my_robot_driver driver.launch.py
```

### 2. Using Bridge Networking Without DDS Config

**Problem:** DDS uses multicast for discovery by default. Docker bridge networks do not forward multicast. Nodes in different containers will not discover each other.

**Fix:** Use `network_mode: host` or configure DDS unicast peers explicitly.

```yaml
# BAD: bridge network with no DDS config
services:
  node_a:
    networks: [ros_net]
  node_b:
    networks: [ros_net]

# GOOD: host networking (simplest)
services:
  node_a:
    network_mode: host
  node_b:
    network_mode: host

# GOOD: bridge with CycloneDDS unicast peers
services:
  node_a:
    networks: [ros_net]
    environment:
      - RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
      - CYCLONEDDS_URI=file:///cyclonedds.xml
    volumes:
      - ./cyclonedds.xml:/cyclonedds.xml:ro
```

### 3. Building Packages in the Runtime Image

**Problem:** Installing compilers and build tools in the runtime image bloats it by 1-2 GB and increases attack surface.

**Fix:** Use multi-stage builds. Compile in a build stage, copy only the install space to runtime.

```dockerfile
# BAD: build tools in runtime image (2.5 GB)
FROM ros:humble-ros-base
RUN apt-get update && apt-get install -y build-essential python3-colcon-common-extensions
COPY src/ /ros2_ws/src/
RUN cd /ros2_ws && colcon build
CMD ["ros2", "launch", "my_pkg", "bringup.launch.py"]

# GOOD: multi-stage build (800 MB)
FROM ros:humble-ros-base AS build
RUN apt-get update && apt-get install -y python3-colcon-common-extensions
COPY src/ /ros2_ws/src/
RUN cd /ros2_ws && . /opt/ros/humble/setup.sh && colcon build

FROM ros:humble-ros-core AS runtime
COPY --from=build /ros2_ws/install /ros2_ws/install
CMD ["ros2", "launch", "my_pkg", "bringup.launch.py"]
```

### 4. Mounting the Entire Workspace as a Volume

**Problem:** Mounting the full workspace means colcon writes `build/`, `install/`, and `log/` to a bind mount. On macOS/Windows Docker Desktop, bind mount I/O is 10-50x slower. Builds that take 2 minutes take 20+ minutes.

**Fix:** Mount only `src/` as a bind mount. Use named volumes for build artifacts.

```yaml
# BAD:
volumes:
  - ./my_ros2_ws:/ros2_ws

# GOOD:
volumes:
  - ./my_ros2_ws/src:/ros2_ws/src
  - build_vol:/ros2_ws/build
  - install_vol:/ros2_ws/install
  - log_vol:/ros2_ws/log
```

### 5. Running Containers as Root

**Problem:** Running as root inside containers is a security risk. If compromised, the attacker has root access to mounted volumes and devices.

**Fix:** Create a non-root user with appropriate group membership.

```dockerfile
# BAD:
FROM ros:humble-ros-base
COPY --from=build /ros2_ws/install /ros2_ws/install
CMD ["ros2", "launch", "my_pkg", "bringup.launch.py"]

# GOOD:
FROM ros:humble-ros-base
RUN groupadd -r rosuser && \
    useradd -r -g rosuser -G video,dialout -m -s /bin/bash rosuser
COPY --from=build --chown=rosuser:rosuser /ros2_ws/install /ros2_ws/install
USER rosuser
CMD ["ros2", "launch", "my_pkg", "bringup.launch.py"]
```

### 6. Ignoring Layer Cache Order in Dockerfile

**Problem:** Placing `COPY src/ .` before `rosdep install` means every source change invalidates the dependency cache. All apt packages are re-downloaded on every build.

**Fix:** Copy only `package.xml` files first, install dependencies, then copy source.

```dockerfile
# BAD: source copy before rosdep
COPY src/ /ros2_ws/src/
RUN rosdep install --from-paths src --ignore-src -r -y
RUN colcon build

# GOOD: package.xml first, then rosdep, then source
COPY src/my_pkg/package.xml /ros2_ws/src/my_pkg/package.xml
RUN . /opt/ros/humble/setup.sh && rosdep install --from-paths src --ignore-src -r -y
COPY src/ /ros2_ws/src/
RUN . /opt/ros/humble/setup.sh && colcon build
```

### 7. Hardcoding ROS_DOMAIN_ID

**Problem:** Hardcoding `ROS_DOMAIN_ID=42` causes conflicts when multiple robots or developers share a network. Two robots with the same domain ID will cross-talk.

**Fix:** Use environment variables with defaults. Set domain ID at deploy time.

```yaml
# BAD:
environment:
  - ROS_DOMAIN_ID=42

# GOOD:
environment:
  - ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-0}
```

```bash
ROS_DOMAIN_ID=1 docker compose up -d    # Robot 1
ROS_DOMAIN_ID=2 docker compose up -d    # Robot 2
```

### 8. Forgetting to Source setup.bash in Entrypoint

**Problem:** The `CMD` runs `ros2 launch ...` but the shell has not sourced the ROS2 setup files. Fails with `ros2: command not found`.

**Fix:** Use an entrypoint script that sources the underlay and overlay before executing the command.

```dockerfile
# BAD: no sourcing
FROM ros:humble-ros-core
COPY --from=build /ros2_ws/install /ros2_ws/install
CMD ["ros2", "launch", "my_pkg", "bringup.launch.py"]

# GOOD: entrypoint script handles sourcing
FROM ros:humble-ros-core
COPY --from=build /ros2_ws/install /ros2_ws/install
COPY ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["ros2", "launch", "my_pkg", "bringup.launch.py"]
```

```bash
#!/bin/bash
# ros_entrypoint.sh
set -e
source /opt/ros/${ROS_DISTRO}/setup.bash
if [ -f /ros2_ws/install/setup.bash ]; then
    source /ros2_ws/install/setup.bash
fi
exec "$@"
```

## Docker ROS2 Deployment Checklist

1. **Multi-stage build** -- Separate dev, build, and runtime stages so production images contain no compilers or build tools
2. **Non-root user** -- Create a dedicated `rosuser` with only the group memberships needed (video, dialout) instead of privileged mode
3. **DDS configuration** -- Ship a `cyclonedds.xml` or `fastdds.xml` with explicit peer lists if not using host networking
4. **Health checks** -- Every service has a health check that verifies the node is running and publishing on expected topics
5. **Resource limits** -- Set `mem_limit`, `cpus`, and GPU reservations for each service to prevent resource starvation
6. **Restart policy** -- Use `restart: unless-stopped` for all services and `restart: always` for critical drivers and watchdogs
7. **Log management** -- Configure Docker logging driver (json-file with max-size/max-file) to prevent disk exhaustion from ROS2 log output
8. **Environment injection** -- Use `.env` files or orchestrator secrets for `ROS_DOMAIN_ID`, DDS config paths, and device mappings rather than hardcoding
9. **Shared memory** -- Set `shm_size` to at least 256 MB (512 MB for image topics) and configure DDS shared memory transport for high-bandwidth topics
10. **Device stability** -- Use udev rules on the host to create stable `/dev/robot/*` symlinks and reference those in compose device mappings
11. **Image versioning** -- Tag images with both `latest` and a commit SHA or semantic version; never deploy unversioned `latest` to production
12. **Backup and rollback** -- Keep the previous image version available so a failed deployment can be rolled back by reverting the image tag
