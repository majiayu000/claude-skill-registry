---
name: visionos-spatial
description: visionOS spatial computing fundamentals for Vision Pro, including windows, volumes, immersive spaces, RealityKit integration, spatial gestures, and cross-platform spatial patterns. Use when user asks about visionOS, Vision Pro, spatial computing, RealityKit, immersive spaces, 3D UI, or mixed reality development.
allowed-tools: Bash, Read, Write, Edit
---

# visionOS Spatial Computing

Fundamentals of visionOS development for Apple Vision Pro, including windows, volumes, immersive spaces, and spatial UI patterns.

## Prerequisites

- Xcode 26+ with visionOS SDK
- visionOS Simulator or Apple Vision Pro
- RealityKit familiarity helpful

---

## App Structure Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    visionOS APP HIERARCHY                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WINDOW          Standard 2D SwiftUI window in 3D space     │
│      ↓                                                       │
│  VOLUME          3D content in a bounded container          │
│      ↓                                                       │
│  IMMERSIVE SPACE Full/mixed reality, unbounded 3D           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Windows

### Basic Window

```swift
import SwiftUI

@main
struct MyVisionApp: App {
    var body: some Scene {
        // Standard window - floats in space
        WindowGroup {
            ContentView()
        }
        .windowStyle(.automatic)  // Glass material
    }
}

struct ContentView: View {
    var body: some View {
        NavigationStack {
            List {
                NavigationLink("Photos", destination: PhotosView())
                NavigationLink("Videos", destination: VideosView())
            }
            .navigationTitle("My Content")
        }
    }
}
```

### Window Sizing

```swift
WindowGroup {
    ContentView()
}
// Default size (points)
.defaultSize(width: 800, height: 600)

// With depth for 3D content
.defaultSize(width: 800, height: 600, depth: 400)

// Size constraints
.windowResizability(.contentSize)
```

### Plain Window Style

```swift
WindowGroup {
    // No glass material, fully custom
    CustomBackgroundView()
}
.windowStyle(.plain)
```

---

## Volumes

### Basic Volume

```swift
@main
struct VolumetricApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        // Volumetric window for 3D content
        WindowGroup(id: "globe") {
            GlobeView()
        }
        .windowStyle(.volumetric)
        .defaultSize(width: 0.5, height: 0.5, depth: 0.5, in: .meters)
    }
}

struct GlobeView: View {
    var body: some View {
        Model3D(named: "Earth") { model in
            model
                .resizable()
                .scaledToFit()
        } placeholder: {
            ProgressView()
        }
    }
}

// Open volume from window
struct ContentView: View {
    @Environment(\.openWindow) private var openWindow

    var body: some View {
        Button("Show Globe") {
            openWindow(id: "globe")
        }
    }
}
```

### RealityKit in Volume

```swift
import RealityKit

struct RealityKitVolume: View {
    var body: some View {
        RealityView { content in
            // Load 3D model
            if let model = try? await Entity.load(named: "Robot") {
                content.add(model)

                // Apply animation
                if let animation = model.availableAnimations.first {
                    model.playAnimation(animation.repeat())
                }
            }
        } update: { content in
            // Update on state changes
        }
        .gesture(
            TapGesture()
                .targetedToAnyEntity()
                .onEnded { value in
                    // Handle tap on entity
                    print("Tapped: \(value.entity)")
                }
        )
    }
}
```

---

## Immersive Spaces

### Space Types

```swift
@main
struct ImmersiveApp: App {
    @State private var immersionStyle: ImmersionStyle = .mixed

    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        // Immersive space
        ImmersiveSpace(id: "immersive") {
            ImmersiveView()
        }
        .immersionStyle(selection: $immersionStyle, in: .mixed, .progressive, .full)
    }
}

/*
 Immersion Styles:
 - .mixed: Content blends with passthrough (default)
 - .progressive: User controls passthrough dimming
 - .full: Complete immersion, no passthrough
*/
```

### Opening/Closing Spaces

```swift
struct ContentView: View {
    @Environment(\.openImmersiveSpace) private var openImmersiveSpace
    @Environment(\.dismissImmersiveSpace) private var dismissImmersiveSpace
    @State private var isImmersed = false

    var body: some View {
        VStack {
            Toggle("Immersive Mode", isOn: $isImmersed)
        }
        .onChange(of: isImmersed) { _, newValue in
            Task {
                if newValue {
                    let result = await openImmersiveSpace(id: "immersive")
                    if case .error = result {
                        isImmersed = false
                    }
                } else {
                    await dismissImmersiveSpace()
                }
            }
        }
    }
}
```

### Immersive View with Anchors

```swift
import RealityKit
import ARKit

struct ImmersiveView: View {
    @State private var session = ARKitSession()
    @State private var worldTracking = WorldTrackingProvider()

    var body: some View {
        RealityView { content in
            // Add content anchored to world
            let floor = ModelEntity(
                mesh: .generatePlane(width: 10, depth: 10),
                materials: [SimpleMaterial(color: .gray.withAlphaComponent(0.3), isMetallic: false)]
            )
            floor.position = [0, 0, 0]
            content.add(floor)

        } update: { content in
            // Update based on tracking
        }
        .task {
            // Start ARKit session
            do {
                try await session.run([worldTracking])
            } catch {
                print("ARKit session failed: \(error)")
            }
        }
    }
}
```

---

## Spatial Gestures

### Tap Gesture

```swift
struct TappableModel: View {
    @State private var tapped = false

    var body: some View {
        RealityView { content in
            let sphere = ModelEntity(
                mesh: .generateSphere(radius: 0.1),
                materials: [SimpleMaterial(color: .blue, isMetallic: true)]
            )
            sphere.components.set(InputTargetComponent())
            sphere.components.set(CollisionComponent(shapes: [.generateSphere(radius: 0.1)]))
            sphere.name = "sphere"
            content.add(sphere)
        }
        .gesture(
            TapGesture()
                .targetedToEntity(named: "sphere")
                .onEnded { _ in
                    tapped.toggle()
                }
        )
    }
}
```

### Drag Gesture (Move Objects)

```swift
struct DraggableObject: View {
    @State private var position: SIMD3<Float> = [0, 1, -2]

    var body: some View {
        RealityView { content in
            let cube = ModelEntity(
                mesh: .generateBox(size: 0.2),
                materials: [SimpleMaterial(color: .orange, isMetallic: false)]
            )
            cube.position = position
            cube.components.set(InputTargetComponent(allowedInputTypes: .indirect))
            cube.components.set(CollisionComponent(shapes: [.generateBox(size: [0.2, 0.2, 0.2])]))
            cube.name = "cube"
            content.add(cube)
        } update: { content in
            if let cube = content.entities.first(where: { $0.name == "cube" }) {
                cube.position = position
            }
        }
        .gesture(
            DragGesture()
                .targetedToEntity(named: "cube")
                .onChanged { value in
                    position = value.convert(value.location3D, from: .local, to: .scene)
                }
        )
    }
}
```

### Rotation Gesture

```swift
struct RotatableModel: View {
    @State private var rotation: Rotation3D = .identity

    var body: some View {
        Model3D(named: "Trophy")
            .rotation3DEffect(rotation)
            .gesture(
                RotateGesture3D()
                    .onChanged { value in
                        rotation = value.rotation
                    }
            )
    }
}
```

### Magnify Gesture (Scale)

```swift
struct ScalableModel: View {
    @State private var scale: Double = 1.0

    var body: some View {
        Model3D(named: "Car")
            .scaleEffect(scale)
            .gesture(
                MagnifyGesture()
                    .onChanged { value in
                        scale = value.magnification
                    }
            )
    }
}
```

---

## Ornaments

### Window Ornaments

```swift
struct OrnamentedWindow: View {
    @State private var volume: Double = 0.5

    var body: some View {
        VideoPlayer()
            .ornament(attachmentAnchor: .scene(.bottom)) {
                // Playback controls below window
                HStack {
                    Button(action: {}) {
                        Image(systemName: "backward.fill")
                    }
                    Button(action: {}) {
                        Image(systemName: "play.fill")
                    }
                    Button(action: {}) {
                        Image(systemName: "forward.fill")
                    }

                    Slider(value: $volume)
                        .frame(width: 100)
                }
                .padding()
                .glassBackgroundEffect()
            }
    }
}
```

### Multiple Ornaments

```swift
struct MultiOrnamentView: View {
    var body: some View {
        MainContent()
            // Top ornament
            .ornament(attachmentAnchor: .scene(.top)) {
                Text("Title")
                    .font(.title)
                    .padding()
                    .glassBackgroundEffect()
            }
            // Side ornament
            .ornament(attachmentAnchor: .scene(.trailing)) {
                VStack {
                    Button("Option 1") {}
                    Button("Option 2") {}
                    Button("Option 3") {}
                }
                .padding()
                .glassBackgroundEffect()
            }
    }
}
```

---

## Hand Tracking

### ARKit Hand Tracking

```swift
import ARKit
import RealityKit

struct HandTrackingView: View {
    @State private var session = ARKitSession()
    @State private var handTracking = HandTrackingProvider()

    var body: some View {
        RealityView { content in
            // Add hand visualization entities
        } update: { content in
            // Update hand positions
        }
        .task {
            // Check authorization
            let authorization = await session.requestAuthorization(for: [.handTracking])
            guard authorization[.handTracking] == .allowed else { return }

            do {
                try await session.run([handTracking])

                // Process hand updates
                for await update in handTracking.anchorUpdates {
                    let hand = update.anchor

                    // Access joints
                    if let indexTip = hand.handSkeleton?.joint(.indexFingerTip) {
                        let position = hand.originFromAnchorTransform * indexTip.anchorFromJointTransform
                        // Use position
                    }
                }
            } catch {
                print("Hand tracking failed: \(error)")
            }
        }
    }
}
```

### Custom Hand Gestures

```swift
@Observable
class PinchDetector {
    var isPinching = false

    func update(hand: HandAnchor) {
        guard let skeleton = hand.handSkeleton else { return }

        let thumbTip = skeleton.joint(.thumbTip)
        let indexTip = skeleton.joint(.indexFingerTip)

        guard thumbTip.isTracked && indexTip.isTracked else { return }

        // Calculate distance between thumb and index
        let thumbPosition = hand.originFromAnchorTransform * thumbTip.anchorFromJointTransform
        let indexPosition = hand.originFromAnchorTransform * indexTip.anchorFromJointTransform

        let distance = simd_distance(
            thumbPosition.columns.3.xyz,
            indexPosition.columns.3.xyz
        )

        isPinching = distance < 0.02  // 2cm threshold
    }
}

extension simd_float4 {
    var xyz: SIMD3<Float> {
        SIMD3(x, y, z)
    }
}
```

---

## Spatial Audio

### Spatial Audio Entity

```swift
import RealityKit

struct SpatialAudioScene: View {
    var body: some View {
        RealityView { content in
            // Create audio source entity
            let audioEntity = Entity()
            audioEntity.position = [0, 1, -2]  // 2 meters in front

            // Add spatial audio component
            let audioResource = try? AudioFileResource.load(named: "ambient.mp3")
            if let resource = audioResource {
                let audioController = audioEntity.prepareAudio(resource)
                audioController.play()
            }

            // Configure spatial audio
            audioEntity.spatialAudio = SpatialAudioComponent(
                gain: 0.8,
                directivity: .beam(focus: 0.5)
            )

            content.add(audioEntity)
        }
    }
}
```

---

## Cross-Platform Patterns

### Shared Code with Platform Checks

```swift
struct CrossPlatformView: View {
    var body: some View {
        #if os(visionOS)
        VisionContentView()
        #elseif os(iOS)
        iOSContentView()
        #elseif os(macOS)
        macOSContentView()
        #endif
    }
}

// Shared model works everywhere
@Observable
class SharedViewModel {
    var items: [Item] = []

    func load() async {
        // Same business logic
    }
}
```

### Platform-Adaptive Layouts

```swift
struct AdaptiveGallery: View {
    let items: [GalleryItem]

    var body: some View {
        #if os(visionOS)
        // Spatial gallery
        LazyHGrid(rows: [GridItem(.adaptive(minimum: 200))]) {
            ForEach(items) { item in
                GalleryCard(item: item)
                    .frame(depth: 50)  // Add depth
            }
        }
        .ornament(attachmentAnchor: .scene(.bottom)) {
            GalleryControls()
        }
        #else
        // Flat gallery
        LazyVGrid(columns: [GridItem(.adaptive(minimum: 150))]) {
            ForEach(items) { item in
                GalleryCard(item: item)
            }
        }
        #endif
    }
}
```

### Shared RealityKit Experiences

```swift
// Works on iOS with ARKit and visionOS
struct ARExperience: View {
    var body: some View {
        RealityView { content in
            // Load shared 3D content
            if let model = try? await Entity.load(named: "SharedModel") {
                #if os(visionOS)
                // Position in front of user
                model.position = [0, 1.5, -1]
                #else
                // Position at detected surface (iOS AR)
                model.position = [0, 0, 0]
                #endif

                content.add(model)
            }
        }
    }
}
```

---

## Best Practices

### DO

```swift
// ✓ Start with windows, add immersion progressively
WindowGroup { ... }
ImmersiveSpace(id: "enhance") { ... }
    .immersionStyle(selection: $style, in: .mixed)

// ✓ Respect user's physical space
.defaultSize(width: 1, height: 0.8, depth: 0.5, in: .meters)

// ✓ Use glass materials for UI
.glassBackgroundEffect()

// ✓ Add collision for interactive entities
entity.components.set(CollisionComponent(shapes: [...]))
entity.components.set(InputTargetComponent())

// ✓ Provide ornaments for contextual UI
.ornament(attachmentAnchor: .scene(.bottom)) { ... }
```

### DON'T

```swift
// ✗ Don't go full immersion immediately
.immersionStyle(selection: .constant(.full), in: .full)

// ✗ Don't place content too close or far
position = [0, 1.5, -0.3]  // Too close!
position = [0, 1.5, -10]   // Too far!

// ✗ Don't ignore accessibility
// Always provide alternatives to spatial gestures

// ✗ Don't require precise gestures
// Make hit targets generous
```

### Comfort Guidelines

```
┌─────────────────────────────────────────────────────────────┐
│                    COMFORT ZONES                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  OPTIMAL DISTANCE     1-2 meters from user                  │
│  COMFORTABLE RANGE    0.5-4 meters                          │
│  CONTENT HEIGHT       Eye level (1.5m from ground)          │
│  FIELD OF VIEW        Avoid edges of vision                 │
│  MOTION              Minimize rapid movements               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Official Resources

- [visionOS Documentation](https://developer.apple.com/documentation/visionos)
- [RealityKit Documentation](https://developer.apple.com/documentation/realitykit)
- [Human Interface Guidelines - visionOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos)
- [WWDC23: Meet SwiftUI for spatial computing](https://developer.apple.com/videos/play/wwdc2023/10109/)
- [WWDC23: Build spatial experiences with RealityKit](https://developer.apple.com/videos/play/wwdc2023/10080/)
