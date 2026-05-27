---
name: create-lut
description: >
  Generate or bake cinematic 3D LUTs (.cube) from reference/source pairs or presets.
triggers:
  - create lut
  - generate lut
  - bake lut
  - 3d lut
allowed-tools:
  - Bash
  - Python
metadata:
  short-description: Create cinematic 3D LUTs (.cube)

provides:
  - create-lut
composes: [, task-monitor]
---

# create-lut

Programmatically generate or bake cinematic 3D LUTs (.cube).

## Usage

```bash
./run.sh bake --ref ref.png --source src.png --output match.cube
./run.sh generate --preset "fujifilm_sim" --size 33
```

## Contract

- **Input**: Image pairs (reference/source) or procedural parameters.
- **Output**: Single `.cube` (3D LUT) file.
- **Dependencies**: `colour-science`, `numpy`, `opencv-python`.

## Features

- **Match Grade**: Calculate a color transform between a reference frame (learned from a movie) and a generated frame.
- **Procedural Simulation**: Apply standard film stock mathematical models (e.g., Kodak 2383).
- **Identity Export**: Generate a clean neutral LUT for pipeline testing.
