---
name: realitykit-ar
description: "Build augmented reality experiences with RealityKit and ARKit on iOS. Use when adding 3D content with RealityView, loading entities and models, placing objects via raycasting, configuring AR camera sessions, handling world tracking, scene understanding, or implementing entity interactions and gestures."
---

# RealityKit + ARKit

Build AR experiences on iOS using RealityKit for rendering and ARKit for world
tracking. Covers `RealityView`, entity management, raycasting, scene
understanding, and gesture-based interactions. Targets Swift 6.2 / iOS 26+.

## Contents

- [Setup](#setup)
- [RealityView Basics](#realityview-basics)
- [Loading and Creating Entities](#loading-and-creating-entities)
- [Anchoring and Placement](#anchoring-and-placement)
- [Raycasting](#raycasting)
- [Gestures and Interaction](#gestures-and-interaction)
- [Scene Understanding](#scene-understanding)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

### Project Configuration

1. Add `NSCameraUsageDescription` to Info.plist
2. For iOS, RealityKit uses the device camera by default via `RealityViewCameraContent` (iOS 18+, macOS 15+)
3. No additional capabilities required for basic AR on iOS

### Device Requirements

AR features require devices with an A9 chip or later. Always verify support
before presenting AR UI.

```swift
import ARKit

guard ARWorldTrackingConfiguration.isSupported else {
    showUnsupportedDeviceMessage()
    return
}
```

### Key Types

| Type | Platform | Role |
|---|---|---|
| `RealityView` | iOS 18+, visionOS 1+ | SwiftUI view that hosts RealityKit content |
| `RealityViewCameraContent` | iOS 18+, macOS 15+ | Content displayed through the device camera |
| `Entity` | All | Base class for all scene objects |
| `ModelEntity` | All | Entity with a visible 3D model |
| `AnchorEntity` | All | Tethers entities to a real-world anchor |

## RealityView Basics

`RealityView` is the SwiftUI entry point for RealityKit. On iOS, it provides
`RealityViewCameraContent` which renders through the device camera for AR.

```swift
import SwiftUI
import RealityKit

struct ARExperienceView: View {
    var body: some View {
        RealityView { content in
            // content is RealityViewCameraContent on iOS
            let sphere = ModelEntity(
                mesh: .generateSphere(radius: 0.05),
                materials: [SimpleMaterial(
                    color: .blue,
                    isMetallic: true
                )]
            )
            sphere.position = [0, 0, -0.5]  // 50cm in front of camera
            content.add(sphere)
        }
    }
}
```

### Make and Update Pattern

Use the `update` closure to respond to SwiftUI state changes:

```swift
struct PlacementView: View {
    @State private var modelColor: UIColor = .red

    var body: some View {
        RealityView { content in
            let box = ModelEntity(
                mesh: .generateBox(size: 0.1),
                materials: [SimpleMaterial(
                    color: .red,
                    isMetallic: false
                )]
            )
            box.name = "colorBox"
            box.position = [0, 0, -0.5]
            content.add(box)
        } update: { content in
            if let box = content.entities.first(
                where: { $0.name == "colorBox" }
            ) as? ModelEntity {
                box.model?.materials = [SimpleMaterial(
                    color: modelColor,
                    isMetallic: false
                )]
            }
        }

        Button("Change Color") {
            modelColor = modelColor == .red ? .green : .red
        }
    }
}
```

## Loading and Creating Entities

### Loading from USDZ Files

Load 3D models asynchronously to avoid blocking the main thread:

```swift
RealityView { content in
    if let robot = try? await ModelEntity(named: "robot") {
        robot.position = [0, -0.2, -0.8]
        robot.scale = [0.01, 0.01, 0.01]
        content.add(robot)
    }
}
```

### Programmatic Mesh Generation

```swift
// Box
let box = ModelEntity(
    mesh: .generateBox(size: [0.1, 0.2, 0.1], cornerRadius: 0.005),
    materials: [SimpleMaterial(color: .gray, isMetallic: true)]
)

// Sphere
let sphere = ModelEntity(
    mesh: .generateSphere(radius: 0.05),
    materials: [SimpleMaterial(color: .blue, roughness: 0.2, isMetallic: true)]
)

// Plane
let plane = ModelEntity(
    mesh: .generatePlane(width: 0.3, depth: 0.3),
    materials: [SimpleMaterial(color: .green, isMetallic: false)]
)
```

### Adding Components

Entities use an ECS (Entity Component System) architecture. Add components
to give entities behavior:

```swift
let box = ModelEntity(
    mesh: .generateBox(size: 0.1),
    materials: [SimpleMaterial(color: .red, isMetallic: false)]
)

// Make it respond to physics
box.components.set(PhysicsBodyComponent(
    massProperties: .default,
    material: .default,
    mode: .dynamic
))

// Add collision shape for interaction
box.components.set(CollisionComponent(
    shapes: [.generateBox(size: [0.1, 0.1, 0.1])]
))

// Enable input targeting for gestures
box.components.set(InputTargetComponent())
```

## Anchoring and Placement

### AnchorEntity

Use `AnchorEntity` to anchor content to detected surfaces or world positions:

```swift
RealityView { content in
    // Anchor to a horizontal surface
    let floorAnchor = AnchorEntity(.plane(
        .horizontal,
        classification: .floor,
        minimumBounds: [0.2, 0.2]
    ))

    let model = ModelEntity(
        mesh: .generateBox(size: 0.1),
        materials: [SimpleMaterial(color: .orange, isMetallic: false)]
    )
    floorAnchor.addChild(model)
    content.add(floorAnchor)
}
```

### Anchor Targets

| Target | Description |
|---|---|
| `.plane(.horizontal, ...)` | Horizontal surfaces (floors, tables) |
| `.plane(.vertical, ...)` | Vertical surfaces (walls) |
| `.plane(.any, ...)` | Any detected plane |
| `.world(transform:)` | Fixed world-space position |

## Raycasting

Use `RealityViewCameraContent` to convert between SwiftUI view coordinates
and RealityKit world space. Pair with `SpatialTapGesture` to place objects
where the user taps on a detected surface.

## Gestures and Interaction

### Drag Gesture on Entities

```swift
struct DraggableARView: View {
    var body: some View {
        RealityView { content in
            let box = ModelEntity(
                mesh: .generateBox(size: 0.1),
                materials: [SimpleMaterial(color: .blue, isMetallic: true)]
            )
            box.position = [0, 0, -0.5]
            box.components.set(CollisionComponent(
                shapes: [.generateBox(size: [0.1, 0.1, 0.1])]
            ))
            box.components.set(InputTargetComponent())
            box.name = "draggable"
            content.add(box)
        }
        .gesture(
            DragGesture()
                .targetedToAnyEntity()
                .onChanged { value in
                    let entity = value.entity
                    guard let parent = entity.parent else { return }
                    entity.position = value.convert(
                        value.location3D,
                        from: .local,
                        to: parent
                    )
                }
        )
    }
}
```

### Tap to Select

```swift
.gesture(
    SpatialTapGesture()
        .targetedToAnyEntity()
        .onEnded { value in
            let tappedEntity = value.entity
            highlightEntity(tappedEntity)
        }
)
```

## Scene Understanding

### Per-Frame Updates

Subscribe to scene update events for continuous processing:

```swift
RealityView { content in
    let entity = ModelEntity(
        mesh: .generateSphere(radius: 0.05),
        materials: [SimpleMaterial(color: .yellow, isMetallic: false)]
    )
    entity.position = [0, 0, -0.5]
    content.add(entity)

    _ = content.subscribe(to: SceneEvents.Update.self) { event in
        let time = Float(event.deltaTime)
        entity.position.y += sin(Float(Date().timeIntervalSince1970)) * time * 0.1
    }
}
```

### visionOS Note

On visionOS, ARKit provides a different API surface with `ARKitSession`,
`WorldTrackingProvider`, and `PlaneDetectionProvider`. These visionOS-specific
types are not available on iOS. On iOS, RealityKit handles world tracking
automatically through `RealityViewCameraContent`.

## Common Mistakes

### DON'T: Skip AR capability checks

Not all devices support AR. Showing a black camera view with no feedback
confuses users.

```swift
// WRONG -- no device check
struct MyARView: View {
    var body: some View {
        RealityView { content in
            // Fails silently on unsupported devices
        }
    }
}

// CORRECT -- check support and show fallback
struct MyARView: View {
    var body: some View {
        if ARWorldTrackingConfiguration.isSupported {
            RealityView { content in
                // AR content
            }
        } else {
            ContentUnavailableView(
                "AR Not Supported",
                systemImage: "arkit",
                description: Text("This device does not support AR.")
            )
        }
    }
}
```

### DON'T: Load heavy models synchronously

Loading large USDZ files on the main thread causes frame drops and hangs.
The `make` closure of `RealityView` is `async` -- use it.

```swift
// WRONG -- synchronous load blocks the main thread
RealityView { content in
    let model = try! Entity.load(named: "large-scene")
    content.add(model)
}

// CORRECT -- async load
RealityView { content in
    if let model = try? await ModelEntity(named: "large-scene") {
        content.add(model)
    }
}
```

### DON'T: Forget collision and input target components for interactive entities

Gestures only work on entities that have both `CollisionComponent` and
`InputTargetComponent`. Without them, taps and drags pass through.

```swift
// WRONG -- entity ignores gestures
let box = ModelEntity(mesh: .generateBox(size: 0.1))
content.add(box)

// CORRECT -- add collision and input components
let box = ModelEntity(
    mesh: .generateBox(size: 0.1),
    materials: [SimpleMaterial(color: .red, isMetallic: false)]
)
box.components.set(CollisionComponent(
    shapes: [.generateBox(size: [0.1, 0.1, 0.1])]
))
box.components.set(InputTargetComponent())
content.add(box)
```

### DON'T: Create new entities in the update closure

The `update` closure runs on every SwiftUI state change. Creating entities
there duplicates content on each render pass.

```swift
// WRONG -- duplicates entities on every state change
RealityView { content in
    // empty
} update: { content in
    let sphere = ModelEntity(mesh: .generateSphere(radius: 0.05))
    content.add(sphere)  // Added again on every update
}

// CORRECT -- create in make, modify in update
RealityView { content in
    let sphere = ModelEntity(mesh: .generateSphere(radius: 0.05))
    sphere.name = "mySphere"
    content.add(sphere)
} update: { content in
    if let sphere = content.entities.first(
        where: { $0.name == "mySphere" }
    ) as? ModelEntity {
        // Modify existing entity
        sphere.position.y = newYPosition
    }
}
```

### DON'T: Ignore camera permission

RealityKit on iOS needs camera access. If the user denies permission, the
view shows a black screen with no explanation.

```swift
// WRONG -- no permission handling
RealityView { content in
    // Black screen if camera denied
}

// CORRECT -- check and request permission
struct ARContainerView: View {
    @State private var cameraAuthorized = false

    var body: some View {
        Group {
            if cameraAuthorized {
                RealityView { content in
                    // AR content
                }
            } else {
                ContentUnavailableView(
                    "Camera Access Required",
                    systemImage: "camera.fill",
                    description: Text("Enable camera in Settings to use AR.")
                )
            }
        }
        .task {
            let status = AVCaptureDevice.authorizationStatus(for: .video)
            if status == .authorized {
                cameraAuthorized = true
            } else if status == .notDetermined {
                cameraAuthorized = await AVCaptureDevice
                    .requestAccess(for: .video)
            }
        }
    }
}
```

## Review Checklist

- [ ] `NSCameraUsageDescription` set in Info.plist
- [ ] AR device capability checked before presenting AR views
- [ ] Camera permission requested and denial handled with a fallback UI
- [ ] 3D models loaded asynchronously in the `make` closure
- [ ] Entities created in `make`, modified in `update` (not created in `update`)
- [ ] Interactive entities have both `CollisionComponent` and `InputTargetComponent`
- [ ] Collision shapes match the visual size of the entity
- [ ] `SceneEvents.Update` subscriptions used for per-frame logic (not SwiftUI timers)
- [ ] Large scenes use `ModelEntity(named:)` async loading, not `Entity.load(named:)`
- [ ] Anchor entities target appropriate surface types for the use case
- [ ] Entity names set for lookup in the `update` closure

## References

- Extended patterns (physics, animations, lighting, ECS): `references/realitykit-patterns.md`
- [RealityKit framework](https://sosumi.ai/documentation/realitykit)
- [RealityView](https://sosumi.ai/documentation/realitykit/realityview)
- [RealityViewCameraContent](https://sosumi.ai/documentation/realitykit/realityviewcameracontent)
- [Entity](https://sosumi.ai/documentation/realitykit/entity)
- [ModelEntity](https://sosumi.ai/documentation/realitykit/modelentity)
- [AnchorEntity](https://sosumi.ai/documentation/realitykit/anchorentity)
- [ARKit framework](https://sosumi.ai/documentation/arkit)
- [ARKit in iOS](https://sosumi.ai/documentation/arkit/arkit-in-ios)
- [ARWorldTrackingConfiguration](https://sosumi.ai/documentation/arkit/arworldtrackingconfiguration)
- [Loading entities from a file](https://sosumi.ai/documentation/realitykit/loading-entities-from-a-file)
