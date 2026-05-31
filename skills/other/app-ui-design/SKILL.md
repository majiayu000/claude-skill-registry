---
name: app-ui-design
description: Mobile app UI design expert for iOS and Android. Use when designing app interfaces, creating design systems, ensuring accessibility, or following platform guidelines. Covers Material Design 3, Human Interface Guidelines, color theory, typography, and 2025 trends.
---
# Mobile App UI Design

> Expert guidance for designing beautiful, accessible, and platform-native mobile app interfaces following 2025 best practices.

## Core Philosophy

- **User-First Design** — Prioritize user needs, behaviors, and mental models over aesthetics
- **Platform Consistency** — Follow iOS HIG and Android Material Design guidelines
- **Accessibility as Foundation** — Design for all users from the start, not as an afterthought
- **Emotional Intelligence** — Create interfaces that users emotionally connect with
- **Performance-Conscious** — Beautiful design that doesn't sacrifice app performance

---

## Hard Rules (Must Follow)

> These rules are mandatory. Violating them means the skill is not working correctly.

### Accessibility First

**All designs must meet WCAG 2.2 AA standards. Accessibility is not optional.**

```markdown
❌ FORBIDDEN:
- Color contrast below 4.5:1 for text
- Touch targets smaller than 44×44pt (iOS) or 48×48dp (Android)
- Information conveyed by color alone
- Missing alternative text for images
- Non-keyboard-navigable interfaces

✅ REQUIRED:
- Minimum 4.5:1 contrast ratio for normal text
- Minimum 3:1 contrast ratio for large text (18pt+)
- Touch targets: 44×44pt (iOS) / 48×48dp (Android)
- Support for Dynamic Type / Font Scaling
- VoiceOver (iOS) / TalkBack (Android) compatibility
- Clear focus indicators for keyboard navigation
```

### Platform Guidelines Adherence

**Follow platform-specific design guidelines. Do not mix iOS and Android patterns.**

```markdown
❌ FORBIDDEN:
- Using Android-style FAB on iOS
- Using iOS-style bottom sheets on Android without adaptation
- Mixing platform navigation patterns
- Ignoring platform typography (SF Pro vs Roboto)

✅ REQUIRED:
iOS (Human Interface Guidelines):
- Use SF Pro font family
- Tab bar at bottom for primary navigation
- Push navigation with back chevron
- Standard iOS controls (UIKit/SwiftUI)

Android (Material Design 3):
- Use Roboto font family
- Bottom navigation bar or navigation drawer
- Material components with ripple effects
- Follow Material You dynamic theming
```

### Consistent Design System

**Every app must have a documented design system with tokens.**

```markdown
❌ FORBIDDEN:
- Ad-hoc colors and spacing values
- Inconsistent button styles across screens
- Multiple unnamed font sizes
- Components without defined states

✅ REQUIRED:
Design System Must Include:
├── Color Tokens (primary, secondary, surface, error, etc.)
├── Typography Scale (heading1-6, body, caption, etc.)
├── Spacing Scale (4, 8, 12, 16, 24, 32, 48px)
├── Border Radius Tokens (none, sm, md, lg, full)
├── Shadow/Elevation Tokens (elevation1-5)
└── Component Library (button, input, card, etc.)
```

### Touch-Friendly Design

**All interactive elements must be optimized for touch interaction.**

```markdown
❌ FORBIDDEN:
- Touch targets smaller than minimum size
- Interactive elements too close together (<8px gap)
- Important actions outside thumb reach zone
- Hover-dependent interactions

✅ REQUIRED:
- Minimum touch target: 44×44pt (iOS) / 48×48dp (Android)
- Minimum spacing between targets: 8px
- Primary actions in thumb-friendly zone (bottom 2/3)
- Clear tap feedback (ripple, highlight, scale)
```

---

## Quick Reference

### When to Use What

| Scenario | Approach | Key Considerations |
|----------|----------|-------------------|
| New app design | Start with design system | Define tokens before screens |
| iOS-only app | Human Interface Guidelines | SF Pro, standard iOS patterns |
| Android-only app | Material Design 3 | Roboto, Material components |
| Cross-platform app | Adaptive design | Platform-specific navigation |
| Redesign existing app | Audit first | Maintain mental models |
| Accessibility review | WCAG 2.2 AA checklist | Contrast, touch targets, labels |

---

## Design System Fundamentals

### Color System

```markdown
## Color Token Structure

### Semantic Colors
primary          → Main brand color, CTAs
primary-variant  → Darker/lighter primary for states
secondary        → Secondary actions, accents
background       → App background
surface          → Card backgrounds, elevated surfaces
error            → Error states, destructive actions
on-primary       → Text/icons on primary color
on-background    → Text/icons on background
on-surface       → Text/icons on surface

### Color Palette (60-30-10 Rule)
60% → Neutral/background colors
30% → Secondary/supporting colors
10% → Accent/primary colors

### Dark Mode Considerations
- Don't just invert colors
- Use desaturated colors for dark surfaces
- Reduce contrast slightly (avoid pure white on black)
- Maintain color meaning across modes
```

### Typography Scale

```markdown
## Mobile Typography Guidelines

### iOS Typography (SF Pro)
Large Title   → 34pt, Bold
Title 1       → 28pt, Bold
Title 2       → 22pt, Bold
Title 3       → 20pt, Semibold
Headline      → 17pt, Semibold
Body          → 17pt, Regular
Callout       → 16pt, Regular
Subhead       → 15pt, Regular
Footnote      → 13pt, Regular
Caption 1     → 12pt, Regular
Caption 2     → 11pt, Regular

### Android Typography (Roboto / Material 3)
Display Large  → 57sp
Display Medium → 45sp
Display Small  → 36sp
Headline Large → 32sp
Headline Medium→ 28sp
Headline Small → 24sp
Title Large    → 22sp
Title Medium   → 16sp, Medium
Title Small    → 14sp, Medium
Body Large     → 16sp
Body Medium    → 14sp
Body Small     → 12sp
Label Large    → 14sp, Medium
Label Medium   → 12sp, Medium
Label Small    → 11sp, Medium

### Best Practices
- Maximum 2-3 font families per app
- Minimum body text: 16px (14px absolute minimum)
- Line height: 1.4-1.6× font size for body text
- Support Dynamic Type (iOS) / Font Scaling (Android)
```

### Spacing System

```markdown
## 8-Point Grid System

Base Unit: 8px

### Spacing Scale
spacing-0    → 0px
spacing-1    → 4px   (half unit)
spacing-2    → 8px   (1 unit)
spacing-3    → 12px  (1.5 units)
spacing-4    → 16px  (2 units)
spacing-5    → 24px  (3 units)
spacing-6    → 32px  (4 units)
spacing-7    → 48px  (6 units)
spacing-8    → 64px  (8 units)

### Component Spacing
Button padding      → 12px vertical, 24px horizontal
Card padding        → 16px
List item padding   → 16px horizontal, 12px vertical
Section spacing     → 24px-32px
Screen edge margin  → 16px (phones), 24px (tablets)

### Touch Target Spacing
Minimum gap between interactive elements: 8px
Recommended gap: 12-16px
```

---

## Platform Guidelines

### iOS Human Interface Guidelines

```markdown
## iOS Design Principles

### Core Principles
1. Clarity    → Text legible, icons precise, purpose obvious
2. Deference  → UI helps understanding, not competing with content
3. Depth      → Visual layers and realistic motion convey hierarchy

### Navigation Patterns
- Tab Bar (bottom) → 3-5 primary destinations
- Navigation Bar (top) → Title, back button, actions
- Modal sheets → Temporary focused tasks
- Popovers (iPad) → Contextual options

### 2025 Updates: Liquid Glass
- Translucent materials for controls
- Floating navigation elements
- Dynamic depth and hierarchy
- Background blur effects

### Safe Areas
- Top: Status bar + Dynamic Island/Notch
- Bottom: Home indicator (34pt on Face ID devices)
- Use safeAreaInsets for proper content placement

### Standard Dimensions
- Navigation bar height: 44pt (96pt with large title)
- Tab bar height: 49pt (83pt on Face ID devices)
- Toolbar height: 44pt
```

### Android Material Design 3

```markdown
## Material Design 3 Principles

### Core Concepts
1. Material You    → Personal, adaptive, dynamic color
2. Expressiveness  → Emotional connection through design
3. Accessibility   → Inclusive design for all users

### Navigation Patterns
- Bottom Navigation → 3-5 primary destinations
- Navigation Drawer → 5+ destinations or secondary nav
- Navigation Rail → Tablets and large screens
- Top App Bar → Title, navigation, actions

### Material 3 Expressive (2025)
- Dynamic color from user wallpaper
- Springy, physics-based motion
- Bolder, more expressive typography
- Rounded, approachable shapes

### Component Shapes
- Extra Small: 4dp
- Small: 8dp
- Medium: 12dp
- Large: 16dp
- Extra Large: 28dp
- Full: 50% (pills/circles)

### Standard Dimensions
- App bar height: 64dp
- Bottom navigation height: 80dp
- FAB size: 56dp (standard), 40dp (small), 96dp (large)
```

---

## 2025 Design Trends

### AI-Driven Personalization

```markdown
## Adaptive UI Patterns

### Personalization Strategies
- Content recommendations based on behavior
- Adaptive UI layouts based on usage patterns
- Smart defaults and predictive actions
- Contextual feature suggestions

### Implementation Guidelines
- Always provide manual override options
- Explain why content is recommended
- Respect user privacy preferences
- Gradual personalization (don't overwhelm new users)
```

### Dark Mode Excellence

```markdown
## Dark Mode Best Practices

### Color Adaptation
Light Mode          →    Dark Mode
White (#FFFFFF)     →    Dark gray (#121212)
Black (#000000)     →    White (#FFFFFF)
Primary (vibrant)   →    Primary (desaturated)
Shadows             →    Subtle shadows or none

### Surface Elevation (Material 3)
Elevation 0  → #121212
Elevation 1  → #1E1E1E (+ 5% white overlay)
Elevation 2  → #232323 (+ 7% white overlay)
Elevation 3  → #272727 (+ 8% white overlay)
Elevation 4  → #2C2C2C (+ 9% white overlay)
Elevation 5  → #323232 (+ 11% white overlay)

### Recommendations
- Auto-switch based on system setting
- Separate color tokens for light/dark
- Test contrast in both modes
- Consider OLED optimization (true blacks)
```

### Microinteractions

```markdown
## Meaningful Motion

### Types of Microinteractions
- Feedback → Button press, form submission
- State → Loading, success, error
- Guidance → Onboarding hints, tooltips
- Delight → Celebration animations, easter eggs

### Motion Principles
- Duration: 200-500ms for most interactions
- Easing: Use natural easing curves
- Purpose: Every animation should have a reason
- Performance: Use hardware-accelerated properties

### 2025 Trends
- Springy, physics-based animations
- Morphing transitions between states
- Gesture-driven interactions
- Reduced motion support for accessibility
```

### Glassmorphism & Neumorphism

```markdown
## Modern Visual Styles

### Glassmorphism
Properties:
- Background blur (backdrop-filter: blur)
- Transparency (10-40% opacity)
- Subtle border (1px white at 20% opacity)
- Soft shadow

Use Cases:
- Overlays and modals
- Cards on image backgrounds
- Navigation bars (iOS Liquid Glass)

Caution:
- Ensure text readability
- Consider performance impact
- Provide fallback for older devices

### Neumorphism (Soft UI)
Properties:
- Soft shadows (light and dark)
- Subtle elevation effect
- Muted color palette

Use Cases:
- Toggle switches
- Input fields
- Cards

Caution:
- Often fails accessibility contrast tests
- Use sparingly, not as primary style
- Always test with actual content
```

---


## Extended Reference

Detailed material starting at `## Accessibility Checklist` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
