---
name: iOS UI & Layout
description: Standards for UIKit, Auto Layout, and Apple Human Interface Guidelines.
metadata:
  labels: [ios, uikit, autolayout, snapkit, layouts]
  triggers:
    files: ['**/*View.swift', '**/*.xib', '**/*.storyboard']
    keywords: [NSLayoutConstraint, UIStackView, SnapKit, layoutSubviews]
---

# iOS UI & Layout Standards

## **Priority: P0**

## Implementation Guidelines

### Auto Layout

- **Code-Based Layout**: Prefer programmatic layout using `NSLayoutAnchor` or SnapKit over Storyboards for better source control.
- **Safe Area**: Always respect `view.safeAreaLayoutGuide`.
- **UIStackView**: Use for linear layouts to reduce constraint complexity.

### UIKit Best Practices

- **View Lifecycle**: Perform layout adjustments in `viewWillLayoutSubviews` or `updateConstraints`.
- **Reusable Views**: Extract complex UI into custom `UIView` subclasses.
- **Image Optimization**: Use SF Symbols for icons. Preferred vector (PDF/SVG) for custom assets.
- **SwiftUI Bridge**: Use `UIViewRepresentable` or `UIViewControllerRepresentable` to host UIKit in SwiftUI.

### Human Interface Guidelines (HIG)

- **Accessibility**: Support Dynamic Type and provide meaningful `accessibilityLabel`.
- **Feedback**: Use `UINotificationFeedbackGenerator` for haptic feedback on actions.
- **Margins**: Follow standard system margins (typically 16-20pt).

## Anti-Patterns

- **Hardcoded Frames**: `**No CGRect(x:y:w:h)**: Use Auto Layout.`
- **Pyramid of Constraints**: `**No complex constraint logic in VC**: Use UIStackView or custom views.`
- **Missing Loading States**: `**No Blank Screens**: Use skeleton views or UIActivityIndicatorView.`

## References

- [Auto Layout & HIG Compliance](references/implementation.md)
