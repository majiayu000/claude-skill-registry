---
name: oref
description: Guidance for using the Oref Flutter signals/state management library and its DevTools/analyzer tooling. Use when answering questions about installing Oref, creating signals/computed/effects, async data, reactive collections, SignalBuilder usage, analyzer lints, DevTools extension setup/usage, or troubleshooting Oref behavior.
---

# Oref

> Based on the Oref docs and repository examples. Use BuildContext-bound APIs inside widget builds when possible.

## Preferences

- Match the user's language.
- Prefer concise, runnable snippets over long explanations.
- Use `signal(context, ...)`/`computed(context, ...)`/`effect(context, ...)` inside `build`.
- Use `null` context only outside widgets, and keep the dispose handle.
- Use `SignalBuilder` to scope rebuilds to small subtrees.
- Use `batch()` for multi-step updates or collection mutations.
- Avoid writing to signals inside `computed` getters.
- Call hooks unconditionally at the top level of a build scope.

## Core

| Topic             | Description                                                                 | Reference                                        |
| ----------------- | --------------------------------------------------------------------------- | ------------------------------------------------ |
| Quick Start       | Install + minimal signal/computed/effect usage                              | [quick-start](references/quick-start.md)         |
| Reactivity Core   | Signals, computed, writableComputed, effects, batch, untrack, SignalBuilder | [core-api](references/core-api.md)               |
| Hooks & Lifecycle | Hook ordering rules, onMounted/onUnmounted, cleanup                         | [hooks-lifecycle](references/hooks-lifecycle.md) |
| Async Data        | `useAsyncData` lifecycle and rendering                                      | [async-data](references/async-data.md)           |
| Collections       | ReactiveList/Map/Set patterns                                               | [collections](references/collections.md)         |

## Tooling

| Topic           | Description                     | Reference                                        |
| --------------- | ------------------------------- | ------------------------------------------------ |
| Analyzer Lints  | Plugin setup + lint catalog     | [analyzer-lints](references/analyzer-lints.md)   |
| DevTools        | Extension setup + runtime notes | [devtools](references/devtools.md)               |
| Troubleshooting | Common pitfalls and fixes       | [troubleshooting](references/troubleshooting.md) |

## Quick Reference

### Minimal widget

```dart
import 'package:flutter/material.dart';
import 'package:oref/oref.dart';

class Counter extends StatelessWidget {
  const Counter({super.key});

  @override
  Widget build(BuildContext context) {
    final count = signal(context, 0);
    final doubled = computed(context, (_) => count() * 2);

    return Column(
      children: [
        Text('Count: ${count()} / ${doubled()}'),
        TextButton(onPressed: () => count.set(count() + 1), child: const Text('Add')),
      ],
    );
  }
}
```

### Key imports

```dart
import 'package:oref/oref.dart';
```

## Response workflow

1. Identify the question type and open the matching reference.
2. Provide the smallest snippet that answers the question.
3. Ask for missing context only if required (Flutter version, target platform, existing code).
4. Avoid guessing versions; read the user's `pubspec.yaml` or ask them to confirm.
