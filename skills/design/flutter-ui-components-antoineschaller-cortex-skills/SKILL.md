---
description: "Flutter UI patterns: widget composition, Material 3, builder patterns, slots. Use when building reusable widgets or implementing complex UIs."
version: "1.0.0"
updated: "2026-01-07"
---

# Flutter UI Components

## Widget Types

### StatelessWidget (Default)
```dart
class EventCard extends StatelessWidget {
  final Event event;
  const EventCard({super.key, required this.event});

  @override
  Widget build(BuildContext context) {
    return Card(child: Text(event.title));
  }
}
```

### ConsumerWidget (Riverpod)
```dart
class EventsListView extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return ref.watch(eventsNotifierProvider).when(
      data: (events) => ListView.builder(...),
      loading: () => const CircularProgressIndicator(),
      error: (e, _) => ErrorWidget(error: e),
    );
  }
}
```

## Composition Patterns

### Slot Pattern
```dart
class PageScaffold extends StatelessWidget {
  final Widget title;
  final Widget body;
  final Widget? floatingActionButton;

  const PageScaffold({required this.title, required this.body, this.floatingActionButton});
}
```

### Builder Pattern
```dart
class DataList<T> extends StatelessWidget {
  final List<T> items;
  final Widget Function(BuildContext, T) itemBuilder;
}
```

## Material 3

### Cards
```dart
Card(
  elevation: 0,
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(12),
    side: BorderSide(color: Theme.of(context).colorScheme.outlineVariant),
  ),
)
```

### Buttons
```dart
FilledButton(onPressed: _submit, child: const Text('Submit'))
OutlinedButton(onPressed: _cancel, child: const Text('Cancel'))
IconButton(onPressed: _refresh, icon: const Icon(Icons.refresh), tooltip: 'Refresh')
```

## Performance

```dart
// Use const
const SizedBox(height: 16)

// Keys for lists
ValueKey(items[i].id)

// Extract rebuild-prone widgets
const ExpensiveWidget()
```

## Related Skills
- **flutter-accessibility**: A11y requirements
- **flutter-theming**: Theme customization
- **flutter-performance**: Optimization
