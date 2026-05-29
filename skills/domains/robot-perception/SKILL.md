---
name: robot-perception
description: >
  Comprehensive best practices for robot perception systems covering cameras, LiDARs, depth sensors,
  IMUs, and multi-sensor setups. Use this skill when working with RGB image processing, depth maps,
  point clouds, sensor calibration (intrinsic, extrinsic, hand-eye), object detection, semantic
  segmentation, 3D reconstruction, visual servoing, or perception pipeline optimization. Trigger
  whenever the user mentions OpenCV, Open3D, PCL, RealSense, ZED, OAK-D, camera calibration,
  AprilTags, ArUco markers, stereo vision, RGBD, point cloud filtering, ICP registration, coordinate
  transforms, camera intrinsics, distortion correction, image undistortion, sensor streaming,
  frame synchronization, or any computer vision task in a robotics context. Also covers multi-camera
  rigs, time synchronization across sensors, perception latency budgets, and production deployment
  of perception pipelines.
---

# Robot Perception Skill

## When to Use This Skill
- Setting up and configuring camera, LiDAR, or depth sensors
- Building RGB, depth, or point cloud processing pipelines
- Calibrating cameras (intrinsic, extrinsic, hand-eye)
- Implementing object detection, segmentation, or tracking for robots
- Fusing data from multiple sensor modalities
- Streaming sensor data with proper threading and buffering
- Synchronizing multi-sensor rigs
- Deploying perception models on robot hardware (GPU, edge)
- Debugging perception failures (latency, dropped frames, misalignment)

## Sensor Landscape

### Sensor Types and Characteristics

```
Sensor Type        Output              Range       Rate     Best For
─────────────────────────────────────────────────────────────────────────
RGB Camera         (H,W,3) uint8       ∞           30-120Hz Object detection, tracking, visual servoing
Stereo Camera      (H,W,3)+(H,W,3)    0.3-20m     30-90Hz  Dense depth from passive stereo
Structured Light   (H,W) float + RGB   0.2-10m     30Hz     Indoor manipulation, short range
ToF Depth          (H,W) float + RGB   0.1-10m     30Hz     Indoor, medium range
LiDAR (spinning)   (N,3) or (N,4)     0.5-200m    10-20Hz  Outdoor navigation, mapping
LiDAR (solid-st.)  (N,3)              0.5-200m    10-30Hz  Automotive, outdoor
IMU                (6,) or (9,)        N/A         200-1kHz Orientation, motion estimation
Force/Torque       (6,) float          N/A         1kHz+    Contact detection, force control
Tactile            (H,W) or (N,3)      Contact     30-100Hz Grasp quality, texture
Event Camera       Events (x,y,t,p)    ∞           μs       High-speed tracking, HDR scenes
```

### Common Sensor Hardware

```
Device             Type               SDK/Driver           ROS2 Package
──────────────────────────────────────────────────────────────────────────
Intel RealSense    Structured Light   pyrealsense2         realsense2_camera
Stereolabs ZED     Stereo + IMU       pyzed                zed_wrapper
Luxonis OAK-D      Stereo + Neural    depthai              depthai_ros
FLIR/Basler        Industrial RGB     PySpin/pypylon       spinnaker_camera_driver
Velodyne           Spinning LiDAR     velodyne_driver      velodyne
Ouster             Spinning LiDAR     ouster-sdk           ros2_ouster
Livox              Solid-state LiDAR  livox_sdk            livox_ros2_driver
USB Webcam         RGB                OpenCV VideoCapture  usb_cam / v4l2_camera
```

## Camera Models and Calibration

### Pinhole Camera Model

```
                    3D World Point (X, Y, Z)
                           |
                    [R | t] — Extrinsic (world → camera)
                           |
                    Camera Point (Xc, Yc, Zc)
                           |
                    K — Intrinsic (camera → pixel)
                           |
                    Pixel (u, v)

K = [ fx   0   cx ]      fx, fy = focal lengths (pixels)
    [  0  fy   cy ]      cx, cy = principal point
    [  0   0    1 ]

Projection:  [u, v, 1]^T = K @ [R | t] @ [X, Y, Z, 1]^T
```

### Intrinsic Calibration

```python
import cv2
import numpy as np
from pathlib import Path

class IntrinsicCalibrator:
    """Camera intrinsic calibration using checkerboard pattern"""

    def __init__(self, board_size=(9, 6), square_size_m=0.025):
        self.board_size = board_size
        self.square_size = square_size_m

        # Prepare object points (3D coordinates of checkerboard corners)
        self.objp = np.zeros((board_size[0] * board_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[
            0:board_size[0], 0:board_size[1]
        ].T.reshape(-1, 2) * square_size_m

    def collect_calibration_images(self, camera, num_images=30,
                                    min_coverage=0.6):
        """Collect calibration images with good spatial coverage.

        IMPORTANT: Move the board to cover all regions of the image,
        including corners and edges. Tilt the board at various angles.
        Bad coverage = bad calibration, especially at image edges.
        """
        obj_points = []
        img_points = []
        coverage_map = np.zeros((4, 4), dtype=int)  # Track board positions

        while len(obj_points) < num_images:
            frame = camera.capture()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            found, corners = cv2.findChessboardCorners(
                gray, self.board_size,
                cv2.CALIB_CB_ADAPTIVE_THRESH |
                cv2.CALIB_CB_NORMALIZE_IMAGE |
                cv2.CALIB_CB_FAST_CHECK
            )

            if found:
                # Sub-pixel refinement — critical for accuracy
                criteria = (cv2.TERM_CRITERIA_EPS +
                           cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                corners = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1), criteria)

                # Track coverage
                center = corners.mean(axis=0).flatten()
                grid_x = int(center[0] / gray.shape[1] * 4)
                grid_y = int(center[1] / gray.shape[0] * 4)
                grid_x = min(grid_x, 3)
                grid_y = min(grid_y, 3)
                coverage_map[grid_y, grid_x] += 1

                obj_points.append(self.objp)
                img_points.append(corners)

        coverage = (coverage_map > 0).sum() / coverage_map.size
        if coverage < min_coverage:
            print(f"WARNING: Only {coverage:.0%} coverage. "
                  f"Move board to uncovered regions.")

        return obj_points, img_points, gray.shape[::-1]

    def calibrate(self, obj_points, img_points, image_size):
        """Run calibration and return camera matrix + distortion coeffs"""
        ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
            obj_points, img_points, image_size, None, None)

        if ret > 1.0:
            print(f"WARNING: High reprojection error ({ret:.3f} px). "
                  f"Check image quality and board detection.")

        # Compute per-image reprojection errors
        errors = []
        for i in range(len(obj_points)):
            projected, _ = cv2.projectPoints(
                obj_points[i], rvecs[i], tvecs[i], K, dist)
            err = cv2.norm(img_points[i], projected, cv2.NORM_L2)
            err /= len(projected)
            errors.append(err)

        print(f"Calibration complete:")
        print(f"  RMS reprojection error: {ret:.4f} px")
        print(f"  Per-image errors: mean={np.mean(errors):.4f}, "
              f"max={np.max(errors):.4f}")
        print(f"  Focal length: fx={K[0,0]:.1f}, fy={K[1,1]:.1f}")
        print(f"  Principal point: cx={K[0,2]:.1f}, cy={K[1,2]:.1f}")

        return CalibrationResult(
            camera_matrix=K, dist_coeffs=dist,
            rms_error=ret, image_size=image_size)

    def save(self, result, path):
        """Save calibration to YAML (OpenCV-compatible format)"""
        fs = cv2.FileStorage(str(path), cv2.FILE_STORAGE_WRITE)
        fs.write("camera_matrix", result.camera_matrix)
        fs.write("dist_coeffs", result.dist_coeffs)
        fs.write("image_width", result.image_size[0])
        fs.write("image_height", result.image_size[1])
        fs.write("rms_error", result.rms_error)
        fs.release()

    @staticmethod
    def load(path):
        """Load calibration from YAML"""
        fs = cv2.FileStorage(str(path), cv2.FILE_STORAGE_READ)
        K = fs.getNode("camera_matrix").mat()
        dist = fs.getNode("dist_coeffs").mat()
        w = int(fs.getNode("image_width").real())
        h = int(fs.getNode("image_height").real())
        fs.release()
        return CalibrationResult(
            camera_matrix=K, dist_coeffs=dist,
            image_size=(w, h), rms_error=0.0)
```

### Extrinsic Calibration (Camera-to-Camera, Camera-to-LiDAR)

```python
class ExtrinsicCalibrator:
    """Compute transform between two sensors using shared targets"""

    def calibrate_stereo(self, calib_left, calib_right,
                          obj_points, img_points_left, img_points_right,
                          image_size):
        """Stereo calibration: find relative pose between two cameras"""
        ret, K1, d1, K2, d2, R, T, E, F = cv2.stereoCalibrate(
            obj_points, img_points_left, img_points_right,
            calib_left.camera_matrix, calib_left.dist_coeffs,
            calib_right.camera_matrix, calib_right.dist_coeffs,
            image_size,
            flags=cv2.CALIB_FIX_INTRINSIC  # Use pre-calibrated intrinsics
        )

        print(f"Stereo calibration RMS: {ret:.4f} px")
        print(f"Baseline: {np.linalg.norm(T):.4f} m")

        return StereoCalibration(R=R, T=T, E=E, F=F, rms_error=ret)

    def calibrate_camera_to_lidar(self, camera_points_2d,
                                    lidar_points_3d, K, dist):
        """Find camera-to-LiDAR transform using corresponding points.

        Use a calibration target visible to both sensors (e.g.,
        checkerboard with reflective tape corners).
        """
        # PnP: find pose of 3D points relative to camera
        success, rvec, tvec = cv2.solvePnP(
            lidar_points_3d, camera_points_2d, K, dist,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            raise CalibrationError("PnP failed — check point correspondences")

        R, _ = cv2.Rodrigues(rvec)
        T_camera_lidar = np.eye(4)
        T_camera_lidar[:3, :3] = R
        T_camera_lidar[:3, 3] = tvec.flatten()

        # Verify by reprojecting
        projected, _ = cv2.projectPoints(
            lidar_points_3d, rvec, tvec, K, dist)
        error = np.mean(np.linalg.norm(
            camera_points_2d - projected.reshape(-1, 2), axis=1))
        print(f"Camera-LiDAR reprojection error: {error:.2f} px")

        return T_camera_lidar
```

### Hand-Eye Calibration (Camera-to-Robot)

```python
class HandEyeCalibrator:
    """Solve AX = XB for camera mounted on robot end-effector (eye-in-hand)
    or camera mounted on a fixed base (eye-to-hand).

    Requires moving the robot to multiple poses while observing a
    fixed calibration target.
    """

    def __init__(self, K, dist, board_size=(9, 6), square_size=0.025):
        self.K = K
        self.dist = dist
        self.board_size = board_size
        self.square_size = square_size
        self.objp = np.zeros((board_size[0] * board_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[
            0:board_size[0], 0:board_size[1]
        ].T.reshape(-1, 2) * square_size

    def collect_poses(self, camera, robot, num_poses=20):
        """Collect camera-target and robot poses at multiple configurations.

        IMPORTANT: Move to diverse robot orientations. At least 3 different
        rotation axes. Pure translations are NOT sufficient.
        """
        R_gripper2base = []
        t_gripper2base = []
        R_target2cam = []
        t_target2cam = []

        for i in range(num_poses):
            input(f"Move robot to pose {i+1}/{num_poses}, press Enter...")

            # Get robot end-effector pose
            ee_pose = robot.get_ee_pose()  # 4x4 homogeneous matrix
            R_gripper2base.append(ee_pose[:3, :3])
            t_gripper2base.append(ee_pose[:3, 3])

            # Detect calibration target in camera
            frame = camera.capture()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            found, corners = cv2.findChessboardCorners(
                gray, self.board_size, None)

            if not found:
                print(f"  Board not detected at pose {i+1}, skip.")
                continue

            corners = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1),
                (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))

            ret, rvec, tvec = cv2.solvePnP(
                self.objp, corners, self.K, self.dist)
            R, _ = cv2.Rodrigues(rvec)
            R_target2cam.append(R)
            t_target2cam.append(tvec.flatten())

        return (R_gripper2base, t_gripper2base,
                R_target2cam, t_target2cam)

    def calibrate_eye_in_hand(self, R_g2b, t_g2b, R_t2c, t_t2c):
        """Eye-in-hand: camera mounted on end-effector.
        Solves for T_camera_to_gripper."""
        R, t = cv2.calibrateHandEye(
            R_g2b, t_g2b, R_t2c, t_t2c,
            method=cv2.CALIB_HAND_EYE_TSAI  # Also: PARK, HORAUD, DANIILIDIS
        )
        T_cam2gripper = np.eye(4)
        T_cam2gripper[:3, :3] = R
        T_cam2gripper[:3, 3] = t.flatten()
        return T_cam2gripper

    def calibrate_eye_to_hand(self, R_g2b, t_g2b, R_t2c, t_t2c):
        """Eye-to-hand: camera fixed in workspace.
        Solves for T_camera_to_base."""
        # Invert robot poses (base-to-gripper → gripper-to-base)
        R_b2g = [R.T for R in R_g2b]
        t_b2g = [-R.T @ t for R, t in zip(R_g2b, t_g2b)]

        R, t = cv2.calibrateHandEye(
            R_b2g, t_b2g, R_t2c, t_t2c,
            method=cv2.CALIB_HAND_EYE_TSAI
        )
        T_cam2base = np.eye(4)
        T_cam2base[:3, :3] = R
        T_cam2base[:3, 3] = t.flatten()
        return T_cam2base

    def verify_calibration(self, T_cam2ee, robot, camera, target_points_3d):
        """Verify by projecting a known 3D point through the full chain.
        Error should be < 5mm for manipulation tasks."""
        ee_pose = robot.get_ee_pose()
        T_cam2base = ee_pose @ T_cam2ee

        # Project world point to camera
        point_in_cam = np.linalg.inv(T_cam2base) @ np.append(
            target_points_3d[0], 1.0)
        projected, _ = cv2.projectPoints(
            point_in_cam[:3].reshape(1, 3),
            np.zeros(3), np.zeros(3), self.K, self.dist)

        print(f"Verification projection: {projected.flatten()}")
        return projected.flatten()
```

### Calibration Quality Checklist

```
✅ Intrinsic calibration:
   - RMS reprojection error < 0.5 px (good), < 0.3 px (excellent)
   - ≥ 20 images with board covering full image area (corners + edges)
   - Board tilted at multiple angles (not just fronto-parallel)
   - Fixed focus / fixed zoom during calibration AND operation

✅ Extrinsic calibration (stereo / camera-LiDAR):
   - RMS < 1.0 px for stereo
   - Reprojection error < 3 px for camera-LiDAR
   - Verified with independent measurement (ruler / known distance)

✅ Hand-eye calibration:
   - ≥ 15 poses with diverse orientations (≥ 3 rotation axes)
   - Verification error < 5mm for manipulation, < 10mm for navigation
   - Robot repeatability accounted for (UR5 ≈ ±0.03mm, low-cost ≈ ±1mm)

⚠️  Recalibrate when:
   - Camera is physically bumped or remounted
   - Lens focus or zoom is changed
   - Temperature changes significantly (thermal expansion shifts intrinsics)
   - Robot is re-homed or joints are recalibrated
```

## Sensor Streaming Best Practices

### Camera Streaming Architecture

```python
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Optional
import numpy as np

@dataclass
class StampedFrame:
    """Frame with capture timestamp for synchronization"""
    data: np.ndarray
    timestamp: float          # time.monotonic() at capture
    sequence: int             # Frame counter
    sensor_id: str

class CameraStream:
    """Thread-safe camera streaming with bounded buffer.

    Design principles:
    1. Capture runs in a dedicated thread at sensor rate
    2. Processing never blocks capture
    3. Always use the LATEST frame (drop old ones for real-time)
    4. Timestamp at capture, not at processing time
    """

    def __init__(self, camera, buffer_size=2, name="camera"):
        self.camera = camera
        self.name = name
        self._buffer = deque(maxlen=buffer_size)
        self._lock = threading.Lock()
        self._new_frame = threading.Event()
        self._running = False
        self._sequence = 0
        self._thread = None

        # Diagnostics
        self._capture_times = deque(maxlen=100)
        self._drop_count = 0

    def start(self):
        """Start capture thread"""
        self._running = True
        self._thread = threading.Thread(
            target=self._capture_loop, daemon=True, name=f"{self.name}_capture")
        self._thread.start()

    def stop(self):
        """Stop capture thread"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)

    def _capture_loop(self):
        while self._running:
            t_start = time.monotonic()

            try:
                raw = self.camera.capture()
                timestamp = time.monotonic()  # Timestamp AFTER capture

                frame = StampedFrame(
                    data=raw,
                    timestamp=timestamp,
                    sequence=self._sequence,
                    sensor_id=self.name
                )
                self._sequence += 1

                with self._lock:
                    if len(self._buffer) == self._buffer.maxlen:
                        self._drop_count += 1
                    self._buffer.append(frame)

                self._new_frame.set()
                self._capture_times.append(time.monotonic() - t_start)

            except Exception as e:
                print(f"[{self.name}] Capture error: {e}")
                time.sleep(0.01)  # Back off on error

    def get_latest(self) -> Optional[StampedFrame]:
        """Get most recent frame (non-blocking). Returns None if empty."""
        with self._lock:
            if self._buffer:
                return self._buffer[-1]
        return None

    def wait_for_frame(self, timeout=1.0) -> Optional[StampedFrame]:
        """Block until a new frame arrives"""
        self._new_frame.clear()
        if self._new_frame.wait(timeout=timeout):
            return self.get_latest()
        return None

    def get_diagnostics(self) -> dict:
        """Streaming health metrics"""
        if self._capture_times:
            times = list(self._capture_times)
            fps = 1.0 / np.mean(times) if np.mean(times) > 0 else 0
        else:
            fps = 0
        return {
            "sensor": self.name,
            "fps": round(fps, 1),
            "frames_captured": self._sequence,
            "frames_dropped": self._drop_count,
            "buffer_size": len(self._buffer),
            "avg_capture_ms": round(np.mean(times) * 1000, 1) if self._capture_times else 0,
        }
```

### Multi-Sensor Synchronization

```python
class SyncedMultiSensor:
    """Synchronize frames from multiple sensors by timestamp.

    Uses nearest-neighbor matching within a time tolerance.
    For hardware-synced sensors, use hardware trigger instead.
    """

    def __init__(self, sensors: dict, max_time_diff_ms=33):
        """
        Args:
            sensors: {"rgb": CameraStream, "depth": CameraStream, ...}
            max_time_diff_ms: Maximum allowed time difference between
                              synced frames. Default 33ms (1 frame at 30Hz).
        """
        self.sensors = sensors
        self.max_dt = max_time_diff_ms / 1000.0
        self._synced_callback = None

    def start(self):
        for s in self.sensors.values():
            s.start()

    def stop(self):
        for s in self.sensors.values():
            s.stop()

    def get_synced(self) -> Optional[dict]:
        """Get time-synchronized frames from all sensors.
        Returns None if any sensor is missing or too far out of sync."""
        frames = {}
        for name, stream in self.sensors.items():
            frame = stream.get_latest()
            if frame is None:
                return None
            frames[name] = frame

        # Check time alignment against the first sensor
        ref_time = list(frames.values())[0].timestamp
        for name, frame in frames.items():
            dt = abs(frame.timestamp - ref_time)
            if dt > self.max_dt:
                return None  # Out of sync

        return frames

    def get_synced_interpolated(self) -> Optional[dict]:
        """For sensors at different rates, interpolate to common timestamp.
        Useful for IMU + camera fusion."""
        # Get latest from each sensor
        frames = {}
        for name, stream in self.sensors.items():
            frame = stream.get_latest()
            if frame is None:
                return None
            frames[name] = frame

        # Use the SLOWEST sensor's timestamp as reference
        ref_time = min(f.timestamp for f in frames.values())

        result = {}
        for name, frame in frames.items():
            dt = frame.timestamp - ref_time
            if abs(dt) <= self.max_dt:
                result[name] = frame
            # For high-rate sensors (IMU), could interpolate here

        return result if len(result) == len(self.sensors) else None
```

### Hardware-Triggered Synchronization

```python
class HardwareSyncConfig:
    """Configure hardware trigger for multi-camera synchronization.

    ALWAYS prefer hardware sync over software sync for:
    - Stereo depth computation
    - Multi-camera 3D reconstruction
    - Fast-moving scenes

    Common trigger methods:
    - GPIO pulse from microcontroller (Arduino, ESP32)
    - Camera's own sync output → other cameras' trigger input
    - PTP (Precision Time Protocol) for GigE cameras
    """

    @staticmethod
    def setup_realsense_sync(master_serial, slave_serials):
        """Configure RealSense hardware sync (Inter-Cam sync mode)"""
        import pyrealsense2 as rs

        # Master camera: generates sync signal
        master = rs.pipeline()
        master_cfg = rs.config()
        master_cfg.enable_device(master_serial)
        master_sensor = master.start(master_cfg)

        # Set master to mode 1 (master)
        depth_sensor = master_sensor.get_device().first_depth_sensor()
        depth_sensor.set_option(rs.option.inter_cam_sync_mode, 1)

        # Slave cameras: receive sync signal
        slaves = []
        for serial in slave_serials:
            pipe = rs.pipeline()
            cfg = rs.config()
            cfg.enable_device(serial)
            profile = pipe.start(cfg)
            sensor = profile.get_device().first_depth_sensor()
            sensor.set_option(rs.option.inter_cam_sync_mode, 2)  # Slave
            slaves.append(pipe)

        return master, slaves

    @staticmethod
    def setup_ptp_sync(camera_ips):
        """Enable PTP synchronization for GigE Vision cameras.

        Requires PTP-capable network switch.
        Achieves < 1μs sync accuracy.
        """
        # Example with Basler/pylon cameras
        # import pypylon.pylon as py
        #
        # for ip in camera_ips:
        #     cam = py.InstantCamera(py.TlFactory.GetInstance()
        #         .CreateDevice(py.CDeviceInfo().SetIpAddress(ip)))
        #     cam.Open()
        #     cam.GevIEEE1588.Value = True  # Enable PTP
        #     cam.Close()
        pass
```

### Streaming Anti-Patterns

```python
# ❌ BAD: Capture and process in same thread — limits to slowest operation
def bad_pipeline():
    while True:
        frame = camera.capture()           # 5ms
        detections = model.detect(frame)   # 100ms
        # Effective rate: ~9 FPS regardless of camera's 30 FPS

# ✅ GOOD: Decouple capture from processing
def good_pipeline():
    stream = CameraStream(camera)
    stream.start()
    while True:
        frame = stream.get_latest()        # Always latest, non-blocking
        if frame:
            detections = model.detect(frame.data)  # 100ms
            # Camera still capturing at 30 FPS in background
            # Processing at ~10 FPS but always on freshest frame


# ❌ BAD: Unbounded buffer — memory grows until OOM
buffer = []  # Will grow forever if consumer is slower than producer!

# ✅ GOOD: Bounded buffer with drop policy
buffer = deque(maxlen=2)  # Keep latest 2, drop old automatically


# ❌ BAD: Sleeping for frame timing
time.sleep(1.0 / 30)  # Drift accumulates, doesn't account for jitter

# ✅ GOOD: Event-driven or spin with wall clock
frame = stream.wait_for_frame(timeout=0.1)


# ❌ BAD: Timestamp at processing time
def process_callback(raw_data):
    timestamp = time.time()  # WRONG: includes queue delay + scheduling
    frame = decode(raw_data)
    publish(frame, timestamp)

# ✅ GOOD: Timestamp at capture time
def capture_thread():
    raw_data = sensor.read()
    timestamp = time.monotonic()  # RIGHT: timestamp at source
    queue.put((raw_data, timestamp))
```

## RGB Processing Pipelines

### Image Undistortion

```python
class ImageUndistorter:
    """Pre-compute undistortion maps for fast runtime correction.

    ALWAYS undistort before any geometric computation
    (pose estimation, 3D reconstruction, visual servoing).
    """

    def __init__(self, K, dist, image_size, alpha=0.0):
        """
        Args:
            alpha: 0.0 = crop all black pixels (default, recommended)
                   1.0 = keep all pixels (shows black borders)
        """
        self.new_K, self.roi = cv2.getOptimalNewCameraMatrix(
            K, dist, image_size, alpha, image_size)

        # Pre-compute maps (do this ONCE, not per frame)
        self.map1, self.map2 = cv2.initUndistortRectifyMap(
            K, dist, None, self.new_K, image_size, cv2.CV_16SC2)

    def undistort(self, image):
        """Apply undistortion using pre-computed maps (fast)"""
        return cv2.remap(image, self.map1, self.map2,
                         interpolation=cv2.INTER_LINEAR)

    def undistort_points(self, points_2d):
        """Undistort 2D point coordinates"""
        return cv2.undistortPoints(
            points_2d.reshape(-1, 1, 2).astype(np.float64),
            self.K, self.dist, P=self.new_K
        ).reshape(-1, 2)
```

### Object Detection Integration

```python
class RobotObjectDetector:
    """Object detection for robotic manipulation.

    Wraps a detection model with robotics-specific post-processing:
    - Workspace filtering (ignore detections outside robot reach)
    - Stability tracking (reject flickering detections)
    - 3D pose estimation from 2D detections + depth
    """

    def __init__(self, model, K, workspace_bounds=None, min_confidence=0.5):
        self.model = model
        self.K = K
        self.workspace_bounds = workspace_bounds
        self.min_confidence = min_confidence
        self.tracker = DetectionTracker(max_age=5, min_hits=3)

    def detect(self, rgb, depth=None) -> list:
        """Run detection with robotics post-processing"""
        # Raw detection
        raw_dets = self.model(rgb)

        # Filter by confidence
        dets = [d for d in raw_dets if d.confidence >= self.min_confidence]

        # Estimate 3D position if depth is available
        if depth is not None:
            for det in dets:
                det.position_3d = self._backproject(det.center, depth)

                # Filter by workspace
                if self.workspace_bounds and det.position_3d is not None:
                    if not self.workspace_bounds.contains(det.position_3d):
                        det.in_workspace = False
                        continue
                    det.in_workspace = True

        # Track across frames for stability
        tracked = self.tracker.update(dets)

        return tracked

    def _backproject(self, pixel, depth_image):
        """Convert 2D pixel + depth to 3D point in camera frame.

        This is the INVERSE of projection:
        X = (u - cx) * Z / fx
        Y = (v - cy) * Z / fy
        Z = depth
        """
        u, v = int(pixel[0]), int(pixel[1])

        # Sample depth with a small window (more robust than single pixel)
        h, w = depth_image.shape[:2]
        u = np.clip(u, 2, w - 3)
        v = np.clip(v, 2, h - 3)
        patch = depth_image[v-2:v+3, u-2:u+3]

        # Use median to reject outliers (holes, edges)
        valid = patch[patch > 0]
        if len(valid) == 0:
            return None
        Z = np.median(valid)

        # Convert from depth sensor units (often mm) to meters
        if Z > 100:  # Likely millimeters
            Z = Z / 1000.0

        fx, fy = self.K[0, 0], self.K[1, 1]
        cx, cy = self.K[0, 2], self.K[1, 2]

        X = (u - cx) * Z / fx
        Y = (v - cy) * Z / fy

        return np.array([X, Y, Z])
```

### Fiducial Marker Detection (AprilTag / ArUco)

```python
class FiducialDetector:
    """Detect and estimate pose of fiducial markers.

    Use cases:
    - Robot localization (known marker positions)
    - Object pose estimation (marker attached to object)
    - Calibration targets
    - Sim-to-real ground truth
    """

    def __init__(self, K, dist, marker_size_m=0.05,
                 dictionary=cv2.aruco.DICT_APRILTAG_36h11):
        self.K = K
        self.dist = dist
        self.marker_size = marker_size_m
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(dictionary)
        self.params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.params)

    def detect(self, image) -> list:
        """Detect markers and estimate their 6DOF poses"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = self.detector.detectMarkers(gray)

        results = []
        if ids is not None:
            for i, marker_id in enumerate(ids.flatten()):
                # Estimate pose (rotation + translation)
                rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                    corners[i:i+1], self.marker_size, self.K, self.dist)

                R, _ = cv2.Rodrigues(rvecs[0])
                T = np.eye(4)
                T[:3, :3] = R
                T[:3, 3] = tvecs[0].flatten()

                results.append(MarkerDetection(
                    marker_id=int(marker_id),
                    corners=corners[i].reshape(4, 2),
                    pose=T,
                    distance=np.linalg.norm(tvecs[0]),
                ))

        return results

    def draw(self, image, detections):
        """Visualize detected markers with axes"""
        vis = image.copy()
        for det in detections:
            cv2.aruco.drawDetectedMarkers(
                vis, [det.corners.reshape(1, 4, 2)],
                np.array([[det.marker_id]]))
            rvec, _ = cv2.Rodrigues(det.pose[:3, :3])
            cv2.drawFrameAxes(
                vis, self.K, self.dist, rvec,
                det.pose[:3, 3], self.marker_size * 0.5)
        return vis
```

### Semantic Segmentation for Manipulation

```python
class WorkspaceSegmenter:
    """Segment a robot's workspace into actionable regions.

    Common segmentation targets for manipulation:
    - Graspable objects vs background
    - Table / support surface
    - Robot body (for self-collision avoidance)
    - Free space vs obstacles
    """

    def __init__(self, model, class_map):
        self.model = model
        self.class_map = class_map  # {0: 'background', 1: 'table', 2: 'object', ...}

    def segment(self, rgb) -> SegmentationResult:
        """Run segmentation and extract per-class masks"""
        mask = self.model.predict(rgb)  # (H, W) with class IDs

        return SegmentationResult(
            full_mask=mask,
            object_mask=(mask == self.class_map['object']),
            table_mask=(mask == self.class_map['table']),
            free_space_mask=(mask == self.class_map['free_space']),
        )

    def get_grasp_candidates(self, rgb, depth, K):
        """Combine segmentation with depth to find graspable regions"""
        seg = self.segment(rgb)

        # Find connected components in object mask
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            seg.object_mask.astype(np.uint8))

        candidates = []
        for i in range(1, num_labels):  # Skip background (0)
            component_mask = (labels == i)
            area = stats[i, cv2.CC_STAT_AREA]

            if area < 100:  # Too small, likely noise
                continue

            # Get median depth of this object
            obj_depths = depth[component_mask]
            valid_depths = obj_depths[obj_depths > 0]
            if len(valid_depths) == 0:
                continue

            center_px = centroids[i]
            median_depth = np.median(valid_depths)

            # Backproject center to 3D
            fx, fy = K[0, 0], K[1, 1]
            cx, cy = K[0, 2], K[1, 2]
            X = (center_px[0] - cx) * median_depth / fx
            Y = (center_px[1] - cy) * median_depth / fy

            candidates.append(GraspCandidate(
                position_3d=np.array([X, Y, median_depth]),
                pixel_center=center_px,
                mask=component_mask,
                area_pixels=area,
            ))

        return candidates
```

## Depth Processing

### Depth Map Filtering and Cleanup

```python
class DepthProcessor:
    """Clean up raw depth maps for downstream use.

    Raw depth from sensors is noisy: holes, flying pixels at edges,
    multi-path interference, and range noise. Always filter before use.
    """

    def __init__(self, depth_scale=0.001, min_depth_m=0.1, max_depth_m=3.0):
        self.depth_scale = depth_scale  # Raw units to meters
        self.min_depth = min_depth_m
        self.max_depth = max_depth_m

    def process(self, raw_depth) -> np.ndarray:
        """Full depth cleanup pipeline"""
        depth = raw_depth.astype(np.float32) * self.depth_scale

        # 1. Range filtering
        depth[(depth < self.min_depth) | (depth > self.max_depth)] = 0

        # 2. Edge filtering — remove flying pixels at depth discontinuities
        depth = self._remove_flying_pixels(depth)

        # 3. Hole filling — fill small holes via inpainting
        depth = self._fill_holes(depth, max_hole_size=10)

        # 4. Spatial smoothing — bilateral filter preserves edges
        depth = self._bilateral_filter(depth)

        return depth

    def _remove_flying_pixels(self, depth, threshold=0.05):
        """Remove pixels at depth discontinuities (flying pixels).
        These are artifacts where the sensor interpolates between
        foreground and background."""
        dx = np.abs(np.diff(depth, axis=1, prepend=0))
        dy = np.abs(np.diff(depth, axis=0, prepend=0))
        gradient = np.sqrt(dx**2 + dy**2)
        depth[gradient > threshold] = 0
        return depth

    def _fill_holes(self, depth, max_hole_size=10):
        """Fill small holes using inpainting. Large holes remain as 0."""
        mask = (depth == 0).astype(np.uint8)

        # Only fill small holes
        kernel = np.ones((max_hole_size, max_hole_size), np.uint8)
        small_holes = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        small_holes = small_holes & mask

        if small_holes.any():
            # Normalize depth to uint16 for inpainting
            d_norm = (depth * 1000).astype(np.uint16)
            filled = cv2.inpaint(
                d_norm, small_holes, max_hole_size, cv2.INPAINT_NS)
            depth = np.where(small_holes, filled.astype(np.float32) / 1000, depth)

        return depth

    def _bilateral_filter(self, depth, d=5, sigma_color=0.02, sigma_space=5):
        """Bilateral filter: smooths noise while preserving depth edges"""
        # Convert to uint16 for cv2 bilateral (doesn't support float)
        d_uint16 = (depth * 10000).astype(np.uint16)
        filtered = cv2.bilateralFilter(d_uint16, d,
                                        sigma_color * 10000, sigma_space)
        return filtered.astype(np.float32) / 10000
```

### Depth-to-Point Cloud Conversion

```python
class DepthToPointCloud:
    """Convert depth images to organized and unorganized point clouds."""

    def __init__(self, K, image_size):
        self.K = K
        # Pre-compute pixel coordinate grid (do once, reuse every frame)
        h, w = image_size[1], image_size[0]
        u_coords, v_coords = np.meshgrid(np.arange(w), np.arange(h))
        self.u = u_coords.astype(np.float32)
        self.v = v_coords.astype(np.float32)
        self.fx, self.fy = K[0, 0], K[1, 1]
        self.cx, self.cy = K[0, 2], K[1, 2]

    def convert(self, depth, rgb=None) -> np.ndarray:
        """Convert depth image to point cloud.

        Returns:
            points: (N, 3) or (N, 6) if rgb provided [x, y, z, r, g, b]
        """
        # Backproject all pixels in parallel (vectorized)
        Z = depth.astype(np.float32)
        X = (self.u - self.cx) * Z / self.fx
        Y = (self.v - self.cy) * Z / self.fy

        # Stack into (H, W, 3) organized point cloud
        points = np.stack([X, Y, Z], axis=-1)

        # Filter invalid points
        valid_mask = Z > 0
        points_valid = points[valid_mask]

        if rgb is not None:
            colors = rgb[valid_mask].astype(np.float32) / 255.0
            return np.hstack([points_valid, colors])

        return points_valid

    def convert_organized(self, depth, rgb=None):
        """Return organized point cloud (H, W, 3) — preserves pixel layout.
        Invalid points are NaN."""
        Z = depth.astype(np.float32)
        X = (self.u - self.cx) * Z / self.fx
        Y = (self.v - self.cy) * Z / self.fy

        organized = np.stack([X, Y, Z], axis=-1)
        organized[depth == 0] = np.nan

        return organized
```

### RGBD Alignment

```python
class RGBDAligner:
    """Align RGB and depth images from different sensors.

    Most RGBD sensors (RealSense, ZED) provide built-in alignment.
    Use this when combining separate RGB + depth cameras.
    """

    def __init__(self, K_rgb, K_depth, T_depth_to_rgb, rgb_size, depth_size):
        self.K_rgb = K_rgb
        self.K_depth = K_depth
        self.T = T_depth_to_rgb  # 4x4 transform: depth frame → rgb frame
        self.rgb_size = rgb_size
        self.depth_size = depth_size

    def align_depth_to_rgb(self, depth):
        """Reproject depth image into RGB camera's frame.

        For each pixel in depth image:
        1. Backproject to 3D using depth intrinsics
        2. Transform to RGB camera frame
        3. Project to RGB pixel using RGB intrinsics
        """
        h_d, w_d = depth.shape
        h_r, w_r = self.rgb_size[1], self.rgb_size[0]
        aligned = np.zeros((h_r, w_r), dtype=np.float32)

        # Backproject depth pixels to 3D
        v_d, u_d = np.mgrid[0:h_d, 0:w_d].astype(np.float32)
        Z = depth.astype(np.float32)
        valid = Z > 0

        X = (u_d[valid] - self.K_depth[0, 2]) * Z[valid] / self.K_depth[0, 0]
        Y = (v_d[valid] - self.K_depth[1, 2]) * Z[valid] / self.K_depth[1, 1]
        pts_3d = np.stack([X, Y, Z[valid], np.ones_like(X)], axis=0)

        # Transform to RGB frame
        pts_rgb = self.T @ pts_3d

        # Project to RGB pixels
        u_r = (self.K_rgb[0, 0] * pts_rgb[0] / pts_rgb[2] +
               self.K_rgb[0, 2]).astype(int)
        v_r = (self.K_rgb[1, 1] * pts_rgb[1] / pts_rgb[2] +
               self.K_rgb[1, 2]).astype(int)

        # Fill aligned depth (z-buffer for occlusion handling)
        in_bounds = (u_r >= 0) & (u_r < w_r) & (v_r >= 0) & (v_r < h_r)
        for u, v, z in zip(u_r[in_bounds], v_r[in_bounds],
                           pts_rgb[2][in_bounds]):
            if aligned[v, u] == 0 or z < aligned[v, u]:
                aligned[v, u] = z

        return aligned
```

## Point Cloud Processing

### Filtering and Downsampling

```python
import open3d as o3d

class PointCloudProcessor:
    """Point cloud processing pipeline using Open3D.

    Pipeline order matters:
    1. Crop to region of interest (reduces data volume first)
    2. Remove statistical outliers
    3. Downsample (voxel grid)
    4. Estimate normals
    5. Application-specific processing
    """

    def preprocess(self, points, colors=None,
                   workspace_bounds=None, voxel_size=0.005):
        """Standard preprocessing pipeline"""
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points[:, :3])
        if colors is not None:
            pcd.colors = o3d.utility.Vector3dVector(colors)

        # 1. Crop to workspace
        if workspace_bounds:
            bbox = o3d.geometry.AxisAlignedBoundingBox(
                min_bound=workspace_bounds['min'],
                max_bound=workspace_bounds['max'])
            pcd = pcd.crop(bbox)

        # 2. Statistical outlier removal
        pcd, inlier_idx = pcd.remove_statistical_outlier(
            nb_neighbors=20, std_ratio=2.0)

        # 3. Voxel downsampling
        pcd = pcd.voxel_down_sample(voxel_size=voxel_size)

        # 4. Normal estimation
        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(
                radius=voxel_size * 4, max_nn=30))
        # Orient normals toward camera
        pcd.orient_normals_towards_camera_location(
            camera_location=np.array([0, 0, 0]))

        return pcd

    def segment_plane(self, pcd, distance_threshold=0.005,
                      ransac_n=3, num_iterations=1000):
        """Segment the dominant plane (table / floor) using RANSAC.
        Returns plane model and inlier/outlier point clouds."""
        plane_model, inliers = pcd.segment_plane(
            distance_threshold=distance_threshold,
            ransac_n=ransac_n,
            num_iterations=num_iterations)

        plane_cloud = pcd.select_by_index(inliers)
        objects_cloud = pcd.select_by_index(inliers, invert=True)

        a, b, c, d = plane_model
        print(f"Plane: {a:.3f}x + {b:.3f}y + {c:.3f}z + {d:.3f} = 0")

        return plane_model, plane_cloud, objects_cloud

    def cluster_objects(self, pcd, eps=0.02, min_points=50):
        """Cluster point cloud into individual objects using DBSCAN"""
        labels = np.array(pcd.cluster_dbscan(
            eps=eps, min_points=min_points, print_progress=False))

        clusters = []
        for label_id in range(labels.max() + 1):
            cluster_mask = labels == label_id
            cluster_pcd = pcd.select_by_index(
                np.where(cluster_mask)[0])

            bbox = cluster_pcd.get_axis_aligned_bounding_box()
            center = bbox.get_center()
            extent = bbox.get_extent()

            clusters.append(PointCloudCluster(
                cloud=cluster_pcd,
                centroid=center,
                extent=extent,
                num_points=cluster_mask.sum(),
                bbox=bbox,
            ))

        # Sort by size (largest first)
        clusters.sort(key=lambda c: c.num_points, reverse=True)
        return clusters
```

### Point Cloud Registration (ICP)

```python
class PointCloudRegistration:
    """Align two point clouds using ICP and its variants.

    Use cases:
    - Multi-view reconstruction (combine views from different poses)
    - Object model matching (align scan to CAD model)
    - LiDAR odometry (align consecutive scans)
    - Bin picking (match object template to scene)
    """

    def align_icp(self, source, target, initial_transform=np.eye(4),
                  max_distance=0.05, method='point_to_plane'):
        """Iterative Closest Point alignment.

        Args:
            source: point cloud to align
            target: reference point cloud
            initial_transform: starting guess (CRITICAL for convergence)
            max_distance: max correspondence distance
            method: 'point_to_point' or 'point_to_plane'
        """
        if method == 'point_to_plane':
            # Point-to-plane converges faster but needs normals
            if not target.has_normals():
                target.estimate_normals(
                    search_param=o3d.geometry.KDTreeSearchParamHybrid(
                        radius=0.05, max_nn=30))
            estimation = o3d.pipelines.registration.TransformationEstimationPointToPlane()
        else:
            estimation = o3d.pipelines.registration.TransformationEstimationPointToPoint()

        result = o3d.pipelines.registration.registration_icp(
            source, target, max_distance, initial_transform,
            estimation,
            o3d.pipelines.registration.ICPConvergenceCriteria(
                max_iteration=100,
                relative_fitness=1e-6,
                relative_rmse=1e-6))

        print(f"ICP fitness: {result.fitness:.4f}, "
              f"RMSE: {result.inlier_rmse:.6f}")

        if result.fitness < 0.3:
            print("WARNING: Low fitness — ICP likely failed. "
                  "Check initial alignment or increase max_distance.")

        return result.transformation, result

    def align_global(self, source, target, voxel_size=0.01):
        """Global registration (no initial guess needed).
        Use FPFH features + RANSAC for coarse alignment,
        then refine with ICP."""

        # Downsample for feature computation
        source_down = source.voxel_down_sample(voxel_size)
        target_down = target.voxel_down_sample(voxel_size)

        # Compute normals
        for pcd in [source_down, target_down]:
            pcd.estimate_normals(
                o3d.geometry.KDTreeSearchParamHybrid(
                    radius=voxel_size * 2, max_nn=30))

        # Compute FPFH features
        source_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
            source_down,
            o3d.geometry.KDTreeSearchParamHybrid(
                radius=voxel_size * 5, max_nn=100))
        target_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
            target_down,
            o3d.geometry.KDTreeSearchParamHybrid(
                radius=voxel_size * 5, max_nn=100))

        # RANSAC-based global registration
        coarse = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
            source_down, target_down, source_fpfh, target_fpfh,
            mutual_filter=True,
            max_correspondence_distance=voxel_size * 2,
            estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(),
            ransac_n=3,
            checkers=[
                o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
                o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(voxel_size * 2),
            ],
            criteria=o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))

        # Refine with ICP
        refined, _ = self.align_icp(
            source, target,
            initial_transform=coarse.transformation,
            max_distance=voxel_size * 1.5,
            method='point_to_plane')

        return refined
```

## Multi-Sensor Fusion

### Perception Fusion Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  RGB Camera  │    │ Depth Sensor │    │    LiDAR     │
│   30 Hz      │    │   30 Hz      │    │   10 Hz      │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Detection   │    │    Depth     │    │ Point Cloud  │
│  + Segment   │    │  Filtering   │    │  Processing  │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       └───────────┬───────┘───────────────────┘
                   ▼
          ┌────────────────┐
          │  Fusion Layer  │
          │  (association  │
          │   + tracking)  │
          └────────┬───────┘
                   ▼
          ┌────────────────┐
          │  World Model   │
          │  (tracked      │
          │   objects)     │
          └────────────────┘
```

### Camera + LiDAR Fusion

```python
class CameraLiDARFusion:
    """Project LiDAR points into camera image for cross-modal association.

    Two fusion strategies:
    1. Early fusion: Project LiDAR → camera, combine at data level
    2. Late fusion: Detect in each modality, associate results

    Early fusion is simpler and recommended when sensors are calibrated.
    """

    def __init__(self, K, T_lidar_to_camera, image_size):
        self.K = K
        self.T = T_lidar_to_camera  # 4x4 transform
        self.image_size = image_size  # (w, h)

    def project_lidar_to_image(self, lidar_points):
        """Project 3D LiDAR points to 2D image pixels.

        Returns:
            pixels: (N, 2) pixel coordinates
            depths: (N,) depth values
            valid_mask: (N,) bool — True if point projects into image
        """
        N = len(lidar_points)
        # Homogeneous coordinates
        pts_h = np.hstack([lidar_points[:, :3], np.ones((N, 1))])

        # Transform to camera frame
        pts_cam = (self.T @ pts_h.T).T

        # Points behind camera
        valid = pts_cam[:, 2] > 0
        depths = pts_cam[:, 2]

        # Project to pixels
        pixels = np.zeros((N, 2))
        pixels[:, 0] = self.K[0, 0] * pts_cam[:, 0] / pts_cam[:, 2] + self.K[0, 2]
        pixels[:, 1] = self.K[1, 1] * pts_cam[:, 1] / pts_cam[:, 2] + self.K[1, 2]

        # Check image bounds
        w, h = self.image_size
        valid &= (pixels[:, 0] >= 0) & (pixels[:, 0] < w)
        valid &= (pixels[:, 1] >= 0) & (pixels[:, 1] < h)

        return pixels, depths, valid

    def colorize_pointcloud(self, lidar_points, rgb_image):
        """Paint LiDAR points with RGB colors from camera image"""
        pixels, depths, valid = self.project_lidar_to_image(lidar_points)

        colors = np.zeros((len(lidar_points), 3), dtype=np.float32)
        valid_px = pixels[valid].astype(int)
        colors[valid] = rgb_image[valid_px[:, 1], valid_px[:, 0]] / 255.0

        return colors, valid

    def enrich_detections(self, detections_2d, lidar_points):
        """Add 3D information to 2D camera detections using LiDAR.

        For each 2D bounding box, find LiDAR points that project
        inside it, and compute the 3D centroid.
        """
        pixels, depths, valid = self.project_lidar_to_image(lidar_points)

        enriched = []
        for det in detections_2d:
            x1, y1, x2, y2 = det.bbox

            # Find LiDAR points inside this bounding box
            in_box = (valid &
                      (pixels[:, 0] >= x1) & (pixels[:, 0] <= x2) &
                      (pixels[:, 1] >= y1) & (pixels[:, 1] <= y2))

            if in_box.sum() > 3:
                # Use LiDAR points for 3D position (more accurate than depth camera)
                box_points = lidar_points[in_box]

                # Median is robust to outliers from other objects
                position_3d = np.median(box_points[:, :3], axis=0)
                det.position_3d = position_3d
                det.num_lidar_points = in_box.sum()
                det.has_3d = True
            else:
                det.has_3d = False

            enriched.append(det)

        return enriched
```

### Multi-Object Tracking

```python
class PerceptionTracker:
    """Track detected objects across frames for temporal consistency.

    Why tracking matters in robotics:
    - Detections flicker (present one frame, absent the next)
    - Robot needs consistent object IDs for manipulation
    - Velocity estimation requires temporal association
    - Occlusion handling prevents phantom disappearances
    """

    def __init__(self, max_age=5, min_hits=3, iou_threshold=0.3):
        self.max_age = max_age            # Frames before deleting lost track
        self.min_hits = min_hits          # Frames before confirming track
        self.iou_threshold = iou_threshold
        self.tracks = {}
        self.next_id = 0

    def update(self, detections) -> list:
        """Associate detections with existing tracks.

        Uses Hungarian algorithm for optimal assignment.
        """
        if not self.tracks:
            # First frame: create tracks for all detections
            for det in detections:
                self._create_track(det)
            return list(self.tracks.values())

        # Compute cost matrix (IoU for 2D, Euclidean for 3D)
        track_list = list(self.tracks.values())
        cost_matrix = self._compute_cost_matrix(track_list, detections)

        # Hungarian assignment
        from scipy.optimize import linear_sum_assignment
        row_idx, col_idx = linear_sum_assignment(cost_matrix)

        matched = set()
        for r, c in zip(row_idx, col_idx):
            if cost_matrix[r, c] < self.iou_threshold:
                track_list[r].update(detections[c])
                matched.add(c)

        # Create new tracks for unmatched detections
        for i, det in enumerate(detections):
            if i not in matched:
                self._create_track(det)

        # Age out old tracks
        stale = [tid for tid, t in self.tracks.items()
                 if t.age > self.max_age]
        for tid in stale:
            del self.tracks[tid]

        # Return confirmed tracks only
        return [t for t in self.tracks.values()
                if t.hits >= self.min_hits]

    def _create_track(self, detection):
        track = Track(
            track_id=self.next_id,
            detection=detection,
            hits=1, age=0)
        self.tracks[self.next_id] = track
        self.next_id += 1

    def _compute_cost_matrix(self, tracks, detections):
        n_tracks = len(tracks)
        n_dets = len(detections)
        cost = np.ones((n_tracks, n_dets))

        for i, track in enumerate(tracks):
            for j, det in enumerate(detections):
                if hasattr(det, 'position_3d') and det.position_3d is not None:
                    # 3D Euclidean distance (preferred)
                    dist = np.linalg.norm(
                        track.position_3d - det.position_3d)
                    cost[i, j] = dist
                else:
                    # 2D IoU
                    cost[i, j] = 1.0 - self._iou(track.bbox, det.bbox)

        return cost

    @staticmethod
    def _iou(box1, box2):
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])
        inter = max(0, x2 - x1) * max(0, y2 - y1)
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
        return inter / (area1 + area2 - inter + 1e-6)
```

## Perception Latency Budget

```
Component                   Typical Latency    Budget Target
───────────────────────────────────────────────────────────────
Sensor capture              1-10 ms            —
Image transfer (USB3)       2-5 ms             —
Undistortion                1-2 ms             < 3 ms
Detection (GPU)             10-50 ms           < 30 ms
Detection (CPU)             50-500 ms          < 100 ms
Depth processing            2-5 ms             < 5 ms
Point cloud generation      3-10 ms            < 10 ms
Segmentation (GPU)          15-40 ms           < 30 ms
Tracking update             0.5-2 ms           < 2 ms
3D pose estimation          5-20 ms            < 15 ms
───────────────────────────────────────────────────────────────
TOTAL PIPELINE              ~50-150 ms         < 100 ms target

For 10 Hz perception: budget = 100 ms per frame
For 30 Hz perception: budget = 33 ms per frame

RULE: Perception latency + planning latency < control period
      If control runs at 100 Hz (10 ms), perception must be
      pipelined — process frame N while control uses frame N-1.
```

## Perception Anti-Patterns

### 1. Processing Every Frame When You Don't Need To
```python
# ❌ BAD: Running heavy detection at sensor framerate
def callback(self, msg):
    detections = self.heavy_model(msg)  # 100ms on every 30Hz frame

# ✅ GOOD: Decimate or skip frames
def callback(self, msg):
    self.frame_count += 1
    if self.frame_count % 3 != 0:  # Process every 3rd frame
        return
    detections = self.heavy_model(msg)
```

### 2. Not Validating Depth Values
```python
# ❌ BAD: Using raw depth blindly
z = depth_image[v, u]
point_3d = backproject(u, v, z)  # z might be 0 (hole) or 65535 (invalid)

# ✅ GOOD: Always validate depth
z = depth_image[v, u]
if z <= 0 or z > max_range:
    return None
z_meters = z * depth_scale
```

### 3. Assuming Cameras Are Calibrated
```python
# ❌ BAD: Using default/nominal intrinsics
K = np.array([[600, 0, 320], [0, 600, 240], [0, 0, 1]])  # Guess

# ✅ GOOD: Load actual calibration
K = load_calibration("camera_serial_12345.yaml").camera_matrix
```

### 4. Ignoring Sensor Warmup
```python
# ❌ BAD: Using first frames from sensor
camera.start()
frame = camera.capture()  # Often overexposed, auto-exposure not settled

# ✅ GOOD: Discard initial frames
camera.start()
for _ in range(30):  # Let auto-exposure settle (~1 second at 30Hz)
    camera.capture()
frame = camera.capture()  # Now usable
```

### 5. Single-Pixel Depth Sampling
```python
# ❌ BAD: Single pixel is noisy and may be a hole
z = depth[int(center_y), int(center_x)]

# ✅ GOOD: Sample a neighborhood, use median
patch = depth[cy-3:cy+4, cx-3:cx+4]
valid = patch[patch > 0]
z = np.median(valid) if len(valid) > 0 else None
```

### 6. Not Handling Coordinate Frame Transforms
```python
# ❌ BAD: Assuming everything is in the same frame
object_position = detection.position  # In camera frame? Robot frame? World frame?
robot.move_to(object_position)        # Which frame does move_to expect?

# ✅ GOOD: Explicit frame tracking
object_in_camera = detection.position_3d       # Camera frame
object_in_base = T_base_camera @ np.append(object_in_camera, 1.0)  # Robot frame
robot.move_to(object_in_base[:3])
```

## Production Perception Checklist

1. **Calibrate before deploying** — intrinsics, extrinsics, hand-eye
2. **Validate calibration** with independent measurements
3. **Set sensor exposure** appropriately — auto-exposure can cause detection flicker
4. **Undistort** before any geometric computation
5. **Filter depth** — remove flying pixels, fill small holes
6. **Timestamp at capture** — not at processing time
7. **Track objects** across frames — don't rely on single-frame detections
8. **Handle sensor failures** — missing frames, degraded depth, overexposure
9. **Log perception output** — bounding boxes, confidence scores, 3D positions
10. **Benchmark latency** — measure each pipeline stage, find bottlenecks
11. **Test with edge cases** — empty scenes, cluttered scenes, reflective surfaces, direct sunlight
12. **Version your models** — pin detection/segmentation model versions in deployment
