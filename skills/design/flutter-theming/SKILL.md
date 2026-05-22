---
description: "Flutter theming: Material 3 ColorScheme, typography, dark mode, design tokens. Use when implementing themes or matching web app design system."
version: "1.0.0"
updated: "2026-01-07"
---

# Flutter Theming

## Quick Setup

```dart
MaterialApp(
  theme: BalleeTheme.light,
  darkTheme: BalleeTheme.dark,
  themeMode: ThemeMode.system,
)
```

## Using Theme

```dart
Theme.of(context).colorScheme.primary
Theme.of(context).colorScheme.surface
Theme.of(context).textTheme.headlineMedium
Theme.of(context).extension<BalleeColors>()?.coral500
```

## Ballee Color Palette

```dart
class BalleeColorPalette {
  static const Color coral50 = Color(0xFFFDF3F2);
  static const Color coral100 = Color(0xFFFDE8E7);
  static const Color coral500 = Color(0xFFBF5F60);  // Primary
  static const Color coral900 = Color(0xFF773234);

  static const Color neutral100 = Color(0xFFF5F5F5);
  static const Color neutral900 = Color(0xFF171717);

  static const Color success = Color(0xFF22C55E);
  static const Color warning = Color(0xFFF59E0B);
  static const Color error = Color(0xFFEF4444);
}
```

## ColorScheme

```dart
static ThemeData get light {
  final colorScheme = ColorScheme.fromSeed(
    seedColor: BalleeColorPalette.coral500,
    brightness: Brightness.light,
  ).copyWith(
    primary: BalleeColorPalette.coral500,
    onPrimary: Colors.white,
    surface: Colors.white,
    onSurface: BalleeColorPalette.neutral900,
    error: BalleeColorPalette.error,
  );

  return ThemeData(
    useMaterial3: true,
    colorScheme: colorScheme,
    extensions: [BalleeColors.light()],
  );
}
```

## Theme Extensions

```dart
class BalleeColors extends ThemeExtension<BalleeColors> {
  final Color coral500;
  final Color success;
  final Color warning;

  const BalleeColors({required this.coral500, required this.success, required this.warning});

  factory BalleeColors.light() => const BalleeColors(
    coral500: BalleeColorPalette.coral500,
    success: BalleeColorPalette.success,
    warning: BalleeColorPalette.warning,
  );

  @override
  BalleeColors copyWith({Color? coral500, Color? success, Color? warning}) =>
    BalleeColors(
      coral500: coral500 ?? this.coral500,
      success: success ?? this.success,
      warning: warning ?? this.warning,
    );

  @override
  BalleeColors lerp(BalleeColors? other, double t) {
    if (other == null) return this;
    return BalleeColors(
      coral500: Color.lerp(coral500, other.coral500, t)!,
      success: Color.lerp(success, other.success, t)!,
      warning: Color.lerp(warning, other.warning, t)!,
    );
  }
}
```

## Dark Mode Provider

```dart
@riverpod
class ThemeModeNotifier extends _$ThemeModeNotifier {
  @override
  ThemeMode build() {
    final prefs = ref.watch(sharedPreferencesProvider);
    final saved = prefs.getString('themeMode');
    return ThemeMode.values.firstWhere((m) => m.name == saved, orElse: () => ThemeMode.system);
  }

  Future<void> setThemeMode(ThemeMode mode) async {
    await ref.read(sharedPreferencesProvider).setString('themeMode', mode.name);
    state = mode;
  }
}
```

## Component Theming

```dart
static CardTheme _cardTheme(ColorScheme cs) => CardTheme(
  color: cs.surface,
  elevation: 0,
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(12),
    side: BorderSide(color: cs.outlineVariant),
  ),
);

static ElevatedButtonThemeData _buttonTheme(ColorScheme cs) => ElevatedButtonThemeData(
  style: ElevatedButton.styleFrom(
    backgroundColor: cs.primary,
    foregroundColor: cs.onPrimary,
    minimumSize: const Size(double.infinity, 48),
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
  ),
);
```

## Related Skills
- **flutter-ui-components**: Widget patterns
- **flutter-accessibility**: Color contrast
- **ui-patterns**: Web app design system
