---
name: liquid-glass-design
description: iOS 26/macOS 26 Liquid Glass design system with complete API coverage. Use when user asks about iOS 26 design, Liquid Glass, glassEffect modifier, GlassEffectContainer, morphing animations, HIG compliance, visual styling, or the new Apple design language.
allowed-tools: Bash, Read, Write, Edit
license: MIT
compatibility: Xcode 26+ with Swift 6 toolchain on macOS
---

# Liquid Glass Design System

Comprehensive guide to iOS 26 and macOS Tahoe's revolutionary Liquid Glass design system, including complete SwiftUI API coverage, Human Interface Guidelines, morphing animations, and implementation best practices.

## Prerequisites

- Xcode 26+
- iOS 26 / macOS Tahoe deployment target
- SwiftUI framework

---

## Overview

Liquid Glass is Apple's new design language introduced at WWDC 2025. It creates a lightweight, dynamic material that:

- **Bends light** in real-time (lensing effect)
- **Responds to motion** with specular highlights
- **Adapts** to content behind it
- **Morphs** between states fluidly
- **Respects accessibility** settings automatically

### Design Philosophy

Liquid Glass establishes a clear **visual hierarchy**:
1. **Content Layer** - Your app's main content sits at the bottom
2. **Navigation Layer** - Glass controls float above content

> **Key Principle**: Reserve glass for navigation and controls, NOT for content.

---

## Material Properties

### Light Behavior

```
┌─────────────────────────────────────┐
│  Liquid Glass Material Properties   │
├─────────────────────────────────────┤
│  • Translucency with depth          │
│  • Real-time light refraction       │
│  • Specular highlights on motion    │
│  • Adaptive shadows                 │
│  • Color informed by backdrop       │
│  • Light/dark environment aware     │
└─────────────────────────────────────┘
```

### Visual Characteristics

- **Lensing**: Content behind glass appears subtly magnified/distorted
- **Specular Highlights**: Bright spots that respond to device tilt
- **Adaptive Tint**: Glass picks up colors from underlying content
- **Depth**: Material has apparent thickness and dimension

---

## Glass Variants

### Regular Glass (Default)

The versatile, adaptive variant. Use for most UI elements.

```swift
Button("Action") {
    performAction()
}
.buttonStyle(.glass)
```

**Characteristics:**
- Adapts to light/dark mode automatically
- Picks up underlying content colors
- Standard blur and translucency
- Best for most use cases

### Clear Glass

Permanently transparent variant with minimal visual impact.

```swift
Button("Subtle Action") {
    performAction()
}
.buttonStyle(.glassClear)
```

**Characteristics:**
- Higher transparency
- Requires background dimming for contrast
- Use when content visibility is paramount
- Less prominent than regular glass

### Identity Glass

No glass effect applied. Use for comparisons or opt-out.

```swift
.glassEffect(.identity)
```

---

## Critical Design Rule

> **NEVER mix Regular and Clear glass variants in the same interface.**

This creates visual inconsistency and violates HIG principles.

```swift
// WRONG - Mixed variants
HStack {
    Button("Save") { }
        .buttonStyle(.glass)        // Regular
    Button("Cancel") { }
        .buttonStyle(.glassClear)   // Clear - DON'T MIX
}

// CORRECT - Consistent variant
HStack {
    Button("Save") { }
        .buttonStyle(.glass)
    Button("Cancel") { }
        .buttonStyle(.glass)
}
```

---

## SwiftUI API Reference

### Basic Glass Effect

```swift
// Simple glass effect with default shape
View()
    .glassEffect()

// Glass with specific shape
View()
    .glassEffect(in: RoundedRectangle(cornerRadius: 16))

// Glass with variant and shape
View()
    .glassEffect(.regular, in: Capsule())

// Conditional glass
View()
    .glassEffect(in: Circle(), isEnabled: showGlass)
```

### Glass Effect Signature

```swift
func glassEffect(
    _ glass: Glass = .regular,
    in shape: some Shape = .rect,
    isEnabled: Bool = true
) -> some View
```

### Glass Enum

```swift
enum Glass {
    case regular      // Adaptive, versatile (default)
    case clear        // High transparency
    case identity     // No effect
}
```

---

## Glass Effect Modifiers

### Tint

Add color tint to glass elements:

```swift
Button("Tinted") { }
    .buttonStyle(.glass)
    .tint(.blue)

// Or with glass directly
View()
    .glassEffect(in: RoundedRectangle(cornerRadius: 12))
    .tint(.green)
```

### Interactive

Enable interactive behaviors for glass:

```swift
View()
    .glassEffect(.regular.interactive(), in: Capsule())
```

### Button Styles

```swift
// Standard glass button
Button("Glass") { }
    .buttonStyle(.glass)

// Prominent glass button (more opaque)
Button("Prominent") { }
    .buttonStyle(.glassProminent)

// Borderless glass
Button("Borderless") { }
    .buttonStyle(.glassBorderless)
```

---

## GlassEffectContainer

`GlassEffectContainer` combines multiple glass shapes into a single morphable unit with shared visual properties.

### Basic Usage

```swift
GlassEffectContainer {
    HStack {
        Button("First") { }
            .glassEffect(in: Capsule())

        Button("Second") { }
            .glassEffect(in: Capsule())

        Button("Third") { }
            .glassEffect(in: Capsule())
    }
}
```

### Spacing Parameter

The `spacing` parameter controls the threshold distance for morphing:

```swift
// Buttons close together will merge
GlassEffectContainer(spacing: 8) {
    HStack(spacing: 4) {  // Less than container spacing
        Button("A") { }
            .glassEffect(in: Capsule())
        Button("B") { }
            .glassEffect(in: Capsule())
    }
    // These buttons will visually merge into one glass shape
}

// Buttons far apart stay separate
GlassEffectContainer(spacing: 8) {
    HStack(spacing: 20) {  // Greater than container spacing
        Button("A") { }
            .glassEffect(in: Capsule())
        Button("B") { }
            .glassEffect(in: Capsule())
    }
    // These buttons maintain individual glass shapes
}
```

### Container Benefits

When views are inside a `GlassEffectContainer`:

1. **Automatic Blending** - Overlapping shapes blend seamlessly
2. **Consistent Effects** - Shared blur and lighting
3. **Morphing Transitions** - Smooth animations between states
4. **Performance** - Optimized rendering for multiple glass elements

### Container Example: Expandable Menu

```swift
struct ExpandableMenu: View {
    @State private var isExpanded = false
    @Namespace private var animation

    var body: some View {
        GlassEffectContainer {
            if isExpanded {
                VStack {
                    Button("Option 1") { }
                        .glassEffect(in: Capsule())
                        .glassEffectID("menu", in: animation)

                    Button("Option 2") { }
                        .glassEffect(in: Capsule())

                    Button("Option 3") { }
                        .glassEffect(in: Capsule())
                }
            } else {
                Button("Menu") {
                    withAnimation(.spring) {
                        isExpanded.toggle()
                    }
                }
                .glassEffect(in: Capsule())
                .glassEffectID("menu", in: animation)
            }
        }
    }
}
```

---

## Morphing Animations

### Glass Effect ID

Link glass elements across states for fluid morphing:

```swift
@Namespace private var animation

// Source state
Button("Collapsed") { }
    .glassEffect(in: Capsule())
    .glassEffectID("button", in: animation)

// Expanded state
HStack {
    Button("Edit") { }
        .glassEffect(in: Capsule())
        .glassEffectID("button", in: animation)  // Same ID = morph

    Button("Delete") { }
        .glassEffect(in: Capsule())
}
```

### Glass Effect Union

Combine multiple glass shapes into one:

```swift
GlassEffectContainer {
    ForEach(items) { item in
        ItemView(item: item)
            .glassEffect(in: RoundedRectangle(cornerRadius: 12))
            .glassEffectUnion(id: "group", namespace: animation)
    }
}
```

### Glass Effect Transition

Control how glass appears/disappears:

```swift
View()
    .glassEffect(in: Capsule())
    .glassEffectTransition(.scale, isEnabled: true)

// Transition types
.glassEffectTransition(.opacity)
.glassEffectTransition(.scale)
.glassEffectTransition(.slide)
.glassEffectTransition(.identity)  // No transition
```

### Complete Morphing Example

```swift
struct MorphingToolbar: View {
    @State private var mode: Mode = .browse
    @Namespace private var morphing

    enum Mode {
        case browse, edit, select
    }

    var body: some View {
        GlassEffectContainer {
            switch mode {
            case .browse:
                HStack {
                    Button("Edit") {
                        withAnimation(.spring(duration: 0.4)) {
                            mode = .edit
                        }
                    }
                    .glassEffect(in: Capsule())
                    .glassEffectID("primary", in: morphing)
                }

            case .edit:
                HStack {
                    Button("Done") {
                        withAnimation(.spring(duration: 0.4)) {
                            mode = .browse
                        }
                    }
                    .glassEffect(in: Capsule())
                    .glassEffectID("primary", in: morphing)

                    Button("Select All") { }
                        .glassEffect(in: Capsule())
                        .glassEffectTransition(.scale)
                }

            case .select:
                HStack {
                    Button("Cancel") {
                        withAnimation(.spring(duration: 0.4)) {
                            mode = .browse
                        }
                    }
                    .glassEffect(in: Capsule())
                    .glassEffectID("primary", in: morphing)

                    Spacer()

                    Button("Delete") { }
                        .glassEffect(in: Capsule())
                        .tint(.red)
                }
            }
        }
        .padding()
    }
}
```

---

## Known Issues

### iOS 26.1: Menu in GlassEffectContainer

> **Bug**: Placing a `Menu` inside a `GlassEffectContainer` breaks morphing animations.

```swift
// AVOID in iOS 26.1
GlassEffectContainer {
    Menu("Options") {  // This breaks morphing
        Button("Edit") { }
        Button("Delete") { }
    }
    .glassEffect(in: Capsule())
}

// WORKAROUND: Move Menu outside container
VStack {
    Menu("Options") {
        Button("Edit") { }
        Button("Delete") { }
    }
    .buttonStyle(.glass)

    GlassEffectContainer {
        // Other morphing content
    }
}
```

---

## Toolbar Integration

### Glass Toolbars

Toolbars automatically adopt Liquid Glass in iOS 26:

```swift
struct ContentView: View {
    var body: some View {
        NavigationStack {
            ContentList()
                .toolbar {
                    ToolbarItem(placement: .primaryAction) {
                        Button("Add", systemImage: "plus") {
                            addItem()
                        }
                    }

                    ToolbarSpacer(.fixed)  // NEW: Group related items

                    ToolbarItem(placement: .secondaryAction) {
                        Button("Edit") {
                            editMode.toggle()
                        }
                    }
                }
        }
    }
}
```

### Toolbar Spacer

New in iOS 26 for grouping toolbar items:

```swift
.toolbar {
    // Group 1
    ToolbarItem(placement: .primaryAction) {
        Button("Save") { }
    }

    ToolbarSpacer(.fixed)  // Creates visual separation

    // Group 2
    ToolbarItem(placement: .secondaryAction) {
        Button("Share") { }
    }
    ToolbarItem(placement: .secondaryAction) {
        Button("Delete") { }
    }
}
```

### Close Button Role

New button role for dismiss actions with glass X styling:

```swift
.toolbar {
    ToolbarItem(placement: .cancellationAction) {
        Button("Close", role: .close) {
            dismiss()
        }
        // Automatically renders as glass X button
    }
}
```

### Toolbar Glass Visibility

Control glass background visibility:

```swift
.toolbar {
    ToolbarItem(placement: .primaryAction) {
        Button("Action") { }
    }
}
.toolbarBackgroundVisibility(.visible, for: .navigationBar)
// Options: .automatic, .visible, .hidden
```

---

## Navigation with Glass

### Navigation Bar

```swift
NavigationStack {
    ContentView()
        .navigationTitle("My App")
        .navigationBarTitleDisplayMode(.large)
        // Glass navigation bar is automatic in iOS 26
}
```

### Tab Bar

```swift
TabView {
    HomeView()
        .tabItem {
            Label("Home", systemImage: "house")
        }

    SearchView()
        .tabItem {
            Label("Search", systemImage: "magnifyingglass")
        }
        .tab(role: .search)  // NEW: Search morphs into field
}
// Glass tab bar is automatic
```

### Split View

```swift
NavigationSplitView {
    Sidebar()
} content: {
    ContentList()
} detail: {
    DetailView()
}
// Glass adapts to column visibility
```

---

## Accessibility

Liquid Glass **automatically** respects accessibility settings:

### Reduce Transparency

When enabled:
- Glass becomes more opaque/frosty
- Background content is more obscured
- Better contrast for readability

```swift
// Check setting in code if needed
@Environment(\.accessibilityReduceTransparency) var reduceTransparency

var body: some View {
    if reduceTransparency {
        // Provide alternative styling if needed
    }
}
```

### Increase Contrast

When enabled:
- Glass shifts to predominantly black/white
- Borders become more prominent
- Higher contrast ratios

```swift
@Environment(\.colorSchemeContrast) var contrast

var body: some View {
    if contrast == .increased {
        // Adjust colors for higher contrast
    }
}
```

### Reduce Motion

When enabled:
- Morphing animations are subdued
- Transitions are shorter/simpler
- Less visual movement

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion

var body: some View {
    withAnimation(reduceMotion ? .none : .spring) {
        // Animation
    }
}
```

---

## UIKit/AppKit Integration

### Scene Bridging

Bring SwiftUI glass into UIKit apps:

```swift
class ViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()

        let swiftUIView = GlassButtonView()
        let hostingController = UIHostingController(rootView: swiftUIView)

        addChild(hostingController)
        view.addSubview(hostingController.view)
        hostingController.didMove(toParent: self)
    }
}

struct GlassButtonView: View {
    var body: some View {
        Button("SwiftUI Glass") { }
            .buttonStyle(.glass)
    }
}
```

### UIViewControllerRepresentable

Wrap UIKit in SwiftUI with glass:

```swift
struct LegacyViewWrapper: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> LegacyViewController {
        LegacyViewController()
    }

    func updateUIViewController(_ vc: LegacyViewController, context: Context) {}
}

// Usage with glass overlay
struct ContentView: View {
    var body: some View {
        ZStack {
            LegacyViewWrapper()

            VStack {
                Spacer()
                HStack {
                    Button("Control") { }
                        .buttonStyle(.glass)
                }
                .padding()
            }
        }
    }
}
```

---

## App Icon Guidelines

### Redesigning for Liquid Glass

iOS 26 introduces new icon aesthetics:

1. **Grid System** - Follow the updated icon grid
2. **Safe Areas** - Respect new safe margins
3. **Translucency** - Consider subtle glass effects in icon
4. **Simplicity** - Reduce complexity for glass aesthetic
5. **Color** - Use colors that complement glass UI

### Icon Specifications

```
┌─────────────────────────────────┐
│     iOS 26 App Icon Grid        │
│                                 │
│  ┌─────────────────────────┐   │
│  │                         │   │
│  │    Safe Content Area    │   │
│  │                         │   │
│  │  ┌─────────────────┐   │   │
│  │  │                 │   │   │
│  │  │   Main Element  │   │   │
│  │  │                 │   │   │
│  │  └─────────────────┘   │   │
│  │                         │   │
│  └─────────────────────────┘   │
│                                 │
│  1024x1024 @ 1x                │
└─────────────────────────────────┘
```

---

## Best Practices

### DO

1. **Use glass for navigation elements** - Toolbars, tab bars, floating buttons
2. **Keep content behind glass** - Let users see through to their content
3. **Use morphing for state changes** - Connect related UI with glassEffectID
4. **Test accessibility** - Verify with Reduce Transparency enabled
5. **Maintain visual hierarchy** - Glass floats, content grounds

### DON'T

1. **Glass on content** - Don't apply glass to cards, lists, text containers
2. **Mix variants** - Never combine regular and clear glass
3. **Nest glass** - Avoid glass-on-glass layering
4. **Overuse morphing** - Reserve for meaningful state transitions
5. **Ignore accessibility** - Always test with accessibility settings

---

## Complete Example: Glass Interface

```swift
import SwiftUI

struct GlassInterfaceView: View {
    @State private var isEditing = false
    @State private var selectedTab = 0
    @Namespace private var morphing

    var body: some View {
        TabView(selection: $selectedTab) {
            // Home Tab
            NavigationStack {
                ScrollView {
                    ContentGrid()
                }
                .navigationTitle("Home")
                .toolbar {
                    ToolbarItem(placement: .primaryAction) {
                        GlassEffectContainer {
                            if isEditing {
                                HStack {
                                    Button("Done") {
                                        withAnimation(.spring(duration: 0.35)) {
                                            isEditing = false
                                        }
                                    }
                                    .glassEffect(in: Capsule())
                                    .glassEffectID("edit", in: morphing)

                                    Button("Select All") { }
                                        .glassEffect(in: Capsule())
                                        .glassEffectTransition(.scale)
                                }
                            } else {
                                Button("Edit") {
                                    withAnimation(.spring(duration: 0.35)) {
                                        isEditing = true
                                    }
                                }
                                .glassEffect(in: Capsule())
                                .glassEffectID("edit", in: morphing)
                            }
                        }
                    }
                }
            }
            .tabItem {
                Label("Home", systemImage: "house")
            }
            .tag(0)

            // Search Tab
            SearchView()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }
                .tab(role: .search)
                .tag(1)

            // Settings Tab
            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
                .tag(2)
        }
    }
}

struct ContentGrid: View {
    let items = (1...20).map { "Item \($0)" }

    var body: some View {
        LazyVGrid(columns: [
            GridItem(.adaptive(minimum: 150))
        ], spacing: 16) {
            ForEach(items, id: \.self) { item in
                ContentCard(title: item)
            }
        }
        .padding()
    }
}

struct ContentCard: View {
    let title: String

    var body: some View {
        VStack {
            RoundedRectangle(cornerRadius: 12)
                .fill(.secondary.opacity(0.2))
                .frame(height: 100)

            Text(title)
                .font(.headline)
        }
        // NO glass on content cards - they're content, not navigation
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }
}

struct SearchView: View {
    @State private var query = ""

    var body: some View {
        NavigationStack {
            List {
                ForEach(searchResults, id: \.self) { result in
                    Text(result)
                }
            }
            .navigationTitle("Search")
            .searchable(text: $query)
        }
    }

    var searchResults: [String] {
        // Filter results based on query
        []
    }
}

struct SettingsView: View {
    var body: some View {
        NavigationStack {
            List {
                Section("Account") {
                    NavigationLink("Profile") { Text("Profile") }
                    NavigationLink("Privacy") { Text("Privacy") }
                }

                Section("App") {
                    NavigationLink("Appearance") { Text("Appearance") }
                    NavigationLink("Notifications") { Text("Notifications") }
                }
            }
            .navigationTitle("Settings")
        }
    }
}

#Preview {
    GlassInterfaceView()
}
```

---

## Debugging Glass Effects

### Visual Debugging

```swift
// Temporarily add borders to see glass boundaries
View()
    .glassEffect(in: RoundedRectangle(cornerRadius: 12))
    .border(.red)  // Debug: see actual frame
```

### Check Container Scope

```swift
// Verify GlassEffectContainer is wrapping correctly
GlassEffectContainer {
    VStack {
        // All glass effects here share container
    }
}
.border(.blue)  // Debug: see container bounds
```

### Animation Debugging

```swift
// Slow down animations for debugging
withAnimation(.spring(duration: 2.0)) {  // Slower for inspection
    state.toggle()
}
```

---

## Official Resources

- [Meet Liquid Glass - WWDC25](https://developer.apple.com/videos/play/wwdc2025/219/)
- [Get to know the new design system - WWDC25](https://developer.apple.com/videos/play/wwdc2025/356/)
- [Build a SwiftUI app with the new design - WWDC25](https://developer.apple.com/videos/play/wwdc2025/323/)
- [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views)
- [Human Interface Guidelines - Materials](https://developer.apple.com/design/human-interface-guidelines/materials)
