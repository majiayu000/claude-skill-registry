---
name: motion-capture
description: "Capture and process motion capture data for realistic character animation. Use for: mocap session planning, marker placement, data capture, cleaning mocap data, retargeting to characters, facial mocap, solving mocap issues, and integrating mocap into production pipelines."
---

# Motion Capture

Capture and process motion capture data for realistic character animation in games and film.

## Overview

This skill covers the complete motion capture pipeline from session planning to final animation. Learn marker placement, data capture techniques, cleaning and solving mocap data, retargeting to custom characters, facial mocap workflows, and integrating mocap into production pipelines.

## Quick Start: Mocap System Selection

| System Type | Best For | Cost | Reference |
|-------------|----------|------|-----------|
| Optical (Vicon, OptiTrack) | Professional film/AAA games | High | `/references/optical-systems.md` |
| Inertial (Xsens, Perception Neuron) | On-location, outdoor capture | Medium | `/references/inertial-systems.md` |
| Markerless (Rokoko, Move.ai) | Indie games, quick capture | Low-Medium | `/references/markerless-systems.md` |
| Facial (Faceware, iPhone ARKit) | Dialogue, expressions | Medium | `/references/facial-mocap.md` |

## Core Mocap Concepts

### Motion Capture Types

**Optical Systems:**
- Infrared cameras track reflective markers
- High accuracy (sub-millimeter)
- Requires controlled environment
- Industry standard for film/AAA

**Inertial Systems:**
- Wearable sensors (IMUs)
- No cameras required
- Works anywhere (outdoor, on-set)
- Slightly less accurate than optical

**Markerless Systems:**
- Computer vision, no markers/suits
- Webcam or video-based
- Lower accuracy but very accessible
- Improving rapidly with AI

**Hybrid Systems:**
- Combine optical + inertial
- Best accuracy and flexibility
- Used in high-end productions

## Mocap Pipeline Stages

### Stage 1: Pre-Production Planning

**Define Requirements:**
- What actions/movements needed?
- How many performers?
- Props and environment needs?
- Quality requirements?
- Budget and timeline?

**Performer Selection:**
- Match character proportions if possible
- Skilled performers vs. actors
- Stunt performers for action
- Facial capture considerations

**Session Planning:**
- Shot list and priorities
- Timing and scheduling
- Backup plans
- Reference video

### Stage 2: Calibration and Setup

**System Calibration:**
- Camera calibration (optical)
- Sensor calibration (inertial)
- Volume calibration (capture space)
- Verify accuracy

**Marker Placement:**
- Follow standard marker sets (e.g., Vicon Plug-in Gait)
- Anatomical landmarks
- Rigid body markers for props
- Minimize occlusion

**Test Capture:**
- Capture test movements
- Verify marker visibility
- Check data quality
- Adjust as needed

### Stage 3: Capture Session

**Recording:**
- Slate each take (identify in data)
- Capture reference video
- Multiple takes for safety
- Monitor data quality in real-time

**Direction:**
- Communicate clearly with performer
- Review takes immediately
- Iterate and refine
- Capture variations

### Stage 4: Data Processing

**Cleaning:**
- Fill gaps (missing marker data)
- Remove noise and jitter
- Fix marker swaps
- Smooth trajectories

**Solving:**
- Reconstruct skeleton from markers
- Solve for joint rotations
- Handle occlusions
- Verify solve quality

**Export:**
- Export to FBX, BVH, or other formats
- Include skeleton and animation
- Proper scale and orientation
- Metadata and notes

### Stage 5: Retargeting

**Character Mapping:**
- Map mocap skeleton to character skeleton
- Handle proportion differences
- Adjust for different bone counts
- Maintain motion quality

**Refinement:**
- Adjust foot contact
- Fix penetrations
- Polish hand poses
- Add secondary animation

## Software and Tools

### Capture Software

| Software | System Type | Features |
|----------|-------------|----------|
| Vicon Shogun | Optical | Professional capture and solve |
| Motive (OptiTrack) | Optical | Real-time capture and streaming |
| MVN Analyze (Xsens) | Inertial | Full-body inertial capture |
| Rokoko Studio | Markerless/Inertial | Affordable, user-friendly |

### Processing Software

- **MotionBuilder**: Industry standard for mocap cleanup and retargeting
- **Maya**: Full pipeline, HumanIK for retargeting
- **Blender**: Free option, improving mocap tools
- **iClone**: Real-time character animation with mocap

### Cleanup Tools

- **Shogun Post**: Vicon's post-processing software
- **MotionBuilder**: Excellent cleanup and filtering tools
- **Custom scripts**: Python/MEL for batch processing

## Best Practices

### Marker Placement

1. **Anatomical accuracy** — Place markers on bony landmarks
2. **Minimize occlusion** — Avoid markers blocking each other
3. **Rigid clusters** — Use 3+ markers for rigid bodies
4. **Symmetry** — Mirror left and right sides
5. **Documentation** — Photo reference of marker placement

### Capture Session

1. **Calibrate frequently** — Recalibrate if setup changes
2. **Capture ROM** — Range of motion for each performer
3. **Reference video** — Always record video reference
4. **Multiple takes** — Capture backups of important actions
5. **Real-time review** — Check data quality during session

### Data Cleanup

1. **Work non-destructively** — Keep original data
2. **Fill gaps carefully** — Use appropriate interpolation
3. **Smooth judiciously** — Don't over-smooth and lose detail
4. **Verify solve** — Check skeleton solve quality
5. **Document issues** — Note problems for future reference

## Common Challenges and Solutions

### Challenge: Marker Occlusion

**Solution**: Use more cameras from different angles, adjust marker placement, use predictive gap filling, capture multiple takes.

### Challenge: Foot Sliding

**Solution**: Lock feet during contact, adjust retargeting, use IK constraints, manually key foot positions.

### Challenge: Proportion Mismatch

**Solution**: Use proper retargeting tools, adjust limb lengths, use IK for extremities, accept some differences.

### Challenge: Noisy Data

**Solution**: Apply appropriate filtering, check calibration, improve lighting (optical), reduce magnetic interference (inertial).

## Using the Reference Files

### When to Read Each Reference

**`/references/optical-systems.md`** — Read when setting up optical mocap systems, calibrating cameras, placing markers, or troubleshooting optical capture issues.

**`/references/inertial-systems.md`** — Read when using inertial mocap suits, calibrating sensors, capturing on-location, or solving inertial data.

**`/references/markerless-systems.md`** — Read when using markerless/AI-based mocap, processing video for mocap, or working with accessible mocap solutions.

**`/references/facial-mocap.md`** — Read when capturing facial performances, setting up facial rigs for mocap, processing facial data, or integrating facial animation.
