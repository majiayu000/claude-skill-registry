---
name: ios-a11y
description: Use when iOS accessibility issues arise — VoiceOver, UIKit/SwiftUI labels, traits, focus, Dynamic Type, contrast
user-invokable: false
metadata:
  keywords:
    - voiceover
    - ios-accessibility
    - accessibility-label
    - dynamic-type
  agent-affinity:
    - epost-a11y-specialist
    - epost-implementer
  platforms:
    - ios
  connections:
    extends: [a11y]
---

# iOS Accessibility Skill

## Purpose

Comprehensive WCAG 2.1 AA accessibility rules for iOS development. Covers VoiceOver support, UIKit/SwiftUI accessibility attributes, focus management, color contrast, and testing patterns.

## Aspect Files

| File | Coverage |
|------|----------|
| `references/a11y-core.md` | Core principles, UIKit enabling, properties, VoiceOver detection, **unreachable element detection**, **Dynamic Type (UIKit)**, SwiftUI modifiers |
| `references/a11y-buttons.md` | Button accessibility: labels, traits, states, icon buttons, toggle buttons, groups, **buttons-read-as-images**, **bottom-bar button groups**, **tab bar items** |
| `references/a11y-forms.md` | Form input accessibility: labels, validation, error states, input types, form structure |
| `references/a11y-headings.md` | Heading structure: `.header` trait, heading levels (H1-H6), navigation, dynamic content |
| `references/a11y-focus.md` | Focus management: notifications, indicators, focus order, groups, programmatic focus, screen changes |
| `references/a11y-colors-contrast.md` | Visual accessibility: WCAG contrast ratios (4.5:1 normal, 3:1 large/UI), color independence, testing |
| `references/a11y-testing.md` | Testing: Xcode Accessibility Inspector, VoiceOver testing, simulator, automated testing, checklists |

## Fix Templates (iOS)

| Template | Action |
|----------|--------|
| `add_button_label` | Add `accessibilityLabel`, `accessibilityTraits = .button` |
| `add_heading_trait` | Add `.header` trait and heading level |
| `add_form_label` | Add `accessibilityLabel` to form field |
| `make_image_decorative` | Set `isAccessibilityElement = false` |
| `add_modal_focus_trap` | Set `accessibilityViewIsModal`, manage focus |
| `add_status_announcement` | Add `UIAccessibility.post()` announcement |
| `other_manual` | Propose fix based on WCAG rules, mark NEEDS_REVIEW |

## Known Findings

See `a11y` skill for known-findings database documentation. Schema at `.github/assets/known-findings-schema.json`.

## Agents Using This Skill

- `epost-a11y-specialist` — Unified accessibility agent (guidance, audit, and fix modes)

## Related Documents

- `ios/development/references/tester.md` — iOS testing patterns (includes accessibilityIdentifier examples)
- `.epost-data/a11y/known-findings.json` — Project-specific known violations (if exists)
