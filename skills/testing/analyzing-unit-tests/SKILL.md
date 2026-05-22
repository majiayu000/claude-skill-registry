---
name: analyzing-unit-tests
description: Use when analyzing unit test coverage, patterns, and test code for isolated component testing
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(mkdir:*, ls:*)
  - Write(docs/unwind/**)
  - Edit(docs/unwind/**)
---

# Analyzing Unit Tests

**Output:** `docs/unwind/layers/unit-tests/` (folder with index.md + section files)

**Principles:** See `analysis-principles.md` - completeness, machine-readable, link to source, no commentary, incremental writes.

## Output Structure

```
docs/unwind/layers/unit-tests/
├── index.md           # Test summary, coverage overview
├── service-tests.md   # Service layer tests
├── domain-tests.md    # Domain/entity tests
├── utilities.md       # Test utilities, factories
└── coverage-gaps.md   # Classes without tests
```

For large codebases (50+ test files), split by domain:
```
docs/unwind/layers/unit-tests/
├── index.md
├── users-tests.md
├── orders-tests.md
└── ...
```

## Process (Incremental Writes)

**Step 1: Setup**
```bash
mkdir -p docs/unwind/layers/unit-tests/
```
Write initial `index.md`:
```markdown
# Unit Tests

## Sections
- [Service Tests](service-tests.md) - _pending_
- [Domain Tests](domain-tests.md) - _pending_
- [Test Utilities](utilities.md) - _pending_
- [Coverage Gaps](coverage-gaps.md) - _pending_

## Summary
_Analysis in progress..._
```

**Step 2: Analyze and write service-tests.md**
1. Find all service layer tests
2. Include actual test code showing what is tested
3. Write `service-tests.md` immediately
4. Update `index.md`

**Step 3: Analyze and write domain-tests.md**
1. Find all domain/entity tests
2. Write `domain-tests.md` immediately
3. Update `index.md`

**Step 4: Analyze and write utilities.md**
1. Find test utilities, factories, mocks
2. Write `utilities.md` immediately
3. Update `index.md`

**Step 5: Analyze and write coverage-gaps.md**
1. Identify classes without tests
2. Write `coverage-gaps.md` immediately
3. Update `index.md`

**Step 6: Finalize index.md**
Add coverage summary table

## Output Format

```markdown
# Unit Tests

## Configuration

[pom.xml test dependencies](https://github.com/owner/repo/blob/main/pom.xml#L50-L70)

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.9.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <version>5.0.0</version>
    <scope>test</scope>
</dependency>
```

## Test Summary

| Layer | Classes | Tested | Coverage |
|-------|---------|--------|----------|
| Service | 12 | 10 | 83% |
| Domain | 8 | 8 | 100% |
| Repository | 6 | 4 | 67% |

## Service Tests

### UserServiceTest

[UserServiceTest.java](https://github.com/owner/repo/blob/main/src/test/java/service/UserServiceTest.java)

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserService userService;

    @Test
    void createUser_success() {
        CreateUserRequest request = new CreateUserRequest("test@example.com", "password", "Test");
        when(userRepository.existsByEmail(request.email())).thenReturn(false);
        when(passwordEncoder.encode(request.password())).thenReturn("encoded");
        when(userRepository.save(any())).thenAnswer(inv -> inv.getArgument(0));

        User result = userService.createUser(request);

        assertThat(result.getEmail()).isEqualTo("test@example.com");
        verify(userRepository).save(any());
    }

    @Test
    void createUser_duplicateEmail_throws() {
        CreateUserRequest request = new CreateUserRequest("existing@example.com", "password", "Test");
        when(userRepository.existsByEmail(request.email())).thenReturn(true);

        assertThrows(DuplicateEmailException.class, () -> userService.createUser(request));
    }
}
```

Tests: `createUser_success`, `createUser_duplicateEmail_throws`, `getUser_success`, `getUser_notFound_throws`

[Continue for ALL test classes...]

## Domain Tests

### UserTest

[UserTest.java](https://github.com/owner/repo/blob/main/src/test/java/domain/UserTest.java)

```java
class UserTest {

    @Test
    void suspend_activeUser_setsSuspended() {
        User user = new User("test@example.com", "hash");
        user.setStatus(UserStatus.ACTIVE);

        user.suspend();

        assertThat(user.getStatus()).isEqualTo(UserStatus.SUSPENDED);
    }

    @Test
    void suspend_deletedUser_throws() {
        User user = new User("test@example.com", "hash");
        user.setStatus(UserStatus.DELETED);

        assertThrows(IllegalStateException.class, () -> user.suspend());
    }
}
```

## Test Utilities

### TestDataFactory

[TestDataFactory.java](https://github.com/owner/repo/blob/main/src/test/java/util/TestDataFactory.java)

```java
public class TestDataFactory {
    public static User createUser() {
        return new User("test@example.com", "encodedPassword");
    }

    public static Order createOrder(User user) {
        Order order = new Order(user);
        order.addItem(createProduct(), 2);
        return order;
    }
}
```

## Coverage Gaps

Classes without unit tests:
- `PaymentService`
- `NotificationService`
- `LegacyOrderAdapter`

## Unknowns

- [List anything unclear]
```

## Refresh Mode

If `docs/unwind/layers/unit-tests/` exists, compare current state and add `## Changes Since Last Review` section to `index.md`.
