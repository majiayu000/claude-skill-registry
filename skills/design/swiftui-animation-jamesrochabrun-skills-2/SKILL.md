---
name: swiftui-animation
description: This skill provides comprehensive guidance for implementing advanced SwiftUI animations, transitions, matched geometry effects, and Metal shader integration. Use when building animations, view transitions, hero animations, or GPU-accelerated effects in SwiftUI apps for iOS and macOS.
---

# SwiftUI Animation Expert

Expert guidance for implementing advanced SwiftUI animations and Metal shader integration. Covers animation curves, springs, transitions, matched geometry effects, PhaseAnimator, KeyframeAnimator, and GPU-accelerated shader effects.

## When to Use This Skill

- Understanding motion design principles and when to use animation
- Making animations accessible and platform-appropriate
- Implementing animations in SwiftUI (springs, easing, keyframes)
- Creating view transitions (fade, slide, scale, custom)
- Building hero animations with matchedGeometryEffect
- Adding GPU-accelerated effects with Metal shaders
- Optimizing animation performance
- Creating multi-phase orchestrated animations

## Quick Reference

### Animation Basics

```swift
// Explicit animation (preferred)
withAnimation(.spring(response: 0.4, dampingFraction: 0.75)) {
    isExpanded.toggle()
}

// iOS 17+ spring presets
withAnimation(.snappy) { ... }  // Fast, small bounce
withAnimation(.smooth) { ... }  // Gentle, no bounce
withAnimation(.bouncy) { ... }  // More bounce
```

### Common Transitions

```swift
// Basic
.transition(.opacity)
.transition(.scale)
.transition(.slide)
.transition(.move(edge: .bottom))

// Combined
.transition(.move(edge: .trailing).combined(with: .opacity))

// Asymmetric
.transition(.asymmetric(
    insertion: .move(edge: .bottom),
    removal: .opacity
))
```

### Matched Geometry Effect

```swift
@Namespace var namespace

// Source view
ThumbnailView()
    .matchedGeometryEffect(id: "hero", in: namespace)

// Destination view
DetailView()
    .matchedGeometryEffect(id: "hero", in: namespace)
```

### Metal Shader Effects (iOS 17+)

```swift
// Color manipulation
.colorEffect(ShaderLibrary.invert())

// Pixel displacement
.distortionEffect(
    ShaderLibrary.wave(.float(time)),
    maxSampleOffset: CGSize(width: 20, height: 20)
)

// Full layer access
.layerEffect(ShaderLibrary.blur(.float(radius)), maxSampleOffset: .zero)
```

## Reference Materials

Detailed documentation is available in `references/`:

- **motion-guidelines.md** - HIG Motion design principles
  - Purpose-driven motion philosophy
  - Accessibility requirements
  - Platform-specific considerations (iOS, visionOS, watchOS)
  - Animation anti-patterns to avoid

- **animations.md** - Complete animation API guide
  - Implicit vs explicit animations
  - Spring parameters and presets
  - Animation modifiers (speed, delay, repeat)
  - PhaseAnimator for multi-step sequences
  - KeyframeAnimator for property-specific timelines
  - Custom animatable properties

- **transitions.md** - View transition guide
  - Built-in transitions (opacity, scale, slide, move)
  - Combined and asymmetric transitions
  - Matched geometry effect implementation
  - Hero animation patterns
  - Content transitions (iOS 17+)
  - Custom transition creation

- **metal-shaders.md** - GPU shader integration
  - SwiftUI shader modifiers (colorEffect, distortionEffect, layerEffect)
  - Writing Metal shader functions
  - Embedding MTKView with UIViewRepresentable
  - Cross-platform Metal integration (iOS/macOS)
  - Performance considerations

## Common Patterns

### Expandable Card

```swift
struct ExpandableCard: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            RoundedRectangle(cornerRadius: isExpanded ? 20 : 12)
                .fill(.blue)
                .frame(
                    width: isExpanded ? 300 : 150,
                    height: isExpanded ? 400 : 100
                )
        }
        .onTapGesture {
            withAnimation(.spring(response: 0.35, dampingFraction: 0.75)) {
                isExpanded.toggle()
            }
        }
    }
}
```

### List Item Appearance

```swift
ForEach(Array(items.enumerated()), id: \.element.id) { index, item in
    ItemRow(item: item)
        .transition(.asymmetric(
            insertion: .move(edge: .trailing).combined(with: .opacity),
            removal: .move(edge: .leading).combined(with: .opacity)
        ))
        .animation(.spring().delay(Double(index) * 0.05), value: items)
}
```

### Pulsing Indicator

```swift
Circle()
    .fill(.blue)
    .frame(width: 20, height: 20)
    .scaleEffect(isPulsing ? 1.2 : 1.0)
    .opacity(isPulsing ? 0.6 : 1.0)
    .onAppear {
        withAnimation(.easeInOut(duration: 1.0).repeatForever(autoreverses: true)) {
            isPulsing = true
        }
    }
```

## Best Practices

1. **Motion should be purposeful** - Don't add animation for its own sake; support the experience without overshadowing it
2. **Make motion optional** - Supplement with haptics and audio; never use motion as the only way to communicate
3. **Aim for brevity** - Brief, precise animations feel lightweight and convey information effectively
4. **Prefer explicit animations** - Use `withAnimation` over `.animation()` modifier for clarity
5. **Use spring animations** - They feel more natural and iOS-native
6. **Start with `.spring(response: 0.35, dampingFraction: 0.8)`** - Good default for most interactions
7. **Keep animations under 400ms** - Longer feels sluggish
8. **Let people cancel motion** - Don't force users to wait for animations to complete
9. **Test on device** - Simulator animation timing differs
10. **Profile shader performance** - GPU time matters for complex effects

## Troubleshooting

### Animation not working

- Ensure state change is wrapped in `withAnimation`
- Check that the property is animatable
- Verify the view is actually changing

### Matched geometry jumps

- Both views must use the same ID and namespace
- Use explicit `withAnimation` when toggling
- Check `zIndex` for proper layering

### Shader not appearing

- Verify `.metal` file is added to target
- Check shader function signature matches expected format
- Ensure `maxSampleOffset` is set correctly for distortion effects
