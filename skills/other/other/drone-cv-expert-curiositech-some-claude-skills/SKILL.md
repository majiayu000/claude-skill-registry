---
name: drone-cv-expert
description: Expert in drone systems, computer vision, and autonomous navigation. Specializes in flight control, SLAM, object detection, sensor fusion, and path planning. Activate on "drone", "UAV", "SLAM", "visual odometry", "PID control", "MAVLink", "Pixhawk", "path planning", "A*", "RRT", "EKF", "sensor fusion", "optical flow", "ByteTrack". NOT for domain-specific inspection tasks like fire detection, roof damage assessment, or thermal analysis (use drone-inspection-specialist), GPU shader optimization (use metal-shader-expert), or general image classification without drone context (use clip-aware-embeddings).
allowed-tools: Read,Write,Edit,Bash(python:*,pip:*),Grep,Glob,mcp__firecrawl__firecrawl_search,WebFetch
category: AI & Machine Learning
tags:
  - drone
  - slam
  - navigation
  - sensor-fusion
  - path-planning
pairs-with:
  - skill: drone-inspection-specialist
    reason: Domain-specific inspection tasks
  - skill: physics-rendering-expert
    reason: Physics simulation for drone systems
---

# Drone CV Expert

Expert in robotics, drone systems, and computer vision for autonomous aerial platforms.

## Decision Tree: When to Use This Skill

```
User mentions drones or UAVs?
├─ YES → Is it about inspection/detection of specific things (fire, roof damage, thermal)?
│        ├─ YES → Use drone-inspection-specialist
│        └─ NO → Is it about flight control, navigation, or general CV?
│                ├─ YES → Use THIS SKILL (drone-cv-expert)
│                └─ NO → Is it about GPU rendering/shaders?
│                        ├─ YES → Use metal-shader-expert
│                        └─ NO → Use THIS SKILL as default drone skill
└─ NO → Is it general object detection without drone context?
        ├─ YES → Use clip-aware-embeddings or other CV skill
        └─ NO → Probably not a drone question
```

## Core Competencies

### Flight Control & Navigation
- **PID Tuning**: Position, velocity, attitude control loops
- **SLAM**: ORB-SLAM, LSD-SLAM, visual-inertial odometry (VIO)
- **Path Planning**: A*, RRT, RRT*, Dijkstra, potential fields
- **Sensor Fusion**: EKF, UKF, complementary filters
- **GPS-Denied Navigation**: AprilTags, visual odometry, LiDAR SLAM

### Computer Vision
- **Object Detection**: YOLO (v5/v8/v10), EfficientDet, SSD
- **Tracking**: ByteTrack, DeepSORT, SORT, optical flow
- **Edge Deployment**: TensorRT, ONNX, OpenVINO optimization
- **3D Vision**: Stereo depth, point clouds, structure-from-motion

### Hardware Integration
- **Flight Controllers**: Pixhawk, Ardupilot, PX4, DJI
- **Protocols**: MAVLink, DroneKit, MAVSDK
- **Edge Compute**: Jetson (Nano/Xavier/Orin), Coral TPU
- **Sensors**: IMU, GPS, barometer, LiDAR, depth cameras

## Anti-Patterns to Avoid

### 1. "Simulation-Only Syndrome"
**Wrong**: Testing only in Gazebo/AirSim, then deploying directly to real drone.
**Right**: Simulation → Bench test → Tethered flight → Controlled environment → Field.

### 2. "EKF Overkill"
**Wrong**: Using Extended Kalman Filter when complementary filter suffices.
**Right**: Match filter complexity to requirements:
- Complementary filter: Basic stabilization, attitude only
- EKF: Multi-sensor fusion, GPS+IMU+baro
- UKF: Highly nonlinear systems, aggressive maneuvers

### 3. "Max Resolution Assumption"
**Wrong**: Processing 4K frames at 30fps expecting real-time performance.
**Right**: Resolution trade-offs by altitude/speed:
| Altitude | Speed | Resolution | FPS | Rationale |
|----------|-------|------------|-----|-----------|
| &lt;30m | Slow | 1920x1080 | 30 | Detail needed |
| 30-100m | Medium | 1280x720 | 30 | Balance |
| &gt;100m | Fast | 640x480 | 60 | Speed priority |

### 4. "Single-Thread Processing"
**Wrong**: Sequential detect → track → control in one loop.
**Right**: Pipeline parallelism:
```
Thread 1: Camera capture (async)
Thread 2: Object detection (GPU)
Thread 3: Tracking + state estimation
Thread 4: Control commands
```

### 5. "GPS Trust"
**Wrong**: Assuming GPS is always accurate and available.
**Right**: Multi-source position estimation:
- GPS: 2-5m accuracy outdoor, unavailable indoor
- Visual odometry: 0.1-1% drift, lighting dependent
- AprilTags: cm-level accuracy where deployed
- IMU: Short-term only, drift accumulates

### 6. "One Model Fits All"
**Wrong**: Using same YOLO model for all scenarios.
**Right**: Model selection by constraint:
| Constraint | Model | Notes |
|------------|-------|-------|
| Latency critical | YOLOv8n | 6ms inference |
| Balanced | YOLOv8s | 15ms, better accuracy |
| Accuracy first | YOLOv8x | 50ms, highest mAP |
| Edge device | YOLOv8n + TensorRT | 3ms on Jetson |

## Problem-Solving Framework

### 1. Constraint Analysis
- **Compute**: What hardware? (Jetson Nano = ~5 TOPS, Xavier = 32 TOPS)
- **Power**: Battery capacity? Flight time impact?
- **Latency**: Control loop rate? Detection response time?
- **Weight**: Payload capacity? Center of gravity?
- **Environment**: Indoor/outdoor? GPS available? Lighting conditions?

### 2. Algorithm Selection Matrix

| Problem | Classical Approach | Deep Learning | When to Use Each |
|---------|-------------------|---------------|------------------|
| Feature tracking | KLT optical flow | FlowNet | Classical: Real-time, limited compute. DL: Robust, more compute |
| Object detection | HOG+SVM | YOLO/SSD | Classical: Simple objects, no GPU. DL: Complex, GPU available |
| SLAM | ORB-SLAM | DROID-SLAM | Classical: Mature, debuggable. DL: Better in challenging scenes |
| Path planning | A*, RRT | RL-based | Classical: Known environments. DL: Complex, dynamic |

### 3. Safety Checklist
- [ ] Kill switch tested and accessible
- [ ] Geofence configured
- [ ] Return-to-home altitude set
- [ ] Low battery action defined
- [ ] Signal loss action defined
- [ ] Propeller guards (if applicable)
- [ ] Pre-flight sensor calibration
- [ ] Weather conditions checked

## Quick Reference Tables

### MAVLink Message Types
| Message | Purpose | Frequency |
|---------|---------|-----------|
| HEARTBEAT | Connection alive | 1 Hz |
| ATTITUDE | Roll/pitch/yaw | 10-100 Hz |
| LOCAL_POSITION_NED | Position | 10-50 Hz |
| GPS_RAW_INT | Raw GPS | 1-10 Hz |
| SET_POSITION_TARGET | Commands | As needed |

### Kalman Filter Tuning
| Matrix | High Values | Low Values |
|--------|-------------|------------|
| Q (process noise) | Trust measurements more | Trust model more |
| R (measurement noise) | Trust model more | Trust measurements more |
| P (initial covariance) | Uncertain initial state | Confident initial state |

### Common Coordinate Frames
| Frame | Origin | Axes | Use |
|-------|--------|------|-----|
| NED | Takeoff point | North-East-Down | Navigation |
| ENU | Takeoff point | East-North-Up | ROS standard |
| Body | Drone CG | Forward-Right-Down | Control |
| Camera | Lens center | Right-Down-Forward | Vision |

## Reference Files

Detailed implementations in `references/`:
- `navigation-algorithms.md` - SLAM, path planning, localization
- `sensor-fusion-ekf.md` - Kalman filters, multi-sensor fusion
- `object-detection-tracking.md` - YOLO, ByteTrack, optical flow

## Simulation Tools

| Tool | Strengths | Weaknesses | Best For |
|------|-----------|------------|----------|
| Gazebo | ROS integration, physics | Graphics quality | ROS development |
| AirSim | Photorealistic, CV-focused | Windows-centric | Vision algorithms |
| Webots | Multi-robot, accessible | Less drone-specific | Swarm simulations |
| MATLAB/Simulink | Control design | Not real-time | Controller tuning |

## Emerging Technologies (2024-2025)

- **Event cameras**: 1μs temporal resolution, no motion blur
- **Neuromorphic computing**: Loihi 2 for ultra-low-power inference
- **4D Radar**: Velocity + 3D position, works in all weather
- **Swarm autonomy**: Decentralized coordination, emergent behavior
- **Foundation models**: SAM, CLIP for zero-shot detection

## Integration Points

- **drone-inspection-specialist**: Domain-specific detection (fire, damage, thermal)
- **metal-shader-expert**: GPU-accelerated vision processing, custom shaders
- **collage-layout-expert**: Report generation, visual composition

---

**Key Principle**: In drone systems, reliability trumps performance. A 95% accurate system that never crashes is better than 99% accurate that fails unpredictably. Always have fallbacks.
