# 📦 Skill: App Distribution & Deployment

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-app-distribution` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `app-distribution`, `testflight`, `play-console`, `firebase-distribution`, `fastlane`, `beta-testing` |
| **Referencia** | [Flutter Deployment](https://docs.flutter.dev/deployment) |

## 🔑 Keywords para Invocación

- `app-distribution`
- `testflight`
- `play-console`
- `firebase-distribution`
- `fastlane`
- `beta-testing`
- `app-deployment`
- `@skill:app-distribution`

### Ejemplos de Prompts

```
Configura app-distribution con testflight y play-console
```

```
Implementa fastlane para automated deployment
```

```
Setup firebase-distribution para beta testing
```

```
@skill:app-distribution - Pipeline completo de distribución
```

## 📖 Descripción

Este skill cubre la distribución de aplicaciones Flutter en múltiples canales: TestFlight (iOS), Google Play Internal Testing, Firebase App Distribution, y automatización con Fastlane. Incluye configuración de flavors, signing, y CI/CD integration.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

### ✅ Cuándo Usar Este Skill

- Distribución a beta testers
- Internal testing pre-production
- Staged rollouts
- Automatizar releases
- Multiple build variants (dev/staging/prod)
- App Store submission
- Play Store submission

### ❌ Cuándo NO Usar Este Skill

- Solo desarrollo local
- No necesitas beta testing
- App no está lista para distribución

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   └── config/
│       ├── flavor_config.dart
│       └── app_config.dart
│
├── android/
│   ├── app/
│   │   ├── build.gradle
│   │   └── src/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── production/
│   ├── key.properties
│   └── fastlane/
│       ├── Fastfile
│       └── Appfile
│
├── ios/
│   ├── fastlane/
│   │   ├── Fastfile
│   │   └── Appfile
│   └── ExportOptions.plist
│
├── scripts/
│   ├── distribute.sh
│   └── build_flavors.sh
│
└── .github/
    └── workflows/
        ├── distribute_ios.yml
        └── distribute_android.yml
```

## 📦 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter

dev_dependencies:
  flutter_launcher_icons: ^0.13.1
  flutter_native_splash: ^2.3.7
```

## 💻 Implementación

### 1. Flavors Configuration

#### 1.1 Flutter Flavor Config

```dart
// lib/config/flavor_config.dart
enum Flavor {
  dev,
  staging,
  production,
}

class FlavorConfig {
  final Flavor flavor;
  final String name;
  final String apiBaseUrl;
  final String appName;
  final String bundleId;
  final bool enableAnalytics;
  final bool enableCrashlytics;

  static FlavorConfig? _instance;

  FlavorConfig._internal({
    required this.flavor,
    required this.name,
    required this.apiBaseUrl,
    required this.appName,
    required this.bundleId,
    required this.enableAnalytics,
    required this.enableCrashlytics,
  });

  static FlavorConfig get instance => _instance!;

  static bool get isProduction => _instance?.flavor == Flavor.production;
  static bool get isStaging => _instance?.flavor == Flavor.staging;
  static bool get isDevelopment => _instance?.flavor == Flavor.dev;

  static void setFlavor(Flavor flavor) {
    switch (flavor) {
      case Flavor.dev:
        _instance = FlavorConfig._internal(
          flavor: Flavor.dev,
          name: 'DEV',
          apiBaseUrl: 'https://dev-api.example.com',
          appName: 'MyApp DEV',
          bundleId: 'com.example.myapp.dev',
          enableAnalytics: false,
          enableCrashlytics: false,
        );
        break;

      case Flavor.staging:
        _instance = FlavorConfig._internal(
          flavor: Flavor.staging,
          name: 'STAGING',
          apiBaseUrl: 'https://staging-api.example.com',
          appName: 'MyApp STAGING',
          bundleId: 'com.example.myapp.staging',
          enableAnalytics: true,
          enableCrashlytics: true,
        );
        break;

      case Flavor.production:
        _instance = FlavorConfig._internal(
          flavor: Flavor.production,
          name: 'PRODUCTION',
          apiBaseUrl: 'https://api.example.com',
          appName: 'MyApp',
          bundleId: 'com.example.myapp',
          enableAnalytics: true,
          enableCrashlytics: true,
        );
        break;
    }
  }

  @override
  String toString() => name;
}
```

```dart
// lib/main_dev.dart
import 'package:flutter/material.dart';
import 'config/flavor_config.dart';
import 'app.dart';

void main() {
  FlavorConfig.setFlavor(Flavor.dev);
  runApp(const MyApp());
}

// lib/main_staging.dart
import 'package:flutter/material.dart';
import 'config/flavor_config.dart';
import 'app.dart';

void main() {
  FlavorConfig.setFlavor(Flavor.staging);
  runApp(const MyApp());
}

// lib/main_production.dart
import 'package:flutter/material.dart';
import 'config/flavor_config.dart';
import 'app.dart';

void main() {
  FlavorConfig.setFlavor(Flavor.production);
  runApp(const MyApp());
}
```

#### 1.2 Android Flavor Configuration

```gradle
// android/app/build.gradle
android {
    defaultConfig {
        applicationId "com.example.myapp"
        // ...
    }

    signingConfigs {
        release {
            if (System.getenv("CI")) {
                // CI/CD environment
                storeFile file(System.getenv("KEYSTORE_PATH"))
                storePassword System.getenv("KEYSTORE_PASSWORD")
                keyAlias System.getenv("KEY_ALIAS")
                keyPassword System.getenv("KEY_PASSWORD")
            } else {
                // Local development
                def keystoreProperties = new Properties()
                def keystorePropertiesFile = rootProject.file('key.properties')
                if (keystorePropertiesFile.exists()) {
                    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
                }
                storeFile file(keystoreProperties['storeFile'])
                storePassword keystoreProperties['storePassword']
                keyAlias keystoreProperties['keyAlias']
                keyPassword keystoreProperties['keyPassword']
            }
        }
    }

    flavorDimensions "environment"
    productFlavors {
        dev {
            dimension "environment"
            applicationIdSuffix ".dev"
            versionNameSuffix "-dev"
            resValue "string", "app_name", "MyApp DEV"
            buildConfigField "String", "API_BASE_URL", '"https://dev-api.example.com"'
        }

        staging {
            dimension "environment"
            applicationIdSuffix ".staging"
            versionNameSuffix "-staging"
            resValue "string", "app_name", "MyApp STAGING"
            buildConfigField "String", "API_BASE_URL", '"https://staging-api.example.com"'
        }

        production {
            dimension "environment"
            resValue "string", "app_name", "MyApp"
            buildConfigField "String", "API_BASE_URL", '"https://api.example.com"'
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
        
        debug {
            applicationIdSuffix ".debug"
        }
    }
}
```

```properties
# android/key.properties (NO commitar, agregar a .gitignore)
storeFile=../upload-keystore.jks
storePassword=your_keystore_password
keyAlias=upload
keyPassword=your_key_password
```

#### 1.3 iOS Flavor Configuration

```xml
<!-- ios/Runner/Info.plist -->
<key>CFBundleDisplayName</key>
<string>$(APP_DISPLAY_NAME)</string>
<key>CFBundleIdentifier</key>
<string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
```

```bash
# Configurar schemes en Xcode:
# 1. Product > Scheme > Manage Schemes
# 2. Crear schemes: dev, staging, production
# 3. Para cada scheme, configurar Build Configuration

# En Xcode, agregar User-Defined Settings:
# DEV:
#   APP_DISPLAY_NAME = MyApp DEV
#   PRODUCT_BUNDLE_IDENTIFIER = com.example.myapp.dev
# STAGING:
#   APP_DISPLAY_NAME = MyApp STAGING
#   PRODUCT_BUNDLE_IDENTIFIER = com.example.myapp.staging
# PRODUCTION:
#   APP_DISPLAY_NAME = MyApp
#   PRODUCT_BUNDLE_IDENTIFIER = com.example.myapp
```

### 2. TestFlight Distribution

#### 2.1 Fastlane iOS Setup

```bash
# Instalar Fastlane
sudo gem install fastlane -NV

# Inicializar en carpeta ios/
cd ios
fastlane init
```

```ruby
# ios/fastlane/Fastfile
default_platform(:ios)

platform :ios do
  desc "Push a new beta build to TestFlight"
  lane :beta do
    # Increment build number
    increment_build_number(
      xcodeproj: "Runner.xcodeproj",
      build_number: latest_testflight_build_number + 1
    )

    # Build app
    build_app(
      scheme: "production",
      export_method: "app-store",
      export_options: {
        provisioningProfiles: {
          "com.example.myapp" => "match AppStore com.example.myapp"
        }
      }
    )

    # Upload to TestFlight
    upload_to_testflight(
      skip_waiting_for_build_processing: true,
      skip_submission: true,
      distribute_external: false,
      notify_external_testers: false
    )

    # Send notification
    slack(
      message: "New iOS beta build uploaded to TestFlight! 🚀",
      success: true
    )
  end

  desc "Deploy to App Store"
  lane :release do
    increment_build_number(
      xcodeproj: "Runner.xcodeproj"
    )

    build_app(
      scheme: "production",
      export_method: "app-store"
    )

    upload_to_app_store(
      submit_for_review: false,
      automatic_release: false,
      skip_metadata: true,
      skip_screenshots: true,
      precheck_include_in_app_purchases: false
    )
  end

  desc "Staging build"
  lane :staging do
    build_app(
      scheme: "staging",
      export_method: "development"
    )

    firebase_app_distribution(
      app: "1:123456789:ios:abcd1234",
      testers: "testers@example.com",
      release_notes: "Staging build for testing"
    )
  end
end
```

```ruby
# ios/fastlane/Appfile
app_identifier("com.example.myapp")
apple_id("your@email.com")
team_id("TEAMID123")
```

### 3. Google Play Console Distribution

#### 3.1 Fastlane Android Setup

```bash
cd android
fastlane init
```

```ruby
# android/fastlane/Fastfile
default_platform(:android)

platform :android do
  desc "Deploy to Internal Testing track"
  lane :internal do
    # Build AAB
    gradle(
      task: "bundle",
      flavor: "production",
      build_type: "Release"
    )

    # Upload to Internal Testing
    upload_to_play_store(
      track: 'internal',
      aab: '../build/app/outputs/bundle/productionRelease/app-production-release.aab',
      skip_upload_screenshots: true,
      skip_upload_images: true,
      skip_upload_metadata: true
    )

    slack(
      message: "New Android build uploaded to Internal Testing! 🎉",
      success: true
    )
  end

  desc "Promote Internal to Beta"
  lane :promote_to_beta do
    upload_to_play_store(
      track: 'internal',
      track_promote_to: 'beta',
      skip_upload_aab: true,
      skip_upload_screenshots: true,
      skip_upload_images: true
    )
  end

  desc "Deploy to Production (Staged Rollout)"
  lane :production do
    gradle(
      task: "bundle",
      flavor: "production",
      build_type: "Release"
    )

    upload_to_play_store(
      track: 'production',
      rollout: '0.1',  # 10% rollout
      aab: '../build/app/outputs/bundle/productionRelease/app-production-release.aab'
    )
  end

  desc "Staging build to Firebase"
  lane :staging do
    gradle(
      task: "assemble",
      flavor: "staging",
      build_type: "Release"
    )

    firebase_app_distribution(
      app: "1:123456789:android:abcd1234",
      testers: "testers@example.com",
      release_notes: "Staging build for testing",
      apk_path: "../build/app/outputs/apk/staging/release/app-staging-release.apk"
    )
  end
end
```

```ruby
# android/fastlane/Appfile
json_key_file("service-account-key.json")
package_name("com.example.myapp")
```

### 4. Firebase App Distribution

#### 4.1 Firebase CLI Setup

```bash
# Instalar Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Configurar proyecto
firebase init
```

```bash
# scripts/distribute_firebase.sh
#!/bin/bash

# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Build Flutter app
cd mobile
flutter build apk --flavor staging --release
flutter build ios --flavor staging --release --no-codesign
cd ..

# Distribute Android
firebase appdistribution:distribute \
  build/app/outputs/apk/staging/release/app-staging-release.apk \
  --app 1:123456789:android:abcd1234 \
  --groups "testers" \
  --release-notes "Staging build $(date)"

# Distribute iOS (requiere .ipa firmado)
firebase appdistribution:distribute \
  build/ios/ipa/Runner.ipa \
  --app 1:123456789:ios:abcd1234 \
  --groups "testers" \
  --release-notes "Staging build $(date)"
```

### 5. GitHub Actions CI/CD

#### 5.1 iOS Distribution Workflow

```yaml
# .github/workflows/distribute_ios.yml
name: iOS Distribution

on:
  push:
    branches: [ main, develop ]
  workflow_dispatch:

jobs:
  distribute_ios:
    runs-on: macos-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          channel: 'stable'

      - name: Install dependencies
        run: flutter pub get

      - name: Run tests
        run: flutter test

      - name: Setup Fastlane
        run: |
          cd ios
          bundle install

      - name: Configure Apple Certificates
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          FASTLANE_USER: ${{ secrets.FASTLANE_USER }}
          FASTLANE_PASSWORD: ${{ secrets.FASTLANE_PASSWORD }}
        run: |
          cd ios
          bundle exec fastlane match appstore

      - name: Build and deploy to TestFlight
        env:
          FASTLANE_USER: ${{ secrets.FASTLANE_USER }}
          FASTLANE_PASSWORD: ${{ secrets.FASTLANE_PASSWORD }}
        run: |
          cd ios
          bundle exec fastlane beta

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: ios-build
          path: ios/build/Runner.ipa
```

#### 5.2 Android Distribution Workflow

```yaml
# .github/workflows/distribute_android.yml
name: Android Distribution

on:
  push:
    branches: [ main, develop ]
  workflow_dispatch:

jobs:
  distribute_android:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          distribution: 'zulu'
          java-version: '17'

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          channel: 'stable'

      - name: Install dependencies
        run: flutter pub get

      - name: Run tests
        run: flutter test

      - name: Configure Keystore
        env:
          KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
          KEY_PROPERTIES: ${{ secrets.KEY_PROPERTIES }}
        run: |
          echo $KEYSTORE_BASE64 | base64 -d > android/app/upload-keystore.jks
          echo "$KEY_PROPERTIES" > android/key.properties

      - name: Build AAB
        working-directory: mobile
        run: flutter build appbundle --flavor production --release

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.0'
          bundler-cache: true
          working-directory: android

      - name: Deploy to Play Console
        env:
          PLAY_STORE_CONFIG_JSON: ${{ secrets.PLAY_STORE_CONFIG_JSON }}
        run: |
          echo "$PLAY_STORE_CONFIG_JSON" > android/fastlane/service-account-key.json
          cd android
          bundle exec fastlane internal

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: android-build
          path: build/app/outputs/bundle/productionRelease/app-production-release.aab
```

### 6. Version Management

```dart
// lib/config/app_config.dart
class AppConfig {
  static const String version = '1.0.0';
  static const int buildNumber = 1;
  
  static String get versionString => '$version+$buildNumber';
  
  static String get fullVersionString {
    final flavor = FlavorConfig.instance.name;
    return '$version+$buildNumber ($flavor)';
  }
}
```

```bash
# scripts/bump_version.sh
#!/bin/bash

# Bump version in pubspec.yaml
VERSION=$1
BUILD_NUMBER=$2

if [ -z "$VERSION" ] || [ -z "$BUILD_NUMBER" ]; then
    echo "Usage: ./bump_version.sh <version> <build_number>"
    echo "Example: ./bump_version.sh 1.2.0 42"
    exit 1
fi

# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Update mobile/pubspec.yaml
sed -i "" "s/^version: .*/version: $VERSION+$BUILD_NUMBER/" mobile/pubspec.yaml

echo "✅ Version updated to $VERSION+$BUILD_NUMBER"

# Commit changes
git add mobile/pubspec.yaml
git commit -m "chore: bump version to $VERSION+$BUILD_NUMBER"
git tag "v$VERSION"

echo "📦 Created tag v$VERSION"
```

## 🎯 Mejores Prácticas

### 1. Signing & Security

✅ **DO:**
- Usa diferentes signing keys para dev/staging/prod
- Almacena keys en CI secrets
- Rota keys regularmente
- Usa Google Play App Signing

❌ **DON'T:**
- Commitear keys al repositorio
- Compartir keys por email
- Usar mismo key para todas builds

### 2. Release Notes

✅ **DO:** Genera release notes automáticas
```bash
# Generate changelog from git commits
git log --oneline --pretty=format:"- %s" v1.0.0..HEAD > release_notes.txt
```

### 3. Staged Rollouts

✅ **DO:** Usa staged rollouts para production
```ruby
# Start with 10%, monitor, then increase
upload_to_play_store(
  track: 'production',
  rollout: '0.1'  # 10%
)
```

## 🚨 Troubleshooting

### Error: "Keystore not found"

```bash
# Verificar que el path en key.properties es correcto
# Debe ser relativo a android/app/
storeFile=../upload-keystore.jks
```

### Error: TestFlight "Missing Compliance"

```xml
<!-- Agregar a Info.plist -->
<key>ITSAppUsesNonExemptEncryption</key>
<false/>
```

### Error: Play Console "Version code already exists"

```gradle
// Auto-increment version code
def buildNumber = System.getenv("BUILD_NUMBER") ?: "1"
versionCode buildNumber.toInteger()
```

## 📚 Recursos

- [Fastlane Documentation](https://docs.fastlane.tools/)
- [TestFlight Guide](https://developer.apple.com/testflight/)
- [Play Console Documentation](https://support.google.com/googleplay/android-developer/)
- [Firebase App Distribution](https://firebase.google.com/docs/app-distribution)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,100+

