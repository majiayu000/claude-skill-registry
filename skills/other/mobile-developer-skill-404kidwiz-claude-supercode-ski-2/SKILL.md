---
name: mobile-developer
description: Expert in pure native development (Swift/Kotlin) for iOS and Android, maximizing platform capabilities and performance.
---

# Native Mobile Developer

## Purpose

Provides native mobile development expertise specializing in Swift (iOS) and Kotlin (Android). Builds platform-native applications maximizing device capabilities, performance, and OS features like Dynamic Island, Widgets, and Foldables.

## When to Use

- Building high-fidelity apps requiring 100% native performance
- Implementing complex background services (Location tracking, Audio processing)
- Developing SDKs or native modules for React Native/Flutter
- Integrating heavily with system APIs (Siri, Shortcuts, HealthKit, Wallet)
- Requiring zero-dependency architectures (Banking, Medical apps)
- Adopting bleeding-edge OS features day-one (iOS 18 APIs)

---
---

## 2. Decision Framework

### Native vs. KMP vs. Cross-Platform

```
Architecture Choice?
│
├─ **Pure Native (Swift/Kotlin)**
│  ├─ Needs deep system integration? → **Yes** (Best access)
│  ├─ Zero compromise UX? → **Yes** (Standard platform behavior)
│  └─ Team size? → **Large** (Requires separate iOS/Android teams)
│
├─ **Kotlin Multiplatform (KMP)**
│  ├─ Share business logic only? → **Yes** (Shared Domain/Data layer)
│  ├─ Native UI required? → **Yes** (SwiftUI on iOS, Compose on Android)
│  └─ Existing native app? → **Yes** (Good for migration)
│
└─ **Cross-Platform (RN/Flutter)**
   ├─ UI consistency priority? → **Yes** (Same UI on both)
   └─ Single codebase priority? → **Yes**
```

### UI Framework Selection

| Platform | Framework | State of Tech (2026) | Recommendation |
|----------|-----------|----------------------|----------------|
| **iOS** | **SwiftUI** | Mature, Default choice | **Use for 95% of new apps.** Fallback to UIKit only for complex custom gestures/legacy. |
| **iOS** | **UIKit** | Legacy, Stable | Maintenance only, or wrapping old libs. |
| **Android** | **Jetpack Compose** | Standard, Default | **Use for 100% of new apps.** XML is legacy. |
| **Android** | **XML / View** | Legacy | Maintenance only. |

### Concurrency Model

| Platform | Model | Best Practice |
|----------|-------|---------------|
| **iOS** | **Swift Concurrency** | `async/await`, `Actors` for thread safety. Avoid GCD/closures. |
| **Android** | **Kotlin Coroutines** | `suspend` functions, `Flow` for streams. `Dispatchers.IO` for work. |

**Red Flags → Escalate to `mobile-app-developer` (Cross-platform):**
- Client has budget for only 1 developer but wants 2 apps
- App is a simple form-based utility with no device hardware usage
- Timeline is < 4 weeks for dual-platform launch

---
---

## 3. Core Workflows

### Workflow 1: Modern iOS Architecture (SwiftUI + MVVM)

**Goal:** Build a scalable iOS app using Swift 6 concurrency and SwiftUI.

**Steps:**

1.  **Project Setup**
    -   Target: iOS 17.0+ (Aggressive adoption for modern APIs).
    -   Swift Strict Concurrency Checking: `Complete`.

2.  **ViewModel Definition (Observable)**
    ```swift
    import SwiftUI
    import Observation

    @Observable
    class ProductListViewModel {
        var products: [Product] = []
        var isLoading = false
        var error: Error?

        private let service: ProductService

        init(service: ProductService = .live) {
            self.service = service
        }

        func loadProducts() async {
            isLoading = true
            defer { isLoading = false }
            
            do {
                products = try await service.fetchProducts()
            } catch {
                self.error = error
            }
        }
    }
    ```

3.  **View Implementation**
    ```swift
    struct ProductListView: View {
        @State private var viewModel = ProductListViewModel()

        var body: some View {
            NavigationStack {
                List(viewModel.products) { product in
                    ProductRow(product: product)
                }
                .overlay {
                    if viewModel.isLoading { ProgressView() }
                }
                .task {
                    await viewModel.loadProducts()
                }
                .navigationTitle("Products")
            }
        }
    }
    ```

---
---

### Workflow 3: Kotlin Multiplatform (KMP) Setup

**Goal:** Share networking and database logic between iOS and Android.

**Steps:**

1.  **Shared Module Structure**
    ```
    shared/
      src/commonMain/kotlin/  # Shared logic
      src/androidMain/kotlin/ # Android specific
      src/iosMain/kotlin/     # iOS specific
    ```

2.  **Networking (Ktor)**
    ```kotlin
    // commonMain
    class ApiClient {
        private val client = HttpClient {
            install(ContentNegotiation) {
                json(Json { ignoreUnknownKeys = true })
            }
        }

        suspend fun getData(): Data = client.get("...").body()
    }
    ```

3.  **Consumption**
    -   **Android:** Call `ApiClient().getData()` directly in ViewModel.
    -   **iOS:** Call `ApiClient().getData()` via Swift interop (wrapper may be needed for `async/await` bridging if older Kotlin version).

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: "Massive View Controller" (MVC)

**What it looks like:**
-   3,000 line `ViewController.swift` files containing networking, logic, and UI code.

**Why it fails:**
-   Untestable.
-   Impossible to maintain.

**Correct approach:**
-   Use **MVVM** (Model-View-ViewModel) or **TCA** (The Composable Architecture) on iOS.
-   Use **MVI** (Model-View-Intent) or **MVVM** on Android.
-   Separate Logic from UI entirely.

### ❌ Anti-Pattern 2: Ignoring Lifecycle Events

**What it looks like:**
-   Starting a network request in `onAppear` but not cancelling it on `onDisappear`.
-   Assuming the app always starts from scratch (ignoring process death on Android).

**Why it fails:**
-   Memory leaks.
-   Crashes when background tasks try to update UI that no longer exists.
-   Data loss when Android kills the app to save memory.

**Correct approach:**
-   Use structured concurrency (`.task` in SwiftUI cancels auto).
-   Use `SavedStateHandle` in Android ViewModels to persist state across process death.

### ❌ Anti-Pattern 3: Blocking the Main Thread

**What it looks like:**
-   Decoding JSON or filtering a large list on the Main/UI thread.
-   Dropped frames (jank).

**Why it fails:**
-   App becomes unresponsive (ANR on Android).
-   Watchdog kills the app.

**Correct approach:**
-   **Always** move heavy work to background dispatchers (`Dispatchers.Default` / `Task.detached`).

---
---

## Examples

### Example 1: Enterprise Banking App Development

**Scenario:** Build a secure, compliant banking app for iOS and Android with biometric authentication.

**Development Approach:**
1. **Architecture**: Clean Architecture with MVVM
2. **Authentication**: Face ID/Touch ID integration with secure enclave
3. **Networking**: Certificate pinning with retry logic
4. **Offline Support**: Local encryption with periodic sync

**Implementation Highlights:**
```swift
// iOS Biometric Authentication
func authenticateWithBiometrics() async throws {
    let context = LAContext()
    var error: NSError?
    
    guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
        throw AuthenticationError.biometricsNotAvailable
    }
    
    do {
        let success = try await context.evaluatePolicy(
            .deviceOwnerAuthenticationWithBiometrics,
            reason: "Authenticate to access your account"
        )
        guard success else { throw AuthenticationError.authenticationFailed }
    } catch {
        throw AuthenticationError.authenticationFailed
    }
}
```

**Results:**
- Released on both App Store and Play Store
- 500,000+ downloads in first month
- 4.9-star rating on both platforms
- Zero security incidents in 2 years

### Example 2: Healthcare App with HIPAA Compliance

**Scenario:** Develop a patient management app with strict HIPAA compliance requirements.

**Compliance Implementation:**
1. **Data Encryption**: AES-256 encryption at rest
2. **Audit Logging**: Complete audit trail of all data access
3. **Session Management**: Auto-logout with configurable timeout
4. **Network Security**: TLS 1.3 with certificate pinning

**Android Implementation:**
```kotlin
// Encrypted SharedPreferences
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val encryptedPrefs = EncryptedSharedPreferences.create(
    context,
    "patient_data",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

// Usage
encryptedPrefs.edit().putString("patient_id", "12345").apply()
```

**Results:**
- HIPAA audit passed with zero critical findings
- Integrated with 15+ healthcare systems
- 99.9% uptime SLA achieved
- FDA-compliant for medical device classification

### Example 3: IoT Control App with BLE Integration

**Scenario:** Build a smart home control app integrating with IoT devices via Bluetooth Low Energy.

**BLE Implementation:**
1. **Device Discovery**: Background scanning with filters
2. **Connection Management**: Automatic reconnection with backoff
3. **Data Parsing**: Protocol buffer deserialization
4. **Offline Control**: Local command queue with sync

**Architecture:**
- SwiftUI for iOS, Jetpack Compose for Android
- Reactive state management with Combine/Flow
- Background processing for BLE operations
- Battery optimization with proper lifecycle handling

**Results:**
- Supports 50+ device types
- 50ms average response time
- 40% better battery life than competitors
- Featured in Apple Watch integration

## Best Practices

### Platform-Specific Development

- **iOS**: Leverage SwiftUI for modern apps, use UIKit for complex animations
- **Android**: Default to Compose, migrate from XML gradually
- **Navigation**: Use NavigationPath (iOS) and NavHost (Android)
- **State Management**: Observable (iOS), StateFlow (Android)

### Performance Optimization

- **Lazy Loading**: Defer image/resource loading until needed
- **Image Caching**: Implement with memory and disk cache
- **Memory Management**: Monitor memory pressure, use profiling tools
- **Battery Life**: Minimize background operations, use batched updates

### Security Implementation

- **Secure Storage**: Keychain (iOS), EncryptedSharedPreferences (Android)
- **Network Security**: Certificate pinning, TLS configuration
- **Input Validation**: Sanitize all user inputs
- **Code Obfuscation**: Enable ProGuard/R8 for release builds

### Testing Strategy

- **Unit Tests**: ViewModels, repositories, business logic
- **UI Tests**: Critical user flows and interactions
- **Integration Tests**: API calls, database operations
- **Performance Tests**: Startup time, memory usage, scrolling performance

### Distribution and Deployment

- **App Store**: Follow Apple review guidelines, prepare metadata
- **Play Store**: Optimize for Play Console features, testing tracks
- **Enterprise**: Implement enterprise distribution certificates
- **Updates**: Plan backward compatibility for major versions

## Quality Checklist

**Platform Standards:**
-   [ ] **iOS:** Supports Dynamic Type (text scaling).
-   [ ] **iOS:** Supports Dark Mode seamlessly.
-   [ ] **Android:** Handles configuration changes (rotation) without data loss.
-   [ ] **Android:** Back navigation stack works correctly.
-   [ ] **iOS:** Supports iPad with adaptive layouts.
-   [ ] **Android:** Supports different screen sizes and densities.

**Performance:**
-   [ ] **Scroll:** Lists scroll at 60fps/120fps.
-   [ ] **Memory:** No retain cycles (iOS) or leaked Activities (Android).
-   [ ] **Startup:** App is usable within 2 seconds.
-   [ ] **Network:** Efficient batching and caching.

**Architecture:**
-   [ ] **Separation:** UI code contains NO business logic.
-   [ ] **Dependency Injection:** Dependencies (API, DB) are injected, not instantiated directly.
-   [ ] **Testing:** Unit tests exist for all ViewModels/Interactors.
-   [ ] **Navigation:** Deep linking support implemented.

**Security:**
-   [ ] **Sensitive Data:** Stored in Keychain/Keystore, NOT UserDefaults/SharedPreferences.
-   [ ] **Networking:** SSL Pinning enabled for sensitive endpoints.
-   [ ] **Logs:** No PII printed to console in release builds.
-   [ ] **Authentication:** Biometric or secure authentication implemented.
-   [ ] **Compliance:** Meets platform guidelines (App Store/Play Store).
