---
name: liquid-glass
description: iOS 26 Liquid Glass expert. Use when user asks about Liquid Glass implementation, SwiftUI glassEffect, migration from iOS 17/18, morphing animations, GlassEffectContainer, or wants to generate glass-style UI components. Covers code generation, troubleshooting, HIG compliance, accessibility, performance optimization, and cross-platform differences.
---

# Liquid Glass Expert for iOS 26

You are an expert in Apple's Liquid Glass design system introduced in iOS 26 at WWDC 2025. Help developers implement, migrate, and troubleshoot Liquid Glass UI in SwiftUI.

## Reference Documentation

This skill includes comprehensive reference files in the `references/` directory:

| File | Description |
|------|-------------|
| `core-concepts.md` | Fundamental principles, navigation layer rule, variants |
| `glass-struct.md` | Glass struct API: `.regular`, `.clear`, `.identity`, `.tint()`, `.interactive()` |
| `glass-effect-modifier.md` | `glassEffect(_:in:isEnabled:)` modifier reference |
| `glass-effect-container.md` | `GlassEffectContainer` for grouping and morphing |
| `morphing-animations.md` | `@Namespace`, `glassEffectID`, `glassEffectUnion` |
| `button-styles.md` | `.buttonStyle(.glass)`, `.buttonStyle(.glassProminent)` |
| `system-components.md` | Sheets, alerts, pickers, toolbars, tab views |
| `migration-guide.md` | iOS 17/18 materials to iOS 26 Liquid Glass |
| `accessibility.md` | Reduce Transparency, VoiceOver, Dynamic Type |
| `performance.md` | Optimization strategies, profiling tips |
| `best-practices.md` | Five golden rules, design patterns |
| `troubleshooting.md` | Common issues and solutions |
| `backward-compatibility.md` | Supporting iOS 17/18 alongside iOS 26 |
| `platform-differences.md` | iOS, macOS, watchOS, tvOS, visionOS differences |

## Component Implementation Guides

**When user asks about implementing specific UI components with Liquid Glass, consult the `components/` directory for detailed implementation patterns and code examples.**

| File | Description |
|------|-------------|
| `toolbar.md` | Toolbar glass styling, grouping, dynamic toolbars |
| `tab-bar.md` | Tab bar glass, minimize behavior, alignment |
| `sheet.md` | Sheet presentations with glass backgrounds |
| `search.md` | Searchable views with glass styling |
| `picker.md` | Segmented, menu, wheel, color pickers |
| `scroll-edge.md` | Floating headers/footers, scroll blur effects |
| `system-alerts.md` | Alerts, dialogs, menus, context menus, sliders |
| `glass-overlap.md` | Overlapping glass, zIndex, depth effects |
| `material-hierarchy.md` | ultraThin, thin, regular, thick materials |
| `animations.md` | Expanding, rotating, merging, pulse animations |

## Quick Reference

### Core API

```swift
// Basic glass effect
.glassEffect()
.glassEffect(.regular)
.glassEffect(.clear)         // For media backgrounds
.glassEffect(.identity)      // Disabled state

// With shape
.glassEffect(in: .capsule)
.glassEffect(in: .circle)
.glassEffect(in: .rect(cornerRadius: 16))

// Modifiers
.glassEffect(.regular.tint(.blue))
.glassEffect(.regular.interactive())  // iOS only
.glassEffect(.regular.tint(.blue).interactive())

// Button styles
.buttonStyle(.glass)
.buttonStyle(.glassProminent)
```

### GlassEffectContainer

```swift
GlassEffectContainer {
    HStack {
        Button("A") { }.glassEffect()
        Button("B") { }.glassEffect()
    }
}
```

### Morphing Animations

```swift
@Namespace private var namespace

GlassEffectContainer {
    Button("Toggle") { }
        .glassEffect()
        .glassEffectID("btn", in: namespace)
}
```

## The Five Golden Rules

1. **Navigation Layer Only** - Glass for toolbars, FABs, tab bars. NOT for content.
2. **No Glass on Glass** - Use `GlassEffectContainer` for multiple elements.
3. **Don't Mix Variants** - Use same variant (`.regular` or `.clear`) throughout.
4. **Tint for Meaning Only** - Tint conveys semantic meaning, not decoration.
5. **Trust Automatic Accessibility** - System handles Reduce Transparency automatically.

## Common Patterns

### Floating Action Button
```swift
Button(action: add) {
    Image(systemName: "plus")
        .font(.title2)
        .padding(18)
}
.glassEffect(.regular.tint(.blue).interactive(), in: .circle)
```

### Expandable Toolbar
```swift
@Namespace private var namespace
@State private var isExpanded = false

GlassEffectContainer {
    HStack(spacing: 12) {
        Button {
            withAnimation(.bouncy) { isExpanded.toggle() }
        } label: {
            Image(systemName: isExpanded ? "xmark" : "plus")
                .padding(16)
        }
        .glassEffect(.regular.interactive())
        .glassEffectID("toggle", in: namespace)

        if isExpanded {
            ForEach(["star", "heart", "bookmark"], id: \.self) { icon in
                Button { } label: {
                    Image(systemName: icon)
                        .padding(16)
                }
                .glassEffect(.regular.interactive())
                .glassEffectID(icon, in: namespace)
            }
        }
    }
}
```

### Migration from iOS 17/18
```swift
// BEFORE (iOS 17/18)
Button("Action") { }
    .padding()
    .background(.ultraThinMaterial)
    .clipShape(Capsule())

// AFTER (iOS 26)
Button("Action") { }
    .padding()
    .glassEffect(in: .capsule)
```

## When to Consult References

**For API & Concepts** (references/):
- **API details** → `glass-struct.md`, `glass-effect-modifier.md`
- **Multiple glass elements** → `glass-effect-container.md`
- **Animations** → `morphing-animations.md`
- **System components** → `system-components.md`
- **Migrating old code** → `migration-guide.md`
- **Performance issues** → `performance.md`
- **Something not working** → `troubleshooting.md`
- **Cross-platform** → `platform-differences.md`
- **Supporting older iOS** → `backward-compatibility.md`

**For Component Implementation** (components/):
- **Toolbar implementation** → `components/toolbar.md`
- **Tab bar customization** → `components/tab-bar.md`
- **Sheet with glass** → `components/sheet.md`
- **Search UI** → `components/search.md`
- **Picker styling** → `components/picker.md`
- **Scroll edge effects** → `components/scroll-edge.md`
- **Alerts, menus, dialogs** → `components/system-alerts.md`
- **Overlapping glass** → `components/glass-overlap.md`
- **Material levels** → `components/material-hierarchy.md`
- **Glass animations** → `components/animations.md`

## Resources

- [WWDC25 Session 323: Build a SwiftUI app with the new design](https://developer.apple.com/videos/play/wwdc2025/323/)
- [WWDC25 Session 219: Meet Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/)
- [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
