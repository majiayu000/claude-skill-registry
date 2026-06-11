---
name: kotlin-testing
description: "Kotlin testing with JUnit 5, Kotest, and coroutine dispatchers."
user-invocable: false
context: fork
agent: kotlin-general-engineer
routing:
  triggers:
    - "kotlin testing"
    - "junit kotlin"
    - "kotest"
    - "junit 5 kotlin"
    - "kotlin test dispatcher"
  category: kotlin
  pairs_with:
    - kotlin-coroutines
    - test-driven-development
---

# Kotlin Testing Patterns

## JUnit 5 Fundamentals

Use `@Test` for simple test cases. Prefer `@DisplayName` for readable test names.

```kotlin
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.DisplayName
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith

class UserServiceTest {

    @Test
    @DisplayName("should return user by ID when user exists")
    fun findUserById() {
        val service = UserService(FakeUserRepository())
        val user = service.findById(1L)
        assertEquals("Alice", user.name)
    }

    @Test
    fun `should throw when user not found`() {
        val service = UserService(FakeUserRepository())
        assertFailsWith<UserNotFoundException> {
            service.findById(999L)
        }
    }
}
```

## Parameterized Tests

Use `@ParameterizedTest` with `@MethodSource` for complex inputs or `@CsvSource` for simple value pairs.

```kotlin
import org.junit.jupiter.params.ParameterizedTest
import org.junit.jupiter.params.provider.CsvSource
import org.junit.jupiter.params.provider.MethodSource
import org.junit.jupiter.params.provider.Arguments
import java.util.stream.Stream

class ValidatorTest {

    @ParameterizedTest
    @CsvSource(
        "alice@example.com, true",
        "not-an-email, false",
        "'', false"
    )
    fun `should validate email addresses`(input: String, expected: Boolean) {
        assertEquals(expected, EmailValidator.isValid(input))
    }

    @ParameterizedTest
    @MethodSource("provideUserInputs")
    fun `should reject invalid users`(input: UserInput, expectedError: String) {
        val result = UserValidator.validate(input)
        assertTrue(result.isFailure)
        assertEquals(expectedError, result.exceptionOrNull()?.message)
    }

    companion object {
        @JvmStatic
        fun provideUserInputs(): Stream<Arguments> = Stream.of(
            Arguments.of(UserInput(name = "", age = 25), "Name must not be blank"),
            Arguments.of(UserInput(name = "Bob", age = -1), "Age must be positive"),
        )
    }
}
```

## Table-Driven Tests

Kotlin's data classes and list literals make table-driven tests natural without frameworks.

```kotlin
@Test
fun `should parse duration strings correctly`() {
    data class Case(val input: String, val expectedMs: Long, val label: String)

    val cases = listOf(
        Case("100ms", 100, "milliseconds"),
        Case("5s", 5000, "seconds"),
        Case("2m", 120_000, "minutes"),
        Case("1h", 3_600_000, "hours"),
    )

    cases.forEach { (input, expectedMs, label) ->
        val result = DurationParser.parse(input)
        assertEquals(expectedMs, result, "Failed for $label: input=$input")
    }
}
```

## Kotest Styles

Kotest offers multiple spec styles. Pick one per project for consistency.

```kotlin
import io.kotest.core.spec.style.FunSpec
import io.kotest.core.spec.style.BehaviorSpec
import io.kotest.core.spec.style.StringSpec
import io.kotest.matchers.shouldBe
import io.kotest.assertions.throwables.shouldThrow

// FunSpec — closest to JUnit, good default choice
class CalculatorFunSpec : FunSpec({
    test("addition of two numbers") {
        Calculator.add(2, 3) shouldBe 5
    }

    context("division") {
        test("divides evenly") {
            Calculator.divide(10, 2) shouldBe 5
        }

        test("throws on divide by zero") {
            shouldThrow<ArithmeticException> {
                Calculator.divide(1, 0)
            }
        }
    }
})

// BehaviorSpec — Given/When/Then for acceptance-style tests
class OrderBehaviorSpec : BehaviorSpec({
    Given("a cart with two items") {
        val cart = Cart().apply {
            add(Item("Widget", 9.99))
            add(Item("Gadget", 19.99))
        }

        When("checkout is completed") {
            val order = cart.checkout()

            Then("order total reflects both items") {
                order.total shouldBe 29.98
            }

            Then("order contains two line items") {
                order.items.size shouldBe 2
            }
        }
    }
})

// StringSpec — minimal boilerplate for simple tests
class StringSpecExample : StringSpec({
    "length of hello should be 5" {
        "hello".length shouldBe 5
    }

    "trimmed string should not contain leading spaces" {
        "  padded  ".trim() shouldBe "padded"
    }
})
```

## Kotest Matchers

Kotest provides expressive matchers beyond `shouldBe`.

```kotlin
import io.kotest.matchers.collections.shouldContainExactly
import io.kotest.matchers.collections.shouldHaveSize
import io.kotest.matchers.string.shouldStartWith
import io.kotest.matchers.nulls.shouldNotBeNull

val names = listOf("Alice", "Bob", "Charlie")
names shouldHaveSize 3
names shouldContainExactly listOf("Alice", "Bob", "Charlie")

val greeting: String? = getGreeting()
greeting.shouldNotBeNull()
greeting shouldStartWith "Hello"
```

## Coroutine Testing

Use `runTest` from `kotlinx-coroutines-test` to test suspending functions. `runTest` auto-advances virtual time.

```kotlin
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.advanceUntilIdle

class NotificationServiceTest {

    private val testDispatcher = StandardTestDispatcher()

    @Test
    fun `should send notification after delay`() = runTest(testDispatcher) {
        val service = NotificationService(dispatcher = testDispatcher)

        service.scheduleNotification("Hello", delayMs = 5000)
        advanceUntilIdle()

        assertEquals(1, service.sentCount)
    }

    @Test
    fun `should cancel pending notifications`() = runTest(testDispatcher) {
        val service = NotificationService(dispatcher = testDispatcher)
        val job = service.scheduleNotification("Hello", delayMs = 5000)

        job.cancel()
        advanceUntilIdle()

        assertEquals(0, service.sentCount)
    }
}
```

## MockK

MockK is the idiomatic Kotlin mocking library. Use `every {}` for stubs, `verify {}` for assertions, and `coEvery {}` / `coVerify {}` for suspending functions.

```kotlin
import io.mockk.mockk
import io.mockk.every
import io.mockk.coEvery
import io.mockk.verify
import io.mockk.coVerify
import io.mockk.slot

class OrderServiceTest {

    private val repo = mockk<OrderRepository>()
    private val notifier = mockk<Notifier>(relaxed = true)
    private val service = OrderService(repo, notifier)

    @Test
    fun `should save order and notify`() {
        val orderSlot = slot<Order>()
        every { repo.save(capture(orderSlot)) } returns Order(id = 42)

        service.placeOrder(items = listOf("Widget"))

        assertEquals(42, orderSlot.captured.id)
        verify(exactly = 1) { notifier.send(any()) }
    }

    @Test
    fun `should fetch order from remote API`() = runTest {
        coEvery { repo.fetchRemote(1L) } returns Order(id = 1, status = "shipped")

        val order = service.getOrder(1L)

        assertEquals("shipped", order.status)
        coVerify { repo.fetchRemote(1L) }
    }
}
```

## Assertion Libraries Summary

| Library | Syntax Style | Best For |
|---------|-------------|----------|
| `kotlin.test` | `assertEquals(expected, actual)` | JUnit 5 projects, zero extra deps |
| Kotest matchers | `actual shouldBe expected` | Readable assertions, rich matcher library |
| AssertJ (via assertk) | `assertThat(actual).isEqualTo(expected)` | Java interop, fluent chains |

## Key Principles

1. **One assertion concept per test** -- a test should verify one behavior, though it may need multiple assertions to do so.
2. **Use `runTest` for all coroutine tests** -- never use `runBlocking` in tests; `runTest` handles virtual time and uncaught exceptions.
3. **Prefer fakes over mocks** -- mocks couple tests to implementation; fakes (manual implementations) couple tests to contracts.
4. **Name tests as behavior specifications** -- backtick names like `` `should return empty list when no results` `` read better in reports.
5. **Inject dispatchers** -- never hardcode `Dispatchers.IO` in production code; accept a `CoroutineDispatcher` parameter so tests can supply `TestDispatcher`.
