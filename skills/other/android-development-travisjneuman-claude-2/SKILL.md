---
name: android-development
description: Android development with Kotlin, Jetpack Compose, and modern Android architecture. Use when building Android apps, implementing Material Design, or following Android best practices.
---

# Android Development

Comprehensive guide for building modern Android applications.

## Platforms Covered

| Platform       | Min SDK      | Target SDK  |
| -------------- | ------------ | ----------- |
| Android Phone  | API 24 (7.0) | API 34 (14) |
| Android Tablet | API 24       | API 34      |
| Android TV     | API 24       | API 34      |
| Wear OS        | API 30       | API 34      |
| Android Auto   | API 29       | API 34      |

---

## Jetpack Compose (Modern UI)

### Basic Structure

```kotlin
@Composable
fun MyApp() {
    MaterialTheme {
        Surface(
            modifier = Modifier.fillMaxSize(),
            color = MaterialTheme.colorScheme.background
        ) {
            MainScreen()
        }
    }
}

@Composable
fun MainScreen() {
    var count by remember { mutableStateOf(0) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Count: $count",
            style = MaterialTheme.typography.headlineLarge
        )

        Spacer(modifier = Modifier.height(16.dp))

        Button(onClick = { count++ }) {
            Text("Increment")
        }
    }
}
```

### State Management

```kotlin
// Local state
var text by remember { mutableStateOf("") }

// State hoisting
@Composable
fun StatefulCounter() {
    var count by remember { mutableStateOf(0) }
    StatelessCounter(count = count, onIncrement = { count++ })
}

@Composable
fun StatelessCounter(count: Int, onIncrement: () -> Unit) {
    Button(onClick = onIncrement) {
        Text("Count: $count")
    }
}

// ViewModel state
@HiltViewModel
class MainViewModel @Inject constructor(
    private val repository: ItemRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(UiState())
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    fun loadItems() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                val items = repository.getItems()
                _uiState.update { it.copy(items = items, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }
}

// Collecting in Compose
@Composable
fun MainScreen(viewModel: MainViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    when {
        uiState.isLoading -> LoadingIndicator()
        uiState.error != null -> ErrorMessage(uiState.error!!)
        else -> ItemList(uiState.items)
    }
}
```

### Navigation

```kotlin
// Navigation setup
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            HomeScreen(
                onNavigateToDetail = { id ->
                    navController.navigate("detail/$id")
                }
            )
        }
        composable(
            route = "detail/{itemId}",
            arguments = listOf(navArgument("itemId") { type = NavType.StringType })
        ) { backStackEntry ->
            val itemId = backStackEntry.arguments?.getString("itemId")
            DetailScreen(itemId = itemId)
        }
    }
}

// Type-safe navigation (recommended)
@Serializable
data class DetailRoute(val itemId: String)

navController.navigate(DetailRoute(itemId = "123"))
```

### Lists

```kotlin
@Composable
fun ItemList(items: List<Item>) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(
            items = items,
            key = { it.id }
        ) { item ->
            ItemCard(item = item)
        }
    }
}

// Pull to refresh
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RefreshableList(
    items: List<Item>,
    isRefreshing: Boolean,
    onRefresh: () -> Unit
) {
    val pullRefreshState = rememberPullToRefreshState()

    PullToRefreshBox(
        isRefreshing = isRefreshing,
        onRefresh = onRefresh,
        state = pullRefreshState
    ) {
        LazyColumn { /* content */ }
    }
}
```

---

## Modern Android Architecture

### Clean Architecture Layers

```
app/
├── data/
│   ├── local/
│   │   ├── AppDatabase.kt
│   │   └── ItemDao.kt
│   ├── remote/
│   │   ├── ApiService.kt
│   │   └── ItemDto.kt
│   └── repository/
│       └── ItemRepositoryImpl.kt
├── domain/
│   ├── model/
│   │   └── Item.kt
│   ├── repository/
│   │   └── ItemRepository.kt
│   └── usecase/
│       └── GetItemsUseCase.kt
├── presentation/
│   ├── home/
│   │   ├── HomeScreen.kt
│   │   └── HomeViewModel.kt
│   └── navigation/
│       └── AppNavigation.kt
└── di/
    └── AppModule.kt
```

### Dependency Injection (Hilt)

```kotlin
@HiltAndroidApp
class MyApplication : Application()

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

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
    @Singleton
    fun provideApiService(): ApiService {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideItemRepository(
        apiService: ApiService,
        database: AppDatabase
    ): ItemRepository {
        return ItemRepositoryImpl(apiService, database.itemDao())
    }
}
```

---

## Data Layer

### Room Database

```kotlin
@Entity(tableName = "items")
data class ItemEntity(
    @PrimaryKey val id: String,
    val name: String,
    val createdAt: Long
)

@Dao
interface ItemDao {
    @Query("SELECT * FROM items ORDER BY createdAt DESC")
    fun getItems(): Flow<List<ItemEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertItems(items: List<ItemEntity>)

    @Delete
    suspend fun deleteItem(item: ItemEntity)
}

@Database(entities = [ItemEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun itemDao(): ItemDao
}
```

### Retrofit API

```kotlin
interface ApiService {
    @GET("items")
    suspend fun getItems(): List<ItemDto>

    @POST("items")
    suspend fun createItem(@Body item: CreateItemRequest): ItemDto

    @DELETE("items/{id}")
    suspend fun deleteItem(@Path("id") id: String)
}

data class ItemDto(
    val id: String,
    val name: String,
    @SerializedName("created_at") val createdAt: String
)
```

### Repository Pattern

```kotlin
interface ItemRepository {
    fun getItems(): Flow<List<Item>>
    suspend fun refreshItems()
    suspend fun deleteItem(id: String)
}

class ItemRepositoryImpl @Inject constructor(
    private val apiService: ApiService,
    private val itemDao: ItemDao
) : ItemRepository {

    override fun getItems(): Flow<List<Item>> {
        return itemDao.getItems().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    override suspend fun refreshItems() {
        val items = apiService.getItems()
        itemDao.insertItems(items.map { it.toEntity() })
    }
}
```

---

## Material Design 3

### Theme Setup

```kotlin
@Composable
fun MyAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context)
            else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
```

### Common Components

```kotlin
// Top App Bar
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MyTopBar(
    title: String,
    onBackClick: () -> Unit
) {
    TopAppBar(
        title = { Text(title) },
        navigationIcon = {
            IconButton(onClick = onBackClick) {
                Icon(Icons.Default.ArrowBack, contentDescription = "Back")
            }
        },
        actions = {
            IconButton(onClick = { /* menu */ }) {
                Icon(Icons.Default.MoreVert, contentDescription = "Menu")
            }
        }
    )
}

// Bottom Navigation
@Composable
fun MyBottomBar(
    selectedTab: Int,
    onTabSelected: (Int) -> Unit
) {
    NavigationBar {
        NavigationBarItem(
            icon = { Icon(Icons.Default.Home, contentDescription = null) },
            label = { Text("Home") },
            selected = selectedTab == 0,
            onClick = { onTabSelected(0) }
        )
        NavigationBarItem(
            icon = { Icon(Icons.Default.Settings, contentDescription = null) },
            label = { Text("Settings") },
            selected = selectedTab == 1,
            onClick = { onTabSelected(1) }
        )
    }
}
```

---

## Platform-Specific

### Android TV

```kotlin
// Focus management
@Composable
fun TvButton(
    onClick: () -> Unit,
    content: @Composable () -> Unit
) {
    var isFocused by remember { mutableStateOf(false) }

    Box(
        modifier = Modifier
            .onFocusChanged { isFocused = it.isFocused }
            .focusable()
            .clickable(onClick = onClick)
            .background(
                if (isFocused) MaterialTheme.colorScheme.primary
                else MaterialTheme.colorScheme.surface
            )
    ) {
        content()
    }
}
```

### Wear OS

```kotlin
@Composable
fun WearApp() {
    MaterialTheme {
        ScalingLazyColumn(
            modifier = Modifier.fillMaxSize(),
            anchorType = ScalingLazyListAnchorType.ItemCenter
        ) {
            item { TimeText() }
            item {
                Chip(
                    onClick = { },
                    label = { Text("Action") }
                )
            }
        }
    }
}
```

---

## Testing

### Unit Tests

```kotlin
@Test
fun `getItems returns mapped domain objects`() = runTest {
    val repository = ItemRepositoryImpl(
        apiService = FakeApiService(),
        itemDao = FakeItemDao()
    )

    val items = repository.getItems().first()

    assertEquals(2, items.size)
    assertEquals("Item 1", items[0].name)
}
```

### Compose UI Tests

```kotlin
@HiltAndroidTest
class MainScreenTest {
    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun displayItems_whenLoaded() {
        composeTestRule.onNodeWithText("Item 1").assertIsDisplayed()
        composeTestRule.onNodeWithText("Item 2").assertIsDisplayed()
    }

    @Test
    fun navigateToDetail_onItemClick() {
        composeTestRule.onNodeWithText("Item 1").performClick()
        composeTestRule.onNodeWithText("Item Details").assertIsDisplayed()
    }
}
```

---

## Play Store Requirements

### Required

- Privacy policy
- App icon (512x512)
- Feature graphic (1024x500)
- Screenshots (min 2)
- Target API 34+

### App Bundle

```groovy
android {
    bundle {
        language {
            enableSplit = true
        }
        density {
            enableSplit = true
        }
        abi {
            enableSplit = true
        }
    }
}
```

---

## Best Practices

### DO:

- Use Kotlin Coroutines and Flow
- Follow unidirectional data flow
- Use Jetpack Compose for new UI
- Implement proper lifecycle handling
- Support multiple screen sizes

### DON'T:

- Block main thread
- Leak contexts
- Hardcode dimensions
- Ignore process death
- Skip ProGuard rules

---

## Kotlin Multiplatform (KMP) / Compose Multiplatform (CMP)

### Shared Business Logic with KMP

```kotlin
// shared/src/commonMain/kotlin/UserRepository.kt
expect class PlatformContext

class UserRepository(private val api: ApiService, private val db: Database) {
    suspend fun getUsers(): List<User> {
        return try {
            val remote = api.fetchUsers()
            db.saveUsers(remote)
            remote
        } catch (e: Exception) {
            db.getCachedUsers()
        }
    }
}

// shared/src/androidMain/kotlin/PlatformContext.kt
actual class PlatformContext(val context: Context)

// shared/src/iosMain/kotlin/PlatformContext.kt
actual class PlatformContext
```

### Compose Multiplatform (Shared UI)

```kotlin
// shared/src/commonMain/kotlin/App.kt
@Composable
fun App() {
    MaterialTheme {
        var users by remember { mutableStateOf<List<User>>(emptyList()) }
        val repository = remember { UserRepository() }

        LaunchedEffect(Unit) {
            users = repository.getUsers()
        }

        LazyColumn {
            items(users) { user ->
                UserCard(user)
            }
        }
    }
}

// Runs natively on Android, iOS, Desktop, and Web
```

### KMP Project Structure

```
project/
├── shared/
│   └── src/
│       ├── commonMain/     # Shared Kotlin code
│       ├── androidMain/    # Android-specific
│       ├── iosMain/        # iOS-specific
│       └── desktopMain/    # Desktop-specific
├── androidApp/             # Android entry point
├── iosApp/                 # iOS entry point (Swift/SwiftUI)
└── desktopApp/             # Desktop entry point
```

---

## Navigation 3 (Type-Safe Navigation)

```kotlin
// Define routes as serializable data classes
@Serializable
data object Home

@Serializable
data class Detail(val itemId: String)

@Serializable
data class Settings(val section: String? = null)

// Navigation setup
@Composable
fun AppNavHost(navController: NavHostController = rememberNavController()) {
    NavHost(navController = navController, startDestination = Home) {
        composable<Home> {
            HomeScreen(onItemClick = { id ->
                navController.navigate(Detail(itemId = id))
            })
        }
        composable<Detail> { backStackEntry ->
            val detail: Detail = backStackEntry.toRoute()
            DetailScreen(itemId = detail.itemId)
        }
        composable<Settings> { backStackEntry ->
            val settings: Settings = backStackEntry.toRoute()
            SettingsScreen(section = settings.section)
        }
    }
}
```

---

## API 35 (Android 15) Features

| Feature                    | Description                                           |
| -------------------------- | ----------------------------------------------------- |
| **Edge-to-edge enforced**  | Apps must handle insets properly                       |
| **Predictive back**        | System back gesture with preview animations           |
| **Private Space**          | User-controlled hidden app profile                    |
| **Satellite connectivity** | SMS/MMS over satellite                                |
| **App archival**           | Auto-archive unused apps, preserve data               |
| **Health Connect**         | Updated health data APIs                              |

```kotlin
// Edge-to-edge (required on API 35+)
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    enableEdgeToEdge()

    setContent {
        Scaffold(
            modifier = Modifier.fillMaxSize(),
            contentWindowInsets = ScaffoldDefaults.contentWindowInsets,
        ) { innerPadding ->
            MainContent(modifier = Modifier.padding(innerPadding))
        }
    }
}

// Predictive back with Compose
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DetailScreen(onBack: () -> Unit) {
    BackHandler(onBack = onBack)
    // Content renders with predictive back animation automatically
}
```

---

## Baseline Profiles for Startup Performance

```kotlin
// baselineprofile/build.gradle.kts
dependencies {
    implementation("androidx.benchmark:benchmark-macro-junit4:1.3.0")
}

// BaselineProfileGenerator.kt
@RunWith(AndroidJUnit4::class)
class BaselineProfileGenerator {
    @get:Rule
    val rule = BaselineProfileRule()

    @Test
    fun generateBaselineProfile() {
        rule.collect(packageName = "com.example.app") {
            // Critical user journey
            pressHome()
            startActivityAndWait()
            device.findObject(By.text("Login")).click()
            device.wait(Until.hasObject(By.text("Dashboard")), 5000)
        }
    }
}
```

```groovy
// app/build.gradle.kts
android {
    buildTypes {
        release {
            // Baseline profiles improve startup by 15-30%
            baselineProfile.automaticGenerationDuringBuild = true
        }
    }
}
```

---

## Credential Manager API

```kotlin
// Modern sign-in replacing legacy APIs
val credentialManager = CredentialManager.create(context)

// Sign in with passkeys, passwords, or federated identity
suspend fun signIn() {
    val request = GetCredentialRequest(listOf(
        GetPasswordOption(),
        GetPublicKeyCredentialOption(requestJson = passkeyRequestJson),
        GetGoogleIdOption(serverClientId = WEB_CLIENT_ID),
    ))

    try {
        val result = credentialManager.getCredential(context, request)
        handleSignIn(result)
    } catch (e: GetCredentialException) {
        handleSignInError(e)
    }
}

// Create a passkey
suspend fun createPasskey() {
    val request = CreatePublicKeyCredentialRequest(
        requestJson = createPasskeyRequestJson
    )
    val result = credentialManager.createCredential(context, request)
    handlePasskeyCreation(result)
}
```
