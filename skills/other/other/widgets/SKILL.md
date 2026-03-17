---
name: Flutter UI Widgets
description: Principles for maintainable UI components.
metadata:
  labels: [ui, widgets]
  triggers:
    files: ['**_page.dart', '**_screen.dart', '**/widgets/**']
    keywords: [StatelessWidget, const, Theme, ListView]
---

# UI & Widgets

## **Priority: P1 (OPERATIONAL)**

Standards for building reusable, performant Flutter widgets and UI components.

- **State**: Use `StatelessWidget` by default. `StatefulWidget` only for local state/controllers.
- **Composition**: Extract UI into small, atomic `const` widgets.
- **Theming**: Use `Theme.of(context)`. No hardcoded colors.
- **Layout**: Use `Flex` + `Gap/SizedBox`.
- **Widget Keys**: All interactive elements must use keys from `widget_keys.dart`.
- **File Size**: If a UI file exceeds ~80 lines, extract sub-widgets into private classes.
- **Specialized**:
  - `SelectionArea`: For multi-widget text selection.
  - `InteractiveViewer`: For zoom/pan.
  - `ListWheelScrollView`: For pickers.
  - `IntrinsicWidth/Height`: Avoid unless strictly required.
- **Large Lists**: Always use `ListView.builder`.

```dart
class AppButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;
  const AppButton({super.key, required this.label, required this.onPressed});

  @override
  Widget build(BuildContext context) => ElevatedButton(onPressed: onPressed, child: Text(label));
}
```

## Related Topics

performance | testing
