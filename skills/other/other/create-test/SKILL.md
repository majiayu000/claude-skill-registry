---
name: create-test
description: Analyze a Java class and scaffold a JUnit 5 test with proper structure and assertions
---

# Create Test Skill

Analyze a Java class, identify testable methods, and scaffold a comprehensive JUnit 5 test class.

## When to Use

- User asks to "write tests for", "test", or "add tests to" a class
- You've implemented a new class and need to verify it
- Improving test coverage for existing code

## Process

### Step 1: Analyze the Source Class

Read the source class and identify:

- Class name and package
- Dependencies (for mocking)
- Public methods to test
- Constructor parameters

```bash
# Find the class
find src/main -name "UserService.java" | head -1
```

### Step 2: Determine Test Type

| Source Class Type | Test Approach                      |
| ----------------- | ---------------------------------- |
| Service           | Unit test with mocked dependencies |
| Controller        | MockMvc integration test           |
| Repository        | @DataJpaTest slice test            |
| Utility           | Pure unit test                     |
| Entity/DTO        | Unit test for validation           |

### Step 3: Create Test Class

Test file location mirrors source:

```
src/main/java/com/example/service/UserService.java
src/test/java/com/example/service/UserServiceTest.java
```

### Step 4: Run the Test

```bash
./mvnw -Dtest=UserServiceTest test -B
```

## Test Templates

### Service Test (with Mocks)

```java
package com.example.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("UserService")
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Nested
    @DisplayName("findById")
    class FindById {

        @Test
        @DisplayName("returns user when exists")
        void returnsUserWhenExists() {
            // Given
            User user = new User(1L, "Test User", "test@example.com");
            when(userRepository.findById(1L)).thenReturn(Optional.of(user));

            // When
            Optional<UserDto> result = userService.findById(1L);

            // Then
            assertThat(result).isPresent();
            assertThat(result.get().name()).isEqualTo("Test User");
            verify(userRepository).findById(1L);
        }

        @Test
        @DisplayName("returns empty when not found")
        void returnsEmptyWhenNotFound() {
            // Given
            when(userRepository.findById(anyLong())).thenReturn(Optional.empty());

            // When
            Optional<UserDto> result = userService.findById(99L);

            // Then
            assertThat(result).isEmpty();
        }
    }

    @Nested
    @DisplayName("create")
    class Create {

        @Test
        @DisplayName("creates and returns new user")
        void createsAndReturnsNewUser() {
            // Given
            CreateUserRequest request = new CreateUserRequest("New User", "new@example.com");
            User savedUser = new User(1L, "New User", "new@example.com");
            when(userRepository.save(any(User.class))).thenReturn(savedUser);

            // When
            UserDto result = userService.create(request);

            // Then
            assertThat(result.id()).isEqualTo(1L);
            assertThat(result.name()).isEqualTo("New User");
            verify(userRepository).save(any(User.class));
        }
    }
}
```

### Controller Test (MockMvc)

```java
package com.example.controller;

import com.example.service.UserService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Optional;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserController.class)
@DisplayName("UserController")
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private UserService userService;

    @Test
    @DisplayName("GET /api/users/{id} returns user when found")
    void getUserReturnsUserWhenFound() throws Exception {
        // Given
        UserDto user = new UserDto(1L, "Test", "test@example.com");
        when(userService.findById(1L)).thenReturn(Optional.of(user));

        // When/Then
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.name").value("Test"));
    }

    @Test
    @DisplayName("GET /api/users/{id} returns 404 when not found")
    void getUserReturns404WhenNotFound() throws Exception {
        // Given
        when(userService.findById(anyLong())).thenReturn(Optional.empty());

        // When/Then
        mockMvc.perform(get("/api/users/99"))
            .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("POST /api/users creates user with valid input")
    void createUserWithValidInput() throws Exception {
        // Given
        CreateUserRequest request = new CreateUserRequest("New User", "new@example.com");
        UserDto created = new UserDto(1L, "New User", "new@example.com");
        when(userService.create(any())).thenReturn(created);

        // When/Then
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1));
    }
}
```

### Repository Test (DataJpaTest)

```java
package com.example.repository;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;

import java.util.Optional;

import static org.assertj.core.api.Assertions.*;

@DataJpaTest
@DisplayName("UserRepository")
class UserRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private UserRepository userRepository;

    @Test
    @DisplayName("findByEmail returns user when exists")
    void findByEmailReturnsUserWhenExists() {
        // Given
        User user = new User();
        user.setName("Test User");
        user.setEmail("test@example.com");
        entityManager.persistAndFlush(user);

        // When
        Optional<User> found = userRepository.findByEmail("test@example.com");

        // Then
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Test User");
    }
}
```

## Test Naming Convention

Follow the pattern: `methodName_condition_expectedResult`

```java
void findById_WhenUserExists_ReturnsUser()
void create_WithInvalidEmail_ThrowsValidationException()
void delete_WhenNotFound_ReturnsNotFound()
```

## Assertions (AssertJ Preferred)

```java
// Basic assertions
assertThat(result).isNotNull();
assertThat(result.getName()).isEqualTo("expected");
assertThat(list).hasSize(3);
assertThat(list).contains(item);

// Exception assertions
assertThatThrownBy(() -> service.validate(null))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessageContaining("cannot be null");

// Optional assertions
assertThat(result).isPresent();
assertThat(result).isEmpty();
```

## Running After Creation

```bash
# Run the new test immediately
./mvnw -Dtest=UserServiceTest test -B

# Run with verbose output
./mvnw -Dtest=UserServiceTest test -B -Dsurefire.useFile=false
```

## Web Environment Notes

Always use batch mode when running tests:

```bash
# GOOD
./mvnw -Dtest=MyTest test -B

# BAD - may hang
./mvnw -Dtest=MyTest test
```
