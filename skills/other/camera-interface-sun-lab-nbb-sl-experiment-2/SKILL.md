---
name: implementing-camera-interface
description: >-
  Guides implementation of camera hardware interfaces using ataraxis-video-system. Covers camera discovery,
  configuration verification, interactive testing, and binding class patterns. Use when adding camera support
  to any acquisition system or troubleshooting camera connectivity.
---

# Camera Interface Implementation

Guides the implementation of camera hardware interfaces using the ataraxis-video-system library. This skill focuses on
the low-level hardware integration patterns applicable to any acquisition system.

---

## When to Use This Skill

Use this skill when:

- Adding camera support to an acquisition system
- Troubleshooting camera connectivity issues
- Verifying camera configuration before runtime
- Testing cameras with interactive acquisition
- Understanding the VideoSystem API

For system-specific integration (modifying sl-shared-assets configuration, integrating into mesoscope-vr), use the
`/modifying-mesoscope-vr-system` skill instead.

---

## Verification Requirements

**Before writing any camera code, verify the current state of dependent libraries.**

### Step 0: Version Verification

Follow the **Cross-Referenced Library Verification** procedure in `CLAUDE.md`:

1. Check local ataraxis-video-system version against GitHub
2. If version mismatch exists, ask the user how to proceed
3. Use the verified source for API reference

### Step 1: Content Verification

| File                                                                 | What to Check                                   |
|----------------------------------------------------------------------|-------------------------------------------------|
| `../ataraxis-video-system/README.md`                                 | Current usage instructions and MCP server setup |
| `../ataraxis-video-system/src/ataraxis_video_system/__init__.py`     | Exported classes, functions, and public API     |
| `../ataraxis-video-system/src/ataraxis_video_system/video_system.py` | VideoSystem constructor parameters and methods  |
| sl-experiment `pyproject.toml`                                       | Current pinned version dependency               |

### Step 2: Hardware Verification

**Before implementing camera code, verify cameras are connected and accessible using MCP tools.**

The ataraxis-video-system library provides an MCP server for camera discovery. Start the server with:
```bash
axvs mcp
```

**Verification workflow:**

1. **Check runtime requirements**: `check_runtime_requirements()` - Verify FFMPEG and GPU availability
2. **Check CTI status** (if using Harvesters): `get_cti_status()` - Verify GenTL Producer is configured
3. **Discover cameras**: `list_cameras()` - Verify expected cameras are detected with correct indices

**Expected output from `list_cameras()`:**
```
OpenCV Cameras:
  Index 0: 1920x1080 @ 30fps
  Index 1: 640x480 @ 30fps

Harvesters Cameras:
  Index 0: Allied Vision Mako G-040B (1936x1216)
```

If cameras are not detected:
- Check physical USB/GigE connections
- Verify camera drivers are installed
- For Harvesters: ensure CTI file is configured (`get_cti_status()`)
- Check for port conflicts with other applications

**Do not proceed with implementation until expected cameras are verified.**

---

## Camera Discovery

Use the ataraxis-video-system MCP tools for camera discovery. These tools provide programmatic access to connected
cameras.

### MCP Tools Available

| Tool                         | Purpose                                                |
|------------------------------|--------------------------------------------------------|
| `list_cameras`               | Discovers all OpenCV and Harvesters cameras            |
| `get_cti_status`             | Checks if GenTL Producer (.cti) file is configured     |
| `set_cti_file`               | Configures the CTI file path for GeniCam cameras       |
| `check_runtime_requirements` | Verifies FFMPEG and GPU availability                   |

### Discovery Workflow

1. **Check runtime requirements**: Verify FFMPEG and GPU availability
2. **Check CTI status**: Ensure GenTL Producer is configured for Harvesters cameras
3. **List cameras**: Discover all connected cameras with their indices and properties
4. **Record camera indices**: Note the indices for configuration files

---

## Interactive Camera Testing

Test cameras using the MCP video session tools before integrating into the acquisition system.

### Test Session Workflow

1. **Start video session**: Initialize camera with test parameters
2. **Verify preview**: Check that frames are being acquired and displayed
3. **Start frame saving**: Test recording to temporary directory
4. **Stop session**: Clean up resources

### MCP Session Tools

| Tool                   | Purpose                                    |
|------------------------|--------------------------------------------|
| `start_video_session`  | Starts capture with camera/encoding params |
| `stop_video_session`   | Stops capture and releases resources       |
| `start_frame_saving`   | Begins recording to video file             |
| `stop_frame_saving`    | Stops recording, keeps session active      |
| `get_session_status`   | Returns current session state              |

### Test Parameters

For testing, use conservative parameters with a temporary directory:

```python
# Test configuration
output_directory = None          # Use temp directory (or specify path for manual verification)
camera_interface = "harvesters"  # or "opencv"
camera_index = 0                 # From discovery
display_frame_rate = 15          # Low for testing
video_encoder = "h264"           # CPU encoding for compatibility
quantization_parameter = 25      # Moderate quality
```

The MCP tools use a temporary directory by default for test recordings. Specify an output directory only if the user
wants to manually verify the recorded video file.

---

## VideoSystem API Reference

See [CAMERA_INTERFACE_GUIDE.md](CAMERA_INTERFACE_GUIDE.md) for the complete API reference including:

- VideoSystem constructor parameters
- Enumeration values (CameraInterfaces, VideoEncoders, EncoderSpeedPresets)
- Lifecycle methods (start, stop, start_frame_saving, stop_frame_saving)
- Discovery functions (discover_camera_ids, check_cti_file, add_cti_file)

---

## Binding Class Patterns

When implementing camera support in a binding class, follow these patterns:

### Basic Structure

```python
class VideoSystems:
    """Manages video acquisition from cameras.

    Args:
        data_logger: DataLogger instance for timestamp logging.
        output_directory: Directory path for video file output.
        camera_configuration: Camera settings from system configuration.

    Attributes:
        _camera: VideoSystem instance for frame acquisition.
        _camera_started: Tracks whether acquisition has started.
    """

    def __init__(
        self,
        data_logger: DataLogger,
        output_directory: Path,
        camera_configuration: CameraConfig,
    ) -> None:
        self._camera: VideoSystem = VideoSystem(
            system_id=np.uint8(51),
            data_logger=data_logger,
            output_directory=output_directory,
            camera_index=camera_configuration.camera_index,
            camera_interface=CameraInterfaces.HARVESTERS,
            # ... other parameters from configuration
        )
        self._camera_started: bool = False

    def start(self) -> None:
        """Starts frame acquisition (does not save frames)."""
        if self._camera_started:
            return
        self._camera.start()
        self._camera_started = True

    def start_saving(self) -> None:
        """Begins saving frames to disk."""
        self._camera.start_frame_saving()

    def stop(self) -> None:
        """Stops acquisition and releases resources."""
        if self._camera_started:
            self._camera.stop_frame_saving()
        self._camera.stop()
        self._camera_started = False
```

### Key Patterns

| Pattern              | Purpose                                       |
|----------------------|-----------------------------------------------|
| Idempotency guards   | Prevent double-start with `_started` flags    |
| Destructor cleanup   | `__del__` method calls `stop()` for safety    |
| Separate start/save  | Preview mode before recording                 |
| Configuration inject | Pass dataclass from sl-shared-assets          |

### System ID Allocation

| ID Range | Purpose                                                                    |
|----------|----------------------------------------------------------------------------|
| 1-49     | Reserved for non-camera hardware systems                                   |
| 50-99    | Camera and video acquisition systems                                       |
| 100+     | Reserved for future expansion                                              |

Current allocations in mesoscope-vr: `51` (face camera), `62` (body camera).

---

## Configuration Requirements

Camera configuration must be defined in sl-shared-assets before implementation.

### Required Configuration Fields

| Field                    | Type  | Range | Description                                |
|--------------------------|-------|-------|--------------------------------------------|
| `*_camera_index`         | `int` | 0+    | Camera index from discovery                |
| `*_camera_quantization`  | `int` | 0-51  | Encoding quality (lower = higher quality)  |
| `*_camera_preset`        | `int` | 1-7   | Encoding speed preset (maps to IntEnum)    |

### Configuration Dataclass Pattern

```python
@dataclass()
class SystemCameras:
    """Camera configuration for the acquisition system."""

    camera_index: int = 0
    """Camera index from the discovery function output."""

    camera_quantization: int = 15
    """Quantization parameter (0-51). Lower values produce higher quality."""

    camera_preset: int = 5
    """Encoding speed preset (1-7). Maps to EncoderSpeedPresets enum (SLOW=5 default)."""
```

---

## Troubleshooting

### Camera Not Detected

1. Verify driver software is installed
2. For Harvesters: check CTI file is configured using `get_cti_status()` MCP tool
3. Check physical connections and power
4. Run `list_cameras()` MCP tool to see available cameras

### Encoding Failures

1. Verify FFMPEG installation using `check_runtime_requirements()` MCP tool
2. Check GPU availability for hardware encoding
3. Monitor GPU memory and thermal status

### Frame Drops

1. Reduce `display_frame_rate` or disable preview (`None`)
2. Use faster `encoder_speed_preset`
3. Increase `quantization_parameter` (reduces quality)

### Process Crashes

1. Ensure DataLogger is initialized before VideoSystem
2. Verify output directory exists and is writable
3. Check available disk space

---

## Implementation Checklist

Before integrating cameras into an acquisition system:

```
- [ ] Verified ataraxis-video-system version matches requirements
- [ ] Confirmed FFMPEG and GPU availability using check_runtime_requirements() MCP tool
- [ ] Configured CTI file (for Harvesters cameras) using get_cti_status() and set_cti_file() MCP tools
- [ ] Verified cameras are detected using list_cameras() MCP tool
- [ ] Recorded camera indices from discovery output
- [ ] Tested camera with interactive session using MCP video session tools
- [ ] Created configuration dataclass in sl-shared-assets
- [ ] Implemented binding class with lifecycle methods
- [ ] Allocated unique system IDs for each camera
```
