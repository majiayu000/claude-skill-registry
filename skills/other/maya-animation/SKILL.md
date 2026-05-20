---
name: maya-animation
description: "Create professional 3D animations in Autodesk Maya using industry-standard workflows. Use for: keyframe animation, character rigging, IK/FK systems, blend shapes, Graph Editor refinement, motion capture integration, animation cycles, constraint systems, timeline management, and game engine export."
---

# Maya Animation

Master professional 3D animation techniques in Autodesk Maya, the industry-standard software for film, television, and game development.

## Overview

Autodesk Maya is a comprehensive 3D graphics software widely recognized as an industry standard for animation, modeling, visual effects (VFX), and rendering. This skill focuses on animation workflows, from basic keyframing to advanced character animation and motion capture integration.

## Animation Fundamentals

### Keyframe Animation

**Core Concepts**:
- Keyframes define object properties at specific points in time
- Maya interpolates between keyframes automatically
- Position, rotation, and scale can be keyframed independently
- Timing and spacing control animation quality

**Setting Keyframes**:
- **S Key**: Set keyframe on selected attributes
- **Shift+W/E/R**: Keyframe translate/rotate/scale
- **Right-click attribute**: Key Selected
- **Auto Key**: Automatically set keys when values change
- **Hold Current Keys**: Prevent accidental key creation

**Keyframe Types**:
- **Breakdown Keys**: In-between poses for refinement
- **Stepped Keys**: No interpolation, pose-to-pose animation
- **Linear Keys**: Constant velocity interpolation
- **Spline Keys**: Smooth, curved interpolation

### Timeline and Playback

**Timeline Controls**:
- Set frame range for animation
- Playback speed and direction
- Frame rate settings (24fps film, 30fps video, 60fps games)
- Current time indicator
- Range slider for focused playback

**Time Management**:
- **Animation Start/End**: Overall project timeline
- **Playback Range**: Focused section for review
- **Frame Rate**: Matches target output format
- **Time Unit**: Frames, seconds, or timecode

### Animation Principles

**12 Principles of Animation**:
1. **Squash and Stretch**: Volume preservation, impact emphasis
2. **Anticipation**: Prepare for main action
3. **Staging**: Clear presentation of idea
4. **Straight Ahead vs. Pose-to-Pose**: Animation approaches
5. **Follow Through and Overlapping**: Secondary motion
6. **Slow In and Slow Out**: Ease in/out of movements
7. **Arcs**: Natural motion paths
8. **Secondary Action**: Supporting main action
9. **Timing**: Speed and rhythm
10. **Exaggeration**: Enhance appeal and clarity
11. **Solid Drawing**: Form and weight
12. **Appeal**: Engaging character design

## Graph Editor

### Understanding Animation Curves

**Curve Components**:
- **Keys**: Points on the curve representing keyframes
- **Tangents**: Control interpolation between keys
- **Handles**: Adjust tangent weight and angle
- **Infinity**: Behavior before first and after last key

**Curve Analysis**:
- Steep curves = fast motion
- Flat curves = slow motion
- Smooth curves = natural motion
- Sharp angles = sudden changes

### Graph Editor Tools

**Tangent Types**:
- **Auto**: Smooth, automatic tangent calculation
- **Spline**: Smooth curve through keys
- **Linear**: Straight line between keys
- **Flat**: Horizontal tangents, ease in/out
- **Stepped**: No interpolation, holds value
- **Clamped**: Prevents overshoot
- **Plateau**: Flat tangents at peaks and valleys

**Editing Techniques**:
- **Insert Keys**: Add keys without changing curve shape
- **Delete Keys**: Remove unnecessary keys
- **Move Keys**: Adjust timing
- **Scale Keys**: Expand or compress timing
- **Lattice Deform**: Reshape curve sections
- **Buffer Curves**: Store and compare curve versions

**Curve Refinement**:
- Simplify curves by removing redundant keys
- Smooth curves for natural motion
- Add keys for detail and control
- Offset curves for overlapping action
- Cycle curves for looping animations

### Advanced Graph Editor

**Infinity Types**:
- **Constant**: Hold first/last value
- **Linear**: Continue at same rate
- **Cycle**: Repeat animation
- **Cycle with Offset**: Repeat with accumulation
- **Oscillate**: Ping-pong back and forth

**Curve Filters**:
- View specific attributes
- Isolate selected objects
- Show only keyed channels
- Filter by curve color

## Character Rigging Basics

### Joint Systems

**Creating Joints**:
- Skeleton > Joint Tool
- Click to place joints in hierarchy
- Plan joint placement for natural deformation
- Mirror joints for symmetry
- Orient joints for proper rotation

**Joint Hierarchy**:
- Parent-child relationships
- Root joint at character base or pelvis
- Spine, arms, legs as branches
- Proper naming conventions (L_/R_ prefixes)

**Joint Orientation**:
- Consistent axis alignment
- Primary axis along bone length
- Secondary axis for twist
- Proper orientation prevents gimbal lock

### Inverse Kinematics (IK)

**IK Handles**:
- Skeleton > Create IK Handle
- Click start joint, then end joint
- Automatically calculates joint rotations
- Ideal for limbs (arms, legs)

**IK Solvers**:
- **Single Chain (SC)**: Simple two-joint chains
- **Rotate Plane (RP)**: Three+ joints with pole vector
- **Spline IK**: Joints follow curve (spine, tail)

**Pole Vectors**:
- Control IK chain orientation
- Prevent flipping
- Position in front of knee/elbow
- Constrain to locator for animator control

### Forward Kinematics (FK)

**FK Animation**:
- Rotate each joint individually
- Parent-child rotation inheritance
- Precise control over each joint
- Ideal for spine, fingers, facial features

**IK/FK Switching**:
- Blend between IK and FK
- Switch mid-animation for different needs
- IK for planted feet, FK for free movement
- Attribute-driven blend controls

### Skinning (Binding)

**Smooth Bind**:
- Skin > Bind Skin > Smooth Bind
- Attaches mesh to skeleton
- Multiple joints influence each vertex
- Weight distribution determines deformation

**Weight Painting**:
- Skin > Paint Skin Weights Tool
- Adjust joint influence on vertices
- Smooth transitions between joints
- Lock weights to prevent changes
- Mirror weights for symmetry

**Binding Best Practices**:
- Bind in neutral pose
- Clean geometry before binding
- Appropriate joint placement
- Test deformation with simple poses
- Iterate weight painting for quality

## Blend Shapes (Morph Targets)

### Creating Blend Shapes

**Workflow**:
1. Duplicate base mesh
2. Sculpt or modify duplicate to target shape
3. Select target(s), then base mesh
4. Deform > Blend Shape
5. Adjust blend shape slider (0-1)

**Applications**:
- Facial expressions
- Corrective shapes for joint deformation
- Muscle bulging
- Clothing wrinkles
- Lip sync phonemes

### Blend Shape Management

**Multiple Targets**:
- Add multiple blend shapes to one object
- Combine blend shapes additively
- In-between targets for progressive deformation
- Parallel blend shapes for independent controls

**Blend Shape Editor**:
- Manage all blend shapes
- Adjust target weights
- Reorder targets
- Add/remove targets
- Set target in-betweens

### Facial Animation

**FACS (Facial Action Coding System)**:
- Anatomically-based facial poses
- Individual muscle movements
- Combine for complex expressions
- Industry standard for realistic faces

**Phoneme Shapes**:
- Mouth shapes for speech sounds
- A, E, I, O, U vowels
- M, B, P, F, V consonants
- Blend between shapes for lip sync

## Animation Constraints

### Constraint Types

**Parent Constraint**:
- Object follows position and rotation of target
- Maintain offset option
- Multiple targets with weights
- Use for prop attachment, character interaction

**Point Constraint**:
- Object follows position only
- Useful for floating objects
- Constrain to multiple targets

**Orient Constraint**:
- Object follows rotation only
- Maintain offset for local rotation
- Blend between multiple targets

**Aim Constraint**:
- Object aims at target
- Specify aim axis and up axis
- Use for eyes, cameras, turrets

**Pole Vector Constraint**:
- Control IK chain orientation
- Constrain IK pole vector to locator
- Essential for stable IK animation

### Constraint Workflows

**Animator-Friendly Rigs**:
- Constraints hidden in rig structure
- Simple controls for animators
- Attributes for constraint blending
- Space switching for different constraint targets

**Constraint Blending**:
- Animate constraint weights
- Blend between multiple targets
- Keyframe constraint on/off
- Smooth transitions between constraint states

## Animation Cycles

### Creating Cycles

**Walk Cycle**:
- Contact, down, passing, up positions
- Typically 16-24 frames
- Match first and last frame
- Offset arms and legs
- Add secondary motion (head bob, arm swing)

**Run Cycle**:
- Similar to walk but faster
- More airborne time
- Exaggerated poses
- Typically 12-16 frames

**Cycle Workflow**:
1. Animate one complete cycle
2. Ensure first and last frames match
3. Set Graph Editor infinity to Cycle
4. Adjust timing and spacing
5. Add variation to prevent repetition

### Smoothing Cycles

**Graph Editor Techniques**:
- Match tangents on first and last keys
- Use Cycle with Offset for traveling motion
- Plateau tangents for smooth loops
- Remove overshoot and undershoot

**Cycle Variations**:
- Slight timing offsets
- Amplitude variation
- Add noise for organic feel
- Layer secondary animation

## Motion Capture Integration

### Motion Capture Basics

**Mocap Data**:
- Real-world movement recorded
- Marker-based or markerless systems
- High frame rate capture
- Import as animation curves or skeleton

**Data Cleanup**:
- Remove noise and jitter
- Fill gaps from missing markers
- Smooth curves while preserving detail
- Retarget to custom rig

### Retargeting

**HumanIK**:
- Maya's built-in retargeting system
- Map mocap skeleton to custom rig
- Adjust for proportion differences
- Blend mocap with keyframe animation

**Retargeting Workflow**:
1. Import mocap data
2. Create HumanIK character definition
3. Map mocap skeleton to rig
4. Adjust retargeting settings
5. Bake animation to rig controls
6. Refine and polish

## Baking and Export

### Baking Animation

**Purpose**:
- Convert constraints and simulations to keyframes
- Prepare for game engine export
- Simplify complex rig animation
- Optimize performance

**Baking Process**:
1. Select objects to bake
2. Edit > Keys > Bake Simulation
3. Set frame range
4. Choose channels to bake
5. Sample rate (every frame or sparse)
6. Bake and verify results

### Game Engine Export

**FBX Export**:
- Industry standard for game engines
- File > Export Selection > FBX
- Include animation, skeleton, and mesh
- Set appropriate FBX version
- Configure animation settings

**Export Best Practices**:
- Bake animation before export
- Delete non-deformer history
- Freeze transformations on root
- Check scale and orientation
- Test in target engine

## Advanced Techniques

### Motion Trails
