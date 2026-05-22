---
name: software-mobile
description: Production-grade mobile app development with Swift (iOS), Kotlin (Android), React Native, and WebView patterns, including UI/UX, navigation, state management, networking, local storage, push notifications, and App Store deployment.
---

# Mobile Development Skill — Quick Reference

This skill equips mobile developers with execution-ready patterns for building native and cross-platform mobile applications. Apply these patterns when you need iOS/Android app architecture, UI components, navigation flows, API integration, offline storage, authentication, or mobile-specific features.

---

## When to Use This Skill

Use this skill when you need:

- iOS app development (Swift, SwiftUI, UIKit)
- Android app development (Kotlin, Jetpack Compose)
- Cross-platform development (React Native, WebView)
- Mobile app architecture and patterns
- Navigation and routing
- State management (Redux, MobX, MVVM)
- Network requests and API integration
- Local data storage (Core Data, Room, SQLite)
- Authentication and session management
- Push notifications (APNs, FCM)
- Camera and media access
- Location services
- App Store / Play Store deployment
- Mobile performance optimization
- Offline-first architecture
- Deep linking and universal links

---

## Quick Reference Table

| Task | iOS | Android | Cross-Platform | When to Use |
|------|-----|---------|----------------|-------------|
| Native UI | SwiftUI + UIKit | Jetpack Compose + Views | React Native | Native: Best performance; Cross-platform: Code sharing |
| Navigation | NavigationStack | Navigation Component | React Navigation | Platform-specific for native feel |
| State Management | @State/@Observable | ViewModel + StateFlow | Redux/MobX | iOS: @Observable; Android: ViewModel; RN: Redux |
| Networking | URLSession + async/await | Retrofit + Coroutines | Axios/Fetch | Native: Type-safe; RN: JavaScript ecosystem |
| Local Storage | Core Data + SwiftData | Room Database | AsyncStorage/SQLite | Native: Full control; RN: Simpler |
| Push Notifications | APNs | FCM | React Native Firebase | Native: Platform-specific; RN: Unified API |
| Background Tasks | BGTaskScheduler | WorkManager | Headless JS | For scheduled/background work |
| Deep Linking | Universal Links | App Links | React Navigation linking | For URL-based app entry |
| Authentication | AuthenticationServices | Credential Manager | Expo AuthSession | For social/biometric auth |
| Analytics | Firebase/Amplitude | Firebase/Amplitude | Expo Analytics | Track user behavior |

---

## Decision Tree: Platform Selection

```text
Need to build mobile app for: [Target Audience]
    │
    ├─ iOS only?
    │   ├─ New app? → SwiftUI (modern, declarative)
    │   ├─ Existing UIKit codebase? → UIKit + incremental SwiftUI adoption
    │   └─ Complex animations? → UIKit for fine-grained control
    │
    ├─ Android only?
    │   ├─ New app? → Jetpack Compose (modern, declarative)
    │   ├─ Existing Views codebase? → Views + incremental Compose adoption
    │   └─ Complex custom views? → Custom View for fine-grained control
    │
    ├─ Both iOS and Android?
    │   ├─ Need maximum performance / platform fidelity?
    │   │   └─ Build separate native apps (Swift + Kotlin)
    │   │
    │   ├─ Need faster development + code sharing (70%+)?
    │   │   ├─ JavaScript team? → React Native
    │   │   ├─ Dart team? → Flutter
    │   │   └─ Kotlin team? → Kotlin Multiplatform
    │   │
    │   └─ Wrapping existing web app?
    │       ├─ Simple wrapper? → WebView (iOS WKWebView / Android WebView)
    │       └─ Native features needed? → Capacitor or React Native WebView
    │
    └─ Prototype/MVP only?
        └─ React Native or Flutter for fastest iteration
```

## Decision Tree: Architecture Pattern

```text
Choosing architecture pattern?
    │
    ├─ iOS (Swift)?
    │   ├─ SwiftUI app? → MVVM with @Observable
    │   ├─ UIKit app? → MVVM-C (Coordinator pattern)
    │   ├─ Large team? → Clean Architecture + MVVM
    │   └─ Simple app? → MVC (Apple default)
    │
    ├─ Android (Kotlin)?
    │   ├─ Compose app? → MVVM with ViewModel + StateFlow
    │   ├─ Views app? → MVVM with LiveData
    │   ├─ Large team? → Clean Architecture + MVVM
    │   └─ Simple app? → Activity/Fragment-based
    │
    └─ React Native?
        ├─ Small app? → Context API + useState
        ├─ Medium app? → Redux Toolkit or Zustand
        └─ Large app? → Redux + RTK Query + feature-based structure
```

## Decision Tree: Data Persistence

```text
Need to store data locally?
    │
    ├─ Simple key-value pairs?
    │   ├─ iOS → UserDefaults
    │   ├─ Android → SharedPreferences / DataStore
    │   └─ RN → AsyncStorage
    │
    ├─ Structured data with relationships?
    │   ├─ iOS → Core Data or SwiftData
    │   ├─ Android → Room Database
    │   └─ RN → WatermelonDB or Realm
    │
    ├─ Secure credentials?
    │   ├─ iOS → Keychain
    │   ├─ Android → EncryptedSharedPreferences / Keystore
    │   └─ RN → react-native-keychain
    │
    └─ Large files/media?
        ├─ iOS → FileManager (Documents/Cache)
        ├─ Android → Internal/External Storage
        └─ RN → react-native-fs
```

## Decision Tree: Networking

```text
Need to make API calls?
    │
    ├─ iOS?
    │   ├─ Simple REST? → URLSession + async/await
    │   ├─ Complex API? → URLSession + Codable
    │   └─ GraphQL? → Apollo iOS
    │
    ├─ Android?
    │   ├─ Simple REST? → Retrofit + Coroutines
    │   ├─ Complex API? → Retrofit + OkHttp interceptors
    │   └─ GraphQL? → Apollo Android
    │
    └─ React Native?
        ├─ Simple REST? → fetch() or Axios
        ├─ Complex API? → RTK Query or React Query
        └─ GraphQL? → Apollo Client
```

---

## Core Capabilities

### iOS Development

- **UI Frameworks**: SwiftUI (declarative), UIKit (imperative)
- **Architecture**: MVVM, Clean Architecture, Coordinator
- **Concurrency**: async/await, Combine, GCD
- **Storage**: Core Data, SwiftData, Keychain
- **Networking**: URLSession, async/await patterns
- **Platform compliance**: Privacy manifests + required-reason APIs, background execution limits, and accessibility settings (Dynamic Type, VoiceOver)
- **Defensive Decoding**: Handle missing fields, array/dict formats, snake_case/camelCase

### Android Development

- **UI Frameworks**: Jetpack Compose (declarative), Views (XML)
- **Architecture**: MVVM, Clean Architecture, MVI
- **Concurrency**: Coroutines, Flow, LiveData
- **Storage**: Room, DataStore, Keystore
- **Networking**: Retrofit, OkHttp, Ktor

### Cross-Platform Development

- **React Native**: JavaScript/TypeScript, native modules
- **Flutter**: Dart, widget tree, platform channels
- **WebView**: WKWebView (iOS), WebView (Android), JavaScript bridge

---

## Platform Baselines (Dec 2025)

### iOS/iPadOS (Core)

- Privacy manifest files (app + embedded SDKs) are maintained and reviewed https://developer.apple.com/documentation/bundleresources/privacy_manifest_files
- Required-reason APIs are declared with valid reasons https://developer.apple.com/documentation/bundleresources/privacy_manifest_files
- Background work uses supported primitives (avoid fragile timers) https://developer.apple.com/documentation/backgroundtasks
- App Transport Security is configured; exceptions are justified and documented https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity

### Android (Core)

- Background work uses WorkManager for deferrable, guaranteed work https://developer.android.com/topic/libraries/architecture/workmanager
- Network calls and auth state survive process death (no hidden singleton assumptions) [Inference]
- Target SDK meets Google Play requirements (plan upgrades early) https://support.google.com/googleplay/android-developer/answer/11926878

### Cross-Platform (Core)

- Feature parity is explicit (document what is native-only vs shared) [Inference]
- Bridges are treated as public APIs (versioned, tested, and observable) [Inference]

### Optional: AI/Automation Extensions

> **Note**: Skip unless the app ships AI/automation features.

- iOS: Apple Foundation Models (on-device) https://developer.apple.com/documentation/foundationmodels
- Android: Google ML Kit https://developers.google.com/ml-kit
- Verify: model size/battery impact, offline/online behavior, user controls (cancel/undo), and privacy boundaries [Inference]

---

## Common Patterns

### App Startup Checklist

1. **Initialize dependencies**
   - Configure DI container (Hilt/Koin/Swinject)
   - Set up logging and crash reporting
   - Initialize analytics

2. **Check authentication state**
   - Validate stored tokens
   - Refresh if needed
   - Route to login or main screen

3. **Configure app state**
   - Load user preferences
   - Set up push notification handlers
   - Initialize deep link handling

### Offline-First Architecture

```text
1. Local-first data access
   - Always read from local database
   - Display cached data immediately
   - Show loading indicator for sync

2. Background sync
   - Queue write operations
   - Sync when connectivity available
   - Handle conflict resolution

3. Optimistic updates
   - Update UI immediately
   - Sync in background
   - Rollback on failure
```

### Push Notification Setup

```text
iOS (APNs):
1. Enable Push Notifications capability
2. Request user permission
3. Register for remote notifications
4. Handle device token
5. Implement notification delegate

Android (FCM):
1. Add Firebase to project
2. Implement FirebaseMessagingService
3. Handle notification/data messages
4. Manage notification channels (Android 8+)
5. Handle background/foreground states
```

---

## Performance Optimization

| Area | iOS | Android | Metric |
|------|-----|---------|--------|
| Launch time | Pre-warm, lazy loading | Cold start optimization | < 2s cold start |
| List scrolling | LazyVStack, prefetch | LazyColumn, paging | 60 FPS |
| Image loading | AsyncImage, cache | Coil/Glide, disk cache | < 100ms visible |
| Memory | Instruments profiling | LeakCanary, Profiler | No memory leaks |
| Battery | Background App Refresh limits | Doze mode compliance | Minimal drain |

---

## App Store Deployment Checklist

### iOS App Store

- [ ] App icons (all required sizes)
- [ ] Launch screen configured
- [ ] Privacy manifest per target and embedded frameworks (iOS 18+)
- [ ] Required-reason APIs declared with justifications
- [ ] Third-party SDK privacy manifests attached; SDK signature attestation (iOS 19+)
- [ ] Info.plist permissions explanations
- [ ] App Store screenshots (all device sizes)
- [ ] App Store description and keywords
- [ ] Privacy policy URL
- [ ] TestFlight beta testing

### Google Play Store

- [ ] App icons and feature graphic
- [ ] Store listing screenshots
- [ ] Privacy policy URL
- [ ] Content rating questionnaire
- [ ] Target API level compliance
- [ ] Data safety form
- [ ] Internal/closed/open testing tracks

---

## Navigation

### Resources

- [resources/ios-best-practices.md](resources/ios-best-practices.md) — iOS architecture, concurrency, testing, performance, defensive decoding, and accessibility
- [resources/android-best-practices.md](resources/android-best-practices.md) — Android/Kotlin architecture, coroutines, Compose, testing, performance
- [resources/operational-playbook.md](resources/operational-playbook.md) — Mobile architecture patterns, platform-specific guides, security notes, and decision tables
- [README.md](README.md) — Folder overview and usage notes
- [data/sources.json](data/sources.json) — Curated external references by platform

### Shared Checklists

- [../software-clean-code-standard/templates/checklists/mobile-release-checklist.md](../software-clean-code-standard/templates/checklists/mobile-release-checklist.md) — Product-agnostic mobile release readiness checklist (core + optional AI)

### Shared Utilities (Centralized patterns — extract, don't duplicate)

- [../software-clean-code-standard/utilities/auth-utilities.md](../software-clean-code-standard/utilities/auth-utilities.md) — Argon2id, jose JWT, OAuth 2.1/PKCE (backend auth for mobile clients)
- [../software-clean-code-standard/utilities/error-handling.md](../software-clean-code-standard/utilities/error-handling.md) — Error patterns, Result types
- [../software-clean-code-standard/utilities/resilience-utilities.md](../software-clean-code-standard/utilities/resilience-utilities.md) — Retry, circuit breaker for network calls
- [../software-clean-code-standard/utilities/logging-utilities.md](../software-clean-code-standard/utilities/logging-utilities.md) — Structured logging patterns
- [../software-clean-code-standard/utilities/testing-utilities.md](../software-clean-code-standard/utilities/testing-utilities.md) — Test factories, fixtures, mocks
- [../software-clean-code-standard/resources/clean-code-standard.md](../software-clean-code-standard/resources/clean-code-standard.md) — Canonical clean code rules (`CC-*`) for citation

### Templates

- **Swift**: [templates/swift/template-swift.md](templates/swift/template-swift.md), [templates/swift/template-swift-concurrency.md](templates/swift/template-swift-concurrency.md), [templates/swift/template-swift-combine.md](templates/swift/template-swift-combine.md), [templates/swift/template-swift-performance.md](templates/swift/template-swift-performance.md), [templates/swift/template-swift-testing.md](templates/swift/template-swift-testing.md)
- **SwiftUI**: [templates/swiftui/template-swiftui-advanced.md](templates/swiftui/template-swiftui-advanced.md)
- **Kotlin/Android**: [templates/kotlin/template-kotlin.md](templates/kotlin/template-kotlin.md), [templates/kotlin/template-kotlin-coroutines.md](templates/kotlin/template-kotlin-coroutines.md), [templates/kotlin/template-kotlin-compose-advanced.md](templates/kotlin/template-kotlin-compose-advanced.md), [templates/kotlin/template-kotlin-testing.md](templates/kotlin/template-kotlin-testing.md)
- **Cross-platform**: [templates/cross-platform/template-platform-patterns.md](templates/cross-platform/template-platform-patterns.md), [templates/cross-platform/template-webview.md](templates/cross-platform/template-webview.md)

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Blocking main thread | UI freezes, ANRs | Use async/coroutines for all I/O |
| Massive view controllers | Hard to test/maintain | Extract to MVVM/services |
| Hardcoded strings | No localization | Use NSLocalizedString/strings.xml |
| Ignoring lifecycle | Memory leaks, crashes | Respect activity/view lifecycle |
| No offline handling | Poor UX without network | Cache data, queue operations |
| Storing secrets in code | Security vulnerability | Use Keychain/Keystore |
| Using `decode()` without fallback | Crashes on missing/malformed API data | Use `decodeIfPresent()` with defaults |
| Missing @Bindable for @Observable | NavigationStack bindings don't work | Add `@Bindable var vm = vm` in body |

---

## Related Skills

- [../software-frontend/SKILL.md](../software-frontend/SKILL.md) — Web-facing UI patterns and Next.js integration
- [../software-backend/SKILL.md](../software-backend/SKILL.md) — API design, auth, and backend contracts for mobile clients
- [../qa-testing-strategy/SKILL.md](../qa-testing-strategy/SKILL.md) — Mobile CI, test strategy, and reliability gates
- [../qa-resilience/SKILL.md](../qa-resilience/SKILL.md) — Resilience patterns for networked mobile apps
- [../qa-testing-ios/SKILL.md](../qa-testing-ios/SKILL.md) — iOS-focused test planning, XCTest/Swift Testing patterns, device matrix, and app health checks
- [../software-ui-ux-design/SKILL.md](../software-ui-ux-design/SKILL.md) — Mobile UI/UX design patterns and accessibility
