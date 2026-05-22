---
name: android-project
description: Navigate and analyze Android project structure, modules, and dependencies. Use when exploring project structure, finding related files, analyzing dependencies, or locating code patterns.
license: MIT
version: 1.0.0
---

# Android Project Skill

Navigate and analyze Android project structure, modules, and dependencies.

## When to Use

- Exploring project structure
- Finding related files
- Analyzing module dependencies
- Understanding package organization
- Locating specific code patterns

## Standard Android Project Structure

```
android-app/
├── app/src/
│   ├── main/java/com/example/app/
│   │   ├── biz/                    # Business logic layer
│   │   │   ├── manage/             # Managers (GameManager, UserManager)
│   │   │   ├── service/            # Services (AuthService, SyncService)
│   │   │   ├── repo/               # Repositories
│   │   │   └── util/               # Utilities
│   │   ├── di/                     # Dependency injection (Koin/Hilt)
│   │   └── ui/                     # Presentation layer
│   │       ├── launcher/           # Screens by feature
│   │       ├── component/          # Reusable components
│   │       ├── navigation/         # NavRoutes, NavHost
│   │       ├── viewmodel/          # ViewModels
│   │       └── theme/              # Theme definitions
│   └── test/                       # Unit tests
├── docs/                           # Documentation
├── gradle/                         # Gradle config
└── CLAUDE.md                       # AI dev guide
```

## File Patterns

### By Layer

| Layer | Pattern | Example |
|-------|---------|---------|
| Manager | `biz/manage/**/*Manager*.kt` | GameManagerImpl.kt |
| Service | `biz/service/**/*Service*.kt` | AuthService.kt |
| Repository | `biz/repo/**/*Repository*.kt` | QuestionRepository.kt |
| ViewModel | `ui/viewmodel/*ViewModel.kt` | GameViewModel.kt |
| Screen | `ui/launcher/**/*Route.kt` | GameRoute.kt |
| Component | `ui/component/**/*.kt` | QzdsGameButton.kt |
| Test | `test/**/*Test.kt` | GameManagerImplTest.kt |

### Common Search Commands

```bash
# Find all ViewModels
find . -name "*ViewModel.kt" -type f

# Find all Route composables
grep -r "@Composable.*fun.*Route" --include="*.kt"

# Find class definition
grep -rn "class GameManager" --include="*.kt"

# Find class usages
grep -rn "GameManager" --include="*.kt" | grep -v "class GameManager"

# Find test file
find . -name "*GameManagerImplTest.kt" -type f
```

## Architecture Navigation

### MVVM Layer Flow
```
UI (Route) → ViewModel → Manager/UseCase → Repository → DataSource
```

### Key File Types

| Purpose | Naming Convention |
|---------|------------------|
| Entry point | `LauncherActivity.kt`, `App.kt` |
| DI setup | `AppModule.kt`, `*Module.kt` |
| Navigation | `NavRoutes.kt`, `AppNavHost.kt` |
| State machine | `*Phase.kt`, `*State.kt` |
| Session | `Current*Session.kt` |

## Dependency Analysis

```bash
# Show full dependency tree
./gradlew dependencies

# Show specific module dependencies
./gradlew :app:dependencies --configuration implementation

# Check for version conflicts
./gradlew dependencies | grep -E "^\+---|^\\\\---" | grep "->"
```

## Quick Navigation Tips

1. **Find related files**: Search for class name across project
2. **Trace data flow**: Follow imports from UI → ViewModel → Manager
3. **Find tests**: Replace `Impl.kt` with `ImplTest.kt`
4. **Check DI**: Look in `AppModule.kt` for registration

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't find class | Check import statements, package name |
| Missing dependency | Verify DI module registration |
| Test not found | Ensure test in correct source set |
| Circular dependency | Review DI graph in AppModule |

## Command Workflows

```bash
# Full codebase exploration
find . -name "*.kt" -type f | head -20  # List Kotlin files
grep -rn "class.*Manager" --include="*.kt"  # Find managers
grep -rn "koinViewModel" --include="*.kt"  # Find ViewModel injections

# Feature impact analysis
grep -rn "GameManager" --include="*.kt" | wc -l  # Count usages
git log --oneline --follow -- "**/GameManager*.kt"  # File history
```

## References

- [Android App Architecture](https://developer.android.com/topic/architecture)
- [Koin Documentation](https://insert-koin.io/docs/quickstart/android)
- [Navigation Component](https://developer.android.com/guide/navigation)

Use this skill to quickly locate files and understand relationships.
