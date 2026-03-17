---
name: flutter-performance-docs
description: "[Flutter] Flutter performance best practices and optimization guide. Build cost, rendering, lists, animations, and anti-patterns. (project)"
---

# Flutter Performance Best Practices

## The 16ms Rule

| Display | Frame Budget | Build | Render |
|---------|--------------|-------|--------|
| 60Hz | 16ms | ~8ms | ~8ms |
| 120Hz | 8ms | ~4ms | ~4ms |

Always profile in **profile mode**, not debug mode.

---

## 1. Control build() Cost

### Split Large Widgets
```dart
// BAD: Monolithic widget
class MyPage extends StatelessWidget {
  Widget build(context) => Column(children: [header, content, footer]);
}

// GOOD: Split into smaller widgets
class MyPage extends StatelessWidget {
  Widget build(context) => Column(children: [
    HeaderWidget(),
    ContentWidget(),
    FooterWidget(),
  ]);
}
```

### Localize setState()
```dart
// BAD: setState high in tree
class Parent extends StatefulWidget {
  void update() => setState(() {}); // Rebuilds entire subtree
}

// GOOD: setState only where needed
class Child extends StatefulWidget {
  void update() => setState(() {}); // Only rebuilds this widget
}
```

### Use const Constructors
```dart
// GOOD: Flutter skips rebuild for const widgets
const Text('Hello');
const SizedBox(height: 16);
const MyCustomWidget();
```

### Prefer StatelessWidget Over Functions
```dart
// BAD: Function returns widget
Widget buildHeader() => Container(...);

// GOOD: StatelessWidget (enables const, better rebuild tracking)
class Header extends StatelessWidget {
  const Header();
  Widget build(context) => Container(...);
}
```

---

## 2. Lists & Grids

### Use Lazy Builders
```dart
// BAD: Builds all items at once
ListView(children: items.map((i) => ItemWidget(i)).toList())

// GOOD: Only builds visible items
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
)
```

### Avoid Intrinsic Passes
Intrinsic passes poll all cells for sizing - expensive for large grids.

```dart
// BAD: Causes intrinsic pass
IntrinsicHeight(child: Row(children: [...]))

// GOOD: Fixed sizes
SizedBox(height: 100, child: Row(children: [...]))
```

**Debug:** Enable "Track layouts" in DevTools to see intrinsic timeline events.

---

## 3. Minimize saveLayer()

`saveLayer()` allocates offscreen buffer - expensive!

### Widgets That Trigger saveLayer()
- `ShaderMask`
- `ColorFilter`
- `Chip` (if `disabledColorAlpha != 0xff`)
- `Text` (with `overflowShader`)

### Debug
Enable `PerformanceOverlayLayer.checkerboardOffscreenLayers` in DevTools.

---

## 4. Opacity & Clipping

### Opacity
```dart
// BAD: Wraps widget in Opacity
Opacity(opacity: 0.5, child: Image(...))

// GOOD: Apply directly to image
Image(..., color: Colors.white.withOpacity(0.5), colorBlendMode: BlendMode.modulate)

// GOOD: For text, use semitransparent color
Text('Hello', style: TextStyle(color: Colors.black54))

// GOOD: For animations
AnimatedOpacity(opacity: _visible ? 1.0 : 0.0, child: ...)
FadeInImage(placeholder: ..., image: ...)
```

### Clipping
```dart
// BAD: Explicit clipping
ClipRRect(borderRadius: BorderRadius.circular(8), child: Container(...))

// GOOD: Use decoration borderRadius
Container(
  decoration: BoxDecoration(borderRadius: BorderRadius.circular(8)),
  child: ...
)
```

Default is `Clip.none` - enable clipping only when needed.

---

## 5. Animations

### TransitionBuilder Pattern
```dart
// BAD: Rebuilds everything
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) => Transform.rotate(
    angle: _controller.value,
    child: ExpensiveWidget(), // Rebuilt every frame!
  ),
)

// GOOD: Child is not rebuilt
AnimatedBuilder(
  animation: _controller,
  child: ExpensiveWidget(), // Built once
  builder: (context, child) => Transform.rotate(
    angle: _controller.value,
    child: child, // Reused
  ),
)
```

### Pre-clip Images for Animation
```dart
// BAD: Clips during animation
AnimatedBuilder(
  builder: (_, __) => ClipRRect(
    borderRadius: BorderRadius.circular(8),
    child: Image(...),
  ),
)

// GOOD: Pre-clipped image
final clippedImage = ClipRRect(
  borderRadius: BorderRadius.circular(8),
  child: Image(...),
);
AnimatedBuilder(
  child: clippedImage,
  builder: (_, child) => Transform.scale(scale: _scale, child: child),
)
```

---

## 6. String Concatenation

```dart
// BAD: Creates intermediate strings
String result = '';
for (var item in items) {
  result += item.toString(); // O(n²)
}

// GOOD: Single concatenation
final buffer = StringBuffer();
for (var item in items) {
  buffer.write(item.toString());
}
final result = buffer.toString(); // O(n)
```

---

## Anti-Patterns Summary

| Anti-Pattern | Solution |
|--------------|----------|
| `Opacity` widget in animations | `AnimatedOpacity`, `FadeInImage` |
| `ListView(children: [...])` | `ListView.builder()` |
| `ClipRRect` in animations | Pre-clip before animating |
| Override `operator ==` on Widget | Only for leaf widgets with efficient comparison |
| Large monolithic widgets | Split into smaller widgets |
| `setState()` high in tree | Localize to affected subtree |
| `IntrinsicHeight/Width` | Fixed sizes or custom `RenderObject` |

---

## Debugging Tools

| Tool | Purpose |
|------|---------|
| DevTools Performance View | Timeline, frame analysis |
| DevTools Inspector | Track widget rebuilds |
| "Track layouts" option | Find intrinsic passes |
| `checkerboardOffscreenLayers` | Find saveLayer calls |
| Profile mode build | Accurate performance measurement |

---

## Mobile: Use Impeller

Impeller is Flutter's default graphics renderer. Eliminates shader compilation jank.

```bash
# Verify Impeller is enabled (default on iOS/Android)
flutter run --enable-impeller
```

---

## Official Docs
- [Performance best practices](https://docs.flutter.dev/perf/best-practices)
- [Rendering performance](https://docs.flutter.dev/perf/rendering-performance)
- [DevTools Performance View](https://docs.flutter.dev/tools/devtools/performance)
