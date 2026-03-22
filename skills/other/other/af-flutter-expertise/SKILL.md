---
name: af-flutter-expertise
description: Use when developing Flutter mobile applications within AgentFlow projects. Covers monorepo structure, Widgetbook, widget tests, design tokens, and CI/CD for mobile.

# AgentFlow documentation fields
title: Flutter Development Expertise
created: 2026-01-30
updated: 2026-02-03
last_checked: 2026-02-03
tags: [skill, expertise, mobile, flutter, dart, ios, android]
parent: ../README.md
---

# Flutter Development Expertise

**Status:** Active
**Related Issue:** AF-82

Use this skill when developing Flutter mobile applications within AgentFlow projects. This skill provides **patterns and reference material**.

> **For step-by-step installation**, see: [Flutter Mobile Setup Guide](../../docs/guides/gaininsight-standard/flutter-mobile-setup.md)

---

## Overview

Flutter enables cross-platform mobile development (iOS + Android) from a single Dart codebase.

**This skill covers:**
- Patterns and architectural decisions
- Code reference for common tasks
- Troubleshooting and learnings
- CI/CD configuration

**The setup guide covers:**
- Step-by-step installation after Layer 1
- Monorepo conversion
- Amplify integration setup
- Widgetbook configuration

---

## Monorepo Structure

When a project has both web and mobile:

```
/
├── amplify/                    # Shared backend (Gen 2)
│   ├── auth/
│   ├── data/
│   └── functions/
├── packages/
│   ├── web/                    # Next.js app
│   │   ├── src/
│   │   ├── stories/           # Storybook
│   │   └── package.json
│   └── mobile/                # Flutter app
│       ├── lib/
│       ├── widgetbook/        # Widgetbook
│       └── pubspec.yaml
├── .claude/                    # AgentFlow (root level)
├── amplify_outputs.json        # Generated config (at root)
└── package.json               # Workspaces config
```

### Sharing amplify_outputs.json

The `amplify_outputs.json` is generated at root during `ampx sandbox` or deployment. Both web and mobile need access.

**Web (Next.js)**: Use postinstall script (symlinks don't work cross-platform with git):
```json
{
  "scripts": {
    "postinstall": "cp ../../amplify_outputs.json . 2>/dev/null || true"
  }
}
```

**Mobile (Flutter)**: Generate Dart config from JSON (see Amplify Flutter Integration section).

---

## Flutter on Linux (gidev)

### Installation

Flutter SDK installed at: `/var/lib/tmux-shared/flutter/`

Add to PATH:
```bash
export PATH="/var/lib/tmux-shared/flutter/bin:$PATH"
```

### What Works on Linux

| Activity | Linux | macOS Required |
|----------|-------|----------------|
| Write Dart code | ✅ | |
| Hot reload | ✅ | |
| Android emulator | ✅ | |
| Build Android APK/AAB | ✅ | |
| Flutter Web dev server | ✅ | |
| iOS Simulator | ❌ | ✅ |
| Build iOS IPA | ❌ | ✅ |

### Running Flutter Web (Headless Server)

Don't use `flutter run -d chrome` (requires local browser).

Instead, run headless web server:
```bash
flutter run -d web-server --web-port=73000 --web-hostname=0.0.0.0
```

Caddy proxies the port to external URL (e.g., `aft.gaininsight.co.uk`).

---

## Port Allocation

**IMPORTANT:** Ports are allocated per-project using `port_base` from the project registry. Each project gets a 1000-port range with service offsets.

| Service | Offset Range | Indigo (base 3000) | AFT (base 10000) |
|---------|--------------|--------------------|--------------------|
| Next.js/Main | +0-99 | 3000-3099 | 10000-10099 |
| Flutter Web | +100-199 | 3100-3199 | 10100-10199 |
| Storybook | +300-399 | 3300-3399 | 10300-10399 |
| Widgetbook | +400-499 | 3400-3499 | 10400-10499 |
| Test Reports | +600-699 | 3600-3699 | 10600-10699 |

**Port formula:** `PORT_BASE + OFFSET + SLOT` where SLOT is 0 for main/develop, or issue number.

**Example for AFT-82:**
- Main: 10000 + 0 + 82 = 10082
- Flutter: 10000 + 100 + 82 = 10182
- Widgetbook: 10000 + 400 + 82 = 10482

Use `project-registry <project> port_base` to check port_base values.

---

## Widgetbook (Flutter's Storybook)

Widgetbook is the Flutter equivalent of Storybook - a component catalog for visual development.

### Minimum Versions

**For debug mode to work correctly:**
- Flutter 3.38+ (Dart 3.10+)
- Widgetbook 3.20+
- widgetbook_annotation 3.9+

Older versions (Flutter 3.24.x with Widgetbook <3.10) have a debug mode issue where `web-server` shows blank white screen.

### Setup

```yaml
# pubspec.yaml
environment:
  sdk: ^3.10.0  # Dart 3.10+ required

dev_dependencies:
  widgetbook: ^3.20.0
  widgetbook_annotation: ^3.9.0
```

### Structure

```
packages/mobile/
├── lib/
│   └── components/
│       └── button.dart
└── widgetbook/
    ├── main.dart           # Widgetbook app entry
    └── button.story.dart   # Component stories
```

### Running Widgetbook

With the minimum versions above, debug mode works correctly:

```bash
cd packages/mobile

# Debug mode (with hot reload) - REQUIRES Flutter 3.38+ / Widgetbook 3.20+
flutter run -d web-server -t widgetbook/main.dart --web-port=PORT --web-hostname=0.0.0.0
```

**Legacy fallback (Flutter <3.38 or Widgetbook <3.20):**
If you're stuck on older versions, debug mode shows a blank white screen. Use release builds instead:

```bash
# Build release and serve static files
flutter build web -t widgetbook/main.dart --release
python3 -m http.server PORT --directory build/web
```

---

## Widget Tests

Flutter's equivalent of React Testing Library (RTL) tests.

### Example

```dart
// test/components/button_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:aft_mobile/components/button.dart';

void main() {
  testWidgets('Button displays label', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Button(label: 'Click me'),
      ),
    );

    expect(find.text('Click me'), findsOneWidget);
  });

  testWidgets('Button triggers onPressed', (tester) async {
    var pressed = false;

    await tester.pumpWidget(
      MaterialApp(
        home: Button(
          label: 'Click me',
          onPressed: () => pressed = true,
        ),
      ),
    );

    await tester.tap(find.byType(Button));
    expect(pressed, isTrue);
  });
}
```

### Selector Contracts (Key objects)

Flutter uses `Key` objects instead of `data-testid`:

```dart
// lib/keys/auth_keys.dart
class AuthKeys {
  static const loginButton = Key('auth_login_button');
  static const emailField = Key('auth_email_field');
  static const passwordField = Key('auth_password_field');
}

// In widget:
ElevatedButton(
  key: AuthKeys.loginButton,
  onPressed: _handleLogin,
  child: Text('Login'),
)

// In test:
await tester.tap(find.byKey(AuthKeys.loginButton));
```

---

## Golden Tests (Visual Regression)

Golden tests capture pixel-perfect snapshots for visual regression testing.

```dart
testWidgets('Button matches golden', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Button(label: 'Click me'),
    ),
  );

  await expectLater(
    find.byType(Button),
    matchesGoldenFile('goldens/button.png'),
  );
});
```

Update goldens: `flutter test --update-goldens`

---

## Amplify Flutter Integration

Flutter apps connect to the same Amplify backend as web using a parallel configuration pattern.

```yaml
# pubspec.yaml
dependencies:
  amplify_flutter: ^2.0.0
  amplify_auth_cognito: ^2.0.0
  amplify_api: ^2.0.0
```

### Web vs Flutter Config Pattern

Both platforms load `amplify_outputs.json` at runtime, but the mechanisms differ:

| Aspect | Web (Next.js) | Flutter |
|--------|---------------|---------|
| **Sync mechanism** | `postinstall` script copies JSON | Shell script copies to `assets/` |
| **Loading** | ES module dynamic import | `rootBundle.loadString()` |
| **Initialization** | `Amplify.configure(outputs)` | `Amplify.configure(jsonString)` |
| **Configured flag** | Module-level `let configured = false` | Top-level `bool _amplifyConfigured = false` |
| **Fallback** | Returns early if no config | Fallback JSON constant |

### Web Pattern (Reference)

```typescript
// packages/web/src/lib/amplify-config.ts
import { Amplify } from 'aws-amplify';
import outputs from '../../amplify_outputs.json';

let configured = false;

export function configureAmplify() {
  if (configured) return;
  try {
    Amplify.configure(outputs);
    configured = true;
  } catch (e) {
    console.warn('Amplify config not available');
  }
}
```

```json
// packages/web/package.json
{
  "scripts": {
    "postinstall": "cp ../../amplify_outputs.json . 2>/dev/null || true"
  }
}
```

### Flutter Pattern (Parallel)

```dart
// lib/amplify_config.dart
import 'dart:convert';
import 'package:flutter/services.dart';

String? _cachedConfig;

/// Load Amplify config from bundled asset
/// Parallel to web's dynamic import approach
Future<String> loadAmplifyConfig() async {
  if (_cachedConfig != null) return _cachedConfig!;

  try {
    final jsonString = await rootBundle.loadString('assets/amplify_outputs.json');
    json.decode(jsonString); // Validate JSON
    _cachedConfig = jsonString;
    return jsonString;
  } catch (e) {
    return _fallbackConfig; // Dev mode fallback
  }
}

const _fallbackConfig = '''
{
  "version": "1",
  "auth": {"user_pool_id": "", "aws_region": "eu-west-2"},
  "data": {"url": "", "aws_region": "eu-west-2"}
}
''';
```

```dart
// lib/main.dart
import 'package:amplify_flutter/amplify_flutter.dart';
import 'package:amplify_auth_cognito/amplify_auth_cognito.dart';
import 'package:amplify_api/amplify_api.dart';
import 'amplify_config.dart';

bool _amplifyConfigured = false;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await _configureAmplify();
  runApp(const MyApp());
}

Future<void> _configureAmplify() async {
  if (_amplifyConfigured) return;

  try {
    final config = await loadAmplifyConfig();
    await Amplify.addPlugins([AmplifyAuthCognito(), AmplifyAPI()]);
    await Amplify.configure(config);
    _amplifyConfigured = true;
    safePrint('Amplify configured successfully');
  } on AmplifyAlreadyConfiguredException {
    _amplifyConfigured = true;
  } catch (e) {
    safePrint('Error configuring Amplify: $e');
  }
}
```

### Asset Setup

```yaml
# pubspec.yaml
flutter:
  assets:
    - assets/amplify_outputs.json
```

```bash
# scripts/sync-amplify-config.sh
#!/bin/bash
# Run after `npx ampx sandbox` or `ampx deploy`
SOURCE="../../amplify_outputs.json"
DEST="assets/amplify_outputs.json"

if [ -f "$SOURCE" ]; then
  cp "$SOURCE" "$DEST"
  echo "✅ Synced amplify_outputs.json"
else
  echo '{"version":"1","auth":{},"data":{}}' > "$DEST"
fi
```

### Stack Validation (Todo.list Query)

Both web and Flutter validate the full stack by querying the same endpoint. This proves AppSync, API key auth, and DynamoDB are all working.

**Web pattern:**
```typescript
// packages/web/src/app/page.tsx
const client = generateClient<Schema>();
const result = await client.models.Todo.list();
// Shows: "No todos yet - API is working!" or "{n} todo(s) found"
```

**Flutter parallel:**
```dart
// lib/main.dart
Future<void> _fetchTodos() async {
  try {
    const listTodosQuery = '''
      query ListTodos {
        listTodos {
          items { id content isDone }
        }
      }
    ''';

    final request = GraphQLRequest<String>(document: listTodosQuery);
    final response = await Amplify.API.query(request: request).response;

    if (response.errors.isNotEmpty) {
      // Handle GraphQL errors
      return;
    }

    final json = jsonDecode(response.data!) as Map<String, dynamic>;
    final items = (json['listTodos']?['items'] as List?) ?? [];

    // Success: "No todos yet - API is working!" or "{n} todo(s) found"
    _status = items.isEmpty
        ? 'No todos yet - API is working!'
        : '${items.length} todo(s) found';
  } catch (e) {
    // Handle error
  }
}
```

**Key difference:** Web uses typed client (`client.models.Todo.list()`), Flutter uses raw GraphQL. Same endpoint, same result.

**What this validates:**
| Layer | Component | Proof |
|-------|-----------|-------|
| Config | `amplify_outputs.json` | Loaded without error |
| Network | AppSync endpoint | Request completes |
| Auth | API key | Request authorized |
| Data | DynamoDB | Query returns (even if empty) |

---

## iOS Strategy (Without Local Mac)

### Daily Development (Linux)
- Write code, test on Android emulator
- Preview on Flutter Web via Caddy URL
- Widget tests catch most issues

### CI/CD for iOS (Codemagic)
- Push to GitHub triggers Codemagic
- Codemagic has macOS runners
- Builds iOS IPA, uploads to TestFlight
- No local Mac required for builds

### When Mac IS Required
- Initial App Store setup (certificates, provisioning profiles)
- Debugging iOS-specific issues
- Approximately 1-2 hours per release cycle

---

## CI/CD Strategy (Hybrid)

Use **GitHub Actions for Android** (free) and **Codemagic for iOS only** (paid macOS required).

### Why Hybrid?

| Platform | GitHub Actions | Codemagic |
|----------|---------------|-----------|
| Android | ✅ Free Linux runners | ❌ Unnecessary cost |
| iOS | ❌ No macOS (or expensive) | ✅ macOS included |

### Build Triggers

| Branch | Android | iOS | Destination |
|--------|---------|-----|-------------|
| PR | ✅ GHA | ❌ | Code review |
| develop | ✅ GHA | ❌ | Dev environment |
| staging | ✅ GHA | ✅ Codemagic | Test environment (QA) |
| main | ✅ GHA | ✅ Codemagic | Production release |

**Rationale:** Flutter is 90-95% cross-platform consistent. QA catches iOS issues in staging before production.

### GitHub Actions (Android + Tests)

```yaml
# .github/workflows/mobile.yml
name: Mobile CI

on:
  push:
    branches: [develop, staging, main]
    paths: ['packages/mobile/**']
  pull_request:
    paths: ['packages/mobile/**']

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: packages/mobile
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.24.5'
          channel: 'stable'
      - run: flutter pub get
      - run: flutter test
      - run: flutter analyze

  build-android:
    needs: test
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: packages/mobile
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.24.5'
      - run: flutter pub get
      - run: flutter build apk --release
      - uses: actions/upload-artifact@v4
        with:
          name: android-apk
          path: packages/mobile/build/app/outputs/flutter-apk/app-release.apk

  # Only on staging/main - upload to Play Console internal track
  deploy-android:
    if: github.ref == 'refs/heads/staging' || github.ref == 'refs/heads/main'
    needs: build-android
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: android-apk
      - uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.GOOGLE_PLAY_SERVICE_ACCOUNT }}
          packageName: com.gaininsight.aft
          releaseFiles: app-release.apk
          track: internal
```

### Codemagic (iOS Only)

```yaml
# packages/mobile/codemagic.yaml
workflows:
  ios-staging:
    name: iOS Staging Build
    instance_type: mac_mini_m2
    max_build_duration: 30
    triggering:
      events:
        - push
      branch_patterns:
        - pattern: staging
          include: true
    environment:
      ios_signing:
        distribution_type: app_store
        bundle_identifier: com.gaininsight.aft
      groups:
        - app_store_credentials  # APPLE_ID, APP_STORE_CONNECT_KEY, etc.
      flutter: 3.24.5
    scripts:
      - name: Get dependencies
        script: |
          cd packages/mobile
          flutter pub get
      - name: Run tests
        script: |
          cd packages/mobile
          flutter test
      - name: Build iOS
        script: |
          cd packages/mobile
          flutter build ipa --release --export-options-plist=/Users/builder/export_options.plist
    artifacts:
      - packages/mobile/build/ios/ipa/*.ipa
    publishing:
      app_store_connect:
        auth: integration
        submit_to_testflight: true
      slack:  # (legacy — migrate to Zulip webhook)
        channel: '#mobile-builds'
        notify_on_build_start: false

  ios-production:
    name: iOS Production Release
    instance_type: mac_mini_m2
    max_build_duration: 30
    triggering:
      events:
        - push
      branch_patterns:
        - pattern: main
          include: true
    environment:
      ios_signing:
        distribution_type: app_store
        bundle_identifier: com.gaininsight.aft
      groups:
        - app_store_credentials
      flutter: 3.24.5
    scripts:
      - name: Get dependencies
        script: |
          cd packages/mobile
          flutter pub get
      - name: Build iOS
        script: |
          cd packages/mobile
          flutter build ipa --release --export-options-plist=/Users/builder/export_options.plist
    artifacts:
      - packages/mobile/build/ios/ipa/*.ipa
    publishing:
      app_store_connect:
        auth: integration
        submit_to_testflight: true
        submit_to_app_store: true
      slack:  # (legacy — migrate to Zulip webhook)
        channel: '#releases'
```

### Codemagic Setup Steps

1. **Create account**: [codemagic.io](https://codemagic.io) → Sign up with GitHub
2. **Connect repo**: Add your repository
3. **Apple Developer connection**:
   - Settings → Integrations → Apple Developer Portal
   - Connect with App Store Connect API key
   - Codemagic auto-manages certificates and provisioning profiles
4. **Environment variables** (in Codemagic UI):
   ```
   APPLE_ID=your@email.com
   APP_STORE_CONNECT_ISSUER_ID=xxx
   APP_STORE_CONNECT_KEY_ID=xxx
   APP_STORE_CONNECT_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----...
   ```
5. **Add codemagic.yaml** to repo at `packages/mobile/codemagic.yaml`

### Cost Estimate

| Activity | Platform | Minutes/month | Cost |
|----------|----------|---------------|------|
| PR checks | GHA Linux | 100 | Free |
| develop builds | GHA Linux | 50 | Free |
| staging iOS | Codemagic macOS | 30 | ~$1.14 |
| production iOS | Codemagic macOS | 10 | ~$0.38 |
| **Total** | | | **~$2/month** |

*Based on ~$0.038/min for Mac mini M2. Free tier (500 min) covers most small teams.*

### Prerequisites

| Item | Cost | Notes |
|------|------|-------|
| Apple Developer Account | $99/year | Required for iOS distribution |
| Google Play Console | $25 one-time | Required for Android distribution |
| App Bundle IDs | Free | e.g., `com.gaininsight.aft` |
| Android Keystore | Free | Generate with `keytool` |

---

## Design Tokens Bridge

Style Dictionary can generate both CSS variables (web) and Dart theme (mobile):

```
tokens/
├── colors.json
├── typography.json
└── spacing.json
    ↓
style-dictionary build
    ↓
├── packages/web/src/styles/tokens.css
└── packages/mobile/lib/theme/tokens.dart
```

### Tokens That Transfer Cleanly
- Colors → ColorScheme
- Typography scale → TextTheme
- Spacing scale → EdgeInsets constants
- Border radius → BorderRadius constants

### Platform-Specific Handling
- Shadows/elevation (different mental models)
- Animation curves (platform conventions)
- Component-specific tokens

---

## Commands Reference

```bash
# Create new Flutter app
flutter create --org com.gaininsight packages/mobile

# Run on Android emulator
flutter run -d emulator-5554

# Run Flutter web (headless for gidev)
flutter run -d web-server --web-port=73000 --web-hostname=0.0.0.0

# Run Widgetbook (debug mode with hot reload)
flutter run -d web-server -t widgetbook/main.dart --web-port=76000 --web-hostname=0.0.0.0

# Run tests
flutter test

# Update golden files
flutter test --update-goldens

# Build Android APK
flutter build apk

# Build Android App Bundle (Play Store)
flutter build appbundle
```

---

## Learnings Log

<!-- Capture learnings as we build against AFT -->

### 2026-01-30: Initial Setup
- Flutter 3.24.5 installed on gidev at `/var/lib/tmux-shared/flutter/`
- Android SDK already present (v33.0.0)
- Chrome not needed for headless web server
- AFT converted to monorepo: `packages/web/` (Next.js), `packages/mobile/` (Flutter)

### 2026-01-30: Monorepo Conversion
- Used `flutter create --org com.gaininsight mobile --project-name aft_mobile`
- Root package.json uses npm workspaces: `"workspaces": ["packages/*"]`
- Flutter web server tested successfully on port 4500
- **Port discovery**: Initial skill draft had invalid ports (73000 > 65535 max)
- Corrected port allocation: Flutter Web at 4000+, Widgetbook at 7000+
- **Symlink issue**: Git doesn't reliably check in symlinks cross-platform
- **Solution**: Use postinstall script instead: `"postinstall": "cp ../../amplify_outputs.json . 2>/dev/null || true"`
- GID-13 updated with Part 3: Flutter port allocation for gidev (offsets +1000, +4000)

### 2026-01-30: Widgetbook Setup
- **Version compatibility**: Flutter 3.24.5 (Dart 3.5.4) requires Widgetbook 3.7.1, not 3.10+
- Newer Widgetbook requires Dart 3.7+, check `flutter --version` before choosing version
- Import paths in widgetbook/ must use package imports: `import 'package:aft_mobile/components/...'`
- Relative imports (`../lib/...`) don't work from widgetbook/ directory
- Created AftButton component with primary/secondary/disabled variants
- Test keys pattern: `lib/keys/component_keys.dart` with `Key('button_primary')` etc.

### 2026-01-30: Amplify Flutter Integration
- Amplify Flutter SDK: `amplify_flutter`, `amplify_auth_cognito`, `amplify_api`
- Config pattern: Create `lib/amplify_config.dart` with JSON string from `amplify_outputs.json`
- Initialize in main(): `WidgetsFlutterBinding.ensureInitialized()` then `Amplify.configure()`
- Graceful error handling: catch errors if config is empty/invalid during dev
- Same Amplify backend serves both web and mobile (shared amplify/ directory)

### 2026-01-30: CI/CD Strategy Decision
- **Hybrid approach**: GitHub Actions for Android (free), Codemagic for iOS only (paid)
- Android builds work fine on Linux - no need to pay Codemagic for them
- iOS builds on staging + main only (not PRs or develop) - saves cost
- Flutter is ~95% cross-platform consistent - QA catches iOS issues in staging
- Estimated cost: ~$2/month for small team (mostly free tier)
- Codemagic handles Apple certificates/profiles automatically via API key connection

### 2026-01-30: Stack Validation Pattern
- Web uses typed client: `client.models.Todo.list()` - auto-generates GraphQL
- Flutter uses raw GraphQL: `Amplify.API.query()` with document string
- Same endpoint, same auth (public API key), same result
- Both show: "No todos yet - API is working!" or "{n} todo(s) found"
- This validates the full stack: config → AppSync → API key → DynamoDB
- Created `scripts/sync-amplify-config.sh` to copy config to assets/
- Flutter loads config at runtime via `rootBundle.loadString()`

### 2026-02-03: Widgetbook Debug Mode Issue & Resolution (Mind Project)
- **Problem**: Widgetbook displays blank white screen with Flutter's `web-server` debug mode
- **Symptoms**: No console errors, just empty white page via Caddy proxy
- **Initial workaround**: Build release mode + serve static files
- **Root cause identified**: Version-specific incompatibility between Flutter 3.24.x and Widgetbook <3.10.0
- **Solution**: Upgrade to minimum versions:
  - Flutter 3.38+ (upgraded gidev from 3.24.5 → 3.38.9)
  - Widgetbook 3.20+ (upgraded from 3.9.0 → 3.20.2)
  - Dart SDK 3.10+
- **Result**: Debug mode now works correctly with hot reload
- **Recommended pubspec.yaml**:
  ```yaml
  environment:
    sdk: ^3.10.0
  dev_dependencies:
    widgetbook: ^3.20.0
    widgetbook_annotation: ^3.9.0
  ```
- **GainInsight Standard integration**: `start-work-impl` creates Caddy entries with `-widgetbook` suffix
- **Port allocation**: Widgetbook uses offset +400 (e.g., port_base 17000 → Widgetbook on 17400)

---

## References

**AgentFlow:**
- [Flutter Mobile Setup Guide](../../docs/guides/gaininsight-standard/flutter-mobile-setup.md) - Step-by-step installation
- [AFT Reference Implementation](/srv/worktrees/aft/develop/packages/mobile/) - Working example

**External:**
- [Flutter Documentation](https://docs.flutter.dev/)
- [Widgetbook](https://docs.widgetbook.io/)
- [Amplify Flutter](https://docs.amplify.aws/flutter/)
- [Codemagic CI/CD](https://codemagic.io/)

**Related:** AF-82 (Flutter Mobile Support)
