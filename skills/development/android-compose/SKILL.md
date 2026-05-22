---
name: android-compose
description: |
  Jetpack Compose framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Android Compose projects, or when the user mentions Jetpack Compose.
  Provides composable patterns, state management, Material 3, navigation, and lifecycle guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: kotlin
  extensions: ".kt"
---

# Android Jetpack Compose Guide

> Applies to: Android SDK 24+, Jetpack Compose 1.5+, Kotlin 1.9+, Material Design 3

## Core Principles

1. **Declarative UI**: Describe what the UI should look like, not how to build it step-by-step
2. **Unidirectional Data Flow**: State flows down, events flow up -- always
3. **Composable Functions Are Cheap**: The framework handles when to recompose; keep composables pure
4. **State Hoisting**: Lift state to the nearest common ancestor that needs it
5. **Lifecycle Awareness**: Collect flows with `collectAsStateWithLifecycle()`, never raw `collectAsState()`

## Guardrails

### Composable Conventions

- Every composable accepts `modifier: Modifier = Modifier` as its first optional parameter
- Keep composables small and focused (one responsibility per function)
- Use `@Preview` on every reusable component with representative data
- Never perform side effects (network, DB, analytics) directly inside a composable body
- Use `LaunchedEffect`, `DisposableEffect`, or `SideEffect` for side-effect work
- Prefer stateless composables; hoist state to the caller or ViewModel

```kotlin
// BAD: side effects in composition
@Composable
fun UserList(users: List<User>) {
    analytics.trackScreenView("user_list") // fires on every recomposition
    LazyColumn { ... }
}

// GOOD: side effect in LaunchedEffect
@Composable
fun UserList(users: List<User>) {
    LaunchedEffect(Unit) {
        analytics.trackScreenView("user_list")
    }
    LazyColumn { ... }
}
```

### State Management

- Use `StateFlow` in ViewModel, collect with `collectAsStateWithLifecycle()`
- Model UI state as a sealed interface (`Loading`, `Success`, `Error`)
- Never expose `MutableStateFlow` publicly from a ViewModel
- Use `remember` for local composable state; `rememberSaveable` when it must survive config changes
- Use `derivedStateOf` for expensive computations that depend on other state

```kotlin
// Sealed UI state pattern
sealed interface HomeUiState {
    data object Loading : HomeUiState
    data class Success(val users: List<User>) : HomeUiState
    data class Error(val message: String) : HomeUiState
}

// ViewModel exposes immutable StateFlow
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val userRepository: UserRepository,
) : ViewModel() {
    private val _uiState = MutableStateFlow<HomeUiState>(HomeUiState.Loading)
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    fun loadUsers() {
        viewModelScope.launch {
            _uiState.value = HomeUiState.Loading
            userRepository.getUsers()
                .catch { e -> _uiState.value = HomeUiState.Error(e.message ?: "Unknown error") }
                .collect { users -> _uiState.value = HomeUiState.Success(users) }
        }
    }
}

// Screen collects lifecycle-aware
@Composable
fun HomeScreen(viewModel: HomeViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    when (val state = uiState) {
        is HomeUiState.Loading -> LoadingIndicator()
        is HomeUiState.Success -> UserList(state.users)
        is HomeUiState.Error -> ErrorMessage(state.message, onRetry = viewModel::loadUsers)
    }
}
```

### Navigation

- Define routes as a sealed class or sealed interface for type safety
- Never pass complex objects as navigation arguments; pass IDs and load from ViewModel
- Clear back stack correctly with `popUpTo` and `inclusive` when navigating to auth screens
- Use `hiltViewModel()` inside `composable {}` blocks for scoped ViewModels

```kotlin
sealed class Screen(val route: String) {
    data object Login : Screen("login")
    data object Home : Screen("home")
    data object Detail : Screen("detail/{userId}") {
        fun createRoute(userId: String) = "detail/$userId"
    }
}

@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = Screen.Home.route) {
        composable(Screen.Home.route) {
            HomeScreen(onUserClick = { userId ->
                navController.navigate(Screen.Detail.createRoute(userId))
            })
        }
        composable(
            route = Screen.Detail.route,
            arguments = listOf(navArgument("userId") { type = NavType.StringType }),
        ) { backStackEntry ->
            val userId = backStackEntry.arguments?.getString("userId") ?: ""
            DetailScreen(userId = userId, onBack = { navController.popBackStack() })
        }
    }
}
```

### Material 3 Theming

- Always wrap the app root in your custom `MaterialTheme` composable
- Support dynamic color on Android 12+ with `dynamicLightColorScheme` / `dynamicDarkColorScheme`
- Define color tokens in a dedicated `Color.kt`; typography in `Type.kt`; theme in `Theme.kt`
- Use `MaterialTheme.colorScheme.*` and `MaterialTheme.typography.*` instead of hardcoded values
- Support both light and dark themes from day one

```kotlin
@Composable
fun MyAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit,
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }
    MaterialTheme(colorScheme = colorScheme, typography = Typography, content = content)
}
```

### Dependency Injection (Hilt)

- Annotate `Application` with `@HiltAndroidApp`, `Activity` with `@AndroidEntryPoint`
- Annotate ViewModels with `@HiltViewModel` and use `@Inject constructor`
- Use `hiltViewModel()` in composables, never construct ViewModels manually
- Organize DI modules by layer: `AppModule`, `NetworkModule`, `DatabaseModule`

### Lifecycle & Effects

| Effect | Trigger | Use for |
|--------|---------|---------|
| `LaunchedEffect(key)` | On enter + when key changes | One-shot loads, navigation events |
| `DisposableEffect(key)` | On enter + when key changes (with cleanup) | Listeners, observers, callbacks |
| `SideEffect` | After every successful recomposition | Syncing compose state to non-compose |
| `rememberCoroutineScope()` | Manual launch from callbacks | Button clicks launching coroutines |

```kotlin
// One-shot load on screen enter
LaunchedEffect(Unit) { viewModel.loadData() }

// Clean up a listener when leaving composition
DisposableEffect(lifecycleOwner) {
    val observer = LifecycleEventObserver { _, event -> ... }
    lifecycleOwner.lifecycle.addObserver(observer)
    onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
}
```

## Project Structure

```
app/src/main/java/com/example/myapp/
├── MyApplication.kt               # @HiltAndroidApp
├── MainActivity.kt                # @AndroidEntryPoint, setContent {}
├── navigation/
│   └── AppNavigation.kt           # NavHost, route definitions
├── ui/
│   ├── theme/                     # Color.kt, Type.kt, Theme.kt
│   ├── screens/                   # Feature screens
│   │   ├── home/
│   │   │   ├── HomeScreen.kt      # Composable
│   │   │   └── HomeViewModel.kt   # ViewModel + UiState
│   │   └── detail/
│   │       ├── DetailScreen.kt
│   │       └── DetailViewModel.kt
│   └── components/                # Shared composables
│       ├── LoadingIndicator.kt
│       └── ErrorMessage.kt
├── data/
│   ├── model/                     # Domain models (@Serializable)
│   ├── remote/                    # Retrofit service, DTOs
│   ├── local/                     # Room database, DAOs
│   └── repository/                # Repository implementations
└── di/                            # Hilt modules
    ├── AppModule.kt
    └── NetworkModule.kt
```

- **ui/screens/**: One sub-package per feature, each with `Screen.kt` + `ViewModel.kt`
- **ui/components/**: Reusable composables shared across screens
- **data/**: Models, repositories, API services; no Compose dependencies here
- **di/**: Hilt modules providing singletons and scoped dependencies

## Key Dependencies

```kotlin
// build.gradle.kts (app)
val composeBom = platform("androidx.compose:compose-bom:2024.01.00")
implementation(composeBom)
implementation("androidx.compose.ui:ui")
implementation("androidx.compose.material3:material3")
implementation("androidx.compose.ui:ui-tooling-preview")
implementation("androidx.activity:activity-compose:1.8.2")
implementation("androidx.lifecycle:lifecycle-runtime-compose:2.7.0")
implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
implementation("androidx.navigation:navigation-compose:2.7.6")
implementation("androidx.hilt:hilt-navigation-compose:1.1.0")
implementation("com.google.dagger:hilt-android:2.50")
ksp("com.google.dagger:hilt-compiler:2.50")
implementation("io.coil-kt:coil-compose:2.5.0")

// Testing
testImplementation("junit:junit:4.13.2")
testImplementation("io.mockk:mockk:1.13.9")
testImplementation("app.cash.turbine:turbine:1.0.0")
testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
androidTestImplementation(composeBom)
androidTestImplementation("androidx.compose.ui:ui-test-junit4")
debugImplementation("androidx.compose.ui:ui-tooling")
debugImplementation("androidx.compose.ui:ui-test-manifest")
```

## Testing

### ViewModel Unit Tests

- Use `StandardTestDispatcher` + `Dispatchers.setMain()` for coroutine control
- Use Turbine for `StateFlow` assertions
- Use MockK with `coEvery` / `coVerify` for suspend function mocking
- Reset dispatcher in `@After` with `Dispatchers.resetMain()`

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class HomeViewModelTest {
    private val testDispatcher = StandardTestDispatcher()
    private val userRepository = mockk<UserRepository>()

    @Before fun setup() { Dispatchers.setMain(testDispatcher) }
    @After fun tearDown() { Dispatchers.resetMain() }

    @Test
    fun `loadUsers emits Success state on valid data`() = runTest {
        val users = listOf(User(id = "1", email = "a@b.com", name = "Alice"))
        coEvery { userRepository.getUsers() } returns flowOf(users)

        val viewModel = HomeViewModel(userRepository)
        advanceUntilIdle()

        viewModel.uiState.test {
            val state = awaitItem()
            assertTrue(state is HomeUiState.Success)
            assertEquals(users, (state as HomeUiState.Success).users)
        }
    }
}
```

### Compose UI Tests

- Use `createComposeRule()` for isolated composable tests
- Query nodes with `onNodeWithText`, `onNodeWithTag`, `onNodeWithContentDescription`
- Assert with `assertExists()`, `assertIsDisplayed()`, `assertIsEnabled()`
- Perform actions with `performClick()`, `performTextInput()`

```kotlin
class HomeScreenTest {
    @get:Rule val composeTestRule = createComposeRule()

    @Test
    fun displays_user_name_when_loaded() {
        composeTestRule.setContent {
            MyAppTheme {
                UserCard(user = User("1", "a@b.com", "Alice"), onClick = {}, onDeleteClick = {})
            }
        }
        composeTestRule.onNodeWithText("Alice").assertIsDisplayed()
        composeTestRule.onNodeWithText("a@b.com").assertIsDisplayed()
    }
}
```

## Commands

```bash
# Build
./gradlew assembleDebug            # Debug APK
./gradlew assembleRelease          # Release APK
./gradlew bundleRelease            # AAB for Play Store

# Test
./gradlew test                     # Unit tests
./gradlew connectedAndroidTest     # Instrumented tests on device/emulator

# Quality
./gradlew lint                     # Android Lint
./gradlew ktlintCheck              # Code style check
./gradlew ktlintFormat             # Auto-fix formatting
./gradlew detekt                   # Static analysis

# Install & Run
./gradlew installDebug             # Install on connected device
./gradlew clean                    # Clean build artifacts
```

## Best Practices Summary

### Do

- Use `collectAsStateWithLifecycle()` for all Flow collection in composables
- Use `remember {}` for expensive local computations
- Use `LaunchedEffect` for one-shot side effects, `DisposableEffect` for cleanup
- Keep composables stateless; hoist state to ViewModel or caller
- Use sealed interfaces for UI state with exhaustive `when` expressions
- Provide `contentDescription` on all interactive and decorative icons
- Use `Modifier` chaining; accept `modifier` parameter in every public composable
- Preview every reusable component with `@Preview`

### Avoid

- Performing I/O, network calls, or analytics tracking directly in composable bodies
- Exposing `MutableStateFlow` or `MutableState` from ViewModels
- Using `!!` operator in production code
- Hardcoding colors, dimensions, or strings (use theme tokens and resources)
- Creating ViewModels manually (use `hiltViewModel()`)
- Passing complex objects through navigation arguments (pass IDs instead)
- Ignoring configuration changes (use `rememberSaveable` when needed)

## References

For detailed UI patterns, animation, testing strategies, performance, and accessibility guidance, see:

- [references/patterns.md](references/patterns.md) -- UI composition patterns, animation, performance, accessibility, testing recipes

## External References

- [Jetpack Compose Documentation](https://developer.android.com/jetpack/compose)
- [Compose API Guidelines](https://android.googlesource.com/platform/frameworks/support/+/refs/heads/androidx-main/compose/docs/compose-api-guidelines.md)
- [Material Design 3 for Compose](https://developer.android.com/jetpack/compose/designsystems/material3)
- [Navigation in Compose](https://developer.android.com/jetpack/compose/navigation)
- [Side-effects in Compose](https://developer.android.com/jetpack/compose/side-effects)
- [Compose Testing](https://developer.android.com/jetpack/compose/testing)
- [Hilt with Compose](https://developer.android.com/jetpack/compose/libraries#hilt)
- [Coil Image Loading](https://coil-kt.github.io/coil/compose/)
