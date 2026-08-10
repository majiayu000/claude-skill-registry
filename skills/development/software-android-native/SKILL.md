---
name: software-android-native
description: "Guides native Android development with Kotlin, Jetpack Compose, and Views interop. Use when building, rewriting, or reviewing modern Android apps after establishing runtime truth."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Native Android Development

Use this skill for native Android work only. It is the default shared-skill entrypoint for Compose-first Android apps targeting API 28+, bounded rewrites from older codebases, and agent-assisted workflows in Android Studio, Codex, and Claude Code.

## Quick Reference

| Task | Default Picks | Notes |
|------|---------------|-------|
| **State & UI** | | |
| New UI screens | Jetpack Compose | Views interop only where existing mature flows or third-party SDKs require it |
| Observable state | ViewModel + `StateFlow` (Kotlin 2.x) | Replaces LiveData for new code |
| Async work | Kotlin Coroutines + Flow | `Dispatchers.IO` for blocking, `Dispatchers.Default` for CPU; structured concurrency preferred |
| Unit/integration tests | JUnit 5 + Turbine | Turbine for Flow testing; JUnit 5 for coroutine lifecycle |
| UI tests | Compose Testing APIs (`ComposeTestRule`) | Espresso only for Views interop or legacy screens |
| **State machine discipline** | | |
| Submit guard | `if (_uiState.value is Loading) return` | Prevents double-tap duplicate submissions in ViewModel |
| Auto-reset transitions | `viewModelScope.launch { delay(500); _uiState.value = Idle }` | Input ready for next action without manual UI reset |
| Minimal sealed classes | Remove states that can't happen anymore | Dead sealed subclasses produce dead `when` branches and mislead future readers |
| **Networking & resilience** | | |
| Network reachability | `ConnectivityManager` + `NetworkCallback` wrapped in `StateFlow` | Publish `isConnected`; disable submit buttons when offline; observe in `collectAsStateWithLifecycle` |
| **DI & architecture** | | |
| Dependency injection | Hilt | `@HiltViewModel`, `@Inject constructor`, `@Module` + `@InstallIn` |
| Local persistence | Room + KSP | Prefer `@Upsert` over separate insert/update; KSP replaces KAPT |
| Background work | WorkManager + `CoroutineWorker` | Deferrable, constraint-aware background processing |
| **Agent tooling & build** | | |
| Agent tooling (in Android Studio) | Android Studio Gemini assistant | Built-in coding agent surface |
| Agent tooling (outside IDE) | Gradle CLI + ADB | Terminal-first build, install, launch, and inspection |
| Build command | `./gradlew assembleDebug` | Or specific module: `./gradlew :app:assembleDebug` |
| Install command | `adb install -r app/build/outputs/apk/debug/app-debug.apk` | `-r` replaces existing without clearing data |
| Launch command | `adb shell am start -n com.example.app/.MainActivity` | Verify package and component name from manifest |
| Emulator management | `avdmanager`, `emulator` CLI | Headless: `emulator -avd Name -no-window -no-audio` for CI |
| Logcat | `adb logcat -s TAG:V` | Filter by tag; `adb logcat *:E` for errors only |
| Screenshot | `adb exec-out screencap -p > screenshot.png` | Fast visual proof from emulator or device |
| **Compose patterns** | | |
| LazyColumn / LazyRow | Always provide `key` in `items(key = { it.id })` | Prevents recomposition bugs on list mutation |
| Canvas drawing | `Canvas(modifier) { drawScope -> ... }` with `DrawScope` | Use `drawLine`, `drawCircle`, `drawArc`, `drawPath` |
| Canvas gestures | `Modifier.pointerInput(Unit) { detectTapGestures / detectDragGestures }` | Compute hit targets from coordinates, not invisible tap areas |
| Type-safe navigation | `@Serializable` route classes + `NavHost` (Navigation 2.9+) | Compile-time route safety; replaces string-based routes |
| Animations | `animateFloatAsState`, `Animatable`, `InfiniteTransition` | Choose based on one-shot vs continuous vs interruptible |
| `derivedStateOf` | `remember { derivedStateOf { ... } }` | For computed state that depends on frequently changing sources |
| Side effects | `LaunchedEffect`, `DisposableEffect`, `SideEffect` | `LaunchedEffect(key)` for coroutine work; `DisposableEffect` for cleanup |
| Modifier order | Padding before background vs after changes result | Modifier chain is sequential; order is layout-significant |
| `Modifier.testTag` | `Modifier.testTag("submit_button")` | Required for Compose test node finders |
| Snackbar | `SnackbarHostState` + `SharedFlow` from ViewModel | Collect events in `LaunchedEffect`; never use `Toast` for important feedback |
| **Billing & payments** | | |
| BillingClient | Play Billing Library 8+ (v9.x current as of 2026-07-11; v8+ mandatory for all new apps/updates by 2026-08-31, extension to 2026-11-01) | Initialize in `Application.onCreate` or Hilt singleton; verify current minimum at [developer.android.com/google/play/billing/release-notes](https://developer.android.com/google/play/billing/release-notes) |
| Acknowledge purchases | `acknowledgePurchase()` within 3 days | Unacknowledged purchases auto-refund after 3 days |
| Subscription offers | `ProductDetails.subscriptionOfferDetails` | Base plan, offer phases (free trial, introductory price) |
| Promotional offers | Developer-determined offers in Play Console | Configure offer eligibility; apply via `BillingFlowParams.SubscriptionUpdateParams` |
| Consumables | `consumeAsync()` after backend confirms | Prevents re-granting; consume only after server receipt |
| **Adaptive layouts** | | |
| Window size classes | `WindowSizeClass` from `material3-window-size-class` | `Compact`, `Medium`, `Expanded`; branch layout in Composable |
| List-detail pane | `ListDetailPaneScaffold` (Material3 adaptive) | Canonical two-pane pattern for tablets and foldables |
| Navigation suite | `NavigationSuiteScaffold` | Auto-switches between bottom nav, rail, and drawer by size class |
| Foldable support | `WindowInfoTracker` (Jetpack Window) | Detect fold posture, hinge bounds; adapt layout for table-top mode |
| **Auth & push** | | |
| Credential Manager | `CredentialManager` API (Jetpack) | Unified passkeys, passwords, and federated sign-in |
| Biometric auth | `BiometricPrompt` (AndroidX) | `canAuthenticate()` check first; `BIOMETRIC_STRONG` for crypto |
| Push notifications | FCM (`FirebaseMessaging`) | `onNewToken` for registration; `onMessageReceived` for data messages |
| Notification channels | `NotificationChannel` (API 26+) | Must create before posting; group related channels with `NotificationChannelGroup` |
| Deep links | Compose Navigation deep links | `navDeepLink { uriPattern = "app://..." }` on route; App Links require `assetlinks.json` |
| `collectAsStateWithLifecycle` | `stateFlow.collectAsStateWithLifecycle()` | Lifecycle-aware collection; prevents updates when app is backgrounded |
| **Strong Skipping (Kotlin 2.x)** | | |
| UI state instance identity | Split state into `@Immutable` slices; hoist derived lists to ViewModel | Strong Skipping Mode compares unstable params by **reference**; a fresh `copy()` per frame defeats skipping |
| `LazyListScope` lambdas | `val onClick = remember(id) { { vm.onClick(id) } }` | Lambda memoization from Strong Skipping only applies inside `@Composable` — **not** inside `items { }` |
| Main-thread UI mutation | Do blocking work under `withContext(Dispatchers.IO)`, assign `_uiState.value = ...` outside that block | Off-main state mutation surfaces as `CalledFromWrongThreadException` or `ConcurrentModificationException` in `SnapshotStateObserver` |

## When to Use This Skill

Use this skill to:

- Build new Compose-first screens and features for Android apps targeting API 28+
- Plan and execute bounded rewrites from Views or older Kotlin/Java codebases
- Set up agent-assisted Android workflows in Android Studio, Codex, or Claude Code
- Implement Kotlin Coroutines, Flow, and ViewModel state patterns
- Prepare data safety declarations, target SDK compliance, and release gates
- Review native Android code for architecture, performance, and compliance

## Defaults

- New native Android work: prefer Jetpack Compose for new screens and Views interop only where existing mature flows or third-party SDKs require it.
- New observable UI state: prefer ViewModel + `StateFlow` and keep UI-facing state collected on the main thread with `collectAsStateWithLifecycle`.
- Async work: prefer Kotlin Coroutines with structured concurrency; use `Dispatchers.IO` for blocking I/O and `Dispatchers.Default` for CPU-bound work.
- Dependency injection: prefer Hilt for new projects.
- Local persistence: prefer Room with KSP annotation processing.
- Build system: prefer Gradle KTS (`build.gradle.kts`) with version catalogs (`libs.versions.toml`).
- Navigation: prefer type-safe Compose Navigation 2.9+ with `@Serializable` route classes.
- New unit and integration tests: prefer JUnit 5 with Turbine for Flow assertions.
- UI tests: prefer Compose Testing APIs; keep Espresso for legacy Views screens.
- Release gates: treat target SDK compliance, data safety declarations, ProGuard/R8 rules, Play Integrity, accessibility, and real-device verification as non-optional.

## ASCII Flow

```text
Android native task
  -> Confirm app shape: Compose, Views interop, service, or release gate
  -> Prove Gradle, emulator/device, install, and launch reality
  -> Choose architecture: ViewModel, StateFlow, Hilt, Room, Navigation
  -> Implement bounded slice with lifecycle-aware state and tests
  -> Check Kotlin, Compose, R8, billing, and Play-policy traps
  -> Build, install, launch, inspect logs, and report proof
```

## Known Kotlin Traps

These are current headline footguns for Compose-first native Android on Kotlin 2.x. Each is source-backed; re-verify versions against the linked release notes before quoting a fix window.

- **`CalledFromWrongThreadException` / `ConcurrentModificationException` in `SnapshotStateObserver`.** Compose reads snapshot state on the main thread; mutating `_uiState.value` from a coroutine body that ran on `Dispatchers.IO` without switching back surfaces as a main-thread crash or a reentrant-modification race. Fix: keep `withContext(Dispatchers.IO) { ... }` blocks pure (return a value, do not mutate state inside), assign `_uiState.value = ...` on the main dispatcher, and collect via `collectAsStateWithLifecycle()` — never a raw `collect` inside `LaunchedEffect`. See [references/compose-state-concurrency.md](references/compose-state-concurrency.md).
- **Strong Skipping Mode identity checks.** On Kotlin 2.x + Compose 1.8+, Strong Skipping Mode compares **unstable** params by instance reference. Emitting UI state as a fresh `data class` per event (`_state.value = _state.value.copy(...)`) defeats skipping even though the observable values are unchanged — `LazyColumn` rows recompose on every unrelated update. Fix: hoist derived lists and filtered views to the ViewModel with `stateIn(scope, WhileSubscribed(5000), ...)`; split UI state into `@Immutable` slices; pass `PersistentList<T>` from `kotlinx-collections-immutable`. Source: [developer.android.com/develop/ui/compose/performance/stability/strongskipping](https://developer.android.com/develop/ui/compose/performance/stability/strongskipping).
- **`LazyListScope` lambda memoization gap.** Strong Skipping's automatic lambda memoization applies inside `@Composable` functions; it does **not** apply inside `LazyListScope.items { ... }` or `LazyColumn`'s content block. Unremembered callbacks captured there produce a new instance per recomposition. Fix: `val onClick = remember(id) { { vm.onClick(id) } }` at the items-block site, or hoist to a stable `() -> Unit` reference.
- **Compose plugin version skew on Kotlin 2.x.** Since Kotlin 2.0 the Compose compiler ships with the Kotlin compiler and is applied via the Gradle plugin `kotlin("plugin.compose")`. A stale or missing plugin declaration surfaces as `Argument type mismatch: actual type 'Function0<Unit>', but '@Composable ComposableFunction0<Unit>' was expected` — the transform did not run. Fix: lock `plugin.compose` to the exact Kotlin version in `libs.versions.toml`. Source: [developer.android.com/jetpack/androidx/releases/compose-kotlin](https://developer.android.com/jetpack/androidx/releases/compose-kotlin).
- **Compose runtime regressions fixed upstream.** If you see a crash in pausable composition under `LookaheadScope`, nested `Popup` positioning against the screen instead of the parent, or a reentrant-modification crash in `SnapshotStateObserver`, upgrade to the latest Compose UI patch release before treating the problem as app-level — as of 2026-07-11 the production Compose BOM is in the `2026.06.xx` line (Compose runtime/UI ~1.11.4, with 1.12 in beta requiring `compileSdk 37` + AGP 9), and the `SnapshotStateObserver` reentrant-modification guard landed in the 1.10.0-rc01 cycle; a project still pinned below that line should treat this class of crash as a known-fixed upgrade target, not a fresh bug. Verify current at [developer.android.com/jetpack/androidx/releases/compose-ui](https://developer.android.com/jetpack/androidx/releases/compose-ui). Route to [../software-android-runtime-debugging/references/compose-debugging.md](../software-android-runtime-debugging/references/compose-debugging.md).
- **`kotlinx-serialization` + R8 full mode.** Since kotlinx-serialization 1.9.0, AGP 8.x release builds can fail with `SerializationException: Serializer for class 'X' is not found` or `ExceptionInInitializerError`, and the build emits warnings about `<1>$*` keep rules. Fix: keep the generated `$serializer` classes explicitly and run a release-variant smoke test in CI that exercises every `@Serializable` entry point. Route to [../software-android-runtime-debugging/references/proguard-r8-triage.md](../software-android-runtime-debugging/references/proguard-r8-triage.md).

## Kotlin Anti-Patterns

These are behaviors to actively refuse in new code; they are not compile errors but each has caused measurable harm in production Kotlin/Android codebases.

| # | Anti-pattern | Why it bites | Better default |
|---|-------------|-------------|----------------|
| K1 | `GlobalScope.launch { ... }` | Marked `@DelicateCoroutinesApi`; JetBrains is phasing it out. Coroutines started here survive navigation, never cancel, and accumulate as memory leaks on busy screens. | `viewModelScope`, `lifecycleScope`, or an injected `CoroutineScope` parented to a `SupervisorJob` you own. |
| K2 | Passing an external `Job` into `launch(externalJob)` to "inherit" cancellation | Overrides the scope's job, becomes the parent, and breaks structured concurrency. Cancellation of the scope no longer propagates. Recent IntelliJ releases flag this with a coroutine inspection. | Never pass `Job` as a context argument. Use a child scope or a `SupervisorJob` explicitly scoped to the lifecycle you want. |
| K3 | `LiveData` + `observeAsState` in new Compose code | Hidden main-thread hop, older backpressure, worse interaction with Strong Skipping because `State<T>` produced by `observeAsState` wraps a mutable holder. | `StateFlow` + `collectAsStateWithLifecycle()` for new code. Keep LiveData only for legacy Views screens still on it. |
| K4 | Nullability as the primary way to model "loading" / "error" / "success" | Forces every call site to branch on `null` and loses type information about why the value is absent. | Sealed class / sealed interface: `Idle` / `Loading` / `Success(data)` / `Error(message, cause)` with an exhaustive `when`. Kotlin's compiler warns on missing branches when a new state is added. |
| K5 | Keeping `kapt` on Kotlin 2.x annotation processors | `kapt` uses the old JVM backend and is often incompatible with K2; slows every build and can silently drop generated code. | Migrate to KSP2 (K2-compatible). Hilt, Room, and Moshi-codegen all support KSP2; verify current support status in each library's release notes. |
| K6 | Treating `StateFlow.value = copy(field = new)` as free | Strong Skipping Mode compares the new object's reference to the old one. Even if only one primitive changed, consumers that take the whole state object as a parameter recompose. | Split state into logical slices, hoist derived lists, and prefer primitives or `@Immutable` sub-objects as composable parameters. |
| K7 | Filtering or sorting lists inside a composable body | Creates a new list reference per recomposition; Strong Skipping can never skip a downstream `LazyColumn`. | Compute in ViewModel, expose as `StateFlow<ImmutableList<T>>`; or wrap in `derivedStateOf { ... }` inside a `remember`. |
| K8 | `runBlocking { ... }` in production code paths (outside `main()` and tests) | Blocks the calling thread; on the main thread it freezes the UI and can ANR; in library code it defeats structured concurrency. | Make the function `suspend` and let the caller pick the scope. |

Route deeper pattern material through [references/compose-state-concurrency.md](references/compose-state-concurrency.md).

## Architecture Judgment Calls

Decisions that need a rationale, not just a default pick. As of 2026-07-11, verify each version-specific claim at the linked source before quoting it.

- **Compose vs Views in 2026.** Compose is the default for all new screens; there is no scenario in a greenfield API 28+ app where Views is the right starting point. Keep Views only for: (1) a third-party SDK that ships a `View`-based render surface with no Compose wrapper (some map, ad, or video SDKs), (2) a legacy screen mid-migration where the cost of a full rewrite outweighs the interop tax, or (3) `SurfaceView`/`TextureView`-backed continuous rendering (camera preview, custom video) where Compose's `AndroidView` bridge is the right embedding, not a reason to avoid Compose for the rest of the screen. Do not accept "Views is faster" as a reason in 2026 — Compose's skip/restart model with Strong Skipping enabled is on par with or ahead of View-based `RecyclerView` diffing for list-heavy UI when state discipline (K6, K7) is followed.
- **Hilt vs Koin.** Hilt (compile-time, annotation-processor-based, built on Dagger) remains the repo default for new API 28+ apps: it fails at compile time on a broken graph, has first-class `@HiltViewModel` / `WorkManager` / `Compose Navigation` integration, and is what most enterprise Android codebases already standardize on. Prefer Koin instead only when: the team explicitly wants to avoid annotation processing and Gradle plugin overhead (KSP-free build), the project is small enough that compile-time graph validation matters less than iteration speed, or the codebase is a Kotlin Multiplatform module where Hilt cannot run (Hilt is Android/JVM-only; Koin runs on all KMP targets). Do not switch an existing Hilt codebase to Koin mid-project without a concrete, named pain point — DI framework churn has a high cost for a marginal ergonomics gain.
- **Kotlin Multiplatform (KMP).** KMP has been stable since November 2023 and Compose Multiplatform for iOS reached stable with 1.8.0; Jetpack libraries including Room, DataStore, and ViewModel now ship `commonMain` artifacts. This is a real option for sharing business logic (networking, persistence, ViewModel state) across Android and iOS — but it is a **product/architecture decision**, not a default for this skill. If the task is "should we share code with iOS," route to [software-mobile](../software-mobile/SKILL.md) (or the `software-mobile-architect` advisor, where available) for the cross-platform tradeoff call before writing shared-module code; this skill assumes the Android-native side once that call is made. Verify current KMP/Compose Multiplatform stability status at [kotlinlang.org/docs/multiplatform/supported-platforms.html](https://kotlinlang.org/docs/multiplatform/supported-platforms.html).
- **When NOT to go native.** If the actual question is "should this feature be a native Android screen at all" (vs. a cross-platform framework, a web view, or a KMP-shared module), that decision belongs to [software-mobile](../software-mobile/SKILL.md) (or the `software-mobile-architect` advisor) — do not let this skill's Compose-first defaults silently answer a platform-choice question it was not asked.
- **Coroutines vs Flow failure modes.** A `suspend fun` returns one value and is the wrong tool for anything that emits more than once (search-as-you-type, connectivity state, DB observation) — using a polling `suspend` loop instead of `Flow` produces stale reads and duplicate work. Conversely, wrapping a one-shot operation (a single network POST) in a `Flow` that a caller collects once adds `Flow`'s cancellation/backpressure machinery for no benefit — a plain `suspend fun` is simpler and equally cancellable via structured concurrency. Rule of thumb: one value now -> `suspend fun`; zero-to-many values over time -> `Flow`; a single ViewModel-to-UI event stream that should not replay -> `SharedFlow` with `replay = 0`, not `StateFlow`.
- **Process death and `SavedStateHandle`.** `ViewModel` survives configuration change but not process death under memory pressure. Anything the user would be upset to lose on a background-kill-and-restore (form input mid-fill, scroll position, in-progress multi-step flow state) must go through `SavedStateHandle` (`@HiltViewModel` constructor-injects it automatically), not just `ViewModel` field state. Test this with `adb shell am kill <package>` while backgrounded, not just rotation — rotation alone never exercises the process-death path and gives false confidence.

## ANR and Frame Budget Arithmetic

Use these thresholds when diagnosing jank or ANR reports; re-derive the math rather than quoting a remembered number.

- **Input dispatch ANR: 5 seconds.** If the main thread does not return from handling a touch or key event within 5s, the system raises `Input dispatching timed out`. This is the most common production ANR class and is almost always a synchronous DB/network/disk call on the main thread, not an actual 5-second-long computation.
- **Foreground service start ANR: 5 seconds.** `startForegroundService()` must reach `startForeground()` within 5s or the system raises `ForegroundServiceDidNotStartInTimeException` territory (see S3 below for the related `ForegroundServiceStartNotAllowedException`/`MissingForegroundServiceTypeException` cases).
- **Broadcast receiver ANR: 10s foreground / 60s background.** `onReceive()` running past this window on the relevant app-state timer raises an ANR; move any real work off `onReceive()` into `WorkManager` or a coroutine launched from a longer-lived scope.
- **Service execution ANR: 20s foreground / 200s background.** `onCreate()`/`onStartCommand()`/`onBind()` blocking past this window raises an ANR; verify current thresholds at [developer.android.com/topic/performance/anrs/diagnose-and-fix-anrs](https://developer.android.com/topic/performance/anrs/diagnose-and-fix-anrs) since these have shifted across Android versions.
- **Frame budget at 60Hz: 1000ms / 60 = 16.666...ms per frame.** A composable recomposition, layout, and draw pass that together exceed ~16.67ms drops a frame; two consecutive misses read as visible jank.
- **Frame budget at 120Hz: 1000ms / 120 = 8.333...ms per frame.** High-refresh-rate devices (now the majority of mid-range and flagship Android hardware) halve the available budget — a composable that was "fine" at 60Hz can visibly jank at 120Hz. Do not assume a perf fix validated at 60Hz on an emulator holds on a 120Hz physical device; re-verify with `adb shell dumpsys gfxinfo <package> framestats` or Android Studio's Frame Profiler on the actual refresh rate.

## Runtime Truth And Prompting

Use a proof-first execution loop for native Android work:

- verify tool reality first: Android Studio Gemini, Gradle CLI, ADB, and emulator or device availability
- prove build, install, and launch before UI diagnosis
- keep repo memory lean and fact-only
- require bounded slices with explicit proof artifacts

Load [references/runtime-proof-and-prompts.md](references/runtime-proof-and-prompts.md) for:

- AI-agent defaults
- proof-first and token-discipline rules
- the execution loop
- high-value prompt shape

## Rewrite Workflow

1. Lock the baseline:
   existing app behavior, minimum API level, device classes, external integrations, and non-goals.
2. Choose the target defaults:
   Compose-first, API 28+, ViewModel + StateFlow, Hilt, Room + KSP, Kotlin Coroutines, JUnit 5, Compose Testing.
3. Slice the rewrite into bounded vertical features:
   app shell (Application class, Hilt setup, navigation graph), auth/session, core navigation, feature flows, integrations, release surfaces.
   - If the project uses multi-module Gradle, verify module dependencies and build order before adding new modules.
   - If migrating from Java to Kotlin, convert one file at a time using Android Studio's converter, then review and fix idiom issues. Do not bulk-convert entire packages without validation.
   - If migrating from Views to Compose, use `ComposeView` in existing XML layouts as a bridge. Do not rewrite an entire Activity/Fragment hierarchy in one pass.
4. For each slice, require evidence:
   build success, install and launch success, targeted tests, parity notes, and known gaps.
5. Keep release-only concerns visible throughout:
   data safety declarations, target SDK compliance, ProGuard/R8 rules, Play Integrity, push/deep-link behavior, store metadata.
6. End every batch with a handoff:
   changed behavior, validation performed, residual risk, next slice.
7. When a backend change eliminates an error class (e.g., unifying two API paths into one), immediately remove the now-impossible error types, decoders, and UI states from the Android client. Dead error handling misleads future developers about what can actually happen and inflates the codebase.

## Specialized Patterns

Load [references/ui-and-integration-patterns.md](references/ui-and-integration-patterns.md) when the work involves:

- Compose, adaptive-layout, or foldable-specific implementation patterns
- native/backend integration gotchas for auth, onboarding, or Supabase or Firebase-backed flows
- Google Play Billing rules and RTDN constraints

## When NOT to Use This Skill

Use a different skill when:

- **Cross-platform or platform-choice decisions** -> [software-mobile](../software-mobile/SKILL.md)
- **Android test execution, device matrix, Espresso deep dives** -> [qa-testing-android](../qa-testing-android/SKILL.md)
- **Web UI or browser app implementation** -> [software-frontend](../software-frontend/SKILL.md)
- **General architecture without Android-specific constraints** -> [software-architecture-design](../software-architecture-design/SKILL.md)
- **Backend platform selection (Supabase, Firebase, Convex)** -> [software-baas-platforms](../software-baas-platforms/SKILL.md)

## Scenarios

Recipes keyed to symptoms or migration moments. Each lists the shortest path to resolution using patterns above.

### S1 — Compose recomposition perf bug after Strong Skipping upgrade

1. Enable Compose compiler metrics: add `freeCompilerArgs += ["-P", "plugin:androidx.compose.compiler.plugins.kotlin:reportsDestination=..."]`.
2. Identify composables marked `unstable` in the report; focus on those receiving the full UI state object.
3. Split the monolithic state into `@Immutable` slices and hoist derived lists to `StateFlow` in ViewModel.
4. Replace `List<T>` params with `ImmutableList<T>` from `kotlinx-collections-immutable`.
5. Re-run the metrics; verify the hot composables are now marked `skippable`.
6. Confirm the fix with a baseline profile trace before and after on a real device.

### S2 — R8 stripping kotlinx-serialization classes

1. Reproduce in a release build: run `./gradlew :app:assembleRelease` and trigger the failing serialization path.
2. Check the R8 mapping file and logcat for `SerializationException: Serializer for class 'X' is not found`.
3. Add explicit keep rules for every `@Serializable` class and its generated `$serializer` companion; see [references/android-release-and-compliance.md](references/android-release-and-compliance.md).
4. Add a release-variant smoke test in CI that exercises every serialized entry point.
5. Verify the fixed APK with `adb install -r` and re-run the failing path end-to-end.

### S3 — Foreground service crash on API 35

1. Check the crash log for `ForegroundServiceStartNotAllowedException` or `MissingForegroundServiceTypeException`.
2. Declare `android:foregroundServiceType` in the `<service>` manifest element (e.g. `dataSync`, `mediaPlayback`).
3. Pass the matching `ServiceInfo.FOREGROUND_SERVICE_TYPE_*` flag to `startForeground()`.
4. Add a runtime check: if the app is in the background, use WorkManager instead of starting a foreground service.
5. Test on an API 35 emulator with `adb shell am kill` to simulate background-state entry before the start call.

### S4 — Predictive back gesture migration

1. Set `android:enableOnBackInvokedCallback="true"` in the manifest `<application>` element.
2. Replace all `onBackPressed()` overrides with `OnBackPressedCallback` registered on `onBackPressedDispatcher`.
3. For Compose Navigation, confirm `NavHost` handles `OnBackPressedCallback` automatically; add explicit callbacks only for custom back logic.
4. Test with gesture navigation enabled on API 33+ device; verify animated back preview renders correctly.
5. Remove any legacy `KeyEvent.KEYCODE_BACK` handlers that now conflict with the new callback.

### S5 — In-app billing v7 entitlement reconciliation

1. Initialize `BillingClient` as a Hilt singleton; connect in `Application.onCreate`.
2. On `BillingClient.BillingResponseCode.OK` after purchase, call the backend to verify the purchase token server-side before granting access.
3. Call `acknowledgePurchase()` within 3 days; unacknowledged purchases auto-refund.
4. Subscribe to `PurchasesUpdatedListener` and `queryPurchasesAsync(QueryPurchasesParams)` on app foreground to catch out-of-band purchases.
5. Handle `ITEM_ALREADY_OWNED` gracefully by querying existing entitlements rather than surfacing an error.

## Navigation

### References

| Resource | Purpose |
|----------|---------|
| [references/android-rewrite-playbook.md](references/android-rewrite-playbook.md) | Rewrite slicing, acceptance criteria, and evidence rules |
| [references/agentic-android-tooling.md](references/agentic-android-tooling.md) | Android Studio Gemini, Gradle CLI + ADB, and emulator selection rules |
| [references/android-studio-workflows.md](references/android-studio-workflows.md) | Gradle wrapper, build variants, canonical build/test/install loops |
| [references/codex-claude-android-workflows.md](references/codex-claude-android-workflows.md) | Repo memory, approval boundaries, and prompt patterns |
| [references/runtime-proof-and-prompts.md](references/runtime-proof-and-prompts.md) | Proof-first runtime execution, token discipline, and prompt shape |
| [references/ui-and-integration-patterns.md](references/ui-and-integration-patterns.md) | Compose, adaptive-layout, backend integration, and billing patterns |
| [references/compose-state-concurrency.md](references/compose-state-concurrency.md) | Verified app-layer defaults for Compose, StateFlow, and coroutines |
| [references/android-release-and-compliance.md](references/android-release-and-compliance.md) | Target SDK, data safety, ProGuard/R8, and release-gate checks |
| [data/sources.json](data/sources.json) | Primary sources and current external references |

### Templates

Use the rewrite brief at project start, the feature request per slice, the proof checklist at each verification gate, and the agent handoff at batch boundaries.

| Template | Purpose |
|----------|---------|
| [assets/template-android-rewrite-brief.md](assets/template-android-rewrite-brief.md) | Rewrite scope and constraint brief |
| [assets/template-android-feature-request.md](assets/template-android-feature-request.md) | Feature-level Codex / Claude Code request format |
| [assets/template-android-proof-checklist.md](assets/template-android-proof-checklist.md) | Source-backed proof and validation checklist |
| [assets/template-android-agent-handoff.md](assets/template-android-agent-handoff.md) | Post-change handoff with evidence and residual risk |

### Related Skills

| Skill | Purpose |
|-------|---------|
| [software-mobile](../software-mobile/SKILL.md) | Platform choice and cross-platform tradeoffs |
| [qa-testing-android](../qa-testing-android/SKILL.md) | Android test execution, device matrix, and Espresso/UI Automator |
| [qa-testing-mobile](../qa-testing-mobile/SKILL.md) | Cross-platform mobile QA strategy |
| [agents-memory](../agents-memory/SKILL.md) | Shared `AGENTS.md` / `CLAUDE.md` memory strategy |
| [dev-context-engineering](../dev-context-engineering/SKILL.md) | Cross-tool context design for Codex and Claude Code |
| [software-performance](../software-performance/SKILL.md) | Performance measurement and regression gates |
| [software-baas-platforms](../software-baas-platforms/SKILL.md) | Backend platform selection and comparison |
| [ai-context-layer/references/conversational-surfaces-cross-platform.md](../ai-context-layer/references/conversational-surfaces-cross-platform.md) | Natural-conversation composition for Android (Gemini Nano via AICore / ML Kit GenAI, ObjectBox on-device vector index, deterministic Composer B for non-AICore devices) inside the cross-platform recipe |

---

## Freshness Protocol

### Trigger Conditions

- "Latest Android Studio / Compose / Kotlin changes?"
- "Gradle or AGP setup?"
- "Android data safety declaration requirements?"
- "Play Store submission requirements?"
- "Is [Android framework/tool] still the default?"
- "Target SDK deadline?"

### How to Freshness-Check

1. Start from [data/sources.json](data/sources.json) for Google/Android docs and release notes.
2. Run a targeted web search for the specific Android Studio, Compose, or Kotlin question.
3. Prefer developer.android.com, kotlinlang.org, and official Android release notes.

### What to Report

- **Current landscape**: stable Jetpack libraries and tooling
- **Emerging tools**: new Android Studio features, Kotlin evolution, Compose updates
- **Deprecated/declining**: APIs being sunset, tools losing support
- **Recommendation**: default choice with rationale

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Prefer developer.android.com, kotlinlang.org, and Android release notes for Compose, Kotlin, Hilt, Room, Navigation, WorkManager, Play Billing, and store requirements.
- Prefer official OpenAI and Anthropic docs for Codex / Claude Code memory and workflow behavior.
- Prefer the official Gradle and AGP documentation for build system behavior.
- If a claim is not source-backed or clearly labeled as a repo default, remove it.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

