---
name: apple-hig-designer
description: Design iOS apps following Apple's Human Interface Guidelines. Generate native components, validate designs, and ensure accessibility compliance for iPhone, iPad, and Apple Watch.
---

# Apple HIG Designer

Design beautiful, native iOS apps following Apple's Human Interface Guidelines (HIG). Create accessible, intuitive interfaces with native components, proper typography, semantic colors, and Apple's design principles.

## What This Skill Does

Helps you design and build iOS apps that feel native and follow Apple's guidelines:
- **Generate iOS Components** - Create SwiftUI and UIKit components
- **Validate Designs** - Check compliance with Apple HIG
- **Ensure Accessibility** - VoiceOver, Dynamic Type, color contrast
- **Apply Design Principles** - Clarity, Deference, Depth
- **Use Semantic Colors** - Automatic dark mode support
- **Implement Typography** - San Francisco font system
- **Follow Spacing** - 8pt grid system and safe areas

## Apple's Design Principles

### 1. Clarity

**Make content clear and focused.**

Text is legible at every size, icons are precise and lucid, adornments are subtle and appropriate, and a focus on functionality drives the design.

```swift
// ✅ Clear, focused content
Text("Welcome back, Sarah")
    .font(.title)
    .foregroundColor(.primary)

// ❌ Unclear, cluttered
Text("Welcome back, Sarah!!!")
    .font(.title)
    .foregroundColor(.red)
    .background(.yellow)
    .overlay(Image(systemName: "star.fill"))
```

### 2. Deference

**UI helps people understand and interact with content, but never competes with it.**

The interface defers to content, using a light visual treatment that keeps focus on the content and gives the content room to breathe.

```swift
// ✅ Content-focused
VStack(alignment: .leading, spacing: 8) {
    Text("Article Title")
        .font(.headline)
    Text("Article content goes here...")
        .font(.body)
        .foregroundColor(.secondary)
}
.padding()

// ❌ Distracting UI
VStack(spacing: 8) {
    Text("Article Title")
        .font(.headline)
        .foregroundColor(.white)
        .background(.blue)
        .border(.red, width: 3)
}
```

### 3. Depth

**Visual layers and realistic motion convey hierarchy and help people understand relationships.**

Distinct visual layers and realistic motion impart vitality and facilitate understanding. Touch and discoverability heighten delight and enable access to functionality without losing context.

```swift
// ✅ Clear depth hierarchy
ZStack {
    Color(.systemBackground)

    VStack {
        // Card with elevation
        CardView()
            .shadow(radius: 8)
    }
}

// Using blur for depth
Text("Content")
    .background(.ultraThinMaterial)
```

## iOS UI Components

### Navigation Patterns

#### 1. Navigation Bar

**Top bar for navigation and actions.**

```swift
NavigationStack {
    List {
        Text("Item 1")
        Text("Item 2")
    }
    .navigationTitle("Title")
    .navigationBarTitleDisplayMode(.large)
    .toolbar {
        ToolbarItem(placement: .navigationBarTrailing) {
            Button("Add") {
                // Action
            }
        }
    }
}
```

**Guidelines:**
- Use large titles for top-level views
- Use inline titles for detail views
- Keep actions relevant to current context
- Maximum 2-3 toolbar items

#### 2. Tab Bar

**Bottom navigation for top-level destinations.**

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

    ProfileView()
        .tabItem {
            Label("Profile", systemImage: "person")
        }
}
```

**Guidelines:**
- 3-5 tabs maximum
- Use SF Symbols for icons
- Labels should be concise (one word)
- Never hide or disable tabs
- Don't use tab bar with toolbar in same view

#### 3. List

**Scrollable list of items.**

```swift
List {
    Section("Today") {
        ForEach(items) { item in
            NavigationLink {
                DetailView(item: item)
            } label: {
                HStack {
                    Image(systemName: item.icon)
                        .foregroundColor(.accentColor)
                    Text(item.title)
                }
            }
        }
    }
}
.listStyle(.insetGrouped)
```

**List Styles:**
- `.plain` - Edge-to-edge rows
- `.insetGrouped` - Rounded, inset sections (iOS default)
- `.sidebar` - For navigation sidebars

#### 4. Sheet (Modal)

**Present content modally.**

```swift
struct ContentView: View {
    @State private var showSheet = false

    var body: some View {
        Button("Show Details") {
            showSheet = true
        }
        .sheet(isPresented: $showSheet) {
            DetailView()
                .presentationDetents([.medium, .large])
        }
    }
}
```

**Sheet Detents:**
- `.medium` - Half screen
- `.large` - Full screen
- Custom heights available

### Form Controls

#### 1. Button

**Primary action control.**

```swift
// Filled button (primary action)
Button("Continue") {
    // Action
}
.buttonStyle(.borderedProminent)

// Bordered button (secondary action)
Button("Cancel") {
    // Action
}
.buttonStyle(.bordered)

// Plain button (tertiary action)
Button("Learn More") {
    // Action
}
.buttonStyle(.plain)
```

**Button Hierarchy:**
1. **Prominent** - Primary action (one per screen)
2. **Bordered** - Secondary actions
3. **Plain** - Tertiary actions, links

**Guidelines:**
- Minimum tap target: 44x44 points
- Use verbs for button labels
- Make destructive actions require confirmation

#### 2. TextField

**Text input control.**

```swift
@State private var username = ""
@State private var password = ""

VStack(alignment: .leading, spacing: 16) {
    // Standard text field
    TextField("Username", text: $username)
        .textFieldStyle(.roundedBorder)
        .textContentType(.username)
        .textInputAutocapitalization(.never)
        .autocorrectionDisabled()

    // Secure field
    SecureField("Password", text: $password)
        .textFieldStyle(.roundedBorder)
        .textContentType(.password)
}
```

**Text Content Types:**
- `.username` - Username field
- `.password` - Password field
- `.emailAddress` - Email field
- `.telephoneNumber` - Phone number
- `.creditCardNumber` - Credit card

#### 3. Toggle

**Boolean control (switch).**

```swift
@State private var isEnabled = false

Toggle("Enable notifications", isOn: $isEnabled)
    .toggleStyle(.switch)
```

**Guidelines:**
- Label describes what the toggle controls
- Effect should be immediate
- Use for binary choices only

#### 4. Picker

**Selection control.**

```swift
@State private var selectedSize = "Medium"
let sizes = ["Small", "Medium", "Large"]

// Menu style
Picker("Size", selection: $selectedSize) {
    ForEach(sizes, id: \.self) { size in
        Text(size).tag(size)
    }
}
.pickerStyle(.menu)

// Segmented style (for 2-5 options)
Picker("Size", selection: $selectedSize) {
    ForEach(sizes, id: \.self) { size in
        Text(size).tag(size)
    }
}
.pickerStyle(.segmented)
```

**Picker Styles:**
- `.menu` - Dropdown menu (default)
- `.segmented` - Segmented control (2-5 options)
- `.wheel` - Scrollable wheel
- `.inline` - Inline list (in forms)

### Cards and Containers

#### Card View

```swift
struct CardView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Title")
                .font(.headline)

            Text("Description goes here with some details about the content.")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .lineLimit(2)

            Spacer()

            Button("Action") {
                // Action
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
        .frame(width: 300, height: 200)
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 8, x: 0, y: 4)
    }
}
```

## Typography

### San Francisco Font System

Apple's system font designed for optimal legibility.

```swift
// Dynamic Type text styles
Text("Large Title").font(.largeTitle)      // 34pt
Text("Title").font(.title)                 // 28pt
Text("Title 2").font(.title2)              // 22pt
Text("Title 3").font(.title3)              // 20pt
Text("Headline").font(.headline)           // 17pt semibold
Text("Body").font(.body)                   // 17pt regular
Text("Callout").font(.callout)             // 16pt
Text("Subheadline").font(.subheadline)     // 15pt
Text("Footnote").font(.footnote)           // 13pt
Text("Caption").font(.caption)             // 12pt
Text("Caption 2").font(.caption2)          // 11pt
```

### Custom Fonts with Dynamic Type

```swift
// Custom font that scales with Dynamic Type
Text("Custom Text")
    .font(.custom("YourFont-Regular", size: 17, relativeTo: .body))
```

### Font Weights

```swift
Text("Light").fontWeight(.light)
Text("Regular").fontWeight(.regular)
Text("Medium").fontWeight(.medium)
Text("Semibold").fontWeight(.semibold)
Text("Bold").fontWeight(.bold)
Text("Heavy").fontWeight(.heavy)
```

### Typography Guidelines

**Do:**
- ✅ Use system font (San Francisco) for consistency
- ✅ Support Dynamic Type for accessibility
- ✅ Use semantic text styles (.headline, .body, etc.)
- ✅ Minimum body text: 17pt
- ✅ Line spacing: 120-145% of font size

**Don't:**
- ❌ Use too many font sizes (stick to system styles)
- ❌ Make text smaller than 11pt
- ❌ Use all caps for long text
- ❌ Disable Dynamic Type

## Colors

### Semantic Colors

**Colors that automatically adapt to light/dark mode.**

```swift
// UI Element Colors
Color(.label)                    // Primary text
Color(.secondaryLabel)           // Secondary text
Color(.tertiaryLabel)            // Tertiary text
Color(.quaternaryLabel)          // Watermark text

Color(.systemBackground)         // Primary background
Color(.secondarySystemBackground) // Secondary background
Color(.tertiarySystemBackground)  // Tertiary background

Color(.systemFill)               // Fill colors
Color(.secondarySystemFill)
Color(.tertiarySystemFill)
Color(.quaternarySystemFill)

Color(.separator)                // Separator lines
Color(.opaqueSeparator)          // Non-transparent separator
```

### System Colors

```swift
// Standard system colors (adapt to dark mode)
Color(.systemRed)
Color(.systemOrange)
Color(.systemYellow)
Color(.systemGreen)
Color(.systemMint)
Color(.systemTeal)
Color(.systemCyan)
Color(.systemBlue)
Color(.systemIndigo)
Color(.systemPurple)
Color(.systemPink)
Color(.systemBrown)
Color(.systemGray)
```

### Custom Colors with Dark Mode

```swift
// Define adaptive color
extension Color {
    static let customBackground = Color("CustomBackground")
}

// In Assets.xcassets, create color set with:
// - Any Appearance: #FFFFFF
// - Dark Appearance: #000000
```

### Color Contrast Guidelines

**WCAG AA Compliance:**
- Normal text: 4.5:1 contrast ratio minimum
- Large text (24pt+): 3:1 contrast ratio minimum
- UI components: 3:1 contrast ratio

**Custom colors:**
- Test with Increase Contrast enabled
- Aim for 7:1 for critical text
- Provide sufficient contrast in both modes

## Spacing and Layout

### 8-Point Grid System

**All spacing should be multiples of 8.**

```swift
// Spacing values
.padding(8)      // 8pt
.padding(16)     // 16pt (standard)
.padding(24)     // 24pt
.padding(32)     // 32pt
.padding(40)     // 40pt
.padding(48)     // 48pt

// Edge-specific padding
.padding(.horizontal, 16)
.padding(.vertical, 24)
.padding(.top, 16)
.padding(.bottom, 16)
```

### Safe Areas

**Respect device safe areas.**

```swift
// Content within safe area (default)
VStack {
    Text("Content")
}

// Extend beyond safe area
VStack {
    Color.blue
}
.ignoresSafeArea()

// Extend top only
VStack {
    Color.blue
}
.ignoresSafeArea(edges: .top)
```

### Touch Targets

**Minimum interactive size: 44x44 points.**

```swift
Button("Tap") {
    // Action
}
.frame(minWidth: 44, minHeight: 44)
```

### Spacing Guidelines

```swift
// Component spacing
VStack(spacing: 8) {       // Tight spacing
    Text("Line 1")
    Text("Line 2")
}

VStack(spacing: 16) {      // Standard spacing
    Text("Section 1")
    Text("Section 2")
}

VStack(spacing: 24) {      // Loose spacing
    SectionView()
    SectionView()
}
```

## Accessibility

### VoiceOver Support

**Screen reader for blind and low-vision users.**

```swift
// Accessible label
Image(systemName: "heart.fill")
    .accessibilityLabel("Favorite")

// Accessible value
Slider(value: $volume)
    .accessibilityLabel("Volume")
    .accessibilityValue("\(Int(volume * 100))%")

// Accessible hint
Button("Share") {
    share()
}
.accessibilityHint("Shares this item with others")

// Group elements
HStack {
    Image(systemName: "person")
    Text("John Doe")
}
.accessibilityElement(children: .combine)

// Hidden from VoiceOver
Image("decorative")
    .accessibilityHidden(true)
```

### Dynamic Type

**Support user's preferred text size.**

```swift
// Automatically supported with system fonts
Text("This text scales")
    .font(.body)

// Limit scaling (if necessary)
Text("This text has limits")
    .font(.body)
    .dynamicTypeSize(...DynamicTypeSize.xxxLarge)

// Custom font with Dynamic Type
Text("Custom font")
    .font(.custom("YourFont", size: 17, relativeTo: .body))
```

### Color Blindness

**Design for color-blind users.**

```swift
// Don't rely on color alone
HStack {
    Image(systemName: "checkmark.circle.fill")
        .foregroundColor(.green)
    Text("Success")
}

// Not just color
Circle()
    .fill(.green)
// ❌ Color only

// Better with shape/icon
HStack {
    Image(systemName: "checkmark.circle.fill")
    Circle().fill(.green)
}
// ✅ Color + shape
```

### Reduce Motion

**Respect user's motion preferences.**

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion

var animation: Animation {
    reduceMotion ? .none : .spring()
}

Button("Animate") {
    withAnimation(animation) {
        // Animate
    }
}
```

### Increase Contrast

**Support high contrast mode.**

```swift
@Environment(\.colorSchemeContrast) var contrast

var textColor: Color {
    contrast == .increased ? .primary : .secondary
}

Text("Content")
    .foregroundColor(textColor)
```

## Dark Mode

**Support both light and dark appearances.**

### Automatic Support

```swift
// Use semantic colors (automatic)
Color(.label)                // Adapts automatically
Color(.systemBackground)     // Adapts automatically
```

### Testing Dark Mode

```swift
// Preview both modes
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .preferredColorScheme(.light)

        ContentView()
            .preferredColorScheme(.dark)
    }
}
```

### Dark Mode Guidelines

**Do:**
- ✅ Use semantic colors
- ✅ Test with Increase Contrast
- ✅ Test with Reduce Transparency
- ✅ Ensure sufficient contrast in both modes

**Don't:**
- ❌ Use pure black (#000000) - use systemBackground
- ❌ Invert colors automatically
- ❌ Assume user preference

## SF Symbols

**Apple's icon system (3000+ symbols).**

```swift
// Basic symbol
Image(systemName: "heart")

// Colored symbol
Image(systemName: "heart.fill")
    .foregroundColor(.red)

// Sized symbol
Image(systemName: "heart")
    .imageScale(.large)

// Font-based sizing
Image(systemName: "heart")
    .font(.title)

// Multicolor symbols
Image(systemName: "person.crop.circle.fill.badge.checkmark")
    .symbolRenderingMode(.multicolor)

// Hierarchical rendering
Image(systemName: "heart.fill")
    .symbolRenderingMode(.hierarchical)
    .foregroundColor(.red)
```

### SF Symbols Guidelines

- Use system symbols when available
- Maintain visual weight consistency
- Use multicolor for semantic meaning
- Size appropriately for context

## App Icons

### Icon Sizes

```
iOS:
- 1024x1024 (App Store)
- 180x180 (iPhone @3x)
- 120x120 (iPhone @2x)
- 167x167 (iPad Pro)
- 152x152 (iPad @2x)

watchOS:
- 1024x1024 (App Store)
- 196x196 (49mm)
- 216x216 (45mm)
```

### Icon Design Guidelines

**Do:**
- ✅ Use simple, recognizable shapes
- ✅ Fill entire icon space
- ✅ Test on device (not just mockups)
- ✅ Use consistent visual style

**Don't:**
- ❌ Include text (very small)
- ❌ Use photos
- ❌ Replicate Apple hardware
- ❌ Use translucency

## Animation and Motion

### Standard Animations

```swift
// Spring animation (natural, bouncy)
withAnimation(.spring()) {
    offset = 100
}

// Linear animation
withAnimation(.linear(duration: 0.3)) {
    opacity = 0
}

// Ease in/out
withAnimation(.easeInOut(duration: 0.3)) {
    scale = 1.2
}
```

### Gesture-Driven

```swift
@State private var offset = CGSize.zero

var body: some View {
    Circle()
        .offset(offset)
        .gesture(
            DragGesture()
                .onChanged { value in
                    offset = value.translation
                }
                .onEnded { _ in
                    withAnimation(.spring()) {
                        offset = .zero
                    }
                }
        )
}
```

### Motion Guidelines

- Keep animations under 0.3 seconds
- Use spring animations for interactive elements
- Respect Reduce Motion setting
- Provide visual feedback for all interactions

## Best Practices

### Navigation

- **Hierarchical** - Use NavigationStack for drilldown
- **Flat** - Use TabView for peer destinations
- **Content-Driven** - Use for media apps

### Feedback

- **Visual** - Highlight on tap
- **Haptic** - Use UIImpactFeedbackGenerator
- **Audio** - Use system sounds sparingly

### Loading States

```swift
struct LoadingView: View {
    var body: some View {
        VStack {
            ProgressView()
                .scaleEffect(1.5)
            Text("Loading...")
                .font(.caption)
                .foregroundColor(.secondary)
                .padding(.top)
        }
    }
}
```

### Error States

```swift
struct ErrorView: View {
    let message: String
    let retry: () -> Void

    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "exclamationmark.triangle")
                .font(.system(size: 48))
                .foregroundColor(.orange)

            Text("Something went wrong")
                .font(.headline)

            Text(message)
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)

            Button("Try Again") {
                retry()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```

### Empty States

```swift
struct EmptyStateView: View {
    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "tray")
                .font(.system(size: 64))
                .foregroundColor(.secondary)

            Text("No Items")
                .font(.title2)

            Text("Your items will appear here")
                .font(.subheadline)
                .foregroundColor(.secondary)

            Button("Add Item") {
                // Action
            }
            .buttonStyle(.borderedProminent)
        }
    }
}
```

## Platform Considerations

### iPhone

- Design for various sizes (SE, Pro, Pro Max)
- Support portrait and landscape
- Use safe areas for notch/Dynamic Island
- Consider one-handed use

### iPad

- Support multitasking (Split View, Slide Over)
- Use sidebars for navigation
- Adapt to larger screen (don't just scale)
- Consider keyboard shortcuts
- Support external displays

### Apple Watch

- Glanceable information
- Large touch targets (>44pt)
- Minimal interaction required
- Use Digital Crown for scrolling
- Support Always-On display

## Resources

- [Apple HIG Official](https://developer.apple.com/design/human-interface-guidelines/)
- [SF Symbols App](https://developer.apple.com/sf-symbols/)
- [WWDC Videos](https://developer.apple.com/videos/)
- [Apple Design Resources](https://developer.apple.com/design/resources/)

---

**"Design is not just what it looks like and feels like. Design is how it works." - Steve Jobs**
