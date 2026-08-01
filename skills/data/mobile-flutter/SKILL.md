---
name: mobile-flutter
description: '> Flutter/Dart best practices ve performance optimization.'
---

---
name: mobile_flutter
router_kit: FullStackKit
description: Flutter/Dart best practices, Riverpod state management ve performance optimization.
metadata:
  skillport:
    category: development
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, mobile flutter, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - mobile-react-native
---

# 🐦 Mobile Flutter

> Flutter/Dart best practices ve performance optimization.

---

## 📁 1. Proje Yapısı (Feature-First)

```
lib/
├── core/
│   ├── theme/
│   └── widgets/
├── features/
│   ├── auth/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   └── home/
├── services/
└── main.dart
```

---

## 🧩 2. Widget Best Practices

```dart
// ✅ const constructor kullan
class MyButton extends StatelessWidget {
  const MyButton({super.key, required this.onPressed});
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(onPressed: onPressed, child: Text('Click'));
  }
}

// ✅ const widget'ları işaretle
const SizedBox(height: 16),
```

---

## 📦 3. State (Riverpod)

```dart
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.watch(authRepositoryProvider));
});

class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier(this._repo) : super(const AuthState());

  Future<void> login(String email, String password) async {
    state = state.copyWith(isLoading: true);
    final user = await _repo.login(email, password);
    state = state.copyWith(user: user, isLoading: false);
  }
}
```

---

## ⚡ 4. Performance

```dart
// ✅ ListView.builder (lazy loading)
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemCard(item: items[index]),
)

// ✅ RepaintBoundary
RepaintBoundary(child: ExpensiveWidget())

// ✅ Isolate for CPU-heavy
final result = await compute(parseUsers, jsonString);
```

---

## 🔐 5. Secure Storage

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

final storage = FlutterSecureStorage();
await storage.write(key: 'token', value: token);
final token = await storage.read(key: 'token');
```

---

## 📱 6. Responsive

```dart
// MediaQuery
final isTablet = MediaQuery.of(context).size.width > 600;

// LayoutBuilder
LayoutBuilder(
  builder: (context, constraints) {
    return constraints.maxWidth > 600 ? WideLayout() : NarrowLayout();
  },
)
```

---

*Mobile Flutter v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Flutter Engineering Best Practices](https://docs.flutter.dev/perf/best-practices) & [Riverpod Architecture](https://riverpod.dev/docs/concepts/about_code_generation)

### Aşama 1: Architecture Setup
- [ ] **Layering**: Feature-First yapısını kur (Presentation, Domain, Data).
- [ ] **State Management**: Riverpod `NotifierProvider` ve Code Generation (@riverpod) kullan.
- [ ] **Routing**: GoRouter ile type-safe navigasyon ve deep linking yapılandır.

### Aşama 2: Implementation
- [ ] **UI**: `const` constructorları kullanarak rebuild'leri minimize et.
- [ ] **Network**: Dio ve Retrofit ile API katmanını (Interceptor, Error Handling) yaz.
- [ ] **Storage**: Hassas veriler için `flutter_secure_storage`, cache için `Isar` veya `Hive` kullan.

### Aşama 3: Release & Quality
- [ ] **Testing**: Unit, Widget ve Integration testlerini (Golden Tests dahir) yaz.
- [ ] **Performance**: DevTools ile "Jank" (kare atlama) analizi yap (Shader compilation warm-up).
- [ ] **CI/CD**: Fastlane ile otomatik build ve store upload süreçlerini kur.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Business logic UI'dan (Widget'lardan) tamamen ayrılmış mı? |
| 2 | App cold start süresi <2 saniye mi? |
| 3 | Farklı ekran boyutlarında (Tablet/Foldable) responsive davranıyor mu? |
