---
name: kotlin-expert
version: 1.0.0
description: Expert-level Kotlin development, Android, coroutines, and multiplatform
category: languages
tags: [kotlin, android, coroutines, multiplatform, jvm]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(kotlin:*, gradle:*)
---

# Kotlin Expert

Expert guidance for Kotlin development, Android, coroutines, Kotlin Multiplatform, and modern JVM development.

## Core Concepts

### Kotlin Fundamentals
- Null safety
- Extension functions
- Data classes
- Sealed classes
- Coroutines and Flow
- Higher-order functions

### Android Development
- Jetpack Compose
- ViewModel and LiveData
- Room database
- Retrofit networking
- Dependency injection (Hilt)
- Android lifecycle

### Kotlin Multiplatform
- Shared business logic
- Platform-specific implementations
- iOS and Android targets
- Common module architecture

## Modern Kotlin Syntax

```kotlin
// Data classes
data class User(
    val id: String,
    val name: String,
    val email: String,
    val createdAt: LocalDateTime = LocalDateTime.now()
)

// Sealed classes for type-safe states
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Exception) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

// Extension functions
fun String.isValidEmail(): Boolean {
    return this.contains("@") && this.contains(".")
}

// Scope functions
fun processUser(user: User) {
    user.run {
        println("Processing user: $name")
        // 'this' refers to user
    }

    user.let { u ->
        // 'it' or custom name refers to user
        println(u.email)
    }

    user.apply {
        // Modify properties
        // Returns the object
    }
}

// Null safety
fun findUser(id: String): User? {
    return database.find(id)
}

val user = findUser("123")
val name = user?.name ?: "Unknown" // Elvis operator
user?.let { println(it.name) } // Safe call with let

// When expression
fun getUserStatus(user: User): String = when {
    user.isActive && user.isPremium -> "Premium Active"
    user.isActive -> "Active"
    else -> "Inactive"
}
```

## Coroutines and Flow

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

class UserRepository {
    private val api: UserApi

    // Suspend function
    suspend fun fetchUser(id: String): User {
        return withContext(Dispatchers.IO) {
            api.getUser(id)
        }
    }

    // Flow for reactive streams
    fun observeUsers(): Flow<List<User>> = flow {
        while (true) {
            val users = fetchUsers()
            emit(users)
            delay(5000) // Refresh every 5 seconds
        }
    }.flowOn(Dispatchers.IO)

    // StateFlow for state management
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users.asStateFlow()

    suspend fun refreshUsers() {
        _users.value = fetchUsers()
    }
}

// Coroutine scopes
class UserViewModel : ViewModel() {
    private val repository = UserRepository()

    fun loadUsers() {
        viewModelScope.launch {
            try {
                val users = repository.fetchUser("123")
                // Update UI
            } catch (e: Exception) {
                // Handle error
            }
        }
    }

    // Parallel execution
    suspend fun loadMultipleUsers(ids: List<String>): List<User> {
        return coroutineScope {
            ids.map { id ->
                async { repository.fetchUser(id) }
            }.awaitAll()
        }
    }

    // Flow transformation
    fun searchUsers(query: String): Flow<List<User>> {
        return repository.observeUsers()
            .map { users -> users.filter { it.name.contains(query, ignoreCase = true) } }
            .distinctUntilChanged()
            .debounce(300)
    }
}
```

## Android Jetpack Compose

```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier

@Composable
fun UserListScreen(viewModel: UserViewModel = viewModel()) {
    val users by viewModel.users.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    Scaffold(
        topBar = { TopAppBar(title = { Text("Users") }) }
    ) { padding ->
        if (isLoading) {
            CircularProgressIndicator(
                modifier = Modifier.fillMaxSize()
            )
        } else {
            LazyColumn(
                modifier = Modifier.padding(padding)
            ) {
                items(users) { user ->
                    UserCard(user = user)
                }
            }
        }
    }
}

@Composable
fun UserCard(user: User) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = user.name,
                style = MaterialTheme.typography.headlineSmall
            )
            Text(
                text = user.email,
                style = MaterialTheme.typography.bodyMedium
            )
        }
    }
}
```

## Room Database

```kotlin
import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "name") val name: String,
    @ColumnInfo(name = "email") val email: String,
    @ColumnInfo(name = "created_at") val createdAt: Long
)

@Dao
interface UserDao {
    @Query("SELECT * FROM users")
    fun getAllUsers(): Flow<List<UserEntity>>

    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUserById(userId: String): UserEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: UserEntity)

    @Update
    suspend fun updateUser(user: UserEntity)

    @Delete
    suspend fun deleteUser(user: UserEntity)

    @Query("DELETE FROM users WHERE id = :userId")
    suspend fun deleteUserById(userId: String)
}

@Database(entities = [UserEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}
```

## Dependency Injection with Hilt

```kotlin
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    @Provides
    @Singleton
    fun provideUserApi(retrofit: Retrofit): UserApi {
        return retrofit.create(UserApi::class.java)
    }
}

@HiltAndroidApp
class MyApplication : Application()

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    @Inject lateinit var repository: UserRepository
}
```

## Kotlin Multiplatform

```kotlin
// commonMain
expect class Platform() {
    val name: String
}

expect fun platformSpecificFunction(): String

// androidMain
actual class Platform actual constructor() {
    actual val name: String = "Android ${android.os.Build.VERSION.SDK_INT}"
}

actual fun platformSpecificFunction(): String = "Android implementation"

// iosMain
actual class Platform actual constructor() {
    actual val name: String = UIDevice.currentDevice.systemName()
}

actual fun platformSpecificFunction(): String = "iOS implementation"

// Shared business logic
class UserService {
    suspend fun fetchUser(id: String): User {
        // Shared logic works on all platforms
        return api.getUser(id)
    }
}
```

## Best Practices

### Kotlin Style
- Use val over var when possible
- Leverage null safety features
- Use data classes for DTOs
- Prefer extension functions
- Use sealed classes for type-safe states
- Follow naming conventions

### Coroutines
- Use appropriate dispatchers (IO, Main, Default)
- Handle cancellation properly
- Avoid GlobalScope
- Use structured concurrency
- Prefer Flow over LiveData
- Use StateFlow for state

### Android
- Follow MVVM architecture
- Use Jetpack Compose for UI
- Implement proper lifecycle handling
- Use dependency injection
- Handle configuration changes
- Implement proper error handling

## Anti-Patterns

❌ Using !! (non-null assertion)
❌ GlobalScope.launch
❌ Blocking main thread
❌ Not handling coroutine cancellation
❌ Tight coupling
❌ God classes
❌ Ignoring memory leaks

## Resources

- Kotlin Docs: https://kotlinlang.org/docs/
- Android Developers: https://developer.android.com/kotlin
- Kotlin Coroutines: https://kotlinlang.org/docs/coroutines-overview.html
- Jetpack Compose: https://developer.android.com/jetpack/compose
