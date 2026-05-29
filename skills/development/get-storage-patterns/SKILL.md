---
name: "GetStorage Patterns"
description: "Local storage with GetStorage for preferences, caching, and offline-first patterns"
version: "1.0.0"
---

# GetStorage Patterns

## Initialization

```dart
// main.dart
void main() async {
  await GetStorage.init();
  runApp(MyApp());
}
```

## Storage Service Pattern

```dart
class StorageService {
  final GetStorage _box;
  
  StorageService() : _box = GetStorage();
  
  // Token management
  String? get token => _box.read<String>('auth_token');
  Future<void> setToken(String token) => _box.write('auth_token', token);
  Future<void> clearToken() => _box.remove('auth_token');
  
  // User data
  Map<String, dynamic>? get userData => _box.read<Map<String, dynamic>>('user_data');
  Future<void> setUserData(Map<String, dynamic> data) => _box.write('user_data', data);
  
  // Preferences
  bool get isDarkMode => _box.read<bool>('dark_mode') ?? false;
  Future<void> setDarkMode(bool value) => _box.write('dark_mode', value);
  
  String get locale => _box.read<String>('locale') ?? 'en';
  Future<void> setLocale(String locale) => _box.write('locale', locale);
  
  // Clear all
  Future<void> clearAll() => _box.erase();
  
  // Listen to changes
  void listenKey(String key, Function(dynamic) callback) {
    _box.listenKey(key, callback);
  }
}
```

## Local Data Source Pattern

```dart
class UserLocalDataSource {
  final GetStorage _storage;
  static const String _usersKey = 'cached_users';
  static const String _userKeyPrefix = 'cached_user_';
  static const Duration _cacheDuration = Duration(hours: 24);
  
  UserLocalDataSource(this._storage);
  
  Future<void> cacheUser(UserModel user) async {
    final cacheData = {
      'user': user.toJson(),
      'timestamp': DateTime.now().toIso8601String(),
    };
    await _storage.write('$_userKeyPrefix${user.id}', cacheData);
  }
  
  Future<UserModel?> getCachedUser(String id) async {
    final cacheData = _storage.read<Map<String, dynamic>>('$_userKeyPrefix$id');
    
    if (cacheData == null) return null;
    
    // Check cache expiration
    final timestamp = DateTime.parse(cacheData['timestamp']);
    if (DateTime.now().difference(timestamp) > _cacheDuration) {
      await _storage.remove('$_userKeyPrefix$id');
      return null;
    }
    
    return UserModel.fromJson(cacheData['user']);
  }
  
  Future<void> cacheUsers(List<UserModel> users) async {
    final cacheData = {
      'users': users.map((u) => u.toJson()).toList(),
      'timestamp': DateTime.now().toIso8601String(),
    };
    await _storage.write(_usersKey, cacheData);
  }
  
  Future<List<UserModel>?> getCachedUsers() async {
    final cacheData = _storage.read<Map<String, dynamic>>(_usersKey);
    
    if (cacheData == null) return null;
    
    final timestamp = DateTime.parse(cacheData['timestamp']);
    if (DateTime.now().difference(timestamp) > _cacheDuration) {
      await _storage.remove(_usersKey);
      return null;
    }
    
    final List<dynamic> usersList = cacheData['users'];
    return usersList.map((json) => UserModel.fromJson(json)).toList();
  }
  
  Future<void> clearCache() async {
    await _storage.erase();
  }
}
```

## GetX Service Integration

```dart
class CacheService extends GetxService {
  final GetStorage _storage;
  
  CacheService() : _storage = GetStorage();
  
  Future<CacheService> init() async {
    await GetStorage.init();
    return this;
  }
  
  // Reactive cache
  final _cachedData = <String, dynamic>{}.obs;
  
  T? get<T>(String key) {
    return _storage.read<T>(key);
  }
  
  Future<void> put<T>(String key, T value, {Duration? expiry}) async {
    if (expiry != null) {
      final expiryData = {
        'value': value,
        'expiry': DateTime.now().add(expiry).toIso8601String(),
      };
      await _storage.write(key, expiryData);
    } else {
      await _storage.write(key, value);
    }
    _cachedData[key] = value;
  }
  
  Future<void> remove(String key) async {
    await _storage.remove(key);
    _cachedData.remove(key);
  }
  
  bool has(String key) {
    return _storage.hasData(key);
  }
}
```

## Best Practices

- Initialize GetStorage before running app
- Use type-safe reads (`read<String>`, `read<int>`, etc.)
- Implement cache expiration for time-sensitive data
- Clear cache on logout
- Use separate keys for different data types
- Listen to changes for reactive updates
