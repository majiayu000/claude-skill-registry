---
name: kotlin-patterns
description: Coroutine patterns, Flow operators, Jetpack Compose state management, Ktor routing, and Kotlin Multiplatform shared code.
---

# Kotlin Patterns

Modern Kotlin patterns for Android, server-side, and multiplatform development.

## Coroutine Patterns

```kotlin
import kotlinx.coroutines.*

// Structured concurrency: child failures cancel siblings
suspend fun loadDashboard(): Dashboard = coroutineScope {
    val profile = async { api.fetchProfile() }
    val orders = async { api.fetchRecentOrders() }
    val stats = async { api.fetchStats() }

    // All run concurrently; if one fails, others are cancelled
    Dashboard(
        profile = profile.await(),
        orders = orders.await(),
        stats = stats.await()
    )
}

// SupervisorScope: child failures don't cancel siblings
suspend fun loadOptionalData(): HomeScreen = supervisorScope {
    val required = async { api.fetchRequiredData() }
    val optional = async {
        try { api.fetchRecommendations() }
        catch (e: Exception) { emptyList() }  // Graceful fallback
    }

    HomeScreen(
        data = required.await(),
        recommendations = optional.await()
    )
}

// Retry with exponential backoff
suspend fun <T> retryWithBackoff(
    maxRetries: Int = 3,
    initialDelayMs: Long = 1000,
    factor: Double = 2.0,
    block: suspend () -> T
): T {
    var currentDelay = initialDelayMs
    repeat(maxRetries - 1) { attempt ->
        try {
            return block()
        } catch (e: Exception) {
            if (e is CancellationException) throw e  // Never swallow cancellation
            delay(currentDelay)
            currentDelay = (currentDelay * factor).toLong()
        }
    }
    return block()  // Last attempt, let exception propagate
}
```

## Flow Operators

```kotlin
import kotlinx.coroutines.flow.*

// Repository pattern with Flow
class OrderRepository(private val api: OrderApi, private val db: OrderDao) {

    // Offline-first: emit cached, then fetch fresh
    fun getOrders(): Flow<List<Order>> = flow {
        // Emit cached data first
        emit(db.getAllOrders())

        // Fetch fresh data
        val fresh = api.fetchOrders()
        db.insertAll(fresh)
        emit(fresh)
    }.catch { e ->
        // On network error, emit cached data
        emit(db.getAllOrders())
    }

    // Debounce search input
    fun search(queryFlow: Flow<String>): Flow<List<Order>> =
        queryFlow
            .debounce(300)
            .distinctUntilChanged()
            .filter { it.length >= 2 }
            .flatMapLatest { query ->
                flow { emit(api.search(query)) }
                    .catch { emit(emptyList()) }
            }

    // Combine multiple flows
    fun getDashboard(): Flow<DashboardState> =
        combine(
            getOrders(),
            getStats(),
            getNotifications()
        ) { orders, stats, notifications ->
            DashboardState(orders, stats, notifications)
        }
}

// StateFlow for UI state (hot flow, always has value)
class OrderViewModel(private val repo: OrderRepository) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            repo.getOrders()
                .map { orders -> UiState.Success(orders) as UiState }
                .catch { emit(UiState.Error(it.message ?: "Unknown error")) }
                .collect { _uiState.value = it }
        }
    }

    sealed interface UiState {
        data object Loading : UiState
        data class Success(val orders: List<Order>) : UiState
        data class Error(val message: String) : UiState
    }
}
```

## Jetpack Compose State

```kotlin
@Composable
fun OrderListScreen(viewModel: OrderViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    when (val state = uiState) {
        is UiState.Loading -> LoadingIndicator()
        is UiState.Error -> ErrorMessage(state.message) { viewModel.retry() }
        is UiState.Success -> OrderList(
            orders = state.orders,
            onOrderClick = { viewModel.selectOrder(it) },
            onDelete = { viewModel.deleteOrder(it) }
        )
    }
}

// Stateless composable with hoisted state
@Composable
fun OrderList(
    orders: List<Order>,
    onOrderClick: (Order) -> Unit,
    onDelete: (Order) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(modifier = modifier) {
        items(orders, key = { it.id }) { order ->
            OrderItem(
                order = order,
                onClick = { onOrderClick(order) },
                onDelete = { onDelete(order) },
                modifier = Modifier.animateItem()
            )
        }
    }
}

// Remember expensive computation
@Composable
fun FilteredOrders(orders: List<Order>, filter: String) {
    val filtered = remember(orders, filter) {
        orders.filter { it.status.name.contains(filter, ignoreCase = true) }
    }
    OrderList(orders = filtered, onOrderClick = {}, onDelete = {})
}
```

## Ktor Server Routing

```kotlin
import io.ktor.server.application.*
import io.ktor.server.routing.*
import io.ktor.server.response.*
import io.ktor.server.request.*
import io.ktor.http.*

fun Application.configureRouting() {
    routing {
        route("/api/v1") {
            // Middleware: auth check for all routes under /api/v1
            install(AuthPlugin)

            route("/orders") {
                get {
                    val page = call.parameters["page"]?.toIntOrNull() ?: 1
                    val limit = call.parameters["limit"]?.toIntOrNull()?.coerceIn(1, 100) ?: 20
                    val orders = orderService.findAll(page, limit)
                    call.respond(ApiResponse.success(orders))
                }

                get("/{id}") {
                    val id = call.parameters["id"]
                        ?: return@get call.respond(HttpStatusCode.BadRequest, "Missing ID")
                    val order = orderService.findById(id)
                        ?: return@get call.respond(HttpStatusCode.NotFound)
                    call.respond(ApiResponse.success(order))
                }

                post {
                    val input = call.receive<CreateOrderInput>()
                    val validated = input.validate()
                        ?: return@post call.respond(HttpStatusCode.BadRequest, "Invalid input")
                    val order = orderService.create(validated)
                    call.respond(HttpStatusCode.Created, ApiResponse.success(order))
                }
            }
        }
    }
}

// Typed API response wrapper
@Serializable
data class ApiResponse<T>(
    val success: Boolean,
    val data: T? = null,
    val error: String? = null
) {
    companion object {
        fun <T> success(data: T) = ApiResponse(success = true, data = data)
        fun error(message: String) = ApiResponse<Nothing>(success = false, error = message)
    }
}
```

## Kotlin Multiplatform Shared Code

```kotlin
// shared/src/commonMain/kotlin
expect class PlatformContext

// Repository shared between Android/iOS
class SharedOrderRepository(
    private val httpClient: HttpClient,
    private val database: SharedDatabase
) {
    suspend fun getOrders(): List<Order> {
        return try {
            val remote = httpClient.get("https://api.example.com/orders").body<List<Order>>()
            database.orderDao().insertAll(remote)
            remote
        } catch (e: Exception) {
            database.orderDao().getAll()  // Offline fallback
        }
    }
}

// shared/src/androidMain/kotlin
actual class PlatformContext(val context: android.content.Context)

// shared/src/iosMain/kotlin
actual class PlatformContext
```

## Checklist

- [ ] Structured concurrency: always use coroutineScope or supervisorScope
- [ ] Never swallow CancellationException (rethrow it)
- [ ] StateFlow for UI state, SharedFlow for one-time events
- [ ] State hoisting in Compose: stateless composables preferred
- [ ] Use `key` parameter in LazyColumn items for stable identity
- [ ] collectAsStateWithLifecycle over collectAsState (lifecycle-aware)
- [ ] Validate and coerce API input parameters (page, limit bounds)
- [ ] Remember expensive computations in Compose with proper keys

## Anti-Patterns

- GlobalScope.launch: leaks coroutines, no structured cancellation
- Mutable state in Compose without State/MutableState wrapper
- Flow.collect in init block without lifecycle awareness (memory leak)
- Blocking calls (Thread.sleep) inside coroutines (use delay)
- Catching Exception without re-throwing CancellationException
- Business logic in Composable functions (keep in ViewModel/UseCase)
