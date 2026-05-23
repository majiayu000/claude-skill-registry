---
description: "Flutter performance: DevTools profiling, widget optimization, memory management, const widgets. Use when optimizing render performance or debugging jank."
version: "1.0.0"
updated: "2026-01-07"
---

# Flutter Performance

## Commands

```bash
flutter run --profile  # Required for profiling
flutter pub global run devtools
```

## Targets

| Target | Threshold |
|--------|-----------|
| 60 FPS | 16.67ms/frame |
| Cold start | < 2s |

## Widget Optimization

### Const Constructors
```dart
// GOOD
const Column(children: [Text('Static'), Icon(Icons.star)])
```

### Extract Widgets
```dart
// GOOD: Only counter rebuilds
Column(
  children: [
    const ExpensiveWidget(),  // no rebuild
    _Counter(),               // isolated state
  ],
)
```

### RepaintBoundary
```dart
RepaintBoundary(child: AnimatedWidget())
```

## Build Optimization

```dart
// BAD: compute in build
final sorted = items..sort();

// GOOD: compute once
late List<Item> _sorted;
void initState() { _sorted = items..sort(); }
```

## Memory Management

```dart
@override
void dispose() {
  _animController.dispose();
  _textController.dispose();
  _subscription?.cancel();
  super.dispose();
}

// Check mounted
if (!mounted) return;
setState(() => _data = data);
```

## Lists

```dart
// Use builder
ListView.builder(itemCount: items.length, itemBuilder: ...)

// Fixed extent
ListView.builder(itemExtent: 72, ...)

// Keys
ValueKey(item.id)
```

## Images

```dart
CachedNetworkImage(
  imageUrl: url,
  memCacheWidth: 200,
  memCacheHeight: 200,
)
```

## Checklist
- [ ] Profiled in profile mode
- [ ] No expensive ops in build()
- [ ] Const constructors used
- [ ] ListView.builder for lists
- [ ] Controllers disposed
- [ ] Check mounted before setState

## Related Skills
- **flutter-animations**: Animation performance
- **flutter-code-quality**: Static analysis
