---
name: theme-management
description: "Expert theming decisions for iOS/tvOS: when custom themes add value vs system colors suffice, color token architecture trade-offs, theme switching animation strategies, and accessibility contrast compliance. Use when designing color systems, implementing dark mode, or building theme pickers. Trigger keywords: theme, dark mode, light mode, color scheme, appearance, colorScheme, ThemeManager, adaptive colors, dynamic colors, color tokens, WCAG contrast"
version: "3.0.0"
---

# Theme Management — Expert Decisions

Expert decision frameworks for theming choices in SwiftUI. Claude knows Color and colorScheme — this skill provides judgment calls for when custom theming adds value and architecture trade-offs.

---

## Decision Trees

### Do You Need Custom Theming?

```
What's your color requirement?
├─ Standard light/dark mode only
│  └─ System colors are sufficient
│     Color(.systemBackground), Color(.label)
│
├─ Brand colors that differ from system
│  └─ Asset catalog colors (Named Colors)
│     Define light/dark variants in xcassets
│
├─ User-selectable themes (beyond light/dark)
│  └─ Full ThemeManager with custom palettes
│     User can choose "Ocean", "Forest", etc.
│
└─ White-label app (different branding per client)
   └─ Remote theme configuration
      Fetch brand colors from server
```

**The trap**: Building a ThemeManager for an app that only needs light/dark mode. Asset catalog colors already handle this automatically.

### Color Token Architecture

```
How should you organize colors?
├─ Small app (< 20 screens)
│  └─ Direct Color("name") usage
│     Don't over-engineer
│
├─ Medium app, single brand
│  └─ Color extension with static properties
│     Color.appPrimary, Color.appBackground
│
├─ Large app, design system
│  └─ Semantic tokens + primitive tokens
│     Primitives: blue500, gray100
│     Semantic: textPrimary → gray900/gray100
│
└─ Multi-brand/white-label
   └─ Protocol-based themes
      protocol Theme { var primary: Color }
```

### Theme Switching Strategy

```
When should theme changes apply?
├─ Immediate (all screens at once)
│  └─ Environment-based (@Environment(\.colorScheme))
│     System handles propagation
│
├─ Per-screen animation
│  └─ withAnimation on theme property change
│     Smooth transition within visible content
│
├─ Custom transition (like morphing)
│  └─ Snapshot + crossfade technique
│     Complex, usually not worth it
│
└─ App restart required
   └─ For deep UIKit integration
      Sometimes unavoidable with third-party SDKs
```

### Dark Mode Compliance Level

```
What's your dark mode strategy?
├─ System automatic (no custom colors)
│  └─ Free dark mode support
│     UIColor semantic colors work automatically
│
├─ Custom colors with asset catalog
│  └─ Define both appearances per color
│     Xcode handles switching
│
├─ Programmatic dark variants
│  └─ Use Color.dynamic(light:dark:)
│     More flexible, harder to maintain
│
└─ Ignoring dark mode
   └─ DON'T — accessibility issue
      Users expect dark mode support
```

---

## NEVER Do

### Color Definition

**NEVER** hardcode colors in views:
```swift
// ❌ Doesn't adapt to dark mode
Text("Hello")
    .foregroundColor(Color(red: 0, green: 0, blue: 0))
    .background(Color.white)

// ✅ Adapts automatically
Text("Hello")
    .foregroundColor(Color(.label))
    .background(Color(.systemBackground))

// Or use named colors from asset catalog
Text("Hello")
    .foregroundColor(Color("TextPrimary"))
```

**NEVER** use opposite colors for dark mode:
```swift
// ❌ Pure black/white has harsh contrast
let background = colorScheme == .dark ? Color.black : Color.white
let text = colorScheme == .dark ? Color.white : Color.black

// ✅ Use elevated surfaces and softer contrasts
let background = Color(.systemBackground)  // Slightly elevated in dark mode
let text = Color(.label)  // Not pure white in dark mode
```

**NEVER** check colorScheme when system colors suffice:
```swift
// ❌ Unnecessary — system colors do this
@Environment(\.colorScheme) var colorScheme

var textColor: Color {
    colorScheme == .dark ? .white : .black  // Reimplementing Color(.label)!
}

// ✅ Just use the semantic color
.foregroundColor(Color(.label))
```

### Theme Architecture

**NEVER** store theme in multiple places:
```swift
// ❌ State scattered — which is source of truth?
class ThemeManager {
    @Published var isDark = false
}

struct SettingsView: View {
    @AppStorage("isDark") var isDark = false  // Different storage!
}

// ✅ Single source of truth
class ThemeManager: ObservableObject {
    @AppStorage("theme") var theme: Theme = .system  // One place
}
```

**NEVER** force override system preference without user consent:
```swift
// ❌ Ignores user's system-wide preference
init() {
    UIApplication.shared.windows.first?.overrideUserInterfaceStyle = .dark
}

// ✅ Only override if user explicitly chose in-app
func applyUserPreference(_ theme: Theme) {
    switch theme {
    case .system:
        window?.overrideUserInterfaceStyle = .unspecified  // Respect system
    case .light:
        window?.overrideUserInterfaceStyle = .light
    case .dark:
        window?.overrideUserInterfaceStyle = .dark
    }
}
```

**NEVER** forget accessibility contrast requirements:
```swift
// ❌ Low contrast — fails WCAG AA
let textColor = Color(white: 0.6)  // On white background = 2.5:1 ratio
let backgroundColor = Color.white

// ✅ Meets WCAG AA (4.5:1 for normal text)
let textColor = Color(.secondaryLabel)  // System ensures compliance
let backgroundColor = Color(.systemBackground)
```

### Performance

**NEVER** recompute colors on every view update:
```swift
// ❌ Creates new color object every render
var body: some View {
    Text("Hello")
        .foregroundColor(Color(UIColor { traits in
            traits.userInterfaceStyle == .dark ? .white : .black
        }))  // New UIColor closure every time!
}

// ✅ Define once, reuse
extension Color {
    static let adaptiveText = Color(UIColor { traits in
        traits.userInterfaceStyle == .dark ? .white : .black
    })
}

var body: some View {
    Text("Hello")
        .foregroundColor(.adaptiveText)
}
```

---

## Essential Patterns

### Semantic Color System

```swift
// Primitive tokens (raw values)
extension Color {
    enum Primitive {
        static let blue500 = Color(hex: "#007AFF")
        static let blue600 = Color(hex: "#0056B3")
        static let gray900 = Color(hex: "#1A1A1A")
        static let gray100 = Color(hex: "#F5F5F5")
    }
}

// Semantic tokens (usage-based)
extension Color {
    static let textPrimary = Color("TextPrimary")  // gray900 light, gray100 dark
    static let textSecondary = Color("TextSecondary")
    static let surfacePrimary = Color("SurfacePrimary")
    static let surfaceSecondary = Color("SurfaceSecondary")
    static let interactive = Color("Interactive")  // blue500
    static let interactivePressed = Color("InteractivePressed")  // blue600

    // Feedback colors (always same hue, adjusted for mode)
    static let success = Color("Success")
    static let warning = Color("Warning")
    static let error = Color("Error")
}
```

### ThemeManager with Persistence

```swift
@MainActor
final class ThemeManager: ObservableObject {
    static let shared = ThemeManager()

    @AppStorage("selectedTheme") private var storedTheme: String = Theme.system.rawValue

    @Published private(set) var currentTheme: Theme = .system

    enum Theme: String, CaseIterable {
        case system, light, dark

        var overrideStyle: UIUserInterfaceStyle {
            switch self {
            case .system: return .unspecified
            case .light: return .light
            case .dark: return .dark
            }
        }
    }

    private init() {
        currentTheme = Theme(rawValue: storedTheme) ?? .system
        applyTheme(currentTheme)
    }

    func setTheme(_ theme: Theme) {
        currentTheme = theme
        storedTheme = theme.rawValue
        applyTheme(theme)
    }

    private func applyTheme(_ theme: Theme) {
        // Apply to all windows (handles multiple scenes)
        for scene in UIApplication.shared.connectedScenes {
            guard let windowScene = scene as? UIWindowScene else { continue }
            for window in windowScene.windows {
                window.overrideUserInterfaceStyle = theme.overrideStyle
            }
        }
    }
}
```

### Contrast Validation

```swift
extension Color {
    func contrastRatio(against background: Color) -> Double {
        let fgLuminance = relativeLuminance
        let bgLuminance = background.relativeLuminance

        let lighter = max(fgLuminance, bgLuminance)
        let darker = min(fgLuminance, bgLuminance)

        return (lighter + 0.05) / (darker + 0.05)
    }

    var meetsWCAGAA: Bool {
        // Check against both light and dark backgrounds
        let lightBg = Color.white
        let darkBg = Color.black
        return contrastRatio(against: lightBg) >= 4.5 ||
               contrastRatio(against: darkBg) >= 4.5
    }

    private var relativeLuminance: Double {
        guard let components = UIColor(self).cgColor.components,
              components.count >= 3 else { return 0 }

        func linearize(_ value: CGFloat) -> Double {
            let v = Double(value)
            return v <= 0.03928 ? v / 12.92 : pow((v + 0.055) / 1.055, 2.4)
        }

        return 0.2126 * linearize(components[0]) +
               0.7152 * linearize(components[1]) +
               0.0722 * linearize(components[2])
    }
}
```

---

## Quick Reference

### When to Use Custom Theming

| Scenario | Solution |
|----------|----------|
| Standard light/dark | System colors only |
| Brand colors | Asset catalog named colors |
| User-selectable themes | ThemeManager + color palettes |
| White-label | Remote config + theme protocol |

### System vs Custom Colors

| Need | System | Custom |
|------|--------|--------|
| Text colors | Color(.label), Color(.secondaryLabel) | Only if brand requires |
| Backgrounds | Color(.systemBackground) | Only if brand requires |
| Dividers | Color(.separator) | Rarely |
| Tint/accent | Color.accentColor | Usually brand color |

### Contrast Ratios (WCAG)

| Level | Normal Text | Large Text | Use Case |
|-------|-------------|------------|----------|
| AA | 4.5:1 | 3:1 | Minimum acceptable |
| AAA | 7:1 | 4.5:1 | Enhanced readability |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| Color(red:green:blue:) in view | No dark mode | Use semantic colors |
| @Environment colorScheme everywhere | Over-engineering | System colors adapt automatically |
| Pure black/white | Harsh contrast | Elevated surfaces |
| Theme in multiple @AppStorage | Split source of truth | Single ThemeManager |
| window.overrideUserInterfaceStyle in init | Ignores user pref | Only on explicit user action |
