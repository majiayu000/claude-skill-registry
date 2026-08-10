---
name: software-android-design
description: "Designs and audits native Android interfaces. Use when reviewing Compose layout, typography, color, motion, or adaptive patterns on a verified emulator build."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Native Android Design

Use this skill for visual design decisions and design-focused audits in native Android apps. Prefer it when the user needs Material 3 aligned screen structure, current Android-native visual defaults, or a screenshot-to-fix loop after a fresh verified build/install/launch. If the request is really about greenfield scaffolding, Gradle build loops, module selection, or broader Android implementation workflow, route to `software-mobile` and return here once the question becomes visual structure or design quality.

## Quick Reference

| Design concern | Default | Notes |
|---------------|---------|-------|
| Type | `MaterialTheme.typography` | Display → Headline → Title → Body → Label scale |
| Color | `MaterialTheme.colorScheme` | primary, secondary, tertiary, surface, error, and `on*` variants |
| Shape | `MaterialTheme.shapes` | ExtraSmall→ExtraLarge; `RoundedCornerShape` |
| Dynamic color | `dynamicDarkColorScheme` / `dynamicLightColorScheme` | Android 12+; static seed palette on older APIs |
| Bottom nav | `NavigationBar` 3–5 destinations | `NavigationRail` on medium, `NavigationDrawer` on expanded, or `NavigationSuiteScaffold` for auto |
| Top bar | `TopAppBar` / `MediumTopAppBar` / `LargeTopAppBar` / `CenterAlignedTopAppBar` | Choose by headline presence; collapsing variants for rich headers |
| Cards | `ElevatedCard` hero, `Card` primary, `OutlinedCard` secondary | tonalElevation 3 + shadow for hero |
| Custom data viz | `Canvas` | Radar charts, score rings, gradient bars, gauges — standard components insufficient |
| Adaptive layouts | `ListDetailPaneScaffold`, `SupportingPaneScaffold`, `NavigationSuiteScaffold` | Feed grids for homogeneous content |
| Detail views | `ModalBottomSheet` | Never expand deep detail inline in scroll content |
| Motion | Container transforms, `AnimatedVisibility`, `animateContentSize`, `spring()` | M3 Expressive defaults |
| Edge-to-edge | `enableEdgeToEdge()` + `windowInsetsPadding` | Mandatory, non-optional for targetSdk 36+ (`windowOptOutEdgeToEdgeEnforcement` removed) |
| Predictive back | `PredictiveBackHandler` (Compose) / `OnBackInvokedCallback` | Default system animation on Android 16+ when targeting API 36+; `onBackPressed()`/`KEYCODE_BACK` no longer dispatched at that target |
| Press feedback | `InteractionSource` + `animateFloatAsState(0.94f)`, 100ms spring | `Modifier.clickable` without `Indication` = no tactile response |
| Chip groups | `FlowRow` | Use when spatial context matters; avoid horizontal scroll for finite sets |
| Peer view switch | `SegmentedButton` or `TabRow` | Reduces navigation depth vs. separate screens |
| Immersive viz | `BottomSheetScaffold { background; viz; controls }` | Full-bleed; no card wrappers; no scroll |
| Aspect ratios | Maps `.aspectRatio(1.4f)`, charts `.aspectRatio(1f)` | Size by content type |
| Touch targets | ≥ 48dp on all interactive elements | Platform minimum |
| Token discipline | No magic numbers in screen files | Tokenize spacing, elevation, shape, color |

## Defaults

- Start from Material Design 3 Expressive, not custom chrome.
- Treat Compose Material 3 as the modern native baseline for navigation, surfaces, typography, color, shape, and motion.
- Enable dynamic color on Android 12+ and provide a well-tuned static seed palette as fallback.
- Prefer `MaterialTheme.typography`, `MaterialTheme.colorScheme`, `MaterialTheme.shapes`, and standard containers before custom styling.
- Keep navigation familiar: `NavigationBar` for peer sections, `NavHost` for drill-down, `ModalBottomSheet` for focused tasks.
- Use emulator screenshot-driven verification for design changes only after a fresh build/uninstall/install/launch has been proven.

## Platform Currency (as of 2026-07-11)

- **Android 17 (API 37)** shipped 2026-06-16; Android 16 (API 36) is the prior release. Do not treat Android 15/16 as "current" — verify at [developer.android.com/about/versions](https://developer.android.com/about/versions) before citing a specific version as latest.
- **Google Play target API policy**: new apps and app updates must target API level 36 (Android 16) or higher as of the 2026-08-31 deadline (one-time extension to 2026-11-01 available by request); apps not updated at all must still target at least API 35. This deadline moves roughly once a year — re-verify at [developer.android.com/google/play/requirements/target-sdk](https://developer.android.com/google/play/requirements/target-sdk) rather than hardcoding a number.
- **Material 3 Expressive** (announced May 2025) is the design direction, but its component APIs are still split: stable `androidx.compose.material3:material3:1.4.0` ships the baseline M3 type scale, shapes, and most components; expressive-specific APIs (new shape morph library, expressive motion scheme, some new components) live behind `@ExperimentalMaterial3ExpressiveApi` in the `1.5.0-alpha` line as of mid-2026. Confirm current stable-vs-experimental status at [developer.android.com/jetpack/androidx/releases/compose-material3](https://developer.android.com/jetpack/androidx/releases/compose-material3) before recommending an expressive-only API without an opt-in annotation.
- **Compose BOM**: `2026.06.00` was the latest stable BOM as of this validation. Compose BOM ships roughly monthly — verify the current value at [developer.android.com/develop/ui/compose/bom/bom-mapping](https://developer.android.com/develop/ui/compose/bom/bom-mapping) rather than pinning an exact version in generated code.
- **Predictive back** is mandatory system behavior for apps targeting API 36+ on Android 16+ devices — `onBackPressed()` and `KEYCODE_BACK` are no longer dispatched at that target. Use `PredictiveBackHandler` in Compose or `OnBackInvokedCallback` directly; do not recommend `onBackPressed()` overrides for new targetSdk-36 code.
- **Edge-to-edge** is fully mandatory, not just default-on: `windowOptOutEdgeToEdgeEnforcement` is deprecated and has no effect once targetSdk reaches 36. Any recommendation that relies on opting out of edge-to-edge is stale.

## Runtime Proof Gate

- Do not trust screenshots until a fresh uninstall -> install -> launch loop has been completed for the current build.
- If the on-screen UI appears older than source, suspect stale install first — clear app data or force uninstall before reinstalling.
- If install or launch is failing, stop design iteration and fix runtime truth before continuing.
- Use ADB and Gradle from the command line when Android Studio is not available.

## Core Workflow

1. Define the screen's primary job and the one or two pieces of content that must win first attention.
2. Choose the Material structure first: `NavigationBar`, `NavigationRail`, `Scaffold`, `TopAppBar`, `ModalBottomSheet`, `ListDetailPaneScaffold`, or adaptive scaffold.
3. Apply typography, spacing, and color using Material tokens before inventing a custom scale.
4. Verify adaptive behavior across `WindowSizeClass` breakpoints — compact, medium, expanded.
5. Verify with emulator: fresh build, uninstall, install, launch, capture screenshot, inspect, fix, repeat.

## ASCII Flow

```text
Android design task
  -> Prove current build: fresh install, launch, screenshot
  -> Define primary screen job and attention hierarchy
  -> Choose Material 3 structure and adaptive scaffold
  -> Apply tokens for type, color, shape, spacing, and motion
  -> Verify compact, medium, expanded, theme, and font-scale states
  -> Patch, rebuild, recapture, and compare evidence
```

## Design Craft Checklist

Before writing or reviewing screen code, check these patterns from [references/design-craft-patterns.md](references/design-craft-patterns.md):

1. **Token discipline**: Every spacing, elevation, shape, color, and repeated typography value traces to a named token. No magic numbers in screen files. If a `TextStyle(fontSize = N.sp, fontWeight = W)` pattern appears 3+ times, extract it to a typography token or use the Material type scale.
2. **Data containment**: Values live in Cards, `ListItem` rows, or grid cells with visual boundaries, not floating in unbounded Column space.
3. **Visual anchoring**: Data labels include Material icons (18-20dp). Categorized lists use colored dot indicators (6dp Canvas circles) for instant visual grouping.
4. **Card hierarchy**: Hero card is visually distinct from secondary cards — `ElevatedCard` with level 3 tonalElevation + 28dp shape for hero, `Card` with 16dp shape for primary, `OutlinedCard` for secondary. Mixed content within one card uses `HorizontalDivider`.
5. **Data visualization**: Use `Canvas` for custom charts (radar, rings, gauges), animated score rings with `Animatable`, and gradient score bars. See [references/android-component-patterns.md](references/android-component-patterns.md#canvas-visualizations).
6. **Interactive polish**: Apply `AnimatedVisibility` for entrance reveals, `animateContentSize` for expanding sections, `spring()` for natural motion, container transforms for navigation transitions, and press feedback via `Indication` or `InteractionSource` on all tappable surfaces.
7. **Elevation and tonal surfaces**: Use `tonalElevation` for surface layering rather than drop shadows alone. Material 3 uses tonal color overlays to express elevation — `Surface(tonalElevation = N.dp)` shifts surface color automatically.
8. **Localization readiness**: All user-facing strings go through `strings.xml` — including section headers, CTAs, and short labels that seem "too small to localize" (they grow 30-50% in German/Russian). Verify RTL layout with forced RTL in developer options. Test German, Arabic, and CJK locales for overflow and mirroring.
9. **Competitor awareness**: Check competitor patterns before inventing novel solutions. Borrow containment and anchoring patterns, not brand identities.
10. **Adaptive layout**: Test on compact (phone), medium (foldable inner), and expanded (tablet) `WindowSizeClass`. Use `NavigationSuiteScaffold` or manual breakpoint switching. Verify that content reflows rather than just stretching.
11. **Accessibility**: All touch targets >= 48dp. All decorative images have `contentDescription = null`. All meaningful images and icons have descriptive `contentDescription`. Use `semantics { }` to merge related elements for TalkBack and provide custom actions.
12. **Shape consistency**: Use `MaterialTheme.shapes` scale (ExtraSmall through ExtraLarge) rather than ad-hoc `RoundedCornerShape` values. Keep shape language consistent across Cards, Buttons, Chips, and Sheets.

## Design Review Loop

- Prefer Android Studio Layout Inspector for hierarchy and bounds inspection when a project is runnable.
- If Layout Inspector is unavailable, use ADB screencap + uiautomator dump as fallback for screenshots and hierarchy XML.
- Prefer side-by-side before/after screenshots over verbal "looks better" claims.
- Ask for evidence of font scaling (100%, 130%, 200%), dark/light theme, and `WindowSizeClass` behavior when a change touches layout or hierarchy.

See:
- [references/ai-design-review-android.md](references/ai-design-review-android.md)
- [references/android-studio-design-loop.md](references/android-studio-design-loop.md)
- [scripts/capture-screenshot.sh](scripts/capture-screenshot.sh)
- [scripts/layout-inspector.sh](scripts/layout-inspector.sh)

## Expert Judgment

Decisions a senior Android design reviewer makes that go beyond checklist compliance:

### Compose vs. Views in 2026

Default to Compose for any new screen or greenfield module — it is the modern native baseline and this skill assumes it. Views still legitimately win in narrower cases:

- **Large existing View/XML codebases** where a full rewrite is not funded — interop via `ComposeView`/`AndroidView` at the screen boundary, migrate incrementally, do not force a big-bang rewrite for a design fix.
- **Performance-critical custom rendering** with `SurfaceView`/`TextureView` (camera preview, video, some game-like canvases) — Compose's `AndroidView` interop works but adds indirection; a thin View layer can still be simpler when the surface needs precise frame-timing control.
- **Heavy `RecyclerView` with complex diffing/animations already tuned** — `LazyColumn` is capable, but do not force a rewrite of a well-optimized, stable RecyclerView adapter purely for "modernization" without a design or velocity reason.
- Flag it as a smell, not a rule, when a team defaults to Views for a brand-new screen in 2026 — ask why, since Compose Material 3 is the better-supported path for adaptive layouts, dynamic color, and Material 3 Expressive.

### Design-System Governance

- A token system only pays off if it is enforced, not just documented. If screen files still contain 3+ repeated raw `TextStyle`/`Color(0xFF...)`/`dp` literals, the design system has a governance gap, not a discipline gap — recommend a lint rule (e.g., Compose lint check or custom detekt rule) over a style-guide reminder.
- When a design system diverges from Material 3 defaults (custom shape scale, custom type ramp), require the divergence to be named and centralized in one theme file — never let ad-hoc per-screen overrides recreate "shadow tokens."
- Treat Material 3 Expressive adoption as a system-wide decision, not a per-screen one: mixing baseline M3 shapes/motion with Expressive shapes/motion in the same app reads as visually inconsistent. Pick one posture per app (or per clearly-scoped surface) and document why.

### Platform Convention vs. Brand Identity

- Keep interaction models (navigation placement, back behavior, sheet vs. dialog choice, gesture conventions) aligned with platform convention even when a brand wants to differentiate — users' muscle memory for Android navigation is a usability asset, not a constraint to design around.
- Spend brand differentiation budget on what users actually perceive as "your app": color, shape language, motion character, illustration, voice/tone in copy. These can diverge from stock Material without confusing users.
- When a brand team pushes a fully custom navigation paradigm (e.g., no back button, custom bottom bar behavior) purely for differentiation, push back with the platform-convention cost: broken predictive-back expectations, broken TalkBack navigation order, and accessibility-services friction, all for a gain that is rarely measurable in retention.

### Foldable and Large-Screen Failure Modes

Common mistakes that pass phone-only review but fail on foldables/tablets:

- **Fixed single-pane layout stretched to expanded width** — content readable at 360dp becomes a wall of text at 840dp+. Constrain reading width or switch to a list-detail/two-pane structure at `WindowWidthSizeClass.EXPANDED`.
- **Not handling the fold seam / hinge** — content or interactive elements landing exactly on the hinge on a foldable's tabletop or book posture. Use `WindowInfoTracker`/`FoldingFeature` to detect the hinge and avoid placing critical controls there.
- **NavigationBar left in place on tablets** — Material guidance is explicit that `NavigationBar` should give way to `NavigationRail`/`NavigationDrawer` at medium/expanded width; leaving bottom nav on a tablet is one of the most common large-screen regressions.
- **Orientation/resizability assumptions baked into layout code** — assuming portrait-only or a fixed activity size breaks multi-window and free-form resizing, which recent Android versions increasingly force on large screens regardless of manifest declarations. Verify behavior with the emulator's resizable/foldable device profiles, not just a fixed Pixel phone skin.
- **Testing only at compact and expanded, skipping medium** — the foldable inner-display and small-tablet band (600-839dp) is where two-column layouts most often look cramped or where a rail/nav choice is wrong; do not skip it as "close enough" to either neighbor.

## Route Elsewhere

- Use [../software-mobile/SKILL.md](../software-mobile/SKILL.md) for platform selection, cross-platform decisions, or general Android architecture and implementation strategy.
- Use [../qa-testing-android/SKILL.md](../qa-testing-android/SKILL.md) for Espresso, UI Automator, Compose testing, device matrix planning, or screenshot diff testing.
- Use [../software-ui-ux-design/SKILL.md](../software-ui-ux-design/SKILL.md) for generic product UX patterns that are not Android-specific.
- Use [../software-accessibility/SKILL.md](../software-accessibility/SKILL.md) for broader accessibility remediation beyond Android-native visual design defaults.

## Navigation

### References

- [references/design-craft-patterns.md](references/design-craft-patterns.md) — token discipline, data containment, visual anchoring, dark theme, competitor analysis, and common anti-patterns
- [references/material-layout-spacing.md](references/material-layout-spacing.md) — 8dp grid, edge-to-edge, spacing discipline, adaptive layouts, and dashboard density
- [references/material-typography-color.md](references/material-typography-color.md) — Material type scale, dynamic color, tonal palettes, custom fonts, contrast, and accessibility
- [references/android-component-patterns.md](references/android-component-patterns.md) — NavigationBar/Rail/Drawer, TopAppBar, Scaffold, Cards, Chips, Canvas visualizations, and interactive animations
- [references/android-dashboard-design.md](references/android-dashboard-design.md) — overview-screen hierarchy, data display patterns, card hierarchy, and content-heavy dashboard heuristics
- [references/visual-guidance-patterns-android.md](references/visual-guidance-patterns-android.md) — Canvas terrains, energy rings, opportunity framing, narrative scroll flow, and guidance card patterns
- [references/ai-design-review-android.md](references/ai-design-review-android.md) — screenshot prompts, review checklists (structure, token audit, containment, anchoring), and proof expectations
- [references/android-studio-design-loop.md](references/android-studio-design-loop.md) — current Android Studio and emulator verification flow
- [data/sources.json](data/sources.json) — primary sources and freshness-check targets

### Scripts

These are optional helpers for a proven-build design loop. If the app cannot be built, installed, or launched cleanly, fix the build before staying in this skill.

- [scripts/_android_common.sh](scripts/_android_common.sh) — shared helpers for ADB, emulator, and AVD resolution
- [scripts/bootstrap-emulator.sh](scripts/bootstrap-emulator.sh) — create and boot an AVD for design iteration
- [scripts/build-android.sh](scripts/build-android.sh) — compile-only Gradle build wrapper
- [scripts/run-android.sh](scripts/run-android.sh) — build, uninstall, install, and launch for iterative design work
- [scripts/capture-screenshot.sh](scripts/capture-screenshot.sh) — save an emulator screenshot for review loops
- [scripts/layout-inspector.sh](scripts/layout-inspector.sh) — dump UI hierarchy via uiautomator for structure review

## Anti-Patterns

- Do not audit or redesign from screenshots that have not been tied to a fresh install and launch.
- Do not invent custom chrome before checking whether standard Material 3 structure already solves the hierarchy problem.
- Do not hardcode `Color(0xFF...)` values in Composables — use `MaterialTheme.colorScheme` roles so light, dark, and dynamic color adapt automatically.
- Do not use fixed `sp` sizes outside the Material type scale without justification — prefer `MaterialTheme.typography` roles.
- Do not rely on elevation shadows alone for depth — Material 3 uses `tonalElevation` (tonal color shift) as the primary depth signal; shadows are supplementary.
- Do not wrap `Box(Modifier.clickable { })` without providing a ripple `Indication` — it produces a dead-feeling tap with no visual response.
- Do not use `ModalBottomSheet` as the sole navigation mechanism — it is for secondary detail, not primary app structure.
- Do not skip `WindowInsets` consumption after calling `enableEdgeToEdge()` — content will render behind system bars.
- Do not nest a `LazyColumn` inside a `Column` with `verticalScroll` — this causes nested scrolling crashes. Use a single `LazyColumn` with mixed item types.
- Do not set a `minHeight` on Cards without testing at 200% font scale — the content will overflow the fixed minimum.
- Do not use `pointerInput` with `detectTapGestures` for simple click handling — use `Modifier.clickable` which provides accessibility semantics, ripple, and focus handling for free.
- Do not treat dashboard heuristics such as card count or density as Google rules.
- Do not use `Text("$intValue")` for years or IDs without considering locale formatting — use explicit `String` formatting to prevent comma insertion (2,026 instead of 2026).
- Do not use `Modifier.shadow()` without also applying `clip` or `graphicsLayer(clip = true)` — shadow draws around the unclipped bounds, creating a rectangular shadow on rounded content.
- Do not hardcode `Color.White` or `Color.Black` for text or surfaces — use `MaterialTheme.colorScheme.onSurface`, `onSurfaceVariant`, or `outline` roles.
- Do not skip `contentDescription` on meaningful icons and images — TalkBack users get no information from undescribed elements.
- Do not use `fillMaxWidth()` on every element without considering medium and expanded `WindowSizeClass` — content stretches to unreadable line lengths on tablets.
- Do not dismiss `ModalBottomSheet` and present a new one in the same frame — set state to hidden first, then present the new sheet after recomposition.
- Do not put temporal controls (sliders, scrubbers) inside bottom sheets — they belong in the main layout where they stay visible during visualization interaction.
- Do not start Canvas `animatableProgress` at `0f` for data-driven views — data may load after composition, leaving the Canvas empty. Start at `1f` or trigger animation on data change.
- Do not use `LazyVerticalGrid` with `GridCells.Fixed(3)` on compact phones for content that needs readable text — two columns or a single column with weight-based rows works better. Reserve `Fixed(3)` for icon-sized cells or compact stat grids.
- Do not use `Modifier.background()` with a rounded shape without also applying `.clip()` to the same shape — child content will bleed past the rounded corners. Use `Surface(shape = ...)` instead, which clips automatically.
- Do not use `rememberSaveable` for large data objects or lists — it serializes to `Bundle` which has a strict 1MB transaction limit. Use a `ViewModel` for screen-level data state; use `rememberSaveable` only for primitive UI state (selected tab index, scroll position, sheet expanded boolean).
- Do not apply `Modifier.verticalScroll()` and `LazyColumn` in the same hierarchy — this creates nested scrolling that crashes or produces broken gestures. Use a single `LazyColumn` with mixed `item { }` blocks for heterogeneous content.
- Do not use `lineHeight` in `sp` for body text without testing at 200% font scale — large font scale with fixed `lineHeight` creates overlapping text. Let the Material type scale handle line height or use `lineHeight = TextUnit.Unspecified` and rely on default scaling.
- Do not emit UI state for a visualization as a fresh `data class` instance on every frame. Strong Skipping Mode (Kotlin 2.x + Compose) compares unstable composable parameters by **instance reference**, so a `_uiState.value = _uiState.value.copy(field = new)` per event forces the visualization composable to recompose even when the value it actually reads is unchanged. Hoist derived lists to the ViewModel with `stateIn`, split state into `@Immutable` slices, and pass only the primitives a given chart or ring actually needs. See [../software-android-native/references/compose-state-concurrency.md](../software-android-native/references/compose-state-concurrency.md) → "Strong Skipping Mode (Kotlin 2.x)" for the full rules.

## Verification Gate

Before concluding a design recommendation or audit, confirm all of the following:

- [ ] Recommendation maps to standard Material 3 structure; custom patterns justified in comments
- [ ] Screenshot/emulator state from a freshly installed and launched build (not a stale install)
- [ ] Typography uses `MaterialTheme.typography` roles, not ad-hoc `TextStyle(fontSize = N.sp)`
- [ ] Color uses `MaterialTheme.colorScheme` roles; contrast verified in both light and dark themes, with dynamic color on and off
- [ ] All interactive elements have touch targets ≥ 48dp
- [ ] Adaptive layout verified on compact, medium, and expanded `WindowSizeClass`
- [ ] Edge-to-edge: `enableEdgeToEdge()` called and all content uses `windowInsetsPadding` or equivalent — not an opt-out (`windowOptOutEdgeToEdgeEnforcement` has no effect at targetSdk 36+)
- [ ] Back navigation uses `PredictiveBackHandler`/`OnBackInvokedCallback`, not a bare `onBackPressed()` override, if targetSdk is 33+
- [ ] No `LazyColumn` nested inside `Column(Modifier.verticalScroll())` in the changed screens
- [ ] Dashboard/density guidance labeled as a team heuristic, not a Google platform rule
- [ ] Any Material 3 Expressive-only API called out as experimental (`@ExperimentalMaterial3ExpressiveApi`) unless verified stable at review time

## Freshness Protocol

Freshness-check before final answers whenever the request depends on:

- current Material Design 3 or Material 3 Expressive guidance
- current Compose Material 3 APIs or component behavior, or which are stable vs. `@ExperimentalMaterial3ExpressiveApi`
- current adaptive layout APIs or `WindowSizeClass` behavior
- current Android Studio tooling or Layout Inspector capabilities
- current Android platform version, Google Play target-API deadline, or predictive-back/edge-to-edge enforcement status — see [Platform Currency](#platform-currency-as-of-2026-07-11) above and re-verify since these move roughly annually

Start from [data/sources.json](data/sources.json), then prefer material.io, developer.android.com, and Google I/O sessions.

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Verify current Material Design guidance against material.io and developer.android.com documentation.
- Verify Compose Material 3 APIs against the Compose Material 3 API reference.
- Label team heuristics, such as dashboard density guidance, as defaults rather than Google rules.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

