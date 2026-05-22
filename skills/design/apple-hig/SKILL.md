---
name: apple-hig
description: Expert guide for designing iOS, macOS, watchOS, tvOS, and visionOS apps following Apple Human Interface Guidelines. Use when building Apple platform apps or interfaces, implementing SF Symbols, designing with iOS components, following accessibility guidelines, or creating native Apple experiences. Covers design principles, patterns, components, typography, color, layout, navigation, and platform-specific conventions.
---

# Apple Human Interface Guidelines Skill

Design exceptional experiences for Apple platforms following official Apple HIG principles, patterns, and best practices.

## Core Design Principles

### Clarity
- **Text must be legible** at every size
- **Icons should be precise and lucid**
- **Adornments are subtle and appropriate**
- **Functionality is obvious through focus on content**

### Deference
- **Content fills the entire screen** while UI stays out of the way
- **Translucency and blurring** hint at more content
- **Minimal use of bezels, gradients, and shadows** keeps interface light and airy

### Depth
- **Visual layers and realistic motion** convey hierarchy and vitality
- **Touch and discoverability** heighten delight
- **Smooth transitions** maintain spatial orientation

## Platform-Specific Guidelines

###iOS / iPadOS

**Key Characteristics:**
- Touch-first interaction
- Portrait and landscape orientations
- Safe area respect (notch, Dynamic Island, home indicator)
- Gestures: swipe, tap, long press, pinch, rotate

**Layout:**
- Use **SF Pro** text (system font)
- Respect safe areas and readable content guides
- Adopt **Auto Layout** for adaptive interfaces
- Support **Dynamic Type** for accessibility

**Navigation:**
- **Tab Bar:** 3-5 primary destinations, always visible
- **Navigation Bar:** Hierarchical browsing, back button
- **Search:** Prominent when important to app experience

For complete iOS patterns, see [references/ios.md](references/ios.md)

### macOS

**Key Characteristics:**
- Mouse/trackpad/keyboard interaction
- Resizable windows
- Menu bar at top of screen
- Dock for launching apps

**Layout:**
- Use **SF Pro** (system font)
- Window controls (close, minimize, zoom) on left
- **Sidebars** for navigation (leading edge)
- **Toolbars** for primary actions

**Interaction:**
- Right-click context menus
- Keyboard shortcuts (⌘ Command key)
- Drag and drop between windows

For complete macOS patterns, see [references/macos.md](references/macos.md)

### watchOS

**Key Characteristics:**
- Glanceable information
- Quick interactions
- Digital Crown and side button
- Always-on display support

**Layout:**
- **SF Compact** (rounded system font for watches)
- Edge-to-edge content
- Vertical scrolling preferred

**Interaction:**
- **Tap:** Primary action
- **Digital Crown:** Scroll and zoom
- **Force Touch:** (older models) Context menu
- **Raise to wake**

For complete watchOS patterns, see [references/watchos.md](references/watchos.md)

### tvOS

**Key Characteristics:**
- 10-foot viewing distance
- Siri Remote (directional pad + touch)
- Focus-driven navigation
- Parallax effects

**Layout:**
- **SF Pro** (system font)
- Large touch targets (minimum 250pt)
- Grid layouts for content
- Focus engine handles navigation

**Interaction:**
- **Directional:** Up/down/left/right focus movement
- **Select (click):** Primary action
- **Menu:** Back navigation
- **Siri:** Voice commands

For complete tvOS patterns, see [references/tvos.md](references/tvos.md)

### visionOS

**Key Characteristics:**
- Spatial computing environment
- 3D depth and windows
- Eye tracking + hand gestures
- Immersive and windowed modes

**Layout:**
- **Depth and layers** in 3D space
- **Glass materials** with vibrancy
- **SF Pro** (system font)

**Interaction:**
- **Gaze + pinch:** Primary selection
- **Hand gestures:** Tap, drag, rotate
- **Voice:** Siri commands
- **Immersion:** Dial controls environment blend

For complete visionOS patterns, see [references/visionos.md](references/visionos.md)

## Typography

### SF Symbols
- **6,000+ icons** designed by Apple
- **Variable weight and scale** (Ultralight to Black)
- **Multicolor, hierarchical, palette, monochrome** rendering modes
- **SF Symbols 6** latest version

**Usage:**
```swift
Image(systemName: "star.fill")
Image(systemName: "heart.circle.fill")
```

**Guidelines:**
- Match symbol weight to text weight
- Use filled variants for selected states
- Leverage multicolor for semantic meaning

### San Francisco (SF)
Apple's system font family optimized for legibility:

- **SF Pro:** iOS, macOS, tvOS
- **SF Compact:** watchOS (rounded)
- **SF Mono:** Code and tabular data
- **SF Arabic, SF Hebrew:** Localized variants

**Text Styles (Dynamic Type):**
- Large Title, Title 1/2/3
- Headline, Body, Callout
- Subheadline, Footnote, Caption 1/2

**Always support Dynamic Type** for accessibility.

## Color

### System Colors
Use semantic colors that adapt to light/dark mode:

- **Label:** Primary text
- **Secondary Label:** Secondary text
- **Tertiary Label:** Disabled text
- **System Background:** Main background
- **System Fill:** Fill colors for UI elements

### Accent Colors
- Use **accent color** for interactive elements (buttons, links)
- Ensure **sufficient contrast** (WCAG AA: 4.5:1 for text)
- Test in **both light and dark modes**

### Vibrancy
- **Materials:** Blur backgrounds to show depth
- **Vibrancy:** Colors that adapt to material behind them

## Components

### iOS Components

**Buttons:**
- Filled, Tinted, Gray, Plain styles
- Size: Small, Medium, Large
- Use SF Symbols for icons

**Lists:**
- Inset grouped style (modern iOS)
- Swipe actions (leading/trailing)
- Context menus

**Sheets:**
- Modal presentation
- Detents: medium, large
- Drag to dismiss

**Navigation:**
- Large titles (iOS 11+)
- Inline titles for scrolled state
- Search bar integration

For all iOS components, see [references/ios-components.md](references/ios-components.md)

### macOS Components

**Windows:**
- Standard, utility, panel types
- Titlebar styles: default, transparent, unified
- Sidebars and split views

**Toolbars:**
- Icon + text or icon-only buttons
- Segmented controls for views
- Search fields

For all macOS components, see [references/macos-components.md](references/macos-components.md)

## Layout & Spacing

### Grid System
- **8pt grid** as baseline (iOS, macOS)
- **Margins:** 16pt (iPhone), 20pt (iPad), 20pt (Mac)
- **Spacing:** 8pt, 16pt, 24pt, 32pt standard increments

### Safe Areas
- **Top:** Status bar, notch, Dynamic Island
- **Bottom:** Home indicator (iPhone), dock (iPad)
- **Leading/Trailing:** Avoid placing content too close to edges

### Adaptive Layouts
- **Size classes:** Compact, Regular (width/height)
- **Trait variations:** Light/Dark mode, Dynamic Type sizes
- Support **landscape and portrait**

## Accessibility

### VoiceOver
- Provide meaningful **accessibility labels**
- Group related elements
- Ensure logical **focus order**

### Dynamic Type
- Support all text sizes (from -3 to +7 default)
- Test at **Accessibility sizes** (AX1-AX5)
- Use **scalable fonts** and layouts

### Color Contrast
- **WCAG AA:** 4.5:1 for normal text, 3:1 for large text
- **WCAG AAA:** 7:1 for normal text, 4.5:1 for large text
- Test with **grayscale** and **color blindness** modes

### Reduce Motion
- Provide alternatives to animations
- Use **crossfade** instead of slides when motion reduced

## Interaction Patterns

### Gestures (iOS/iPadOS)
- **Tap:** Primary action
- **Long press:** Context menu or drag preview
- **Swipe:** Navigate, delete, reveal actions
- **Pinch:** Zoom in/out
- **Rotate:** Rotate content
- **Edge swipe:** Back navigation

### Haptics (iOS)
- **Impact:** Physical collision or boundary
- **Notification:** Success, warning, error
- **Selection:** Picker or toggle change

### Keyboard Shortcuts (macOS/iPadOS)
- **⌘ Command:** Primary actions (⌘N new, ⌘S save)
- **⇧ Shift:** Modify command (⇧⌘S save as)
- **⌥ Option:** Alternative behavior
- **⌃ Control:** Context-specific

## Animation & Motion

### Duration
- **Quick:** 0.2-0.3s (button press, small transitions)
- **Standard:** 0.3-0.5s (screen transitions, sheets)
- **Slow:** 0.5-0.8s (complex, spatial transitions)

### Easing
- **Ease In/Out:** Standard for most animations
- **Spring:** Natural, playful motion
- **Linear:** Progress indicators only

### Principles
- **Continuity:** Elements smoothly transition
- **Anticipation:** Hint at upcoming change
- **Follow-through:** Motion completes naturally

## Dark Mode

### Guidelines
- **Test both modes** during development
- Use **semantic colors** (system colors adapt automatically)
- **Elevate** surfaces with subtle color increases (not just lighter)
- **Avoid pure black** (#000000) — use dark gray for true blacks

### Materials
- iOS: `.systemBackground`, `.secondarySystemBackground`, `.tertiarySystemBackground`
- macOS: `.windowBackgroundColor`, `.controlBackgroundColor`

## Platform Integration

### iOS Features
- **Widgets:** Home Screen, Lock Screen, StandBy
- **Live Activities:** Dynamic Island, Lock Screen
- **App Clips:** Lightweight app experiences
- **Shortcuts:** Siri Shortcuts integration
- **App Intents:** System-level actions

### macOS Features
- **Menu Bar:** Global app menus
- **Dock:** App icon with badges
- **Touch Bar:** (older MacBook Pros)
- **Extensions:** Share, Today, Finder
- **Continuity:** Handoff, Universal Clipboard

## Quick Reference

| Platform | Font | Grid | Safe Areas | Primary Interaction |
|----------|------|------|------------|-------------------|
| iOS | SF Pro | 8pt | Yes (notch/home indicator) | Touch |
| macOS | SF Pro | 8pt | No | Mouse/keyboard |
| watchOS | SF Compact | - | Yes (round/square) | Digital Crown + tap |
| tvOS | SF Pro | - | Yes (overscan) | Siri Remote focus |
| visionOS | SF Pro | - | Yes (spatial bounds) | Gaze + gesture |

---

## Resources

- [iOS Patterns](references/ios.md) - Complete iOS component library
- [macOS Patterns](references/macos.md) - Complete macOS component library
- [watchOS Patterns](references/watchos.md) - Complete watchOS component library  
- [tvOS Patterns](references/tvos.md) - Complete tvOS component library
- [visionOS Patterns](references/visionos.md) - Complete visionOS patterns
- [iOS Components Reference](references/ios-components.md) - All iOS UIKit/SwiftUI components
- [macOS Components Reference](references/macos-components.md) - All macOS AppKit/SwiftUI components

---

*Based on Apple Human Interface Guidelines - https://developer.apple.com/design/human-interface-guidelines*
