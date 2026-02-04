---
name: liquid-glass-ios
description: "Apple's Liquid Glass design system for iOS 26+ and iPadOS 26+. Use when: (1) building iOS 26+ UI with glassEffect, (2) implementing GlassEffectContainer for multiple elements, (3) working with glass morphing transitions, (4) integrating glass effects in navigation layers, (5) ensuring glass effect accessibility, (6) migrating from UIKit to SwiftUI glass APIs."
---

# Liquid Glass Design for iOS

Implementation patterns for Apple's Liquid Glass design system in iOS 26+ and iPadOS 26+, covering SwiftUI glassEffect APIs and UIKit NSGlassEffectView integration.

## References

See [references/liquid-glass.md](references/liquid-glass.md) for comprehensive guidance organized by:

- **Platform & Availability** - iOS 26+ version checking and fallbacks
- **Navigation & UI Layer** - Proper layer placement for glass effects
- **Variants & Styling** - Glass variants (regular, thin, clear) and color usage
- **Container & Multi-Element Management** - GlassEffectContainer patterns and spacing
- **Morphing & Animations** - Transition effects and identity management
- **Performance & Limits** - Element constraints and optimization
- **Accessibility** - VoiceOver and reduced transparency support
- **UIKit Integration** - NSGlassEffectView patterns
- **Framework Interoperability** - SwiftUI and UIKit mixing constraints
