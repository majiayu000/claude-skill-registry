---
name: flutter-expert
description: Expert in building cross-platform apps with Flutter 3+. Specializes in Dart, Riverpod, Flame (Game Engine), and FFI (Native Integration).
---

# Flutter Expert

## Purpose

Provides cross-platform mobile development expertise specializing in Flutter 3+, Dart programming, and Riverpod state management. Builds high-fidelity applications for Mobile, Web, and Desktop with advanced rendering optimization (Impeller), custom render objects, and native integrations via FFI and Method Channels.

## When to Use

- Building pixel-perfect cross-platform apps (iOS/Android/Web/Desktop)
- Implementing complex state management (Riverpod/BLoC)
- Optimizing rendering performance (Impeller, Repaint Boundary)
- Developing 2D games (Flame Engine)
- Integrating C/C++/Rust libraries via FFI (Foreign Function Interface)
- Creating custom render objects or shaders (Fragment Shaders)

---
---

## 2. Decision Framework

### State Management Selection

| Pattern | Best For | Complexity | Pros |
|---------|----------|------------|------|
| **Riverpod** | Default Choice | Medium | Compile-time safety, no context dependency, testable. |
| **BLoC/Cubit** | Enterprise | High | Strict event/state separation, great for logging/analytics. |
| **Provider** | Legacy/Simple | Low | Built-in, simple, but relies on BuildContext. |
| **GetX** | Rapid MVP | Low | "Magic" reactive, less boilerplate, but non-standard patterns. |

### Platform Integration Strategy

```
How to talk to Native?
│
├─ **Method Channels (Standard)**
│  ├─ Async calls? → **MethodChannel**
│  └─ Streams? → **EventChannel**
│
├─ **FFI (High Performance)**
│  ├─ C/C++ Library? → **dart:ffi**
│  └─ Rust Library? → **Flutter Rust Bridge**
│
└─ **Platform Views (UI)**
   ├─ Native UI inside Flutter? → **AndroidView / UiKitView**
   └─ Performance Critical? → **Hybrid Composition**
```

### Rendering Engine (Impeller vs Skia)

*   **Impeller (Default iOS):** Predetermined shaders. Zero jank.
*   **Skia (Legacy/Android):** Runtime shader compilation. Can have jank on first run.
*   **Optimization:** Use `RepaintBoundary` to isolate heavy paints (e.g., video players, rotating spinners).

**Red Flags → Escalate to `mobile-developer` (Native):**
- Requirements for App Clips / Instant Apps (Flutter support is limited/heavy)
- Extremely memory-constrained environments (Flutter engine adds ~10-20MB overhead)
- OS-level integrations not yet exposed (e.g., brand new iOS beta features)

---
---

### Workflow 2: Custom Shader (Fragment Program)

**Goal:** Create a visual effect (e.g., pixelation).

**Steps:**

1.  **Shader Code (`shaders/pixelate.frag`)**
    ```glsl
    #include <flutter/runtime_effect.glsl>

    uniform vec2 uSize;
    uniform float uPixels;
    uniform sampler2D uTexture;

    out vec4 fragColor;

    void main() {
        vec2 uv = FlutterFragCoord().xy / uSize;
        vec2 pixelatedUV = floor(uv * uPixels) / uPixels;
        fragColor = texture(uTexture, pixelatedUV);
    }
    ```

2.  **Load & Apply**
    ```dart
    // Load asset
    final program = await FragmentProgram.fromAsset('shaders/pixelate.frag');
    
    // CustomPainter
    void paint(Canvas canvas, Size size) {
      final shader = program.fragmentShader();
      shader.setFloat(0, size.width); // uSize.x
      shader.setFloat(1, size.height); // uSize.y
      shader.setFloat(2, 50.0); // uPixels (50x50 grid)
      
      final paint = Paint()..shader = shader;
      canvas.drawRect(Offset.zero & size, paint);
    }
    ```

---
---

## 4. Patterns & Templates

### Pattern 1: Clean Architecture (Layers)

**Use case:** Scalable enterprise apps.

```
lib/
  domain/       # Entities, Repository Interfaces (Pure Dart)
    entities/
    repositories/
  data/         # Implementations (API, DB)
    datasources/
    repositories/
    models/     # DTOs
  presentation/ # UI, Controllers (Flutter)
    pages/
    widgets/
    controllers/
```

### Pattern 2: Repository Pattern (Riverpod)

**Use case:** Decoupling API from UI.

```dart
@riverpod
AuthRepository authRepository(AuthRepositoryRef ref) {
  return FirebaseAuthImpl(FirebaseAuth.instance);
}

@riverpod
Future<User> currentUser(CurrentUserRef ref) {
  return ref.watch(authRepositoryProvider).getCurrentUser();
}
```

### Pattern 3: Responsive Layout (Adaptive)

**Use case:** Supporting Phone, Tablet, and Desktop.

```dart
class AdaptiveScaffold extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    
    if (width > 900) {
      return Row(children: [NavRail(), Expanded(child: Body())]);
    } else {
      return Scaffold(
        drawer: Drawer(),
        body: Body(),
        bottomNavigationBar: BottomNavBar(),
      );
    }
  }
}
```

---
---

## 6. Integration Patterns

### **backend-developer:**
-   **Handoff**: Backend provides Swagger/OpenAPI → Flutter Expert uses `openapi_generator` to build Dart clients.
-   **Collaboration**: Handling JWT refresh tokens (interceptors).
-   **Tools**: Dio Interceptors.

### **mobile-developer:**
-   **Handoff**: Native dev writes Swift/Kotlin plugin → Flutter Expert wraps it in Method Channel.
-   **Collaboration**: Debugging platform-specific crashes (Xcode/Android Studio).
-   **Tools**: Pigeon (Type-safe interop).

### **ui-designer:**
-   **Handoff**: Designer provides Rive animation (`.riv`) → Flutter Expert integrates via `rive` package.
-   **Collaboration**: Implementing custom Painter for non-standard shapes.
-   **Tools**: Rive, Flutter Shape Maker.

---
