---
name: android-a11y
description: (ePost) Use when Android accessibility issues arise — TalkBack, contentDescription, touch targets, focus order, contrast in Compose or Views/XML
user-invocable: false
metadata:
  keywords:
    - talkback
    - android-accessibility
    - content-description
    - touch-target
  agent-affinity:
    - epost-a11y-specialist
    - epost-fullstack-developer
  platforms:
    - android
  connections:
    extends: [a11y]
---

# Android Accessibility Skill

## Purpose

WCAG 2.1 AA accessibility rules for Android development. Covers both **Jetpack Compose** (rustX/communities modules) and **traditional Views/XML** (epostSdk/app modules). Includes TalkBack support, content descriptions, touch targets, focus semantics, heading structure, color contrast, custom Views, RecyclerView, and AccessibilityDelegate patterns.

## Aspect Files

| File | Coverage |
|------|----------|
| `references/android-content-descriptions.md` | **Compose**: contentDescription for images, icons, composables — meaningful vs decorative, live regions, custom actions |
| `references/android-touch-targets.md` | 48×48dp minimum, MinimumTouchTargetSize, Box padding patterns |
| `references/android-focus-semantics.md` | **Compose**: mergeDescendants, stateDescription, traversalIndex, clearAndSetSemantics, toggleableState |
| `references/android-headings.md` | heading() semantic, hierarchy, TalkBack heading navigation |
| `references/android-contrast.md` | WCAG contrast ratios, MaterialTheme, dark mode, dynamic color, testing tools |
| `references/android-views-xml-a11y.md` | **Views/XML**: contentDescription, importantForAccessibility, labelFor, liveRegion, custom View onInitializeAccessibilityNodeInfo, RecyclerView/ViewHolder, AccessibilityDelegate |

## Fix Templates

| Template ID | Violation | Fix |
|-------------|-----------|-----|
| `add_content_description` | Image/Icon missing contentDescription (Compose) | Add `contentDescription = "..."` to Image or Icon |
| `make_decorative` | Decorative image incorrectly announced (Compose) | Set `contentDescription = null` on Image or Icon |
| `add_content_description_xml` | Image/Icon missing contentDescription (XML) | Add `android:contentDescription="..."` to ImageView/ImageButton |
| `make_decorative_xml` | Decorative image announced (XML) | Set `android:importantForAccessibility="no"` |
| `add_viewholder_description` | RecyclerView item missing accessible description | Set `holder.itemView.contentDescription` in `onBindViewHolder` |
| `add_touch_target` | Tap target smaller than 48×48dp | Wrap in Box with `Modifier.sizeIn(minWidth = 48.dp, minHeight = 48.dp)` |
| `add_heading_semantic` | Section title not marked as heading | Add `Modifier.semantics { heading() }` |
| `add_state_description` | Custom toggle/state without state announcement | Add `Modifier.semantics { stateDescription = "..." }` |
| `other_manual` | Complex semantic issue requiring human judgment | Flag for manual review — no automated fix |

## Key Compose Accessibility APIs

| API | Purpose | Example |
|-----|---------|---------|
| `contentDescription` | Announce element to TalkBack | `Image(contentDescription = "Profile photo")` |
| `Modifier.semantics { }` | Override or extend semantic properties | `Modifier.semantics { stateDescription = "Selected" }` |
| `mergeDescendants = true` | Group child semantics into single node | Groups icon + label into one TalkBack announcement |
| `stateDescription` | Describe current toggle/checkbox state | `"Checked"` / `"Unchecked"` for custom controls |
| `heading()` | Mark text as section heading | Enables TalkBack heading navigation |
| `clearAndSetSemantics { }` | Replace all child semantics | Full control over composite composable announcements |
| `traversalIndex` | Custom TalkBack focus order | `semantics { traversalIndex = 0f }` — lower = earlier |

## Touch Target Minimum

All interactive composables (buttons, checkboxes, icon buttons, clickable rows) must meet the **48×48dp minimum** touch target. Material3 enforces this by default for standard components. Custom composables require explicit sizing.

## Related Documents

- `a11y` — POUR framework, severity scoring, operating modes
- `ios-a11y` — iOS equivalent (VoiceOver, UIKit, SwiftUI)
