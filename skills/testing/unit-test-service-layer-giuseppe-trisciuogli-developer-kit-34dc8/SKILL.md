---
name: unit-test-service-layer
description: Unit tests for service layer with Mockito. Test business logic in isolation by mocking dependencies. Use when validating service behaviors and business logic without database or external services.
category: testing
tags: [junit-5, mockito, unit-testing, service-layer, business-logic]
version: 1.0.1
---

# Unit Testing Service Layer with Mockito

Test @Service annotated classes by mocking all injected dependencies. Focus on business logic validation without starting the Spring container.

## When to Use This Skill

Use this skill when:
- Testing business logic in @Service classes
- Mocking repository and external client dependencies
- Verifying service interactions with mocked collaborators
- Testing complex workflows and orchestration logic
- Want fast, isolated unit tests (no database, no API calls)
- Testing error handling and edge cases in services

## Setup with Mockito and JUnit 5

### Maven
```xml
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
  <groupId>org.mockito</groupId>
  <artifactId>mockito-junit-jupiter</artifactId>
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
  testImplementation("org.junit.jupiter:junit-jupiter")
  testImplementation("org.mockito:mockito-core")
  testImplementation("org.mockito:mockito-junit-jupiter")
  testImplementation("org.assertj:assertj-core")
}
```

## Basic Pattern: Service with Mocked Dependencies

### Single Dependency

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.assertj.core.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

  @Mock
  private UserRepository userRepository;

  @InjectMocks
  private UserService userService;

  @Test
  void shouldReturnAllUsers() {
    // Arrange
    List<User> expectedUsers = List.of(
      new User(1L, "Alice"),
      new User(2L, "Bob")
    );
    when(userRepository.findAll()).thenReturn(expectedUsers);

    // Act
    List<User> result = userService.getAllUsers();

    // Assert
    assertThat(result).hasSize(2);
    assertThat(result).containsExactly(
      new User(1L, "Alice"),
      new User(2L, "Bob")
    );
    verify(userRepository, times(1)).findAll();
  }
}
```

### Multiple Dependencies

```java
@ExtendWith(MockitoExtension.class)
class UserEnrichmentServiceTest {

  @Mock
  private UserRepository userRepository;

  @Mock
  private EmailService emailService;

  @Mock
  private AnalyticsClient analyticsClient;

  @InjectMocks
  private UserEnrichmentService enrichmentService;

  @Test
  void shouldCreateUserAndSendWelcomeEmail() {
    User newUser = new User(1L, "Alice", "alice@example.com");
    when(userRepository.save(any(User.class))).thenReturn(newUser);
    doNothing().when(emailService).sendWelcomeEmail(newUser.getEmail());

    User result = enrichmentService.registerNewUser("Alice", "alice@example.com");

    assertThat(result.getId()).isEqualTo(1L);
    assertThat(result.getName()).isEqualTo("Alice");
    
    verify(userRepository).save(any(User.class));
    verify(emailService).sendWelcomeEmail("alice@example.com");
    verify(analyticsClient, never()).trackUserRegistration(any());
  }
}
```

## Testing Exception Handling

### Service Throws Expected Exception

```java
@Test
void shouldThrowExceptionWhenUserNotFound() {
  when(userRepository.findById(999L))
    .thenThrow(new UserNotFoundException("User not found"));

  assertThatThrownBy(() -> userService.getUserDetails(999L))
    .isInstanceOf(UserNotFoundException.class)
    .hasMessageContaining("User not found");

  verify(userRepository).findById(999L);
}

@Test
void shouldRethrowRepositoryException() {
  when(userRepository.findAll())
    .thenThrow(new DataAccessException("Database connection failed"));

  assertThatThrownBy(() -> userService.getAllUsers())
    .isInstanceOf(DataAccessException.class)
    .hasMessageContaining("Database connection failed");
}
```

## Testing Complex Workflows

### Multiple Service Method Calls

```java
@Test
void shouldTransferMoneyBetweenAccounts() {
  Account fromAccount = new Account(1L, 1000.0);
  Account toAccount = new Account(2L, 500.0);

  when(accountRepository.findById(1L)).thenReturn(Optional.of(fromAccount));
  when(accountRepository.findById(2L)).thenReturn(Optional.of(toAccount));
  when(accountRepository.save(any(Account.class)))
    .thenAnswer(invocation -> invocation.getArgument(0));

  moneyTransferService.transfer(1L, 2L, 200.0);

  // Verify both accounts were updated
  verify(accountRepository, times(2)).save(any(Account.class));
  assertThat(fromAccount.getBalance()).isEqualTo(800.0);
  assertThat(toAccount.getBalance()).isEqualTo(700.0);
}
```

## Argument Capturing and Verification

### Capture Arguments Passed to Mock

```java
import org.mockito.ArgumentCaptor;

@Test
void shouldCaptureUserDataWhenSaving() {
  ArgumentCaptor<User> userCaptor = ArgumentCaptor.forClass(User.class);
  when(userRepository.save(any(User.class)))
    .thenAnswer(invocation -> invocation.getArgument(0));

  userService.createUser("Alice", "alice@example.com");

  verify(userRepository).save(userCaptor.capture());
  User capturedUser = userCaptor.getValue();
  
  assertThat(capturedUser.getName()).isEqualTo("Alice");
  assertThat(capturedUser.getEmail()).isEqualTo("alice@example.com");
}

@Test
void shouldCaptureMultipleArgumentsAcrossMultipleCalls() {
  ArgumentCaptor<User> userCaptor = ArgumentCaptor.forClass(User.class);

  userService.createUser("Alice", "alice@example.com");
  userService.createUser("Bob", "bob@example.com");

  verify(userRepository, times(2)).save(userCaptor.capture());
  
  List<User> capturedUsers = userCaptor.getAllValues();
  assertThat(capturedUsers).hasSize(2);
  assertThat(capturedUsers.get(0).getName()).isEqualTo("Alice");
  assertThat(capturedUsers.get(1).getName()).isEqualTo("Bob");
}
```

## Verification Patterns

### Verify Call Order and Frequency

```java
import org.mockito.InOrder;

@Test
void shouldCallMethodsInCorrectOrder() {
  InOrder inOrder = inOrder(userRepository, emailService);

  userService.registerNewUser("Alice", "alice@example.com");

  inOrder.verify(userRepository).save(any(User.class));
  inOrder.verify(emailService).sendWelcomeEmail(any());
}

@Test
void shouldCallMethodExactlyOnce() {
  userService.getUserDetails(1L);

  verify(userRepository, times(1)).findById(1L);
  verify(userRepository, never()).findAll();
}
```

## Testing Async/Reactive Services

### Service with CompletableFuture

```java
@Test
void shouldReturnCompletableFutureWhenFetchingAsyncData() {
  List<User> users = List.of(new User(1L, "Alice"));
  when(userRepository.findAllAsync())
    .thenReturn(CompletableFuture.completedFuture(users));

  CompletableFuture<List<User>> result = userService.getAllUsersAsync();

  assertThat(result).isCompletedWithValue(users);
}
```

## Best Practices

- **Use @ExtendWith(MockitoExtension.class)** for JUnit 5 integration
- **Construct service manually** instead of using reflection when possible
- **Mock only direct dependencies** of the service under test
- **Verify interactions** to ensure correct collaboration
- **Use descriptive variable names**: `expectedUser`, `actualUser`, `captor`
- **Test one behavior per test method** - keep tests focused
- **Avoid testing framework code** - focus on business logic

## Common Patterns

**Partial Mock with Spy**:
```java
@Spy
@InjectMocks
private UserService userService; // Real instance, but can stub some methods

@Test
void shouldUseRealMethodButMockDependency() {
  when(userRepository.findById(any())).thenReturn(Optional.of(new User()));
  // Calls real userService methods but userRepository is mocked
}
```

**Constructor Injection for Testing**:
```java
// In your service (production code)
public class UserService {
  private final UserRepository userRepository;
  
  public UserService(UserRepository userRepository) {
    this.repository = userRepository;
  }
}

// In your test - can inject mocks directly
@Test
void test() {
  UserRepository mockRepo = mock(UserRepository.class);
  UserService service = new UserService(mockRepo);
}
```

## Troubleshooting

**UnfinishedStubbingException**: Ensure all `when()` calls are completed with `thenReturn()`, `thenThrow()`, or `thenAnswer()`.

**UnnecessaryStubbingException**: Remove unused stub definitions. Use `@ExtendWith(MockitoExtension.class)` with `MockitoExtension.LENIENT` if you intentionally have unused stubs.

**NullPointerException in test**: Verify `@InjectMocks` correctly injects all mocked dependencies into the service constructor.

## References

- [Mockito Documentation](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [AssertJ Assertions](https://assertj.github.io/assertj-core-features-highlight.html)
