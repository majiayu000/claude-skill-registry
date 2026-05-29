---
name: stitch-swiftui-components
description: Converts Stitch mobile designs into SwiftUI views for native iOS apps — VStack/HStack/ZStack layout mapping, Color asset tokens with dark mode, NavigationStack/TabView routing, and Xcode project structure.
allowed-tools:
  - "stitch*:*"
  - "Bash"
  - "Read"
  - "Write"
---

# Stitch → SwiftUI (Native iOS)

You are a Swift/SwiftUI engineer. You convert Stitch mobile designs (deviceType: MOBILE) into native iOS SwiftUI views — `.swift` files that build and run in Xcode. You follow Apple's Human Interface Guidelines and produce code that feels like it belongs on iOS.

## When to use this skill

Use this skill when:
- The user wants **native iOS** output from a Stitch design
- The user mentions "SwiftUI", "Xcode", "iOS", "native iOS app"
- The design was generated with `deviceType: MOBILE`

**Note:** This skill targets iOS 16+ with SwiftUI. For cross-platform (iOS + Android), use `stitch-react-native-components` instead.

## Prerequisites

- Stitch design with `deviceType: MOBILE`
- Xcode 15+ on macOS
- Swift 5.9+

## Step 1: Retrieve the design

1. `list_tools` → find Stitch MCP prefix
2. `[prefix]:get_screen` → fetch metadata
3. Download HTML: `bash scripts/fetch-stitch.sh "[htmlCode.downloadUrl]" "temp/source.html"`
4. Check `screenshot.downloadUrl` — confirm mobile layout before converting

Only convert **MOBILE** designs. Desktop Stitch designs don't map well to SwiftUI without significant layout rethinking.

## Step 2: Xcode project structure

```
MyApp/
├── MyApp.swift              ← @main entry point
├── ContentView.swift        ← Root view (TabView or NavigationStack)
├── Theme/
│   ├── ThemeTokens.swift    ← Design token constants
│   └── Color+App.swift      ← Color extension with semantic names
├── Views/
│   ├── [ScreenName]View.swift   ← One file per Stitch screen
│   └── Components/
│       └── [Name]View.swift     ← Reusable component views
├── Models/
│   └── MockData.swift       ← Static preview data
└── Assets.xcassets/
    └── Colors/              ← Color assets for light/dark mode
```

## Step 3: The HTML/CSS → SwiftUI layout mapping

This is the core translation. Apply these rules to every element in the Stitch HTML:

### Layout containers

| HTML/CSS pattern | → SwiftUI |
|---|---|
| `display:flex; flex-direction:column` | `VStack(alignment: .leading, spacing: 16)` |
| `display:flex; flex-direction:row` | `HStack(alignment: .center, spacing: 12)` |
| `display:flex; justify-content:space-between` | `HStack { Spacer() }` pattern |
| `position:absolute` overlay | `ZStack` with layered views |
| `display:grid` (2-column) | `LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 16)` |
| `overflow-y: scroll` | `ScrollView(.vertical, showsIndicators: false)` |
| Repeated list of items | `List` or `ForEach` inside `ScrollView + LazyVStack` |
| `position:fixed` bottom nav | `TabView` (preferred) or explicit `VStack` with `Spacer()` |

### Spacing mapping

SwiftUI uses points (1pt ≈ 1dp on non-retina, 2px on Retina @2x):

```swift
// Spacing from Tailwind → SwiftUI points
// p-1(4px)→4  p-2(8px)→8  p-3(12px)→12  p-4(16px)→16
// p-6(24px)→24  p-8(32px)→32  p-12(48px)→48  p-16(64px)→64
```

### Geometry mapping

```swift
// Tailwind rounded- → SwiftUI cornerRadius
// rounded-sm → .cornerRadius(4)
// rounded-md → .cornerRadius(8)
// rounded-lg → .cornerRadius(12)
// rounded-xl → .cornerRadius(16)
// rounded-full → .clipShape(Capsule())  or .cornerRadius(9999)
```

### Content elements

| HTML | → SwiftUI |
|---|---|
| `<p>`, `<span>`, text | `Text("content")` |
| `<h1>` | `Text("title").font(.largeTitle).fontWeight(.bold)` |
| `<h2>` | `Text("title").font(.title2).fontWeight(.semibold)` |
| `<h3>` | `Text("title").font(.headline)` |
| `<p>` body | `Text("body").font(.body)` |
| `<small>` / caption | `Text("caption").font(.caption).foregroundStyle(.secondary)` |
| `<img>` | `AsyncImage(url: URL(string: "..."))` for remote, `Image("name")` for asset |
| `<button>` primary | `Button("Label") { action() }.buttonStyle(.borderedProminent)` |
| `<button>` secondary | `Button("Label") { action() }.buttonStyle(.bordered)` |
| `<button>` ghost/text | `Button("Label") { action() }.buttonStyle(.plain)` |
| `<input type="text">` | `TextField("Placeholder", text: $binding)` |
| `<input type="password">` | `SecureField("Password", text: $binding)` |
| `<select>` | `Picker("Label", selection: $binding) { ForEach(...) }` |
| `<toggle>` / checkbox | `Toggle("Label", isOn: $binding)` |
| Icon-only button | `Button { action() } label: { Image(systemName: "xmark") }` |

### Navigation patterns

| Pattern | SwiftUI implementation |
|---------|----------------------|
| Bottom tab bar | `TabView` with `tabItem { Label("Home", systemImage: "house") }` |
| Stack navigation | `NavigationStack { ... NavigationLink(destination: ...) }` |
| Modal / sheet | `.sheet(isPresented: $showModal) { ModalView() }` |
| Full screen modal | `.fullScreenCover(isPresented: $show) { FullView() }` |
| Back navigation | Automatic with `NavigationStack` |
| Action sheet | `.confirmationDialog("Title", isPresented: $show) { ... }` |

## Step 4: Design tokens in SwiftUI

### Color extension (semantic tokens)

```swift
// Theme/Color+App.swift

import SwiftUI

extension Color {
  // Extract these hex values from the Stitch HTML's tailwind.config

  // Backgrounds
  static let appBackground = Color("AppBackground")    // Asset catalog
  static let appSurface = Color("AppSurface")

  // Brand
  static let appPrimary = Color("AppPrimary")
  static let appPrimaryFg = Color("AppPrimaryForeground")

  // Text
  static let appText = Color("AppText")
  static let appTextMuted = Color("AppTextMuted")

  // Borders
  static let appBorder = Color("AppBorder")
}
```

### Color asset catalog (light + dark)

Create named Color Sets in `Assets.xcassets/Colors/`:

For each color (e.g., `AppPrimary`):
- **Any Appearance:** `#6366F1` (the light mode value)
- **Dark Appearance:** `#818CF8` (lighter shade for dark bg)

Alternatively, define programmatically (no asset catalog needed):

```swift
// Theme/ThemeTokens.swift

import SwiftUI

struct ThemeTokens {
  let background: Color
  let surface: Color
  let primary: Color
  let primaryFg: Color
  let text: Color
  let textMuted: Color
  let border: Color

  static let light = ThemeTokens(
    background: Color(hex: "#FFFFFF"),
    surface:    Color(hex: "#F4F4F5"),
    primary:    Color(hex: "#6366F1"),
    primaryFg:  Color(hex: "#FFFFFF"),
    text:       Color(hex: "#09090B"),
    textMuted:  Color(hex: "#71717A"),
    border:     Color(hex: "#E4E4E7")
  )

  static let dark = ThemeTokens(
    background: Color(hex: "#09090B"),
    surface:    Color(hex: "#18181B"),
    primary:    Color(hex: "#818CF8"),   // Lightened for dark bg
    primaryFg:  Color(hex: "#09090B"),
    text:       Color(hex: "#FAFAFA"),
    textMuted:  Color(hex: "#A1A1AA"),
    border:     Color(hex: "#27272A")
  )
}

// Convenience: Color from hex string
extension Color {
  init(hex: String) {
    let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
    var int: UInt64 = 0
    Scanner(string: hex).scanHexInt64(&int)
    let r = Double((int & 0xFF0000) >> 16) / 255
    let g = Double((int & 0x00FF00) >> 8) / 255
    let b = Double(int & 0x0000FF) / 255
    self.init(red: r, green: g, blue: b)
  }
}
```

### Environment-based theme access

```swift
// Anywhere in a view — automatic dark mode
@Environment(\.colorScheme) var colorScheme

var theme: ThemeTokens {
  colorScheme == .dark ? .dark : .light
}

// Usage
Text("Hello")
  .foregroundStyle(theme.text)
  .background(theme.surface)
```

## Step 5: Component template

```swift
// Views/Components/StitchComponentView.swift

import SwiftUI

/// StitchComponent — [describe purpose in one sentence]
struct StitchComponentView: View {
  // MARK: - Properties (equivalent to props)
  let title: String
  var description: String = ""
  var onAction: (() -> Void)? = nil

  // MARK: - Environment
  @Environment(\.colorScheme) private var colorScheme

  private var theme: ThemeTokens {
    colorScheme == .dark ? .dark : .light
  }

  // MARK: - State
  @State private var isPressed = false

  // MARK: - Body
  var body: some View {
    VStack(alignment: .leading, spacing: 8) {
      Text(title)
        .font(.headline)
        .foregroundStyle(theme.text)

      if !description.isEmpty {
        Text(description)
          .font(.subheadline)
          .foregroundStyle(theme.textMuted)
      }

      if let action = onAction {
        Button("Action", action: action)
          .buttonStyle(.borderedProminent)
          .tint(theme.primary)
      }
    }
    .padding(16)
    .frame(maxWidth: .infinity, alignment: .leading)
    .background(theme.surface)
    .clipShape(RoundedRectangle(cornerRadius: 12))
    .overlay(
      RoundedRectangle(cornerRadius: 12)
        .stroke(theme.border, lineWidth: 1)
    )
    // Minimum touch target — 44pt Apple HIG requirement
    .frame(minHeight: 44)
  }
}

// MARK: - Preview
#Preview {
  VStack(spacing: 16) {
    StitchComponentView(title: "Card Title", description: "Supporting text")
    StitchComponentView(title: "With Action", description: "Tap the button", onAction: {})
  }
  .padding()
}
```

## Step 6: Main app entry point

```swift
// MyApp.swift
import SwiftUI

@main
struct MyApp: App {
  var body: some Scene {
    WindowGroup {
      ContentView()
    }
  }
}

// ContentView.swift — root with TabView
struct ContentView: View {
  var body: some View {
    TabView {
      HomeView()
        .tabItem {
          Label("Home", systemImage: "house")
        }
      ProfileView()
        .tabItem {
          Label("Profile", systemImage: "person")
        }
    }
  }
}
```

## Step 7: Accessibility in SwiftUI

SwiftUI handles much of this automatically, but always verify:

```swift
// Image accessibility
Image("hero-photo")
  .accessibilityLabel("Team collaborating in a modern office")

// Decorative images (screen reader skips)
Image(decorative: "background-pattern")

// Buttons — label is automatic if using Text inside
Button("Sign In") { ... }  // VoiceOver reads "Sign In, button"

// Custom accessibility label when button label is ambiguous
Button { deleteItem() } label: {
  Image(systemName: "trash")
}
.accessibilityLabel("Delete item")

// Group elements (treats as single unit)
VStack {
  Text("Sarah Johnson")
  Text("Product Designer")
}
.accessibilityElement(children: .combine)

// Dynamic type support — always use semantic fonts
Text("Headline")
  .font(.headline)   // ✅ Scales with user's text size
  // NOT .font(.system(size: 17, weight: .semibold))  // ❌ Fixed size
```

## Step 8: SwiftUI animations

SwiftUI has excellent built-in animations — use them for the micro-interactions:

```swift
// Button press spring
Button(action: primaryAction) {
  Text("Get Started")
    .padding(.horizontal, 24)
    .padding(.vertical, 14)
    .background(theme.primary)
    .foregroundStyle(theme.primaryFg)
    .clipShape(Capsule())
    .scaleEffect(isPressed ? 0.96 : 1.0)
    .animation(.spring(response: 0.2, dampingFraction: 0.6), value: isPressed)
}
.simultaneousGesture(
  DragGesture(minimumDistance: 0)
    .onChanged { _ in isPressed = true }
    .onEnded { _ in isPressed = false }
)

// Card appear transition
VStack { /* card content */ }
  .transition(.move(edge: .bottom).combined(with: .opacity))

// Respect reduced motion
@Environment(\.accessibilityReduceMotion) var reduceMotion

var animation: Animation {
  reduceMotion ? .none : .spring(response: 0.3, dampingFraction: 0.7)
}
```

## Execution steps

1. **Verify** the Stitch design uses `deviceType: MOBILE`
2. **Create Xcode project** — File → New → App, SwiftUI interface, Swift language
3. **Data layer** — create `Models/MockData.swift` from static content in the design
4. **Theme** — create `Theme/ThemeTokens.swift` with extracted hex values, and `Color+App.swift`
5. **Components** — convert the Stitch HTML sections to SwiftUI views, file by file
6. **Navigation** — wire up `TabView` (tab bar) or `NavigationStack` (stack)
7. **Build and run** — in Xcode, Cmd+R. Test on both light and dark mode (⌃⌘A toggles appearance in Simulator)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| View overflows screen | Add `.frame(maxWidth: .infinity)` + parent `ScrollView` |
| Text truncates unexpectedly | Add `.lineLimit(nil)` or `.fixedSize(horizontal: false, vertical: true)` |
| Color looks wrong in dark mode | Ensure the Color Set in Assets.xcassets has a Dark appearance set |
| Image not loading | For `AsyncImage`, check URL is valid. For local images, file must be in Assets.xcassets |
| TabView items don't show label | Content must be directly inside `.tabItem { }` — no wrapping views |
| Sheet not dismissible | Add `@Environment(\.dismiss) var dismiss` and call `dismiss()` in the sheet |
| Preview crashes | Check `#Preview` has valid mock data — never optional-unwrap without fallback |

## References

- `resources/component-template.swift` — Boilerplate SwiftUI view
- `resources/layout-mapping.md` — Full HTML/CSS → SwiftUI reference
- `resources/architecture-checklist.md` — Pre-ship checklist
- `scripts/fetch-stitch.sh` — Reliable GCS HTML downloader
