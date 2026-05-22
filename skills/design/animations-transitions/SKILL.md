---
name: animations-transitions
description: SwiftUI animations, @Animatable macro, withAnimation, transitions, PhaseAnimator, KeyframeAnimator, and interactive motion design. Use when user asks about animations, transitions, @Animatable, withAnimation, spring animations, keyframes, or motion design.
allowed-tools: Bash, Read, Write, Edit
---

# SwiftUI Animations and Transitions

Comprehensive guide to SwiftUI animations, the new @Animatable macro (iOS 26), transitions, and motion design best practices for modern iOS development.

## Prerequisites

- iOS 17+ for PhaseAnimator/KeyframeAnimator
- iOS 26+ for @Animatable macro
- Xcode 26+

---

## @Animatable Macro (iOS 26 - NEW!)

### The Revolution in Custom Animations

iOS 26 introduces the `@Animatable` macro, eliminating the tedious boilerplate previously required for animating custom shapes and views.

### Before iOS 26 (Manual Approach)

```swift
// OLD WAY - Lots of boilerplate
struct PieSlice: Shape {
    var startAngle: Angle
    var endAngle: Angle

    // Manual animatableData implementation required
    var animatableData: AnimatablePair<Double, Double> {
        get {
            AnimatablePair(startAngle.radians, endAngle.radians)
        }
        set {
            startAngle = Angle(radians: newValue.first)
            endAngle = Angle(radians: newValue.second)
        }
    }

    func path(in rect: CGRect) -> Path {
        var path = Path()
        let center = CGPoint(x: rect.midX, y: rect.midY)
        let radius = min(rect.width, rect.height) / 2
        path.move(to: center)
        path.addArc(center: center, radius: radius,
                    startAngle: startAngle, endAngle: endAngle,
                    clockwise: false)
        path.closeSubpath()
        return path
    }
}
```

### After iOS 26 (With @Animatable)

```swift
// NEW WAY - Just add @Animatable
@Animatable
struct PieSlice: Shape {
    var startAngle: Angle
    var endAngle: Angle

    func path(in rect: CGRect) -> Path {
        var path = Path()
        let center = CGPoint(x: rect.midX, y: rect.midY)
        let radius = min(rect.width, rect.height) / 2
        path.move(to: center)
        path.addArc(center: center, radius: radius,
                    startAngle: startAngle, endAngle: endAngle,
                    clockwise: false)
        path.closeSubpath()
        return path
    }
}
```

### @AnimatableIgnored

Exclude properties from animation:

```swift
@Animatable
struct CustomShape: Shape {
    var animatedValue: CGFloat
    @AnimatableIgnored var staticConfiguration: Bool  // Not animated

    func path(in rect: CGRect) -> Path {
        // Use both values, but only animatedValue will animate
    }
}
```

### Supported Types for Animation

The @Animatable macro automatically handles:
- `CGFloat`, `Double`, `Float`
- `Angle`
- `CGSize`, `CGPoint`, `CGRect`
- `UnitPoint`
- `Color` (component interpolation)
- Custom types conforming to `VectorArithmetic`

### Complex Example with Multiple Properties

```swift
@Animatable
struct MorphingShape: Shape {
    var cornerRadius: CGFloat
    var insetAmount: CGFloat
    var rotation: Angle
    @AnimatableIgnored var fillColor: Color

    func path(in rect: CGRect) -> Path {
        let insetRect = rect.insetBy(dx: insetAmount, dy: insetAmount)
        var path = Path(roundedRect: insetRect, cornerRadius: cornerRadius)

        let transform = CGAffineTransform(rotationAngle: rotation.radians)
        return path.applying(transform)
    }
}

// Usage
struct MorphingView: View {
    @State private var isExpanded = false

    var body: some View {
        MorphingShape(
            cornerRadius: isExpanded ? 50 : 10,
            insetAmount: isExpanded ? 20 : 50,
            rotation: isExpanded ? .degrees(45) : .zero,
            fillColor: .blue
        )
        .fill(.blue)
        .frame(width: 200, height: 200)
        .onTapGesture {
            withAnimation(.spring(duration: 0.6, bounce: 0.3)) {
                isExpanded.toggle()
            }
        }
    }
}
```

---

## withAnimation

### Basic Usage

```swift
struct ContentView: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            Rectangle()
                .frame(width: isExpanded ? 200 : 100,
                       height: isExpanded ? 200 : 100)

            Button("Toggle") {
                withAnimation {
                    isExpanded.toggle()
                }
            }
        }
    }
}
```

### With Animation Type

```swift
withAnimation(.spring(duration: 0.5, bounce: 0.3)) {
    isExpanded.toggle()
}

withAnimation(.easeInOut(duration: 0.3)) {
    opacity = 1.0
}

withAnimation(.linear(duration: 1.0)) {
    progress = 1.0
}
```

### Completion Handler (iOS 17+)

```swift
withAnimation(.easeInOut(duration: 0.5)) {
    showDetails = true
} completion: {
    // Called when animation completes
    print("Animation finished")
    fetchMoreData()
}
```

### Nested Animations with Different Timings

```swift
Button("Animate") {
    withAnimation(.spring(duration: 0.4)) {
        isExpanded = true
    }

    withAnimation(.easeOut(duration: 0.6).delay(0.2)) {
        opacity = 1.0
    }
}
```

---

## Animation Types

### Built-in Animations

```swift
// Linear - constant speed
.linear(duration: 0.3)

// Ease variants - acceleration/deceleration
.easeIn(duration: 0.3)      // Slow start
.easeOut(duration: 0.3)     // Slow end
.easeInOut(duration: 0.3)   // Slow both

// Default (ease in/out)
.default
```

### Spring Animations (Modern)

```swift
// Modern spring with duration and bounce
.spring(duration: 0.5, bounce: 0.3)

// Bounce values:
// 0.0 = no bounce (critically damped)
// 0.5 = medium bounce
// 1.0 = maximum bounce (never settles)

// Extra bounce parameter for overshoot
.spring(duration: 0.5, bounce: 0.4, blendDuration: 0.2)
```

### Spring Presets

```swift
// Bouncy - playful, energetic
.bouncy
.bouncy(duration: 0.4, extraBounce: 0.1)

// Snappy - quick, responsive
.snappy
.snappy(duration: 0.3, extraBounce: 0.05)

// Smooth - gentle, elegant
.smooth
.smooth(duration: 0.5, extraBounce: 0.0)
```

### Interactive Spring

```swift
// For gesture-driven animations
.interactiveSpring()
.interactiveSpring(response: 0.3, dampingFraction: 0.7)

// Best for drag gestures
.interactiveSpring(response: 0.15, dampingFraction: 0.86, blendDuration: 0.25)
```

### Custom Timing Curves

```swift
// Bezier curve timing
.timingCurve(0.2, 0.8, 0.2, 1.0, duration: 0.5)

// Parameters: (x1, y1, x2, y2)
// Start: (0, 0), End: (1, 1)
// Control points define the curve shape
```

### Animation Modifiers

```swift
// Delay before starting
.spring().delay(0.2)

// Speed multiplier
.spring().speed(2.0)  // 2x faster

// Repeat
.linear(duration: 1.0).repeatCount(3)
.linear(duration: 1.0).repeatForever()

// Autoreverse
.easeInOut(duration: 0.5).repeatForever(autoreverses: true)
```

---

## Explicit Animation Modifier

### Preferred Approach

```swift
struct ContentView: View {
    @State private var scale = 1.0

    var body: some View {
        Circle()
            .scaleEffect(scale)
            // Explicit: animate only when scale changes
            .animation(.spring, value: scale)
            .onTapGesture {
                scale = scale == 1.0 ? 1.5 : 1.0
            }
    }
}
```

### Why Explicit is Better

```swift
// AVOID: Implicit animation (animates everything)
Circle()
    .animation(.spring)  // Deprecated warning in newer iOS

// PREFER: Explicit animation (precise control)
Circle()
    .animation(.spring, value: specificValue)
```

### Multiple Explicit Animations

```swift
struct MultiAnimatedView: View {
    @State private var scale = 1.0
    @State private var opacity = 1.0
    @State private var rotation = 0.0

    var body: some View {
        Rectangle()
            .scaleEffect(scale)
            .opacity(opacity)
            .rotationEffect(.degrees(rotation))
            // Different animations for different properties
            .animation(.bouncy, value: scale)
            .animation(.easeOut(duration: 0.2), value: opacity)
            .animation(.spring(duration: 1.0), value: rotation)
    }
}
```

---

## Transitions

### Basic Transitions

```swift
struct ContentView: View {
    @State private var showDetail = false

    var body: some View {
        VStack {
            if showDetail {
                DetailView()
                    .transition(.slide)
            }

            Button("Toggle") {
                withAnimation {
                    showDetail.toggle()
                }
            }
        }
    }
}
```

### Built-in Transitions

```swift
.transition(.opacity)           // Fade in/out
.transition(.scale)             // Scale from center
.transition(.scale(scale: 0.5)) // Scale from 50%
.transition(.slide)             // Slide from leading edge
.transition(.move(edge: .top))  // Move from specific edge
.transition(.push(from: .bottom)) // Push with replacement
.transition(.offset(x: 100, y: 0))  // Custom offset
```

### Combined Transitions

```swift
// Combine multiple transitions
.transition(.scale.combined(with: .opacity))

// Chain combinations
.transition(
    .scale(scale: 0.8)
    .combined(with: .opacity)
    .combined(with: .offset(y: 20))
)
```

### Asymmetric Transitions

```swift
// Different transitions for insert vs removal
.transition(.asymmetric(
    insertion: .scale.combined(with: .opacity),
    removal: .slide
))

// Common pattern: slide in from one side, out the other
.transition(.asymmetric(
    insertion: .push(from: .trailing),
    removal: .push(from: .leading)
))
```

### Custom Transitions

```swift
extension AnyTransition {
    static var flipFromBottom: AnyTransition {
        .modifier(
            active: FlipModifier(angle: -90),
            identity: FlipModifier(angle: 0)
        )
    }
}

struct FlipModifier: ViewModifier {
    let angle: Double

    func body(content: Content) -> some View {
        content
            .rotation3DEffect(
                .degrees(angle),
                axis: (x: 1, y: 0, z: 0)
            )
            .opacity(angle == 0 ? 1 : 0)
    }
}

// Usage
DetailView()
    .transition(.flipFromBottom)
```

---

## Phase Animator (iOS 17+)

### Basic Usage

```swift
enum AnimationPhase: CaseIterable {
    case initial
    case middle
    case final

    var scale: CGFloat {
        switch self {
        case .initial: return 1.0
        case .middle: return 1.2
        case .final: return 1.0
        }
    }

    var opacity: Double {
        switch self {
        case .initial: return 1.0
        case .middle: return 0.5
        case .final: return 1.0
        }
    }
}

struct PulsingView: View {
    var body: some View {
        PhaseAnimator(AnimationPhase.allCases) { phase in
            Circle()
                .fill(.blue)
                .scaleEffect(phase.scale)
                .opacity(phase.opacity)
        }
    }
}
```

### Triggered Animation

```swift
struct TriggerableAnimation: View {
    @State private var trigger = false

    var body: some View {
        VStack {
            PhaseAnimator(
                AnimationPhase.allCases,
                trigger: trigger
            ) { phase in
                Star()
                    .scaleEffect(phase.scale)
                    .rotationEffect(.degrees(phase.rotation))
            }

            Button("Animate") {
                trigger.toggle()
            }
        }
    }
}
```

### Custom Animation Per Phase

```swift
PhaseAnimator(AnimationPhase.allCases) { phase in
    ContentView(phase: phase)
} animation: { phase in
    switch phase {
    case .initial: .spring(duration: 0.3)
    case .middle: .easeOut(duration: 0.2)
    case .final: .bouncy
    }
}
```

---

## Keyframe Animator (iOS 17+)

### Basic Keyframe Animation

```swift
struct AnimationValues {
    var scale = 1.0
    var rotation = 0.0
    var yOffset = 0.0
}

struct BouncingView: View {
    @State private var trigger = false

    var body: some View {
        Circle()
            .fill(.blue)
            .frame(width: 100, height: 100)
            .keyframeAnimator(
                initialValue: AnimationValues(),
                trigger: trigger
            ) { content, value in
                content
                    .scaleEffect(value.scale)
                    .rotationEffect(.degrees(value.rotation))
                    .offset(y: value.yOffset)
            } keyframes: { _ in
                KeyframeTrack(\.scale) {
                    SpringKeyframe(1.2, duration: 0.2)
                    SpringKeyframe(0.9, duration: 0.15)
                    SpringKeyframe(1.0, duration: 0.15)
                }

                KeyframeTrack(\.rotation) {
                    LinearKeyframe(0, duration: 0.1)
                    SpringKeyframe(10, duration: 0.15)
                    SpringKeyframe(-10, duration: 0.15)
                    SpringKeyframe(0, duration: 0.1)
                }

                KeyframeTrack(\.yOffset) {
                    SpringKeyframe(-30, duration: 0.2)
                    SpringKeyframe(0, duration: 0.3)
                }
            }
            .onTapGesture {
                trigger.toggle()
            }
    }
}
```

### Keyframe Types

```swift
KeyframeTrack(\.value) {
    // Linear interpolation
    LinearKeyframe(targetValue, duration: 0.3)

    // Spring-based interpolation
    SpringKeyframe(targetValue, duration: 0.3)
    SpringKeyframe(targetValue, duration: 0.3, spring: .bouncy)

    // Cubic bezier interpolation
    CubicKeyframe(targetValue, duration: 0.3)

    // Move without animation
    MoveKeyframe(targetValue)
}
```

### Complex Multi-Track Animation

```swift
struct ComplexAnimationValues {
    var xOffset = 0.0
    var yOffset = 0.0
    var scale = 1.0
    var opacity = 1.0
    var blur = 0.0
}

struct ComplexAnimation: View {
    @State private var animating = false

    var body: some View {
        Image(systemName: "star.fill")
            .font(.system(size: 50))
            .keyframeAnimator(
                initialValue: ComplexAnimationValues(),
                repeating: animating
            ) { content, value in
                content
                    .offset(x: value.xOffset, y: value.yOffset)
                    .scaleEffect(value.scale)
                    .opacity(value.opacity)
                    .blur(radius: value.blur)
            } keyframes: { _ in
                KeyframeTrack(\.xOffset) {
                    LinearKeyframe(0, duration: 0.25)
                    LinearKeyframe(100, duration: 0.5)
                    LinearKeyframe(100, duration: 0.25)
                    LinearKeyframe(0, duration: 0.5)
                }

                KeyframeTrack(\.yOffset) {
                    SpringKeyframe(-50, duration: 0.5)
                    SpringKeyframe(0, duration: 0.5)
                }

                KeyframeTrack(\.scale) {
                    SpringKeyframe(1.5, duration: 0.25)
                    SpringKeyframe(1.0, duration: 0.25)
                    SpringKeyframe(1.2, duration: 0.25)
                    SpringKeyframe(1.0, duration: 0.25)
                }
            }
            .onAppear {
                animating = true
            }
    }
}
```

---

## Matched Geometry Effect

### Hero Transitions

```swift
struct HeroTransition: View {
    @Namespace private var animation
    @State private var isExpanded = false

    var body: some View {
        VStack {
            if isExpanded {
                // Expanded state
                RoundedRectangle(cornerRadius: 20)
                    .fill(.blue)
                    .matchedGeometryEffect(id: "card", in: animation)
                    .frame(width: 300, height: 400)
            } else {
                // Collapsed state
                RoundedRectangle(cornerRadius: 10)
                    .fill(.blue)
                    .matchedGeometryEffect(id: "card", in: animation)
                    .frame(width: 100, height: 100)
            }
        }
        .onTapGesture {
            withAnimation(.spring(duration: 0.5, bounce: 0.3)) {
                isExpanded.toggle()
            }
        }
    }
}
```

### Tab Bar Selection Indicator

```swift
struct TabBar: View {
    @Namespace private var animation
    @State private var selectedTab = 0
    let tabs = ["Home", "Search", "Profile"]

    var body: some View {
        HStack {
            ForEach(Array(tabs.enumerated()), id: \.offset) { index, title in
                Button(title) {
                    withAnimation(.spring(duration: 0.3)) {
                        selectedTab = index
                    }
                }
                .padding()
                .background {
                    if selectedTab == index {
                        Capsule()
                            .fill(.blue.opacity(0.2))
                            .matchedGeometryEffect(id: "background", in: animation)
                    }
                }
            }
        }
    }
}
```

### Properties for Matched Geometry

```swift
.matchedGeometryEffect(
    id: "identifier",
    in: namespace,
    properties: .frame,        // What to match: .frame, .position, .size
    anchor: .center,           // Anchor point for matching
    isSource: true             // Whether this is the source of truth
)
```

---

## Content Transition

### Text Morphing

```swift
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        Text("\(count)")
            .font(.largeTitle)
            .contentTransition(.numericText())
            .onTapGesture {
                withAnimation {
                    count += 1
                }
            }
    }
}
```

### Available Content Transitions

```swift
// Numeric text morphing
.contentTransition(.numericText())
.contentTransition(.numericText(value: count))
.contentTransition(.numericText(countsDown: true))

// Interpolate between text
.contentTransition(.interpolate)

// Identity (no transition)
.contentTransition(.identity)

// Opacity crossfade
.contentTransition(.opacity)

// Symbol effect
.contentTransition(.symbolEffect(.replace))
```

---

## Symbol Effects

### SF Symbol Animations

```swift
struct SymbolEffectsView: View {
    @State private var isActive = false

    var body: some View {
        VStack(spacing: 30) {
            // Bounce effect
            Image(systemName: "bell.fill")
                .symbolEffect(.bounce, value: isActive)

            // Pulse effect
            Image(systemName: "heart.fill")
                .symbolEffect(.pulse)

            // Variable color
            Image(systemName: "wifi")
                .symbolEffect(.variableColor.iterative)

            // Scale effect
            Image(systemName: "star.fill")
                .symbolEffect(.scale.up, isActive: isActive)

            // Replace effect
            Image(systemName: isActive ? "checkmark.circle" : "circle")
                .contentTransition(.symbolEffect(.replace))

            Button("Toggle") {
                withAnimation {
                    isActive.toggle()
                }
            }
        }
        .font(.largeTitle)
    }
}
```

### Symbol Effect Options

```swift
// Bounce variations
.symbolEffect(.bounce)
.symbolEffect(.bounce.up)
.symbolEffect(.bounce.down)
.symbolEffect(.bounce.byLayer)
.symbolEffect(.bounce.wholeSymbol)

// Variable color
.symbolEffect(.variableColor)
.symbolEffect(.variableColor.iterative)
.symbolEffect(.variableColor.reversing)
.symbolEffect(.variableColor.cumulative)

// Scale
.symbolEffect(.scale.up)
.symbolEffect(.scale.down)

// Pulse
.symbolEffect(.pulse)
.symbolEffect(.pulse.byLayer)
```

---

## Interactive Animations

### Drag Gesture Animation

```swift
struct DraggableCard: View {
    @State private var offset = CGSize.zero
    @State private var isDragging = false

    var body: some View {
        RoundedRectangle(cornerRadius: 20)
            .fill(.blue)
            .frame(width: 200, height: 300)
            .offset(offset)
            .scaleEffect(isDragging ? 1.05 : 1.0)
            .animation(.interactiveSpring(response: 0.3), value: isDragging)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        offset = value.translation
                        isDragging = true
                    }
                    .onEnded { value in
                        isDragging = false
                        withAnimation(.spring(duration: 0.5, bounce: 0.3)) {
                            offset = .zero
                        }
                    }
            )
    }
}
```

### Gesture State for Smooth Tracking

```swift
struct SmoothDrag: View {
    @GestureState private var dragOffset = CGSize.zero
    @State private var position = CGSize.zero

    var body: some View {
        Circle()
            .fill(.blue)
            .frame(width: 100, height: 100)
            .offset(
                x: position.width + dragOffset.width,
                y: position.height + dragOffset.height
            )
            .animation(.interactiveSpring(), value: dragOffset)
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
    }
}
```

### Velocity-Based Animation

```swift
struct VelocityDrag: View {
    @State private var offset = CGSize.zero

    var body: some View {
        RoundedRectangle(cornerRadius: 20)
            .fill(.blue)
            .frame(width: 200, height: 300)
            .offset(offset)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        offset = value.translation
                    }
                    .onEnded { value in
                        // Use velocity for natural-feeling spring back
                        let velocity = CGSize(
                            width: value.predictedEndTranslation.width - value.translation.width,
                            height: value.predictedEndTranslation.height - value.translation.height
                        )

                        withAnimation(.spring(
                            response: 0.5,
                            dampingFraction: 0.7,
                            blendDuration: 0
                        )) {
                            offset = .zero
                        }
                    }
            )
    }
}
```

---

## Scroll Animations

### Scroll Transition (iOS 17+)

```swift
struct ScrollTransitionView: View {
    var body: some View {
        ScrollView {
            LazyVStack(spacing: 20) {
                ForEach(0..<20) { index in
                    RoundedRectangle(cornerRadius: 12)
                        .fill(.blue.gradient)
                        .frame(height: 100)
                        .scrollTransition { content, phase in
                            content
                                .opacity(phase.isIdentity ? 1 : 0.5)
                                .scaleEffect(phase.isIdentity ? 1 : 0.9)
                                .blur(radius: phase.isIdentity ? 0 : 2)
                        }
                }
            }
            .padding()
        }
    }
}
```

### Visual Effect Modifier (iOS 17+)

```swift
struct ParallaxScroll: View {
    var body: some View {
        ScrollView {
            LazyVStack(spacing: 0) {
                ForEach(0..<10) { index in
                    Image("photo\(index)")
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(height: 300)
                        .clipped()
                        .visualEffect { content, proxy in
                            content
                                .offset(y: parallaxOffset(proxy))
                        }
                }
            }
        }
    }

    func parallaxOffset(_ proxy: GeometryProxy) -> CGFloat {
        let frame = proxy.frame(in: .scrollView)
        return -frame.minY * 0.3
    }
}
```

---

## Performance Best Practices

### 1. Use Explicit Animations

```swift
// GOOD: Explicit animation tied to specific value
.animation(.spring, value: isExpanded)

// AVOID: Implicit animation (deprecated, less performant)
.animation(.spring)
```

### 2. Animate Efficiently

```swift
// GOOD: Animate transforms (GPU-accelerated)
.scaleEffect(scale)
.rotationEffect(.degrees(rotation))
.offset(x: offsetX, y: offsetY)
.opacity(opacity)

// AVOID: Animating layout-affecting properties when possible
// (These trigger re-layout each frame)
.frame(width: animatedWidth)
.padding(animatedPadding)
```

### 3. Limit Animation Scope

```swift
// GOOD: Animation on specific view
ChildView()
    .animation(.spring, value: childState)

// AVOID: Animation on parent affecting all children
ParentView()
    .animation(.spring, value: anyChange)  // All children animate
```

### 4. Use drawingGroup for Complex Graphics

```swift
// For complex composited views
ComplexAnimatedShape()
    .drawingGroup()  // Renders to offscreen buffer
```

### 5. Keep Durations Short

```swift
// RECOMMENDED: Under 0.4 seconds for UI feedback
.spring(duration: 0.3, bounce: 0.2)

// Reserve longer animations for:
// - Onboarding flows
// - Celebrations
// - State transitions
```

### 6. Test on Device

```swift
// Simulator timing is NOT accurate
// Always test animations on physical device
// Different devices have different performance characteristics
```

---

## Common Patterns

### Loading Spinner

```swift
struct LoadingSpinner: View {
    @State private var isAnimating = false

    var body: some View {
        Circle()
            .trim(from: 0, to: 0.7)
            .stroke(.blue, lineWidth: 4)
            .frame(width: 40, height: 40)
            .rotationEffect(.degrees(isAnimating ? 360 : 0))
            .animation(
                .linear(duration: 1.0).repeatForever(autoreverses: false),
                value: isAnimating
            )
            .onAppear {
                isAnimating = true
            }
    }
}
```

### Pulsing Indicator

```swift
struct PulsingDot: View {
    @State private var isPulsing = false

    var body: some View {
        Circle()
            .fill(.green)
            .frame(width: 12, height: 12)
            .scaleEffect(isPulsing ? 1.2 : 1.0)
            .opacity(isPulsing ? 0.6 : 1.0)
            .animation(
                .easeInOut(duration: 0.8).repeatForever(autoreverses: true),
                value: isPulsing
            )
            .onAppear {
                isPulsing = true
            }
    }
}
```

### Shake Effect

```swift
struct ShakeEffect: GeometryEffect {
    var amount: CGFloat = 10
    var shakesPerUnit = 3
    var animatableData: CGFloat

    func effectValue(size: CGSize) -> ProjectionTransform {
        ProjectionTransform(CGAffineTransform(translationX:
            amount * sin(animatableData * .pi * CGFloat(shakesPerUnit)),
            y: 0))
    }
}

// Usage
TextField("Email", text: $email)
    .modifier(ShakeEffect(animatableData: shakeAmount))
    .onChange(of: hasError) {
        withAnimation(.default) {
            shakeAmount = hasError ? 1 : 0
        }
    }
```

---

## Official Resources

- [SwiftUI Animations Documentation](https://developer.apple.com/documentation/swiftui/animations)
- [Animating Views and Transitions](https://developer.apple.com/tutorials/swiftui/animating-views-and-transitions)
- [PhaseAnimator Documentation](https://developer.apple.com/documentation/swiftui/phaseanimator)
- [KeyframeAnimator Documentation](https://developer.apple.com/documentation/swiftui/keyframeanimator)
- [WWDC23: Wind your way through advanced animations](https://developer.apple.com/videos/play/wwdc2023/10157/)
