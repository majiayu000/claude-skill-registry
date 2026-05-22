---
name: "Swift Concurrency Expert Guide"
description: "Deep dive into Swift's async/await runtime, Sendable enforcement, actors, and migration strategies."
version: "1.0.0"
dependencies: []
tags:
  - swift
  - concurrency
  - async-await
  - sendable
  - migration
---

# The Swift Concurrency Paradigm: A Comprehensive Architectural Analysis

## Executive Summary

The introduction of native concurrency in Swift represents the most
significant architectural shift in the ecosystem's history, moving from
a library-based threading model (Grand Central Dispatch) to a
language-integrated, compiler-enforced model. This report provides an
exhaustive examination of this transition. It analyzes the theoretical
underpinnings of the cooperative thread pool, the state-machine
mechanics of async/await, and the enforcement of data safety through the
Actor model and Sendable protocol.

Crucially, this document addresses the \"strict concurrency\"
requirements of Swift 6, offering detailed strategies for migration,
handling reentrancy, and managing legacy interoperability. It explores
advanced synchronization primitives, contrasting the dangers of
DispatchSemaphore with modern CheckedContinuation patterns, and details
the use of OSAllocatedUnfairLock for high-performance critical sections.
Through this analysis, we establish a definitive guide for engineering
robust, race-free applications on Apple platforms.

## 1. Theoretical Foundations: The Cooperative Execution Model

### 1.1 From Preemptive to Cooperative Multitasking

To understand the architecture of Swift Concurrency, one must first
deconstruct the limitations of its predecessor, Grand Central Dispatch
(GCD). GCD operates on a preemptive model where the operating system
creates and manages threads. While this abstracted raw pthread
management, it did not solve the problem of \"thread explosion.\" In
GCD, if a thread blocks (e.g., waiting on a semaphore or synchronous
I/O), the system spawns a new thread to maintain concurrency. This often
results in applications spawning hundreds of threads, leading to
excessive memory overhead and context-switching latency that degrades
CPU efficiency.^1^

Swift Concurrency abandons this approach in favor of a **cooperative
threading model**. In this system, the runtime maintains a limited pool
of threads, roughly equal to the number of logical CPU cores.^2^ Tasks
in Swift do not map 1:1 to threads. Instead, tasks are multiplexed onto
this fixed pool.

The defining characteristic of this model is the prohibition of
blocking. Because the thread pool is fixed, blocking a single thread
(e.g., Thread.sleep or semaphore.wait) effectively removes a CPU core
from the application\'s available resources. If enough threads are
blocked, the application enters a state of starvation or deadlock, as
the runtime cannot spawn \"rescue\" threads to unblock the system.^3^
Consequently, the await keyword is not merely a pause; it is a
**suspension point**. It signals the runtime that the current task is
yielding its thread, allowing the executor to swap in another pending
task. This context switch happens at the user-space level (mostly),
which is significantly cheaper than a kernel-level thread context
switch.^2^

### 1.2 The async/await State Machine

The transformation of a function marked async is a compile-time
operation. The compiler effectively slices the function into multiple
\"partial tasks\" at every suspension point (await).

When a function hits an await:

1.  **State Preservation:** The local variables and execution pointer
    are captured into a heap-allocated frame (a continuation).

2.  **Stack Release:** The function returns, releasing the stack frame
    and freeing the underlying thread to process other work.

3.  **Resumption:** Once the awaited operation completes, the runtime
    schedules the continuation for execution.

This mechanism implies that an async function may start on one thread,
suspend, and resume on a completely different thread from the
cooperative pool.^2^ This \"thread hopping\" is fundamental to the
model\'s efficiency but introduces complexity regarding thread-local
storage, which is no longer a viable mechanism for state persistence in
Swift Concurrency.

### 1.3 Continuation Passing Style (CPS)

Under the hood, Swift utilizes a form of Coroutine representation. This
eliminates the nested closure syntax (\"callback hell\") typical of GCD.
In GCD, handling errors and control flow across asynchronous boundaries
required complex, often duplicated logic. In Swift, the linear flow of
async/await allows standard Swift error handling (do-catch) to function
seamlessly across asynchronous boundaries.^2^

The implications for memory management are profound. In a closure-based
model, developers frequently had to manage capture lists (\[weak self\])
manually to avoid retain cycles. In structured concurrency, because the
child task's lifetime is bound to the parent's scope, self captures are
often implicit and safe, provided the task does not outlive the
object---a guarantee enforced by structured concurrency but not by
unstructured tasks.^5^

## 2. Structured Concurrency: Hierarchy and Control

Structured Concurrency is the enforcement of a parent-child relationship
on asynchronous operations. This philosophy dictates that a task cannot
complete until all tasks it has spawned have also completed. This
mirrors the behavior of synchronous code, where a function cannot return
until its internal statements have executed.

### 2.1 The Scope of async let

The simplest form of concurrency is async let, which allows for a fixed
number of child tasks to run in parallel.

> Swift

async let image = downloadImage()\
async let metadata = downloadMetadata()\
let result = try await combine(image, metadata)

Here, image and metadata are child tasks of the surrounding function. If
the parent function exits (e.g., throws an error) before these tasks
complete, the Swift runtime automatically cancels the child tasks.^7^
This automatic cancellation propagation significantly reduces the risk
of \"orphaned\" background tasks consuming resources unnecessarily.

### 2.2 TaskGroups: Dynamic Concurrency

For scenarios where the number of concurrent operations is unknown at
compile time---such as processing a list of URLs---TaskGroup is the
required primitive. Accessed via withTaskGroup or withThrowingTaskGroup,
this construct creates a scope where tasks can be added dynamically.^8^

#### 2.2.1 The Concurrency Window Pattern

A critical limitation of TaskGroup compared to OperationQueue is the
lack of a built-in maxConcurrentOperationCount property. If a developer
naïvely adds 10,000 tasks to a group in a loop, the runtime will accept
them, potentially leading to excessive memory consumption as 10,000
child tasks are initialized (though they may not all execute
simultaneously due to the thread pool limit).^9^

To mitigate this, developers must implement a \"sliding window\"
pattern. This involves filling the group up to a threshold (e.g., 10
tasks) and then waiting for one task to finish before adding the next.

**Table 1: Managing Concurrency Limits**

  -----------------------------------------------------------------------
  **Pattern**       **Mechanism**     **Pros**          **Cons**
  ----------------- ----------------- ----------------- -----------------
  **Unbounded       for url in urls { Simple syntax;    High memory
  Addition**        group.addTask     Maximizes         usage; Potential
                    {\... } }         parallelism.      server overload.

  **Sliding         if tasks \>=      Constant memory   More complex
  Window**          limit { await     footprint;        implementation;
                    group.next() }    Controlled load.  Requires manual
                                                        loop management.

  **Batching**      Split input into  Easier to reason  \"Straggler\"
                    chunks, process   about than        tasks delay the
                    chunks            windows.          entire batch.
                    sequentially.                       
  -----------------------------------------------------------------------

The \"Sliding Window\" approach is generally preferred for
high-throughput network operations.^9^

#### 2.2.2 Dependency Chains in TaskGroups

While TaskGroup is designed for parallel execution, it can model complex
dependencies. For example, a login sequence requiring sequential steps
(Location -\> Permissions -\> API Auth -\> Logging) can be modeled as a
single task within a group, or as a chain of tasks where the result of
one await feeds the next. Because the group handles error propagation,
if any step in the sequence fails (throws), the group catches the error,
and can be configured to cancel all other running sequences
immediately.^6^

### 2.3 Unstructured Concurrency: Task.init vs. Task.detached

When an asynchronous operation must extend beyond the current scope
(e.g., initiating a background download from a UI button press),
developers must break out of structured concurrency using
\"unstructured\" tasks.

1.  **Task.init (or Task { })**: Creates a new top-level task that
    inherits the **actor isolation** and **priority** of the surrounding
    context. This is the standard tool for bridging synchronous UI code
    to async logic.^2^

2.  **Task.detached**: Creates a task with *no* context inheritance. It
    does not run on the caller's actor and uses default priority. This
    is rarely needed unless the developer explicitly wants to avoid
    blocking the main thread with a computationally expensive operation
    that should not inherit the UI priority.

**Warning:** Unstructured tasks do not automatically cancel when the
creating scope ends. Developers must manually manage the Task handle and
call .cancel() if the operation should be terminated (e.g., when a view
controller deinitializes).^2^

## 3. The Actor Model: Isolation and State Integrity

The Actor model is Swift's primary mechanism for eliminating data races.
Conceptually, an actor is a reference type (like a class) that
serializes all access to its mutable state. It creates an \"island of
serialization\" in a concurrent sea.

### 3.1 The Mailbox Metaphor vs. Locks

Unlike a standard class protected by a lock (NSLock), an actor
integrates serialization into the function call itself. When code from
Task A calls a method on Actor B, the call is treated as a message sent
to Actor B\'s mailbox. If Actor B is processing another message, Task A
suspends.

This distinction is crucial: Locks block threads; Actors suspend tasks.

A lock-based approach waiting for a resource stalls the thread. An
actor-based approach yields the thread to other work.11

### 3.2 The Reentrancy Dilemma

The most significant source of logical errors in Swift Concurrency is
**Actor Reentrancy**. Swift actors are reentrant, meaning that if an
actor method suspends (encounters an await), the actor releases its
\"lock.\" Other tasks can then execute methods on the actor *before* the
original method resumes.^12^

Scenario: The Bank Account Overdraft

Consider a withdraw(amount:) method:

1.  Check balance (balance \>= amount).

2.  await database.verify().

3.  Deduct balance (balance -= amount).

If two withdrawal tasks (A and B) enter this method:

1.  Task A checks balance (success).

2.  Task A awaits database (suspends, releases lock).

3.  Task B enters, checks balance (success, because A hasn\'t deducted
    yet).

4.  Task B awaits database (suspends).

5.  Task A resumes, deducts balance.

6.  Task B resumes, deducts balance.

**Result:** A race condition resulting in a double spend or negative
balance. The state invariants validated in step 1 are no longer valid in
step 3.^12^

#### 3.2.1 Architectural Solutions to Reentrancy

Developers cannot disable reentrancy in standard Swift actors. Instead,
they must adopt specific patterns:

1.  **Invariant Re-verification:** After every await, re-check the
    conditions (e.g., is balance still sufficient?).

2.  **State Snapshotting:** Perform all calculations and mutations
    synchronously *before* or *after* the async work, minimizing the
    split logic.

3.  **Task Queues:** Implement a custom serial queue (e.g., using
    AsyncStream) inside the actor to process requests strictly
    one-by-one, essentially simulating non-reentrant behavior.^13^

### 3.3 nonisolated Access and Global Actors

Not all actor properties require isolation. Immutable data (let) is
inherently thread-safe. Marking a property or function as nonisolated
exempts it from the actor\'s protection domain, allowing synchronous
access from any thread.^15^ This is frequently used for protocol
conformance (e.g., CustomStringConvertible) where the protocol requires
a synchronous property (like description).^16^

**Global Actors** extend actor isolation to the entire program. The
\@MainActor is the most prominent example, ensuring that annotated types
and functions execute on the main thread. This effectively replaces
DispatchQueue.main logic with compiler-guaranteed safety.^18^

### 3.4 Custom Actor Executors (Swift 5.9+)

While standard actors run on the default cooperative pool, advanced use
cases (such as interacting with a database that requires thread
affinity) may demand specific execution contexts. Swift allows actors to
define a custom unownedExecutor.

By implementing the SerialExecutor protocol, an actor can route its
tasks to a specific DispatchQueue or a shared serial executor. This is
powerful for grouping multiple actors onto a single serial context to
ensure synchronous mutual exclusion across different objects without
context switching.^20^

## 4. Data Safety: The Sendable Protocol

Swift 6 strict concurrency relies on the Sendable protocol to verify
that data passed between isolation domains (e.g., from Actor A to Actor
B) cannot cause data races.

### 4.1 Value vs. Reference Semantics

- **Value Types (Structs/Enums):** Implicitly Sendable if all their
  properties are Sendable. Since copies are independent, they are safe
  to pass.^23^

- **Reference Types (Classes):** Not implicitly Sendable. Passing a
  class instance to a task creates a shared mutable reference, a classic
  race condition recipe.

To make a class Sendable, it must be:

1.  final (to prevent inheritance subversion).

2.  contain only immutable (let) properties.

3.  ensure all properties are themselves Sendable.^23^

### 4.2 \@unchecked Sendable and Internally Synchronized Classes

There are cases where a class is thread-safe but the compiler cannot
prove it---typically because it uses internal locking (mutexes, queues).
In these instances, developers can apply \@unchecked Sendable. This
annotation disables compiler checks for that type, effectively placing
the burden of safety verification on the developer.^24^

**Warning:** Using \@unchecked Sendable without implementing rigorous
internal locking (via NSLock or OSAllocatedUnfairLock) defeats the
purpose of Swift concurrency and introduces undefined behavior.^26^

### 4.3 Region-Based Isolation (Swift 6)

Swift 6 introduces sophisticated flow analysis known as Region-Based
Isolation. This allows non-Sendable types to be passed between actors
*if* the compiler can prove that the sender explicitly gives up
ownership and retains no references to the object. This \"transfer\"
semantic allows for more performant patterns (like passing a mutable
buffer to a background worker) without requiring the type to be
fundamentally thread-safe, provided uniqueness is guaranteed.^27^

## 5. Migration Strategy: Moving to Swift 6

Adopting Swift 6 is not merely a version update; it is a compliance
audit for data safety. The migration process typically follows a phased
approach to manage the deluge of compiler warnings.

### 5.1 Concurrency Checking Modes

Migration is controlled via compiler flags in Swift 5 mode:

1.  **Minimal:** Basic checks, enforcing explicit Sendable adoption but
    loose on inference.

2.  **Targeted:** Enforces Sendable constraints on code that explicitly
    uses concurrency features (like Task or actor).

3.  **Complete (Strict):** Approximates Swift 6 behavior. Every
    potential data race is flagged. Implicit \"Main Actor\" assumptions
    are removed.^27^

### 5.2 The \"Leaf Module\" Strategy

The most effective migration strategy is \"Outside-In\" or
\"Leaf-First.\"

1.  **Identify Leaf Modules:** Start with low-level utility modules that
    have no dependencies.

2.  **Enable Complete Checking:** Turn on strict concurrency for these
    modules.

3.  **Audit Public Types:** Ensure public structs and classes conform to
    Sendable. If a type cannot be Sendable, consider if it should be an
    Actor.

4.  **Propagate Upward:** Once the foundation is solid, move to feature
    modules. This prevents a cascade of warnings where higher-level
    modules complain about lower-level types being non-Sendable.^27^

### 5.3 Handling Common Migration Warnings

**Warning:** \"Capture of non-Sendable type in \@Sendable closure.\"

- **Context:** Often occurs when a closure captures self or a local
  variable that is mutable.

- **Solution:** Capture specific properties by value (\[name =
  self.name\]) or ensure the captured object is an actor (which is
  Sendable).^29^

**Warning:** \"Main actor-isolated property cannot be mutated from
non-isolated context.\"

- **Context:** A background task tries to update a UI property.

- **Solution:** Wrap the mutation in await MainActor.run {\... } or mark
  the calling function as \@MainActor.^30^

The \@preconcurrency Escape Hatch

When a project depends on a third-party library that has not yet updated
to Swift 6 (i.e., its types are not marked Sendable), the compiler will
generate warnings for code using that library. By importing the module
with \@preconcurrency import ModuleName, developers can suppress these
warnings, instructing the compiler to downgrade strict checks to dynamic
runtime checks for that specific dependency.28

## 6. Advanced Synchronization Primitives

In the transition to Swift Concurrency, many legacy patterns must be
abandoned. The most dangerous among them is the use of
DispatchSemaphore.

### 6.1 The Hazard of DispatchSemaphore

In GCD, it was common to use a semaphore to force a synchronous wait for
an asynchronous callback.

> Swift

// DANGEROUS IN SWIFT CONCURRENCY\
let sem = DispatchSemaphore(value: 0)\
asyncTask { sem.signal() }\
sem.wait() // Blocks the thread

In the cooperative pool, sem.wait() does not yield the thread; it holds
it hostage. If this pattern is used in a Task, it can deadlock the
system by consuming a thread that might be needed by the very asyncTask
it is waiting for (Priority Inversion/Starvation).^32^

### 6.2 The Solution: CheckedContinuation

To bridge legacy callback-based code to async/await without blocking,
Swift provides Continuations.

> Swift

// CORRECT PATTERN\
func modernAsync() async -\> ResultType {\
await withCheckedContinuation { continuation in\
legacyCallbackBasedAPI { result in\
continuation.resume(returning: result)\
}\
}\
}

withCheckedContinuation suspends the current task and provides a
continuation handle. The thread is freed. When the legacy API calls the
completion block, continuation.resume() is called, and the runtime
schedules the task to resume. This bridges the worlds safely.^34^

**Note:** CheckedContinuation performs runtime checks to ensure resume
is called exactly once. UnsafeContinuation skips these checks for
performance but yields undefined behavior if misused.^36^

### 6.3 Low-Level Locking: OSAllocatedUnfairLock

Sometimes, actors are too heavy. If a class needs to protect a single
integer or a small buffer synchronously, an actor\'s await requirement
is cumbersome. Swift 6 and recent OS versions introduce
OSAllocatedUnfairLock.

Unlike os_unfair_lock (which is a C-struct and unsafe to move/copy in
Swift), OSAllocatedUnfairLock is a managed object. It is safe to use in
Swift classes.

> Swift

final class ThreadSafeCounter: \@unchecked Sendable {\
let lock = OSAllocatedUnfairLock(initialState: 0)\
\
func increment() {\
lock.withLock { state in\
state += 1\
}\
}\
}

This pattern is performant and correct for small critical sections. The
class is marked \@unchecked Sendable because the compiler doesn\'t
understand the lock\'s semantics, but the developer asserts safety via
the lock.^26^

## 7. Performance Optimization and UI Integration

### 7.1 View Lifecycle: .task vs. .onAppear

In SwiftUI, initiating async work is best done via .task.

- **.onAppear**: Synchronous. Executes when the view graph is updated.
  Work started here (e.g., via Task { }) is not automatically cancelled
  when the view disappears.

- **.task**: Asynchronous context. Automatically cancels the task when
  the view disappears.

**Nuance:** .task runs asynchronously. If a view relies on data loaded
in .task to render its initial frame, the user may see a flicker or a
placeholder. .onAppear runs eagerly during the view update cycle, which
can sometimes result in faster initial data readiness if the data is
locally cached, but .task is architecturally superior for network
operations due to lifecycle management.^38^

### 7.2 Priority Inversion and Thread Explosion

Swift Concurrency employs Priority Inheritance to mitigate inversions,
where a high-priority task blocked by a low-priority task boosts the
latter\'s priority. However, in a constrained thread pool, \"Thread
Explosion\" is the greater risk.

Thread explosion happens when tasks block on external resources (IO)
without suspending. The runtime may (in limited cases) spawn threads to
compensate, but generally, it relies on developers using await. To avoid
priority inversions:

1.  Use specific Task priorities (.userInitiated, .background)
    appropriate to the work.

2.  Use Task.yield() in long-running background loops to allow
    higher-priority tasks access to the CPU.^40^

3.  **Never** perform blocking IO in a Task; use FileHandle.bytes or
    URLSession async APIs.^2^

### 7.3 Testing Concurrent Code

Testing async code requires the XCTest framework\'s support for async
test methods.

> Swift

func testAsyncOperation() async throws {\
let result = try await myActor.doWork()\
XCTAssertTrue(result)\
}

Unit tests naturally support await. However, testing precise
interleaving (race conditions) remains difficult. Frameworks like Swift
Testing (the new testing framework) and Point-Free\'s Concurrency Extras
are evolving to provide deterministic control over the serial executor
for testing purposes.^2^

## Conclusion

The transition to Swift Concurrency and Swift 6 is a fundamental
re-platforming of the Apple ecosystem. It trades the flexibility and
danger of raw pointer/thread manipulation for the safety and structure
of compiled-verified task graphs. By mastering Actors for state
isolation, TaskGroups for dynamic concurrency, and Continuations for
legacy interoperability, developers can construct applications that are
immune to entire categories of memory corruption and race conditions.
The cost is a stricter adherence to architectural rules---specifically
regarding locking and reentrancy---but the result is a codebase that
scales securely on modern multi-core silicon.

**Citations:**

#### Works cited

1.  Swift 6 Incomplete Migration Guide for Dummies - BrightDigit,
    accessed November 24, 2025,
    [[https://brightdigit.com/tutorials/swift-6-async-await-actors-fixes]{.underline}](https://brightdigit.com/tutorials/swift-6-async-await-actors-fixes)

2.  Async await in Swift explained with code examples - SwiftLee,
    accessed November 24, 2025,
    [[https://www.avanderlee.com/swift/async-await/]{.underline}](https://www.avanderlee.com/swift/async-await/)

3.  Basics of DispatchSemaphore: Synchronization in Swift - Medium,
    accessed November 24, 2025,
    [[https://medium.com/@hyleedevelop/swift-basics-of-dispatchsemaphore-c1081d273806]{.underline}](https://medium.com/@hyleedevelop/swift-basics-of-dispatchsemaphore-c1081d273806)

4.  In Swift async/await, can I use Lock or Semaphore - Stack Overflow,
    accessed November 24, 2025,
    [[https://stackoverflow.com/questions/76562442/in-swift-async-await-can-i-use-lock-or-semaphore]{.underline}](https://stackoverflow.com/questions/76562442/in-swift-async-await-can-i-use-lock-or-semaphore)

5.  Mastering Concurrency in iOS App Development: A Deep Dive into Swift
    Concurrency and Async/Await - 30 Days Coding, accessed November 24,
    2025,
    [[https://30dayscoding.com/blog/developing-ios-apps-with-swift-concurrency-and-async-await]{.underline}](https://30dayscoding.com/blog/developing-ios-apps-with-swift-concurrency-and-async-await)

6.  TaskGroup as a workflow design tool - try Code, accessed November
    24, 2025,
    [[https://trycombine.com/posts/swift-concurrency-task-group-workflow/]{.underline}](https://trycombine.com/posts/swift-concurrency-task-group-workflow/)

7.  Question about WWDC Video - Explore Structured Concurrency in Swift,
    accessed November 24, 2025,
    [[https://forums.swift.org/t/question-about-wwdc-video-explore-structured-concurrency-in-swift/83145]{.underline}](https://forums.swift.org/t/question-about-wwdc-video-explore-structured-concurrency-in-swift/83145)

8.  Task Groups in Swift explained with code examples - SwiftLee,
    accessed November 24, 2025,
    [[https://www.avanderlee.com/concurrency/task-groups-in-swift/]{.underline}](https://www.avanderlee.com/concurrency/task-groups-in-swift/)

9.  Mastering TaskGroups in Swift \| Swift with Majid, accessed November
    24, 2025,
    [[https://swiftwithmajid.com/2025/02/04/mastering-task-groups-in-swift/]{.underline}](https://swiftwithmajid.com/2025/02/04/mastering-task-groups-in-swift/)

10. What is the difference between .onAppear() and .task() in SwiftUI
    3? - Stack Overflow, accessed November 24, 2025,
    [[https://stackoverflow.com/questions/68114509/what-is-the-difference-between-onappear-and-task-in-swiftui-3]{.underline}](https://stackoverflow.com/questions/68114509/what-is-the-difference-between-onappear-and-task-in-swiftui-3)

11. Migrating to Swift 6: The Strict Concurrency You Must Adopt -
    Apiumhub, accessed November 24, 2025,
    [[https://apiumhub.com/tech-blog-barcelona/migrating-to-swift-6/]{.underline}](https://apiumhub.com/tech-blog-barcelona/migrating-to-swift-6/)

12. Swift Actor Reentrancy Explained: Safer Concurrency With a Hidden
    \..., accessed November 24, 2025,
    [[https://medium.com/@tungvt.it.01/swift-actor-reentrancy-explained-safer-concurrency-with-a-hidden-trap-3ef3259c0c6c]{.underline}](https://medium.com/@tungvt.it.01/swift-actor-reentrancy-explained-safer-concurrency-with-a-hidden-trap-3ef3259c0c6c)

13. Blog - Actor Reentrancy in Swift - Michael Tsai, accessed November
    24, 2025,
    [[https://mjtsai.com/blog/2024/07/29/actor-reentrancy-in-swift/]{.underline}](https://mjtsai.com/blog/2024/07/29/actor-reentrancy-in-swift/)

14. \[Concurrency\] Actors & actor isolation - Page 3 - Pitches - Swift
    Forums, accessed November 24, 2025,
    [[https://forums.swift.org/t/concurrency-actors-actor-isolation/41613?page=3]{.underline}](https://forums.swift.org/t/concurrency-actors-actor-isolation/41613?page=3)

15. How to Make Parts of an Actor Nonisolated in Swift - DhiWise,
    accessed November 24, 2025,
    [[https://www.dhiwise.com/post/how-to-make-parts-of-an-actor-nonisolated-in-swift]{.underline}](https://www.dhiwise.com/post/how-to-make-parts-of-an-actor-nonisolated-in-swift)

16. Nonisolated and isolated keywords: Understanding Actor isolation -
    SwiftLee, accessed November 24, 2025,
    [[https://www.avanderlee.com/swift/nonisolated-isolated/]{.underline}](https://www.avanderlee.com/swift/nonisolated-isolated/)

17. when use nonisolated with stored properties of actor? - Stack
    Overflow, accessed November 24, 2025,
    [[https://stackoverflow.com/questions/75651770/when-use-nonisolated-with-stored-properties-of-actor]{.underline}](https://stackoverflow.com/questions/75651770/when-use-nonisolated-with-stored-properties-of-actor)

18. MainActor usage in Swift explained to dispatch to the main thread,
    accessed November 24, 2025,
    [[https://www.avanderlee.com/swift/mainactor-dispatch-main-thread/]{.underline}](https://www.avanderlee.com/swift/mainactor-dispatch-main-thread/)

19. SwiftUI Closures on the Main Thread: Why \@MainActor Is a
    Game-Changer - Medium, accessed November 24, 2025,
    [[https://medium.com/@bala.mobdev/swiftui-closures-on-the-main-thread-why-mainactor-is-a-game-changer-c749ee79650c]{.underline}](https://medium.com/@bala.mobdev/swiftui-closures-on-the-main-thread-why-mainactor-is-a-game-changer-c749ee79650c)

20. SerialExecutor \| Apple Developer Documentation, accessed November
    24, 2025,
    [[https://developer.apple.com/documentation/swift/serialexecutor]{.underline}](https://developer.apple.com/documentation/swift/serialexecutor)

21. swift-evolution/proposals/0392-custom-actor-executors.md at main -
    GitHub, accessed November 24, 2025,
    [[https://github.com/swiftlang/swift-evolution/blob/main/proposals/0392-custom-actor-executors.md]{.underline}](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0392-custom-actor-executors.md)

22. Controlling Actors With Custom Executors \| Jack Morris, accessed
    November 24, 2025,
    [[https://jackmorris.xyz/posts/2023/11/21/controlling-actors-with-custom-executors/]{.underline}](https://jackmorris.xyz/posts/2023/11/21/controlling-actors-with-custom-executors/)

23. Sendability and Reference Types in Swift \| by abdul ahad - Medium,
    accessed November 24, 2025,
    [[https://abdulahd1996.medium.com/sendability-and-reference-types-in-swift-56a793a3822d]{.underline}](https://abdulahd1996.medium.com/sendability-and-reference-types-in-swift-56a793a3822d)

24. Beware \@unchecked Sendable, or Watch Out for Counterintuitive
    Implicit Actor-Isolation, accessed November 24, 2025,
    [[https://jaredsinclair.com/2024/11/12/beware-unchecked.html]{.underline}](https://jaredsinclair.com/2024/11/12/beware-unchecked.html)

25. Preventing regressions when conforming to \`Sendable\` with
    \`@unchecked\` - Swift Forums, accessed November 24, 2025,
    [[https://forums.swift.org/t/preventing-regressions-when-conforming-to-sendable-with-unchecked/62137]{.underline}](https://forums.swift.org/t/preventing-regressions-when-conforming-to-sendable-with-unchecked/62137)

26. Beware of os_unfair_lock - mcky.dev, accessed November 24, 2025,
    [[https://mcky.dev/blog/beware-os-unfair/]{.underline}](https://mcky.dev/blog/beware-os-unfair/)

27. Migration Strategy \| Documentation - Swift Programming Language,
    accessed November 24, 2025,
    [[https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/migrationstrategy/]{.underline}](https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/migrationstrategy/)

28. Migrate Your App to Swift 6: A Comprehensive Guide - DEV Community,
    accessed November 24, 2025,
    [[https://dev.to/arshtechpro/migrate-your-app-to-swift-6-a-comprehensive-guide-14df]{.underline}](https://dev.to/arshtechpro/migrate-your-app-to-swift-6-a-comprehensive-guide-14df)

29. Swift concurrency hack for passing non-sendable closures - Jesse
    Squires, accessed November 24, 2025,
    [[https://www.jessesquires.com/blog/2024/06/05/swift-concurrency-non-sendable-closures/]{.underline}](https://www.jessesquires.com/blog/2024/06/05/swift-concurrency-non-sendable-closures/)

30. Understanding the New Swift 6 Concurrency Features \| by Anand
    Nimje - Medium, accessed November 24, 2025,
    [[https://medium.com/@nimjea/understanding-the-new-swift-6-concurrency-features-3bff267426cc]{.underline}](https://medium.com/@nimjea/understanding-the-new-swift-6-concurrency-features-3bff267426cc)

31. Swift 6 strict concurrency : r/swift - Reddit, accessed November 24,
    2025,
    [[https://www.reddit.com/r/swift/comments/1icj54z/swift_6_strict_concurrency/]{.underline}](https://www.reddit.com/r/swift/comments/1icj54z/swift_6_strict_concurrency/)

32. Difference between Dispatch Groups and Semaphores? : r/swift -
    Reddit, accessed November 24, 2025,
    [[https://www.reddit.com/r/swift/comments/7yyf7l/difference_between_dispatch_groups_and_semaphores/]{.underline}](https://www.reddit.com/r/swift/comments/7yyf7l/difference_between_dispatch_groups_and_semaphores/)

33. Using \`async\` functions from synchronous functions (and breaking
    all the rules) - Using Swift, accessed November 24, 2025,
    [[https://forums.swift.org/t/using-async-functions-from-synchronous-functions-and-breaking-all-the-rules/59782]{.underline}](https://forums.swift.org/t/using-async-functions-from-synchronous-functions-and-breaking-all-the-rules/59782)

34. withCheckedContinuation and \[weak self\] in Swift Concurrency? -
    Stack Overflow, accessed November 24, 2025,
    [[https://stackoverflow.com/questions/78148038/withcheckedcontinuation-and-weak-self-in-swift-concurrency]{.underline}](https://stackoverflow.com/questions/78148038/withcheckedcontinuation-and-weak-self-in-swift-concurrency)

35. How to create and async/await-based semaphore in Swift like this one
    in JavaScript which uses Promise? - Stack Overflow, accessed
    November 24, 2025,
    [[https://stackoverflow.com/questions/76546496/how-to-create-and-async-await-based-semaphore-in-swift-like-this-one-in-javascri]{.underline}](https://stackoverflow.com/questions/76546496/how-to-create-and-async-await-based-semaphore-in-swift-like-this-one-in-javascri)

36. Mastering SwiftUI: Understanding All Continuations in Swift \| by
    ViralSwift - Medium, accessed November 24, 2025,
    [[https://medium.com/@viralswift/mastering-swiftui-understanding-all-continuations-in-swift-6d8c94fd4453]{.underline}](https://medium.com/@viralswift/mastering-swiftui-understanding-all-continuations-in-swift-6d8c94fd4453)

37. OSAllocatedUnfairLock \| Apple Developer Documentation, accessed
    November 24, 2025,
    [[https://developer.apple.com/documentation/os/osallocatedunfairlock]{.underline}](https://developer.apple.com/documentation/os/osallocatedunfairlock)

38. Running Code When Your View Appears - Chris Eidhof, accessed
    November 24, 2025,
    [[https://chris.eidhof.nl/post/swiftui-on-appear-vs-task/]{.underline}](https://chris.eidhof.nl/post/swiftui-on-appear-vs-task/)

39. Running Code Only Once in SwiftUI \| Swiftjective-C, accessed
    November 24, 2025,
    [[https://www.swiftjectivec.com/swiftui-run-code-only-once-versus-onappear-or-task/]{.underline}](https://www.swiftjectivec.com/swiftui-run-code-only-once-versus-onappear-or-task/)

40. How to Set Task Priority in SwiftUI for Better App Performance -
    DhiWise, accessed November 24, 2025,
    [[https://www.dhiwise.com/post/how-to-set-task-priority-in-swiftui-for-better-app-performance]{.underline}](https://www.dhiwise.com/post/how-to-set-task-priority-in-swiftui-for-better-app-performance)

41. Concurrency Visualized --- Part 3: Pitfalls and Conclusion - Medium,
    accessed November 24, 2025,
    [[https://medium.com/@almalehdev/concurrency-visualized-part-3-pitfalls-and-conclusion-2b893e04b97d]{.underline}](https://medium.com/@almalehdev/concurrency-visualized-part-3-pitfalls-and-conclusion-2b893e04b97d)
