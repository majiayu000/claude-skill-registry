---
name: widgetkit-code-review
description: Reviews WidgetKit code for timeline management, view composition, configurable intents, and performance. Use when reviewing code with import WidgetKit, TimelineProvider, Widget protocol, or @main struct Widget.
---

# WidgetKit Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| TimelineProvider, entries, reload policies | [references/timeline.md](references/timeline.md) |
| Widget families, containerBackground, deep linking | [references/views.md](references/views.md) |
| AppIntentConfiguration, EntityQuery, @Parameter | [references/intents.md](references/intents.md) |
| Refresh budget, memory limits, caching | [references/performance.md](references/performance.md) |

## Review Checklist

- [ ] `placeholder(in:)` returns immediately without async work
- [ ] Timeline entries spaced at least 5 minutes apart
- [ ] `getSnapshot` checks `context.isPreview` for gallery previews
- [ ] `containerBackground(for:)` used for iOS 17+ compatibility
- [ ] `widgetURL` used for systemSmall (not Link)
- [ ] No Button views (use Link or widgetURL)
- [ ] No AsyncImage or UIViewRepresentable in widget views
- [ ] Images downsampled to widget display size (~30MB limit)
- [ ] App Groups configured for data sharing between app and widget
- [ ] EntityQuery implements `defaultResult()` for non-optional parameters
- [ ] New intent parameters handle nil for existing widgets after updates
- [ ] `reloadTimelines` called strategically (not on every data change)

## When to Load References

- TimelineProvider implementation or refresh issues -> timeline.md
- Widget sizes, Lock Screen, containerBackground -> views.md
- Configurable widgets, AppIntent migration -> intents.md
- Memory issues, caching, budget management -> performance.md

## Review Questions

1. Does the widget provide fallback entries for when system delays refresh?
2. Are Lock Screen families (accessoryCircular/Rectangular/Inline) handled appropriately?
3. Would migrating from IntentConfiguration break existing user widgets?
4. Is timeline populated with future entries or does it rely on frequent refreshes?
5. Is data cached via App Groups for widget access?
