---
name: project-secure-storage
description: Guide for storing secrets securely using app_secure_storage package with platform-native storage (project)
---

# Flutter Secure Storage Skill

This skill guides the implementation of secure storage for sensitive user data using the `app_secure_storage` package.

## When to Use

Trigger this skill when:
- Storing API tokens, passwords, or encryption keys
- Managing user authentication credentials
- Saving sensitive configuration data
- **Storing third-party API keys** (OpenAI, Stripe, Firebase, etc.) - **MUST use secure storage**
- User asks to "store secret", "save token", "secure storage", "keychain", "save credentials"

**IMPORTANT**: Third-party API keys and secrets **MUST** be stored using `app_secure_storage`. Never store API keys in:
- SharedPreferences (not encrypted)
- Database (not designed for secrets)
- Environment variables bundled in app (can be extracted)
- Hardcoded strings (visible in binary)

## Package Import

```dart
import 'package:app_secure_storage/app_secure_storage.dart';
```

## Platform Storage Mechanisms

| Platform | Storage Backend |
|----------|-----------------|
| iOS | Keychain Services |
| macOS | Keychain Services |
| Android | EncryptedSharedPreferences (AES-GCM) |
| Linux | libsecret (GNOME Keyring / KWallet) |
| Windows | Credential Manager |

## Accessing the Vault

The `VaultRepository` is injected via `MainProvider` and available throughout the app:

```dart
import 'package:app_secure_storage/app_secure_storage.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

// In any widget with access to BuildContext
final vault = context.read<VaultRepository>();
```

## Basic Operations

### Store a Secret

```dart
await vault.write(key: 'api_token', value: 'your-secret-token');
await vault.write(key: 'refresh_token', value: 'refresh-token-value');
```

### Read a Secret

```dart
final token = await vault.read(key: 'api_token');
if (token != null) {
  // Use the token for API authentication
  headers['Authorization'] = 'Bearer $token';
}
```

### Check if Key Exists

```dart
final hasToken = await vault.containsKey(key: 'api_token');
if (!hasToken) {
  // Redirect to login
  context.goNamed('login');
}
```

### Delete a Secret

```dart
await vault.delete(key: 'api_token');
```

### Delete All Secrets

```dart
await vault.deleteAll();
```

### Read All Secrets

```dart
final allSecrets = await vault.readAll();
// Returns Map<String, String>
for (final entry in allSecrets.entries) {
  print('Key: ${entry.key}');
}
```

## Using Namespaces

Namespaces prevent key collisions between features and allow scoped deletion:

```dart
// In main.dart - create namespaced vaults
final authVault = SecureStorageVaultRepository(namespace: 'auth');
final apiVault = SecureStorageVaultRepository(namespace: 'api');

// Keys are automatically prefixed internally
await authVault.write(key: 'access_token', value: 'jwt-token');
// Actually stored as 'auth_access_token'

await apiVault.write(key: 'key', value: 'api-key-123');
// Actually stored as 'api_key'

// Scoped deletion - only deletes keys with 'auth_' prefix
await authVault.deleteAll();
```

## Complete Example: Third-Party API Keys

When integrating third-party services (OpenAI, Stripe, Google Maps, etc.), always store API keys securely:

```dart
class ApiKeyService {
  final VaultRepository _vault;

  ApiKeyService(this._vault);

  // Key constants for third-party services
  static const _openAiKeyKey = 'openai_api_key';
  static const _stripeKeyKey = 'stripe_publishable_key';
  static const _googleMapsKeyKey = 'google_maps_api_key';

  // OpenAI
  Future<void> saveOpenAiKey(String apiKey) async {
    await _vault.write(key: _openAiKeyKey, value: apiKey);
  }

  Future<String?> getOpenAiKey() async {
    return _vault.read(key: _openAiKeyKey);
  }

  Future<bool> hasOpenAiKey() async {
    return _vault.containsKey(key: _openAiKeyKey);
  }

  Future<void> deleteOpenAiKey() async {
    await _vault.delete(key: _openAiKeyKey);
  }

  // Generic method for any third-party service
  Future<void> saveApiKey({
    required String service,
    required String apiKey,
  }) async {
    await _vault.write(key: '${service}_api_key', value: apiKey);
  }

  Future<String?> getApiKey({required String service}) async {
    return _vault.read(key: '${service}_api_key');
  }
}

// Usage in widget
class SettingsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final vault = context.read<VaultRepository>();
    final apiKeyService = ApiKeyService(vault);

    return ListTile(
      title: const Text('OpenAI API Key'),
      subtitle: FutureBuilder<bool>(
        future: apiKeyService.hasOpenAiKey(),
        builder: (context, snapshot) {
          final hasKey = snapshot.data ?? false;
          return Text(hasKey ? 'Configured' : 'Not configured');
        },
      ),
      onTap: () => _showApiKeyDialog(context, apiKeyService),
    );
  }

  void _showApiKeyDialog(BuildContext context, ApiKeyService service) {
    final controller = TextEditingController();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Enter OpenAI API Key'),
        content: TextField(
          controller: controller,
          obscureText: true,
          decoration: const InputDecoration(
            hintText: 'sk-...',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () async {
              await service.saveOpenAiKey(controller.text);
              if (context.mounted) {
                Navigator.pop(context);
              }
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }
}
```

## Complete Example: Authentication Service

```dart
class AuthService {
  final VaultRepository _vault;

  AuthService(this._vault);

  static const _accessTokenKey = 'access_token';
  static const _refreshTokenKey = 'refresh_token';
  static const _userIdKey = 'user_id';

  Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
    required String userId,
  }) async {
    await Future.wait([
      _vault.write(key: _accessTokenKey, value: accessToken),
      _vault.write(key: _refreshTokenKey, value: refreshToken),
      _vault.write(key: _userIdKey, value: userId),
    ]);
  }

  Future<String?> getAccessToken() async {
    return _vault.read(key: _accessTokenKey);
  }

  Future<String?> getRefreshToken() async {
    return _vault.read(key: _refreshTokenKey);
  }

  Future<bool> isLoggedIn() async {
    return _vault.containsKey(key: _accessTokenKey);
  }

  Future<void> logout() async {
    await Future.wait([
      _vault.delete(key: _accessTokenKey),
      _vault.delete(key: _refreshTokenKey),
      _vault.delete(key: _userIdKey),
    ]);
  }
}
```

## Complete Example: Login Screen

```dart
class LoginScreen extends StatefulWidget {
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool _isLoading = false;

  Future<void> _handleLogin(String email, String password) async {
    setState(() => _isLoading = true);

    try {
      // Call your API
      final response = await api.login(email: email, password: password);

      // Store tokens securely
      final vault = context.read<VaultRepository>();
      await vault.write(key: 'access_token', value: response.accessToken);
      await vault.write(key: 'refresh_token', value: response.refreshToken);

      if (mounted) {
        context.goNamed('home');
      }
    } catch (e) {
      if (mounted) {
        showErrorToast(
          context: context,
          message: 'Login failed: ${e.toString()}',
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    // ... login form UI
  }
}
```

## Complete Example: Auto-Login Check

```dart
class SplashScreen extends StatefulWidget {
  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _checkAuth();
  }

  Future<void> _checkAuth() async {
    final vault = context.read<VaultRepository>();
    final hasToken = await vault.containsKey(key: 'access_token');

    if (!mounted) return;

    if (hasToken) {
      // Validate token is still valid
      final token = await vault.read(key: 'access_token');
      if (token != null && _isTokenValid(token)) {
        context.goNamed('home');
      } else {
        // Token expired, clear and go to login
        await vault.deleteAll();
        context.goNamed('login');
      }
    } else {
      context.goNamed('login');
    }
  }

  bool _isTokenValid(String token) {
    // Check JWT expiration or validate with server
    return true;
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: CircularProgressIndicator()),
    );
  }
}
```

## Testing with Mock Repository

```dart
class MockVaultRepository implements VaultRepository {
  final Map<String, String> _storage = {};

  @override
  Future<void> write({required String key, required String value}) async {
    _storage[key] = value;
  }

  @override
  Future<String?> read({required String key}) async {
    return _storage[key];
  }

  @override
  Future<void> delete({required String key}) async {
    _storage.remove(key);
  }

  @override
  Future<bool> containsKey({required String key}) async {
    return _storage.containsKey(key);
  }

  @override
  Future<void> deleteAll() async {
    _storage.clear();
  }

  @override
  Future<Map<String, String>> readAll() async {
    return Map.from(_storage);
  }
}

// In tests
void main() {
  testWidgets('stores token on login', (tester) async {
    final mockVault = MockVaultRepository();

    await tester.pumpWidget(
      RepositoryProvider<VaultRepository>.value(
        value: mockVault,
        child: const MaterialApp(home: LoginScreen()),
      ),
    );

    // Perform login actions...

    // Verify token was stored
    expect(await mockVault.containsKey(key: 'access_token'), isTrue);
  });
}
```

## Error Handling

Always handle potential storage errors:

```dart
Future<void> saveToken(String token) async {
  try {
    await vault.write(key: 'api_token', value: token);
  } on PlatformException catch (e) {
    // Handle platform-specific errors
    // e.g., Keychain access denied on iOS
    logger.e('Failed to save token: ${e.message}');
    rethrow;
  } catch (e) {
    logger.e('Unexpected error saving token: $e');
    rethrow;
  }
}
```

## Platform Setup Requirements

### iOS
Add to `ios/Runner/DebugProfile.entitlements` and `ios/Runner/Release.entitlements`:
```xml
<key>keychain-access-groups</key>
<array/>
```

### macOS
Add to `macos/Runner/DebugProfile.entitlements` and `macos/Runner/Release.entitlements`:
```xml
<key>keychain-access-groups</key>
<array/>
```

### Android
Disable auto backup in `AndroidManifest.xml` to prevent key errors:
```xml
<application android:allowBackup="false" ...>
```

### Linux
Install dependencies:
```bash
sudo apt-get install libsecret-1-dev libjsoncpp-dev
```

See `app_lib/secure_storage/README.md` for complete platform setup instructions.

## Best Practices

1. **Use meaningful key names** - e.g., `auth_access_token`, `api_refresh_token`
2. **Use namespaces** for logical grouping and scoped deletion
3. **Delete secrets on logout** - don't leave credentials after user logs out
4. **Handle errors gracefully** - storage can fail (permissions, keyring unavailable)
5. **Check `mounted`** before updating UI after async operations
6. **Validate tokens** - check expiration before using stored tokens
7. **Don't log secrets** - never print token values to console
8. **Use parallel writes** with `Future.wait` for multiple secrets
9. **Test with mocks** - use `MockVaultRepository` for unit tests

## API Reference

### VaultRepository Interface

| Method | Returns | Description |
|--------|---------|-------------|
| `write({key, value})` | `Future<void>` | Store a secret |
| `read({key})` | `Future<String?>` | Read a secret (null if not found) |
| `delete({key})` | `Future<void>` | Delete a secret |
| `containsKey({key})` | `Future<bool>` | Check if key exists |
| `deleteAll()` | `Future<void>` | Delete all secrets |
| `readAll()` | `Future<Map<String, String>>` | Get all secrets |

### SecureStorageVaultRepository Constructor

| Parameter | Type | Description |
|-----------|------|-------------|
| `storage` | `FlutterSecureStorage?` | Custom storage instance (optional) |
| `namespace` | `String?` | Key prefix for scoped storage (optional) |
