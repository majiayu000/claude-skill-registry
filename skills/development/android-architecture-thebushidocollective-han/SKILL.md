---
name: android-architecture
description: Use when implementing MVVM, clean architecture, dependency injection with Hilt, or structuring Android app layers.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Android - Architecture

Modern Android architecture patterns following Google's recommended practices.

## Key Concepts

### MVVM Architecture

Model-View-ViewModel separates UI from business logic:

```kotlin
// UI State
data class UserUiState(
    val user: User? = null,
    val isLoading: Boolean = false,
    val error: String? = null
)

// ViewModel
class UserViewModel(
    private val userRepository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(UserUiState())
    val uiState: StateFlow<UserUiState> = _uiState.asStateFlow()

    fun loadUser(userId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }

            userRepository.getUser(userId)
                .onSuccess { user ->
                    _uiState.update { it.copy(user = user, isLoading = false) }
                }
                .onFailure { error ->
                    _uiState.update { it.copy(error = error.message, isLoading = false) }
                }
        }
    }
}

// Composable
@Composable
fun UserScreen(viewModel: UserViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    when {
        uiState.isLoading -> LoadingIndicator()
        uiState.error != null -> ErrorMessage(uiState.error!!)
        uiState.user != null -> UserContent(uiState.user!!)
    }
}
```

### Clean Architecture Layers

```
app/
├── data/
│   ├── local/           # Room database, DataStore
│   │   ├── dao/
│   │   └── entities/
│   ├── remote/          # Retrofit, network
│   │   ├── api/
│   │   └── dto/
│   └── repository/      # Repository implementations
├── domain/
│   ├── model/           # Domain models
│   ├── repository/      # Repository interfaces
│   └── usecase/         # Business logic
└── presentation/
    ├── ui/              # Composables
    └── viewmodel/       # ViewModels
```

### Repository Pattern

```kotlin
// Domain layer - interface
interface UserRepository {
    fun getUser(id: String): Flow<User>
    suspend fun saveUser(user: User): Result<Unit>
    suspend fun deleteUser(id: String): Result<Unit>
}

// Data layer - implementation
class UserRepositoryImpl(
    private val userApi: UserApi,
    private val userDao: UserDao
) : UserRepository {

    override fun getUser(id: String): Flow<User> = flow {
        // Emit cached data first
        userDao.getUser(id)?.let { emit(it.toDomain()) }

        // Fetch fresh data
        try {
            val remoteUser = userApi.getUser(id)
            userDao.insertUser(remoteUser.toEntity())
            emit(remoteUser.toDomain())
        } catch (e: Exception) {
            // Network error, cached data already emitted
        }
    }

    override suspend fun saveUser(user: User): Result<Unit> = runCatching {
        userApi.updateUser(user.toDto())
        userDao.insertUser(user.toEntity())
    }
}
```

## Best Practices

### Dependency Injection with Hilt

```kotlin
// Module definition
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .addConverterFactory(MoshiConverterFactory.create())
            .build()
    }

    @Provides
    @Singleton
    fun provideUserApi(retrofit: Retrofit): UserApi {
        return retrofit.create(UserApi::class.java)
    }
}

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindUserRepository(impl: UserRepositoryImpl): UserRepository
}

// ViewModel injection
@HiltViewModel
class UserViewModel @Inject constructor(
    private val getUserUseCase: GetUserUseCase,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val userId: String = savedStateHandle.get<String>("userId")
        ?: throw IllegalArgumentException("userId required")

    // ViewModel implementation
}
```

### Use Cases for Business Logic

```kotlin
class GetUserUseCase @Inject constructor(
    private val userRepository: UserRepository,
    private val analyticsTracker: AnalyticsTracker
) {
    operator fun invoke(userId: String): Flow<Result<User>> = flow {
        emit(Result.Loading)

        userRepository.getUser(userId)
            .catch { e ->
                analyticsTracker.trackError("get_user_failed", e)
                emit(Result.Error(e))
            }
            .collect { user ->
                emit(Result.Success(user))
            }
    }
}

// Sealed class for results
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Throwable) : Result<Nothing>()
    object Loading : Result<Nothing>()
}
```

### Room Database Setup

```kotlin
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: String,
    val name: String,
    val email: String,
    @ColumnInfo(name = "created_at") val createdAt: Long
)

@Dao
interface UserDao {
    @Query("SELECT * FROM users WHERE id = :id")
    suspend fun getUser(id: String): UserEntity?

    @Query("SELECT * FROM users ORDER BY name ASC")
    fun getAllUsers(): Flow<List<UserEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: UserEntity)

    @Delete
    suspend fun deleteUser(user: UserEntity)
}

@Database(entities = [UserEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}

// Hilt module
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app_database"
        ).build()
    }

    @Provides
    fun provideUserDao(database: AppDatabase): UserDao {
        return database.userDao()
    }
}
```

### Data Mapping

```kotlin
// DTO (Data Transfer Object) - from API
data class UserDto(
    @Json(name = "id") val id: String,
    @Json(name = "full_name") val fullName: String,
    @Json(name = "email_address") val email: String
)

// Entity - for Room
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: String,
    val name: String,
    val email: String
)

// Domain model
data class User(
    val id: String,
    val name: String,
    val email: String
)

// Mappers
fun UserDto.toEntity() = UserEntity(
    id = id,
    name = fullName,
    email = email
)

fun UserDto.toDomain() = User(
    id = id,
    name = fullName,
    email = email
)

fun UserEntity.toDomain() = User(
    id = id,
    name = name,
    email = email
)

fun User.toEntity() = UserEntity(
    id = id,
    name = name,
    email = email
)
```

## Common Patterns

### Single Source of Truth

```kotlin
class OfflineFirstRepository @Inject constructor(
    private val api: ItemApi,
    private val dao: ItemDao
) : ItemRepository {

    override fun getItems(): Flow<List<Item>> {
        return dao.getAllItems()
            .map { entities -> entities.map { it.toDomain() } }
            .onStart {
                // Refresh from network in background
                refreshItems()
            }
    }

    private suspend fun refreshItems() {
        try {
            val remoteItems = api.getItems()
            dao.deleteAll()
            dao.insertAll(remoteItems.map { it.toEntity() })
        } catch (e: Exception) {
            // Log error, local data still available
        }
    }
}
```

### Navigation with Type-Safe Args

```kotlin
// Define routes
sealed class Screen(val route: String) {
    object Home : Screen("home")
    object Detail : Screen("detail/{itemId}") {
        fun createRoute(itemId: String) = "detail/$itemId"
    }
    object Settings : Screen("settings")
}

// Navigation setup
@Composable
fun AppNavigation(navController: NavHostController) {
    NavHost(navController = navController, startDestination = Screen.Home.route) {
        composable(Screen.Home.route) {
            HomeScreen(
                onItemClick = { itemId ->
                    navController.navigate(Screen.Detail.createRoute(itemId))
                }
            )
        }
        composable(
            route = Screen.Detail.route,
            arguments = listOf(navArgument("itemId") { type = NavType.StringType })
        ) { backStackEntry ->
            DetailScreen(
                itemId = backStackEntry.arguments?.getString("itemId") ?: return@composable
            )
        }
    }
}
```

### Error Handling

```kotlin
sealed class UiState<out T> {
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String, val retry: (() -> Unit)? = null) : UiState<Nothing>()
}

@Composable
fun <T> StateHandler(
    state: UiState<T>,
    onRetry: () -> Unit = {},
    content: @Composable (T) -> Unit
) {
    when (state) {
        is UiState.Loading -> {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        }
        is UiState.Error -> {
            Column(
                modifier = Modifier.fillMaxSize(),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Text(state.message)
                Spacer(modifier = Modifier.height(16.dp))
                Button(onClick = onRetry) {
                    Text("Retry")
                }
            }
        }
        is UiState.Success -> content(state.data)
    }
}
```

## Anti-Patterns

### God Activity/Fragment

Bad: All logic in one Activity.

Good: Use MVVM with clear separation of concerns.

### Network Calls in ViewModel

Bad:

```kotlin
class BadViewModel : ViewModel() {
    fun loadData() {
        val client = OkHttpClient()  // Direct network dependency
        // ...
    }
}
```

Good: Inject repository through constructor.

### Exposing Mutable State

Bad:

```kotlin
class BadViewModel : ViewModel() {
    val uiState = MutableStateFlow(UiState())  // Mutable exposed!
}
```

Good:

```kotlin
class GoodViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(UiState())
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()
}
```

## Related Skills

- **android-jetpack-compose**: UI layer patterns
- **android-kotlin-coroutines**: Async operations
