---
name: rigging-animation
description: "Create professional character rigs for animation in games and film. Use for: building skeletal hierarchies, creating IK/FK systems, weight painting, constraint setup, facial rigging, creating animation controls, rigging for game engines, and preparing characters for motion capture."
---

# Rigging Animation

Create professional character rigs with skeletal systems, controls, and constraints for high-quality animation.

## Overview

This skill covers the complete character rigging pipeline from skeleton creation to animation-ready controls. Learn skeletal hierarchy design, IK/FK systems, weight painting techniques, constraint setup, facial rigging, and optimization for both game engines and film production.

## Quick Start: Rig Type Selection

| Character Type | Rig Complexity | Primary Systems | Reference |
|----------------|----------------|-----------------|-----------|
| Game character (basic) | Simple skeleton + weights | FK limbs, basic controls | `/references/game-rigging.md` |
| Game character (advanced) | Full IK/FK, constraints | IK/FK blend, twist bones | `/references/advanced-systems.md` |
| Film character | Complex controls, layers | Advanced IK, space switching | `/references/film-rigging.md` |
| Facial rig | Blend shapes + bones | FACS blend shapes, jaw/eyes | `/references/facial-rigging.md` |
| Creature/quadruped | Custom skeleton | Spine IK, digitigrade legs | `/references/advanced-systems.md` |

## Core Rigging Principles

### Skeletal Hierarchy Fundamentals

1. **Root bone** — Base of hierarchy, controls entire character position
2. **Spine chain** — Pelvis → spine bones → chest, supports torso bending
3. **Limb chains** — Shoulder → upper arm → forearm → hand (3-bone IK chains)
4. **Extremities** — Fingers, toes, facial bones
5. **Helper bones** — Twist bones, corrective bones, cloth bones

### Bone Naming Conventions

**Standard Naming:**
- **Left/Right prefix**: `L_` or `R_` (e.g., `L_Shoulder`, `R_Wrist`)
- **Center bones**: `C_` or no prefix (e.g., `C_Spine01`, `Root`)
- **Descriptive names**: `UpperArm`, `Forearm`, `Hand`, `Index01`, etc.
- **Consistent casing**: CamelCase or snake_case throughout

**Example Hierarchy:**
```
Root
├── C_Pelvis
│   ├── C_Spine01
│   │   ├── C_Spine02
│   │   │   ├── C_Spine03
│   │   │   │   ├── C_Neck
│   │   │   │   │   └── C_Head
│   │   │   │   ├── L_Clavicle
│   │   │   │   │   └── L_UpperArm
│   │   │   │   │       └── L_Forearm
│   │   │   │   │           └── L_Hand
│   │   │   │   └── R_Clavicle (mirror)
│   ├── L_Thigh
│   │   └── L_Calf
│   │       └── L_Foot
│   │           └── L_Toes
│   └── R_Thigh (mirror)
```

## Rigging Pipeline Stages

### Stage 1: Skeleton Creation

**Bone Placement:**
- Position bones at joint centers
- Align bones with limb direction
- Use reference anatomy for accuracy
- Mirror left/right sides
- Set proper bone roll/orientation

**Joint Orientation:**
- X-axis: Bone length direction (typically)
- Y-axis: Bend direction (elbow, knee)
- Z-axis: Twist direction
- Consistent orientation critical for animation

### Stage 2: IK/FK Systems

**FK (Forward Kinematics):**
- Direct bone rotation
- Parent-child hierarchy
- Good for: Arms swinging, spine bending, overlapping motion
- Simple, predictable, animator-friendly

**IK (Inverse Kinematics):**
- Goal-driven positioning
- Solve chain to reach target
- Good for: Feet planted, hands grabbing objects, precise positioning
- Complex but powerful

**IK/FK Blending:**
- Switch between IK and FK modes
- Blend slider (0 = FK, 1 = IK)
- Essential for professional rigs
- Allows animator flexibility

### Stage 3: Weight Painting

**Skinning Process:**
- Bind mesh to skeleton
- Paint vertex weights (influence per bone)
- Smooth weight transitions
- Test deformation in poses
- Iterate and refine

**Weight Painting Best Practices:**
- Start with automatic weights, refine manually
- Smooth gradients at joints
- 100% total weight per vertex
- Limit bone influences (2-4 bones per vertex)
- Test extreme poses

### Stage 4: Constraints and Controls

**Common Constraints:**
- **Aim/Look At**: Eyes track target, head follows
- **Parent**: Dynamic parent switching
- **Pole Vector**: Control IK bend direction
- **Copy Rotation/Location**: Mirror or follow other bones
- **Limit**: Restrict bone rotation/position ranges

**Control Rig:**
- Separate control objects from deformation bones
- Animator manipulates controls, not bones directly
- Custom shapes for controls (circles, boxes, arrows)
- Color-coded controls (left = red, right = blue, center = yellow)
- Organized control hierarchy

### Stage 5: Facial Rigging

**Facial Rig Components:**
- Jaw bone for mouth opening
- Eye bones for eye rotation
- Blend shapes for expressions
- Bone-driven blend shapes
- Eyelid and brow controls

**Blend Shape Integration:**
- Create blend shape targets
- Link to control sliders
- Combine multiple blend shapes
- Test expression combinations

### Stage 6: Testing and Refinement

**Test Poses:**
- Neutral pose (T-pose or A-pose)
- Extreme joint bends (90°, 135°)
- Combination poses (squat, reach, twist)
- Facial expressions
- Animation cycles (walk, run)

**Common Issues:**
- Pinching at joints → Add corrective blend shapes
- Volume loss → Adjust weights, add twist bones
- Flipping → Fix bone orientation, pole vectors
- Gimbal lock → Adjust rotation order

## Software and Tools

### Primary Rigging Software

| Software | Strengths | Best For |
|----------|-----------|----------|
| Maya | Industry standard, robust tools | Film, AAA games, professional production |
| Blender | Free, Rigify addon, good tools | Indie games, learning, full pipeline |
| 3ds Max | CAT rig, Biped system | Game development, motion capture |
| MotionBuilder | Real-time rigging, mocap | Motion capture, animation retargeting |

### Rigging Tools and Plugins

**Maya:**
- Advanced Skeleton: Auto-rigging system
- mGear: Modular rigging framework
- Red9: Animation and rigging tools
- Comet: Rigging and animation scripts

**Blender:**
- Rigify: Automatic rig generation
- Auto-Rig Pro: Commercial auto-rigging
- BlenRig: Advanced character rig
- CloudRig: Modular rigging system

**3ds Max:**
- CAT (Character Animation Toolkit): Built-in rigging
- Biped: Humanoid rigging system
- Custom Attribute Manager: Control creation

## Best Practices

### Rig Organization

1. **Layer system** — Separate deformation bones, controls, helpers
2. **Naming consistency** — Follow strict naming conventions
3. **Color coding** — Visual organization of controls
4. **Hierarchy clarity** — Clean, logical bone structure
5. **Documentation** — Notes on rig features and usage

### Performance Optimization

**For Games:**
- Minimize bone count (30-80 bones typical)
- Limit bone influences per vertex (2-4)
- Avoid complex constraints
- Optimize for real-time evaluation
- Test in target engine early

**For Film:**
- More bones acceptable (100-200+)
- Complex control systems allowed
- Focus on animator usability
- Render-time evaluation acceptable

### Animation-Friendly Rigs

1. **Intuitive controls** — Easy to understand and manipulate
2. **Predictable behavior** — No unexpected flipping or popping
3. **Flexible systems** — IK/FK blending, space switching
4. **Visual feedback** — Control shapes indicate function
5. **Animator input** — Get feedback from animators during development

## Common Challenges and Solutions

### Challenge: Joint Pinching

**Solution**: Add twist bones between joints, use corrective blend shapes, refine weight painting with smoother gradients.

### Challenge: Shoulder Deformation

**Solution**: Implement clavicle bone, add shoulder helper bones, create corrective blend shapes for arm raise, use dual quaternion skinning.

### Challenge: Spine Flexibility vs. Control

**Solution**: Use 3-5 spine bones for flexibility, add IK spline for easy posing, provide FK controls for detailed animation, implement stretchy spine option.

### Challenge: Foot Roll and Toe Control

**Solution**: Create reverse foot rig with heel, toe, and ball pivots, add foot roll attribute, implement toe curl and spread controls.

## Using the Reference Files

### When to Read Each Reference

**`/references/game-rigging.md`** — Read when creating rigs for game engines, optimizing bone counts, setting up for real-time animation, or exporting to Unity/Unreal.

**`/references/film-rigging.md`** — Read when building complex control rigs for film, implementing advanced constraint systems, or creating animator-friendly interfaces.

**`/references/facial-rigging.md`** — Read when rigging faces for dialogue and expressions, setting up blend shape systems, or creating eye and jaw controls.

**`/references/advanced-systems.md`** — Read when implementing IK/FK blending, creating twist bone systems, building custom rigging tools, or rigging non-humanoid characters.
