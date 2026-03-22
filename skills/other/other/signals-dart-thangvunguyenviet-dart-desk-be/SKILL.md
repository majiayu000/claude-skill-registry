---
name: signals-dart
description: "Expert guidance for Signals.dart, a reactive state management library for Dart and Flutter. Use when (1) implementing reactive state with signals, computed values, or effects, (2) working with async signals (FutureSignal, StreamSignal, AsyncState), (3) using Flutter integration (Watch widget, SignalsMixin, hooks), (4) managing reactive collections (ListSignal, MapSignal, SetSignal), (5) migrating from ValueNotifier, Provider, Riverpod, or BLoC to Signals.dart. Triggers include signal, reactive state, computed, effect, Watch widget, SignalsMixin, futureSignal, streamSignal, AsyncState, ListSignal, signals.dart."
---

# Signals.dart

Reactive state management using fine-grained reactive primitives. Works across Dart VM, WASM, Flutter, and server.

## Installation

```bash
# Flutter
flutter pub add signals

# Dart
dart pub add signals
```

```dart
// Dart projects
import 'package:signals/signals.dart';

// Flutter projects (includes ValueNotifier compatibility)
import 'package:signals/signals_flutter.dart';
```

## Core Primitives

### Signal - Reactive State

```dart
final counter = signal(0);
print(counter.value);  // Read
counter.value = 1;     // Write (notifies dependents)
counter.peek();        // Read without tracking
counter.set(value, force: true);  // Force update
```

### Computed - Derived Values

```dart
final name = signal("Jane");
final surname = signal("Doe");
final fullName = computed(() => "${name.value} ${surname.value}");
```

### Effect - Side Effects

```dart
final dispose = effect(() => print(counter.value));
dispose();  // Stop effect

// With cleanup
effect(() {
  print(s.value);
  return () => print('Cleanup');
});
```

**Warning:** Never mutate signals inside effects without `untracked()` - causes infinite loops.

### Untracked and Batch

```dart
// Read without creating dependency
untracked(() => counter.value);

// Batch multiple updates
batch(() {
  name.value = "Foo";
  surname.value = "Bar";
});  // Single notification
```

## Flutter Integration

### Watch Widget (Recommended)

```dart
Watch((context) => Text('Count: ${counter.value}'));

// With child optimization
Watch.builder(
  builder: (context, child) => Column(children: [
    Text('Count: ${counter.value}'),
    child!,  // Doesn't rebuild
  ]),
  child: ExpensiveWidget(),
);
```

### SignalsMixin (Auto-disposal)

```dart
class _MyState extends State<MyWidget> with SignalsMixin {
  late final count = createSignal(0);
  late final isEven = createComputed(() => count.value.isEven);

  @override
  void initState() {
    super.initState();
    createEffect(() => print('Count: ${count.value}'));  // Effects in initState!
  }
}
```

## Async Signals

### FutureSignal

```dart
final data = futureSignal(() async => fetchData());

// With dependencies (re-executes on change)
final data = futureSignal(
  () async => fetchDataFor(id.value),
  dependencies: [id],
);

data.reset();    // Return to initial
data.refresh();  // Keep state, set loading
data.reload();   // Reset to loading with preserved value
```

### AsyncState Pattern Matching

```dart
return switch (data.value) {
  AsyncLoading() => CircularProgressIndicator(),
  AsyncData(:final value) => Text('$value'),
  AsyncError(:final error) => Text('Error: $error'),
};

// Or map()
data.value.map(
  loading: () => CircularProgressIndicator(),
  data: (value) => DataWidget(value),
  error: (err, _) => ErrorWidget(err),
);
```

## Collections

```dart
final list = listSignal([1, 2, 3]);
final map = mapSignal({'a': 1});
final set = setSignal({1, 2, 3});

list.add(4);      // Triggers updates
map['b'] = 2;     // Triggers updates
set.remove(1);    // Triggers updates
```

## Best Practices

1. Use `Watch` widget instead of `.watch(context)`
2. Never mutate signals inside effects without `untracked()`
3. Use `batch()` for multiple updates
4. Put effects in `initState()`, not as late fields
5. Access signal values BEFORE await in `computedAsync()`
6. Prefer `computedFrom()` over `computedAsync()` to avoid await timing issues
7. Always add `debugLabel` to every signal — use the variable name (no class prefix):
   ```dart
   final counter = Signal<int>(0, debugLabel: 'counter');
   final data = FutureSignal(() => fetch(), debugLabel: 'data');
   final items = ListSignal([], debugLabel: 'items');
   late final total = Computed(() => items.value.length, debugLabel: 'total');
   ```

## Reference

For detailed API documentation including Flutter hooks, SignalProvider, ValueNotifier compatibility, async signals detail, collections API, advanced patterns (SignalsContainer, persisted signals, bi-directional flow, SignalsObserver), DI patterns, testing, and migration guides, see [references/api_reference.md](references/api_reference.md).
