---
name: Kotlin Coroutines
description: Use when kotlin coroutines for structured concurrency including suspend functions, coroutine builders, Flow, channels, and patterns for building efficient asynchronous code with cancellation and exception handling.
allowed-tools: []
---

# Kotlin Coroutines

## Introduction

Kotlin coroutines provide a powerful framework for asynchronous programming that
is lightweight, expressive, and built on structured concurrency principles.
Coroutines enable writing asynchronous code that looks and behaves like
sequential code, eliminating callback hell and improving readability.

Unlike threads, coroutines are extremely lightweight—millions can run on limited
resources. The coroutine framework includes suspend functions for non-blocking
operations, builders for launching work, Flow for reactive streams, and
comprehensive cancellation and exception handling mechanisms.

This skill covers coroutine fundamentals, builders, contexts, Flow, channels,
and production patterns for Android development and server-side Kotlin.

## Suspend Functions

Suspend functions are the building blocks of coroutines, enabling non-blocking
operations that can be paused and resumed without blocking threads.

```kotlin
// Basic suspend function
suspend fun fetchUser(id: Int): User {
    delay(1000) // Suspends without blocking
    return User(id, "Alice")
}

data class User(val id: Int, val name: String)

// Calling suspend functions
suspend fun loadUserProfile(id: Int): UserProfile {
    val user = fetchUser(id)
    val posts = fetchPosts(user.id)
    return UserProfile(user, posts)
}

suspend fun fetchPosts(userId: Int): List<Post> {
    delay(500)
    return emptyList()
}

data class Post(val id: Int, val title: String)
data class UserProfile(val user: User, val posts: List<Post>)

// Sequential vs concurrent execution
suspend fun loadDataSequential(): Pair<User, List<Post>> {
    val user = fetchUser(1)
    val posts = fetchPosts(1)
    return user to posts
}

suspend fun loadDataConcurrent(): Pair<User, List<Post>> = coroutineScope {
    val userDeferred = async { fetchUser(1) }
    val postsDeferred = async { fetchPosts(1) }
    userDeferred.await() to postsDeferred.await()
}

// Suspend functions with callbacks
suspend fun fetchData(url: String): String = suspendCoroutine { continuation ->
    fetchDataWithCallback(url) { result, error ->
        if (error != null) {
            continuation.resumeWithException(error)
        } else {
            continuation.resume(result)
        }
    }
}

fun fetchDataWithCallback(
    url: String,
    callback: (String, Exception?) -> Unit
) {
    // Simulated callback-based API
    callback("data", null)
}

// Cancellable suspend functions
suspend fun downloadFile(url: String): ByteArray =
    suspendCancellableCoroutine { continuation ->
        val request = startDownload(url) { data, error ->
            if (error != null) {
                continuation.resumeWithException(error)
            } else {
                continuation.resume(data)
            }
        }

        continuation.invokeOnCancellation {
            request.cancel()
        }
    }

class DownloadRequest {
    fun cancel() {}
}

fun startDownload(url: String, callback: (ByteArray, Exception?) -> Unit):
    DownloadRequest {
    return DownloadRequest()
}

// Using withContext for dispatcher switching
suspend fun saveToDatabase(user: User) {
    withContext(Dispatchers.IO) {
        // Database operation on IO dispatcher
        println("Saving user: ${user.name}")
    }
}

suspend fun updateUI(user: User) {
    withContext(Dispatchers.Main) {
        // UI update on main thread
        println("Updating UI for: ${user.name}")
    }
}
```

Suspend functions are marked with the `suspend` modifier and can only be called
from other suspend functions or coroutines, ensuring proper context.

## Coroutine Builders

Coroutine builders launch coroutines with different lifecycle and result
handling semantics, enabling structured and unstructured concurrency.

```kotlin
// launch: fire-and-forget coroutine
fun launchExample() {
    GlobalScope.launch {
        val user = fetchUser(1)
        println("User: ${user.name}")
    }
}

// async: coroutine with result
fun asyncExample() {
    GlobalScope.launch {
        val deferredUser = async { fetchUser(1) }
        val deferredPosts = async { fetchPosts(1) }

        val user = deferredUser.await()
        val posts = deferredPosts.await()

        println("Loaded ${posts.size} posts for ${user.name}")
    }
}

// runBlocking: bridges blocking and suspending worlds
fun runBlockingExample() = runBlocking {
    val user = fetchUser(1)
    println("User loaded: ${user.name}")
}

// coroutineScope: structured concurrency
suspend fun loadMultipleUsers(ids: List<Int>): List<User> = coroutineScope {
    ids.map { id ->
        async { fetchUser(id) }
    }.awaitAll()
}

// supervisorScope: independent child failures
suspend fun loadDataWithSupervisor(): List<User> = supervisorScope {
    val user1 = async { fetchUser(1) }
    val user2 = async {
        delay(100)
        throw Exception("Failed")
    }

    // user1 succeeds even if user2 fails
    listOfNotNull(
        try { user1.await() } catch (e: Exception) { null }
    )
}

// withTimeout: time-limited coroutines
suspend fun fetchWithTimeout(id: Int): User? {
    return try {
        withTimeout(2000) {
            fetchUser(id)
        }
    } catch (e: TimeoutCancellationException) {
        null
    }
}

// Structured concurrency with lifecycle
class ViewModel : CoroutineScope {
    private val job = SupervisorJob()
    override val coroutineContext: CoroutineContext
        get() = Dispatchers.Main + job

    fun loadData() {
        launch {
            val user = fetchUser(1)
            // Update UI
        }
    }

    fun onCleared() {
        job.cancel()
    }
}
```

Structured concurrency with `coroutineScope` ensures child coroutines complete
before the scope exits, preventing leaks and ensuring proper cleanup.

## Coroutine Context and Dispatchers

Coroutine context defines the execution environment including dispatcher, job,
exception handler, and coroutine name for debugging.

```kotlin
// Dispatchers for thread pools
suspend fun dispatcherExamples() {
    // Main: UI thread (Android/JavaFX)
    withContext(Dispatchers.Main) {
        println("On main thread: ${Thread.currentThread().name}")
    }

    // IO: for blocking I/O operations
    withContext(Dispatchers.IO) {
        println("On IO thread: ${Thread.currentThread().name}")
    }

    // Default: CPU-intensive work
    withContext(Dispatchers.Default) {
        println("On default thread: ${Thread.currentThread().name}")
    }

    // Unconfined: starts in caller thread, resumes where suspended
    withContext(Dispatchers.Unconfined) {
        println("Unconfined: ${Thread.currentThread().name}")
    }
}

// Coroutine context elements
fun contextExample() {
    val scope = CoroutineScope(
        Dispatchers.Main +
        SupervisorJob() +
        CoroutineName("MyCoroutine") +
        CoroutineExceptionHandler { _, throwable ->
            println("Caught: $throwable")
        }
    )

    scope.launch {
        println("Context: $coroutineContext")
    }
}

// Inheriting context
fun inheritContextExample() {
    CoroutineScope(Dispatchers.Main).launch {
        println("Parent: ${Thread.currentThread().name}")

        launch {
            // Inherits Dispatchers.Main
            println("Child: ${Thread.currentThread().name}")
        }

        launch(Dispatchers.IO) {
            // Overrides with IO dispatcher
            println("Override: ${Thread.currentThread().name}")
        }
    }
}

// ThreadLocal context element
val threadLocalValue = ThreadLocal<String>()

suspend fun threadLocalExample() {
    threadLocalValue.set("initial")

    withContext(threadLocalValue.asContextElement("new value")) {
        println("In context: ${threadLocalValue.get()}")
    }

    println("After context: ${threadLocalValue.get()}")
}

// Custom context element
data class UserId(val id: Int) : AbstractCoroutineContextElement(Key) {
    companion object Key : CoroutineContext.Key<UserId>
}

suspend fun customContextExample() {
    withContext(UserId(42)) {
        val userId = coroutineContext[UserId]
        println("User ID: ${userId?.id}")
    }
}
```

Dispatchers determine which thread pool executes the coroutine. Context
elements are inherited by child coroutines and can be overridden.

## Flow for Reactive Streams

Flow represents a cold stream of values that are computed on demand, providing
reactive programming capabilities with backpressure and transformation operators.

```kotlin
// Basic Flow
fun numberFlow(): Flow<Int> = flow {
    for (i in 1..5) {
        delay(100)
        emit(i)
    }
}

suspend fun collectFlow() {
    numberFlow().collect { value ->
        println("Received: $value")
    }
}

// Flow builders
fun flowBuilders() {
    // flowOf: emit fixed values
    val fixedFlow = flowOf(1, 2, 3, 4, 5)

    // asFlow: convert collections
    val listFlow = listOf(1, 2, 3).asFlow()

    // flow: custom emission logic
    val customFlow = flow {
        repeat(3) {
            emit(it)
            delay(100)
        }
    }
}

// Flow transformations
suspend fun flowTransformations() {
    numberFlow()
        .map { it * 2 }
        .filter { it > 5 }
        .take(3)
        .collect { println(it) }
}

// Flow combining
suspend fun combineFlows() {
    val flow1 = flowOf(1, 2, 3)
    val flow2 = flowOf("A", "B", "C")

    // zip: pairs elements
    flow1.zip(flow2) { num, letter ->
        "$num$letter"
    }.collect { println(it) }

    // combine: latest from each
    flow1.combine(flow2) { num, letter ->
        "$num$letter"
    }.collect { println(it) }
}

// Flow exception handling
suspend fun flowExceptionHandling() {
    flow {
        emit(1)
        emit(2)
        throw Exception("Error!")
    }.catch { e ->
        println("Caught: ${e.message}")
        emit(-1)
    }.collect { println(it) }
}

// StateFlow and SharedFlow
class DataRepository {
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users

    private val _events = MutableSharedFlow<Event>()
    val events: SharedFlow<Event> = _events

    suspend fun loadUsers() {
        val loaded = fetchUsers()
        _users.value = loaded
    }

    suspend fun emitEvent(event: Event) {
        _events.emit(event)
    }

    private suspend fun fetchUsers(): List<User> {
        delay(100)
        return listOf(User(1, "Alice"))
    }
}

data class Event(val type: String)

// Flow on different dispatchers
suspend fun flowWithContext() {
    flow {
        emit(1)
        emit(2)
    }
    .flowOn(Dispatchers.IO)
    .collect { value ->
        // Collected on caller's context
        println("Value: $value")
    }
}

// Channel Flow for hot streams
fun channelFlowExample() = channelFlow {
    launch {
        repeat(3) {
            send(it)
            delay(100)
        }
    }

    launch {
        repeat(3) {
            send(it * 10)
            delay(150)
        }
    }
}
```

Flow is cold—it doesn't execute until collected. StateFlow holds state,
SharedFlow broadcasts events, and channelFlow enables concurrent emissions.

## Channels for Communication

Channels provide communication primitives for sending and receiving values
between coroutines, similar to BlockingQueue but suspending.

```kotlin
// Basic channel usage
suspend fun channelExample() {
    val channel = Channel<Int>()

    launch {
        for (x in 1..5) {
            channel.send(x)
        }
        channel.close()
    }

    for (y in channel) {
        println("Received: $y")
    }
}

// Buffered channels
fun bufferedChannelExample() {
    val channel = Channel<Int>(capacity = 4)

    GlobalScope.launch {
        for (x in 1..10) {
            println("Sending $x")
            channel.send(x)
        }
        channel.close()
    }

    GlobalScope.launch {
        delay(1000)
        for (y in channel) {
            println("Received: $y")
            delay(200)
        }
    }
}

// Channel types
fun channelTypes() {
    // Rendezvous: no buffer, sender suspends until receiver
    val rendezvous = Channel<Int>()

    // Buffered: specified capacity
    val buffered = Channel<Int>(10)

    // Unlimited: unlimited buffer
    val unlimited = Channel<Int>(Channel.UNLIMITED)

    // Conflated: keeps only latest value
    val conflated = Channel<Int>(Channel.CONFLATED)
}

// Produce builder
fun produceNumbers(): ReceiveChannel<Int> = GlobalScope.produce {
    for (x in 1..5) {
        send(x * x)
        delay(100)
    }
}

suspend fun consumeNumbers() {
    val channel = produceNumbers()
    channel.consumeEach { println(it) }
}

// Multiple consumers
suspend fun multipleConsumers() {
    val channel = Channel<Int>()

    repeat(3) { id ->
        launch {
            for (value in channel) {
                println("Consumer $id received: $value")
            }
        }
    }

    repeat(10) {
        channel.send(it)
        delay(100)
    }

    channel.close()
}

// Select expression for multiple channels
suspend fun selectExample() {
    val channel1 = produce { send("A") }
    val channel2 = produce { send("B") }

    select<Unit> {
        channel1.onReceive { value ->
            println("From channel1: $value")
        }
        channel2.onReceive { value ->
            println("From channel2: $value")
        }
    }
}

fun CoroutineScope.produce(block: suspend () -> Unit): ReceiveChannel<String> {
    return produce {
        block()
    }
}
```

Channels enable fan-out (multiple consumers), fan-in (multiple producers), and
pipeline patterns for concurrent data processing.

## Cancellation and Exception Handling

Coroutines support cooperative cancellation and structured exception handling to
ensure proper resource cleanup and error propagation.

```kotlin
// Basic cancellation
suspend fun cancellationExample() {
    val job = GlobalScope.launch {
        repeat(1000) { i ->
            println("Working: $i")
            delay(500)
        }
    }

    delay(2000)
    println("Cancelling...")
    job.cancel()
    job.join()
    println("Cancelled")
}

// Checking for cancellation
suspend fun checkCancellation() {
    GlobalScope.launch {
        var i = 0
        while (isActive) {
            println("Computing: ${i++}")
        }
    }
}

// Non-cancellable work
suspend fun nonCancellableCleanup() {
    val job = GlobalScope.launch {
        try {
            repeat(1000) {
                delay(500)
            }
        } finally {
            withContext(NonCancellable) {
                println("Cleanup in non-cancellable context")
                delay(1000)
                println("Cleanup complete")
            }
        }
    }

    delay(1000)
    job.cancelAndJoin()
}

// Timeout handling
suspend fun timeoutExample() {
    try {
        withTimeout(1000) {
            repeat(100) {
                delay(100)
                println("Working...")
            }
        }
    } catch (e: TimeoutCancellationException) {
        println("Timed out")
    }
}

// Exception handling in coroutines
suspend fun exceptionHandlingExample() {
    val handler = CoroutineExceptionHandler { _, exception ->
        println("Caught: $exception")
    }

    GlobalScope.launch(handler) {
        throw Exception("Coroutine failed")
    }

    delay(100)
}

// Structured exception handling
suspend fun structuredExceptions() = coroutineScope {
    val job1 = launch {
        delay(100)
        throw Exception("Job 1 failed")
    }

    val job2 = launch {
        delay(200)
        println("Job 2 completed")
    }

    // job2 is cancelled when job1 fails
}

// SupervisorScope for independent failures
suspend fun supervisorExample() = supervisorScope {
    val job1 = launch {
        delay(100)
        throw Exception("Job 1 failed")
    }

    val job2 = launch {
        delay(200)
        println("Job 2 completed")
    }

    // job2 continues even if job1 fails
}

// Error handling with try-catch
suspend fun errorHandling() {
    coroutineScope {
        launch {
            try {
                fetchUser(1)
            } catch (e: Exception) {
                println("Error: ${e.message}")
            }
        }
    }
}
```

Cancellation is cooperative—coroutines must check `isActive` or call suspending
functions. Exception handling respects structured concurrency boundaries.

## Best Practices

1. **Use structured concurrency with scopes** to ensure coroutines are properly
   managed and cancelled when no longer needed

2. **Choose appropriate dispatchers** for the work type: IO for blocking
   operations, Default for CPU work, Main for UI updates

3. **Handle cancellation cooperatively** by checking isActive in loops and using
   suspending functions that support cancellation

4. **Prefer Flow over callbacks** for reactive streams to gain backpressure,
   operators, and structured lifecycle management

5. **Use supervisorScope for independent operations** to prevent one failure
   from cancelling unrelated coroutines

6. **Avoid GlobalScope except for truly application-wide work** to prevent leaks
   and maintain structured concurrency benefits

7. **Apply withContext for dispatcher switching** instead of launching new
   coroutines to maintain structure and reduce overhead

8. **Handle exceptions explicitly** with try-catch or CoroutineExceptionHandler
   to prevent silent failures

9. **Use StateFlow for state** and SharedFlow for events to provide observable
   streams with proper lifecycle awareness

10. **Test coroutines with TestCoroutineDispatcher** to control time and ensure
    deterministic test execution

## Common Pitfalls

1. **Using GlobalScope for scoped work** causes memory leaks when coroutines
   outlive their relevant context like activities or view models

2. **Blocking inside coroutines** with Thread.sleep or blocking I/O defeats the
   purpose and can exhaust thread pools

3. **Not handling cancellation** in long-running loops causes coroutines to
   continue executing after cancellation

4. **Forgetting suspend modifier** on functions that call other suspend
   functions causes compilation errors

5. **Catching CancellationException** and not rethrowing it prevents proper
   cancellation propagation in structured concurrency

6. **Using delay(0) to yield** is less clear than explicitly calling yield() for
   cooperative multitasking

7. **Creating too many coroutines unnecessarily** can degrade performance; batch
   or throttle operations when possible

8. **Not using withContext for dispatcher switching** and instead launching
   unnecessary child coroutines adds complexity

9. **Assuming immediate execution** after launch; coroutines may not start until
   dispatcher has capacity

10. **Mixing callbacks and coroutines incorrectly** without proper bridging
    creates race conditions and leaks

## When to Use This Skill

Use Kotlin coroutines when building Android applications for asynchronous
operations like network calls, database queries, or any I/O-bound work that
should not block the main thread.

Apply coroutines in server-side Kotlin applications with Ktor or Spring Boot for
handling concurrent requests efficiently without thread-per-request overhead.

Employ Flow for reactive streams in MVVM architecture, replacing LiveData or
RxJava for state management and event propagation with lifecycle awareness.

Leverage structured concurrency for coordinating multiple async operations,
ensuring proper cancellation when navigating away from screens or closing
connections.

Use channels for producer-consumer patterns, pipelines, or any scenario
requiring explicit communication between concurrent coroutines.

## Resources

- [Kotlin Coroutines Guide](<https://kotlinlang.org/docs/coroutines-guide.html>)
- [Coroutines on Android](<https://developer.android.com/kotlin/coroutines>)
- [Flow Documentation](<https://kotlinlang.org/docs/flow.html>)
- [KotlinConf Coroutines Talks](<https://www.youtube.com/kotlinconf>)
- [Coroutines Best Practices](<https://developer.android.com/kotlin/coroutines/coroutines-best-practices>)
