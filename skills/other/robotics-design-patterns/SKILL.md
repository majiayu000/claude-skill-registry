---
name: robotics-design-patterns
description: >
  Architecture patterns, design principles, and proven recipes for building robust robotics software.
  Use this skill when designing robot software architectures, choosing between behavioral frameworks,
  structuring perception-planning-control pipelines, implementing state machines, designing safety
  systems, or architecting multi-robot systems. Trigger whenever the user mentions behavior trees,
  finite state machines, subsumption architecture, sensor fusion, robot safety, watchdogs, heartbeats,
  graceful degradation, hardware abstraction layers, real-time constraints, or software architecture
  for robots. Also applies to sim-to-real transfer, digital twins, and robot fleet management.
---

# Robotics Design Patterns

## When to Use This Skill
- Designing robot software architecture from scratch
- Choosing between behavior trees, FSMs, or hybrid approaches
- Structuring perception → planning → control pipelines
- Implementing safety systems and watchdogs
- Building hardware abstraction layers (HAL)
- Designing for sim-to-real transfer
- Architecting multi-robot / fleet systems
- Making real-time vs. non-real-time tradeoffs

## Pattern 1: The Robot Software Stack

Every robot system follows this layered architecture, regardless of complexity:

```
┌─────────────────────────────────────────────┐
│               APPLICATION LAYER              │
│    Mission planning, task allocation, UI     │
├─────────────────────────────────────────────┤
│              BEHAVIORAL LAYER                │
│  Behavior trees, FSMs, decision-making       │
├─────────────────────────────────────────────┤
│             FUNCTIONAL LAYER                 │
│  Perception, Planning, Control, Estimation   │
├─────────────────────────────────────────────┤
│           COMMUNICATION LAYER                │
│     ROS2, DDS, shared memory, IPC            │
├─────────────────────────────────────────────┤
│          HARDWARE ABSTRACTION LAYER          │
│    Drivers, sensor interfaces, actuators     │
├─────────────────────────────────────────────┤
│              HARDWARE LAYER                  │
│    Cameras, LiDARs, motors, grippers, IMUs   │
└─────────────────────────────────────────────┘
```

**Design Rule**: Information flows UP through perception, decisions flow DOWN through control. Never let the application layer directly command hardware.

## Pattern 2: Behavior Trees (BT)

Behavior trees are the **recommended default** for robot decision-making. They're modular, reusable, and easier to debug than FSMs for complex behaviors.

### Core Node Types

```
Sequence (→)     : Execute children left-to-right, FAIL on first failure
Fallback (?)     : Execute children left-to-right, SUCCEED on first success
Parallel (⇉)     : Execute all children simultaneously
Decorator        : Modify a single child's behavior
Action (leaf)    : Execute a robot action
Condition (leaf) : Check a condition (no side effects)
```

### Example: Pick-and-Place BT

```
                    → Sequence
                   /    |      \
            → Check     → Pick     → Place
           /    \      /   |  \     /  |  \
       Battery  Obj  Open  Move  Close Move Open Release
       OK?    Found? Grip  To    Grip  To   Grip
                      per  Obj   per   Goal per
```

### Implementation Pattern

```python
import py_trees

class MoveToTarget(py_trees.behaviour.Behaviour):
    """Action node: Move robot to a target pose"""

    def __init__(self, name, target_key="target_pose"):
        super().__init__(name)
        self.target_key = target_key
        self.action_client = None

    def setup(self, **kwargs):
        """Called once when tree is set up — initialize resources"""
        self.node = kwargs.get('node')  # ROS2 node
        self.action_client = ActionClient(
            self.node, MoveBase, 'move_base')

    def initialise(self):
        """Called when this node first ticks — send the goal"""
        bb = self.blackboard
        target = bb.get(self.target_key)
        self.goal_handle = self.action_client.send_goal(target)
        self.logger.info(f"Moving to {target}")

    def update(self):
        """Called every tick — check progress"""
        if self.goal_handle is None:
            return py_trees.common.Status.FAILURE

        status = self.goal_handle.status
        if status == GoalStatus.STATUS_SUCCEEDED:
            return py_trees.common.Status.SUCCESS
        elif status == GoalStatus.STATUS_ABORTED:
            return py_trees.common.Status.FAILURE
        else:
            return py_trees.common.Status.RUNNING

    def terminate(self, new_status):
        """Called when node exits — cancel if preempted"""
        if new_status == py_trees.common.Status.INVALID:
            if self.goal_handle:
                self.goal_handle.cancel_goal()
                self.logger.info("Movement cancelled")

# Build the tree
def create_pick_place_tree():
    root = py_trees.composites.Sequence("PickAndPlace", memory=True)

    # Safety checks (Fallback: if any fails, abort)
    safety = py_trees.composites.Sequence("SafetyChecks", memory=False)
    safety.add_children([
        CheckBattery("BatteryOK", threshold=20.0),
        CheckEStop("EStopClear"),
    ])

    pick = py_trees.composites.Sequence("Pick", memory=True)
    pick.add_children([
        DetectObject("FindObject"),
        MoveToTarget("ApproachObject", target_key="object_pose"),
        GripperCommand("CloseGripper", action="close"),
    ])

    place = py_trees.composites.Sequence("Place", memory=True)
    place.add_children([
        MoveToTarget("MoveToPlace", target_key="place_pose"),
        GripperCommand("OpenGripper", action="open"),
    ])

    root.add_children([safety, pick, place])
    return root
```

### Blackboard Pattern

```python
# The Blackboard is the shared memory for BT nodes
bb = py_trees.blackboard.Blackboard()

# Perception nodes WRITE to blackboard
class DetectObject(py_trees.behaviour.Behaviour):
    def update(self):
        detections = self.perception.detect()
        if detections:
            self.blackboard.set("object_pose", detections[0].pose)
            self.blackboard.set("object_class", detections[0].label)
            return Status.SUCCESS
        return Status.FAILURE

# Action nodes READ from blackboard
class MoveToTarget(py_trees.behaviour.Behaviour):
    def initialise(self):
        target = self.blackboard.get("object_pose")
        self.send_goal(target)
```

## Pattern 3: Finite State Machines (FSM)

Use FSMs for **simple, well-defined sequential behaviors** with clear states. Prefer BTs for anything complex.

```python
from enum import Enum, auto
import smach  # ROS state machine library

class RobotState(Enum):
    IDLE = auto()
    NAVIGATING = auto()
    PICKING = auto()
    PLACING = auto()
    ERROR = auto()
    CHARGING = auto()

# SMACH implementation
class NavigateState(smach.State):
    def __init__(self):
        smach.State.__init__(self,
            outcomes=['succeeded', 'aborted', 'preempted'],
            input_keys=['target_pose'],
            output_keys=['final_pose'])

    def execute(self, userdata):
        # Navigation logic
        result = navigate_to(userdata.target_pose)
        if result.success:
            userdata.final_pose = result.pose
            return 'succeeded'
        return 'aborted'

# Build state machine
sm = smach.StateMachine(outcomes=['done', 'failed'])
with sm:
    smach.StateMachine.add('NAVIGATE', NavigateState(),
        transitions={'succeeded': 'PICK', 'aborted': 'ERROR'})
    smach.StateMachine.add('PICK', PickState(),
        transitions={'succeeded': 'PLACE', 'aborted': 'ERROR'})
    smach.StateMachine.add('PLACE', PlaceState(),
        transitions={'succeeded': 'done', 'aborted': 'ERROR'})
    smach.StateMachine.add('ERROR', ErrorRecovery(),
        transitions={'recovered': 'NAVIGATE', 'fatal': 'failed'})
```

**When to use FSM vs BT**:
- FSM: Linear workflows, simple devices, UI states, protocol implementations
- BT: Complex robots, reactive behaviors, many conditional branches, reusable sub-behaviors

## Pattern 4: Perception Pipeline

```
Raw Sensors → Preprocessing → Detection/Estimation → Fusion → World Model
```

### Sensor Fusion Architecture

```python
class SensorFusion:
    """Multi-sensor fusion using a central world model"""

    def __init__(self):
        self.world_model = WorldModel()
        self.filters = {
            'pose': ExtendedKalmanFilter(state_dim=6),
            'objects': MultiObjectTracker(),
        }

    def update_from_camera(self, detections, timestamp):
        """Camera provides object detections with high latency"""
        for det in detections:
            self.filters['objects'].update(
                det, sensor='camera',
                uncertainty=det.confidence,
                timestamp=timestamp
            )

    def update_from_lidar(self, points, timestamp):
        """LiDAR provides precise geometry with lower latency"""
        clusters = self.segment_points(points)
        for cluster in clusters:
            self.filters['objects'].update(
                cluster, sensor='lidar',
                uncertainty=0.02,  # 2cm typical LiDAR accuracy
                timestamp=timestamp
            )

    def update_from_imu(self, imu_data, timestamp):
        """IMU provides high-frequency attitude estimates"""
        self.filters['pose'].predict(imu_data, dt=timestamp - self.last_imu_t)
        self.last_imu_t = timestamp

    def get_world_state(self):
        """Query the fused world model"""
        return WorldState(
            robot_pose=self.filters['pose'].state,
            objects=self.filters['objects'].get_tracked_objects(),
            confidence=self.filters['objects'].get_confidence_map()
        )
```

### The Perception-Action Loop Timing

```
Camera (30Hz)  ─┐
LiDAR (10Hz)   ─┼──→ Fusion (50Hz) ──→ Planner (10Hz) ──→ Controller (100Hz+)
IMU (200Hz)    ─┘

RULE: Controller frequency > Planner frequency > Sensor frequency
      This ensures smooth execution despite variable perception latency.
```

## Pattern 5: Hardware Abstraction Layer (HAL)

**Never let application code talk directly to hardware.** Always go through an abstraction layer.

```python
from abc import ABC, abstractmethod

class GripperInterface(ABC):
    """Abstract gripper interface — implement for each hardware type"""

    @abstractmethod
    def open(self, width: float = 1.0) -> bool: ...

    @abstractmethod
    def close(self, force: float = 0.5) -> bool: ...

    @abstractmethod
    def get_state(self) -> GripperState: ...

    @abstractmethod
    def get_width(self) -> float: ...


class RobotiqGripper(GripperInterface):
    """Concrete implementation for Robotiq 2F-85"""
    def __init__(self, port='/dev/ttyUSB0'):
        self.serial = serial.Serial(port, 115200)
        # ... Modbus RTU setup

    def close(self, force=0.5):
        cmd = self._build_modbus_cmd(force=int(force * 255))
        self.serial.write(cmd)
        return self._wait_for_completion()


class SimulatedGripper(GripperInterface):
    """Simulation gripper for testing"""
    def __init__(self):
        self.width = 0.085  # 85mm open
        self.state = GripperState.OPEN

    def close(self, force=0.5):
        self.width = 0.0
        self.state = GripperState.CLOSED
        return True


# Factory pattern for hardware instantiation
def create_gripper(config: dict) -> GripperInterface:
    gripper_type = config.get('type', 'simulated')
    if gripper_type == 'robotiq':
        return RobotiqGripper(port=config['port'])
    elif gripper_type == 'simulated':
        return SimulatedGripper()
    else:
        raise ValueError(f"Unknown gripper type: {gripper_type}")
```

## Pattern 6: Safety Systems

### The Safety Hierarchy

```
Level 0: Hardware E-Stop (physical button, cuts power)
Level 1: Safety-rated controller (SIL2/SIL3, hardware watchdog)
Level 2: Software watchdog (monitors heartbeats, enforces limits)
Level 3: Application safety (collision avoidance, workspace limits)
```

### Software Watchdog Pattern

```python
import threading
import time

class SafetyWatchdog:
    """Monitors system health and triggers safe stop on failures"""

    def __init__(self, timeout_ms=500):
        self.timeout = timeout_ms / 1000.0
        self.heartbeats = {}
        self.lock = threading.Lock()
        self.safe_stop_triggered = False

        # Start monitoring thread
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

    def register_component(self, name: str, critical: bool = True):
        """Register a component that must send heartbeats"""
        with self.lock:
            self.heartbeats[name] = {
                'last_beat': time.monotonic(),
                'critical': critical,
                'alive': True
            }

    def heartbeat(self, name: str):
        """Called by components to signal they're alive"""
        with self.lock:
            if name in self.heartbeats:
                self.heartbeats[name]['last_beat'] = time.monotonic()
                self.heartbeats[name]['alive'] = True

    def _monitor_loop(self):
        while True:
            now = time.monotonic()
            with self.lock:
                for name, info in self.heartbeats.items():
                    elapsed = now - info['last_beat']
                    if elapsed > self.timeout and info['alive']:
                        info['alive'] = False
                        if info['critical']:
                            self._trigger_safe_stop(
                                f"Critical component '{name}' "
                                f"timed out ({elapsed:.1f}s)")
            time.sleep(self.timeout / 4)

    def _trigger_safe_stop(self, reason: str):
        if not self.safe_stop_triggered:
            self.safe_stop_triggered = True
            logger.critical(f"SAFE STOP: {reason}")
            self._execute_safe_stop()

    def _execute_safe_stop(self):
        """Bring robot to a safe state"""
        # 1. Stop all motion (zero velocity command)
        # 2. Engage brakes
        # 3. Publish emergency state to all nodes
        # 4. Log the event
        pass
```

### Workspace Limits

```python
class WorkspaceMonitor:
    """Enforce that robot stays within safe operational bounds"""

    def __init__(self, limits: dict):
        self.joint_limits = limits['joints']    # {joint: (min, max)}
        self.cartesian_bounds = limits['cartesian']  # AABB or convex hull
        self.velocity_limits = limits['velocity']
        self.force_limits = limits['force']

    def check_command(self, command) -> SafetyResult:
        """Validate a command BEFORE sending to hardware"""
        violations = []

        # Joint limit check
        for joint, value in command.joint_positions.items():
            lo, hi = self.joint_limits[joint]
            if not (lo <= value <= hi):
                violations.append(
                    f"Joint {joint}={value:.3f} outside [{lo:.3f}, {hi:.3f}]")

        # Velocity check
        for joint, vel in command.joint_velocities.items():
            if abs(vel) > self.velocity_limits[joint]:
                violations.append(
                    f"Joint {joint} velocity {vel:.3f} exceeds limit")

        if violations:
            return SafetyResult(safe=False, violations=violations)
        return SafetyResult(safe=True)
```

## Pattern 7: Sim-to-Real Architecture

```
┌────────────────────────────────────┐
│         Application Code           │
│  (Same code runs in sim AND real)  │
├──────────────┬─────────────────────┤
│   Sim HAL    │     Real HAL        │
│  (MuJoCo/    │  (Hardware          │
│   Gazebo/    │   drivers)          │
│   Isaac)     │                     │
└──────────────┴─────────────────────┘
```

**Key Principles**:
1. Application code NEVER knows if it's in sim or real
2. Same message types, same topic names, same interfaces
3. Use `use_sim_time` parameter to switch clock sources
4. Domain randomization happens INSIDE the sim HAL
5. Transfer learning adapters sit at the HAL boundary

```python
# Config-driven sim/real switching
class RobotDriver:
    def __init__(self, config):
        if config['mode'] == 'simulation':
            self.arm = SimulatedArm(config['sim'])
            self.camera = SimulatedCamera(config['sim'])
        elif config['mode'] == 'real':
            self.arm = UR5Driver(config['real']['arm_ip'])
            self.camera = RealSenseDriver(config['real']['camera_serial'])

        # Application code uses the same interface regardless
        self.perception = PerceptionPipeline(self.camera)
        self.planner = MotionPlanner(self.arm)
```

## Pattern 8: Data Recording Architecture

**Critical for learning-based robotics** — designed for the ForgeIR ecosystem:

```
┌─────────────────────────────────────────────┐
│              Event-Based Recorder            │
│  Triggers: action boundaries, anomalies,     │
│  task completions, operator signals           │
├─────────────────────────────────────────────┤
│           Multimodal Data Streams            │
│  Camera (30Hz) | Joint State (100Hz) |       │
│  Force/Torque (1kHz) | Language Annotations  │
├─────────────────────────────────────────────┤
│            Storage Layer                     │
│  Episode-based structure with metadata       │
│  Format: MCAP / Zarr / HDF5 / RLDS          │
├─────────────────────────────────────────────┤
│           Quality Assessment                 │
│  Completeness checks, trajectory validation  │
│  Anomaly detection, diversity analysis       │
└─────────────────────────────────────────────┘
```

```python
class EpisodeRecorder:
    """Records robot episodes with event-based boundaries"""

    def __init__(self, config):
        self.streams = {}
        self.episode_active = False
        self.current_episode = None
        self.storage = StorageBackend(config['format'])  # Zarr, MCAP, etc.

    def register_stream(self, name, msg_type, frequency_hz):
        self.streams[name] = StreamConfig(
            name=name, type=msg_type, freq=frequency_hz)

    def start_episode(self, metadata: dict):
        """Begin recording an episode with metadata"""
        self.current_episode = Episode(
            id=uuid4(),
            start_time=time.monotonic(),
            metadata=metadata,  # task, operator, environment, etc.
            streams={name: [] for name in self.streams}
        )
        self.episode_active = True

    def record_step(self, stream_name, data, timestamp):
        if self.episode_active:
            self.current_episode.streams[stream_name].append(
                DataPoint(data=data, timestamp=timestamp))

    def end_episode(self, outcome: str, annotations: dict = None):
        """Finalize and store the episode"""
        self.episode_active = False
        self.current_episode.end_time = time.monotonic()
        self.current_episode.outcome = outcome
        self.current_episode.annotations = annotations

        # Validate before saving
        quality = self.validate_episode(self.current_episode)
        self.current_episode.quality_score = quality

        self.storage.save(self.current_episode)
        return self.current_episode.id
```

## Anti-Patterns to Avoid

### 1. God Node
**Problem**: One node does everything — perception, planning, control, logging.
**Fix**: Single responsibility. One node, one job. Connect via topics.

### 2. Hardcoded Magic Numbers
**Problem**: `if distance < 0.35:` scattered everywhere.
**Fix**: Parameters with descriptive names, loaded from config files.

### 3. Polling Instead of Events
**Problem**: `while True: check_sensor(); sleep(0.01)`
**Fix**: Use callbacks, subscribers, event-driven architecture.

### 4. No Error Recovery
**Problem**: Robot stops forever on first error.
**Fix**: Every action node needs a failure mode. Behavior trees with fallbacks.

### 5. Sim-Only Code
**Problem**: Code works perfectly in simulation, crashes on real hardware.
**Fix**: HAL pattern. Test with hardware-in-the-loop early and often.

### 6. No Timestamps
**Problem**: Sensor data without timestamps — impossible to fuse or replay.
**Fix**: Timestamp EVERYTHING at the source. Use monotonic clocks for control.

### 7. Blocking the Control Loop
**Problem**: Perception computation blocks the 100Hz control loop.
**Fix**: Separate processes/threads. Control loop must NEVER be blocked.

### 8. No Data Logging
**Problem**: Can't reproduce bugs, can't train models, can't audit behavior.
**Fix**: Always record. Event-based recording is cheap. Use MCAP format.

## Architecture Decision Checklist

When designing a new robot system, answer these questions:

1. **What's the safety architecture?** (E-stop, watchdog, workspace limits)
2. **What are the real-time requirements?** (Control at 100Hz+, perception at 10-30Hz)
3. **What's the behavioral framework?** (BT for complex, FSM for simple)
4. **How does sim-to-real work?** (HAL pattern, same interfaces)
5. **How is data recorded?** (Episode-based, event-triggered, with metadata)
6. **How are failures handled?** (Graceful degradation, recovery behaviors)
7. **What's the communication middleware?** (ROS2 for most cases)
8. **How is the system deployed?** (Docker, snap, direct install)
9. **How is it tested?** (Unit, integration, hardware-in-the-loop, field)
10. **How is it monitored?** (Heartbeats, metrics, dashboards)
