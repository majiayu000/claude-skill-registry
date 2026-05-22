---
description: "Flutter animations: Rive-first approach, Lottie, micro-interactions, timing guidelines. Use when adding animations or improving UX polish."
version: "1.0.0"
updated: "2026-01-07"
---

# Flutter Animations (Rive-First)

## Animation Stack Priority

1. **Rive** (Primary): Interactive, 60fps, small files, state machines
2. **Lottie** (Secondary): Non-interactive, existing assets
3. **flutter_animate**: Micro-interactions, quick effects

## Timing Guidelines

| Type | Duration | Use |
|------|----------|-----|
| Micro-interactions | 50-150ms | Button press, toggle |
| Component transitions | 200-400ms | Expand, collapse |
| Page transitions | 300-600ms | Hero, route change |
| Loading indicators | 800-1200ms | Infinite loop |

## Rive (Recommended)

```dart
// State machine pattern
class AnimatedButton extends StatefulWidget {
  @override
  State<AnimatedButton> createState() => _AnimatedButtonState();
}

class _AnimatedButtonState extends State<AnimatedButton> {
  SMIBool? _isPressed;

  void _onInit(Artboard artboard) {
    final controller = StateMachineController.fromArtboard(artboard, 'ButtonState');
    artboard.addController(controller!);
    _isPressed = controller.findInput<bool>('isPressed') as SMIBool?;
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => _isPressed?.value = true,
      onTapUp: (_) => _isPressed?.value = false,
      child: RiveAnimation.asset(
        'assets/animations/button.riv',
        onInit: _onInit,
      ),
    );
  }
}
```

## Lottie

```dart
Lottie.asset(
  'assets/animations/loading.json',
  width: 100,
  height: 100,
  repeat: true,
)
```

## flutter_animate

```dart
Text('Hello')
  .animate()
  .fadeIn(duration: 200.ms)
  .slideX(begin: -0.2, end: 0)
```

## Implicit Animations

```dart
AnimatedContainer(
  duration: const Duration(milliseconds: 200),
  width: _expanded ? 200 : 100,
  color: _active ? Colors.blue : Colors.grey,
)

AnimatedOpacity(
  duration: const Duration(milliseconds: 150),
  opacity: _visible ? 1.0 : 0.0,
  child: content,
)
```

## Hero Animations

```dart
// Source
Hero(tag: 'event-${event.id}', child: EventCard(event: event))

// Destination
Hero(tag: 'event-${event.id}', child: EventImage(event: event))
```

## Asset Organization

```
assets/animations/
├── buttons/
├── loaders/
├── onboarding/
└── icons/
```

## Related Skills
- **flutter-ui-components**: Widget patterns
- **flutter-performance**: Performance
- **flutter-accessibility**: A11y
