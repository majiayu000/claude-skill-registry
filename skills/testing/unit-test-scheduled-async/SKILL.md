---
name: unit-test-scheduled-async
description: Unit tests for scheduled and async tasks using @Scheduled and @Async. Mock task execution and timing. Use when validating asynchronous operations and scheduling behavior.
category: testing
tags: [junit-5, scheduled, async, concurrency, completablefuture]
version: 1.0.1
---

# Unit Testing @Scheduled and @Async Methods

Test scheduled tasks and async methods using JUnit 5 without running the actual scheduler. Verify execution logic, timing, and asynchronous behavior.

## When to Use This Skill

Use this skill when:
- Testing @Scheduled method logic
- Testing @Async method behavior
- Verifying CompletableFuture results
- Testing async error handling
- Want fast tests without actual scheduling
- Testing background task logic in isolation

## Setup: Async/Scheduled Testing

### Maven
```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter</artifactId>
</dependency>
<dependency>
  <groupId>org.junit.jupiter</groupId>
  <artifactId>junit-jupiter</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.awaitility</groupId>
  <artifactId>awaitility</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.assertj</groupId>
  <artifactId>assertj-core</artifactId>
  <scope>test</scope>
</dependency>
```

### Gradle
```kotlin
dependencies {
  implementation("org.springframework.boot:spring-boot-starter")
  testImplementation("org.junit.jupiter:junit-jupiter")
  testImplementation("org.awaitility:awaitility")
  testImplementation("org.assertj:assertj-core")
}
```

## Testing @Async Methods

### Basic Async Testing with CompletableFuture

```java
// Service with async methods
@Service
public class EmailService {

  @Async
  public CompletableFuture<Boolean> sendEmailAsync(String to, String subject) {
    return CompletableFuture.supplyAsync(() -> {
      // Simulate email sending
      System.out.println("Sending email to " + to);
      return true;
    });
  }

  @Async
  public void notifyUser(String userId) {
    System.out.println("Notifying user: " + userId);
  }
}

// Unit test
import java.util.concurrent.CompletableFuture;
import static org.assertj.core.api.Assertions.*;

class EmailServiceAsyncTest {

  @Test
  void shouldReturnCompletedFutureWhenSendingEmail() throws Exception {
    EmailService service = new EmailService();

    CompletableFuture<Boolean> result = service.sendEmailAsync("test@example.com", "Hello");

    Boolean success = result.get(); // Wait for completion
    assertThat(success).isTrue();
  }

  @Test
  void shouldCompleteWithinTimeout() {
    EmailService service = new EmailService();

    CompletableFuture<Boolean> result = service.sendEmailAsync("test@example.com", "Hello");

    assertThat(result)
      .isCompletedWithValue(true);
  }
}
```

## Testing Async with Mocked Dependencies

### Async Service with Dependencies

```java
@Service
public class UserNotificationService {

  private final EmailService emailService;
  private final SmsService smsService;

  public UserNotificationService(EmailService emailService, SmsService smsService) {
    this.emailService = emailService;
    this.smsService = smsService;
  }

  @Async
  public CompletableFuture<String> notifyUserAsync(String userId) {
    return CompletableFuture.supplyAsync(() -> {
      emailService.send(userId);
      smsService.send(userId);
      return "Notification sent";
    });
  }
}

// Unit test
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class UserNotificationServiceAsyncTest {

  @Mock
  private EmailService emailService;

  @Mock
  private SmsService smsService;

  @InjectMocks
  private UserNotificationService notificationService;

  @Test
  void shouldNotifyUserAsynchronously() throws Exception {
    CompletableFuture<String> result = notificationService.notifyUserAsync("user123");

    String message = result.get();
    assertThat(message).isEqualTo("Notification sent");

    verify(emailService).send("user123");
    verify(smsService).send("user123");
  }

  @Test
  void shouldHandleAsyncExceptionGracefully() {
    doThrow(new RuntimeException("Email service failed"))
      .when(emailService).send(any());

    CompletableFuture<String> result = notificationService.notifyUserAsync("user123");

    assertThatThrownBy(result::get)
      .isInstanceOf(ExecutionException.class)
      .hasCauseInstanceOf(RuntimeException.class);
  }
}
```

## Testing @Scheduled Methods

### Mock Task Execution

```java
// Scheduled task
@Component
public class DataRefreshTask {

  private final DataRepository dataRepository;

  public DataRefreshTask(DataRepository dataRepository) {
    this.dataRepository = dataRepository;
  }

  @Scheduled(fixedDelay = 60000)
  public void refreshCache() {
    List<Data> data = dataRepository.findAll();
    // Update cache
  }

  @Scheduled(cron = "0 0 * * * *") // Every hour
  public void cleanupOldData() {
    dataRepository.deleteOldData(LocalDateTime.now().minusDays(30));
  }
}

// Unit test - test logic without actual scheduling
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class DataRefreshTaskTest {

  @Mock
  private DataRepository dataRepository;

  @InjectMocks
  private DataRefreshTask dataRefreshTask;

  @Test
  void shouldRefreshCacheFromRepository() {
    List<Data> expectedData = List.of(new Data(1L, "item1"));
    when(dataRepository.findAll()).thenReturn(expectedData);

    dataRefreshTask.refreshCache(); // Call method directly

    verify(dataRepository).findAll();
  }

  @Test
  void shouldCleanupOldData() {
    LocalDateTime cutoffDate = LocalDateTime.now().minusDays(30);

    dataRefreshTask.cleanupOldData();

    verify(dataRepository).deleteOldData(any(LocalDateTime.class));
  }
}
```

## Testing Async with Awaility

### Wait for Async Completion

```java
import org.awaitility.Awaitility;
import java.util.concurrent.atomic.AtomicInteger;

@Service
public class BackgroundWorker {

  private final AtomicInteger processedCount = new AtomicInteger(0);

  @Async
  public void processItems(List<String> items) {
    items.forEach(item -> {
      // Process item
      processedCount.incrementAndGet();
    });
  }

  public int getProcessedCount() {
    return processedCount.get();
  }
}

class AwaitilityAsyncTest {

  @Test
  void shouldProcessAllItemsAsynchronously() {
    BackgroundWorker worker = new BackgroundWorker();
    List<String> items = List.of("item1", "item2", "item3");

    worker.processItems(items);

    // Wait for async operation to complete (up to 5 seconds)
    Awaitility.await()
      .atMost(Duration.ofSeconds(5))
      .pollInterval(Duration.ofMillis(100))
      .untilAsserted(() -> {
        assertThat(worker.getProcessedCount()).isEqualTo(3);
      });
  }

  @Test
  void shouldTimeoutWhenProcessingTakesTooLong() {
    BackgroundWorker worker = new BackgroundWorker();
    List<String> items = List.of("item1", "item2", "item3");

    worker.processItems(items);

    assertThatThrownBy(() -> 
      Awaitility.await()
        .atMost(Duration.ofMillis(100))
        .until(() -> worker.getProcessedCount() == 10)
    ).isInstanceOf(ConditionTimeoutException.class);
  }
}
```

## Testing Async Error Handling

### Handle Exceptions in Async Methods

```java
@Service
public class DataProcessingService {

  @Async
  public CompletableFuture<Boolean> processDataAsync(String data) {
    return CompletableFuture.supplyAsync(() -> {
      if (data == null || data.isEmpty()) {
        throw new IllegalArgumentException("Data cannot be empty");
      }
      // Process data
      return true;
    });
  }

  @Async
  public CompletableFuture<String> safeFetchData(String id) {
    return CompletableFuture.supplyAsync(() -> {
      try {
        return fetchData(id);
      } catch (Exception e) {
        return "Error: " + e.getMessage();
      }
    });
  }
}

class AsyncErrorHandlingTest {

  @Test
  void shouldPropagateExceptionFromAsyncMethod() {
    DataProcessingService service = new DataProcessingService();

    CompletableFuture<Boolean> result = service.processDataAsync(null);

    assertThatThrownBy(result::get)
      .isInstanceOf(ExecutionException.class)
      .hasCauseInstanceOf(IllegalArgumentException.class)
      .hasMessageContaining("Data cannot be empty");
  }

  @Test
  void shouldHandleExceptionGracefullyWithFallback() throws Exception {
    DataProcessingService service = new DataProcessingService();

    CompletableFuture<String> result = service.safeFetchData("invalid");

    String message = result.get();
    assertThat(message).startsWith("Error:");
  }
}
```

## Testing Scheduled Task Timing

### Test Schedule Configuration

```java
@Component
public class HealthCheckTask {

  private final HealthCheckService healthCheckService;
  private int executionCount = 0;

  public HealthCheckTask(HealthCheckService healthCheckService) {
    this.healthCheckService = healthCheckService;
  }

  @Scheduled(fixedRate = 5000) // Every 5 seconds
  public void checkHealth() {
    executionCount++;
    healthCheckService.check();
  }

  public int getExecutionCount() {
    return executionCount;
  }
}

class ScheduledTaskTimingTest {

  @Test
  void shouldExecuteTaskMultipleTimes() {
    HealthCheckService mockService = mock(HealthCheckService.class);
    HealthCheckTask task = new HealthCheckTask(mockService);

    // Execute manually multiple times
    task.checkHealth();
    task.checkHealth();
    task.checkHealth();

    assertThat(task.getExecutionCount()).isEqualTo(3);
    verify(mockService, times(3)).check();
  }
}
```

## Best Practices

- **Test async method logic directly** without Spring async executor
- **Use CompletableFuture.get()** to wait for results in tests
- **Mock dependencies** that async methods use
- **Test error paths** for async operations
- **Use Awaitility** when testing actual async behavior is needed
- **Mock scheduled tasks** by calling methods directly in tests
- **Verify task execution count** for testing scheduling logic

## Common Pitfalls

- Testing with actual @Async executor (use direct method calls instead)
- Not waiting for CompletableFuture completion in tests
- Forgetting to test exception handling in async methods
- Not mocking dependencies that async methods call
- Trying to test actual scheduling timing (test logic instead)

## Troubleshooting

**CompletableFuture hangs in test**: Ensure methods complete or set timeout with `.get(timeout, unit)`.

**Async method not executing**: Call method directly instead of relying on @Async in tests.

**Awaitility timeout**: Increase timeout duration or reduce polling interval.

## References

- [Spring @Async Documentation](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/scheduling/annotation/Async.html)
- [Spring @Scheduled Documentation](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/scheduling/annotation/Scheduled.html)
- [Awaitility Testing Library](https://github.com/awaitility/awaitility)
- [CompletableFuture API](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletableFuture.html)
