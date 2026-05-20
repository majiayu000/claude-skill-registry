---
name: cross-platform
cluster: mobile
description: "React Native+Expo (EAS), Flutter/Dart (Bloc/Riverpod), Capacitor, KMM — framework selection"
tags: ["cross-platform","react-native","flutter","expo","capacitor"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "react native flutter expo cross platform mobile capacitor kmm"
---

# cross-platform

## Purpose
This skill guides the selection and implementation of cross-platform mobile frameworks like React Native with Expo, Flutter with Dart (using Bloc or Riverpod), Capacitor, and Kotlin Multiplatform Mobile (KMM). It focuses on choosing the right framework based on project needs and provides step-by-step integration for efficient mobile app development.

## When to Use
Use this skill for projects requiring multi-platform deployment (iOS/Android) to reduce code duplication. Apply it when building apps with shared business logic, such as e-commerce apps, social networks, or productivity tools. Ideal for teams with limited resources or when rapid prototyping is needed, like integrating native modules or handling state management across platforms.

## Key Capabilities
- Framework selection: Choose React Native for JavaScript-heavy apps, Flutter for custom UI with Dart, Capacitor for web-to-mobile conversion, or KMM for shared Kotlin codebases.
- Expo integration: Use EAS (Expo Application Services) for streamlined builds, including OTA updates and cloud services.
- State management: Implement Bloc for event-driven state in Flutter or Riverpod for reactive state in Flutter/Dart apps.
- Cross-platform features: Handle platform-specific code, like accessing device APIs (e.g., camera, GPS) via Capacitor's bridge or KMM's expect/actual declarations.
- Configuration: Manage app configs in JSON/YAML formats, such as Expo's app.json for routing and permissions.

## Usage Patterns
To select a framework, evaluate based on tech stack: use React Native if the team knows JS; Flutter for high-performance UIs. Start by initializing a project:
- For React Native with Expo: Run `expo init MyApp --template blank` then add dependencies with `npm install @react-navigation/native`.
- For Flutter with Riverpod: Create a project with `flutter create MyApp` and set up state: `final counterProvider = StateProvider((ref) => 0);` in a Dart file.
Always wrap platform-specific code: In KMM, use `expect fun platformFunction() {}` in common code and implement in iOS/Android modules.
For Capacitor, convert a web app by running `npx cap add android` after setting up a web project.

## Common Commands/API
- Expo (React Native): Use `expo login` (requires $EXPO_API_KEY env var), `eas build --platform all` for multi-platform builds, and API endpoint `POST https://api.expo.dev/v2/projects` for project management.
- Flutter: Run `flutter pub add flutter_bloc` for Bloc, or `flutter run --device-id emulator-5554` to target a specific emulator; access APIs like `BlocProvider.of(context).add(Event())` for state changes.
- Capacitor: Execute `npx cap sync` to update native projects, or `npx cap open android` to launch Android Studio; use Capacitor's Plugins API, e.g., `Capacitor.Plugins.Camera.getPhoto()` in JavaScript.
- KMM: Build with `./gradlew build` in the shared module, and use KMM Bridge for iOS: `import shared.Platform().hello()` in Swift.
Config formats: Edit Expo's app.json like `{ "expo": { "name": "MyApp", "slug": "myapp", "platforms": ["ios", "android"] } }`; for Flutter, modify pubspec.yaml with `dependencies: flutter_riverpod: ^2.0.0`.

## Integration Notes
Integrate these frameworks with backends by setting environment variables for auth, e.g., export $BACKEND_API_KEY for API calls. For React Native, use Expo's Fetch API: `fetch('https://api.example.com/data', { headers: { Authorization: `Bearer ${process.env.BACKEND_API_KEY}` } })`. In Flutter, add HTTP packages: `http.get(Uri.parse('https://api.example.com/data'), headers: {'Authorization': 'Bearer $envVar'}).then((response) => ...);`. For Capacitor, bridge web requests: Install `@capacitor/core` and use `CapacitorHttp.get({url: 'https://api.example.com/data', headers: {Authorization: $BACKEND_API_KEY}});`. KMM integration: Share networking code via common module and call from native apps, ensuring Gradle sync for dependencies.

## Error Handling
Handle common errors by checking for platform mismatches: In React Native, if `expo build` fails with "Invalid platform", verify app.json platforms array. For Flutter, if `flutter run` errors on "No devices", use `flutter emulators --launch Pixel_API_33` then retry. Capacitor errors like "Plugin not found" require `npx cap sync` and verifying package.json. In KMM, resolve build failures with `./gradlew clean` for corrupted caches. Always log errors: In Expo, use `console.error(e)` and check EAS build logs; in Flutter, wrap with try-catch: `try { await http.get(...); } catch (e) { print(e.toString()); }`. Use env vars for secure keys to avoid exposure.

## Graph Relationships
- Connected to: mobile cluster
- Relates to: react-native skill, flutter skill, expo skill, capacitor skill
- Depends on: cross-platform tags for embedding
- Interacts with: kmm framework in mobile ecosystem
