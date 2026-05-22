---
name: swiftui-colors-modifiers
description: Modern SwiftUI colors, ShapeStyle, gradients, MeshGradient, and custom ViewModifiers. Use when user asks about colors, foregroundStyle, gradients, hierarchical colors, tint, custom ViewModifiers, or SwiftUI styling.
allowed-tools: Bash, Read, Write, Edit
---

# SwiftUI Colors and Modifiers

Comprehensive guide to modern SwiftUI color APIs, ShapeStyle, gradients, and creating reusable ViewModifiers for iOS 26.

## Prerequisites

- iOS 15+ for foregroundStyle (iOS 26 recommended)
- Xcode 26+

---

## Modern Color APIs

### foregroundStyle (Recommended)

Replaces the deprecated `foregroundColor(_:)`:

```swift
// DEPRECATED
Text("Hello")
    .foregroundColor(.blue)

// MODERN - Use foregroundStyle
Text("Hello")
    .foregroundStyle(.blue)

// With gradients
Text("Gradient Text")
    .foregroundStyle(
        LinearGradient(
            colors: [.blue, .purple],
            startPoint: .leading,
            endPoint: .trailing
        )
    )
```

### ShapeStyle Protocol

`foregroundStyle` accepts any `ShapeStyle`:

```swift
// Colors
.foregroundStyle(.red)
.foregroundStyle(Color.blue)

// Gradients
.foregroundStyle(LinearGradient(...))
.foregroundStyle(RadialGradient(...))
.foregroundStyle(AngularGradient(...))
.foregroundStyle(MeshGradient(...))

// Materials
.foregroundStyle(.ultraThinMaterial)
.foregroundStyle(.regularMaterial)

// Hierarchical
.foregroundStyle(.primary)
.foregroundStyle(.secondary)
.foregroundStyle(.tertiary)
```

---

## Hierarchical Colors

### Setting Hierarchy at Root

```swift
// Set all three levels at once
ContentView()
    .foregroundStyle(.red, .orange, .yellow)

// Children use hierarchical levels
struct ContentView: View {
    var body: some View {
        VStack {
            Text("Primary")      // Red
                .foregroundStyle(.primary)
            Text("Secondary")    // Orange
                .foregroundStyle(.secondary)
            Text("Tertiary")     // Yellow
                .foregroundStyle(.tertiary)
        }
    }
}
```

### Available Levels

```swift
.foregroundStyle(.primary)     // Level 1 - Most prominent
.foregroundStyle(.secondary)   // Level 2
.foregroundStyle(.tertiary)    // Level 3
.foregroundStyle(.quaternary)  // Level 4
.foregroundStyle(.quinary)     // Level 5 - Least prominent
```

**Note**: Only first three can be customized via `foregroundStyle(_:_:_:)`.

### Practical Example

```swift
struct CardView: View {
    let title: String
    let subtitle: String
    let detail: String

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title)
                .font(.headline)
                .foregroundStyle(.primary)

            Text(subtitle)
                .font(.subheadline)
                .foregroundStyle(.secondary)

            Text(detail)
                .font(.caption)
                .foregroundStyle(.tertiary)
        }
    }
}
```

---

## Semantic Colors

### System Colors

```swift
// Adaptive colors (change with Dark Mode)
Color.primary          // Black/White
Color.secondary        // Gray
Color.accentColor      // App's accent color

// UI element colors
Color(uiColor: .systemBackground)
Color(uiColor: .secondarySystemBackground)
Color(uiColor: .tertiarySystemBackground)
Color(uiColor: .label)
Color(uiColor: .secondaryLabel)
```

### Accent Color

Set in Asset Catalog or programmatically:

```swift
// In code
Button("Action") { }
    .tint(.blue)

// App-wide in Assets.xcassets:
// Create "AccentColor" color set
```

### Tint Modifier

Override accent color for a hierarchy:

```swift
// tint affects interactive elements, not all foreground
VStack {
    Button("Blue") { }  // Uses blue tint
    Link("Website", destination: url)  // Uses blue tint
    Text("Plain")  // NOT affected by tint
}
.tint(.blue)
```

**tint vs foregroundStyle:**
- `tint`: Affects buttons, links, controls
- `foregroundStyle`: Affects all foreground content

---

## Gradients

### LinearGradient

```swift
LinearGradient(
    colors: [.blue, .purple],
    startPoint: .topLeading,
    endPoint: .bottomTrailing
)

// With stops for control
LinearGradient(
    stops: [
        .init(color: .red, location: 0),
        .init(color: .orange, location: 0.3),
        .init(color: .yellow, location: 1)
    ],
    startPoint: .top,
    endPoint: .bottom
)

// Usage
Rectangle()
    .fill(
        LinearGradient(
            colors: [.blue, .cyan],
            startPoint: .leading,
            endPoint: .trailing
        )
    )
```

### RadialGradient

```swift
RadialGradient(
    colors: [.white, .blue],
    center: .center,
    startRadius: 0,
    endRadius: 200
)

// With offset center
RadialGradient(
    colors: [.yellow, .orange, .red],
    center: .topLeading,
    startRadius: 50,
    endRadius: 300
)
```

### AngularGradient

```swift
AngularGradient(
    colors: [.red, .yellow, .green, .blue, .purple, .red],
    center: .center
)

// Conic gradient with angle
AngularGradient(
    colors: [.blue, .purple],
    center: .center,
    startAngle: .degrees(0),
    endAngle: .degrees(180)
)
```

### MeshGradient (iOS 18+)

Complex multi-point gradients:

```swift
MeshGradient(
    width: 3,
    height: 3,
    points: [
        // Row 0
        [0.0, 0.0], [0.5, 0.0], [1.0, 0.0],
        // Row 1
        [0.0, 0.5], [0.5, 0.5], [1.0, 0.5],
        // Row 2
        [0.0, 1.0], [0.5, 1.0], [1.0, 1.0]
    ],
    colors: [
        .red, .orange, .yellow,
        .green, .blue, .purple,
        .pink, .cyan, .mint
    ]
)

// Animated mesh
struct AnimatedMesh: View {
    @State private var offset: CGFloat = 0

    var body: some View {
        MeshGradient(
            width: 3,
            height: 3,
            points: [
                [0.0, 0.0], [0.5, 0.0], [1.0, 0.0],
                [0.0, 0.5], [0.5 + offset, 0.5], [1.0, 0.5],
                [0.0, 1.0], [0.5, 1.0], [1.0, 1.0]
            ],
            colors: [
                .blue, .cyan, .teal,
                .purple, .indigo, .blue,
                .pink, .orange, .yellow
            ],
            smoothsColors: true
        )
        .onAppear {
            withAnimation(.easeInOut(duration: 2).repeatForever()) {
                offset = 0.2
            }
        }
    }
}
```

---

## Asset Catalog Colors

### Creating Color Sets

1. Open Assets.xcassets
2. Right-click → New Color Set
3. Configure for appearances:
   - Any Appearance
   - Light
   - Dark
   - High Contrast variants

### Using Asset Colors

```swift
// By name
Color("BrandPrimary")
Color("BackgroundColor")

// With bundle
Color("CustomColor", bundle: .module)
```

### Organizing Colors

```
Assets.xcassets/
├── Colors/
│   ├── Brand/
│   │   ├── BrandPrimary
│   │   ├── BrandSecondary
│   │   └── BrandAccent
│   ├── UI/
│   │   ├── BackgroundPrimary
│   │   ├── BackgroundSecondary
│   │   └── SeparatorColor
│   └── Text/
│       ├── TextPrimary
│       ├── TextSecondary
│       └── TextTertiary
```

---

## Custom ShapeStyles (iOS 17+)

```swift
struct StripedStyle: ShapeStyle {
    var color1: Color
    var color2: Color
    var stripeWidth: CGFloat

    func resolve(in environment: EnvironmentValues) -> some ShapeStyle {
        // Return a resolved style
        LinearGradient(
            stops: generateStripeStops(),
            startPoint: .leading,
            endPoint: .trailing
        )
    }

    private func generateStripeStops() -> [Gradient.Stop] {
        var stops: [Gradient.Stop] = []
        var position: CGFloat = 0

        while position < 1 {
            stops.append(.init(color: color1, location: position))
            stops.append(.init(color: color1, location: position + stripeWidth / 2))
            stops.append(.init(color: color2, location: position + stripeWidth / 2))
            stops.append(.init(color: color2, location: position + stripeWidth))
            position += stripeWidth
        }

        return stops
    }
}

// Usage
Rectangle()
    .fill(StripedStyle(color1: .blue, color2: .white, stripeWidth: 0.1))
```

---

## Custom ViewModifiers

### Basic Modifier

```swift
struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(.regularMaterial)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .shadow(radius: 4)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardStyle())
    }
}

// Usage
Text("Card Content")
    .cardStyle()
```

### Configurable Modifier

```swift
struct RoundedStyle: ViewModifier {
    var cornerRadius: CGFloat
    var backgroundColor: Color
    var shadowRadius: CGFloat

    func body(content: Content) -> some View {
        content
            .padding()
            .background(backgroundColor)
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
            .shadow(radius: shadowRadius)
    }
}

extension View {
    func rounded(
        cornerRadius: CGFloat = 12,
        backgroundColor: Color = .white,
        shadowRadius: CGFloat = 4
    ) -> some View {
        modifier(RoundedStyle(
            cornerRadius: cornerRadius,
            backgroundColor: backgroundColor,
            shadowRadius: shadowRadius
        ))
    }
}

// Usage
Text("Custom")
    .rounded(cornerRadius: 20, backgroundColor: .blue)
```

### Environment-Aware Modifier

```swift
struct AdaptiveCard: ViewModifier {
    @Environment(\.colorScheme) var colorScheme

    func body(content: Content) -> some View {
        content
            .padding()
            .background(colorScheme == .dark ? Color.gray.opacity(0.2) : Color.white)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .shadow(
                color: colorScheme == .dark ? .clear : .black.opacity(0.1),
                radius: 8
            )
    }
}
```

### Conditional Modifier

```swift
extension View {
    @ViewBuilder
    func `if`<Content: View>(
        _ condition: Bool,
        transform: (Self) -> Content
    ) -> some View {
        if condition {
            transform(self)
        } else {
            self
        }
    }

    @ViewBuilder
    func ifLet<T, Content: View>(
        _ value: T?,
        transform: (Self, T) -> Content
    ) -> some View {
        if let value {
            transform(self, value)
        } else {
            self
        }
    }
}

// Usage
Text("Hello")
    .if(isHighlighted) { view in
        view.foregroundStyle(.yellow)
    }
    .ifLet(user) { view, user in
        view.badge(user.notificationCount)
    }
```

---

## iOS 26 New Modifiers

### Close Button Role

```swift
.toolbar {
    ToolbarItem(placement: .cancellationAction) {
        Button("Dismiss", role: .close) {
            dismiss()
        }
        // Renders as glass X button
    }
}
```

### Glass Button Styles

```swift
Button("Glass") { }
    .buttonStyle(.glass)

Button("Prominent") { }
    .buttonStyle(.glassProminent)
```

### Custom Slider Ticks

```swift
Slider(value: $value, in: 0...100) {
    Text("Value")
} minimumValueLabel: {
    Text("0")
} maximumValueLabel: {
    Text("100")
}
.sliderStyle(.ticked(count: 10))  // iOS 26
```

---

## Design System Example

```swift
// DesignSystem.swift
enum DS {
    enum Colors {
        static let primary = Color("Primary")
        static let secondary = Color("Secondary")
        static let background = Color("Background")
        static let surface = Color("Surface")
        static let error = Color("Error")
        static let success = Color("Success")
    }

    enum Spacing {
        static let xs: CGFloat = 4
        static let sm: CGFloat = 8
        static let md: CGFloat = 16
        static let lg: CGFloat = 24
        static let xl: CGFloat = 32
    }

    enum CornerRadius {
        static let sm: CGFloat = 4
        static let md: CGFloat = 8
        static let lg: CGFloat = 16
        static let xl: CGFloat = 24
    }
}

// Modifiers using design system
struct DSCard: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding(DS.Spacing.md)
            .background(DS.Colors.surface)
            .clipShape(RoundedRectangle(cornerRadius: DS.CornerRadius.lg))
    }
}

extension View {
    func dsCard() -> some View {
        modifier(DSCard())
    }
}
```

---

## Best Practices

1. **Use foregroundStyle** - Not deprecated foregroundColor
2. **Leverage Hierarchical Colors** - .primary, .secondary, .tertiary
3. **Asset Catalog for Themes** - Organize colors properly
4. **DRY with Modifiers** - Create reusable ViewModifiers
5. **Compose Modifiers** - Build complex styles from simple ones
6. **Environment Awareness** - Respect colorScheme and accessibility

---

## Official Resources

- [Color Documentation](https://developer.apple.com/documentation/swiftui/color)
- [ShapeStyle Documentation](https://developer.apple.com/documentation/swiftui/shapestyle)
- [ViewModifier Documentation](https://developer.apple.com/documentation/swiftui/viewmodifier)
