---
description: Validates YARS rendering by exporting first frame as PNG and comparing with reference screenshot
version: 1.0.0
allowed-tools: [Bash, Read]
---

# Validate YARS Rendering

This skill ensures that rendering and texture functionality works correctly by:

1. Running YARS with image export enabled to capture the first frame
2. Comparing the exported frame with the reference screenshot.png
3. Reporting any visual differences that might indicate rendering issues

## Usage

Automatically invoked when:
- User asks to check visualization or rendering
- After graphics/texture changes
- When validating material or shader modifications
- To verify Ogre3D rendering is working correctly

## Validation Steps

```bash
# Navigate to build directory
cd build

# Create frames directory for output
mkdir -p frames

# Run YARS with frame capture
# NOTE: Frame export requires setting frames directory in XML config
# or via __YARS_GET_FRAMES_DIRECTORY macro
# Frame capture auto-enables if directory is set (see SdlWindow.cpp:82-88)
timeout 60s ./bin/yars --xml ../xml/braitenberg.xml --iterations 10

# Expected output: frames/frame_00000001.png through frame_00000010.png

# Compare first frame with reference using ImageMagick
compare -metric RMSE frames/frame_00000001.png ../screenshot.png diff.png

# Or use visual diff
# open frames/frame_00000001.png
# open ../screenshot.png
```

## Success Criteria

- ✅ YARS builds and runs without errors
- ✅ Frames are successfully exported to frames/ directory
- ✅ Exported images are valid PNG files
- ✅ Visual comparison shows matching rendering (textures, geometry, lighting)
- ✅ Pixel difference within acceptable threshold

## Configuration Notes

**Frame Export Setup** (from SdlWindow.cpp):
- Auto-enables when `__YARS_GET_FRAMES_DIRECTORY` is set
- Exports to: `{framesDir}/frame_{index:08d}.png`
- Uses Ogre3D's `RenderTexture::writeContentsToFile()`

**To Enable Frame Export:**
1. Check XML config for frames directory setting
2. OR modify configuration to set frames output directory
3. Frames will be captured automatically each step

## Known Limitations

- Need to determine exact XML config or command-line option for frames directory
- Reference screenshot.png may be from specific simulation state
- May need to match exact camera position/orientation
- Lighting and shadow settings affect visual comparison
