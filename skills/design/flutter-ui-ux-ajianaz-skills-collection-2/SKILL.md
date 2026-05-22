---
name: flutter-ui-ux
description: |
  Comprehensive Flutter UI/UX development skill for creating beautiful, responsive, and animated mobile applications. Use when user asks to:
  (1) Build Flutter UI components or screens
  (2) Implement animations and transitions
  (3) Design responsive layouts
  (4) Create custom widgets and themes
  (5) Optimize UI performance and accessibility
  Triggers: "create Flutter UI", "build Flutter screen", "Flutter animations", "responsive Flutter layout", "custom Flutter widgets", "Flutter theme design"
---

# Flutter UI/UX Development

Create beautiful, responsive, and animated Flutter applications with modern design patterns and best practices.

## Core Philosophy

**"Mobile-first, animation-enhanced, accessible design"** - Focus on:

| Priority | Area | Purpose |
|----------|------|---------|
| 1 | Widget Composition | Reusable, maintainable UI components |
| 2 | Responsive Design | Adaptive layouts for all screen sizes |
| 3 | Animations | Smooth, purposeful transitions and micro-interactions |
| 4 | Custom Themes | Consistent, branded visual identity |
| 5 | Performance | 60fps rendering and optimal resource usage |

## Development Workflow

Execute phases sequentially. Complete each before proceeding.

### Phase 1: Analyze Requirements

1. **Understand app structure** - Identify existing widgets, screens, and navigation
2. **Design system review** - Check existing themes, colors, and typography
3. **Platform considerations** - Note iOS/Android specific requirements
4. **Performance constraints** - Identify animation complexity and rendering needs

Output: UI requirements analysis with component breakdown.

### Phase 2: Design Widget Architecture

1. **Widget hierarchy planning** - Design composition tree
2. **State management strategy** - Choose StatefulWidget vs StatelessWidget
3. **Custom widget identification** - Plan reusable components
4. **Theme integration** - Define color schemes and typography

Output: Widget architecture diagram and component specifications.

### Phase 3: Implement Core UI

1. **Create base widgets** - Build foundational components
2. **Implement responsive layouts** - Use MediaQuery, LayoutBuilder, Flex/Expanded
3. **Add custom themes** - ThemeData, ColorScheme, TextThemes
4. **Integrate navigation** - Implement routing and transitions

**Widget Composition Patterns:**
```dart
// ✅ DO: Compose small, reusable widgets
class CustomCard extends StatelessWidget {
  final Widget child;
  final EdgeInsets padding;

  const CustomCard({required this.child, this.padding = EdgeInsets.all(16)});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      child: Padding(padding: padding, child: child),
    );
  }
}

// ✅ DO: Use const constructors where possible
const Icon(Icons.add) // Better than Icon(Icons.add)
```

### Phase 4: Add Animations

1. **Implicit animations** - AnimatedContainer, AnimatedOpacity
2. **Explicit animations** - AnimationController with Tween
3. **Hero animations** - Screen transitions with Hero widgets
4. **Micro-interactions** - Button presses, hover effects, loading states

**Animation Performance Rules:**
```dart
// ✅ DO: Use performance-optimized animations
AnimatedBuilder(
  animation: controller,
  builder: (context, child) => Transform.rotate(
    angle: controller.value * 2 * math.pi,
    child: child, // Pass child to avoid rebuilding
  ),
  child: const Icon(Icons.refresh),
)

// ❌ DON'T: Animate expensive operations
// Avoid animating complex layouts or heavy widgets
```

### Phase 5: Optimize and Test

1. **Performance profiling** - Use Flutter DevTools
2. **Accessibility testing** - Screen readers, contrast ratios
3. **Responsive testing** - Multiple screen sizes and orientations
4. **Animation smoothness** - 60fps validation

## Quick Reference

### Responsive Design Patterns

| Technique | Use Case | Implementation |
|-----------|-----------|----------------|
| LayoutBuilder | Responsive layouts | `LayoutBuilder(builder: (context, constraints) => ...)` |
| MediaQuery | Screen info | `MediaQuery.of(context).size.width` |
| Flexible/Expanded | Flex layouts | `Flexible(child: ...)` or `Expanded(child: ...)` |
| AspectRatio | Fixed ratios | `AspectRatio(aspectRatio: 16/9, child: ...)` |

### Animation Types

| Type | Widget | Duration | Use Case |
|-------|---------|----------|----------|
| Fade | AnimatedOpacity | 200-300ms | Show/hide content |
| Slide | SlideTransition | 250-350ms | Screen transitions |
| Scale | AnimatedScale | 150-250ms | Button presses |
| Rotation | RotationTransition | 1000-2000ms | Loading indicators |

### Custom Widget Examples

**Themed Button:**
```dart
class ThemedButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;

  const ThemedButton({required this.text, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: Theme.of(context).colorScheme.primary,
        foregroundColor: Theme.of(context).colorScheme.onPrimary,
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      ),
      child: Text(text),
    );
  }
}
```

**Responsive Card:**
```dart
class ResponsiveCard extends StatelessWidget {
  final Widget child;

  const ResponsiveCard({required this.child});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth > 600) {
          return _buildWideLayout(child);
        } else {
          return _buildNarrowLayout(child);
        }
      },
    );
  }

  Widget _buildWideLayout(Widget child) {
    return Card(
      margin: const EdgeInsets.all(16),
      child: Padding(padding: const EdgeInsets.all(24), child: child),
    );
  }

  Widget _buildNarrowLayout(Widget child) {
    return Card(
      margin: const EdgeInsets.all(8),
      child: Padding(padding: const EdgeInsets.all(16), child: child),
    );
  }
}
```

## Resources

- **Widget patterns**: See `references/widget-patterns.md`
- **Animation examples**: See `references/animation-patterns.md`
- **Theme templates**: See `references/theme-templates.md`
- **Performance guide**: See `references/performance-optimization.md`

## Technical Stack

- **Core Widgets**: StatelessWidget, StatefulWidget, InheritedWidget
- **Layout**: Row, Column, Stack, GridView, ListView
- **Animation**: AnimationController, Tween, AnimatedWidget
- **Themes**: ThemeData, ColorScheme, TextTheme
- **Navigation**: Navigator, MaterialPageRoute, Hero

## Accessibility (Required)

Always implement:
```dart
// Semantic labels for screen readers
Semantics(
  label: 'Add item to cart',
  button: true,
  child: IconButton(icon: Icon(Icons.add_cart), onPressed: () {}),
)

// High contrast support
Theme.of(context).colorScheme.contrast() == Brightness.dark

// Font scaling
MediaQuery.of(context).accessibleNavigation
```

## Performance Guidelines

- Use `const` widgets where possible
- Prefer `ListView.builder` for long lists
- Avoid unnecessary rebuilds with `const` keys
- Use `RepaintBoundary` for complex animations
- Profile with Flutter DevTools regularly

---

This Flutter UI/UX skill transforms mobile app development into a systematic process that ensures beautiful, responsive, and performant applications with exceptional user experiences.