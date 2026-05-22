---
name: java-concurrency
description: Use when Java concurrency with ExecutorService, CompletableFuture, and virtual threads. Use when building concurrent applications.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Java Concurrency

Master Java's concurrency utilities including ExecutorService,
CompletableFuture, locks, and modern virtual threads for building
high-performance concurrent applications.

## Thread Basics

Understanding Java threads is fundamental to concurrency.

**Creating and running threads:**

```java
public class ThreadBasics {
    public static void main(String[] args) {
        // Using Thread class
        Thread thread1 = new Thread(() -> {
            System.out.println("Running in thread: " +
                Thread.currentThread().getName());
        });
        thread1.start();

        // Using Runnable
        Runnable task = () -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Task iteration: " + i);
            }
        };
        Thread thread2 = new Thread(task);
        thread2.start();

        // Join threads
        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## ExecutorService

ExecutorService provides thread pool management and task scheduling.

**Basic executor usage:**

```java
import java.util.concurrent.*;

public class ExecutorBasics {
    public static void main(String[] args) {
        // Fixed thread pool
        ExecutorService executor = Executors.newFixedThreadPool(3);

        // Submit tasks
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Task " + taskId + " on " +
                    Thread.currentThread().getName());
                return taskId * 2;
            });
        }

        // Shutdown executor
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
```

**Different executor types:**

```java
public class ExecutorTypes {
    public static void main(String[] args) {
        // Single thread executor
        ExecutorService single = Executors.newSingleThreadExecutor();

        // Fixed thread pool
        ExecutorService fixed = Executors.newFixedThreadPool(4);

        // Cached thread pool (creates threads as needed)
        ExecutorService cached = Executors.newCachedThreadPool();

        // Scheduled executor
        ScheduledExecutorService scheduled =
            Executors.newScheduledThreadPool(2);

        // Schedule task with delay
        scheduled.schedule(() -> {
            System.out.println("Delayed task");
        }, 5, TimeUnit.SECONDS);

        // Schedule periodic task
        scheduled.scheduleAtFixedRate(() -> {
            System.out.println("Periodic task");
        }, 0, 1, TimeUnit.SECONDS);

        // Work stealing pool (uses available processors)
        ExecutorService workStealing =
            Executors.newWorkStealingPool();
    }
}
```

**Future pattern:**

```java
public class FutureExample {
    public static void main(String[] args) throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(2);

        // Submit callable
        Future<Integer> future = executor.submit(() -> {
            Thread.sleep(1000);
            return 42;
        });

        // Do other work
        System.out.println("Waiting for result...");

        // Get result (blocks until ready)
        Integer result = future.get();
        System.out.println("Result: " + result);

        // With timeout
        try {
            Integer result2 = future.get(500, TimeUnit.MILLISECONDS);
        } catch (TimeoutException e) {
            System.out.println("Timed out");
            future.cancel(true);
        }

        // Check status
        boolean isDone = future.isDone();
        boolean isCancelled = future.isCancelled();

        executor.shutdown();
    }
}
```

## CompletableFuture

CompletableFuture enables composable asynchronous programming.

**Basic CompletableFuture:**

```java
import java.util.concurrent.CompletableFuture;

public class CompletableFutureBasics {
    public static void main(String[] args) {
        // Create completed future
        CompletableFuture<String> future =
            CompletableFuture.completedFuture("Hello");

        // Async computation
        CompletableFuture<Integer> asyncFuture =
            CompletableFuture.supplyAsync(() -> {
                sleep(1000);
                return 42;
            });

        // Run async without return value
        CompletableFuture<Void> runAsync =
            CompletableFuture.runAsync(() -> {
                System.out.println("Running async");
            });

        // Get result (blocking)
        try {
            Integer result = asyncFuture.get();
            System.out.println("Result: " + result);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void sleep(long millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

**Chaining operations:**

```java
public class CompletableFutureChaining {
    public static void main(String[] args) {
        // thenApply - transform result
        CompletableFuture<String> future =
            CompletableFuture.supplyAsync(() -> "Hello")
                .thenApply(s -> s + " World")
                .thenApply(String::toUpperCase);

        System.out.println(future.join()); // HELLO WORLD

        // thenAccept - consume result
        CompletableFuture.supplyAsync(() -> 42)
            .thenAccept(result ->
                System.out.println("Result: " + result));

        // thenRun - run after completion
        CompletableFuture.supplyAsync(() -> "Done")
            .thenRun(() -> System.out.println("Finished"));

        // thenCompose - flatten nested futures
        CompletableFuture<String> composed =
            CompletableFuture.supplyAsync(() -> "User123")
                .thenCompose(userId -> fetchUserDetails(userId));
    }

    static CompletableFuture<String> fetchUserDetails(String userId) {
        return CompletableFuture.supplyAsync(() ->
            "Details for " + userId);
    }
}
```

**Combining futures:**

```java
public class CombiningFutures {
    public static void main(String[] args) {
        CompletableFuture<Integer> future1 =
            CompletableFuture.supplyAsync(() -> 10);
        CompletableFuture<Integer> future2 =
            CompletableFuture.supplyAsync(() -> 20);

        // Combine two futures
        CompletableFuture<Integer> combined = future1.thenCombine(
            future2,
            (a, b) -> a + b
        );
        System.out.println(combined.join()); // 30

        // Accept both results
        future1.thenAcceptBoth(future2, (a, b) ->
            System.out.println("Sum: " + (a + b)));

        // Run after both complete
        future1.runAfterBoth(future2, () ->
            System.out.println("Both completed"));

        // Either - whichever completes first
        CompletableFuture<String> either =
            future1.applyToEither(future2, result ->
                "First result: " + result);

        // All of - wait for all
        CompletableFuture<Void> allOf =
            CompletableFuture.allOf(future1, future2);

        // Any of - wait for any
        CompletableFuture<Object> anyOf =
            CompletableFuture.anyOf(future1, future2);
    }
}
```

**Error handling:**

```java
public class FutureErrorHandling {
    public static void main(String[] args) {
        // exceptionally - handle error
        CompletableFuture<Integer> future1 =
            CompletableFuture.supplyAsync(() -> {
                if (Math.random() > 0.5) {
                    throw new RuntimeException("Error!");
                }
                return 42;
            }).exceptionally(ex -> {
                System.err.println("Error: " + ex.getMessage());
                return -1; // Default value
            });

        // handle - handle both success and error
        CompletableFuture<Integer> future2 =
            CompletableFuture.supplyAsync(() -> 10 / 0)
                .handle((result, ex) -> {
                    if (ex != null) {
                        System.err.println("Error: " + ex.getMessage());
                        return 0;
                    }
                    return result;
                });

        // whenComplete - side effect for both success and error
        CompletableFuture.supplyAsync(() -> "Hello")
            .whenComplete((result, ex) -> {
                if (ex != null) {
                    System.err.println("Failed");
                } else {
                    System.out.println("Success: " + result);
                }
            });
    }
}
```

## Locks and Synchronization

Beyond synchronized blocks, Java provides explicit locks.

**ReentrantLock:**

```java
import java.util.concurrent.locks.ReentrantLock;

public class ReentrantLockExample {
    private final ReentrantLock lock = new ReentrantLock();
    private int counter = 0;

    public void increment() {
        lock.lock();
        try {
            counter++;
        } finally {
            lock.unlock(); // Always unlock in finally
        }
    }

    public void tryLockExample() {
        if (lock.tryLock()) {
            try {
                // Critical section
                counter++;
            } finally {
                lock.unlock();
            }
        } else {
            System.out.println("Could not acquire lock");
        }
    }

    public void fairLockExample() {
        // Fair lock - serves threads in order
        ReentrantLock fairLock = new ReentrantLock(true);
        fairLock.lock();
        try {
            // Critical section
        } finally {
            fairLock.unlock();
        }
    }
}
```

**ReadWriteLock:**

```java
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.HashMap;
import java.util.Map;

public class ReadWriteLockExample {
    private final Map<String, String> cache = new HashMap<>();
    private final ReadWriteLock lock = new ReentrantReadWriteLock();

    public String get(String key) {
        lock.readLock().lock();
        try {
            return cache.get(key);
        } finally {
            lock.readLock().unlock();
        }
    }

    public void put(String key, String value) {
        lock.writeLock().lock();
        try {
            cache.put(key, value);
        } finally {
            lock.writeLock().unlock();
        }
    }
}
```

**Condition variables:**

```java
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.LinkedList;
import java.util.Queue;

public class BoundedBuffer<T> {
    private final Queue<T> queue = new LinkedList<>();
    private final int capacity;
    private final Lock lock = new ReentrantLock();
    private final Condition notFull = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();

    public BoundedBuffer(int capacity) {
        this.capacity = capacity;
    }

    public void put(T item) throws InterruptedException {
        lock.lock();
        try {
            while (queue.size() == capacity) {
                notFull.await(); // Wait until not full
            }
            queue.add(item);
            notEmpty.signal(); // Signal waiting consumers
        } finally {
            lock.unlock();
        }
    }

    public T take() throws InterruptedException {
        lock.lock();
        try {
            while (queue.isEmpty()) {
                notEmpty.await(); // Wait until not empty
            }
            T item = queue.remove();
            notFull.signal(); // Signal waiting producers
            return item;
        } finally {
            lock.unlock();
        }
    }
}
```

## CountDownLatch and CyclicBarrier

Coordination utilities for managing thread synchronization.

**CountDownLatch:**

```java
import java.util.concurrent.CountDownLatch;

public class CountDownLatchExample {
    public static void main(String[] args) throws InterruptedException {
        int workerCount = 3;
        CountDownLatch startSignal = new CountDownLatch(1);
        CountDownLatch doneSignal = new CountDownLatch(workerCount);

        for (int i = 0; i < workerCount; i++) {
            new Thread(new Worker(startSignal, doneSignal)).start();
        }

        System.out.println("Preparing workers...");
        Thread.sleep(1000);

        startSignal.countDown(); // Start all workers
        doneSignal.await(); // Wait for all to finish

        System.out.println("All workers completed");
    }

    static class Worker implements Runnable {
        private final CountDownLatch startSignal;
        private final CountDownLatch doneSignal;

        Worker(CountDownLatch startSignal, CountDownLatch doneSignal) {
            this.startSignal = startSignal;
            this.doneSignal = doneSignal;
        }

        public void run() {
            try {
                startSignal.await(); // Wait for start signal
                doWork();
                doneSignal.countDown(); // Signal completion
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        void doWork() {
            System.out.println("Worker " +
                Thread.currentThread().getName() + " working");
        }
    }
}
```

**CyclicBarrier:**

```java
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.BrokenBarrierException;

public class CyclicBarrierExample {
    public static void main(String[] args) {
        int parties = 3;
        CyclicBarrier barrier = new CyclicBarrier(parties, () -> {
            System.out.println("All threads reached barrier");
        });

        for (int i = 0; i < parties; i++) {
            new Thread(new Task(barrier, i)).start();
        }
    }

    static class Task implements Runnable {
        private final CyclicBarrier barrier;
        private final int id;

        Task(CyclicBarrier barrier, int id) {
            this.barrier = barrier;
            this.id = id;
        }

        public void run() {
            try {
                System.out.println("Task " + id + " working");
                Thread.sleep(1000 * id);
                System.out.println("Task " + id + " waiting at barrier");
                barrier.await(); // Wait for others
                System.out.println("Task " + id + " passed barrier");
            } catch (InterruptedException | BrokenBarrierException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
```

## Virtual Threads

Virtual threads enable lightweight concurrency at scale.

**Creating virtual threads:**

```java
public class VirtualThreads {
    public static void main(String[] args) throws InterruptedException {
        // Create and start virtual thread
        Thread vThread = Thread.startVirtualThread(() -> {
            System.out.println("Running in virtual thread: " +
                Thread.currentThread());
        });
        vThread.join();

        // Using builder
        Thread virtual = Thread.ofVirtual()
            .name("virtual-worker")
            .start(() -> {
                System.out.println("Virtual thread task");
            });
        virtual.join();

        // Factory for virtual threads
        ThreadFactory factory = Thread.ofVirtual().factory();
        Thread t = factory.newThread(() -> {
            System.out.println("Created by factory");
        });
        t.start();
        t.join();
    }
}
```

**Virtual thread executor:**

```java
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;

public class VirtualThreadExecutor {
    public static void main(String[] args) {
        // Executor with virtual threads
        try (ExecutorService executor =
                Executors.newVirtualThreadPerTaskExecutor()) {

            // Submit many tasks
            for (int i = 0; i < 10_000; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    Thread.sleep(1000);
                    System.out.println("Task " + taskId);
                    return null;
                });
            }
        } // Auto-shutdown with try-with-resources
    }
}
```

## Atomic Variables

Lock-free thread-safe operations using atomic classes.

**AtomicInteger and friends:**

```java
import java.util.concurrent.atomic.*;

public class AtomicExample {
    private final AtomicInteger counter = new AtomicInteger(0);
    private final AtomicLong longCounter = new AtomicLong(0);
    private final AtomicBoolean flag = new AtomicBoolean(false);
    private final AtomicReference<String> ref =
        new AtomicReference<>("initial");

    public void increment() {
        counter.incrementAndGet();
    }

    public int getAndAdd(int delta) {
        return counter.getAndAdd(delta);
    }

    public boolean compareAndSet(int expect, int update) {
        return counter.compareAndSet(expect, update);
    }

    public void updateReference() {
        ref.updateAndGet(current -> current.toUpperCase());
    }

    public void accumulateExample() {
        // Accumulate with custom operation
        counter.accumulateAndGet(5, (current, value) ->
            current + value * 2);
    }
}
```

## Thread-Safe Collections

Concurrent collections for safe multi-threaded access.

**ConcurrentHashMap:**

```java
import java.util.concurrent.ConcurrentHashMap;

public class ConcurrentMapExample {
    private final ConcurrentHashMap<String, Integer> map =
        new ConcurrentHashMap<>();

    public void basicOperations() {
        // Thread-safe put
        map.put("key", 1);

        // Atomic put if absent
        map.putIfAbsent("key", 2); // Won't update, returns 1

        // Atomic compute
        map.compute("key", (k, v) -> v == null ? 1 : v + 1);

        // Atomic compute if absent
        map.computeIfAbsent("newKey", k -> k.length());

        // Atomic compute if present
        map.computeIfPresent("key", (k, v) -> v * 2);

        // Atomic replace
        map.replace("key", 1, 10); // Only if current value is 1

        // Merge values
        map.merge("key", 5, (oldVal, newVal) -> oldVal + newVal);
    }

    public void bulkOperations() {
        // forEach with parallelism threshold
        map.forEach(10, (k, v) ->
            System.out.println(k + " = " + v));

        // Search
        String result = map.search(10, (k, v) ->
            v > 100 ? k : null);

        // Reduce
        Integer sum = map.reduce(10,
            (k, v) -> v,
            (v1, v2) -> v1 + v2);
    }
}
```

**Other concurrent collections:**

```java
import java.util.concurrent.*;

public class ConcurrentCollections {
    public static void main(String[] args) {
        // Blocking queue
        BlockingQueue<String> queue =
            new LinkedBlockingQueue<>(10);

        // Priority blocking queue
        BlockingQueue<Integer> priorityQueue =
            new PriorityBlockingQueue<>();

        // Concurrent linked queue (non-blocking)
        ConcurrentLinkedQueue<String> linkedQueue =
            new ConcurrentLinkedQueue<>();

        // Copy on write list (reads without locking)
        CopyOnWriteArrayList<String> list =
            new CopyOnWriteArrayList<>();

        // Concurrent skip list map (sorted)
        ConcurrentSkipListMap<String, Integer> skipList =
            new ConcurrentSkipListMap<>();
    }
}
```

## When to Use This Skill

Use java-concurrency when you need to:

- Execute tasks concurrently with thread pools
- Perform asynchronous operations with callbacks
- Coordinate multiple threads with barriers or latches
- Implement producer-consumer patterns
- Handle high-concurrency scenarios with virtual threads
- Protect shared state with locks or atomic operations
- Process tasks in parallel for better performance
- Implement timeout and cancellation for long operations
- Build reactive or event-driven applications
- Scale applications to handle thousands of concurrent tasks

## Best Practices

- Use ExecutorService instead of raw threads
- Always shutdown executors properly
- Prefer CompletableFuture for async operations
- Use virtual threads for I/O-bound tasks
- Minimize lock contention and critical sections
- Use concurrent collections over synchronized collections
- Handle InterruptedException appropriately
- Avoid blocking operations in CompletableFuture chains
- Use try-finally for lock acquisition/release
- Consider using atomic variables over locks

## Common Pitfalls

- Not shutting down executors (resource leak)
- Blocking virtual threads with synchronized blocks
- Deadlocks from incorrect lock ordering
- Race conditions from improper synchronization
- Thread pool exhaustion from blocking tasks
- Ignoring InterruptedException
- Using too many platform threads (use virtual threads)
- Not handling CompletableFuture exceptions
- Excessive lock contention hurting performance
- Incorrect use of volatile vs atomic vs synchronized

## Resources

- [Java Concurrency Tutorial](<https://docs.oracle.com/javase/tutorial/essential/concurrency/>)
- [ExecutorService Documentation](<https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ExecutorService.html>)
- [CompletableFuture Guide](<https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CompletableFuture.html>)
- [Virtual Threads JEP](<https://openjdk.org/jeps/444>)
- [Java Concurrency in Practice Book](<https://jcip.net/>)
