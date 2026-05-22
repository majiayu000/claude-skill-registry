---
name: swiftui-animation
description: "Implement, review, or improve SwiftUI animations and transitions. Use when adding explicit animations with withAnimation, configuring implicit animations with .animation(_:body:) or .animation(_:value:), configuring spring animations (.smooth, .snappy, .bouncy), building phase or keyframe animations with PhaseAnimator/KeyframeAnimator, creating hero transitions with matchedGeometryEffect or matchedTransitionSource, adding SF Symbol effects (bounce, pulse, variableColor, breathe, rotate, wiggle), implementing custom Transition or CustomAnimation types, or ensuring animations respect accessibilityReduceMotion."
---

# SwiftUI Animation (iOS 26+)

Review, write, and fix SwiftUI animations. Apply modern animation APIs with
correct timing, transitions, and accessibility handling using Swift 6.2 patterns.

## Contents

- [Triage Workflow](#triage-workflow)
- [withAnimation (Explicit Animation)](#withanimation-explicit-animation)
- [Implicit Animation](#implicit-animation)
- [Spring Type (iOS 17+)](#spring-type-ios-17)
- [PhaseAnimator (iOS 17+)](#phaseanimator-ios-17)
- [KeyframeAnimator (iOS 17+)](#keyframeanimator-ios-17)
- [@Animatable Macro](#animatable-macro)
- [matchedGeometryEffect (iOS 14+)](#matchedgeometryeffect-ios-14)
- [Navigation Zoom Transition (iOS 18+)](#navigation-zoom-transition-ios-18)
- [Transitions (iOS 17+)](#transitions-ios-17)
- [ContentTransition (iOS 16+)](#contenttransition-ios-16)
- [Symbol Effects (iOS 17+)](#symbol-effects-ios-17)
- [Symbol Rendering Modes](#symbol-rendering-modes)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Triage Workflow

### Step 1: Identify the animation category

| Category | API | When to use |
|---|---|---|
| State-driven | `withAnimation`, `.animation(_:body:)`, `.animation(_:value:)` | Explicit state changes, selective modifier animation, or simple value-bound changes |
| Multi-phase | `PhaseAnimator` | Sequenced multi-step animations |
| Keyframe | `KeyframeAnimator` | Complex multi-property choreography |
| Shared element | `matchedGeometryEffect` | Layout-driven hero transitions |
| Navigation | `matchedTransitionSource` + `.navigationTransition(.zoom)` | NavigationStack push/pop zoom |
| View lifecycle | `.transition()` | Insertion and removal |
| Text content | `.contentTransition()` | In-place text/number changes |
| Symbol | `.symbolEffect()` | SF Symbol animations |
| Custom | `CustomAnimation` protocol | Novel timing curves |

### Step 2: Choose the animation curve

```swift
// Timing curves
.linear                              // constant speed
.easeIn(duration: 0.3)              // slow start
.easeOut(duration: 0.3)             // slow end
.easeInOut(duration: 0.3)           // slow start and end

// Spring presets (preferred for natural motion)
.smooth                              // no bounce, fluid
.smooth(duration: 0.5, extraBounce: 0.0)
.snappy                              // small bounce, responsive
.snappy(duration: 0.4, extraBounce: 0.1)
.bouncy                              // visible bounce, playful
.bouncy(duration: 0.5, extraBounce: 0.2)

// Custom spring
.spring(duration: 0.5, bounce: 0.3, blendDuration: 0.0)
.spring(Spring(duration: 0.6, bounce: 0.2), blendDuration: 0.0)
.interactiveSpring(response: 0.15, dampingFraction: 0.86)
```

### Step 3: Apply and verify

- Confirm animation triggers on the correct state change.
- Test with Accessibility > Reduce Motion enabled.
- Verify no expensive work runs inside animation content closures.

## withAnimation (Explicit Animation)

```swift
withAnimation(.spring) { isExpanded.toggle() }

// With completion (iOS 17+)
withAnimation(.smooth(duration: 0.35), completionCriteria: .logicallyComplete) {
    isExpanded = true
} completion: { loadContent() }
```

## Implicit Animation

Prefer `.animation(_:body:)` when only specific modifiers should animate.
Use `.animation(_:value:)` for simple value-bound changes that can animate the
view's animatable modifiers together.

```swift
Badge()
    .foregroundStyle(isActive ? .green : .secondary)
    .animation(.snappy) { content in
        content
            .scaleEffect(isActive ? 1.15 : 1.0)
            .opacity(isActive ? 1.0 : 0.7)
    }
```

```swift
Circle()
    .scaleEffect(isActive ? 1.2 : 1.0)
    .opacity(isActive ? 1.0 : 0.6)
    .animation(.bouncy, value: isActive)
```

## Spring Type (iOS 17+)

Four initializer forms for different mental models.

```swift
// Perceptual (preferred)
Spring(duration: 0.5, bounce: 0.3)

// Physical
Spring(mass: 1.0, stiffness: 100.0, damping: 10.0)

// Response-based
Spring(response: 0.5, dampingRatio: 0.7)

// Settling-based
Spring(settlingDuration: 1.0, dampingRatio: 0.8)
```

Three presets mirror Animation presets: `.smooth`, `.snappy`, `.bouncy`.

## PhaseAnimator (iOS 17+)

Cycle through discrete phases with per-phase animation curves.

```swift
enum PulsePhase: CaseIterable {
    case idle, grow, shrink
}

struct PulsingDot: View {
    var body: some View {
        PhaseAnimator(PulsePhase.allCases) { phase in
            Circle()
                .frame(width: 40, height: 40)
                .scaleEffect(phase == .grow ? 1.4 : 1.0)
                .opacity(phase == .shrink ? 0.5 : 1.0)
        } animation: { phase in
            switch phase {
            case .idle: .easeIn(duration: 0.2)
            case .grow: .spring(duration: 0.4, bounce: 0.3)
            case .shrink: .easeOut(duration: 0.3)
            }
        }
    }
}
```

Trigger-based variant runs one cycle per trigger change:

```swift
PhaseAnimator(PulsePhase.allCases, trigger: tapCount) { phase in
    // ...
} animation: { _ in .spring(duration: 0.4) }
```

## KeyframeAnimator (iOS 17+)

Animate multiple properties along independent timelines.

```swift
struct AnimValues {
    var scale: Double = 1.0
    var yOffset: Double = 0.0
    var opacity: Double = 1.0
}

struct BounceView: View {
    @State private var trigger = false

    var body: some View {
        Image(systemName: "star.fill")
            .font(.largeTitle)
            .keyframeAnimator(
                initialValue: AnimValues(),
                trigger: trigger
            ) { content, value in
                content
                    .scaleEffect(value.scale)
                    .offset(y: value.yOffset)
                    .opacity(value.opacity)
            } keyframes: { _ in
                KeyframeTrack(\.scale) {
                    SpringKeyframe(1.5, duration: 0.3)
                    CubicKeyframe(1.0, duration: 0.4)
                }
                KeyframeTrack(\.yOffset) {
                    CubicKeyframe(-30, duration: 0.2)
                    CubicKeyframe(0, duration: 0.4)
                }
                KeyframeTrack(\.opacity) {
                    LinearKeyframe(0.6, duration: 0.15)
                    LinearKeyframe(1.0, duration: 0.25)
                }
            }
            .onTapGesture { trigger.toggle() }
    }
}
```

Keyframe types: `LinearKeyframe` (linear), `CubicKeyframe` (smooth curve),
`SpringKeyframe` (spring physics), `MoveKeyframe` (instant jump).

Use `repeating: true` for looping keyframe animations.

## @Animatable Macro

Replaces manual `AnimatableData` boilerplate. Attach to any type with
animatable stored properties.

```swift
// WRONG: Manual AnimatableData (verbose, error-prone)
struct WaveShape: Shape, Animatable {
    var frequency: Double
    var amplitude: Double
    var phase: Double

    var animatableData: AnimatablePair<Double, AnimatablePair<Double, Double>> {
        get { AnimatablePair(frequency, AnimatablePair(amplitude, phase)) }
        set {
            frequency = newValue.first
            amplitude = newValue.second.first
            phase = newValue.second.second
        }
    }
    // ...
}

// CORRECT: @Animatable macro synthesizes animatableData
@Animatable
struct WaveShape: Shape {
    var frequency: Double
    var amplitude: Double
    var phase: Double
    @AnimatableIgnored var lineWidth: CGFloat

    func path(in rect: CGRect) -> Path {
        // draw wave using frequency, amplitude, phase
    }
}
```

Rules:
- Stored properties must conform to `VectorArithmetic`.
- Use `@AnimatableIgnored` to exclude non-animatable properties.
- Computed properties are never included.

## matchedGeometryEffect (iOS 14+)

Synchronize geometry between views for shared-element animations.

```swift
struct HeroView: View {
    @Namespace private var heroSpace
    @State private var isExpanded = false

    var body: some View {
        if isExpanded {
            DetailCard()
                .matchedGeometryEffect(id: "card", in: heroSpace)
                .onTapGesture {
                    withAnimation(.spring(duration: 0.4, bounce: 0.2)) {
                        isExpanded = false
                    }
                }
        } else {
            ThumbnailCard()
                .matchedGeometryEffect(id: "card", in: heroSpace)
                .onTapGesture {
                    withAnimation(.spring(duration: 0.4, bounce: 0.2)) {
                        isExpanded = true
                    }
                }
        }
    }
}
```

Exactly one view per ID must be visible at a time for the interpolation to work.

## Navigation Zoom Transition (iOS 18+)

Pair `matchedTransitionSource` on the source view with
`.navigationTransition(.zoom(...))` on the destination.

```swift
struct GalleryView: View {
    @Namespace private var zoomSpace
    let items: [GalleryItem]

    var body: some View {
        NavigationStack {
            ScrollView {
                LazyVGrid(columns: [GridItem(.adaptive(minimum: 100))]) {
                    ForEach(items) { item in
                        NavigationLink {
                            GalleryDetail(item: item)
                                .navigationTransition(
                                    .zoom(sourceID: item.id, in: zoomSpace)
                                )
                        } label: {
                            ItemThumbnail(item: item)
                                .matchedTransitionSource(
                                    id: item.id, in: zoomSpace
                                )
                        }
                    }
                }
            }
        }
    }
}
```

Apply `.navigationTransition` on the destination view, not on inner containers.

## Transitions (iOS 17+)

Control how views animate on insertion and removal.

```swift
if showBanner {
    BannerView()
        .transition(.move(edge: .top).combined(with: .opacity))
}
```

Built-in types: `.opacity`, `.slide`, `.scale`, `.scale(_:anchor:)`,
`.move(edge:)`, `.push(from:)`, `.offset(x:y:)`, `.identity`,
`.blurReplace`, `.blurReplace(_:)`, `.symbolEffect`,
`.symbolEffect(_:options:)`.

Asymmetric transitions:

```swift
.transition(.asymmetric(
    insertion: .push(from: .bottom),
    removal: .opacity
))
```

## ContentTransition (iOS 16+)

Animate in-place content changes without insertion/removal.

```swift
Text("\(score)")
    .contentTransition(.numericText(countsDown: false))
    .animation(.snappy, value: score)

// For SF Symbols
Image(systemName: isMuted ? "speaker.slash" : "speaker.wave.3")
    .contentTransition(.symbolEffect(.replace.downUp))
```

Types: `.identity`, `.interpolate`, `.opacity`,
`.numericText(countsDown:)`, `.numericText(value:)`, `.symbolEffect`.

## Symbol Effects (iOS 17+)

Animate SF Symbols with semantic effects.

```swift
// Discrete (triggers on value change)
Image(systemName: "bell.fill")
    .symbolEffect(.bounce, value: notificationCount)

Image(systemName: "arrow.clockwise")
    .symbolEffect(.wiggle.clockwise, value: refreshCount)

// Indefinite (active while condition holds)
Image(systemName: "wifi")
    .symbolEffect(.pulse, isActive: isSearching)

Image(systemName: "mic.fill")
    .symbolEffect(.breathe, isActive: isRecording)

// Variable color with chaining
Image(systemName: "speaker.wave.3.fill")
    .symbolEffect(
        .variableColor.iterative.reversing.dimInactiveLayers,
        options: .repeating,
        isActive: isPlaying
    )
```

All effects: `.bounce`, `.pulse`, `.variableColor`, `.scale`, `.appear`,
`.disappear`, `.replace`, `.breathe`, `.rotate`, `.wiggle`.

Scope: `.byLayer`, `.wholeSymbol`. Direction varies per effect.

## Symbol Rendering Modes

Control how SF Symbol layers are colored with `.symbolRenderingMode(_:)`.

| Mode | Effect | When to use |
|------|--------|-------------|
| `.monochrome` | Single color applied uniformly (default) | Toolbars, simple icons matching text |
| `.hierarchical` | Single color with opacity layers for depth | Subtle depth without multiple colors |
| `.multicolor` | System-defined fixed colors per layer | Weather, file types — Apple's intended palette |
| `.palette` | Custom colors per layer via `.foregroundStyle` | Brand colors, custom multi-color icons |

```swift
// Hierarchical — single tint, opacity layers for depth
Image(systemName: "speaker.wave.3.fill")
    .symbolRenderingMode(.hierarchical)
    .foregroundStyle(.blue)

// Palette — custom color per layer
Image(systemName: "person.crop.circle.badge.plus")
    .symbolRenderingMode(.palette)
    .foregroundStyle(.blue, .green)

// Multicolor — system-defined colors
Image(systemName: "cloud.sun.rain.fill")
    .symbolRenderingMode(.multicolor)
```

**Variable color:** `.symbolVariableColor(value:)` for percentage-based fill (signal strength, volume):

```swift
Image(systemName: "wifi")
    .symbolVariableColor(value: signalStrength) // 0.0–1.0
```

> **Docs:** [SymbolRenderingMode](https://sosumi.ai/documentation/swiftui/symbolrenderingmode) · [symbolRenderingMode(_:)](https://sosumi.ai/documentation/swiftui/view/symbolrenderingmode(_:))

## Common Mistakes

### 1. Using bare `.animation(_:)` when you need precise scope

```swift
// TOO BROAD — applies when the view changes
.animation(.easeIn)

// CORRECT — bind animation to one value
.animation(.easeIn, value: isVisible)

// CORRECT — scope animation to selected modifiers
.animation(.easeIn) { content in
    content.opacity(isVisible ? 1.0 : 0.0)
}
```

### 2. Expensive work inside animation closures

Never run heavy computation in `keyframeAnimator` / `PhaseAnimator` content closures — they execute every frame. Precompute outside, animate only visual properties.

### 3. Missing reduce motion support

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion
withAnimation(reduceMotion ? .none : .bouncy) { showDetail = true }
```

### 4. Multiple matchedGeometryEffect sources

Only one view per ID should be visible at a time. Two visible views with the same ID causes undefined layout.

### 5. Using DispatchQueue or UIView.animate

```swift
// WRONG
DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) { withAnimation { isVisible = true } }
// CORRECT
withAnimation(.spring.delay(0.5)) { isVisible = true }
```

### 6. Forgetting animation on ContentTransition

```swift
// WRONG — no animation, content transition has no effect
Text("\(count)").contentTransition(.numericText(countsDown: true))
// CORRECT — pair with animation
Text("\(count)")
    .contentTransition(.numericText(countsDown: true))
    .animation(.snappy, value: count)
```

### 7. navigationTransition on wrong view

Apply `.navigationTransition(.zoom(sourceID:in:))` on the outermost destination view, not inside a container.

## Review Checklist

- [ ] Animation curve matches intent (spring for natural, ease for mechanical)
- [ ] `withAnimation` wraps the state change; implicit animation uses `.animation(_:body:)` for selective modifier scope or `.animation(_:value:)` with an explicit value
- [ ] `matchedGeometryEffect` has exactly one source per ID; zoom uses matching `id`/`namespace`
- [ ] `@Animatable` macro used instead of manual `animatableData`
- [ ] `accessibilityReduceMotion` checked; no `DispatchQueue`/`UIView.animate`
- [ ] Transitions use `.transition()`; `contentTransition` is paired with animation and uses the narrowest implicit animation scope that fits
- [ ] Animated state changes on @MainActor; animation-driving types are Sendable

## References

- See `references/animation-advanced.md` for CustomAnimation protocol, full Spring variants, all Transition types, symbol effect details, Transaction system, UnitCurve types, and performance guidance.
