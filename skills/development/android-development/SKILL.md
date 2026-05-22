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
