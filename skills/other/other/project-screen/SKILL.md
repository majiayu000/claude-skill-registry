---
name: project-screen
description: Guide for creating screens with routing conventions (name/path constants) and adaptive scaffold (project)
---

# Flutter Screen Development Skill

This skill guides the creation of screens following this project's routing and layout conventions.

## When to Use

Trigger this skill when:
- Creating a new screen or page
- Adding a route to the application
- User asks to "create a screen", "add a page", or "implement a new view"

## Mason Template

**Always use Mason template first:**

```bash
# Basic screen with optional subfolder
mason make screen --name ScreenName --folder subfolder

# Options available:
# --has_adaptive_scaffold: Use AppAdaptiveScaffold (default: true)
# --has_app_bar: Include SliverAppBar (default: true)
```

## Project Structure

Screens are organized in `lib/screens/` by domain:

```
lib/screens/
├── app/                    # App-level screens (splash, error)
│   ├── splash_screen.dart
│   └── error_screen.dart
├── home/                   # Home feature
│   └── home_screen.dart
├── settings/               # Settings feature
│   ├── settings_screen.dart
│   ├── appearance_settings_screen.dart
│   └── accent_color_settings_screen.dart
└── showcase/               # Demo/example screens
    └── showcase_screen.dart
```

## Routing Convention (MANDATORY)

Every screen MUST define static route constants:

```dart
class ProfileScreen extends StatelessWidget {
  static const name = 'Profile Screen';  // Display name
  static const path = '/profile';         // GoRouter path

  const ProfileScreen({super.key});
  // ...
}
```

## Screen Template

```dart
import 'package:app_adaptive_widgets/app_adaptive_widgets.dart';
import 'package:app_locale/app_locale.dart';
import 'package:flutter/material.dart';
import 'package:flutter_app_template/destination.dart';

class ExampleScreen extends StatelessWidget {
  static const name = 'Example Screen';
  static const path = '/example';

  const ExampleScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return AppAdaptiveScaffold(
      selectedIndex: Destinations.indexOf(const Key(ExampleScreen.name), context),
      onSelectedIndexChange: (idx) => Destinations.changeHandler(idx, context),
      destinations: Destinations.navs(context),
      appBar: AppBar(
        title: Text(context.l10n.screenTitle),
        centerTitle: true,
        foregroundColor: Theme.of(context).colorScheme.onPrimary,
        backgroundColor: Theme.of(context).colorScheme.primary,
      ),
      body: (context) => SafeArea(
        child: Center(
          child: Text('Screen content'),
        ),
      ),
    );
  }
}
```

## Router Integration

After creating a screen, add it to `lib/router.dart`:

```dart
GoRoute(
  name: ExampleScreen.name,
  path: ExampleScreen.path,
  pageBuilder: (context, state) => NoTransitionPage(
    key: state.pageKey,
    child: const ExampleScreen(),
  ),
),
```

## Navigation Destinations

For screens in the main navigation, update `lib/destination.dart`:

```dart
static List<NavigationDestination> navs(BuildContext context) {
  return [
    // existing destinations...
    NavigationDestination(
      key: Key(ExampleScreen.name),
      icon: const Icon(Icons.example),
      label: context.l10n.example,
    ),
  ];
}
```

## Key Dependencies

```dart
import 'package:app_adaptive_widgets/app_adaptive_widgets.dart';  // Responsive layout
import 'package:app_locale/app_locale.dart';                      // Localization
import 'package:app_artwork/app_artwork.dart';                    // Icons, animations
import 'package:flutter_app_template/destination.dart';           // Navigation
```

## AppAdaptiveScaffold Features

### Responsive Body Slots

```dart
AppAdaptiveScaffold(
  // Main body - used for medium+ breakpoints
  body: (context) => MainContent(),

  // Small screen body (mobile)
  smallBody: (context) => MobileContent(),

  // Medium-large screen body (tablet)
  mediumLargeBody: (context) => TabletContent(),

  // Large screen body (desktop)
  largeBody: (context) => DesktopContent(),

  // Extra large screen body
  extraLargeBody: (context) => WideDesktopContent(),
)
```

### Secondary Body (Split View)

```dart
AppAdaptiveScaffold(
  body: (context) => ListView(...),

  // Secondary panel (detail view)
  secondaryBody: (context) => DetailView(),

  // Hide secondary on small screens
  smallSecondaryBody: AdaptiveScaffold.emptyBuilder,

  // Body to secondary ratio (0.3 = 30% body, 70% secondary)
  bodyRatio: 0.3,

  // Orientation of split
  bodyOrientation: Axis.horizontal, // or Axis.vertical
)
```

### Collapsible Navigation Rail

```dart
AppAdaptiveScaffold(
  // Enable collapse toggle button
  showCollapseToggle: true,

  // Custom icons for toggle
  collapseIcon: Icons.menu_open,
  expandIcon: Icons.menu,

  // Control extended state externally
  isExtendedOverride: isNavExtended,

  // Listen for state changes
  onExtendedChange: (isExtended) {
    setState(() => isNavExtended = isExtended);
  },
)
```

### Navigation Rail Customization

```dart
AppAdaptiveScaffold(
  // Leading widget (collapsed state)
  leadingUnextendedNavRail: Icon(Icons.menu),

  // Leading widget (extended state)
  leadingExtendedNavRail: Text('My App'),

  // Trailing widget below destinations
  trailingNavRail: IconButton(icon: Icon(Icons.logout), onPressed: logout),

  // Rail width
  navigationRailWidth: 72,
  extendedNavigationRailWidth: 192,

  // Destination alignment
  groupAlignment: -1.0, // Top aligned
)
```

### Drawer Configuration

```dart
AppAdaptiveScaffold(
  // Use drawer instead of bottom nav on small desktop
  useDrawer: true,

  // Custom breakpoint for drawer
  drawerBreakpoint: Breakpoints.smallDesktop,

  // Custom app bar when using drawer
  appBar: AppBar(title: Text('My App')),

  // Breakpoint to show app bar
  appBarBreakpoint: Breakpoints.small,
)
```

### Breakpoints Reference

- `Breakpoints.small` - Mobile (< 600px)
- `Breakpoints.medium` - Tablet (600-840px)
- `Breakpoints.mediumLarge` - Small desktop (840-1200px)
- `Breakpoints.large` - Desktop (1200-1600px)
- `Breakpoints.extraLarge` - Wide desktop (> 1600px)

## AppAdaptiveAction (Responsive Action Buttons)

For action buttons that adapt to screen size:

```dart
// Define actions
final actions = [
  AppAdaptiveAction(
    title: 'Edit',
    icon: Icons.edit,
    onPressed: () => handleEdit(),
  ),
  AppAdaptiveAction(
    title: 'Delete',
    icon: Icons.delete,
    onPressed: () => handleDelete(),
    disabled: !canDelete,
  ),
];

// Display in AppBar or elsewhere
AppAdaptiveActionList(
  actions: actions,
  size: AppAdaptiveActionSize.medium, // small, medium, large
  direction: Axis.horizontal,
  hideDisabled: true,
)
```

**Action Sizes:**
- `small` - Popup menu (overflow menu)
- `medium` - Icon buttons only
- `large` - Text buttons with icons

## Localization

Add screen text to `app_lib/locale/lib/l10n/app_en.arb`:

```json
{
  "exampleTitle": "Example",
  "@exampleTitle": {
    "description": "Title for the example screen"
  }
}
```

Then run: `melos run gen-l10n`

## Testing

Create screen tests in `test/screens/`:

```dart
testWidgets('ExampleScreen renders correctly', (tester) async {
  await tester.pumpWidget(
    MaterialApp(home: ExampleScreen()),
  );
  expect(find.text('Example'), findsOneWidget);
});
```

Run tests: `flutter test test/screens/example_screen_test.dart`
