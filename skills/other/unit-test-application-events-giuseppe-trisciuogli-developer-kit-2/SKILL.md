---
name: unit-test-application-events
description: Provides patterns for testing Spring application events (ApplicationEvent) with @EventListener and ApplicationEventPublisher. Handles event publishing, listening, and async event handling in Spring Boot applications. Use when validating event-driven workflows in your Spring Boot services.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Unit Testing Application Events

## Overview

This skill provides comprehensive patterns for testing Spring ApplicationEvent publishers and event listeners using JUnit 5. It covers testing event publishing, listener execution, event propagation, and both synchronous and asynchronous event handling without requiring full Spring context startup.

## When to Use

Use this skill when:
- Testing ApplicationEventPublisher event publishing
- Testing @EventListener method invocation
- Verifying event listener logic and side effects
- Testing event propagation through listeners
- Want fast event-driven architecture tests
- Testing both synchronous and asynchronous event handling

## Instructions

1. **Add required dependencies**: Include spring-boot-starter, JUnit 5, Mockito, and AssertJ in your project
2. **Mock the ApplicationEventPublisher**: In service tests, use `@Mock` to mock the event publisher
3. **Use ArgumentCaptor**: Capture published events to verify their content using `ArgumentCaptor.forClass(EventType.class)`
4. **Test listener side effects**: Invoke listener methods directly and verify their effects on mocked dependencies
5. **Test event data integrity**: Always verify that the captured event contains the correct data
6. **Handle async events**: For @Async listeners, use Thread.sleep() or Awaitility to wait for completion
7. **Test error scenarios**: Verify exception handling in both publishers and listeners

## Examples

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
  <groupId>org.mockito</groupId>
  <artifactId>mockito-core</artifactId>
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
  testImplementation("org.mockito:mockito-core")
  testImplementation("org.assertj:assertj-core")
}
```

## Basic Pattern: Event Publishing and Listening

### Custom Event and Publisher

```java
// Custom application event
public class UserCreatedEvent extends ApplicationEvent {
  private final User user;

  public UserCreatedEvent(Object source, User user) {
    super(source);
    this.user = user;
  }

  public User getUser() {
    return user;
  }
}

// Service that publishes events
@Service
public class UserService {

  private final ApplicationEventPublisher eventPublisher;
  private final UserRepository userRepository;

  public UserService(ApplicationEventPublisher eventPublisher, UserRepository userRepository) {
    this.eventPublisher = eventPublisher;
    this.userRepository = userRepository;
  }

  public User createUser(String name, String email) {
    User user = new User(name, email);
    User savedUser = userRepository.save(user);
    
    eventPublisher.publishEvent(new UserCreatedEvent(this, savedUser));
    
    return savedUser;
  }
}

// Unit test
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserServiceEventTest {

  @Mock
  private ApplicationEventPublisher eventPublisher;

  @Mock
  private UserRepository userRepository;

  @InjectMocks
  private UserService userService;

  @Test
  void shouldPublishUserCreatedEvent() {
    User newUser = new User(1L, "Alice", "alice@example.com");
    when(userRepository.save(any(User.class))).thenReturn(newUser);

    ArgumentCaptor<UserCreatedEvent> eventCaptor = ArgumentCaptor.forClass(UserCreatedEvent.class);

    userService.createUser("Alice", "alice@example.com");

    verify(eventPublisher).publishEvent(eventCaptor.capture());
    
    UserCreatedEvent capturedEvent = eventCaptor.getValue();
    assertThat(capturedEvent.getUser()).isEqualTo(newUser);
  }
}
```

## Testing Event Listeners

### @EventListener Annotation

```java
// Event listener
@Component
public class UserEventListener {

  private final EmailService emailService;

  public UserEventListener(EmailService emailService) {
    this.emailService = emailService;
  }

  @EventListener
  public void onUserCreated(UserCreatedEvent event) {
    User user = event.getUser();
    emailService.sendWelcomeEmail(user.getEmail());
  }
}

// Unit test for listener
class UserEventListenerTest {

  @Test
  void shouldSendWelcomeEmailWhenUserCreated() {
    EmailService emailService = mock(EmailService.class);
    UserEventListener listener = new UserEventListener(emailService);

    User newUser = new User(1L, "Alice", "alice@example.com");
    UserCreatedEvent event = new UserCreatedEvent(this, newUser);

    listener.onUserCreated(event);

    verify(emailService).sendWelcomeEmail("alice@example.com");
  }

  @Test
  void shouldNotThrowExceptionWhenEmailServiceFails() {
    EmailService emailService = mock(EmailService.class);
    doThrow(new RuntimeException("Email service down"))
      .when(emailService).sendWelcomeEmail(any());

    UserEventListener listener = new UserEventListener(emailService);
    User newUser = new User(1L, "Alice", "alice@example.com");
    UserCreatedEvent event = new UserCreatedEvent(this, newUser);

    // Should handle exception gracefully
    assertThatCode(() -> listener.onUserCreated(event))
      .doesNotThrowAnyException();
  }
}
```

## Testing Multiple Listeners

### Event Propagation

```java
class UserCreatedEvent extends ApplicationEvent {
  private final User user;
  private final List<String> notifications = new ArrayList<>();

  public UserCreatedEvent(Object source, User user) {
    super(source);
    this.user = user;
  }

  public void addNotification(String notification) {
    notifications.add(notification);
  }

  public List<String> getNotifications() {
    return notifications;
  }
}

class MultiListenerTest {

  @Test
  void shouldNotifyMultipleListenersSequentially() {
    EmailService emailService = mock(EmailService.class);
    NotificationService notificationService = mock(NotificationService.class);
    AnalyticsService analyticsService = mock(AnalyticsService.class);

    UserEventListener emailListener = new UserEventListener(emailService);
    UserEventListener notificationListener = new UserEventListener(notificationService);
    UserEventListener analyticsListener = new UserEventListener(analyticsService);

    User user = new User(1L, "Alice", "alice@example.com");
    UserCreatedEvent event = new UserCreatedEvent(this, user);

    emailListener.onUserCreated(event);
    notificationListener.onUserCreated(event);
    analyticsListener.onUserCreated(event);

    verify(emailService).send(any());
    verify(notificationService).notify(any());
    verify(analyticsService).track(any());
  }
}
```

## Testing Conditional Event Listeners

### @EventListener with Condition

```java
@Component
public class ConditionalEventListener {

  @EventListener(condition = "#event.user.age > 18")
  public void onAdultUserCreated(UserCreatedEvent event) {
    // Handle adult user
  }
}

class ConditionalListenerTest {

  @Test
  void shouldProcessEventWhenConditionMatches() {
    // Test logic for matching condition
  }

  @Test
  void shouldSkipEventWhenConditionDoesNotMatch() {
    // Test logic for non-matching condition
  }
}
```

## Testing Async Event Listeners

### @Async with @EventListener

```java
@Component
public class AsyncEventListener {

  private final SlowService slowService;

  @EventListener
  @Async
  public void onUserCreatedAsync(UserCreatedEvent event) {
    slowService.processUser(event.getUser());
  }
}

class AsyncEventListenerTest {

  @Test
  void shouldProcessEventAsynchronously() throws Exception {
    SlowService slowService = mock(SlowService.class);
    AsyncEventListener listener = new AsyncEventListener(slowService);

    User user = new User(1L, "Alice", "alice@example.com");
    UserCreatedEvent event = new UserCreatedEvent(this, user);

    listener.onUserCreatedAsync(event);

    // Event processed asynchronously
    Thread.sleep(100); // Wait for async completion
    verify(slowService).processUser(user);
  }
}
```

## Best Practices

- **Mock ApplicationEventPublisher** in unit tests
- **Capture published events** using ArgumentCaptor
- **Test listener side effects** explicitly
- **Test error handling** in listeners
- **Keep event listeners focused** on single responsibility
- **Verify event data integrity** when capturing
- **Test both sync and async** event processing

## Common Pitfalls

- Testing actual event publishing without mocking publisher
- Not verifying listener invocation
- Not capturing event details
- Testing listener registration instead of logic
- Not handling listener exceptions

## Constraints and Warnings

- **Do not test Spring framework behavior**: Focus on your event logic, not Spring's event publishing mechanism
- **Avoid Thread.sleep() in production code**: Use it only in test scenarios for async event verification
- **Event listeners should be idempotent**: Design listeners to handle duplicate events gracefully
- **Beware of event ordering**: Spring does not guarantee listener execution order without @Order annotation
- **Test event serialization**: If events are sent across JVM boundaries, test serialization/deserialization
- **Memory considerations**: Be cautious with event-driven architecture in long-running processes; events can accumulate

## Best Practices

**Event not being captured**: Verify ArgumentCaptor type matches event class.

**Listener not invoked**: Ensure event is actually published and listener is registered.

**Async listener timing issues**: Use Thread.sleep() or Awaitility to wait for completion.

## References

- [Spring ApplicationEvent](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/ApplicationEvent.html)
- [Spring ApplicationEventPublisher](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/ApplicationEventPublisher.html)
- [@EventListener Documentation](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/event/EventListener.html)
