# 🎨 Skill: Theming Avanzado

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-theming-advanced` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `theming`, `theme`, `dark-mode`, `material3`, `design-system` |
| **Referencia** | [Flutter Theming](https://docs.flutter.dev/cookbook/design/themes) |

## 🔑 Keywords para Invocación

- `theming`
- `theme`
- `dark-mode`
- `light-mode`
- `material3`
- `design-system`
- `@skill:theming`

### Ejemplos de Prompts

```
Implementa theming con dark mode y Material 3
```

```
Crea un sistema de diseño con temas personalizados
```

```
@skill:theming - Agrega soporte para múltiples temas
```

## 📖 Descripción

Theming Avanzado permite crear un sistema de diseño consistente con soporte para múltiples temas (light/dark/custom), Material 3, tipografía personalizada, y cambio dinámico de temas. Incluye tokens de diseño, componentes reutilizables y adaptación automática al sistema.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

### ✅ Cuándo Usar Este Skill

- Necesitas dark mode + light mode
- Quieres un design system consistente
- Múltiples temas o branding
- Material 3 con custom colors
- Soporte de preferencias del sistema
- Componentes reutilizables estilizados

### ❌ Cuándo NO Usar Este Skill

- App muy simple sin requerimientos de diseño
- Solo un tema sin variaciones

## 🏗️ Estructura del Proyecto

```
lib/
├── core/
│   ├── theme/
│   │   ├── app_theme.dart
│   │   ├── theme_cubit.dart
│   │   ├── theme_state.dart
│   │   ├── color_schemes.dart
│   │   ├── text_theme.dart
│   │   ├── app_colors.dart
│   │   └── app_typography.dart
│   └── widgets/
│       └── themed/
│           ├── themed_button.dart
│           ├── themed_card.dart
│           └── themed_input.dart
└── main.dart
```

## 📦 Dependencias Requeridas

```yaml
dependencies:
  flutter:
    sdk: flutter

  # State management para temas
  flutter_bloc: ^8.1.3

  # Persistencia de preferencias
  shared_preferences: ^2.2.2

  # Google Fonts (opcional)
  google_fonts: ^6.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
```

## 💻 Implementación

### 1. Tokens de Diseño - Colores

```dart
// lib/core/theme/app_colors.dart
import 'package:flutter/material.dart';

class AppColors {
  // Primary Colors
  static const Color primary = Color(0xFF6750A4);
  static const Color primaryContainer = Color(0xFFEADDFF);
  static const Color onPrimary = Color(0xFFFFFFFF);
  static const Color onPrimaryContainer = Color(0xFF21005D);

  // Secondary Colors
  static const Color secondary = Color(0xFF625B71);
  static const Color secondaryContainer = Color(0xFFE8DEF8);
  static const Color onSecondary = Color(0xFFFFFFFF);
  static const Color onSecondaryContainer = Color(0xFF1D192B);

  // Tertiary Colors
  static const Color tertiary = Color(0xFF7D5260);
  static const Color tertiaryContainer = Color(0xFFFFD8E4);
  static const Color onTertiary = Color(0xFFFFFFFF);
  static const Color onTertiaryContainer = Color(0xFF31111D);

  // Error Colors
  static const Color error = Color(0xFFB3261E);
  static const Color errorContainer = Color(0xFFF9DEDC);
  static const Color onError = Color(0xFFFFFFFF);
  static const Color onErrorContainer = Color(0xFF410E0B);

  // Surface Colors
  static const Color surface = Color(0xFFFFFBFE);
  static const Color surfaceDim = Color(0xFFE7E0EC);
  static const Color surfaceBright = Color(0xFFFFFBFE);
  static const Color surfaceContainerLowest = Color(0xFFFFFFFF);
  static const Color surfaceContainerLow = Color(0xFFF7F2FA);
  static const Color surfaceContainer = Color(0xFFF3EDF7);
  static const Color surfaceContainerHigh = Color(0xFFECE6F0);
  static const Color surfaceContainerHighest = Color(0xFFE6E0E9);

  // Outline
  static const Color outline = Color(0xFF79747E);
  static const Color outlineVariant = Color(0xFFCAC4D0);

  // Background (deprecated in M3 pero útil para compatibilidad)
  static const Color background = Color(0xFFFFFBFE);
  static const Color onBackground = Color(0xFF1C1B1F);

  // Inverse Colors
  static const Color inverseSurface = Color(0xFF313033);
  static const Color inverseOnSurface = Color(0xFFF4EFF4);
  static const Color inversePrimary = Color(0xFFD0BCFF);

  // Shadow & Scrim
  static const Color shadow = Color(0xFF000000);
  static const Color scrim = Color(0xFF000000);
}

// Dark Theme Colors
class AppColorsDark {
  static const Color primary = Color(0xFFD0BCFF);
  static const Color primaryContainer = Color(0xFF4F378B);
  static const Color onPrimary = Color(0xFF371E73);
  static const Color onPrimaryContainer = Color(0xFFEADDFF);

  static const Color secondary = Color(0xFFCCC2DC);
  static const Color secondaryContainer = Color(0xFF4A4458);
  static const Color onSecondary = Color(0xFF332D41);
  static const Color onSecondaryContainer = Color(0xFFE8DEF8);

  static const Color tertiary = Color(0xFFEFB8C8);
  static const Color tertiaryContainer = Color(0xFF633B48);
  static const Color onTertiary = Color(0xFF492532);
  static const Color onTertiaryContainer = Color(0xFFFFD8E4);

  static const Color error = Color(0xFFF2B8B5);
  static const Color errorContainer = Color(0xFF8C1D18);
  static const Color onError = Color(0xFF601410);
  static const Color onErrorContainer = Color(0xFFF9DEDC);

  static const Color surface = Color(0xFF1C1B1F);
  static const Color surfaceDim = Color(0xFF1C1B1F);
  static const Color surfaceBright = Color(0xFF3B383E);
  static const Color surfaceContainerLowest = Color(0xFF0F0D13);
  static const Color surfaceContainerLow = Color(0xFF1D1B20);
  static const Color surfaceContainer = Color(0xFF211F26);
  static const Color surfaceContainerHigh = Color(0xFF2B2930);
  static const Color surfaceContainerHighest = Color(0xFF36343B);

  static const Color outline = Color(0xFF938F99);
  static const Color outlineVariant = Color(0xFF49454F);

  static const Color background = Color(0xFF1C1B1F);
  static const Color onBackground = Color(0xFFE6E1E5);

  static const Color inverseSurface = Color(0xFFE6E1E5);
  static const Color inverseOnSurface = Color(0xFF313033);
  static const Color inversePrimary = Color(0xFF6750A4);

  static const Color shadow = Color(0xFF000000);
  static const Color scrim = Color(0xFF000000);
}
```

### 2. Tipografía

```dart
// lib/core/theme/app_typography.dart
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTypography {
  // Material 3 Typography
  static TextTheme textTheme = TextTheme(
    // Display
    displayLarge: GoogleFonts.roboto(
      fontSize: 57,
      fontWeight: FontWeight.w400,
      letterSpacing: -0.25,
      height: 1.12,
    ),
    displayMedium: GoogleFonts.roboto(
      fontSize: 45,
      fontWeight: FontWeight.w400,
      height: 1.16,
    ),
    displaySmall: GoogleFonts.roboto(
      fontSize: 36,
      fontWeight: FontWeight.w400,
      height: 1.22,
    ),

    // Headline
    headlineLarge: GoogleFonts.roboto(
      fontSize: 32,
      fontWeight: FontWeight.w400,
      height: 1.25,
    ),
    headlineMedium: GoogleFonts.roboto(
      fontSize: 28,
      fontWeight: FontWeight.w400,
      height: 1.29,
    ),
    headlineSmall: GoogleFonts.roboto(
      fontSize: 24,
      fontWeight: FontWeight.w400,
      height: 1.33,
    ),

    // Title
    titleLarge: GoogleFonts.roboto(
      fontSize: 22,
      fontWeight: FontWeight.w400,
      height: 1.27,
    ),
    titleMedium: GoogleFonts.roboto(
      fontSize: 16,
      fontWeight: FontWeight.w500,
      letterSpacing: 0.15,
      height: 1.50,
    ),
    titleSmall: GoogleFonts.roboto(
      fontSize: 14,
      fontWeight: FontWeight.w500,
      letterSpacing: 0.1,
      height: 1.43,
    ),

    // Body
    bodyLarge: GoogleFonts.roboto(
      fontSize: 16,
      fontWeight: FontWeight.w400,
      letterSpacing: 0.5,
      height: 1.50,
    ),
    bodyMedium: GoogleFonts.roboto(
      fontSize: 14,
      fontWeight: FontWeight.w400,
      letterSpacing: 0.25,
      height: 1.43,
    ),
    bodySmall: GoogleFonts.roboto(
      fontSize: 12,
      fontWeight: FontWeight.w400,
      letterSpacing: 0.4,
      height: 1.33,
    ),

    // Label
    labelLarge: GoogleFonts.roboto(
      fontSize: 14,
      fontWeight: FontWeight.w500,
      letterSpacing: 0.1,
      height: 1.43,
    ),
    labelMedium: GoogleFonts.roboto(
      fontSize: 12,
      fontWeight: FontWeight.w500,
      letterSpacing: 0.5,
      height: 1.33,
    ),
    labelSmall: GoogleFonts.roboto(
      fontSize: 11,
      fontWeight: FontWeight.w500,
      letterSpacing: 0.5,
      height: 1.45,
    ),
  );
}
```

### 3. Theme Configuration

```dart
// lib/core/theme/app_theme.dart
import 'package:flutter/material.dart';
import 'app_colors.dart';
import 'app_typography.dart';

class AppTheme {
  // Light Theme
  static ThemeData lightTheme() {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,

      // Color Scheme
      colorScheme: const ColorScheme.light(
        primary: AppColors.primary,
        primaryContainer: AppColors.primaryContainer,
        onPrimary: AppColors.onPrimary,
        onPrimaryContainer: AppColors.onPrimaryContainer,

        secondary: AppColors.secondary,
        secondaryContainer: AppColors.secondaryContainer,
        onSecondary: AppColors.onSecondary,
        onSecondaryContainer: AppColors.onSecondaryContainer,

        tertiary: AppColors.tertiary,
        tertiaryContainer: AppColors.tertiaryContainer,
        onTertiary: AppColors.onTertiary,
        onTertiaryContainer: AppColors.onTertiaryContainer,

        error: AppColors.error,
        errorContainer: AppColors.errorContainer,
        onError: AppColors.onError,
        onErrorContainer: AppColors.onErrorContainer,

        surface: AppColors.surface,
        onSurface: AppColors.onBackground,

        outline: AppColors.outline,
        outlineVariant: AppColors.outlineVariant,

        inverseSurface: AppColors.inverseSurface,
        onInverseSurface: AppColors.inverseOnSurface,
        inversePrimary: AppColors.inversePrimary,

        shadow: AppColors.shadow,
        scrim: AppColors.scrim,
      ),

      // Typography
      textTheme: AppTypography.textTheme,

      // AppBar Theme
      appBarTheme: AppBarTheme(
        centerTitle: false,
        elevation: 0,
        backgroundColor: AppColors.surface,
        foregroundColor: AppColors.onBackground,
        titleTextStyle: AppTypography.textTheme.titleLarge,
      ),

      // Card Theme
      cardTheme: CardTheme(
        elevation: 1,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        color: AppColors.surfaceContainer,
      ),

      // Input Decoration Theme
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.surfaceContainerHighest,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.outline),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.primary, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.error),
        ),
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 16,
          vertical: 16,
        ),
      ),

      // Elevated Button Theme
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primary,
          foregroundColor: AppColors.onPrimary,
          elevation: 1,
          padding: const EdgeInsets.symmetric(
            horizontal: 24,
            vertical: 16,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: AppTypography.textTheme.labelLarge,
        ),
      ),

      // Text Button Theme
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: AppColors.primary,
          padding: const EdgeInsets.symmetric(
            horizontal: 24,
            vertical: 16,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: AppTypography.textTheme.labelLarge,
        ),
      ),

      // Outlined Button Theme
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: AppColors.primary,
          side: BorderSide(color: AppColors.outline),
          padding: const EdgeInsets.symmetric(
            horizontal: 24,
            vertical: 16,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: AppTypography.textTheme.labelLarge,
        ),
      ),

      // Floating Action Button Theme
      floatingActionButtonTheme: FloatingActionButtonThemeData(
        backgroundColor: AppColors.primaryContainer,
        foregroundColor: AppColors.onPrimaryContainer,
        elevation: 3,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
      ),

      // Bottom Navigation Bar Theme
      bottomNavigationBarTheme: BottomNavigationBarThemeData(
        backgroundColor: AppColors.surface,
        selectedItemColor: AppColors.primary,
        unselectedItemColor: AppColors.onSurface.withOpacity(0.6),
        type: BottomNavigationBarType.fixed,
        elevation: 3,
      ),

      // Chip Theme
      chipTheme: ChipThemeData(
        backgroundColor: AppColors.surfaceContainerHighest,
        labelStyle: AppTypography.textTheme.labelLarge,
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),

      // Dialog Theme
      dialogTheme: DialogTheme(
        backgroundColor: AppColors.surface,
        elevation: 3,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(28),
        ),
        titleTextStyle: AppTypography.textTheme.headlineSmall,
        contentTextStyle: AppTypography.textTheme.bodyMedium,
      ),

      // Divider Theme
      dividerTheme: DividerThemeData(
        color: AppColors.outlineVariant,
        thickness: 1,
        space: 1,
      ),
    );
  }

  // Dark Theme
  static ThemeData darkTheme() {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,

      colorScheme: const ColorScheme.dark(
        primary: AppColorsDark.primary,
        primaryContainer: AppColorsDark.primaryContainer,
        onPrimary: AppColorsDark.onPrimary,
        onPrimaryContainer: AppColorsDark.onPrimaryContainer,

        secondary: AppColorsDark.secondary,
        secondaryContainer: AppColorsDark.secondaryContainer,
        onSecondary: AppColorsDark.onSecondary,
        onSecondaryContainer: AppColorsDark.onSecondaryContainer,

        tertiary: AppColorsDark.tertiary,
        tertiaryContainer: AppColorsDark.tertiaryContainer,
        onTertiary: AppColorsDark.onTertiary,
        onTertiaryContainer: AppColorsDark.onTertiaryContainer,

        error: AppColorsDark.error,
        errorContainer: AppColorsDark.errorContainer,
        onError: AppColorsDark.onError,
        onErrorContainer: AppColorsDark.onErrorContainer,

        surface: AppColorsDark.surface,
        onSurface: AppColorsDark.onBackground,

        outline: AppColorsDark.outline,
        outlineVariant: AppColorsDark.outlineVariant,

        inverseSurface: AppColorsDark.inverseSurface,
        onInverseSurface: AppColorsDark.inverseOnSurface,
        inversePrimary: AppColorsDark.inversePrimary,

        shadow: AppColorsDark.shadow,
        scrim: AppColorsDark.scrim,
      ),

      textTheme: AppTypography.textTheme,

      appBarTheme: AppBarTheme(
        centerTitle: false,
        elevation: 0,
        backgroundColor: AppColorsDark.surface,
        foregroundColor: AppColorsDark.onBackground,
        titleTextStyle: AppTypography.textTheme.titleLarge,
      ),

      // Otros componentes similares al light theme
    );
  }
}
```

### 4. Theme State Management

```dart
// lib/core/theme/theme_mode_enum.dart
enum AppThemeMode {
  light,
  dark,
  system,
}
```

```dart
// lib/core/theme/theme_cubit.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shared_preferences/shared_preferences.dart';

enum AppThemeMode { light, dark, system }

class ThemeCubit extends Cubit<ThemeMode> {
  static const String _themeModeKey = 'theme_mode';
  final SharedPreferences prefs;

  ThemeCubit(this.prefs) : super(ThemeMode.system) {
    _loadSavedTheme();
  }

  void _loadSavedTheme() {
    final savedTheme = prefs.getString(_themeModeKey);
    if (savedTheme != null) {
      emit(_themeModeFromString(savedTheme));
    }
  }

  Future<void> setThemeMode(AppThemeMode mode) async {
    final themeMode = _convertToThemeMode(mode);
    await prefs.setString(_themeModeKey, mode.name);
    emit(themeMode);
  }

  ThemeMode _convertToThemeMode(AppThemeMode mode) {
    switch (mode) {
      case AppThemeMode.light:
        return ThemeMode.light;
      case AppThemeMode.dark:
        return ThemeMode.dark;
      case AppThemeMode.system:
        return ThemeMode.system;
    }
  }

  ThemeMode _themeModeFromString(String value) {
    switch (value) {
      case 'light':
        return ThemeMode.light;
      case 'dark':
        return ThemeMode.dark;
      default:
        return ThemeMode.system;
    }
  }

  AppThemeMode get currentAppThemeMode {
    switch (state) {
      case ThemeMode.light:
        return AppThemeMode.light;
      case ThemeMode.dark:
        return AppThemeMode.dark;
      case ThemeMode.system:
        return AppThemeMode.system;
    }
  }
}
```

### 5. Main Setup

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'core/theme/app_theme.dart';
import 'core/theme/theme_cubit.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final prefs = await SharedPreferences.getInstance();

  runApp(MyApp(prefs: prefs));
}

class MyApp extends StatelessWidget {
  final SharedPreferences prefs;

  const MyApp({super.key, required this.prefs});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => ThemeCubit(prefs),
      child: BlocBuilder<ThemeCubit, ThemeMode>(
        builder: (context, themeMode) {
          return MaterialApp(
            title: 'Themed App',
            theme: AppTheme.lightTheme(),
            darkTheme: AppTheme.darkTheme(),
            themeMode: themeMode,
            home: const HomeScreen(),
          );
        },
      ),
    );
  }
}
```

### 6. Theme Switcher Widget

```dart
// lib/core/widgets/theme_switcher.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../theme/theme_cubit.dart';

class ThemeSwitcher extends StatelessWidget {
  const ThemeSwitcher({super.key});

  @override
  Widget build(BuildContext context) {
    final currentMode = context.watch<ThemeCubit>().currentAppThemeMode;

    return PopupMenuButton<AppThemeMode>(
      icon: Icon(_getIconForMode(currentMode)),
      tooltip: 'Change Theme',
      onSelected: (AppThemeMode mode) {
        context.read<ThemeCubit>().setThemeMode(mode);
      },
      itemBuilder: (BuildContext context) {
        return [
          PopupMenuItem(
            value: AppThemeMode.light,
            child: Row(
              children: [
                const Icon(Icons.light_mode),
                const SizedBox(width: 8),
                const Text('Light'),
                if (currentMode == AppThemeMode.light)
                  const Padding(
                    padding: EdgeInsets.only(left: 8),
                    child: Icon(Icons.check, size: 18),
                  ),
              ],
            ),
          ),
          PopupMenuItem(
            value: AppThemeMode.dark,
            child: Row(
              children: [
                const Icon(Icons.dark_mode),
                const SizedBox(width: 8),
                const Text('Dark'),
                if (currentMode == AppThemeMode.dark)
                  const Padding(
                    padding: EdgeInsets.only(left: 8),
                    child: Icon(Icons.check, size: 18),
                  ),
              ],
            ),
          ),
          PopupMenuItem(
            value: AppThemeMode.system,
            child: Row(
              children: [
                const Icon(Icons.settings_suggest),
                const SizedBox(width: 8),
                const Text('System'),
                if (currentMode == AppThemeMode.system)
                  const Padding(
                    padding: EdgeInsets.only(left: 8),
                    child: Icon(Icons.check, size: 18),
                  ),
              ],
            ),
          ),
        ];
      },
    );
  }

  IconData _getIconForMode(AppThemeMode mode) {
    switch (mode) {
      case AppThemeMode.light:
        return Icons.light_mode;
      case AppThemeMode.dark:
        return Icons.dark_mode;
      case AppThemeMode.system:
        return Icons.settings_suggest;
    }
  }
}

// Uso en AppBar
AppBar(
  title: const Text('My App'),
  actions: const [
    ThemeSwitcher(),
  ],
)
```

## 🎯 Mejores Prácticas

### 1. Usar Theme Extensions

✅ **DO:**
```dart
final primaryColor = Theme.of(context).colorScheme.primary;
final titleStyle = Theme.of(context).textTheme.titleLarge;
```

❌ **DON'T:**
```dart
final primaryColor = Colors.blue;  // ❌ Hardcoded
final titleStyle = TextStyle(fontSize: 22);  // ❌ Hardcoded
```

### 2. Responsive Sizing

✅ **DO:**
```dart
Text(
  'Title',
  style: Theme.of(context).textTheme.titleLarge,
)
```

### 3. Semantic Colors

✅ **DO:**
```dart
Container(
  color: Theme.of(context).colorScheme.surface,
  child: Text(
    'Content',
    style: TextStyle(
      color: Theme.of(context).colorScheme.onSurface,
    ),
  ),
)
```

## 📚 Recursos Adicionales

- [Material 3 Design](https://m3.material.io/)
- [Flutter Theming](https://docs.flutter.dev/cookbook/design/themes)
- [Google Fonts](https://pub.dev/packages/google_fonts)

## 🔗 Skills Relacionados

- [i18n](../i18n/SKILL.md) - Internacionalización
- [Project Setup](../project-setup/SKILL.md) - Configuración inicial

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
