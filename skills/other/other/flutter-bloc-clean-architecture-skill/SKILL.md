---
name: flutter-bloc-development
description: Build Flutter features using BLoC state management, clean architecture layers, and the project's design system. Apply when creating screens, widgets, or data integrations.
license: Complete terms in LICENSE.txt
---

# Flutter BLoC Development

This skill enforces BLoC state management, strict layer separation, and mandatory use of design system constants for all Flutter development in this codebase.

## Decision Tree: Choosing Your Approach

```
User task → What are they building?
    │
    ├─ New screen/feature → Full feature implementation:
    │   1. Create feature folder (lib/[feature]/)
    │   2. Define BLoC (bloc/[feature]_event.dart, _state.dart, _bloc.dart)
    │   3. Create data layer (data/datasources/, data/repositories/, data/models/)
    │   4. Build UI (view/[feature]_page.dart, view/widgets/)
    │   5. Create barrel files ([feature].dart, data/data.dart, view/view.dart)
    │
    ├─ New widget only → Presentation layer:
    │   1. Feature-specific: feature/view/widgets/
    │   2. Shared/reusable: shared/widgets/
    │   3. Use design system constants (NO hardcoded values)
    │   4. Connect to existing BLoC if needed
    │
    ├─ Data integration → Data layer only:
    │   1. Create datasource (feature/data/datasources/)
    │   2. Create repository (feature/data/repositories/)
    │   3. Wire up in existing or new BLoC
    │
    └─ Refactoring → Identify violations:
        1. Check for hardcoded colors/spacing/typography
        2. Check for business logic in UI
        3. Check for direct SDK calls outside datasources
        4. Check for missing Loading state before async operations
        5. Check for missing Equatable on Events/States
        6. Check for improper error handling (use SnackBar + AppColors.error)
```

## Architecture at a Glance

**Feature-first structure** (official BLoC recommendation):

```
lib/
├── [feature]/                    # Feature folder (e.g., earnings/, auth/, trips/)
│   ├── bloc/
│   │   ├── [feature]_bloc.dart
│   │   ├── [feature]_event.dart
│   │   └── [feature]_state.dart
│   ├── data/
│   │   ├── datasources/          # Feature-specific API calls
│   │   ├── repositories/         # Data orchestration
│   │   ├── models/               # Feature-specific DTOs
│   │   └── data.dart             # Data layer barrel file
│   ├── view/
│   │   ├── [feature]_page.dart   # Main screen
│   │   ├── widgets/              # Feature-specific widgets
│   │   └── view.dart             # View barrel file
│   └── [feature].dart            # Feature barrel file
├── shared/                       # Cross-feature code
│   ├── data/
│   │   ├── datasources/          # Shared API clients (ApiClient, UserDataSource)
│   │   ├── models/               # Shared models (User, ApiResponse)
│   │   └── data.dart             # Shared data barrel file
│   ├── widgets/                  # Reusable UI components
│   └── utils/                    # Design system (colors, spacing, typography)
└── app.dart                      # App entry point
```

### When to Use Feature vs Shared Data

| Scenario | Location | Example |
|----------|----------|---------|
| API endpoints used by ONE feature | `feature/data/` | `EarningsDataSource` → `/api/earnings/...` |
| API client/service used by MANY features | `shared/data/` | `ApiClient`, `UserDataSource` |
| Models used by ONE feature | `feature/data/models/` | `EarningsSummary` |
| Models used by MANY features | `shared/data/models/` | `User`, `ApiResponse` |

**Barrel Files** — Single import per layer:
```dart
// Feature barrel: earnings/earnings.dart
export 'bloc/earnings_bloc.dart';
export 'bloc/earnings_event.dart';
export 'bloc/earnings_state.dart';
export 'data/data.dart';
export 'view/view.dart';

// Data layer barrel: earnings/data/data.dart
export 'datasources/earnings_datasource.dart';
export 'repositories/earnings_repository.dart';
export 'models/earnings_summary.dart';

// Shared data barrel: shared/data/data.dart
export 'datasources/api_client.dart';
export 'datasources/user_datasource.dart';
export 'models/user.dart';
```

**Key Rules:**
- All state changes flow through BLoC
- No direct backend SDK calls outside datasources
- Zero hardcoded values (colors, spacing, typography)
- Repository pattern for all data access
- Feature-specific code stays in feature folder
- Shared code (used by 2+ features) goes in `shared/`

---

## BLoC Implementation

### Event → State → BLoC (Three Files Per Feature)

**Events** — User actions and system triggers:
```dart
abstract class FeatureEvent extends Equatable {
  const FeatureEvent();
  @override
  List<Object?> get props => [];
}

class FeatureActionRequested extends FeatureEvent {
  final String param;
  const FeatureActionRequested({required this.param});
  @override
  List<Object> get props => [param];
}
```

**States** — All possible UI states:
```dart
abstract class FeatureState extends Equatable {
  const FeatureState();
  @override
  List<Object?> get props => [];
}

class FeatureInitial extends FeatureState {}
class FeatureLoading extends FeatureState {}

class FeatureSuccess extends FeatureState {
  final DataType data;
  const FeatureSuccess(this.data);
  @override
  List<Object> get props => [data];
}

class FeatureError extends FeatureState {
  final String message;
  const FeatureError(this.message);
  @override
  List<Object> get props => [message];
}
```

**BLoC** — Event handlers with Loading → Success/Error pattern:
```dart
class FeatureBloc extends Bloc<FeatureEvent, FeatureState> {
  final FeatureRepository _repository;

  FeatureBloc({required FeatureRepository repository})
      : _repository = repository,
        super(FeatureInitial()) {
    on<FeatureActionRequested>(_onActionRequested);
  }

  Future<void> _onActionRequested(
    FeatureActionRequested event,
    Emitter<FeatureState> emit,
  ) async {
    emit(FeatureLoading());
    try {
      final result = await _repository.doSomething(event.param);
      emit(FeatureSuccess(result));
    } catch (e) {
      emit(FeatureError(e.toString()));
    }
  }
}
```

**CRITICAL**: Always emit `Loading` before async work, then `Success` or `Error`. Never skip the loading state.

---

## Data Layer

**Data Flow:**
```
UI Event → BLoC (emit Loading) → Repository → Datasource (SDK)
    ↓
Response → Repository (map to entity) → BLoC (emit Success/Error) → UI
```

**Datasource** — Backend SDK calls only:
```dart
class FeatureDataSource {
  final SupabaseClient _supabase;
  FeatureDataSource(this._supabase);

  Future<Map<String, dynamic>> fetch() async {
    return await _supabase.from('table').select().single();
  }
}
```

**Repository** — Orchestration and mapping:
```dart
class FeatureRepository {
  final FeatureDataSource _dataSource;
  FeatureRepository(this._dataSource);

  Future<DomainEntity> fetchData() async {
    final response = await _dataSource.fetch();
    return DomainEntity.fromJson(response);
  }
}
```

---

## Design System (Non-Negotiable)

### Colors
✅ `AppColors.primary`, `AppColors.error`, `AppColors.textPrimary`
❌ `Color(0xFF...)`, `Colors.blue`, inline hex values

### Spacing
✅ `AppSpacing.xs` (4), `AppSpacing.sm` (8), `AppSpacing.md` (16), `AppSpacing.lg` (24), `AppSpacing.xl` (32)
✅ `AppSpacing.screenHorizontal` (24), `AppSpacing.screenVertical` (16)
❌ `EdgeInsets.all(16.0)`, hardcoded padding values

### Border Radius
✅ `AppRadius.sm` (8), `AppRadius.md` (12), `AppRadius.lg` (16), `AppRadius.xl` (24)
❌ `BorderRadius.circular(12)`, inline radius values

### Typography
✅ `AppTypography.headlineLarge`, `AppTypography.bodyMedium`, `theme.textTheme.bodyMedium`
❌ `TextStyle(fontSize: 16)`, inline text styles

---

## UI Patterns

### Screen Template
```dart
GradientScaffold(
  body: SafeArea(
    child: Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(AppSpacing.screenHorizontal),
          child: HeaderWidget(),
        ),
        Expanded(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: AppSpacing.screenHorizontal),
            child: ContentWidget(),
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(AppSpacing.screenHorizontal),
          child: ActionButton(
            onPressed: () => context.read<FeatureBloc>().add(ActionEvent()),
          ),
        ),
      ],
    ),
  ),
)
```

### BLoC Consumer Pattern
```dart
BlocConsumer<FeatureBloc, FeatureState>(
  listener: (context, state) {
    if (state is FeatureError) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.message), backgroundColor: AppColors.error),
      );
    }
  },
  builder: (context, state) {
    if (state is FeatureLoading) return const Center(child: CircularProgressIndicator());
    if (state is FeatureSuccess) return SuccessWidget(data: state.data);
    return const SizedBox.shrink();
  },
)
```

---

## Common Pitfalls

❌ Business logic in widgets → Move to BLoC
❌ Direct Supabase/Firebase calls in repository → Move to datasource
❌ Skipping loading state before async operations → Always emit Loading first
❌ Hardcoded colors like `Color(0xFF4A90A4)` → Use `AppColors.primary`
❌ Magic numbers like `padding: 16` → Use `AppSpacing.md`

---

## Quick Reference

| Action | Pattern |
|--------|---------|
| Dispatch event | `context.read<Bloc>().add(Event())` |
| Watch state inline | `context.watch<Bloc>().state` |
| Listen + Build | `BlocConsumer` |
| Listen only | `BlocListener` |
| Build only | `BlocBuilder` |

---

## Checklist Before Submitting

- [ ] Events/States/BLoC use `Equatable`
- [ ] All async: Loading → Success/Error
- [ ] No business logic in UI
- [ ] No SDK calls outside datasources
- [ ] Zero hardcoded colors/spacing/typography
- [ ] Error handling shows SnackBar with `AppColors.error`
- [ ] Code formatted with `dart format`