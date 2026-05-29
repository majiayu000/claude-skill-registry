---
name: swiftui-code-review
description: Reviews SwiftUI code for view composition, state management, performance, and accessibility. Use when reviewing .swift files containing SwiftUI views, property wrappers (@State, @Binding, @Observable), or UI code.
---

# SwiftUI Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| View extraction, modifiers, body complexity | [references/view-composition.md](references/view-composition.md) |
| @State, @Binding, @Observable, @Bindable | [references/state-management.md](references/state-management.md) |
| LazyStacks, AnyView, ForEach, identity | [references/performance.md](references/performance.md) |
| VoiceOver, Dynamic Type, labels, traits | [references/accessibility.md](references/accessibility.md) |

## Gates (review workflow)

Complete in order; do not skip ahead.

1. **Anchor scope** — Pass when: every reviewed file is listed as a repo-relative `.swift` path (or the review explicitly states “none opened / N/A” with reason).
2. **Reference before critique** — Pass when: for any non-trivial body, modifier chain, or wrapper-ownership question, you have opened the matching `references/*.md` row from the table above *or* you state “not needed” with one line why.
3. **Evidence-bound findings** — Pass when: each substantive issue includes **`[FILE:LINE]`** (or a bounded line range) before recommendations; symbols/snippets may supplement but not replace the location anchor; no finding that rests only on “typical SwiftUI” without pointing at this code.

## Review Checklist

- [ ] View body under 10 composed elements (extract subviews)
- [ ] Modifiers in correct order (padding before background)
- [ ] @StateObject for view-owned objects, @ObservedObject for passed objects
- [ ] @Bindable used for two-way bindings to @Observable (iOS 17+)
- [ ] LazyVStack/LazyHStack for scrolling lists with 50+ items
- [ ] No AnyView (use @ViewBuilder or generics instead)
- [ ] ForEach uses stable Identifiable IDs (not array indices)
- [ ] All images/icons have accessibilityLabel
- [ ] Custom controls have accessibilityAddTraits(.isButton)
- [ ] Dynamic Type supported (no fixed font sizes)
- [ ] .task modifier for async work (not onAppear + Task)

## When to Load References

- Complex view bodies or modifier chains -> view-composition.md
- Property wrapper usage (@State, @Observable) -> state-management.md
- List performance or view identity issues -> performance.md
- VoiceOver or accessibility implementation -> accessibility.md

## Review Questions

1. Could this large view body be split into smaller, reusable Views?
2. Is modifier order intentional? (padding -> background -> frame)
3. Is @StateObject/@ObservedObject usage correct for ownership?
4. Could LazyVStack improve this ScrollView's performance?
5. Would VoiceOver users understand this interface?
