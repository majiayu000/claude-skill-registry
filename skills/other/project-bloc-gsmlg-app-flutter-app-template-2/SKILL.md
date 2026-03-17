---
name: project-bloc
description: Guide for creating BLoC patterns with events, states, and proper structure in app_bloc packages (project)
---

# Flutter BLoC Development Skill

This skill guides the creation of BLoC (Business Logic Component) packages following this project's conventions.

## When to Use

Trigger this skill when:
- Creating a new BLoC package
- Adding events or states to an existing BLoC
- Implementing business logic that manages application state
- User asks to "create a bloc", "add state management", or "implement feature with BLoC"

## Mason Templates Available

**Always use Mason templates first:**

```bash
# Simple BLoC (basic state management)
mason make simple_bloc -o app_bloc/feature_name --name=feature_name

# List BLoC (for managing lists with CRUD operations)
mason make list_bloc -o app_bloc/feature_name --name=feature_name

# Form BLoC (for form validation and submission)
mason make form_bloc --name Login --field_names "email,password"
```

## Project Structure

BLoC packages MUST be created in `app_bloc/`:

```
app_bloc/
└── feature_name/
    ├── lib/
    │   ├── feature_name_bloc.dart  # Barrel export file
    │   └── src/
    │       ├── bloc.dart           # BLoC class with event handlers
    │       ├── event.dart          # Event definitions
    │       └── state.dart          # State class with status enum
    ├── test/
    │   └── feature_name_bloc_test.dart
    └── pubspec.yaml
```

## BLoC Pattern Conventions

### Event Naming
- Events are named as actions: `LoadData`, `SubmitForm`, `ChangeTheme`
- Use past tense for completed actions: `DataLoaded`, `FormSubmitted`

### State Structure
- States use a status enum: `initial`, `loading`, `completed`, `error`
- Use `copyWith()` for immutable state updates
- Extend `Equatable` for proper state comparison

### Event Handlers
- Prefix handlers with `_on`: `_onLoadData`, `_onSubmitForm`
- Use `Emitter<State>` for state emissions
- Handle errors with try-catch and emit error states

## Reference Implementation

ThemeBloc (`app_bloc/theme/`) serves as the reference implementation:

```dart
class ThemeBloc extends Bloc<ThemeEvent, ThemeState> {
  ThemeBloc(this.pref) : super(ThemeState.initial(pref)) {
    on<ChangeTheme>(_onThemeChanged);
    on<ChangeThemeMode>(_onThemeModeChanged);
  }

  Future<void> _onThemeChanged(
    ChangeTheme event,
    Emitter<ThemeState> emitter,
  ) async {
    emitter(state.copyWith(theme: event.theme));
    pref.setString('themeName', event.theme.name);
  }
}
```

## Dependencies

In `pubspec.yaml`, use workspace resolution:

```yaml
dependencies:
  bloc: any
  flutter_bloc: any
  equatable: any
```

## Testing Requirements

Every BLoC MUST have tests in `test/` directory:
- Test initial state
- Test each event handler
- Test state transitions
- Test error handling

Run tests: `cd app_bloc/feature_name && flutter test`

## Integration with UI

Use `BlocProvider` and `BlocBuilder` from `flutter_bloc`:

```dart
BlocProvider(
  create: (context) => FeatureBloc(),
  child: BlocBuilder<FeatureBloc, FeatureState>(
    builder: (context, state) {
      // Build UI based on state
    },
  ),
)
```
