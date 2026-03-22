---
name: ios-accessibility
description: "Implement, review, or improve accessibility in iOS/macOS apps with SwiftUI and UIKit. Use when adding VoiceOver support with accessibility labels, hints, values, and traits; when grouping or reordering accessibility elements; when managing focus with @AccessibilityFocusState; when supporting Dynamic Type with @ScaledMetric; when building custom rotors or accessibility actions; when auditing a11y compliance; or when adapting UI for assistive technologies and system accessibility preferences."
---

# iOS Accessibility — SwiftUI and UIKit

Every user-facing view must be usable with VoiceOver, Switch Control, Voice Control, Full Keyboard Access, and other assistive technologies. This skill covers the patterns and APIs required to build accessible iOS apps.

## Contents

- [Core Principles](#core-principles)
- [How VoiceOver Reads Elements](#how-voiceover-reads-elements)
- [SwiftUI Accessibility Modifiers](#swiftui-accessibility-modifiers)
- [Focus Management](#focus-management)
- [Dynamic Type](#dynamic-type)
- [Custom Rotors](#custom-rotors)
- [System Accessibility Preferences](#system-accessibility-preferences)
- [Decorative Content](#decorative-content)
- [Assistive Access (iOS 18+)](#assistive-access-ios-18)
- [UIKit Accessibility Patterns](#uikit-accessibility-patterns)
- [Accessibility Custom Content](#accessibility-custom-content)
- [Testing Accessibility](#testing-accessibility)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

---

## Core Principles

1. Every interactive element MUST have an accessible label. If no visible text exists, add `.accessibilityLabel`.
2. Every custom control MUST have correct traits via `.accessibilityAddTraits` (never direct assignment).
3. Decorative images MUST be hidden from assistive technologies.
4. Sheet and dialog dismissals MUST return VoiceOver focus to the trigger element.
5. All tap targets MUST be at least 44x44 points.
6. Dynamic Type MUST be supported everywhere (system fonts, `@ScaledMetric`, adaptive layouts).
7. No information conveyed by color alone -- always provide text or icon alternatives.
8. System accessibility preferences MUST be respected: Reduce Motion, Reduce Transparency, Bold Text, Increase Contrast.

## How VoiceOver Reads Elements

VoiceOver reads element properties in a fixed, non-configurable order:

**Label -> Value -> Trait -> Hint**

Design your labels, values, and hints with this reading order in mind.

## SwiftUI Accessibility Modifiers

See `references/a11y-patterns.md` for detailed SwiftUI modifier examples (labels, hints, traits, grouping, custom controls, adjustable actions, and custom actions).

## Focus Management

Focus management is where most apps fail. When a sheet, alert, or popover is dismissed, VoiceOver focus MUST return to the element that triggered it.

### @AccessibilityFocusState (iOS 15+)

`@AccessibilityFocusState` is a property wrapper that reads and writes the current accessibility focus. It works with `Bool` for single-target focus or an optional `Hashable` enum for multi-target focus.

```swift
struct ContentView: View {
    @State private var showSheet = false
    @AccessibilityFocusState private var focusOnTrigger: Bool

    var body: some View {
        Button("Open Settings") { showSheet = true }
            .accessibilityFocused($focusOnTrigger)
            .sheet(isPresented: $showSheet) {
                SettingsSheet()
                    .onDisappear {
                        // Slight delay allows the transition to complete before moving focus
                        Task { @MainActor in
                            try? await Task.sleep(for: .milliseconds(100))
                            focusOnTrigger = true
                        }
                    }
            }
    }
}
```

### Multi-Target Focus with Enum

```swift
enum A11yFocus: Hashable {
    case nameField
    case emailField
    case submitButton
}

struct FormView: View {
    @AccessibilityFocusState private var focus: A11yFocus?

    var body: some View {
        Form {
            TextField("Name", text: $name)
                .accessibilityFocused($focus, equals: .nameField)
            TextField("Email", text: $email)
                .accessibilityFocused($focus, equals: .emailField)
            Button("Submit") { validate() }
                .accessibilityFocused($focus, equals: .submitButton)
        }
    }

    func validate() {
        if name.isEmpty {
            focus = .nameField // Move VoiceOver to the invalid field
        }
    }
}
```

### Custom Modals

Custom overlay views need the `.isModal` trait to trap VoiceOver focus and an escape action for dismissal:

```swift
CustomDialog()
    .accessibilityAddTraits(.isModal)
    .accessibilityAction(.escape) { dismiss() }
```

### Accessibility Notifications (UIKit)

When you need to announce changes or move focus imperatively in UIKit contexts:

```swift
// Announce a status change (e.g., "Item deleted", "Upload complete")
UIAccessibility.post(notification: .announcement, argument: "Upload complete")

// Partial screen update -- move focus to a specific element
UIAccessibility.post(notification: .layoutChanged, argument: targetView)

// Full screen transition -- move focus to the new screen
UIAccessibility.post(notification: .screenChanged, argument: newScreenView)
```

## Dynamic Type

See `references/a11y-patterns.md` for Dynamic Type and adaptive layout examples, including @ScaledMetric and minimum tap target patterns.

## Custom Rotors

Rotors let VoiceOver users quickly navigate to specific content types. Add custom rotors for content-heavy screens. See `references/a11y-patterns.md` for complete rotor examples.

## System Accessibility Preferences

Always respect these environment values:

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion
@Environment(\.accessibilityReduceTransparency) var reduceTransparency
@Environment(\.colorSchemeContrast) var contrast         // .standard or .increased
@Environment(\.legibilityWeight) var legibilityWeight    // .regular or .bold
```

### Reduce Motion

Replace movement-based animations with crossfades or no animation:

```swift
withAnimation(reduceMotion ? nil : .spring()) {
    showContent.toggle()
}
content.transition(reduceMotion ? .opacity : .slide)
```

### Reduce Transparency, Increase Contrast, Bold Text

```swift
// Solid backgrounds when transparency is reduced
.background(reduceTransparency ? Color(.systemBackground) : Color(.systemBackground).opacity(0.85))

// Stronger colors when contrast is increased
.foregroundStyle(contrast == .increased ? .primary : .secondary)

// Bold weight when system bold text is enabled
.fontWeight(legibilityWeight == .bold ? .bold : .regular)
```

## Decorative Content

```swift
// Decorative images: hidden from VoiceOver
Image(decorative: "background-pattern")
Image("visual-divider").accessibilityHidden(true)

// Icon next to text: Label handles this automatically
Label("Settings", systemImage: "gear")

// Icon-only buttons: MUST have an accessibility label
Button(action: { }) {
    Image(systemName: "gear")
}
.accessibilityLabel("Settings")
```

## Assistive Access (iOS 18+)

Assistive Access provides a simplified interface for users with cognitive disabilities. Apps should support this mode:

```swift
// Check if Assistive Access is active (iOS 18+)
@Environment(\.accessibilityAssistiveAccessEnabled) var isAssistiveAccessEnabled

var body: some View {
    if isAssistiveAccessEnabled {
        SimplifiedContentView()
    } else {
        FullContentView()
    }
}
```

Key guidelines:
- Reduce visual complexity: fewer controls, larger tap targets, simpler navigation
- Use clear, literal language for labels and instructions
- Minimize the number of choices presented at once
- Test with Assistive Access enabled in Settings > Accessibility > Assistive Access

## UIKit Accessibility Patterns

When working with UIKit views:

- Set `isAccessibilityElement = true` on meaningful custom views.
- Set `accessibilityLabel` on all interactive elements without visible text.
- Use `.insert()` and `.remove()` for trait modification (not direct assignment).
- Set `accessibilityViewIsModal = true` on custom overlay views to trap focus.
- Post `.announcement` for transient status messages.
- Post `.layoutChanged` with a target view for partial screen updates.
- Post `.screenChanged` for full screen transitions.

```swift
// UIKit trait modification
customButton.accessibilityTraits.insert(.button)
customButton.accessibilityTraits.remove(.staticText)

// Modal overlay
overlayView.accessibilityViewIsModal = true
```

## Accessibility Custom Content

See `references/a11y-patterns.md` for UIKit accessibility patterns and custom content examples.

```swift
ProductRow(product: product)
    .accessibilityCustomContent("Price", product.formattedPrice)
    .accessibilityCustomContent("Rating", "\(product.rating) out of 5")
    .accessibilityCustomContent(
        "Availability",
        product.inStock ? "In stock" : "Out of stock",
        importance: .high  // .high reads automatically with the element
    )
```

## Testing Accessibility

- **Accessibility Inspector** (Xcode > Open Developer Tool): Audit views for missing labels, traits, and contrast issues. Run audits against the Simulator or connected device.
- **VoiceOver testing**: Enable in Settings > Accessibility > VoiceOver. Navigate every screen with swipe gestures.
- **Dynamic Type**: Test with all text sizes in Settings > Accessibility > Display & Text Size > Larger Text.

## Common Mistakes

1. **Direct trait assignment**: `.accessibilityTraits(.isButton)` overwrites all existing traits. Use `.accessibilityAddTraits(.isButton)`.
2. **Missing focus restoration**: Dismissing sheets without returning VoiceOver focus to the trigger element.
3. **Ungrouped list rows**: Multiple text elements per row create excessive swipe stops. Use `.accessibilityElement(children: .combine)`.
4. **Redundant trait in labels**: `.accessibilityLabel("Settings button")` reads as "Settings button, button." Omit the type.
5. **Missing labels on icon-only buttons**: Every `Image`-only button MUST have `.accessibilityLabel`.
6. **Ignoring Reduce Motion**: Always check `accessibilityReduceMotion` before movement animations.
7. **Fixed font sizes**: `.font(.system(size: 16))` ignores Dynamic Type. Use `.font(.body)` or similar text styles.
8. **Small tap targets**: Icons without `frame(minWidth: 44, minHeight: 44)` and `.contentShape()`.
9. **Color as sole indicator**: Red/green for error/success without text or icon alternatives.
10. **Missing `.isModal` on overlays**: Custom modals without `.accessibilityAddTraits(.isModal)` let VoiceOver escape.

## Review Checklist

For every user-facing view, verify:

- [ ] Every interactive element has an accessible label
- [ ] Custom controls use correct traits via `.accessibilityAddTraits`
- [ ] Decorative images are hidden (`Image(decorative:)` or `.accessibilityHidden(true)`)
- [ ] List rows group content with `.accessibilityElement(children: .combine)`
- [ ] Sheets and dialogs return focus to the trigger on dismiss
- [ ] Custom overlays have `.isModal` trait and escape action
- [ ] All tap targets are at least 44x44 points
- [ ] Dynamic Type supported (`@ScaledMetric`, system fonts, adaptive layouts)
- [ ] Reduce Motion respected (no movement animations when enabled)
- [ ] Reduce Transparency respected (solid backgrounds when enabled)
- [ ] Increase Contrast respected (stronger foreground colors)
- [ ] No information conveyed by color alone
- [ ] Custom actions provided for swipe-to-reveal and context menu features
- [ ] Icon-only buttons have labels
- [ ] Heading traits set on section headers
- [ ] Custom accessibility types and notification payloads are `Sendable` when passed across concurrency boundaries

## References

- Detailed patterns: `references/a11y-patterns.md`

