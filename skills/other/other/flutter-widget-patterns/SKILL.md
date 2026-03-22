---
name: flutter-widget-patterns
description: Flutter widget composition patterns — Stateless vs Stateful, widget decomposition, keys, const constructors, BuildContext, InheritedWidget, and Builder
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[widget file or pattern question]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: flutter, widgets, patterns
---

# Flutter Widget Patterns

## Overview

Reference guide for idiomatic Flutter widget design in Dart. Apply these patterns when building, reviewing, or refactoring widgets to ensure correct rebuilds, good performance, and maintainable widget trees.

## Stateless vs Stateful Decision Tree

```
Does the widget...
├── Need to change after initial build?
│   ├── NO → StatelessWidget ✓
│   └── YES → Does the change come from...
│       ├── Parent rebuilding with new props? → StatelessWidget ✓
│       ├── Internal state (counter, toggle, animation)?
│       │   └── YES → StatefulWidget ✓
│       ├── AnimationController or TickerProvider?
│       │   └── YES → StatefulWidget with TickerProviderStateMixin ✓
│       └── Global/shared state (theme, auth, data)?
│           └── Use state management (Provider/Riverpod) ✓
```

### StatelessWidget

```dart
class UserAvatar extends StatelessWidget {
  const UserAvatar({
    super.key,
    required this.imageUrl,
    this.radius = 24.0,
  });

  final String imageUrl;
  final double radius;

  @override
  Widget build(BuildContext context) {
    return CircleAvatar(
      radius: radius,
      backgroundImage: NetworkImage(imageUrl),
    );
  }
}
```

### StatefulWidget

```dart
class ExpandableCard extends StatefulWidget {
  const ExpandableCard({
    super.key,
    required this.title,
    required this.content,
  });

  final String title;
  final Widget content;

  @override
  State<ExpandableCard> createState() => _ExpandableCardState();
}

class _ExpandableCardState extends State<ExpandableCard> {
  bool _isExpanded = false;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        GestureDetector(
          onTap: () => setState(() => _isExpanded = !_isExpanded),
          child: Text(widget.title),
        ),
        if (_isExpanded) widget.content,
      ],
    );
  }
}
```

## Widget Decomposition

### When to Extract a Widget

Extract a widget when:
1. The build method exceeds **50 lines**
2. A subtree is **reused** in 2+ places
3. A subtree has its **own state**
4. You want to limit the **rebuild scope** (extracted widgets only rebuild when their inputs change)

### Extract as Widget, Not Method

```dart
// BAD: Helper method — rebuilds with parent, no independent lifecycle
class MyPage extends StatelessWidget {
  Widget _buildHeader(String title) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Text(title, style: const TextStyle(fontSize: 24)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(children: [_buildHeader('Hello')]);
  }
}

// GOOD: Extracted widget — independent rebuild, can be const
class PageHeader extends StatelessWidget {
  const PageHeader({super.key, required this.title});
  final String title;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Text(title, style: const TextStyle(fontSize: 24)),
    );
  }
}
```

## Keys

### When to Use Each Key Type

```
Do I need a key?
├── Static list (never reordered/filtered)? → No key needed
├── Dynamic list with unique domain IDs?
│   └── ValueKey(item.id) ✓
├── Dynamic list without unique IDs but with unique field combo?
│   └── ValueKey('${item.name}_${item.date}') ✓
├── Need to preserve state when widget moves in tree?
│   └── GlobalKey (sparingly) ✓
├── Need every instance to be unique?
│   └── UniqueKey() (forces rebuild, rarely needed)
└── Objects with proper == and hashCode?
    └── ObjectKey(item) ✓
```

```dart
// GOOD: ValueKey with stable ID
ListView.builder(
  itemCount: tasks.length,
  itemBuilder: (context, index) {
    final task = tasks[index];
    return TaskTile(
      key: ValueKey(task.id), // Stable across reorders
      task: task,
      onToggle: () => toggleTask(task.id),
    );
  },
);

// BAD: Using index as key — breaks when list reorders
key: ValueKey(index) // WRONG for reorderable lists
```

### GlobalKey — Use Sparingly

```dart
// Accessing State from outside the widget
final formKey = GlobalKey<FormState>();

Form(
  key: formKey,
  child: Column(children: [/* fields */]),
);

// Validate from parent
if (formKey.currentState?.validate() ?? false) {
  formKey.currentState!.save();
}
```

## Const Constructors for Performance

Mark widgets as `const` when all fields are compile-time constants. Const widgets are canonicalized — Flutter skips rebuilding them entirely.

```dart
// GOOD: const constructor — widget never rebuilds
class AppDivider extends StatelessWidget {
  const AppDivider({super.key}); // const constructor

  @override
  Widget build(BuildContext context) {
    return const Divider(height: 1, thickness: 1); // const child too
  }
}

// Usage — const at call site
const AppDivider(), // Flutter caches this instance

// When you CAN'T use const
class UserChip extends StatelessWidget {
  const UserChip({super.key, required this.name}); // const constructor OK
  final String name;

  @override
  Widget build(BuildContext context) {
    return Chip(label: Text(name)); // Not const — name is runtime value
  }
}
// But call site can't be const because name varies:
UserChip(name: user.name) // No const prefix
```

### The Const Lint

Enable `prefer_const_constructors` and `prefer_const_declarations` in `analysis_options.yaml`.

## BuildContext Usage

### Rules

1. Never store `BuildContext` in state or pass it to async gaps without checking `mounted`
2. Use `context` to read the nearest ancestor: `Theme.of(context)`, `MediaQuery.of(context)`
3. After an `await`, check `mounted` before using context

```dart
class _MyWidgetState extends State<MyWidget> {
  Future<void> _submit() async {
    final navigator = Navigator.of(context); // Capture before await
    final messenger = ScaffoldMessenger.of(context);

    try {
      await api.submit(data);
      if (!mounted) return; // Check before using context
      navigator.pop();
    } catch (e) {
      if (!mounted) return;
      messenger.showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }
}
```

## InheritedWidget Pattern

Use for dependency injection and efficient rebuilds based on data changes.

```dart
class AppConfig extends InheritedWidget {
  const AppConfig({
    super.key,
    required this.apiBaseUrl,
    required this.featureFlags,
    required super.child,
  });

  final String apiBaseUrl;
  final Map<String, bool> featureFlags;

  static AppConfig of(BuildContext context) {
    final result = context.dependOnInheritedWidgetOfExactType<AppConfig>();
    assert(result != null, 'No AppConfig found in context');
    return result!;
  }

  // Optional: static method that doesn't subscribe to changes
  static AppConfig? maybeOf(BuildContext context) {
    return context.dependOnInheritedWidgetOfExactType<AppConfig>();
  }

  @override
  bool updateShouldNotify(AppConfig oldWidget) {
    return apiBaseUrl != oldWidget.apiBaseUrl ||
        featureFlags != oldWidget.featureFlags;
  }
}

// Usage
final config = AppConfig.of(context);
if (config.featureFlags['darkMode'] == true) { /* ... */ }
```

## Builder Pattern

Use Builder widgets to get a new `BuildContext` below a widget you just created.

```dart
// Problem: Scaffold.of(context) fails because context is ABOVE the Scaffold
@override
Widget build(BuildContext context) {
  return Scaffold(
    body: ElevatedButton(
      onPressed: () {
        // BAD: context is above Scaffold, no ScaffoldMessenger found
        ScaffoldMessenger.of(context).showSnackBar(/*...*/);
      },
      child: const Text('Show Snackbar'),
    ),
  );
}

// Solution: Builder provides a context BELOW the Scaffold
@override
Widget build(BuildContext context) {
  return Scaffold(
    body: Builder(
      builder: (scaffoldContext) {
        return ElevatedButton(
          onPressed: () {
            // GOOD: scaffoldContext is below Scaffold
            ScaffoldMessenger.of(scaffoldContext).showSnackBar(/*...*/);
          },
          child: const Text('Show Snackbar'),
        );
      },
    ),
  );
}
```

### LayoutBuilder for Responsive Widgets

```dart
class ResponsiveGrid extends StatelessWidget {
  const ResponsiveGrid({super.key, required this.children});
  final List<Widget> children;

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final columns = constraints.maxWidth > 900 ? 3
            : constraints.maxWidth > 600 ? 2
            : 1;
        return GridView.count(
          crossAxisCount: columns,
          children: children,
        );
      },
    );
  }
}
```

## Anti-patterns

### Mega-Build Methods (>50 Lines)

Split into extracted widgets. Long build methods are hard to read and cause unnecessary rebuilds of the entire subtree.

### setState in initState

```dart
// BAD: setState in initState triggers unnecessary rebuild
@override
void initState() {
  super.initState();
  setState(() { _value = widget.initialValue; }); // WRONG
}

// GOOD: Initialize directly
@override
void initState() {
  super.initState();
  _value = widget.initialValue; // No setState needed
}
```

### Missing Const Constructors

Every widget whose fields are all final and whose super constructor is const should have a const constructor. Missing it prevents const instantiation and wastes rebuilds.

### Rebuilding Entire Subtrees

```dart
// BAD: Entire Column rebuilds when counter changes
class _MyState extends State<MyWidget> {
  int _counter = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const ExpensiveHeader(),       // Rebuilds unnecessarily
        Text('$_counter'),             // Only this needs to update
        const ExpensiveFooter(),       // Rebuilds unnecessarily
      ],
    );
  }
}

// GOOD: Extract the changing part into its own widget
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const ExpensiveHeader(),   // Never rebuilds
        const CounterText(),       // Only this rebuilds
        const ExpensiveFooter(),   // Never rebuilds
      ],
    );
  }
}

class CounterText extends StatefulWidget {
  const CounterText({super.key});

  @override
  State<CounterText> createState() => _CounterTextState();
}

class _CounterTextState extends State<CounterText> {
  int _counter = 0;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => setState(() => _counter++),
      child: Text('$_counter'),
    );
  }
}
```
