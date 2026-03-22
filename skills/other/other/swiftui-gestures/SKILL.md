---
name: swiftui-gestures
description: "Implement, review, or improve SwiftUI gesture handling. Use when adding tap, long press, drag, magnify, or rotate gestures, composing gestures with simultaneously/sequenced/exclusively, managing transient state with @GestureState, resolving parent/child gesture conflicts with highPriorityGesture or simultaneousGesture, building custom Gesture protocol conformances, or migrating from deprecated MagnificationGesture/RotationGesture to MagnifyGesture/RotateGesture."
---

# SwiftUI Gestures (iOS 26+)

Review, write, and fix SwiftUI gesture interactions. Apply modern gesture APIs
with correct composition, state management, and conflict resolution using
Swift 6.2 patterns.

## Contents

- [Gesture Overview](#gesture-overview)
- [TapGesture](#tapgesture)
- [LongPressGesture](#longpressgesture)
- [DragGesture](#draggesture)
- [MagnifyGesture (iOS 17+)](#magnifygesture-ios-17)
- [RotateGesture (iOS 17+)](#rotategesture-ios-17)
- [Gesture Composition](#gesture-composition)
- [@GestureState](#gesturestate)
- [Adding Gestures to Views](#adding-gestures-to-views)
- [Custom Gesture Protocol](#custom-gesture-protocol)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Gesture Overview

| Gesture | Type | Value | Since |
|---|---|---|---|
| `TapGesture` | Discrete | `Void` | iOS 13 |
| `LongPressGesture` | Discrete | `Bool` | iOS 13 |
| `DragGesture` | Continuous | `DragGesture.Value` | iOS 13 |
| `MagnifyGesture` | Continuous | `MagnifyGesture.Value` | iOS 17 |
| `RotateGesture` | Continuous | `RotateGesture.Value` | iOS 17 |
| `SpatialTapGesture` | Discrete | `SpatialTapGesture.Value` | iOS 16 |

**Discrete** gestures fire once (`.onEnded`). **Continuous** gestures stream
updates (`.onChanged`, `.onEnded`, `.updating`).

## TapGesture

Recognizes one or more taps. Use the `count` parameter for multi-tap.

```swift
// Single, double, and triple tap
TapGesture()            .onEnded { tapped.toggle() }
TapGesture(count: 2)    .onEnded { handleDoubleTap() }
TapGesture(count: 3)    .onEnded { handleTripleTap() }

// Shorthand modifier
Text("Tap me").onTapGesture(count: 2) { handleDoubleTap() }
```

## LongPressGesture

Succeeds after the user holds for `minimumDuration`. Fails if finger moves
beyond `maximumDistance`.

```swift
// Basic long press (0.5s default)
LongPressGesture()
    .onEnded { _ in showMenu = true }

// Custom duration and distance tolerance
LongPressGesture(minimumDuration: 1.0, maximumDistance: 10)
    .onEnded { _ in triggerHaptic() }
```

With visual feedback via `@GestureState` + `.updating()`:

```swift
@GestureState private var isPressing = false

Circle()
    .fill(isPressing ? .red : .blue)
    .scaleEffect(isPressing ? 1.2 : 1.0)
    .gesture(
        LongPressGesture(minimumDuration: 0.8)
            .updating($isPressing) { current, state, _ in state = current }
            .onEnded { _ in completedLongPress = true }
    )
```

Shorthand: `.onLongPressGesture(minimumDuration:perform:onPressingChanged:)`.

## DragGesture

Tracks finger movement. `Value` provides `startLocation`, `location`,
`translation`, `velocity`, and `predictedEndTranslation`.

```swift
@State private var offset = CGSize.zero

RoundedRectangle(cornerRadius: 16)
    .fill(.blue)
    .frame(width: 100, height: 100)
    .offset(offset)
    .gesture(
        DragGesture()
            .onChanged { value in offset = value.translation }
            .onEnded { _ in withAnimation(.spring) { offset = .zero } }
    )
```

Configure minimum distance and coordinate space:

```swift
DragGesture(minimumDistance: 20, coordinateSpace: .global)
```

## MagnifyGesture (iOS 17+)

Replaces the deprecated `MagnificationGesture`. Tracks pinch-to-zoom scale.

```swift
@GestureState private var magnifyBy = 1.0

Image("photo")
    .resizable().scaledToFit()
    .scaleEffect(magnifyBy)
    .gesture(
        MagnifyGesture()
            .updating($magnifyBy) { value, state, _ in
                state = value.magnification
            }
    )
```

With persisted scale:

```swift
@State private var currentScale = 1.0
@GestureState private var gestureScale = 1.0

Image("photo")
    .scaleEffect(currentScale * gestureScale)
    .gesture(
        MagnifyGesture(minimumScaleDelta: 0.01)
            .updating($gestureScale) { value, state, _ in state = value.magnification }
            .onEnded { value in
                currentScale = min(max(currentScale * value.magnification, 0.5), 5.0)
            }
    )
```

## RotateGesture (iOS 17+)

Replaces the deprecated `RotationGesture`. Tracks two-finger rotation angle.

```swift
@State private var angle = Angle.zero

Rectangle()
    .fill(.blue).frame(width: 200, height: 200)
    .rotationEffect(angle)
    .gesture(
        RotateGesture(minimumAngleDelta: .degrees(1))
            .onChanged { value in angle = value.rotation }
    )
```

With persisted rotation:

```swift
@State private var currentAngle = Angle.zero
@GestureState private var gestureAngle = Angle.zero

Rectangle()
    .rotationEffect(currentAngle + gestureAngle)
    .gesture(
        RotateGesture()
            .updating($gestureAngle) { value, state, _ in state = value.rotation }
            .onEnded { value in currentAngle += value.rotation }
    )
```

## Gesture Composition

### `.simultaneously(with:)` — both gestures recognized at the same time

```swift
let magnify = MagnifyGesture()
    .onChanged { value in scale = value.magnification }

let rotate = RotateGesture()
    .onChanged { value in angle = value.rotation }

Image("photo")
    .scaleEffect(scale)
    .rotationEffect(angle)
    .gesture(magnify.simultaneously(with: rotate))
```

The value is `SimultaneousGesture.Value` with `.first` and `.second` optionals.

### `.sequenced(before:)` — first must succeed before second begins

```swift
let longPressBeforeDrag = LongPressGesture(minimumDuration: 0.5)
    .sequenced(before: DragGesture())
    .onEnded { value in
        guard case .second(true, let drag?) = value else { return }
        finalOffset.width += drag.translation.width
        finalOffset.height += drag.translation.height
    }
```

### `.exclusively(before:)` — only one succeeds (first has priority)

```swift
let doubleTapOrLongPress = TapGesture(count: 2)
    .map { ExclusiveResult.doubleTap }
    .exclusively(before:
        LongPressGesture()
            .map { _ in ExclusiveResult.longPress }
    )
    .onEnded { result in
        switch result {
        case .first(let val): handleDoubleTap()
        case .second(let val): handleLongPress()
        }
    }
```

## @GestureState

`@GestureState` is a property wrapper that **automatically resets** to its
initial value when the gesture ends. Use for transient feedback; use `@State`
for values that persist.

```swift
@GestureState private var dragOffset = CGSize.zero  // resets to .zero
@State private var position = CGSize.zero            // persists

Circle()
    .offset(
        x: position.width + dragOffset.width,
        y: position.height + dragOffset.height
    )
    .gesture(
        DragGesture()
            .updating($dragOffset) { value, state, _ in
                state = value.translation
            }
            .onEnded { value in
                position.width += value.translation.width
                position.height += value.translation.height
            }
    )
```

Custom reset with animation: `@GestureState(resetTransaction: Transaction(animation: .spring))`

## Adding Gestures to Views

Three modifiers control gesture priority in the view hierarchy:

| Modifier | Behavior |
|---|---|
| `.gesture()` | Default priority. Child gestures win over parent. |
| `.highPriorityGesture()` | Parent gesture takes precedence over child. |
| `.simultaneousGesture()` | Both parent and child gestures fire. |

```swift
// Problem: parent tap swallows child tap
VStack {
    Button("Child") { handleChild() }  // never fires
}
.gesture(TapGesture().onEnded { handleParent() })

// Fix 1: Use simultaneousGesture on parent
VStack {
    Button("Child") { handleChild() }
}
.simultaneousGesture(TapGesture().onEnded { handleParent() })

// Fix 2: Give parent explicit priority
VStack {
    Text("Child")
        .gesture(TapGesture().onEnded { handleChild() })
}
.highPriorityGesture(TapGesture().onEnded { handleParent() })
```

### GestureMask

Control which gestures participate when using `.gesture(_:including:)`:

```swift
.gesture(drag, including: .gesture)   // only this gesture, not subviews
.gesture(drag, including: .subviews)  // only subview gestures
.gesture(drag, including: .all)       // default: this + subviews
```

## Custom Gesture Protocol

Create reusable gestures by conforming to `Gesture`:

```swift
struct SwipeGesture: Gesture {
    enum Direction { case left, right, up, down }
    let minimumDistance: CGFloat
    let onSwipe: (Direction) -> Void

    init(minimumDistance: CGFloat = 50, onSwipe: @escaping (Direction) -> Void) {
        self.minimumDistance = minimumDistance
        self.onSwipe = onSwipe
    }

    var body: some Gesture {
        DragGesture(minimumDistance: minimumDistance)
            .onEnded { value in
                let h = value.translation.width, v = value.translation.height
                if abs(h) > abs(v) {
                    onSwipe(h > 0 ? .right : .left)
                } else {
                    onSwipe(v > 0 ? .down : .up)
                }
            }
    }
}

// Usage
Rectangle().gesture(SwipeGesture { print("Swiped \($0)") })
```

Wrap in a `View` extension for ergonomic API:

```swift
extension View {
    func onSwipe(perform action: @escaping (SwipeGesture.Direction) -> Void) -> some View {
        gesture(SwipeGesture(onSwipe: action))
    }
}
```

## Common Mistakes

### 1. Conflicting parent/child gestures

```swift
// DON'T: Parent .gesture() conflicts with child tap
VStack {
    Button("Action") { doSomething() }
}
.gesture(TapGesture().onEnded { parentAction() })

// DO: Use .simultaneousGesture() or .highPriorityGesture()
VStack {
    Button("Action") { doSomething() }
}
.simultaneousGesture(TapGesture().onEnded { parentAction() })
```

### 2. Using @State instead of @GestureState for transient state

```swift
// DON'T: @State doesn't auto-reset — view stays offset after gesture ends
@State private var dragOffset = CGSize.zero

DragGesture()
    .onChanged { value in dragOffset = value.translation }
    .onEnded { _ in dragOffset = .zero }  // manual reset required

// DO: @GestureState auto-resets when gesture ends
@GestureState private var dragOffset = CGSize.zero

DragGesture()
    .updating($dragOffset) { value, state, _ in
        state = value.translation
    }
```

### 3. Not using .updating() for intermediate feedback

```swift
// DON'T: No visual feedback during long press
LongPressGesture(minimumDuration: 2.0)
    .onEnded { _ in showResult = true }

// DO: Provide feedback while pressing
@GestureState private var isPressing = false

LongPressGesture(minimumDuration: 2.0)
    .updating($isPressing) { current, state, _ in
        state = current
    }
    .onEnded { _ in showResult = true }
```

### 4. Using deprecated gesture types on iOS 17+

```swift
// DON'T: Deprecated since iOS 17
MagnificationGesture()   // deprecated
RotationGesture()        // deprecated

// DO: Use modern replacements
MagnifyGesture()         // iOS 17+
RotateGesture()          // iOS 17+
```

### 5. Heavy computation in onChanged

```swift
// DON'T: Expensive work called every frame (~60-120 Hz)
DragGesture()
    .onChanged { value in
        let result = performExpensiveHitTest(at: value.location)
        let filtered = applyComplexFilter(result)
        updateModel(filtered)
    }

// DO: Throttle or defer expensive work
DragGesture()
    .onChanged { value in
        dragPosition = value.location  // lightweight state update only
    }
    .onEnded { value in
        performExpensiveHitTest(at: value.location)  // once at end
    }
```

## Review Checklist

- [ ] Correct gesture type: `MagnifyGesture`/`RotateGesture` (not deprecated `Magnification`/`Rotation` variants)
- [ ] `@GestureState` used for transient values that should reset; `@State` for persisted values
- [ ] `.updating()` provides intermediate visual feedback during continuous gestures
- [ ] Parent/child conflicts resolved with `.highPriorityGesture()` or `.simultaneousGesture()`
- [ ] `onChanged` closures are lightweight — no heavy computation every frame
- [ ] Composed gestures use correct combinator: `simultaneously`, `sequenced`, or `exclusively`
- [ ] Persisted scale/rotation clamped to reasonable bounds in `onEnded`
- [ ] Custom `Gesture` conformances use `var body: some Gesture` (not `View`)
- [ ] Gesture-driven animations use `.spring` or similar for natural deceleration
- [ ] `GestureMask` considered when mixing gestures across view hierarchy levels

## References

- See `references/gesture-patterns.md` for drag-to-reorder, pinch-to-zoom, combined rotate+scale, velocity calculations, and SwiftUI/UIKit gesture interop.
- [Gesture protocol](https://sosumi.ai/documentation/swiftui/gesture)
- [TapGesture](https://sosumi.ai/documentation/swiftui/tapgesture)
- [LongPressGesture](https://sosumi.ai/documentation/swiftui/longpressgesture)
- [DragGesture](https://sosumi.ai/documentation/swiftui/draggesture)
- [MagnifyGesture](https://sosumi.ai/documentation/swiftui/magnifygesture)
- [RotateGesture](https://sosumi.ai/documentation/swiftui/rotategesture)
- [GestureState](https://sosumi.ai/documentation/swiftui/gesturestate)
- [Composing SwiftUI gestures](https://sosumi.ai/documentation/swiftui/composing-swiftui-gestures)
- [Adding interactivity with gestures](https://sosumi.ai/documentation/swiftui/adding-interactivity-with-gestures)
