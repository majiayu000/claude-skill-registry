# 🔒 Skill: Security Best Practices

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-security` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `security`, `obfuscation`, `certificate-pinning`, `secure-storage`, `encryption`, `biometric` |
| **Referencia** | [OWASP Mobile Security](https://owasp.org/www-project-mobile-top-10/) |

## 🔑 Keywords para Invocación

Usa cualquiera de estos keywords en tus prompts para invocar este skill:

- `security`
- `obfuscation`
- `certificate-pinning`
- `secure-storage`
- `encryption`
- `biometric`
- `ssl-pinning`
- `root-detection`
- `@skill:security`

### Ejemplos de Prompts

```
Implementa security best practices con certificate pinning y secure storage
```

```
Configura code obfuscation y protección contra root/jailbreak
```

```
@skill:security - Setup completo de seguridad para producción
```

```
Necesito biometric authentication y encrypted storage
```

```
Protege API keys y implementa SSL pinning
```

## 📖 Descripción

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

Security en Flutter apps requiere múltiples capas de protección: desde code obfuscation y certificate pinning hasta secure storage y biometric authentication. Este skill cubre las mejores prácticas y técnicas esenciales para proteger aplicaciones Flutter en producción.

### ✅ Cuándo Usar Este Skill

- Apps en producción con datos sensibles
- Aplicaciones financieras/bancarias
- Apps con información médica (HIPAA compliance)
- E-commerce con datos de pago
- Apps empresariales con datos corporativos
- Cualquier app que maneje PII (Personally Identifiable Information)
- Apps con autenticación de usuarios
- Comunicación con APIs privadas

### ❌ Cuándo NO Usar Este Skill

- Prototipos internos sin datos reales
- Apps sin datos sensibles
- Aplicaciones de contenido público
- MVPs en fase de validación

**Importante:** Incluso apps "simples" deben implementar seguridad básica. Este skill ofrece niveles progresivos de seguridad.

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── core/
│   │   ├── security/
│   │   │   ├── secure_storage_service.dart
│   │   │   ├── encryption_service.dart
│   │   │   ├── certificate_pinning.dart
│   │   │   ├── biometric_service.dart
│   │   │   ├── root_detection.dart
│   │   │   └── api_key_manager.dart
│   │   ├── network/
│   │   │   ├── secure_http_client.dart
│   │   │   └── ssl_pinning_interceptor.dart
│   │   └── config/
│   │       ├── environment.dart
│   │       └── secrets.dart.example
│   │
│   ├── services/
│   │   └── auth_service.dart
│   │
│   └── main.dart
│
├── android/
│   ├── app/
│   │   ├── proguard-rules.pro
│   │   └── build.gradle
│   └── key.properties.example
│
├── ios/
│   └── Runner/
│       └── Info.plist
│
├── assets/
│   └── certificates/
│       ├── cert.pem
│       └── README.md
│
├── .env.example
└── scripts/
    └── obfuscate.sh
```

## 📦 Dependencias Requeridas

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Secure Storage
  flutter_secure_storage: ^9.0.0

  # Encryption
  encrypt: ^5.0.3
  crypto: ^3.0.3

  # Biometric Authentication
  local_auth: ^2.1.7

  # Certificate Pinning
  dio: ^5.4.0

  # Root/Jailbreak Detection
  flutter_jailbreak_detection: ^1.10.0

  # Environment Variables
  flutter_dotenv: ^5.1.0

  # Platform Security
  flutter_windowmanager: ^0.2.0  # Android screenshot prevention

  # Utilities
  uuid: ^4.2.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
```

## 💻 Implementación

### 1. Code Obfuscation

#### 1.1 Configuración Android

```gradle
// android/app/build.gradle
android {
    buildTypes {
        release {
            // Enable obfuscation
            minifyEnabled true
            shrinkResources true

            // ProGuard configuration
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'

            // Additional security
            debuggable false
            jniDebuggable false
            renderscriptDebuggable false

            // Signing config
            signingConfig signingConfigs.release
        }
    }
}
```

```proguard
# android/app/proguard-rules.pro

# Flutter wrapper
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.**  { *; }
-keep class io.flutter.util.**  { *; }
-keep class io.flutter.view.**  { *; }
-keep class io.flutter.**  { *; }
-keep class io.flutter.plugins.**  { *; }

# Preserve generic signatures for serialization
-keepattributes Signature
-keepattributes *Annotation*
-keepattributes EnclosingMethod

# Keep native methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# Obfuscate everything else
-repackageclasses ''
-allowaccessmodification

# Keep line numbers for stack traces
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

# Remove logging in production
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}
```

#### 1.2 Configuración iOS

```xml
<!-- ios/Runner/Info.plist -->
<key>ITSAppUsesNonExemptEncryption</key>
<false/>

<!-- Prevent debugging -->
<key>UIFileSharingEnabled</key>
<false/>
<key>LSSupportsOpeningDocumentsInPlace</key>
<false/>
```

#### 1.3 Flutter Obfuscation

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Build con obfuscation (Android)
cd mobile
flutter build apk --obfuscate --split-debug-info=build/app/outputs/symbols
cd ..

# Build con obfuscation (iOS)
cd mobile
flutter build ipa --obfuscate --split-debug-info=build/ios/outputs/symbols
cd ..

# Build AAB para Play Store
cd mobile
flutter build appbundle --obfuscate --split-debug-info=build/app/outputs/symbols --release
cd ..
```

#### 1.4 Script de Automatización

```bash
#!/bin/bash
# scripts/obfuscate.sh

echo "🔒 Building with obfuscation..."

# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

PLATFORM=$1
VERSION=$(grep 'version:' mobile/pubspec.yaml | awk '{print $2}' | cut -d'+' -f1)

if [ -z "$PLATFORM" ]; then
    echo "Usage: ./scripts/obfuscate.sh [android|ios|all]"
    exit 1
fi

build_android() {
    echo "📱 Building Android..."
    cd mobile
    flutter build appbundle \
        --obfuscate \
        --split-debug-info=build/android/symbols/$VERSION \
        --release
    cd ..

    echo "✅ Android build complete: build/app/outputs/bundle/release/"
}

build_ios() {
    echo "🍎 Building iOS..."
    cd mobile
    flutter build ipa \
        --obfuscate \
        --split-debug-info=build/ios/symbols/$VERSION \
        --release
    cd ..

    echo "✅ iOS build complete: build/ios/ipa/"
}

case $PLATFORM in
    android)
        build_android
        ;;
    ios)
        build_ios
        ;;
    all)
        build_android
        build_ios
        ;;
    *)
        echo "Invalid platform: $PLATFORM"
        exit 1
        ;;
esac

echo "🎉 Obfuscated builds complete!"

# Uso:
# ./scripts/obfuscate.sh android
# ./scripts/obfuscate.sh ios
# ./scripts/obfuscate.sh all
```

### 2. Secure Storage

#### 2.1 Secure Storage Service

```dart
// lib/core/security/secure_storage_service.dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:injectable/injectable.dart';

@singleton
class SecureStorageService {
  final FlutterSecureStorage _storage;

  SecureStorageService()
      : _storage = const FlutterSecureStorage(
          aOptions: AndroidOptions(
            encryptedSharedPreferences: true,
            // Reset on error
            resetOnError: true,
          ),
          iOptions: IOSOptions(
            accessibility: KeychainAccessibility.first_unlock_this_device,
          ),
        );

  // Generic read
  Future<String?> read(String key) async {
    try {
      return await _storage.read(key: key);
    } catch (e) {
      print('Error reading from secure storage: $e');
      return null;
    }
  }

  // Generic write
  Future<void> write(String key, String value) async {
    try {
      await _storage.write(key: key, value: value);
    } catch (e) {
      print('Error writing to secure storage: $e');
      rethrow;
    }
  }

  // Generic delete
  Future<void> delete(String key) async {
    try {
      await _storage.delete(key: key);
    } catch (e) {
      print('Error deleting from secure storage: $e');
      rethrow;
    }
  }

  // Delete all
  Future<void> deleteAll() async {
    try {
      await _storage.deleteAll();
    } catch (e) {
      print('Error deleting all from secure storage: $e');
      rethrow;
    }
  }

  // Check if key exists
  Future<bool> containsKey(String key) async {
    try {
      return await _storage.containsKey(key: key);
    } catch (e) {
      print('Error checking key in secure storage: $e');
      return false;
    }
  }

  // Read all keys
  Future<Map<String, String>> readAll() async {
    try {
      return await _storage.readAll();
    } catch (e) {
      print('Error reading all from secure storage: $e');
      return {};
    }
  }

  // Specific methods for common use cases
  static const _keyAuthToken = 'auth_token';
  static const _keyRefreshToken = 'refresh_token';
  static const _keyUserId = 'user_id';
  static const _keyBiometricEnabled = 'biometric_enabled';
  static const _keyEncryptionKey = 'encryption_key';

  Future<String?> getAuthToken() => read(_keyAuthToken);
  Future<void> setAuthToken(String token) => write(_keyAuthToken, token);
  Future<void> deleteAuthToken() => delete(_keyAuthToken);

  Future<String?> getRefreshToken() => read(_keyRefreshToken);
  Future<void> setRefreshToken(String token) => write(_keyRefreshToken, token);

  Future<String?> getUserId() => read(_keyUserId);
  Future<void> setUserId(String userId) => write(_keyUserId, userId);

  Future<bool> isBiometricEnabled() async {
    final value = await read(_keyBiometricEnabled);
    return value == 'true';
  }

  Future<void> setBiometricEnabled(bool enabled) =>
      write(_keyBiometricEnabled, enabled.toString());

  Future<String?> getEncryptionKey() => read(_keyEncryptionKey);
  Future<void> setEncryptionKey(String key) => write(_keyEncryptionKey, key);

  // Clear all authentication data
  Future<void> clearAuthData() async {
    await Future.wait([
      deleteAuthToken(),
      delete(_keyRefreshToken),
      delete(_keyUserId),
    ]);
  }
}
```

#### 2.2 Encryption Service

```dart
// lib/core/security/encryption_service.dart
import 'dart:convert';
import 'dart:typed_data';
import 'package:encrypt/encrypt.dart';
import 'package:crypto/crypto.dart';
import 'package:injectable/injectable.dart';

@singleton
class EncryptionService {
  late final Encrypter _encrypter;
  late final IV _iv;

  EncryptionService() {
    // Generate or retrieve encryption key
    final key = Key.fromSecureRandom(32); // AES-256
    _iv = IV.fromSecureRandom(16);
    _encrypter = Encrypter(AES(key, mode: AESMode.cbc));
  }

  // Initialize with specific key (from secure storage)
  void initializeWithKey(String base64Key) {
    final key = Key.fromBase64(base64Key);
    _iv = IV.fromSecureRandom(16);
    _encrypter = Encrypter(AES(key, mode: AESMode.cbc));
  }

  // Generate new encryption key
  static String generateKey() {
    final key = Key.fromSecureRandom(32);
    return key.base64;
  }

  // Encrypt string
  String encrypt(String plainText) {
    try {
      final encrypted = _encrypter.encrypt(plainText, iv: _iv);
      return encrypted.base64;
    } catch (e) {
      throw EncryptionException('Failed to encrypt data: $e');
    }
  }

  // Decrypt string
  String decrypt(String encryptedText) {
    try {
      final encrypted = Encrypted.fromBase64(encryptedText);
      return _encrypter.decrypt(encrypted, iv: _iv);
    } catch (e) {
      throw EncryptionException('Failed to decrypt data: $e');
    }
  }

  // Encrypt bytes
  Uint8List encryptBytes(Uint8List data) {
    try {
      final encrypted = _encrypter.encryptBytes(data, iv: _iv);
      return encrypted.bytes;
    } catch (e) {
      throw EncryptionException('Failed to encrypt bytes: $e');
    }
  }

  // Decrypt bytes
  Uint8List decryptBytes(Uint8List encryptedData) {
    try {
      final encrypted = Encrypted(encryptedData);
      return Uint8List.fromList(_encrypter.decryptBytes(encrypted, iv: _iv));
    } catch (e) {
      throw EncryptionException('Failed to decrypt bytes: $e');
    }
  }

  // Hash password (one-way)
  String hashPassword(String password, {String? salt}) {
    final saltToUse = salt ?? _generateSalt();
    final bytes = utf8.encode(password + saltToUse);
    final digest = sha256.convert(bytes);
    return '$saltToUse:${digest.toString()}';
  }

  // Verify password hash
  bool verifyPassword(String password, String hashedPassword) {
    try {
      final parts = hashedPassword.split(':');
      if (parts.length != 2) return false;

      final salt = parts[0];
      final hash = parts[1];

      final bytes = utf8.encode(password + salt);
      final digest = sha256.convert(bytes);

      return digest.toString() == hash;
    } catch (e) {
      return false;
    }
  }

  // Generate random salt
  String _generateSalt() {
    final random = Key.fromSecureRandom(16);
    return random.base64;
  }

  // Encrypt JSON
  String encryptJson(Map<String, dynamic> json) {
    final jsonString = jsonEncode(json);
    return encrypt(jsonString);
  }

  // Decrypt JSON
  Map<String, dynamic> decryptJson(String encryptedJson) {
    final jsonString = decrypt(encryptedJson);
    return jsonDecode(jsonString) as Map<String, dynamic>;
  }
}

class EncryptionException implements Exception {
  final String message;
  EncryptionException(this.message);

  @override
  String toString() => 'EncryptionException: $message';
}
```

### 3. Certificate Pinning

#### 3.1 Certificate Pinning Implementation

```dart
// lib/core/network/certificate_pinning.dart
import 'dart:io';
import 'package:flutter/services.dart';
import 'package:dio/dio.dart';
import 'package:dio/io.dart';

class CertificatePinning {
  static const String _certificatePath = 'assets/certificates/cert.pem';

  // Lista de SHA-256 fingerprints permitidos
  static const List<String> _allowedFingerprints = [
    // Ejemplo: SHA-256 del certificado del servidor
    'AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99',
  ];

  static Future<Dio> createDioWithPinning() async {
    final dio = Dio(
      BaseOptions(
        baseUrl: 'https://api.example.com',
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        validateStatus: (status) => status! < 500,
      ),
    );

    // Configure HTTP client with certificate pinning
    (dio.httpClientAdapter as IOHttpClientAdapter).createHttpClient = () {
      final client = HttpClient();

      client.badCertificateCallback = (cert, host, port) {
        // Verify certificate fingerprint
        final certFingerprint = _getCertificateFingerprint(cert);

        if (_allowedFingerprints.contains(certFingerprint)) {
          return true;
        }

        print('Certificate pinning failed for $host:$port');
        print('Received fingerprint: $certFingerprint');
        return false;
      };

      return client;
    };

    return dio;
  }

  // Get certificate SHA-256 fingerprint
  static String _getCertificateFingerprint(X509Certificate cert) {
    final der = cert.der;
    final hash = SHA256();
    final digest = hash.convert(der);

    return digest.bytes
        .map((byte) => byte.toRadixString(16).padLeft(2, '0').toUpperCase())
        .join(':');
  }

  // Load certificate from assets
  static Future<SecurityContext> loadCertificateFromAssets() async {
    final context = SecurityContext.defaultContext;

    try {
      final certData = await rootBundle.load(_certificatePath);
      final certBytes = certData.buffer.asUint8List();
      context.setTrustedCertificatesBytes(certBytes);
    } catch (e) {
      print('Error loading certificate: $e');
    }

    return context;
  }
}

// Alternative: Using package
// lib/core/network/ssl_pinning_interceptor.dart
import 'package:dio/dio.dart';

class SSLPinningInterceptor extends Interceptor {
  final List<String> allowedHosts;
  final List<String> allowedFingerprints;

  SSLPinningInterceptor({
    required this.allowedHosts,
    required this.allowedFingerprints,
  });

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final host = Uri.parse(options.baseUrl).host;

    if (!allowedHosts.contains(host)) {
      return handler.reject(
        DioException(
          requestOptions: options,
          error: 'Host not allowed: $host',
          type: DioExceptionType.badCertificate,
        ),
      );
    }

    handler.next(options);
  }
}
```

#### 3.2 Configuración de Certificados

```yaml
# pubspec.yaml
flutter:
  assets:
    - assets/certificates/

# assets/certificates/README.md
# Certificates

## Obtener certificado del servidor:

```bash
# Opción 1: Usando openssl
openssl s_client -connect api.example.com:443 -showcerts < /dev/null | openssl x509 -outform PEM > cert.pem

# Opción 2: Obtener fingerprint SHA-256
openssl s_client -connect api.example.com:443 < /dev/null 2>/dev/null | openssl x509 -fingerprint -sha256 -noout -in /dev/stdin

# Opción 3: Desde navegador
# Chrome -> DevTools -> Security -> View Certificate -> Details -> Export
```

### 4. Biometric Authentication

#### 4.1 Biometric Service

```dart
// lib/core/security/biometric_service.dart
import 'package:local_auth/local_auth.dart';
import 'package:local_auth/error_codes.dart' as auth_error;
import 'package:injectable/injectable.dart';

@singleton
class BiometricService {
  final LocalAuthentication _auth = LocalAuthentication();

  // Check if device supports biometric authentication
  Future<bool> isDeviceSupported() async {
    try {
      return await _auth.isDeviceSupported();
    } catch (e) {
      print('Error checking device support: $e');
      return false;
    }
  }

  // Check if biometrics are available
  Future<bool> canCheckBiometrics() async {
    try {
      return await _auth.canCheckBiometrics;
    } catch (e) {
      print('Error checking biometrics availability: $e');
      return false;
    }
  }

  // Get available biometric types
  Future<List<BiometricType>> getAvailableBiometrics() async {
    try {
      return await _auth.getAvailableBiometrics();
    } catch (e) {
      print('Error getting available biometrics: $e');
      return [];
    }
  }

  // Authenticate with biometrics
  Future<BiometricAuthResult> authenticate({
    required String localizedReason,
    bool useErrorDialogs = true,
    bool stickyAuth = true,
    bool sensitiveTransaction = false,
  }) async {
    try {
      // Check if device supports biometrics
      final canCheck = await canCheckBiometrics();
      if (!canCheck) {
        return BiometricAuthResult.notAvailable;
      }

      // Get available biometrics
      final availableBiometrics = await getAvailableBiometrics();
      if (availableBiometrics.isEmpty) {
        return BiometricAuthResult.notEnrolled;
      }

      // Authenticate
      final authenticated = await _auth.authenticate(
        localizedReason: localizedReason,
        options: AuthenticationOptions(
          useErrorDialogs: useErrorDialogs,
          stickyAuth: stickyAuth,
          sensitiveTransaction: sensitiveTransaction,
          biometricOnly: true,
        ),
      );

      return authenticated
          ? BiometricAuthResult.success
          : BiometricAuthResult.failure;
    } on PlatformException catch (e) {
      print('Biometric authentication error: ${e.code} - ${e.message}');

      switch (e.code) {
        case auth_error.notAvailable:
          return BiometricAuthResult.notAvailable;
        case auth_error.notEnrolled:
          return BiometricAuthResult.notEnrolled;
        case auth_error.lockedOut:
        case auth_error.permanentlyLockedOut:
          return BiometricAuthResult.lockedOut;
        case auth_error.passcodeNotSet:
          return BiometricAuthResult.passcodeNotSet;
        default:
          return BiometricAuthResult.failure;
      }
    } catch (e) {
      print('Unexpected biometric error: $e');
      return BiometricAuthResult.failure;
    }
  }

  // Authenticate with fallback to PIN/Pattern
  Future<bool> authenticateWithFallback({
    required String localizedReason,
  }) async {
    try {
      return await _auth.authenticate(
        localizedReason: localizedReason,
        options: const AuthenticationOptions(
          useErrorDialogs: true,
          stickyAuth: true,
          biometricOnly: false, // Allow PIN/Pattern fallback
        ),
      );
    } catch (e) {
      print('Authentication with fallback error: $e');
      return false;
    }
  }

  // Stop authentication
  Future<void> stopAuthentication() async {
    try {
      await _auth.stopAuthentication();
    } catch (e) {
      print('Error stopping authentication: $e');
    }
  }

  // Check if Face ID or Touch ID is available (iOS specific)
  Future<bool> isFaceIdAvailable() async {
    final biometrics = await getAvailableBiometrics();
    return biometrics.contains(BiometricType.face);
  }

  Future<bool> isFingerprintAvailable() async {
    final biometrics = await getAvailableBiometrics();
    return biometrics.contains(BiometricType.fingerprint);
  }

  // Get biometric type name for UI
  Future<String> getBiometricTypeName() async {
    final biometrics = await getAvailableBiometrics();

    if (biometrics.contains(BiometricType.face)) {
      return 'Face ID';
    } else if (biometrics.contains(BiometricType.fingerprint)) {
      return 'Touch ID';
    } else if (biometrics.contains(BiometricType.iris)) {
      return 'Iris';
    } else {
      return 'Biometric';
    }
  }
}

enum BiometricAuthResult {
  success,
  failure,
  notAvailable,
  notEnrolled,
  lockedOut,
  passcodeNotSet,
}

extension BiometricAuthResultExtension on BiometricAuthResult {
  String get message {
    switch (this) {
      case BiometricAuthResult.success:
        return 'Authentication successful';
      case BiometricAuthResult.failure:
        return 'Authentication failed';
      case BiometricAuthResult.notAvailable:
        return 'Biometric authentication not available';
      case BiometricAuthResult.notEnrolled:
        return 'No biometric enrolled. Please set up biometric authentication in settings';
      case BiometricAuthResult.lockedOut:
        return 'Too many failed attempts. Please try again later';
      case BiometricAuthResult.passcodeNotSet:
        return 'Please set up a passcode first';
    }
  }

  bool get isSuccess => this == BiometricAuthResult.success;
}
```

#### 4.2 Uso de Biometric Service

```dart
// lib/screens/biometric_login_screen.dart
import 'package:flutter/material.dart';

class BiometricLoginScreen extends StatefulWidget {
  @override
  State<BiometricLoginScreen> createState() => _BiometricLoginScreenState();
}

class _BiometricLoginScreenState extends State<BiometricLoginScreen> {
  final _biometricService = BiometricService();
  String _message = '';

  @override
  void initState() {
    super.initState();
    _checkBiometricSupport();
  }

  Future<void> _checkBiometricSupport() async {
    final isSupported = await _biometricService.isDeviceSupported();
    final canCheck = await _biometricService.canCheckBiometrics();

    if (!isSupported || !canCheck) {
      setState(() {
        _message = 'Biometric authentication not available';
      });
    }
  }

  Future<void> _authenticate() async {
    final result = await _biometricService.authenticate(
      localizedReason: 'Please authenticate to access your account',
      useErrorDialogs: true,
      stickyAuth: true,
      sensitiveTransaction: true,
    );

    setState(() {
      _message = result.message;
    });

    if (result.isSuccess) {
      // Navigate to home screen
      Navigator.pushReplacementNamed(context, '/home');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Biometric Login')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.fingerprint, size: 100),
            SizedBox(height: 32),
            ElevatedButton(
              onPressed: _authenticate,
              child: Text('Authenticate'),
            ),
            SizedBox(height: 16),
            Text(_message),
          ],
        ),
      ),
    );
  }
}
```

### 5. Root/Jailbreak Detection

```dart
// lib/core/security/root_detection.dart
import 'package:flutter_jailbreak_detection/flutter_jailbreak_detection.dart';
import 'package:injectable/injectable.dart';

@singleton
class RootDetectionService {
  // Check if device is jailbroken/rooted
  Future<bool> isDeviceCompromised() async {
    try {
      final isJailbroken = await FlutterJailbreakDetection.jailbroken;
      final isDeveloperMode = await FlutterJailbreakDetection.developerMode;

      return isJailbroken || isDeveloperMode;
    } catch (e) {
      print('Error checking root/jailbreak: $e');
      // En caso de error, asumir que está comprometido (fail-secure)
      return true;
    }
  }

  // Get detailed status
  Future<DeviceSecurityStatus> getDeviceStatus() async {
    try {
      final isJailbroken = await FlutterJailbreakDetection.jailbroken;
      final isDeveloperMode = await FlutterJailbreakDetection.developerMode;

      return DeviceSecurityStatus(
        isJailbroken: isJailbroken,
        isDeveloperMode: isDeveloperMode,
        isSecure: !isJailbroken && !isDeveloperMode,
      );
    } catch (e) {
      print('Error getting device status: $e');
      return DeviceSecurityStatus(
        isJailbroken: true,
        isDeveloperMode: false,
        isSecure: false,
      );
    }
  }

  // Handle compromised device
  void handleCompromisedDevice() {
    // Opciones:
    // 1. Mostrar warning pero permitir continuar
    // 2. Deshabilitar funciones sensibles
    // 3. Bloquear completamente la app
    // 4. Reportar al backend para análisis

    print('⚠️ Device appears to be compromised (rooted/jailbroken)');
  }
}

class DeviceSecurityStatus {
  final bool isJailbroken;
  final bool isDeveloperMode;
  final bool isSecure;

  DeviceSecurityStatus({
    required this.isJailbroken,
    required this.isDeveloperMode,
    required this.isSecure,
  });

  String get message {
    if (isSecure) {
      return 'Device is secure';
    }

    final issues = <String>[];
    if (isJailbroken) issues.add('jailbroken/rooted');
    if (isDeveloperMode) issues.add('developer mode enabled');

    return 'Security warning: ${issues.join(', ')}';
  }
}
```

### 6. API Key Protection

```dart
// lib/core/config/environment.dart
import 'package:flutter_dotenv/flutter_dotenv.dart';

class Environment {
  // Load environment variables
  static Future<void> load() async {
    await dotenv.load(fileName: '.env');
  }

  // API Keys (NEVER hardcode these)
  static String get apiKey => dotenv.env['API_KEY'] ?? '';
  static String get apiSecret => dotenv.env['API_SECRET'] ?? '';
  static String get googleMapsKey => dotenv.env['GOOGLE_MAPS_KEY'] ?? '';

  // Base URLs
  static String get apiBaseUrl => dotenv.env['API_BASE_URL'] ?? 'https://api.example.com';

  // Feature flags
  static bool get enableAnalytics => dotenv.env['ENABLE_ANALYTICS'] == 'true';
  static bool get enableCrashlytics => dotenv.env['ENABLE_CRASHLYTICS'] == 'true';

  // Environment type
  static String get environment => dotenv.env['ENVIRONMENT'] ?? 'development';
  static bool get isProduction => environment == 'production';
  static bool get isDevelopment => environment == 'development';
}

// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Load environment variables
  await Environment.load();

  runApp(MyApp());
}
```

```bash
# .env.example (commit this)
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
GOOGLE_MAPS_KEY=your_google_maps_key_here
API_BASE_URL=https://api.example.com
ENVIRONMENT=development
ENABLE_ANALYTICS=false
ENABLE_CRASHLYTICS=false

# .env (add to .gitignore, NEVER commit)
# Copy .env.example to .env and fill with real values
```

```gitignore
# .gitignore
.env
*.key
*.keystore
*.jks
key.properties
secrets.dart
```

### 7. Network Security

#### 7.1 Secure HTTP Client

```dart
// lib/core/network/secure_http_client.dart
import 'package:dio/dio.dart';
import 'package:injectable/injectable.dart';
import '../security/secure_storage_service.dart';
import 'certificate_pinning.dart';

@singleton
class SecureHttpClient {
  late final Dio _dio;
  final SecureStorageService _secureStorage;

  SecureHttpClient(this._secureStorage) {
    _initializeDio();
  }

  Future<void> _initializeDio() async {
    _dio = await CertificatePinning.createDioWithPinning();

    // Add interceptors
    _dio.interceptors.addAll([
      _AuthInterceptor(_secureStorage),
      _LoggingInterceptor(),
      _ErrorInterceptor(),
    ]);
  }

  Dio get dio => _dio;

  // Convenience methods
  Future<Response<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) =>
      _dio.get<T>(path, queryParameters: queryParameters, options: options);

  Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) =>
      _dio.post<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
}

// Auth Interceptor
class _AuthInterceptor extends Interceptor {
  final SecureStorageService _secureStorage;

  _AuthInterceptor(this._secureStorage);

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Add auth token to requests
    final token = await _secureStorage.getAuthToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }

    // Add security headers
    options.headers['X-App-Version'] = '1.0.0';
    options.headers['X-Platform'] = Platform.operatingSystem;

    handler.next(options);
  }
}

// Logging Interceptor (only in debug)
class _LoggingInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    if (kDebugMode) {
      print('REQUEST[${options.method}] => ${options.uri}');
    }
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    if (kDebugMode) {
      print('RESPONSE[${response.statusCode}] <= ${response.requestOptions.uri}');
    }
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (kDebugMode) {
      print('ERROR[${err.response?.statusCode}] => ${err.requestOptions.uri}');
      print('Message: ${err.message}');
    }
    handler.next(err);
  }
}

// Error Interceptor
class _ErrorInterceptor extends Interceptor {
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    // Handle specific error cases
    switch (err.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        // Handle timeout
        break;
      case DioExceptionType.badCertificate:
        // Certificate pinning failed
        print('❌ Certificate validation failed!');
        break;
      case DioExceptionType.badResponse:
        // Handle HTTP errors
        if (err.response?.statusCode == 401) {
          // Token expired, refresh or logout
        }
        break;
      default:
        break;
    }

    handler.next(err);
  }
}
```

## 🎯 Mejores Prácticas

### 1. Seguridad por Capas (Defense in Depth)

✅ **DO:** Implementa múltiples capas de seguridad
```
Capa 1: Code Obfuscation
Capa 2: Certificate Pinning
Capa 3: Secure Storage
Capa 4: Encryption
Capa 5: Biometric Auth
Capa 6: Root Detection
```

### 2. Principio de Menor Privilegio

✅ **DO:**
```xml
<!-- Android: Solo permisos necesarios -->
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.USE_BIOMETRIC"/>

<!-- iOS: Justificaciones claras -->
<key>NSFaceIDUsageDescription</key>
<string>We use Face ID to securely authenticate you</string>
```

❌ **DON'T:**
```xml
<!-- No pedir permisos innecesarios -->
<uses-permission android:name="android.permission.READ_CONTACTS"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
```

### 3. Secrets Management

✅ **DO:**
- Usar `.env` para configuración
- Secrets en secure storage
- Backend para API keys críticas
- Rotate keys regularmente

❌ **DON'T:**
```dart
// ❌ NUNCA hagas esto
const String API_KEY = 'sk_live_123456789abcdef';
const String SECRET = 'my_secret_password';
```

### 4. OWASP Mobile Top 10

1. **M1: Improper Platform Usage** ✅
   - Usa platform security features
   - Keychain (iOS), KeyStore (Android)

2. **M2: Insecure Data Storage** ✅
   - flutter_secure_storage
   - Nunca guardar secrets en SharedPreferences

3. **M3: Insecure Communication** ✅
   - HTTPS only
   - Certificate pinning
   - TLS 1.2+

4. **M4: Insecure Authentication** ✅
   - Biometric authentication
   - JWT tokens con expiración
   - Refresh tokens

5. **M5: Insufficient Cryptography** ✅
   - AES-256 encryption
   - Secure random number generation
   - No custom crypto algorithms

6. **M6: Insecure Authorization** ✅
   - Validación backend
   - Tokens en headers seguros
   - Role-based access control

7. **M7: Client Code Quality** ✅
   - Code obfuscation
   - Static analysis
   - Linters y code review

8. **M8: Code Tampering** ✅
   - Root/jailbreak detection
   - Signature verification
   - Runtime integrity checks

9. **M9: Reverse Engineering** ✅
   - Obfuscation
   - Native code para lógica crítica
   - No secrets en código

10. **M10: Extraneous Functionality** ✅
    - Remover debug logs en producción
    - Deshabilitar developer tools
    - Clean code antes de release

## 🚨 Troubleshooting

### Error: Certificate Pinning Falla en Debug

```dart
// Deshabilitar pinning solo en debug
if (kDebugMode) {
  // Allow any certificate in debug
  HttpOverrides.global = MyHttpOverrides();
}

class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback = (cert, host, port) => true;
  }
}
```

### Error: Secure Storage Falla en Android

```gradle
// android/app/build.gradle
android {
    defaultConfig {
        minSdkVersion 23  // Requerido para secure storage
    }
}
```

### Error: Biometric No Funciona en Simulador

```dart
// Verificar si es simulador
import 'package:device_info_plus/device_info_plus.dart';

Future<bool> isPhysicalDevice() async {
  final deviceInfo = DeviceInfoPlugin();
  if (Platform.isAndroid) {
    final androidInfo = await deviceInfo.androidInfo;
    return androidInfo.isPhysicalDevice;
  } else if (Platform.isIOS) {
    final iosInfo = await deviceInfo.iosInfo;
    return iosInfo.isPhysicalDevice;
  }
  return true;
}
```

## 📚 Recursos Adicionales

### Documentación Oficial
- [OWASP Mobile Security Testing Guide](https://owasp.org/www-project-mobile-security-testing-guide/)
- [Flutter Security Best Practices](https://docs.flutter.dev/security)
- [Android Security Tips](https://developer.android.com/training/articles/security-tips)
- [iOS Security Guide](https://support.apple.com/guide/security/welcome/web)

### Herramientas
- [MobSF - Mobile Security Framework](https://github.com/MobSF/Mobile-Security-Framework-MobSF)
- [jadx - DEX decompiler](https://github.com/skylot/jadx)
- [Frida - Dynamic instrumentation](https://frida.re/)

### Compliance
- [GDPR Compliance](https://gdpr.eu/)
- [HIPAA Compliance](https://www.hhs.gov/hipaa/index.html)
- [PCI DSS](https://www.pcisecuritystandards.org/)

## 🔗 Skills Relacionados

- [Code Generation](../code-generation/SKILL.md) - DI para security services
- [Firebase](../firebase/SKILL.md) - Firebase Auth y Security Rules
- [Offline-First](../offline-first/SKILL.md) - Secure local storage
- [Testing](../testing/SKILL.md) - Security testing

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,150+
