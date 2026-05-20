---
name: augmented-reality-tracking
description: Tracking and registration fundamentals for augmented reality. Covers the six classes of tracking (marker, markerless, inertial, SLAM, outside-in, inside-out), registration error sources (calibration, latency, drift, distortion), the Azuma definition of AR, display configurations (optical see-through, video see-through, projection, handheld), and the interaction between tracking precision and user perception of "being there." Use when designing AR experiences, diagnosing registration issues, or selecting tracking technology.
type: skill
category: spatial-computing
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/spatial-computing/augmented-reality-tracking/SKILL.md
superseded_by: null
---
# Augmented Reality Tracking

Augmented reality succeeds or fails on registration — the precise alignment of virtual content with the physical world. A perfectly rendered virtual object floating six inches from where it should be is worse than no augmentation at all. This skill catalogs the tracking techniques, error sources, and design heuristics that determine whether AR content feels anchored to reality or simply pasted over it.

**Agent affinity:** azuma (registration, tracking, AR definition), sutherland (first HMD), furness (head tracking and displays)

**Concept IDs:** spatial-coordinate-navigation, spatial-reasoning-3d, spatial-signal-propagation

## The Azuma Definition of AR

Azuma (1997) defined AR as any system that:

1. Combines real and virtual
2. Is interactive in real time
3. Is registered in 3D

This is the minimum bar. Systems that meet fewer than all three are not AR in the technical sense — a video feed with overlaid text is not AR (not 3D-registered); a prerendered overlay is not AR (not real-time); a VR headset is not AR (no real content). The definition scopes what this skill addresses.

## Tracking Classes

| Class | Mechanism | Precision | Range | Cost | Failure modes |
|---|---|---|---|---|---|
| Marker-based | Recognized fiducial (ARTag, ARUCO, QR) | High | Line-of-sight to marker | Low | Occlusion, lighting |
| Markerless feature | Track natural features (corners, edges) | Medium-high | Feature-rich scenes | Medium | Textureless surfaces |
| Inertial (IMU) | Gyroscope + accelerometer | Medium (drifts) | Unlimited | Low | Drift over seconds |
| SLAM | Simultaneous localization and mapping | Medium-high | Unlimited | High | Dynamic scenes, low texture |
| Outside-in | External cameras watch trackers | Very high | Room-scale | High | Occlusion, range |
| Inside-out | Cameras on HMD watch environment | High | Unlimited | Medium | Feature loss in empty rooms |

Most modern AR uses a combination: visual-inertial SLAM combines IMU (high frequency, drifts slowly) with visual features (lower frequency, no drift) to get the best of both.

## Sources of Registration Error

Getting the virtual object to appear in the right place in the real world is hard because errors compound across the pipeline. Azuma identified six major sources:

1. **Optical distortion** — lenses distort the view; the distortion must be measured and compensated.
2. **Tracker error** — the tracker's estimate of pose has some uncertainty.
3. **Mechanical misalignment** — cameras, displays, and trackers are not perfectly aligned on the headset.
4. **Tracker-to-eye error** — the tracker measures the headset position, but the user's eye is somewhere else; the offset must be calibrated per user.
5. **Latency** — the time between the tracker reading and the rendered frame. At 100ms latency and 1 m/s head motion, content is 10 cm off.
6. **Incorrect calibration** — any parameter that is wrong (lens curvature, IPD, camera extrinsics) propagates through all the above.

### Latency is the dominant problem

For handheld AR (phones and tablets), static latency of 50ms is tolerable because the world moves slowly relative to the frame. For HMD AR, latency under 20ms is usually required for content to feel anchored. Higher frame rates (90-120 Hz) and predictive tracking help but do not eliminate the problem.

## Display Configurations

Different AR hardware configurations trade off transparency, field of view, brightness, and social presence.

### Optical see-through (OST)

Real world passes through a partially reflective combiner. Virtual content is projected into the optical path. Advantages: real world is unmediated, no camera latency. Disadvantages: virtual content cannot occlude real content, low contrast in bright conditions, narrow field of view in current hardware.

### Video see-through (VST)

Real world is captured by cameras and composited with virtual content on a display. Advantages: virtual content can fully occlude real content, color correction possible. Disadvantages: all real content suffers camera latency, limited dynamic range, resolution cap.

### Projection

Virtual content is projected onto real surfaces. Advantages: users do not need to wear headsets, many users can see the same augmentation. Disadvantages: surfaces must be prepared, projectors need line of sight, content is geometry-dependent.

### Handheld (phone/tablet)

Most common AR today. The device is both sensor and display. Advantages: ubiquitous hardware, low friction, easy sharing. Disadvantages: user must hold the device, small field of view, one-handed operation.

## Registration Design Heuristics

Given that registration is never perfect, how should designers mitigate the consequences?

### Tolerate drift in anchored content

If the virtual object is allowed to drift slightly when the user is not looking at it, errors can be smoothed. Looking away and back "re-anchors" content at the current pose estimate.

### Use natural fiducials

Tables, corners, and walls are usually stable and texture-rich. Content anchored to these tends to register better than content floating in empty space.

### Shadow grounding

A virtual object casting a shadow on a real surface is more convincingly placed than one floating without a shadow. Even approximate shadows help.

### Contact-rich placement

Content that touches multiple real surfaces (a virtual chair whose legs all contact the floor) is registered using multiple constraints. If any leg is off, the user notices.

### Hide occlusion mismatches

In OST systems that cannot occlude, design content that does not require occlusion for interpretation. Holographic-style ghosting is a common style choice.

## AR vs Mixed Reality vs Extended Reality

Industry terminology has proliferated:

- **AR** — Azuma's definition; real world is primary, virtual is overlay
- **MR** — usually means AR with mutual interaction (virtual objects react to real geometry)
- **VR** — real world is replaced, virtual is primary
- **XR** — umbrella term for all of the above

These terms are marketed aggressively and used loosely. This skill uses Azuma's strict definition of AR and notes where extensions (occlusion, physics interaction, shared multi-user) apply.

## When to Use This Skill

- Designing AR applications with specific registration requirements
- Selecting tracking hardware for a use case
- Diagnosing registration drift, jitter, or misalignment
- Explaining AR limitations to stakeholders or users

## When NOT to Use This Skill

- Pure VR design (no registration to real world)
- Non-interactive overlay graphics (not AR by Azuma's definition)
- Hardware selection for pure 3D scanning (use a photogrammetry skill)

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Ignoring latency budget | Content lags head motion, user notices | Target 20ms or below for HMD |
| Testing only in ideal lighting | SLAM fails in real use | Test in diverse lighting |
| Assuming markers work everywhere | Occlusion, distance, angle fail them | Add markerless fallback |
| Not calibrating per user | IPD and eye offset vary | Provide a calibration step |
| Placing content mid-air without anchors | Nothing to register against, drift obvious | Anchor to natural fiducials |
| Ignoring occlusion mismatch in OST | Ghostly content, breaks illusion | Design for the display type |

## Cross-References

- **azuma agent:** Registration, tracking, and AR foundational survey
- **sutherland agent:** First head-mounted display, 1968
- **furness agent:** Military HMDs, Super Cockpit, high-stakes AR
- **3d-interaction-design skill:** Interaction techniques that AR applications use
- **immersive-environment-design skill:** Environment design for AR-compatible spaces

## References

- Azuma, R. (1997). "A survey of augmented reality." *Presence*, 6(4), 355-385.
- Azuma, R., Baillot, Y., Behringer, R., Feiner, S., Julier, S., & MacIntyre, B. (2001). "Recent advances in augmented reality." *IEEE CGA*, 21(6), 34-47.
- Milgram, P., & Kishino, F. (1994). "A taxonomy of mixed reality visual displays." *IEICE Transactions*, E77-D(12), 1321-1329.
- Sutherland, I. E. (1968). "A head-mounted three-dimensional display." *AFIPS '68 Fall Joint Computer Conference*.
- Welch, G., & Foxlin, E. (2002). "Motion tracking: no silver bullet." *IEEE CGA*, 22(6), 24-38.
