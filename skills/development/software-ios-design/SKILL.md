---
name: software-ios-design
description: "Designs and audits native iOS interfaces. Use when reviewing or refining SwiftUI layout, typography, Liquid Glass, navigation, or dashboards on a freshly verified build."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Native iOS Design

Use this skill for visual design decisions and design-focused audits in any native iOS app. Prefer it when the user needs HIG-aligned screen structure, current Apple-native visual defaults, or a screenshot-to-fix loop after a fresh verified build/install/launch. If the request is really about greenfield scaffolding, CLI build loops, scheme selection, or broader iOS implementation workflow, route to `software-ios-native` and return here once the question becomes visual structure or design quality.

## Quick Reference

### Foundations
- Start from the current Apple design system; do not invent custom chrome when a standard control solves it.
- Use system typography, Dynamic Type text styles, semantic colors, SF Symbols, and standard containers first.
- Treat Liquid Glass as the navigation-layer material on iOS 26. Standard chrome (tab bars, toolbars, nav bars, sheets, sidebars) already adopts it. See [references/ios26-liquid-glass.md](references/ios26-liquid-glass.md).
- Tokenize every spacing, tracking, radius, and color in screen files. No magic numbers.
- Enforce a 44 × 44 pt minimum tap target; expand hit area via `.contentShape()` when the visible glyph is smaller.

### Layout & Content
- Contain data in visual boundaries (grid cells, action rows). Never let values float in card space.
- Anchor labels with small SF Symbol icons (10–12pt) and colored dot indicators for scannability.
- Prefer bottom sheets (`.sheet` + `.presentationDetents`) for detail over inline expansion.
- Prefer grids over horizontal carousels for any finite set of peer items — grids give spatial context.
- Use `ScrollView > LazyVStack` with `.scrollTransition` for narrative screens; reserve `List(.insetGrouped)` for settings-style hubs.
- Use expandable sections (spring animation) for data-dense reports instead of flat scroll dumps.
- For dense diagrams, charts, bodygraphs, maps, and canvases, the visualization is the primary surface. Do not cover it with popups, floating summary cards, or bottom overlays; put summary points below the diagram or in a sheet that leaves the diagram inspectable.
- Do not add a decorative container around a full-bleed or inspection-focused diagram unless the frame improves legibility. A visible card can make the chart feel smaller and harder to inspect.
- Detail/help sheets with peer containers must use full-width rows (`.frame(maxWidth: .infinity, alignment: .leading)`) so short rows do not shrink beside longer rows.

### Interaction & Feedback
- Propagate press feedback at the **shared-component** level, not just individual call sites. A `SharedListRow` using `.buttonStyle(.plain)` internally ships dead taps from every screen that uses it. Fix the shared component once; every caller benefits.
- Canonical tappable-container idiom: `@State private var tapCount: Int = 0`, `{ tapCount &+= 1; action() }` in the button action, `.sensoryFeedback(.selection, trigger: tapCount)` on the view. Use `&+=` for overflow-safe wrap-around.
- Build **one** global `motionSensitive()` view modifier for Reduce Motion (kills descendant transactions when `accessibilityReduceMotion` is true); attach at the app root. Per-screen checks are the anti-pattern.
- Add SwiftUI `iOS 17+` polish: `.scrollTransition`, `.sensoryFeedback`, `.symbolEffect`, `.contentTransition(.numericText)`. Standardize scroll reveals into a shared `ViewModifier` (e.g., `.appScrollReveal()`).
- Add press feedback to every tappable element via a custom `ButtonStyle` (`scaleEffect(0.94)` on `.isPressed` + 100 ms easeOut). `.buttonStyle(.plain)` alone fails the "toy quality" bar.
- For dense diagrams where labels or gates overlap, add native inspection controls before redesigning the geometry: zoom in/out/reset, pan/scroll when zoomed, and semantic filters for visible groups.
- Chart primitives should be tappable when they naturally carry meaning. Centers, gates, channels, nodes, and markers should open explanations; summary rows alone are not enough for an inspection surface.

### Navigation & Structure
- Merge related screens with segmented pickers to reduce navigation depth.
- Use `.presentationDetents([.medium, .large])` on sheets. Use `.presentationBackgroundInteraction(.enabled(upThrough:))` when the surface behind the sheet should stay interactive at peek height.
- For immersive visualization screens, use the full-bleed pattern: `ZStack { background; visualization; controls; .sheet(persistent) }` — no card wrappers, no scroll.
- For immersive controls, prefer native `Picker(.segmented)` + `Menu` overflow over custom material-backed button strips.
- **Tab bar vs sidebar-adaptive decision**: default to `TabView` for 3-5 peer top-level sections on iPhone. Reach for `NavigationSplitView` (sidebar-adaptive) when (a) the app is iPad/Mac-first and needs a persistent list-detail relationship, (b) there are 6+ top-level destinations that would force a tab-bar "More" overflow, or (c) the same information architecture must scale from iPhone compact width to iPad/Mac without a redesign. `NavigationSplitView` collapses to a stack on iPhone automatically — it is the correct default for adaptive multi-platform apps, not just a Mac/iPad nicety. Do not default to a custom hamburger-drawer sidebar on iPhone; it is not a system pattern and fails discoverability audits.

### Judgment: Following vs Diverging From Platform Convention
- Default posture is to follow the current Apple system pattern (tab bar behavior, sheet detents, glass materials) because it is free accessibility support, free Dynamic Type support, and matches user muscle memory.
- Diverge deliberately, and say so explicitly in the review, when: (a) the system default measurably regresses task completion for this app's core flow (e.g., a collapsing tab bar hides the primary action during the exact scroll state users are in most), (b) the app's category has an established, better-tested convention from a best-in-class competitor (e.g., camera apps keeping shutter controls fixed rather than following generic toolbar collapse), or (c) an accessibility setting is on and the system default itself is the accessibility bug (see Reduce Transparency contrast caveats in [references/ios26-liquid-glass.md](references/ios26-liquid-glass.md)).
- Never diverge silently. A divergence from HIG default must be called out as a deliberate, justified exception in the design review, not presented as if it were the platform default — this is what separates informed craft from "we didn't know the convention."

### Localization
- Every user-facing string runs through l10n — including short labels. German/Russian grow ~30–50%, Japanese breaks word-boundary assumptions, Arabic tests RTL.
- Verify every localized surface in one long-string locale (de, ru) and one non-Latin locale (ja, ar) before "complete."
- When a screen mixes static UI strings and backend-generated prose, confirm BOTH paths are localized — half-localized screens read as bugged.
- Localized does not mean "key exists." If non-English catalogs contain English fallback text for new keys, the design is not ready for localized review.

### Accessibility
- Every screen must survive Dynamic Type AX5, Reduce Motion, Reduce Transparency, and VoiceOver ON. See [references/ios-accessibility-patterns.md](references/ios-accessibility-patterns.md).
- Every interactive element needs a meaningful `.accessibilityLabel`. Combine multi-element rows with `.accessibilityElement(children: .combine)`.
- Declare support only for accessibility features you actually ship — Accessibility Nutrition Labels (iOS 26) are verified by App Store review.

### Performance & Proof
- Pipe CLI `xcodebuild` output through `xcbeautify` when XcodeBuildMCP is unavailable — raw output buries errors in thousands of lines.
- Use DocSetQuery for fast local Apple documentation lookups, or sosumi.ai for web-based Apple docs during freshness checks. Don't guess at current HIG behavior.
- Verify design fixes with screenshots from a freshly installed, freshly launched build. If the on-screen UI appears older than source, suspect stale install — route to [../software-ios-runtime-debugging/SKILL.md](../software-ios-runtime-debugging/SKILL.md).
- When screenshots alone can't diagnose, ask the agent to add verbose logs around the layout/appearance/accessibility surface and re-launch.

## Defaults

- Start from Apple's current design system, not custom chrome.
- Treat Liquid Glass as the navigation-layer baseline on iOS 26. Do **not** apply glass to content cards.
- Prefer system typography, Dynamic Type, semantic colors, SF Symbols, and standard containers before custom styling.
- Use materials and translucency to support hierarchy only where they improve legibility and context; do not add glass effects everywhere.
- Keep navigation familiar: tab views for peer sections, navigation stacks for drill-down, sheets for focused tasks.
- Use screenshot-driven verification for design changes only after a fresh simulator build/install/launch has been proven.

## Runtime Proof Gate

- Do not trust screenshots until a fresh uninstall → install → launch loop has completed for the current build.
- If the on-screen UI appears older than source, suspect stale install first. Route to [../software-ios-runtime-debugging/SKILL.md](../software-ios-runtime-debugging/SKILL.md).
- If install or launch is failing, stop design iteration and fix runtime truth before continuing.
- Use XcodeBuildMCP when it is actually callable. Otherwise use Apple CLI and route packaging or simulator-health issues to the runtime-debugging skill.
- When reviewing notification surfaces, verify banners, lock-screen cards, Notification Center, and the post-tap open experience on a physically proven build — simulator screenshots do not prove iPhone notification UX.

## Core Workflow

1. Define the screen's primary job and the one or two pieces of content that must win first attention.
2. Choose the native structure: tab view, navigation stack, list, sheet, inspector, or split view.
3. Apply typography, spacing, and semantic color using system defaults before inventing a custom scale.
4. Adopt Liquid Glass through standard controls and materials, then audit readability in both appearances.
5. Verify with XcodeBuildMCP or CLI fallback: fresh build, uninstall, install, launch, capture screenshot, inspect, fix, repeat.

## ASCII Flow

```text
iOS design task
  -> Prove current build, launch, and screenshot state
  -> Define screen job, hierarchy, and iOS platform fit
  -> Choose native navigation, sheets, lists, controls, and safe areas
  -> Check Dynamic Type, themes, permissions, and edge states
  -> Patch design details and recapture evidence
  -> Report before/after proof and residual interaction risk
```

## Feel Bar

Native iOS work is judged on feel as much as layout. Every substantive screen should be reviewed against these rows. If three or more fail, the screen is debt regardless of HIG conformance. See [references/ios-craft-and-feel.md](references/ios-craft-and-feel.md) for the full playbook.

| Dimension | Pass | Fail |
|-----------|------|------|
| Spring physics | curve token chosen per intent (snappy/smooth/bouncy) | default `.easeInOut` everywhere |
| Haptic vocabulary | `.success`/`.impact`/`.selection` mapped to commit weight | silent commits or one haptic for everything |
| SF Symbol craft | hierarchical/palette/variable + Symbol Effects on state changes | flat monochrome, no transitions |
| Press feedback | shared `ButtonStyle` with scale + haptic on every tappable | `.buttonStyle(.plain)` ships dead taps |
| Numbers | tabular figures + locale-aware formatter + `.contentTransition(.numericText)` | proportional digits jitter on update |
| Hero transitions | `matchedGeometryEffect` from list to detail | full sheet replace breaks spatial continuity |
| Pull-to-refresh | resistance + commit haptic + skeleton | spinner without tactile confirmation |
| Live Activities / widgets | designed for Lock Screen + Dynamic Island, not afterthought | desktop-style cards crammed into widget frame |
| Reduce Motion | one global `motionSensitive()` modifier, descendant transactions killed | per-screen ad-hoc checks, motion still leaks |
| First-run delight | one moment that earns a smile (symbol bounce, haptic chord) | none |
| Sound | rare, intentional, system sounds where possible | decorative tones on every action |
| Editorial polish | optical alignment, capital-letter kerning, glyph balance | pixel-equal but reads off |

## Design Craft Checklist

Before writing or reviewing screen code, check these patterns from [references/design-craft-patterns.md](references/design-craft-patterns.md):

1. **Token discipline**: Every spacing, tracking, radius, color, and repeated font value traces to a named token. No magic numbers in screen files.
2. **Data containment**: Values live in grid cells or action rows with visual boundaries, not floating in card space.
3. **Visual anchoring**: Data labels include SF Symbol icons. Categorized lists use colored dot indicators.
4. **Card hierarchy**: Hero card is visually distinct from secondary cards (larger radius, more padding). Mixed content within one card uses thin dividers.
5. **Data visualization**: Use Canvas for custom charts (radar, wheels, rings); use animated score rings with `.contentTransition(.numericText)`; use gradient score bars. See [references/ios-component-patterns.md](references/ios-component-patterns.md#canvas-based-data-visualizations).
6. **Interactive polish**: Press feedback (shared `ButtonStyle`), haptics (`.sensoryFeedback`), SF Symbol animation (`.symbolEffect(.bounce)`), expandable sections, entrance animations on sheets.
7. **Localization readiness**: All user-facing strings through l10n. Verify keys exist in every locale JSON — silent fallback is the bug that hides until someone switches locale.
8. **Competitor awareness**: Borrow containment and anchoring patterns, not brand identities.
9. **Control density**: When labels wrap on iPhone, switch segmented controls to a horizontally scrollable pill rail; move reset/status actions out of the primary rail.
10. **Readable depth**: For radial or information-dense charts, use subtle parallax, layered depth, and focus states before attempting literal 3D.
11. **Disclosure control**: If repeated polish still feels noisy, lower simultaneous disclosure and introduce mode filters.
12. **Accessibility on interactive elements**: Sheet-triggering buttons need `.accessibilityHint`. Multi-element rows use `.accessibilityElement(children: .combine)`. Navigation chevrons need explicit labels. See [references/ios-accessibility-patterns.md](references/ios-accessibility-patterns.md).
13. **Design verification tests**: Fast unit-level snapshot tests for token/layout regression. UI tests only at handoff — they take over the simulator and slow iteration. Automated accessibility audits (`accessibilityLabel` presence) belong in the fast test target.

## Design Review Loop

- Prefer the XcodeBuildMCP loop when an iOS project is runnable and the tool is callable: build and run, navigate to the target screen, capture a screenshot, inspect hierarchy and logs, apply SwiftUI fixes, re-run.
- If XcodeBuildMCP is unavailable, pipe `xcodebuild` through `xcbeautify` (`xcodebuild ... 2>&1 | xcbeautify`) and use `simctl` — don't feed raw `xcodebuild` output to agents.
- Prefer side-by-side before/after screenshots over verbal "looks better" claims.
- Ask for evidence of Dynamic Type, light/dark appearance, and device-size behavior when a change touches layout or hierarchy.
- When screenshots alone cannot diagnose, ask the agent to add runtime logging around the design property (layout constraints, trait changes, appearance updates) and read logs after a fresh launch.

See:

- [references/ai-design-review.md](references/ai-design-review.md)
- [references/xcodebuildmcp-design-loop.md](references/xcodebuildmcp-design-loop.md)
- [scripts/bootstrap-xcodebuildmcp.sh](scripts/bootstrap-xcodebuildmcp.sh)

## Route Elsewhere

- Use [../software-ios-native/SKILL.md](../software-ios-native/SKILL.md) for SwiftUI architecture, Observation, concurrency, release gates, or general iOS implementation strategy.
- Use [../software-ios-runtime-debugging/SKILL.md](../software-ios-runtime-debugging/SKILL.md) for stale builds, simulator drift, install failures, or any case where the screenshot may not reflect the current build.
- Use [../software-mobile/SKILL.md](../software-mobile/SKILL.md) for platform-selection or cross-platform decisions.
- Use [../software-ui-ux-design/SKILL.md](../software-ui-ux-design/SKILL.md) for generic product UX patterns that are not iOS-specific.
- Use [../software-accessibility/SKILL.md](../software-accessibility/SKILL.md) for broader accessibility remediation beyond iOS-native visual design defaults.

Widgets, Live Activities, Control Center custom controls, and Lock-screen surfaces are first-class iOS design surfaces. This skill's patterns apply (typography, Dynamic Type, materials, touch targets, accessibility) but the platform constraints differ — widget timelines, size families, interactive affordance rules. When designing these surfaces specifically, also consult Apple HIG → Widgets and HIG → Live Activities; the core rules in this skill still apply to their content surfaces.

## Navigation

### Foundations

- [references/hig-typography-color.md](references/hig-typography-color.md) — San Francisco, Dynamic Type scale, semantic color, contrast targets, materials, Dark Mode pitfalls
- [references/hig-layout-spacing.md](references/hig-layout-spacing.md) — touch targets, safe areas, spacing scale, thumb zones, keyboard avoidance, layout adaptivity
- [references/ios26-liquid-glass.md](references/ios26-liquid-glass.md) — `glassEffect`, `GlassEffectContainer`, morphing, fallback for pre-iOS 26, accessibility interactions
- [references/ios-accessibility-patterns.md](references/ios-accessibility-patterns.md) — VoiceOver, Dynamic Type, Reduce Motion, Reduce Transparency, Nutrition Labels, haptics

### Patterns

- [references/ios-component-patterns.md](references/ios-component-patterns.md) — tab views, navigation stacks, sheets, cards, lists, toolbars, FlowLayout, immersive visualization
- [references/ios-dashboard-design.md](references/ios-dashboard-design.md) — overview-screen hierarchy, data display patterns, card hierarchy, dual-view dashboards
- [references/visual-guidance-patterns.md](references/visual-guidance-patterns.md) — narrative/guidance screen archetype, Canvas terrains, opportunity framing, energy rings
- [references/design-craft-patterns.md](references/design-craft-patterns.md) — token discipline, data containment, visual anchoring, dark theme, competitor analysis
- [references/motion-tokens.md](references/motion-tokens.md) — motion intents, curves, durations, Reduce Motion handling
- [references/swiftui-design-antipatterns.md](references/swiftui-design-antipatterns.md) — state/identity, navigation, layout, color/Dark Mode, animations, controls, sheets, data display anti-patterns
- [references/ios-craft-and-feel.md](references/ios-craft-and-feel.md) — spring physics, haptic choreography, SF Symbol craft, transition continuity, editorial number polish, Live Activities
- [references/ios-pro-craft-scenarios.md](references/ios-pro-craft-scenarios.md) — onboarding, IAP/paywall, settings, search, photo viewer, media player, focused-input, daily-habit, camera, charts, inbox, App Intents
- [references/ios-surfaces-reference.md](references/ios-surfaces-reference.md) — Swift Charts vs Canvas, Dynamic Island stages, widgets, App Clips, App Intents, Transferable, ShareLink, NavigationSplitView, swipe actions, Live Activities, multitasking
- [references/ios-shipping-antipatterns.md](references/ios-shipping-antipatterns.md) — ATT/push/IAP timing, toolbar overcrowding, alert vs confirmationDialog, App Store screenshot/preview/metadata, Sign in with Apple, App Review traps

### Review & Tooling

- [references/app-review-guidelines-map.md](references/app-review-guidelines-map.md) — App Store Review Guidelines mapped to pass/fail checks across all five sections (Safety, Performance, Business, Design, Legal), incl. the 4.3(b) saturated-category gate (astrology/fortune-telling) and AI-generated-content rules
- [references/ai-design-review.md](references/ai-design-review.md) — screenshot prompts, review checklists, proof expectations
- [references/xcodebuildmcp-design-loop.md](references/xcodebuildmcp-design-loop.md) — current XcodeBuildMCP setup and simulator verification flow
- [data/sources.json](data/sources.json) — primary Apple sources and freshness-check targets

### Scripts

Optional helpers for a proven-build design loop. If the project uses a `Makefile`, `make` can replace the individual scripts. If the app cannot build/install/launch cleanly, route to [../software-ios-runtime-debugging/SKILL.md](../software-ios-runtime-debugging/SKILL.md).

- [scripts/bootstrap-xcodebuildmcp.sh](scripts/bootstrap-xcodebuildmcp.sh) — verify CLI availability and scaffold a repo-local `.xcodebuildmcp/config.yaml`
- [scripts/build-ios.sh](scripts/build-ios.sh) — compile-only simulator build wrapper
- [scripts/run-ios.sh](scripts/run-ios.sh) — build-and-run wrapper for iterative design work
- [scripts/test-ios.sh](scripts/test-ios.sh) — simulator test wrapper with optional extra args
- [scripts/capture-screenshot.sh](scripts/capture-screenshot.sh) — save a simulator screenshot for review loops

## Anti-Patterns

For the full anti-pattern catalog — SwiftUI state/identity, navigation, layout, color/Dark Mode, animations, controls, sheets, data display, Canvas, and runtime footguns — see [references/swiftui-design-antipatterns.md](references/swiftui-design-antipatterns.md).

## Verification Gate

| Check | Pass condition | Fail condition |
|---|---|---|
| Standard structure | Recommendation maps to a standard iOS pattern | Custom pattern used without justification |
| Screenshot origin | Freshly installed and launched build | Screenshot from a prior install or simulator session not tied to current build |
| Typography | Dynamic Type text styles throughout | Fixed-size design tokens |
| Color and materials | Contrast and hierarchy preserved in light and dark mode | Material or color breaks in one appearance |
| Touch targets | ≥ 44 × 44 pt; `.contentShape()` used where glyph is smaller | Target below minimum; dead taps on tappable rows |
| Notification surface | Verified on real iPhone in correct APNs environment | Simulator-only screenshots for notification UX |
| Dashboard heuristics | Labeled as team default, not platform rule | Presented as HIG requirement without citation |
| XcodeBuildMCP guidance | Verified against upstream docs | Repeated from memory or prior session |
| Release metadata | `Info.plist` iPad orientation keys present on device-universal apps | Simulator UI passes but `Info.plist` missing keys for App Store validation |

## Freshness Protocol

Freshness-check before final answers whenever the request depends on:

- current Apple design language or Liquid Glass behavior
- current HIG navigation or control guidance
- current SF Symbols or San Francisco guidance
- current XcodeBuildMCP config keys, CLI commands, or workflows

Start from [data/sources.json](data/sources.json), then prefer Apple Developer documentation, WWDC sessions, and upstream XcodeBuildMCP docs. For fast local lookups, use DocSetQuery against Apple DocSet bundles. For web-based lookups, use sosumi.ai.

**Current stable baseline (verify at each session):** iOS/iPadOS 26.x is shipping; Liquid Glass, SF Symbols 7, and the Accessibility Nutrition Labels described in this skill are current, shipped behavior. **Announced, not shipped:** WWDC26 (June 2026) previewed iOS/iPadOS/macOS 27, SF Symbols 8, and Icon Composer 2 — including reduced default Liquid Glass transparency, a system-level Clear/Tinted appearance control, darkened glass edges, and reversed tab-bar search placement. As of this validation pass, iOS 27 and SF Symbols 8 are beta-only. Do not present iOS 27 design changes as the current default; label them explicitly as "iOS 27, announced at WWDC26, not yet GA" and re-verify the current beta/GA split before quoting a specific point release.

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Verify current Apple design guidance against Apple Developer documentation and WWDC sessions.
- Verify XcodeBuildMCP commands and config keys against upstream docs listed in [data/sources.json](data/sources.json).
- Label team heuristics (e.g., dashboard density) as defaults rather than Apple rules.
- Treat every "iOS 27" / SF Symbols 8 / Icon Composer 2 claim as provisional until Apple's GA release notes confirm it — WWDC-announced design changes routinely shift between beta seeds.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

