---
name: motion-tracking
description: "Master motion tracking techniques for video production including planar tracking, 3D camera tracking, and matchmoving. Use for: tracking objects in footage, stabilizing shots, integrating CGI elements, screen replacements, adding graphics to moving surfaces, camera solve, point tracking, and creating realistic visual effects composites."
---

# Motion Tracking

Master professional motion tracking techniques for seamless VFX integration and camera matchmoving.

## Overview

Motion tracking analyzes video footage to determine the movement of objects or cameras, enabling the integration of digital elements that move realistically with the original footage. This skill covers planar tracking, 3D camera tracking, point tracking, and professional workflows for visual effects production.

## Core Tracking Methods

### Planar Tracking

Track flat surfaces and textures in 2D space.

**Applications**:
- Screen replacements (phones, monitors, billboards)
- Adding graphics to walls or floors
- Object removal and cleanup
- Image stabilization

**Key Characteristics**:
- Tracks translation, rotation, scale, and skew
- Computationally efficient
- Ideal for flat surfaces
- Struggles with depth changes

### 3D Camera Tracking (Matchmoving)

Reconstruct camera movement in 3D space.

**Applications**:
- Integrating 3D CGI elements
- Set extensions and environment enhancement
- Complex VFX requiring accurate 3D placement
- Virtual production workflows

**Key Characteristics**:
- Tracks camera position, rotation, and focal length
- Handles complex camera movements
- Requires sufficient detail in footage
- More computationally intensive

### Point Tracking

Track specific points or features across frames.

**Applications**:
- Attaching graphics to moving objects
- Stabilization
- Simple object tracking
- Data for other effects

## Professional Workflows

### Pre-Production Considerations

- Ensure sufficient contrast and detail for tracking
- Add tracking markers when possible
- Plan camera movements for trackability
- Consider lighting consistency

### Tracking Workflow

1. **Analyze footage** for trackable features
2. **Select tracking method** based on requirements
3. **Set up tracking** points, planes, or camera solve
4. **Execute track** and review results
5. **Refine tracking** data as needed
6. **Apply tracking** to target elements
7. **Verify integration** across full shot

## Software and Tools

| Software | Tracking Capabilities | Best For |
|----------|----------------------|----------|
| Mocha Pro | Planar tracking, 3D camera tracking | Screen replacements, rotoscoping |
| SynthEyes | 3D camera tracking, object tracking | Complex matchmoving |
| After Effects | Point tracking, 3D camera tracker | Motion graphics, basic VFX |
| Nuke | All tracking types | High-end VFX compositing |
| Blender | Camera tracking, object tracking | 3D integration, free solution |
| PFTrack | Professional 3D tracking | Film and TV production |

## Best Practices

- **Start with good footage**: High contrast, detailed, well-lit
- **Use multiple tracking points**: Increases accuracy and stability
- **Track through entire shot**: Even if effect only appears partially
- **Verify tracking data**: Check for drift or errors
- **Refine manually when needed**: Automatic tracking isn't always perfect
- **Consider motion blur**: Can affect tracking accuracy
- **Save tracking data**: For revisions and iterations

## Common Challenges

| Challenge | Cause | Solution |
|-----------|-------|----------|
| Tracking drift | Accumulated errors over time | Add more tracking points, manual refinement |
| Lost tracking | Occlusion or motion blur | Track visible portions, interpolate gaps |
| Jittery results | Insufficient tracking data | Smooth tracking data, add more points |
| Perspective issues | Incorrect camera solve | Refine solve, add survey data if available |
| Scale problems | Lack of reference | Add known measurements or objects |

## Using the Reference Files

### When to Read Each Reference

**`/references/planar-tracking-techniques.md`** — Read when working with screen replacements, adding graphics to flat surfaces, or using Mocha Pro for planar tracking workflows.

**`/references/3d-camera-tracking.md`** — Read when integrating 3D elements, performing camera solves, or working with matchmoving for VFX shots.

**`/references/tracking-workflows.md`** — Read when setting up professional tracking pipelines, optimizing workflows, or working on complex multi-shot projects.

**`/references/troubleshooting-tracking.md`** — Read when encountering tracking failures, drift issues, or when automatic tracking produces unsatisfactory results.
