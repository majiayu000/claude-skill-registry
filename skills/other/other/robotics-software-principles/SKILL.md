---
name: robotics-software-principles
description: >
  Foundational software design principles applied specifically to robotics module development.
  Use this skill when designing robot software modules, structuring codebases, making architecture
  decisions, reviewing robotics code, or building reusable robotics libraries. Trigger whenever the
  user mentions SOLID principles for robots, modular robotics software, clean architecture for robots,
  dependency injection in robotics, interface design for hardware, real-time design constraints, error
  handling strategies for robots, configuration management, separation of concerns in perception-planning-
  control, composability of robot behaviors, or any discussion of software craftsmanship in a robotics
  context. Also trigger for code reviews of robotics code, refactoring robot software, or designing
  APIs for robotics libraries.
---

# Robotics Software Design Principles

## Why Robotics Software Is Different

Robotics code operates under constraints that most software never faces:

1. **Physical consequences** — A bug doesn't just crash a process, it crashes a robot into a wall
2. **Real-time deadlines** — Missing a 1ms control loop deadline can cause oscillation or damage
3. **Sensor uncertainty** — All inputs are noisy, delayed, and occasionally wrong
4. **Hardware diversity** — Same algorithm must work on 10 different grippers from 5 vendors
5. **Sim-to-real gap** — Code must run identically in simulation and on real hardware
6. **Long-running operation** — Robots run for hours/days; memory leaks and drift matter
7. **Safety criticality** — Some failures must NEVER happen, regardless of software state

These constraints demand disciplined design. Below are principles that account for them.

---

## Principle 1: Single Responsibility — One Module, One Job

Every module (node, class, function) should have exactly ONE reason to change.

**Why it matters in robotics**: A perception module that also does control means a camera driver update can break your arm controller. In safety-critical systems, this coupling is unacceptable.

```python
# ❌ BAD: God module — perception + planning + control + logging
class RobotController:
    def __init__(self):
        self.camera = RealSenseCamera()
        self.detector = YOLODetector()
        self.planner = RRTPlanner()
        self.arm = UR5Driver()
        self.logger = DataLogger()

    def run(self):
        image = self.camera.capture()
        objects = self.detector.detect(image)
        path = self.planner.plan(objects[0].pose)
        self.arm.execute(path)
        self.logger.log(image, objects, path)
        # If ANY of these changes, you touch this class

# ✅ GOOD: Separated responsibilities with clear interfaces
class PerceptionModule:
    """ONLY responsibility: raw sensor data → detected objects"""
    def __init__(self, camera: CameraInterface, detector: DetectorInterface):
        self.camera = camera
        self.detector = detector

    def get_detections(self) -> List[Detection]:
        image = self.camera.capture()
        return self.detector.detect(image)

class PlanningModule:
    """ONLY responsibility: goal + world state → trajectory"""
    def __init__(self, planner: PlannerInterface):
        self.planner = planner

    def plan_to(self, target: Pose, obstacles: List[Obstacle]) -> Trajectory:
        return self.planner.plan(target, obstacles)

class ExecutionModule:
    """ONLY responsibility: trajectory → hardware commands"""
    def __init__(self, arm: ArmInterface):
        self.arm = arm

    def execute(self, trajectory: Trajectory) -> ExecutionResult:
        return self.arm.follow_trajectory(trajectory)
```

**Test**: Can you describe what a module does WITHOUT using "and"? If not, split it.

---

## Principle 2: Dependency Inversion — Depend on Abstractions, Not Hardware

High-level modules (planning, behavior) should never depend on low-level modules (drivers, hardware). Both should depend on abstractions.

**Why it matters in robotics**: This is the foundation of sim-to-real. If your planner imports `UR5Driver` directly, it can't run in simulation. If it depends on `ArmInterface`, you swap implementations freely.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
import numpy as np

# ─── ABSTRACTIONS (the contracts) ────────────────────────────

class ArmInterface(ABC):
    """Abstract arm — every arm implementation must honor this contract"""

    @abstractmethod
    def get_joint_positions(self) -> np.ndarray:
        """Returns current joint positions in radians"""
        ...

    @abstractmethod
    def get_ee_pose(self) -> Pose:
        """Returns current end-effector pose"""
        ...

    @abstractmethod
    def move_to_joints(self, positions: np.ndarray,
                        velocity: float = 0.5) -> bool:
        """Move to joint positions. Returns True on success."""
        ...

    @abstractmethod
    def stop(self) -> None:
        """Immediately stop all motion"""
        ...

    @property
    @abstractmethod
    def joint_limits(self) -> List[tuple]:
        """Returns [(min, max)] for each joint"""
        ...


class CameraInterface(ABC):
    """Abstract camera — any RGB camera must honor this"""

    @abstractmethod
    def capture(self) -> np.ndarray:
        """Returns (H, W, 3) uint8 RGB image"""
        ...

    @abstractmethod
    def get_intrinsics(self) -> CameraIntrinsics:
        """Returns camera intrinsic parameters"""
        ...

    @property
    @abstractmethod
    def resolution(self) -> tuple:
        """Returns (width, height)"""
        ...


class GripperInterface(ABC):
    @abstractmethod
    def open(self, width: float = 1.0) -> bool: ...

    @abstractmethod
    def close(self, force: float = 0.5) -> bool: ...

    @abstractmethod
    def get_width(self) -> float: ...

    @abstractmethod
    def is_grasping(self) -> bool: ...


# ─── CONCRETE IMPLEMENTATIONS ────────────────────────────────

class UR5Arm(ArmInterface):
    """Real UR5 via RTDE protocol"""
    def __init__(self, ip: str):
        self.rtde = RTDEControl(ip)
        self.rtde_receive = RTDEReceive(ip)

    def get_joint_positions(self) -> np.ndarray:
        return np.array(self.rtde_receive.getActualQ())

    def move_to_joints(self, positions, velocity=0.5):
        self.rtde.moveJ(positions.tolist(), velocity)
        return True

    def stop(self):
        self.rtde.stopScript()

    @property
    def joint_limits(self):
        return [(-2*np.pi, 2*np.pi)] * 6


class MuJoCoArm(ArmInterface):
    """Simulated arm in MuJoCo — SAME interface"""
    def __init__(self, model_path: str, joint_names: List[str]):
        self.model = mujoco.MjModel.from_xml_path(model_path)
        self.data = mujoco.MjData(self.model)
        self.joint_ids = [mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, n)
                          for n in joint_names]

    def get_joint_positions(self) -> np.ndarray:
        return np.array([self.data.qpos[jid] for jid in self.joint_ids])

    def move_to_joints(self, positions, velocity=0.5):
        # Simulate motion with position control
        self.data.ctrl[:len(positions)] = positions
        for _ in range(100):
            mujoco.mj_step(self.model, self.data)
        return True

    def stop(self):
        self.data.ctrl[:] = 0


# ─── HIGH-LEVEL CODE DEPENDS ONLY ON ABSTRACTIONS ────────────

class PickPlaceTask:
    """This class works with ANY arm + gripper + camera.
    It never knows or cares if it's sim or real."""

    def __init__(self, arm: ArmInterface, gripper: GripperInterface,
                 camera: CameraInterface, detector: DetectorInterface):
        self.arm = arm
        self.gripper = gripper
        self.camera = camera
        self.detector = detector

    def execute(self, target_class: str) -> bool:
        image = self.camera.capture()
        detections = self.detector.detect(image)
        target = next((d for d in detections if d.label == target_class), None)
        if target is None:
            return False

        self.arm.move_to_joints(self.ik(target.pose))
        self.gripper.close()
        self.arm.move_to_joints(self.place_joints)
        self.gripper.open()
        return True
```

**The Dependency Rule in Robotics**:
```
Application / Tasks
    ↓ depends on
Interfaces (ABC)
    ↑ implements
Hardware Drivers / Simulators
```

Arrows point inward. High-level policy never imports low-level drivers.

---

## Principle 3: Open-Closed — Extend Without Modifying

Modules should be open for extension but closed for modification. Add new capabilities by adding new code, not changing existing code.

**Why it matters in robotics**: You constantly add new sensors, new robots, new tasks. If adding a new camera requires modifying your perception pipeline, you'll break existing deployments.

```python
# ❌ BAD: Adding a new sensor requires modifying existing code
class PerceptionPipeline:
    def process(self, sensor_type: str, data):
        if sensor_type == 'realsense':
            return self._process_realsense(data)
        elif sensor_type == 'zed':
            return self._process_zed(data)
        elif sensor_type == 'oakd':    # New sensor = modify this class
            return self._process_oakd(data)

# ✅ GOOD: Plugin architecture — add sensors without touching core
class SensorPlugin(ABC):
    """Base class for all sensor plugins"""
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def process(self, raw_data) -> ProcessedData: ...

    @abstractmethod
    def get_intrinsics(self) -> dict: ...


class RealSensePlugin(SensorPlugin):
    def name(self): return 'realsense'
    def process(self, raw_data):
        # RealSense-specific processing
        return ProcessedData(...)


class ZEDPlugin(SensorPlugin):
    def name(self): return 'zed'
    def process(self, raw_data):
        # ZED-specific processing
        return ProcessedData(...)


# Core pipeline never changes when you add sensors
class PerceptionPipeline:
    def __init__(self):
        self._plugins: dict[str, SensorPlugin] = {}

    def register_sensor(self, plugin: SensorPlugin):
        """Extend the pipeline without modifying it"""
        self._plugins[plugin.name()] = plugin

    def process(self, sensor_name: str, data):
        if sensor_name not in self._plugins:
            raise ValueError(f"Unknown sensor: {sensor_name}")
        return self._plugins[sensor_name].process(data)


# Adding OAK-D = add a file, register at startup. Zero changes to core.
class OAKDPlugin(SensorPlugin):
    def name(self): return 'oakd'
    def process(self, raw_data):
        return ProcessedData(...)

pipeline = PerceptionPipeline()
pipeline.register_sensor(RealSensePlugin())
pipeline.register_sensor(OAKDPlugin())  # No core code changed
```

---

## Principle 4: Interface Segregation — Small, Focused Interfaces

Don't force modules to depend on interfaces they don't use. Many small interfaces beat one large one.

**Why it matters in robotics**: A simple 1-DOF gripper shouldn't implement a 6-DOF dexterous hand interface. A fixed camera shouldn't implement pan-tilt methods.

```python
# ❌ BAD: Fat interface — every camera must implement ALL of these
class CameraInterface(ABC):
    @abstractmethod
    def capture_rgb(self) -> np.ndarray: ...
    @abstractmethod
    def capture_depth(self) -> np.ndarray: ...
    @abstractmethod
    def capture_pointcloud(self) -> np.ndarray: ...
    @abstractmethod
    def set_exposure(self, value: float): ...
    @abstractmethod
    def set_pan_tilt(self, pan: float, tilt: float): ...
    @abstractmethod
    def stream_video(self) -> Iterator[np.ndarray]: ...
    # A simple USB webcam can't do half of these!

# ✅ GOOD: Segregated interfaces — implement only what you support
class RGBCamera(ABC):
    """Any camera that produces RGB images"""
    @abstractmethod
    def capture_rgb(self) -> np.ndarray: ...

    @property
    @abstractmethod
    def resolution(self) -> tuple: ...

class DepthCamera(ABC):
    """Cameras that also produce depth"""
    @abstractmethod
    def capture_depth(self) -> np.ndarray: ...

    @abstractmethod
    def get_depth_intrinsics(self) -> DepthIntrinsics: ...

class ControllableCamera(ABC):
    """Cameras with adjustable settings"""
    @abstractmethod
    def set_exposure(self, value: float): ...

    @abstractmethod
    def set_white_balance(self, value: float): ...

class PTZCamera(ABC):
    """Pan-tilt-zoom cameras"""
    @abstractmethod
    def set_pan_tilt(self, pan: float, tilt: float): ...

    @abstractmethod
    def set_zoom(self, level: float): ...


# A RealSense implements RGB + Depth, but not PTZ
class RealSenseD435(RGBCamera, DepthCamera, ControllableCamera):
    def capture_rgb(self): ...
    def capture_depth(self): ...
    def set_exposure(self, value): ...
    # No PTZ methods — it's not a PTZ camera!

# A webcam implements only RGB
class USBWebcam(RGBCamera):
    def capture_rgb(self): ...
    # Nothing else required

# Perception code that only needs RGB doesn't pull in depth dependencies
class ObjectDetector:
    def __init__(self, camera: RGBCamera):  # Only needs RGB
        self.camera = camera

    def detect(self) -> List[Detection]:
        image = self.camera.capture_rgb()
        return self.model.predict(image)
```

---

## Principle 5: Liskov Substitution — Replaceable Implementations

Any implementation of an interface must be substitutable without the caller knowing. If your code works with `ArmInterface`, it must work with ANY arm that implements it.

**Why it matters in robotics**: Sim-to-real transfer, hardware swaps, and multi-robot support all depend on this.

```python
# ❌ BAD: Violates substitution — caller must know the implementation
class FrankaArm(ArmInterface):
    def move_to_joints(self, positions, velocity=0.5):
        if len(positions) != 7:
            raise ValueError("Franka has 7 joints!")  # Franka-specific
        # ...

class UR5Arm(ArmInterface):
    def move_to_joints(self, positions, velocity=0.5):
        if len(positions) != 6:
            raise ValueError("UR5 has 6 joints!")  # UR5-specific
        # ...

# Caller must know which arm it's using to pass correct joint count!
# This breaks substitutability.

# ✅ GOOD: Self-describing implementations
class ArmInterface(ABC):
    @property
    @abstractmethod
    def num_joints(self) -> int: ...

    @property
    @abstractmethod
    def joint_limits(self) -> List[tuple]: ...

    @abstractmethod
    def move_to_joints(self, positions: np.ndarray, velocity: float = 0.5) -> bool:
        """Positions must have length == self.num_joints"""
        ...

class FrankaArm(ArmInterface):
    @property
    def num_joints(self): return 7

    def move_to_joints(self, positions, velocity=0.5):
        assert len(positions) == self.num_joints
        # ...

# Caller code is generic — works with any arm
def move_to_home(arm: ArmInterface):
    home = np.zeros(arm.num_joints)  # Queries the arm, doesn't assume
    arm.move_to_joints(home)
```

**Substitution test**: Take every line of caller code. Replace `UR5` with `Franka` with `SimArm`. Does it still work? If not, your abstraction leaks.

---

## Principle 6: Separation of Rates — Respect Timing Boundaries

Different subsystems run at different rates. Never couple them.

```
Component          Typical Rate     Criticality
─────────────────────────────────────────────────
Safety monitor     1000 Hz          HARD real-time
Joint controller   500-1000 Hz      HARD real-time
Trajectory exec    100-200 Hz       Firm real-time
State estimation   50-200 Hz        Firm real-time
Perception         10-30 Hz         Soft real-time
Planning           1-10 Hz          Best effort
Task management    0.1-1 Hz         Best effort
Logging            1-30 Hz          Best effort
UI/Dashboard       1-10 Hz          Best effort
```

```python
# ❌ BAD: Perception blocks the control loop
class Robot:
    def control_loop(self):  # Must run at 100Hz = 10ms budget
        image = self.camera.capture()           # 5ms
        objects = self.detector.detect(image)    # 200ms ← BLOCKS!
        pose = self.estimate_pose(objects)       # 2ms
        cmd = self.controller.compute(pose)      # 0.1ms
        self.arm.send_command(cmd)               # 0.5ms
        # Total: 207ms. Control runs at 5Hz instead of 100Hz!

# ✅ GOOD: Decoupled rates with async boundaries
class Robot:
    def __init__(self):
        self.latest_detections = []
        self.detection_lock = threading.Lock()

        # Perception runs in its own thread at its own rate
        self.perception_thread = threading.Thread(
            target=self._perception_loop, daemon=True)
        self.perception_thread.start()

    def _perception_loop(self):
        """Runs at ~10Hz — as fast as the detector allows"""
        while self.running:
            image = self.camera.capture()
            detections = self.detector.detect(image)
            with self.detection_lock:
                self.latest_detections = detections

    def control_loop(self):
        """Runs at 100Hz — NEVER blocked by perception"""
        rate = Rate(100)  # 10ms period
        while self.running:
            with self.detection_lock:
                detections = self.latest_detections  # Latest available

            pose = self.estimate_pose(detections)
            cmd = self.controller.compute(pose)
            self.arm.send_command(cmd)
            rate.sleep()
```

**Rule**: If subsystem A is slower than subsystem B, A must communicate to B via a buffer (topic, shared variable, queue) — never by direct call.

---

## Principle 7: Fail-Safe Defaults — Safe Until Proven Otherwise

Every module should default to the safest possible behavior. Safety is not a feature you add — it's the default you degrade from.

```python
# ❌ BAD: Unsafe defaults
class ArmController:
    def __init__(self):
        self.max_velocity = 3.14       # Full speed by default!
        self.collision_check = False    # Off by default!
        self.workspace_limits = None    # No limits by default!

# ✅ GOOD: Safe defaults — must explicitly opt into danger
class ArmController:
    def __init__(self):
        self.max_velocity = 0.1              # Crawl speed by default
        self.collision_check = True           # Always on
        self.workspace_limits = DEFAULT_SAFE_WORKSPACE  # Conservative box
        self.require_enable = True            # Must be explicitly enabled
        self._enabled = False

    def enable(self, operator_confirmed: bool = False):
        """Explicit enable step — requires operator confirmation for real hardware"""
        if not operator_confirmed and not self.is_simulation:
            raise SafetyError(
                "Real hardware requires operator confirmation to enable")
        self._enabled = True

    def move_to(self, target: np.ndarray, velocity: float = None):
        if not self._enabled:
            raise SafetyError("Controller not enabled")

        velocity = velocity or self.max_velocity

        # Clamp velocity to safe range
        velocity = min(velocity, self.max_velocity)

        # Check workspace limits BEFORE moving
        if not self.workspace_limits.contains(target):
            raise WorkspaceViolation(f"Target {target} outside safe workspace")

        # Check for collisions BEFORE moving
        if self.collision_check:
            if self.collision_detector.would_collide(target):
                raise CollisionRisk(f"Collision predicted for target {target}")

        return self._execute_move(target, velocity)
```

**The rule**: What happens when a module receives no input, invalid input, or loses communication? It should stop safely, not continue blindly.

```python
class SafetyDefaults:
    """Centralized safe defaults for the entire system"""

    # Communication loss → stop
    HEARTBEAT_TIMEOUT_MS = 500
    ACTION_ON_TIMEOUT = 'stop'           # Not 'continue_last_command'

    # Unknown state → stop
    ACTION_ON_UNKNOWN_STATE = 'stop'     # Not 'assume_safe'

    # Sensor failure → stop
    ACTION_ON_SENSOR_LOSS = 'stop'       # Not 'use_last_reading'

    # Joint limit approach → slow down
    JOINT_LIMIT_MARGIN_RAD = 0.05        # Stop 0.05 rad before limit
    VELOCITY_NEAR_LIMITS = 0.05          # Crawl near limits

    # Default workspace (conservative bounding box)
    WORKSPACE_MIN = np.array([-0.5, -0.5, 0.0])   # meters
    WORKSPACE_MAX = np.array([0.5, 0.5, 0.8])      # meters
```

---

## Principle 8: Configuration Over Code — Externalize Everything That Changes

Anything that might differ between deployments, robots, or environments should be in configuration, not code.

```python
# ❌ BAD: Hardcoded values scattered across files
class GraspPlanner:
    def plan(self, object_pose):
        approach_height = 0.15          # Magic number
        grasp_depth = 0.02              # Magic number
        if object_pose.z < 0.05:        # Magic number
            return None

# ✅ GOOD: Configuration-driven
# config/grasp_planner.yaml
# grasp_planner:
#   approach_height_m: 0.15
#   grasp_depth_m: 0.02
#   min_object_height_m: 0.05
#   max_grasp_width_m: 0.08
#   approach_velocity: 0.1
#   grasp_force_n: 10.0

@dataclass
class GraspConfig:
    approach_height_m: float = 0.15
    grasp_depth_m: float = 0.02
    min_object_height_m: float = 0.05
    max_grasp_width_m: float = 0.08
    approach_velocity: float = 0.1
    grasp_force_n: float = 10.0

    @classmethod
    def from_yaml(cls, path: str) -> 'GraspConfig':
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data.get('grasp_planner', {}))

    def validate(self):
        assert self.approach_height_m > 0, "Approach height must be positive"
        assert 0 < self.grasp_force_n < 100, "Force out of safe range"


class GraspPlanner:
    def __init__(self, config: GraspConfig):
        config.validate()
        self.config = config

    def plan(self, object_pose):
        if object_pose.z < self.config.min_object_height_m:
            return None
        # ...
```

**What goes in config**: robot IP addresses, joint limits, sensor parameters, safety thresholds, workspace boundaries, task-specific constants, file paths, feature flags.

**What stays in code**: algorithms, control logic, data structures, interface definitions, error handling.

---

## Principle 9: Idempotent Operations — Safe to Retry

Every command should be safe to send twice. Network drops, message duplicates, and retries are facts of life in robotics.

```python
# ❌ BAD: Non-idempotent — sending twice moves the robot twice as far
def move_relative(self, delta: np.ndarray):
    current = self.get_position()
    self.move_to(current + delta)
    # If this message is sent twice due to a retry,
    # the robot moves 2x the intended distance!

# ✅ GOOD: Idempotent — sending twice has the same effect as once
def move_to_absolute(self, target: np.ndarray, command_id: str):
    if command_id == self._last_executed_command:
        return  # Already executed this command, skip
    self._last_executed_command = command_id
    self.move_to(target)
    # Sending this twice is harmless — same target, same result

# ✅ GOOD: Idempotent gripper commands
def set_gripper(self, width: float):
    """Set gripper to absolute width — not open/close toggle"""
    self.gripper.move_to_width(width)
    # Calling set_gripper(0.04) ten times still results in 0.04m width
```

---

## Principle 10: Observe Everything — You Can't Debug What You Can't See

Every module should emit structured telemetry. When a robot behaves unexpectedly at 2 AM, logs are all you have.

```python
import structlog
from dataclasses import dataclass, asdict

logger = structlog.get_logger()

@dataclass
class PerceptionEvent:
    timestamp: float
    num_detections: int
    processing_time_ms: float
    frame_id: str
    detector_confidence: float

class PerceptionModule:
    def process(self, image):
        t_start = time.monotonic()
        detections = self.detector.detect(image)
        t_elapsed = (time.monotonic() - t_start) * 1000

        # Structured logging — machine-parseable
        event = PerceptionEvent(
            timestamp=time.time(),
            num_detections=len(detections),
            processing_time_ms=t_elapsed,
            frame_id=image.header.frame_id,
            detector_confidence=max(
                (d.confidence for d in detections), default=0.0),
        )
        logger.info("perception.processed", **asdict(event))

        # Performance warnings
        if t_elapsed > 100:
            logger.warning("perception.slow",
                processing_time_ms=t_elapsed,
                threshold_ms=100)

        # Anomaly detection
        if len(detections) == 0 and self._expected_objects > 0:
            logger.warning("perception.no_detections",
                expected=self._expected_objects,
                image_mean=float(image.data.mean()))

        return detections
```

**What to log**: state transitions, command executions, safety events, performance metrics, sensor health, error conditions, configuration changes.

**How to log**: structured key-value pairs (not printf strings), with timestamps, severity levels, and module identifiers.

---

## Principle 11: Composability — Build Complex Behaviors from Simple Ones

Design modules as composable building blocks. Complex robot behaviors should emerge from combining simple, tested primitives.

```python
# Primitive skills — simple, tested, reusable
class MoveTo(Skill):
    """Move end-effector to a target pose"""
    def execute(self, target: Pose) -> bool: ...

class Grasp(Skill):
    """Close gripper with force control"""
    def execute(self, force: float = 10.0) -> bool: ...

class Release(Skill):
    """Open gripper"""
    def execute(self) -> bool: ...

class LookAt(Skill):
    """Point camera at a target"""
    def execute(self, target: Point) -> bool: ...

class Detect(Skill):
    """Detect objects of a given class"""
    def execute(self, target_class: str) -> List[Detection]: ...


# Composite skills — built from primitives
class Pick(CompositeSkill):
    """Pick = Detect + MoveTo + Grasp"""
    def __init__(self, detect: Detect, move: MoveTo, grasp: Grasp):
        self.detect = detect
        self.move = move
        self.grasp = grasp

    def execute(self, object_class: str) -> bool:
        detections = self.detect.execute(object_class)
        if not detections:
            return False
        approach = compute_approach_pose(detections[0].pose)
        if not self.move.execute(approach):
            return False
        if not self.move.execute(detections[0].pose):
            return False
        return self.grasp.execute()


class Place(CompositeSkill):
    """Place = MoveTo + Release"""
    def __init__(self, move: MoveTo, release: Release):
        self.move = move
        self.release = release

    def execute(self, target: Pose) -> bool:
        if not self.move.execute(target):
            return False
        return self.release.execute()


class PickAndPlace(CompositeSkill):
    """PickAndPlace = Pick + Place — composed from compositions"""
    def __init__(self, pick: Pick, place: Place):
        self.pick = pick
        self.place = place

    def execute(self, object_class: str, target: Pose) -> bool:
        if not self.pick.execute(object_class):
            return False
        return self.place.execute(target)


# Dependency injection wires everything together at startup
def build_skill_library(arm, gripper, camera, detector):
    move = MoveTo(arm)
    grasp = Grasp(gripper)
    release = Release(gripper)
    look = LookAt(arm)
    detect = Detect(camera, detector)
    pick = Pick(detect, move, grasp)
    place = Place(move, release)
    pick_and_place = PickAndPlace(pick, place)
    return {
        'move': move, 'grasp': grasp, 'release': release,
        'pick': pick, 'place': place,
        'pick_and_place': pick_and_place,
    }
```

---

## Principle 12: Graceful Degradation — Work With What You Have

When components fail, the robot should degrade gracefully rather than stop entirely.

```python
class DegradedModeManager:
    """Manages capability degradation as components fail"""

    def __init__(self):
        self.capabilities = {
            'full_autonomy': {'requires': ['camera', 'lidar', 'arm', 'gripper']},
            'blind_manipulation': {'requires': ['arm', 'gripper']},
            'perception_only': {'requires': ['camera', 'lidar']},
            'safe_stop': {'requires': []},
        }
        self.active_components = set()

    def component_online(self, name: str):
        self.active_components.add(name)
        self._update_mode()

    def component_offline(self, name: str):
        self.active_components.discard(name)
        logger.warning(f"Component offline: {name}")
        self._update_mode()

    def _update_mode(self):
        """Find the best mode we can support with available components"""
        for mode, spec in self.capabilities.items():
            if set(spec['requires']).issubset(self.active_components):
                if mode != self.current_mode:
                    logger.info(f"Mode change: {self.current_mode} → {mode}")
                    self.current_mode = mode
                return
        self.current_mode = 'safe_stop'
        self._execute_safe_stop()
```

---

## Quick Reference: Principle Checklist

Use this during code reviews:

| # | Principle | Check |
|---|-----------|-------|
| 1 | Single Responsibility | Can you describe the module without "and"? |
| 2 | Dependency Inversion | Does high-level code import hardware drivers? |
| 3 | Open-Closed | Does adding a new sensor require modifying existing code? |
| 4 | Interface Segregation | Are implementations forced to stub out unused methods? |
| 5 | Liskov Substitution | Can you swap sim/real without changing caller code? |
| 6 | Separation of Rates | Does perception block the control loop? |
| 7 | Fail-Safe Defaults | What happens on communication loss? |
| 8 | Configuration Over Code | Are there magic numbers in the source? |
| 9 | Idempotent Operations | Is it safe to send every command twice? |
| 10 | Observe Everything | Can you diagnose a 2 AM failure from logs alone? |
| 11 | Composability | Can you build new tasks from existing skills? |
| 12 | Graceful Degradation | What's the robot's behavior when a sensor fails? |
