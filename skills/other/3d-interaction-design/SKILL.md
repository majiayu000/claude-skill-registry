---
name: 3d-interaction-design
description: Design heuristics for three-dimensional interaction — input modalities (6DoF controllers, gaze, gesture, voice), selection and manipulation techniques (ray-cast, virtual hand, go-go, world-in-miniature), navigation (teleport, continuous, redirected walking), and feedback loops (haptic, audio, visual). Covers Fitts' law in 3D, discoverability vs affordance, safe-zone design, and comfort/simulator sickness mitigation. Use when designing VR/AR interactions, immersive walkthroughs, or any input system where the user's body is the controller.
type: skill
category: spatial-computing
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/spatial-computing/3d-interaction-design/SKILL.md
superseded_by: null
---
# 3D Interaction Design

Interaction in three dimensions is fundamentally different from interaction in two. Every designer trained on windows and cursors must unlearn assumptions about planar layout, pixel-precise pointing, and implicit desktop context. This skill catalogs the major input modalities, selection and manipulation techniques, navigation metaphors, and feedback strategies, with heuristics for when each applies.

**Agent affinity:** bret-victor (direct manipulation and feedback), sutherland (input device foundations), krueger (gestural and responsive interaction)

**Concept IDs:** spatial-reasoning-3d, spatial-coordinate-navigation, spatial-iterative-build-process

## Input Modalities

| Modality | Degrees of freedom | Precision | Fatigue | Best for |
|---|---|---|---|---|
| 6DoF controller | 6 per hand | High | Low | VR manipulation, precise placement |
| Gaze | 2 (direction) | Medium | Low | Targeting, dwell-select |
| Gesture (free-hand) | Variable | Medium-low | High | Expressive, social, short sessions |
| Voice | Symbolic | High (recognition) | None | Labeling, commands, dictation |
| Eye tracking | 2 | High | None | Foveated rendering, implicit targeting |
| Brain-computer | Symbolic | Very low | Variable | Research, accessibility |
| Props / tangibles | Varies | High | Low | Authoring, haptic grounding |

The designer's first decision is which modality or combination the interaction will use. Voice plus gaze is a common accessibility-friendly pair. 6DoF plus audio is a common VR game pair. Gesture plus projected video is Krueger's VIDEOPLACE legacy.

## Selection Techniques

Selecting an object in 3D is the precursor to manipulating it. The difficulty depends on distance, occlusion, density of candidates, and input modality.

### Ray-cast (pointing)

Cast a ray from the controller (or from the head) into the scene. The first intersected object is the candidate. Simple, familiar, works at arbitrary distance. Fails when candidates are densely packed or partially occluded.

### Virtual hand

The user's hand (represented by a 3D model) reaches into the scene and touches the object. Direct, tangible, satisfying. Limited by arm length.

### Go-go

Extends the virtual hand nonlinearly as the user reaches further. Close objects use 1:1 mapping; distant objects get amplified reach. Popularized by Poupyrev et al. 1996.

### World-in-miniature (WIM)

Present a small replica of the scene in the user's hand. Selecting in the miniature selects the corresponding object in the full scene. Excellent for selecting occluded or distant objects.

### Image-plane selection

Treat the user's hand as if it were projecting onto a 2D plane at arm's length. Selection becomes 2D pointing in a virtual window. Easier precision, loses depth cues.

## Manipulation Techniques

Once selected, the object must be moved, rotated, scaled, or otherwise transformed.

### 6DoF translate-rotate

Attach the object to the controller transform. Intuitive, fast, but constrained by the user's physical reach. Standard in VR building tools.

### Widget-based

Display manipulation widgets (arrows for translation, rings for rotation) around the selected object. Precision improves, exploration slows.

### Constrained manipulation

Lock the object to a grid, a plane, or an axis. Essential for building tasks where alignment matters. Trades freedom for precision.

### Two-handed manipulation

Use both hands to specify transformations: distance between hands for scale, vector between hands for orientation. Natural for symmetric tasks.

## Navigation Techniques

Moving through a 3D environment is its own interaction problem, distinct from object manipulation.

### Teleport

Point to a destination; the user's position jumps there. Comfortable (no vection), discontinuous (breaks immersion). Standard for comfort-first VR.

### Continuous (thumbstick)

Smooth locomotion via thumbstick. Immersive, cinematic, but causes simulator sickness in a meaningful fraction of users. Mitigation: blinders, low field-of-view during motion.

### Redirected walking

Subtly rotate the virtual environment so the user walks in physical circles while believing they are walking in a straight line in the virtual environment. Allows large virtual spaces in small rooms. Requires careful calibration.

### World-in-miniature navigation

Grab and drag the miniature to reposition. Used in architectural walkthroughs.

### Portal

Step through a portal to move to a distant location. Narratively expressive, spatially discontinuous.

## Fitts' Law in 3D

Fitts' law (1954) relates selection time to target distance and size: MT = a + b log2(D/W + 1). In 3D, W must be generalized to the smallest angular dimension of the target from the user's viewpoint, and D is path length through 3D space. The implications for designers:

- Large targets are easier. Minimum touchable target in VR is about 2-3 cm at arm's length.
- Distance matters more than in 2D because the user's hand must actually move through physical space.
- Depth occlusion adds cost. A target behind another requires rotation or navigation before selection.

## Feedback Design

Feedback closes the loop between user action and system response. Without feedback, the user does not know whether the interaction succeeded.

### Visual

Highlight the target on hover. Show the trajectory of a thrown object. Animate the manipulation in real time. Use motion blur or trails to indicate velocity.

### Audio

Play a click on selection. Play a whoosh on fast movement. Play a clunk when an object lands on a surface. Spatial audio cues direction.

### Haptic

Vibrate the controller on contact. Increase vibration intensity with resistance. Use haptic patterns to distinguish events (short pulse for selection, long rumble for impact).

### Proprioceptive

Align virtual hand with physical hand position. When the two diverge (because the virtual object was released or because collision overrode the transform), the user gets a subtle mismatch cue that something changed.

## Comfort and Simulator Sickness

Visual-vestibular mismatch causes simulator sickness. The common triggers:

- Continuous locomotion without head movement
- Sudden acceleration or deceleration
- Low frame rate (under 90 Hz)
- High field of view during motion
- Camera shake or roll

Mitigations: teleport, comfort vignettes, stable horizon lines, reduced FoV during movement, 90 Hz minimum, seated modes for longer sessions.

## When to Use This Skill

- Designing VR/AR applications where the user's body is the primary input
- Reviewing 3D interfaces for discoverability, comfort, and efficiency
- Choosing selection/manipulation/navigation techniques for a specific task shape
- Diagnosing user complaints about difficulty, fatigue, or nausea

## When NOT to Use This Skill

- Pure 2D UI design
- Screen-based 3D (Unity Editor, CAD tools on a desktop) where the input is mouse/keyboard
- Non-interactive 3D rendering

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Porting 2D widgets into 3D unchanged | Widgets overlap, occlude, fail to afford 3D use | Redesign for 3D placement and scale |
| Small distant targets | Fitts penalty compounds with hand movement | Enlarge or use WIM |
| No feedback on selection | User cannot tell if tap registered | Always provide multi-modal feedback |
| Continuous locomotion without comfort options | Fraction of users get sick | Offer teleport as primary, continuous as opt-in |
| Gesture without discoverability | Users do not know what gestures exist | Provide a tutorial and on-demand cheat sheet |
| Ignoring fatigue in free-hand interfaces | Gorilla arm after 5 minutes | Allow arm rest, add input alternatives |

## Cross-References

- **sutherland agent:** History of input devices, from Sketchpad's light pen onward
- **bret-victor agent:** Direct-manipulation principles and feedback immediacy
- **krueger agent:** Responsive environments and gestural input lineage
- **furness agent:** Military and medical VR, high-stakes interaction
- **azuma agent:** AR registration and tracking that underlies interaction precision
- **immersive-environment-design skill:** Environment design that sets the stage for interaction

## References

- Sutherland, I. E. (1968). "A head-mounted three-dimensional display." *AFIPS Proceedings*, 33, 757-764.
- Fitts, P. M. (1954). "The information capacity of the human motor system." *Journal of Experimental Psychology*, 47(6), 381-391.
- Poupyrev, I., Billinghurst, M., Weghorst, S., & Ichikawa, T. (1996). "The go-go interaction technique." *UIST '96*.
- Bowman, D. A., Kruijff, E., LaViola, J. J., & Poupyrev, I. (2005). *3D User Interfaces: Theory and Practice*. Addison-Wesley.
- Razzaque, S., Kohn, Z., & Whitton, M. (2001). "Redirected walking." *Eurographics 2001*.
