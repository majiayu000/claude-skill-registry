---
name: "flutter-theming-apps"
description: "Customizes the visual appearance of a Flutter app using the theming system. Use when defining global styles, colors, or typography for an application."
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Thu, 12 Mar 2026 22:14:47 GMT"

---
# Implementing Flutter Theming and Adaptive Design

## Contents
- [Core Theming Concepts](#core-theming-concepts)
- [Material 3 Guidelines](#material-3-guidelines)
- [Component Theme Normalization](#component-theme-normalization)
- [Button Styling](#button-styling)
- [Platform Idioms & Adaptive Design](#platform-idioms--adaptive-design)
- [Workflows](#workflows)
- [Examples](#examples)

## Core Theming Concepts
Flutter applies styling in a strict hierarchy: styles applied to the specific widget -> themes that override the immediate parent theme -> the main app theme. 

- Define app-wide themes using the `theme` property of `MaterialApp` with a `ThemeData` instance.
- Override themes for specific widget subtrees by wrapping them in a `Theme` widget and using `Theme.of(context).copyWith(...)`.
- **Do not** use deprecated `ThemeData` properties:
  - Replace `accentColor` with `colorScheme.secondary`.
  - Replace `accentTextTheme` with `textTheme` (using `colorScheme.onSecondary` for contrast).
  - Replace `AppBarTheme.color` with `AppBarTheme.backgroundColor`.

## Material 3 Guidelines
Material 3 is the default theme as of Flutter 3.16. 

- **Colors:** Generate color schemes using `ColorScheme.fromSeed(seedColor: Colors.blue)`. This ensures accessible contrast ratios.
- **Elevation:** Material 3 uses `ColorScheme.surfaceTint` to indicate elevation instead of just drop shadows. To revert to M2 shadow behavior, set `surfaceTint: Colors.transparent` and define a `shadowColor`.
- **Typography:** Material 3 updates font sizes, weights, and line heights. If text wrapping breaks legacy layouts, adjust `letterSpacing` on the specific `TextStyle`.
- **Modern Components:** 
  - Replace `BottomNavigationBar` with `NavigationBar`.
  - Replace `Drawer` with `NavigationDrawer`.
  - Replace `ToggleButtons` with `SegmentedButton`.
  - Use `FilledButton` for a high-emphasis button without the elevation of `ElevatedButton`.

## Component Theme Normalization
Component themes in `ThemeData` have been normalized to use `*ThemeData` classes rather than `*Theme` widgets. 

When defining `ThemeData`, strictly use the `*ThemeData` suffix for the following properties:
- `cardTheme`: Use `CardThemeData` (Not `CardTheme`)
- `dialogTheme`: Use `DialogThemeData` (Not `DialogTheme`)
- `tabBarTheme`: Use `TabBarThemeData` (Not `TabBarTheme`)
- `appBarTheme`: Use `AppBarThemeData` (Not `AppBarTheme`)
- `bottomAppBarTheme`: Use `BottomAppBarThemeData` (Not `BottomAppBarTheme`)
- `inputDecorationTheme`: Use `InputDecorationThemeData` (Not `InputDecorationTheme`)

## Button Styling
Legacy button classes (`FlatButton`, `RaisedButton`, `OutlineButton`) are obsolete. 

- Use `TextButton`, `ElevatedButton`, and `OutlinedButton`.
- Configure button appearance using a `ButtonStyle` object.
- For simple overrides based on the theme's color scheme, use the static utility method: `TextButton.styleFrom(foregroundColor: Colors.blue)`.
- For state-dependent styling (hovered, focused, pressed, disabled), use `MaterialStateProperty.resolveWith`.

## Platform Idioms & Adaptive Design
When building adaptive apps, respect platform-specific norms to reduce cognitive load and build user trust.

- **Scrollbars:** Desktop users expect omnipresent scrollbars; mobile users expect them only during scrolling. Toggle `thumbVisibility` on the `Scrollbar` widget based on the platform.
- **Selectable Text:** Web and desktop users expect text to be selectable. Wrap text in `SelectableText` or `SelectableText.rich`.
- **Horizontal Button Order:** Windows places confirmation buttons on the left; macOS/Linux place them on the right. Use a `Row` with `TextDirection.rtl` for Windows and `TextDirection.ltr` for others.
- **Context Menus & Tooltips:** Desktop users expect hover and right-click interactions. Implement `Tooltip` for hover states and use context menu packages for right-click actions.

## Workflows

### Workflow: Migrating Legacy Themes to Material 3
Use this workflow when updating an older Flutter codebase.

**Task Progress:**
- [ ] 1. Remove `useMaterial3: false` from `ThemeData` (it is true by default).
- [ ] 2. Replace manual `ColorScheme` definitions with `ColorScheme.fromSeed()`.
- [ ] 3. Run validator -> review errors -> fix: Search for and replace deprecated `accentColor`, `accentColorBrightness`, `accentIconTheme`, and `accentTextTheme`.
- [ ] 4. Run validator -> review errors -> fix: Search for `AppBarTheme(color: ...)` and replace with `backgroundColor`.
- [ ] 5. Update `ThemeData` component properties to use `*ThemeData` classes (e.g., `cardTheme: CardThemeData()`).
- [ ] 6. Replace legacy buttons (`FlatButton` -> `TextButton`, `RaisedButton` -> `ElevatedButton`, `OutlineButton` -> `OutlinedButton`).
- [ ] 7. Replace legacy navigation components (`BottomNavigationBar` -> `NavigationBar`, `Drawer` -> `NavigationDrawer`).

### Workflow: Implementing Adaptive UI Components
Use this workflow when building a widget intended for both mobile and desktop/web.

**Task Progress:**
- [ ] 1. If displaying a list/grid, wrap it in a `Scrollbar` and set `thumbVisibility: DeviceType.isDesktop`.
- [ ] 2. If displaying read-only data, use `SelectableText` instead of `Text`.
- [ ] 3. If implementing a dialog with action buttons, check the platform. If Windows, set `TextDirection.rtl` on the button `Row`.
- [ ] 4. If implementing interactive elements, wrap them in `Tooltip` widgets to support mouse hover states.

## Examples

### Example: Modern Material 3 ThemeData Setup
```dart
MaterialApp(
  title: 'Adaptive App',
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.deepPurple,
      brightness: Brightness.light,
    ),
    // Use *ThemeData classes for component normalization
    appBarTheme: const AppBarThemeData(
      backgroundColor: Colors.deepPurple, // Do not use 'color'
      elevation: 0,
    ),
    cardTheme: const CardThemeData(
      elevation: 2,
    ),
    textTheme: const TextTheme(
      bodyMedium: TextStyle(letterSpacing: 0.2),
    ),
  ),
  home: const MyHomePage(),
);
```

### Example: State-Dependent ButtonStyle
```dart
TextButton(
  style: ButtonStyle(
    // Default color
    foregroundColor: MaterialStateProperty.all<Color>(Colors.blue),
    // State-dependent overlay color
    overlayColor: MaterialStateProperty.resolveWith<Color?>(
      (Set<MaterialState> states) {
        if (states.contains(MaterialState.hovered)) {
          return Colors.blue.withOpacity(0.04);
        }
        if (states.contains(MaterialState.focused) || states.contains(MaterialState.pressed)) {
          return Colors.blue.withOpacity(0.12);
        }
        return null; // Defer to the widget's default.
      },
    ),
  ),
  onPressed: () {},
  child: const Text('Adaptive Button'),
)
```

### Example: Adaptive Dialog Button Order
```dart
Row(
  // Windows expects confirmation on the left (RTL reverses the standard LTR Row)
  textDirection: Platform.isWindows ? TextDirection.rtl : TextDirection.ltr,
  mainAxisAlignment: MainAxisAlignment.end,
  children: [
    TextButton(
      onPressed: () => Navigator.pop(context, false),
      child: const Text('Cancel'),
    ),
    FilledButton(
      onPressed: () => Navigator.pop(context, true),
      child: const Text('Confirm'),
    ),
  ],
)
```
