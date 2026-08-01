---
name: image-to-mission
description: Extract creative intent from images into executable build specs. Activates on images + build intent, "image to mission", "i2m", or capturing visual energy in code/design.
domain: creative-translation
context: fork
activation: domain
dependencies:
  optional:
    - vision-to-mission
format: 2025-10-02
version: 1.0.0
status: ACTIVE
updated: 2026-04-15
triggers:
  - user provides an image and wants it turned into a build spec or mission
  - '"image to mission" or "i2m" is requested'
  - capturing visual or design energy from an image into code or a mission package
---

# Image to Mission

Takes one or more images plus optional creator context and produces:
1. Structured 4-layer visual analysis (literal, spatial, relational, mood)
2. Extracted technical parameters (color, geometry, material, feel)
3. Executable build instructions with philosophy annotations
4. Self-contained transmission package for cross-context handoff

## When to Activate

Activate when the user provides images AND expresses intent to:
- Build, create, or make something based on the images
- Translate visual reference into code, design, or specifications
- Capture the "feel" or "energy" of images in another medium
- Create a mission package from visual reference
- Direct keywords: "image to mission", "i2m"
- Target medium: "translate this to [canvas/react/three.js/SVG/CSS]"

DO NOT activate when the user:
- Simply asks "what's in this image?" (use standard image analysis)
- Wants image editing or manipulation
- Needs OCR or text extraction from images
- Is asking about image file formats or metadata
- Asks to describe colors or content without build intent

## Observation Protocol

Before building anything, enter observation mode:

### Phase 1: Observe (mandatory — do not skip)
Process each image through four layers:
- **Literal:** Inventory all visible objects, materials, colors
- **Spatial:** Map relationships, arrangements, density
- **Relational:** Find patterns across images, note changes vs. constants
- **Mood:** Quantify atmosphere (energy, intimacy, order, handmade, ceremony)

### Phase 2: Listen (if creator provides context)
Structure context into: process, intent, constraints, accidents, multipurpose.
Extract the process insight — the key understanding about HOW it was made.

### Phase 3: Connect
Synthesize observations + context into unified understanding.
Find what neither source reveals alone.

### Phase 4: Extract
Convert understanding to numerical parameters:
- Colors (palette, temperature, contrast, relationships)
- Geometry (shape, arrangement, symmetry, constants)
- Materials (surfaces, light interaction, blend modes)
- Feel (energy, intimacy, order, handmade, ceremony — all 0-1)

### Phase 5: Build
Translate parameters to target medium.
Generate step-by-step instructions with philosophy notes.

### Phase 6: Document
Package everything for transmission.
Validate self-containment.

## Output Formats

| Format | When | Content |
|--------|------|---------|
| Direct build | Simple, single-medium output | Code/SVG + philosophy notes |
| Build spec | Medium complexity | Step-by-step instructions |
| Mission package | Complex, multi-component | Full vision_to_mission handoff |
| Transmission package | Cross-context work | JSON/Markdown bundle |

## Implementation

Code lives in `src/vtm/image-to-mission/`. Key modules:
- **observation-engine** — four-layer observation (literal/spatial/relational/mood)
- **context-integrator** — freeform text parser, layer mapping, process insight extraction
- **connection-engine** — cross-image linker, visual-context bridge, synthesis orchestrator
- **parameter-extractor** — color/geometry/material/feel extraction with reference tables
- **translation-code** — Canvas, React/JSX, Three.js, CSS translators
- **translation-design** — SVG, palette, markdown layout spec
- **build-generator** — ordered atomic build steps with philosophy annotations
- **transmission-packager** — 5 self-containment checks, JSON + markdown serialization
- **pipeline-bridge** — complexity scoring (0-12), routing, override detection, v2m handoff

## Key Principles

1. **Observe before building** — spend time with images
2. **Process reveals pattern** — ask how, not just what
3. **Emergent > designed** — honor organic over mechanical
4. **Feel over fidelity** — capture energy, not pixels
5. **Document for transmission** — write for the next mind

## Safety

- Output is inspired by, not a copy of, source images
- Creator context is attributed, never silently absorbed
- Simple description requests are rejected to avoid wasting observation protocol
