---
name: "Shared SwiftUI App Workflow"
description: "End-to-end Xcode workflow for architecting, debugging, profiling, and shipping a shared SwiftUI app on iOS and macOS."
version: "1.0.0"
dependencies: []
tags:
  - xcode
  - swiftui
  - workflow
  - cicd
  - multiplatform
---

# Instructions

- **Overview:** This workflow outlines best practices to **build, test,
  and deploy** a SwiftUI app targeting both iOS and macOS (with an
  option for Catalyst). It covers project setup, architecture choices,
  development practices, and continuous delivery steps.
- **Prerequisites:** Ensure you have the latest Xcode installed (Xcode
  15 or newer) and are enrolled in the Apple Developer Program (required
  for code signing, Xcode Cloud, and TestFlight). Familiarity with
  SwiftUI, Git source control, and basic iOS/macOS app development is
  assumed.
- **Usage:** Follow the steps below in sequence to configure a
  multi-platform Xcode project, manage dependencies, implement an
  architecture (MVVM or TCA), debug and profile efficiently, set up
  CI/CD pipelines, and finally distribute the app via TestFlight.
- **Conventions:** This guide uses **bold titles** for key actions and
  *italics* for tool names or concepts. Replace example placeholders
  (like bundle identifiers or scheme names) with your own
  project-specific values when applying these steps.

# Workflow

1.  **Create a Multiplatform Xcode Project:** Begin by creating a new
    Xcode project that supports both iOS and macOS targets. Xcode 14+
    offers a **Multiplatform App** template, which sets up a single
    target capable of building for iOS (and iPadOS) and macOS using
    SwiftUI. This unified target shares most code and assets across
    platforms. If you prefer separate targets, you can instead create an
    iOS app and then add a macOS target (or enable Mac Catalyst for the
    iOS target). Ensure that shared code (like SwiftUI views and models)
    is grouped in a cross-platform group, and use platform checks
    (`#if os(iOS)`, `#if os(macOS)`) for any platform-specific code. By
    structuring the project as a **shared codebase**, you minimize
    duplication while still tailoring the UI where necessary for each
    device type.

2.  **Set Up Targets, Schemes, and Configurations:** With a
    multi-platform project, Xcode may already include separate
    configurations for Debug and Release. You might add custom **Build
    Configurations** (e.g. Staging or QA) if needed. If using separate
    targets (for Catalyst or environment flavors), give each target a
    unique **Bundle Identifier** and Info.plist. For example, suffix the
    bundle ID with \".mac\" for a macOS target or \".dev\" for a
    development build. Create corresponding **Schemes** for each app
    target or environment so you can easily run and archive each
    version. Mark schemes as "Shared" to include them in source control
    (important for team use and CI). This multi-target setup allows you
    to, for instance, have an iOS app, a native macOS app, and even a
    Catalyst app all in one project, each with its own scheme and bundle
    ID.

3.  **Configure Environment Settings:** Manage environment-specific
    settings by using Xcode's build configuration options. For example,
    you can define custom **XCConfig** files or use **User-Defined Build
    Settings** for values like API endpoints or feature flags. Define
    keys in Info.plist that reference these settings. For instance, add
    a key for `BaseURL` in your Info.plist and assign it a value like
    `$(BASE_URL)` which is set per configuration. In Build Settings,
    create a user-defined variable `BASE_URL` for each configuration
    (e.g. Dev, QA, Prod), each pointing to the appropriate URL. Your app
    can read these at runtime, for example:

<!-- -->

    let apiURL = Bundle.main.object(forInfoDictionaryKey: "BaseURL") as? String

This way, you avoid hardcoding environment values. Additionally,
consider using **Compiler Flags** for conditional code. In each
configuration's build settings, you might add Swift flags like
`-DDEVELOPMENT` or `-DPRODUCTION`. Then in Swift code, use
`#if DEVELOPMENT` to include debug-only logic or use placeholders for
testing. This approach keeps configuration differences isolated at build
time. Finally, ensure each app target uses distinct app icons and names
if needed (e.g. add suffix "Dev" to the app name for a development
build) -- you can set this via Info.plist or Asset catalogs per target.

1.  **Manage Dependencies (SPM and CocoaPods):** Use **Swift Package
    Manager (SPM)** as the primary tool for adding libraries and
    frameworks. SPM is built into Xcode, making dependency management
    seamless for SwiftUI projects. To add a package, go to **File ▸ Add
    Packages\...** and enter the package Git URL. Target the dependency
    to your app target (and not to any CocoaPods-generated target) so
    the package integrates correctly. SPM automatically fetches and
    updates packages and keeps them sandboxed within Xcode. Commit the
    `Package.resolved` file so that team members and CI use the same
    versions. If you need a library that isn't available via SPM (or
    contains significant Objective-C/legacy code), you can integrate
    **CocoaPods**. Initialize a Podfile (`pod init`) and specify pods,
    then run `pod install` to generate an `.xcworkspace`. Continue
    working from the workspace thereafter. It's possible to mix SPM and
    CocoaPods in one project -- just ensure that when adding SPM
    packages you select your main project in the add dialog (not the
    Pods project). Keep your Pod dependencies updated with `pod update`
    as needed. In general, prefer SPM for pure Swift dependencies due to
    its native Xcode support and ease of use, using CocoaPods only for
    exceptions. Maintain clear documentation of third-party packages in
    your README.

2.  **Apply an Architecture Pattern (MVVM or TCA):** Structure your
    SwiftUI code using a robust architecture to manage complexity. A
    popular choice is **MVVM (Model-View-ViewModel)**, which works
    naturally with SwiftUI's data binding. In MVVM, define your data
    models to represent app data, use SwiftUI Views for the UI, and
    create **ViewModel** classes (conforming to `ObservableObject`) to
    handle business logic and state. For example, a `GameViewModel`
    might publish a `@Published var score` and handle methods to update
    the score. The corresponding `GameView` uses `@StateObject` or
    `@ObservedObject` to watch the ViewModel and update the UI. This
    separation keeps the SwiftUI view declarative and lightweight, while
    logic lives in the ViewModel (making it easier to test). For larger
    apps or more complex state management, consider adopting **The
    Composable Architecture (TCA)**. TCA is a library (addable via SPM)
    that follows a unidirectional data flow (inspired by Redux). You
    break down your app into **State**, **Actions**, and **Reducers**. A
    Reducer is a pure function that takes the current State and an
    Action and produces a new State (and optionally, side effects known
    as Effects). A **Store** connects your SwiftUI View to the state and
    business logic: the View sends Actions (for example, button taps),
    which the Store receives and feeds into the Reducer, updating State
    which then flows back to the View. TCA encourages a very modular
    structure: you can compose small features into larger ones, and it
    provides tools to manage dependencies and side effects in a
    controlled way. While TCA has a learning curve, it excels in
    testability (you can easily write tests for reducer logic) and
    scalability for big apps. Choose either MVVM (simpler, uses
    SwiftUI's built-in reactive state features) or TCA (more structured,
    ideal for complex apps) depending on project needs -- both will help
    maintain a clear separation of concerns in your code.

3.  **Debugging and Profiling Practices:** During development, use
    Xcode's robust debugging tools to catch and fix issues early. Set
    **breakpoints** in your code (by clicking the gutter next to a line
    number) to pause execution and inspect variables at runtime. While
    paused, use the **LLDB console** (`po` command) to print out values
    or call functions to verify state. This is invaluable for logic in
    ViewModels or TCA reducers where you want to ensure the correct data
    flow. For SwiftUI views, the **View Hierarchy Debugger** is
    extremely useful: run your app in Simulator and choose **Debug ▸
    View Debugging ▸ Capture View Hierarchy**. This lets you inspect the
    UI layout after a pause, so you can pinpoint why a view might not
    appear or is misplaced. Additionally, leverage **Instruments** for
    profiling. Xcode's Instruments app offers templates like **Time
    Profiler** (to measure CPU performance and find slow functions) and
    **Leaks** (to detect memory leaks and retain cycles). For example,
    if a SwiftUI view is laggy, run Time Profiler while interacting with
    it to identify expensive computations. SwiftUI in Xcode 15+ also
    includes a dedicated "SwiftUI" animation and rendering timeline
    instrument to analyze UI performance. Always test and profile in
    **Release mode** periodically as well, since SwiftUI performance can
    differ between Debug and Release builds. Use **os_log** or print
    statements for lightweight debugging, especially to trace execution
    paths or data changes (just be sure to remove or disable noisy logs
    in production). By regularly debugging and profiling throughout
    development, you ensure the app runs smoothly and catches bugs
    before release.

4.  **Write Unit and UI Tests:** Set up automated tests to maintain code
    quality. Xcode can generate a Unit Test target and a UI Test target
    when you create the project (you can also add them manually via
    **File ▸ New ▸ Target** if not present). **Unit Tests** (using the
    XCTest framework) should cover your core business logic. For MVVM,
    test your ViewModel methods and state changes independently of the
    UI. For TCA, you can leverage the TCA testing utilities to send
    actions to your reducers and assert on state changes or effect
    outputs. Aim to test edge cases and error conditions (e.g., if a
    network call fails, the ViewModel should present an error state).
    **UI Tests** use Xcode's UI Testing framework (built on XCTest) to
    launch the app and simulate user interaction. You can record UI test
    scripts by interacting with the app in the simulator, which
    generates code for taps and swipes, or write them manually for more
    control. Focus UI tests on critical flows, such as onboarding or a
    purchase flow -- things that must work perfectly. Use assertions to
    verify that expected elements appear or that navigating to a certain
    screen is successful. Keep tests organized in groups and use
    descriptive test method names. It's also helpful to run tests under
    different configurations (Xcode's Test Plans can run a suite in
    multiple schemes or environments). By automating testing, you can
    catch regressions quickly and ensure new changes don't break
    existing functionality. Make sure to run the test suite regularly
    during development, and definitely include test execution as part of
    your CI pipelines.

5.  **Continuous Integration with Xcode Cloud:** To streamline building
    and testing, set up **Xcode Cloud** if you host your code in a
    supported git repository (GitHub, Bitbucket, GitLab, etc.). Xcode
    Cloud is Apple's integrated CI service that can automatically build
    your app on Apple's servers. To configure it, open your project in
    Xcode, navigate to the Xcode Cloud settings (in the Report Navigator
    or via Product ▸ Xcode Cloud) and enable a new workflow. Choose a
    repository branch (e.g. main) and select actions like **build**,
    **analyze**, **test**, and **archive**. You can specify triggers --
    for example, run on every push, or only on pull requests. Xcode
    Cloud will handle provisioning by linking with your Apple Developer
    account; it can manage certificates and profiles for cloud builds
    seamlessly if set to automatic signing. Add all your schemes that
    need building/testing to the workflow (for instance, include both
    iOS and macOS app schemes, and the test targets). Xcode Cloud
    provides a simple web interface (or within Xcode) to monitor build
    status and view logs or test results. You can also configure it to
    automatically distribute successful builds to TestFlight (see step
    10). One advantage of Xcode Cloud is deep integration: it uses the
    same environment as local Xcode, and can run parallel tests on
    multiple devices. Keep an eye on your Xcode Cloud minutes usage
    (Apple provides some free tier, but heavy usage might require a
    subscription). For team projects, Xcode Cloud ensures everyone's
    changes are continuously validated. It's a great set-and-forget CI
    for Apple platform apps, as long as your project is configured
    properly.

6.  **Continuous Integration with GitHub Actions:** As an alternative or
    in addition to Xcode Cloud, you can use **GitHub Actions** to set up
    CI/CD, which offers more customization. Create a workflow YAML (e.g.
    `.github/workflows/ci.yml`) in your repository. Use a **macOS
    runner** (e.g. `runs-on: macos-latest`) to build iOS/macOS apps. A
    typical job installs dependencies, builds the app, runs tests, and
    archives the app artifact. For example, include steps to check out
    code (`actions/checkout`), set up any required Ruby or Node
    environment (if using tools like Fastlane or CocoaPods), then run
    **Xcode build commands**. You can use `xcodebuild` in command-line
    mode to build and test:

<!-- -->

    - name: Build and Test (iOS)
      run: xcodebuild -workspace YourApp.xcworkspace -scheme "YourApp-iOS" -configuration Debug -sdk iphonesimulator -destination 'platform=iOS Simulator,name=iPhone 14' clean test

The above sample command builds the iOS scheme and runs tests on a
simulator. Similarly, you could build the macOS scheme by specifying the
scheme and destination as a Mac. If you have CocoaPods, remember to run
`pod install` before building. Save build artifacts if needed (Xcode
produces an archive `.xcarchive` and you can export an `.ipa` for iOS).
Using GitHub Secrets, you can store your distribution signing
certificate (as a Base64 .p12 file) and provisioning profile, as well as
App Store Connect API keys or an app-specific password. Then use a step
to install the certificate into the Keychain and environment variables
for signing. Many teams integrate **Fastlane** into GitHub Actions to
simplify code signing and uploading. For instance, after building, call
`fastlane deliver` or a custom lane to upload to TestFlight (Fastlane
can use the API key for App Store Connect to authenticate). There are
also community GitHub Actions (such as
`apple-actions/app-store-connect`) for uploading binaries to TestFlight.
Ensure your workflow runs on pull requests and merges to main, so that
every change is validated. With GitHub Actions, you have full control to
incorporate additional checks (like linting, SwiftLint, etc.) or
parallelize across matrix of devices/OS versions. It's a flexible
complement or alternative to Xcode Cloud, especially if you prefer
storing the CI config as code in your repo.

1.  **Manage Code Signing and Provisioning:** Code signing is required
    for running on devices and distributing via TestFlight/App Store.
    Throughout development, Xcode's automatic signing can be enabled for
    each target -- this ties the project to your Apple Developer Team
    and will create the necessary certificates and provisioning profiles
    for Debug and Release builds. Ensure each app target's **Signing &
    Capabilities** has a team selected and a unique bundle identifier.
    For distribution (TestFlight/App Store), you need an **iOS
    Distribution certificate** and an **App Store provisioning profile**
    for each app target. Xcode can create these if automatic signing is
    on and the project's archive build is set to "Any iOS Device" (for
    iOS) or "Any Mac" (for Mac apps). When using CI outside Xcode (like
    GitHub Actions), you'll need to supply signing materials: export
    your Distribution certificate as a `.p12` file and download the
    provisioning profile (.mobileprovision) from Apple Developer portal.
    Store these securely (environment secrets or keychain in CI) and
    have scripts or Fastlane import them during the build. A recommended
    approach is to use **Fastlane Match** or **codemagic/xcodesign** to
    manage signing identities in a secure, automated way. Also generate
    an **App Store Connect API Key** (in App Store Connect \> Users and
    Access \> Keys) if you plan to upload builds via API (used by CI
    tools and Fastlane). Keep the key ID, issuer ID, and the private key
    file secure; these allow CI to authenticate to App Store Connect
    without requiring your Apple ID credentials. In summary, set up
    signing early and test that you can archive and export the app
    locally. This ensures that when CI tries to do the same, the process
    is smooth. Maintaining consistent bundle IDs, provisioning profiles,
    and entitlements across local and CI environments is critical.

2.  **Deploy to TestFlight:** Once you have a signed archive build (an
    *.xcarchive*), the next step is distributing it to testers.
    **TestFlight** is Apple's beta distribution platform integrated with
    App Store Connect. If using Xcode locally, go to **Product ▸
    Archive**, then in the Organizer choose **Distribute App** → **App
    Store Connect** → **Upload**. Xcode will handle the upload to
    TestFlight (you'll need to increment the app version or build number
    each time). For CI-based uploads, use either Xcode's command-line
    tools or Fastlane. With Xcode command line, after archiving you can
    export an IPA using `xcodebuild -exportArchive` (with an export
    options plist), then upload with Apple's **altool** or the newer
    **Transporter** CLI. Fastlane simplifies this via `fastlane pilot`
    (for TestFlight) or `fastlane upload_to_testflight`. In Xcode Cloud,
    enabling the "Upload to TestFlight" action in your workflow will
    automatically push the archive to App Store Connect once the cloud
    build succeeds. After the upload, App Store Connect will process the
    build (this can take a few minutes). You can then log in to App
    Store Connect to manage testers and send out the build to your
    internal or external tester groups. It's good practice to annotate
    what changes are in the build (TestFlight release notes) for your
    testers. With CI/CD, you might choose to deploy every commit to an
    internal TestFlight group for rapid iteration, and then promote
    certain builds to external testers or App Store submission. Finally,
    always monitor the TestFlight build for any **critical issues**
    flagged by Apple (like crashes or missing compliance info) -- you'll
    be notified in App Store Connect if something needs addressing. Once
    a build is verified through testing, you can use it to submit the
    app to the App Store for review.

# Examples

- **GitHub Actions CI Workflow (Excerpt):** The following is a
  simplified example of a GitHub Actions workflow file for an iOS app
  that installs dependencies, builds, tests, and uploads a TestFlight
  build. It demonstrates how to use Xcode command-line tools and
  Fastlane in CI:

<!-- -->

    name: CI-iOS-TestFlight
    on:
      push:
        branches: [ main ]
    jobs:
      build-test-deploy:
        runs-on: macos-latest
        steps:
          - name: Checkout code
            uses: actions/checkout@v3

          - name: Install CocoaPods dependencies
            run: pod install
            continue-on-error: true  # Only if using CocoaPods

          - name: Build and Run Unit Tests (iOS)
            run: xcodebuild clean test -workspace YourApp.xcworkspace -scheme "YourApp-iOS" -sdk iphonesimulator -configuration Debug -destination 'platform=iOS Simulator,name=iPhone 14,OS=latest'

          - name: Archive App for Distribution
            run: xcodebuild clean archive -workspace YourApp.xcworkspace -scheme "YourApp-iOS" -configuration Release -destination 'generic/platform=iOS' -archivePath ${{ github.workspace }}/YourApp.xcarchive

          - name: Export .ipa from Archive
            run: xcodebuild -exportArchive -archivePath ${{ github.workspace }}/YourApp.xcarchive -exportOptionsPlist ExportOptions.plist -exportPath ${{ github.workspace }}/build

          - name: Install Fastlane
            run: gem install fastlane

          - name: Upload to TestFlight
            env:
              APP_STORE_CONNECT_API_KEY_ID: ${{ secrets.ASC_KEY_ID }}
              APP_STORE_CONNECT_API_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
              APP_STORE_CONNECT_API_KEY: ${{ secrets.ASC_KEY }}
            run: fastlane pilot upload -u ${{ secrets.APP_STORE_CONNECT_EMAIL }} -ipa ${{ github.workspace }}/build/YourApp.ipa --api_key_path ./ApiKeyFile.p8

In this YAML, the workflow triggers on pushes to the main branch. It
checks out the repository, installs pods (if applicable), then builds
and tests the app on an iOS simulator. Next it archives the app and
exports an IPA using an ExportOptions.plist (which would specify method
\"app-store\" and the provisioning profile). Finally, it uses Fastlane
Pilot to upload the IPA to TestFlight using App Store Connect API key
credentials stored in GitHub Secrets. This example can be extended with
additional jobs or steps for Mac builds, code linting, etc., and
illustrates how CI can fully automate the build and deploy process.

- **MVVM ViewModel Example (SwiftUI):** Below is a brief example of a
  SwiftUI view and a ViewModel following the MVVM pattern. It shows how
  a view model drives the UI state and handles logic, which could then
  be unit-tested independently of the view:

<!-- -->

    import SwiftUI
    import Combine

    // Model
    struct Game {
        var score: Int
    }

    // ViewModel
    class GameViewModel: ObservableObject {
        @Published var game: Game
        private var cancellables = Set<AnyCancellable>()

        init(game: Game = Game(score: 0)) {
            self.game = game
        }

        func increaseScore() {
            game.score += 1
        }

        func resetScore() {
            game.score = 0
        }
    }

    // View
    struct GameView: View {
        @StateObject private var viewModel = GameViewModel()

        var body: some View {
            VStack {
                Text("Score: \(viewModel.game.score)")
                    .font(.largeTitle)
                HStack {
                    Button("Increase") {
                        viewModel.increaseScore()
                    }
                    Button("Reset") {
                        viewModel.resetScore()
                    }
                }
            }
            .padding()
        }
    }

In this example, `GameViewModel` is an `ObservableObject` that manages
the state (the `Game` model). The SwiftUI `GameView` uses `@StateObject`
to instantiate and observe the ViewModel. Tapping the \"Increase\"
button calls a ViewModel method to update the score; thanks to
`@Published`, the view reflects the change automatically. This
architecture cleanly separates UI from logic: we can write unit tests
for `GameViewModel.increaseScore()` and `resetScore()` to ensure they
behave correctly without involving SwiftUI at all. The view simply
renders based on the current state. This pattern scales up such that for
each screen or component, you have a corresponding ViewModel (and
possibly service/model layers), making the app more maintainable and
testable.

# References

- Apple Developer Documentation -- **Multiplatform Apps:** Guide on
  configuring a single Xcode target for iOS and macOS, and sharing code
  between platforms.
- Apple Developer Documentation -- **Xcode Cloud:** Overview of setting
  up Xcode Cloud workflows for continuous integration and delivery of
  apps (build, test, deploy with TestFlight).
- Apple Developer Documentation -- **TestFlight Distribution:**
  Instructions for archiving an app and uploading builds to TestFlight
  via Xcode or CI tools.
- **Pointfree (Composable Architecture):** Official GitHub repository
  and documentation for The Composable Architecture (TCA) library,
  including guides on integrating it into SwiftUI projects.
- **XCTest Framework Reference:** Apple's reference for writing unit and
  UI tests with XCTest, including using `XCTAssert` functions and UI
  test recording.
- **Fastlane Documentation:** Guides for using Fastlane tools (`match`,
  `pilot`, etc.) to automate code signing and TestFlight deployments,
  useful for setting up CI/CD pipelines outside Xcode Cloud.

------------------------------------------------------------------------
