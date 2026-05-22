---
name: android-unit-test
description: Эксперт Android тестирования. Используй для JUnit, Espresso и Android test patterns.
---

# Android Unit Testing Expert

Эксперт по тестированию Android приложений с использованием JUnit 5, Mockito и Kotlin.

## Настройка зависимостей

```groovy
// build.gradle (app)
dependencies {
    // Unit testing
    testImplementation 'junit:junit:4.13.2'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.9.3'
    testImplementation 'org.mockito:mockito-core:5.3.1'
    testImplementation 'org.mockito.kotlin:mockito-kotlin:5.0.0'
    testImplementation 'io.mockk:mockk:1.13.5'
    testImplementation 'org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.1'
    testImplementation 'app.cash.turbine:turbine:1.0.0'

    // Instrumentation testing
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
    androidTestImplementation 'androidx.test:runner:1.5.2'
    androidTestImplementation 'androidx.test:rules:1.5.0'
}
```

## AAA Pattern (Arrange, Act, Assert)

```kotlin
class UserRepositoryTest {

    @Test
    fun `getUser returns user when found`() {
        // Arrange
        val userId = "user_123"
        val expectedUser = User(userId, "John Doe", "john@example.com")
        val mockDataSource = mock<UserDataSource> {
            on { getUser(userId) } doReturn expectedUser
        }
        val repository = UserRepository(mockDataSource)

        // Act
        val result = repository.getUser(userId)

        // Assert
        assertEquals(expectedUser, result)
        verify(mockDataSource).getUser(userId)
    }
}
```

## ViewModel Testing

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class UserViewModelTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private lateinit var viewModel: UserViewModel
    private lateinit var repository: UserRepository

    @Before
    fun setup() {
        repository = mock()
        viewModel = UserViewModel(repository)
    }

    @Test
    fun `loadUser updates state to success when repository returns user`() = runTest {
        // Arrange
        val user = User("1", "John", "john@example.com")
        whenever(repository.getUser("1")).thenReturn(Result.success(user))

        // Act
        viewModel.loadUser("1")

        // Assert
        val state = viewModel.uiState.value
        assertTrue(state is UserUiState.Success)
        assertEquals(user, (state as UserUiState.Success).user)
    }

    @Test
    fun `loadUser updates state to error when repository fails`() = runTest {
        // Arrange
        val exception = IOException("Network error")
        whenever(repository.getUser("1")).thenReturn(Result.failure(exception))

        // Act
        viewModel.loadUser("1")

        // Assert
        val state = viewModel.uiState.value
        assertTrue(state is UserUiState.Error)
        assertEquals("Network error", (state as UserUiState.Error).message)
    }
}
```

## MainDispatcherRule

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class MainDispatcherRule(
    private val testDispatcher: TestDispatcher = UnconfinedTestDispatcher()
) : TestWatcher() {

    override fun starting(description: Description) {
        Dispatchers.setMain(testDispatcher)
    }

    override fun finished(description: Description) {
        Dispatchers.resetMain()
    }
}
```

## Repository Testing

```kotlin
class UserRepositoryTest {

    private lateinit var repository: UserRepository
    private lateinit var remoteDataSource: UserRemoteDataSource
    private lateinit var localDataSource: UserLocalDataSource

    @Before
    fun setup() {
        remoteDataSource = mock()
        localDataSource = mock()
        repository = UserRepository(remoteDataSource, localDataSource)
    }

    @Test
    fun `getUsers returns cached data when available`() = runTest {
        // Arrange
        val cachedUsers = listOf(User("1", "John", "john@example.com"))
        whenever(localDataSource.getUsers()).thenReturn(cachedUsers)

        // Act
        val result = repository.getUsers()

        // Assert
        assertEquals(cachedUsers, result)
        verify(localDataSource).getUsers()
        verifyNoInteractions(remoteDataSource)
    }

    @Test
    fun `getUsers fetches from remote when cache is empty`() = runTest {
        // Arrange
        val remoteUsers = listOf(User("1", "John", "john@example.com"))
        whenever(localDataSource.getUsers()).thenReturn(emptyList())
        whenever(remoteDataSource.getUsers()).thenReturn(remoteUsers)

        // Act
        val result = repository.getUsers()

        // Assert
        assertEquals(remoteUsers, result)
        verify(localDataSource).saveUsers(remoteUsers)
    }
}
```

## Flow Testing с Turbine

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class FlowTestExample {

    @Test
    fun `userFlow emits expected values`() = runTest {
        val repository = UserRepository()

        repository.userFlow.test {
            // Initial state
            assertEquals(UserState.Loading, awaitItem())

            // After loading
            assertEquals(UserState.Success(user), awaitItem())

            // Cancel and ensure no more emissions
            cancelAndIgnoreRemainingEvents()
        }
    }

    @Test
    fun `searchFlow debounces and emits results`() = runTest {
        val viewModel = SearchViewModel()

        viewModel.searchResults.test {
            viewModel.onSearchQueryChanged("test")
            advanceTimeBy(300) // Debounce time

            val result = awaitItem()
            assertTrue(result.isNotEmpty())

            cancelAndIgnoreRemainingEvents()
        }
    }
}
```

## Параметризованные тесты

```kotlin
class CalculatorTest {

    @ParameterizedTest
    @CsvSource(
        "1, 1, 2",
        "2, 3, 5",
        "10, -5, 5",
        "0, 0, 0"
    )
    fun `add returns correct sum`(a: Int, b: Int, expected: Int) {
        val calculator = Calculator()
        assertEquals(expected, calculator.add(a, b))
    }

    @ParameterizedTest
    @MethodSource("divisionTestData")
    fun `divide handles edge cases`(a: Int, b: Int, expected: Result<Int>) {
        val calculator = Calculator()
        assertEquals(expected, calculator.divide(a, b))
    }

    companion object {
        @JvmStatic
        fun divisionTestData() = listOf(
            Arguments.of(10, 2, Result.success(5)),
            Arguments.of(9, 3, Result.success(3)),
            Arguments.of(5, 0, Result.failure<Int>(ArithmeticException()))
        )
    }
}
```

## MockK для Kotlin

```kotlin
class UserServiceTest {

    @MockK
    private lateinit var api: UserApi

    @MockK
    private lateinit var cache: UserCache

    private lateinit var service: UserService

    @Before
    fun setup() {
        MockKAnnotations.init(this)
        service = UserService(api, cache)
    }

    @Test
    fun `getUser uses coEvery for suspend functions`() = runTest {
        // Arrange
        val user = User("1", "John", "john@example.com")
        coEvery { api.getUser("1") } returns user
        coEvery { cache.save(any()) } just Runs

        // Act
        val result = service.getUser("1")

        // Assert
        assertEquals(user, result)
        coVerify { cache.save(user) }
    }

    @Test
    fun `verify call order`() = runTest {
        val user = User("1", "John", "john@example.com")
        coEvery { api.getUser("1") } returns user
        coEvery { cache.save(any()) } just Runs

        service.getUser("1")

        coVerifyOrder {
            api.getUser("1")
            cache.save(user)
        }
    }
}
```

## Test Data Factories

```kotlin
object UserFactory {
    fun create(
        id: String = "user_${UUID.randomUUID()}",
        name: String = "Test User",
        email: String = "test@example.com",
        isActive: Boolean = true
    ) = User(id, name, email, isActive)

    fun createList(count: Int = 5) = (1..count).map {
        create(id = "user_$it", name = "User $it")
    }
}

// Usage in tests
@Test
fun `test with factory`() {
    val user = UserFactory.create(name = "Custom Name")
    val users = UserFactory.createList(10)
}
```

## Custom Assertions

```kotlin
fun <T> Result<T>.shouldBeSuccess(): T {
    assertTrue(this.isSuccess, "Expected success but was failure: ${this.exceptionOrNull()}")
    return this.getOrThrow()
}

fun <T> Result<T>.shouldBeFailure(): Throwable {
    assertTrue(this.isFailure, "Expected failure but was success: ${this.getOrNull()}")
    return this.exceptionOrNull()!!
}

// Usage
@Test
fun `repository returns success`() {
    val result = repository.getUser("1")
    val user = result.shouldBeSuccess()
    assertEquals("John", user.name)
}
```

## Espresso UI Testing

```kotlin
@RunWith(AndroidJUnit4::class)
class LoginActivityTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(LoginActivity::class.java)

    @Test
    fun loginButton_isDisabled_whenEmailIsEmpty() {
        onView(withId(R.id.emailInput)).perform(clearText())
        onView(withId(R.id.passwordInput)).perform(typeText("password123"))

        onView(withId(R.id.loginButton)).check(matches(not(isEnabled())))
    }

    @Test
    fun successfulLogin_navigatesToHome() {
        onView(withId(R.id.emailInput)).perform(typeText("test@example.com"))
        onView(withId(R.id.passwordInput)).perform(typeText("password123"))
        onView(withId(R.id.loginButton)).perform(click())

        onView(withId(R.id.homeScreen)).check(matches(isDisplayed()))
    }
}
```

## Лучшие практики

1. **Один тест = одно поведение** — каждый тест проверяет одну вещь
2. **Описательные имена** — используйте backticks для читаемых названий
3. **AAA паттерн** — Arrange, Act, Assert в каждом тесте
4. **Изолированность** — тесты не зависят друг от друга
5. **Быстрота** — unit тесты должны выполняться мгновенно
6. **Тестируйте edge cases** — null, пустые списки, ошибки
