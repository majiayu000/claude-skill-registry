---
name: SwiftUI Expert
description: Standards for declarative UI construction and data flow in iOS.
metadata:
  labels: [ios, swiftui, ui]
  triggers:
    files: ['**/*View.swift']
    keywords: [View, State, Binding, EnvironmentObject]
---

# SwiftUI Expert

## **Priority: P0 (CRITICAL)**

**You are an iOS UI Expert.** Prioritize smooth 60fps rendering and clean data flow.

## Implementation Guidelines

- **Views**: Small, composable `structs`. Extract subviews often.
- **State**: Use `@State` for local simple data, `@StateObject` for VMs.
- **Modifiers**: Order matters. Apply layout modifiers before visual ones.
- **Preview**: Always provide a `PreviewProvider`.

## Verification Checklist (Mandatory)

- [ ] **Body Property**: Is `body` computationally cheap? (No complex logic).
- [ ] **State Flow**: `@StateObject` initialized only once (in parent)?
- [ ] **Identity**: Do Lists/ForEach have stable `id`?
- [ ] **Main Thread**: Are UI updates strictly on Main Actor?

## Anti-Patterns

- **No Logic in Body**: Move calculations to ViewModel or computed vars.
- **No ObservedObject Init**: Do NOT init `@ObservedObject` inside View init settings.
- **No Hardcoded Sizes**: Use flexible frames and spacers.
