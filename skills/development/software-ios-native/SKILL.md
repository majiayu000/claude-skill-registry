---
name: software-ios-native
description: "Guides native iOS with Swift, SwiftUI, UIKit interop, concurrency, and persistence. Use when building or reviewing iPhone/iPad apps after establishing runtime truth."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Native iOS Development

Use this skill for native iOS work only. It is the default shared-skill entrypoint for SwiftUI-first iOS 17+ apps, bounded rewrites from older codebases, and agent-assisted workflows in Xcode, Codex, and Claude Code.

## Quick Reference

| Task | Default Picks | Notes |
|------|---------------|-------|
| **State & UI** | | |
| New UI screens | SwiftUI | UIKit interop only where Apple APIs require it |
| Observable state (iOS 17+) | `@Observable` + main actor isolation | Replaces ObservableObject/Published |
| Async work | `async`/`await`, structured concurrency | Detached tasks only when intentionally breaking inheritance |
| Unit/integration tests | Swift Testing | Preferred over XCTest for new tests |
| UI automation tests | XCTest / XCUITest | Keep using for UI and performance tests |
| **State machine discipline** | | |
| Submit guard | `guard state == .idle else { return }` | Prevents double-tap duplicate submissions in `@Observable` stores |
| Auto-reset transitions | `Task { try await Task.sleep(for: .milliseconds(500)); state = .idle }` | Composer/input ready for next action without manual UI reset |
| Minimal state enums | Remove states that can't happen anymore | Dead enum cases produce dead error handling and mislead future readers |
| **Networking & resilience** | | |
| Network reachability | `@Observable` singleton + `NWPathMonitor` | Publish `isConnected`; disable submit buttons when offline; start monitor in screen `.onAppear` |
| **Agent tooling & build** | | |
| Agent tooling (in Xcode) | Xcode native assistant | Current stable is Xcode 26.6 (Swift 6.3); Xcode 27 beta (Swift 6.4, on-device AI code completion) shipped from WWDC26 but is not yet GA — do not build release submissions against a beta SDK |
| Agent tooling (outside Xcode) | XcodeBuildMCP if callable | Otherwise fall back immediately to Apple CLI |
| CLI fallback | `xcodebuild`, `simctl`, `xcresulttool` | Default path when MCP is unavailable or blocked |
| Build / install / stale-app failures | `software-ios-runtime-debugging` | Use before UI or feature diagnosis |
| XcodeGen projects | `scripts/generate-xcodeproj.sh` | Must regenerate after adding new Swift files |
| **Local-dev launcher pair** | `scripts/run-local-ios-dev.sh` + `scripts/stop-local-ios-dev.sh` | Two defensive guards (grep env + generated plist for `localhost:`); persist simulator UDID; never `pkill -f Simulator`. See [quick-reference-extended.md#agent-tooling--build](references/quick-reference-extended.md#agent-tooling--build) |
| `.pbxproj`-managed projects | Add new files to target membership | Do not assume on-disk Swift files are auto-discovered |
| **Generated files / CI landmines** | Commit generated outputs or regenerate in CI hook | `git add -f` for gitignored-folder tracked files; Xcode Cloud `ci_post_clone.sh` for env shims. See [quick-reference-extended.md](references/quick-reference-extended.md#agent-tooling--build) |
| **TARGETED_DEVICE_FAMILY → "1"** | Requires fresh archive + ASC build attachment | Changing `project.yml` alone is insufficient; value is baked into binary. |
| **Canvas & visualization** | | |
| Canvas data views | Start `animatedProgress` at 1 | Data loads after `.onAppear`; starting at 0 leaves Canvas empty |
| Canvas gestures | `DragGesture` + `SpatialTapGesture` overlay | Compute hit targets from coordinates, not invisible tap areas |
| Type checker crashes | Split complex views into helper functions | `.overlay { if }` and tuple `ForEach` are common triggers |
| **StoreKit & billing** | | |
| StoreKit 2 subscriptions | `@Observable` StoreKitManager + TransactionSyncService | `transaction.finish()` only after backend sync confirms |
| Paywall presentation | `.sheet(isPresented:)` from any locked screen | Don't navigate to Settings; present modal directly |
| Product pricing display | `product.displayPrice` from StoreKit | Never hardcode prices; Apple handles locale formatting |
| Promotional offers (rewards) | Server-signed `.promotionalOffer()` in `Product.purchase(options:)` | Bridges Stripe credit gaps for Apple-billed users; user must redeem |
| **Paid Apps Agreement (#1 invisible blocker)** | Verify Active at appstoreconnect.apple.com/business | Silent empty `Product.products(for:)` results; check before subscription-level diagnosis. Full decision table + timeline in [app-store-connect-checklist.md Phase 5](../software-mobile/references/app-store-connect-checklist.md). See [quick-reference-extended.md](references/quick-reference-extended.md#storekit--billing) |
| **ASC `Missing Metadata`** | Fill all required fields: prices, localization, review screenshot | Products exist but fields incomplete. Workflow in [app-store-connect-checklist.md](../software-mobile/references/app-store-connect-checklist.md). See [quick-reference-extended.md](references/quick-reference-extended.md#storekit--billing) |
| **Review screenshot** | sRGB 8-bit RGB PNG 72 DPI, 1284 × 2778 | ASC rejects Display P3 / 16-bit device screenshots; use Pillow profile conversion. See [quick-reference-extended.md](references/quick-reference-extended.md#storekit--billing) |
| **Accounting currency (backend-denominated)** | `NumberFormatter` + explicit `currencyCode` + `locale = .current` | Never `String(format: "£%.2f", …)`; details in [quick-reference-extended.md](references/quick-reference-extended.md#storekit--billing) |
| Year/ID display | `Text(verbatim:)` | Suppress locale number formatting (2026 not 2,026) |
| **Immersive screens & sheets** | | |
| Immersive viz screens | `ZStack { bg; scene; controls; .sheet(persistent) }` | No scroll, no card wrappers, sheet peek + bottom padding |
| Persistent sheet | `.presentationBackgroundInteraction(.enabled(upThrough: .medium))` | Allows gestures on viz while sheet is visible |
| Viz state: inspect (chart) | Parent `@Binding` for zoom/drag | Controls strip reads/writes same state |
| Viz state: orbit (3D) | Parent `@State` + callback | SceneKit drives camera, reports back |
| Viz state: navigate (map) | Internal `@State` | Zero-latency gesture response for spatial pan/zoom |
| Parent-initiated reset | Reset token (`Int` incremented by parent) | View `.onChange(of: token)` resets internal state |
| Viz overlay controls | `Picker(.segmented)` + `Menu` | Native controls, not custom material-backed buttons |
| Dense diagram controls | Zoom in/out/reset + semantic filters | When gates, labels, or markers overlap, expose inspection controls before redrawing the whole chart |
| Diagram detail placement | Below-chart summary or persistent sheet | Do not cover the diagram with popups or bottom overlays that block inspection |
| Canvas animation (glow/pulse) | `TimelineView(.animation)` wrapping Canvas | Gate behind condition to avoid 30fps waste |
| Square Canvas sizing | `.aspectRatio(1, contentMode: .fit)` | Prevents dead space in taller-than-wide frames |
| Viz export/share | `ImageRenderer` + `proposedSize` | Static export view, no gestures or parallax |
| Immersive shared state | `@Observable` class via `@State` + `@Bindable` | Avoids 15+ `@Binding` prop-drilling |
| Year/ID in `navigationTitle` | String concat: `name + " " + String(year)` | No `verbatim:` overload — interpolation resolves to `LocalizedStringKey` |
| Multiple sheets | Multiple `.sheet` modifiers on one view | iOS 16.4+; each gated by its own `Optional` property |
| Grid cell width | `.frame(maxWidth: .infinity)` inside `LazyVGrid` cells | Content doesn't stretch automatically; without this, columns are unequal |
| Help/detail row width | `.frame(maxWidth: .infinity, alignment: .leading)` | Leading `VStack` rows shrink to intrinsic width unless explicitly stretched, making peer containers uneven |
| Grid cell clip shape | `RoundedRectangle` not `Capsule` | Capsule pinches at wide aspect ratios in stretched grid cells |
| Deleting `.pbxproj` files | Remove `PBXBuildFile`, `PBXFileReference`, group child, and sources entry | Missing any one leaves stale references or build warnings |
| Sheet swapping | Set `item` to `nil`, delay ~350ms, set new value | `.sheet(item:)` can't swap in one frame; `onDismiss` + state = loop |
| l10n in plain enums | Call l10n in View body, not enum methods | `@MainActor` l10n store can't be called from nonisolated enum funcs |
| l10n key coverage | Verify all `l10n.text()` keys exist in locale JSONs | Fallback strings mask missing keys in the default language; switch language to confirm |
| l10n value coverage | Verify new non-English values are not English fallbacks | Key parity alone is insufficient; generated catalogs can contain English defaults in every locale |
| l10n large-file edits | Use `json.load` → modify → `json.dump` for locale JSONs | The Edit tool silently fails on files >500KB; always verify writes programmatically |
| Generated l10n catalogs | Fix upstream source-of-truth, then regenerate | Editing only the generated iOS copy is a stopgap — next regeneration overwrites it |
| `LocalizationStore.text` crash | Patch source-of-truth, regenerate, test | Stack trace in `resolvedTemplate` = shipped catalog missing key; Swift fallback alone doesn't survive next generation |
| **Backend locale propagation** | `?locale=` query + `Accept-Language` header on every request | Priority: `?locale=` > `Accept-Language` > stored profile. Call `propagateLocaleToAPIClient()` on every picker change. See [quick-reference-extended.md](references/quick-reference-extended.md#l10n--backend-locale) |
| **Locale-aware time formatting** | `DateFormatter.dateFormat(fromTemplate: "jm", options: 0, locale: locale)` | "jm" skeleton respects 12h/24h user override; cache instances in `NSCache`. See [quick-reference-extended.md](references/quick-reference-extended.md#l10n--backend-locale) |
| **Backend prose vs structural data** | Structural data: client-side enum helpers; prose: server-side translation | Chart positions/names need no backend translation; only generated prose does. See [quick-reference-extended.md](references/quick-reference-extended.md#l10n--backend-locale) |
| **Interpolated prose template split** | Translate `prefix`/`suffix` templates; inject runtime values verbatim | Never cache strings with embedded runtime values (explodes cache key space). See [quick-reference-extended.md](references/quick-reference-extended.md#l10n--backend-locale) |
| **Auth & push** | | |
| Sign in with Apple | `ASAuthorizationController` + `CheckedContinuation` | Required by Guideline 4.8 if any 3rd-party social login is offered |
| OTP code input | Hidden `TextField` + `.textContentType(.oneTimeCode)` | Better than magic links for native; iOS auto-fills from notifications |
| Non-`@MainActor` delegates | `nonisolated` + `MainActor.assumeIsolated` | For `ASAuthorizationControllerDelegate`, `MKLocalSearchCompleterDelegate`, etc. |
| Push notification categories | Register `UNNotificationCategory` in `didFinishLaunchingWithOptions` | Must be set before any notification arrives; match `aps.category` from backend |
| Badge count (iOS 16+) | `try? await UNUserNotificationCenter.current().setBadgeCount(0)` | `applicationIconBadgeNumber` is deprecated; `setBadgeCount` is `async throws` |
| Push delegate isolation | `@unchecked Sendable` + `@MainActor` async UN delegate | `nonisolated async` + nested `await MainActor.run` crashes with `_performBlockAfterCATransactionCommitSynchronizes:`. See [swiftui-observation-concurrency.md](references/swiftui-observation-concurrency.md#nonisolated-async-delegate-methods--nested-mainactorrun) and [quick-reference-extended.md](references/quick-reference-extended.md#auth--push--detailed-rows) |
| Bare `Task { }` isolation | `Task { @MainActor [weak self] in ... }` from `@MainActor` classes | Bare `Task {}` runs on global executor; does NOT inherit `@MainActor`. See [swiftui-observation-concurrency.md](references/swiftui-observation-concurrency.md#bare-task---does-not-inherit-mainactor) |
| `actor` vs `@MainActor final class` | Prefer `@MainActor final class` when all consumers are `@MainActor` | Round-trip `@MainActor → actor → @MainActor` causes post-await tail on wrong executor. See [swiftui-observation-concurrency.md](references/swiftui-observation-concurrency.md#actor--mainactor-final-class-refactoring-guidance) |
| `@Sendable async` closure awaited from `@MainActor` | Retype as `@MainActor async` closure | Does NOT reliably resume on main; common in SDK `RequestExecutor` typealiases. See [swiftui-observation-concurrency.md](references/swiftui-observation-concurrency.md#sendable-async-closure-isolation-footgun) |
| `SCNView` in `UIViewRepresentable` | Build scene once in `makeUIView`, `updateUIView` is a no-op | Reassigning `scene` in `updateUIView` crashes via CATransaction off-main. See [swiftui-observation-concurrency.md](references/swiftui-observation-concurrency.md#scnview-reassignment-in-updateuiview-anti-pattern) |
| Push action routing | Check `response.actionIdentifier` in `didReceive` | `UNNotificationDefaultActionIdentifier` = tap; custom IDs = action buttons; dismiss = no route |
| Push-open ownership, preferences, entitlements, APNs proof, archive gate, backend routing, QA loop | See full rows in [quick-reference-extended.md](references/quick-reference-extended.md#auth--push--detailed-rows) | Archive gate: `codesign -d --entitlements` must print `production`; backend: per-device `push_environment` column authoritative |
| Swift Concurrency crash triage | Symptom-first triage runbook | Private SwiftUI symbol crash → start at [swift-concurrency-crash-triage.md](../software-ios-runtime-debugging/references/swift-concurrency-crash-triage.md); ladder: console → MTC → TSan → lldb `bt` |
| **SwiftUI API modernization** | | |
| Deprecated API review | [references/swiftui-deprecated-api.md](references/swiftui-deprecated-api.md) | Systematic deprecated→modern mapping |
| SwiftUI performance audit | [references/swiftui-performance.md](references/swiftui-performance.md) | View splitting, lazy stacks, modifier efficiency |
| Modern Swift idioms | [references/modern-swift-patterns.md](references/modern-swift-patterns.md) | Foundation modernization, date/string/collection patterns |
| **Concurrency (constructive)** | | |
| Writing correct concurrency | [references/swift-concurrency-patterns.md](references/swift-concurrency-patterns.md) | Structured concurrency, async streams, bridging, migration |
| Concurrency compiler errors | [references/swift-concurrency-diagnostics.md](references/swift-concurrency-diagnostics.md) | Error→fix mapping for Swift 6 diagnostics |
| **Persistence** | | |
| SwiftData modeling | [references/swiftdata-core.md](references/swiftdata-core.md) | Core rules, predicates, CloudKit, indexing, class inheritance |
| Core Data persistence | [references/core-data-persistence.md](references/core-data-persistence.md) | Stack setup, contexts, object IDs, batch ops, migrations, CloudKit |
| Reusable app skeleton | [references/native-ios-app-foundation-skeleton.md](references/native-ios-app-foundation-skeleton.md) | SwiftUI shell, Observation state, persistence, CloudKit, App Intents, local AI hooks, release gates |
| iCloud database app | [references/icloud-cloudkit-app-skeleton.md](references/icloud-cloudkit-app-skeleton.md) | SwiftData/Core Data/CloudKit choice, private/public/shared scopes, no-server limits |
| **Stacks & monetization** | | |
| Pick a starter stack to monetize/engage | [references/starter-stacks-and-monetization.md](references/starter-stacks-and-monetization.md) | CloudKit→Cloudflare→RevenueCat→Supabase graduation ladder; on-device AI as free tier; webhook idempotency traps |
| Run iOS dev as a conveyor / app factory | [references/ios-app-conveyor.md](references/ios-app-conveyor.md) | 4 pillars: default stack per class, shared SPM, Fastlane+Match CI, agent build loop; 2026 stack survey |
| **Build performance** | | |
| Xcode build optimization | [references/xcode-build-optimization.md](references/xcode-build-optimization.md) | Benchmarking, diagnostic flags, SPM analysis, common wins |
| **Swift 6.2+ / Xcode 26+ additions** | | |
| Default actor isolation (new projects) | `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` in Xcode 26+ | App targets benefit most; library targets stay `nonisolated`. Flip flag, triage leaf types, mark non-UI `nonisolated`/`@concurrent`, remove defensive `MainActor.run` wraps. Do NOT bulk-silence with `@preconcurrency` |
| `withAnimation` in `@MainActor` | Known iOS 26 regression | Hoist `withAnimation` outside `@MainActor` body or wrap in `Task { @MainActor in withAnimation(…) { … } }`; verify on iOS 26.0 / 26.2 / 26.4 |
| `SubscriptionStatus.all` stale after subscription change | Xcode 26 StoreKit 2 bug | Query `Product.SubscriptionInfo.Status` directly after `Transaction.updates` tick; don't trust cached `all` array |
| `AnyView` avoidance | Type erasure defeats diffing | Use `@ViewBuilder`, `some View`, or `Group + if/switch` instead |
| `@ObservedObject` in new code | Legacy pre-iOS-17 pattern | Replace with `@Observable` + `@Bindable`; `@StateObject` → `@State`; `@Published` unnecessary on `@Observable` |
| `NavigationView` deprecation | Replaced | `NavigationStack` for push/pop; `NavigationSplitView` for multi-column |
| `.id(UUID())` force refresh | Anti-pattern | Causes full re-init + retained subscriptions; drive refreshes from state |
| Combine subscription lifecycle | Memory leak #1 | Every `sink`/`assign` into `.store(in: &cancellables)` or cancel in `onDisappear`/`deinit` |
| Coordinator-pattern navigation | `NavigationStack` + enum routes | `@Observable AppCoordinator` with `path`; inject via `@Entry`; one coordinator per module |

## When to Use This Skill

SwiftUI-first iOS 17+ screens, app skeletons, UIKit bounded rewrites, agent-assisted Xcode/Codex/Claude Code workflows, Swift Concurrency, SwiftData/Core Data persistence, Xcode build optimization, privacy manifests, release gates, and native iOS code review.

## Defaults

- UI: SwiftUI-first; UIKit interop only where Apple APIs require it.
- State: `@Observable` + main actor isolation (iOS 17+).
- New projects: `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` (Xcode 26+); `nonisolated`/`@concurrent` only when breaking out.
- Async: structured concurrency + `async`/`await`; detached tasks only when intentionally breaking inheritance.
- Tests: Swift Testing for unit/integration; XCTest/XCUITest for UI automation.
- Release gates: privacy manifests, required-reason APIs, SDK compliance, accessibility, real-device verification — non-optional. Verify minimum Xcode version at developer.apple.com/news/releases each release cycle.

## Version Currency (check every session)

- **Current stable (verify at each session):** iOS/iPadOS 26.x, Xcode 26.6, Swift 6.3. App Store Connect has rejected uploads not built with the iOS 26 SDK since 2026-04-28 — this gate does not change your deployment target, only the build SDK.
- **Announced, not shipped:** WWDC26 (June 2026) previewed iOS/iPadOS/macOS 27 and Xcode 27 (Swift 6.4, on-device AI code completion, agent skills bundled with Xcode). As of this session Xcode 27 is beta-only. Do not recommend Xcode 27/iOS 27 APIs for anything shipping to the App Store; treat every "iOS 27" claim as provisional until Apple's GA release notes confirm it, and re-verify the current stable/beta split before quoting a specific point release — these move every few weeks.
- Point releases (26.2 vs 26.4 vs 26.6) drift fast; treat any specific point-release number in this skill as the value observed at last validation, not a permanent fact.

## Expert Judgment Calls

- **SwiftUI vs UIKit:** default to SwiftUI. Reach for UIKit interop only for a named capability gap (e.g., precise text-kit control, certain camera/AR compositions, legacy `UICollectionView` compositional layouts not yet matched in SwiftUI) — not because a contributor is more comfortable in UIKit. Re-evaluate the gap list each Xcode cycle; SwiftUI closes gaps yearly and yesterday's justified UIKit escape hatch is often removable.
- **Strict concurrency adoption:** for a new project, take the Xcode 26 defaults (Approachable Concurrency on, `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, Strict Concurrency Checking = Complete) — migration pain is close to zero because there is no legacy code to fight. For an existing pre-Swift-6 codebase, do not flip strict concurrency in one PR: enable it module-by-module or file-by-file, starting from leaf types with no dependents, and budget real calendar time — the Swift Forums "explosion of isolation violations" reports are the normal experience, not a sign something is wrong. Never bulk-silence with `@preconcurrency` as a substitute for doing the migration.
- **Dependency management:** Swift Package Manager is the default for every new dependency and for new projects outright. Only keep CocoaPods where an existing project already depends on it and the migration cost (Pods with no SPM manifest, deeply nested transitive Pod dependencies) currently exceeds the maintenance tax of running two package managers. Don't introduce a new CocoaPods dependency into an SPM-only project to save a day of integration work — it reintroduces the exact tooling fragmentation SPM removed.
- **Modularization threshold:** don't split into SPM modules pre-emptively. Splitting pays off once a target exceeds roughly 150-200 files, once independent teams need to build/test in isolation, or once agent-driven workflows need a bounded package to avoid loading the whole app graph for one feature. Below that, module boundaries add build-graph and API-surface overhead without a compiler-enforced win. See [xcode-build-optimization.md → SPM Dependency Analysis](references/xcode-build-optimization.md#spm-dependency-analysis) for the build-time tradeoffs either way.
- **TestFlight and phased release discipline:** never promote straight from internal build to a 100% production release. Run at least one external TestFlight wave sized to catch device/OS-version variance, then use phased release (7-day ramp) for production so a bad build caps its blast radius before full rollout. Treat a skipped phased release as a release-risk finding worth calling out, not a minor process nit.

## ASCII Flow

```text
iOS native task
  -> Confirm app shape: SwiftUI, UIKit interop, service, or release gate
  -> Prove Xcode, simulator/device, build, install, and launch reality
  -> Choose architecture: Observation, concurrency, persistence, navigation
  -> For reusable skeletons, add iCloud data, App Intents, local AI/retrieval hooks, and release gates
  -> Implement bounded slice with tests and privacy/accessibility checks
  -> Check Swift, StoreKit, signing, privacy, and App Store traps
  -> Build, run, inspect logs/screenshots, and report proof
```

## Runtime Truth And Prompting

Proof-first: verify tool reality (Xcode assistant → XcodeBuildMCP → Apple CLI), prove build+launch before UI diagnosis, require bounded slices with explicit proof artifacts. Load [references/runtime-proof-and-prompts.md](references/runtime-proof-and-prompts.md) for agent defaults, proof rules, execution loop, and prompt shape.

## Rewrite Workflow

1. Lock the baseline:
   existing app behavior, minimum OS, device classes, external integrations, and non-goals.
2. Choose the target defaults:
   SwiftUI-first, iOS 17+, Observation, Swift Concurrency, Swift Testing, XCTest/XCUITest.
3. Slice the rewrite into bounded vertical features:
   app shell, auth/session, core navigation, feature flows, integrations, release surfaces.
   XcodeGen: run `scripts/generate-xcodeproj.sh` after adding new files. `.pbxproj` projects: register new files in target membership explicitly.
4. For each slice, require evidence:
   build success, run success, targeted tests, parity notes, and known gaps.
5. Keep release-only concerns visible throughout: privacy manifests, entitlement changes, required-reason APIs, push, store metadata.
   Push QA: sign off `sandbox` (device) and `production` (TestFlight) paths separately; validate cold-start tap, warm resume, and normal reopen.
6. End every batch with a handoff: changed behavior, validation performed, residual risk, next slice.
7. When a backend change eliminates an error class, immediately remove the now-impossible error types, decoders, and UI states from the iOS client.

## Specialized Patterns

Load [references/ui-and-integration-patterns.md](references/ui-and-integration-patterns.md) for Canvas/gesture/immersive surfaces, auth/onboarding/Supabase integration gotchas, and StoreKit 2 billing + server-notification rules.

## Release Signing And Distribution

- `Release` signing gate: disable auto-signing, set `Signing Certificate = Apple Distribution` + `App Store Connect` provisioning profile. Turning auto-signing off alone doesn't fix archive.
- Valid distribution archive must show `aps-environment = production`, `get-task-allow = false`, `beta-reports-active = true`. Still see `development` or `get-task-allow = true` → archive is dev-signed; not ready for TestFlight.
- Inspect the exact newest `.xcarchive`; don't use a generic `find ... .app` that can hit an older one.
- In Organizer choose `App Store Connect` for TestFlight/App Review — not `Release Testing`.
- Validation can fail on generated `Info.plist` (e.g., missing `UISupportedInterfaceOrientations~ipad`); review generated plist, not just UI.
- Encryption prompt: Apple/system crypto only → `None of the algorithms mentioned above`. Suppress with `ITSAppUsesNonExemptEncryption = NO` in plist.
## Known iOS Traps

Full trap table (31 rows) in [references/ios-traps-and-scenarios.md](references/ios-traps-and-scenarios.md). Top traps by crash frequency and silent-failure risk:

| Trap | Symptom | Fix |
|---|---|---|
| `_performBlockAfterCATransactionCommitSynchronizes:` | Private SwiftUI assertion on Concurrency Task | One of 5 root causes below; never add defensive `MainActor.run` wraps |
| `nonisolated async` UN delegate + nested `await MainActor.run` | Notification-tap freeze / crash | Mark delegate `@MainActor`; `@unchecked Sendable`; delete nested hops |
| Bare `Task { }` in `@MainActor` class mutating `@Observable` | Same crash; cooldown timers, `Transaction.updates`, post-sleep resets | `Task { @MainActor [weak self] in … }` |
| `@MainActor → actor → @MainActor` round-trip | Post-await tail on actor executor, not main | Promote `actor` to `@MainActor final class` when all callers are main-isolated |
| `@Sendable async` closure awaited from `@MainActor` | Continuation doesn't reliably resume on main | Retype as `@MainActor async` closure |
| `SCNView.scene = scene` in `updateUIView` | CATransaction on SceneKit render thread, UIKit crash | Build scene once in `makeUIView`; `updateUIView` no-op |
| iOS 26 `withAnimation` in `@MainActor` methods | Animations fail to start or skip starting state | Hoist `withAnimation` out of `@MainActor` body |
| Xcode 26 `SubscriptionStatus.all` stale | StoreKit 2 shows wrong tier post-upgrade | Query `Product.SubscriptionInfo.Status` directly |
| Locale-change handler missing store reset | Language change has no visible effect | `reset()` every prose-caching store + `URLCache.shared.removeAllCachedResponses()` |
| Stored profile locale wins over `?locale=` param | iOS user sees English despite picker showing Russian | Server priority must be `?locale=` > `Accept-Language` > stored profile |

Web-search `_performBlockAfterCATransactionCommitSynchronizes:` before code review (private symbol). `dataCorrupted` + `<!DOCTYPE html>` = API routing/auth bug, not push crash. Never bulk-silence Swift 6 errors with `@preconcurrency`. Detailed recipes in [swift-concurrency-crash-triage.md](../software-ios-runtime-debugging/references/swift-concurrency-crash-triage.md).

## When NOT to Use This Skill

Use a different skill when:

- **Cross-platform or platform-choice decisions** → [software-mobile](../software-mobile/SKILL.md)
- **iOS build/install/launch failures, stale installs, simulator drift, XcodeGen issues** → [software-ios-runtime-debugging](../software-ios-runtime-debugging/SKILL.md)
- **iOS test execution, simulator flake control, `xcresult` triage** → [qa-testing-ios](../qa-testing-ios/SKILL.md)
- **Web UI or browser app implementation** → [software-frontend](../software-frontend/SKILL.md)
- **General architecture without iOS-specific constraints** → [software-architecture-design](../software-architecture-design/SKILL.md)
- **iOS visual design, HIG layout/typography, dark mode design, dashboard patterns** → [software-ios-design](../software-ios-design/SKILL.md)

## Scenarios

Full recipes (S1–S5) in [references/ios-traps-and-scenarios.md](references/ios-traps-and-scenarios.md).

| Scenario | Key steps |
|---|---|
| S1 · StoreKit 2 entitlement reconciliation | `Transaction.updates` listener on launch; query `SubscriptionInfo.Status` directly; `finish()` only after backend sync |
| S2 · APNs sandbox vs production proof | `codesign -d --entitlements`; store per-device `push_environment`; server-side deterministic send; verify `production` on TestFlight row |
| S3 · Swift 6.2 concurrency migration | Flip `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`; promote leaf actors; remove defensive `MainActor.run`; no `@preconcurrency` bulk-silence |
| S4 · `withAnimation` Xcode 26 regression | Hoist out of `@MainActor` body or `Task { @MainActor in withAnimation { } }`; verify 26.0 / 26.2 / 26.4 separately |
| S5 · Privacy manifest pre-submission audit | `rg` for required-reason APIs; add `NSPrivacyAccessedAPITypes`; validate `.xcarchive` with Organizer before upload |

## Navigation

### References

| Resource | Purpose |
|----------|---------|
| [references/quick-reference-extended.md](references/quick-reference-extended.md) | Verbose Quick Reference rows moved from SKILL.md: local-dev launcher, CI landmines, StoreKit/ASC, l10n, push |
| [references/ios-traps-and-scenarios.md](references/ios-traps-and-scenarios.md) | Full Known iOS Traps table (31 rows) and Scenarios S1–S5 recipes |
| [references/ios-rewrite-playbook.md](references/ios-rewrite-playbook.md) | Rewrite slicing, acceptance criteria, and evidence rules |
| [references/agentic-ios-tooling.md](references/agentic-ios-tooling.md) | Xcode's native coding agent, XcodeBuildMCP, and CLI fallback selection rules |
| [references/xcodebuildmcp-workflows.md](references/xcodebuildmcp-workflows.md) | Verified XcodeBuildMCP install, config, and workflow loops |
| [references/codex-claude-ios-workflows.md](references/codex-claude-ios-workflows.md) | Repo memory, approval boundaries, and prompt patterns |
| [references/runtime-proof-and-prompts.md](references/runtime-proof-and-prompts.md) | Proof-first runtime execution, token discipline, and prompt shape |
| [references/ui-and-integration-patterns.md](references/ui-and-integration-patterns.md) | Canvas, immersive UI, backend integration, and StoreKit 2 patterns |
| [references/swiftui-observation-concurrency.md](references/swiftui-observation-concurrency.md) | Verified app-layer defaults for SwiftUI, Observation, and concurrency |
| [references/swiftui-deprecated-api.md](references/swiftui-deprecated-api.md) | Deprecated→modern SwiftUI API mapping |
| [references/swiftui-performance.md](references/swiftui-performance.md) | View splitting, lazy stacks, modifier efficiency, and rendering patterns |
| [references/swift-concurrency-patterns.md](references/swift-concurrency-patterns.md) | Structured concurrency, async streams, bridging, and migration tables |
| [references/swift-concurrency-diagnostics.md](references/swift-concurrency-diagnostics.md) | Swift concurrency compiler error→fix mapping |
| [references/swiftdata-core.md](references/swiftdata-core.md) | SwiftData modeling, predicates, CloudKit, indexing, and class inheritance |
| [references/core-data-persistence.md](references/core-data-persistence.md) | Core Data stack ownership, context rules, migrations, and CloudKit constraints |
| [references/native-ios-app-foundation-skeleton.md](references/native-ios-app-foundation-skeleton.md) | Reusable SwiftUI app foundation: modules, defaults, extension points, proof gates |
| [references/icloud-cloudkit-app-skeleton.md](references/icloud-cloudkit-app-skeleton.md) | iCloud/CloudKit data-layer: schema, database scopes, no-server boundaries |
| [references/modern-swift-patterns.md](references/modern-swift-patterns.md) | Modern Swift idioms, Foundation API, and coding style |
| [references/xcode-build-optimization.md](references/xcode-build-optimization.md) | Build benchmarking, compilation diagnostics, and optimization workflow |
| [references/ios-release-and-compliance.md](references/ios-release-and-compliance.md) | Privacy, SDK compliance, and release-gate checks |
| [data/sources.json](data/sources.json) | Primary sources and current external references |

### Templates

| Template | Purpose |
|----------|---------|
| [assets/template-ios-rewrite-brief.md](assets/template-ios-rewrite-brief.md) | Rewrite scope and constraint brief |
| [assets/template-native-ios-app-skeleton.md](assets/template-native-ios-app-skeleton.md) | Copyable native iOS app foundation layout and module checklist |
| [assets/template-ios-cloudkit-persistence-stack.md](assets/template-ios-cloudkit-persistence-stack.md) | SwiftData/Core Data/CloudKit stack starter with schema and sync gates |
| [assets/template-ios-makefile-and-proof-loop.md](assets/template-ios-makefile-and-proof-loop.md) | Agent-friendly Makefile targets and build/test/archive proof loop |
| [assets/template-ios-feature-request.md](assets/template-ios-feature-request.md) | Feature-level Codex / Claude Code request format |
| [assets/template-ios-proof-checklist.md](assets/template-ios-proof-checklist.md) | Source-backed proof and validation checklist |
| [assets/template-ios-agent-handoff.md](assets/template-ios-agent-handoff.md) | Post-change handoff with evidence and residual risk |
| [assets/scaffolds/app-class-blueprints.md](assets/scaffolds/app-class-blueprints.md) | Pick app class (CRUD/notes, AI wrapper, content/feed, utility-IAP) → tier, scaffolds, monetization, cost |
| [assets/scaffolds/entitlement-and-paywall.md](assets/scaffolds/entitlement-and-paywall.md) | Copy-paste StoreKit 2 `EntitlementStore` + `PaywallGate` (single source of truth) |
| [assets/scaffolds/push-and-engagement.md](assets/scaffolds/push-and-engagement.md) | Copy-paste `PushManager` with deferred opt-in + `Reachability` |
| [assets/scaffolds/cloudflare-worker-backend.md](assets/scaffolds/cloudflare-worker-backend.md) | Worker scaffold: subscription webhook (idempotent, re-fetch), AI proxy, push |

### Related Skills

| Skill | Purpose |
|-------|---------|
| [software-mobile](../software-mobile/SKILL.md) | Platform choice and cross-platform tradeoffs |
| [software-ios-runtime-debugging](../software-ios-runtime-debugging/SKILL.md) | Build/install/launch proof, stale-build triage, and simulator/package debugging |
| [qa-testing-ios](../qa-testing-ios/SKILL.md) | iOS test execution, `xcresult`, and simulator stability |
| [agents-memory](../agents-memory/SKILL.md) | Shared `AGENTS.md` / `CLAUDE.md` memory strategy |
| [dev-context-engineering](../dev-context-engineering/SKILL.md) | Cross-tool context design for Codex and Claude Code |
| [software-performance](../software-performance/SKILL.md) | Performance measurement and regression gates |
| [software-ios-design](../software-ios-design/SKILL.md) | iOS design patterns, HIG compliance, dark mode, dashboard layout |

---

## Freshness Protocol

Freshness-check before final answers on Xcode/SwiftUI/Swift Testing changes, XcodeBuildMCP setup, iOS privacy manifests, App Store requirements, or any "is X still the default?" question. Start from [data/sources.json](data/sources.json), then Apple Developer docs and WWDC sessions.

## Fact-Checking

Version-specific crashes, regressions, and workarounds must be verified against current primary sources. Prefer Apple docs/release notes for Xcode/SwiftUI/privacy/store; official Anthropic/OpenAI docs for Codex/Claude Code; XcodeBuildMCP repo for tool names and config. Remove claims that are not source-backed.

## Learnings Loop

Before non-trivial tasks: read `learnings.consolidated.md` (and `learnings.md` if present). After: append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md`.
