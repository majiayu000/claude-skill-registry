---
name: robotics-testing
description: >
  Testing strategies, patterns, and tools for robotics software. Use this skill when writing unit tests,
  integration tests, simulation tests, or hardware-in-the-loop tests for robot systems. Trigger whenever
  the user mentions testing ROS nodes, pytest with ROS, launch_testing, simulation testing, CI/CD for
  robotics, test fixtures for sensors, mock hardware, deterministic replay, regression testing for robot
  behaviors, or validating perception/planning/control pipelines. Also covers property-based testing
  for kinematics, fuzz testing for message handlers, and golden-file testing for trajectories.
---

# Robotics Testing Skill

## When to Use This Skill
- Writing unit tests for ROS1/ROS2 nodes
- Setting up integration tests with launch_testing
- Mocking hardware (sensors, actuators) for CI/CD
- Building simulation-based test suites
- Testing perception pipelines with ground truth
- Validating trajectory planners and controllers
- Setting up CI/CD pipelines for robotics packages
- Debugging flaky tests in robotics systems

## The Robotics Testing Pyramid

```
                    ╱╲
                   ╱  ╲        Field Tests
                  ╱    ╲       (Real robot, real environment)
                 ╱──────╲
                ╱        ╲     Hardware-in-the-Loop (HIL)
               ╱          ╲    (Real hardware, controlled environment)
              ╱────────────╲
             ╱              ╲   Simulation Tests
            ╱                ╲  (Full sim, realistic physics)
           ╱──────────────────╲
          ╱                    ╲  Integration Tests
         ╱                      ╲ (Multi-node, message passing)
        ╱────────────────────────╲
       ╱                          ╲ Unit Tests
      ╱____________________________╲ (Single function/class, fast, deterministic)

MORE tests at the bottom, FEWER at the top.
Bottom = fast, cheap, deterministic. Top = slow, expensive, realistic.
```

## Unit Testing Patterns

### Testing ROS2 Nodes with pytest

```python
# test_perception_node.py
import pytest
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from my_pkg.perception_node import PerceptionNode
import numpy as np

@pytest.fixture(scope='module')
def ros_context():
    """Initialize ROS2 context once per test module"""
    rclpy.init()
    yield
    rclpy.shutdown()

@pytest.fixture
def perception_node(ros_context):
    """Create a fresh perception node for each test"""
    node = PerceptionNode()
    yield node
    node.destroy_node()

@pytest.fixture
def test_image():
    """Generate a synthetic test image"""
    msg = Image()
    msg.height = 256
    msg.width = 256
    msg.encoding = 'rgb8'
    msg.step = 256 * 3
    msg.data = np.random.randint(0, 255, (256, 256, 3),
                                  dtype=np.uint8).tobytes()
    return msg

class TestPerceptionNode:

    def test_initialization(self, perception_node):
        """Node should initialize with correct default parameters"""
        assert perception_node.get_parameter('confidence_threshold').value == 0.7
        assert perception_node.get_parameter('rate_hz').value == 30.0

    def test_parameter_validation(self, perception_node):
        """Node should reject invalid parameter values"""
        from rcl_interfaces.msg import SetParametersResult
        result = perception_node.set_parameters([
            rclpy.parameter.Parameter('confidence_threshold',
                                       value=-0.5)  # Invalid!
        ])
        assert not result[0].successful

    def test_image_callback_publishes_detections(self, perception_node, test_image):
        """Processing an image should produce detection output"""
        received = []

        # Create a test subscriber
        sub_node = Node('test_subscriber')
        sub_node.create_subscription(
            DetectionArray, '/perception/detections',
            lambda msg: received.append(msg), 10)

        # Simulate image callback
        perception_node.image_callback(test_image)

        # Spin briefly to allow message propagation
        rclpy.spin_once(sub_node, timeout_sec=1.0)
        rclpy.spin_once(perception_node, timeout_sec=1.0)

        # Verify
        assert len(received) > 0
        sub_node.destroy_node()

    def test_empty_image_handling(self, perception_node):
        """Node should handle empty/corrupted images gracefully"""
        empty_msg = Image()  # No data
        # Should not crash
        perception_node.image_callback(empty_msg)
```

### Testing Pure Functions (No ROS Dependency)

```python
# test_kinematics.py
import pytest
import numpy as np
from my_pkg.kinematics import (
    forward_kinematics, inverse_kinematics,
    quaternion_multiply, transform_point
)

class TestForwardKinematics:

    @pytest.mark.parametrize("joint_angles,expected_pos", [
        # Home position
        (np.zeros(7), np.array([0.088, 0.0, 1.033])),
        # Known calibrated pose
        (np.array([0, -0.785, 0, -2.356, 0, 1.571, 0.785]),
         np.array([0.307, 0.0, 0.59])),
    ])
    def test_known_poses(self, joint_angles, expected_pos):
        """FK should match known calibrated positions"""
        result = forward_kinematics(joint_angles)
        np.testing.assert_allclose(result[:3], expected_pos, atol=0.01)

    def test_fk_ik_roundtrip(self):
        """FK(IK(pose)) should return the original pose"""
        original_pose = np.array([0.4, 0.1, 0.5, 1.0, 0.0, 0.0, 0.0])
        joint_angles = inverse_kinematics(original_pose)
        recovered_pose = forward_kinematics(joint_angles)
        np.testing.assert_allclose(recovered_pose, original_pose, atol=1e-4)

    def test_joint_limits_respected(self):
        """IK should not return angles outside joint limits"""
        target = np.array([0.5, 0.2, 0.3, 1.0, 0.0, 0.0, 0.0])
        joints = inverse_kinematics(target)
        for i, (lo, hi) in enumerate(JOINT_LIMITS):
            assert lo <= joints[i] <= hi, \
                f"Joint {i}: {joints[i]} outside [{lo}, {hi}]"


class TestQuaternionMath:

    def test_identity_multiply(self):
        """q * identity = q"""
        q = np.array([0.5, 0.5, 0.5, 0.5])
        identity = np.array([1.0, 0.0, 0.0, 0.0])
        result = quaternion_multiply(q, identity)
        np.testing.assert_allclose(result, q, atol=1e-10)

    def test_inverse_multiply(self):
        """q * q_inv = identity"""
        q = np.array([0.5, 0.5, 0.5, 0.5])
        q_inv = np.array([0.5, -0.5, -0.5, -0.5])
        result = quaternion_multiply(q, q_inv)
        np.testing.assert_allclose(result, [1, 0, 0, 0], atol=1e-10)

    @pytest.mark.parametrize("q", [
        np.random.randn(4) for _ in range(20)  # Random quaternions
    ])
    def test_unit_quaternion_preserved(self, q):
        """Multiplication of unit quaternions should produce unit quaternion"""
        q = q / np.linalg.norm(q)  # Normalize
        q2 = np.array([0.707, 0.707, 0, 0])  # 90° rotation
        result = quaternion_multiply(q, q2)
        assert abs(np.linalg.norm(result) - 1.0) < 1e-10
```

### Property-Based Testing with Hypothesis

```python
from hypothesis import given, strategies as st, settings
import hypothesis.extra.numpy as hnp

class TestTrajectoryInterpolation:

    @given(
        start=hnp.arrays(np.float64, (7,),
            elements=st.floats(min_value=-3.14, max_value=3.14)),
        end=hnp.arrays(np.float64, (7,),
            elements=st.floats(min_value=-3.14, max_value=3.14)),
        num_steps=st.integers(min_value=2, max_value=1000),
    )
    @settings(max_examples=200)
    def test_interpolation_properties(self, start, end, num_steps):
        """Trajectory interpolation should satisfy mathematical properties"""
        traj = linear_interpolate(start, end, num_steps)

        # Property 1: Correct number of steps
        assert len(traj) == num_steps

        # Property 2: Starts at start, ends at end
        np.testing.assert_allclose(traj[0], start, atol=1e-10)
        np.testing.assert_allclose(traj[-1], end, atol=1e-10)

        # Property 3: Monotonic progress (each step closer to goal)
        for i in range(1, len(traj)):
            dist_prev = np.linalg.norm(traj[i-1] - end)
            dist_curr = np.linalg.norm(traj[i] - end)
            assert dist_curr <= dist_prev + 1e-10

        # Property 4: No jumps exceed max step size
        diffs = np.diff(traj, axis=0)
        max_step = np.max(np.abs(diffs))
        expected_max = np.max(np.abs(end - start)) / (num_steps - 1)
        assert max_step <= expected_max + 1e-10

    @given(
        points=hnp.arrays(np.float64, (3,),
            elements=st.floats(min_value=-10, max_value=10, allow_nan=False)),
    )
    def test_transform_roundtrip(self, points):
        """Transform followed by inverse transform = identity"""
        T = random_transform_matrix()
        T_inv = np.linalg.inv(T)
        transformed = transform_point(T, points)
        recovered = transform_point(T_inv, transformed)
        np.testing.assert_allclose(recovered, points, atol=1e-8)
```

## Integration Testing

### ROS2 Launch Testing

```python
# test_integration.py
import pytest
import launch_testing
from launch import LaunchDescription
from launch_ros.actions import Node
import rclpy
import unittest

@pytest.mark.launch_test
def generate_test_description():
    """Launch the nodes we want to test"""
    perception_node = Node(
        package='my_pkg', executable='perception_node',
        parameters=[{'use_sim_time': True}],
    )
    planner_node = Node(
        package='my_pkg', executable='planner_node',
        parameters=[{'use_sim_time': True}],
    )

    return LaunchDescription([
        perception_node,
        planner_node,
        launch_testing.actions.ReadyToTest(),
    ])


class TestPerceptionPlannerIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rclpy.init()
        cls.node = rclpy.create_node('integration_test')

    @classmethod
    def tearDownClass(cls):
        cls.node.destroy_node()
        rclpy.shutdown()

    def test_perception_publishes_to_planner(self):
        """Perception detections should reach the planner"""
        # Publish a test image
        pub = self.node.create_publisher(Image, '/camera/image_raw', 10)
        test_img = create_test_image_with_object()
        pub.publish(test_img)

        # Wait for planner output
        received = []
        sub = self.node.create_subscription(
            Path, '/planner/path',
            lambda msg: received.append(msg), 10)

        end_time = self.node.get_clock().now() + rclpy.duration.Duration(seconds=5)
        while self.node.get_clock().now() < end_time and not received:
            rclpy.spin_once(self.node, timeout_sec=0.1)

        self.assertGreater(len(received), 0, "Planner should produce a path")
        self.assertGreater(len(received[0].poses), 0, "Path should have poses")
```

## Mock Hardware Patterns

```python
class MockCamera:
    """Mock camera for testing without hardware"""

    def __init__(self, image_dir=None, resolution=(640, 480)):
        self.resolution = resolution
        self.frame_count = 0

        if image_dir:
            # Use pre-recorded test images
            self.images = self._load_test_images(image_dir)
        else:
            # Generate synthetic images
            self.images = None

    def get_frame(self):
        self.frame_count += 1
        if self.images:
            idx = self.frame_count % len(self.images)
            return self.images[idx]
        else:
            return self._generate_synthetic_frame()

    def _generate_synthetic_frame(self):
        """Generate a deterministic test frame with known objects"""
        img = np.zeros((*self.resolution[::-1], 3), dtype=np.uint8)
        # Draw a red rectangle (simulated object)
        img[100:200, 150:250] = [255, 0, 0]
        return img


class MockJointStatePublisher:
    """Publish deterministic joint states for testing"""

    def __init__(self, node, trajectory=None):
        self.pub = node.create_publisher(
            JointState, '/joint_states', 10)
        self.step = 0

        if trajectory is not None:
            self.trajectory = trajectory
        else:
            # Sinusoidal motion for testing
            t = np.linspace(0, 2*np.pi, 100)
            self.trajectory = np.column_stack([
                0.1 * np.sin(t + i * 0.5) for i in range(7)
            ])

    def publish_next(self):
        msg = JointState()
        msg.header.stamp = self.node.get_clock().now().to_msg()
        msg.name = [f'joint_{i}' for i in range(7)]
        idx = self.step % len(self.trajectory)
        msg.position = self.trajectory[idx].tolist()
        self.pub.publish(msg)
        self.step += 1
```

## Golden File Testing (Trajectory Regression)

```python
class TestTrajectoryRegression:
    """Compare planner output against known-good trajectories"""

    GOLDEN_DIR = Path(__file__).parent / 'golden_trajectories'

    def test_straight_line_plan(self):
        start = np.array([0.3, 0.0, 0.5])
        goal = np.array([0.5, 0.2, 0.3])

        trajectory = planner.plan(start, goal)

        golden_file = self.GOLDEN_DIR / 'straight_line.npy'
        if not golden_file.exists():
            # First run: save as golden
            np.save(golden_file, trajectory)
            pytest.skip("Golden file created — re-run to test")

        golden = np.load(golden_file)
        np.testing.assert_allclose(trajectory, golden, atol=1e-4,
            err_msg="Trajectory regression! Planner output changed.")

    def test_obstacle_avoidance_plan(self):
        start = np.array([0.3, 0.0, 0.5])
        goal = np.array([0.5, 0.2, 0.3])
        obstacles = [Sphere(center=[0.4, 0.1, 0.4], radius=0.05)]

        trajectory = planner.plan(start, goal, obstacles=obstacles)

        # Verify no collisions
        for point in trajectory:
            for obs in obstacles:
                dist = np.linalg.norm(point[:3] - obs.center)
                assert dist > obs.radius, \
                    f"Collision at {point[:3]}, dist={dist:.4f}"
```

## Simulation Testing

```python
class SimulationTestHarness:
    """Run behavior tests in simulation with deterministic physics"""

    def __init__(self, sim_config):
        self.sim = MuJoCoSimulator(sim_config)
        self.sim.set_seed(42)  # Deterministic physics

    def test_pick_and_place(self):
        """Full pick-and-place task in simulation"""
        # Setup scene
        self.sim.reset()
        self.sim.spawn_object('red_block', pose=[0.4, 0.1, 0.02])

        # Run behavior tree
        bt = create_pick_place_tree()
        bt.setup(sim=self.sim)

        max_steps = 1000
        for step in range(max_steps):
            bt.tick()
            self.sim.step()

            if bt.root.status == Status.SUCCESS:
                break

        # Verify outcome
        block_pose = self.sim.get_object_pose('red_block')
        target_pose = np.array([0.5, -0.1, 0.02])
        assert np.linalg.norm(block_pose[:3] - target_pose) < 0.02, \
            f"Block not at target: {block_pose[:3]} vs {target_pose}"
        assert step < max_steps - 1, "Task did not complete in time"

    def test_collision_safety(self):
        """Robot should never collide with table"""
        self.sim.reset()
        self.sim.spawn_object('obstacle', pose=[0.35, 0.0, 0.15])

        trajectory = planner.plan_with_obstacle(
            start=[0.3, -0.2, 0.3],
            goal=[0.3, 0.2, 0.3])

        for joints in trajectory:
            self.sim.set_joint_positions(joints)
            contacts = self.sim.get_contacts()
            robot_contacts = [c for c in contacts
                            if 'robot' in c.body1 or 'robot' in c.body2]
            assert len(robot_contacts) == 0, \
                f"Robot collision detected: {robot_contacts}"
```

## CI/CD Pipeline for Robotics

```yaml
# .github/workflows/robotics_ci.yml
name: Robotics CI

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-22.04
    container:
      image: ros:humble-ros-base
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: |
          apt-get update
          rosdep install --from-paths src --ignore-src -y
          pip install pytest hypothesis numpy

      - name: Build
        run: |
          source /opt/ros/humble/setup.bash
          colcon build --packages-select my_pkg
          source install/setup.bash

      - name: Unit tests
        run: |
          source install/setup.bash
          colcon test --packages-select my_pkg
          colcon test-result --verbose

  integration-tests:
    runs-on: ubuntu-22.04
    container:
      image: ros:humble-ros-base
    needs: unit-tests
    steps:
      - uses: actions/checkout@v4

      - name: Build full workspace
        run: |
          source /opt/ros/humble/setup.bash
          colcon build

      - name: Integration tests
        run: |
          source install/setup.bash
          launch_test src/my_pkg/test/test_integration.py

  simulation-tests:
    runs-on: ubuntu-22.04
    needs: integration-tests
    steps:
      - uses: actions/checkout@v4

      - name: Setup MuJoCo
        run: pip install mujoco

      - name: Simulation tests
        run: pytest tests/simulation/ -v --timeout=120
```

## Testing Anti-Patterns

### 1. Testing with `sleep()`
```python
# BAD: Flaky, slow, non-deterministic
def test_message_received():
    pub.publish(msg)
    time.sleep(2.0)  # Hope it arrives!
    assert received

# GOOD: Event-driven waiting with timeout
def test_message_received():
    pub.publish(msg)
    event = threading.Event()
    sub = create_sub(callback=lambda m: event.set())
    assert event.wait(timeout=5.0), "Message not received within timeout"
```

### 2. Not Testing Failure Cases
```python
# BAD: Only test the happy path

# GOOD: Test failures explicitly
def test_planner_unreachable_goal(self):
    """Planner should return None for unreachable goals"""
    result = planner.plan(start, unreachable_goal)
    assert result is None

def test_perception_no_objects(self):
    """Perception should return empty list when no objects visible"""
    empty_image = np.zeros((256, 256, 3), dtype=np.uint8)
    detections = perception.detect(empty_image)
    assert detections == []
```

### 3. Non-Deterministic Tests
```python
# BAD: Random seed changes between runs
trajectory = planner.plan(start, goal)  # Uses random sampling internally

# GOOD: Fix random seed for reproducibility
def test_rrt_planner(self):
    np.random.seed(42)
    trajectory = planner.plan(start, goal, seed=42)
    assert len(trajectory) > 0
```
