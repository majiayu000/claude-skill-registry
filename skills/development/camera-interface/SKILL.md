---
name: using-camera-interface
description: >-
  Guide for using ataraxis-video-system to implement camera functionality in sl-experiment.
  Maps library architecture, public API, and integration patterns used in this codebase.
---

# Camera Interface Usage Guide

When implementing camera functionality in sl-experiment, use the ataraxis-video-system library
following the patterns established in this codebase.

See [CAMERA_INTERFACE_GUIDE.md](CAMERA_INTERFACE_GUIDE.md) for complete API reference and integration patterns.

## IMPORTANT: Verification Requirement

**Before writing any camera code, you MUST verify the current state of the dependent libraries.**
The documentation in this skill may be outdated.

### Step 0: Version Verification

Follow the **Cross-Referenced Library Verification** procedure in `CLAUDE.md` to ensure local copies
of `ataraxis-video-system` and `sl-shared-assets` are up to date with their GitHub repositories.
If version mismatches exist, ask the user how to proceed before continuing.

### Content Verification

After version verification, perform the following content checks:

### 1. Verify ataraxis-video-system

- Read `README.md` in `/home/cyberaxolotl/Desktop/GitHubRepos/ataraxis-video-system/` for current
  usage instructions
- Read examples in `/home/cyberaxolotl/Desktop/GitHubRepos/ataraxis-video-system/examples/` for
  recommended patterns
- Read `src/ataraxis_video_system/__init__.py` to confirm exported classes and functions
- Read `src/ataraxis_video_system/video_system.py` to verify `VideoSystem` constructor parameters
  and methods
- Check `pyproject.toml` in sl-experiment for the current version dependency

### 2. Verify sl-shared-assets

- Read `README.md` in `/home/cyberaxolotl/Desktop/GitHubRepos/sl-shared-assets/` for current
  conventions
- Read `src/sl_shared_assets/data_classes/configuration_data.py` to confirm camera configuration
  patterns
- Verify `AcquisitionSystems` enum members for existing systems
- Check existing camera dataclasses (e.g., `MesoscopeCameras`) for current field conventions
- Review `__init__.py` exports to understand public API

### 3. Verify sl-experiment binding patterns

- Read `src/sl_experiment/mesoscope_vr/binding_classes.py` to confirm current `VideoSystems`
  implementation
- Check for any new patterns or conventions introduced since this skill was written

**If any discrepancies are found between this guide and the actual library state, follow the
current library implementation rather than this documentation.**

---

## Decision Logic

```
Does the acquisition system already have a binding class?
│
├─ YES → Add camera wrapper to existing binding_classes.py
│
└─ NO  → Create full binding hierarchy (see de-novo system guide)
```

**Existing binding classes:** `src/sl_experiment/mesoscope_vr/binding_classes.py`

## Quick Reference

### Core Import

```python
from ataraxis_video_system import (
    VideoSystem,
    VideoEncoders,
    CameraInterfaces,
    OutputPixelFormats,
    EncoderSpeedPresets,
)
```

### VideoSystem Instantiation

```python
camera = VideoSystem(
    system_id=np.uint8(51),
    data_logger=logger,
    output_directory=output_path,
    camera_interface=CameraInterfaces.HARVESTERS,
    camera_index=camera_config.camera_index,
    display_frame_rate=25,
    video_encoder=VideoEncoders.H265,
    gpu=0,
    encoder_speed_preset=EncoderSpeedPresets(camera_config.preset),
    output_pixel_format=OutputPixelFormats.YUV420,
    quantization_parameter=camera_config.quantization,
)
```

### Lifecycle Pattern

```python
camera.start()              # Begin frame acquisition
camera.start_frame_saving() # Begin recording to disk
# ... acquisition runs ...
camera.stop_frame_saving()  # Stop recording
camera.stop()               # Release resources
```

## sl-shared-assets Requirements

Camera configuration must be defined in sl-shared-assets before sl-experiment implementation.

**For existing systems:** Add camera dataclass if not present
**For de-novo systems:** Create full configuration hierarchy

### Required Configuration Classes

```python
# sl-shared-assets/src/sl_shared_assets/data_classes/configuration_data.py

@dataclass()
class YourSystemCameras:
    camera_index: int = 0
    camera_quantization: int = 20  # 0-51, lower = better
    camera_preset: int = 7         # 0-5, maps to EncoderSpeedPresets
```

### System Configuration Container

```python
@dataclass()
class YourSystemConfiguration(YamlConfig):
    cameras: YourSystemCameras = field(default_factory=YourSystemCameras)
    # ... other components
```

## Existing Integration

See `src/sl_experiment/mesoscope_vr/binding_classes.py` for the `VideoSystems` wrapper class that
manages face and body cameras in this codebase.

## System ID Allocation

| ID Range | Purpose        |
|----------|----------------|
| 50-99    | Camera systems |

Current: `51` (face), `62` (body)
